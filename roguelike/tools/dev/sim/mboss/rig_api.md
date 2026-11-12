# Corrupted Guardian (파수꾼・타락) rig: API contract

Generator: `tools/build_mboss_guardian_rig.mjs` (with `guardian_paint.mjs`, `guardian_paint_lib.mjs`,
`guardian_geometry.mjs`, `guardian_pose.mjs`, `guardian_rig_math.mjs`, `guardian_clips.mjs`).

```
node tools/build_mboss_guardian_rig.mjs --resourcepack <unpacked RP> [--datapack <dp>] [--no-paint | --paint a,b]
```

- It owns and rewrites `data/rlk/function/mboss/guardian/rig/**`. Never hand-edit those files.
- In the RP it writes:
  - `assets/rlk/textures/mboss/guardian/*.png` (appended to `assets/minecraft/atlases/items.json`);
  - `assets/rlk/models/item/mboss/guardian/*.json`;
  - `assets/rlk/items/mboss/guardian/*.json`.
- The manifest is `tools/mboss_guardian_rig_manifest.json`: parts, UUIDs, clips, events, element looks.
- `--debug-dp <scratch dir>` also writes exact per-tick poses (`gd_dbg/<clip>/<t>`) for the offline renderer. It never writes into the real pack.

All functions below are `rlk:mboss/guardian/rig/...`. Unless a line says otherwise, **@s is the rig anchor**: the boss body (the hitbox husk) or any other entity that carries the rig. Call them `as` the anchor and `at` it.

## 1. Calls

| function | when | what |
|---|---|---|
| `init` | load (idempotent) | Objectives `gdRigC` (clip id), `gdRigT` (clip tick), `gdRigF` (flash), `gdRigEye`, `gdRigSp` (looks), `gdRigY` (scratch). |
| `spawn` | once, as/at the anchor, rotated as it | Kills old parts, summons the 29 parts in the idle pose at the anchor's position and yaw, starts `idle`, and re-applies the stored eye/spear looks. |
| `tick` | **every game tick**, `execute as <anchor> at @s run function rlk:mboss/guardian/rig/tick` | Respawns if the parts are missing. Parts follow the anchor position + yaw (teleport_duration 1). Advances the current clip and applies its keys. Counts down the flash. |
| `play/<clip>` | any time | Starts `<clip>` from tick 0 at the next `tick`: the same game tick if `tick` runs after it, else the next tick. The first key segment blends from the current pose (at least 3 t, `blend` per clip). |
| `kill` | cleanup | `kill @e[type=item_display,tag=rlk_mb_guardian_part]`. Props are separate (`prop/clear`). |
| `face/player` | as needed | Instant yaw toward the nearest non-spectator player. The rig takes the anchor's yaw every tick. |
| `face/track` | each tick while tracking | Turns at most 12°/call toward the nearest player. Uses a temporary marker `rlk_mb_gd_face`. |
| `face/set {yaw:<deg>}` | macro | Sets the anchor yaw. |
| `eye/<el>` | record state | Shield eye look: `geo` (painted default), `pyro`, `hydro`, `electro`, `cryo`, `gold` (guard aura), `red` (chaos). |
| `spear/<el>` | enchant state | Spear head enchant + aura colour. Same names; `geo` = the gold spear. |
| `tint/<el>` | both | `eye/<el>` + `spear/<el>`. |
| `look_apply` | after a manual score change | Re-applies `gdRigEye`/`gdRigSp` (ids: 0 geo, 1 pyro, 2 hydro, 3 electro, 4 cryo, 5 gold, 6 red; ids 1-4 match `#elem`). |
| `flash` | on a body hit (optional) | White-gold outline (`Glowing`) on the parts for 3 t. |
| `prop/spear` | javelin flight, giant fail spears | Summons a free spear `item_display` at the execution position/yaw. Tags: `rlk_room`, `rlk_mb_aux`, `rlk_mb_gd_prop` and, for this call only, `rlk_mb_gd_prop_new`. Scale 2.2 = her spear; model frame: grip at the origin, tip along +Y. It carries no rig tag, so `tick` never moves it. Coloured copies: item models `rlk:mboss/guardian/prop_spear_<red\|gold\|pyro\|hydro\|electro\|cryo>`. Giant spears: set the scale to about 5-6. |
| `prop/clear` | cleanup | Kills all props. |

Order inside the boss tick: run the AI, which may call `play/...`, `face/...` and move the body; then run `rig/tick`. The clip's tick 0 then applies in the same game tick.

## 2. Entities, tags, cost

- 29 `item_display` parts with **fixed UUIDs** `524c4b4d-4247-4400-8000-0000000000NN` (NN = 01..1d, part order in the manifest). Every per-tick command addresses a part by UUID, so there are no selector scans:
  - follow: 29 `tp <uuid>`;
  - keys: only the parts whose interpolation segment starts on that tick.
- One guardian rig can exist at a time. A second `spawn` kills the first.
- Tags on every part: `rlk_room`, `rlk_mb_aux`, `rlk_mb_part`, `rlk_mb_guardian_part`, `rlk_mb_gp_<part>`. The framework's `kill @e[tag=rlk_mb_aux]` removes the rig.
- Parts, in UUID order:
  - body: pelvis, skirt_f, skirt_o, tail, leg_r, leg_l, torso, head (with the eye; brightness 15), halo, halo_glow;
  - arms: r_upper, r_fore, r_hand, l_upper, l_fore (gauntlet, 15), l_hand, bracket;
  - shield and wing: shield, shield_eye (15), wing_cov, wing_sec, wing_pri;
  - spear: spear (15), spear_glow (15), trail_1, trail_2;
  - cubes_a, cubes_b, cubes_c (floating red/black cubes: right arm, below the feet, neck).
- Body parts use brightness 12-13 (sky 15). `width/height 16`, `view_range 2.5`.
- Clips compile to interpolation segments. A part gets a key only when the client's lerp/slerp would drift from the authored pose: more than 0.012 b, 0.5-2°, or 1.5 % scale.
  - Result: 24 clips, about 900 key files and 9 800 part keys, about 6.7 MB.
  - Raiden's rig is 32 MB.
  - Dispatch is two small binary trees (clip id, key tick); no macros on the hot path.

## 3. Body travel versus clip motion

- The rig follows the **anchor**. Clips carry heights, leans, limbs and the spear relative to the anchor (pos y holds the 0.35 b hover).
- **Horizontal travel is the pattern code's job.** Move the anchor (the body) along the paths below.
- The hitbox stays on the floor while the rig rises (K9).
- Vertical motion is in the clips:
  - `flyslam`: +8 b;
  - chaos: +3 b hover, +4.8 b in the fail;
  - `death`: flies out.
- While the spear is planted (it is a rig part), keep the anchor still:
  - `slam` 26-48;
  - `flyslam` 41-71;
  - `groggy_*`, `getup` 0-8;
  - `entrance` 14-26.

## 4. Clips (ticks at 20/s; events are clip ticks)

| clip | id | len | then | events | notes / body travel |
|---|---|---|---|---|---|
| `idle` | 0 | 40 | loop | | Hover bob +0.05 b at t20. The wing tiers breathe, the skirt and tail sway, the cubes drift. |
| `glide` | 1 | 24 | loop | | Moving pose (approach, guard drift, reposition): leans into the travel, spear level toward the target, wing swept back. |
| `thrust` | 2 | 91 | idle | glow 4, glint 19, **hit1 28**, rise 38, dive 54, **hit2 58**, land 65, flourish 72 | Lunge 2-3 b forward at 27-28; fly back 4-6 b during 38-54; dash 5-6 b along the dive at 57-58. |
| `javelin` | 3 | 74 | idle | spin 0, vanish 8, glyph 9, beam 26, rematerialise 29, **release 33**, launch 34, return 56, catch 61 | The rig spear is hidden 8-29 and 34-61. The flying spear is a `prop/spear` moved by the pattern code: out at 34, back by 61. |
| `slam` | 4 | 70 | idle | raise 0, ring 9, glint 12, down 22, **impact 26**, pull 48, twirl 54 | Disc r 5 centred 3.5 b in front. The ring leads by 17 t. The spear stays planted 26-48. |
| `pull` | 5 | 40 | idle | aura 0, cage 11, **relocate 32** | The corrupted claw casts; the left hand holds the shaft. Play `swing` 10-14 t after the relocation (K15). |
| `swing` | 6 | 51 | idle | windup 0, **swing1 20-24**, **swing2 33-39** | Two full 360° spins at waist height: a forehand, then a backhand rising low-right to high-left. |
| `flyslam` | 7 | 101 | idle | raise 0, glint 2, beam 16, takeoff 19, ring 21, gone 23, dive 39, **impact 41**, spikes 47, pull 71, twirl 79 | Up to +8 b at 19-23. Move the anchor to the locked ring centre during 23-39. The spear is planted 41-71. |
| `guard_entry` | 8 | 50 | guard | twirl 0, discs 16, ring 35, settle 44, guard 50 | Baton twirl, then vertical spin discs to her right and in front, then the ground ring, then she settles into the guard pose. |
| `guard` | 9 | 40 | loop | | Guard hold (100 t in the pattern): spear diagonal up-right, wing raised and opened. Drift the anchor about 1 b/s toward the player. Call `eye/gold` for the aura. |
| `sweep` | 10 | 44 | idle | windup 0, **active 19-24** | Gold sweep: 180-210° front arc from her left to her right, r 4.5-5. |
| `sweep_e` | 11 | 50 | idle | enchant 0, windup 7, **active 19-27** | Enchanted sweep. Call `spear/<el>` before it and `spear/geo` after. |
| `chaos_leap` | 12 | 32 | chaos_charge | leap 0, **land 32** | Leap 0-9, then an arcing flight 9-31: move the anchor to the arena centre. |
| `chaos_charge` | 13 | 36 | chaos_hover | charge 0, flare 7, rise 30, hover 36 | Spear level on the centre for 30 t, then the rise to the hover (feet 3 b up). |
| `chaos_hover` | 14 | 40 | loop | | Chaos hold: arms up, spear horizontal behind the shoulders, wing spread. |
| `chaos_fail` | 15 | 40 | hold | twist 10, rise 21, high 25 | Timeout: a twist with the wing swept across her front, then a rise to +4.8 b, held. Play `chaos_land` after the fail spears. |
| `chaos_land` | 16 | 26 | idle | land 22 | Descends to the floor. |
| `chaos_fall` | 17 | 20 | groggy_a | hang 0, fall 6, land 18 | The 2nd star breaks: she falls about 1 BH; no impact. |
| `groggy_a` | 18 | 40 | loop | | Pose A: slumped, the spear planted head-down at her right, wing drooped, halo blazing. |
| `groggy_b` | 19 | 34 | getup | fold 0, getup 34 | Pose B: she folds forward and the shield swings in front. Groggy total (K13): `chaos_fall` 20 + `groggy_a` about 116 + `groggy_b` 34 + `getup` 40. |
| `getup` | 20 | 40 | idle | spread 0, lift 6, stance 12 | The wing spreads widest, she lifts off, the spear comes forward. |
| `entrance` | 21 | 60 | idle | fall 0, **impact 14**, appear 14, grab 26, pull 34 | The spear plunges from +7 b and plants at 14 (damage). She fades in beside it (14-24), grabs it at 26 and pulls it out. |
| `death` | 22 | 80 | hold | slump 0, takeoff 22, gone 76 | Slump, then the fly-away to +15 b with a fade. Call `kill` after 80. |
| `pose_ref` | 23 | 20 | loop | | The official render pose. For screenshots. |

Hit geometry, damage, telegraphs, sounds and FX belong to the pattern code (patterns.md §3-§11, plan.md K-decisions). The clips only time the body.

## 5. Looks

- The default spear is gold. The shield eye is painted in the Geo colours (white core, orange bezel, amber iris).
- `spear/<el>` swaps three things:
  - the head to a luminance version tinted per element;
  - the shaft, gems and stars, which stay gold/red;
  - the aura card colour.
- `eye/<el>` swaps the gem/iris/field to the tinted version. A white-hot core plate stays on top.
- Tint values (item `minecraft:constant`):

  | element | eye | spear | glow |
  |---|---|---|---|
  | pyro | `#FF8A4C` | `#FFB088` | `#FF7A3C` |
  | hydro | `#5CC8FF` | `#9CDCFF` | `#4CB8FF` |
  | electro | `#E484FC` | `#EEB4FF` | `#D46CFC` |
  | cryo | `#A2FEFD` | `#D4FFFE` | `#8CF0FF` |
  | gold | `#FCE484` | `#FFF2B8` | `#FCD84C` |
  | red | `#E03A3A` | `#FF7A6A` | `#E0303C` |

- The halo blaze (groggy, chaos charge) and the spear glow strength are pose channels inside the clips.

## 6. Not in the rig (pattern / FX code)

- Particles, ground decals and hazard meshes.
- The chaos cross sigil and the stars.
- Cube streams and the pull cage.
- Screen effects and sounds.
- Moving `prop/spear` copies (javelin, giant fail spears).
