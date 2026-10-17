# Corrupted Guardian (파수꾼・타락) rig: API contract

This is the contract between the rig and the mid-boss pattern code. README.md §"중간보스 파수꾼・타락 모델과 리그" gives the overview in Korean.

Generator: `tools/build_mboss_guardian_rig.mjs`, with `guardian_paint.mjs`, `guardian_paint_lib.mjs`, `guardian_geometry.mjs`, `guardian_pose.mjs`, `guardian_rig_math.mjs` and `guardian_clips.mjs`.

```
node tools/build_mboss_guardian_rig.mjs --resourcepack <unpacked RP> [--datapack <dp>] [--no-paint | --paint a,b] [--debug-dp <scratch dir>]
```

- It owns and rewrites `data/rlk/function/mboss/guardian/rig/**`. Never hand-edit those files.
- In the RP it writes:
  - `assets/rlk/textures/mboss/guardian/*.png`, appended to `assets/minecraft/atlases/items.json`;
  - `assets/rlk/models/item/mboss/guardian/*.json`;
  - `assets/rlk/items/mboss/guardian/*.json`.
- The manifest is `tools/mboss_guardian_rig_manifest.json`. It lists the parts, UUIDs, clips, events and element looks.
- `--debug-dp <scratch dir>` also writes the exact per-tick poses (`gd_dbg/<clip>/<t>`) for the offline renderer. It never writes into the real pack.

All functions below are `rlk:mboss/guardian/rig/...`. Unless a line says otherwise, **@s is the rig anchor**: the boss body (the hitbox husk) or any other entity that carries the rig. Call the functions `as` the anchor and `at` it.

## 1. Calls

| function | when | what |
|---|---|---|
| `init` | load (idempotent) | Adds the objectives `gdRigC` (clip id), `gdRigT` (clip tick), `gdRigF` (flash), `gdRigEye` and `gdRigSp` (looks), `gdRigGl` (glow look), and `gdRigY` (scratch). |
| `spawn` | once, as/at the anchor, rotated as it | Kills old parts and summons the 29 parts in the idle pose at the anchor's position and yaw. Queues `idle` from its tick 0 for the next `tick`. Re-applies the stored eye and spear looks. |
| `spawn_hidden` | instead of `spawn`, before an entrance | The same, but every part starts at scale 0, so nothing shows. Play the opening clip in the same tick (`play/entrance`); its first key brings the parts in. With no clip played, idle grows in over 3 t. |
| `tick` | **every game tick**: `execute as <anchor> at @s run function rlk:mboss/guardian/rig/tick` | Respawns the parts if they are missing. **A respawn restarts the rig in `idle`**, so replay the current clip if it matters. The parts follow the anchor position and yaw (teleport_duration 1). Advances the current clip, applies its keys and counts down the flash. |
| `play/<clip>` | any time | Starts `<clip>` from tick 0 at the next `tick`: the same game tick if `tick` runs after it, otherwise the next tick. The first key segment blends from the current pose over at least 3 t (`blend` per clip). |
| `kill` | cleanup | `kill @e[type=item_display,tag=rlk_mb_guardian_part]`. Props are separate (`prop/clear`). |
| `face/player` | as needed | Instant yaw toward the nearest non-spectator player. The rig takes the anchor's yaw every tick. |
| `face/track` | each tick while tracking | Turns at most 12° per call toward the nearest player. Both yaws are normalised into [-180°, 180°) first, so tracking stays correct however many turns the player circles. Uses a temporary marker `rlk_mb_gd_face`. |
| `face/set {yaw:<deg>}` | macro | Sets the anchor yaw. |
| `eye/<el>` | record state | Shield eye look: `geo` (the painted default), `pyro`, `hydro`, `electro`, `cryo`, `gold` (guard aura) or `red` (chaos). |
| `spear/<el>` | enchant state | Spear head enchant, aura colour and the two afterimage trails. Same names; `geo` is the gold spear. |
| `tint/<el>` | both | `eye/<el>` + `spear/<el>`. |
| `look_apply` | after a manual score change | Re-applies `gdRigEye` / `gdRigSp` / `gdRigGl`. Ids: 0 geo, 1 pyro, 2 hydro, 3 electro, 4 cryo, 5 gold, 6 red; ids 1-4 match `#elem`. |
| `flash` | on a body hit (optional) | White-gold outline (`Glowing`) on the parts for 3 t, then back to the glow look (`flash_off` → `glow_apply`). |
| `glow/gold`, `glow/off` | guard mode's gold aura (the core: window open → record or the gold sweep's end) | A persistent `Glowing` outline `#FCD84C` on every part except the glow cards and the afterimages (`gdRigGl` 1 / 0; kept over a respawn, restored after a hit flash). |
| `prop/spear` | javelin flight, giant fail spears | Summons a free spear `item_display` at the execution position and yaw. |
| `prop/clear` | cleanup | Kills all props. |

`prop/spear` details:
- Tags: `rlk_room`, `rlk_mb_aux`, `rlk_mb_gd_prop`, and for this call only `rlk_mb_gd_prop_new`.
- Scale 2.2 matches her spear. Model frame: the grip is at the origin and the tip points along +Y.
- It carries no rig tag, so `tick` never moves it.
- Coloured copies are the item models `rlk:mboss/guardian/prop_spear_<red|gold|pyro|hydro|electro|cryo>`.
- For the giant fail spears, set the scale to about 5-6.

Order inside the boss tick: run the AI first, which may call `play/...`, `face/...` and move the body. Then run `rig/tick`, so a clip's tick 0 applies in the same game tick.

## 2. Entities, tags, cost

- 29 `item_display` parts with **fixed UUIDs** `524c4b4d-4247-4400-8000-0000000000NN` (NN = 01..1d, in manifest order).
- Every per-tick command addresses a part by UUID, so nothing scans selectors:
  - follow: 29 `tp <uuid>`;
  - keys: only the parts whose interpolation segment starts on that tick.
- Only one guardian rig can exist at a time; a second `spawn` kills the first.
- Tags on every part: `rlk_room`, `rlk_mb_aux`, `rlk_mb_part`, `rlk_mb_guardian_part`, `rlk_mb_gp_<part>`. The framework's `kill @e[tag=rlk_mb_aux]` removes the rig.
- Parts, in UUID order:
  - body: pelvis, skirt_f, skirt_o, tail, leg_r, leg_l, torso, head (with the eye; brightness 15), halo, halo_glow;
    the front panel (skirt_f), the outer panels (skirt_o) and the tail give way to the voxel legs: a leg pitched further
    forward (back) than in idle pushes them along by the excess, so the leg cubes never cut the feathers;
  - arms: r_upper, r_fore, r_hand, l_upper, l_fore (gauntlet, 15), l_hand, bracket;
  - shield and wing: shield, shield_eye (15), wing_cov, wing_sec, wing_pri;
  - spear: spear (15), spear_glow (15), trail_1, trail_2;
  - cubes_a, cubes_b, cubes_c: floating red/black cubes at the right shoulder, below the feet and at the neck.
    cubes_b (the loose cubes by the shins and the trail under the feet) follows the mean leg swing and has 8 drift frames
    (`cubes_b`, `cubes_b_1`..`cubes_b_7`); every clip swaps them every 5 t (per 40 t cube cycle). Pattern code never sets its item model.
- Body parts use brightness 12-13 (sky 15), `width`/`height` 16 and `view_range` 2.5.
- Clips compile to interpolation segments. A part gets a key only where the client's lerp/slerp would drift from the authored pose by more than 0.012 b, 0.5-2° or 1.5 % scale.
  - Result: 25 clips, about 980 key files and 10 100 part keys, about 2.8 MB.
  - Raiden's rig is 32 MB.
  - Dispatch is two small binary trees (clip id, then key tick), with no macros on the hot path.

## 3. Build checks

The generator refuses to write a rig that fails these checks. `--allow-steps` and `--allow-butt` turn them into warnings while authoring.

- **Rotation per tick:** no part (trails aside) turns more than 120° between two ticks.
- **Rotation per key:** no interpolation segment, including the blend into a clip, turns more than 120°. Near 180° the client's shortest-path slerp has no stable direction.
- **Finial on the face:** in every clip and tick, the red butt finial and the orbit star must stay out of a box in front of the face diamond: |dx| < 0.22, −0.35 < dy < 0.12 and not behind the face.
- **Half-tick path (warning only):** a 1-tick step above 45° is also solved at the half tick. Where the client's slerp leaves that path by more than 35°, the build prints a warning.
- **Pose solver continuity:** the elbow bend plane, the fist's roll around the shaft and each arm segment's roll are carried from tick to tick, and each turns at most 40-55° per tick. The solver therefore never flips an elbow or a wrist in one tick on its own; any large turn comes from the authored motion, which the checks above bound.

## 4. Body travel versus clip motion

- The rig follows the **anchor**. Clips carry heights, leans, limbs and the spear relative to the anchor; pos y holds the 0.35 b hover.
- **Horizontal travel is the pattern code's job:** move the anchor (the body) along the paths below.
- The hitbox stays on the floor while the rig rises (K9).
- Vertical motion is in the clips:
  - `flyslam`: +8 b;
  - chaos: +3 b hover, +4.8 b in the fail;
  - `death`: flies out.
- While the spear is planted (it is a rig part), keep the anchor still:
  - `slam` 26-48;
  - `flyslam` 41-71;
  - `groggy_*`, and `getup` 0-8;
  - `entrance` 14-26.

## 5. Clips (ticks at 20/s; events are clip ticks)

| clip | id | len | then | events | notes and body travel |
|---|---|---|---|---|---|
| `idle` | 0 | 40 | loop | | Hover bob +0.05 b at t20. The corrupted arm reaches out to her right, and the claw holds the shaft at the crescent. The butt star sits on the halo's upper edge on her left. The wing tiers breathe, the skirt and tail sway, the legs swing out of step, the cubes drift. |
| `glide` | 1 | 24 | loop | | Moving pose (approach, guard drift, reposition). She leans into the travel, the spear is level toward the target and the wing sweeps back. |
| `thrust` | 2 | 91 | idle | glow 4, glint 19, **hit1 28**, rise 38, dive 54, **hit2 58**, land 65, flourish 72 | Lunge 2-3 b forward at 27-28. Fly back 4-6 b during 38-54. Dash 5-6 b along the dive at 57-58. |
| `javelin` | 3 | 76 | idle | spin 0, vanish 10, glyph 11, beam 28, rematerialise 31, **release 35**, launch 36, return 58, catch 63 | A full spin of the spear around her (5-9) before it vanishes. The rig spear is hidden 10-31 and 36-63. The flying spear is a `prop/spear` moved by the pattern code: out at 36, back by 63. |
| `slam` | 4 | 70 | idle | raise 0, ring 9, glint 12, down 22, **impact 26**, pull 48, twirl 54 | Disc r 5 centred 3.5 b in front. The ring leads by 17 t. The spear stays planted 26-48. |
| `pull` | 5 | 40 | idle | aura 0, cage 11, **relocate 32** | The corrupted claw casts while the left hand holds the shaft. Play `swing` 10-14 t after the relocation (K15). |
| `swing` | 6 | 51 | idle | windup 0, **swing1 20-24**, **swing2 33-39** | Two full 360° spins at waist height: a one-handed forehand (it comes round over 17-20), then a backhand rising from low right to high left. |
| `flyslam` | 7 | 101 | idle | raise 0, glint 6, beam 16, takeoff 19, ring 21, gone 23, dive 39, **impact 41**, spikes 47, pull 71, twirl 79 | Up to +8 b at 19-23. Move the anchor to the locked ring centre during 23-39. The spear is planted 41-71. |
| `guard_entry` | 8 | 50 | guard | twirl 0, discs 16, ring 35, settle 44, guard 50 | Baton twirl, vertical spin discs to her right and then in front, the ground ring, then she settles into the guard pose. |
| `guard` | 9 | 40 | loop | | Guard hold (100 t in the pattern): spear diagonal up-right, wing raised and opened. Drift the anchor about 1 b/s toward the player. Call `eye/gold` for the aura. |
| `sweep` | 10 | 44 | idle | windup 0, **active 19-24** | Gold sweep: a 180-210° front arc from her left to her right, r 4.5-5. |
| `sweep_e` | 11 | 50 | idle | enchant 0, windup 7, **active 19-27** | Enchanted sweep. Call `spear/<el>` before it and `spear/geo` after; the trails take the element colour too. |
| `chaos_leap` | 12 | 32 | chaos_charge | leap 0, **land 32** | Leap 0-9, then an arcing flight 9-31: move the anchor to the arena centre. |
| `chaos_charge` | 13 | 36 | chaos_hover | charge 0, flare 7, rise 30, hover 36 | Spear level on the centre for 30 t, then the rise to the hover (feet 3 b up). |
| `chaos_hover` | 14 | 40 | loop | | Chaos hold: arms up, spear horizontal behind the shoulders, wing spread. |
| `chaos_fail` | 15 | 40 | hold | twist 10, rise 21, high 25 | Timeout (tick 0 = timer full, T0): a twist with the wing swept across her front, then a rise to +4.8 b, held. See the fail sequence below. |
| `chaos_land` | 16 | 26 | hold | land 22 | She comes down to stand on the floor at the centre, the spear still across her shoulders, and holds that stance. |
| `chaos_fall` | 17 | 20 | groggy_a | hang 0, fall 6, land 18 | The 2nd star breaks: she lets go with the left hand, the spear arm comes down round her right side, and she falls about 1 BH with no impact. |
| `groggy_a` | 18 | 40 | loop | | Pose A: slumped, the spear planted head-down at her right, wing drooped, halo blazing. |
| `groggy_b` | 19 | 34 | getup | fold 0, getup 34 | Pose B: she folds forward and the shield swings in front. Groggy total (K13): `chaos_fall` 20 + `groggy_a` about 116 + `groggy_b` 34 + `getup` 40. |
| `getup` | 20 | 40 | idle | spread 0, lift 6, stance 12 | The wing spreads widest, she lifts off and the spear comes forward. |
| `entrance` | 21 | 60 | idle | fall 0, **impact 14**, appear 14, grab 26, pull 34 | The spear plunges from +7 b and plants at 14 (damage). She fades in beside it (14-24), grabs it at 26 and pulls it out. Use `spawn_hidden` + `play/entrance` so she is never seen before it. |
| `death` | 22 | 80 | hold | slump 0, takeoff 22, gone 76 | Slump, then the fly-away to +15 b with a fade. Call `kill` after 80. |
| `pose_ref` | 23 | 20 | loop | | The official render pose, for screenshots. |
| `chaos_raise` | 24 | 24 | idle | raise 0, **overhead 6** | Fail spear 2: from the across-the-shoulders stance she raises the spear vertically overhead in 6 t, holds, then returns to idle. |

**Chaos fail sequence** (patterns.md §9.4; T0 = chaos timer full):
1. At T0, play `chaos_fail`.
2. At T0+33 (`chaos_fail` tick 33), play `chaos_land`. She lands at T0+55, between fail spear 1 (impact T0+49) and fail spear 2 (impact T0+80).
3. For a second surviving star, play `chaos_raise` at T0+74, so the spear is overhead at the drop.
4. After the last spear, play `idle` or `glide`. She leaves the centre at about T0+90.

Hit geometry, damage, telegraphs, sounds and FX belong to the pattern code (patterns.md §3-§11, plan.md K-decisions). The clips only time the body.

## 6. Looks

- The default spear is gold. The shield eye is painted in the Geo colours: a small white-hot gem with an orange bezel on a glowing amber-gold star field, thin maroon crescents and an amber iris.
- `spear/<el>` swaps:
  - the head to a luminance version tinted per element (the shaft, gems and stars stay gold/red);
  - the aura card colour;
  - the two afterimage trails.
- `eye/<el>` swaps the eye to the tinted version. A white-hot core plate stays on top.
- Tint values (item `minecraft:constant`):

  | element | eye | spear | glow and trails |
  |---|---|---|---|
  | geo | painted | painted | `#F4D07C` (trails `#F4D27A`) |
  | pyro | `#FF8A4C` | `#FFB088` | `#FF7A3C` |
  | hydro | `#5CC8FF` | `#9CDCFF` | `#4CB8FF` |
  | electro | `#E484FC` | `#EEB4FF` | `#D46CFC` |
  | cryo | `#A2FEFD` | `#D4FFFE` | `#8CF0FF` |
  | gold | `#FCE484` | `#FFF2B8` | `#FCD84C` |
  | red | `#E03A3A` | `#FF7A6A` | `#E0303C` |

- The halo blaze (groggy, chaos charge) and the spear glow strength are pose channels inside the clips.

## 7. Not in the rig (pattern / FX code)

- Particles, ground decals and hazard meshes.
- The chaos cross sigil and the stars.
- Cube streams and the pull cage.
- Screen effects and sounds.
- Moving `prop/spear` copies (javelin, giant fail spears).

## Non-rig resources the rig generator also writes

- Chaos element star crystals (summoned by the module as `item_display`s, not rig parts): item models
  `rlk:mboss/guardian/star_<k>` for k = 1-4 (active element), 5 / 6 (inert gold / blue), `flash`, `dark`. An upright
  faceted 4-point crystal, 1 b tall at scale 1 and centred: two crossed cards (`gd_star_<k>`, light / mid / dark per
  kind) and a white-hot core cross turned 45 degrees (`gd_star_core`, translucent).
- P4 screen overlay font `rlk:mboss_gd` (`tools/guardian_screen.mjs`): per frame (vig0-vig5, field, diamond) four
  256 x 144 px bitmap tiles drawn at 128 x 72 title units (top row ascent 69, bottom row -3), the flash as one flat
  16 x 9 glyph, and two negative spaces (U+E5F0 = -1 for the advance gaps, U+E5F1 = -257 back to the left edge);
  glyphs U+E500.. The build stops when a codepoint collides with another font of the pack. The manifest's `screen`
  entry holds each frame's title component (used by `tools/mboss_guardian/p34.py`).
