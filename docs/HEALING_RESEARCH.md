# Healing lifecycle research

This audit targets the installed build:

- CDDA experimental `2026-08-10-0437`
- commit `251cf6cf23a0277d5118b67bee0efc9625c6cfeb`

The installed source snapshot under `/tmp` was read only. No CDDA C++ source was
modified, patched, compiled, or added to the mod.

## Native wound timing

The native wound object is the authoritative timer, but the timer is not exposed
to JSON.

Relevant installed-source paths and functions:

- `src/character.cpp`, `Character::process_turn`: calls `update_wounds( 1_turns )`
  once per character turn.
- `src/character_health.cpp`, `Character::update_wounds`: passes the elapsed turn
  to every bodypart.
- `src/bodypart.cpp`, `bodypart::update_wounds`: erases any wound for which
  `wound::update_wound` returns true.
- `src/wound.cpp`, `wound::update_wound`: adds the elapsed duration directly to
  `healing_progress` and completes at `healing_progress >= healing_time`.
- `src/wound.cpp`, `wound::healing_percentage` and `wound::get_pain`: calculate
  progress internally and reduce pain by `1 - healing_percentage()`.
- `src/wound.cpp`, `wound::serialize`/`deserialize`: save `type`,
  `healing_time`, `healing_progress`, and `pain` for each wound instance.

The update path applies the same elapsed turn while awake, resting, or asleep.
It does not inspect health, nutrition, vitamins, traits, mutations, effects,
medical skill, or treatment. This commit therefore implements wound recovery as
wall-clock character time. Existing healing modifiers for ordinary bodypart HP
are separate and do not alter this wound timer.

Pain decreases continuously because `get_pain()` uses the native percentage.
Functional penalties do not: `bodypart::wound_adjusted_limb_value` in
`src/bodypart.cpp` sums each wound type's static `limb_scores` values without
consulting healing progress. The medical UI likewise displays the wound type's
fixed name and description; percentage is shown only in debug mode.

Natural completion is a `std::remove_if`/erase operation in
`bodypart::update_wounds`. It sends no event, invokes no EOC, and prints no
message.

## Treatment behavior

`fix_wound_activity_actor::finish` in `src/activity_actor.cpp`:

1. verifies the original wound and requirements;
2. consumes components/tools;
3. calls `bodypart::remove_wound` for every `wounds_removed` ID;
4. calls `bodypart::add_wound` for every `wounds_added` ID;
5. practices skills/proficiencies and prints the fixed success message.

The new wound is constructed from its wound type. It receives a fresh random
`healing_time`, zero `healing_progress`, and fresh pain. Progress from the source
wound is not transferred.

`wound_fix` loading in `src/wound.h` and `src/wound.cpp` has no `success_eoc`,
`on_success`, or equivalent callback field. `character_finished_activity` is
sent before the activity actor's `finish` method and exposes only character,
activity ID, and canceled state. It does not expose bodypart, source wound,
target wound, or wound-fix ID.

## JSON wound inspection

No JSON-accessible wound identity/progress query exists in this commit.

The complete source search found no dialogue condition, talker method, or math
function corresponding to:

- `u_has_wound` / `npc_has_wound`;
- wound enumeration by ID/bodypart;
- wound healing time/progress/percentage.

The available dialogue effects are implemented in `src/npctalk.cpp`:

- `u_add_wound` / `npc_add_wound` call `bodypart::add_or_worsen_wound`;
- `u_remove_wound` / `npc_remove_wound` remove specified IDs;
- `u_pick_bodypart` / `npc_pick_bodypart` can filter to a bodypart that has at
  least one wound, but cannot identify which wound it has.

The installed `doc/JSON/EFFECT_ON_CONDITION.md` documents the same interface.
There is no hidden wound condition to prove with headless validation.

## Wound lifecycle events

`src/event.h` defines no wound-created, wound-replaced, wound-removed, or
wound-healed event. `Character::apply_wound`, `bodypart::add_wound`, and natural
removal do not send one. Damage events provide damage/bodypart context, not the
native primary wound selected afterward.

Consequences:

- native primary creation cannot initialize a wound-specific tracker;
- natural completion cannot trigger an exact final message;
- treatment cannot cancel or replace a pending wound-specific timer;
- delayed JSON cannot verify that reinjury progressed the wound to another ID.

## Effect capabilities

Effects can be bodypart-local and can vary their name, description, and modifiers
by intensity. `int_decay_step`, `int_decay_tick`, and `int_decay_remove` can
decrease intensity and eventually remove an effect. `remove_message` is printed
only for the avatar in `Creature::remove_effect`, and removal emits
`character_loses_effect` with character, bodypart, and effect ID.

These features are not a safe wound controller in this build:

- effect intensity changes do not emit an event or invoke an EOC;
- an effect cannot read or share the wound instance's randomly selected healing
  duration;
- treatment cannot remove/replace the correct tracker;
- multiple wound instances on one bodypart cannot be represented by one effect
  instance without merging their timers;
- an effect may expire before or after the wound, making a completion message
  false.

`remove_message` is therefore not used as an approximate wound-healed message.

## Recurring and scheduled EOCs

Recurring EOCs can run for the avatar and NPCs, and scheduled `run_eocs` calls can
preserve context variables and the character talker. Neither mechanism can test
for a particular wound ID or its progress. A stale transition would be unable to
distinguish:

- the original wound still existing;
- the wound having healed naturally;
- native treatment having replaced it;
- reinjury having progressed it to a worse state.

Running per-wound/per-bodypart recurring dispatchers would add cost without
solving identity or synchronization. Scheduled transitions would be capable of
resurrecting or downgrading replaced wounds and are rejected.

## Taking ownership of primary generation

The existing damage-type overlays could technically add primary wounds from
`ondamage_eocs`, but this does not solve the lifecycle safely:

- native primary selection would have to be disabled for every current wound to
  prevent duplicates;
- EOC `u_add_wound` does not enforce the automatic selector's `limit` check;
- the EOC API cannot query the affected `bp` variable's limb type/flags, so full
  compatibility would require hardcoded vanilla bodypart IDs;
- recreating every native weighted overlap exactly would be large and brittle;
- most importantly, native `wound_fix` would still replace wounds without a
  tracker callback.

Taking over primary generation while leaving native treatment unsynchronized
would only move the race condition. It is not a safe v0.2 architecture.

## Reinjury progression

`bodypart::add_or_worsen_wound` in `src/bodypart.cpp` checks a wound type's
`wound_progression` only when that same wound ID is added again. On a successful
progression it constructs the target wound, adds the old and new healing times,
adds pain, resets progress to zero, removes the old wound, and adds the new one.
This is damage-driven worsening, not timed healing.

A separate JSON timer cannot observe that replacement and could later downgrade
the new injury. Existing reinjury progression is therefore left unchanged.

## Completion messages

An exact one-per-wound message requires one of:

1. a native wound-healed event carrying character, bodypart, and wound ID;
2. a safe query that confirms the final wound state before JSON removes it; or
3. a tracker initialized/replaced by native wound creation and `wound_fix` using
   the exact wound instance duration.

This commit provides none of those. `u_message` could print a message, and effect
removal could notify the avatar silently for NPCs, but neither can be synchronized
to the wound. No completion message is enabled because a false message is worse
than no message.

## Required engine capability

The requested lifecycle becomes safely representable if CDDA exposes either:

- wound JSON fields such as stage thresholds/final message evaluated against the
  native wound instance; or
- JSON conditions/math access for wound ID, bodypart, healing time, and healing
  progress, plus wound-created/healed and wound-fix-completed events carrying
  character/bodypart/wound/fix context.

Progress-preserving wound replacement would also be needed if visible stages use
separate wound IDs. Until one of those interfaces exists, the safe result is to
retain the native timer and document the UI limitation rather than implement a
desynchronizing parallel state machine.
