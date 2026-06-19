# Astrology reading request — entry

You are invoking the `astrology-skill`. Route the supplied **pre-calculated**
chart data into the `SKILL.md` retrieval workflow. Do **not** calculate,
rectify, or derive any chart factor — use only what is supplied.

This template is **enum-driven**: it works for every `reading_type` in
`assets/schemas/chart_input_schema.json` without being rewritten. Per-type
framing is layered on by the optional fragment in step 4.

## 1. Resolve the chart input

Accept the chart in any of these forms and resolve it to one object:

1. **Inline JSON** in the fenced block below (`--- BEGIN CHART INPUT ---`).
2. **File path** to a JSON file conforming to
   `assets/schemas/chart_input_schema.json`.
3. **Birth-data script output** — the stdout of `tools/birth_to_chart.py`
   (already schema-conforming; produced by a separate, opt-in process).

If the block contains a path that exists on disk, load that file. Otherwise
treat the block contents as inline JSON.

## 2. Validate (single gate)

The resolved object MUST conform to `assets/schemas/chart_input_schema.json`:

- `reading_type` MUST be one of the values in
  `assets/schemas/chart_input_schema.json` → `properties.reading_type.enum`.
- `chart_data` MUST be present and be an object.

You may run `python3 entry_commands.py --route <chart-or-path>` to resolve and
gate the object deterministically. If validation fails, stop and ask for the
specific missing or invalid fields. Do **not** infer, default, or fill them in.

## 3. Route

Hand the resolved object to **`SKILL.md` → Workflow step 1** ("Parse the
supplied chart data and reading request"). `SKILL.md` owns all retrieval,
factor ranking, synthesis, scope, and self-check behavior. This entry does not
duplicate any of it; it only resolves, validates, and hands off.

## 4. Optional per-type guidance

If `prompts/entry/{reading_type}.md` exists, append its framing to this
request. If it does not exist, proceed with the generic route (this is not an
error — `SKILL.md` already defines the "exact module missing → broader
fallback → name it in the reading plan" behavior).

## Placeholders

The caller or host fills these before the reading runs:

- `{reading_type}` — the value of `reading_type` in the resolved object.
- `{chart_input_or_path_or_script_output}` — inline JSON, a file path, or the
  pre-processor's stdout.

--- BEGIN CHART INPUT ---
{chart_input_or_path_or_script_output}
--- END CHART INPUT ---
