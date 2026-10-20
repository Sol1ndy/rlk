# 야타용왕 (Azhdaha · 봉인된 바위 용의 왕) rig: API contract (stage R3b)

This is the contract between the Azhdaha display-entity rig and the chapter-1 boss module (not written yet). Stage R1
delivered the model, the skeleton, the element looks, the body states and the hit-proxy points; R2 refined the four
regions in parallel; R3 integrated them (seams, the RIGLIB shared libraries, the fixed UUID table, per-region budgets,
the root-offset rule, `look/petrify` and `glow/gold_*`; §11). R3a authored the 41 motion clips of plan.md §3 and wrote
the manifest in schema v1 (`az/contract/manifest.md`; §6, §7, §12); the R1 static poses survive as `dbg_*` clips. R3b
polished the model from `rigwork/r3_critique.md` and fixed poses without changing a clip name, length, event tick or
the manifest schema (§13). Binding decisions: scratchpad `az/plan.md` "Rig decisions" R1-R11, Rig decision
changes 1-3, §3 and the change notes; `az/contract/manifest.md`; references `az/understand/model.md`, `motion.md`,
`rigtech.md`.

Generator: `tools/build_mboss_azhdaha_rig.mjs`, split by region so that four authors can refine head, body, legs and
tail in parallel (plan.md R9):

| file | owns |
|---|---|
| `build_mboss_azhdaha_rig.mjs` | parts list check, the fixed UUID name table, per-region and total budgets, RP write (models, item definitions, tinted overlays, the sprites some model uses), clip compile, pose checks, API functions, hit-proxy points, manifest |
| `azhdaha_pose.mjs` | the skeleton `J` (rest joints, H = 7.0 b), `PART_SCALE`, `solve()` (FK of the spine / neck / head / jaw / beard / apron, plate-group flare, two-bone foot IK of the four legs, the tail chain), `toDisplay()`, `PROXIES` (the 12 columns of the contract, R3a) / `proxyPoints()` |
| `azhdaha_clips.mjs` | R3a: the binding clip table `CLIP_TABLE` (name, played / authored length, loop / next, RETIME knots, events at played ticks), the clip specs (key poses, foot plans, overlays, springs, hidden spans, states, anchors) baked by `bake()` into dense per-played-tick keys, `MIRRORS` (the `_r` clips derived from the `_l` ones), `RESPAWN_CLIP`, `TRACK_CLIPS`, `DEFAULT_POSE`, the tail curves (`TAIL_*`, `PILLAR_ROOT`), the `dbg_*` poses, helpers `tailUp`, `fore`, `hind` |
| `azhdaha_geometry.mjs` | thin aggregator: `PARTS`, `partModels()`, `LOOKS`, `TINTED`, `LOOK_BRIGHT` over the four region modules |
| `azhdaha_paint.mjs` | thin aggregator: `azhdahaSprites(keep)`, `spriteRegions()`, `paintAzhdahaTextures()`, `spriteId()`, the 1.2 M px atlas budget |
| `azhdaha_head.mjs` | head (V-wedge mask plates, brow ledges and wings, keel blade, a two-rank crown of gold-rimmed blades and crest fins, cheek guards, the ear plates 回 on their mounts, rounded skull, palate, upper teeth), jaw (V chin shield over a V-wedge lower jaw: cheek plates, underside, mouth floor, teeth, fangs, tongue), eyes (slits), horns (broad gold sleeve band bent into a C, gold-first meander inlay, bright outer rim and a dark inner lip, the ball knob at the band's lower end, the long dark horn flaring outward), beard bibs (card-only layers with thin top lips) |
| `azhdaha_body.mjs` | chest / belly / pelvis (sagging hide bands, scute rows, the rump ending inside t1), neck, apron (+ glow overlay), the four dorsal plate groups (saw-tooth profiles, left/right jitter), the three gold crystal groups (broad trident blades with solid cores) |
| `azhdaha_legs.mjs` | upper arms (round shoulder masses), engraved octagonal bracers (ragged dark crown, painted flush gold studs, solid amber elbow crystals), paws (knuckles, 4 talons, dew claw), haunches (round haunch + knee masses), shins (`gaiter_*`), the ribbed gaiter columns on `foot_*` (collar, crystal heel spur, forward-leaning rings, flared plinth, 3 + 1 talons), the four leg glow overlays |
| `azhdaha_tail.mjs` | t1..t8 (a broad lens-section body: cream ventral face with the gold midrib and chevrons, dark scale-plated flanks, the ridge blades, the V-fan side rows and the flank plates; collared, capped joints), the gnarled leafy branch t6..t8 and the tip (thorns, twigs, leaf sprays / blossoms), `tail_skirt` (R3b: the cream rump bell under the tail root, a flap hinged at t1, §13), the tail's per-part culling boxes (`CULL_BOX`) |
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
| `spawn` | boss spawn, respawn | Kills old parts, summons the 47 parts in the rest pose plus the shadow helper, re-applies the stored looks and body state (visibility, follow list, shadow radius), and queues the looping clip that holds that state: normal `idle`, burrowed `burrow_travel`, tail-only `tail_pillar` (manifest `rig_states.respawn_clip`), so a respawn never shows a hidden body. |
| `tick` | every tick | Respawns missing parts, follows the anchor (position + yaw; only the parts of the state's follow list, skipped while the anchor has not moved), advances the clip, runs the hit flash. |
| `play/<clip>` | any time | Plays a clip from tick 0 at the next `tick` (the 41 clips of §6; `play/dbg_<pose>` for the 8 static debug poses, manifest `functions.play_dbg`). A clip that ends with `next` chains into it; one without `next` (`tail_pillar_sink`, `death`) holds its last pose. |
| `start/<clip>` | internal | Chains into a clip now. |
| `face/player`, `face/track`, `face/set {yaw}` | AI | Anchor yaw (track: at most 2 degrees per call: a slow, heavy turn). |
| `look/legs/<geo\|hydro\|pyro>` | phase 2 absorb | Legs channel: bracers, paws, the gaiter columns (`foot_*`), apron, belly cracks, glow overlays. Stored in `azRigLegs`. |
| `look/tail/<geo\|cryo\|electro>` | phase 3 absorb | Tail channel: the four dorsal plate groups and the tail chain (leaves to blossoms). Stored in `azRigTail`. |
| `look_apply` | after respawn | Re-applies both stored looks. |
| `look/petrify` | death (t96) | Death seal: both channels back to geo (stored), every part 3 levels darker (block and sky), a 12-tick gold rim pulse on the horns and crystals (`azRigF`). A respawn shows the base looks at full brightness: call it again. |
| `glow/gold_on`, `glow/gold_off` | the 천동만상 tell, the absorbs | The gold parts (horns, the three crystal groups) from matte 13 to 15 and back. Not stored (re-call after a respawn). |
| `state/normal`, `state/burrowed`, `state/tail_only` | burrow, phase 3 | Records the body state (`azRigState`), hides what must not show, sets the follow list and the shadow radius (§3). The clips call them themselves at their state ticks (§6 `state`), so the module only needs them outside a clip. |
| `follow`, `follow_now` | internal / state changes | The RIGLIB follow (`createRigFollow`): `follow_now` drops the static-skip cache first. |
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
- Per tick: 47 `tp` (follow) + dispatch + the keys of the current clip. Elements shown at once (R3b): 5 618 at rest in Geo,
  at most 5 748 (Hydro legs + Geo tail) over the 9 look combinations; the build fails above 8 000 (rigtech.md §2.2:
  6-8 k visible is the client budget).

## 3. Body states (plan.md R7, rigtech.md §4, contract §4.6)

| state | id | follow list (`azRigFl`) | shadow | respawn clip | what shows |
|---|---|---|---|---|---|
| normal | 0 | `all` (47 parts) | 4.5 | `idle` | what the clip keys show |
| burrowed | 1 | `none` | 0 | `burrow_travel` | nothing: every part at scale 0 (the clip keeps them there, root -9 b) |
| tail-only | 2 | `tail` (`t1..t8 tip`) | 1.2 | `tail_pillar` | the tail chain only: every non-tail part at scale 0; the root sunk (`PILLAR_ROOT`, y -8.55) and offset by the root z of Rig decision change 1 (`root_z` +4.75 b, local frame) so the tail root lies under the anchor and the column rises straight out of the floor to ~12 b, the crown nodding forward |

The anchor (husk body) never goes into blocks: the clips sink the **rig** below the opaque arena floor. The floor
under the burrow must be opaque full blocks (rigtech.md §4.1). The tail-only state keeps the tail look. The parts
outside the follow list are not teleported (static follow skip, RIGLIB), so a burrowed or tail-only boss costs no
`tp` for its hidden parts. Hidden spans are exact per tick (§6 `hidden`; more parts may hide inside a span, never
fewer), and a looping clip per hidden state exists (the respawn clip), or the build fails.

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
`azhdaha_clips.mjs`: `TAIL_REST` (idle arc), `TAIL_LOOP`, `TAIL_LOW`, `TAIL_WHIP`, R3a's `TAIL_HIGH` (the slam
raise), `TAIL_FLAT` (the slam impact), `TAIL_BRACE` (the rear-up third leg), `TAIL_CAST` (the scorpion cast),
`TAIL_TUCK` (the dive), `TAIL_PILLAR` (+ `PILLAR_ROOT`); authored bends stay at 30 degrees per joint or less except
the pillar's t1 (+90 about the pelvis). Clips carry no horizontal root travel and no root
yaw (the module moves and turns the anchor). The legs are solved by two-bone IK at bake time with the rest bend as
the pole (`ik()` with `prevV` continuity across frames). Leg parts (R2): `uarm_*` / `thigh_*` turn with their bone
relative to its rest direction (rest-aligned masses); `bracer_*` (elbow -> wrist) and `gaiter_*` (the shin, knee ->
hock) are bone-aligned columns; `paw_*` / `foot_*` sit at the wrist / hock with their eulers. The hock is 1.5 b up:
`foot_*` is the near-vertical ribbed gaiter column (the metatarsus) plus the toes, so a planted hind foot keeps
`hfL/hfR` near [0,0,0] and a lifted one hangs the column from the hock. Soles: `SOLE` = paw -0.5, foot -1.5 (part frame).

## 6. Clips (R3a: plan.md §3, motion.md §5)

41 clips at played length (authored length in brackets: the wind-ups of plan.md §3 are cut by 25 % with RETIME knots
`authored>played`; every key is baked per played tick, so RETIME is already in the keys and the module only reads the
played ticks). Events are played ticks and match the table of plan.md §3 / contract §5 exactly (the build checks it).
`hidden` spans are inclusive played ticks (`all`: every part, `body`: every non-tail part); `state` calls the state
function at that tick; `root_z` spans `[t0-t1 dz]` (local frame, + = forward); `yaw` is the anchor yaw the module
applies over the clip (the schedule per played tick is in the manifest; + = clockwise, toward the boss's right);
`tracks`: `tail_root` / `tail_tip` per tick (manifest `clips[].tracks`).

| clip | len (authored) | then | events (played tick) | RETIME | hidden | other |
|---|---|---|---|---|---|---|
| `idle` | 80 (80) | loop | snarl 30 |  |  |  |
| `walk` | 40 (40) | loop | lh 0, lf 10, rh 20, rf 30 |  |  |  |
| `walk_stop` | 16 (16) | idle | plant 4 |  |  |  |
| `turn45_l` | 24 (24) | idle | plant_1 10, plant_2 17, yaw0 4, yaw1 18 |  |  | yaw -45 |
| `turn45_r` | 24 (24) | idle | plant_1 10, plant_2 17, yaw0 4, yaw1 18 |  |  | yaw +45; mirror of `turn45_l` |
| `turn90_l` | 36 (36) | idle | plant_1 12, plant_2 18, plant_3 24, plant_4 30, yaw0 6, yaw1 30 |  |  | yaw -90 |
| `turn90_r` | 36 (36) | idle | plant_1 12, plant_2 18, plant_3 24, plant_4 30, yaw0 6, yaw1 30 |  |  | yaw +90; mirror of `turn90_l` |
| `turn180` | 60 (60) | idle | plant_1 12, plant_2 18, plant_3 24, plant_4 30, plant_5 36, plant_6 42, plant_7 48, plant_8 54, yaw0 6, yaw1 54 |  |  | yaw -180 |
| `intro` | 150 (150) | idle | eyes 25, rise 30, crack1 50, crack2 70, seal 112, land 116, roar 120, blast 130 |  |  |  |
| `pose_ref` | 20 (20) | loop |  |  |  |  |
| `roar_low` | 40 (50) | idle | roar 8, blast 10 | 0>0 10>8 50>40 |  |  |
| `roar_rear` | 82 (100) | idle | rise 8, roar 20, drop 62, land 74 | 0>0 20>20 76>62 100>82 |  |  |
| `chin_slam` | 65 (84) | idle | lift 2, rear 14, top 23, drop 32, impact 35 | 0>0 47>35 84>65 |  |  |
| `jump_slam` | 53 (60) | idle | crouch 0, takeoff 6, apex 13, land 21, wave2 32 | 0>0 28>21 60>53 |  |  |
| `charge_coil` | 26 (34) | charge_run | coil 6, launch 24 | 0>0 32>24 34>26 |  |  |
| `charge_run` | 12 (12) | loop | plant 6 |  |  |  |
| `charge_stop` | 21 (24) | idle | skid 0, stop 8 | 0>0 8>8 24>21 |  |  |
| `spikes` | 40 (48) | idle | brace 0, launch 14, launch_last 20, gold_on 0, gold_off 22 | 0>0 18>14 24>20 48>40 |  |  |
| `stomp_fl` | 63 (72) | idle | lift 5, slam 13, w1 17, w2 32, w3 47 | 0>0 22>17 52>47 72>63 |  |  |
| `stomp_fr` | 63 (72) | idle | lift 5, slam 13, w1 17, w2 32, w3 47 | 0>0 22>17 52>47 72>63 |  | mirror of `stomp_fl` |
| `stomp_hl` | 63 (72) | idle | lift 5, slam 13, w1 17, w2 32, w3 47 | 0>0 22>17 52>47 72>63 |  |  |
| `stomp_hr` | 63 (72) | idle | lift 5, slam 13, w1 17, w2 32, w3 47 | 0>0 22>17 52>47 72>63 |  | mirror of `stomp_hl` |
| `stomp3_fl` | 85 (90) | idle | lift 3, s1 17, s2 40, s3 63 | 0>0 22>17 90>85 |  |  |
| `stomp3_fr` | 85 (90) | idle | lift 3, s1 17, s2 40, s3 63 | 0>0 22>17 90>85 |  | mirror of `stomp3_fl` |
| `feint` | 50 (56) | idle | sway 0, swayback 12, drop 18, burst 22 | 0>0 22>22 56>50 |  |  |
| `tail_whip_l` | 64 (64) | idle | raise 0, cock 12, pivot 20, sweep 23, sweep_end 31, erupt 33, settle 42 |  |  | yaw +115; tracks |
| `tail_whip_r` | 64 (64) | idle | raise 0, cock 12, pivot 20, sweep 23, sweep_end 31, erupt 33, settle 42 |  |  | yaw -115; mirror of `tail_whip_l`; tracks |
| `tail_slam` | 70 (90) | idle | raise 0, hold 9, slam 36, impact 39, spikes 41 | 0>0 52>39 58>45 90>70 |  | tracks |
| `burrow_dive` | 40 (44) | burrow_travel | snarl 3, dive 14, under 40 | 0>0 18>14 44>40 |  | state 40 burrowed |
| `burrow_travel` | 20 (20) | loop |  |  | 0-19 all |  |
| `burrow_breach` | 36 (36) | burrow_travel | ring 0, burst 8, hit 10, under 30 |  | 0-7 all, 30-35 all | state 8 normal, 30 burrowed |
| `burrow_emerge` | 53 (56) | idle | rumble 0, burst 8, fore 24, out 38, shake 40 | 0>0 40>40 56>53 | 0-23 all | state 24 normal |
| `landslide` | 203 (270) | idle | tell 0, w1 57, w2 77, w3 98, w4 118, w5 139, rear 159, w6 179, end 203 | 0>0 76>57 104>77 132>98 156>118 186>139 212>159 240>179 270>203 |  |  |
| `absorb` | 94 (108) | idle | press 0, rise 46, burst 47, stamp1 62, stamp2 86, gold_on 0, gold_off 60 | 0>0 12>12 60>46 108>94 |  |  |
| `absorb_p3` | 52 (70) | idle | orb 0, burst 42, gather 42, gold_on 0, gold_off 50 | 0>0 60>42 70>52 |  |  |
| `p3_sink` | 66 (80) | tail_pillar | sink 8, under 40, tail 40, pillar 58 | 0>0 8>8 50>40 80>66 | 40-65 body | state 40 tail_only; root_z 40-65 +4.75; tracks |
| `tail_pillar` | 80 (80) | loop | pulse 0, pulse2 40 |  | 0-79 body | root_z 0-79 +4.75; tracks |
| `tail_pillar_strike` | 24 (24) | tail_pillar | strike 10 |  | 0-23 body | root_z 0-23 +4.75; tracks |
| `tail_pillar_sink` | 20 (20) | hold | gone 18 |  | 0-17 body, 18-19 all | state 18 burrowed; root_z 0-19 +4.75; tracks |
| `tail_cast` | 34 (40) | idle | raise 0, charge 12, fire 18, lower 26 | 0>0 24>18 40>34 |  | tracks |
| `death` | 120 (120) | hold | stagger 0, chin 34, tail 66, last 80, head 92, still 96 |  |  |  |

Debug poses (R1, 2-tick loops, not in the module's table): `dbg_rest dbg_head_up dbg_roar dbg_rear_up dbg_stomp_lift
dbg_whip_mid dbg_loop dbg_tail_low`.

How the clips are made (`azhdaha_clips.mjs bake`): key poses at authored ticks with per-key easing, per-channel lag
(the pelvis / head trail the chest), a per-segment tail delay (`tailLag`: the tip arrives last), overlays (breath,
tremors, sways, gait functions), springs on the beards and the apron, then the feet:
`W` world-planted (counter-rotated by the anchor yaw schedule and compensated for the root), `K` body-key wrist /
hock targets, `R` riding the root, `F` gait functions, `S` hanging offsets from the shoulder / hip (rear-ups, the
air). The root never travels in x / z and never yaws (the module moves and turns the anchor); `pos y` and pitch /
roll only. A floor guard lifts the body (`bodyLift`) or the part (neck, beards, apron, wrists, tail) where a pose
would cut the floor, except inside a clip's `contact` span (the chin slam, the absorb press, the death collapse:
<= 0.22 b) and while airborne (`jump_slam` 7-20: the module raises the anchor). The `_r` clips are exact mirrors of
the `_l` ones (x negated, yaw negated, the anchors and tracks mirrored).

## 7. Manifest and objectives

`tools/mboss_azhdaha_rig_manifest.json`, schema 1 (`az/contract/manifest.md`): `schema`, `boss`, `source` (`rig`),
`runtime` (namespace, clip / tick / state / look objectives), `functions` (init, spawn, tick, kill, uninstall,
look_apply, `play` per clip, `play_dbg`, `face`, `state`, `look_legs`, `look_tail`, petrify, glow_on / glow_off,
`flash`, follow, follow_now), `parts`, `shadow`, `uuids`, `skeleton`, `rest_anchors` (contract local frame: x left,
z forward, so the rig's z is negated: nose, head column / front, chest, hips, tail root, the four soles, back),
`torso_hw` 3.0, `proxies` (`layout`, `rest`, `rest_pose`, `note`), `states` and `capsules` (contract §4), `rig_states`
(ids, `respawn_clip`, `follow_list`, the RIGLIB follow lists / fixed shadow / static skip), `flash_groups`, `looks`,
`tinted_items`, `clips`, `culling` {30, 12, 3}, `culling_per_part`, `rest_extents`, `budgets`, `objectives`,
`textures`.

Per clip: `id name len authored loop next mirror_of retime events` (played ticks), `anchors` ({event: [[x, y, z] per
named point]} in the local frame at that played tick: `impact`, `nose`, `chin`, `paw` (the planted foot of
`plants`), `tip_end`, `back`, `launch_1..4`, `tail_root`, `tail_tip`), `tracks` (tail clips, §6), `px` (`lerp: true`,
`keys` {"<t>": {proxy: [x, z, top]}}: every proxy in every key, keys at 0 and len-1 and wherever the linear
interpolation of the per-tick points would miss by more than 0.1 b; `top` = the column top above the floor, 0 =
hidden), `yaw` (per played tick or null), `hidden`, `root_z`, `state`, `extents` (world box over the clip; null when
nothing shows, `burrow_travel`), `cull_overhang`, `keyFiles`, `keys`, `note`.

Objectives: `azRigC` clip id, `azRigT` clip tick, `azRigF` flash countdown, `azRigY` face scratch, `azRigLegs`,
`azRigTail`, `azRigState`, `azRigFl` follow list (0 all, 1 tail, 2 none) and `azRigQ`, `azRigQx/y/z/w` (the RIGLIB
static-skip cache).

Hit proxies (plan.md R5, contract §6.1): the 12 ground-anchored columns of the contract, in UUID order `head chest
belly hips tail1..tail4 paw_l paw_r foot_l foot_r` (0x41 ... 0x4C), on the bones head, chest, belly, pelvis, t1, t3,
t5, t7, paw_l/r, foot_l/r (R3's `tail5` on the tip is gone). `proxies.rest` keeps the contract's pinned rest numbers
(the module's stub reads them; `api.P_TAIL_LANE` uses `tail2`), `proxies.rest_pose` the real points of the idle pose;
for tail1..tail4 the two differ (§12). A column is the bone point projected on the floor (local frame) with its
width `w` and top margin from `layout`; its top is 0 (hidden) when the bone is at scale 0 or under the floor. The framework side
(interaction entities, `combat/apply` routing, dedupe) is a later stage.

## 8. Build checks and budgets

- Parts 44-48 (warn), cap 56 (fail); every part has a display scale, a region and a `UUID_INDEX` entry (unique,
  0x01-0x3F); part names outside the tag space above; at most 16 hit proxies.
- Per-region budgets (plan.md §3.1, atlas px rebalanced by change note 1), fail when exceeded:

  | region | parts | sprite px | R3 use | R3b use |
  |---|---|---|---|---|
  | head | 8 | 0.24 M | 7 parts, 0.187 M | 7 parts, 0.182 M |
  | body | 14 | 0.42 M | 14 parts, 0.397 M | 14 parts, 0.400 M |
  | legs | 16 | 0.32 M | 16 parts, 0.314 M | 16 parts, 0.306 M |
  | tail | 10 | 0.16 M | 10 parts, 0.146 M | 10 parts, 0.149 M |
  | shared material tiles | - | 0.06 M | 0.053 M | 0.053 M |
  | total | 48 (cap 56) | 1.2 M | 47 parts, 1.097 M px, 154 sprites | 47 parts, 1.09 M px, 137 sprites |

- Elements shown at once <= 8 000 in every look combination (R3: 4 465 max; R3b: 5 748 max, hydro / geo; 11 626
  elements in all models, 5 618 shown at rest).
- `checkBounds` on every model (all coordinates within -16..32: reach 1.5 x scale from the joint).
- Every pose of every clip: no root x travel and no root yaw; a root z offset only on ticks where no body (non-tail)
  part is shown (Rig decision change 1, recorded as `root_z`); the soles of the paws and feet at or above the floor
  unless the root is sunk, the clip is airborne (`floorFree`) or hidden; the hidden spans exact per tick; the
  tail-only state shows no non-tail part; the events equal the binding table; the culling-box overhang (radial
  `cullOverhang`: the box does not turn with the yaw; buried points do not count) is recorded (warning) per clip.
  Rotation step checks of the shared compiler (120 degrees per tick / key).
- Contract checks: the chin slam's head column top <= 3.5 b on played 35-55; the tail-only columns stack on the
  anchor (<= 0.3 b) on the pillar ticks; every `TRACK_CLIPS` clip has tracks of `len` entries; the mirrors equal their
  source mirrored (<= 0.08 b).
- Gold parts at 13 and in no look channel; the eyes at 15 in every look; a looping clip per hidden body state (the
  respawn clip).
- Runtime suite (scratchpad `az/tests_rig/test_az_rig.py`, mcsim over the generated functions): the UUID table and
  budgets of the manifest, spawn / respawn of the 47 parts + shadow, the follow, every clip to its end with its tick-0
  pose equal to the exact debug pose, the clip states, the 9 look combinations and their respawn, the body states and
  their respawn, the flash groups, `glow/gold_*`, `look/petrify`, the root-offset rule, uninstall; R3a adds the v1
  manifest, the idle queued at spawn, every clip run to its end (state switches, follow lists, the hand-over, loop or
  hold, the gold glow), the tick-0 keys against the debug poses of their targets, the hidden spans per tick, the state
  lists and shadow radii, the respawn clips (604 checks). The module's `tests_mod/check_az_manifest.py` (S1-MOD)
  passes against this manifest (3 317 checks).
- Sprites: sides multiples of 16 and <= 512; only the sprites some model uses are painted and registered.
- Every look item exists; every tinted item points at a model.

## 9. Not in the rig

The element sigils, brands, floor glyphs, rocks, meteors, water orbs, ice spikes, lightning, the absorb vortex, the
burrow crater and rubble, the dust (fx kit); the seal steles (arena props); the interaction hit proxies and the body
solidity push (framework); the anchor's motion: walking speed, the turn yaw (the clips carry the schedule), the jump's
height and glide, the charge glide, the burrow travel (module).

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
  1-3 per cluster, within the R1 crystal part reach. (R3b: broad trident blades, §13.)

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
  the tail chain raised (t2..t8 0.5-1.4 b into the floor with the rear_up tail curl). R3a went back to the
  contract's 12 proxies (tail5 dropped, §7).

## 12. R3a notes (clip authoring)

- Key-pose strips per clip next to the footage frames: scratchpad `az/rigwork/r3a/strip_<clip>.jpg` (top: footage at
  the authored tick; below: the rig at the matching played ticks and the events, 3/4 front and side, the anchor yaw
  applied; `tools/strip.py`), numeric checks `tools/ck.mjs` (floor per shown part, IK reach and stretch, the chin
  column, the pillar stack), the debug dp `rigwork/r3a/dbg` (`build.sh`).
- Floor contacts left on purpose: the chin slam jaw (0.16 b on played 36-39), the absorb press and the death
  collapse (inside their `contact` spans); the fore bracer rims touch the floor by up to 0.14 b in the turns, the
  whip and the charge coil (the wrist lift is capped so the paws do not leave the floor).
- Things the rig cannot know: the landslide turns the anchor in the module during 0-45, the planted feet then slide
  with it; the jump's air poses assume the module's leap height; the charge run assumes the 1.0 b/t glide.
- `proxies.rest` stays pinned to the contract numbers for tail1..tail4 while `rest_pose` has the real points; S1-MOD
  should move contract §6.1, the stub and the checker to the real numbers (or the rig re-pins them).
- The limb stretch reaches 1.08-1.10 at a few transition ticks (turn90 / turn180 steps, the roar and intro landings,
  the chin slam rear) and 1.12 in `dbg_rear_up` (reach 0.27 short: a static R1 pose).

## 13. R3b notes (rig polish from `rigwork/r3_critique.md`)

Clip names, lengths, event ticks and the manifest schema are unchanged; the manifest's poses, tracks, proxies and
extents follow the new geometry and poses. Renders: scratchpad `az/rigwork/r3b/U2_sheet.jpg` (the U1 layout) and
`az/rigwork/r3b/P1_before_after.jpg` (the critique's P1 items, before = `r3crit/out`).

- Body (`azhdaha_body.mjs`): the flank's widest line sags from the shoulder to mid-body and rises to the groin (the
  hide bands follow it instead of level rings); darker, greener hide ramp (`SKIN`, now in `azhdaha_materials.mjs` with
  `skinPx`, shared with the legs); the scute rows and the plastron rolls repainted darker; hide ledges darkened like
  the wrap; the rump tapers to end inside t1 and its underside behind the haunches is hide (no cream ledges there);
  neck1's top stays under the hump (max y 3.96 b vs the chest top 4.29 b); the neck ruff plates sit further forward.
  Gold crystals: 9 clusters of broad trident blades (0.47-0.62 b across, two-tone gold with a ridge line, a solid
  core to half length), each with two side prongs at -45 / +45 degrees, rooted 0.22 b inside the hull, left / right
  copies jittered. Plates: saw-tooth edges, the orange only on the tips of one cell, a ridge line and greyish rims,
  small extra plates, left / right length and position jitter. Apron: hem lifted at the sides, the meander moved up.
- Legs (`azhdaha_legs.mjs`): the shoulder (`uarm_*`) and haunch (`thigh_*`) are round masses (the same ellipsoid
  lofted along z and along x with inscribed stations, ledges retextured to light-corrected tiles), a knee mass on the
  haunch, a thicker shin; elbow crystals and the heel spur are solid amber prisms with facet cards; the gold cube studs
  are gone (flush painted studs on the collar); the bracer narrower (r 0.74-0.8) with a taller dark crown; the gaiter
  rings lean forward and widen downward to a flared plinth.
- Head (`azhdaha_head.mjs`): the horn sleeve is shorter with gold-first meander inlay, a bright rim and a dark inner
  lip; the ball knob sits at the band's lower end; the dark horn is longer (top 5.9 b at rest) and flares outward
  (`PART_SCALE` horn_l / horn_r 2.0 -> 2.7); the beak is a V; narrower jaw cheeks; the beards are card-only layers with
  thin top lips; saturated eye paint.
- Tail (`azhdaha_tail.mjs`): the segment cores end tucked inside the next segment; a ventral blade row (mirrored
  downward blades) on t2..t5; a narrower cream band and irregular scute cells; 8 leaf clusters with bigger sprays.
  `tail_skirt` (`PART_SCALE` 1.8 -> 2.2) is a lobed bell of bent card strips (the cream centre strip with the gold Y
  vein, the side strips bent 45 degrees and painted as dark rump hide so that they do not read as a cream plank from
  the side) with a dark seal box inside t1, hung SKIRT_TILT = 35 degrees bottom-forward under the rump.
- The skirt flap (`azhdaha_pose.mjs`, after the root transform): it hangs at most `SKIRT_HANG` = 50 degrees from the
  vertical; where its hem (`SKIRT_HEM`, samples along the lobed hem of all three strips) would go below
  `SKIRT_FLOOR` = 0.04 b it swings (<= 30 degrees, the way it already leans), then folds into the tail root (its
  length and wrap depth scaled down to >= 0.05); the guard fades out between root y -0.6 and -1.0 (sinking clips).
  The skirt is no longer in the clip baker's floor-guard body group (`GROUPS.body`), so it never lifts the root.
- Poses (`azhdaha_clips.mjs`): `REAR()` swings the apron by -0.8 x the pelvis pitch, so it hangs and covers the
  rearing chest; the roar_rear / intro fores hang down and a little forward from the shoulders (chest-frame wrist
  offsets [1.5, -1.65, 1.9] / [1.45, -1.85, 1.7], paws curled), the bracers within ~30 degrees of the body axis and
  clear of the head from the side; `TAIL_HIGH`'s branch (t5-t8) curls further over the back so the raised tip of
  tail_whip_l / _r and tail_slam stays inside its 18 b culling box (it overshot by 0.19 / 0.38 b). No culling
  warnings remain.
- Floor (`rigwork/r3b/tools/ck.mjs`, every played tick of every clip, the skirt by its hem samples): the skirt no
  longer touches the floor in any clip (it dipped up to 0.9 b in the rear-ups before the fold); the R3a bracer rim
  contacts in the turns, the whip and the charge coil are gone with the narrower bracer. Left: the chin slam jaw
  (0.16 b on played 36-39, the contact span), jump_slam paw_l 0.14 b at t6 (the crouch), burrow_dive foot_r 0.23 b
  at t17 (the dive), p3_sink paw_r 0.11 b at t11, and soles at -0.06 b in a few charge_run / jump_slam ticks.
- head_up: the beard ends about 1 b ahead of the apron when the head rises; the throat between them shows the neck's
  cream underside ledges, not the dark hide (`rigwork/r3b/out/zz_throat.jpg`).
- Atlas 1.09 M px (head 0.182, body 0.400, legs 0.306, tail 0.149, shared 0.053 of the change-note-2 shares 0.24 /
  0.42 / 0.32 / 0.16 / 0.06); elements shown max 5 748 / 8 000.
