# Detailed Wounds contributor guidance

Detailed Wounds is a JSON-only Cataclysm: Dark Days Ahead mod. Do not modify or
require CDDA C++ as a solution. Preserve existing wound IDs because saves serialize
them, and preserve the specialized eye, mouth, head, torso, secondary, and treated
wound architecture.

The v0.1 primary/treatment baseline and specialized Phase D coverage have passed
runtime testing. Production secondary routing now uses audited JSON-only damage
and source-effect hooks. Prefer the smallest change that fixes an identified
problem; do not rebalance existing wounds or redesign working architecture without
a concrete functional reason.

Important invariants:

- The matching `whitelist_bp_with_flag` and `blacklist_bp_with_flag` value
  `BIONIC_LIMB` intentionally prevents automatic selection of secondary and treated
  wounds. Explicit `u_add_wound` and `wound_fix` additions still work.
- Multiple `whitelist_body_part_types` values have AND semantics and are suspicious.
- Severe wounds may intentionally omit `healing_time` until treatment makes them
  recoverable.
- Use `u_lose_effect`, never the stale `u_remove_effect` key.
- Keep `dw_ocular_laceration` covered through damage 1000.
- Do not restore the obsolete cold source IDs in `wounds_removed`.
- Do not allow contamination intensity 3 to be replaced by intensity 2.
- Generic `sensor` and `mouth` exclusions are intentional; fill coverage with
  specialized wounds rather than removing those exclusions.
- There is currently no native `wound_fix` success EOC. Keep bridge logic unless a
  current JSON-only lifecycle hook is proven, but do not claim dormant logic works.
- Vanilla damage-type hooks must use same-ID self-copy overlays. Never add a bare
  replacement for `bash`, `cut`, `stab`, `bullet`, `electric`, or `heat`.
- `ondamage_eocs` uses `u` as the damage source and `npc` as the damaged target.
  Production routes deliberately swap those talkers before calling existing
  `u_add_wound` outcome EOCs.
- Every production hook must test positive post-armor `damage_taken`; fully resisted
  non-immune damage can still invoke the EOC with zero damage.
- Production structural routing selects one weighted result per type/hit. Do not
  restore independent rolls for every tissue family.
- Physical bite, thermal-airway, contamination/treatment cleanup, and treated-state
  reopening are documented API limitations. Do not approximate them with generic
  damage or permanent effects.
- Native wound progress is not JSON-readable in audited commit `251cf6c`, and there
  are no wound-created/healed or context-rich wound-fix events. Do not add companion
  healing timers, scheduled stage transitions, or completion messages unless a
  newer build exposes enough lifecycle context to prevent treatment/reinjury races.
- Production wound-addition EOCs must keep one avatar-only acquisition message per
  wound outcome. Keep it sensory/non-clinical and valid for either a new structural
  injury or aggravation because native progression success is not observable.
- `dw_respiratory_impairment` and `dw_chest_wall_impairment` removal messages describe
  only expiration of the finite acute effect. They must never claim the longer wound
  has healed.

After a coherent implementation change, run:

```bash
python3 tools/validate_mod.py --strict
```

The validator automatically uses a sibling `cataclysmdda-0.J/data` directory when
present. A different build can be selected with `--cdda-data PATH`. Use
`--coverage-output docs/WOUND_MATRIX.md` to regenerate the coverage document.
Use `--healing-matrix-output docs/HEALING_MATRIX.md` and
`--healing-duration-output docs/HEALING_DURATION_AUDIT.md` to regenerate the
healing audits. Use `--message-audit-output docs/V02_MESSAGE_AUDIT.md` to
regenerate the feedback coverage report.

Do not mark runtime checks passed without an actual game test. Headless
`--check-mods` confirms loading and references, not combat frequency or balance.
