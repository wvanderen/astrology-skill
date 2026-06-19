#!/usr/bin/env python3
"""Birth-data → chart JSON pre-processor for the astrology skill.

Converts raw birth data into a chart JSON object that conforms to
``assets/schemas/chart_input_schema.json``. The output is *geometry +
provenance only*; the skill supplies doctrine. This script is a standalone
developer tool and is NOT imported, loaded, or referenced by the interpretive
skill (``SKILL.md`` + ``references/``). See ``tools/README.md`` and
``docs/birth_to_chart_design.md`` for the boundary and licensing rationale.

Calculation engine: Swiss Ephemeris via the ``pyswisseph`` package
(dual-licensed AGPL-3.0 / Swiss Ephemeris Professional License — see
``tools/NOTICE.md``). Works out of the box with the built-in Moshier
ephemeris (no data files required); point ``--ephe-path`` / ``SWISSEPH_PATH``
at a directory of ``.se1`` files for higher precision.

USAGE (non-interactive)
-----------------------
    python tools/birth_to_chart.py \\
        --date 1990-05-21 --time 14:32 \\
        --lat 40.7128 --lon -74.0060 \\
        --tz "America/New_York" \\
        --house-system "Whole Sign" \\
        --name "Subject A" --place "Brooklyn, NY" \\
        --reading-type natal --tradition-mode blended --tone practical \\
        --validate --output chart.json

    # Feed all flags as JSON instead:
    python tools/birth_to_chart.py --input birth.json --validate

    # Drop into interactive prompts:
    python tools/birth_to_chart.py

EXIT CODES
----------
    0  success (and --validate, if requested, passed)
    2  bad/missing input or validation failure (message names the field)

See ``tools/README.md`` for install, data-file handling, and licensing.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import swisseph as swe

__version__ = "1.0.0"


# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SPEED_LUMINARY = "luminary"
SPEED_FAST = "fast"
SPEED_SLOW = "slow"
SPEED_NODE = "node"

# (display name, Swiss Ephemeris body id, speed class, default-on)
_PLANETS: list[tuple[str, int, str, bool]] = [
    ("Sun", swe.SUN, SPEED_LUMINARY, True),
    ("Moon", swe.MOON, SPEED_LUMINARY, True),
    ("Mercury", swe.MERCURY, SPEED_FAST, True),
    ("Venus", swe.VENUS, SPEED_FAST, True),
    ("Mars", swe.MARS, SPEED_FAST, True),
    ("Jupiter", swe.JUPITER, SPEED_SLOW, True),
    ("Saturn", swe.SATURN, SPEED_SLOW, True),
    ("Uranus", swe.URANUS, SPEED_SLOW, True),
    ("Neptune", swe.NEPTUNE, SPEED_SLOW, True),
    ("Pluto", swe.PLUTO, SPEED_SLOW, True),
    ("True Node", swe.TRUE_NODE, SPEED_NODE, True),
]
_EXTRA_BODIES = {
    "chiron": ("Chiron", swe.CHIRON, SPEED_SLOW),
    "lilith": ("Lilith", swe.MEAN_APOG, SPEED_SLOW),
}

# House system name → Swiss Ephemeris house letter.
HOUSE_SYSTEMS: dict[str, bytes] = {
    "Whole Sign": b"W",
    "Placidus": b"P",
    "Regiomontanus": b"R",
    "Koch": b"K",
    "Equal": b"A",
    "Campanus": b"C",
    "Porphyrius": b"O",
    "Morinus": b"M",
    "Alcabitius": b"B",
    "Topocentric": b"T",
}

# Aspects: name → (angle in degrees, is_major). Minor aspects opt-in via flag.
ASPECT_DEFS: list[tuple[str, float, bool]] = [
    ("conjunction", 0.0, True),
    ("opposition", 180.0, True),
    ("trine", 120.0, True),
    ("square", 90.0, True),
    ("sextile", 60.0, True),
    ("quincunx", 150.0, False),
    ("semisextile", 30.0, False),
]

# Per speed-class maximum orb (degrees). Pair orb = max of the two bodies'.
BODY_ORB: dict[str, float] = {
    SPEED_LUMINARY: 10.0,
    SPEED_FAST: 7.0,
    SPEED_SLOW: 8.0,
    SPEED_NODE: 5.0,
    "angle": 8.0,  # Ascendant / Midheaven when included in aspects
}
# Per-aspect orb caps (degrees). ``None`` means no cap beyond the pair orb.
ASPECT_ORB_CAP: dict[str, float | None] = {
    "conjunction": None,
    "opposition": None,
    "trine": None,
    "square": None,
    "sextile": 6.0,
    "quincunx": 3.0,
    "semisextile": 2.0,
}

EXACT_TOL_DEG = 0.05        # orb below which an aspect is reported exact
STATIONARY_SPEED = 0.01     # |daily longitude speed| at/below → "stationary"

# Valid sect confidence labels (see references/foundations/birth_time_uncertainty.md).
CONF_TIMED = "Timed"
CONF_APPROX = "Approximate"
CONF_UNKNOWN = "Unknown"
CONF_RECTIFIED = "Rectified"
_VALID_CONFIDENCE = {CONF_TIMED, CONF_APPROX, CONF_UNKNOWN, CONF_RECTIFIED}


# --------------------------------------------------------------------------- #
# Errors
# --------------------------------------------------------------------------- #

class ConfigError(ValueError):
    """A user-facing input/configuration error (exit code 2)."""


# --------------------------------------------------------------------------- #
# Small geometry / formatting helpers
# --------------------------------------------------------------------------- #

def _normalize_deg(value: float) -> float:
    """Fold any longitude into the half-open [0, 360) interval."""
    return value % 360.0


def sign_and_degree(abs_deg: float) -> tuple[str, float, float]:
    """Return (sign_name, in_sign_degree, absolute_degree) for a longitude."""
    abs_deg = _normalize_deg(abs_deg)
    index = int(abs_deg // 30) % 12
    return SIGN_NAMES[index], abs_deg - index * 30.0, abs_deg


def zodiac_position(abs_deg: float) -> dict:
    """Schema-shaped zodiac position object."""
    sign, degree, absolute = sign_and_degree(abs_deg)
    return {
        "sign": sign,
        "degree": round(degree, 4),
        "absolute_degree": round(absolute, 4),
    }


def obliquity_deg(jd: float) -> float:
    """Mean obliquity of the ecliptic (IAU 1980), degrees. Used for sect only."""
    t = (jd - 2451545.0) / 36525.0
    return (
        23.439291111
        - 0.0130041667 * t
        - 1.638889e-7 * t * t
        + 5.036111e-7 * t ** 3
    )


# --------------------------------------------------------------------------- #
# Input parsing
# --------------------------------------------------------------------------- #

_DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
_TIME_RE = re.compile(r"^([01]?\d|2[0-3]):([0-5]\d)(?::([0-5]\d))?$")
_OFFSET_RE = re.compile(r"^([+-])(\d{2}):(\d{2})(?::(\d{2}))?$")


def parse_date(value: str) -> tuple[int, int, int]:
    m = _DATE_RE.match(value.strip())
    if not m:
        raise ConfigError(f"--date must be ISO YYYY-MM-DD, got {value!r}")
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    try:
        datetime(y, mo, d)
    except ValueError as exc:
        raise ConfigError(f"--date is not a valid calendar date: {value!r} ({exc})")
    return y, mo, d


def parse_time(value: str) -> tuple[int, int, int]:
    m = _TIME_RE.match(value.strip())
    if not m:
        raise ConfigError(
            f"--time must be HH:MM or HH:MM:SS (24h), got {value!r}"
        )
    return int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)


def resolve_timezone(tz_spec: str | None, use_lmt: bool, lon: float | None):
    """Return (tzinfo, label, kind). Never guesses; missing → ConfigError.

    kind is one of ``"iana"``, ``"offset"``, ``"lmt"`` for provenance notes.
    """
    if use_lmt:
        if lon is None:
            raise ConfigError("--lmt requires --lon (to derive the offset).")
        off_seconds = round((lon / 15.0) * 3600.0)
        return timezone(timedelta(seconds=off_seconds)), "LMT", "lmt"
    if not tz_spec:
        raise ConfigError(
            "No timezone supplied. Pass --tz (IANA name like "
            "'America/New_York' or a fixed offset like '+05:30') or --lmt. "
            "Birth-time uncertainty must be made explicit, never guessed."
        )
    # IANA first.
    try:
        return ZoneInfo(tz_spec), tz_spec, "iana"
    except (ZoneInfoNotFoundError, ValueError):
        pass
    m = _OFFSET_RE.match(tz_spec)
    if not m:
        raise ConfigError(
            f"--tz {tz_spec!r} is neither a known IANA zone nor a fixed "
            f"offset like '+05:30'."
        )
    sign = 1 if m.group(1) == "+" else -1
    hh = int(m.group(2))
    mm = int(m.group(3))
    ss = int(m.group(4) or 0)
    off = sign * (hh * 3600 + mm * 60 + ss)
    return timezone(timedelta(seconds=off)), tz_spec, "offset"


def wallclock_to_ut(
    y: int, mo: int, d: int, hh: int, mm: int, ss: int, tz
) -> datetime:
    """Convert a wall-clock instant in ``tz`` to a UTC datetime."""
    try:
        local = datetime(y, mo, d, hh, mm, ss, tzinfo=tz)
    except ValueError as exc:
        raise ConfigError(f"Invalid date/time combination: {exc}")
    # Non-existent or ambiguous wall-clock instants (DST folds) are resolved
    # by the tzinfo; we surface the resolved UTC rather than guessing.
    return local.astimezone(timezone.utc)


def ut_to_jd(ut: datetime) -> float:
    """UTC datetime → Julian Day (UT) for Swiss Ephemeris."""
    frac = (
        ut.hour
        + ut.minute / 60.0
        + (ut.second + ut.microsecond / 1e6) / 3600.0
    )
    return swe.julday(ut.year, ut.month, ut.day, frac)


# --------------------------------------------------------------------------- #
# Core computation
# --------------------------------------------------------------------------- #

def _flags(sidereal: bool, topo: bool) -> int:
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    if sidereal:
        flags |= swe.FLG_SIDEREAL
    if topo:
        flags |= swe.FLG_TOPOCTR
    return flags


def compute_positions(
    jd: float, body_list: list[tuple[str, int, str]], flags: int,
    topocentric_moon: bool, elevation: float | None,
) -> tuple[list[dict], str]:
    """Return (placements, ephemeris_mode_label).

    Each placement carries body, sign, degree, absolute_degree, motion,
    condition [], dignity []. House assignment is added later when a time is
    known. ``topocentric_moon`` applies parallax to the Moon only.
    """
    placements: list[dict] = []
    mode_label = "Moshier (built-in)"
    if topocentric_moon and elevation is not None:
        swe.set_topo(0.0, 0.0, elevation)  # lon/lat unused; elevation only
    for name, pid, _speed_class in body_list:
        use_topo = topocentric_moon and name == "Moon"
        call_flags = flags | (swe.FLG_TOPOCTR if use_topo else 0)
        try:
            result, retflag = swe.calc_ut(jd, pid, call_flags)
        except swe.Error as exc:
            if ".se1" in str(exc) or "not found" in str(exc):
                raise ConfigError(
                    f"Cannot compute {name!r} with the built-in Moshier "
                    f"ephemeris: this body requires Swiss Ephemeris data "
                    f"files (.se1). Download them from Astrodienst and pass "
                    f"--ephe-path <dir> (or set SWISSEPH_PATH). "
                    f"({exc})")
            raise
        lon, _lat, _dist, lon_speed = result[0], result[1], result[2], result[3]
        mode_label = _ephe_mode_label(retflag)
        sign, degree, absolute = sign_and_degree(lon)
        placements.append({
            "body": name,
            "sign": sign,
            "degree": round(degree, 4),
            "absolute_degree": round(absolute, 4),
            "motion": _motion_from_speed(lon_speed),
            "speed_deg_per_day": round(lon_speed, 6),  # provenance extra-prop
            "condition": [],
            "dignity": [],
        })
    if topocentric_moon:
        swe.set_topo(0.0, 0.0, 0.0)
    return placements, mode_label


def _ephe_mode_label(retflag: int) -> str:
    if retflag & swe.FLG_MOSEPH:
        return "Moshier (built-in)"
    if retflag & swe.FLG_SWIEPH:
        return "Swiss Ephemeris .se1"
    return "unknown"


def _motion_from_speed(speed: float) -> str:
    if abs(speed) < STATIONARY_SPEED:
        return "stationary"
    return "retrograde" if speed < 0 else "direct"


def compute_angles_and_houses(
    jd: float, lat: float, lon: float, hsys_letter: bytes, sidereal: bool,
) -> tuple[dict, dict, list[dict], float, tuple[float, ...]]:
    """Return (ascendant, midheaven, house_cusps, armc_deg, raw_cusps).

    ``swe.houses`` is tropical; for a sidereal chart we use ``houses_ex`` with
    the ``FLG_SIDEREAL`` flag so the angles/cusps carry the ayanamsa.
    """
    if sidereal:
        cusps, ascmc = swe.houses_ex(
            jd, lat, lon, hsys_letter, swe.FLG_SIDEREAL)
    else:
        cusps, ascmc = swe.houses(jd, lat, lon, hsys_letter)
    asc = zodiac_position(ascmc[0])
    mc = zodiac_position(ascmc[1])
    armc = ascmc[2]
    house_cusps = []
    for i, cusp_lon in enumerate(cusps, start=1):
        pos = zodiac_position(cusp_lon)
        house_cusps.append({"house": i, **pos})
    return asc, mc, house_cusps, armc, cusps


def assign_houses(placements: list[dict], cusps: tuple[float, ...]) -> None:
    """Mutate placements in place, setting ``house`` by cusp-interval membership."""
    n = len(cusps)
    for p in placements:
        lon = p["absolute_degree"]
        house = _house_of(lon, cusps, n)
        p["house"] = house


def _house_of(lon: float, cusps: tuple[float, ...], n: int) -> int:
    for i in range(n):
        c0 = cusps[i]
        c1 = cusps[(i + 1) % n]
        span = (c1 - c0) % 360.0
        off = (lon - c0) % 360.0
        if off < span:
            return i + 1
    return n


def sun_altitude(jd: float, sun_lon: float, lat: float, armc_deg: float) -> float:
    """Sun altitude in degrees. ARMC == local sidereal time in degrees."""
    eps = math.radians(obliquity_deg(jd))
    lam = math.radians(_normalize_deg(sun_lon))
    beta = 0.0
    ra = math.atan2(
        math.sin(lam) * math.cos(eps) - math.tan(beta) * math.sin(eps),
        math.cos(lam),
    )
    ra_deg = math.degrees(ra) % 360.0
    dec = math.asin(
        math.sin(beta) * math.cos(eps)
        + math.cos(beta) * math.sin(eps) * math.sin(lam)
    )
    phi = math.radians(lat)
    ha = math.radians((armc_deg - ra_deg) % 360.0)
    alt = math.asin(
        math.sin(phi) * math.sin(dec)
        + math.cos(phi) * math.cos(dec) * math.cos(ha)
    )
    return math.degrees(alt)


def compute_sect(
    jd: float, sun_abs: float, lat: float, armc_deg: float,
) -> dict:
    """Sect object. Day iff the Sun is above the horizon (altitude > 0)."""
    alt = sun_altitude(jd, sun_abs, lat, armc_deg)
    is_day = alt > 0.0
    if is_day:
        return {
            "status": "day",
            "luminary_of_sect": "Sun",
            "sect_mate_planets": ["Jupiter", "Saturn"],
            "notes": f"Sun altitude {alt:.1f}° at birth (above horizon).",
        }
    return {
        "status": "night",
        "luminary_of_sect": "Moon",
        "sect_mate_planets": ["Venus", "Mars", "Mercury"],
        "notes": f"Sun altitude {alt:.1f}° at birth (below horizon).",
    }


def _body_orb_class(name: str, speed_class: str) -> str:
    if name in ("Ascendant", "Midheaven"):
        return "angle"
    return speed_class


def _allowed_orb(name_a: str, cls_a: str, name_b: str, cls_b: str,
                 aspect_name: str) -> float:
    pair = max(BODY_ORB[_body_orb_class(name_a, cls_a)],
               BODY_ORB[_body_orb_class(name_b, cls_b)])
    cap = ASPECT_ORB_CAP[aspect_name]
    return pair if cap is None else min(pair, cap)


def _aspect_relation(lon_a: float, speed_a: float | None, lon_b: float,
                     speed_b: float | None, aspect_deg: float):
    """Return (orb, applying_bool_or_None).

    Uses the angular-distance model: an aspect of angle A is in orb when the
    angular separation between the bodies is near A (A in {0,60,90,120,180}).
    The signed separation in (-180, 180] drives applying/separating. This avoids
    the "nearest multiple" pitfall that conflates a 1.8° gap with both a
    conjunction and an opposition.
    """
    diff = (lon_a - lon_b) % 360.0
    if diff > 180.0:
        diff -= 360.0  # signed separation in (-180, 180]
    absdiff = abs(diff)
    if aspect_deg == 0.0:
        orb = absdiff              # conjunction: separation near 0
        target_signed = 0.0
    elif aspect_deg == 180.0:
        orb = 180.0 - absdiff      # opposition: separation near 180
        target_signed = 180.0 if diff >= 0 else -180.0
    else:
        orb = abs(absdiff - aspect_deg)  # e.g. trine/square/sextile
        target_signed = aspect_deg if diff >= 0 else -aspect_deg
    rate = (speed_a if speed_a is not None else 0.0) - (
        speed_b if speed_b is not None else 0.0)
    s = diff - target_signed  # signed offset from the exact aspect
    if orb < 1e-9:
        applying = True
    elif rate == 0.0:
        applying = None
    else:
        applying = (s > 0 and rate < 0) or (s < 0 and rate > 0)
    return orb, applying


def compute_aspects(
    placements: list[dict], angles: dict[str, tuple[float, float | None, str]],
    include_minor: bool,
) -> list[dict]:
    """Build aspect list among placements (+ Asc/MC when provided).

    ``angles`` maps name → (absolute_degree, speed_or_None, speed_class).
    """
    # Build (name, lon, speed, speed_class) entries.
    bodies: list[tuple[str, float, float | None, str]] = []
    for p in placements:
        bodies.append((p["body"], p["absolute_degree"],
                       p.get("speed_deg_per_day"), _infer_class(p["body"])))
    for aname, (lon, spd, cls) in angles.items():
        bodies.append((aname, lon, spd, cls))

    wanted = [a for a in ASPECT_DEFS if a[2] or include_minor]
    out: list[dict] = []
    seen_pairs: set[tuple[str, str]] = set()
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            name_a, lon_a, spd_a, cls_a = bodies[i]
            name_b, lon_b, spd_b, cls_b = bodies[j]
            key = tuple(sorted((name_a, name_b)))
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            for aspect_name, aspect_deg, _major in wanted:
                orb, applying = _aspect_relation(
                    lon_a, spd_a, lon_b, spd_b, aspect_deg)
                allowed = _allowed_orb(name_a, cls_a, name_b, cls_b, aspect_name)
                if orb > allowed:
                    continue
                rec: dict = {
                    "body_a": name_a,
                    "aspect": aspect_name,
                    "body_b": name_b,
                    "orb_degrees": round(orb, 4),
                }
                if applying is True:
                    rec["applying"] = True
                elif applying is False:
                    rec["separating"] = True
                rec["exact"] = orb < EXACT_TOL_DEG
                out.append(rec)
    return out


def _infer_class(body_name: str) -> str:
    for name, _pid, cls, _on in _PLANETS:
        if name == body_name:
            return cls
    for _key, (name, _pid, cls) in _EXTRA_BODIES.items():
        if name == body_name:
            return cls
    return SPEED_SLOW


def compute_lot_of_fortune(
    asc_abs: float, sun_abs: float, moon_abs: float, is_day: bool,
    cusps: tuple[float, ...],
) -> dict:
    """Sect-aware Lot of Fortune: day = Asc+Moon−Sun; night = Asc+Sun−Moon."""
    if is_day:
        lon = _normalize_deg(asc_abs + moon_abs - sun_abs)
        formula = "Asc + Moon − Sun (day sect)"
    else:
        lon = _normalize_deg(asc_abs + sun_abs - moon_abs)
        formula = "Asc + Sun − Moon (night sect)"
    pos = zodiac_position(lon)
    return {
        "name": "Lot of Fortune",
        **pos,
        "house": _house_of(lon, cusps, len(cusps)),
        "formula": formula,
    }


# --------------------------------------------------------------------------- #
# Confidence rules
# --------------------------------------------------------------------------- #

_APPROX_WORDS = ("around", "about", "approx", "approximate", "~", "circa")


def infer_confidence(
    has_time: bool, explicit: str | None, approximate: bool,
    rectified: bool, place: str | None, notes_hint: str | None,
) -> str:
    """Apply the rules in references/foundations/birth_time_uncertainty.md."""
    if explicit:
        label = explicit.capitalize()
        if label not in _VALID_CONFIDENCE:
            raise ConfigError(
                f"--confidence must be one of "
                f"{sorted(_VALID_CONFIDENCE)}, got {explicit!r}"
            )
        return label
    if rectified:
        return CONF_RECTIFIED
    if approximate:
        return CONF_APPROX
    # Wording hints → approximate even with a time.
    hay = " ".join(filter(None, [place, notes_hint])).lower()
    if any(w in hay for w in _APPROX_WORDS):
        return CONF_APPROX
    if not has_time:
        return CONF_UNKNOWN
    return CONF_TIMED


# --------------------------------------------------------------------------- #
# Source notes / provenance
# --------------------------------------------------------------------------- #

def build_source_notes(
    *, swisseph_version: str, house_system: str, frame: str,
    ayanamsa: str | None, ephemeris_mode: str, topocentric_moon: bool,
    elevation: float | None, name: str | None, place: str | None,
    date_str: str, time_str: str | None, tz_label: str, tz_kind: str,
    lat: float, lon: float, confidence: str, extra: list[str],
) -> str:
    parts: list[str] = []
    parts.append(
        f"Computed by pyswisseph/Swiss Ephemeris {swisseph_version}.")
    parts.append(f"Frame: {frame}.")
    parts.append(f"House system: {house_system}.")
    parts.append(f"Ephemeris mode: {ephemeris_mode}.")
    parts.append(f"Topocentric Moon: {'on' if topocentric_moon else 'off'}"
                 + (f" (elevation {elevation} m)." if topocentric_moon else "."))
    parts.append(f"Birth-time confidence: {confidence}.")
    parts.append(
        f"Input: date {date_str}, time {time_str or '(none)'}, "
        f"tz {tz_label} ({tz_kind}), lat {lat}, lon {lon}.")
    if name:
        parts.append(f"Subject: {name}.")
    if place:
        parts.append(f"Place (label only; coordinates are authoritative): {place}.")
    parts.extend(extra)
    return " ".join(parts)


# --------------------------------------------------------------------------- #
# Top-level chart assembly
# --------------------------------------------------------------------------- #

def build_chart(cfg: dict) -> dict:
    """Assemble the full chart JSON from a parsed configuration dict."""
    # --- Parse inputs -------------------------------------------------------
    for req in ("date", "lat", "lon"):
        if cfg.get(req) is None:
            raise ConfigError(
                f"Missing required field '{req}' (pass --{req.replace('_', '-')} "
                f"or include it in --input JSON).")
    y, mo, d = parse_date(str(cfg["date"]))
    house_system = cfg.get("house_system", "Whole Sign")
    if house_system not in HOUSE_SYSTEMS:
        raise ConfigError(
            f"--house-system must be one of {sorted(HOUSE_SYSTEMS)}, "
            f"got {house_system!r}"
        )
    hsys_letter = HOUSE_SYSTEMS[house_system]

    lat = float(cfg["lat"])
    lon = float(cfg["lon"])
    if not -90.0 <= lat <= 90.0:
        raise ConfigError(f"--lat must be within [-90, 90], got {lat}")
    if not -180.0 <= lon <= 180.0:
        raise ConfigError(f"--lon must be within [-180, 180], got {lon}")

    tz, tz_label, tz_kind = resolve_timezone(
        cfg.get("tz"), cfg.get("lmt", False), lon)

    has_time = cfg.get("time") is not None
    noon_for_unknown = cfg.get("noon_for_unknown", False)
    if not has_time and not noon_for_unknown:
        raise ConfigError(
            "No birth time supplied. Pass --time HH:MM, or --noon-for-unknown "
            "to compute a noon-reference chart with birth_time_confidence=Unknown "
            "(angles/houses/sect omitted). A time is never silently guessed.")
    if has_time:
        hh, mm, ss = parse_time(cfg["time"])
    else:
        hh, mm, ss = 12, 0, 0  # explicit noon reference

    ut = wallclock_to_ut(y, mo, d, hh, mm, ss, tz)
    jd = ut_to_jd(ut)

    confidence = infer_confidence(
        has_time=has_time,
        explicit=cfg.get("confidence"),
        approximate=cfg.get("approximate", False),
        rectified=cfg.get("rectified", False),
        place=cfg.get("place"),
        notes_hint=cfg.get("confidence_notes"),
    )

    # --- Ephemeris setup ----------------------------------------------------
    ephe_path = cfg.get("ephe_path") or os.environ.get("SWISSEPH_PATH")
    if ephe_path:
        if not Path(ephe_path).is_dir():
            raise ConfigError(f"--ephe-path not found or not a directory: {ephe_path}")
        swe.set_ephe_path(str(ephe_path))
    else:
        swe.set_ephe_path(None)  # Moshier built-in

    ayanamsa = cfg.get("ayanamsa", "tropical")
    sidereal = ayanamsa != "tropical"
    if sidereal:
        mode = _resolve_ayanamsa(ayanamsa)
        swe.set_sid_mode(mode, 0, 0)

    elevation = cfg.get("elevation")
    topocentric_moon = elevation is not None

    # --- Bodies -------------------------------------------------------------
    body_list = [(name, pid, cls) for (name, pid, cls, _on) in _PLANETS]
    for key in cfg.get("extra_bodies", []) or []:
        if key not in _EXTRA_BODIES:
            raise ConfigError(
                f"Unknown --extra-body {key!r}; choose from "
                f"{sorted(_EXTRA_BODIES)}.")
        body_list.append(_EXTRA_BODIES[key])

    flags = _flags(sidereal, topo=False)
    placements, ephemeris_mode = compute_positions(
        jd, body_list, flags,
        topocentric_moon=topocentric_moon, elevation=elevation)

    # Map body → absolute longitude for aspects / lots.
    lon_map = {p["body"]: p["absolute_degree"] for p in placements}
    speed_map = {p["body"]: p.get("speed_deg_per_day") for p in placements}

    # --- Time-dependent factors (only when confidence implies a real time) --
    time_known = confidence in (CONF_TIMED, CONF_APPROX, CONF_RECTIFIED)
    chart_data: dict = {}
    extra_notes: list[str] = []
    angles_for_aspects: dict[str, tuple[float, float | None, str]] = {}
    asc_abs = moon_abs = sun_abs = None
    cusps = None

    if time_known:
        asc, mc, house_cusps, armc, raw_cusps = compute_angles_and_houses(
            jd, lat, lon, hsys_letter, sidereal)
        cusps = raw_cusps
        asc_abs = asc["absolute_degree"]
        sun_abs = lon_map["Sun"]
        moon_abs = lon_map["Moon"]
        chart_data["house_system"] = house_system
        chart_data["ascendant"] = asc
        chart_data["midheaven"] = mc
        chart_data["house_cusps"] = house_cusps  # extra-prop (additionalProperties)
        assign_houses(placements, raw_cusps)
        angles_for_aspects["Ascendant"] = (asc_abs, None, "angle")
        angles_for_aspects["Midheaven"] = (mc["absolute_degree"], None, "angle")
        if confidence == CONF_APPROX:
            extra_notes.append(
                "Angles/houses computed from an approximate time and are "
                "provisional; treat Ascendant, MC, cusps, and angularity as "
                "uncertain across the possible time range.")
        elif confidence == CONF_RECTIFIED:
            extra_notes.append(
                "Angles/houses come from a user-supplied RECTIFIED time, not a "
                "record-level time; do not present them as certain.")
    else:
        # Unknown: positions computed at the explicit noon reference.
        extra_notes.append(
            "No reliable birth time: positions are computed at a noon "
            "reference instant and birth_time_confidence is Unknown. The "
            "Ascendant, MC, houses, sect, and angle-based timing are omitted. "
            "The Moon's degree and sign may shift without a known time; treat "
            "lunar factors as provisional.")
        # Flag the Moon placement as provisional.
        for p in placements:
            if p["body"] == "Moon":
                p["notes"] = "Provisional: computed at the noon reference."

    # Strip the internal speed helper from output unless verbose.
    # (Done AFTER aspects so applying/separating can use daily speeds.)

    chart_data["placements"] = placements

    # --- Aspects ------------------------------------------------------------
    include_minor = cfg.get("minor_aspects", False)
    aspects = compute_aspects(
        placements,
        angles_for_aspects if not cfg.get("no_angle_aspects") else {},
        include_minor=include_minor,
    )
    chart_data["aspects"] = aspects

    if not cfg.get("verbose"):
        for p in placements:
            p.pop("speed_deg_per_day", None)

    # --- Sect & Lot of Fortune (require time) -------------------------------
    if time_known and asc_abs is not None:
        # Sect is a sky-position judgement: always use the TROPICAL Sun so the
        # ecliptic->equatorial altitude conversion is correct even when the
        # chart frame is sidereal.
        trop_sun, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH)
        sect = compute_sect(jd, trop_sun[0], lat, armc)
        chart_data["sect"] = sect
        if not cfg.get("no_lots") and cusps is not None:
            is_day = sect["status"] == "day"
            lot = compute_lot_of_fortune(asc_abs, sun_abs, moon_abs, is_day, cusps)
            chart_data["lots"] = [lot]

    # --- Provenance ---------------------------------------------------------
    source_notes = build_source_notes(
        swisseph_version=swe.version,
        house_system=house_system,
        frame=("sidereal, ayanamsa=" + ayanamsa) if sidereal else "tropical",
        ayanamsa=ayanamsa if sidereal else None,
        ephemeris_mode=ephemeris_mode,
        topocentric_moon=topocentric_moon,
        elevation=elevation,
        name=cfg.get("name"),
        place=cfg.get("place"),
        date_str=cfg["date"],
        time_str=cfg.get("time"),
        tz_label=tz_label,
        tz_kind=tz_kind,
        lat=lat,
        lon=lon,
        confidence=confidence,
        extra=extra_notes,
    )
    chart_data["source_notes"] = source_notes
    chart_data["birth_time_confidence"] = confidence

    # --- Top-level envelope (enum-validated so --input can't emit bad values) -
    reading_type = cfg.get("reading_type", "natal")
    tradition_mode = cfg.get("tradition_mode", "blended")
    tone = cfg.get("tone", "practical")
    _enforce_enum("reading_type", reading_type,
                  ["natal", "transit", "synastry", "solar_return",
                   "annual_profection", "horary", "electional"])
    _enforce_enum("tradition_mode", tradition_mode,
                  ["classical", "modern", "blended"])
    _enforce_enum("tone", tone,
                  ["practical", "poetic", "psychological", "technical",
                   "beginner-friendly"])
    out: dict = {
        "reading_type": reading_type,
        "tradition_mode": tradition_mode,
        "tone": tone,
        "chart_data": chart_data,
    }
    if cfg.get("user_question"):
        out["user_question"] = cfg["user_question"]
    return out


def _enforce_enum(field: str, value: str, allowed: list[str]) -> None:
    if value not in allowed:
        raise ConfigError(
            f"{field} must be one of {allowed}, got {value!r}")


def _resolve_ayanamsa(name: str) -> int:
    key = "SIDM_" + name.upper().replace(" ", "_")
    mode = getattr(swe, key, None)
    if mode is None:
        raise ConfigError(
            f"Unknown ayanamsa {name!r}. Use 'tropical' or a Swiss Ephemeris "
            f"sidereal mode such as 'Lahiri'.")
    return int(mode)


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #

def validate_against_schema(instance: dict, schema_path: Path) -> None:
    """Validate ``instance`` against the chart input JSON schema.

    Requires the ``jsonschema`` package (see tools/requirements-dev.txt).
    """
    try:
        import jsonschema  # type: ignore
    except ImportError:
        raise ConfigError(
            "--validate requires the 'jsonschema' package. "
            "Install with: pip install -r tools/requirements-dev.txt")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        jsonschema.Draft202012Validator(schema).validate(instance)
    except jsonschema.ValidationError as exc:
        path = ".".join(str(p) for p in exc.absolute_path) or "<root>"
        raise ConfigError(
            f"Output failed schema validation at {path}: {exc.message}")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _repo_schema_path() -> Path:
    return Path(__file__).resolve().parents[1] / "assets" / "schemas" / "chart_input_schema.json"


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="birth_to_chart.py",
        description="Convert birth data into chart JSON "
                    "(assets/schemas/chart_input_schema.json).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    g = p.add_argument_group("birth data")
    g.add_argument("--date", help="ISO date YYYY-MM-DD")
    g.add_argument("--time", help="Birth time HH:MM or HH:MM:SS (24h). "
                                  "Omit for Unknown; then pass --noon-for-unknown.")
    g.add_argument("--lat", type=float, help="Latitude in decimal degrees")
    g.add_argument("--lon", type=float, help="Longitude in decimal degrees")
    g.add_argument("--elevation", type=float, help="Elevation (m); enables "
                                                   "topocentric Moon.")
    g.add_argument("--tz", help="IANA zone (America/New_York) or fixed "
                                "offset (+05:30).")
    g.add_argument("--lmt", action="store_true", help="Use Local Mean Time "
                                                       "derived from --lon.")
    g.add_argument("--place", help="Free-text place label (coords are "
                                    "authoritative; no geocoding).")
    g.add_argument("--name", help="Optional subject label (source_notes only).")

    g = p.add_argument_group("chart options")
    g.add_argument("--house-system", default="Whole Sign",
                   choices=sorted(HOUSE_SYSTEMS))
    g.add_argument("--reading-type", default="natal",
                   choices=["natal", "transit", "synastry", "solar_return",
                            "annual_profection", "horary", "electional"])
    g.add_argument("--tradition-mode", default="blended",
                   choices=["classical", "modern", "blended"])
    g.add_argument("--tone", default="practical",
                   choices=["practical", "poetic", "psychological", "technical",
                            "beginner-friendly"])
    g.add_argument("--user-question", help="Optional querent focus.")

    g = p.add_argument_group("confidence (see birth_time_uncertainty.md)")
    g.add_argument("--confidence", choices=["timed", "approximate", "rectified",
                                            "unknown"],
                   help="Override the inferred confidence label.")
    g.add_argument("--approximate", action="store_true",
                   help="Mark the time as Approximate.")
    g.add_argument("--rectified", action="store_true",
                   help="Mark the time as Rectified (user-supplied).")
    g.add_argument("--noon-for-unknown", action="store_true",
                   help="With no --time, compute a noon-reference chart and "
                        "set birth_time_confidence=Unknown.")
    g.add_argument("--confidence-notes", dest="confidence_notes",
                   help="Free text scanned for 'around/about/approx' wording.")

    g = p.add_argument_group("ephemeris & frame")
    g.add_argument("--ephe-path", help="Directory of .se1 files "
                                       "(or set SWISSEPH_PATH).")
    g.add_argument("--ayanamsa", default="tropical",
                   help="'tropical' (default) or a SE sidereal mode (e.g. Lahiri).")
    g.add_argument("--extra-body", action="append", dest="extra_bodies",
                   choices=sorted(_EXTRA_BODIES),
                   help="Add Chiron / Lilith (repeatable).")

    g = p.add_argument_group("output options")
    g.add_argument("--minor-aspects", action="store_true",
                   help="Include quincunx/semisextile.")
    g.add_argument("--no-angle-aspects", action="store_true",
                   help="Suppress aspects to Ascendant/Midheaven.")
    g.add_argument("--no-lots", action="store_true",
                   help="Suppress the Lot of Fortune.")
    g.add_argument("--verbose", action="store_true",
                   help="Include internal planet speeds in placements.")
    g.add_argument("--validate", action="store_true",
                   help="Validate output against chart_input_schema.json.")
    g.add_argument("--schema", type=Path, default=_repo_schema_path(),
                   help="Path to chart_input_schema.json for --validate.")
    g.add_argument("--input", type=Path,
                   help="Read all options from a JSON file instead of flags.")
    g.add_argument("--output", type=Path, help="Write JSON to a file "
                                               "(default: stdout).")
    return p


def _prompt(msg: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    sys.stderr.write(f"{msg}{suffix}: ")
    sys.stderr.flush()
    val = input()
    return val.strip() or (default or "")


def collect_interactive() -> dict:
    """Prompt for the required fields when no args / --input are given."""
    sys.stderr.write(
        "birth_to_chart — interactive mode. Press Ctrl-C to cancel.\n\n")
    sys.stderr.flush()
    cfg: dict = {}
    cfg["date"] = _prompt("Date (YYYY-MM-DD)")
    t = _prompt("Time HH:MM (blank if unknown)")
    if t:
        cfg["time"] = t
    else:
        cfg["noon_for_unknown"] = True
    cfg["lat"] = _prompt("Latitude (decimal degrees)")
    cfg["lon"] = _prompt("Longitude (decimal degrees)")
    tz = _prompt("Timezone IANA name or +HH:MM (blank to use LMT from longitude)")
    if tz:
        cfg["tz"] = tz
    else:
        cfg["lmt"] = True
    hs = _prompt("House system", "Whole Sign")
    cfg["house_system"] = hs or "Whole Sign"
    place = _prompt("Place label (optional)")
    if place:
        cfg["place"] = place
    name = _prompt("Subject name (optional)")
    if name:
        cfg["name"] = name
    return cfg


def args_to_cfg(ns: argparse.Namespace) -> dict:
    cfg = {
        "date": ns.date, "time": ns.time, "lat": ns.lat, "lon": ns.lon,
        "elevation": ns.elevation, "tz": ns.tz, "lmt": ns.lmt,
        "place": ns.place, "name": ns.name,
        "house_system": ns.house_system, "reading_type": ns.reading_type,
        "tradition_mode": ns.tradition_mode, "tone": ns.tone,
        "user_question": ns.user_question,
        "confidence": ns.confidence, "approximate": ns.approximate,
        "rectified": ns.rectified, "noon_for_unknown": ns.noon_for_unknown,
        "confidence_notes": ns.confidence_notes,
        "ephe_path": str(ns.ephe_path) if ns.ephe_path else None,
        "ayanamsa": ns.ayanamsa, "extra_bodies": ns.extra_bodies,
        "minor_aspects": ns.minor_aspects,
        "no_angle_aspects": ns.no_angle_aspects, "no_lots": ns.no_lots,
        "verbose": ns.verbose, "validate": ns.validate,
        "schema": ns.schema, "output": ns.output,
    }
    return cfg


def _looks_bare(cfg: dict) -> bool:
    """True when no core data was supplied via flags → go interactive."""
    return not cfg.get("date") and not cfg.get("lat") and not cfg.get("lon")


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    ns = parser.parse_args(argv)

    if ns.input:
        if not ns.input.is_file():
            print(f"FAIL: --input file not found: {ns.input}", file=sys.stderr)
            return 2
        cfg = json.loads(ns.input.read_text(encoding="utf-8"))
        # Allow --validate / --output / --schema to override the file.
        cfg["validate"] = ns.validate
        cfg["output"] = str(ns.output) if ns.output else cfg.get("output")
        if ns.schema:
            cfg["schema"] = ns.schema
    else:
        cfg = args_to_cfg(ns)
        if _looks_bare(cfg):
            try:
                cfg.update(collect_interactive())
            except (KeyboardInterrupt, EOFError):
                print("\nCancelled.", file=sys.stderr)
                return 2

    try:
        chart = build_chart(cfg)
        if cfg.get("validate"):
            schema_path = Path(cfg.get("schema") or _repo_schema_path())
            if not schema_path.is_file():
                raise ConfigError(
                    f"--schema file not found: {schema_path}")
            validate_against_schema(chart, schema_path)
    except ConfigError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2

    text = json.dumps(chart, indent=2, ensure_ascii=False)
    out = cfg.get("output")
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)

    if cfg.get("validate"):
        print("VALID: output conforms to chart_input_schema.json.",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    swe.set_ephe_path(None)  # default to Moshier; overridden if --ephe-path
    raise SystemExit(main())
