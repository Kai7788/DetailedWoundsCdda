# Healing system architecture

## Ideal complete lifecycle

The target user-facing lifecycle remains:

```text
fresh injury
→ early healing
→ advanced healing
→ almost healed
→ healed
```

Stage count should be severity-dependent, total recovery time should remain close
to the current native range, pain and functional penalties should decline
monotonically, treatment-required wounds should begin recovery only after
treatment, and the avatar should receive one concise final message.

## Complete current classification

The repository contains 256 wounds. Every one is assigned exactly once in
[the generated healing matrix](HEALING_MATRIX.md):

| Category | Meaning | Count |
|---|---|---:|
| A | Naturally healing primary | 21 |
| B | Treatment-optional primary family, including treated descendants | 98 |
| C | Treatment-required primary family, including treated descendants | 44 |
| D | Production-reachable secondary structural family and treated states | 70 |
| E | Production-reachable respiratory/exposure family | 9 |
| F | Dormant/unreachable family and descendants | 14 |

There are 221 finite native wound definitions and 35 treatment-gated definitions
without `healing_time`. All 35 retain a treatment path to a finite recoverable
state; the strict validator checks that graph.

## Architecture decision for the audited build

The requested timed visible stages cannot be implemented safely in installed
commit `251cf6cf23a0277d5118b67bee0efc9625c6cfeb` using JSON alone.

The detailed evidence is in [the research audit](HEALING_RESEARCH.md). The decisive
combination is:

```text
native wound progress is private to C++
+ no wound-ID/progress JSON query
+ no wound-created/healed event
+ no wound_fix completion context
= no safe way to synchronize a second JSON timer
```

Consequently, no gameplay lifecycle controller, stage wound, tracker effect, or
exact wound-completion message is enabled. v0.2 adds feedback only at transitions
JSON can prove: production injury creation, successful native treatment, and the
end of a finite acute breathing restriction. It does not resurrect treated wounds,
announce false healing, or strand old saves.

## Rejected designs

### Observe native progress

Preferred, but unavailable. `healing_percentage()` is used internally and shown
only by the medical UI's debug mode. Dialogue/math JSON cannot read it.

### Native lifecycle events

Unavailable. The event registry has no wound creation/removal/healing event.

### Companion effect controller

Rejected. Effects can decay and display intensity stages, but cannot share the
wound's randomized duration or receive treatment/reinjury synchronization. Their
removal messages could be early, late, or false.

### Scheduled or recurring EOC state machine

Rejected. EOCs cannot verify a wound ID before replacing it. A stale scheduled
transition could recreate an already treated wound or downgrade a reinjury.

### Detailed Wounds owns primary generation

Rejected. Damage EOCs could add wounds, but they cannot reproduce native limit and
dynamic anatomy behavior completely, and native `wound_fix` would remain
unobservable. It does not solve the critical race.

## Current safe healing behavior

The existing native system remains authoritative:

```text
finite wound
→ healing_progress advances one turn per character turn
→ pain continuously declines
→ wound disappears at its sampled healing_time
```

Static limb-score penalties do not decline before completion. Wounds without a
finite timer remain until their treatment graph creates a finite state. Treatment
constructs a new wound with a fresh duration and zero progress, exactly as in v0.1.
Existing saves retain their serialized wound type, duration, progress, and pain.

Finite `dw_respiratory_impairment` and `dw_chest_wall_impairment` effects now print
one avatar-only message when they actually expire. This is an acute recovery
milestone, not a claim that the longer wound has disappeared.

[The duration audit](HEALING_DURATION_AUDIT.md) confirms that this safe result
changes no healing range.

## Future implementation contract

When the required CDDA JSON capability becomes available, implementation should:

1. keep every existing v0.1 ID as an entry/migration state;
2. observe the native wound instance rather than duplicate its timer;
3. use two stages for very minor wounds, three for ordinary wounds, and three or
   four for serious treated injuries;
4. preserve total min/max recovery within approximately 10%;
5. reduce pain/functional penalties monotonically;
6. preserve treatment-required gates and realistic treatment windows;
7. extend damage-driven `wound_progression` separately for reinjury;
8. emit exactly one avatar-only completion message after verified removal;
9. progress NPC wounds silently;
10. validate every transition, duration sum, treatment target, reinjury edge, and
    completion mechanism before changing the mod version.

This contract prevents future work from confusing native damage progression with
timed recovery or reintroducing an unsafe parallel timer.
