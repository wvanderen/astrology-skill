#!/usr/bin/env python3
"""Single green/red validation matrix for the astrology skill (td-3b7112, A.1).

Re-runnable command that runs every deterministic validation surface and
prints one green/red matrix. Covers the six ``A.1`` checks from
``docs/e2e_validation_plan.md`` plus the two ``A.2`` structural-drift guards
landed in this task.

The matrix is the honest snapshot: a check is ``PASS`` (exit 0), ``FAIL``
(non-zero), or ``SKIP`` (a venv-only check when ``.venv`` is absent). The
script exits 0 only when every check is ``PASS``.

Today the matrix is **expected to be red on exactly one row** —
``A.2.1 gap-matrix drift`` — because ``references/reference_gap_matrix.md`` is
a pre-Phase-5/6/7 snapshot that td-76f5e0 (Phase B.2) will refresh. That row's
``note`` points at the fixing task. Once B.2 lands, the matrix goes fully
green and this script guards against regression.

Checks
------
A.1 deterministic suite (must be green before B–D proceed):
  1. quick_validate.py            (system python3; SKILL.md + entry parity)
  2. entry_commands.py --check    (system python3; enum/fragment parity)
  3. tests/entry/smoke_test.py    (system python3; full entry surface)
  4. tests/entry/end_to_end_test.py (.venv; calculator-backed stages)
  5. tools/smoke_test.py          (.venv; Asc/MC within ±0.05° on 3 fixtures)
  6. schema + agents/openai.yaml parse (.venv; ROADMAP Phase 5 static guard)

A.2 structural-drift guards (new in td-3b7112):
  7. tests/structure/gap_matrix_drift.py        (system python3)
  8. tests/structure/source_notes_pointers.py   (system python3)

Run
---
    python3 tests/run_validation_matrix.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent  # tests/
ROOT = HERE.parent                    # repo root
VENV_PY = ROOT / ".venv" / "bin" / "python3"

# Width helpers for the printed table.
_COL_ID = 6
_COL_INTERP = 7


@dataclass
class Check:
    cid: str
    group: str
    label: str
    interpreter: str  # "system" or "venv"
    argv: list[str]
    note: str
    # Populated by run().
    status: str = "SKIP"
    detail: str = field(default="")


CHECKS: list[Check] = [
    Check("A.1.1", "A.1", "quick_validate.py",
          "system", ["quick_validate.py"],
          "SKILL.md metadata + folded entry parity"),
    Check("A.1.2", "A.1", "entry_commands.py --check",
          "system", ["entry_commands.py", "--check"],
          "enum <-> fragment parity (8 reading types)"),
    Check("A.1.3", "A.1", "tests/entry/smoke_test.py",
          "system", ["tests/entry/smoke_test.py"],
          "full entry-command surface"),
    Check("A.1.4", "A.1", "tests/entry/end_to_end_test.py",
          "venv", ["tests/entry/end_to_end_test.py"],
          "calculator-backed stages + failure modes"),
    Check("A.1.5", "A.1", "tools/smoke_test.py",
          "venv", ["tools/smoke_test.py"],
          "Asc/MC within +/-0.05 deg on 3 fixtures"),
    Check("A.1.6", "A.1", "schema + agents/openai.yaml parse",
          "venv", ["tests/structure/schema_and_agents_parse.py"],
          "ROADMAP Phase 5 static-asset guard"),
    Check("A.2.1", "A.2", "tests/structure/gap_matrix_drift.py",
          "system", ["tests/structure/gap_matrix_drift.py"],
          "EXPECTED FAIL until td-76f5e0 refreshes the gap matrix"),
    Check("A.2.2", "A.2", "tests/structure/source_notes_pointers.py",
          "system", ["tests/structure/source_notes_pointers.py"],
          "Source-notes pointer targets exist"),
]


def _resolve_interpreter(kind: str) -> str | None:
    if kind == "system":
        return sys.executable or shutil.which("python3") or "python3"
    if kind == "venv":
        if VENV_PY.is_file():
            return str(VENV_PY)
        return None
    raise ValueError(f"unknown interpreter kind: {kind!r}")


def _last_meaningful_line(stdout: str, stderr: str) -> str:
    """Return a one-line summary of the check's output."""
    blob = "\n".join(part for part in (stdout, stderr) if part).strip()
    if not blob:
        return ""
    # Prefer the final PASS/FAIL/DRIFT/SKIP summary line.
    for line in reversed(blob.splitlines()):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped[:6].upper() in ("PASS: ", "FAIL: ", "DRIFT:", "SKIP: ") or \
                stripped.lower().startswith(("pass", "all ", "drift")):
            return stripped
    return blob.splitlines()[-1].strip()


def run_check(check: Check) -> None:
    py = _resolve_interpreter(check.interpreter)
    if py is None:
        check.status = "SKIP"
        check.detail = ".venv absent (venv-only check)"
        return
    argv = [py, *check.argv]
    try:
        proc = subprocess.run(
            argv, capture_output=True, text=True, cwd=str(ROOT), timeout=120,
        )
    except subprocess.TimeoutExpired:
        check.status = "FAIL"
        check.detail = "timed out after 120s"
        return
    check.status = "PASS" if proc.returncode == 0 else "FAIL"
    check.detail = _last_meaningful_line(proc.stdout, proc.stderr)


def print_matrix(checks: list[Check]) -> None:
    print()
    print("Astrology skill — deterministic validation matrix")
    print("=" * 72)
    label_w = max(len(c.label) for c in checks)
    print(f"{'ID':<{_COL_ID}}  {'Check':<{label_w}}  {'Status':<6}  "
          f"{'Interp':<{_COL_INTERP}}  Note")
    print("-" * (72))
    last_group = None
    for c in checks:
        if c.group != last_group:
            if last_group is not None:
                print()
            last_group = c.group
        print(f"{c.cid:<{_COL_ID}}  {c.label:<{label_w}}  {c.status:<6}  "
              f"{c.interpreter:<{_COL_INTERP}}  {c.note}")
        # Show the captured summary line only when it adds information
        # (non-PASS, or a SKIP/FAIL explanation).
        if c.status != "PASS" and c.detail and c.detail != c.note:
            print(f"{'':<{_COL_ID}}  {'':<{label_w}}  {'':<6}  "
                  f"{'':<{_COL_INTERP}}  -> {c.detail}")
    print()


def main() -> int:
    for check in CHECKS:
        run_check(check)

    print_matrix(CHECKS)

    # Group tallies.
    groups: dict[str, list[Check]] = {}
    for c in CHECKS:
        groups.setdefault(c.group, []).append(c)

    for gid in sorted(groups):
        row = groups[gid]
        p = sum(1 for c in row if c.status == "PASS")
        f = sum(1 for c in row if c.status == "FAIL")
        s = sum(1 for c in row if c.status == "SKIP")
        tag = f"{p}/{len(row)} PASS"
        if f:
            tag += f", {f} FAIL"
        if s:
            tag += f", {s} SKIP"
        print(f"  {gid} ({len(row)} checks): {tag}")

    fails = [c for c in CHECKS if c.status == "FAIL"]
    skips = [c for c in CHECKS if c.status == "SKIP"]
    print()
    if not fails and not skips:
        print("MATRIX GREEN: every deterministic check passed.")
        return 0
    if fails:
        print(f"MATRIX RED: {len(fails)} check(s) failed:")
        for c in fails:
            print(f"  - [{c.cid}] {c.label}: {c.detail}")
    if skips:
        print(f"MATRIX AMBER: {len(skips)} check(s) skipped:")
        for c in skips:
            print(f"  - [{c.cid}] {c.label}: {c.detail}")
    print()
    print(
        "Note: A.2.1 (gap-matrix drift) is EXPECTED to fail until td-76f5e0 "
        "(Phase B.2) refreshes references/reference_gap_matrix.md. All other "
        "rows should be green."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
