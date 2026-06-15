# Resource Index

Use this index to locate bundled interpretation resources and to name new modules consistently. Prefer the most specific implemented module that matches the supplied chart data; when no exact module exists, fall back to a broader implemented module and record the missing exact resource in the reading plan.

## Status key

- Implemented: file or directory exists in this repository.
- Planned: supported by the skill contract or roadmap, but not yet present.

## Implemented modules

### Foundations

Foundational references are always loaded before synthesis.

- `references/foundations/interpretive_principles.md`
- `references/foundations/synthesis_rules.md`
- `references/foundations/ethics_and_scope.md`

### Traditions

Use these when `tradition_mode` is `classical`, `modern`, or `blended`.

- `references/traditions/classical.md`
- `references/traditions/modern.md`

### Reading types

Use the module matching the requested `reading_type` when it exists.

- `references/reading_types/natal.md`

### Templates

Use templates when creating new composable interpretation modules.

- `references/templates/interpretation_module_template.md`

## Planned modules

These categories are supported by the skill workflow and should be added with the naming conventions below.

### Planets

Planet core modules define baseline function, motivations, topics, and interpretive cautions.

- Directory: `references/planets/`
- Pattern: `references/planets/{planet}.md`
- Example: `references/planets/mars.md`
- Planned names: `sun.md`, `moon.md`, `mercury.md`, `venus.md`, `mars.md`, `jupiter.md`, `saturn.md`, `uranus.md`, `neptune.md`, `pluto.md`

### Signs

Sign modules define style, temperament, modality, element, and expression.

- Directory: `references/signs/`
- Pattern: `references/signs/{sign}.md`
- Example: `references/signs/cancer.md`
- Planned names: `aries.md`, `taurus.md`, `gemini.md`, `cancer.md`, `leo.md`, `virgo.md`, `libra.md`, `scorpio.md`, `sagittarius.md`, `capricorn.md`, `aquarius.md`, `pisces.md`

### Houses

House modules define topics, angularity, life areas, and interpretive scope.

- Directory: `references/houses/`
- Pattern: `references/houses/{house}.md`
- Example: `references/houses/10th.md`
- Planned names: `1st.md`, `2nd.md`, `3rd.md`, `4th.md`, `5th.md`, `6th.md`, `7th.md`, `8th.md`, `9th.md`, `10th.md`, `11th.md`, `12th.md`

### Planet in sign placements

Use for exact planet-sign combinations.

- Directory: `references/placements/planet_in_sign/`
- Pattern: `references/placements/planet_in_sign/{planet}_{sign}.md`
- Example: `references/placements/planet_in_sign/mars_cancer.md`
- Naming: lowercase planet, underscore, lowercase sign.

### Planet in house placements

Use for exact planet-house combinations.

- Directory: `references/placements/planet_in_house/`
- Pattern: `references/placements/planet_in_house/{planet}_{house}.md`
- Example: `references/placements/planet_in_house/saturn_10th.md`
- Naming: lowercase planet, underscore, ordinal house number (`1st` through `12th`).

### Rulerships

Use for house ruler placement and rulership-based synthesis.

- Directory: `references/placements/planet_as_house_ruler/`
- Pattern: `references/placements/planet_as_house_ruler/{source_house}_ruler_in_{placement_house}.md`
- Example: `references/placements/planet_as_house_ruler/7th_ruler_in_10th.md`
- Naming: ordinal source house, `_ruler_in_`, ordinal placement house.

### Conditions

Use for dignity, debility, sect, reception, angularity, retrograde condition, combustion, visibility, bonification, maltreatment, and related condition modifiers.

- Directory: `references/placements/planet_condition/`
- Pattern: `references/placements/planet_condition/{condition}.md`
- Examples: `references/placements/planet_condition/fall.md`, `references/placements/planet_condition/sect.md`, `references/placements/planet_condition/retrograde.md`
- Naming: lowercase snake_case condition name.

### Aspects

Aspect type modules describe the aspect's general interpretive mechanics.

- Directory: `references/aspects/`
- Pattern: `references/aspects/{aspect_type}.md`
- Examples: `references/aspects/conjunction.md`, `references/aspects/square.md`
- Planned aspect type names: `conjunction.md`, `sextile.md`, `square.md`, `trine.md`, `opposition.md`

Planet pair aspect modules describe exact combinations.

- Directory: `references/aspects/by_planet_pair/`
- Pattern: `references/aspects/by_planet_pair/{planet1}_{aspect}_{planet2}.md`
- Example: `references/aspects/by_planet_pair/mars_square_moon.md`
- Naming: lowercase planet, aspect type, lowercase planet, separated by underscores. Preserve the order used by the source chart data unless a module already exists in the reverse order.

### Traditions

Tradition modules describe method-specific rules and language.

- Current broad pattern: `references/traditions/{tradition}.md`
- Current examples: `references/traditions/classical.md`, `references/traditions/modern.md`
- Planned focused pattern: `references/traditions/{tradition}/{topic}.md`
- Planned examples: `references/traditions/classical/dignities.md`, `references/traditions/classical/sect.md`, `references/traditions/classical/bonification_maltreatment.md`, `references/traditions/modern/psychological_framing.md`, `references/traditions/modern/outer_planets.md`, `references/traditions/modern/archetypal_language.md`
- Naming: lowercase tradition directory, lowercase snake_case topic file.

### Reading types

Reading type modules define retrieval priorities, uncertainty rules, and synthesis emphasis for a request type.

- Directory: `references/reading_types/`
- Pattern: `references/reading_types/{reading_type}.md`
- Implemented: `references/reading_types/natal.md`
- Planned names: `transit.md`, `synastry.md`, `solar_return.md`, `annual_profection.md`, `horary.md`, `electional.md`
- Naming: lowercase snake_case reading type.

### Synthesis patterns

Synthesis pattern modules describe how to combine repeated chart factors around a topic or interpretive problem.

- Directory: `references/synthesis_patterns/`
- Pattern: `references/synthesis_patterns/{topic}.md`
- Examples: `references/synthesis_patterns/vocation.md`, `references/synthesis_patterns/relationships.md`, `references/synthesis_patterns/resources.md`
- Naming: lowercase snake_case topic name.

## Naming rules

- Use lowercase filenames.
- Use snake_case for multiword names.
- Use ordinal house labels: `1st`, `2nd`, `3rd`, `4th`, `5th`, `6th`, `7th`, `8th`, `9th`, `10th`, `11th`, `12th`.
- Use exact planet and sign names rather than glyphs or abbreviations.
- Keep one interpretive unit per file so modules remain composable.
- Prefer exact modules over broad modules during retrieval, but do not invent missing chart data to reach an exact module.
