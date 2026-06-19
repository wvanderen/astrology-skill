# Reference Gap Matrix

Use this matrix to prioritize enrichment of the bundled reference library. It
compares every implemented reference category against the source canon
(`references/source_canon_and_rights_ledger.md`), the retrieval contract in
`SKILL.md`, the naming/coverage notes in `references/resource_index.md`, the
`ROADMAP.md` phase structure, and the templates in `references/templates/`.

This is a planning artifact, not doctrine. It records where depth is thin,
which source families can safely fill the gap, and which modules should stay
compact. Draw the doctrine itself in the Phase 3 and Phase 4 extraction tasks,
not here.

## How to use

- Before enriching a module, read its row, confirm the source family in the
  rights ledger, and follow the ledger's extraction and paraphrase rules.
- Match the priority tier to the downstream phase TD: Phase 5 (core natal),
  Phase 6 (conditions, rulerships, aspect combinations), Phase 7 (reading
  workflows and topic synthesis).
- Prefer depth and consistency over breadth. The skill's compositional model
  already falls back from an exact module to broader planet, sign, house,
  aspect-type, and synthesis modules, so coverage gaps are lower-risk than
  depth gaps in frequently retrieved modules.

## Vocabulary

- Depth: `Starter` (thin skeleton), `Moderate` (serviceable, template-complete),
  `Rich` (already deepened with prose and worked modifiers), `Mixed` (varies by
  file).
- Priority: `P0 first-wave`, `P1 second-wave`, `P2 on-demand`, `P3 keep-compact`.
- Risk: `Low` (safe to enrich with paraphrase), `Medium` (watch for bloat, tone
  drift, or copyright), `High` (ethics-sensitive, copyright-sensitive, or bloat-
  prone; enrich carefully and narrowly).

## Summary matrix

| Category | Modules | Depth | Coverage | Priority | Risk | Headline gap |
| --- | --- | --- | --- | --- | --- | --- |
| Foundations | 6 | Mixed | Full | P3 | Low | Anchors intentionally terse; only light spot-enrich |
| Traditions, broad | 2 | Starter | Full | P3 | Low | Routing stubs; weight belongs in focused modules |
| Traditions, classical focused | 3 | Starter–Moderate | Core only | P1 | Medium | Classical condition/aspect/reception doctrine thin |
| Traditions, modern focused | 3 | Starter | Core only | P2 | Medium | Public-domain modern psychological language under-used |
| Planets | 10 | Moderate | Full (7 trad + 3 outer) | P1 | Low | Serviceable; lacks classical nature + sect-depth |
| Signs | 12 | Starter | Full | P0 | Medium | No Ptolemaic sign-powers or modern-ruler doctrine |
| Houses | 12 | Moderate | Full | P0 | Medium | No classical house doctrine, joys, or derived houses |
| Aspect types | 5 | Moderate | Full | P2 | Low | Good; light classical aspect-theory layer optional |
| Planet-pair aspects | 26 | Starter (1 Rich) | Partial pairs | P1 | Medium | Depth-consistency gap vs the one rich exemplar |
| Planet in sign | 3 | Moderate | 3 of 120 | P2 | Low | On-demand exemplar strategy; do not fill all 120 |
| Planet in house | 2 | Moderate | 2 of 120 | P2 | Low | On-demand exemplar strategy; do not fill all 120 |
| Conditions | 13 | Starter | Full names | P0 | Medium | Full set, thin each; classical dignity/sect/orb depth |
| Rulerships | 7 | Moderate | 7 traditional | P2 | Medium | Outer-planet modern rulership notes missing |
| Reading types | 9 | Rich | Full | P3 | Low | Already deepened; spot-fix only |
| Synthesis patterns | 12 | Mixed | Broad | P2/P3 | Medium | 8 compact topics; enrich selectively, keep narrow ones compact |

Counts: 125 reference modules plus templates and this matrix.

## Category detail

### Foundations

- Modules: `interpretive_principles`, `synthesis_rules`, `ethics_and_scope`,
  `anti_patterns`, `birth_time_uncertainty`, `aspect_precision`.
- Current depth: Mixed. `anti_patterns` (6.2 KB) and `birth_time_uncertainty`
  (6.5 KB) are already rich; `interpretive_principles` (2.0 KB) and
  `ethics_and_scope` (2.0 KB) are intentionally compact anchors.
- Missing classical doctrine: none load-bearing. Ethics anchors should stay
  tradition-neutral.
- Missing modern language: none load-bearing.
- Missing synthesis modifiers: `synthesis_rules` could cross-reference the
  timing-pattern weighting once; optional.
- Source candidates: not source-bound. Cross-check `ethics_and_scope` against
  the rights-ledger cautions when tone is adapted from historical sources.
- Risk: Low. Bloat risk if anchors grow.
- Priority: P3 keep-compact. Enrich only the `anti_patterns` and
  `birth_time_uncertainty` modules if forward testing exposes new drift.

### Traditions, broad

- Modules: `traditions/classical.md`, `traditions/modern.md`.
- Current depth: Starter (~0.6 KB each); emphasis + cautions only.
- Missing classical doctrine: deliberately delegated to focused modules.
- Missing modern language: deliberately delegated to focused modules.
- Missing synthesis modifiers: none; these are routing fallbacks.
- Source candidates: none directly; point to focused modules and the rights
  ledger.
- Risk: Low. Broad stubs should stay compact so focused modules carry weight.
- Priority: P3 keep-compact. Keep as fallback routing; do not fold focused
  doctrine back in.

### Traditions, classical focused

- Modules: `classical/dignities`, `classical/sect`, `classical/bonification_maltreatment`.
- Current depth: Starter–Moderate (2.0–3.0 KB). `dignities` is the strongest;
  `sect` is 38 lines and thin for the centerpiece of classical condition.
- Missing classical doctrine: sect-depth (benefic/malefic sect reversal,
  trigon/triplicity lords as a sect-adjacent timing idea, solar vs lunar sect
  mechanics); reception mechanics and mutual reception examples; a fuller
  bonification/maltreatment vocabulary ( enclosure, witnessing, hurling rays,
  dexter/sinister aspects).
- Missing modern language: translation notes so classical terms stay readable
  in blended readings.
- Missing synthesis modifiers: how sect and reception modify planet-in-house,
  rulership, and aspect modules (cross-links).
- Source candidates: Ptolemy (sect-adjacent diurnal/nocturnal, dignities,
  aspects — Strong); Valens (practical sect/time-lord use — Strong, paraphrase
  only); Lilly (reception, application/separation, dignity/debility — Strong,
  PD English).
- Risk: Medium. Sect and reception are easy to flatten or modernize past
  recognition; keep terminology distinct per ledger cautions.
- Priority: P1 second-wave (Phase 6).

### Traditions, modern focused

- Modules: `modern/psychological_framing`, `modern/outer_planets`,
  `modern/archetypal_language`.
- Current depth: Starter (1.8–2.2 KB).
- Missing classical doctrine: none required; keep modern modules tradition-
  aware so blended readings stay grounded.
- Missing modern language: richer, public-domain modern psychological and
  archetypal vocabulary; early twentieth-century character/synthesis language
  adapted to non-deterministic framing; clearer outer-planet integration rules.
- Missing synthesis modifiers: how outer planets modify planet, sign, house,
  and aspect modules only when angular, exact, repeated, or requested.
- Source candidates: Alan Leo PD corpus (Strong for psychological language;
  verify edition <=1930 per ledger); Raphael/Cross and Sepharial (Some, as
  secondary modern-popular witnesses).
- Risk: Medium. Theosophical, gendered, and moralizing tone in PD modern
  sources needs adaptation to the skill's ethics style.
- Priority: P2 on-demand (Phase 7).

### Planets

- Modules: all ten cores (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn,
  Uranus, Neptune, Pluto).
- Current depth: Moderate and uniform (~4.3–4.9 KB); template-complete.
- Missing classical doctrine: Ptolemaic planetary natures (hot/cold/moist/dry,
  benefic/malefic baseline); Valens-style practical combinations; fuller sect
  treatment per planet; traditional congenial/enmity and reception defaults.
- Missing modern language: outer-planet modern framing already present but
  could be deepened for Uranus/Neptune/Pluto from PD modern sources.
- Missing synthesis modifiers: cross-links to condition, rulership, and
  planet-pair modules are present but could name the most common modifier
  chains more tightly.
- Source candidates: Ptolemy (Strong); Valens (Strong, paraphrase); Lilly
  (Strong for the seven traditional planets); Alan Leo (Strong for outer
  planets and psychological framing).
- Risk: Low. Modules are stable and template-bound; enrichment is additive.
- Priority: P1 second-wave (Phase 5). Light enrichment; do not convert into
  monographs.

### Signs

- Modules: all twelve.
- Current depth: Starter and uniform (~1.3–1.5 KB). Element, modality, ruler,
  polarity, core motifs, cautions, and a short synthesis section only.
- Missing classical doctrine: Ptolemaic sign-powers — commanding/obeying,
  masculine/feminine sign pairs, solid/bicorporeal/solstitial/equinoctial,
  signs that hear/see each other, hot/cold/moist/dry and humoral associations,
  bodily and place associations. Confirmed absent by grep (0/12 mention
  commanding, obeying, humoral, decan/face, triplicity, or exaltation).
- Missing modern language: modern outer-planet rulership nuance (e.g., modern
  co-rulership notes for Scorpio, Aquarius, Pisces) framed as optional modern
  testimony, not as default rulership.
- Missing synthesis modifiers: how sign qualities modify dignity, reception,
  aspect (e.g., aspect reception by sign, commanding/obeying pair dynamics),
  and triplicity-by-sect context.
- Source candidates: Ptolemy Tetrabiblos Book I (Strong; confirmed chapters:
  solid/bicorporeal, masculine/feminine signs, commanding/obeying signs in the
  LacusCurtius Robbins table of contents, PD via non-renewal per ledger);
  Lilly (Strong for sign-ruler practice); Alan Leo (Strong for modern ruler
  nuance).
- Risk: Medium. Signs are high-frequency reference cards; enrichment must add
  doctrine without bloating into glossaries. Keep modern-ruler notes clearly
  optional and do not override chart-specific rulership.
- Priority: P0 first-wave (Phase 5).

### Houses

- Modules: all twelve.
- Current depth: Moderate and uniform (~2.0–2.4 KB). Topics, angularity,
  classical notes, modern notes, common misreadings, rulership interaction.
- Missing classical doctrine: classical topic lists (Valens/Firmicus/Lilly),
  planetary joys, derived/turned houses for relationship, horary, and synastry
  work, aversion/inconjunct relationship to the ascendant, the four angles and
  pivot/succedent/cadent strength (terminology present in 8/12 but
  underdeveloped), good and bad houses by aspect to the ascendant.
- Missing modern language: psychological framing of each house as a
  developmental field; already lightly present, could be deepened.
- Missing synthesis modifiers: how house strength modifies planets, rulers,
  and aspects; how turned houses feed synastry, horary, and profection
  modules.
- Source candidates: Valens (Some–Strong for practical houses); Firmicus
  (Strong for houses, tone caution); Lilly (Strong for houses, horary turned
  houses); Bonatti (Strong for questions/turned houses).
- Risk: Medium. Fatalistic and status-conscious classical house language needs
  adaptation; turned-house doctrine must stay clearly tied to supplied reading
  type.
- Priority: P0 first-wave (Phase 5).

### Aspect types

- Modules: conjunction, opposition, square, trine, sextile.
- Current depth: Moderate (~4.2–5.0 KB); dynamics, ease/tension, orb, and
  applying/separating guidance present.
- Missing classical doctrine: Ptolemaic aspect theory (configuring signs,
  hearing/seeing, dexter/sinister or right/left aspects, bodily vs. sign-based
  aspects); witness and testimony language.
- Missing modern language: minimal; aspect-type modules are mechanics, not
  psychological content.
- Missing synthesis modifiers: cross-link to `aspect_precision.md` and the
  applying/separating timing notes in planet-pair modules.
- Source candidates: Ptolemy (Strong); Valens (Strong for practical aspect
  use); Lilly (Strong for applying/separation and reception in aspects).
- Risk: Low. Modules are stable; enrichment is a light classical layer.
- Priority: P2 on-demand (Phase 6). Optional; do not bloat.

### Planet-pair aspects

- Modules: 26 in `aspects/by_planet_pair/`; one rich exemplar
  (`mars_square_moon.md`, 8.0 KB), 25 starters (~2.2–2.8 KB).
- Current depth: Mixed. All 26 already include transit, synastry, reception,
  and sect sections (confirmed by grep), so the gap is depth and modifier
  richness, not missing structure.
- Missing classical doctrine: reception-led cooperation vs. friction
  judgments; applying/separating and dexter/sinister timing; sect-modified
  benefic/malefic contact; enclosure and witnessing language for hard pairs.
- Missing modern language: developmental and regulatory framing consistent
  with the `mars_square_moon` exemplar across natal, transit, and synastry.
- Missing synthesis modifiers: house-ruled/occupied routing, dignity and
  reception modifiers, and reading-type-specific weighting in the starters.
- Source candidates: Ptolemy (Strong); Valens (Strong for combinations);
  Lilly (Strong, PD English for aspect/reception mechanics); Alan Leo (Some
  for relational psychological framing).
- Risk: Medium. Twenty-six files; bring the most-frequently-retrieved pairs
  toward exemplar depth rather than enriching all uniformly. Watch tone in
  relational pairs (synastry ethics).
- Priority: P1 second-wave (Phase 6). Prioritize Sun-Moon, Moon-Saturn,
  Venus-Mars, Venus-Saturn, Mars-Saturn, Mars-Moon first.
- Coverage note: named P2-E3-TD2 pairs are complete (Sun-Moon, Moon-Saturn,
  Venus-Mars, Mars-Saturn, Mercury-Jupiter, Venus-Saturn, Mars-Moon each have
  conjunction/square/opposition where applicable). Missing pairs (e.g.,
  Jupiter-Saturn, Sun-Jupiter, Moon-Venus) are on-demand; the compositional
  fallback to aspect-type + planet modules covers them.

### Planet in sign placements

- Modules: 3 of 120 (`mercury_gemini`, `mars_cancer`, `mars_virgo`).
- Current depth: Moderate (4.4–5.0 KB), template-complete exemplars.
- Missing classical doctrine: dignity/debility-specific treatment per
  combination (e.g., fall, domicile, exaltation, detriment effects in sign).
- Missing modern language: psychological integration notes per combination.
- Missing synthesis modifiers: house, ruler, sect, aspect, and reception
  modifiers per the template.
- Source candidates: Valens (Strong for planet-in-sign delineation); Lilly
  (Strong); Alan Leo (Strong for modern character language).
- Risk: Low. On-demand; adding modules is low-risk but low-priority.
- Priority: P2 on-demand (Phase 5). Do not fill all 120; add only
  high-frequency or high-doctrine combinations when forward testing or user
  requests surface them.

### Planet in house placements

- Modules: 2 of 120 (`saturn_10th`, `mercury_10th`).
- Current depth: Moderate (4.9–5.6 KB), template-complete exemplars.
- Missing classical doctrine: angularity-specific and topic-specific
  classical treatment per combination.
- Missing modern language: developmental framing of the planet-house field.
- Missing synthesis modifiers: ruler, sect, dignity, aspect, and reception
  modifiers per the template.
- Source candidates: Valens (Some–Strong); Firmicus (Strong, tone caution);
  Lilly (Strong); Bonatti (Strong for angular and question houses).
- Risk: Low. On-demand.
- Priority: P2 on-demand (Phase 5). Same exemplar strategy as planet-in-sign.

### Conditions (planet_condition)

- Modules: 13 — domicile, exaltation, detriment, fall, triplicity, term, face,
  sect, angularity, retrograde, combustion, cazimi, under_beams.
- Current depth: Starter and uniform (1.4–2.3 KB). Full naming set; thin each.
  Only `cazimi`, `combustion`, and `under_beams` cite specific orb numbers.
- Missing classical doctrine: per-condition classical depth — triplicity-by-sect
  and trigon lord mechanics; bound/term lord management; face/decan role;
  peregrine judgment; cazimi/combustion/under-beams orb precision with source
  attribution (Lilly convention: cazimi within ~17', combustion within ~8.5 deg,
  under the beams toward ~15 deg); retrograde and station meaning; angularity
  strength gradation.
- Missing modern language: developmental translation of each condition (e.g.,
  fall as lowered recognition, exaltation as aspirational pressure) — lightly
  present, could be deepened.
- Missing synthesis modifiers: how each condition modifies planet, rulership,
  aspect, and timing modules; interaction with sect and reception; clear "do
  not derive minor dignity from missing data" guardrails (already present in
  `dignities.md`, repeat per condition where relevant).
- Source candidates: Ptolemy (Strong for dignities/aspects); Valens (Strong for
  practical condition); Firmicus (Strong, tone caution); Lilly (Strong for
  combustion/cazimi/reception/retrograde, PD English); Bonatti (Strong for
  condition and questions).
- Risk: Medium. Combustion/cazimi orb numbers are convention-sensitive; cite
  the source family and keep the skill's "do not derive missing data" rule.
- Priority: P0 first-wave (Phase 6).

### Rulerships

- Modules: 7 — Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn
  (planet-led, house-by-house).
- Current depth: Moderate (3.5–4.0 KB).
- Missing classical doctrine: reception and mutual-reception effects on the
  ruled house; turned-house rulership links for horary and synastry; sect and
  dignity effects on the ruler's administration.
- Missing modern language: outer-planet rulership notes (Uranus, Neptune,
  Pluto) for modern or blended charts where an outer planet is the supplied
  modern ruler of a house — framed as optional modern testimony, not default.
- Missing synthesis modifiers: cross-links to the ruler's placement, dignity,
  reception, and aspect modules are present; could be tightened.
- Source candidates: Ptolemy (Strong); Valens (Strong); Lilly (Strong,
  PD English); Bonatti (Strong for questions/rulers); Alan Leo (Some for
  outer-planet modern rulership).
- Risk: Medium. Do not assert natural-house rulership as chart-specific; keep
  modern outer rulers clearly optional and tied to supplied data.
- Priority: P2 on-demand (Phase 6).

### Reading types

- Modules: 9 — natal, transit, transit_examples, synastry, synastry_examples,
  solar_return, annual_profection, horary, electional.
- Current depth: Rich (4.9–13.9 KB); the deepest category.
- Missing classical doctrine: minimal; horary and electional already lean on
  Lilly-style method. Could add Valens time-lord framing to annual_profection.
- Missing modern language: minimal; natal and synastry already integrate
  modern framing.
- Missing synthesis modifiers: cross-links to the timing, relationships, and
  vocation synthesis patterns are present.
- Source candidates: Lilly (Strong for horary/electional, PD English); Valens
  (Strong for profections/time-lords, paraphrase); Ptolemy (Some for
  directions/returns).
- Risk: Low. Bloat risk if these grow further.
- Priority: P3 keep-compact / spot-fix only. Enrich only if forward testing
  finds a concrete gap.

### Synthesis patterns

- Modules: 12 — vocation, consulting_advisory_vocation,
  professional_collaboration, relationships, resources, home, creative_work,
  health_routines, spirituality, conflict, strengths, timing.
- Current depth: Mixed. Four rich (vocation 7.2 KB, consulting 6.3 KB,
  professional_collaboration 6.0 KB, relationships 10.2 KB); eight compact
  starters (2.4–2.7 KB).
- Missing classical doctrine: classical topic routing for the compact
  patterns (e.g., home = 4th, resources = 2nd, creative_work = 5th, health =
  6th) is implied; could be stated with ruler and aspect testimony.
- Missing modern language: developmental framing for the compact patterns.
- Missing synthesis modifiers: retrieval order, primary vs. secondary
  testimony, and uncertainty cautions are present but thin in the eight
  starters.
- Source candidates: Ptolemy (Strong for natal topics); Valens (Strong);
  Lilly (Strong for topic questions); Alan Leo (Strong for synthesis/
  character language).
- Risk: Medium. Eight compact patterns could be enriched selectively; keep
  narrow ones (strengths, conflict, timing) compact if inherently focused.
- Priority: P2/P3 (Phase 7). Enrich the topic patterns that forward testing
  shows are under-served; leave the rest compact.

## First enrichment wave

Work these first because they are high-frequency retrieval targets with clear,
source-vetted classical doctrine gaps. Each maps to a downstream phase TD.

P0 first-wave:

- Signs (Phase 5, `td-722c1d`): add Ptolemaic sign-powers doctrine
  (commanding/obeying, masculine/feminine pairs, solid/bicorporeal,
  hot/cold/moist/dry and humoral associations) and optional modern-ruler
  notes. Source: Ptolemy Tetrabiblos Book I (PD Robbins/Ashmand); Alan Leo for
  modern nuance.
- Houses (Phase 5, `td-722c1d`): add classical topic depth, planetary joys,
  derived/turned houses for synastry and horary, and aversion-to-ascendant.
  Source: Valens, Firmicus, Lilly, Bonatti.
- Conditions (Phase 6, `td-fb39c1`): deepen each of the 13 condition modules
  with classical doctrine and combustion/cazimi/under-beams orb precision.
  Source: Ptolemy, Valens, Lilly, Bonatti.

P1 second-wave:

- Classical focused traditions (Phase 6, `td-fb39c1`): deepen sect and
  reception; add bonification/maltreatment vocabulary.
- Planets (Phase 5, `td-722c1d`): light classical-nature and sect enrichment;
  keep moderate.
- Planet-pair aspects (Phase 6, `td-fb39c1`): bring the six most-frequently-
  retrieved pairs toward the `mars_square_moon` exemplar depth; do not enrich
  all 26 uniformly.

## Modules to keep compact

Do not enrich these beyond spot-fixes; they are intentionally terse, already
rich, or inherently narrow. Enriching them raises bloat or drift risk without
proportional retrieval value.

- Foundations anchors: `interpretive_principles`, `ethics_and_scope`,
  `synthesis_rules`. Terse routing anchors by design.
- Traditions broad stubs: `classical.md`, `modern.md`. Routing fallbacks;
  focused modules carry the doctrine.
- Aspect types: already moderate; at most a light classical layer.
- Reading types: already rich; spot-fix only on forward-test evidence.
- Synthesis patterns `timing`, `strengths`, `conflict`: decent or inherently
  narrow; enrich only if testing shows a gap.
- Planet-in-sign and planet-in-house: keep the on-demand exemplar strategy;
  do not attempt all 120 + 120 combinations. The compositional fallback to
  planet + sign + house modules covers unlisted combinations by design.

## Coverage strategy for placements and planet-pair aspects

The skill is compositional, not exhaustive. Exact planet-in-sign,
planet-in-house, and planet-pair modules are preferred when they exist but are
not required: the retrieval contract falls back to planet + sign, planet +
house, and aspect-type + planet modules. Therefore:

- Treat placement and planet-pair coverage gaps as on-demand, not as a wave.
- Add a new exact module only when (a) forward testing or repeated user
  requests surface the gap, (b) the combination carries distinctive doctrine
  not recoverable from the broader modules, and (c) it follows the template.
- Record any on-demand addition in `references/resource_index.md` in the same
  change, per the index maintenance rules.

## Research pass

Logged with `td log` for `td-67c460`. Local files consulted: `SKILL.md`,
`ROADMAP.md`, `references/resource_index.md`,
`references/source_canon_and_rights_ledger.md`,
`references/templates/interpretation_module_template.md`,
`references/templates/rulership_module_template.md`, and a representative
sample across every reference category (planets, signs, houses, aspect types,
planet-pair aspects, conditions, rulerships, reading types, synthesis
patterns, foundations, and traditions). Depth and coverage confirmed with
`find`, `wc -c`, and targeted `grep` for absent doctrine terms.

Source-canon references used: the Phase 1 rights ledger
(`references/source_canon_and_rights_ledger.md`, task `td-ef5c84`), which vets
Ptolemy Tetrabiblos, Vettius Valens Anthologies, Firmicus, medieval Arabic and
Latin sources, Bonatti, Lilly Christian Astrology, and public-domain modern
sources (Alan Leo, Raphael/Cross, Sepharial) with edition, rights posture, and
doctrinal strengths.

External confirmations: the LacusCurtius Robbins Tetrabiblos table of contents
(PD via non-renewal per the ledger) returned HTTP 200 and lists Ptolemy Book I
chapters 11 (solid/bicorporeal signs), 12 (masculine/feminine signs), and 14
(commanding and obeying signs), confirming the sign-powers doctrine absent
from the sign modules is available in a vetted public-domain source. Network
access was confirmed available; external lookups were kept targeted to the
load-bearing doctrine-to-source mappings for this gap matrix. Deeper
per-source extraction belongs to Phase 3 (`td-3b52ed`) and Phase 4
(`td-b9588a`).
