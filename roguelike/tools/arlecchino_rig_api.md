# 아를레키노 (Arlecchino) rig: API (stage S2)

The display-entity rig of the chapter-4 boss 아를레키노 and the contract between the rig and the module
(`tools/mboss_arlecchino/*`, S3 / S4). Binding inputs: `S:ar/PLAN.md` §2-3, `S:ar/contract.md` §3.2, the frozen table
`tools/mboss_arlecchino/api.py` §7 (parts, looks, calls, anchors, clips). Every clip is read from the footage
(`S:ar/ref/*`, `S:ar/src/v1-v7.mp4`); the clip table below names the source of each.

## 0. Files

```
node tools/build_arlecchino_rig.mjs --resourcepack <unpacked RP> [--datapack <dp>] [--no-paint] [--allow-steps]
     [--debug-dp <scratch dir> [--debug-clips a,b | all] [--debug-step N]]
```

| file | owns |
|---|---|
| `build_arlecchino_rig.mjs` | the build: models / items / sprites / atlas, the per-clip solve, the compile (per-part key segments, form guards, snaps, floor-dip splits), the checks, the runtime functions (spawn, tick, follow, looks, anchors, face), the manifest, the debug pack |
| `arlecchino_pose.mjs` | the skeleton (the avatar's `transform()`, copied as `avatarTransform` for the parity test, scaled by `api.SIZE` 1.4) and `solve(pose, form)`: torso FK, IK legs (planted soles), IK arms (the scythe grips, free hand targets, the off hand on the other haft), each scythe in its cutting plane, the wings / blade legs, the cup and saucer, the floor guards, the anchors |
| `arlecchino_geometry.mjs` | the 26 parts, the P2 part models (skin_33 with the avatar's `skinFaces` layout and overlay inflation, classic 4-px arms), the wing / leg cards, cup, saucer, empty model, the hulls (the avatar's boxes, the scythe from `scythe_geometry.mjs`) |
| `arlecchino_paint.mjs` | the sprites: P1 crimson feather wings (2), P2 crimson blade legs (2), cup, saucer |
| `arlecchino_skin_p2.mjs` | `S:ar/src/skin_33.png` as base64 (written unchanged as `textures/mboss/arlecchino/skin_p2.png`) |
| `arlecchino_clips.mjs` | `DEFAULT_POSE` (the P1 stance), `P2_POSE` and the 41 clips (keys, look events, form switch, snaps) |
| `mboss_arlecchino/seq.py` | the sequences intro / t_p2 / death (written by S3's generator into `seq/**`) |

Generated (never hand-edit): `data/rlk/function/boss/arlecchino/rig/**`, `tools/arlecchino_rig_manifest.json`, the RP's
`assets/rlk/{textures,models/item,items}/mboss/arlecchino/**` and the items-atlas entries `rlk:mboss/arlecchino/*`. Reused,
never written: the avatar's item models `rlk:player_motion/arle/<part>` (phase 1 body; a later change of the avatar skin
changes the boss too) and `rlk:player_motion/weapons/scythe` (both scythes). The shared RIGLIB is used unchanged.

## 1. Calls (all `rlk:boss/arlecchino/rig/…`; @s = the body = the anchor, at its feet)

| function | what |
|---|---|
| `init` | objectives `knRig*` (safe on every load); loads the anchor table into `rlk:kn rig.an` once per table version |
| `spawn` / `spawn_hidden` | kills old parts, summons the 26 parts + the shadow in the rest pose, re-applies the stored form and looks, queues `idle` (`idle2` in form p2) / the same, then hidden |
| `tick` | once per game tick, after the module logic: respawns missing parts, follows the anchor (position + yaw; static skip), the hit flash, the clip step. Hidden: only the follow until a clip is queued |
| `play/<clip>` | the clip's tick 0 at the next `tick` (event *e* shows on the *e*-th tick after the call, counting that first one as 0) |
| `start/<clip>` | tick 0 now |
| `face/player`, `face/track` (≤ 12°/call), `face/set {yaw}` | anchor yaw; the parts take it every tick |
| `look/form/{p1,p2}` | the body models (p1: the avatar's `rlk:player_motion/arle/*`; p2: `rlk:mboss/arlecchino/p2/*`), the wing / leg models, scythe_l. A clip with a form (api.CLIP_FORM) enforces it at its tick 0; `t_p2` swaps p1 -> p2 at its `swap` event (90) itself |
| `look/wings/{off,open}` | P1 only: the crimson wing models (open) or the empty model (off). The wing clips (c2, f1, h1, e70) call it themselves at their wing events and key the wings' spread; S3 does not need to |
| `look/weapon_r/{hand,gone,world}`, `look/weapon_l/…` | hand: the clip keys drive it; gone: the empty model (the clip keys keep running, so `hand` shows it at once in the right pose); world: detached where it is (no follow, no clip keys; back to `hand` it rejoins within 8 t). The throws (b1 / b2 / q1 / q2) hide and re-form the scythe in the clip keys themselves |
| `look/glow/{normal,crimson}` | the crimson glow (outline, #E0303A) on both scythes for the Bond-of-Life tells; t_p2 sets crimson at its start and normal at 170 |
| `look/props/{none,tea}` | the cup and saucer models (the intro sets tea at 0 and none at 34 itself) |
| `anchor/{hand_r,hand_l,blade_r,blade_l,palm_r,chest,spine}` | moves the one `rlk_kn_anchor` marker (summoned if missing; tags `rlk_room rlk_mb_aux rlk_kn_anchor`) to that point of the CURRENT clip tick, yaw = the boss's; effects run `at` / `rotated as` it. The table holds every tick of every clip (form p1 for form-agnostic clips; blade_l = hand_l in P1) |
| `state/hidden` | every part scale 0 in place (never moved, never below the floor); `state/normal` (from hidden) restarts the current clip so its keys show the rig, and does nothing when the rig is already visible |
| `flash` | hit feedback: white-gold outline 3 t on the body parts (`flash_tick`, `flash_off` internal) |
| `kill` / `uninstall` | the parts, the shadow and the anchor marker / + the face marker, the objectives and the rig storage `rlk:kn rig` |

Stored looks: `knRigForm` (0 p1, 1 p2), `knRigWi`, `knRigWr`, `knRigWl`, `knRigGl`, `knRigPr` = the index in `api.LOOKS`.

## 2. Entities

26 item displays `524c4b4d-4b4e-4100-8000-0000000000NN` (NN = `api.PARTS` index), the shadow `…40` (radius 1.0).
Tags: parts `rlk_room rlk_mb_aux rlk_mb_part rlk_kn_part rlk_kn_<part>`, shadow `rlk_room rlk_mb_aux rlk_kn_part
rlk_kn_shadow`, the anchor marker `rlk_room rlk_mb_aux rlk_kn_anchor`. Culling 10 × 10 (the P2 blade legs spread 3.5 b from
her spine; t_p2 lifts her 5.6 b), view range 2, billboard fixed, brightness 13 (body), 15 (scythes, wings / legs), 14 (props).
The sequences add the intro's wisp markers (`rlk_room rlk_mb_aux rlk_kn_prop rlk_kn_wisp rlk_kn_wisp_<i>`) and t_p2's moon
marker (`… rlk_kn_prop rlk_kn_moon`); both are dressed by the kit props `wisp` / `moon_halo`.

## 3. Model (PLAN §2.1-2.3)

The avatar × 1.4: 2.8 b to the head top, hips 1.05. **P1** = the player avatar's own models of `rlk:skin/arlecchino` (white
coat, black, red, white hair, slim 3-px arms; shoulders ±0.34375 × 1.4), the avatar's glowing scythe 「붉은 달의 형상」 in the
right hand (3.6 b), scythe_l hidden; the crimson feather wings (3 fingers a side, 2 segments, 1.25 × the avatar scale) only in
the wing attacks. **P2** = skin_33 (white hair with the black streak, bare shoulders, the black bodice with the red X lacing,
the black skirt with red streaks) on classic 4-px arms (shoulders ±0.375 × 1.4), twin scythes (the left one's crescent turned
to its side: a mirror image), six crimson blade legs from her spine (3 a side, 2 segments, 1.35 × the avatar scale; folded up
behind her shoulders at rest, spread in the attacks, swaying, lagging her torso by 2 t). The teacup and saucer (1.5 × the
boss scale for readability) only in the intro.

The scythe is placed by its cutting plane and the shaft angle in it (`arlecchino_pose.mjs`): every swing sweeps on an arc,
the crescent's point leads the strike (as the avatar's calibrated strikes, `tools/player_motion/arle.json` infused_*), the
hand holds the grip (IK; a straight arm along the haft for the wide sweeps). The intro twirl keeps the footage's trailing hook.
Floor guards: a scythe turns back about its grip in its plane (toward where it was the tick before) until its lowest point
clears the floor; a wing / leg segment lifts about the axis across it; a tilted shin stands on its sole corner; a root lift
catches the rest. Nothing is below the feet at any compiled tick (the build gate and the suite).

## 4. Clips (contract table; events = played ticks)

| clip | len | form | footage | notes |
|---|---|---|---|---|
| `idle` / `idle2` | 40 loop | p1 / p2 | v1 4.6-5.0, v2 16.3 / v4 22.4, v6 7.4 | the stance: crescent low by the right foot, haft across the body (P2: twin scythes, a low X) |
| `walk` / `walk2`, `strafe_*` | 24 / 20 loop | p1 / p2 | v5 13-39, v2 12.5-27 | planted strides (the anchor moves); step1 0, step2 12 |
| `backstep` | 12 | any | v2 37.5 | hop back, land 10 |
| `flinch` | 6 | any | | |
| `brk` | 20 | any | v3 27.05-28.3 | the counter: she reels and sinks toward the knee (then `stun`) |
| `stun` / `stun2` | 140 | p1 / p2 | v3 27.3-29.5 / v7 24.15 | on one knee, the scythe(s) planted, head bowed (20-120 a hold span, played through), rise 120 |
| `intro` | 150 | p1 | v5 33-39.5, v1 0.0-5.2 | §5 below |
| `a2` / `a4` / `a5` | 46 / 100 / 124 | p1 | v2 13-16.6, 19-26.8 | sweep right -> left 14, backhand 24; spin ring 38-50 (h3 44); the two-handed overhead slam 64; a5 the second spin ring 78-90 (h5 84) |
| `b1` / `b2` | 60 / 130 | p1 | v1 15.4-18.1, 19.5-24.6 | the scythe spun into a vertical wheel (two turns), released at 28 (hidden; the kit's wheel flies), caught at 52; b2: a second wheel 40-58, the open-hand reach 76, the grab 96, the scythe back at 100 |
| `c1` / `c2` | 80 / 140 | p1 | v1 26.5-29.0, 32.0-35.0, 35.4-39.9 | crouch, jump 8, the flaming whirl at the apex 18-44, the two-handed dive 48-54; c2: the wings burst open 84, the wing strike 90, held to 130 |
| `d1` / `d2` | 56 / 76 | p1 | v2 0-11.5 | crouched, the scythe drawn back low (the red flare tell), the dash 26, the slash 30; d2 the rising follow-up 46 |
| `e1` | 112 | p1 | v2 37.5-40, v3 0-7.25 | hover pose, five leaning dashes 16-56, the dive 70, sweep 76, the vertical wheel 86-98 (spin 92) |
| `f1` | 232 | p1 | v3 7.5-29.5 | scythe raised, the left hand at the player (sigil), brand 22, arms out at the centre 40, raised 100, thrown down 160, risen on the wings 166, gathered and flung wide 196, settle |
| `g1` | 140 | p1 | v3 29.5-40, v4 0-3.4 | the scythe driven into the floor 0-6, pushes at 34 / 62, turn at 40, wrenched out and lifted 70, slammed 104 |
| `h1` | 156 | p1 | v4 0-13 | up to the web 0-10, perched, the hand flung at the clones 20, the backward drop 96, the wing strike 104, sweep 112 |
| `e70` | 110 | p1 | v2 28-37.7 | rises 1 b 0-20, arms open, the brand thrust 70, the wings burst 74, land 96 |
| `t_p2` | 180 | p1 -> p2 at 90 | v4 13.5-21.4 (designed) | §5 below |
| `q0_hover` / `q0_dive` | 40 loop / 40 | p2 | v4 17.6-21.4 | high, legs spread / the dive, impact 20, the blade eruption push 28 |
| `q1` | 124 | p2 | v4 28.5-37 | spin 14, the inward cross 30, the right scythe thrown 46 (re-forms 52-56), right sweep 66, left sweep 82, both thrown 100 (re-form 108-114) |
| `q2` | 70 | p2 | v4 37-40, v6 0-5 | the right scythe whirled and flung 20, the dash 34, the left sweep 42 (the right re-forms 38) |
| `q3` | 36 | p2 | v6 5-15.5 | legs flare, the spin 7-21 (14) |
| `q4_up` / `q4_shot` / `q4_land` | 20 / 50 / 16 | p2 | v6 15.5-26.5 | scythes crossed before her chest, legs spread; the recoil at fire 26; land 12 |
| `q5a` / `q5b` | 180 / 136 | p2 | v6 26-40, v7 0-27 | both raised and crossed overhead, brand 22; A: slam 95, outward sweep 121, risen and the great slam 158; B: the vertical X 26-50, rapid slashes s1-s9 every 3 t, the final slam 96 |
| `q6` | 200 | p2 | v7 28-40 | up on the spread legs, six volleys flicked 50-100, orbs gathered 110, flung 125, the dive 160-168 |
| `death` | 110 | p2 | wiki | stop, lower 10, the scythes dissolve 30-38, straighten 50, flames 70, vanish 96 (vis 0) |

## 5. The sequences (`mboss_arlecchino/seq.py`)

**intro** (150 t, beat by beat from v1 0.0-5.2; `S:ar/renders/s2_intro_vs_ref.jpg`): E0 tea 0-30 (the saucer at her sternum,
the cup lifted to her lips 8-14, the sip 14-22, lowered 22-30, three white wisps circling her), E1 30-44 (the hands drop,
the cup and saucer burst into embers at 34, the wisps flee to the rim posts 35-55), E2 reach 44-52 (the right arm out to
shoulder height), E3 summon 52-60 (crouch, turned 20° right, the crimson vortex at the palm), E4 form 60-72 (the haft grows
out of the palm both ways, the crescent ignites last at 70, the arm draws it in), E5 hold 72-92 (the haft across her chest,
the crescent hanging at her left; title + the line 「두려운가?…」 at 80), E6 the 360° frontal twirl 92-104 (30°/t, keyed every
tick; the lower half swung forward clear of the floor; the floor flame ring at 98), E7 hold 104-110, E8 the flip 110-116 (over
the top, rolled through the hand), E9 the stance 116-150 (breathing from 130, the push ring r 4 at 140, no damage).
**t_p2** (180 t): stagger, kneel with the scythe planted (0-24), head bowed in the pillar (24-50), blackout 50-70 (blindness
20 t, the arena look `crimson`, two wisps turn red), stands and rises 3 b (70-108; the form swap at 90), the six legs unfold a
pair at 110 / 116 / 122, the twin scythes form 130-138, title + 「보아라, 모든 선의를 불태울 칼날을!」 at 140, the launch 150-176
(vis 0 at 176: S4's `q0` places the body at the hover spot and plays `q0_hover`). **death** (110 t): as the clip; the wisps
turn white at 100. The core owns invulnerability, cine, music, the phase switch, repool and the fight end.

## 6. Build checks and budgets

Strict by default (`--allow-steps` warns instead): the contract (parts, clip len / loop / events / forms) from the stub, no
shown model point below the feet at any compiled tick (every clip, every form it is compiled for; segments whose client
interpolation dips are split), no part turning more than 120° in a tick or a key (a 0-tick snap at a model swap / scythe
appearance excepted), every point inside the culling box, models within -16..32, the atlas ≤ 0.15 M px, ≤ 6 500 elements at
rest. The edge check (warning) lists swing ticks where the crescent's point trails (recoveries and the footage's trailing
twirl). Form-agnostic clips (`backstep`, `flinch`, `brk`) are compiled for both forms; the parts whose keys differ are guarded
by `knRigForm`. Budgets and counts: manifest `budgets`. Suite: `S:ar/tests/test_rig.py [--rebuild]`.
