# Detailed Wounds coverage matrix

Generated from the current files by `python3 tools/validate_mod.py --coverage-output docs/WOUND_MATRIX.md`.
It separates automatically selectable primary wounds from secondary wounds reachable through production JSON hooks.

A cell shows `primary definitions / definitions with a direct wound_fix`.
A zero treatment count is acceptable when every listed wound heals naturally.

| Damage | head | torso | sensor | mouth | arm | hand | leg | foot |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| bash | 8 / 0 | 4 / 0 | 3 / 0 | 5 / 0 | 10 / 5 | 10 / 5 | 10 / 5 | 10 / 5 |
| cut | 6 / 6 | 6 / 6 | 2 / 1 | 3 / 3 | 6 / 6 | 6 / 6 | 6 / 6 | 6 / 6 |
| stab | 6 / 6 | 6 / 6 | 1 / 0 | 3 / 3 | 6 / 6 | 6 / 6 | 6 / 6 | 6 / 6 |
| bullet | 5 / 5 | 5 / 5 | 1 / 0 | 3 / 3 | 5 / 5 | 5 / 5 | 5 / 5 | 5 / 5 |
| heat | 5 / 5 | 5 / 5 | 1 / 0 | 3 / 3 | 5 / 5 | 5 / 5 | 5 / 5 | 5 / 5 |
| acid | 5 / 5 | 5 / 5 | 1 / 1 | 3 / 3 | 5 / 5 | 5 / 5 | 5 / 5 | 5 / 5 |
| electric | 5 / 5 | 5 / 5 | 1 / 0 | 2 / 2 | 5 / 5 | 5 / 5 | 5 / 5 | 5 / 5 |
| cold | 5 / 5 | 5 / 5 | 2 / 2 | 2 / 2 | 5 / 5 | 5 / 5 | 5 / 5 | 5 / 5 |
| biological | secondary only | secondary only | secondary only | secondary only | secondary only | secondary only | secondary only | secondary only |

## Runtime validation of Phase D coverage

The following direct specialized routes have been confirmed in-game. This records
only the bodypart/damage combinations and treatment behavior that were actually
tested; it does not claim runtime coverage of every severity tier.

| Bodypart type | Damage | Specialized generation | Native treatment |
|---|---|:---:|:---:|
| sensor | cold | passed | passed |
| mouth | stab | passed | passed |
| mouth | bullet | passed | passed |
| mouth | heat | passed | passed |
| mouth | acid | passed | passed |
| mouth | electric | passed | passed |
| mouth | cold | passed | passed |

The severe oral chemical irrigation-then-debridement chain passed in-game, and a
resulting treated wound state was verified across save/load.

## Production secondary coverage

These counts include wounds directly added by an active damage/effect hook and worse states reachable through native `wound_progression`.
A cell shows `reachable secondary definitions / definitions with a direct wound_fix`.

| Damage | head | torso | sensor | mouth | arm | hand | leg | foot |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| bash | — | 15 / 7 | — | — | 18 / 16 | 18 / 16 | 18 / 16 | 18 / 16 |
| cut | — | — | — | — | 7 / 7 | 7 / 7 | 7 / 7 | 7 / 7 |
| stab | — | 6 / 0 | — | — | 7 / 7 | 7 / 7 | 7 / 7 | 7 / 7 |
| bullet | — | 11 / 5 | — | — | 7 / 7 | 7 / 7 | 7 / 7 | 7 / 7 |
| heat | — | — | — | — | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| acid | — | — | — | — | — | — | — | — |
| electric | — | — | — | — | 3 / 2 | 3 / 2 | 3 / 2 | 3 / 2 |
| cold | — | — | — | — | — | — | — | — |
| biological | — | 8 / 0 | — | 1 / 0 | — | — | — | — |

Generic structural damage routing is intentionally limited to standard flesh arms, hands, legs, feet, and torso. Head, eye, and mouth physical damage remains under specialized primary wound control; the mouth biological entry above is source-specific upper-airway exposure. Bite trauma and thermal-airway wounds remain defined but lack a sufficiently precise production event in this build.

## Direct primary coverage gaps

None.

`biological` is intentionally not treated as generic direct wound coverage. Existing respiratory
and exposure wounds are secondary-only, and a broad biological-damage hook would create false
lung injuries for non-respiratory poison/internal damage.

## Primary treatment reachability

- Primary wound definitions: 86
- Primary wounds with a direct `wound_fix`: 65
- Naturally healing primary wounds without a direct fix: 21
- Non-healing primary wounds without a treatment path: 0

## Detailed primary definitions

| Damage | Bodypart type | Wound | Damage | Direct fix | Natural healing |
|---|---|---|---:|:---:|:---:|
| bash | head | `dw_minor_bruise` | 2–7 | no | yes |
| bash | head | `dw_heavy_bruise` | 8–15 | no | yes |
| bash | head | `dw_concussion` | 10–24 | no | yes |
| bash | head | `dw_severe_contusion` | 16–25 | no | yes |
| bash | head | `dw_severe_concussion` | 20–38 | no | yes |
| bash | head | `dw_massive_contusion` | 26–1000 | no | yes |
| bash | head | `dw_skull_fracture` | 28–50 | no | yes |
| bash | head | `dw_depressed_skull_fracture` | 45–1000 | no | yes |
| bash | torso | `dw_minor_bruise` | 2–7 | no | yes |
| bash | torso | `dw_heavy_bruise` | 8–15 | no | yes |
| bash | torso | `dw_severe_contusion` | 16–25 | no | yes |
| bash | torso | `dw_massive_contusion` | 26–1000 | no | yes |
| bash | sensor | `dw_minor_ocular_contusion` | 2–7 | no | yes |
| bash | sensor | `dw_blunt_ocular_trauma` | 7–16 | no | yes |
| bash | sensor | `dw_severe_ocular_trauma` | 14–1000 | no | yes |
| bash | mouth | `dw_facial_contusion` | 2–9 | no | yes |
| bash | mouth | `dw_severe_facial_contusion` | 8–18 | no | yes |
| bash | mouth | `dw_dental_trauma` | 8–22 | no | yes |
| bash | mouth | `dw_jaw_injury` | 12–28 | no | yes |
| bash | mouth | `dw_jaw_fracture` | 22–1000 | no | yes |
| bash | arm | `dw_minor_bruise` | 2–7 | no | yes |
| bash | arm | `dw_heavy_bruise` | 8–15 | no | yes |
| bash | arm | `dw_bone_contusion` | 10–20 | no | yes |
| bash | arm | `dw_severe_contusion` | 16–25 | no | yes |
| bash | arm | `dw_hairline_fracture` | 16–30 | yes | yes |
| bash | arm | `dw_closed_fracture` | 24–45 | yes | yes |
| bash | arm | `dw_massive_contusion` | 26–1000 | no | yes |
| bash | arm | `dw_displaced_fracture` | 32–60 | yes | no |
| bash | arm | `dw_comminuted_fracture` | 45–1000 | yes | no |
| bash | arm | `dw_open_fracture` | 55–1000 | yes | no |
| bash | hand | `dw_minor_bruise` | 2–7 | no | yes |
| bash | hand | `dw_heavy_bruise` | 8–15 | no | yes |
| bash | hand | `dw_bone_contusion` | 10–20 | no | yes |
| bash | hand | `dw_severe_contusion` | 16–25 | no | yes |
| bash | hand | `dw_hairline_fracture` | 16–30 | yes | yes |
| bash | hand | `dw_closed_fracture` | 24–45 | yes | yes |
| bash | hand | `dw_massive_contusion` | 26–1000 | no | yes |
| bash | hand | `dw_displaced_fracture` | 32–60 | yes | no |
| bash | hand | `dw_comminuted_fracture` | 45–1000 | yes | no |
| bash | hand | `dw_open_fracture` | 55–1000 | yes | no |
| bash | leg | `dw_minor_bruise` | 2–7 | no | yes |
| bash | leg | `dw_heavy_bruise` | 8–15 | no | yes |
| bash | leg | `dw_bone_contusion` | 10–20 | no | yes |
| bash | leg | `dw_severe_contusion` | 16–25 | no | yes |
| bash | leg | `dw_hairline_fracture` | 16–30 | yes | yes |
| bash | leg | `dw_closed_fracture` | 24–45 | yes | yes |
| bash | leg | `dw_massive_contusion` | 26–1000 | no | yes |
| bash | leg | `dw_displaced_fracture` | 32–60 | yes | no |
| bash | leg | `dw_comminuted_fracture` | 45–1000 | yes | no |
| bash | leg | `dw_open_fracture` | 55–1000 | yes | no |
| bash | foot | `dw_minor_bruise` | 2–7 | no | yes |
| bash | foot | `dw_heavy_bruise` | 8–15 | no | yes |
| bash | foot | `dw_bone_contusion` | 10–20 | no | yes |
| bash | foot | `dw_severe_contusion` | 16–25 | no | yes |
| bash | foot | `dw_hairline_fracture` | 16–30 | yes | yes |
| bash | foot | `dw_closed_fracture` | 24–45 | yes | yes |
| bash | foot | `dw_massive_contusion` | 26–1000 | no | yes |
| bash | foot | `dw_displaced_fracture` | 32–60 | yes | no |
| bash | foot | `dw_comminuted_fracture` | 45–1000 | yes | no |
| bash | foot | `dw_open_fracture` | 55–1000 | yes | no |
| cut | head | `dw_scratch` | 1–4 | yes | yes |
| cut | head | `dw_shallow_cut` | 3–9 | yes | yes |
| cut | head | `dw_laceration` | 7–16 | yes | yes |
| cut | head | `dw_deep_laceration` | 14–26 | yes | yes |
| cut | head | `dw_severe_laceration` | 23–40 | yes | yes |
| cut | head | `dw_avulsion_wound` | 35–1000 | yes | no |
| cut | torso | `dw_scratch` | 1–4 | yes | yes |
| cut | torso | `dw_shallow_cut` | 3–9 | yes | yes |
| cut | torso | `dw_laceration` | 7–16 | yes | yes |
| cut | torso | `dw_deep_laceration` | 14–26 | yes | yes |
| cut | torso | `dw_severe_laceration` | 23–40 | yes | yes |
| cut | torso | `dw_avulsion_wound` | 35–1000 | yes | no |
| cut | sensor | `dw_cornea_abrasion` | 1–5 | yes | yes |
| cut | sensor | `dw_ocular_laceration` | 5–1000 | no | yes |
| cut | mouth | `dw_split_lip` | 2–8 | yes | yes |
| cut | mouth | `dw_oral_laceration` | 7–18 | yes | yes |
| cut | mouth | `dw_deep_facial_laceration` | 15–1000 | yes | yes |
| cut | arm | `dw_scratch` | 1–4 | yes | yes |
| cut | arm | `dw_shallow_cut` | 3–9 | yes | yes |
| cut | arm | `dw_laceration` | 7–16 | yes | yes |
| cut | arm | `dw_deep_laceration` | 14–26 | yes | yes |
| cut | arm | `dw_severe_laceration` | 23–40 | yes | yes |
| cut | arm | `dw_avulsion_wound` | 35–1000 | yes | no |
| cut | hand | `dw_scratch` | 1–4 | yes | yes |
| cut | hand | `dw_shallow_cut` | 3–9 | yes | yes |
| cut | hand | `dw_laceration` | 7–16 | yes | yes |
| cut | hand | `dw_deep_laceration` | 14–26 | yes | yes |
| cut | hand | `dw_severe_laceration` | 23–40 | yes | yes |
| cut | hand | `dw_avulsion_wound` | 35–1000 | yes | no |
| cut | leg | `dw_scratch` | 1–4 | yes | yes |
| cut | leg | `dw_shallow_cut` | 3–9 | yes | yes |
| cut | leg | `dw_laceration` | 7–16 | yes | yes |
| cut | leg | `dw_deep_laceration` | 14–26 | yes | yes |
| cut | leg | `dw_severe_laceration` | 23–40 | yes | yes |
| cut | leg | `dw_avulsion_wound` | 35–1000 | yes | no |
| cut | foot | `dw_scratch` | 1–4 | yes | yes |
| cut | foot | `dw_shallow_cut` | 3–9 | yes | yes |
| cut | foot | `dw_laceration` | 7–16 | yes | yes |
| cut | foot | `dw_deep_laceration` | 14–26 | yes | yes |
| cut | foot | `dw_severe_laceration` | 23–40 | yes | yes |
| cut | foot | `dw_avulsion_wound` | 35–1000 | yes | no |
| stab | head | `dw_minor_puncture` | 1–5 | yes | yes |
| stab | head | `dw_puncture_wound` | 4–11 | yes | yes |
| stab | head | `dw_deep_puncture` | 9–20 | yes | yes |
| stab | head | `dw_penetrating_wound` | 17–30 | yes | yes |
| stab | head | `dw_severe_penetrating_wound` | 27–45 | yes | yes |
| stab | head | `dw_devastating_penetrating_wound` | 40–1000 | yes | no |
| stab | torso | `dw_minor_puncture` | 1–5 | yes | yes |
| stab | torso | `dw_puncture_wound` | 4–11 | yes | yes |
| stab | torso | `dw_deep_puncture` | 9–20 | yes | yes |
| stab | torso | `dw_penetrating_wound` | 17–30 | yes | yes |
| stab | torso | `dw_severe_penetrating_wound` | 27–45 | yes | yes |
| stab | torso | `dw_devastating_penetrating_wound` | 40–1000 | yes | no |
| stab | sensor | `dw_penetrating_ocular_injury` | 6–1000 | no | yes |
| stab | mouth | `dw_oral_puncture_wound` | 1–8 | yes | yes |
| stab | mouth | `dw_deep_oral_puncture_wound` | 7–24 | yes | yes |
| stab | mouth | `dw_severe_penetrating_oral_injury` | 20–1000 | yes | no |
| stab | arm | `dw_minor_puncture` | 1–5 | yes | yes |
| stab | arm | `dw_puncture_wound` | 4–11 | yes | yes |
| stab | arm | `dw_deep_puncture` | 9–20 | yes | yes |
| stab | arm | `dw_penetrating_wound` | 17–30 | yes | yes |
| stab | arm | `dw_severe_penetrating_wound` | 27–45 | yes | yes |
| stab | arm | `dw_devastating_penetrating_wound` | 40–1000 | yes | no |
| stab | hand | `dw_minor_puncture` | 1–5 | yes | yes |
| stab | hand | `dw_puncture_wound` | 4–11 | yes | yes |
| stab | hand | `dw_deep_puncture` | 9–20 | yes | yes |
| stab | hand | `dw_penetrating_wound` | 17–30 | yes | yes |
| stab | hand | `dw_severe_penetrating_wound` | 27–45 | yes | yes |
| stab | hand | `dw_devastating_penetrating_wound` | 40–1000 | yes | no |
| stab | leg | `dw_minor_puncture` | 1–5 | yes | yes |
| stab | leg | `dw_puncture_wound` | 4–11 | yes | yes |
| stab | leg | `dw_deep_puncture` | 9–20 | yes | yes |
| stab | leg | `dw_penetrating_wound` | 17–30 | yes | yes |
| stab | leg | `dw_severe_penetrating_wound` | 27–45 | yes | yes |
| stab | leg | `dw_devastating_penetrating_wound` | 40–1000 | yes | no |
| stab | foot | `dw_minor_puncture` | 1–5 | yes | yes |
| stab | foot | `dw_puncture_wound` | 4–11 | yes | yes |
| stab | foot | `dw_deep_puncture` | 9–20 | yes | yes |
| stab | foot | `dw_penetrating_wound` | 17–30 | yes | yes |
| stab | foot | `dw_severe_penetrating_wound` | 27–45 | yes | yes |
| stab | foot | `dw_devastating_penetrating_wound` | 40–1000 | yes | no |
| bullet | head | `dw_ballistic_graze` | 1–8 | yes | yes |
| bullet | head | `dw_superficial_gunshot_wound` | 6–16 | yes | yes |
| bullet | head | `dw_penetrating_gunshot_wound` | 13–28 | yes | yes |
| bullet | head | `dw_severe_gunshot_wound` | 24–45 | yes | yes |
| bullet | head | `dw_devastating_ballistic_wound` | 40–1000 | yes | no |
| bullet | torso | `dw_ballistic_graze` | 1–8 | yes | yes |
| bullet | torso | `dw_superficial_gunshot_wound` | 6–16 | yes | yes |
| bullet | torso | `dw_penetrating_gunshot_wound` | 13–28 | yes | yes |
| bullet | torso | `dw_severe_gunshot_wound` | 24–45 | yes | yes |
| bullet | torso | `dw_devastating_ballistic_wound` | 40–1000 | yes | no |
| bullet | sensor | `dw_penetrating_ocular_injury` | 6–1000 | no | yes |
| bullet | mouth | `dw_ballistic_oral_wound` | 1–12 | yes | yes |
| bullet | mouth | `dw_severe_maxillofacial_ballistic_trauma` | 10–35 | yes | yes |
| bullet | mouth | `dw_devastating_maxillofacial_ballistic_injury` | 30–1000 | yes | no |
| bullet | arm | `dw_ballistic_graze` | 1–8 | yes | yes |
| bullet | arm | `dw_superficial_gunshot_wound` | 6–16 | yes | yes |
| bullet | arm | `dw_penetrating_gunshot_wound` | 13–28 | yes | yes |
| bullet | arm | `dw_severe_gunshot_wound` | 24–45 | yes | yes |
| bullet | arm | `dw_devastating_ballistic_wound` | 40–1000 | yes | no |
| bullet | hand | `dw_ballistic_graze` | 1–8 | yes | yes |
| bullet | hand | `dw_superficial_gunshot_wound` | 6–16 | yes | yes |
| bullet | hand | `dw_penetrating_gunshot_wound` | 13–28 | yes | yes |
| bullet | hand | `dw_severe_gunshot_wound` | 24–45 | yes | yes |
| bullet | hand | `dw_devastating_ballistic_wound` | 40–1000 | yes | no |
| bullet | leg | `dw_ballistic_graze` | 1–8 | yes | yes |
| bullet | leg | `dw_superficial_gunshot_wound` | 6–16 | yes | yes |
| bullet | leg | `dw_penetrating_gunshot_wound` | 13–28 | yes | yes |
| bullet | leg | `dw_severe_gunshot_wound` | 24–45 | yes | yes |
| bullet | leg | `dw_devastating_ballistic_wound` | 40–1000 | yes | no |
| bullet | foot | `dw_ballistic_graze` | 1–8 | yes | yes |
| bullet | foot | `dw_superficial_gunshot_wound` | 6–16 | yes | yes |
| bullet | foot | `dw_penetrating_gunshot_wound` | 13–28 | yes | yes |
| bullet | foot | `dw_severe_gunshot_wound` | 24–45 | yes | yes |
| bullet | foot | `dw_devastating_ballistic_wound` | 40–1000 | yes | no |
| heat | head | `dw_superficial_burn` | 2–6 | yes | yes |
| heat | head | `dw_superficial_partial_thickness_burn` | 7–13 | yes | yes |
| heat | head | `dw_deep_partial_thickness_burn` | 14–23 | yes | yes |
| heat | head | `dw_full_thickness_burn` | 24–35 | yes | no |
| heat | head | `dw_extensive_full_thickness_burn` | 36–1000 | yes | no |
| heat | torso | `dw_superficial_burn` | 2–6 | yes | yes |
| heat | torso | `dw_superficial_partial_thickness_burn` | 7–13 | yes | yes |
| heat | torso | `dw_deep_partial_thickness_burn` | 14–23 | yes | yes |
| heat | torso | `dw_full_thickness_burn` | 24–35 | yes | no |
| heat | torso | `dw_extensive_full_thickness_burn` | 36–1000 | yes | no |
| heat | sensor | `dw_ocular_thermal_burn` | 3–1000 | no | yes |
| heat | mouth | `dw_oral_thermal_burn` | 2–10 | yes | yes |
| heat | mouth | `dw_deep_oral_thermal_burn` | 8–25 | yes | yes |
| heat | mouth | `dw_severe_oral_thermal_injury` | 22–1000 | yes | no |
| heat | arm | `dw_superficial_burn` | 2–6 | yes | yes |
| heat | arm | `dw_superficial_partial_thickness_burn` | 7–13 | yes | yes |
| heat | arm | `dw_deep_partial_thickness_burn` | 14–23 | yes | yes |
| heat | arm | `dw_full_thickness_burn` | 24–35 | yes | no |
| heat | arm | `dw_extensive_full_thickness_burn` | 36–1000 | yes | no |
| heat | hand | `dw_superficial_burn` | 2–6 | yes | yes |
| heat | hand | `dw_superficial_partial_thickness_burn` | 7–13 | yes | yes |
| heat | hand | `dw_deep_partial_thickness_burn` | 14–23 | yes | yes |
| heat | hand | `dw_full_thickness_burn` | 24–35 | yes | no |
| heat | hand | `dw_extensive_full_thickness_burn` | 36–1000 | yes | no |
| heat | leg | `dw_superficial_burn` | 2–6 | yes | yes |
| heat | leg | `dw_superficial_partial_thickness_burn` | 7–13 | yes | yes |
| heat | leg | `dw_deep_partial_thickness_burn` | 14–23 | yes | yes |
| heat | leg | `dw_full_thickness_burn` | 24–35 | yes | no |
| heat | leg | `dw_extensive_full_thickness_burn` | 36–1000 | yes | no |
| heat | foot | `dw_superficial_burn` | 2–6 | yes | yes |
| heat | foot | `dw_superficial_partial_thickness_burn` | 7–13 | yes | yes |
| heat | foot | `dw_deep_partial_thickness_burn` | 14–23 | yes | yes |
| heat | foot | `dw_full_thickness_burn` | 24–35 | yes | no |
| heat | foot | `dw_extensive_full_thickness_burn` | 36–1000 | yes | no |
| acid | head | `dw_mild_chemical_burn` | 2–6 | yes | yes |
| acid | head | `dw_moderate_chemical_burn` | 7–13 | yes | yes |
| acid | head | `dw_deep_chemical_burn` | 14–23 | yes | yes |
| acid | head | `dw_full_thickness_chemical_burn` | 24–35 | yes | no |
| acid | head | `dw_extensive_chemical_burn` | 36–1000 | yes | no |
| acid | torso | `dw_mild_chemical_burn` | 2–6 | yes | yes |
| acid | torso | `dw_moderate_chemical_burn` | 7–13 | yes | yes |
| acid | torso | `dw_deep_chemical_burn` | 14–23 | yes | yes |
| acid | torso | `dw_full_thickness_chemical_burn` | 24–35 | yes | no |
| acid | torso | `dw_extensive_chemical_burn` | 36–1000 | yes | no |
| acid | sensor | `dw_ocular_chemical_burn` | 2–1000 | yes | no |
| acid | mouth | `dw_oral_chemical_burn` | 2–10 | yes | yes |
| acid | mouth | `dw_deep_oral_chemical_burn` | 8–25 | yes | yes |
| acid | mouth | `dw_severe_corrosive_oral_injury` | 22–1000 | yes | no |
| acid | arm | `dw_mild_chemical_burn` | 2–6 | yes | yes |
| acid | arm | `dw_moderate_chemical_burn` | 7–13 | yes | yes |
| acid | arm | `dw_deep_chemical_burn` | 14–23 | yes | yes |
| acid | arm | `dw_full_thickness_chemical_burn` | 24–35 | yes | no |
| acid | arm | `dw_extensive_chemical_burn` | 36–1000 | yes | no |
| acid | hand | `dw_mild_chemical_burn` | 2–6 | yes | yes |
| acid | hand | `dw_moderate_chemical_burn` | 7–13 | yes | yes |
| acid | hand | `dw_deep_chemical_burn` | 14–23 | yes | yes |
| acid | hand | `dw_full_thickness_chemical_burn` | 24–35 | yes | no |
| acid | hand | `dw_extensive_chemical_burn` | 36–1000 | yes | no |
| acid | leg | `dw_mild_chemical_burn` | 2–6 | yes | yes |
| acid | leg | `dw_moderate_chemical_burn` | 7–13 | yes | yes |
| acid | leg | `dw_deep_chemical_burn` | 14–23 | yes | yes |
| acid | leg | `dw_full_thickness_chemical_burn` | 24–35 | yes | no |
| acid | leg | `dw_extensive_chemical_burn` | 36–1000 | yes | no |
| acid | foot | `dw_mild_chemical_burn` | 2–6 | yes | yes |
| acid | foot | `dw_moderate_chemical_burn` | 7–13 | yes | yes |
| acid | foot | `dw_deep_chemical_burn` | 14–23 | yes | yes |
| acid | foot | `dw_full_thickness_chemical_burn` | 24–35 | yes | no |
| acid | foot | `dw_extensive_chemical_burn` | 36–1000 | yes | no |
| electric | head | `dw_minor_electrical_burn` | 2–6 | yes | yes |
| electric | head | `dw_electrical_contact_burn` | 6–13 | yes | yes |
| electric | head | `dw_deep_electrical_burn` | 12–23 | yes | yes |
| electric | head | `dw_severe_electrical_tissue_injury` | 21–35 | yes | yes |
| electric | head | `dw_extensive_electrical_tissue_destruction` | 32–1000 | yes | no |
| electric | torso | `dw_minor_electrical_burn` | 2–6 | yes | yes |
| electric | torso | `dw_electrical_contact_burn` | 6–13 | yes | yes |
| electric | torso | `dw_deep_electrical_burn` | 12–23 | yes | yes |
| electric | torso | `dw_severe_electrical_tissue_injury` | 21–35 | yes | yes |
| electric | torso | `dw_extensive_electrical_tissue_destruction` | 32–1000 | yes | no |
| electric | sensor | `dw_ocular_electrical_injury` | 4–1000 | no | yes |
| electric | mouth | `dw_oral_electrical_burn` | 2–18 | yes | yes |
| electric | mouth | `dw_deep_oral_electrical_tissue_injury` | 15–1000 | yes | no |
| electric | arm | `dw_minor_electrical_burn` | 2–6 | yes | yes |
| electric | arm | `dw_electrical_contact_burn` | 6–13 | yes | yes |
| electric | arm | `dw_deep_electrical_burn` | 12–23 | yes | yes |
| electric | arm | `dw_severe_electrical_tissue_injury` | 21–35 | yes | yes |
| electric | arm | `dw_extensive_electrical_tissue_destruction` | 32–1000 | yes | no |
| electric | hand | `dw_minor_electrical_burn` | 2–6 | yes | yes |
| electric | hand | `dw_electrical_contact_burn` | 6–13 | yes | yes |
| electric | hand | `dw_deep_electrical_burn` | 12–23 | yes | yes |
| electric | hand | `dw_severe_electrical_tissue_injury` | 21–35 | yes | yes |
| electric | hand | `dw_extensive_electrical_tissue_destruction` | 32–1000 | yes | no |
| electric | leg | `dw_minor_electrical_burn` | 2–6 | yes | yes |
| electric | leg | `dw_electrical_contact_burn` | 6–13 | yes | yes |
| electric | leg | `dw_deep_electrical_burn` | 12–23 | yes | yes |
| electric | leg | `dw_severe_electrical_tissue_injury` | 21–35 | yes | yes |
| electric | leg | `dw_extensive_electrical_tissue_destruction` | 32–1000 | yes | no |
| electric | foot | `dw_minor_electrical_burn` | 2–6 | yes | yes |
| electric | foot | `dw_electrical_contact_burn` | 6–13 | yes | yes |
| electric | foot | `dw_deep_electrical_burn` | 12–23 | yes | yes |
| electric | foot | `dw_severe_electrical_tissue_injury` | 21–35 | yes | yes |
| electric | foot | `dw_extensive_electrical_tissue_destruction` | 32–1000 | yes | no |
| cold | head | `dw_mild_cold_injury` | 2–7 | yes | yes |
| cold | head | `dw_superficial_freezing_injury` | 6–14 | yes | yes |
| cold | head | `dw_deep_freezing_injury` | 12–24 | yes | yes |
| cold | head | `dw_severe_cold_tissue_injury` | 21–38 | yes | yes |
| cold | head | `dw_extensive_cryogenic_tissue_injury` | 34–1000 | yes | no |
| cold | torso | `dw_mild_cold_injury` | 2–7 | yes | yes |
| cold | torso | `dw_superficial_freezing_injury` | 6–14 | yes | yes |
| cold | torso | `dw_deep_freezing_injury` | 12–24 | yes | yes |
| cold | torso | `dw_severe_cold_tissue_injury` | 21–38 | yes | yes |
| cold | torso | `dw_extensive_cryogenic_tissue_injury` | 34–1000 | yes | no |
| cold | sensor | `dw_ocular_freezing_injury` | 2–20 | yes | yes |
| cold | sensor | `dw_severe_ocular_freezing_injury` | 16–1000 | yes | no |
| cold | mouth | `dw_oral_freezing_injury` | 2–20 | yes | yes |
| cold | mouth | `dw_deep_oral_freezing_injury` | 16–1000 | yes | no |
| cold | arm | `dw_mild_cold_injury` | 2–7 | yes | yes |
| cold | arm | `dw_superficial_freezing_injury` | 6–14 | yes | yes |
| cold | arm | `dw_deep_freezing_injury` | 12–24 | yes | yes |
| cold | arm | `dw_severe_cold_tissue_injury` | 21–38 | yes | yes |
| cold | arm | `dw_extensive_cryogenic_tissue_injury` | 34–1000 | yes | no |
| cold | hand | `dw_mild_cold_injury` | 2–7 | yes | yes |
| cold | hand | `dw_superficial_freezing_injury` | 6–14 | yes | yes |
| cold | hand | `dw_deep_freezing_injury` | 12–24 | yes | yes |
| cold | hand | `dw_severe_cold_tissue_injury` | 21–38 | yes | yes |
| cold | hand | `dw_extensive_cryogenic_tissue_injury` | 34–1000 | yes | no |
| cold | leg | `dw_mild_cold_injury` | 2–7 | yes | yes |
| cold | leg | `dw_superficial_freezing_injury` | 6–14 | yes | yes |
| cold | leg | `dw_deep_freezing_injury` | 12–24 | yes | yes |
| cold | leg | `dw_severe_cold_tissue_injury` | 21–38 | yes | yes |
| cold | leg | `dw_extensive_cryogenic_tissue_injury` | 34–1000 | yes | no |
| cold | foot | `dw_mild_cold_injury` | 2–7 | yes | yes |
| cold | foot | `dw_superficial_freezing_injury` | 6–14 | yes | yes |
| cold | foot | `dw_deep_freezing_injury` | 12–24 | yes | yes |
| cold | foot | `dw_severe_cold_tissue_injury` | 21–38 | yes | yes |
| cold | foot | `dw_extensive_cryogenic_tissue_injury` | 34–1000 | yes | no |

## Secondary reachability summary

- Secondary wound definitions: 61
- Production-reachable secondary wounds: 52
- Intentionally dormant/unreachable secondary wounds: 9
- Dormant IDs: `dw_crushing_bite_injury`, `dw_deep_bite_wound`, `dw_devastating_bite_injury`, `dw_irritant_inhalation_injury`, `dw_severe_irritant_lung_injury`, `dw_severe_thermal_airway_injury`, `dw_superficial_bite_wound`, `dw_tearing_bite_wound`, `dw_thermal_airway_injury`
