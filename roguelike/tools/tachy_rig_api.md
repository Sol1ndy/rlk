# 타키 (Tachy) rig: API (stage S2)

The display-entity rig of the special boss 타키 (Stellar Blade's Tachy) and the contract between the rig and the module
(`tools/mboss_tachy/*`, S3 / S4). Binding inputs: `S:tk/PLAN.md` §2-3, `S:tk/contract.md` §3.2, the frozen table
`tools/mboss_tachy/api.py` §7 (parts, looks, calls, clips). The model and every clip are read from the footage
(`S:tk/ref/*`, `S:tk/src/v1-v11.mp4`); the clip table below names the source of each.

## 0. Files

```
node tools/build_tachy_rig.mjs --resourcepack <unpacked RP> [--datapack <dp>] [--no-paint] [--allow-steps]
     [--debug-dp <scratch dir> [--debug-clips a,b | all] [--debug-step N]]
```

| file | owns |
|---|---|
| `build_tachy_rig.mjs` | the build: models / items / sprites / atlas, the two-pass clip solve, the compile (per-part key segments, form guards, snaps), the checks, the API functions, the cables prop, the manifest, the debug pack |
| `tachy_geometry.mjs` | the 40 parts (name, default model, brightness, display scale), every item model (blocks, A-frame, `toUnits`), the look -> model tables, tinted items |
| `tachy_materials.mjs` | the palette read from the footage and the tile sprites (carbon twill, gunmetal panels, hex plates, hazard yellow, gold, copper gloss, visor glass, hair, flesh, steel) |
| `tachy_paint.mjs` | the unique sprites (face, hair cards, the yellow tie fronts with the 3x3 light grid, ring light, cape panels, blade-feather wings + abyss flesh, tendril, blade flats, edge / skull / grid glows; the pyro and electro edges are 4-frame animations) |
| `tachy_pose.mjs` | the skeleton and `solve(pose, form)`: torso FK, IK legs (planted feet), IK arms (the sword grip / free targets / hand plants), the blade in its cutting plane, wings / cape per form (spread, flare, wrap), tendrils, hair (lag, gravity, floor), the floor guards, the root lift |
| `tachy_clips.mjs` | `DEFAULT_POSE` (the P1 stance) and the 41 clips (keys, look events, form switches, cable snaps) |
| `mboss_tachy/seq.py` | the sequences intro / death / t1 / t2 (written by S3's generator into `seq/**`) |

Generated (never hand-edit): `data/rlk/function/boss/tachy/rig/**`, `tools/tachy_rig_manifest.json`, the RP's
`assets/rlk/{textures,models/item,items}/mboss/tachy/**` and the items-atlas entries `rlk:mboss/tachy/*`. The shared RIGLIB
(`mboss_rig_compile`, `mboss_rig_clips`, `mboss_rig_math`, `mboss_model_lib`, `mboss_shape_lib`, `mboss_paint_lib`) is
used unchanged.

## 1. Calls (all `rlk:boss/tachy/rig/…`; @s = the body = the anchor, at its feet)

| function | what |
|---|---|
| `init` | objectives `tkRig*` (safe on every load) |
| `spawn` | kills old parts, summons the 40 parts + the shadow in the rest pose, re-applies the stored form and looks, queues `idle` |
| `tick` | once per game tick, after the module logic: respawns missing parts, follows the anchor (position + yaw; static skip), the hit flash, the clip step. Hidden: only the follow until a clip is queued |
| `play/<clip>` | the clip's tick 0 at the next `tick` (event *e* shows on the *e*-th tick after the call, counting that first one as 0) |
| `start/<clip>` | tick 0 now |
| `face/player`, `face/track` (≤ 12°/call), `face/set {yaw}` | anchor yaw; the parts take it every tick |
| `look/form/{cape,winged,abyss}` | the wing models (cape panels / blade feathers / + dark red flesh), tendrils shown in `abyss`; the wings and tendrils ease (4 t) to the form's rest pose until the next clip key |
| `look/visor/{up_off,down_pyro,down_electro,down_abyss,down_off}` | the skull glow inside the visor (pyro #FFB21E, electro #FFF0A0, abyss #FF3A2A); the helmet's position is keyed by the clips (up as a hood only in `intro` 0-126) |
| `look/edge/{off,yellow,pyro,electro,glint}` | the blade-edge glow (pyro: animated flames, electro: animated arcs) |
| `look/chest/{off,amber,red,gold}` | the 3x3 light grid on the sternum |
| `look/hands/{open,grip,fist}` | both hands (clips key their own hands) |
| `state/hidden` | every part scale 0 in place (never moved, never below the floor); `state/normal` (from hidden) restarts the current clip so its keys show the rig, and does nothing when the rig is already visible (S4's cancels call it) |
| `flash` | hit feedback: white-gold outline 3 t (`flash_tick`, `flash_off` internal) |
| `prop/cables` | the intro cables (6 strands × 3 segments, item displays `rlk:mboss/tachy/cable`) from 25 b up (the lamp machine, `tk_lift` y 226) to her hang pose; the intro clip recoils them at its snap ticks |
| `prop/clear` | removes every rig prop (`rlk_tk_prop`) |
| `kill` / `uninstall` | the parts and the shadow / + props, the face marker and the objectives |

Stored looks: `tkRigForm` (0 cape, 1 winged, 2 abyss), `tkRigV` / `tkRigE` / `tkRigG` / `tkRigH` = the index in
`api.LOOKS`. Clips may show a look for a moment (`lk/<channel>/<value>`, internal) and put the stored one back
(`lk/<channel>/restore`): A1 / B3 / C3 chest red + visor red tell, C / K glint, B2 glint during the raise, W1 yellow charge,
nova chest gold, T1 chest gold, T2 red visor. Clips that set a stored look: `intro` (visor up_off -> down_pyro at 136, chest
amber at 136, edge off -> yellow at 147 -> pyro at 156), `swap_pyro` / `swap_electro` (edge + visor at 14), `death` (visor /
chest off at 50, edge off at 70), `t1_wings` (form winged at 10), `t2_abyss` (form abyss at 60).

## 2. Entities

40 item displays `524c4b4d-544b-4900-8000-0000000000NN` (NN = `api.PARTS` index), the shadow `…40` (radius 1.1).
Tags: parts `rlk_room rlk_mb_aux rlk_mb_part rlk_tk_part rlk_tk_<part>`, shadow `rlk_room rlk_mb_aux rlk_tk_part
rlk_tk_shadow`, cables `rlk_room rlk_mb_aux rlk_tk_prop rlk_tk_prop_cables rlk_tk_cbl_<strand>_<segment>`. Culling 8 × 10
(the plan's 8 × 6 cannot hold the intro hang 7 b above the anchor), view range 2, billboard fixed, brightness 13 (14 the
left pauldron, 15 the glows, 12 the tendrils).

## 3. Model (PLAN §2.1-2.3, footage ref/model_a.jpg, fx_a.jpg, v2 6-16, v8 6.2, v9 1.5)

2.25 b to the helmet top (×1.25 the player); pelvis 1.10, shoulders 1.71, knees 0.55. Black carbon-twill suit, gunmetal
plates with bevelled panel lines, the yellow tie (straps from the collar to the sternum, a strip to the crotch) with the
3x3 light sockets, silver hex plates on her left flank / collar / pack / pauldron, the massive right hex pauldron with two
yellow bands and a ring light, the bulky right gauntlet (yellow band, two orange ring lights), the slim left arm, knee
guards with orange ring lights, yellow thigh band (right), the copper-red glossy helmet dome with the dark visor glass, a
gold rim and temple ring lights, the glowing skull inside, a pale face with dark brows and red lips under a parted fringe,
long dark ash-brown hair (3 locks down the back, lagging 3 t). The long sword: grip 0.34 with gold bands, the round guard
disc with the orange ring light, a 1.9 b blade with the serrated spine and the yellow edge band, the edge glow card.

Forms: `cape` = the folded wings as a long bronze-gold feather-plate cape (3 panels a side, flutter 40 t, streams back
with `wF`), `winged` = 3 blade-feather segments a side (0.95 / 0.95 / 0.80, resting 95 % spread behind her, flap, wrap
into a feather cloak), `abyss` = the same with dark red flesh + the two tendrils. The sheath: in the intro the sword sits
in a sheath rising from her right hip across the back under the cape (the hilt at the hip); after the draw only a short
holster remains (the fight footage shows no scabbard; PLAN §2.1's permanent 2 b diagonal scabbard was dropped).

## 4. Clips (contract table; events = played ticks)

| clip | len | form | footage | notes |
|---|---|---|---|---|
| `idle` | 40 loop | any | v8 0-3, v7 0.4 | stance: weight back, blade low right, tip near the floor |
| `walk` / `strafe_l` / `strafe_r` | 24 / 20 / 20 loop | any | v6, v8 prowl | planted feet, the anchor moves; step1 0, step2 12 |
| `backstep` | 12 | any | v3 / v4 | hop back, land 10 |
| `flinch` / `stagger` / `stun` | 6 / 50 (loop 10-50) / 120 | any | v10 3.6, v11 | `stun`: the hold span 20-100 is not looped (G2's stun is the clip's 120 t); rise 100 |
| `swap_pyro` / `swap_electro` | 24 | any | v6 / v7 | blade dragged on the floor (6), flung up vertical, the element takes (14) |
| `blink_out` / `blink_in` | 8 / 10 | any | v4 29.6, 36.4 | scale to 0 by 6 / from 0 |
| `leap_up` / `hover` / `dive` / `land` | 16 / 40 loop / 12 / 16 | any | v3 29-35, v4 13 | the anchor rises / falls (module); dive: pitched forward, blade down; impact 10 |
| `leap_high` / `hover_high` | 16 / 40 loop | any | v4 5.8-12 | |
| `a1_dash` | 34 | any | v8 4.0-4.4 | coil low (red tell 0-20), launch 16, the slash crosses her front at 20 |
| `b1_wrap2` | 50 | winged | v5 5.8-8.5 | feather cloak 0-22, snaps open 22, horizontal 24, rising diagonal 40 |
| `b2_side4` | 78 | any | v5 18-30 | hop with the blade hidden behind, lunge diagonal 22, two-handed overhead 44, sweeps 54 / 64 |
| `b3_six` | 112 | abyss | v5 30.4-40 | red charge, dash-in, fire arc 40, backhand 50, 60, three two-handed chops 76 / 88 / 100 |
| `c1_combo` | 92 | any | v6 14-22 | diagonal 14, a full spin 26-37 (hit 32), 46, two-handed diagonal 58, glint 68, thrust 86 |
| `c2_combo` / `c3_combo` | 74 / 104 | any / abyss | v7 0-6 / 9.6-15 | |
| `k_hold` / `k_glint` / `k_leap` / `k_plunge` | 20 loop / 18 / 14 / 20 | any | v4 29.6-40, v6 0-6 | wings spread, blade low; glint 0 / thrust 16; up 8; plunge hit 16 |
| `w1_wave` | 88 | any | v3 9.6-28 | blade level to her right, charging (yellow edge 6-46), sweeps 46 / 58 / 70 |
| `w2_air` / `w2_dive` | 66 / 16 | winged | v3 29-35, v4 0-3.2 | three air chops 14 / 28 / 42, pull back 46-66; the dive slash 10 |
| `l_shock` | 20 | any | v4 13.5-14.5 | crouched over the two-handed blade, the burst 10 |
| `mantle_in` / `_hold` / `_break` / `_nova` | 24 / 40 loop / 40 / 44 | any | | wings / cape wrap round her (12), float (20); crack 0, fall to a knee 20; swell, flash 40 |
| `intro` | 184 | cape | v1 0-19, v2 1.6-16.5 | hang 7 b up in the cables (0-30), snaps 30 / 33 / 36, falls, prone 42-60, hands and knees 84, rises 108, cape flare, hair sweep 116-126, visor closes 126-136, skull 136, draw 142-156, ignite 156, stance 170-184 |
| `t1_wings` | 80 | cape | v9 0-4.8 | kneel, model swap at split 10 (a 0-tick snap under the ember burst), spread 30, flare 50, stand 70 |
| `t2_abyss` | 110 | winged | v10 3.6-6.4 | stagger, red visor 20-90, tendrils grow 36-46 (abyss from 36), dark 50, the wing models swap at 60, rise 90 |
| `death` | 130 | any | v11 32-39 | knee 20, sword planted 36, visor off 50, wings sag 70, collapse 100, shrink to the floor 116-130 |

S4's use (`S:tk/requests/s4.md`): `l_shock` is played at the dive's `impact` (10) and blends from the impact crouch;
K / W1 hide the rig with `state/hidden` while gone; S4 stores `look/edge/glint` / `yellow` itself, so the clips' temporary
glint / yellow and their restore agree with it; the anchor carries her through the air (k_leap / k_plunge, hover, dives).

Swings: the blade is keyed as an angle in its cutting plane (`tachy_pose.mjs`), so every cut sweeps on an arc through her
front at its event; the grip turns about the shoulder. Big swings carry dense keys (two-handed chops: a mid key 2 t
before the hit); the compiler keys every part wherever the client's lerp / slerp would leave the solved pose by more
than the tolerance, so no swing reads as a poke.

## 5. Build checks and budgets

Strict by default (`--allow-steps` warns instead): the contract (parts, clip len / loop / events) from the stub, no
shown model point below the feet at any compiled tick (every clip, every form it is compiled for; segments whose client
interpolation dips are split), no part turning more than 120° in a tick or a key (a 0-tick snap at a model swap
excepted), every point inside the culling box, models within -16..32, the atlas ≤ 0.52 M px, ≤ 6 500 elements at rest.
Floor guards: the cape trails back, a wing segment lifts, a tendril trails, the hair lies flat, the sword turns up about
its grip; the chain guards are planned over the whole clip (≤ 22°/t change). The secondary motion (hair lag 3 t, cape
flutter 40 t, wing flap, tendril writhe) is solved per tick; loops solve one silent cycle first.

Form-agnostic clips are compiled for all three forms: the body keys are shared, the wing / tendril keys are guarded by
`tkRigForm` where the forms differ. Budgets and counts: manifest `budgets`. Suite: `S:tk/tests/test_rig.py [--rebuild]`.
