# 아펩의 오아시스 파수꾼 (Apep, Guardian of Apep's Oasis) rig: API (stage AP-RC2)

The display-entity rig of the chapter-3 boss: one superset skeleton of 49 parts that carries both forms (phase 1 종막,
phase 3 기원) and both stances (CROUCH, UPRIGHT). It is the contract between the rig and the Apep module
(`tools/mboss_apep/*`, AP-CORE). Binding inputs: scratchpad `ap/plan.md` R1-R22 (rig decisions), `ap/ap_contract.md`
§0.4 (the manifest schema and the rig API, frozen), `ap/spec/rig_manifest.schema.json` and the frozen clip table
`ap/spec/stub_rig_manifest.json`. References: `ap/understand/model.md`, `model_p3.md`, `motion.md`, `mechanics.md`.

History: AP-R1 built the skeleton with both stances, the block-out of every part, the hand variants, looks and tints,
the 11 hit proxies, capsules, burrow and park and stub clips. AP-R2 refined the five regions in parallel (one region
file each, `S:ap/rigwork/r1_worklist.md`); AP-RC1 keyed all 36 clips (§4). AP-R3 merged the five regions and the RC1
clips on `wip/ap-rig`, brought the atlas back under budget, fixed the cross-region seams and regenerated every output
(§7b). **AP-RC2** (this state) polished the clips against the merged geometry (§4, §7c): the model floor, the R2-claw
plants, R17 secondary motion, eased segments as linear pieces and per-class compiler tolerances (mean keys/t 19.9 ->
14.9); names, lengths and event ticks unchanged.

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
| `apep_head.mjs` | neck, head, face (P1 bud-skull + crescents, P3 rosette mask with the lily emblem, three looks on one model), hood (one cowl for both stances: P1 plate dome + ear flares, P3 visor / crest / horns / plate back, the crawl carapace), crown (P1 cone + sprig + bulb, P3 3D leaf fan + bud), hair ×4 (ribbons designed in world space: P1 drapes to the ground, P3 dark strands with a lime streak + an inner lime strand); P3 petal ruff + lime scarf leaves |
| `apep_body.mjs` | abdomen (P1 rear body / P3 robe stem), hem_a / hem_b (P3 hem flaps splayed on the water), chest (P1 hull + calyx, P3 rib-blade bands), shoulders (P1 hump, bark-dome pauldrons with projected contour tiers, hooks + gems; P3 chevron chest leaves, glossy back plates), core (P1 bulb / P3 chevron sternum), crys_low / crys_back, mantle ×4 (one tinted model: P1 horn blades, P3 carapace wings) |
| `apep_limbs.mjs` | the six limb segments ×2 per form (P1 arched shell paddles, armour legs flaring to a root base; P3 leaf-clad shells, antler blades, carapace plates, pale fringe), the P3 bead vines |
| `apep_hands.mjs` | the 20 hand models (A `p1_planted p1_raised p3_fork`, B `p1_open p1_curl p3_curl p3_open`, C `p1_open p1_curl p3_curl`): the P1 three-blade claw (raised = rolled hook), the spoon-petal feet with the cream cone, the P3 cupped five-lobe leaf hand with grey undersides, the tulip C curl with the spiral glyph, the bud B curl, the bracted fork |
| `apep_tail.mjs` | the seven banded segments (shared by both forms, tinted: two twisted straps, a scaled root sheath on tail_1 / 2 with a leaf frill) and the two tips (P1 spiral scroll + scythe crescent, P3 twisting whip + leaf) |

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
  UPRIGHT world orientation (`STANCES.CRAWL`, hand eulers `hf_*`) and pitches the P3 strands back off the B forearms
  (hair 1 −16° and 15° out, hair 2 −40° and 10° in; AP-RC2).
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

The 36 clips of the frozen table (`ap_contract.md` §0.4.10), ids in table order, keyed by AP-RC1 from `motion.md`, the
video analyses and the footage (`apep_clips.mjs`): a pose library (`POSES`, the P1 key poses of `MO` §5 and the P3
glossary of plan §6.2: UPRIGHT, CRAWL, HUNCH, MOUND, HOOP, SCOIL, CURL, BALL, V, CROUCH_OVER, BELLY_FLOP, KNEEL, …),
per clip keys `[t, pose, ease]` at authored ticks, `RETIME` knots (wind-ups −25 %, plan U4), hidden spans, yaw
schedules (the contract knots), look / face / core / tint / bright events and hand events (P1 clips swap a hand to its
lifted variant automatically when it leaves the ground). Between keys a floor pass re-keys the tail, hem and drape
chains tick by tick so they stay above the water (`GUARD`), except the `move_strike_p3` slam window t62-64 (the
belly-flop splash covers it). AP-RC2 adds the model floor (`PROBE`: bind-space model extremes per part and form; the body
lifts over a dipping hull or tail-root sheath, the hem / hair chains turn, the IK leg wrists rise over a dipping root
flare; per-tick corrections smoothed into an envelope of 14 deg / 0.06 b per tick), R17 secondary motion (`SECONDARY`:
damped spring followers in the world, the anchor yaw included, on the mantle, hair, hem and bead vines, faded out over a
clip's last 8 ticks) and eased segments of 4+ ticks as 2-4 linear pieces through their eased values (`easeKnots`). Stance
blends (`crouch_p3` 0-7, `stand_p3` 0-13 and the blends inside clips) pass a halfway key (`MID`)
with every limb on IK and the B / C wrists off the water. Hidden spans set every part to scale 0 one tick after the
sink reaches −6 b (follow_y offsets, `SINK_TABLE`), and the full follow list returns one tick before a span ends.

| clip | played / authored | next | hidden | yaw knots | keys/t (RC2) |
|---|---|---|---|---|---|
| `entrance_p1` | 110 | idle_p1 | 0-3 | — | 13.4 |
| `idle_p1` / `turn_p1` / `turn_p1_step` | 60 / 20 / 10 | loop / loop / idle_p1 | — | step 0:0 9:-90 | 2.1 / 14.4 / 15.6 |
| `crawl_p1` / `crawl_stop_p1` / `walk_p1` | 16 / 32 / 36 | loop / idle_p1 / loop | — | — | 17.1 / 12.7 / 12.1 |
| `burrow_strike` | 82 / 94 | idle_p1 | 22-43 | — | 18.4 |
| `sink_p1` / `emerge_on_p1` / `burrow_in_p1` / `emerge_crown_p1` | 17 / 24 / 23 / 40 | hold / rotation / hold / idle_p1 | 14-16 / 0 / 21-22 / 0-4 | — | 16.1 / 7.8 / 24.5 / 11.1 |
| `hands` | 140 / 160 | idle_p1 | — | 5:0 27:360 | 14.6 |
| `glow_slams` | 131 / 160 | idle_p1 | — | — | 20.9 |
| `rotation` | 130 / 135 | idle_p1 | — | 47:0 71:360 | 12.8 |
| `tail_p1x2` | 127 / 141 | idle_p1 | — | 27:0 35:200 51:200 59:0 | 12.1 |
| `combo_a` / `b` / `c` / `d` / `combo_end` | 29 / 44 / 20 / 77 / 20 | chained by the module | — | c 5:0 15:360 | 17.4 / 20.0 / 22.6 / 14.8 / 2.5 |
| `sink_revive` / `revival` | 60 / 160 | hold, park / idle_p3 | 45-59 / 0-59 | — | 9.2 / 6.6 |
| `idle_p3` / `turn_p3` / `walk_p3` | 60 / 20 / 32 | loop | — | turn 0:0 19:114 | 4.2 / 10.8 / 8.6 |
| `crouch_p3` / `stand_p3` | 8 / 14 | hold / idle_p3 | — | — | 33.9 / 28.1 |
| `move_strike_p3` | 92 / 100 | idle_p3 | 16-41 | 66:0 72:360 | 24.0 |
| `aftermath` | 224 / 240 | idle_p3 | — | 18:0 36:360 | 10.5 |
| `shells` | 113 / 140 | idle_p3 | — | — | 12.0 |
| `sink_p3` / `surface_p3` | 20 / 40 | hold / stand_p3 | 12-19 / — | — | 27.8 / 10.7 |
| `tail_p3` | 87 / 100 | idle_p3 | — | 13:0 21:200 45:200 53:0 | 20.6 |
| `spikes` | 72 / 84 | idle_p3 | — | — | 15.5 |
| `death` | 120 | hold | 118-119 | — | 9.7 |

Per clip the manifest carries events, anchors (impact / muzzle / ball / face / core / crown / hood_top points per
event), tracks, px keys (fitted, with the mandatory ticks), yaw knots, hidden spans, stance / look / hand / state events
and extents (every clip inside the 30 × 16 culling box; the tallest is `aftermath`, top 15.2 b). The AP-RC2 decisions
and the open items are in §7c.

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
P1 ≤ 7000 / P3 ≤ 8000 (R14). AP-R3 state: 0.876 M px in 239 sprites (body 300 k, head 193 k, hands 159 k, limbs 118 k,
tail 78 k, shared 28 k); elements at rest P1 5664 / P3 4743 (body 1582 / 1484, head 892 / 1061, limbs 2060 / 1296,
hands 724 / 548, tail 406 / 354); 101 models, 325 items. Suite: `S:ap/rigtests/test_ap_rig.py [--rebuild]` (static checks, mcsim runtime of spawn /
tick / looks / park / kill, determinism).

Clip compiler tolerances (`TOL`, AP-RC2; translation 0.012 b, scale 0.015): per part a translation-at-pivot class
`tp` and a surface error that sets the rotation tolerance from the part's reach (`atan(e / reach)`, 0.35-4°, reach =
the farthest model corner over both forms and every hand variant): hood, face and hands 0.012 b / 0.04 b (R16); the
body core (abdomen, chest, shoulders, neck, head, core, crown) and the A / B / C arm and leg bones 0.03 / 0.07; the tail
root `tail_1-2` 0.03 / 0.08; the soft, small or far parts (`tail_3+`, hair, mantle, hem, beads, crystals) 0.08 / 0.14.
Keys per tick: mean 14.9 over the 36 clips (31 129 part keys; RC1 19.9, 43 946), `keys_per_tick` in the manifest.

## 7. Deviations and decisions (R1)

- Hair parents to the **hood**, not the head: the hood swing carries the hair roots from the cowl sides (crouch) to
  beside the face (upright) inside the residual limit.
- The face look `hidden` uses the empty model (the effect of scale 0 kept through clip keys).
- Display scales raised for bounds: head 1.3, hem_b 1.7, core 1.3, crown 1.4.
- The v5 f1104 "umbrella" is the B arms seen from below (up-turned gold-coned tips, dark back, lime rim; v5 f1908), not
  the mantle; the mantle keeps scales 1.7 / 1.5.
- The death stub falls into the crawl (55-82) before its sink so that R9 holds; its stance score stays UPRIGHT.
- The rigid-skeleton fit moved a few CROUCH bind joints from the measured crouch table (hair roots and `hem_a`
  ≤ 0.38 b, the pose-only `clav_a` 0.68 b, the tail joints re-spaced); `skeleton.joints` lists the values used.
- Notes for other stages: `S:ap/requests/rig.md`; the AP-R2 work list: `S:ap/rigwork/r1_worklist.md`.

## 7b. AP-R3 integration (decisions and open items)

- **Atlas.** The merged regions painted 1.017 M px. Cut to 0.876 M with the R13 densities: unused sprites dropped
  (`g_shell`, `p1_leg`, `p3_robe`, `p1_cone`, `p3_cone`, `p1_core`; the empty model's particle is `g_plate`), the limb
  wraps to 32 px/b (`l1_arm` 192², `l3_arm` 128 × 240, `l1_leg` 128 × 192), the body sac / calyx / hook / plate cards
  and the P1 claws / petals, P3 fork / curl rosettes / C tips to 40 or 32 px/b, the P3 mask to 64 px/b.
- **Seams fixed.** P3 chin-to-chest strand in front of the B arm; P1 drapes in front of the front legs; a shared 1.0 b
  A wrist (forearm paddle tapered, claw palm / cuff widened); P1 foot cones out of the leg root base; coplanar hull
  ledges between abdomen / chest (P1) and chest / shoulders (P3). Cross-region z-fighting scan: 0 coplanar pairs in
  the rest, crawl and rear-up poses.
- **Plant height.** The R2 claw stands on its tips 0.59 b under the wrist; `tg()` lifts A plants to ≥ 0.4 b (RC1
  planted them at 0.35 for the R1 claw).
- **Open (geometry / joints):** the P1 A upper arm still crosses the pauldron from the side (a joint matter: the A root
  and elbow are frozen); the P3 tail sheath shows as a pale dome where tail_1 leaves the robe back; the P3 crawl strands
  rest on / cut into the B curl hands (fixed in AP-RC2: the CRAWL hair pose, §3); the P1 cowl underside reads as stacked ledges in the
  rear-up.
- **Open (clips, AP-RC2):** floor dips with the real geometry (outputs of `S:ap/rigwork/r3/tools/ck.mjs` and
  `tailfloor.mjs` in `S:ap/rigwork/r3/ck_r3.txt`, `tailfloor_r3.txt`): the P1 drapes in `rotation` t80-83 (−1.4 b),
  the P3 tail root sheath in the low upright poses (`revival` t72, `spikes` t8, `death` t55, `tail_p3` t40, `shells`
  t47, `aftermath` t186: −0.2 … −0.8 b, under the robe), `move_strike_p3` t62-65 (the slam window, by design), the
  P3 hem in `aftermath` t12 / `tail_p3` t42 / `death` t82, the P1 chest and leg roots 0.2-0.3 b under in the plunges,
  slams and `crawl_p1`; keys/t mean 19.9 (> 15); R17 secondary motion; the A plants. All taken up by AP-RC2 (§7c).

## 7c. AP-RC2 clip polish (decisions and open items)

- **A plants.** The P1 A targets are keyed through `tg()` at `A_PLANT` = 0.6 b (the R2 claw's tips 0.59 b under the
  wrist); RC1's `A_PLANT_MIN` lift is gone.
- **Model floor.** `PROBE` / `PROBE_YM` hold per part and form the bind-space model extremes of the hem, hair, body
  hull, tail root and leg roots (re-derive with `S:ap/rigwork/rc2/tools/probes.mjs` after a geometry change). The floor
  pass checks every visible tick: the body lifts (`BODY_LIFT` ≤ 0.45 b) over a hull or tail-root sheath below −0.12 b,
  the hem / hair chains turn (released towards the clip pose with hysteresis, so they do not pop), an IK leg wrist
  rises (≤ 0.12 b) over a dipping root flare; the per-tick corrections are smoothed into an envelope of ≤ 14° /
  0.06 b per tick and keyed only where they are nonzero. The cloth may touch the water: the P1 drapes down to −0.5 b
  and the P3 strands to −0.3 b (a drape held out flat over the water read worse in the strips), the hem to −0.08 b.
- **`move_strike_p3` slam window.** No ring opening of 4 ticks stays above the water within 120°/tick (a plain uncurl
  dips 5.8 b); the ring opens sideways under the belly-flop splash, t62-64 skipped by the floor pass (−2.3 b at t63).
- **Secondary motion (R17).** `SECONDARY`: world-space damped springs (stiffness 0.18-0.32, damping 0.82, centrifugal
  fling 0.9 from the anchor yaw) on the mantle flaps, hair, hem (pitch only, a rolled hem dipped) and P3 bead vines,
  capped 12-24°, keyed only where the offset exceeds 2°, faded over the last 8 ticks (clip joins unchanged); loops run
  three cycles to settle.
- **Eased segments.** `easeKnots` turns every eased key span of 4+ ticks into 2-4 linear pieces through its eased
  values (the compiler's linear segments then fit them with a third of the keys); it runs after the P1 hand lift-off /
  touch-down keys so a lifted hand never interpolates through the water.
- **Read fixes from the strips** (`S:ap/rigwork/rc2/strip_*.jpg`, vs `rc1`): `glow_slams` holds the second rear-up
  52-65 (≥ 10 t before slam 2, plan §14); `rotation` lands the crash pose on its event tick 40; `combo_d` keeps the far
  slam's tail root off the water; CURL / KNEEL / CRASH / SPRAWL re-seated over the R3 hull; the crawl hair (§3).
- **Open.** 15 clips stay above 15 keys/t, mostly short fast blends (`crouch_p3` 33.9, `stand_p3` 28.1, `sink_p3` 27.8,
  `burrow_in_p1` 24.5, `move_strike_p3` 24.0); the far / soft tolerance class (0.08 b) is looser than R16's 0.03 b on
  the tail, hair, mantle and hem; `tail_p3` hem_a −0.22 b at t15 and the P3 strands −0.21 … −0.31 b in `tail_p3` t6
  and `death` t96-99 remain (cloth on the water, `S:ap/rigwork/rc2/tools/ck.mjs`);
  the `PROBE` tables are R3 geometry (re-derive after AP-R3b); the geometry items of §7b (A upper arm vs pauldron, P3
  tail sheath dome, P1 cowl ledges) are for the geometry stages.


## 7c. AP-R3b critique fixes (region files only)

Critique and results: `S:ap/rigwork/r3_critique.md`; U2 sheet `S:ap/rigwork/r3b/U2_sheet.jpg`, before / after
`S:ap/rigwork/r3b/P1_before_after.jpg`.
- **Crawl beak (head).** The P3 crown keeps only its back layer of six leaves (the front layer hid behind the visor
  upright and stuck out as gold fangs under the carapace in the crawl); the hood gets a beak keel under the carapace
  front (z -1.2 to the tip), closing the crawl front. Upright the keel is behind the visor's top band, above the mask.
- **P1 A arms (limbs).** The shell sections are broad toward the front (wide along X) from mid upper arm to the wrist
  turn (`ARM_TURN` in `apep_limbs.mjs`), so the player's camera sees broad grey-green blades (v2 f2076); the wrist keeps
  the shared 1.0 b front-back width at the claw.
- **Body.** The P1 core sac is a 12-segment round bulb; the shoulder hook gem a stepped cut stone.
- **Hands / limbs.** The planted P1 petal feet are larger (petals 1.2 k long, ~22 % broader); the lower legs' root base
  flares less (0.6 b).
- Budgets: elements at rest P1 6002 / P3 4720 (body 1778 / 1484, head 892 / 1038, limbs 2150 / 1296, hands 776 / 548,
  tail 406 / 354); atlas 0.867 M px in 230 sprites. Open model items: `r3_critique.md` (H2 hood back, T1 tail sheath,
  H3 bud-skull, L2 leg cuffs, T2 / T3 tail straps).
