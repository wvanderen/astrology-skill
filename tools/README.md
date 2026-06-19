# `tools/birth_to_chart.py` — Birth-Data → Chart JSON Pre-Processor

A standalone developer utility that converts raw birth data into a chart JSON
object conforming to
[`assets/schemas/chart_input_schema.json`](../assets/schemas/chart_input_schema.json).
The output is **geometry + provenance only**; the astrology skill supplies the
doctrine. This tool is a *pre-processor* — it is **not** imported, loaded, or
referenced by `SKILL.md` or `references/`, so the skill stays
calculation-free. See [`docs/birth_to_chart_design.md`](../docs/birth_to_chart_design.md)
for the full design and the boundary rationale.

> **License notice.** This `tools/` directory is **AGPL-3.0** because it uses
> `pyswisseph` (Swiss Ephemeris). Read [`NOTICE.md`](NOTICE.md) before use. The
> AGPL boundary is confined to this directory and does not extend to the skill.

---

## Install

The skill itself has no dependencies. This tool is opt-in; install it into a
virtualenv of your own:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements.txt          # runtime: pyswisseph
pip install -r tools/requirements-dev.txt      # adds jsonschema for --validate
```

Requirements: Python 3.10+ (uses stdlib `zoneinfo`).

**No ephemeris data files required.** The script uses the built-in Moshier
ephemeris by default (planets ≈ 0.1″, Moon ≈ 3″ — far inside any natal orb). It
records `ephemeris mode: Moshier (built-in)` in `source_notes`. For maximum
precision, download the `.se1` files once from Astrodienst and pass
`--ephe-path <dir>` (or set `SWISSEPH_PATH`); the mode note switches to
`Swiss Ephemeris .se1`. Never commit `.se1` files into this repo.

---

## Usage

### Non-interactive (flags)

```bash
python tools/birth_to_chart.py \
    --date 1990-05-21 --time 14:32 \
    --lat 40.7128 --lon -74.0060 \
    --tz "America/New_York" \
    --house-system "Whole Sign" \
    --name "Subject A" --place "Brooklyn, NY" \
    --reading-type natal --tradition-mode blended --tone practical \
    --validate --output chart.json
```

### JSON input file

```bash
python tools/birth_to_chart.py --input birth.json --validate --output chart.json
```

`birth.json` is the same keys as the CLI flags:

```json
{
  "date": "1990-05-21",
  "time": "14:32",
  "lat": 40.7128,
  "lon": -74.0060,
  "tz": "America/New_York",
  "house_system": "Whole Sign",
  "name": "Subject A",
  "place": "Brooklyn, NY",
  "reading_type": "natal",
  "approximate": false,
  "validate": true
}
```

### Interactive (no args)

```bash
python tools/birth_to_chart.py
```

Prompts for the required fields. Timezone may be entered as an IANA name or
left blank to use Local Mean Time derived from longitude.

### Output

- Default: JSON printed to **stdout**.
- `--output FILE`: written to a file instead.
- `--validate`: checks the emitted object against
  `assets/schemas/chart_input_schema.json` (requires `jsonschema`); prints
  `VALID: …` to stderr and exits non-zero on failure.

**Exit codes:** `0` success (and `--validate`, if requested, passed); `2`
bad/missing input or validation failure, with a message naming the field.

---

## Inputs

| Field | Required | Notes |
|---|---|---|
| `--date` | yes | ISO `YYYY-MM-DD`. |
| `--time` | see below | `HH:MM` or `HH:MM:SS` (24h). |
| `--lat`, `--lon` | yes | Decimal degrees. `--elevation` (m) enables topocentric Moon. |
| `--tz` | conditional | IANA name (`America/New_York`) **or** fixed offset (`+05:30`). Required unless `--lmt`. |
| `--lmt` | optional | Local Mean Time offset derived from `--lon`. |
| `--place`, `--name` | optional | Free-text labels for `source_notes`. **Coordinates are authoritative** — no network geocoding (deterministic/offline). |
| `--house-system` | optional | Default **`Whole Sign`** (robust to birth-time uncertainty). Also: Placidus, Regiomontanus, Koch, Equal, Campanus, Porphyrius, Morinus, Alcabitius, Topocentric. |
| `--reading-type` / `--tradition-mode` / `--tone` | optional | Pass-through; defaults `natal` / `blended` / `practical`. |
| `--user-question` | optional | Querent focus. |
| `--elevation` | optional | Meters; enables parallax-corrected (topocentric) Moon. |
| `--ayanamsa` | optional | `tropical` (default) or a SE sidereal mode (e.g. `Lahiri`). |
| `--ephe-path` / `SWISSEPH_PATH` | optional | Directory of `.se1` files. |
| `--extra-body` | optional | Add `chiron` / `lilith` (repeatable; Chiron needs `.se1`). |
| `--minor-aspects` | optional | Include quincunx (150°) and semisextile (30°). |
| `--no-angle-aspects` | optional | Suppress aspects to Ascendant/Midheaven. |
| `--no-lots` | optional | Suppress the Lot of Fortune. |
| `--verbose` | optional | Include internal planet daily speeds in placements. |

### Confidence flags (see `references/foundations/birth_time_uncertainty.md`)

| Flag / condition | `birth_time_confidence` |
|---|---|
| valid `--time` + `--tz`, no caveat | `Timed` |
| `--approximate`, or "around/about/approx/circa/~" wording in `--place`/`--confidence-notes` | `Approximate` |
| no `--time` (requires `--noon-for-unknown`), or `--confidence unknown` | `Unknown` |
| `--rectified` | `Rectified` |

**The tool never guesses a timezone or a birth time.**

- Missing `--tz` with no `--lmt` is a hard error.
- Missing `--time` with no `--noon-for-unknown` is a hard error. The user
  must *opt in* to a noon-reference chart.

When confidence is **Unknown**, the Ascendant, MC, houses, house cusps, sect,
and angle-based timing are **omitted**; only stable factors (planet signs,
interplanetary aspects, motion) are emitted, and the Moon placement is flagged
provisional (the Moon can move ~13°/day). This matches
`references/foundations/birth_time_uncertainty.md`. When **Approximate**, angles
and houses are still computed but `source_notes` labels them provisional.

---

## Output shape

Conforms to `chart_input_schema.json` (top-level `reading_type`,
`tradition_mode`, `tone`, optional `user_question`, and `chart_data`):

- `source_notes` — provenance: pyswisseph/SE version, frame, house system,
  ephemeris mode, topocentric on/off, confidence, and the raw input.
- `birth_time_confidence` — `Timed` / `Approximate` / `Unknown` / `Rectified`.
- `ascendant`, `midheaven` — `{sign, degree, absolute_degree}` (when time known).
- `house_system` and `house_cusps` — array of `{house, sign, degree, absolute_degree}` (when time known).
- `placements` — Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus,
  Neptune, Pluto, True Node (+ extras). Each: `body`, `sign`, `degree`,
  `absolute_degree`, `motion` (`direct`/`retrograde`/`stationary`), `house`
  (when known), and empty `condition` / `dignity` arrays — those are
  **interpretive** and belong to the skill.
- `aspects` — major Ptolemaic aspects (conjunction, opposition, trine, square,
  sextile) between planets **and** to the Asc/MC when known; `orb_degrees`,
  `applying`/`separating` (from daily-speed comparison), and `exact`. Minor
  aspects opt-in.
- `sect` — `{status, luminary_of_sect, sect_mate_planets, notes}`; day iff the
  Sun is above the horizon (when time known).
- `lots` — Lot of Fortune (sect-aware: day = Asc + Moon − Sun; night = Asc + Sun − Moon).

### Default orb table

Per-body max orbs (pair orb = the larger of the two): luminaries 10°, personal
planets (Mercury/Venus/Mars) 7°, Jupiter–Pluto 8°, True Node 5°, angles 8°.
Capped per aspect: sextile 6°, quincunx 3°, semisextile 2°; major aspects use
the pair orb uncapped. An aspect is `exact` when its orb is below 0.05°
(3 arcmin). Stationary is reported when |daily longitude speed| < 0.01°/day.

---

## Calculation vs. interpretation boundary

| Computed here (objective) | Deferred to the skill (interpretive) |
|---|---|
| Planet positions, signs, degrees | Sign/planet *meanings* |
| House cusp geometry, Asc/MC, planet-in-house | House *topic* synthesis |
| Sect day/night status | Sect *weighting* |
| Aspect geometry, orbs, applying/separating | Aspect *interpretation* |
| Lot of Fortune position | Lot *significance* |
| Motion (direct/retrograde) | Essential/accidental **dignity**, **condition** |

---

## Smoke test

```bash
python tools/smoke_test.py
```

Runs three documented birth-data sets (different years, hemispheres, IANA
zones) and checks that the script's Ascendant and MC (via Swiss Ephemeris)
agree to **±0.05°** with an **independent** from-scratch recomputation
(IAU 1982 GMST + IAU 1980 obliquity, stdlib only — no Swiss Ephemeris), and
that each output passes `--validate`. Run with the interpreter that has
`pyswisseph` installed.
