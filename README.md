# Astrology Skill

A retrieval-first astrology **interpretation** skill. It synthesizes a reading
from chart data that has **already been calculated** — placements, houses,
aspects, dignities, sect, rulerships, transits, synastry factors, lots, and
timing factors. It does **not** calculate charts, rectify birth times, derive
house cusps, assign dignities, compute aspects, or infer sect.

The skill package itself is **dependency-free** (Python standard library only).
The bundled birth-data → chart calculator is an **opt-in, separate-process**
developer utility that is never imported by the skill runtime.

> **Skill doctrine lives in [`SKILL.md`](SKILL.md).** That file defines the
> input contract, the retrieval workflow, the weighting hierarchy, the output
> guardrails, and the reading self-check. This README is the operational guide.

---

## What it does

- **Interprets** already-calculated chart data into a synthesized reading
  (natal, transit, synastry, solar return, annual profection, horary,
  electional, mundane).
- **Routes** chart JSON through a single validation gate into the retrieval
  workflow described in `SKILL.md`.
- **Loads only the relevant references** (137 interpretive modules under
  [`references/`](references)) rather than free-associating from general
  knowledge.

The hard rule is the **no-calculation boundary**: stage 1 *computes* geometry;
stages 2–3 only *route* and *interpret*. See
[`docs/end_to_end.md`](docs/end_to_end.md) for the full walkthrough.

```
 raw birth data ──► [1] tools/birth_to_chart.py ──► chart JSON   (computes; AGPL, opt-in)
                                                     │
                                  ── no-calculation boundary ──
                                                     │
            chart JSON ──► [2] entry_commands.py --route ──► route ticket   (validates; never computes)
                                                     │
                         route ticket ──► [3] SKILL.md Workflow step 1   (retrieve, rank, synthesize, self-check)
```

---

## Requirements

- **Python 3.10+** (stage 1 uses stdlib `zoneinfo`).
- **No dependencies** for the skill itself, the entry gate, or `SKILL.md` —
  system `python3` is sufficient.
- **Optional** (stage 1 calculator only): `pyswisseph`, plus `jsonschema` if
  you want deep validation. These live in a virtualenv you create (see below).

---

## Installation

### 1. Get the skill

```bash
git clone <this-repo-url> astrology-skill
cd astrology-skill
```

The skill is now usable. An agent host loads `SKILL.md` and the
[`agents/openai.yaml`](agents/openai.yaml) interface metadata; the retrieval
workflow and all references are plain Markdown.

### 2. (Optional) Set up the birth-data calculator

Only needed if you want to generate chart JSON from raw birth data. This is
isolated to [`tools/`](tools) and is **AGPL-3.0** (it uses `pyswisseph`) —
read [`tools/NOTICE.md`](tools/NOTICE.md) first. The AGPL boundary is confined
to `tools/` and does not extend to the skill.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements.txt          # runtime: pyswisseph
pip install -r tools/requirements-dev.txt      # adds jsonschema for --validate
```

No ephemeris data files are required — the built-in Moshier ephemeris is used
by default (planets ≈ 0.1″, Moon ≈ 3″, well inside any natal orb). For maximum
precision, download `.se1` files from Astrodienst and pass `--ephe-path <dir>`
(or set `SWISSEPH_PATH`). Never commit `.se1` files.

---

## Installing the skill into coding agents

This skill follows the [Agent Skills standard](https://agentskills.io/specification):
a directory containing `SKILL.md` with `name` + `description` frontmatter. Any
standard-compliant harness loads it the same way — you register the skill
directory once per harness.

> The skill's [`SKILL.md`](SKILL.md) already conforms to the standard.
> [`agents/openai.yaml`](agents/openai.yaml) is **extra interface metadata**
> (display name, entry-command surface). The standard loader ignores unknown
> fields, so the skill loads even in a harness that does not read that file;
> harnesses that do (e.g. Codex) use it for the entry-command surface.

### Recommended: clone once, symlink into each harness

Keep a single source so `git pull` updates flow through to every harness:

```bash
# clone once (anywhere stable)
git clone <this-repo-url> ~/skills/astrology-skill

# then link it into each harness's skills directory (see paths below)
ln -s ~/skills/astrology-skill ~/.codex/skills/astrology-skill
ln -s ~/skills/astrology-skill ~/.pi/agent/skills/astrology-skill
ln -s ~/skills/astrology-skill ~/.claude/skills/astrology-skill
```

Symlinks are preferred; copy the directory instead if your harness does not
follow symlinks (`cp -R ~/skills/astrology-skill <dest>/`).

### Per-harness locations

| Harness | Skills directory | Notes |
|---|---|---|
| **OpenAI Codex** | `~/.codex/skills/<name>/` | Native path (`$CODEX_HOME/skills`). Codex ships a built-in `skill-installer`; see below. |
| **Pi** | `~/.pi/agent/skills/<name>/` or `~/.agents/skills/<name>/` | Both are scanned. The shared `~/.agents/skills/` location is read by multiple harnesses. |
| **Claude Code** | `~/.claude/skills/<name>/` | Global user skills. Project-level: `.claude/skills/`. |
| **OpenCode** | config / plugin model | No native Agent-Skills directory in this install; register the directory in `opencode.jsonc` or place a project-level `.agents/skills/` symlink (see below). |

#### OpenAI Codex

```bash
mkdir -p ~/.codex/skills
ln -s "$PWD" ~/.codex/skills/astrology-skill
```

Alternatively, Codex's built-in `skill-installer` skill installs into
`~/.codex/skills` from a GitHub repo path — invoke it inside Codex and point it
at this repository. (`agents/openai.yaml` declares the entry-command surface
Codex reads.)

#### Pi

```bash
mkdir -p ~/.pi/agent/skills ~/.agents/skills
ln -s "$PWD" ~/.pi/agent/skills/astrology-skill
ln -s "$PWD" ~/.agents/skills/astrology-skill      # shared across harnesses
```

Pi also accepts a one-off load without installing:

```bash
pi --skill "$PWD"
```

…or a `skills` array in `~/.pi/settings.json` / project `.pi/settings.json`:

```json
{ "skills": ["~/skills/astrology-skill"] }
```

Once installed, the skill registers as `/skill:astrology-skill` and is
auto-suggested when a request matches its description.

#### Claude Code

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD" ~/.claude/skills/astrology-skill
```

For project-only scope, symlink into `.claude/skills/` inside the project root
instead.

#### OpenCode

OpenCode is config/plugin-driven. Two reliable options:

- **Project-level shared skills dir** (read by standard-compliant harnesses):
  symlink the skill into `.agents/skills/` at your project root.
- **Register in config** by adding the directory to your `opencode.jsonc`
  agent/plugin configuration (OpenCode does not scan a fixed `skills/` dir).

> OpenCode's exact Agent-Skills loading can vary by version — confirm against
> your OpenCode release if the skill does not appear.

### Project-level install (all harnesses, per-project)

For a single project, the cross-harness convention is `.agents/skills/` at the
project root (discovered by Pi and other standard-compliant harnesses):

```bash
mkdir -p .agents/skills
ln -s /absolute/path/to/astrology-skill .agents/skills/astrology-skill
```

Claude Code and Pi also read their own project dirs (`.claude/skills/`,
`.pi/skills/`).

### Verify it loaded

After installing, confirm the harness discovered the skill:

```bash
# Pi: list registered skill commands
ls ~/.pi/agent/skills ~/.agents/skills    # astrology-skill present

# Generic: the harness should expose /skill:astrology-skill (Pi) or list the
# skill in its startup roster. Ask the agent: "what skills are available?"
```

Then trigger it with a small chart, e.g.:

```bash
python3 entry_commands.py --route '{
  "reading_type": "natal",
  "chart_data": {
    "house_system": "Whole Sign",
    "placements": [{"body": "Sun", "sign": "Taurus", "degree": 0}]
  }
}'
```

…and ask the agent to interpret the routed chart using the skill.

---

## Usage

### List the available reading functions

Reading types are **enum-driven** off
[`assets/schemas/chart_input_schema.json`](assets/schemas/chart_input_schema.json),
so this command reflects the schema directly:

```bash
python3 entry_commands.py --list
```

Output shows each `reading_type` (`natal`, `transit`, `synastry`,
`solar_return`, `annual_profection`, `horary`, `electional`, `mundane`) mapped
to its retrieval module and entry fragment.

### Route a chart into the workflow (the single entry gate)

`entry_commands.py --route` resolves and validates a chart object, then prints
a **route ticket** that hands control to `SKILL.md` Workflow step 1. It never
calculates. It accepts three input modes:

```bash
# File
python3 entry_commands.py --route chart.json

# Pipe / stdin (no temp file)
... | python3 entry_commands.py --route -

# Inline JSON (small / ad-hoc charts; also works for external-tool output)
python3 entry_commands.py --route '{ "reading_type": "natal", "chart_data": { ... } }'
```

The gate requires `reading_type` (a schema enum value) and a `chart_data`
object. If `jsonschema` is installed it runs full Draft 2020-12 validation;
otherwise a dependency-free structural gate runs (this is the documented
contract, not an error). Every failure exits `2` and points at the schema.

### The full path: birth data → reading

Combine stage 1 (calculator) with stage 2 (entry gate):

```bash
# Stage 1: raw birth data -> chart JSON (AGPL, opt-in; needs the venv)
python3 tools/birth_to_chart.py \
    --date 1990-05-21 --time 14:32 \
    --lat 40.7128 --lon -74.0060 --tz "America/New_York" \
    --house-system "Whole Sign" --reading-type natal \
    --name "Subject A" --place "Brooklyn, NY" \
    --validate --output chart.json

# Stage 2: chart JSON -> route ticket (stdlib; system python3)
python3 entry_commands.py --route chart.json
```

Or as one pipe:

```bash
python3 tools/birth_to_chart.py \
    --date 1990-05-21 --time 14:32 \
    --lat 40.7128 --lon -74.0060 --tz "America/New_York" --validate \
  | python3 entry_commands.py --route -
```

**Stage 3** is the reading itself: the route ticket hands the resolved chart to
`SKILL.md` → Workflow step 1, which builds a reading plan, selects the minimum
references, ranks factors, synthesizes, and runs the reading self-check. The
per-type prompt templates under [`prompts/entry/`](prompts/entry) frame
requests (e.g. horary asks for the querent's question; electional lists
candidate start charts) and add no calculation.

> The calculator **never guesses** a timezone or birth time. Missing `--tz`
> (without `--lmt`) and missing `--time` (without `--noon-for-unknown`) are
> hard errors. When birth-time confidence is `Unknown`, angles/houses/sect are
> omitted and the Moon is flagged provisional. See
> [`tools/README.md`](tools/README.md) for every flag.

### External chart tools

Stage 2 accepts **any** chart JSON that conforms to
`chart_input_schema.json`, not only the bundled calculator's output. The
schema is `additionalProperties: true` everywhere, so external tools may
include extra fields. Example:

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

See [`tests/entry/sample_synastry.json`](tests/entry/sample_synastry.json) for
a richer external-tool-style chart (nested `person_a` / `person_b` blocks plus
inter-chart aspects).

---

## Validation & tests

A single re-runnable matrix runs every deterministic check and prints a
green/red snapshot:

```bash
python3 tests/run_validation_matrix.py
```

Individual checks:

| Command | Needs | What it checks |
|---|---|---|
| `python3 quick_validate.py` | system `python3` | `SKILL.md` frontmatter + entry parity |
| `python3 entry_commands.py --check` | system `python3` | enum ↔ entry-fragment parity |
| `python3 entry_commands.py --list` | system `python3` | enumerate reading functions |
| `python3 tests/entry/smoke_test.py` | system `python3` | full entry surface |
| `python3 tests/entry/end_to_end_test.py` | `.venv` | calculator-backed stages |
| `python3 tools/smoke_test.py` | `.venv` | Asc/MC within ±0.05° on 3 fixtures (independent recomputation) |
| `python3 tests/structure/gap_matrix_drift.py` | system `python3` | reference-gap regression guard |
| `python3 tests/structure/schema_and_agents_parse.py` | `.venv` | schema + `agents/openai.yaml` parse |

See [`docs/e2e_validation_plan.md`](docs/e2e_validation_plan.md) for the full
plan.

---

## Project layout

```
SKILL.md                  Skill doctrine: input contract, workflow, weighting, guardrails, self-check
AGENTS.md                 Agent operating instructions for this repo
entry_commands.py         Entry gate: --list / --check / --route (stdlib; never calculates)
quick_validate.py         Lightweight SKILL.md + entry-parity validator
agents/openai.yaml        Interface metadata for agent hosts
assets/schemas/           chart_input_schema.json (input), reading_plan_schema.json (internal plan)
prompts/entry/            Per-reading-type entry templates + canonical _reading.md
references/               137 interpretive modules (foundations, planets, signs, placements,
                          aspects, rulerships, houses, traditions, reading_types, synthesis_patterns)
tools/                    birth_to_chart.py + smoke tests (AGPL-3.0; opt-in calculator)
docs/                     design notes + end-to-end walkthroughs
tests/                    entry, structure, and forward-testing suites + validation matrix
```

---

## Documentation

- [`SKILL.md`](SKILL.md) — the skill itself (start here).
- [`docs/end_to_end.md`](docs/end_to_end.md) — the full birth-data → reading walkthrough.
- [`docs/entry_commands.md`](docs/entry_commands.md) — entry-command surface design.
- [`docs/birth_to_chart_design.md`](docs/birth_to_chart_design.md) — calculator design + boundary rationale.
- [`tools/README.md`](tools/README.md) — every `birth_to_chart.py` flag.
- [`ROADMAP.md`](ROADMAP.md) — roadmap and phase history.

## License

- The **skill** (`SKILL.md`, `references/`, `prompts/`, `entry_commands.py`,
  schemas, docs) has no bundled license file at the repository root.
- The **calculator** under [`tools/`](tools) is **AGPL-3.0** because it uses
  `pyswisseph` (Swiss Ephemeris). See [`tools/NOTICE.md`](tools/NOTICE.md).
  That AGPL boundary is confined to `tools/` and does not extend to the skill.
