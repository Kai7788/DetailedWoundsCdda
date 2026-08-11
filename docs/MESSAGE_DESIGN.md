# Message design

Detailed Wounds messages communicate a state change, not every state that exists.
The v0.2 policy is intentionally bounded so combat remains readable.

## Categories

The mod uses five conceptual categories:

1. **Injury acquired:** production secondary and source-specific respiratory EOCs.
2. **Injury worsened:** only when the engine exposes a verified worsening callback.
3. **Treatment completed:** native `wound_fix.success_msg`.
4. **Recovery milestone:** expiration of a finite acute respiratory/chest effect.
5. **Fully healed:** only when the engine exposes verified wound completion.

The installed build provides no safe hook for categories 2 and 5. They remain
documented gaps rather than being simulated with unsynchronized timers.

## Spam policy

- Native minor primary wounds rely on the wound UI and normal combat feedback.
- A production damage route selects at most one structural wound per damage type;
  that outcome may print one acquisition message.
- An attack containing several distinct damage types can still create independent
  structural outcomes and messages. This mirrors the existing per-type hook model
  and remains bounded by its damage thresholds and chances.
- Respiratory acquisition prints one message for the selected source/severity
  branch.
- Treatment prints one native success message only after the fix succeeds.
- Acute respiratory/chest recovery prints once when the finite effect expires.
- No recurring flavor EOC, minute-by-minute reminder, or parallel healing timer is
  used.

## Tone

Messages are short, physical, and non-clinical. They describe what the character
can feel:

- muscle: ache, pulling, tearing;
- tendon/ligament: tension, snapping, instability;
- joint: twisting, slipping, displacement;
- nerve: tingling, burning, numbness;
- bone: deep focused pain, giving, shifting;
- internal/ballistic: deep pain, pressure, searing trauma;
- thoracic: pain with breathing, instability;
- respiratory: coughing, burning airways, labored breathing.

The medical UI may identify the exact wound. The log avoids improbable instant
diagnosis.

## Severity

- Mild outcomes use restrained wording and `warning` message type.
- Serious outcomes use stronger wording and `bad` message type.
- Routine scratches and very light bruises do not gain additional dramatic text.

## Avatar, NPC, and bodypart handling

`u_message` and effect `remove_message` are avatar-only in the audited source, so
NPC injury/recovery is silent. Dynamic `bp` context is not converted to a clean
localized bodypart name by this JSON interface; messages use accurate generic
phrasing rather than leaking internal IDs.

## Correctness rule

A message may state only what its hook proves. Effect expiration may say breathing
is easier; it may not say the torso wound has healed. A repeated structural event
may describe pain or tissue giving; it may not assert that native
`wound_progression` succeeded. Natural completion stays silent until CDDA exposes
a wound-healed event or equivalent query.
