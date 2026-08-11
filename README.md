# Detailed Wounds

Detailed Wounds is a JSON-only Cataclysm: Dark Days Ahead mod that adds persistent injury states and native treatment chains alongside ordinary limb HP.

- Version: **0.1**
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
- Wound and treated-state save persistence, as confirmed in the Phase A and Phase D runtime tests.

Secondary routing deliberately selects at most one result per damage type in a hit. Low damage usually produces no structural wound; higher post-armor damage increases both the chance and severity.

## Installation

Place this directory in CDDA's `mods` directory and enable **Detailed Wounds** (`detailed_wounds`) when creating a world. It depends only on `dda`.

Detailed Wounds does not replace limb HP. Incoming damage still uses normal CDDA health and native primary wound selection; the mod adds additional injury state and treatment decisions.

## Compatibility

Production hooks extend vanilla damage types with a same-ID self-copy overlay. This is the safe mechanism for the audited build and preserves the complete previously loaded damage type before appending a Detailed Wounds EOC. Loader behavior must be re-audited when updating to a materially different CDDA build.

Structural routing currently recognizes standard vanilla flesh arm, hand, leg, foot, and torso IDs. This safely excludes full bionic replacement limbs, but nonstandard extra limbs do not receive secondary structural wounds because the installed EOC API cannot query the `bp` context's bodypart type or flags.

## Validation

Run the repository audit in strict mode:

```bash
python3 tools/validate_mod.py --strict
```

Regenerate the coverage matrix with:

```bash
python3 tools/validate_mod.py --strict --coverage-output docs/WOUND_MATRIX.md
```

The validator checks JSON structure, duplicate IDs, CDDA references, wound and treatment graphs, permanently non-healing wounds, damage overlays, EOC graphs, weighted distributions, progression relationships, limb-score anatomy, reserved data, and known regressions.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Wound and treatment coverage](docs/WOUND_MATRIX.md)
- [Runtime results and regression plan](docs/TEST_PLAN.md)
- [Damage-hook source audit](docs/SECONDARY_WOUND_HOOKS.md)
- [EOC classification audit](docs/EOC_AUDIT.md)
- [Known limitations](docs/KNOWN_LIMITATIONS.md)
- [Changelog](CHANGELOG.md)

The contamination/infection treatment lifecycle, generic physical bite identification, thermal-airway source detection, and treated-suture reopening remain explicitly limited by the installed JSON API. They are not claimed as working features.
