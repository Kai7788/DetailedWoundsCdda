# v0.2 feedback capability research

## Audited build

- CDDA experimental: `2026-08-10-0437`
- Commit: `251cf6cf23a0277d5118b67bee0efc9625c6cfeb`
- Installed bundle: `cataclysmdda-0.J`
- Read-only source snapshot used for the audit: commit-matched CDDA `src/`

No C++ source was modified, patched, compiled, or added to the mod. The installed
commit remains authoritative for every decision below.

## Capabilities used by v0.2

### Production EOC acquisition messages

`u_message` is a safe avatar-only message point. Installed
`doc/JSON/EFFECT_ON_CONDITION.md` documents that `u_message` displays only when the
alpha talker is the avatar. `talk_effect_fun_t::f_message` in `src/npctalk.cpp`
resolves the alpha talker and returns without printing when the target is an NPC.

Detailed Wounds' production damage routes already swap talkers before invoking
structural outcome EOCs. The damaged character is therefore `u` at the outcome,
so one `u_message` can accompany the one selected `u_add_wound`. NPC wounds still
generate and heal without filling the avatar's log.

The respiratory `character_gains_effect` event also places the exposed character
in the alpha talker. Each source/severity branch can safely add its wound, finite
impairment, and one acquisition message together.

This is the strongest v0.2 feedback point because JSON knows that the precise
Detailed Wounds outcome is being added. The wording describes sensation rather
than exposing internal wound IDs or over-diagnosing anatomy.

### Native treatment messages

`wound_fix.success_msg` is loaded by `wound_fix::load` and printed by
`fix_wound_activity_actor::finish` in `src/activity_actor.cpp` after requirements
are consumed and the source/target replacement succeeds. It is the authoritative
treatment-completion feedback point.

All 109 Detailed Wounds fixes already had non-empty messages. v0.2 retains them
and makes the seven previously identical chest-support messages specific to the
actual stabilization performed. No unsupported treatment EOC is added.

### Finite acute recovery messages

Installed `doc/JSON/EFFECTS_JSON.md` supports `remove_message`. In
`Creature::remove_effect` (`src/creature.cpp`) the message is printed only when the
affected creature is the avatar, immediately before `character_loses_effect` is
sent.

Detailed Wounds already applies `dw_respiratory_impairment` and
`dw_chest_wall_impairment` for finite, severity-based durations. Their expiration
is therefore a real observable recovery milestone. v0.2 adds a restrained message
when each restriction expires. The messages deliberately say breathing/tightness
has eased, not that the longer wound has healed.

## Capabilities audited but not used as feedback hooks

### Native primary wound creation

Native selection creates a wound after damage but emits no event containing the
selected wound ID. `ondamage_eocs` exposes damage/bodypart context, not the primary
wound selected later. Primary acquisition messages would require guessing which
wound won an overlapping weighted selection and could duplicate the structural
message. They remain silent.

### Natural wound healing and completion

`wound::update_wound` in `src/wound.cpp` increments private
`healing_progress`; `bodypart::update_wounds` in `src/bodypart.cpp` erases the
wound at completion. There is no JSON wound query, wound-created/healed event, or
completion message. The exact source audit remains in
[HEALING_RESEARCH.md](HEALING_RESEARCH.md).

Effects, recurrence, and scheduled EOCs cannot verify the original wound after
treatment or reinjury and cannot share its randomized native duration. v0.2 does
not print a false healing message or run a second healing clock.

### Native wound progression

`bodypart::add_or_worsen_wound` evaluates `wound_progression` only while adding
the same wound ID again. It replaces the wound internally, but emits no event or
EOC and prints only a debug-mode message. JSON cannot know whether the progression
chance succeeded.

The production outcome message therefore uses wording valid for either a newly
created structural injury or a real aggravating event. v0.2 does not claim a
distinct “reopened” message when the engine does not reveal that distinction.

### Bodypart interpolation

EOC messages can interpolate context strings, but `bp` is an internal bodypart ID
and this API offers no reliable conversion from a dynamic context value to a
localized possessive bodypart name. Correct generic phrasing such as “the struck
limb” is preferred over exposing `arm_l` or relying on fragile tag behavior.

## Resulting v0.2 architecture

```text
production structural/source event
→ exactly one selected wound outcome
→ one avatar-only acquisition message

native wound_fix succeeds
→ source removed / treated state added
→ native success_msg

finite acute breathing effect expires
→ impairment actually ends
→ one avatar-only recovery milestone

native wound timer completes
→ wound silently removed by CDDA
→ no unsafe parallel message
```

This adds meaningful feedback wherever JSON owns or observes the real transition,
while leaving unobservable native lifecycle points honest and unchanged.
