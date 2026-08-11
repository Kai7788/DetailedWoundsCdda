# Changelog

## 0.2

- Added severity-aware avatar feedback to all production structural and respiratory wound outcomes.
- Added restrained recovery messages when finite acute respiratory and chest-wall impairment actually expires.
- Audited all 109 native treatment success messages and replaced generic chest-support text with procedure-specific feedback.
- Added a documented anti-spam and non-clinical message policy plus generated feedback coverage auditing.
- Audited all 256 wound descriptions and refined 29 weak or overly generic states, including 13 treated recovery states.
- Refined six acquisition messages, six structural treatment messages, and both finite acute-recovery messages for clearer family identity.
- Added an in-game Detailed Wounds help page explaining primary wounds, secondary trauma, treatment states, natural recovery, and reinjury.
- Added generated treatment-benefit and prose-completeness auditing; all 109 treatment transitions retain at least one mechanical or recovery benefit.
- Audited the proposed visible healing lifecycle against installed CDDA commit `251cf6cf23a0277d5118b67bee0efc9625c6cfeb`.
- Added complete healing classification and unchanged-duration reports for all 256 existing wounds.
- Extended strict validation so every wound has one unambiguous healing category and production feedback cannot silently lose its messages.
- Documented why current JSON cannot safely synchronize timed stages or a final healing message across native generation, treatment, reinjury, and save/load.
- Preserved all wound IDs, healing values, routing probabilities, pain, skills, proficiencies, and limb scores rather than enabling a desynchronizing approximation.

## 0.1

- Added damage-selected primary bruises, cuts, punctures, ballistic wounds, fractures, burns, electrical injuries, cold injuries, and specialized head/face/ocular/oral wounds.
- Added native treatment states and `wound_fix` chains for cleaning, irrigation, dressing, closure, debridement, stabilization, repair, and controlled rewarming.
- Completed specialized eye cold and mouth stab, bullet, heat, acid, electric, and cold coverage.
- Added same-ID self-copy damage overlays for JSON-only bash, cut, stab, bullet, electric, and severe heat secondary structural routing.
- Consolidated each damage tier to one weighted structural result to prevent multi-family wound spam.
- Added source-specific respiratory wound entry for inhaled smoke, tear gas, toxic gas, and fungal exposure.
- Activated finite acute respiratory and chest-wall breathing impairment without relying on a missing treatment callback.
- Added native repeated-injury progression for production-reachable structural and respiratory wounds.
- Removed four orphaned, unreachable reopening/infection EOCs after the final reference audit; retained coherent dormant lifecycle building blocks are explicitly classified.
- Split and organized wound, treatment, requirement, and EOC files while preserving persistent IDs.
- Added strict repository validation, coverage generation, architecture/source audits, known limitations, and regression documentation.
- Retained contamination/infection, bite, thermal-airway, and treatment-bridge definitions only as accurately documented dormant infrastructure where the current JSON API lacks a safe complete lifecycle.
