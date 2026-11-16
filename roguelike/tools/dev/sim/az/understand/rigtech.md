# Rig tech for very large display-entity bosses (야타용왕 Azhdaha, 아펩의 오아시스 파수꾼)

Study for the two chapter bosses: how the existing display-entity rigs work, what changes when the boss is 3-5 times
larger, how player hits reach a huge body, how to burrow, and what to build. Everything below was read from the code
or measured on it; the measurements come from a scale probe built with the real shared libraries (see §0).

Path prefixes:
- `T:` `/home/user/rlk/roguelike/tools`
- `F:` `/home/user/rlk/roguelike/data/rlk/function`
- `FG:` `S:mb3/wt_fg/roguelike` (wip/fg, the newest framework, read only)
- `S:` `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`
- `W:` `S:az/understand/rigtech_work`

## TL;DR

1. **Parts are articulation and server cost; elements are detail and client cost.** Use about **44-48 rig parts (hard cap 56)**,
   not 80 or 120. Put the extra care into elements per part (the Guardian forearm already has 373 elements) and into
   textures. Add about **12 invisible hit proxies** (interaction entities). These have no render cost.
2. **Bounds.** A part reaches at most **1.5 × display scale** blocks from its joint along each axis (model −16..32 =
   joint ±24 units). The probe's head failed `checkBounds` at scale 2 (3.1 b snout) and passed at 2.2. Use scale 2.5-3
   for torso blocks, about 2.2 for the head, and 1.2-2 for legs and tail segments.
3. **Culling box.** All four existing rigs use `width:16f,height:16f`. Every part's box is centred on the **anchor**, so a
   tail tip 14 b behind the anchor is culled while the anchor is off screen. Use **`width:30f,height:12f`** for every
   part of a 20+ b boss, or 0 to turn culling off.
4. **Hits.** Melee and most skills select `@e[tag=rlk_mob,distance=..R]` from the player's feet. That distance is
   measured to the target's **position**, not its hitbox (`F:combat/find_immediate.mcfunction:60-62`).
   - With one body husk, a player standing at the boss's outline is within 3.5 b of the target on only **22.5 %** of
     the outline (worst case 6.2 b).
   - With **11 ground-level hit proxies** (7 on the spine + 4 legs), **100 %** of the outline is within 3.0 b.
   - Proposal: interaction entities tagged `rlk_mob` on the bones. A one-line forward at the top of
     `F:combat/apply.mcfunction` turns a proxy hit into a hit on the body, positioned at the proxy (one HP pool, one
     element aura, one kill path).
   - One hit per attack per boss, using a sequence number.
   - Per-part vulnerability by toggling the `rlk_mob` tag.
5. **Interpolation at scale.** Compile tolerances are absolute (0.012 b). Long parts on arcs therefore need a key every
   tick: the probe's tail whip and burrow cost 23.5 keys per tick out of 29 parts.
   - Moving the whole-body yaw to the **anchor** (`tp` with `teleport_duration`) cut the whip to **6.2 keys/t**.
   - Scale `tol.t` per part (0.035 b cuts the burrow from 23.5 to 11.1 keys/t).
6. **Burrowing.** Sink the root below an **opaque** arena floor; the floor hides the buried part, as the probe renders
   show. Set unused parts to scale 0. Never move the husk body into blocks. Tail-only state: sunk root, tail chain
   raised, the other parts at scale 0, a crater prop, and only the tail proxies vulnerable.
7. **Atlas.** The items atlas of the current RP already holds **11.4-12.5 M px**, of which `raiden/fxg` is 6.9 M. A
   4096² atlas holds 16.8 M px. Budget **≤ 1.2 M px rig + ≤ 0.6 M px kit per chapter boss**, sprite sides multiples
   of 16, ≤ 512.
8. **Renderer.** `S:mb/gw/tools/preview.py` (used by `S:mb3/rigwork/tools/r.sh` and `renders.py`) **no longer exists**.
   `S:az/understand/rigtech_render.py` wraps the surviving `S:preview/raiden_preview.py` with the UUID-selector patch.
   It was verified on the fieldgen rig and on the probe (about 8 s per render).

---

## 0. What was run for this study (reusable)

| file | what |
|---|---|
| `S:az/understand/rigtech_render.py` | Render wrapper. It imports `S:preview/raiden_preview.py`, adds UUID selectors (the patch of `S:mb2/bfv/render_bfv.py:45-67` / `S:mb3/fgi2/render_integ.py:47-67`), runs its CLI and writes JPEG for `-o *.jpg`. Item-model swaps (`data modify entity <uuid> item.components."minecraft:item_model" ...`) work through it; tested with `fieldgen/rig/look/field_swap`. |
| `S:az/understand/rigtech_stats.py` | Models, elements, sprites and atlas px per rig in an RP. |
| `S:az/understand/rigtech_clips.py` | Keys per tick per rig from the rig manifests. |
| `W:tools/rigtech_probe.mjs` | Scale probe: a 29-part box block-out of Azhdaha built with `mboss_model_lib`/`mboss_rig_math`/`mboss_rig_clips`/`mboss_rig_compile` (copies of FG:tools). It runs `checkBounds`, compiles 6 clips at two tolerances (`W:probe_report.txt`), writes `W:rp`, `W:dp` and `W:dbg` (`az_dbg/<clip>/<t>` debug poses) and the rest boxes `W:rest_boxes.json`. |
| `W:rigtech_cover.py` | Melee reach coverage of the body outline for hit-entity layouts (§3.2). |
| `W:probe_rest.jpg`, `probe_tail_whip_20.jpg`, `probe_burrow_22.jpg`, `probe_tail_only_20.jpg`, `test_fg_rest.jpg` | Renders. The blue columns are 0.6 × 1.8 b players. |

The fieldgen rig was rebuilt into `W:` (copy of FG:tools, `--no-paint`, RP = copy of `S:mb3/rp_fg` fieldgen textures) to
prove the loop. Nothing in the repo or any worktree was touched.

---

## 1. How the existing rigs work, end to end

### 1.1 Files and outputs

| rig | generator (entry) | pose / geometry / paint / clips | outputs |
|---|---|---|---|
| Corrupted Guardian | `T:build_mboss_guardian_rig.mjs` | `T:guardian_pose.mjs`, `guardian_geometry.mjs`, `guardian_paint.mjs`, `guardian_clips.mjs`, `guardian_screen.mjs` | RP `assets/rlk/{textures,models/item,items}/mboss/guardian/*`; DP `F:mboss/guardian/rig/**` (rebuilt from scratch, `:44-46`); `T:mboss_guardian_rig_manifest.json` (`:272-281`) |
| Moonlit Butterfly | `T:build_mboss_butterfly_rig.mjs` | `butterfly_pose/geometry/paint/clips.mjs` | same layout, `F:mboss/butterfly/rig/**` |
| Field generator | `FG:tools/build_mboss_fieldgen_rig.mjs` | `fieldgen_pose/geometry/paint/clips.mjs` | same layout, `FG:data/rlk/function/mboss/fieldgen/rig/**` |
| Raiden (chapter boss today) | `T:build_raiden_rig.mjs` (hand-rolled, older) | inline | `F:boss/raiden/rig/**`, `T:raiden_rig_manifest.json` |

Shared libraries (identical on main and wip/fg except `mboss_model_lib.mjs`, which wip/fg extends):
- `T:mboss_rig_compile.mjs`: the clip compiler.
- `T:mboss_rig_math.mjs`: vectors, quaternions, FK/IK.
- `T:mboss_rig_clips.mjs`: clip format, retime, sampling.
- `T:mboss_model_lib.mjs`: item-model geometry.
- `T:mboss_paint_lib.mjs`: procedural sprite painting.
- `T:mboss_screen_lib.mjs`: full-screen overlays drawn as title-font glyphs.

The wip/fg extensions of the model lib add these options (`FG:tools/mboss_model_lib.mjs:148-201`):
- `lathe` `tile` / `inward` / `range` / `phase`.
- `annulus` with `stagger` against z-fighting.

### 1.2 Parts, addressing and the summon

- **Fixed UUIDs per part**, so every per-tick command addresses a part directly with no selector scan.
  - Guardian `524c4b4d-4247-4400-8000-0000000000NN` (`T:build_mboss_guardian_rig.mjs:62-64`).
  - Butterfly `…4246-4c00…` (`T:build_mboss_butterfly_rig.mjs:59-61`).
  - Fieldgen `…4647-4400…` (`FG:…fieldgen_rig.mjs:61-63`).
  - The int form is `[I;1380731725,<block>,-2147483648,NN]`.
- **Tags** on every part: `rlk_room, rlk_mb_aux, rlk_mb_part, rlk_mb_<boss>_part, rlk_mb_<xx>_<part>`, plus alias tags
  (butterfly `:184-186`, fieldgen `:240-242`).
- **Summon NBT**: Guardian `:207`, butterfly `:187`, fieldgen `:243`.

  ```
  item_display {UUID, Tags, billboard:"fixed", item_display:"none", interpolation_duration:1, teleport_duration:1,
                view_range:2.5f (fieldgen 3f), width:16f, height:16f, shadow_radius:0f, brightness:{block:12..15, sky:15},
                transformation:<rest pose>, item:{id:"minecraft:paper", components:{"minecraft:item_model":"rlk:mboss/<id>/<model>"}}}
  ```

  - `item_display:"none"`: no display context transform, so model units / 16 = blocks × part scale.
  - `brightness` is per part: glows are 15, bodies 12-14 (Guardian `PARTS` `:51-61`).
  - `width/height 16` is the frustum-culling box (see §2.5).
- **Part budget checks** in the generators: butterfly ≤ 34 (`:58`), fieldgen ≤ 32 (`FG:…:60`). The earlier plan budget
  was "about 30 display entities" (`S:mb2/code/reuse.md:533-545`).
- **Superset rigs.** Every form's parts exist all the time; unused ones sit at scale 0.
  - Butterfly forms: `form/human|butterfly` (`:223-226`).
  - Fieldgen: seven forms (`FG:…:269-280`).
  - Hidden spans are recorded in the manifest (`FG:…:330`, `FG:tools/fieldgen_clips.mjs:272-276`).

### 1.3 Item models, textures and atlas

- **A-frame.** +X = the boss's left, +Y up, −Z forward. Units are model units relative to the display pivot, the model
  centre `[8,8,8]`.
  - Converted with `toM = (8−X, 8+Y, 8+Z)` (`T:mboss_model_lib.mjs:14-15`).
  - Element rotations are single-axis, in 22.5° steps within ±45, enforced by `rotM` (`:34-39`).
  - Coordinates must stay within **−16..32**: `checkBounds` (`:199-202`) throws, matching the game's model loader.
- **Building blocks.**
  - Boxes `abox` (`:41-57`).
  - Painted cards `cardZ/cardX/cardY` (`:60-101`, `:223-228`): zero thickness, both faces, `shade:false`; the sprite
    carries the lighting.
  - Turned solids `lathe/turned/knob/taperY` (`:148-197`): 16 facets, unshaded, wrap-round sprite.
  - Polar discs (`:168-175`).
  - `mirrorModel` (`:207-220`): the right side is a mirrored copy, so no negative scale is needed.
  - `shiftModel` (`:230-236`).
- **Texture ids.**
  - Sprites are `rlk:mboss/<id>/<name>` PNGs.
  - Each model lists only the sprites it uses (Guardian `writeModel` `:72-76`).
  - Item definitions select the model, optionally with **constant tints**. The Guardian's element looks are one model
    plus N tinted item definitions (`:77-78`, `:87-100`), with faces carrying `tintindex 0` (`cardZ … tint`).
  - Sprites enter the **items atlas** via `minecraft:single` sources in `assets/minecraft/atlases/items.json`
    (427 entries in `S:rp_final7`).
- **Sprite rules** (enforced in the generators):
  - sides ≤ 512 (butterfly animated strips ≤ 1024 high);
  - multiples of 16, so the whole atlas keeps mip level 4;
  - per-rig atlas budget: butterfly 2 M px (`T:build_mboss_butterfly_rig.mjs:78-85`), fieldgen 0.5 M px
    (`FG:…:105-111`).

Measured (`rigtech_stats.py` on `S:rp_final7` and `S:mb3/rp_fg`):

| rig | models | elements (all models) | biggest models | sprites | atlas px | models at the −16..32 limit |
|---|---|---|---|---|---|---|
| Guardian | 47 | 1 303 | l_fore 373, l_upper 338, bracket 259 | 69 | 1.05 M | 0 |
| Butterfly | 57 | 3 110 | pod 630, cocoon 612, orb 272 (props) | 72 | 1.33 M | 0 |
| Fieldgen | 47 | 4 083 | core 488, bubble_* 204 | 106 | 0.45 M | 1: `ring` (scale 2.4, outer radius 3.5 b, `FG:tools/fieldgen_geometry.mjs:65`) |

### 1.4 Pivots, display transforms and scale

- A part's transform is `{translation, left_rotation, scale, right_rotation:[0,0,0,1]}` (`T:mboss_rig_compile.mjs:34`).
  The rotation pivot is the model centre, so each model is authored with its **joint at the model origin** (limbs hang
  along −Y, the tail runs along +Z).
- The rig works in its own frame and converts with a z mirror: `toDisplayT = [x, y, −z]`,
  `toDisplayQ = [−x, −y, z, w]` (`T:mboss_rig_math.mjs:111-112`). Each pose module's `toDisplay` multiplies the scale by
  `PART_SCALE` (`T:guardian_pose.mjs:132-135`, `T:butterfly_pose.mjs:158-161`).
- `PART_SCALE` is blocks per 16 model units:
  - Guardian 1-2.2 (`T:guardian_geometry.mjs:27-31`);
  - butterfly 0.82-3.5, with wings at 3.5 using half-size models (`T:butterfly_pose.mjs:40-46`);
  - fieldgen 1-2.4 (`FG:tools/fieldgen_pose.mjs:36-44`).
- Raiden keeps every piece "within the native model cube bounds. Larger forms use display transforms"
  (`T:build_raiden_rig.mjs:50`).
- **Reach rule.** The −16..32 range is the joint ±24 units, so the maximum reach is **1.5 × scale** blocks per axis.

### 1.5 Poses and clips

- **Clip format** (`T:mboss_rig_clips.mjs:1-20`): `{name, len, loop?, next?, blend?, keys:[[tick, sparse pose, ease]],
  events, note}`.
  - Keys merge onto the default pose (`accumulate` `:52-55`).
  - Eases `io/i/o/l` (`:50`).
  - Channels: numbers and 3-vectors lerp, quaternions slerp, strings switch at their key (`blendPose` `:57-67`).
  - `sampleClip` (`:70-80`) samples fractional ticks.
  - Retime knots (`:19-47`) map authored to played ticks; keys and events are moved with them.
- **Forward kinematics.** Each rig has a `solve(pose)`: a root transform about `ROOT_PIVOT`, FK chains and two-bone arm
  IK with bend-plane continuity (`T:mboss_rig_math.mjs:64-84`) (Guardian `T:guardian_pose.mjs:38-130`).
- **Events.** `events` are ticks that the pattern code schedules hits and fx on; they go to the manifest.
  - Butterfly and fieldgen also export **fx anchors** (world points of hoof tips, wing tips, ports) at each event tick
    (`T:build_mboss_butterfly_rig.mjs:96-105, 165`; `FG:…:124-144, 221`).
- **Per-clip checks** in the generators:
  - butterfly: no root x/z travel (the module moves the body), hooves never below the floor, events inside the clip
    (`:124-143`);
  - fieldgen: tips above the floor (`FG:…:167-187`);
  - Guardian: spear-butt-on-face check (`:138-157`).

### 1.6 Compilation into functions (`T:mboss_rig_compile.mjs`)

- **Segment fitting** (`:46-62`).
  - At tick a, a part gets the pose of tick b with `interpolation_duration b−a`. b is the furthest tick whose
    in-between poses the client's **lerp of translation/scale and slerp of rotation** (`interp` `:35`) reproduce within
    `tol`.
  - `tol.t` in blocks, `tol.s`, `tol.r[part]` in degrees (`close` `:39-45`).
  - A segment never turns more than `maxSegDeg` (120 − 2).
  - The first segment of a clip lasts at least `blend` ticks (default 3), so any clip eases in from any pose.
- **Rotation safety** (`:63-75`, `:88-95`). There is a per-tick step limit of 120° (the build fails above it), and a
  half-tick warning where the client's slerp leaves the authored path by more than 35°.
- **Outputs per clip** (`:80-128`).
  - Key files `c/<clip>/k/<t>` hold one `data merge entity <uuid> {start_interpolation:0,interpolation_duration:N,
    transformation:…}` per keyed part (`:96`).
  - Discrete model channels (hand fist/open, cube frames, looks) compile to item-model swap lines (`:100-102`).
  - `extraLines` run per tick (form or look switches) (`:103`).
  - Debug poses `<x>_dbg/<clip>/<t>`, the exact pose of every part, are for the offline renderer (`:104-105`).
- **Dispatch.**
  - Per-clip runner `c/<clip>/run` (loop/next/hold header) plus a binary tree over the key ticks (≤ 6 leaves)
    (`:108-122`).
  - `play/<clip>` queues the clip and `start/<clip>` chains into it (`:123-124`).
  - Global dispatch `run`: a binary tree on the clip id (`:130-139`).
  - No macros on the hot path.
- **Facing** (`:142-166`): `face/player`, `face/track` (≤ maxDeg per call; fieldgen 4°/t, `FG:…:304`) and `face/set`.
  The anchor's yaw is the body's facing; parts inherit it every tick.

### 1.7 Runtime per tick

Guardian `:222-228`, butterfly `:211-218`, fieldgen `:258-265`. `rig/tick` runs as the body (the anchor) at its feet,
from the module tick (`F:mboss/guardian/tick.mcfunction:15`):

1. `execute unless entity <uuid of a key part> run function …/spawn` respawns the rig if a part is missing.
2. `execute rotated as @s rotated ~ 0 run function …/follow` runs **one `tp <uuid> ~ ~ ~ ~ ~` per part**. With
   `teleport_duration:1` the client interpolates position and yaw; pitch is never inherited.
3. `scoreboard players add @s <x>RigT 1`, then `function …/run` (dispatch, then only the keys that start this tick).
4. The hit flash countdown.
   - `flash` sets `Glowing:1b, glow_color_override` on the outlined parts for 3 ticks (Guardian `:232-236`).
   - Persistent glow looks (`glow_apply` `:237-245`).

Looks are item-model swaps:
- Guardian eye and spear (`:247-258`);
- butterfly wing looks (`:227-239`);
- fieldgen looks and crack stages (`FG:…:281-296`);
- re-applied after a respawn by `look_apply`.

Props are free item_displays that are not rig parts and that `follow` never touches (Guardian `prop/spear` `:263-268`,
butterfly `:255-272`, fieldgen `:307-319`).

### 1.8 Sizes and costs

From `rigtech_clips.py` (manifests) and `du --apparent-size` of the generated rig functions:

| rig | boss size | parts | clips / ticks | key files | part keys | keys per tick: mean (worst clip) | DP rig functions |
|---|---|---|---|---|---|---|---|
| Guardian | ≈ 3.4 b tall (hit 1.6 × 3.4) | 29 | 26 / 1 111 | 939 | 10 142 | 9.1 (31 % of parts); `chaos_leap` 21.3 | 1 429 files, 2.8 MB |
| Butterfly | 2.8 b (BH), wings ≈ 2 × 3.5 b | 30 | 22 / 1 085 | 835 | 14 284 | 13.2 (44 %); `wing_strike` 25.5 | 1 281 files, 3.8 MB |
| Fieldgen | ring D 7.0 b, centre 4.5 b | 29 | 28 / 2 647 | 1 936 | 14 499 | 5.5 (19 %); `slam` 13.9 | 2 880 files, 4.0 MB |
| Raiden | ≈ 4.5 b armoured (husk scale 2.2) | 52 | 25 × 4 phases | every tick is a full pose | 52 per tick | 52 | 2 068 files, **30 MB** |

Per-tick command cost of an mboss rig:

| step | commands |
|---|---|
| respawn check | 1 |
| follow | N `tp` by UUID |
| tick counter | 1 |
| dispatch | about 4-8 |
| keys | k `data merge` |
| total, Guardian | about 29 + 9 + 8 ≈ 46 commands |

The Raiden rig is the expensive model and should not be copied (`T:build_raiden_rig.mjs:455, 477-481, 521-523`):
- 52 `data merge entity @e[tag=rlk_rd_<n>,limit=1]` per tick, each a full entity scan with no UUID and no `type=`;
- a **linear** dispatch of `execute if score @s rdPhase … if score @s rdRigT matches t` lines (`F:boss/raiden/rig/clip/idle.mcfunction` has 165 lines);
- poses for 4 phases;
- 30 MB of functions.

---

## 2. Scaling to a boss several times larger (6-10 b tall, 14-22 b long)

### 2.1 Model bounds and display scale

- **Reach per scale** (joint ±24 units): 1.0 → 1.5 b, 1.5 → 2.25 b, 2.0 → 3.0 b, 2.5 → 3.75 b, 3.0 → 4.5 b. A diagonal
  reaches up to √3 times that.
  - The probe's head (3.1 b from the jaw joint to the snout) failed at scale 2 with
    `model head leaves -16..32: 11.2,9.6,-16.8 …` and passed at 2.2.
  - The fieldgen ring is the only existing model at the limit (scale 2.4 for a 3.5 b radius).
- **Choosing scale.** Use the smallest scale that fits the part's reach plus about 10 % headroom for later sculpting.
  - The display scale does not limit resolution: the texel density is set by the sprite, not the scale (§2.3).
  - Precision is not an issue: elements are rounded to 1e-4 units (`r4`); translations are written with 5 decimals
    (`T:mboss_rig_compile.mjs:30-33`).
- **Pivot placement.** Keep the joint at the model origin and let the part extend one way (tail segments along +Z,
  legs along −Y). Then the whole ±24 range on that side is usable.
  - A part longer than 1.5 × scale needs a larger scale or a split into two parts.
  - A split adds a joint, which helps the animation anyway.
- **Non-uniform scale** works (the Guardian arms stretch along Y, `T:guardian_pose.mjs:90-91, 104-105`). Avoid it on
  painted parts, because it stretches the texels.

### 2.2 Silhouette and geometry at size

- **Element rotations** come in 22.5° steps on one axis per element. Arbitrary angles come only from the part's display
  rotation, so a spike crown at odd angles costs either quantised spikes or extra parts. Quantised 22.5°/45° spikes read
  fine on rock armour.
- **Lathe facets.** A 16-facet lathe has a radius error of 1 − cos 11.25° = **1.9 %**: 0.04 b on a 2.2 b body radius,
  visible on the silhouette.
  - 32 facets would need 11.25° element rotations, which are not available.
  - If a round section matters, two displays rotated 11.25° apart carry two 16-gons. Their union stays within about
    0.5 % of the circle.
  - Organic rock bodies are better built from boxes, cards and plates than from lathes.
- **Back faces.** Item models are back-face culled: a player who walks inside a closed box sees through it. Keep the
  big volumes closed and keep players out of the torso (§3.6). Cards are two-sided by construction (`cardZ` writes
  north and south faces).
- **Translucency.** Every part's entity position is the anchor, so the order of translucent parts between entities is
  not controllable. Prefer cutout (alpha 0/255) for crystals and spikes, and keep translucent glows on parts that do
  not overlap others in common views. The renderer also writes no depth for translucent faces (`S:mb3/fgi2/render_integ.py:358-359`).
- **Client budget.**
  - Existing rigs show at most about 1.3-4 k elements at once.
  - A detailed dragon can afford **about 6-8 k visible elements**, about 25-40 k quads; item displays re-submit their
    quads every frame.
  - Spend them on the head, the paws and the crest. The probe block-out has 53 elements, so the real model will be
    about 100 × that.

### 2.3 Texture resolution and the atlas

- **No UV tiling.** A face's UV is one rectangle inside 0..16 of one sprite. A big wall either shows one large unique
  sprite or is split into several elements, each showing a tile.
  - The fieldgen `lathe … tile:true` option (`FG:tools/mboss_model_lib.mjs:148-157`) exists exactly to reuse a small
    tile on every facet.
  - Use unique painted sprites where the silhouette and features are (face, horns, crest, paws, the mane edge) and
    tiled elements for the bulk hide (rock scales).
- **Texel density target.** At 1080p with FOV 70, one block at distance d covers about 1080 / (2·d·tan 35°) px:
  - 77 px at 10 b;
  - 38 px at 20 b;
  - 26 px at 30 b.

  Players fight a 20 b boss from about 3-15 b. Recommended densities:

  | surface | px per block |
  |---|---|
  | hide and limbs | **32** |
  | head, jaw, eyes, horns, claws, crest crystals | **48-64** |

  For comparison, the Guardian runs about 80-240 px/b on 1-3 b parts (`gd_shield` 384 px over about 1.6 b); that is
  not needed at dragon size.
  - A 4.6 b chest side at 32 px/b is 147 px, so a 160 px sprite.
  - A 3.3 × 1.6 b head side at 64 px/b is 208 × 112 px.
- **Atlas totals.** Measured with `atlases/items.json` sources:

  | RP | items atlas total | largest contributors |
  |---|---|---|
  | `S:rp_final7` | 11.36 M px | raiden/fxg 6.91 M, player weapons 1.11 M, butterfly 1.06 M, guardian 1.05 M, bf_kit 0.83 M |
  | `S:mb3/rp_fg` | 12.47 M px | the above + fg_kit 0.93 M, fieldgen 0.45 M |

  - A 4096² atlas holds 16.8 M px before packing losses.
  - Two chapter bosses at 1.5 M (rig) + 0.9 M (kit) each would push the atlas to **8192 × 4096** (about 170 MB of
    VRAM with mips).
  - Budget **≤ 1.2 M px rig + ≤ 0.6 M px kit per chapter boss**.
  - If Raiden stops being every chapter's boss, its 6.9 M px of `raiden/fxg` (`ringq_*` up to 576²) are the obvious
    place to reclaim.
- **Sprite rules** (as in §1.3): sides ≤ 512, multiples of 16. A single odd-sized sprite lowers the mip level of the
  whole atlas.
- **Element looks.** Phase 2 legs and chest take Pyro/Hydro; phase 3 back and tail take Cryo/Electro. Use the
  Guardian's method:
  - one model per part, whose vein or glow cards carry `tintindex 0` over a white sprite;
  - several **item definitions with constant tints** (`T:build_mboss_guardian_rig.mjs:77-78, 96-100`);
  - `look/<el>` swaps the item model (`T:build_mboss_butterfly_rig.mjs:227-239`).

  No extra models or atlas space are needed.

### 2.4 Z-fighting

- The depth buffer is 24 bit with near plane 0.05. The resolvable depth step is about d² / (0.05 · 2²⁴):

  | distance | depth step |
  |---|---|
  | 20 b | 0.0005 b |
  | 32 b | 0.0012 b |
  | 64 b | 0.0049 b |

- **Rule.** Keep coplanar or overlapping faces at least **0.01 b** apart in world space, that is ≥ 0.16 / scale model
  units (0.064 units at scale 2.5).
- Two **different parts** must never share a surface. Each has its own matrix, so their surfaces never coincide
  exactly and always fight. Seat plates 0.02-0.03 b proud of the hide.
- The libraries already avoid coplanar overlaps inside one model:
  - `turned` overlaps 0.02 units into the wider neighbour and closes steps with discs at 0.995 R
    (`T:mboss_model_lib.mjs:176-189`);
  - `annulus` `stagger` (`FG:tools/mboss_model_lib.mjs:179-192`).

  These are scale-independent in model units, so they get *safer* at larger scale.

### 2.5 View range and the culling box

- `view_range` × 64 × the client's entity-distance setting is the render distance. Existing values:
  - 2.5 gives 160 b at 100 % and 80 b at 50 %;
  - fieldgen uses 3.0.
  
  A 23 b boss in a radius 22-30 arena (`T:mboss_registry.json` arena `r:22`; Raiden arena radius 23,
  `T:build_raiden_arena.py:50`) is fine with **3.0**.
- **Culling box.** `width`/`height` define the frustum-culling AABB around the entity position: ±width/2 horizontally,
  0..height up. 0 in either turns culling off. Every rig part sits at the **anchor** (`follow` tps all parts there), so
  the box is centred on the boss centre for every part.
  - All existing rigs use 16 × 16 (Guardian `:207`, butterfly `:187`, fieldgen `:243`, Raiden `:521`). Fieldgen props
    use 4 × 4 (`FG:…:316`).
  - The probe's rest pose spans z −8.7..+14.25 and y 0..7.5. The tail tip is 14 b behind the anchor, **outside ±8**.
    When the camera looks at the tail with the torso off screen, the tail parts are culled and pop.
  - **Use `width:30f,height:12f` on every part** (2 × the largest horizontal reach + 1 b; crest or raised head + 1 b).
    The cost is only less frustum culling for a few dozen entities.
  - Parts below the anchor, buried, fall outside the box (it starts at the anchor's y). That does not matter, because
    they are hidden.

### 2.6 Brightness, lighting, outline

- `brightness` overrides sampled light per entity: all parts use `{block:12..15, sky:15}`.
  - A part sunk into the floor, or an anchor in a dark corner, would otherwise sample light 0 and render black. Keep a
    fixed brightness on every part.
  - Sky light 15 still follows the world's time of day in the lightmap. For a cave look independent of time, use
    `{block:15, sky:0}`-style values; check in game.
- **Emissive parts** (eyes, gold crystals, phase veins) can only differ by brightness *per entity*. Split them into
  their own parts at 15 (crown, eyes, crystal clusters, as the Guardian does with `halo_glow`, `spear_glow`), and keep
  the hide at 12-13.
- **Shading.** Boxes keep the game's face shading (`shade:true`); painted cards and lathe facets are `shade:false` and
  carry painted light (`T:mboss_model_lib.mjs:107-114`). Keep that split on the dragon: rock blocks shaded, painted
  feature cards unshaded.
- **Hit flash.** The Glowing outline on *every* part (Guardian `:232-236`, 3 ticks) would outline all internal seams of
  a 48-part dragon several times per second. Flash only the **part group of the hit proxy** (head / front / rear /
  tail) or use a short look swap.

### 2.7 Shadows

All parts use `shadow_radius:0f`. The shadow is drawn at the entity's position on the blocks below. For grounding, give
one dedicated invisible display (an empty model) `shadow_radius` 4-5 and `shadow_strength` about 0.8 under the torso,
and optionally one under the head for lunges. Move them with the anchor or with the bones' ground projection, as the
hit proxies (§3.4) are moved. Radius max 64.

### 2.8 Interpolation at scale (measured)

Tolerances are absolute, so a long part swinging on an arc of radius R has a chord error of R(1 − cos(Δθ/2)) per
segment. At R = 8 b and 18° per tick that is 0.098 b, far over `tol.t` 0.012, so it is keyed every tick.

Probe (29 parts, `W:probe_report.txt`):

| clip | default tol (t 0.012 b) | scaled tol (t 0.035 b) |
|---|---|---|
| idle 40 t | 1.8 keys/t | 1.4 |
| **tail_whip** 30 t (root yaw −20 → +35° + tail sweep) | **23.5** | 17.0 |
| **tail_whip_anchor** (same, root yaw left to the anchor) | **6.2** | 5.5 |
| stomp 30 t | 4.0 | 3.0 |
| **burrow** 30 t (root sinks 8.5 b, pitch −25°) | **23.5** | 11.1 |
| tail_only 40 t | 3.4 | 2.2 |

Every clip keys all parts at its first tick (the blend key). That is the peak of 29.

Conclusions:
1. **Whole-body motion goes on the anchor, not on the parts.**
   - Yaw: the module or the clip turns the anchor (`face/set`, `rotate @s`) and `follow` carries it with client
     interpolation for free. That gives 3.8× fewer keys in the whip.
   - Horizontal travel is already the module's job (alignment rule "pos x/z = 0" in butterfly and fieldgen).
   - For a vertical sink, add an optional **follow offset** (a few `follow_y<k>` variants or one macro
     `$tp <uuid> ~ ~$(dy) ~ ~ ~`). The husk body must never go into blocks (§4.1).
2. **Per-part translation tolerance.** Extend `createRigCompiler` with `tol.tp = {part: blocks}` next to the existing
   `tol.r` map (`T:mboss_rig_compile.mjs:42`), default `tol.t`. Use about 0.03 b on the big parts and keep 0.012 on
   head and paws. The other rigs stay byte-identical.
3. Keep the 120° per-tick and 118° per-segment safety rules; tail whips at 20-25°/t per segment are far inside them.

### 2.9 Part budget and per-tick cost

Per-tick server cost of a rig with N parts:
- N `tp` (follow);
- about 5-8 dispatch commands;
- k `data merge`, each an NBT read-merge-write plus an entity-data packet;
- flash: N merges on, N off.

| budget | follow tp/t | keys/t (mean / whip peak) | DP size (est. 40 clips, 3 000 t) | verdict |
|---|---|---|---|---|
| 40 | 40 | about 10 / about 25 | about 5 MB | lean |
| **48** | 48 | about 12 / about 30 (anchor yaw, scaled tol) | **about 6-7 MB** | **recommended** |
| 80 | 80 | about 20 / about 80 | about 11 MB | possible, but the extra parts add little (detail comes from elements) |
| 120 | 120 | about 30 / about 120 | about 16-20 MB, Raiden-like | not advisable |

Notes:
- The DP size estimate uses about 200 bytes per key line; the probe wrote 457 KB for 6 clips and 200 t.
- The commands per tick stay far below the 65 536-command limit; the cost is NBT merges and packets, not the count.
- **Static skip.** Azhdaha stands still in most attacks. Store the anchor's x/z/yaw (×100) and skip `follow` when
  unchanged; this saves the N tps most of the time.
- **Per-state follow lists.** In the tail-only state, follow only the visible parts (as the butterfly's proposed
  `follow_h`/`follow_b`, `S:mb2/code/reuse.md:513`).

---

## 3. Hit detection for a huge body

### 3.1 How player attacks hit bosses today

| path | selection | measured from | file |
|---|---|---|---|
| Click input | the attack button is read from interactions: `atkBlock`/`atkStrike` in front of the eyes, and per-mob **click shields**. A click only triggers the swing; it does not choose the target. | interaction hitbox (vanilla reach 3 b to the box) | `F:combat/atkstrike_spawn.mcfunction`; `F:combat/mshield_tick.mcfunction:2-6` → `mshield_click` → `F:combat/input/poll_attack.mcfunction` |
| Click shield | one interaction per `rlk_mob`, `{w,h}` 1.2 × 2.2 (big custom mobs 1.5 × 2.7); mid-boss body: registry `hit{w,h}`; Raiden 1.4 × 2.6 / 1.8 × 4.5 armoured. None while `rlk_mb_inv`. | follows the mob | `F:mob/shield_ensure.mcfunction:6-25`; `T:build_mboss_core.py:100, 452-455`; butterfly per form `F:mboss/butterfly/form/hitbox_{h,b}.mcfunction` |
| Melee basic attack | `as @e[tag=rlk_mob,distance=..3.5\|5\|4.5]` + front 180° (`melee_front`) | **entity position** (feet) | `F:combat/find_immediate.mcfunction:58-62`; `F:combat/melee_begin.mcfunction`; `F:combat/melee_front.mcfunction` |
| Skills and AoE | `@e[tag=rlk_mob,distance=..R]` with R 1.8-16 (about 150 selectors; most common ..4, ..3.5, ..3, ..5, ..2.5, ..6) | entity position | all over `F:char/**`, `F:items/proc/**` |
| Reactions | `as @e[tag=rlk_mob,distance=..2\|3.5\|4\|12] … element/aoe_hit` | entity position | `F:element/core_*.mcfunction`, `F:element/aoe_hit.mcfunction` |
| Projectiles (bow, Ronova, Navia pellets, Clorinde scan) | `positioned ~-0.75 ~-0.75 ~-0.75 … @e[tag=rlk_mob,dx=0.5,dy=0.5,dz=0.5]`, a ±0.75 b box test | **hitbox** (the husk's scaled box) | `F:char/bow/arrow_step.mcfunction:13`, `arrow_hit.mcfunction:5`, `F:char/navia/pellet.mcfunction:6` |
| Aim assist / target pick | points on the aim ray at 2/4/6/8 b, `distance=..0.88-1.72,sort=nearest` | entity position | `F:char/bow/assist.mcfunction:3-6`, `F:char/ronova/find.mcfunction`, `F:char/arlecchino/find.mcfunction` |
| Camera aim (shoulder view) | `dx=0,dy=0,dz=0` box per 0.5 b step | hitbox | `F:view/aim_step.mcfunction:2` |
| Damage | `F:combat/apply.mcfunction` with @s = the target; aura, RES (`mres` + module `incoming`), number at `~` (the execution position), kill | — | `:15-17` mid-boss dying/inv gates; `:23` module `on_hit`; `:27` aux routing; `:80` `death_start` |
| Aux hit objects | invisible NoAI husks `rlk_mb_hit` with their own HP pool and overhead bar; damage → `mboss/aux_hit` → module hook (`#mbAuxDone`) → `aux/take` | husk | `T:build_mboss_core.py:948-1018` |
| Body | NoAI invisible husk, `attribute minecraft:scale` = registry `scale` (Guardian 1.5, butterfly 1.4 → 1.8 in butterfly form, fieldgen 2.4, Raiden 2.2 armoured); vanilla box 0.6 × 1.95 × scale | — | `T:build_mboss_core.py:420-445` |

Two facts decide the design:
- **Melee and almost all skills measure to one point.** The husk scale attribute enlarges the box, which helps only
  projectiles and camera aim. It does not help `distance=` selectors.
- **Interaction entities are left out of `mob/setup` and `mob/tick`** (`F:tick.mcfunction:31-32`,
  `type=!minecraft:interaction`). An interaction tagged `rlk_mob` is therefore selected by every attack, but gets no HP
  bar, stun, AI or physics.

### 3.2 Why one body fails at this size (measured)

`W:rigtech_cover.py` takes the probe's rest pose, rasterises the floor footprint of the body (45.9 b²) and puts a player
0.4 b outside it at 334 points. For each it computes the horizontal distance to the nearest hit-entity position.

| layout | worst | mean | reached at R 3.5 | R 3.0 | R 2.5 |
|---|---|---|---|---|---|
| A: one body at the anchor (today's model) | 6.20 b | 4.41 b | **22.5 %** | 16.2 % | 0 % |
| B: 7 spine + 4 legs = 11 | 2.65 b | 1.65 b | **100 %** | 100 % | 95.2 % |
| C: 9 spine + 4 legs = 13 | 2.65 b | 1.53 b | 100 % | 100 % | 95.2 % |
| D: 9 spine + 4 legs + 4 flank = 17 | 1.78 b | 1.23 b | 100 % | 100 % | 100 % |

Rule of thumb: along a body of half-width w, spine entities at spacing s leave a worst gap of √((w + 0.4)² + (s/2)²).
For R − margin = 3.0 and the torso half-width 2.3, s ≤ about 3.8 b.

### 3.3 Proposal: interaction hit proxies on the bones, one HP pool

**Entities.** About 12 `minecraft:interaction` proxies per boss, summoned with the rig.
- UUIDs come from the boss's block, NN from 0x40 up.
- Tags `rlk_room, rlk_mb_aux, rlk_mob, boss, rlk_mb_px, rlk_mb_px_<part>`, plus a `response:false` box `{w, h}`.
- Score `mbPart` = part id (head 1, chest 2, …), used for per-part effects.

**Placement.** Proxies are **ground-anchored columns**: position = the bone's floor projection (anchor y), height = the
bone's top + 0.5. Melee distance is then horizontal, and the box still covers the volume for arrows and camera aim.
- An airborne part (jump slam) lifts its proxy to bottom − 1, or is disabled for the jump.
- The rig compiler already samples every tick. Add a **proxy track** per clip: the bone's ground point relative to the
  anchor (`^x ^ ^z`, rig frame +X = left).
  - At key ticks, write the offsets into storage (`data modify storage rlk:<boss>rig px set value {…}`). Emit only when
    a proxy moved more than 0.3 b.
  - Every tick, run one macro `function …/px/follow with storage …` holding
    `$execute rotated as @s rotated ~ 0 positioned ^$(hx) ^ ^$(hz) run tp <uuid> ~ ~ ~` per proxy.
  - Cost: about 12 commands per tick, plus a macro instantiation only when the arguments change.

**Click input.** The proxies are also the click targets. Poll them in the module tick with two lines like
`F:combat/mshield_tick.mcfunction:2-3`:

```
execute as @e[type=interaction,tag=rlk_mb_px] if data entity @s attack at @s run function rlk:combat/mshield_click
execute as @e[type=interaction,tag=rlk_mb_px] if data entity @s interaction at @s run function rlk:combat/mshield_rclick
```

Do not tag them `rlk_mshield`. `mshield_tick` would kill them whenever a tick passes without `rlk_msync`, for example
during a framework pause. Shrink the body's own click shield (registry `hit`) to the torso.

**Routing (framework edit, 1 line in `F:combat/apply.mcfunction`, before the encounter-object line `:8`):**

```
# Hit proxies of a huge boss (interaction entities on its bones): the hit becomes a hit on the body, positioned here.
execute if entity @s[tag=rlk_mb_px] run return run function rlk:mboss/px/hit
```

`mboss/px/hit` (new, in `T:build_mboss_core.py`):

```
# @s = proxy, at @s. One hit per attack per boss (#atkSeq + gametime), body or proxy, whichever is hit first.
execute store result score #now mb run time query gametime
scoreboard players set #dup mb 0
execute as @e[type=husk,tag=rlk_mb_body,limit=1] if score @s mbPxT = #now mb if score @s mbPxS = #atkSeq tmp run scoreboard players set #dup mb 1
execute if score #dup mb matches 1 run return 0
scoreboard players operation #mbPart mb = @s mbPart
scoreboard players set #mbVia tmp 1
execute as @e[type=husk,tag=rlk_mb_body,limit=1] run function rlk:combat/apply
scoreboard players set #mbVia tmp 0
```

`execute as` keeps the proxy's position, so the damage number and hit particles appear at the proxy (they use `~`,
`F:combat/apply.mcfunction:36-49`). Element aura, RES, the module `on_hit`/`incoming` hooks, rewards and `death_start`
all run on the body exactly as today.

**Dedupe.**
- In `combat/apply`, after `:17`, the body also runs the same check-and-stamp for direct hits:
  `execute if entity @s[tag=rlk_mb_big] unless score #mbVia tmp matches 1 if function rlk:mboss/px/dup run return 0`.
  `px/dup` stamps `mbPxT/mbPxS` and returns 1 on a duplicate.
- `#atkSeq tmp` is incremented once per attack event:
  - `F:combat/melee_begin.mcfunction` (before the melee loops);
  - `F:combat/clear_atkflags.mcfunction` (all skill and item paths through `char/dmg_calc` and others);
  - the reaction cores `F:element/core_*.mcfunction`;
  - `F:element/dot.mcfunction`.
- A path that does not increment only risks merging with an earlier attack *in the same tick* on the same boss: a lost
  hit, never a double hit.

**States and per-part flags.**
- A part is **vulnerable** exactly while its proxy carries `rlk_mob`. `px/state/<name>` functions toggle the tag and
  park disabled proxies 8 b under the floor:
  - `normal`
  - `burrowed`: none vulnerable, plus `rlk_mb_inv` on the body; the existing gate at `combat/apply.mcfunction:17`
    blocks everything, true damage included only when wanted.
  - `tail_only`: tail1-4 only.
  - `jump`
  - `dead`
- Per-part damage effects (weak spots, part breaks) go through `#mbPart` in the module `incoming` hook
  (`F:mboss/d/incoming.mcfunction`).
- **HP floor.** The phase-transition floors (2/3, 1/3) and "cannot die while burrowed, a final hit after surfacing"
  are a clamp in `incoming`: `#dmg ≤ mhpC − floor`, floor = 1 while burrowed or tail-only.

**Recommended layout for Azhdaha** (rig frame, rest pose; B of §3.2 plus one head-front proxy):

| proxy | ground point (x, z) b | w × h b | notes |
|---|---|---|---|
| head | 0, −7.2 | 2.8 × 5.0 | follows the head; jaw open lifts h |
| chest | 0, −3.4 | 4.6 × 7.0 | |
| belly | 0, 0.2 | 4.6 × 6.5 | the body husk sits here too (dedupe covers both) |
| hips | 0, 3.2 | 4.4 × 6.0 | |
| tail1 | 0, 6.8 | 2.6 × 4.5 | tail-only: enabled |
| tail2 | 0, 9.4 | 2.2 × 4.0 | tail-only: enabled |
| tail3 | 0, 11.6 | 1.8 × 3.5 | tail-only: enabled |
| tail4 (tip) | 0, 13.4 | 1.4 × 3.0 | tail-only: enabled |
| paws ×4 | ±2.2, −3.0 / ±2.1, 2.7 | 1.8 × 4.5 | stomp patterns |

### 3.4 Alternatives considered

- **Husk aux objects** (`aux/spawn`, `T:build_mboss_core.py:994-1018`). The module hook can take over with
  `#mbAuxDone 1` and subtract from the body. But:
  - the aura and reactions would run on each aux, not on the body (`element/on_hit` runs before the routing at
    `combat/apply.mcfunction:21-27`);
  - every aux gets an overhead HP bar and physics (mob/tick);
  - the kill and reward path is bypassed.
- **One "nearest point" body** that follows the player's closest point on the boss each tick. There is no framework
  edit, but arrows and placed AoE aimed at the far side miss, and a closest-point-to-segments search runs every tick.
- **A bigger husk scale.** The scale attribute is capped at 16. It only helps box tests, and a 4 × 12 pillar pushes
  players and blocks movement around the head.

### 3.5 Per-target state that is written outside `combat/apply` (audit list)

State set *inside* `combat/apply` lands on the body after the forward. Attack code that tags or scores the target
*before* `apply` sees the proxy:

| item | what happens with proxies | fix |
|---|---|---|
| Navia pellets | count hits per mob (`rlk_np` → `nvHit`, `F:char/navia/pellet.mcfunction:6`, `pellet_go.mcfunction:7`); `rose_hit` uses nvHit² (`rose_hit.mcfunction:4-5`). Pellets spread over two proxies split the count, and the dedupe then drops one share. | count on the body: `execute if entity @s[tag=rlk_mb_px] run …` adds to the body's `nvHit` instead |
| Arlecchino `arDir`, Ronova `rnEr`/`rnId`, Yoimiya `aurEnd` | marks stay on whichever proxy was picked | fine while the proxies persist; keep proxies alive (toggle `rlk_mob`, do not kill), or mirror to the body |
| Bow and Ronova assist picks | the target is a proxy; homing aims at its position (the floor point) and still hits the column | fine |
| `mob/aggro_keep` (every 0.5 s, `F:mob/aggro_keep.mcfunction`) | runs `damage @s 0 …` on proxies, which fails harmlessly | fine |
| Minimap `room/map_mobs` (up to 48 `rlk_mob`) | proxies would show as 12 dots | the minimap is hidden in boss fights; otherwise exclude `rlk_mb_px` |

### 3.6 Body solidity

Interactions have no collision. The body husk at the torso centre only pushes players near its narrow box, so players
can walk through a 4.6 b wide dragon. A small module step fixes this: every tick, if `rlk_body` is inside a torso or
head capsule, push it out horizontally, collision-checked like the `mboss/pull/tick` glide (`T:build_mboss_core.py:1836-1837`). Do not
use this for legs and tail, which players stand between and under in the original.

---

## 4. Burrowing

### 4.1 Hiding and showing a rig underground

- **Sink below an opaque floor.** Translate the root down (the `pos` channel; the probe's `burrow` goes to −8.5 b with
  −25° pitch). The arena floor's solid blocks depth-test the buried geometry away.
  - The probe renders show the cut line: `W:probe_burrow_22.jpg`, `W:probe_tail_only_20.jpg` (iso view, the floor
    hides the body).
  - Requirements: the floor where the boss sinks must be **opaque full blocks**, thick enough for the depth.
    - A shallow water layer (Azhdaha's domain) is fine *over* a solid floor; the body must sink below the solid top.
      Translucent blocks such as water, glass and leaves show the buried parts.
    - Below the floor there may be a cavity, so check that no void or lit room is visible from inside the arena.
- **Scale 0 once fully under.** Use the `vis` / per-part show channels. Compiled hidden spans cost one key, because
  hidden-to-hidden segments are always "close" (`T:mboss_rig_compile.mjs:29, 40-41`). Fieldgen already records hidden
  spans per clip in the manifest (`FG:…:330`; `warp_out` hides at 12, `FG:tools/fieldgen_clips.mjs:272-275`). Skip the
  hidden parts in `follow` while burrowed.
- **Cheaper sink.** A follow offset (§2.8, conclusion 1) moves all parts down with zero keys and client interpolation.
  Use it for the straight descent, and keys only for the pitch-in.
- **Brightness** stays fixed (§2.6), so parts crossing the floor never turn black.
- **Never move the husk body into blocks.** It is a mob, takes in-wall suffocation damage, and a vanilla death would
  delete the HP body. Keep the anchor on the floor (`NoGravity`) and sink the *rig* relative to it.
  - While burrowed, set `rlk_mb_inv` (`T:build_mboss_core.py:833-840`; `combat/apply.mcfunction:17`) and
    `px/state/burrowed`.
  - The module moves the anchor along the underground path (its `mv` lib, `T:build_mboss_core.py:1908-`).
- **Travel visuals** (footage v2: the gold crack ring marker, a rock mound or wall surfacing 2-3 times, falling rocks):
  - rubble props, free item_displays moved with `teleport_duration` 2-3 like the fieldgen bomb props;
  - block particles of the floor block;
  - kit decals.

  A brief surfacing in the burrow charge is a short `surface` clip: root from −6 to −1.5 and back, at most 10 t,
  enabling the chest and hips proxies for those ticks only if they should be hittable (the wiki says it is invulnerable
  underground).
- **Emergence.** Play `emerge` with the root starting at −8 under the target point and rising with ease `o`, then call
  `px/state/normal` at the event tick. Add a crack-ring decal and debris.

### 4.2 Azhdaha's tail-only state (phase 3 start)

- **Pose.** Root sunk about 6.4 b with pitch −12°; the tail chain pitched up 20-30° per segment, so 3-4 segments stand
  above the floor (`W:probe_tail_only_20.jpg`).
- **Mask.** The iso render shows the dorsal plates poking through the floor. In this state every non-tail
  part goes to scale 0 (a per-part `show` channel). A **crater / rubble ring prop** at the floor cut hides the
  intersection line.
- **Anchor.** Place the anchor (the body) at the tail's emergence point, so the body husk, the tail proxies and the
  burrow-centre telegraphs share one point.
- **Hits.** `px/state/tail_only`: tail1-4 proxies vulnerable, nothing else. The body's own direct hits are deduped with
  the tail hits and are co-located with them, so no special gate is needed.
- **HP floor.** The 1 HP clamp holds while `tail_only` is on (wiki: if HP reaches 0 while burrowed, a final hit is
  needed after it surfaces).
- **Element look.** Phase 3 colours the back and tail. The tail parts' tinted item definitions apply here before
  anything else is visible.

### 4.3 Apep's Warden

- **Phase 2 is underground for its whole length.**
  - Hide the rig (sunk, then scale 0), `px/state/burrowed`, `rlk_mb_inv`.
  - The **Heart of the Oasis** is a separate object with its own progress, not the boss HP. Use an aux object or a
    module score shown on the boss bar.
  - The organisms are ordinary mobs or aux husks with their own pools.
- **잠복 돌진 / 이동 돌진** (burrow, burst out at the player) use the same `burrow`/`emerge` pair as Azhdaha.
- **Tall body.** The hunched torso and the long thin limbs whose hands plant in the ground ("생명의 손") need limb
  proxies at the planted hands. The spine column needs a large h (8-10 b); the ground-column rule still applies.

### 4.4 Rig API additions

Keep the existing API (`spawn`, `tick`, `play/<clip>`, `face/*`, looks, props) and add:
- `px/state/<normal|burrowed|tail_only|jump|dead>`;
- `px/follow` (macro);
- an optional `follow_y<k>` (sink offset);
- `look/<pyro|hydro|cryo|electro>` and its tail-only variant;
- manifest `hidden` spans and per-clip `px` tracks.

---

## 5. Recommendation

### 5.1 Azhdaha bones and parts (≈ 44 + options, cap 48)

Proportions follow the probe: shoulder about 4.5 b, crest about 7-7.5 b, nose to tail tip about 20-23 b. Rig frame:
+X left, +Y up, −Z forward; the anchor is at the torso centre on the floor.

| group | parts | scale | brightness | notes |
|---|---|---|---|---|
| torso | pelvis, belly, chest | 2.5-3 | 13 | the belly underside is cream, the plate segments are cards; chest takes the phase-2 look |
| spine plates | dorsal_f, dorsal_r | 2 | 13 | dark jagged plates; phase-3 look |
| crystals | crys_l, crys_r (shoulders), crys_back | 1.5-2 | 15 | gold-amber, cutout |
| neck and head | neck, head, jaw, tongue/teeth (in jaw), mane (beard, cream layers), crown (gold horns + brow helm), eyes | neck 2, head 2.2, jaw 2.2, mane 1.5, crown 1.5-2, eyes 1 | 13 / 15 (crown, eyes) | the mane can sway as a secondary part |
| front legs ×2 | upper, fore (glyph bracers), paw | 1.5-2 | 13 | 3-4 claws per paw; phase-2 look on fore and paw |
| hind legs ×2 | thigh, shin, foot | 1.5-2 | 13 | |
| tail | tail1 … tail7 (taper 1.3 → 0.38 b radius, 10 b) + tail tip spikes | 1.5 (1-4), 1.2 (5-7) | 13 | phase-3 look; whip tolerance 0.03 b |
| helpers | shadow (empty model, shadow_radius 4.5) | — | — | not a rig part |

The core list above is 37 parts. The options up to 44-48 give the "care" budget:
- tongue;
- separate claw groups per paw (grip and stomp);
- ear frills ×2;
- an extra mane layer;
- a back crystal row;
- phase-vein overlays as separate bright parts if the tint approach looks dull.

Plus 12 interaction hit proxies (§3.3), not counted against the render budget.

### 5.2 Textures

| area | density | example sprite |
|---|---|---|
| hide / rock scales | 32 px/b, tiled 64-128 px tiles via `lathe tile` or per-element tiles | `hide_a` 128², `hide_b` 128², `plate_dark` 64 × 128 |
| belly plates, mane | 32-48 px/b unique cards | `belly` 160 × 128, `mane` 192 × 192 |
| head (sides, top, jaw, teeth, eyes) | 48-64 px/b | `head_side` 208 × 112, `head_top` 192 × 176, `jaw` 192 × 96 |
| horns, crown, crystals | 48 px/b, cutout | `horn` 128 × 256, `crystal` 64 × 128 |
| bracers (glyph meander) | 48 px/b | `bracer` 160 × 96 |
| element veins | white 32-64 px, tinted by item definition | `vein_*` |

- Total **≤ 1.2 M px**: 0.8-1.0 M is realistic. All sides are multiples of 16, ≤ 512.
- Palette: the wiki's hex values (`S:az/src/wiki.md:38-39`).

### 5.3 Generator file layout and names

Mirror the fieldgen layout (`FG:tools/build_mboss_fieldgen_rig.mjs` + `fieldgen_{paint,geometry,pose,clips}.mjs`):

```
T:build_mboss_azhdaha_rig.mjs   entry: PARTS (budget check 48), UUIDs, RP write, compile, API, proxies, manifest
T:azhdaha_paint.mjs             sprites (mboss_paint_lib), azhdahaSprites() size table, atlas budget 1.2 M
T:azhdaha_geometry.mjs          partModels() with mboss_model_lib (checkBounds), look tints
T:azhdaha_pose.mjs              PART_SCALE, solve() FK (spine/neck/head/jaw, 4 legs with foot-plant IK, tail chain), toDisplay, proxy points
T:azhdaha_clips.mjs             DEFAULT_POSE, CLIPS (+ RETIME), events, hidden spans, px tracks
T:mboss_azhdaha_rig_api.md      contract for the pattern code (as mboss_fieldgen_rig_api.md)
T:mboss_azhdaha_rig_manifest.json
```

- Namespace `rlk:mboss/azhdaha/rig`.
- Objectives `azRigC/T/F/Y/Look/Px`.
- Tags `rlk_mb_azhdaha_part`, `rlk_mb_az_<part>`, `rlk_mb_px`, `rlk_mb_px_<part>`.
- UUID block `524c4b4d-415a-4400-8000-0000000000NN` ("AZ"; ints `[I;1380731725,1096434688,-2147483648,NN]`).
- Apep: `…-4150-4400-…` ("AP"; ints `[…,1095779328,…]`). Neither collides with BG/BF/FG or the probe's `415a-5000`.
- Debug poses `az_dbg/<clip>/<t>`.

Both chapter bosses run inside the mboss framework (hz, pj, aux, bars, `on_hit`/`incoming` hooks), with the chapter
economy flags from the registry (`T:mboss_registry.json` `_doc`: `goldMul` chapter boss ×15).

### 5.4 Shared-library and framework changes (small, back-compatible)

1. `T:mboss_rig_compile.mjs`:
   - per-part translation tolerance `tol.tp` (§2.8);
   - an optional `px` track compiler (offset storage at key ticks).

   Prove that the Guardian, butterfly and fieldgen outputs stay byte-identical, as the earlier lib moves did.
2. Rig builder options: culling `width/height` per rig (30 × 12 here), `view_range` 3, a shadow helper, per-state
   follow lists, the static-anchor follow skip.
3. Framework (`T:build_mboss_core.py` + 1-line edits in shared files):
   - `combat/apply` proxy line;
   - `mboss/px/hit` and `px/dup`;
   - `#atkSeq` increments (`melee_begin`, `clear_atkflags`, `element/core_*`, `element/dot`);
   - the body solidity push;
   - the Navia pellet-count redirect (§3.5).

   Rerun every mcsim suite (`S:mb2/tests/run_all.sh`, `S:mb3/tests`).

### 5.5 Build and render loop (verified for this study)

1. **Sandbox.** Copy the boss's tools (`*.mjs`) to a scratch dir and copy the needed RP textures into a scratch RP.
   Never build into the repo or a worktree.
2. **Build.** `node tools/build_mboss_azhdaha_rig.mjs --resourcepack <rp> --datapack <scratch dp> [--no-paint | --paint a,b] --debug-dp <dbg> --debug-clips <list|all>`.
   This writes the exact per-tick poses `az_dbg/<clip>/<t>` and rest poses, as fieldgen does (`FG:…:146-159, 346-353`).
3. **Render.**

   ```
   python3 -I S:az/understand/rigtech_render.py --dp <dbg> --rp <rp> \
       --spawn rlk:mboss/azhdaha/rig/spawn [player_ref] --apply rlk:az_dbg/<clip>/<t> \
       --views front,right,top,iso --light mc --floor --floor-half 14 -q -o out.jpg
   ```

   - It takes about 8 s for 31 displays.
   - `--strip a..b` gives filmstrips, `--track TAG:x,y,z` motion paths, and `--extent/--center` fixed framing.
   - Add a 0.6 × 1.8 b player reference (`W:tools/rigtech_probe.mjs` `player_ref`) for scale.
4. **Sheets.** Per-clip key-pose sheets against footage crops (as `S:mb3/animwork/tools/clipsheet.py`, `cmp.py`). Model
   critique sheets against `S:az/understand/motion/*.jpg` and the wiki portrait description. Save JPEG.
5. **Validators before any merge.**
   - `checkBounds`, step and segment errors, the atlas budget, the alignment rules (paws ≥ floor while visible, no root
     x/z travel, the tail-only mask, events inside clips).
   - Byte identity of the other rigs when shared libs change.
   - A proxy coverage run (`W:rigtech_cover.py` on the real rest boxes; target 100 % at R 3.0).

Renderer limits to keep in mind:
- no culling box or shadow emulation;
- translucent faces write no depth;
- score-gated lines need `--score`;
- the gone `S:mb/gw/tools/preview.py` flags (`--clean`) do not exist in `raiden_preview.py`.

### 5.6 Open questions for the planner

1. **Final size.** The probe is 22.9 b long and 7.5 b tall. Is the chapter arena radius (22-23 today) enough for the
   charge and burrow patterns? About 28-30 b is suggested.
2. **Proxies as the hit model.** Proxies need 4-5 one-line edits in shared combat files plus the Navia redirect; the
   alternative is the "nearest point" body with its projectile gaps.
3. **Body solidity push** for torso and head, as in Genshin, or allow walking through?
4. **Phase looks.** Tinted item definitions are enough; separate bright vein parts can be added if they look dull.
5. Who owns the Raiden atlas reclaim if both chapter bosses land while Raiden stays for chapter 2?
