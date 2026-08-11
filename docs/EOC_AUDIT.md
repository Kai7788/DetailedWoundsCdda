# EOC classification audit

The structural baseline contained 148 EOCs. Four orphaned dormant entries were removed after the final reference audit, and the production implementation adds 11 hook/event EOCs, for a final total of 155.

## A — reusable outcome EOCs (50)

All EOCs in these files remain reusable outcomes with their established IDs and wound actions:

- `eocs/structural/outcomes_limb_soft_tissue.json` — 22;
- `eocs/structural/outcomes_limb_bone.json` — 6;
- `eocs/structural/outcomes_internal_torso.json` — 10;
- `eocs/structural/outcomes_thoracic.json` — 8 (five serious outcomes now also apply finite acute chest restriction, while preserving their wound outcome IDs/actions).

Also classified A:

- `EOC_DW_STRUCTURAL_NONE` — common weighted no-op;
- `EOC_DW_MINOR_INTERNAL_HEMORRHAGE`;
- `EOC_DW_SIGNIFICANT_INTERNAL_HEMORRHAGE`;
- `EOC_DW_MAJOR_INTERNAL_HEMORRHAGE`.

The hemorrhage outcomes add only the internal hemorrhage wound and a message; they do not fake internal blood loss with external `bleed`.

## B — reusable route EOCs adapted to damage context (35)

These existing IDs now use `damage_taken` bins and exactly one weighted list:

- `EOC_DW_STRUCTURAL_LIMB_BASH_MINOR`
- `EOC_DW_STRUCTURAL_LIMB_BASH_MODERATE`
- `EOC_DW_STRUCTURAL_LIMB_BASH_SEVERE`
- `EOC_DW_STRUCTURAL_LIMB_BASH_EXTREME`
- every EOC in `eocs/structural/route_limb_penetrating.json` — 12 cut/stab/bullet routes;
- every EOC in `eocs/structural/route_limb_energy.json` — 7 electrical/heat routes;
- every EOC in `eocs/structural/route_torso.json` — 12 bash/stab/bullet routes.

These preserve the established route IDs and outcome families while replacing the unavailable `wound_id` condition and independent multi-family rolls.

## C — obsolete wound-ID bridge EOCs retained for compatibility (6)

- `EOC_DW_BRIDGE_ON_WOUND_CREATED`
- `EOC_DW_BRIDGE_ROUTE_INITIAL_COMPLICATION`
- `EOC_DW_BRIDGE_ON_WOUND_TREATED`
- `EOC_DW_STRUCTURAL_ROUTE_LIMB`
- `EOC_DW_STRUCTURAL_ROUTE_TORSO`
- `EOC_DW_STRUCTURAL_ON_WOUND_CREATED`

They have no production root in the installed build. Keeping their IDs avoids unnecessary compatibility churn and preserves a documented future integration point; they are not advertised as active.

## D — unreachable but potentially useful/deliberately dormant EOCs (53)

### Consolidated compatibility routes (3)

- `EOC_DW_STRUCTURAL_LIMB_BONE_MODERATE`
- `EOC_DW_STRUCTURAL_LIMB_BONE_SEVERE`
- `EOC_DW_STRUCTURAL_LIMB_BONE_EXTREME`

These IDs are retained as no-op compatibility entries because bone outcomes now share the one production bash roll.

### Bite routes (4)

Every EOC in `eocs/structural/route_limb_bites.json`. The installed bite actor has no JSON success EOC, and generic damage cannot distinguish bites from claws/weapons.

### Dormant complication graph (13)

Every retained EOC in `eocs/complications/wound_complications.json` except the three active internal hemorrhage outcomes listed under A. This includes contamination/infection/necrosis and initial complication rolls.

### Dormant maintenance graph (10)

Every EOC in `eocs/maintenance/wound_maintenance.json`. The progression guards remain validated, but no contamination entry path is enabled without a safe treatment exit.

### Dormant treatment graph (23)

Every retained EOC in `eocs/treatment/wound_treatment_logic.json`. Native wound treatment exposes no bodypart/wound-aware completion callback.

`EOC_DW_TREATMENT_DOWNGRADE_LOCAL_INFECTION` and `EOC_DW_TREATMENT_CLEAR_LOCAL_INFECTION` are exact allowlisted dormant roots. They remain valid bodypart-aware downgrade/clear operations for a future treatment callback; no production path invokes them today.

## Removed orphaned EOCs (4)

These entries had no production, compatibility, or dormant caller and were removed rather than allowlisted as unexplained dead data:

- `EOC_DW_REOPEN_LACERATION`
- `EOC_DW_REOPEN_DEEP_LACERATION`
- `EOC_DW_REOPEN_SEVERE_LACERATION`
- `EOC_DW_TREATMENT_LOCAL_INFECTION`

The three reopening handlers could not safely determine whether their expected sutured wound existed on `bp`; invoking them without that unavailable query could remove nothing and create an unrelated open wound. The orphaned infection dispatcher added no capability beyond its retained downgrade/clear building blocks.

## New production EOCs (11)

### Damage entry hooks (6)

- `EOC_DW_DAMAGE_BASH_SECONDARY`
- `EOC_DW_DAMAGE_CUT_SECONDARY`
- `EOC_DW_DAMAGE_STAB_SECONDARY`
- `EOC_DW_DAMAGE_BULLET_SECONDARY`
- `EOC_DW_DAMAGE_ELECTRIC_SECONDARY`
- `EOC_DW_DAMAGE_HEAT_SECONDARY`

### Respiratory source event/routes (5)

- `EOC_DW_RESPIRATORY_SOURCE_EFFECT`
- `EOC_DW_RESPIRATORY_ROUTE_SMOKE`
- `EOC_DW_RESPIRATORY_ROUTE_IRRITANT`
- `EOC_DW_RESPIRATORY_ROUTE_TOXIC`
- `EOC_DW_RESPIRATORY_ROUTE_FUNGAL`

These 11 are active roots/routes. The strict validator checks that overlay roots and event roots reach valid EOCs, wounds, effects, and 100-point weighted distributions.
