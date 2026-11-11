# lane VB (round V: the boss in the fight) — progress

Branch `wip/v-boss` (from `origin/wip/v` d7e7cf013), worktree `<S>/cb/wt_vb`, pack copy `<S>/rp_vb` (from `<S>/rp_fin`).
Contract: `v_brief.md` §3 "VB" (1-6) + §4. Scratch `<S>/vb/`: `before/` + `after/` (strips), `dbg/` (the rig's debug frames),
`sim/` (the suites' copy), `measure_{4,7,10}.json`, `gates.out`, `suite_logs/`.

## How to build / run
```bash
S=<scratchpad>; WT=$S/cb/wt_vb/roguelike; cd $WT
node tools/build_scarlet_rig.mjs --resourcepack $S/rp_vb [--debug-dp $S/vb/dbg --debug-clips <fight clips>]   # writes tools/scarlet_blade_track.json too
python3 tools/build_mboss_hr_fx.py --resourcepack $S/rp_vb && python3 tools/build_bossbar.py --resourcepack $S/rp_vb && bash tools/dev/regen_all.sh .
bash $S/vb/simcopy.sh                        # the suites' copy $S/vb/sim (hr1_progress.md "How to run"); then cd $S/vb/sim/hr/tests
python3 test_blade.py $WT                    # the new suite
F="python3 -I $S/vb/sim/hr/vb/fightcam.py $WT --dbg $S/vb/dbg --rp $S/rp_vb"
$F strip --clip a3 --event h1 --dist 7 --field p1 --tells -o x.jpg                  # one hit: her rig + the avatar + path / slash / cue
$F fight --sim $S/vb/sim --key a9 --dist 7 --from 14 --to 31 -o x.jpg              # the generated pattern run in the H1 world
$F measure --dist 7 --json m7.json                                                 # the pixel measures (12 s per hit)
python3 -I tools/dev/sim/hr/vb/windups.py $WT [--track <blade_track.json of an --only build>]
```
Clip authoring loop: `node tools/build_scarlet_rig.mjs --resourcepack <throwaway rp> --datapack <scratch dp> --only a,b` (10-40 s; prints
`contacts <clip>` and writes `<scratch dp>/blade_track.json`), then `windups.py <wt> --track <that>`; a full rig build is 2.5 min.

## What is built (v_brief §3 VB)
1. **Wind-ups** (`tools/scarlet_clips.mjs`): every hit's wind-up pose is reached >= 10 t before a single / first hit, >= 6 t before a
   chain follow-up, and held to the swing (table below; `test_blade.py` `windup`). Reworked: a1 (wide, high at her right from 4; the
   rising-fan flourish is gone), a2 (high at 2, blend 2), a3 h1 (raised at 4) / h2 (23) / h5 (62), a4 (the blade raised at the apex),
   d4 h1 (4) / h4 (47), tri h0 (4) / h2 (42), rings r1 (4), blue (chamber at 12), mx dome (swirl at 21), nb b2 (24) / b3 (34), and the
   gauntlet: g_dash / g_glide / g_drop / g_run hold the next cut's wind-up from their first shown tick, g_sweep / g_wrap / g_dome
   end in the next cut's wind-up, g_rise without its spin, g_vert a falling cut from the raised blade, g_dive 22 t (the wind-up
   held 0-14 in view). **The blade**: look `edge` (model `glow_edge`: the glow sheath CROSSED about the blade's axis, 0.13 b wide;
   every glow look got the crossed form), set by the core for the fight phases / every pattern start, `off` for locked cutscenes.
2. **The drawn blade path** (`tools/mboss_scarlet/blade.py`; kit cards `sw_path` 0.24 b wide with a 0.134-b bright core and a dark
   rim, `sw_head`): generated from `tools/scarlet_blade_track.json` (the rig build's sidecar: blade base / tip per clip tick).
   A swing: the tip's way from the swing's start to the hit as straight pieces (<= 30 deg of blade turn each), riding her; shown 12 t
   before a single / first hit, 8 t before a chain hit; the head is sent each pattern tick to where it shall be one tick later
   and reaches the tip's place of the hit tick ON the hit tick; from the swing's start the path burns white (the tip's trail).
   A dash / plunge (her body carries the blade): the target line from her (blade height / her blade's tip) to the target, aimed
   at the player each tick until the lock, then at the lock marker; its length is measured in the game (`core/sw/march`); a dash
   also gets the tall mark over the locked spot (it runs straight at the lens). kcut's three lines and nb's bands: static path
   cards through the locked spot from the lock on. Gauntlet cuts: the path stands at the cut's station. Colours: P white-gold
   #FFE9A8, N its flash's (yellow #FFE14A, purple #D68BFF, blue #5AA8FF).
3. **Slash effects** (`blade.slash`; kit cards `sw_arc_0..2`): per <= 45 deg of blade sweep one sector card whose apex is the point
   nearest both bounding blade lines, lying in their plane, its rim on the tip's way; born on the pattern tick the sweep is
   shown, fading through two frames, gone 6 t later. Every hand-placed qi_* call at a hit is gone from p1.py / p_ghost.py.
4. **Off-screen / camera**: `LEAP_H` 3.4 (q2 3.6); A4 / A10 stay 3 b from the player in the air; dash-throughs stop 2.0 b before the
   locked spot (`core/near`, `p/<key>/dash`), dives land 1.4 b before it; gauntlet stations 2.2 b at +35 (front right), fixed 10 t
   before the strike (marker `rlk_hr_gst`), A8.3 leaps to 1.3 b before the player; the dive reappears 18 t before the judge 3 b over
   a spot 4.5 b before the player and ends over the spot 2 b before them; the fail's column is a 0.3-b path card for 5 t.
5. **The gauge**: `#buSubSeg bu 5` -> four dividers over the under bar (`tools/build_bossbar.py`, glyph U+E440 3 x 7 px).
6. **Balance**: hit ticks / shapes / tiers / weights untouched; pat_p1 / pat_p2 / pat_ghost / test_bal_hr / test_metro / test_gauge /
   test_flow pass unchanged. hrfair 2.0 `--quick --only p1,p2,kill` (seed 11; `<S>/vb/hrfair/run.log`): P1 / P2 walker intake
   237.7 / 239.9 %/min (÷ 타키's 232.3 = 1.02 / 1.03; T1 1.00-1.15, T2 <= 1.25), T1b 0.49, T1c 0, T3 1.43, T4 19.0 %, T8 1,
   T9 walker Lv15 168 s (150-185), T9b 164 s (125-170), T10 1.50 / 0 (0.8-1.6), T12 100 %, T13 ok, the 35 % rule 35 35 34 35 /
   35 35 35 32: where the 11-11b table had 161-171 s and 162 s. The full three-seed run (~50 min) was not repeated.
Also: the cue star `cue_0` with a dark rim, 1.9 -> 2.3 b, placed from the track (`blade.cue_point`: the blade's middle, or 0.9 b over
her hat's crown when that is under 1.75 b or on the hat); the flashes at her head (not her chest), yellow 2.4 / 3.0 b, purple 2.4 b,
blue 2.6 b, each with a dark-rimmed star (`sw_head`) inside.

## Measured (fightcam.py `measure`, 1080p, FOV 70, the F5 lens 3.5 b behind the pivot 0.5 b over the avatar's head, aimed at her chest)
Columns: the wind-up's lead; the pixels of the frame that differ between the wind-up pose and the stance (avatar in frame) at
4 / 7 / 10 b and their share of her visible figure; the blade edge's least width from any side (0.092 b) when she is 6 / 7 / 10 b
from the avatar; what is drawn and for how many ticks before the hit; the path's (line's) width at 7 b; the share of the cue star
(P) / the flash sphere (N) her hat, her body and the avatar leave visible at 7 b; the worst angle between a shipped slash piece's
plane and the blade positions that bound it.

| hit | P/N | wind-up held (t before hit; rule) | pose px that differ from the stance at 4 / 7 / 10 b (share of her figure) | blade edge, least width px at 6 / 7 / 10 b | what is drawn: lead t | path width px at 7 b | cue star seen / flash seen at 7 b | slash plane vs blade (deg, worst piece as shipped) |
|---|---|---|---|---|---|---|---|---|
| a1 a1.hit @14 | P | 11 (10) | 17091 / 9586 / 6226 (1.22 / 1.20 / 1.18) | 6.9 / 6.3 / 5.0 | path on the blade: 12 | 16.8 | star 1.00 | 0.01 (13 pieces) |
| a2 a2.hit @12 | P | 10 (10) | 12262 / 7075 / 4727 (0.87 / 0.89 / 0.90) | 6.6 / 6.0 / 4.8 | path on the blade: 12 | 16.8 | star 1.00 | 0.01 (14 pieces) |
| a3 a3.h1 @14 | P | 10 (10) | 14259 / 7638 / 4916 (1.02 / 0.96 / 0.93) | 6.8 / 6.2 / 4.9 | path on the blade: 12 | 19.4 | star 1.00 | 0.01 (8 pieces) |
| a3 a3.h2 @30 | P | 8 (6) | 11102 / 6213 / 4039 (0.79 / 0.78 / 0.77) | 6.5 / 6.0 / 4.8 | path on the blade: 8 | 16.4 | star 0.88 | 0.01 (9 pieces) |
| a3 a3.h3 @45 | P | 14 (6) | 16092 / 8947 / 5757 (1.15 / 1.12 / 1.09) | 8.7 / 7.8 / 5.9 | path on the blade: 8 | 18.1 | star 1.00 | 0.01 (7 pieces) |
| a3 a3.h4 @57 | P | 8 (6) | 12264 / 6685 / 4382 (0.87 / 0.84 / 0.83) | 7.4 / 6.7 / 5.2 | path on the blade: 8 | 21.0 | star 1.00 | 0.05 (12 pieces) |
| a3 a3.h5 @69 | P | 8 (6) | 16550 / 9291 / 6117 (1.18 / 1.17 / 1.16) | 6.3 / 5.8 / 4.7 | path on the blade: 8 | 14.1 | star 1.00 | 0.01 (12 pieces) |
| a4 a4.hit @20 | P | 13 (10) | 14908 / 8849 / 5908 (1.06 / 1.11 / 1.12) | 6.5 / 5.9 / 4.7 | line to the target: 12 | 15.5 | star 0.85 | 0.01 (24 pieces) |
| a4 a4.hit2 @34 | P | 9 (6) | 17359 / 9773 / 6404 (1.24 / 1.23 / 1.22) | 7.3 / 6.6 / 5.2 | path on the blade: 8 | 16.3 | star 0.99 | 0.14 (8 pieces) |
| a9 a9.cut @28 | N | 18 (10) | 17450 / 9855 / 6484 (1.24 / 1.24 / 1.23) | 6.5 / 6.0 / 4.8 | line to the target: 12 | 15.6 | flash 0.73 | 0.01 (14 pieces) |
| a10 a10.hit @22 | N | 16 (10) | 19349 / 10956 / 7145 (1.38 / 1.38 / 1.36) | 8.0 / 7.2 / 5.5 | line to the target: 12 | 18.7 | flash 0.78 | 0.01 (6 pieces) |
| d4 d4.h1 @14 | P | 11 (10) | 13709 / 7995 / 5305 (0.98 / 1.00 / 1.01) | 6.8 / 6.2 / 4.9 | path on the blade: 12 | 16.4 | star 1.00 | 0.01 (20 pieces) |
| d4 d4.h2 @34 | P | 14 (6) | 16112 / 9051 / 5863 (1.15 / 1.14 / 1.11) | 8.7 / 7.8 / 5.9 | path on the blade: 8 | 18.3 | star 1.00 | 0.01 (7 pieces) |
| d4 d4.h3 @44 | P | 7 (6) | 13560 / 7323 / 4704 (0.97 / 0.92 / 0.89) | 7.4 / 6.7 / 5.2 | path on the blade: 8 | 20.5 | star 0.97 | 0.02 (13 pieces) |
| d4 d4.h4 @54 | P | 7 (6) | 15897 / 9135 / 6045 (1.13 / 1.15 / 1.15) | 6.6 / 6.0 / 4.8 | path on the blade: 8 | 18.7 | star 1.00 | 0.01 (11 pieces) |
| tri tri.h0 @14 | P | 11 (10) | 16692 / 9320 / 6166 (1.19 / 1.17 / 1.17) | 8.5 / 7.6 / 5.8 | line to the target: 12 | 19.9 | star 0.99 | 0.00 (0 pieces) |
| tri tri.h1 @38 | P | 14 (6) | 12732 / 7575 / 4992 (0.91 / 0.95 / 0.95) | 7.3 / 6.6 / 5.2 | path on the blade: 8 | 18.4 | star 1.00 | 0.01 (12 pieces) |
| tri tri.h2 @48 | P | 6 (6) | 14066 / 8076 / 5293 (1.00 / 1.01 / 1.01) | 6.6 / 6.1 / 4.8 | path on the blade: 8 | 17.1 | star 1.00 | 0.01 (13 pieces) |
| tri tri.h3 @60 | P | 6 (6) | 14265 / 8288 / 5392 (1.02 / 1.04 / 1.02) | 7.3 / 6.6 / 5.1 | path on the blade: 8 | 18.6 | star 1.00 | 0.02 (11 pieces) |
| rings rings.r1 @14 | P | 11 (10) | 14514 / 8420 / 5529 (1.03 / 1.06 / 1.05) | 6.8 / 6.2 / 4.9 | path on the blade: 12 | 16.4 | star 1.00 | 0.01 (22 pieces) |
| rings rings.r2 @24 | P | 6 (6) | 15150 / 8815 / 5724 (1.08 / 1.11 / 1.09) | 6.7 / 6.1 / 4.9 | path on the blade: 8 | 16.6 | star 1.00 | 0.01 (22 pieces) |
| rings rings.r3 @34 | P | 6 (6) | 14492 / 8407 / 5525 (1.03 / 1.06 / 1.05) | 6.8 / 6.2 / 4.9 | path on the blade: 8 | 16.4 | star 1.00 | 0.01 (22 pieces) |
| rings rings.r4 @44 | P | 6 (6) | 15150 / 8815 / 5724 (1.08 / 1.11 / 1.09) | 6.7 / 6.1 / 4.9 | path on the blade: 8 | 16.6 | star 1.00 | 0.01 (22 pieces) |
| rings rings.r5 @54 | P | 6 (6) | 14492 / 8407 / 5525 (1.03 / 1.06 / 1.05) | 6.8 / 6.2 / 4.9 | path on the blade: 8 | 16.4 | star 1.00 | 0.01 (21 pieces) |
| ult ult.cut1 @24 | N | 19 (10) | 17072 / 9473 / 6259 (1.22 / 1.19 / 1.19) | 6.4 / 5.9 / 4.8 | path on the blade: 12 | 16.0 | flash 0.74 | 0.01 (12 pieces) |
| ult ult.cut2 @46 | N | 20 (10) | 17614 / 9926 / 6562 (1.25 / 1.25 / 1.25) | 6.7 / 6.2 / 4.9 | path on the blade: 12 | 19.4 | flash 0.76 | 0.01 (12 pieces) |
| hcut hcut.cut @26 | N | 21 (10) | 18187 / 10128 / 6684 (1.29 / 1.27 / 1.27) | 6.5 / 6.0 / 4.8 | line to the target: 12 | 15.5 | flash 0.64 | 0.01 (11 pieces) |
| blue blue.hit @22 | N | 11 (10) | 15694 / 8912 / 5741 (1.12 / 1.12 / 1.09) | 8.7 / 7.8 / 5.9 | line to the target: 12 | 20.3 | flash 0.74 | 0.00 (1 pieces) |
| kcut kcut.cut @22 | N | 19 (10) | 17174 / 9414 / 6251 (1.22 / 1.18 / 1.19) | 6.4 / 5.9 / 4.7 | line to the target: 12 | 15.4 | flash 0.67 | 0.04 (15 pieces) |
| mx mx.x @16 | N | 13 (10) | 17750 / 9746 / 6359 (1.25 / 1.23 / 1.24) | 6.3 / 5.8 / 4.7 | line to the target: 12 | 15.1 | flash 0.68 | 0.04 (20 pieces) |
| mx mx.dome @28 | P | 7 (6) | 13856 / 7552 / 4925 (0.97 / 0.95 / 0.96) | 8.3 / 7.4 / 5.6 | path on the blade: 8 | 16.3 | star 0.93 | 0.01 (18 pieces) |
| nb nb.b1 @20 | P | 13 (10) | 21158 / 12012 / 7816 (1.49 / 1.51 / 1.52) | 8.1 / 7.3 / 5.6 | path on the blade: 12 | 21.7 | star 1.00 | 0.01 (11 pieces) |
| nb nb.b2 @30 | P | 6 (6) | 22145 / 12357 / 7894 (1.56 / 1.56 / 1.54) | 7.5 / 6.8 / 5.3 | path on the blade: 8 | 20.0 | star 1.00 | 0.02 (11 pieces) |
| nb nb.b3 @40 | P | 6 (6) | 20384 / 11643 / 7454 (1.43 / 1.47 / 1.45) | 8.5 / 7.7 / 5.8 | path on the blade: 8 | 21.3 | star 1.00 | 0.01 (6 pieces) |
| q q_grab.grab @20 | N | n/a (her hand) | 15921 / 8662 / 5545 (1.12 / 1.09 / 1.08) | 6.3 / 5.8 / 4.7 | line to the target: 12 | 15.1 | flash 0.77 | 0.00 (0 pieces) |
| q q_air.beam @43 | P | 13 (6) | 21655 / 12218 / 7826 (1.52 / 1.54 / 1.53) | 7.7 / 6.9 / 5.3 | line to the target: 12 | 18.0 | star 1.00 | 0.02 (8 pieces) |
| q q_air.hit @59 | P | 9 (6) | 24856 / 13245 / 8391 (1.75 / 1.67 / 1.64) | 7.8 / 7.1 / 5.5 | line to the target: 8 | 18.4 | star 1.00 | 0.17 (2 pieces) |
| q q_air.pillar @95 | N | 23 (10) | 22603 / 12082 / 7805 (1.59 / 1.52 / 1.52) | 7.4 / 6.7 / 5.2 | line to the target: 12 | 17.4 | flash 0.63 | 0.01 (7 pieces) |

Gauntlet cuts (chain-aware, `test_blade.py`): the wind-up pose shown before each cut >= 6 t (the approach / the move before), the
path at the station >= 10 t for a cut after an approach, >= 6 t else; slash pieces <= 0.2 deg off the blade.
Contrast (WCAG ratio) of a tell's dark rim / white-gold core: P1 rim vs straw grass 10.7, rim vs her hat 15.4, core vs floor 6.0
(core vs straw 1.4: the rim carries it); P2 core vs floor 9.4, core vs grass 7.0 (rim vs floor 1.6: the core carries it).

## Costs
- commands per tick (mean): test_scarlet P1 499, P2 518 (were 435 / 441); test_flow the whole fight 370 (360), G1 397, G2 407 (budget 830).
  Sweep command lines: 3.8 per pattern tick on average; a target line's aim = <= 64 x 3 commands on <= 6 ticks of a dash / dive.
- display entities: sweep cards alive at once <= 48 (rings; a8 / a13 24, a3 18); the rig's parts and elements at rest unchanged (29 / 224).
- atlas: 12 958 208 px (12.958 M <= 13.2 M): + 16 640 kit (sw_path 256, sw_head 4 096, sw_arc 3 x 4 096) + 2 048 rig (glow_edge).
  Kit sprites 258 304 of 260 000.

## Gates (the final tree; `<S>/vb/gates.out`)
| gate | result |
|---|---|
| build twice (rig -> kit -> bossbar -> `regen_all.sh --mobs`) | identical: pack hash `10526f69dc46`, git tree clean after both; other bosses' outputs untouched |
| `check_mboss_pack.py` | 0 problems |
| loadcheck (26.3 server, tag `vbfin`) | 0 function load failures, server started |
| rplint / atlas_px (`<S>/rp_vb`) | 0 problems / 12 958 208 px |
| new suite | test_blade 7 812 / 7 812 |
| hr suites | pat_p1 559, pat_p2 70, pat_ghost 65, test_scarlet 47, test_metro 30, test_flow 40, test_clips_h1c 297, test_kit 15 262, test_rig 162, test_bal_hr 79, test_gauge 33, test_input_hr 17, test_special_hr, test_reward, test_seq, test_cine 159, test_contact 94, test_actor 158, test_arena_hr 94, test_moon 55, test_hwamu 283, ev_dry 82, ident_hr: all pass |
| test_cam | 1 check fails (D1 "only the shared files change": `bossui/draw`, `bossui/sub` = this lane's gauge dividers; `load.mcfunction` = the 11-11b build stamp, already failing on `wip/v`). Lane VC's suite: see Requests |
| gen_check_hr (`--rp`, seven rig builds) | 28 / 28 (its rig owner list now names `tools/scarlet_blade_track.json`) |

Suites touched: `test_kit.py` (the pins of the hand-placed effects / sizes rebased on round V), `test_cine.py` (g_dive's last tick 22),
`ident_hr.py` (allow `bossui/draw`, `bossui/sub`), new `test_blade.py`.

## Decisions / deviations (and why)
- **Dashes straight at the player**: their way is seen end-on behind the avatar, so a line along it shows nothing. Kept the line
  (it reads from any other angle) and added the tall mark over the locked spot with a head coming down it.
- **Stop short, hazard unchanged**: the dash-throughs stop 2.0 b before the locked spot (ruling 4) but their hazard keeps the probed
  line through the spot and beyond: the cut's slash is at the blade's reach (ruling 3), the rest of the line is told by the target
  line burning white on the hit tick. Not shortened: it would change the hit's shape (ruling "shapes do not change").
- **"At the blade's reach"**: the slash pieces end at the tip; discs / sectors of api.HITS reach up to ~1 b further (rings 2.6 b vs
  the tip at ~2.0 b). Their reach is not drawn bigger than the blade (ruling 3 wins).
- **Slash tolerance**: a piece's rim lies within 0.12 b of the tip's way (the two bounding radii are averaged), its plane within 4
  deg (measured <= 0.2 deg).
- **The cue star is not always on the blade**: low or on-hat blades put it over her hat's crown (ruling: not on the white hat,
  visible; hr_design said "at her blade").
- **Flashes at her head**, not her chest: the avatar's own head covers her chest from the lens when the player aims at her.
- **g_dive's contract** changed (len 10 -> 22, dive 3 -> 15, hit 6 -> 18) and both scripts' dive rows (214 -> 202, 236 -> 224): the
  judge ticks are unchanged. `FAIL5_T['reappear']` 224. g_vert's rise is cut 2 t before the dive's reappearance (burst + hidden).
- **g_vert** cuts down (was a rising cut from a low crouch): its wind-up must be the pose g_dome's tail holds (g_dome is followed
  by g_dome or g_vert).
- The blade track is the SOLVED frame per tick (the shipped keys are within 0.02 b / 0.5 deg of it: the rig's TOL).
- `tools/build_scarlet_rig.mjs` (no owner in v_brief): the track export, the `contacts` authoring print; `scarlet_geometry.mjs` /
  `scarlet_paint.mjs`: the crossed glow, `glow_edge`. `tools/build_bossbar.py` (the gauge drawing): `#buSubSeg`.
- Before strips: the "before" effects are the user's recording (the review's strips); only the 11-11b POSES were re-rendered from
  the same virtual lens (the old kit's cards run on the kit's game-clock engine, which fightcam.py does not replay).

## Requests to other lanes
- **VP (the beat)**: every path / head / slash command sits on a pattern tick (`p/<key>/k/<t>`, `#pt hr`): freeze or slow `#pt` and
  they stay in step. Their 1-tick client interpolations (`teleport_duration:1` of the path cards and heads) finish in real time:
  if you stretch display interpolation during the beat, the cards are `@e[type=item_display,tag=rlk_hr_sw]` (heads also
  `rlk_hr_swh` / `rlk_hr_swlh`); set their `teleport_duration` to your stretch and back to 1. The kit's own cards (cue star,
  flashes: `rlk_hr_fx`) still run on the game clock (the kit's ager), as before.
- **VC**: (1) `test_cam.py` D1's SHARED list: add `bossui/draw`, `bossui/sub` (and it already fails on `load.mcfunction`, the
  release stamp). (2) `repel` starts from g_dive's last pose: unchanged (test_cine passes with the new last tick 22); at the judge
  she is now 1 b over a spot 2 b before the player (was over the player): `seq/repel` places her itself (R0), nothing to do.
  (3) the core now calls `look/blade/off` when a locked sequence starts and `look/blade/edge` for the lead-ins / the fight: a
  cutscene that wants a glow sets it as before.
- **Lead**: api.py is touched in `LOOKS['blade']`, `KIT_SPRITES_HR`, the two scripts' dive rows, `FAIL5_T`, `REAPPEAR`, `LEAP_H`,
  `CLIPS_PLAN['g_dive']`; `stub_rig_manifest.json` regenerated (`--write-stub`).

## Pack files (`<S>/rp_vb` vs `<S>/rp_fin`; all from the generators)
- added: `assets/rlk/textures/mboss/hr_kit/{sw_path,sw_head,sw_arc_0,sw_arc_1,sw_arc_2}.png` + their `models/item/mboss/hr_kit/*.json`
  and `items/mboss/hr_kit/*.json`; `assets/rlk/textures/mboss/scarlet/glow_edge.png` + `models/item/mboss/scarlet/glow_edge.json`,
  `items/mboss/scarlet/glow_edge.json`; `assets/rlk/textures/font/bossbar/seg.png`
- changed: `assets/rlk/textures/mboss/hr_kit/cue_0.png` (dark rim), `assets/rlk/models/item/mboss/scarlet/glow_{lilac,pink,violet,gold}.json`
  (crossed), `assets/rlk/font/bossbar.json` (the divider glyph), `assets/minecraft/atlases/items.json` (the new sprites' sources)

## Before / after strips (scratch)
- before (the recording, copied from `<S>/cb/video2/rev_fight/`): `<S>/vb/before/{attack_97s_strip,slash_boss_97s,slash_boss_79s,slash_boss_92s,unparriable_leap_82s,attack_94s_leap_strip,gauntlet1_end_163s,unparriable_blue_84s,gauntlet_glint_check,glint_native_p1_p2_g1}.jpg`;
  the 11-11b poses from the same virtual lens: `<S>/vb/before/pose_a1_D5.jpg`, `pose_a3h1_D5.jpg`
- after: `<S>/vb/after/pose_a1_D5.jpg`, `pose_a3h1_D5.jpg` (C1 / S1: the wind-up, the path, the cue star, the slash), `a3_D5.jpg` (the
  whole chain), `a4_leap.jpg`, `a10_leap.jpg` (C4: in frame, the line from her blade to the player), `blue_D6.jpg`, `flash_blue_D5.jpg`
  (C5), `g1_cuts_16-50.jpg` (G1: the station's path while she is still far away), `g1_plunge_196-222.jpg` (G2: the dive; rendered
  before the fix that keeps her shown through the dive's wind-up); side by side: `<S>/vb/cmp_pose_a1_D5.jpg`

## Next (open)
- hrfair 2.0 in full (three seeds, the gauntlet rows T5-T7; ~50 min): only the quick run above was made. The gauntlet rows depend
  on the cuts' strike ticks and the F rules, neither of which changed (test_metro 30 / 30).
- test_cam D1 (lane VC's list).

## What only a person in the game can check
- The path / head / slash as real display entities: brightness against both fields, the 1-tick interpolation of the riding cards
  (do they trail her by a tick when she steps or spins?), the head's arrival feeling "on the hit".
- The slash's look: sector pieces with visible seams ("petals") on fast spins; whether 6 t is too long / short.
- The blade's edge sheath in motion (too thick up close? it is 0.13 b), in the ghost form (lilac).
- Stopping 2 b short on the dashes: does the cut still feel like a dash-through; her being in frame after it.
- Leaps at 3.4 b: in frame with a normal camera pitch; a player who looks far down still loses her.
- Gauntlets: the station's path appearing before she arrives (is it clear that it is HER coming cut); the 15-t dive wind-up.
- The gauge's dividers at the player's GUI scale; the thin fail column.
- With lane VP's beat: path, head and slash freezing with her.
