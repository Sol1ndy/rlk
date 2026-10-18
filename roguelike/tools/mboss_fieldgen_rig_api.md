# Experimental Field Generator (실험성 역장 발생 장치 · 브레게 프로토타입) rig: API contract

This is the contract between the rig and the mid-boss module (`tools/mboss_fieldgen/`). The module reads clips,
events, form switches, hidden spans, parts, props and objectives from the manifest, so retimed keys reach it on the
next module build. The clip and event names are the ones the module's stub manifest
(`tools/mboss_fieldgen/stub_rig_manifest.json`) uses; every clip and event the module looks up exists here (§6).

Generator: `tools/build_mboss_fieldgen_rig.mjs`, with `fieldgen_paint.mjs` (textures), `fieldgen_geometry.mjs`
(item models), `fieldgen_pose.mjs` (the free-body pose solver and the seven form poses) and `fieldgen_clips.mjs`
(clips). It is built on the shared mid-boss libraries, as the Guardian and the butterfly are: `mboss_rig_math.mjs`,
`mboss_paint_lib.mjs`, `mboss_model_lib.mjs`, `mboss_rig_clips.mjs` and `mboss_rig_compile.mjs` (§9 lists the
generic extensions this rig added to `mboss_model_lib.mjs`).

```
node tools/build_mboss_fieldgen_rig.mjs --resourcepack <unpacked RP> [--datapack <dp>] [--no-paint | --paint a,b]
                                        [--debug-dp <scratch dir> [--debug-clips a,b | all]] [--allow-steps]
```

- It owns and rewrites `data/rlk/function/mboss/fieldgen/rig/**`. Never hand-edit those files.
- In the RP it writes:
  - `assets/rlk/textures/mboss/fieldgen/*.png` (106 sprites), registered in `assets/minecraft/atlases/items.json`;
  - `assets/rlk/models/item/mboss/fieldgen/*.json` (47 models, the two props included);
  - `assets/rlk/items/mboss/fieldgen/*.json`.
  Stale files of the three folders and stale atlas entries are removed.
- The manifest is `tools/mboss_fieldgen_rig_manifest.json`.
- `--paint a,b` repaints only the named sprites; `--no-paint` keeps the textures on disk.
- `--debug-dp <scratch dir>` writes the rest poses (`fg_dbg/rest_<form>`), the exact per-tick poses of the
  `--debug-clips` (`fg_dbg/<clip>/<t>`) and a link to the rig functions, for the offline renderer. It never writes
  into the real pack.

All functions below are `rlk:mboss/fieldgen/rig/...`. Unless a line says otherwise, **@s is the rig anchor** (the
boss body, on the floor under the ring axis). Call them `as` the anchor and `at` it.

## 1. Calls

| function | when | what |
|---|---|---|
| `init` | load (idempotent) | Adds the objectives (§7). |
| `spawn` | once, as/at the anchor | Kills old parts and summons the 29 parts at the anchor's position and yaw in the rest pose of the stored form (`fgRigForm`, cruise by default), queues that form's hold clip, re-applies the stored look and crack stage. |
| `tick` | **every game tick**, after the AI: `execute as <anchor> at @s run function rlk:mboss/fieldgen/rig/tick` | Respawns the parts if they are missing (the rig restarts in the stored form's hold clip). The parts follow the anchor position and yaw (`teleport_duration` 1). Advances the clip, applies its keys, model swaps and temporary looks, counts the flash down. |
| `play/<clip>` | any time | Starts `<clip>` from tick 0 at the next `tick` (the same game tick when `tick` runs later). The first key segment blends from the current pose over 3 t. |
| `kill` | cleanup | `kill @e[type=item_display,tag=rlk_mb_fieldgen_part]`. Props are separate (`prop/clear`). |
| `uninstall` | optional | `kill`, `prop/clear`, the face marker and the objectives. |
| `form/<dormant\|cruise\|field\|coreup\|tower\|laser\|deployed>` | instant | Stores the form (`fgRigForm` 1-7), snaps every part to that form's rest pose (§3) and queues its hold clip. For reloads, tests and respawns: the clips switch forms themselves (manifest `forms`). |
| `look/<idle\|charge\|field\|groggy\|off>` | state | Stores the look (`fgRigLook` 0-4) and swaps the look parts' models (§4). |
| `look_apply` | after a manual score change | Re-applies `fgRigLook` and `fgRigCrack`. |
| `crack/<0..4>` | 20-hit meter | Stores the bubble stage (`fgRigCrack`): 0 = hits 0-4, 1 = 5-9, 2 = 10-14, 3 = 15-19, 4 = the burst. The bubble shows only in the field look. |
| `flash` | on a body hit (optional) | Warm white outline (`Glowing`, `#FFF5DC`) on the solid parts for 3 t (`flash_tick`, `flash_off`). |
| `face/player` | as needed | Instant yaw toward the nearest non-spectator player. |
| `face/track` | each tick while tracking | Turns at most 4° per call toward the nearest player (a heavy device: 45-90° per second; yaws normalised into [-180°, 180°); temporary marker `rlk_mb_fg_face`). |
| `face/set {yaw:<deg>}` | macro | Sets the anchor yaw. |
| `prop/bomb`, `prop/missile` | patterns | Free props at the execution position and yaw (§5). |
| `prop/clear` | cleanup | Kills every prop (`rlk_mb_fg_prop`). |

Typical sequence (what the module core does): entrance = `init`, `spawn`, `form/dormant`, `look/off`,
`play/entrance`, then `look/idle` at `eye`; the field = `play/warp_out`, the warp (move the body) at `out`,
`play/warp_in_field` at the end of `warp_out`, `crack/0` + `look/field` at `unfold`; the break = `crack/4` +
`play/break`, then `groggy`, `recover` + `look/idle`, `crack/0`.

**Facing.** No clip yaws the whole body: the module turns the anchor (`face/*`). Every spinner inside a clip ends on
whole turns (§6), so nothing unwinds when a clip ends or a blend starts.

## 2. Entities, tags, cost

- 29 `item_display` parts (budget 32) with **fixed UUIDs** `524c4b4d-4647-4400-8000-0000000000NN`
  (int array `[I;1380731725,1179075584,-2147483648,NN]`), NN = 01..1d in the order below.
- Per tick: 29 `tp <uuid>` (follow) and the keys of the parts whose interpolation segment starts on that tick
  (binary dispatch on `fgRigC` / `fgRigT`; no selectors on the hot path, no macros).
- One rig at a time; a second `spawn` kills the first.
- Tags on every part: `rlk_room`, `rlk_mb_aux`, `rlk_mb_part`, `rlk_mb_fieldgen_part`, `rlk_mb_fg_<part>`.
  Alias tags for fx anchors: `rlk_mb_fg_pend` (on `pendulum`), `rlk_mb_fg_medal_e` (on `medal_eye`),
  `rlk_mb_fg_medal_g` (on `medal_gear`); the manifest lists them as `{name, tag, alias_of}`.
- `view_range` 3, `width`/`height` 16, block brightness 13-15 (sky 15). Every part is a free body: model.md §0
  (nothing is connected); unused parts sit at scale 0.

| NN | part | model (idle look) | scale | what |
|---|---|---|---|---|
| 01 | `ring` | ring | 2.4 | the open annulus (no spokes), 16 facets, D 7.0 b: cream crenellated band over bronze with the square-wave seam groove, the lower tier, one tooth per facet (wide / narrow), the back keystone pillar and bell, the dock posts at the ring ends, two top vents, 8 bomb ports under the tier |
| 02 | `ring_glow` | ring_glow_idle | 2.4 | the glowing square-wave seam and the port glows (idle / hot / off) |
| 03 | `hub_eye` | hub_shut | 1 | the front keystone: the iris (shut sunburst fan / open / hot) in its frame with the gold spike (down in cruise, up in core-up / tower) |
| 04 | `halo` | halo | 1.25 | the copper halo over the ring (violet `halo_v` in the field look) |
| 05 | `halo2` | halo2 | 1 | the thin gold inner glow ring under the halo (violet in the field look) |
| 06 | `core` | core | 1 | the plum sphere (28 bands, dark ledges), red pads and cream clamps, the Y bracket |
| 07 | `core_eye` | eye_idle | 1 | the core eye: a bronze tube with a toothed cream collar and the iris face (idle gold / charge white-gold / field red-orange / dim) |
| 08 | `core_arch` | core_arch | 1.1 | the vertical bronze gear ring with the dark-red lining and 8 cream clamps |
| 09 | `core_brim` | core_brim | 1.3 | the tilted grooved brim, the orbit wire and its gold bead |
| 0a | `core_glow` | glow_charge | 1 | clip-driven: the charge sphere / white-gold flash / the exposed gold sphere (scale 0 when unused) |
| 0b | `core_shell` | none | 1 | the field bubble at the crack stage (`bubble_0..3`, `bubble_burst`; empty outside the field look) |
| 0c, 0d | `spike_l`, `spike_r` | spike_l, spike_r | 1.4 | the end spikes: 8-facet gold lance, collar, X frame and lugs, docked at the ring ends |
| 0e | `medal_eye` | medal_eye | 1 | the eye medallion (glowing C face in a gold ring), device left |
| 0f | `medal_gear` | medal_gear | 1 | the toothed gear medallion, device right |
| 10-13 | `drill_fl`, `drill_fr`, `drill_bl`, `drill_br` | drill | 1 | the 4 drill pods under the ring (banded gold cones with crowns) |
| 14, 15 | `plate`, `plate2` | plate, plate2 | 1.25 | the gold brim plates under the core |
| 16 | `pendulum` | pendulum | 1.6 | the silver keyhole cog, the protractor arc with end caps and the gold dagger (plumb) |
| 17 | `pend_glow` | pend_glow | 1.6 | the violet Ousia flame on the cog (field) |
| 18, 19 | `beam_l`, `beam_r` | beam_gold | 1 | the medallion beams: gold laser / gold link beam (`beamLook`), length and width per clip |
| 1a | `column` | col_gold | 1 | the column from the core: gold tell / violet field column (`colLook`), up or down |
| 1b | `tower_col` | tower_col | 2 | the tower column (tower form) |
| 1c, 1d | `tower_t1`, `tower_t2` | tower_t1, tower_t2 | 1.3 / 1.4 | the two telescoped tier discs (the second one is the flame band) |

model.md's 28-part plan plus `core_shell`: the field bubble has its own part (its spare "second core glow shell"), so
the crack stages never fight the clip-driven `core_glow` (charge sphere, flash, gold sphere).

## 3. Forms

`form/<name>` snaps to the rest pose and queues the hold clip; the clips animate every change themselves. Heights are
the ring centre over the floor; the pendulum tip hangs 0.2-0.55 b over the floor in every form (melee can hit it).

| id | form | ring centre | hold clip | pose |
|---|---|---|---|---|
| 1 | `dormant` | 2.15 | `idle_dormant` | folded on the floor: halo and inner ring folded away, the core sunk with the arch flat, the pods tucked, only the dagger below |
| 2 | `cruise` | 4.5 | `idle_cruise` | compact: halo +1.6, the core tucked in the ring hole, medallions docked at the ring ends, pods under the ring, pendulum tip 0.55 b |
| 3 | `field` | 5.8 | `field_idle` | the stack spread: the core hangs 1.7 b under the ring, the medallions beside it on link beams, the pods at core level, plates round the violet column, the Ousia flame on the cog |
| 4 | `coreup` | 5.0 | `hold_coreup` | the core 2.8 b over the ring, the iris and both medallions in a row with their spikes up, roll 10° |
| 5 | `tower` | 4.5 | `hold_tower` | the column with two tiers telescoped up, the halo ×1.7 at +3.2, the medallions on top, the end spikes up 45°, the iris spike up |
| 6 | `laser` | 4.5 | `hold_laser` | the medallions dropped to r 2.8, 2 b under the ring, gold beams down-out at 48° (the hold clip counter-orbits them) |
| 7 | `deployed` | 5.6 | `hold_deployed` | the lances: spikes and medallions 5.6 b out on both sides, the core hanging |

Form switches inside clips (manifest `forms`, `{clip: [[tick, form], ...]}`; the module's hitbox / state may follow
them): `entrance` dormant 0 → cruise 110; `laser` laser 4 → cruise 175; `coreup` coreup 15 → cruise 128;
`tower_throw` tower 38 → cruise 157; `warp_in_field` field 17; `field_end` deployed 40 → cruise 96; `recover` cruise 15.

## 4. Looks and crack stages

- `fgRigLook`: 0 idle (default), 1 charge, 2 field, 3 groggy, 4 off. Look parts: `ring_glow`, `hub_eye`,
  `core_eye`, `halo`, `halo2`, `medal_eye`, `medal_gear` (+ `core_shell` in the field look).
  - **idle**: seam and ports idle gold, the iris shut (sunburst fan), the eye gold, copper halo + gold inner ring.
  - **charge**: seam, ports and bomb ports hot white-gold, the iris hot, the eye white-gold, the medallion faces hot.
  - **field**: seam hot, the iris open, the eye red-orange, both halos violet, the white-gold bubble round the core
    at the stored crack stage.
  - **groggy**: seam off, the iris shut, the eye dim amber. **off**: the same for dormant and death.
- Clips show temporary looks without touching `fgRigLook` (`look/temp_<look>`, `fgRigTmp` 1): the attacks go to
  charge for their tell and active part, `break` to groggy, `entrance` and `death` to off. When the temporary span
  ends the clip calls `look_apply`, so a look set by the module during the clip wins afterwards. A `look/<x>` call
  during a temporary span shows at once and clears `fgRigTmp`.
- `crack/<s>` swaps `core_shell` to `bubble_<s>` (stage 4 `bubble_burst`) when the field look is on, and stores the
  stage for later. The bubble: white-gold glass over the core with radial and ring cracks from several impact
  points; stages 1-3 add cracks and whiten the glass, stage 4 is the shattering flash. `break` flares the bubble
  (0-5), bursts it (5-7, scale 1 → 1.6 → 0) and brings the empty shell back at scale 1 for the next field.
- Clip-driven models (manifest `clip_models`): `core_glow` charge / flash / gold; `beam_l`, `beam_r` gold / link;
  `column` gold / violet.

## 5. Props (free `item_display`s, not rig parts)

Each call summons at the execution position, turned to the execution yaw. Tags: `rlk_room`, `rlk_mb_aux`,
`rlk_mb_fg_prop`, `rlk_mb_fg_prop_<kind>`, and for that call only `rlk_mb_fg_prop_new`. `tick` never moves them.

| function | display | notes |
|---|---|---|
| `prop/bomb` | `bomb` ×1 | A falling bomb: a 0.65 b dark bronze sphere with a gold band and a glowing seam. Summon at a port anchor, then `tp` it down with `teleport_duration`. |
| `prop/missile` | `missile` ×1 | A gold drill missile, 1.4 b, point down (−Y in its frame): turn it with its transformation or summon it rotated. |

## 6. Clips

Ticks at 20/s; events are clip ticks; `then` = the clip that follows by itself (`hold` = it holds its last pose).

**Body travel.** The rig follows the anchor; horizontal travel is the module's job (the bombing glide, the warp).
Every key of every clip has the root at x = z = 0 (the build fails otherwise). Heights, pitches and rolls, the stack
spacing and every part's own motion are in the clips.

**Spinners.** The halo (2.25°/t), inner ring (−4.5), brim (4.5), medallions (4.5 / −6.75), drill pods (11.25), tower
tiers and plates turn at rate channels. Per clip, each spinner's integrated angle is scaled to a whole number of
turns (manifest `spin_turns`), so every clip starts and ends with every spinner at its rest angle and no blend ever
unwinds a spin.

| clip | len | then | events |
|---|---|---|---|
| `idle_cruise` | 160 | loop | cruise hover: bob ±0.12 b, ±1.5° wobble, the arch tilted 35° and rocking ±20°, the pendulum lagging |
| `glide` | 40 | loop | travel: nose down 6°, the pendulum swung back |
| `field_idle` | 240 | loop | field hover: the pods orbit the core, the arch turns round it like a gyroscope |
| `idle_dormant`, `hold_coreup`, `hold_tower`, `hold_laser`, `hold_deployed` | 40 / 80 / 80 / 72 / 80 | loop | the form holds (`form/*` queues them); `hold_laser` counter-orbits the medallions at 5°/t |
| `entrance` | 130 | `idle_cruise` | clank 16, pods 24, unfold 30, eye 54, turn 60, rise 80, risen 110, face 115 |
| `bomb_run` | 58 | `idle_cruise` | turn 0, ports 10, run 12, end 56 |
| `slam` | 45 | `idle_cruise` | column 0, plunge 13, impact 16, rise 23 |
| `laser` | 175 | `idle_cruise` | drop 0, charge 4, aim 23, fire 25, off 158, retract 159 |
| `missiles` | 64 | `idle_cruise` | flare 0, vent 8, launch 22, last 35 |
| `coreup` | 130 | `idle_cruise` | spark 0, eye 1, rim 3, lift 5, up 16, beam 29, column 41, blast 48, sink 81 |
| `tower_throw` | 157 | `idle_cruise` | dip 0, vent 12, tower 20, band 38, burst 55, throw 95, revert 142 |
| `warp_out` | 34 | hold | flip 0, hide 12, out 13 |
| `warp_in_field` | 24 | `field_idle` | in 0, unfold 1, field 17, banner 22 |
| `wave` | 40 | `field_idle` | charge 0, beam 25, impact 25 |
| `wave_long` | 56 | `field_idle` | charge 0, beam 41, impact 41 |
| `wave_drop` | 84 | `field_idle` | charge 0, drop 36, land 40, beam 40, impact 40, lift 60, risen 80 |
| `field_erupt` | 40 | `field_idle` | activate 0, lock 12, erupt 22 |
| `frock` | 110 | `field_idle` | vent 0, flame 8, burst 25, throw 65, end 100 |
| `field_end` | 102 | `idle_cruise` | lift 0, rise 2, lances 20, horiz 40, pack 50, dock 72, packed 96 |
| `break` | 34 | `groggy` | bubble 0, burst 5, tilt 5, wobble 14, sink 34 |
| `groggy` | 160 | loop | the slump: ring centre 3.3 b, roll 25°, pitch 8°, halo slid, pendulum swinging ±12° |
| `recover` | 15 | `idle_cruise` | relevel 0, flip 6, done 15 |
| `death` | 110 | hold | flicker 0, drop 20, sink 40, land 60, out 70, gone 110 |

Notes per clip (the full text is each clip's manifest `note`):

- `entrance` (untargetable until `risen`): the clank, the pods drop and it lifts to 2.6 b (24-30); the halo, inner
  ring and core rise out of the hole and the plates and pendulum drop while it lifts to 3.0 b (30-48); the eye opens
  at 54 (call `look/idle` there); the arch turns (60-78); the rise to 4.5 b (80-110); settled by 115.
- `bomb_run`: nose down 18° (0-10, temporary charge look), the ports glow (10), the run 12-56 (the module glides the
  body and drops the bombs at `port_0..7`), level out (56-58) into the first pose of `slam`, which the module plays
  at 58 for the finisher.
- `slam`: the core turns face down and the gold column reaches the floor (0-13 tell), the plunge 4.5 → 2.3 b
  (13-16) with the stack compressed, impact 16, sit 7 t, rise 23-44.
- `laser`: the medallions drop to r 2.8 b, 2 b under the ring (0-4), the charge (4-23, medallions hot), the beams
  extend over 23-25 (48° from straight down), from `fire` they orbit at exactly 5°/t for 133 t, beams off at 158-160,
  retract and re-dock (159-175). **Hazard aim** (manifest `orbit`): at clip tick t in `from`..`to` (25..158) the eye
  medallion's beam is at azimuth `90 − 5(t − 25)` and the gear's at `−90 + 5(t − 25)` (azimuth = degrees round the
  ring axis from the device's front toward its left, +X); each beam runs from its medallion (r 2.8, 2.0 b under the
  ring) down-out at 48° to a floor spot at r `spot_r` = 5.58 b from the axis (ring centre 4.5 b). The two spots meet
  in front 18 t after `fire`, then every 36 t, back and front.
- `missiles`: the spike tips flare (0-8; fx at `spike_tip_l/r`), the eye turns up and the gold vent column rises
  (8-21), launches 22-35 from `vent_l` / `vent_r` (the module's missiles, `prop/missile`), back by 64.
- `coreup` (지면 충격): the eye out (1-4), gold flash and lift (5-15: the core to +2.8 b, roll 10°), the up-beam
  (29-40), the core drops back with the column down to the floor (41-44), blast 48, settle back (81-130).
- `tower_throw`: dip to 2.8 b with a 27° roll toward the player (0-12), vent column and the medallions flung out
  (12-20), the tower telescopes up (20-38), the flame band (38-55, module fx at `tower_top`), bursts from 55 every
  6 t, throws from 95 every 8 t, revert with a roll wobble (142-157).
- `warp_out` / `warp_in_field` (manifest `hidden`: `warp_out` [12, −1], `warp_in_field` [−1, 1]; −1 = the clip
  start or end): the halo flips upright while the device noses up 35° (0-11), the rig scales to 0 by 12 and stays
  hidden to the end of `warp_out` (it holds there until the module plays `warp_in_field`), so moving the body at
  `out` (13) is invisible. `warp_in_field` scales it back at the body's new spot (0-2, ring centre 5.8 b) and
  unfolds the field form (1-17), link beams and violet column at 17-21.
- `wave` / `wave_long` / `wave_drop` (「인력 충격파」): the charge sphere grows in 4 pulses (24 t / 40 t), the 1 t gold
  beam down and the burst flare at `impact` (the front leaves the axis then). `wave_drop` sinks during the charge and
  drops onto the floor (ring centre 2.4 b) at `land`, grounded 20 t, then rises.
- `field_erupt` (F1): the arch locks facing the front and the eye looks out (0-12), the eruption pulse at 22, back
  to the hover by 40; the module runs the eruption events on its own clock. `frock` is an optional F2 clip (vent
  column, flame band, bursts from 25, throws from 65).
- `field_end`: lift-off flash (0) and a 20 t rise to 6.2 b, the lances out (20-40), the pack-up roll and rock
  (50-72), the lances dock and the core swings up into the hole (72-96; call `look/idle` at 72 or earlier).
- `break`: call `crack/4` at 0 or at `burst`. The bubble flares and bursts (0-7), the whole device tilts 28° in 9 t
  (5-14), a damped wobble ±8° → 0 (14-34) while it sinks into the groggy slump.
- `recover`: re-level 6 t, the core flips to the top 9 t (the arch swings over), back to cruise.
- `death`: the seam flickers hot / off three times (0-18), the halo drops and rolls off, the pods stop and fall, the
  spikes droop, the ring tilts 30° and sinks until its low rim rests on the floor (20-60), the pendulum topples, the
  medallions clatter down; everything scales out (70-110). Call `kill` after 110.

**Anchors.** `anchors[event]` in each manifest clip entry (and `form_states.<form>.rest_anchors`) hold fx points in
rig coordinates, blocks from the anchor: x the device's left, y up, −z its front, so the body-frame position is
`^x ^y ^-z` (`execute as <anchor> at @s rotated ~ 0 positioned ^x ^y ^-z`). They include the clip's own heights,
tilts and rolls at that tick.

| anchor | where |
|---|---|
| `ring_centre`, `core`, `eye` | the ring centre, the core centre, the core eye's front |
| `spike_tip_l`, `spike_tip_r` | the end spike tips (flares) |
| `medal_e`, `medal_g` | the medallion faces (laser emitters: the beams start here) |
| `beam_spot_l`, `beam_spot_r` | the far ends of the beams (the floor spots while firing) |
| `col_end` | the end of the column (floor point of the slam / core-up column) |
| `vent_l`, `vent_r` | the two top vents on the band (missile launch points) |
| `port_0` .. `port_7` | the 8 bomb ports under the lower tier |
| `pend_tip` | the dagger tip |
| `tower_top` | the top of the tower column |

## 7. Manifest and objectives

- `parts`: `{name, uuid, tag, model, brightness, scale, elements}` per part, then the alias entries
  `{name, tag, alias_of}`.
- `clips`: `{id, name, len, loop, next, events, keyFiles, keys, note, anchors, forms?, hidden?, orbit?, spin_turns}`.
- `rig_forms` (the seven names), `forms` (`{clip: [[tick, form], ...]}`), `hidden` (`{clip: [hide, show]}`),
  `form_states` (per form its id, function, hold clip, ring centre, rest anchors).
- `looks`, `look_ids`, `look_models`, `crack` (objective, stages, part), `clip_models`, `props` (function, tag,
  displays, note), `objectives`, `textures`, `atlas_px`.

| objective | holder | meaning |
|---|---|---|
| `fgRigC` | anchor | current clip id |
| `fgRigT` | anchor | tick within the clip (−1 = queued by `play`) |
| `fgRigF` | anchor | hit flash countdown |
| `fgRigY` | fake players | `face/track` scratch |
| `fgRigForm` | anchor | stored form: 1 dormant, 2 cruise, 3 field, 4 core-up, 5 tower, 6 laser, 7 deployed |
| `fgRigLook` | anchor | stored look: 0 idle, 1 charge, 2 field, 3 groggy, 4 off |
| `fgRigCrack` | anchor | bubble crack stage 0-4 |
| `fgRigTmp` | anchor | 1 while a clip shows a temporary look |

## 8. Build checks and budgets

The generator refuses to write a rig that fails these (`--allow-steps` turns the clip checks into warnings):

- **Rotation per tick and per key:** no part turns more than 120° between two ticks or within one interpolation
  segment (blend-ins included); large one-tick steps are also solved at the half tick.
- **Alignment** (every tick of every clip): no horizontal root travel; while visible, the pendulum tip, the drill
  tips and the ring's low rim stay over the floor; every event and form switch inside its clip; form names valid.
- **Keys:** the first key at tick 0, the last at the clip length, `next` must name a clip.
- **Parts** ≤ 32; **item models** within −16..32 (single-axis element rotations, multiples of 22.5°).
- **Atlas:** ≤ 0.5 M px (now 106 sprites, 0.45 M px), every side ≤ 512 px and a multiple of 16.
- Compiled: 27 clips, 1595 key files, 9578 part keys; 47 item models with 4083 elements. A part gets a key only
  where the client's lerp/slerp would drift from the authored pose by more than 0.012 b, 0.25-2° (per part) or
  1.5 % scale.

## 9. The model

- One superset rig for the seven forms. Coordinates: +X the device's left, +Y up, −Z its front (the keystone iris
  side); the item models face −Z and the display transformations mirror Z. Right-side spike and medallion models
  are mirrored copies (no negative scales).
- **Proportions** (model.md): the open ring D = 7.0 b (6.9 b across the band's flat facets, 7.0 b over the facet
  corners and the teeth), the band 0.66 b tall and about 1.0 b with the toothed tier under it, the hole 5.25 b
  across, the core sphere 2.5 b across, spike tips ±5.33 b, the copper halo 3.1 b across at +1.6 b.
- **Construction:** lathes for every turned part (band, tiers, arch, eye tube, spike cones, drills, halo rings, tower
  tiers), annuli for the ring top and bottom faces and the toothed collars, facet-aligned boxes for teeth, posts,
  clamps, caps and the keystone; crossed cards for the dagger, beams, column and glows. All shading is baked into
  per-facet texture variants (four light levels by azimuth, key light from the front-left), so the models read the
  same under any block light.
- **Paint** (`fieldgen_paint.mjs`, palettes from model.md): cream stone blocks over warm bronze, white-gold and
  brass highlights, engraved square-wave grooves and keyline borders, dark-red linings, cream clamps, the plum sphere
  with dark ledges, the C-spiral medallion face, the sunburst iris, violet field halos and column.
- **Shared library extensions** (generic, in `mboss_model_lib.mjs`; the Guardian and butterfly outputs stay
  byte-identical): `lathe(..., {tile, inward, range, phase})` (u tiled per facet, faces turned inward for linings,
  a facet range for partial rings, an azimuth phase, per-facet texture functions) and `annulus(...)` (n segment
  quads that match the lathe facets, `stagger` offsets odd segments along the axis to avoid z-fighting, tile or wrap
  mapping).

## 10. Not in the rig (module / fx code)

- Particles, flashes, decals, hazards, the HUD meter and banner; screen effects; sounds (vanilla only).
- Moving the body (glide, warp) and the props (bombs falling, missiles, slabs).
