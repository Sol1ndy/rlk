# 야타용왕 (Azhdaha · 봉인된 바위 용의 왕) rig: API contract (stage R1)

This is the contract between the Azhdaha display-entity rig and the chapter-1 boss module (not written yet). Stage R1
delivers the model, the skeleton, the element looks, the body states and the hit-proxy points; the motion clips of
`motion.md` §6 come in a later stage (the clips listed in §6 are static debug poses). Binding decisions: scratchpad
`az/plan.md` "Rig decisions" R1-R11; references `az/understand/model.md`, `motion.md`, `rigtech.md`.

Generator: `tools/build_mboss_azhdaha_rig.mjs`, split by region so that four authors can refine head, body, legs and
tail in parallel (plan.md R9):

| file | owns |
|---|---|
| `build_mboss_azhdaha_rig.mjs` | parts list check, UUIDs, RP write (models, item definitions, tinted overlays, atlas budget), clip compile, pose checks, API functions, hit-proxy points, manifest |
| `azhdaha_pose.mjs` | the skeleton `J` (rest joints, H = 7.0 b), `PART_SCALE`, `solve()` (FK of the spine / neck / head / jaw / beard / apron, plate-group flare, two-bone foot IK of the four legs, the tail chain), `toDisplay()`, `PROXIES` / `proxyPoints()` |
| `azhdaha_clips.mjs` | `DEFAULT_POSE` (the idle stance), the debug poses (`CLIPS`), `RETIME` (empty), pose helpers `tailUp`, `fore`, `hind` |
| `azhdaha_geometry.mjs` | thin aggregator: `PARTS`, `partModels()`, `LOOKS`, `TINTED`, `LOOK_BRIGHT` over the four region modules |
| `azhdaha_paint.mjs` | thin aggregator: `azhdahaSprites()`, `paintAzhdahaTextures()`, `spriteId()`, the 1.2 M px atlas budget |
| `azhdaha_head.mjs` | head (face mask plates, keel, crown spikes, ear plates 回, upper teeth), jaw (chin shield, lower teeth, fangs, tongue), eyes, horns (gold sleeve C + knob + dark horn), beard plates |
| `azhdaha_body.mjs` | chest / belly / pelvis, neck, apron (+ glow overlay), the four dorsal plate groups, the three gold crystal groups |
| `azhdaha_legs.mjs` | upper arms, engraved bracers (gold studs, amber elbow crystals), paws and talons, haunches, ribbed gaiters (heel spurs), feet, the four leg glow overlays |
| `azhdaha_tail.mjs` | t1..t8 (a broad lens-section body: cream ventral face with the gold midrib and chevrons, dark scale-plated flanks, the ridge blades, the V-fan side rows and the flank plates; collared, capped joints), the gnarled leafy branch t6..t8 and the tip (thorns, twigs, leaf sprays / blossoms), `tail_skirt` (the cream rump plate under the tail root, rigid with the pelvis), the tail's per-part culling boxes (`CULL_BOX`) |
| `azhdaha_shape.mjs` | shared shape helpers (loft, slab, crossCards, rockBox, retex, mirrorX, tile UV registry) |
| `azhdaha_materials.mjs` | shared palette ramps (model.md §4) and the shared tile sprites (hide, cream, plate, gold, horn, talon, bark, mask/mouth) |

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
  `mboss_rig_compile`) are used unchanged; the Azhdaha-only helpers live in `azhdaha_shape.mjs`.

All functions below are `rlk:mboss/azhdaha/rig/...`. Unless a line says otherwise, **@s is the rig anchor** (the boss
body, on the floor under the centre of the four feet). Call them `as` the anchor and `at` it.

## 1. Calls

| function | when | what |
|---|---|---|
| `init` | load (idempotent) | Adds the objectives (§7). |
| `spawn` | boss spawn, respawn | Kills old parts, summons the 46 parts in the rest pose plus the shadow helper, queues `rest`, re-applies the stored looks and body state. |
| `tick` | every tick | Respawns missing parts, follows the anchor (position + yaw), advances the clip, runs the hit flash. |
| `play/<clip>` | any time | Plays a clip from tick 0 at the next `tick`. |
| `start/<clip>` | internal | Chains into a clip now. |
| `face/player`, `face/track`, `face/set {yaw}` | AI | Anchor yaw (track: at most 2 degrees per call: a slow, heavy turn). |
| `look/legs/<geo\|hydro\|pyro>` | phase 2 absorb | Legs channel: bracers, paws, gaiters, feet, apron, belly cracks, glow overlays. Stored in `azRigLegs`. |
| `look/tail/<geo\|cryo\|electro>` | phase 3 absorb | Tail channel: the four dorsal plate groups and the tail chain (leaves to blossoms). Stored in `azRigTail`. |
| `look_apply` | after respawn | Re-applies both stored looks. |
| `state/normal`, `state/burrowed`, `state/tail_only` | burrow, phase 3 | Records the body state (`azRigState`) and hides what must not show (§3). |
| `flash/<head\|front\|rear\|tail>` | `on_hit` | 3-tick warm outline on one part group only (never all 46 parts, rigtech.md §2.6). |
| `kill`, `uninstall` | cleanup | Remove the parts / the parts and the objectives. |

## 2. Entities, tags, cost

- 47 `item_display` parts (plan.md R3: 44-48, cap 56), fixed UUIDs `524c4b4d-415a-4400-8000-0000000000NN`
  (NN = 1..47 in the order of `PARTS`: head, body, legs, tail). The shadow helper is `...00000040` (an empty model with
  `shadow_radius 4.5`, not a rig part).
- Tags: `rlk_room`, `rlk_mb_aux`, `rlk_mb_part`, `rlk_mb_azhdaha_part`, `rlk_mb_az_<part>`, `rlk_mb_az_g_<region>`.
- Summon: `billboard:"fixed"`, `item_display:"none"`, `interpolation_duration:1`, `teleport_duration:1`,
  `view_range:3f`, **`width:30f,height:12f`** (plan.md R4: the culling box is centred on the anchor; the tail reaches
  15 b behind it; the distal tail `t4..t8 tip` uses `width:44f,height:18f` so it never vanishes when laid out, swept
  or raised: the tail region's `CULL_BOX`, manifest `culling.per_part`), `shadow_radius:0f`, brightness 13 (hide), 14 (gold horns, crystals, tail tip), 15 (eyes, overlays).
- Parts by region: head 7 (`head jaw eyes horn_l horn_r beard1 beard2`), body 14 (`chest belly pelvis neck1 neck2
  apron glow_apron plates_neck plates_sh plates_mid plates_hip crys_sh crys_mid crys_hip`), legs 16 (`uarm_* bracer_*
  paw_* thigh_* gaiter_* foot_*` x2 and `glow_bracer_* glow_gaiter_*`), tail 10 (`t1..t8 tip tail_skirt`; the skirt rides
  the pelvis at the tail root, hidden with the body, and flashes with the `rear` group).
- Per tick: 47 `tp` (follow) + dispatch + the keys of the current clip. Elements shown at rest: about 5.6 k
  (rigtech.md §2.2: 6-8 k visible is the client budget).

## 3. Body states (plan.md R7, rigtech.md §4)

| state | id | clip pose | mask |
|---|---|---|---|
| normal | 0 | any | none |
| burrowed | 1 | root sunk (`pos` y -7.5, see `burrowed`) | every part at scale 0 (`visBody 0`, `visTail 0`) |
| tail-only | 2 | the root pitched nose-down 90 and sunk (`pos` y -11.15, `rot` -90: `TAIL_PILLAR_ROOT`), so the tail rises at the anchor's x / z (t1 and most of t2 under the floor, the crown at ~11 b) (`tail_only`) | every non-tail part at scale 0 (`visBody 0`) |

The anchor (husk body) never goes into blocks: the clips sink the **rig** below the opaque arena floor. The floor
under the burrow must be opaque full blocks (rigtech.md §4.1). The tail-only state keeps the tail look.

## 4. Element looks (plan.md R6, model.md §4.2)

Two independent channels; all four combinations (불/번개, 물/얼음, 불/얼음, 물/번개) render (`r1_looks.jpg`).

| channel | look | parts | how |
|---|---|---|---|
| legs (`azRigLegs`) | geo 0 / hydro 1 / pyro 2 | bracer_l/r, paw_l/r, gaiter_l/r, foot_l/r, apron, belly | palette-swapped models (navy-black or deep red stone, glowing carved lines; the belly cracks glow in Pyro) |
| legs | hydro / pyro | glow_bracer_l/r, glow_gaiter_l/r, glow_apron | white line masks 0.025 b proud, `tintindex 0`, item definitions with constant tints (`#cde6ff` / `#ffb070`), brightness 15; the `empty` model in Geo |
| tail (`azRigTail`) | geo 0 / cryo 1 / electro 2 | plates_neck/sh/mid/hip, t1..t8, tip | palette-swapped models: slate / violet-dark plates with glowing edges; the tail skin, blades and bark go to the deep end of the element's stone ramp with thin glowing cracks and blade rims (the cream ventral face and the skirt keep their gold veins), the leaves become crystal sprays / violet blossoms; t6..t8 and tip (the blossoms) at brightness 15, t1..t5 stay 13 |

The eyes stay red and the gold (horns, crystals, studs) stays gold in every look. The model and item names per
part and look are in the manifest (`looks`).

## 5. Skeleton and pose channels

Rig frame: +X = the boss's left, +Y up, -Z forward, blocks; origin = the floor under the centre of the four feet.
Joints (rest, `azhdaha_pose.mjs J`): pelvis (hip line) 0,3.0,2.4; spine1 0,3.35,0.3; chest 0,3.35,-1.7; neck1
0,3.05,-2.55; neck2 0,2.6,-3.05; head (atlas) 0,2.05,-3.3; jaw hinge 0,1.3,-3.6; left shoulder 2.3,3.25,-2.15,
elbow 2.95,2.3,-1.8, wrist 3.15,0.5,-2.45; left hip 2.0,3.0,2.45, knee 2.35,1.9,1.5, hock 2.5,0.72,3.05; tail root
0,2.85,4.75; tail segments 2.3, 2.1, 1.9, 1.8, 1.7, 1.6, 1.6, 1.5 (14.5 b). Rest silhouette: H 7.0 b (tallest plate),
nose to rump 10.2 b, wheelbase 5.0 b, claw span 8.1 b, horn span 4.4 b, snout 0.85 b, crest 2.65 b, eyes 1.5 b.

Pose channels (`DEFAULT_POSE`): `pos [0,y,0]`, `rot [p,y,r]` (about ROOT_PIVOT 0,2.8,0.4), `pelvis spine chest
neck1 neck2 head` eulers, `jaw` (deg open), `beard1 beard2 apron` eulers, `flN flS flM flH` plate flare (deg, +
stands the plates up), `flK` plate scale, `fwL fwR` wrist targets and `fpL fpR` paw eulers, `hkL hkR` hock targets and
`hfL hfR` foot eulers (root frame: planted feet stay put while the body rears), `t1..t8` tail eulers (pitch - raises a
segment) plus `tLift tCurl tSweep tTwist` (`tSweep` is spread root-weighted by `TAIL_SWEEP` .30 .20 .15 .11 .08 .07
.05 .04: the root leads, the distal tail stays nearly straight), `vis visBody visTail`. The tail curl constants live in
`azhdaha_clips.mjs`: `TAIL_REST` (idle arc), `TAIL_LOOP`, `TAIL_LOW`, `TAIL_WHIP`, `TAIL_PILLAR` (+ `TAIL_PILLAR_ROOT`);
authored bends stay at 30 degrees per joint or less. Clips carry no horizontal root travel and no root
yaw (the module moves and turns the anchor). The legs are solved by two-bone IK at bake time with the rest bend as
the pole (`ik()` with `prevV` continuity across frames).

## 6. Clips (R1: static debug poses)

| clip | state | what |
|---|---|---|
| `rest` | normal | DEFAULT_POSE: idle stance, head low, the tail in a big arc over the back, the leafy tip over the mid-back at ~10 b (v3 23.6 s) |
| `head_up` | normal | the neck raised, the face forward (v1 f2130) |
| `roar` | normal | jaw 45, head thrust up |
| `rear_up` | normal | roar_rear peak: pelvis +45, fore paws at chest height, tail braced on the floor |
| `stomp_lift` | normal | stomp_fl hang: left wrist at 3.0 b, weight to the right |
| `whip_mid` | normal | the tail just off the floor, swept 110 to the left (root-weighted) |
| `loop` | normal | the phase-3 tail loop / shells carry (v8 f2280: top ~11.7 b, the tip over the shoulders) |
| `tail_low` | normal | the tail laid out behind (v3 f1680) |
| `burrow` | normal | burrow dive mid-sink: root -3.4, nose down 22 |
| `burrowed` | burrowed | root -7.5, every part hidden |
| `tail_only` | tail_only | the phase-3 pillar at the anchor: body hidden, the tail rising from the floor in a slight S to ~12 b, the crown nodding forward |

Each is a 2-tick loop (46 keys at tick 0). The motion clips of motion.md §6 replace this list in a later stage.

## 7. Manifest and objectives

`tools/mboss_azhdaha_rig_manifest.json`: `parts` (name, region, uuid, tag, model, brightness, scale, elements),
`shadow`, `clips` (id, len, loop, next, events, keys, state, world `extents`, `cull_overhang` when a pose leaves the
30 x 12 box, `px` = hit-proxy points at tick 0, the events and the last tick), `looks` (per channel: objective, ids,
item per part and look, brightness, functions), `tinted_items`, `states`, `flash_groups`, `proxies` (`layout`: name,
bone, point, column width, top margin, tail-only flag; `rest`: the rest points), `skeleton`, `culling`,
`rest_extents`, `budgets`, `objectives`. The extents (and the culling overhang) come from the corners of each part's
rotated model box, so they are conservative: at rest they read y -0.35 while the lowest real vertex (the talon and
sole cards) sits at about -0.05.

Objectives: `azRigC` clip id, `azRigT` clip tick, `azRigF` flash countdown, `azRigY` face scratch, `azRigLegs`,
`azRigTail`, `azRigState`.

Hit proxies (plan.md R5, rigtech.md §3.3): 13 ground-anchored columns — `head chest belly hips tail1..tail5 paw_l paw_r
foot_l foot_r` — each `{x, z}` (the bone point projected on the floor, rig frame: +x = the boss left, -z = its front),
`base`, `top`, `w`; `hidden: true` when the bone is at scale 0 or the column's top is under the floor. The tail
columns sit on t2, t4, t6, t8 and the tip (the leafy crown, the phase-3 target) and are flagged for the tail-only
state.
The framework side (interaction entities, `combat/apply` routing, dedupe) is a later stage.

## 8. Build checks and budgets

- Parts 44-48 (warn), cap 56 (fail); every part has a display scale.
- `checkBounds` on every model (all coordinates within -16..32: reach 1.5 x scale from the joint).
- Every pose of every clip: no root x/z travel; the soles of the paws and feet at or above the floor unless the root
  is sunk; the tail-only state shows no non-tail part; events inside the clip; the culling-box overhang is recorded
  (warning) per clip. Rotation step checks of the shared compiler (120 degrees per tick / key).
- Sprites: sides multiples of 16 and <= 512; atlas total <= 1.2 M px (R1: 0.95 M px, 70 sprites; 93 models, 12.4 k elements in all, ~5.5 k shown at rest).
- Every look item exists; every tinted item points at a model.

## 9. Not in the rig

The element sigils, brands, floor glyphs, rocks, meteors, water orbs, ice spikes, lightning, the absorb vortex, the
burrow crater and rubble, the dust (fx kit); the seal steles (arena props); the interaction hit proxies and the body
solidity push (framework); the motion clips (later stage).
