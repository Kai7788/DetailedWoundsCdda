# Healing duration audit

The safe JSON-only result leaves every native healing range unchanged. No visible timed
stage chain is enabled because this CDDA build cannot observe wound progress or validate
a delayed transition after treatment/reinjury. Accordingly, the audited result equals the
v0.1 baseline and every duration delta is zero.

| Wound | Category | v0.1 min | v0.1 max | Audited min | Audited max | Delta min | Delta max | Stages |
|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| `dw_ballistic_graze` | B | 2 days | 8 days | 2 days | 8 days | 0% | 0% | 0 |
| `dw_ballistic_internal_trauma` | D | 14 days | 40 days | 14 days | 40 days | 0% | 0% | 0 |
| `dw_ballistic_oral_wound` | B | 4 days | 16 days | 4 days | 16 days | 0% | 0% | 0 |
| `dw_blunt_ocular_trauma` | A | 5 days | 18 days | 5 days | 18 days | 0% | 0% | 0 |
| `dw_bone_contusion` | A | 7 days | 21 days | 7 days | 21 days | 0% | 0% | 0 |
| `dw_cleaned_ballistic_oral_wound` | B | 3 days | 12 days | 3 days | 12 days | 0% | 0% | 0 |
| `dw_cleaned_crushing_bite_injury` | F | 8 days | 28 days | 8 days | 28 days | 0% | 0% | 0 |
| `dw_cleaned_deep_bite_wound` | F | 5 days | 16 days | 5 days | 16 days | 0% | 0% | 0 |
| `dw_cleaned_deep_facial_laceration` | B | 8 days | 28 days | 8 days | 28 days | 0% | 0% | 0 |
| `dw_cleaned_deep_laceration` | B | 6 days | 20 days | 6 days | 20 days | 0% | 0% | 0 |
| `dw_cleaned_deep_oral_puncture_wound` | B | 5 days | 18 days | 5 days | 18 days | 0% | 0% | 0 |
| `dw_cleaned_deep_puncture` | B | 4 days | 14 days | 4 days | 14 days | 0% | 0% | 0 |
| `dw_cleaned_laceration` | B | 2 days | 8 days | 2 days | 8 days | 0% | 0% | 0 |
| `dw_cleaned_minor_puncture` | B | 8 hours | 3 days | 8 hours | 3 days | 0% | 0% | 0 |
| `dw_cleaned_oral_laceration` | B | 3 days | 14 days | 3 days | 14 days | 0% | 0% | 0 |
| `dw_cleaned_oral_puncture_wound` | B | 12 hours | 5 days | 12 hours | 5 days | 0% | 0% | 0 |
| `dw_cleaned_penetrating_gunshot_wound` | B | 8 days | 28 days | 8 days | 28 days | 0% | 0% | 0 |
| `dw_cleaned_penetrating_wound` | B | 8 days | 25 days | 8 days | 25 days | 0% | 0% | 0 |
| `dw_cleaned_puncture_wound` | B | 1 day | 6 days | 1 day | 6 days | 0% | 0% | 0 |
| `dw_cleaned_severe_laceration` | B | 18 days | 50 days | 18 days | 50 days | 0% | 0% | 0 |
| `dw_cleaned_superficial_bite_wound` | F | 1 day | 5 days | 1 day | 5 days | 0% | 0% | 0 |
| `dw_cleaned_superficial_gunshot_wound` | B | 4 days | 14 days | 4 days | 14 days | 0% | 0% | 0 |
| `dw_closed_fracture` | B | 42 days | 84 days | 42 days | 84 days | 0% | 0% | 0 |
| `dw_concussion` | A | 5 days | 21 days | 5 days | 21 days | 0% | 0% | 0 |
| `dw_cooled_deep_oral_thermal_burn` | B | 7 days | 28 days | 7 days | 28 days | 0% | 0% | 0 |
| `dw_cooled_oral_electrical_burn` | B | 2 days | 10 days | 2 days | 10 days | 0% | 0% | 0 |
| `dw_cooled_oral_thermal_burn` | B | 1 day | 7 days | 1 day | 7 days | 0% | 0% | 0 |
| `dw_cornea_abrasion` | B | 12 hours | 4 days | 12 hours | 4 days | 0% | 0% | 0 |
| `dw_cracked_rib` | D | 21 days | 42 days | 21 days | 42 days | 0% | 0% | 0 |
| `dw_crushing_bite_injury` | F | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_debrided_avulsion_wound` | C | 28 days | 84 days | 28 days | 84 days | 0% | 0% | 0 |
| `dw_debrided_deep_oral_electrical_tissue_injury` | C | 18 days | 60 days | 18 days | 60 days | 0% | 0% | 0 |
| `dw_debrided_devastating_ballistic_wound` | C | 35 days | 100 days | 35 days | 100 days | 0% | 0% | 0 |
| `dw_debrided_devastating_bite_injury` | F | 28 days | 84 days | 28 days | 84 days | 0% | 0% | 0 |
| `dw_debrided_devastating_maxillofacial_ballistic_injury` | C | 30 days | 90 days | 30 days | 90 days | 0% | 0% | 0 |
| `dw_debrided_devastating_penetrating_wound` | C | 28 days | 84 days | 28 days | 84 days | 0% | 0% | 0 |
| `dw_debrided_extensive_chemical_burn` | C | 45 days | 105 days | 45 days | 105 days | 0% | 0% | 0 |
| `dw_debrided_extensive_cold_injury` | C | 35 days | 100 days | 35 days | 100 days | 0% | 0% | 0 |
| `dw_debrided_extensive_electrical_tissue_destruction` | C | 35 days | 105 days | 35 days | 105 days | 0% | 0% | 0 |
| `dw_debrided_extensive_full_thickness_burn` | C | 45 days | 105 days | 45 days | 105 days | 0% | 0% | 0 |
| `dw_debrided_full_thickness_burn` | C | 28 days | 70 days | 28 days | 70 days | 0% | 0% | 0 |
| `dw_debrided_full_thickness_chemical_burn` | C | 28 days | 70 days | 28 days | 70 days | 0% | 0% | 0 |
| `dw_debrided_severe_corrosive_oral_injury` | C | 18 days | 60 days | 18 days | 60 days | 0% | 0% | 0 |
| `dw_debrided_severe_electrical_tissue_injury` | B | 18 days | 60 days | 18 days | 60 days | 0% | 0% | 0 |
| `dw_debrided_severe_gunshot_wound` | B | 18 days | 56 days | 18 days | 56 days | 0% | 0% | 0 |
| `dw_debrided_severe_maxillofacial_ballistic_trauma` | B | 14 days | 50 days | 14 days | 50 days | 0% | 0% | 0 |
| `dw_debrided_severe_oral_thermal_injury` | C | 18 days | 60 days | 18 days | 60 days | 0% | 0% | 0 |
| `dw_debrided_severe_penetrating_oral_injury` | C | 18 days | 60 days | 18 days | 60 days | 0% | 0% | 0 |
| `dw_debrided_severe_penetrating_wound` | B | 14 days | 45 days | 14 days | 45 days | 0% | 0% | 0 |
| `dw_debrided_severe_soft_tissue_crush_injury` | D | 28 days | 84 days | 28 days | 84 days | 0% | 0% | 0 |
| `dw_debrided_tearing_bite_wound` | F | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_decompressed_compartment_syndrome` | D | 21 days | 70 days | 21 days | 70 days | 0% | 0% | 0 |
| `dw_deep_bite_wound` | F | 7 days | 21 days | 7 days | 21 days | 0% | 0% | 0 |
| `dw_deep_chemical_burn` | B | 14 days | 42 days | 14 days | 42 days | 0% | 0% | 0 |
| `dw_deep_electrical_burn` | B | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_deep_facial_laceration` | B | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_deep_freezing_injury` | B | 10 days | 30 days | 10 days | 30 days | 0% | 0% | 0 |
| `dw_deep_laceration` | B | 7 days | 21 days | 7 days | 21 days | 0% | 0% | 0 |
| `dw_deep_oral_chemical_burn` | B | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_deep_oral_puncture_wound` | B | 7 days | 24 days | 7 days | 24 days | 0% | 0% | 0 |
| `dw_deep_oral_thermal_burn` | B | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_deep_partial_thickness_burn` | B | 14 days | 42 days | 14 days | 42 days | 0% | 0% | 0 |
| `dw_deep_penetrating_torso_injury` | D | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_deep_puncture` | B | 5 days | 18 days | 5 days | 18 days | 0% | 0% | 0 |
| `dw_deep_torso_contusion` | D | 5 days | 18 days | 5 days | 18 days | 0% | 0% | 0 |
| `dw_dental_trauma` | A | 7 days | 30 days | 7 days | 30 days | 0% | 0% | 0 |
| `dw_depressed_skull_fracture` | A | 60 days | 120 days | 60 days | 120 days | 0% | 0% | 0 |
| `dw_devastating_ballistic_internal_trauma` | D | 45 days | 120 days | 45 days | 120 days | 0% | 0% | 0 |
| `dw_displaced_rib_fracture` | D | 49 days | 98 days | 49 days | 98 days | 0% | 0% | 0 |
| `dw_dressed_ballistic_graze` | B | 1 day | 5 days | 1 day | 5 days | 0% | 0% | 0 |
| `dw_dressed_deep_electrical_burn` | B | 8 days | 28 days | 8 days | 28 days | 0% | 0% | 0 |
| `dw_dressed_deep_partial_thickness_burn` | B | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_dressed_electrical_contact_burn` | B | 3 days | 12 days | 3 days | 12 days | 0% | 0% | 0 |
| `dw_dressed_minor_electrical_burn` | B | 1 day | 4 days | 1 day | 4 days | 0% | 0% | 0 |
| `dw_dressed_scratch` | B | 6 hours | 1 day | 6 hours | 1 day | 0% | 0% | 0 |
| `dw_dressed_shallow_cut` | B | 12 hours | 3 days | 12 hours | 3 days | 0% | 0% | 0 |
| `dw_dressed_split_lip` | B | 1 day | 5 days | 1 day | 5 days | 0% | 0% | 0 |
| `dw_dressed_superficial_burn` | B | 12 hours | 3 days | 12 hours | 3 days | 0% | 0% | 0 |
| `dw_dressed_superficial_partial_thickness_burn` | B | 5 days | 16 days | 5 days | 16 days | 0% | 0% | 0 |
| `dw_electrical_contact_burn` | B | 4 days | 14 days | 4 days | 14 days | 0% | 0% | 0 |
| `dw_facial_contusion` | A | 2 days | 8 days | 2 days | 8 days | 0% | 0% | 0 |
| `dw_fungal_airway_exposure` | E | 3 hours | 1 day | 3 hours | 1 day | 0% | 0% | 0 |
| `dw_fungal_lung_involvement` | E | 3 days | 14 days | 3 days | 14 days | 0% | 0% | 0 |
| `dw_fungal_respiratory_irritation` | E | 12 hours | 4 days | 12 hours | 4 days | 0% | 0% | 0 |
| `dw_hairline_fracture` | B | 28 days | 56 days | 28 days | 56 days | 0% | 0% | 0 |
| `dw_heavy_bruise` | A | 2 days | 7 days | 2 days | 7 days | 0% | 0% | 0 |
| `dw_immobilized_partial_ligament_tear` | D | 18 days | 49 days | 18 days | 49 days | 0% | 0% | 0 |
| `dw_immobilized_partial_tendon_tear` | D | 21 days | 56 days | 21 days | 56 days | 0% | 0% | 0 |
| `dw_improvised_sutured_deep_facial_laceration` | B | 8 days | 24 days | 8 days | 24 days | 0% | 0% | 0 |
| `dw_improvised_sutured_deep_laceration` | B | 6 days | 18 days | 6 days | 18 days | 0% | 0% | 0 |
| `dw_improvised_sutured_laceration` | B | 3 days | 8 days | 3 days | 8 days | 0% | 0% | 0 |
| `dw_improvised_sutured_severe_laceration` | B | 18 days | 45 days | 18 days | 45 days | 0% | 0% | 0 |
| `dw_internal_organ_contusion` | D | 14 days | 45 days | 14 days | 45 days | 0% | 0% | 0 |
| `dw_internal_soft_tissue_trauma` | D | 10 days | 30 days | 10 days | 30 days | 0% | 0% | 0 |
| `dw_irrigated_cornea_abrasion` | B | 8 hours | 3 days | 8 hours | 3 days | 0% | 0% | 0 |
| `dw_irrigated_deep_chemical_burn` | B | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_irrigated_deep_oral_chemical_burn` | B | 7 days | 28 days | 7 days | 28 days | 0% | 0% | 0 |
| `dw_irrigated_mild_chemical_burn` | B | 12 hours | 4 days | 12 hours | 4 days | 0% | 0% | 0 |
| `dw_irrigated_moderate_chemical_burn` | B | 4 days | 14 days | 4 days | 14 days | 0% | 0% | 0 |
| `dw_irrigated_ocular_chemical_burn` | C | 4 days | 30 days | 4 days | 30 days | 0% | 0% | 0 |
| `dw_irrigated_oral_chemical_burn` | B | 1 day | 7 days | 1 day | 7 days | 0% | 0% | 0 |
| `dw_irritant_inhalation_injury` | F | 6 hours | 2 days | 6 hours | 2 days | 0% | 0% | 0 |
| `dw_jaw_fracture` | A | 35 days | 84 days | 35 days | 84 days | 0% | 0% | 0 |
| `dw_jaw_injury` | A | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_joint_subluxation` | D | 14 days | 42 days | 14 days | 42 days | 0% | 0% | 0 |
| `dw_laceration` | B | 3 days | 10 days | 3 days | 10 days | 0% | 0% | 0 |
| `dw_ligament_sprain` | D | 7 days | 21 days | 7 days | 21 days | 0% | 0% | 0 |
| `dw_major_internal_hemorrhage` | D | 21 days | 60 days | 21 days | 60 days | 0% | 0% | 0 |
| `dw_major_penetrating_organ_trauma` | D | 35 days | 100 days | 35 days | 100 days | 0% | 0% | 0 |
| `dw_massive_contusion` | A | 10 days | 28 days | 10 days | 28 days | 0% | 0% | 0 |
| `dw_mild_chemical_burn` | B | 1 day | 5 days | 1 day | 5 days | 0% | 0% | 0 |
| `dw_mild_cold_injury` | B | 12 hours | 4 days | 12 hours | 4 days | 0% | 0% | 0 |
| `dw_mild_smoke_inhalation` | E | 2 hours | 1 day | 2 hours | 1 day | 0% | 0% | 0 |
| `dw_minor_bruise` | A | 12 hours | 3 days | 12 hours | 3 days | 0% | 0% | 0 |
| `dw_minor_electrical_burn` | B | 1 day | 5 days | 1 day | 5 days | 0% | 0% | 0 |
| `dw_minor_internal_hemorrhage` | D | 5 days | 18 days | 5 days | 18 days | 0% | 0% | 0 |
| `dw_minor_ocular_contusion` | A | 1 day | 5 days | 1 day | 5 days | 0% | 0% | 0 |
| `dw_minor_puncture` | B | 12 hours | 4 days | 12 hours | 4 days | 0% | 0% | 0 |
| `dw_moderate_chemical_burn` | B | 5 days | 18 days | 5 days | 18 days | 0% | 0% | 0 |
| `dw_multiple_rib_fractures` | D | 56 days | 112 days | 56 days | 112 days | 0% | 0% | 0 |
| `dw_muscle_contusion` | D | 4 days | 12 days | 4 days | 12 days | 0% | 0% | 0 |
| `dw_muscle_laceration` | D | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_muscle_strain` | D | 5 days | 18 days | 5 days | 18 days | 0% | 0% | 0 |
| `dw_nerve_contusion` | D | 7 days | 21 days | 7 days | 21 days | 0% | 0% | 0 |
| `dw_ocular_electrical_injury` | A | 7 days | 45 days | 7 days | 45 days | 0% | 0% | 0 |
| `dw_ocular_freezing_injury` | B | 5 days | 18 days | 5 days | 18 days | 0% | 0% | 0 |
| `dw_ocular_laceration` | A | 7 days | 30 days | 7 days | 30 days | 0% | 0% | 0 |
| `dw_ocular_thermal_burn` | A | 7 days | 45 days | 7 days | 45 days | 0% | 0% | 0 |
| `dw_oral_chemical_burn` | B | 2 days | 10 days | 2 days | 10 days | 0% | 0% | 0 |
| `dw_oral_electrical_burn` | B | 3 days | 14 days | 3 days | 14 days | 0% | 0% | 0 |
| `dw_oral_freezing_injury` | B | 4 days | 16 days | 4 days | 16 days | 0% | 0% | 0 |
| `dw_oral_laceration` | B | 5 days | 18 days | 5 days | 18 days | 0% | 0% | 0 |
| `dw_oral_puncture_wound` | B | 1 day | 7 days | 1 day | 7 days | 0% | 0% | 0 |
| `dw_oral_thermal_burn` | B | 2 days | 10 days | 2 days | 10 days | 0% | 0% | 0 |
| `dw_partial_ligament_tear` | D | 21 days | 56 days | 21 days | 56 days | 0% | 0% | 0 |
| `dw_partial_muscle_tear` | D | 14 days | 42 days | 14 days | 42 days | 0% | 0% | 0 |
| `dw_partial_tendon_tear` | D | 21 days | 56 days | 21 days | 56 days | 0% | 0% | 0 |
| `dw_penetrating_gunshot_wound` | B | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_penetrating_ocular_injury` | A | 21 days | 90 days | 21 days | 90 days | 0% | 0% | 0 |
| `dw_penetrating_wound` | B | 10 days | 30 days | 10 days | 30 days | 0% | 0% | 0 |
| `dw_peripheral_nerve_injury` | D | 21 days | 70 days | 21 days | 70 days | 0% | 0% | 0 |
| `dw_protected_peripheral_nerve_injury` | D | 21 days | 70 days | 21 days | 70 days | 0% | 0% | 0 |
| `dw_puncture_wound` | B | 2 days | 8 days | 2 days | 8 days | 0% | 0% | 0 |
| `dw_reduced_joint_dislocation` | D | 14 days | 42 days | 14 days | 42 days | 0% | 0% | 0 |
| `dw_reduced_joint_subluxation` | D | 7 days | 21 days | 7 days | 21 days | 0% | 0% | 0 |
| `dw_repaired_ligament_rupture` | D | 42 days | 105 days | 42 days | 105 days | 0% | 0% | 0 |
| `dw_repaired_muscle_laceration` | D | 14 days | 42 days | 14 days | 42 days | 0% | 0% | 0 |
| `dw_repaired_muscle_rupture` | D | 35 days | 90 days | 35 days | 90 days | 0% | 0% | 0 |
| `dw_repaired_nerve_severance` | D | 90 days | 240 days | 90 days | 240 days | 0% | 0% | 0 |
| `dw_repaired_severe_muscle_laceration` | D | 28 days | 75 days | 28 days | 75 days | 0% | 0% | 0 |
| `dw_repaired_severed_tendon` | D | 60 days | 140 days | 60 days | 140 days | 0% | 0% | 0 |
| `dw_repaired_tendon_rupture` | D | 42 days | 105 days | 42 days | 105 days | 0% | 0% | 0 |
| `dw_rewarmed_deep_cold_injury` | B | 8 days | 24 days | 8 days | 24 days | 0% | 0% | 0 |
| `dw_rewarmed_deep_oral_freezing_injury` | C | 12 days | 45 days | 12 days | 45 days | 0% | 0% | 0 |
| `dw_rewarmed_mild_cold_injury` | B | 6 hours | 2 days | 6 hours | 2 days | 0% | 0% | 0 |
| `dw_rewarmed_ocular_freezing_injury` | B | 3 days | 14 days | 3 days | 14 days | 0% | 0% | 0 |
| `dw_rewarmed_oral_freezing_injury` | B | 2 days | 12 days | 2 days | 12 days | 0% | 0% | 0 |
| `dw_rewarmed_severe_cold_injury` | B | 18 days | 50 days | 18 days | 50 days | 0% | 0% | 0 |
| `dw_rewarmed_severe_ocular_freezing_injury` | C | 14 days | 60 days | 14 days | 60 days | 0% | 0% | 0 |
| `dw_rewarmed_superficial_cold_injury` | B | 2 days | 7 days | 2 days | 7 days | 0% | 0% | 0 |
| `dw_rib_contusion` | D | 5 days | 14 days | 5 days | 14 days | 0% | 0% | 0 |
| `dw_rib_fracture` | D | 35 days | 70 days | 35 days | 70 days | 0% | 0% | 0 |
| `dw_scratch` | B | 6 hours | 2 days | 6 hours | 2 days | 0% | 0% | 0 |
| `dw_severe_ballistic_internal_trauma` | D | 28 days | 75 days | 28 days | 75 days | 0% | 0% | 0 |
| `dw_severe_chest_wall_trauma` | D | 60 days | 120 days | 60 days | 120 days | 0% | 0% | 0 |
| `dw_severe_cold_tissue_injury` | B | 21 days | 60 days | 21 days | 60 days | 0% | 0% | 0 |
| `dw_severe_concussion` | A | 14 days | 45 days | 14 days | 45 days | 0% | 0% | 0 |
| `dw_severe_contusion` | A | 5 days | 14 days | 5 days | 14 days | 0% | 0% | 0 |
| `dw_severe_crush_trauma` | D | 30 days | 90 days | 30 days | 90 days | 0% | 0% | 0 |
| `dw_severe_electrical_tissue_injury` | B | 21 days | 70 days | 21 days | 70 days | 0% | 0% | 0 |
| `dw_severe_facial_contusion` | A | 5 days | 18 days | 5 days | 18 days | 0% | 0% | 0 |
| `dw_severe_gunshot_wound` | B | 21 days | 70 days | 21 days | 70 days | 0% | 0% | 0 |
| `dw_severe_irritant_lung_injury` | F | 3 days | 12 days | 3 days | 12 days | 0% | 0% | 0 |
| `dw_severe_laceration` | B | 14 days | 42 days | 14 days | 42 days | 0% | 0% | 0 |
| `dw_severe_maxillofacial_ballistic_trauma` | B | 18 days | 60 days | 18 days | 60 days | 0% | 0% | 0 |
| `dw_severe_ocular_trauma` | A | 14 days | 60 days | 14 days | 60 days | 0% | 0% | 0 |
| `dw_severe_penetrating_torso_injury` | D | 21 days | 60 days | 21 days | 60 days | 0% | 0% | 0 |
| `dw_severe_penetrating_wound` | B | 21 days | 60 days | 21 days | 60 days | 0% | 0% | 0 |
| `dw_severe_peripheral_nerve_injury` | D | 60 days | 180 days | 60 days | 180 days | 0% | 0% | 0 |
| `dw_severe_smoke_inhalation` | E | 4 days | 14 days | 4 days | 14 days | 0% | 0% | 0 |
| `dw_severe_thermal_airway_injury` | F | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_severe_toxic_lung_injury` | E | 7 days | 30 days | 7 days | 30 days | 0% | 0% | 0 |
| `dw_shallow_cut` | B | 12 hours | 5 days | 12 hours | 5 days | 0% | 0% | 0 |
| `dw_significant_internal_hemorrhage` | D | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_skull_fracture` | A | 42 days | 90 days | 42 days | 90 days | 0% | 0% | 0 |
| `dw_smoke_inhalation_injury` | E | 1 day | 5 days | 1 day | 5 days | 0% | 0% | 0 |
| `dw_soft_tissue_crush_injury` | D | 21 days | 60 days | 21 days | 60 days | 0% | 0% | 0 |
| `dw_splinted_closed_fracture` | B | 35 days | 70 days | 35 days | 70 days | 0% | 0% | 0 |
| `dw_splinted_comminuted_fracture` | C | 70 days | 140 days | 70 days | 140 days | 0% | 0% | 0 |
| `dw_splinted_displaced_fracture` | C | 49 days | 98 days | 49 days | 98 days | 0% | 0% | 0 |
| `dw_splinted_hairline_fracture` | B | 21 days | 42 days | 21 days | 42 days | 0% | 0% | 0 |
| `dw_split_lip` | B | 2 days | 8 days | 2 days | 8 days | 0% | 0% | 0 |
| `dw_stabilized_displaced_rib_fracture` | D | 42 days | 84 days | 42 days | 84 days | 0% | 0% | 0 |
| `dw_stabilized_flail_chest` | D | 70 days | 140 days | 70 days | 140 days | 0% | 0% | 0 |
| `dw_stabilized_multiple_rib_fractures` | D | 49 days | 98 days | 49 days | 98 days | 0% | 0% | 0 |
| `dw_stabilized_open_fracture` | C | 84 days | 168 days | 84 days | 168 days | 0% | 0% | 0 |
| `dw_stabilized_severe_chest_wall_trauma` | D | 49 days | 105 days | 49 days | 105 days | 0% | 0% | 0 |
| `dw_stabilized_severe_peripheral_nerve_injury` | D | 45 days | 140 days | 45 days | 140 days | 0% | 0% | 0 |
| `dw_stabilized_sternal_fracture` | D | 35 days | 70 days | 35 days | 70 days | 0% | 0% | 0 |
| `dw_sternal_fracture` | D | 42 days | 84 days | 42 days | 84 days | 0% | 0% | 0 |
| `dw_superficial_bite_wound` | F | 2 days | 7 days | 2 days | 7 days | 0% | 0% | 0 |
| `dw_superficial_burn` | B | 1 day | 4 days | 1 day | 4 days | 0% | 0% | 0 |
| `dw_superficial_freezing_injury` | B | 3 days | 10 days | 3 days | 10 days | 0% | 0% | 0 |
| `dw_superficial_gunshot_wound` | B | 5 days | 18 days | 5 days | 18 days | 0% | 0% | 0 |
| `dw_superficial_partial_thickness_burn` | B | 7 days | 21 days | 7 days | 21 days | 0% | 0% | 0 |
| `dw_supported_cracked_rib` | D | 18 days | 36 days | 18 days | 36 days | 0% | 0% | 0 |
| `dw_supported_ligament_sprain` | D | 5 days | 18 days | 5 days | 18 days | 0% | 0% | 0 |
| `dw_supported_muscle_strain` | D | 3 days | 10 days | 3 days | 10 days | 0% | 0% | 0 |
| `dw_supported_partial_muscle_tear` | D | 10 days | 30 days | 10 days | 30 days | 0% | 0% | 0 |
| `dw_supported_rib_fracture` | D | 28 days | 56 days | 28 days | 56 days | 0% | 0% | 0 |
| `dw_supported_tendon_strain` | D | 7 days | 21 days | 7 days | 21 days | 0% | 0% | 0 |
| `dw_sutured_deep_facial_laceration` | B | 6 days | 20 days | 6 days | 20 days | 0% | 0% | 0 |
| `dw_sutured_deep_laceration` | B | 5 days | 14 days | 5 days | 14 days | 0% | 0% | 0 |
| `dw_sutured_laceration` | B | 2 days | 6 days | 2 days | 6 days | 0% | 0% | 0 |
| `dw_sutured_severe_laceration` | B | 14 days | 35 days | 14 days | 35 days | 0% | 0% | 0 |
| `dw_tearing_bite_wound` | F | 14 days | 42 days | 14 days | 42 days | 0% | 0% | 0 |
| `dw_tendon_strain` | D | 7 days | 21 days | 7 days | 21 days | 0% | 0% | 0 |
| `dw_thermal_airway_injury` | F | 3 days | 14 days | 3 days | 14 days | 0% | 0% | 0 |
| `dw_toxic_inhalation_injury` | E | 2 days | 10 days | 2 days | 10 days | 0% | 0% | 0 |
| `dw_treated_soft_tissue_crush_injury` | D | 10 days | 35 days | 10 days | 35 days | 0% | 0% | 0 |
| `dw_upper_airway_irritation` | E | 1 hour | 12 hours | 1 hour | 12 hours | 0% | 0% | 0 |

## Treatment-gated definitions

These definitions intentionally have no finite native timer. Their existing treatment
graphs reach a finite treated state; the strict validator checks that transitively.

- `dw_avulsion_wound` (category C)
- `dw_comminuted_fracture` (category C)
- `dw_compartment_syndrome` (category D)
- `dw_deep_oral_electrical_tissue_injury` (category C)
- `dw_deep_oral_freezing_injury` (category C)
- `dw_devastating_ballistic_wound` (category C)
- `dw_devastating_bite_injury` (category F)
- `dw_devastating_maxillofacial_ballistic_injury` (category C)
- `dw_devastating_penetrating_wound` (category C)
- `dw_displaced_fracture` (category C)
- `dw_extensive_chemical_burn` (category C)
- `dw_extensive_cryogenic_tissue_injury` (category C)
- `dw_extensive_electrical_tissue_destruction` (category C)
- `dw_extensive_full_thickness_burn` (category C)
- `dw_flail_chest` (category D)
- `dw_full_thickness_burn` (category C)
- `dw_full_thickness_chemical_burn` (category C)
- `dw_irrigated_extensive_chemical_burn` (category C)
- `dw_irrigated_full_thickness_chemical_burn` (category C)
- `dw_irrigated_severe_corrosive_oral_injury` (category C)
- `dw_joint_dislocation` (category D)
- `dw_ligament_rupture` (category D)
- `dw_muscle_rupture` (category D)
- `dw_nerve_severance` (category D)
- `dw_ocular_chemical_burn` (category C)
- `dw_open_fracture` (category C)
- `dw_rewarmed_extensive_cold_injury` (category C)
- `dw_severe_corrosive_oral_injury` (category C)
- `dw_severe_muscle_laceration` (category D)
- `dw_severe_ocular_freezing_injury` (category C)
- `dw_severe_oral_thermal_injury` (category C)
- `dw_severe_penetrating_oral_injury` (category C)
- `dw_severe_soft_tissue_crush_injury` (category D)
- `dw_severed_tendon` (category D)
- `dw_tendon_rupture` (category D)
