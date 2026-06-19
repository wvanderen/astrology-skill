# End-to-End Path: Birth Data → Reading

**Task:** `td-f1eb5b` (parent epic `td-9b20e3`)
**Scope:** The single wired path from raw birth data to a synthesized reading,
and how each stage hands off to the next. This is a walkthrough, not a design
note — every command below is runnable as written.

The path has three stages and a hard boundary between stage 1 and stage 2:

```
 raw birth data ──► [1] tools/birth_to_chart.py ──► chart JSON
                          (the ONLY calculator; AGPL-confined, opt-in)
                                                    │
                                  ── no-calculation boundary ──
                                                    │
            chart JSON ──► [2] entry_commands.py --route ──► route ticket
                          (resolve + validate; never computes)
                                                    │
                         route ticket ──► [3] SKILL.md Workflow step 1
                          (retrieval, ranking, synthesis, self-check)
```

Stage 1 **computes** geometry. Stages 2–3 **never compute** — they route and
interpret. The skill package an agent loads is dependency-free and contains no
link to stage 1; `tools/birth_to_chart.py` is a separate-process pre-processor
the user opts into. See `docs/birth_to_chart_design.md` §1 and
`docs/entry_commands.md` §2 for the boundary rationale.

---

## Prerequisites (stage 1 only)

Stage 1 needs `pyswisseph` (and `jsonschema` for `--validate`). Install them in
a virtualenv of your own — the skill itself has no dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements.txt          # pyswisseph
pip install -r tools/requirements-dev.txt      # jsonschema (for --validate)
```

Stages 2–3 use **only the Python standard library** (system `python3` is fine).

---

## Stage 1 — Birth data → chart JSON

`tools/birth_to_chart.py` converts raw birth data into a chart JSON object that
conforms to [`assets/schemas/chart_input_schema.json`](../assets/schemas/chart_input_schema.json).
The output is **geometry + provenance only** (positions, Asc/MC, houses,
aspects, sect, Lot of Fortune, `source_notes`, `birth_time_confidence`);
condition/dignity arrays are emitted empty — those are interpretive and belong
to the skill.

```bash
python3 tools/birth_to_chart.py \
    --date 1990-05-21 --time 14:32 \
    --lat 40.7128 --lon -74.0060 --tz "America/New_York" \
    --house-system "Whole Sign" --reading-type natal \
    --name "Subject A" --place "Brooklyn, NY" \
    --validate --output chart.json
```

`--validate` checks the emitted object against the schema and prints
`VALID: output conforms to chart_input_schema.json.` to stderr. Exit code is
`0` on success, `2` on bad/missing input or validation failure (the message
names the offending field).

No ephemeris data files are required — the built-in Moshier ephemeris is used
by default; pass `--ephe-path <dir>` for `.se1` precision. See
[`tools/README.md`](../tools/README.md) for every flag.

The tool **never guesses** a timezone or birth time. Missing `--tz` (without
`--lmt`) and missing `--time` (without `--noon-for-unknown`) are hard errors.
When confidence is `Unknown`, angles/houses/sect are omitted and the Moon is
flagged provisional — matching
[`references/foundations/birth_time_uncertainty.md`](../references/foundations/birth_time_uncertainty.md).

---

## Stage 2 — chart JSON → route ticket

`entry_commands.py --route` is the single entry gate. It **resolves** the chart
object, **validates** it, and prints a route ticket that hands control to
`SKILL.md` Workflow step 1. It performs no calculation.

It accepts the chart in three input modes (all resolve to the same object):

| Mode | Invocation | Use when |
|---|---|---|
| **File path** | `--route chart.json` | The script wrote a file (stage 1 example). Repeat use. |
| **stdin / pipe** | `--route -` (reads stdin) | Piping the script's stdout straight in — one command, no temp file. |
| **Inline JSON** | `--route '{...}'` | Small/ad-hoc charts; matches the prompt-template Mode 1. |

### Mode A — file (stage 1 wrote `chart.json`)

```bash
python3 entry_commands.py --route chart.json
```

### Mode B — pipe (script stdout → entry stdin, no temp file)

```bash
python3 tools/birth_to_chart.py \
    --date 1990-05-21 --time 14:32 \
    --lat 40.7128 --lon -74.0060 --tz "America/New_York" --validate \
  | python3 entry_commands.py --route -
```

### What the route ticket looks like

```
ENTRY ROUTE TICKET
==================
status:               VALID — gate passed (deep: jsonschema)
reading_type:         natal
tradition_mode:       blended
tone:                 practical
retrieval module:     references/reading_types/natal.md (present)
entry fragment:       prompts/entry/natal.md (present)

ROUTE -> Hand the resolved object to SKILL.md -> Workflow step 1
        ("Parse the supplied chart data and reading request").
        Do NOT calculate, rectify, or derive any chart factor.
```

`status` shows which gate ran:

- **`(deep: jsonschema)`** — `jsonschema` is installed; full Draft 2020-12
  validation against `chart_input_schema.json` ran in addition to the
  structural gate.
- **`(deep: unavailable)`** — only the dependency-free structural gate ran
  (requires `reading_type` in the enum and a `chart_data` object). This is the
  documented contract when `jsonschema` is absent; it is not an error. Install
  `jsonschema` (`tools/requirements-dev.txt`) if you want full deep validation
  at the gate.

---

## Stage 3 — route ticket → reading

The route ticket hands the **resolved chart object** to `SKILL.md` → Workflow
step 1 ("Parse the supplied chart data and reading request"). From there
`SKILL.md` owns everything: building the reading plan, selecting the minimum
references, ranking factors, synthesizing, and the reading self-check. The
prompt templates under [`prompts/entry/`](../prompts/entry/) frame per-type
requests (e.g. horary asks for the querent's question; electional lists
candidate start charts); they add no calculation.

If you are invoking through a host that supports the skill's prompt surface,
the canonical template [`prompts/entry/_reading.md`](../prompts/entry/_reading.md)
performs the same resolve → validate → route in prompt form.

---

## External chart tools (not just the bundled script)

Stage 2 accepts **any** chart JSON that conforms to
`chart_input_schema.json`, not only the bundled script's output. The schema is
`additionalProperties: true` at the root, in `chart_data`, and inside every
factor, so external tools may include extra fields. The only hard requirements
are:

- `reading_type` — one of the enum values in
  `chart_input_schema.json` → `properties.reading_type.enum`
  (`natal`, `transit`, `synastry`, `solar_return`, `annual_profection`,
  `horary`, `electional`).
- `chart_data` — an object.

Example: a hand-typed or externally-generated natal chart routes fine:

```bash
python3 entry_commands.py --route '{
  "reading_type": "natal",
  "tradition_mode": "classical",
  "tone": "technical",
  "user_question": "What is the vocation pattern?",
  "chart_data": {
    "source_notes": "External astrology program.",
    "house_system": "Whole Sign",
    "ascendant": {"sign": "Virgo", "degree": 18.4},
    "placements": [
      {"body": "Mercury", "sign": "Gemini", "degree": 15.7, "house": 10,
       "dignity": ["domicile"], "rules_houses": [1, 10]}
    ]
  }
}'
```

`tests/entry/sample_synastry.json` shows a richer external-tool-style chart
(nested `person_a` / `person_b` blocks plus inter-chart aspects) — it passes
the gate unchanged.

---

## Failure modes

Every chart-input failure exits `2` and prints a `FAIL:` line that **points at
the schema**, so the user always knows the authoritative shape. Deep-validation
failures (when `jsonschema` is present) print one concise line with the JSON
path instead of a multi-page schema dump.

| Problem | Message (illustrative) |
|---|---|
| Invalid JSON | `could not parse JSON from <inline>: ... See assets/schemas/chart_input_schema.json for the required shape.` |
| Missing `reading_type` | `missing required field: reading_type See assets/schemas/chart_input_schema.json for the required shape.` |
| Unknown `reading_type` | `reading_type 'banana' is not in the schema enum (allowed: ...) See assets/schemas/chart_input_schema.json for the required shape.` |
| Missing `chart_data` | `missing required field: chart_data See assets/schemas/chart_input_schema.json for the required shape.` |
| Wrong type for `chart_data` | `chart_data must be an object, got list See assets/schemas/chart_input_schema.json for the required shape.` |
| Deep failure (jsonschema) | `chart input failed schema validation at $.chart_data.placements[0]: 'body' is a required property See assets/schemas/chart_input_schema.json for the required shape.` |

The entry **never infers, defaults, or fills in** missing fields. If a field is
required for the requested reading but absent from `chart_data`, that is
handled later by `SKILL.md`'s incomplete-data rule (interpret only the factors
provided; ask for the rest, or narrow the reading and label it provisional).

---

## Acceptance-criteria mapping

| Criterion (`td-f1eb5b`) | Where |
|---|---|
| End-to-end path works: birth data → script → chart JSON → entry → workflow | Stage 1 → Stage 2 → Stage 3 above; asserted by `tests/entry/end_to_end_test.py` (real script run, file + pipe modes). |
| Documented example of the full path | This document (Modes A and B). |
| Entry gracefully handles script output **and** external-tool charts | "External chart tools" section; `additionalProperties: true`; tested for both sources. |
| Failure modes surface a clear message pointing to the schema | "Failure modes" table; every gate error appends the schema pointer. |
