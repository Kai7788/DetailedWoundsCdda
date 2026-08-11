# Detailed Wounds

Detailed Wounds is a JSON-only Cataclysm: Dark Days Ahead mod that adds persistent injury states and native treatment chains alongside ordinary limb HP.

- Version: **0.2**
- Author: **Kai Maier**
- Audited CDDA build: **2026-08-10-0437** (`251cf6cf23a0277d5118b67bee0efc9625c6cfeb`)

## Working systems

- Damage-selected primary wounds for bash, cut, stab, bullet, heat, acid, electric, and cold damage.
- Specialized eye, mouth, face, head, and torso wounds without weakening the generic eye/mouth exclusions.
- Native `wound_fix` treatment chains, including cleaning, irrigation, dressing, suturing, debridement, stabilization, repair, and rewarming.
- Skill-zero basic care for minor wounds; skills and proficiencies matter progressively for advanced treatment.
- JSON-only secondary structural routing from post-armor bash, cut, stab, bullet, electric, and severe heat damage.
- Source-specific respiratory wounds for inhaled smoke, tear gas, toxic gas, and fungal exposure.
- Finite acute respiratory and chest-wall breathing impairment that expires without needing a missing treatment callback.
- Native `wound_progression` when the same production-reachable structural wound is inflicted again.
- Severity-aware, avatar-only acquisition feedback for every production structural and respiratory outcome.
- Family-specific native treatment-completion messages for all 109 wound fixes.
- Honest recovery milestones when finite acute respiratory or chest-wall restriction expires.
- Wound and treated-state save persistence, as confirmed in the Phase A and Phase D runtime tests.

Secondary routing deliberately selects at most one result per damage type in a hit. Low damage usually produces no structural wound; higher post-armor damage increases both the chance and severity.

## How Detailed Wounds works

```text
Take damage
→ receive a visible primary wound
→ possibly receive one deeper structural injury
→ inspect the medical menu
→ apply an appropriate treatment
→ see the cleaned, closed, supported, or repaired state
→ recover on CDDA's native wound timer
```

Primary wounds describe the direct injury. Secondary wounds describe deeper damage
caused by the same event, so two wounds on one bodypart are not necessarily
duplicates. For example:

- a cut can become `laceration → cleaned laceration → sutured laceration`;
- a gunshot wound may appear alongside a tendon or nerve injury when the projectile
  damages deeper structures;
- a severe cold injury may remain unable to heal until controlled rewarming or
  debridement produces a recoverable treated state.

Minor scratches and bruises usually recover without expert care. Serious fractures,
deep tissue destruction, ruptures, and similar injuries may require stabilization
or repair before their native recovery timer can run. Further damage can worsen
eligible injuries. An in-game **Detailed Wounds** help page is also appended to
CDDA's normal help menu.

## Installation

Place this directory in CDDA's `mods` directory and enable **Detailed Wounds** (`detailed_wounds`) when creating a world. It depends only on `dda`.

Detailed Wounds does not replace limb HP. Incoming damage still uses normal CDDA health and native primary wound selection; the mod adds additional injury state and treatment decisions.

## Compatibility

Production hooks extend vanilla damage types with a same-ID self-copy overlay. This is the safe mechanism for the audited build and preserves the complete previously loaded damage type before appending a Detailed Wounds EOC. Loader behavior must be re-audited when updating to a materially different CDDA build.

Structural routing currently recognizes standard vanilla flesh arm, hand, leg, foot, and torso IDs. This safely excludes full bionic replacement limbs, but nonstandard extra limbs do not receive secondary structural wounds because the installed EOC API cannot query the `bp` context's bodypart type or flags.

## Healing and feedback

CDDA already advances a private native timer for every finite wound and gradually
reduces wound pain. In the audited build, JSON cannot read that progress, receive a
wound-created/healed event, or observe a completed `wound_fix` with wound/bodypart
context. A separate effect/EOC timer would desynchronize after treatment or
reinjury and could print a false healing message.

For that reason, visible timed healing stages and exact wound-completion messages
are not claimed as working features. v0.2 instead adds feedback at transitions
JSON can prove: a selected production secondary/respiratory wound, a successful
native treatment, and expiration of a finite acute breathing restriction. The
last message describes the restriction easing; it does not falsely claim the
longer wound has healed.

The repository contains a complete 256-wound classification, unchanged-duration
audit, source-backed capability analysis, gameplay-feel audit, message policy, and
generated message coverage report. Native wound timing and save compatibility
remain unchanged from v0.1.

## Validation

Run the repository audit in strict mode:

```bash
python3 tools/validate_mod.py --strict
```

Regenerate the coverage matrix with:

```bash
python3 tools/validate_mod.py --strict --coverage-output docs/WOUND_MATRIX.md
```

Regenerate the healing audits with:

```bash
python3 tools/validate_mod.py --strict \
  --healing-matrix-output docs/HEALING_MATRIX.md \
  --healing-duration-output docs/HEALING_DURATION_AUDIT.md \
  --message-audit-output docs/V02_MESSAGE_AUDIT.md \
  --polish-audit-output docs/V02_POLISH_AUDIT.md
```

The validator checks JSON structure, duplicate IDs, CDDA references, wound and treatment graphs, permanently non-healing wounds, damage overlays, EOC graphs, weighted distributions, progression relationships, limb-score anatomy, reserved data, and known regressions.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Wound and treatment coverage](docs/WOUND_MATRIX.md)
- [Runtime results and regression plan](docs/TEST_PLAN.md)
- [Damage-hook source audit](docs/SECONDARY_WOUND_HOOKS.md)
- [EOC classification audit](docs/EOC_AUDIT.md)
- [Known limitations](docs/KNOWN_LIMITATIONS.md)
- [Healing system architecture](docs/HEALING_SYSTEM.md)
- [Healing lifecycle source research](docs/HEALING_RESEARCH.md)
- [Complete healing classification](docs/HEALING_MATRIX.md)
- [Healing duration audit](docs/HEALING_DURATION_AUDIT.md)
- [v0.2 capability research](docs/V02_RESEARCH.md)
- [v0.2 gameplay-feel audit](docs/V02_GAMEPLAY_AUDIT.md)
- [Message design policy](docs/MESSAGE_DESIGN.md)
- [Generated message coverage](docs/V02_MESSAGE_AUDIT.md)
- [Final wound/treatment polish audit](docs/V02_POLISH_AUDIT.md)
- [Changelog](CHANGELOG.md)

Visible timed healing stages/exact completion messages, distinct native-progression success messages, the contamination/infection treatment lifecycle, generic physical bite identification, thermal-airway source detection, and treated-suture reopening remain explicitly limited by the installed JSON API. They are not claimed as working features.
