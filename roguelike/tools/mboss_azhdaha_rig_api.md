# 야타용왕 (Azhdaha · 봉인된 바위 용의 왕) rig: API contract (stage R3)

This is the contract between the Azhdaha display-entity rig and the chapter-1 boss module (not written yet). Stage R1
delivered the model, the skeleton, the element looks, the body states and the hit-proxy points; R2 refined the four
regions in parallel; R3 integrated them (seams, the RIGLIB shared libraries, the fixed UUID table, per-region budgets,
the root-offset rule, `look/petrify` and `glow/gold_*`; §11). The motion clips of `motion.md` §6 come in R3a (the clips
listed in §6 are static debug poses). Binding decisions: scratchpad `az/plan.md` "Rig decisions" R1-R11, Rig decision
changes 1-3, §3 and the change notes; `az/contract/manifest.md`; references `az/understand/model.md`, `motion.md`,
`rigtech.md`.

Generator: `tools/build_mboss_azhdaha_rig.mjs`, split by region so that four authors can refine head, body, legs and
tail in parallel (plan.md R9):

| file | owns |
|---|---|
| `build_mboss_azhdaha_rig.mjs` | parts list check, the fixed UUID name table, per-region and total budgets, RP write (models, item definitions, tinted overlays, the sprites some model uses), clip compile, pose checks, API functions, hit-proxy points, manifest |
| `azhdaha_pose.mjs` | the skeleton `J` (rest joints, H = 7.0 b), `PART_SCALE`, `solve()` (FK of the spine / neck / head / jaw / beard / apron, plate-group flare, two-bone foot IK of the four legs, the tail chain), `toDisplay()`, `PROXIES` / `proxyPoints()` |
| `azhdaha_clips.mjs` | `DEFAULT_POSE` (the idle stance), the debug poses (`CLIPS`), `RETIME` (empty), pose helpers `tailUp`, `fore`, `hind` |
| `azhdaha_geometry.mjs` | thin aggregator: `PARTS`, `partModels()`, `LOOKS`, `TINTED`, `LOOK_BRIGHT` over the four region modules |
| `azhdaha_paint.mjs` | thin aggregator: `azhdahaSprites(keep)`, `spriteRegions()`, `paintAzhdahaTextures()`, `spriteId()`, the 1.2 M px atlas budget |
| `azhdaha_head.mjs` | head (V-wedge mask plates, brow ledges and wings, keel blade, a two-rank crown of gold-rimmed blades and crest fins, cheek guards, the ear plates 回 on their mounts, rounded skull, palate, upper teeth), jaw (V chin shield over a V-wedge lower jaw: cheek plates, underside, mouth floor, teeth, fangs, tongue), eyes (slits), horns (broad gold sleeve band bent into a C, rim wrapped round its rounded lower end, meander face, dome stud knob, carded dark horn), beard bibs |
| `azhdaha_body.mjs` | chest / belly / pelvis, neck, apron (+ glow overlay), the four dorsal plate groups, the three gold crystal groups |
| `azhdaha_legs.mjs` | upper arms, engraved octagonal bracers (ragged crown, painted gold studs, amber elbow crystals), paws (knuckles, 4 talons, dew claw), haunches, shins (`gaiter_*`), the ribbed gaiter columns on `foot_*` (collar, heel spur, rings, plinth, 3 + 1 talons), the four leg glow overlays |
| `azhdaha_tail.mjs` | t1..t8 (a broad lens-section body: cream ventral face with the gold midrib and chevrons, dark scale-plated flanks, the ridge blades, the V-fan side rows and the flank plates; collared, capped joints), the gnarled leafy branch t6..t8 and the tip (thorns, twigs, leaf sprays / blossoms), `tail_skirt` (the cream rump plate under the tail root, rigid with the pelvis), the tail's per-part culling boxes (`CULL_BOX`) |
| `azhdaha_shape.mjs` | R3: the 3-line re-export shim of the shared `mboss_shape_lib.mjs` (RIGLIB; loft, slab, crossCards, rockBox, retex, mirrorX, tile UV registry); the region modules keep their imports |
| `azhdaha_materials.mjs` | shared palette ramps (model.md §4) and the shared tile sprites (hide, cream, plate, gold, horn, mouth; the R1 tiles no model uses any more, `hide_lg hide_dk talon bark* dark`, stay defined but are not painted) |

Every region module exports the same interface: `REGION`, `PARTS` ([part, default item model, brightness]),
`models()` (model units, every look variant included), `sprites()`, `LOOKS` ({legs|tail: {part: {look: item}}}),
`TINTED` ({item: [model, rgb]}), `LOOK_BRIGHT` ({channel: {look: {part: level}}}). A region author edits only their
module (and, rarely, a skeleton joint in `azhdaha_pose.mjs`); the aggregators fail the build on duplicate model,
sprite or look names. `azhdaha_shape.mjs` / `azhdaha_materials.mjs` are co-owned: changing a material repaints every
region.

```
node tools/build_mboss_azhdaha_rig.mjs --resourcepack <unpacked RP> [--datapack <dp>] [--no-paint | --paint a,b]
                                       [--debug-dp <scratch dir> [--debug-clips a,b | all]] [--allow-steps]
```

- It owns and rewrites `data/rlk/function/mboss/azhdaha/rig/**`. Never hand-edit those files.
- In the RP it writes `assets/rlk/textures/mboss/azhdaha/*.png` (sprites, registered in
  `assets/minecraft/atlases/items.json`), `assets/rlk/models/item/mboss/azhdaha/*.json` and
  `assets/rlk/items/mboss/azhdaha/*.json` (one item definition per model plus the tinted overlay items). Stale files
  of the three folders and stale atlas entries are removed.
- The manifest is `tools/mboss_azhdaha_rig_manifest.json` (§7).
- `--debug-dp <scratch dir>` writes `az_dbg/<clip>/<t>` (exact per-tick poses), `az_dbg/rest`,
  `az_dbg/look_<legs>_<tail>` (look combinations), `az_dbg/player_ref` (1.8 b player references) and its overlay pack
  `<scratch dir>/rp_ref` for the offline renderer (`az/understand/rigtech_render.py --rp <scratch>/rp_ref --rp <rp>`).
  It never writes into the real packs.
- The shared libraries (`mboss_model_lib`, `mboss_paint_lib`, `mboss_rig_math`, `mboss_rig_clips`,
  `mboss_rig_compile`, `mboss_shape_lib`) are used unchanged (RIGLIB, `tools/mboss_shape_lib.md`): the parts and the
  shadow are summoned with `summonPart` / `summonShadow`, the follow file comes from `createRigFollow`, the culling
  check is `cullOverhang`. Requests for library changes go to a RIGLIB stage.

All functions below are `rlk:mboss/azhdaha/rig/...`. Unless a line says otherwise, **@s is the rig anchor** (the boss
body, on the floor under the centre of the four feet). Call them `as` the anchor and `at` it.

## 1. Calls

| function | when | what |
|---|---|---|
| `init` | load (idempotent) | Adds the objectives (§7). |
| `spawn` | boss spawn, respawn | Kills old parts, summons the 47 parts in the rest pose plus the shadow helper, re-applies the stored looks and body state, and queues `rest`, or the looping clip that holds the stored state (burrowed: `burrowed`, tail-only: `tail_only`; manifest `states.respawn_clip`), so a respawn never shows a hidden body (R3). |
| `tick` | every tick | Respawns missing parts, follows the anchor (position + yaw), advances the clip, runs the hit flash. |
| `play/<clip>` | any time | Plays a clip from tick 0 at the next `tick`. |
| `start/<clip>` | internal | Chains into a clip now. |
| `face/player`, `face/track`, `face/set {yaw}` | AI | Anchor yaw (track: at most 2 degrees per call: a slow, heavy turn). |
| `look/legs/<geo\|hydro\|pyro>` | phase 2 absorb | Legs channel: bracers, paws, the gaiter columns (`foot_*`), apron, belly cracks, glow overlays. Stored in `azRigLegs`. |
| `look/tail/<geo\|cryo\|electro>` | phase 3 absorb | Tail channel: the four dorsal plate groups and the tail chain (leaves to blossoms). Stored in `azRigTail`. |
| `look_apply` | after respawn | Re-applies both stored looks. |
| `look/petrify` | death (t96) | Death seal: both channels back to geo (stored), every part 3 levels darker (block and sky), a 12-tick gold rim pulse on the horns and crystals (`azRigF`). A respawn shows the base looks at full brightness: call it again. |
| `glow/gold_on`, `glow/gold_off` | the 천동만상 tell, the absorbs | The gold parts (horns, the three crystal groups) from matte 13 to 15 and back. Not stored (re-call after a respawn). |
| `state/normal`, `state/burrowed`, `state/tail_only` | burrow, phase 3 | Records the body state (`azRigState`) and hides what must not show (§3). |
| `flash/<head\|front\|rear\|tail>` | `on_hit` | 3-tick warm outline on one part group only (never all 46 parts, rigtech.md §2.6). |
| `kill`, `uninstall` | cleanup | Remove the parts / the parts and the objectives. |

## 2. Entities, tags, cost

- 47 `item_display` parts (plan.md R3: 44-48, cap 56), fixed UUIDs `524c4b4d-415a-4400-8000-0000000000NN` from the
  builder's append-only name table `UUID_INDEX` (Rig decision change 3, cm.md §14; manifest `uuids.parts`): R1's order
  head 0x01 ... tip 0x2E, then `tail_skirt` 0x2F (added in R2). A new part takes the next free index; nothing is ever
  renumbered. The shadow helper is `...00000040` (an empty model with `shadow_radius 4.5`, not a rig part). The hit
  proxies (framework) take 0x41 + their position in `proxies.layout` (§7), module props 0x60-0x8F.
- Part names are lower-case and never start with `p<digit>`, `x`, `ap_`, `fld`, `lock`, `kept`, `pat`, `orbc`,
  `seal` or `g_`, nor are they `shadow` / `face` (the module's and the rig's `rlk_mb_az_*` tags; the build asserts it).
- Tags: `rlk_room`, `rlk_mb_aux`, `rlk_mb_part`, `rlk_mb_azhdaha_part`, `rlk_mb_az_<part>`, `rlk_mb_az_g_<region>`.
- Summon: `billboard:"fixed"`, `item_display:"none"`, `interpolation_duration:1`, `teleport_duration:1`,
  `view_range:3f`, **`width:30f,height:12f`** (plan.md R4: the culling box is centred on the anchor; the tail reaches
  15 b behind it; the distal tail `t4..t8 tip` uses `width:44f,height:18f` so it never vanishes when laid out, swept
  or raised: the tail region's `CULL_BOX`, manifest `culling.per_part`), `shadow_radius:0f`, brightness 13 (hide and
  the matte gold horns and crystals, plan.md §3.5), 14 (the leafy branch t6..t8, tip), 15 (eyes, overlays).
- Parts by region: head 7 (`head jaw eyes horn_l horn_r beard1 beard2`), body 14 (`chest belly pelvis neck1 neck2
  apron glow_apron plates_neck plates_sh plates_mid plates_hip crys_sh crys_mid crys_hip`), legs 16 (`uarm_* bracer_*
  paw_* thigh_* gaiter_* foot_*` x2 and `glow_bracer_* glow_gaiter_*`), tail 10 (`t1..t8 tip tail_skirt`; the skirt rides
  the pelvis at the tail root, hidden with the body, and flashes with the `rear` group).
- Per tick: 47 `tp` (follow) + dispatch + the keys of the current clip. Elements shown at once: 4 335 at rest in Geo,
  at most 4 465 (Hydro legs + Geo tail) over the 9 look combinations; the build fails above 8 000 (rigtech.md §2.2:
  6-8 k visible is the client budget).

## 3. Body states (plan.md R7, rigtech.md §4)

| state | id | clip pose | mask |
|---|---|---|---|
| normal | 0 | any | none |
| burrowed | 1 | root sunk (`pos` y -7.5, see `burrowed`) | every part at scale 0 (`visBody 0`, `visTail 0`) |
| tail-only | 2 | the root pitched nose-down 90 and sunk (`pos` y -11.15, `rot` -90: `TAIL_PILLAR_ROOT`), so the tail rises at the anchor's x / z (t1 and most of t2 under the floor, the crown at ~11 b) (`tail_only`) | every non-tail part at scale 0 (`visBody 0`) |

The anchor (husk body) never goes into blocks: the clips sink the **rig** below the opaque arena floor. The floor
under the burrow must be opaque full blocks (rigtech.md §4.1). The tail-only state keeps the tail look. A respawn
(missing parts at `tick`) restores the stored state with its clip (`spawn`): R3a keeps one looping clip per hidden state
(`state` burrowed / tail_only), or the build fails.

## 4. Element looks (plan.md R6, model.md §4.2)

Two independent channels; all four combinations (불/번개, 물/얼음, 불/얼음, 물/번개) render (`r1_looks.jpg`).

| channel | look | parts | how |
|---|---|---|---|
| legs (`azRigLegs`) | geo 0 / hydro 1 / pyro 2 | bracer_l/r, paw_l/r, foot_l/r, apron, belly | palette-swapped models (navy-black or deep red-brown stone, glowing carved lines; the belly cracks glow in Pyro). `gaiter_l/r` is the hide shin since R2 and keeps one model. |
| legs | hydro / pyro | glow_bracer_l/r, glow_gaiter_l/r, glow_apron | white line masks 0.025 b proud, `tintindex 0`, item definitions with constant tints (`#cde6ff` / `#ffb070`), brightness 15; the `empty` model in Geo. `glow_gaiter_*` follows `foot_*` (the ring column). |
| tail (`azRigTail`) | geo 0 / cryo 1 / electro 2 | plates_neck/sh/mid/hip, t1..t8, tip | palette-swapped models: slate / violet-dark plates with glowing edges; the tail skin, blades and bark go to the deep end of the element's stone ramp with thin glowing cracks and blade rims (the cream ventral face and the skirt keep their gold veins), the leaves become crystal sprays / violet blossoms; t6..t8 and tip (the blossoms) at brightness 15, t1..t5 stay 13 |

The eyes stay red at 15 and the gold (horns, crystals, studs) stays matte gold at 13 in every look; `glow/gold_on`
lifts the horns and crystals to 15 (the studs are painted on the bracers and do not change). No look channel touches
the gold parts or the eyes (the build asserts it). `look/petrify` is the death seal (§1). The model and item names per
part and look are in the manifest (`looks`; `looks.gold`, `looks.eyes`, `looks.functions` for petrify / glow).

## 5. Skeleton and pose channels

Rig frame: +X = the boss's left, +Y up, -Z forward, blocks; origin = the floor under the centre of the four feet.
Joints (rest, `azhdaha_pose.mjs J`): pelvis (hip line) 0,3.0,2.4; spine1 0,3.35,0.3; chest 0,3.35,-1.7; neck1
0,3.05,-2.55; neck2 0,2.6,-3.05; head (atlas) 0,2.05,-3.7; jaw hinge 0,1.3,-4.0; left shoulder 2.25,3.6,-2.05,
elbow 2.95,2.35,-2.2, wrist 3.15,0.5,-2.4; left hip 2.0,3.0,2.45, knee 2.3,2.3,1.85, hock 2.5,1.5,2.9; tail root
0,2.85,4.75; tail segments 2.3, 2.1, 1.9, 1.8, 1.7, 1.6, 1.6, 1.5 (14.5 b). Rest silhouette: H 7.0 b (tallest plate),
nose to rump 10.2 b, wheelbase 5.0 b, claw span 8.1 b, horn span 4.4 b, snout 0.85 b, crest 2.65 b, eyes 1.5 b.
Head (R2, measured on the real quads): eyes 1.5 b at z -4.74, chin 0.25 b above the floor, horn span 4.5 b, dark horn
tips 4.9 b (3.4 b above the eyes), nose to rump 10.7 b. The neck (neck1 -> neck2 -> atlas) is 1.5 b, so a chin slam
reaches the floor at z -5.8 with the eyes at 1.4 b (root -0.25 b and tilted 10 degrees nose-down, neck1 +30, neck2
+10, head 0); at that impact the jaw's underside dips 0.23 b into the floor and the beards 0.2 b when they sweep back
(beard1 -35, beard2 -20; hanging straight they reach 0.33 b), inside the 0.3 b impact allowance. A roar_rear at
pelvis +55, head +30 puts the eyes at 8.7 b (the debug rear_up, pelvis +45 and head +22, reaches 7.7 b).

Pose channels (`DEFAULT_POSE`): `pos [0,y,0]`, `rot [p,y,r]` (about ROOT_PIVOT 0,2.8,0.4), `pelvis spine chest
neck1 neck2 head` eulers, `jaw` (deg open: the chin swings down about the hinge; at the head-low rest the chin
clears the floor up to jaw 10, wider needs the head pitched up by about (jaw - 10) / 2 degrees, e.g. jaw 50 with head
+21), `beard1 beard2 apron` eulers, `flN flS flM flH` plate flare (deg, +
stands the plates up), `flK` plate scale, `fwL fwR` wrist targets and `fpL fpR` paw eulers, `hkL hkR` hock targets and
`hfL hfR` foot eulers (root frame: planted feet stay put while the body rears), `t1..t8` tail eulers (pitch - raises a
segment) plus `tLift tCurl tSweep tTwist` (`tSweep` is spread root-weighted by `TAIL_SWEEP` .30 .20 .15 .11 .08 .07
.05 .04: the root leads, the distal tail stays nearly straight), `vis visBody visTail`. The tail curl constants live in
`azhdaha_clips.mjs`: `TAIL_REST` (idle arc), `TAIL_LOOP`, `TAIL_LOW`, `TAIL_WHIP`, `TAIL_PILLAR` (+ `TAIL_PILLAR_ROOT`);
authored bends stay at 30 degrees per joint or less. Clips carry no horizontal root travel and no root
yaw (the module moves and turns the anchor). The legs are solved by two-bone IK at bake time with the rest bend as
the pole (`ik()` with `prevV` continuity across frames). Leg parts (R2): `uarm_*` / `thigh_*` turn with their bone
relative to its rest direction (rest-aligned masses); `bracer_*` (elbow -> wrist) and `gaiter_*` (the shin, knee ->
hock) are bone-aligned columns; `paw_*` / `foot_*` sit at the wrist / hock with their eulers. The hock is 1.5 b up:
`foot_*` is the near-vertical ribbed gaiter column (the metatarsus) plus the toes, so a planted hind foot keeps
`hfL/hfR` near [0,0,0] and a lifted one hangs the column from the hock. Soles: `SOLE` = paw -0.5, foot -1.5 (part frame).

## 6. Clips (R1: static debug poses)

| clip | state | what |
|---|---|---|
| `rest` | normal | DEFAULT_POSE: idle stance, head low, the tail in a big arc over the back, the leafy tip over the mid-back at ~10 b (v3 23.6 s) |
| `head_up` | normal | the neck raised, the face forward (v1 f2130) |
| `roar` | normal | jaw 45, head thrust up |
| `rear_up` | normal | roar_rear peak: pelvis +45, fore paws at chest height, tail braced on the floor |
| `stomp_lift` | normal | stomp_fl hang: the front rises and rolls away, the left elbow high, the bracer a hanging column, wrist 2.4 b |
| `whip_mid` | normal | the tail just off the floor, swept 110 to the left (root-weighted); the throat apron swings forward 12 (R3: its hem hangs 0.06 b above the floor at rest, the 0.2 b crouch would sink it) |
| `loop` | normal | the phase-3 tail loop / shells carry (v8 f2280: top ~11.7 b, the tip over the shoulders) |
| `tail_low` | normal | the tail laid out behind (v3 f1680) |
| `burrow` | normal | burrow dive mid-sink: root -3.4, nose down 22 |
| `burrowed` | burrowed | root -7.5, every part hidden |
| `tail_only` | tail_only | the phase-3 pillar at the anchor: body hidden, the tail rising from the floor in a slight S to ~12 b, the crown nodding forward |

Each is a 2-tick loop (46 keys at tick 0). The motion clips of motion.md §6 replace this list in a later stage.

## 7. Manifest and objectives

`tools/mboss_azhdaha_rig_manifest.json` (still the R1 layout; the schema v1 migration of `az/contract/manifest.md` §10
is R3a): `parts` (name, region, uuid, `idx` = the UUID low byte, tag, model, brightness, scale, elements), `shadow`,
`uuids` (block, ints, the part table, shadow, proxies, props), `clips` (id, len, loop, next, events, keys, state,
world `extents`, `root_z` spans `[t0, t1, dz]` (local, + forward; empty in every debug pose), `cull_overhang` when a
pose leaves its culling box, `px` = hit-proxy points at tick 0, the events and the last tick), `looks` (per channel:
objective, ids, item per part and look, brightness, functions; `gold`, `eyes`, `functions` petrify / glow_on /
glow_off), `tinted_items`, `states`, `flash_groups`, `proxies` (`layout`: name, bone, point, column width, top margin,
tail-only flag; `rest`: the rest points), `skeleton`, `culling`, `rest_extents`, `budgets` (parts, models, elements
all / shown at rest / shown max and per look, atlas px, sprites, `regions` {parts, px, budgets, elements at rest}),
`objectives`. The extents (and the culling overhang) come from the corners of each part's rotated model box, so they
are conservative: at rest they read y -0.25 while the lowest real vertex (the gaiter plinth) sits at -0.03.

Objectives: `azRigC` clip id, `azRigT` clip tick, `azRigF` flash countdown, `azRigY` face scratch, `azRigLegs`,
`azRigTail`, `azRigState`.

Hit proxies (plan.md R5, rigtech.md §3.3): 13 ground-anchored columns, in UUID order — `head chest belly hips
tail1..tail4 paw_l paw_r foot_l foot_r tail5` (0x41 ... 0x4D; the 12 names of the D0 layout keep cm.md §14's bytes,
`tail5` is appended in the reserved 0x4D-0x50) — each `{x, z}` (the bone point projected on the floor, rig frame: +x
= the boss left, -z = its front), `base`, `top`, `w`; `hidden: true` when the bone is at scale 0 or the column's top
is under the floor. The tail columns sit on t2, t4, t6, t8 and the tip (the leafy crown, the phase-3 target) and are
flagged for the tail-only state. R3 check (`rigwork/r3/tools/proxycheck.mjs`): every point lies inside its part, and
in every debug pose 100 % of the footprint outline is within 3.0 b of a live column edge (worst 1.9 b, rear_up).
The framework side (interaction entities, `combat/apply` routing, dedupe) is a later stage.

## 8. Build checks and budgets

- Parts 44-48 (warn), cap 56 (fail); every part has a display scale, a region and a `UUID_INDEX` entry (unique,
  0x01-0x3F); part names outside the tag space above; at most 16 hit proxies.
- Per-region budgets (plan.md §3.1, atlas px rebalanced by change note 1), fail when exceeded:

  | region | parts | sprite px | R3 use |
  |---|---|---|---|
  | head | 8 | 0.24 M | 7 parts, 0.187 M |
  | body | 14 | 0.42 M | 14 parts, 0.397 M |
  | legs | 16 | 0.32 M | 16 parts, 0.314 M |
  | tail | 10 | 0.16 M | 10 parts, 0.146 M |
  | shared material tiles | - | 0.06 M | 0.053 M |
  | total | 48 (cap 56) | 1.2 M | 47 parts, 1.097 M px, 154 sprites |

- Elements shown at once <= 8 000 in every look combination (R3: 4 465 max).
- `checkBounds` on every model (all coordinates within -16..32: reach 1.5 x scale from the joint).
- Every pose of every clip: no root x travel and no root yaw; a root z offset only on ticks where no body (non-tail)
  part is shown (Rig decision change 1, recorded as `root_z`); the soles of the paws and feet at or above the floor
  unless the root is sunk; the tail-only state shows no non-tail part; events inside 0..len; the culling-box overhang
  (radial `cullOverhang`: the box does not turn with the yaw; buried points do not count) is recorded (warning) per
  clip. Rotation step checks of the shared compiler (120 degrees per tick / key).
- Gold parts at 13 and in no look channel; the eyes at 15 in every look; a looping clip per hidden body state (the
  respawn clip).
- Runtime suite (scratchpad `az/tests_rig/test_az_rig.py`, mcsim over the generated functions): the UUID table and
  budgets of the manifest, spawn / respawn of the 47 parts + shadow, the follow, every clip to its end with its tick-0
  pose equal to the exact debug pose, the clip states, the 9 look combinations and their respawn, the body states and
  their respawn, the flash groups, `glow/gold_*`, `look/petrify`, the root-offset rule, uninstall (R3: 157 checks).
- Sprites: sides multiples of 16 and <= 512; only the sprites some model uses are painted and registered.
- Every look item exists; every tinted item points at a model.

## 9. Not in the rig

The element sigils, brands, floor glyphs, rocks, meteors, water orbs, ice spikes, lightning, the absorb vortex, the
burrow crater and rubble, the dust (fx kit); the seal steles (arena props); the interaction hit proxies and the body
solidity push (framework); the motion clips (later stage).

## 10. Body region notes (R2)

- Torso: chest / belly / pelvis are one hull (`azhdaha_body.mjs BODY`, U/egg sections lofted along z) split by
  ownership (chest z <= -1.0, belly -1.0..1.6, pelvis >= 1.6); each part carries tucked overlap past its range so the
  joints stay closed when the spine bends. The hide is a light-corrected wrap sprite per part (`tw_chest`, `tw_belly`,
  `tw_pelvis`, `tw_neck1`, `tw_neck2`), the ventral facets are the cream plastron rolls (`tz_pl*`).
- Legs channel looks: the torso swaps `chest`, `belly` and `pelvis` (`*_hydro`, `*_pyro`: plastron cracks glow in
  Pyro, at brightness 14; Hydro lifts only the belly to 13). The apron keeps its single stone model in every look and
  only its `glow_apron` overlay changes (the R1 `apron_hydro` / `apron_pyro` models are gone).
- Neck part frames: `neck1` / `neck2` carry their bone's rest slope (`azhdaha_pose.mjs NECK_TILT`, a fixed nose-down
  pitch on top of the bone rotation), so their models are lofted along the neck axis. Anything placed in those part
  frames must use the tilted frame.
- Plate groups: the bristle widens a group across X with its flare (`PLATE_SPLAY`), so the side rows roll outward.
- Gold crystals: slender blades as crossed card pairs along each blade's axis (sprite `shards`, 4 cells of 48 x 128),
  1-3 per cluster, within the R1 crystal part reach.

## 11. R3 integration notes

- Merged on `wip/az-rig`: the four R2 regions (`wip/az-rig-head` b2f62d1, `-body` 28a4398, `-legs` 2edd195, `-tail`
  4110e3c; every shared hunk kept, the generated files rebuilt, never hand-merged) and the release line 039b911 (M0 +
  RIGLIB). `azhdaha_shape.mjs` is the shim of `tools/mboss_shape_lib.md` §1; the Guardian, butterfly and field
  generator rig outputs are byte-identical to M0 (scratchpad `az/rigwork/r3/ident/prove.sh`).
- Seams (every debug pose plus 13 private stress poses from motion.md): the upper arm and haunch tops run into the
  flank, the rump skirt mass is sealed to the pelvis; neck / head and neck / body show no gap; no coplanar quads across
  regions in any debug pose; no part below the floor in any debug pose (element-precise check,
  `rigwork/r3/tools/floorcheck.mjs`); no culling overhang.
- For R3a (clip authoring), from the stress probes: the head-low rest leaves little room under the face, so the chin
  slam (jaw / beards / apron 0.2 b and the paws 0.7 b into the floor at root -0.25 tilted 10 nose-down), the brace
  crouch (head pitched -20 at root -0.35: the jaw 1.1 b down), the charge coil and the stomp_hl lift (pelvis -3: the
  apron and the jaw 0.2 b down) need the head / neck lifted or the wrist targets raised; roar_rear at pelvis +55 needs
  the tail chain raised (t2..t8 0.5-1.4 b into the floor with the rear_up tail curl). The hit-proxy layout has 13
  entries (tail5 at 0x4D) while `az/contract/manifest.md` §6.1 / §6.2 still list 12: the v1 migration adds `tail5`
  (layout, `states.normal` and `states.tail_only`) with S1-MOD.
