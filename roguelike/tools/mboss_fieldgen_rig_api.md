# Experimental Field Generator (실험성 역장 발생 장치 · 브레게 프로토타입) rig: API contract

This is the contract between the rig and the mid-boss module (`tools/mboss_fieldgen/`). The module reads clips,
events, form switches, hidden spans, parts, props and objectives from the manifest, so retimed keys reach it on the
next module build. The clip and event names are the ones the module's stub manifest
(`tools/mboss_fieldgen/stub_rig_manifest.json`) and the stage-2 specs (`mb3/spec`) use; every clip and event they
look up exists here (§6). The clips are authored from the footage (`mb3/understand/v1..v4.md`, `model.md` §5) on the
timelines of `mb3/plan.md`.

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
`play/entrance`, then `look/idle` at `eye`; C1 = `play/bomb_run`, then `play/slam` at its end (it also chains by
itself); the field = `play/warp_out`, the warp flash at `hide`, move the body at `out`, `play/warp_in_field` at the
end of `warp_out`, `crack/0` + `look/field` at `unfold`; F1 = `play/field_erupt`, then `play/field_idle` when the
pattern ends; the pack-up = `play/field_end`, `look/idle` at `dock`; the break = `play/break`, `crack/4` at `burst`,
then `groggy` + `look/groggy`, `recover` + `look/idle`, `crack/0`.

`form/<f>` and `play/<clip>` in the same tick (the core's `groggy/rig`, reloads): the clip's first keys overwrite the
form snap before the client sees it, so the clip blends from the visible pose without a pop.

**Facing.** No clip yaws the whole body: the module turns the anchor (`face/*`). Every spinner ends each clip on a
symmetry multiple and the looping / chaining clips snap it back invisibly (§6), so nothing unwinds when a clip ends.

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
them): `entrance` dormant 0 → cruise 94; `laser` laser 4 → cruise 165; `coreup` coreup 15 → cruise 120;
`tower_throw` tower 38 → cruise 150; `warp_in_field` field 17; `field_end` deployed 20 → cruise 70; `recover` cruise 15.

## 4. Looks and crack stages

- `fgRigLook`: 0 idle (default), 1 charge, 2 field, 3 groggy, 4 off. Look parts: `ring_glow`, `hub_eye`,
  `core_eye`, `halo`, `halo2`, `medal_eye`, `medal_gear` (+ `core_shell` in the field look).
  - **idle**: seam and ports idle gold, the iris shut (sunburst fan), the eye gold, copper halo + gold inner ring.
  - **charge**: seam, ports and bomb ports hot white-gold, the iris hot, the eye white-gold, the medallion faces hot.
  - **field**: seam hot, the iris open, the eye red-orange, both halos violet, the white-gold bubble round the core
    at the stored crack stage.
  - **groggy**: seam off, the iris shut, the eye dim amber. **off**: the same for dormant and death.
- Clips show temporary looks without touching `fgRigLook` (`look/temp_<look>`, `fgRigTmp` 1): the attacks go to
  charge for their tell and active part (`bomb_run` 10-57 and `slam` 0-22, `laser` 4-157, `missiles` 0-42,
  `coreup` 0-81, `tower_throw` 10-142), `break` to groggy from 8, `entrance` (0-60) and `death` to off; the field
  clips keep the stored look. When the temporary span
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

Ticks at 20/s; events are clip ticks; `then` = the clip that follows by itself (`loop`, or `hold` = it holds its
last pose). Hit and launch ticks are relative to the clip start. Read every tick from the manifest (`ev`,
`clip_len`), never hard-code one.

**Body travel.** The rig follows the anchor; horizontal travel and yaw are the module's job (the bombing glide, the
warp, `face/*`). Every tick of every clip has the root at x = z = 0 and no root yaw (the build fails otherwise).
Heights, pitches and rolls, the stack spacing and every part's own motion are in the clips.

**Authoring** (`fieldgen_clips.mjs`). Each clip is written as per-channel keys (a key moves only the channels it
names; `k(t, pose, ease, from)` starts the move at `from`), then baked to one pose per tick with overlays (the
hover bob and wobble, the arch rocking, link-beam pulses; exact formulas such as the laser orbit and the drill orbit)
and a simulated pendulum (a stiff damped pendulum, period about 26 t, driven by its hang point's acceleration from
the clip's heights and tilts and by a gentle visual drive where the clip knows the module's travel, soft-limited to
about 28°). Loops and the clips that end in a rest form meet their neighbours exactly (every hover term is 0 at the
loop start).

**Spinners.** halo 2.25°/t, inner ring −4.5, brim precession 4.5, eye medallion 4.5, gear medallion −6, drill pods
11.25, tower tiers ±2.25 (±4.5 in the C6 charge), plates 1.5, the arch gyroscope 3 in the field (0 in cruise). Per
clip each spinner's integrated angle is scaled to a whole number of its **symmetry steps** (manifest `spinners`:
halo 45°, inner ring 22.5°, drill pods 90°, gear medallion 180°, tower tiers 22.5° / 90°, the rest 360°; the
per-clip angle is `spin_deg`), so every clip ends each spinner on a pose that looks exactly like its rest angle and
the loops keep their rates (all exact in the 240 t loops). A clip that loops or chains also **snaps** those parts at
its last tick (`end_snap` lines: the same pose turned back by the symmetry multiple, interpolation 0, invisible), so
the next clip's first key continues each spin forward instead of unwinding it; `field_end` and `recover` snap the
arch they turn over by 180° (the ring's own symmetry) the same way. A clip started in the middle of another one
blends from wherever the spinners are (the first key segment, at least 3 t).

| clip | len | then | events | used for |
|---|---|---|---|---|
| `idle_cruise` | 240 | loop | | cruise hover; the end of every cruise clip |
| `glide` | 80 | loop | | the module's slow glides in / out |
| `entrance` | 110 | `idle_cruise` | clank 16, pods 20, unfold 30, eye 60, turn 60, rise 64, **risen 94**, face 99, settled 110 | the intro (untargetable until `risen`) |
| `bomb_run` | 57 | **`slam`** | turn 0, **ports 10**, **run 12**, drop 12, end 57 | C1 일점 상쇄, the run (then the finisher) |
| `slam` | 37 | `idle_cruise` | column 0, plunge 13, slam 17, **impact 17**, rise 22, risen 37 | C2 내려찍기, and the C1 finisher at 57 |
| `laser` | 165 | `idle_cruise` | dock 0, drop 0, charge 4, aim 20, **fire 22**, off 155, retract 155, end 165 | C3 코어 (manifest `orbit`) |
| `missiles` | 60 | `idle_cruise` | flare 0, tell 0, **vent 8**, **launch 23**, last 37, end 60 | C4 바위 폭탄 |
| `coreup` | 130 | `idle_cruise` | spark 0, eye 1, **rim 3**, lift 5, up 15, beam 29, column 41, **blast 48**, sink 81, end 130 | C5 지면 충격 |
| `tower_throw` | 155 | `idle_cruise` | dip 0, flare 12, vent 12, tower 20, band 38, charge 38, **burst 55**, burst_last 97, **throw 100**, throw_last 132, revert 140, end 155 | C6 파쇄 (manifest `bursts`, `throws`) |
| `warp_out` | 34 | hold | flip 0, **hide 12**, **out 13**, end 34 | field opener, part 1 (hidden from 12) |
| `warp_in_field` | 40 | `field_idle` | in 0, **unfold 1**, field 17, links 17, **banner 22**, settled 40 | field opener, part 2 |
| `wave` | 40 | `field_idle` | charge 0, beam 23, burst 24, **impact 24**, end 40 | 「인력 충격파」 (24 t charge) |
| `wave_long` | 56 | `field_idle` | charge 0, beam 39, burst 40, **impact 40**, end 56 | the opening third wave (40 t charge) |
| `wave_drop` | 84 | `field_idle` | charge 0, beam 39, burst 40, **impact 40**, drop 40, land 44, lift 63, risen 83, end 84 | the closing third wave (drops onto the floor) |
| `field_idle` | 240 | loop | | field hover; the end of every field clip |
| `field_erupt` | 22 | **`field_active`** | activate 0, lock 12, **erupt 22** | F1 감소 영역 activation |
| `field_active` | 240 | loop | | the activated hover after `field_erupt` |
| `frock` | 110 | `field_idle` | vent 0, flame 8, **burst 25**, burst_last 67, **throw 65**, throw_last 97, **end 100** | F2 파쇄 in the field form (manifest `bursts`, `throws`) |
| `field_end` | 70 | `idle_cruise` | lift 0, rise 2, **lances 20**, **horiz 32**, **pack 40**, **dock 58**, **packed 70** | the unbroken field's pack-up |
| `break` | 40 | `groggy` | bubble 0, **burst 5**, tilt 5, **wobble 14**, sink 14, slumped 40 | 역장 붕괴 (the 20th hit) |
| `break_low` | 40 | `groggy` | the same as `break` | 역장 붕괴 while the closing `wave_drop` has the device on the floor (module fix round FID-1) |
| `groggy` | 160 | loop | | the 200 t groggy |
| `recover` | 15 | `idle_cruise` | relevel 0, **flip 6**, done 15 | back to cruise |
| `death` | 110 | hold | flicker 0, **drop 20**, **sink 40**, land 62, **out 80**, gone 110 | death (call `kill` after 110) |
| `idle_dormant`, `hold_coreup`, `hold_tower`, `hold_laser`, `hold_deployed` | 40 / 80 / 80 / 72 / 80 | loop | | the form holds (`form/*` queues them) |

Bold events are the ones the module core and the stage-2 specs read today (`mb3/spec`). Form switches (manifest
`forms`): `entrance` dormant 0 → cruise 94; `laser` laser 4 → cruise 165; `coreup` coreup 15 → cruise 120;
`tower_throw` tower 38 → cruise 150; `warp_in_field` field 17; `field_end` deployed 20 → cruise 70; `recover`
cruise 15. Hidden spans (manifest `hidden`, −1 = the clip start or end): `warp_out` [12, −1], `warp_in_field` [−1, 1].

### 6.1 Per clip

- **`entrance`** (v1 0.0-5.5 s; plan: untargetable until about t94). Folded at ring centre 2.15 b (temporary off
  look), the clank jolt (16), a gold flare at the hub (20-29), the pods drop and spin up (20-30), the halo and the
  inner ring rise out of the hole and the core drum grows on top while the ring lifts to 2.8 b with the plate and the
  pendulum hanging under it, the dagger near the floor (30-50). The eye opens at 60: call `look/idle` there (the
  clip ends its temporary off look at 60). The arch turns from flat to its 35° tilt and the eye swings from up to the
  front (60-78), the rise 2.8 → 4.5 b (64-94, eased) with the stack spreading as it leaves the floor, an overshoot and
  settle (94-110). Turn the body to the player from `risen` (`face/track`; footage +99..110).
- **C1 = `bomb_run` + `slam`** (v1 5.75-10.6 s). `bomb_run` chains into `slam` at 57 by itself and the module plays
  `slam` on the same tick (the same result), so on the pattern clock: turn and nose down 16° while rising to 4.8 b
  0-10, ports glow 10-12 (temporary charge look), the run 12-57 (glide the body about 0.55 b/t, bombs from
  `port_0..7`), level out 48-57; then the column 57-70, the plunge 70-74, the slam **74** (= 57 + `impact`), the rise
  74-94.
- **`slam`** (C2, and the finisher). The eye turns face down, the arch flat, the core sinks 0.35 b (0-4), the gold
  column reaches the floor (4-8) and holds while the device lifts 0.25 b (8-13), the plunge to ring centre 2.1 b
  (13-17, ease in), the slam at 17 (r 5), a bounce and sit (17-22), the rise to 4.5 b (22-37). Charge look 0-22.
- **`laser`** (C3, v1 13.9-22.6 s). The medallions drop from the docks to r 2.8 b, 2 b under the ring, beside the
  core (0-4), the charge (4-22, charge look, the medallions tremble), thin aim lines (20), fire at 22 with a width
  bloom 0.5 → 1.0 b (22-25), 133 t of counter-orbit at exactly 5°/t, the width back to 0.5 (148-155), beams off
  (155-157), the medallions rise back into the docks finishing their second turn (155-165). **Hazard aim** (manifest
  `orbit` {from 22, to 155, rate 5, medal_eye {az0 90, sense −1}, medal_gear {az0 −90, sense +1}, beam {from_down
  48, length 3.74, spot_r 5.58}}): at clip tick t in 22..155 the eye medallion is at azimuth `90 − 5(t − 22)` and the
  gear at `−90 + 5(t − 22)` (azimuth = degrees round the ring axis from the device front toward its **left**, +x; in
  MC yaw terms yaw = body yaw − az). Each beam runs from its medallion (r 2.8, 2.0 b under the ring centre) radially
  down-out at 48° from vertical to a floor spot at r 5.58 b. The spots start at the sides, meet in front 18 t after
  `fire`, then every 36 t (back, front, …). Do not yaw the body during the clip.
- **`missiles`** (C4, v1 25.7-29.3 s). The spikes tip up 10° and tremble while their tips flare (0-8; fx at
  `spike_tip_l/r`), the eye turns up, the arch lies flat and the gold vent column rises 6 b from the core, lifting the
  halo (8-12), held and flickering (12-23), ten launches 23-37 from `vent_l` / `vent_r` with a recoil sag, the column
  drops away (38-41), back to cruise by 60. Charge look 0-42.
- **`coreup`** (C5, v4 2.55-6.5 s; model.md §5.3). The spark (0), the arch upright and the eye out (1-4), the gold
  flash (5-8, `core_glow` 0 → 1.6 → 1.1), the lift (6-15): the exposed gold sphere rises 2.8 b over the ring, the device rises to 5.0 b and rolls
  10°, the spikes roll vertical, the medallions slide to the ring ends facing out and the iris spike flips up; hold
  (15-28), the up-beam (28-40, gold column up 6 b), the core drops back to +0.6 b and the column goes down to the floor
  (41-44), the blast at 48 (a recoil jolt), hold (49-81), the return with a roll rock (81-130).
- **`tower_throw`** (C6, v3 17.0-24.85 s). The dip toward the player to ring centre 2.9 b, nose down 24° and rolled 8°
  (0-12), the vent: column up and the medallions flung up and out to ±5.5 b (12-20), the rise and level while the tower
  telescopes up (20-38; the medallions dock on the column top by 36), the flame band charge (38-55; the tiers
  counter-rotate at 4.5°/t), eight bursts at manifest `bursts` 55, 61, …, 97 (a dip and a tier pulse each), five
  throws at `throws` 100, 108, …, 132 (a roll twitch each), the revert: the tower folds and a roll wobble −18 → 9 → 0
  (140-155). Charge look 10-142.
- **`warp_out` / `warp_in_field`** (v1 31.85-34.4 s). The halo flips upright and spins like a wheel while the device
  pitches nose up 35° (0-11), the rig scales to 0 in 1 t (11-12); flash at `hide` 12, move the body at `out` 13; it
  holds hidden until the module plays `warp_in_field` at 34. `warp_in_field` flashes in (0-2, ring centre 5.8 b) and
  unfolds like a spring (1-17: the core drops and hangs, plates and pendulum spread, pods to core level, medallions
  out, the gyroscope starts; overshoot at 12), the link beams and the violet column appear (17-21), settle (21-40).
  Call `crack/0` + `look/field` at `unfold`.
- **`wave` / `wave_long`**: the charge sphere (`core_glow` charge) grows round the core to scale 1.5 in four pulses (24 / 40 t), the 1 t
  gold beam from the core to the floor at `beam`, the burst at `impact` (the front starts), a 0.16 b recoil lift.
  **`wave_drop`**: the 40 t charge sinks the device 0.5 b, the burst at 40, then it drops onto the floor (40-44:
  ring centre 2.4 b, the core resting on the floor), grounded to 63, the lift-off flash at `lift` 63 and the rise.
- **`field_erupt` → `field_active`** (F1, v3 2.2-3.3 s). The gyroscope arch slows and locks facing the front, the
  eye looks out, the device rises 0.15 b (0-12), the medallions slide out to r 4.2 b on brightening link beams and
  the core flashes gold (12-22). It then loops in `field_active` (arch locked, bright pulsing links) until the module
  plays another clip: **play `field_idle` when the pattern is over** (the footage's gyroscope spins again when the
  beams go off).
- **`frock`** (F2). The arch locks, the gold vent column up 4 b with a roll (0-12), back to the violet column, the
  flame band (8-25, fx), eight bursts at `bursts` 25..67 (dips), five throws at `throws` 65..97 (roll twitches), `end`
  100, back to the field hover by 110.
- **`field_end`** (v2 26.3-31.3 s). The lift-off flash and the rise to 6.3 b (0-20) while the links and the violet
  column go out, the spikes turn spike-down in their docks, the lances move out to 5.6 b with the medallions in their
  X frames (20-28), turn horizontal (32-40, the deployed form), the pack-up roll 24 → −15 → 8° while the core swings
  up to the top (40-55), the lances dock and the pods tuck (50-62), settle to 4.5 b (55-70). Call `look/idle` at
  `dock` (58), so the violet fades with the pack.
- **`break`** (v2 11.9-14.95 s). Call `crack/4` at `burst` (5). The bubble flares with the core (0-5), bursts (5-7,
  scale 1 → 1.6 → 0), the links, the violet column and the Ousia flame go out, the seam goes dark (temporary groggy
  look from 8), the device tilts 28° in 9 t (5-14), a damped wobble ±8° → 0 (14-34) while it sinks to the groggy slump
  (14-40). Then `groggy` (call `look/groggy`).
- **`break_low`** (module fix round FID-1): the break when the 20th hit lands while the closing `wave_drop` has the device
  on the floor or low in its rise (the module plays it instead of `break`; same length and events, so the module's break
  clock is unchanged). It starts from `wave_drop`'s grounded pose (ring centre 2.4 b, the core resting on the floor at
  1.3 b, the stack compressed), so nothing jumps up to the hover first: the bubble flares (0-5) and bursts (5-7) at the
  grounded core, the links go out and the seam goes dark (temporary groggy look from 8), the pods tuck (4-12) and the
  device heaves up to 3.1 b while it tilts 21° (5-14), a damped wobble ±4° → 0 (14-34) while it settles into the groggy
  slump at 3.3 b (14-40). The smaller tilt and wobble keep the low spike tip over the floor.
- **`groggy`**: ring centre 3.3 b, roll 25°, pitch 8°, a slow ±3° wobble, the core sunk with the arch upright, the
  halo slid and tilted, pods at a quarter speed, the pendulum swinging ±12°. **`recover`**: re-level and rise (0-6),
  the core flips to the top while the arch turns 180° over (6-15); call `look/idle` at 0.
- **`death`**: the seam flickers three times (0-16), every spinner stops (14-20), the halo slides off the low side
  and lands flat on the floor, the pods drop, the spikes droop, the ring tilts 40° and sinks onto its low rim (ring
  centre 3.0 b; 26-60) with a bounce (60-67), the pendulum topples, the medallions clatter down; everything scales out
  (80-110). It holds there; call `kill` after 110.

### 6.2 Changes from the first rig (0f7c0e8)

| clip | was | now |
|---|---|---|
| `entrance` | 130: pods 24, eye 54, rise 80, risen 110, face 115 | 110: pods 20, eye 60, rise 64, risen 94, face 99 |
| `bomb_run` | 58 → `idle_cruise`, end 56 | 57 → `slam`, end 57 |
| `slam` | 45: impact 16, rise 23 | 37: impact 17, rise 22, risen 37 |
| `laser` | 175: aim 23, fire 25, off 158, `orbit` 25-158 | 165: aim 20, fire 22, off 155, `orbit` 22-155 |
| `missiles` | 64: launch 22, last 35 | 60: launch 23, last 37 |
| `coreup` | up 16, cruise form at 128 | up 15, cruise form at 120 |
| `tower_throw` | 157: throw 95, revert 142 | 155: throw 100, revert 140 (+ `bursts`, `throws`) |
| `warp_in_field` | 24 | 40 (events unchanged) |
| `wave` / `wave_long` | impact 25 / 41 | impact 24 / 40 (+ `burst`) |
| `wave_drop` | drop 36, land 40, lift 60, risen 80 | burst 40, then drop 40, land 44, lift 63, risen 83 |
| `field_erupt` | 40 → `field_idle` | 22 → `field_active` (new loop) |
| `field_end` | 102: horiz 40, pack 50, dock 72, packed 96 | 70: horiz 32, pack 40, dock 58, packed 70 |
| `break` | 34 | 40 (burst 5, wobble 14 unchanged) |
| `death` | land 60, out 70 | land 62, out 80 |
| `idle_cruise` / `glide` | 160 / 40 | 240 / 80 |

Unchanged: `frock` (burst 25, throw 65, end 100), `warp_out`, `recover`, `groggy`.

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
- `clips`: `{id, name, len, loop, next, events, keyFiles, keys, note, anchors, forms?, hidden?, orbit?, bursts?,
  throws?, spin_deg, end_snap}`: `orbit` (laser) the beam azimuths, `bursts` / `throws` (`tower_throw`, `frock`) the
  clip ticks of every burst dip and throw twitch, `spin_deg` each spinner's angle over the clip (a multiple of its
  symmetry step), `end_snap` the number of parts snapped at the last tick (§6).
- `spinners`: `rates` (degrees per tick in the cruise pose) and `symmetry_deg` (the step each spinner ends on).
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
  tips, the spike tips, the ring's low rim and the core sphere stay over the floor, the medallion centres at least
  0.45 b and the halo centre 0.2 b over it; every event and form switch inside its clip; form names valid.
- **Keys:** the first key at tick 0, the last at the clip length, `next` must name a clip.
- **Parts** ≤ 32; **item models** within −16..32 (single-axis element rotations, multiples of 22.5°).
- **Atlas:** ≤ 0.5 M px (now 106 sprites, 0.45 M px), every side ≤ 512 px and a multiple of 16.
- Compiled: 29 clips, 1975 key files, 14898 part keys; 47 item models with 4083 elements. A part gets a key only
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
