# Astrology Skill Roadmap

This roadmap maps each phase to epics and detailed TDs. A TD is a scoped task definition with a concrete deliverable and acceptance criteria.

## Phase 0: Project Foundation

### Epic P0-E1: Skill Structure

#### TD P0-E1-TD1: Initialize repository structure

Deliverable: Create the base Codex skill project layout.

Acceptance criteria:

- `SKILL.md` exists at the project root.
- `agents/openai.yaml` exists with UI-facing metadata.
- `references/` exists for load-on-demand instruction material.
- `assets/schemas/` exists for structured input and planning schemas.
- `.gitignore` exists with basic local-file exclusions.

#### TD P0-E1-TD2: Validate skill metadata

Deliverable: Ensure the skill can pass basic Codex skill validation.

Acceptance criteria:

- `SKILL.md` frontmatter contains only allowed fields.
- Skill name uses lowercase hyphen-case.
- Skill description clearly states what the skill does and when it should trigger.
- `quick_validate.py` passes.

### Epic P0-E2: Scope and Input Contract

#### TD P0-E2-TD1: Define interpretation boundary

Deliverable: Document that this skill interprets already-calculated chart data rather than calculating charts.

Acceptance criteria:

- `SKILL.md` explicitly prohibits inventing missing placements, house systems, aspects, dignities, lots, birth times, or timing factors.
- `SKILL.md` explains what to do when chart data is incomplete.
- Reading output must preserve uncertainty when source data is partial.

#### TD P0-E2-TD2: Create chart input schema

Deliverable: Define a preferred structured input shape for reading requests.

Acceptance criteria:

- `assets/schemas/chart_input_schema.json` supports reading type, tradition mode, tone, user question, placements, aspects, sect, lots, and timing factors.
- Schema parses as valid JSON.
- Schema allows extra properties so external chart tools can include richer data.

#### TD P0-E2-TD3: Create reading plan schema

Deliverable: Define the internal planning shape used before synthesis.

Acceptance criteria:

- `assets/schemas/reading_plan_schema.json` includes focus, primary factors, resources to load, weighting notes, missing resources, and synthesis warnings.
- Schema parses as valid JSON.
- `SKILL.md` instructs the agent to build this plan before writing the reading.

### Epic P0-E3: Foundation References

#### TD P0-E3-TD1: Add interpretive principles

Deliverable: Create the baseline rules for evidence-based interpretation.

Acceptance criteria:

- `references/foundations/interpretive_principles.md` exists.
- It distinguishes planet, sign, house, aspect, rulership, dignity, sect, and timing.
- It discourages cookbook placement stacking.

#### TD P0-E3-TD2: Add synthesis rules

Deliverable: Create reusable synthesis guidance.

Acceptance criteria:

- `references/foundations/synthesis_rules.md` exists.
- It includes a weighting hierarchy.
- It explains how to use secondary factors to qualify primary factors.

#### TD P0-E3-TD3: Add ethics and scope guardrails

Deliverable: Create safety and uncertainty guidance.

Acceptance criteria:

- `references/foundations/ethics_and_scope.md` exists.
- It prohibits deterministic, diagnostic, medical, legal, financial, and fear-based claims.
- It gives preferred uncertainty language.

## Phase 1: Retrieval Skeleton

### Epic P1-E1: Resource Index and Naming

#### TD P1-E1-TD1: Add resource index

Deliverable: Create `references/resource_index.md`.

Acceptance criteria:

- Index lists every supported resource category.
- Index documents file naming conventions for planets, signs, houses, aspects, rulerships, conditions, traditions, reading types, and synthesis patterns.
- Index distinguishes implemented modules from planned modules.

#### TD P1-E1-TD2: Add module creation checklist

Deliverable: Extend `references/templates/interpretation_module_template.md` or add a companion checklist.

Acceptance criteria:

- Checklist covers core significations, classical notes, modern notes, constructive expression, shadow expression, and synthesis instructions.
- Checklist includes guidance for when a section may be intentionally omitted.
- Checklist keeps modules compact and composable.

### Epic P1-E2: Reading Type Starters

#### TD P1-E2-TD1: Expand natal reading module

Deliverable: Deepen `references/reading_types/natal.md`.

Acceptance criteria:

- Includes standard factor prioritization for self-understanding, vocation, relationships, resources, and home.
- Mentions birth time confidence and house system limits.
- Gives clear retrieval guidance for common natal questions.

#### TD P1-E2-TD2: Add transit reading module

Deliverable: Create `references/reading_types/transit.md`.

Acceptance criteria:

- Separates natal promise from timing triggers.
- Prioritizes transiting outer planets, lunations, station points, angular contacts, and exact aspects when supplied.
- Includes guidance for avoiding event certainty.

#### TD P1-E2-TD3: Add synastry reading module

Deliverable: Create `references/reading_types/synastry.md`.

Acceptance criteria:

- Covers inter-chart aspects, house overlays, repeated relational themes, and asymmetry between partners.
- Includes consent-sensitive language.
- Avoids deterministic compatibility scoring.

#### TD P1-E2-TD4: Add solar return module

Deliverable: Create `references/reading_types/solar_return.md`.

Acceptance criteria:

- Prioritizes solar return Ascendant, chart ruler, Sun condition, angular planets, and links to natal chart.
- Distinguishes annual emphasis from permanent natal character.
- Includes uncertainty rules for relocated versus natal-location returns when unspecified.

#### TD P1-E2-TD5: Add annual profection module

Deliverable: Create `references/reading_types/annual_profection.md`.

Acceptance criteria:

- Covers profected house, Lord of the Year, natal condition, transits to Lord of the Year, and activated topics.
- Explains how to synthesize profection with natal chart data.
- Notes when exact age or birthday timing is missing.

#### TD P1-E2-TD6: Add horary module

Deliverable: Create `references/reading_types/horary.md`.

Acceptance criteria:

- Identifies significators, Moon condition, house relevance, applying aspects, reception, and radicality cautions.
- Uses non-fear-based language for difficult testimony.
- Avoids over-answering when the question, time, or location data is unclear.

#### TD P1-E2-TD7: Add electional module

Deliverable: Create `references/reading_types/electional.md`.

Acceptance criteria:

- Covers goal definition, relevant houses, Moon condition, chart ruler, angularity, malefic mitigation, and benefic support.
- Distinguishes optimization from guarantee.
- Includes guidance for multiple candidate charts.

### Epic P1-E3: Tradition Starters

#### TD P1-E3-TD1: Split classical tradition notes

Deliverable: Expand classical references into focused modules.

Acceptance criteria:

- Add `references/traditions/classical/dignities.md`.
- Add `references/traditions/classical/sect.md`.
- Add `references/traditions/classical/bonification_maltreatment.md`.
- Update `SKILL.md` or `resource_index.md` to point to the split modules.

#### TD P1-E3-TD2: Split modern tradition notes

Deliverable: Expand modern references into focused modules.

Acceptance criteria:

- Add `references/traditions/modern/psychological_framing.md`.
- Add `references/traditions/modern/outer_planets.md`.
- Add `references/traditions/modern/archetypal_language.md`.
- Update `SKILL.md` or `resource_index.md` to point to the split modules.

### Epic P1-E4: Exemplar Modules

#### TD P1-E4-TD1: Add Mars in Cancer exemplar

Deliverable: Create `references/placements/planet_in_sign/mars_cancer.md`.

Acceptance criteria:

- Uses the interpretation module template.
- Includes classical fall condition and modern psychological framing.
- Includes synthesis modifiers for Moon condition, house placement, aspects, sect, dignity, and rulership.

#### TD P1-E4-TD2: Add Saturn in 10th house exemplar

Deliverable: Create `references/placements/planet_in_house/saturn_10th.md`.

Acceptance criteria:

- Covers vocation, responsibility, visibility, delay, mastery, and authority.
- Separates constructive expression from shadow expression.
- Includes modifiers for sect, dignity, angularity, and aspects.

#### TD P1-E4-TD3: Add Mars square Moon exemplar

Deliverable: Create `references/aspects/by_planet_pair/mars_square_moon.md`.

Acceptance criteria:

- Covers emotional reactivity, protection, conflict, assertion, and regulation.
- Includes classical and modern interpretive notes.
- Includes guidance for natal, transit, and synastry contexts.

## Phase 2: Core Natal Library

### Epic P2-E1: Planet Modules

#### TD P2-E1-TD1: Add traditional planet cores

Deliverable: Create core modules for Sun, Moon, Mercury, Venus, Mars, Jupiter, and Saturn.

Acceptance criteria:

- Each module lives under `references/planets/{planet}.md`.
- Each module includes core significations, classical notes, modern notes, constructive expression, shadow expression, and synthesis instructions.
- Each module names key modifiers that change interpretation.

#### TD P2-E1-TD2: Add outer planet cores

Deliverable: Create core modules for Uranus, Neptune, and Pluto.

Acceptance criteria:

- Each module lives under `references/planets/{planet}.md`.
- Each module explains when to use outer planets in classical, modern, and blended readings.
- Each module avoids overpowering chart factors unless angular, exact, repeated, or requested.

### Epic P2-E2: Sign and House Modules

#### TD P2-E2-TD1: Add sign modules

Deliverable: Create one module for each zodiac sign.

Acceptance criteria:

- Each module lives under `references/signs/{sign}.md`.
- Each module includes element, modality, ruler, polarity, core motifs, and interpretive cautions.
- Each module avoids reducing placement interpretation to sign keywords.

#### TD P2-E2-TD2: Add house topic modules

Deliverable: Create one module for each house.

Acceptance criteria:

- Each module lives under `references/houses/{house}.md`.
- Each module includes core topics, angularity/succedent/cadent status, classical notes, modern notes, and common misreadings.
- Each module explains how house topics interact with planetary rulership.

### Epic P2-E3: Aspect Library

#### TD P2-E3-TD1: Add major aspect type modules

Deliverable: Create conjunction, opposition, square, trine, and sextile modules.

Acceptance criteria:

- Each module lives under `references/aspects/{aspect_type}.md`.
- Each module explains aspect dynamics, strength, ease/tension, and synthesis usage.
- Each module accounts for orb and applying/separating status when supplied.

#### TD P2-E3-TD2: Add first planet-pair aspect batch

Deliverable: Create a prioritized batch of planet-pair modules.

Acceptance criteria:

- Include Sun-Moon, Moon-Saturn, Venus-Mars, Mars-Saturn, Mercury-Jupiter, Venus-Saturn, and Mars-Moon major hard/as-needed aspects.
- Use consistent file naming under `references/aspects/by_planet_pair/`.
- Each module includes natal, transit, and synastry notes when relevant.

### Epic P2-E4: Condition Modules

#### TD P2-E4-TD1: Add dignity and debility modules

Deliverable: Create condition modules for domicile, exaltation, detriment, fall, triplicity, term, and face when used.

Acceptance criteria:

- Modules live under `references/placements/planet_condition/` or `references/traditions/classical/`.
- Each module explains interpretive effect without equating dignity with moral goodness.
- `SKILL.md` or `resource_index.md` tells the agent when to retrieve these modules.

#### TD P2-E4-TD2: Add sect and visibility modules

Deliverable: Create modules for sect, angularity, retrograde, combustion, cazimi, and under beams.

Acceptance criteria:

- Each module explains how it modifies planetary expression.
- Each module includes cautions about over-weighting isolated conditions.
- Each module includes examples of synthesis language.

## Phase 3: Topic Synthesis

### Epic P3-E1: Synthesis Pattern Library

#### TD P3-E1-TD1: Add vocation synthesis pattern

Deliverable: Create `references/synthesis_patterns/vocation.md`.

Acceptance criteria:

- Prioritizes 10th house, MC, 10th ruler, Sun, Saturn, 2nd and 6th house links, angularity, and repeated testimony.
- Includes classical and modern synthesis paths.
- Includes guidance for incomplete birth time.

#### TD P3-E1-TD2: Add relationship synthesis pattern

Deliverable: Create `references/synthesis_patterns/relationships.md`.

Acceptance criteria:

- Prioritizes 7th house, 7th ruler, Venus, Mars, Moon, relevant aspects, and repeated relational themes.
- Separates natal relationship patterns from synastry comparison.
- Avoids deterministic compatibility language.

#### TD P3-E1-TD3: Add remaining topic synthesis patterns

Deliverable: Create modules for resources, home, creative work, health routines, spirituality, conflict, strengths, and timing.

Acceptance criteria:

- Each module names primary and secondary chart factors.
- Each module includes retrieval guidance.
- Each module includes safety or uncertainty cautions when relevant.

### Epic P3-E2: Rulership Library

#### TD P3-E2-TD1: Define rulership module template

Deliverable: Add a template for house-ruler placement modules.

Acceptance criteria:

- Template supports `ruler_of_{source_house}_in_{target_house}` modules.
- Template distinguishes the topic being carried from the arena where it manifests.
- Template includes dignity, sect, and aspect modifiers.

#### TD P3-E2-TD2: Add common rulership modules

Deliverable: Create an initial batch of house-ruler combinations.

Acceptance criteria:

- Include common vocation, relationship, resource, and home combinations.
- Use consistent naming under `references/placements/planet_as_house_ruler/`.
- Each module avoids cookbook certainty and points back to full chart synthesis.

### Epic P3-E3: Quality Checks

#### TD P3-E3-TD1: Add synthesis anti-patterns

Deliverable: Create `references/foundations/anti_patterns.md`.

Acceptance criteria:

- Covers over-weighting Sun sign, flattening to placement lists, ignoring house rulers, treating outer planets as always dominant, and inventing missing data.
- Gives correction strategies.
- `SKILL.md` or `resource_index.md` points to it for validation or revision passes.

#### TD P3-E3-TD2: Add reading self-check

Deliverable: Add a final self-check checklist for generated readings.

Acceptance criteria:

- Checklist verifies resource grounding, factor weighting, uncertainty, scope guardrails, and synthesis quality.
- Checklist is short enough to use on every reading.
- Checklist does not require showing internal reasoning to the user.

## Phase 4: Timing and Relationship Workflows

### Epic P4-E1: Transit Workflow

#### TD P4-E1-TD1: Expand transit synthesis guidance

Deliverable: Deepen transit workflow references.

Acceptance criteria:

- Separates natal configuration from active transit.
- Explains how to prioritize exactness, stations, angularity, and repeated timing testimony.
- Includes guidance for time windows without guaranteeing events.

#### TD P4-E1-TD2: Add transit exemplar modules

Deliverable: Add several transit-specific examples.

Acceptance criteria:

- Include Saturn transit to Moon, Jupiter transit to Sun, Mars transit to Ascendant, and Pluto transit to angle examples.
- Each module distinguishes brief, medium, and long-duration transits.
- Each module includes grounded language for uncertainty.

### Epic P4-E2: Profection and Solar Return Workflow

#### TD P4-E2-TD1: Connect profection to natal conditions

Deliverable: Add guidance for interpreting annual profections.

Acceptance criteria:

- Prioritizes profected house and Lord of the Year.
- Connects Lord of the Year natal condition to annual themes.
- Describes how transits to the Lord of the Year modify the reading.

#### TD P4-E2-TD2: Connect solar return to natal chart

Deliverable: Add guidance for solar return synthesis.

Acceptance criteria:

- Prioritizes solar return chart ruler, Sun, Moon, angular planets, and natal contacts.
- Avoids treating solar return chart as standalone fate.
- Includes relocated chart uncertainty language.

### Epic P4-E3: Synastry Workflow

#### TD P4-E3-TD1: Expand synastry synthesis guidance

Deliverable: Deepen relationship comparison rules.

Acceptance criteria:

- Covers inter-chart aspects, house overlays, nodal contacts if supplied, and repeated themes.
- Separates each person's natal baseline from inter-chart dynamics.
- Avoids scoring, fatalism, and one-sided blame.

#### TD P4-E3-TD2: Add synastry exemplar modules

Deliverable: Add first synastry examples.

Acceptance criteria:

- Include Moon-Saturn, Venus-Mars, Sun-Moon, and Mars-Mercury examples.
- Each module includes constructive and challenging expressions.
- Each module includes consent-sensitive and non-deterministic wording.

### Epic P4-E4: Uncertainty Rules

#### TD P4-E4-TD1: Add birth time uncertainty guidance

Deliverable: Create guidance for missing, rounded, or low-confidence birth times.

Acceptance criteria:

- Explains which factors become unreliable.
- Explains which factors remain usable.
- Gives standard language for house and angle uncertainty.

#### TD P4-E4-TD2: Add orb and precision guidance

Deliverable: Create guidance for imprecise aspect data.

Acceptance criteria:

- Explains how exactness affects weight.
- Covers unknown orbs and applying/separating status.
- Instructs the agent not to infer precision that was not supplied.

## Phase 5: Validation and Forward Testing

### Epic P5-E1: Structural Validation

#### TD P5-E1-TD1: Standardize validation command

Deliverable: Document the local validation command.

Acceptance criteria:

- The command accounts for PyYAML availability in the local environment.
- Validation instructions are concise and live in the roadmap or a dedicated development note.
- No extra user-facing docs are added to the skill bundle unless needed.

#### TD P5-E1-TD2: Validate after structural changes

Deliverable: Run validation after schema, frontmatter, or resource-map changes.

Acceptance criteria:

- `quick_validate.py` passes after each structural change.
- JSON schemas parse after schema edits.
- Broken links or renamed resource paths are fixed before handoff.

### Epic P5-E2: Forward Testing

#### TD P5-E2-TD1: Create test prompts

Deliverable: Prepare realistic structured reading prompts.

Acceptance criteria:

- Include at least one natal vocation prompt.
- Include at least one transit prompt.
- Include at least one synastry prompt.
- Include at least one incomplete-data prompt.

#### TD P5-E2-TD2: Run independent forward tests

Deliverable: Use fresh agent contexts to test whether the skill guides realistic readings.

Acceptance criteria:

- Test prompts provide the skill and raw chart data without leaking expected answers.
- Results are evaluated for resource selection, synthesis, weighting, uncertainty, and guardrail compliance.
- Findings lead to concrete SKILL.md or reference updates.

### Epic P5-E3: Tooling Decision

#### TD P5-E3-TD1: Decide on resource index helper

Deliverable: Decide whether to add a script that scans references and generates an index.

Acceptance criteria:

- Decision is based on resource count and maintenance burden.
- If added, script is deterministic and tested.
- If deferred, manual index maintenance rules are documented.

#### TD P5-E3-TD2: Decide on module name validator

Deliverable: Decide whether to add a script that validates naming conventions.

Acceptance criteria:

- Decision is based on how often module names drift.
- If added, script checks expected directories and naming patterns.
- If deferred, naming expectations remain clear in `references/resource_index.md`.
