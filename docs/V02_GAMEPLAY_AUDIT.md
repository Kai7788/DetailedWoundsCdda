# v0.2 gameplay-feel audit

This audit asks what a player experiences, not merely whether an object exists.
“Native recovery” means CDDA advances the wound's private timer and reduces its
pain; the wound name, description, and limb-score modifiers remain fixed until it
disappears.

## Surface and energy injuries

| Family | Acquisition and player view | Consequence and treatment | Recovery/worsening feedback | v0.2 decision |
|---|---|---|---|---|
| Bruises | Native bash selection; visible as severity-specific bruising. | Pain and limb penalties scale by tier; most heal naturally. | Native pain fades; no observable completion callback. | No extra message for routine bruises; avoid combat spam. |
| Lacerations | Native cut selection; specialized eye/mouth variants remain separate. | Cleaning, dressing, proper/improvised closure, and debridement chains exist. | Treated names communicate state; sutured reopening cannot be observed reliably. | Retain native healing and strong family-specific treatment messages. |
| Punctures | Native stab selection with specialized oral/ocular states. | Irrigation/cleaning and severe debridement paths reflect deep localized injury. | Native timer is private; no safe stage callback. | Treatment feedback remains the reliable change signal. |
| Ballistic injuries | Native bullet selection with specialized oral/ocular/torso states. | Severe states impose strong pain/function costs and use debridement/stabilization. | Structural outcomes can announce deep damage; natural completion is silent. | Production-controlled deeper outcomes get severity-aware acquisition messages. |
| Fractures | Native/secondary bone outcomes appear in the wound UI. | Splinting/stabilization enables or improves recovery for severe states. | Repeated production outcome may progress the same wound, but success is not exposed. | Bone outcome messages describe the felt event; splint messages identify the procedure. |
| Thermal burns | Native heat selection; severe limb heat can produce compartment syndrome. | Dressing/debridement chains distinguish depth; severe states need care. | No native healing callback. | Compartment outcome announces dangerous pressure; burn UI/treatment text carries the rest. |
| Chemical burns | Native acid selection, including specialized oral/ocular injuries. | Irrigation is primary; severe states can continue to debridement. | Treatment chain is visible and runtime-tested; no completion callback. | Keep chemically specific irrigation/debridement success feedback. |
| Electrical injuries | Native electric wounds plus production nerve outcomes. | Surface treatment and nerve protection/repair exist by severity. | Production nerve event is observable; native healing is not. | Tingling, burning, numbness, and control-loss messages differentiate nerve trauma. |
| Cold injuries | Native cold selection, including ocular and oral specialized families. | Controlled rewarming and severe-tissue treatment paths exist. | Treated state visibly changes; final disappearance is silent. | Preserve restrained rewarming feedback; no exterior-dressing fiction. |

## Specialized anatomy

| Family | Acquisition and player view | Consequence and treatment | Recovery/worsening feedback | v0.2 decision |
|---|---|---|---|---|
| Head injuries | Native specialized wounds describe concussion/skull/facial trauma. | Pain and relevant penalties vary by tier; treatment paths exist where required. | Native selection and recovery expose no exact hook. | Do not guess head diagnoses from generic damage events. |
| Ocular injuries | Specialized sensor wounds cover all intended physical/energy types. | Vision/night-vision/reaction penalties and anatomy-specific irrigation/rewarming care. | Phase D generation/treatment passed; no natural-completion event. | Rely on wound UI and treatment confirmation; avoid repeated vision spam. |
| Oral/facial injuries | Specialized mouth wounds cover bash/cut/stab/bullet/heat/acid/electric/cold. | Eating, drinking, manipulation, and severe breathing penalties vary anatomically. | Treatment states are visible and Phase D chains passed. | Preserve distinct irrigation, debridement, closure, and rewarming messages. |

## Structural injuries

| Family | Acquisition and player view | Consequence and treatment | Recovery/worsening feedback | v0.2 decision |
|---|---|---|---|---|
| Muscle | Production bash/cut/stab/bullet routes; precise wound shown in UI. | Pain plus lift/movement/manipulation costs; support/repair by severity. | Outcome EOC is observable; progression success is not. | Add aching/pulling/tearing acquisition text valid for new or aggravated trauma. |
| Tendon | Weighted production limb outcome. | Persistent movement/control penalties; immobilization or repair. | Same limitation as muscle. | Add tension/snap/control-loss messages; keep treatment-specific success text. |
| Ligament | Weighted bash limb outcome. | Joint stability, footing, movement, or blocking penalties; support/repair. | Outcome observable, progression result private. | Add twist/buckle/tearing messages. |
| Joint | Weighted bash limb outcome. | Subluxation/dislocation causes major function loss; reduction/stabilization available. | No separate native worsening callback. | Add slipping/wrenching acquisition text without claiming an exact joint name. |
| Nerve | Cut/stab/bullet/electric production routes. | Tingling/numbness/control penalties; protection/repair by severity. | Outcome observable. | Add severity-aware electric/shooting/numbness messages. |
| Crush/compartment | High bash or severe heat production route. | Deep pain/function loss; debridement or decompression required for severe states. | Outcome observable; normal healing private. | Add compression/pressure messages; avoid routine-burn compartment spam through existing thresholds. |
| Thoracic | Torso bash/bullet routes choose rib/chest outcomes. | Pain plus finite acute breathing restriction for severe tiers; chest support treatment. | Structural event and finite effect expiration are observable. | Add one acquisition message, specific stabilization success, and one easing milestone. |
| Internal trauma | Torso bash/stab/bullet routes choose one deep outcome. | Deep pain/function state; severe wounds require stabilization/debridement paths. | Outcome EOC observable; internal native healing private. | Add non-clinical deep pain/pressure messages. |
| Internal hemorrhage | Conservative high-severity torso route; distinct wound state. | Wound represents internal injury without fake external bleed effect. | Existing acquisition messages are production-reachable; completion private. | Retain existing messages and avoid double-counting vanilla bleeding. |

## Respiratory injuries

| Family | Acquisition and player view | Consequence and treatment | Recovery/worsening feedback | v0.2 decision |
|---|---|---|---|---|
| Smoke, irritant, toxic, fungal exposure | Source-specific mouth effect event selects an injury; thermal-airway remains dormant. | Wound plus finite acute global breathing penalty; native wound recovery continues separately. | Acquisition branch and impairment expiration are both observable. | Add source/severity acquisition messages and one honest “breathing becomes easier” milestone. |

## Cross-system findings

- All 109 native wound fixes have non-empty success messages.
- Every source/target pair has a distinct display name and description, so treatment
  produces a visibly different state rather than a hidden ID-only replacement.
- Production structural routing remains one weighted outcome per type/hit, so the
  new message layer follows the existing anti-spam policy.
- Exact natural healing stages, final-healing messages, treated-state reopening,
  and distinct progression-success text remain blocked by missing wound lifecycle
  context.
- No gameplay values, probabilities, wound IDs, pain ranges, healing times, skills,
  proficiencies, or limb scores were changed for this pass.
