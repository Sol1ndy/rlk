# Raiden rig API (S1-RIG, rd/plan.md §C)

Generator: `node tools/build_raiden_rig.mjs --resourcepack <unpacked pack> [--debug-dp <dir>] [--no-paint]`
(sources `raiden_geometry.mjs`, `raiden_clips.mjs`, `raiden_paint.mjs`; shared RIGLIB untouched). Everything under
`data/rlk/function/boss/raiden/rig/`, `tools/raiden_rig_manifest.json` and the pack's `models|items/raiden/*`
(except `fx_*`) and `textures/raiden/rig/*` is generated: change the sources and rebuild.
The build throws on a floor dip (any shown element of a part or prop below the feet at a compiled tick), a step
violation, a missing event key, element or px budget overruns; `--allow-steps` only turns those into warnings for
authoring.

## Calls (all `@s` = the boss = the rig anchor, at its feet)

| function | what |
|---|---|
| `rig/init` | objectives (safe on every load) |
| `rig/spawn` | kills and summons the 30 parts (fixed UUIDs `524c4b4d-5244-4900-8000-0000000000NN`, tag `rlk_raiden_part` + `rlk_rd_<part>`) in the rest pose of the stored state and queues its idle clip. `rig/tick` calls it when a part is missing. |
| `rig/tick` | once per game tick, `at @s`: respawn if missing, follow, flash countdown, clip step. Does nothing but follow while hidden. |
| `rig/play/<clip>` | queue a clip: its tick 0 is applied by the next `rig/tick` (so event tick *e* lands on the *e*-th `rig/tick` after the call, counting that first one as 0). |
| `rig/start/<clip>` | apply tick 0 now (same game tick), then continue from `rig/tick`. |
| `rig/state/{shogun,tenma,hidden}` | form switch (models + follow list). `hidden` scales every part to 0 where it stands (no teleport, never below the floor) and stops the clip; the next `play`/`start` shows the rig again (each clip's tick 0 enforces its own state). |
| `rig/look/{sword,polearm,tenma}` | weapon / form models; `rdRigW` 0 sword, 1 polearm. `switch_*` clips swap at their `swap` tick. |
| `rig/flash` | hit feedback: body + braid glow for 3 t. |
| `rig/face/player` · `rig/face/track` (≤ 12°/call) · `rig/face/set {yaw:<deg>}` | anchor yaw; the rig follows the anchor's yaw. |
| `rig/prop/<kind>` · `rig/prop/clear` | summon a prop at the execution position and yaw (tags `rlk_rd_prop`, `rlk_rd_prop_<kind>`; the new one also has `rlk_rd_prop_new` until the next prop call). Kinds and scales: manifest `props`. |
| `rig/kill` | remove every part (death cleanup); `rig/cleanup` is the old name of the same call. Props go with `rig/prop/clear`. |

Objectives: `rdRigC` clip id, `rdRigT` clip tick (-1 = queued), `rdRigS` state (0 Shogun, 1 Tenma, 2 hidden),
`rdRigW` weapon, `rdRigF` flash, `rdRigFl`/`rdRigQ*` follow cache, `rdRigY` scratch.

## Clips (manifest `clips`; ticks are played clip ticks — the encounter takes its hit ticks from these)

| id | clip | len | form | events | switches |
|---|---|---|---|---|---|
| 0 | `idle_sword` | 40 loop | shogun | — | |
| 1 | `idle_polearm` | 40 loop | shogun | — | |
| 2 | `blink_out` | 6 | shogun | gone 4 | |
| 3 | `blink_in` | 10 | shogun | appear 0, settle 8 | |
| 4 | `iai_dash` | 36 | shogun | stance 0, flash 6, hit1 18, hit2 24 | |
| 5 | `iai_near` | 28 | shogun | raise 0, flash 10, hit1 22, hit2 28 | |
| 6 | `combo5` | 74 | shogun | cue 0, s1 12, s2 22, s3 34, s4 50, s5 64 | |
| 7 | `disc_cast` | 40 | shogun | cue 0, d1 6, d2 10, d3 18, wave 34 | |
| 8 | `rear_iai` | 30 | shogun | cue 0, hit 14 | |
| 9 | `musou` | 166 | shogun | appear 6, raise 10, arc 20, dark 110, slash 130, end 160 | |
| 10 | `guard` | 20 loop | shogun | — | |
| 11 | `parry` | 6 | shogun | flash 1 | |
| 12 | `counter_sword` | 46 | shogun | cue 0, burst 12, bolts 24, lunge 40 | |
| 13 | `counter_spear` | 26 | shogun | cue 0, star 8, sweep 18 | |
| 14 | `karatake` | 32 | shogun | retreat 0, raise 10, hit 30 | |
| 15 | `switch_sword` | 34 | shogun | hoop 2, vortex 8, burst 20, swap 22 | sword at 22 |
| 16 | `switch_polearm` | 32 | shogun | hoop 0, burst 20, swap 22 | polearm at 22 |
| 17 | `p_4hit` | 76 | shogun | raise 4, star 10, h1 22, h2 32, h3 42, h4 56 | |
| 18 | `p_lance` | 24 | shogun | raise 0, glow 6, hit 14 | |
| 19 | `p_twirl_slam` | 52 | shogun | twirl 0, flash 38, hit 40 | |
| 20 | `p_twirl_dash` | 58 | shogun | twirl 0, d1 20, d2 32, d3 44 | |
| 21 | `p_zigzag` | 64 | shogun | hip 0, star 8, dash 14, ring 34, lunge 52 | |
| 22 | `p_rear` | 36 | shogun | twirl 0, h1 16, h2 26 | |
| 23 | `cast` | 20 | shogun | cast 8 | |
| 24 | `stagger` | 60, loops 20-60 | shogun | — | |
| 25 | `stun_recover` | 24 | shogun | burst 24 | |
| 26 | `transform` | 60 | shogun | rise 4, ring 20, pillars 44, form 50 | Tenma at 50 |
| 27 | `death` | 48 | keeps the form | — | |
| 28 | `t_idle` | 60 loop | tenma | — | |
| 29 | `t_blink_out` | 6 | tenma | gone 4 | |
| 30 | `t_blink_in` | 10 | tenma | appear 0, settle 8 | |
| 31 | `t_combo3` | 70 | tenma | raise 0, sw1 14, sw2 26, cock 42, throw 54, reform 62 | |
| 32 | `t_spin_throw` | 46 | tenma | glint 0, spin 13, throw 31 | |
| 33 | `t_iai` | 40 | tenma | crouch 0, flash 10, hit 22 | |
| 34 | `t_waves` | 70 | tenma | glint 0, swing1 8, swing2 53 | |
| 35 | `t_danjeol` | 80 | tenma | halo 6, raise 10, band 24, slam 64 | |
| 36 | `t_summon` | 24 | tenma | sphere 4, throw 16 | |
| 37 | `t_seed` | 20 | tenma | twirl 0, throw 8 | |
| 38 | `t_vajra` | 30 | tenma | hurl 6, hurl2 12, hurl3 18 | |
| 39 | `t_vanish` | 14 | tenma | gone 14 | |
| 40 | `t_reform` | 20 | tenma | appear 0 | |
| 41 | `t_rush` | 52 | tenma | glint 0, flash 13, rush 23, b1 28, b2 34, b3 40 | |
| 42 | `t_collapse` | 46 | tenma | form 20, kneel 46 | Shogun at 20 |
| 43 | `exhausted` | 60 loop | shogun | — | |
| 44 | `recover` | 28 | shogun | — | |

Non-looping clips hold their last pose until the next `play`. The glaive leaves her hand 3 t before its landing
(`t_combo3` 51, hidden until 62, regrown by 70; `t_spin_throw` 28, hidden until 39, regrown by 46): the encounter flies
it to the locked spot (tm/glaive_fly), landing on the `throw` event.

Swing sync (rd-sync): every attacking clip passes its weapon through the hazard's centre line (or the player's bearing
for a disk / ring round her) at the event tick, within 1 t, through the front (never round her back); the strike
visual's `sm` motion (raiden_kit.hz) follows the same direction. `S/rd/sync/tools/audit.py` measures it from the
compiled poses (`--debug-dp`).

## Model notes for pattern authors

- Shogun: katana in her right hand (low, blade back); the polearm look swaps the weapon models only. Halo arch of
  tomoe orbs behind her; `aura` is a flat floor ring shown by `guard` / `counter_*`.
- Tenma: core figure floats about 1 b up. **The giant arm and its glaive are on her right, the three thin arms
  fan out on her left** (as in footage `frames/B/B_v7_06.90`, `B_v9_03.30`; the plan text says "giant left arm",
  which reads the footage from the viewer's side). Gauntlet hands hover low in front, palms up, ≥ 0.58 b.
- Props (manifest `props`): `eye_orb`, `blade_eye`, `musou_orb`, `vajra`, `flower` (≈ 2 b), `dome` (r 8 b at scale 8,
  grow it by its scale), `clap_l`/`clap_r` (4.5 b translucent hands), `slam_palm`, `glaive_planted`, `seed`, `hoop`,
  `vortex`, `clone_ready`/`clone_slash` (+`_glow`; pivot 1.375 b above the feet, the function lifts it).
- The encounter puts props on screen through `object/create {model:"prop/<model>"}` (eyes, clones, the flower) or
  `rig/prop/<kind>`; the release's item ids (`electro_orb`, `lightning_stake`, `remembrance_flower`, `support_hand_*`)
  were deleted in S3 together with the bridge below.

## Removed in S3

The temporary S1-S2 bridge is gone: `rig/legacy_anim` and `rig/legacy/*` (the release's `rdAnim` ids), the
`judgment_rig/{start,tick,cleanup}` shims (the generator deletes the folder) and `rig/target_slam_*` (release P13).
The encounter calls only `rig/play/<clip>` / `rig/start/<clip>` and hides her with `rig/state/hidden`.

## Tests

`python3 S/rd/tests/test_raiden.py <roguelike> -k rig` (`S/rd/tests/rig_tests.py`): manifest v2 against the plan's
§C.5 table (lengths, loops, event ticks), parts/UUIDs, every called function exists, no negative score amounts, no
downward teleports, the S3 shim removal, all 45 clips run in rdsim, hidden/show/Tenma/death/kill/respawn,
no part below y 201. Renders: `S/rd/renders/rig_*.jpg|png` (debug poses `--debug-dp`: `rd_dbg/<clip>/<t>`,
`rd_dbg/props`, `rd_dbg/dome`, `rd_dbg/weapon_{sword,polearm}`, `rd_dbg/rest_{s,t}`).
