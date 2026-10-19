# 아펩의 오아시스 파수꾼 (Apep, Guardian of Apep's Oasis) rig: API (stage AP-R1)

The display-entity rig of the chapter-3 boss: one superset skeleton of 49 parts that carries both forms (phase 1 종막,
phase 3 기원) and both stances (CROUCH, UPRIGHT). It is the contract between the rig and the Apep module
(`tools/mboss_apep/*`, AP-CORE). Binding inputs: scratchpad `ap/plan.md` R1-R22 (rig decisions), `ap/ap_contract.md`
§0.4 (the manifest schema and the rig API, frozen), `ap/spec/rig_manifest.schema.json` and the frozen clip table
`ap/spec/stub_rig_manifest.json`. References: `ap/understand/model.md`, `model_p3.md`, `motion.md`, `mechanics.md`.

Stage R1 delivers the block-out of every part in both forms, the skeleton with both stances, the hand variants, the
looks and tints, the 11 hit proxies, the capsules, burrow and park, and **stub clips**: every clip of the frozen table
exists with its length, events, hidden spans, stance / look / hand / state events, sinks and px tracks, but its keys
are the stance poses (plus the stance blends of `stand_p3`, `crouch_p3` and the blends inside clips). AP-RC1 authors
the motion; AP-R2 refines the five regions (`S:ap/rigwork/r1_worklist.md`).

## 0. Files

```
node tools/build_mboss_apep_rig.mjs --resourcepack <unpacked RP> [--datapack <dp>] [--no-paint | --paint a,b]
     [--debug-dp <scratch dir> [--debug-clips a,b | all]] [--residuals] [--allow-steps]
```

| file | owns |
|---|---|
| `build_mboss_apep_rig.mjs` | items (forms, hands, faces, cores, tint variants), models / item definitions / atlas, the clip compile, pose checks, the R3 residual table, coverage gate, follow lists, the API functions, the manifest |
| `apep_pose.mjs` | the skeleton (`BONES`, bind = CROUCH), `PART_*` tables (name, region, brightness P1 / P3, display scale), `solve()` (FK, limb IK with hand orientation, the parametric tail, root pivot), per-form authoring frames (`FRAMES`, `modelFrames`, `toDisplay`), `FORM_POINTS`, `ANCHOR_POINTS`, `PROXIES`, `CAPSULES` |
| `apep_clips.mjs` | `DEFAULT_POSE`, `STANCES` (CROUCH, UPRIGHT, CRAWL = CROUCH with the P3 hand orientation, MID = the halfway key of a stance blend), the clip table (generated from the stub), stub keys, sinks (`SINK_TABLE`), debug poses `dbg_*` |
| `apep_geometry.mjs`, `apep_paint.mjs` | thin aggregators over the five regions (duplicate names fail the build) |
| `apep_materials.mjs` | palette ramps, tint slots and looks, the shared grey tiles (`g_shell`, `g_plate`, tail bands), gold / cone / emerald / lime / robe / gem / core tiles, sprite helpers |
| `apep_head.mjs` | neck, head, face (P1 bud-skull + crescents, P3 mask), hood (one cowl for both stances), crown, hair ×4 |
| `apep_body.mjs` | abdomen (P1 rear body / P3 robe stem), hem_a / hem_b, chest, shoulders, core (P1 bulb / P3 sternum), crys_low / crys_back, mantle ×4 |
| `apep_limbs.mjs` | the six limb segments ×2 per form, the P3 bead vines |
| `apep_hands.mjs` | the 20 hand models (A `p1_planted p1_raised p3_fork`, B `p1_open p1_curl p3_curl p3_open`, C `p1_open p1_curl p3_curl`) |
| `apep_tail.mjs` | the seven banded segments (shared by both forms, tinted) and the two tips (P1 scythe hook + leaf curl, P3 whip + leaf) |

Every region module exports `REGION`, `PARTS`, `models()` (model units), `FORM_MODELS {part: {p1, p3}}`, `sprites()`.
The builder owns and rewrites `data/rlk/function/mboss/apep/rig/**` and, in the RP, `assets/rlk/{textures,models/item,
items}/mboss/apep/**` (stale files removed) plus the atlas entries; never hand-edit them. The shared libraries
(`mboss_shape_lib`, `mboss_model_lib`, `mboss_paint_lib`, `mboss_rig_math`, `mboss_rig_clips`, `mboss_rig_compile`)
are used unchanged (R20). `--debug-dp` writes `ap_dbg/<clip>/<t>` (exact poses; the `dbg_*` poses always, real clips
with `--debug-clips`), `ap_dbg/look/<form>[_<tint>]`, `ap_dbg/face/*`, `ap_dbg/hands/*`, `ap_dbg/crawl_look`,
`ap_dbg/player_{ref,front,far}`, `ap_dbg/px/<pose>`, `ap_dbg/caps/<pose>` and the overlay pack `<dir>/rp_ref` for the
offline renderer (`S:az/understand/rigtech_render.py`, wrapper `S:ap/rigwork/r1/r.sh`). The `dbg_*` poses never enter
the shipped rig or the manifest.

## 1. Calls (all `rlk:mboss/apep/rig/…`; @s = the anchor, at its feet, unless noted)

| function | when | what |
|---|---|---|
| `init` | load | objectives (§5) |
| `spawn` | spawn / respawn | kills old parts, summons the 49 parts + the shadow in the rest pose of the stored form and stance with every stored look, the state and the park mask |
| `tick` | every tick | parked: returns at once. Else respawns missing parts, follows the anchor (position + yaw; the burrow sink through follow_y), advances the clip, the hit flash |
| `play/<clip>` | any time | plays a clip from tick 0 at the next `tick` (36 clips, §4) |
| `start/<clip>` | internal | chains into a clip now |
| `face/player`, `face/track`, `face/set {yaw}` | AI | turns the anchor (track ≤ 2° per call) |
| `stance/crouch`, `stance/upright` | outside clips | stores `apRigStance` and snaps every part to the rest pose of that stance in the current form (`stance/apply` re-applies; `stance/r/<stance>_<form>` internal) |
| `look/form/<p1\|p3>` | spawn, the CS swap | swaps every non-hand, non-face, non-core part to its form model and sets the form's face, core and hands, tint `none` (`also`) |
| `look/face/<p1_bud\|p3_idle\|p3_charge\|p3_dim\|hidden>` | clips, module | the face item; `hidden` = the empty model |
| `look/core/<p1_bulb\|p3_sternum>`, `look/core_glow/<idle\|lit>` | | the core item / its brightness 12 or 15 |
| `look/tint/<none\|p1_dark\|p1_brown\|withered\|p3_dim>` | burrow, sink, death | re-items every part to `<model>_t<id>` (constant tints, §3) |
| `bright/13`, `bright/15` (= `look/bright/*`) | the P3 charge | every part at its own level / at 15 |
| `look_apply` | after a respawn | re-applies every look channel from the objectives |
| `hands/<p1_rest\|p1_lift\|p3_open\|p3_curl>`, `hand/<part>/<variant>` | clips, module | hand models (a 2-tick 0.9 → 1.0 scale pulse hides the swap) |
| `state/normal`, `state/burrowed` | burrow clips | visibility state (`burrowed`: every part at scale 0 and the parts stop following; `normal`: the next clip key shows them) |
| `park`, `unpark` | phase 2 (R10) | every part scale 0, shadow off, `tick` skipped; a respawn while parked keeps the mask; `unpark` re-applies form, stance, looks, hands and the follow |
| `flash/<head\|body\|front\|rear\|tail\|arms>` | `on_hit` | 3-tick outline of one part group; `flash_tick` / `flash_off` internal |
| `kill`, `uninstall` | cleanup | parts / parts and objectives |

The rig never moves the anchor (except `face/*`), owns no proxy runtime (the framework's `px/*` reads the manifest),
and reads no module score.

## 2. Entities

49 item displays `524c4b4d-4150-4400-8000-0000000000NN` (NN = 0x00-0x30, the frozen order of `manifest.parts`), the
shadow `…40`; proxies `…41`-`…4B` belong to the framework (positions in the manifest). Tags `rlk_room rlk_mb_aux
rlk_mb_part rlk_mb_apep_part rlk_mb_ap_<part>` (the shadow: `rlk_room rlk_mb_aux rlk_mb_apep_part rlk_mb_ap_shadow`).
Culling 30 × 16, view range 3, `billboard fixed`, brightness per part (P1 13 / 14 on the gold and crystal parts; P3 per
`PART_BRIGHT_P3`).

## 3. Forms, stances, looks

- **Superset skeleton.** One skeleton, bind = CROUCH. UPRIGHT is reached by joint angles only (no rescaled bones):
  pelvis 6-DOF lift and pitch, the abdomen as the robe stem, the hood hinge ~107° (the cowl's front tip becomes the
  8.5 b peak behind the face). R3 residuals vs `model_p3` §6.2: max 0.234 b over 60 joints (`stances.residuals`).
- **Authoring frames.** Each part's model is authored in a reference stance per form (`parts[].frames`): P1 models at
  CROUCH, P3 models at UPRIGHT (world axes 'w', or the bone frame 'y' / 'z' for limbs, hem, mantle, hair, tail). The
  display rotation is `R_pose · R_ref⁻¹ · A`, so a P3 model shows as authored in UPRIGHT and a P1 model in CROUCH; the
  hood and the tail are authored once at CROUCH for both forms; the crawl (P3 at CROUCH) turns its hands to their
  UPRIGHT world orientation (`STANCES.CRAWL`, hand eulers `hf_*`).
- **Per-form model points** (`FORM_POINTS`): the face, core, crown and hood top of each form (the face and sternum are
  not joints); anchors and tracks use them.
- **Tints** (R12): every painted face has `tintindex` 0-4 (slots paint / shell / plate / band_a / band_b). Each item
  definition carries 5 constant tints = the form's slot colour × the tint look colour × the face look colour; grey
  shared sprites (`g_*`, `use: "tinted"`) take their colour from the slot. Tint looks: `p1_dark` #2D2A04 and `p1_brown`
  #605D37 (P1 items only), `withered` #8C8458 and `p3_dim` #6F8A73 (P3 items only). Faces: `p3_idle` / `p3_charge`
  (#FFC06A) / `p3_dim` are one model under three colours. The builder fails on an untinted face.
- **Hands** (R8): 4 sets; `stand_p3` opens the left B hand at 5 and the rest at 8, `crouch_p3` curls at 2; the plan's
  phase-3 "open" / "curl" = `p3_open` / `p3_curl`.

## 4. Clips

The 36 clips of the frozen table (`ap_contract.md` §0.4.10), ids in table order. R1 keys: the stance pose of each
segment; stance blends (`crouch_p3` 0-7, `stand_p3` 0-13, `move_strike_p3` 0-7 / 85-91, `aftermath` 72-84,
`sink_p3` 0-7, `tail_p3` 57-86, `death` 55-82 into the crawl before its sink) pass a halfway key with every limb on IK
and the B / C wrists 1.2 b off the water; hidden spans set every part to scale 0 one tick after the sink reaches
−6 b (follow_y offsets, `SINK_TABLE` −0.25 … −6.5), and the full follow list returns one tick before a span ends.
Per clip the manifest carries events, anchors (impact / muzzle / ball / face / core / crown / hood_top points per
event), tracks, px keys (fitted, with the mandatory ticks), yaw knots, hidden spans, stance / look / hand / state
events and extents.

## 5. Manifest and objectives

`tools/mboss_apep_rig_manifest.json`, validated by `python3 -I S:ap/spec/validate.py rig <manifest> --against
S:ap/spec/stub_rig_manifest.json`. Beyond the schema it records `parts[].frames`, `proxies.layout[].bone`,
`proxies.coverage`, `states.aloft.tops`, `stances.{residuals, hood_swing_deg, upright_top, face_centre_upright,
sternum_centre_upright, poses}`, `follow`, `keys_per_tick`, `elements.per_part`. Objectives: `apRigC` clip, `apRigT`
tick, `apRigF` flash, `apRigY` face scratch, `apRigState`, `apRigForm`, `apRigStance`, `apRigFace`, `apRigCore`,
`apRigGlow`, `apRigTint`, `apRigBright`, `apRigHands`, `apRigPark`, `apRigFl` / `apRigFy` / `apRigQ*` (RIGLIB follow).

## 6. Build checks and budgets

Strict by default (`--allow-steps` turns them into warnings for experiments): model bounds −16..32 and single-axis
rotations (R5), the R3 residual ≤ 0.25 b, hood swing ≥ 100°, upright top ≤ 9.0 b, untinted faces, every hand above
−0.2 b outside hidden spans, every part top ≤ −0.1 b at each hidden-span start (R9), no root travel, events inside the
clip, client-interpolation step checks (RIGLIB), the radial culling overhang, coverage ≥ 100 % within 3 b for CROUCH,
UPRIGHT, HOOP, CROUCH_OVER and CRAWL (R7). Budgets: 49 / 56 parts, atlas ≤ 0.9 M px (R13), elements at rest
P1 ≤ 7000 / P3 ≤ 8000 (R14). Suite: `S:ap/rigtests/test_ap_rig.py [--rebuild]` (static checks, mcsim runtime of spawn /
tick / looks / park / kill, determinism).

## 7. Deviations and decisions (R1)

- Hair parents to the **hood**, not the head: the hood swing carries the hair roots from the cowl sides (crouch) to
  beside the face (upright) inside the residual limit.
- The face look `hidden` uses the empty model (the effect of scale 0 kept through clip keys).
- Display scales raised for bounds: head 1.3, hem_b 1.7, core 1.3, crown 1.4.
- The v5 f1104 "umbrella" is the B arms seen from below (up-turned gold-coned tips, dark back, lime rim; v5 f1908), not
  the mantle; the mantle keeps scales 1.7 / 1.5.
- The death stub falls into the crawl (55-82) before its sink so that R9 holds; its stance score stays UPRIGHT.
