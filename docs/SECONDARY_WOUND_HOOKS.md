# Secondary wound hook audit

This audit is specific to installed CDDA experimental build `2026-08-10-0437`, commit `251cf6cf23a0277d5118b67bee0efc9625c6cfeb`. Repository-relative source paths below refer to that exact commit.

## Safe damage-type extension

The supported mechanism in this build is a same-ID self-copy overlay:

```json
{
  "type": "damage_type",
  "id": "bash",
  "copy-from": "bash",
  "ondamage_eocs": [ "EOC_DW_DAMAGE_BASH_SECONDARY" ]
}
```

Detailed Wounds uses this for `bash`, `cut`, `stab`, `bullet`, `electric`, and `heat` in `eocs/hooks/damage_type_overlays.json`.

### Loader evidence

- `src/init.cpp`, `DynamicDataLoader`: registers `damage_type` to `damage_type::load_damage_types`.
- `src/damage.cpp`, `damage_type::load_damage_types`: loads through file-local `generic_factory<damage_type> damage_type_factory`.
- `src/generic_factory.h`, `generic_factory<T>::load` and `handle_inheritance`: `copy-from` clones the already loaded object and sets inherited loading state.
- `src/damage.cpp`, `damage_type::load`: directly appends top-level `onhit_eocs` and `ondamage_eocs` entries.
- `src/generic_factory.h`, `generic_factory<T>::insert`: replaces the existing same-ID factory entry with the preserved clone.

A bare duplicate definition starts from a default object and can lose required/current/future vanilla members. It is unsafe. This loader does not read `ondamage_eocs` through an extend/delete-aware helper, so `extend` and `delete` cannot append or remove these vectors.

Correct self-copy overlays compose in load order: each copies the current object, including EOCs added by an earlier correctly written overlay.

## Execution timing and context

The runtime path is:

1. `src/creature.cpp`, `Creature::deal_damage`, copies the incoming damage and calls `absorb_hit`.
2. Per-type hardcoded handling runs in `Creature::deal_damage_handle_type`.
3. `damage_instance::ondamage_effects` runs after armor/type adjustment and before final bodypart HP application.
4. `src/damage.cpp`, `damage_type::ondamage_effects`, creates the EOC dialogue and context.

Context values are:

- `bp`: hit bodypart ID;
- `damage_taken`: current type's post-armor amount;
- `total_damage`: current type's corresponding pre-armor amount, not the attack-wide total.

Talkers are oriented as:

```text
u / alpha   = damage source
npc / beta  = damaged target
```

Production entry EOCs require `npc_is_character` and `_damage_taken > 0`. They use `run_eocs` with `alpha_talker: "npc"` and `beta_talker: "u"`; `src/npctalk.cpp`, `talk_effect_fun_t::func f_run_eocs`, shows that this creates a swapped dialogue while preserving the complete context. The existing outcome EOCs can therefore retain their established `u_add_wound({ context_val: bp })` actions with the damaged character as `u`.

## Multiple and resisted damage types

`damage_instance::ondamage_effects` keeps a set of used damage-type IDs:

- every unique damage type in a mixed attack can invoke its independent EOC once;
- repeated units of the same type invoke that type only once;
- the implementation uses the first corresponding pre/post unit rather than summing repeated units.

Fully armor-resisted but non-immune damage can still invoke the hook with `damage_taken == 0`; immune damage types are skipped. Every production hook therefore checks positive post-armor damage before routing.

## Production routing policy

Damage cutoffs follow the existing primary/secondary severity ranges:

| Damage | Limb production bins | Torso production bins |
|---|---|---|
| bash | 8–15, 16–25, 26–44, 45+ | 12–25, 26–44, 45+ |
| cut | 7–13, 14–22, 23–34, 35+ | no structural route |
| stab | 9–16, 17–26, 27–39, 40+ | 4–8, 9–16, 17–26, 27–39, 40+ |
| bullet | 6–12, 13–23, 24–39, 40+ | 6–12, 13–23, 24–39, 40+ |
| electric | 6–11, 12–20, 21–31, 32–44, 45+ | none |
| heat | 35–49, 50+ | none |

Each matching tier runs exactly one weighted list. “None” remains a possible result in every tier, and no route independently rolls every structural family. This bounds a type/hit to at most one secondary structural wound while making severe outcomes increasingly likely.

Head, eyes, and mouth do not enter generic structural routes. Acid, cold, biological, and pure damage receive no structural damage-type overlay because no appropriate general structural family exists.

## Anatomy limits

The hook recognizes standard vanilla arm, hand, leg, foot, and torso IDs. Full bionic replacement parts in the audited data use distinct IDs (for example `robofac_arm_bionic_basic_l`) and do not enter the flesh routes.

No installed EOC condition can query the limb type or `BIONIC_LIMB`/`NON_FLESH_LIMB` flag for an arbitrary `bp` context variable. Explicit IDs are therefore the safe choice; nonstandard extra limbs are documented as unsupported for secondary routing.

## Source-specific respiratory events

`src/creature.cpp`, effect application, emits `character_gains_effect`; `src/event.h`, `event_spec<character_gains_effect>`, exposes character, bodypart, effect, and intensity. `EOC_DW_RESPIRATORY_SOURCE_EFFECT` requires `bodypart == "mouth"` and routes only:

- `smoke_lungs`;
- `teargas`;
- `poison` / `badpoison`;
- `fungus`.

The mouth bodypart is what distinguishes inhalation from eye exposure, ingestion, monster poison, or systemic fungal infection. Vanilla `data/json/field_type.json` applies the smoke, tear-gas, and toxic-gas effects to mouth. `src/map_field.cpp`, `map::player_in_field`, applies `fungus` to mouth for `fd_fungal_haze` (and contains an additional mouth-targeted tear-gas path). Thermal-airway injury lacks an equally precise event and remains dormant.

`character_gains_effect` is not emitted for intensity-only changes to an already present effect. Routing therefore uses the intensity at first acquisition and deliberately avoids a periodic poll that could duplicate wounds without a specific wound-query condition.

Tear gas produces the mouth-localized `dw_upper_airway_irritation`. Its existing deeper irritant states are torso wounds and cannot be reached by native progression, which always replaces a wound on the same bodypart; they remain dormant rather than being placed on the wrong anatomy.

## Bite audit

`src/mattack_actors.cpp`, `bite_actor::on_damage`, is source-specific but exposes no JSON success EOC. The damage hook does not receive attack identity. The vanilla infection `bite` effect is applied only on `infection_chance`, so it cannot stand in for all physical bite trauma. General bite wounds remain dormant to avoid false claw/weapon classifications.

## Treatment callback audit

`src/activity_actor.cpp`, `fix_wound_activity_actor::finish`, performs the wound replacement without sending an EOC/event containing its bodypart or wound IDs. `character_finished_activity` lacks that data. No contamination/treatment bridge is enabled from native wound treatment.

## Revalidation requirement

Recheck the damage factory, damage execution path, talker orientation, event fields, and wound activity when changing the supported CDDA commit. Master documentation is not authoritative when it differs from the installed build.
