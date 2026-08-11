# Architecture

Detailed Wounds is entirely JSON. It uses native wounds and `wound_fix` for persistent state, plus EOCs only where the installed CDDA build exposes a complete lifecycle.

## Damage paths

```text
Damage event
├── native CDDA wound selection
│   └── primary or anatomically specialized wound
│
└── damage_type ondamage_eoc
    ├── post-armor damage/bodypart gate
    ├── one severity route
    └── zero or one secondary structural wound
```

Primary selection and secondary routing are independent. `ondamage_eocs` does not expose the primary wound ID, so secondary injuries derive from damage type, post-armor magnitude, anatomy, and a bounded weighted outcome.

The vanilla damage-type overlays use same-ID `copy-from` so the complete loaded vanilla object is preserved before the mod EOC is appended.

## Wound layers

### Primary wounds

Automatically selected from incoming damage. Generic limb wounds deliberately exclude eyes (`sensor`) and mouth; specialized files cover those anatomies instead.

### Secondary wounds

Structural consequences added explicitly by production EOCs. Their contradictory `whitelist_bp_with_flag`/`blacklist_bp_with_flag` `BIONIC_LIMB` filters are defense-in-depth against native automatic selection, not an error.

Production families include limb muscle/tendon/ligament/joint/nerve/bone/crush trauma, torso internal/hemorrhagic/thoracic trauma, and source-specific respiratory wounds.

### Treated wounds

Persistent post-treatment states added only by native `wound_fix`. They use the same automatic-selection exclusion as secondary wounds.

## Treatment

```text
Primary or secondary wound
        │
   native wound_fix
        │
cleaned / irrigated / supported / repaired state
        │
optional later wound_fix
        │
closed / debrided / stabilized state
        │
      healing
```

Some severe wounds intentionally have no `healing_time`; their treatment graph must reach a state with finite healing. `tools/validate_mod.py` verifies this transitively.

Minor care remains accessible at health care 0 without mandatory proficiency. Advanced procedures use progressively higher skills, materials, tools, and optional/mandatory proficiencies as already defined by their `wound_fix` entries.

## Repeated injury

```text
same production wound added again
        │
bodypart::add_or_worsen_wound
        │
native wound_progression chance
        │
logically worse existing wound
```

In the audited source, progression is checked only when the same wound type is added again. It is therefore used on production-reachable structural/respiratory wounds and automatically reachable fractures. It is not placed on treated-only sutures, where it would be inert.

## Respiratory and chest-wall effects

The `character_gains_effect` event provides source-specific respiratory entry for mouth-targeted smoke, tear gas, toxic poison, and fungus effects. The EOC adds an anatomically appropriate torso lung wound or mouth upper-airway wound plus finite global `dw_respiratory_impairment`.

Severe thoracic structural outcome EOCs add finite global `dw_chest_wall_impairment`. Global modifiers are necessary because vanilla breathing is supplied by the mouth bodypart while these wounds live on torso. Natural expiration avoids any dependency on a missing treatment callback.

## Dormant compatibility infrastructure

The following remains defined but is not a production entry path:

- native wound-created bridge and old wound-ID routers;
- native wound-treated bridge;
- contamination, local infection, and necrosis maintenance;
- treatment-triggered cleanup/reopening;
- physical bite structural routes;
- thermal-airway respiratory wounds.

These systems are retained only where they remain coherent future building blocks. Their exact blockers are in [known limitations](KNOWN_LIMITATIONS.md), and every EOC is classified in [the EOC audit](EOC_AUDIT.md).

## Validation boundaries

The validator distinguishes:

- automatic primary applicability;
- explicit production secondary reachability;
- treatment graph reachability;
- active versus allowlisted dormant EOC roots;
- intentional reserved requirements;
- valid native limb scores for all anatomically possible targets.

No C++ patch, fictional `wound_fix` callback, or generic biological/bite approximation is part of the architecture.
