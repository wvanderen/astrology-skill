---
name: astrology-skill
description: Retrieval-first astrological interpretation for already-calculated chart data. Use when the user provides placements, houses, aspects, dignities, sect, rulerships, transits, synastry factors, profections, solar returns, horary details, electional constraints, or a structured astrology reading request and wants a synthesized reading rather than chart calculation.
---

# Astrology Skill

Use this skill to interpret astrological data that has already been calculated. This skill does not calculate charts, rectify birth times, derive house cusps, determine house systems, compute aspects, assign dignities, calculate lots, infer sect, generate timing factors, or fill in missing birth data.

## Core Rule

Perform a controlled interpretive retrieval pass before writing the reading. Identify the relevant chart factors, load only the matching references, rank the factors, then synthesize. Do not free-associate astrology from general model knowledge when a relevant bundled reference exists.

## Input Contract

Expect any mix of:

- `reading_type`: `natal`, `transit`, `synastry`, `solar_return`, `annual_profection`, `horary`, or `electional`
- `tradition_mode`: `classical`, `modern`, or `blended`
- `tone`: `practical`, `poetic`, `psychological`, `technical`, or `beginner-friendly`
- `chart_data`: ascendant, MC, sect, house system, placements, houses, aspects, dignities, lots, rulerships, timing factors, and source notes
- `user_question`: the user's explicit focus

If chart data is incomplete, interpret only the factors that are explicitly provided and state which judgments cannot be made from the source data. Do not invent, assume, derive, or "fill in" missing placements, house systems, houses, aspects, dignities, debilities, lots, birth times, sect, rulership conditions, profections, directions, transits, returns, horary significators, electional constraints, or other timing factors.

When a requested reading depends on missing data:

- Ask for the missing chart data if it is essential to the user's question.
- Offer a narrower reading from the available factors when useful.
- Label any partial interpretation as provisional.
- Preserve uncertainty in the final reading with scope language such as "from the supplied placements," "if this aspect is confirmed," or "house-based topics cannot be assessed without houses."

Use `assets/schemas/chart_input_schema.json` as the preferred structured input shape when a user asks how to provide data.

## Workflow

1. Parse the supplied chart data and reading request.
2. Identify the reading type, tradition mode, tone, and explicit user focus.
3. Build an internal reading plan using `assets/schemas/reading_plan_schema.json` before drafting the reading. Include the focus, primary factors, resources to load, weighting notes, missing resources, and synthesis warnings.
4. Select the minimum necessary references:
   - Always load `references/foundations/interpretive_principles.md`.
   - Always load `references/foundations/synthesis_rules.md`.
   - Always load `references/foundations/ethics_and_scope.md`.
   - Load `references/reading_types/{reading_type}.md` when it exists.
   - Load tradition-specific references when the user requests classical, modern, or blended interpretation.
   - Load placement, aspect, rulership, condition, or topic references when they exist and match the chart factors.
5. Rank the chart factors by relevance and weight.
6. Synthesize across factors instead of listing cookbook meanings.
7. Answer in the requested tone while preserving uncertainty and scope limits.

The reading plan is normally internal. Show it only if the user asks for method, traceability, or a reading outline.

## Resource Selection

Prefer exact, composable modules over broad summaries:

- Planet core: `references/planets/{planet}.md`
- Sign emphasis: `references/signs/{sign}.md`
- Planet in sign: `references/placements/planet_in_sign/{planet}_{sign}.md`
- Planet in house: `references/placements/planet_in_house/{planet}_{house}.md`
- Ruler placement: `references/placements/planet_as_house_ruler/{house}_ruler_in_{house}.md`
- Planet condition: `references/placements/planet_condition/{condition}.md`
- Aspect type: `references/aspects/{aspect_type}.md`
- Planet pair aspect: `references/aspects/by_planet_pair/{planet1}_{aspect}_{planet2}.md`
- Topic synthesis: `references/synthesis_patterns/{topic}.md`

When an exact module does not exist, use the closest available broader module and make the limitation explicit in the reading plan.

## Weighting Hierarchy

Give strongest weight to:

1. The user's explicit question.
2. The reading type.
3. Angles, angular planets, and angular rulers.
4. House rulers relevant to the question.
5. Exact aspects and applying/separating dynamics when supplied.
6. Sect, dignity, debility, reception, and condition.
7. Repeated themes across multiple indicators.
8. Outer planets, asteroids, minor points, and speculative factors only when requested or clearly relevant.

Classical astrology describes condition, function, concrete topics, timing, and external circumstances. Modern astrology describes inner experience, developmental themes, archetypal meaning, and psychological integration. In blended mode, let classical condition shape concrete judgment and modern symbolism shape experiential language.

## Output Guardrails

- Separate observation from interpretation.
- Phrase difficult indications as tendencies, pressures, or themes.
- Mention conflicting indicators as tensions to integrate, not contradictions to erase.
- Avoid fatalistic claims or certainty about events.
- Do not diagnose medical or mental health conditions.
- Do not tell users to make medical, legal, financial, or major relationship decisions solely from astrology.
- Avoid fear-based language in horary, electional, transit, or timing work.
- Name uncertainty when chart data is incomplete or source quality is unclear.
