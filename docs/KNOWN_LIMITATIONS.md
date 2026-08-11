# Known limitations

This file distinguishes deliberate abstractions from features blocked by the audited CDDA JSON API.

## Visible timed healing stages and completion messages

Blocked for native wounds in installed commit `251cf6cf23a0277d5118b67bee0efc9625c6cfeb`.

Native wounds serialize and internally update `healing_time`, `healing_progress`,
and pain, but JSON cannot read a wound ID/progress pair on a bodypart. There is no
wound-created or wound-healed event, and natural completion erases the wound
without a message/EOC. Treatment constructs a new wound with fresh time/progress
without exposing bodypart/source/target/fix context to JSON.

Effects and scheduled EOCs cannot safely approximate this lifecycle: they cannot
share the wound's randomly sampled duration or confirm that treatment/reinjury has
not replaced it. A parallel timer could announce false healing or recreate an old
wound. No visible-stage controller or completion message is enabled.

Required CDDA capability: native wound-stage/final-message JSON fields, or JSON
access to wound ID/bodypart/time/progress plus wound-created, wound-healed, and
wound-fix-completed lifecycle context. See [the full research audit](HEALING_RESEARCH.md).

## Native wound-treatment completion callback

Blocked.

`fix_wound_activity_actor::finish` in `src/activity_actor.cpp` consumes requirements, removes/adds wounds, practices skills/proficiencies, and prints the success message without sending a wound-treatment event or invoking an EOC. `wound_fix` in `src/wound.h`/`src/wound.cpp` has no success-EOC member.

CDDA does emit `character_finished_activity`, but that event exposes only the character, activity ID, and cancellation state. It does not expose the treated bodypart, source wound, target wound, or `wound_fix` ID. Consequently it cannot safely clear a bodypart-specific complication.

Required CDDA capability: a native `wound_fix` success EOC or event carrying at least character, bodypart, source/target wound, and fix ID.

## Contamination, local infection, and necrosis lifecycle

Dormant by design.

The effects and maintenance EOCs remain internally defined, but enabling them on wound creation would create an entry path without a reliable treatment/exit path. `EOC_DW_BRIDGE_ON_WOUND_TREATED` is retained as a compatibility entry but has no native caller. Documentation does not claim contamination/infection as active.

Required CDDA capability: the treatment callback described above, or a wound-state query capable of safely synchronizing bodypart effects after treatment.

## Native wound-created bridge

Dormant.

Native primary wound selection does not invoke `EOC_DW_BRIDGE_ON_WOUND_CREATED` and `ondamage_eocs` does not provide the selected primary `wound_id`. Production secondary routing therefore derives from damage type, post-armor magnitude, and bodypart independently of primary wound selection.

Required CDDA capability: a wound-created event/EOC with character, bodypart, and selected wound ID. The production damage-event system does not require this capability.

## Physical bite identification

Blocked for general use.

`bite_actor::on_damage` in `src/mattack_actors.cpp` knows that an attack is a bite, but the JSON `bite` monster-attack schema exposes no success EOC. Generic damage EOCs know damage type and source/target, not which monster attack produced the damage; routing generic bash/cut/stab as a bite would misclassify claws and weapons.

The vanilla `bite` infection effect is not an adequate physical-trauma signal: `bite_actor` applies it only on its infection-chance roll, so it misses most physical bites. Monster attacks also lack the generic-factory self-copy semantics proven safe for damage types, making global same-ID overlays unsafe.

Required CDDA capability: a bite-attack success EOC carrying the hit bodypart and dealt damage, or an attack identity in the damage EOC context.

Existing Detailed Wounds bite definitions and routes remain reserved/dormant rather than producing false bite wounds.

## Respiratory source coverage

Partially active.

The `character_gains_effect` event safely identifies these inhaled sources when the event bodypart is `mouth`:

- `smoke_lungs` -> smoke inhalation wounds;
- `teargas` -> irritant airway injury;
- `poison`/`badpoison` -> toxic inhalation injury;
- `fungus` -> fungal respiratory injury.

The mouth filter is essential because poison and fungus can also be acquired through ingestion, attacks, or systemic processes.

`character_gains_effect` is emitted when the effect is first acquired, not whenever an existing effect rises in intensity. The selected respiratory tier therefore reflects the newly acquired effect's initial intensity. Polling continuously would duplicate wounds because this build has no bodypart-specific wound query, so intensity-only escalation is not approximated.

Vanilla tear gas is acquired at one effect intensity, so production routing reaches the mouth-localized `dw_upper_airway_irritation` state only. The deeper torso irritant states remain defined but dormant; native `wound_progression` cannot move a wound from mouth to torso.

Thermal-airway wounds remain dormant because this build exposes no distinct “inhaled superheated gas” effect/event. Generic heat damage to mouth is not proof of airway inhalation.

Required CDDA capability for the remaining subtype: a source-specific thermal inhalation effect/event or field EOC carrying exposure route and severity.

## Respiratory and chest-wall impairment synchronization

Implemented as a finite acute abstraction.

Vanilla breathing is a mouth limb score while Detailed Wounds respiratory/thoracic wounds are stored on torso. Source EOCs apply global `dw_respiratory_impairment` for a finite severity-based duration; severe thoracic outcome EOCs similarly apply finite `dw_chest_wall_impairment`. Both expire naturally and cannot trap the player in a permanent state.

These effects are not synchronized to the full wound healing duration because the missing treatment callback cannot remove them early. They represent acute breathing restriction, not the complete recovery curve.

## Treated-wound reopening

Blocked for treated-only states in this build.

Despite the broad wording in `doc/JSON/WOUNDS.md`, `bodypart::add_or_worsen_wound` in `src/bodypart.cpp` evaluates a wound type's `wound_progression` only when that same wound type is being added again. Sutured and repaired states are excluded from automatic selection by the deliberate contradictory `BIONIC_LIMB` gate, so ordinary damage never re-adds them. JSON also has no condition that queries a specific wound ID on a supplied bodypart.

Production-reachable secondary wounds do use native progression when the same structural outcome is inflicted again. Adding inert progression to treated sutures was intentionally avoided.

Required CDDA capability: progression of existing wounds whenever their bodypart is damaged, or a bodypart-specific `has_wound` EOC condition.

## Nonstandard and bionic limbs

Production structural hooks use explicit vanilla flesh IDs (`arm_l/r`, `hand_l/r`, `leg_l/r`, `foot_l/r`, and `torso`). Full bionic replacement limbs use different IDs in the audited data and are therefore excluded safely.

The installed EOC API cannot derive limb type or bodypart flags from the dynamic `bp` context. Extra mutation/mod limbs consequently retain primary wound support through native selection but do not receive production secondary structural wounds.

Required CDDA capability: a condition/mutator that queries limb type and flags for a bodypart variable.

## Internal hemorrhage mechanics

Internal hemorrhage is represented by distinct wounds and their pain/functional state. No external `bleed` effect is applied: doing so would misrepresent anatomy and can double-count vanilla bleeding. The current JSON API exposes no dedicated, treatment-synchronized internal blood-loss state used here.

Required CDDA capability for deeper integration: a safe internal blood-volume mechanic with distinct entry, progression, and treatment/exit hooks.

## Damage overlay compatibility

Same-ID self-copy overlays are proven for installed commit `251cf6cf23a0277d5118b67bee0efc9625c6cfeb`. A later correctly written mod overlay composes by copying the already modified object, but a later bare replacement can still discard fields/EOCs. Re-audit `generic_factory<damage_type>` and `damage_type::load` after updating CDDA.

## Reserved requirements

`dw_minor_debridement` and `dw_pressure_dressing` remain intentionally reserved. They are not forced into semantically unrelated treatments merely to eliminate unused definitions; the strict validator allowlists only these two requirement IDs.
