# Published skill bundle profile

`install.sh` publishes a lean agent-loaded bundle by allowlist. The installed
copy is meant to contain only runtime skill material plus the small amount of
user-facing documentation needed to understand and verify the entry surface.

## Included

- `SKILL.md`
- `LICENSE`
- `README.md`
- `entry_commands.py`
- `agents/openai.yaml`
- `assets/schemas/`
- `prompts/entry/`
- `references/`
- `docs/bundle_profile.md`
- `docs/birth_to_chart_design.md`
- `docs/entry_commands.md`
- `docs/end_to_end.md`
- `docs/report_format.md`

These paths cover the files referenced by `SKILL.md`, the entry-command
metadata consumed by agent hosts, the schemas used by the entry/report gates,
and the report template under `references/templates/`.

## Excluded

Development-only repository context is not copied into Codex, Pi, or
`~/.agents` targets. That includes `AGENTS.md`, `ROADMAP.md`, `tests/`,
`tests/forward_testing/`, `.todos`, VCS/editor/cache files, and non-runtime
tooling such as `tools/`.

The `tools/` calculator remains opt-in and separate from the agent-loaded skill
bundle. `docs/birth_to_chart_design.md` is included because installed metadata
points at its boundary rationale; calculator implementation docs remain in the
development repository.

## Verification

Dry-run mode prints the publish allowlist without copying files:

```bash
./install.sh --dry-run
```

Smoke-test mode stages the same bundle profile in a temporary directory and
runs the installed copy's entry parity check:

```bash
./install.sh --smoke-test
```

Real installs also run `python3 entry_commands.py --check` from the destination
after copying.

If the official Agent Skills reference validator is installed, the development
matrix can validate either this repository root or a staged/published bundle:

```bash
python3 tests/run_validation_matrix.py
SKILLS_REF_TARGET=/path/to/published/astrology-skill \
  python3 tests/structure/skills_ref_validate.py
```

When `skills-ref` is absent, the wrapper reports `SKIP` with install guidance
instead of failing. Treat any installed-validator finding as actionable: either
teach `quick_validate.py` the same local rule or record why the official and
local checks intentionally differ.
