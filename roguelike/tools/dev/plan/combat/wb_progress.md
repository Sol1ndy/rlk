# lane WB (round W: the boss in the fight) — progress

Branch `wip/w-boss` (from `origin/wip/w` 2613c47f0, + the brief's §4 / §5 merged), worktree `<S>/cb/wt_wb`, pack copy
`<S>/rp_wb` (from `<S>/rp_rel3`, the 11-12 release pack). Contract: `w_brief.md` §2 "WB" + §3 + §5 (the trailer
`Claude Opus 5.5`). Scratch `<S>/wb/` (`dbg/` = the rig's debug frames for fightcam, `before/`, `after/` strips, logs).

## Status
- [x] read the briefs, the round V lane (vb_progress), the integration (vi_progress), t3's overview sheets, the fight review
      (`review/w/findings_fight.json`: T3-06 / 08 / 09 / 11 are this lane's)
- [x] the rig track sidecar carries `f0` (the sword's first key ends there: the blend-in before it) and `sp` / `sq` (the sword part's
      translation / rotation as the client shows them each tick) and the top-level `blade` [bladeLo, tip]: `build_scarlet_rig.mjs`
- [x] `blade.py`: round V's path / head / target line / tall mark / static lines and their run-time (`core/sw/aim|march|head`) removed;
      the trail (band, pieces, ribbon, wave) generated from the shown sword
- [x] p1.py / p_ghost.py / core.py / shield.py / s3lib.py wired (every pattern, both gauntlets, the ghost form); the fight hook's ride
      line; core/pp stops it, core/pat_end + core/g/end take what is left; core/cam_ok + core/cam_clear (T3-06)
- [x] kit sprites / models: sw_rib_0..2, sw_quad_0..2 new; sw_arc_0..2 repainted (a wedge with a chord rim: ribbon + ink + faint fill,
      T3-11); sw_path gone; sw_head kept (the flashes' star); models sw_band, sw_rib_k, sw_fan_k (wedge + rim wall), sw_quad_k
- [x] test_blade rewritten (347 checks), test_vi beatpat on the trail, test_kit's sprite pin; all hr suites pass (test_vi rerun)
- [x] fightcam: `trail` measure at 4 / 7 / 10 b on three fields (FOV 90); before / after strips
- [x] full gates (below), docs (README 홍련 + 0-4 / 0-8 lines, hr_design §11), pushed

## Gates (the final tree)
| gate | result |
|---|---|
| regeneration twice (rig -> kit -> bossbar -> `regen_all.sh --mobs`) | round 1 and 2: `git status` of data/ + tools/ empty; pack hash `376a5321ea53` both rounds (the first round on the working pack re-sorted it) |
| other bosses' outputs | byte-identical (`git diff origin/wip/w` outside `boss/scarlet/**`, `tools/`, README: empty; `ident_hr` passes) |
| `check_mboss_pack.py` | 0 problems |
| loadcheck (26.3 server, tag `wbfin`) | 0 function load failures, `Done (` in the log |
| `rplint` / `atlas_px` (`<S>/rp_wb`) | 0 problems / 13 109 184 px (13.109 M) |
| test_blade | 347 / 347 |
| pat_p1 / pat_p2 / pat_ghost | 559 / 70 / 65 |
| test_scarlet / test_metro / test_flow / test_gauge | 48 (P1 505, P2 524 commands per tick) / 30 / 40 / 33 |
| test_clips_h1c / test_kit / test_rig / test_bal_hr | 297 / 15 313 / 162 / 79 |
| test_vi (beatpat on the trail) / ident_hr / gen_check_hr (`--rp`) | 208 / passes / 28 of 28 |
| hrfair 2.0 `--quick --only p1,p2,kill` (seed 11; `<S>/wb/hrfair/run.log`) | P1 / P2 walker intake 237.7 / 239.9 %/min (= round V's quick run: / 타키 232.3 = 1.02 / 1.03), T1b 0.49, T1c 0, T3 1.43, T4 19.0 %, T8 1, T9 walker Lv15 167 s (150-185), T9b 164 s, T10 1.50 / 0, T12 100 %, T13 ok, W35 35 35 34 35 / 35 35 35 32 |

## Job 2 (11-12, the coordinator): re-time the gauntlets for the parry rule without the whiff ladder
Merged `origin/wip/w-player` (47ad3b270: every accepted F locks 12 t, a parry of any tier 1 t, an ignored press blocks F 3 t;
`chainparry.py`). The user chose to re-time the gauntlet cuts only (the lock rule stays). Target: no blind F metronome of any
period 1-40, from any start, gets 5 perfect parries (clear) in G1 / G2.
- Model: `tools/dev/sim/hr/review/metro/fm.c` / `dfs.c` built `-DNOLADDER` (and `-DKMIN=1 -DKMAX=40`); it reproduces lane WP's
  numbers on the old tables (G1 clear by 4 / 6 t; G2 by 3 4 7 13 15 16 t) and test_metro's real-function tables exactly.
- Constraints (the moves' own spacing, as HFA's): G1 gaps >= 14, the D2 reappearance >= the leap's gone + 2 (s4 - s3 >= 23), the
  D1 after the X (s6 - s5 >= 24), D3 >= 8 t after the ring's contact (s7 - s6 >= 24); G2 gaps 14 14 23 21 14 24 14 14 14 14
  (the leap, the ring's vanish, the X); the first cut 22-34, the last <= judge - 24 / - 22 (judges kept).
- **At most 3 everywhere is impossible** under these rules (G1 exhaustive DFS, every period 1-40: 0 sets). At most 4: G1 231 686
  sets (6 364 within 14 t of round V's: picked the one with the fewest periods at 4), G2 rare (random sampling 300 000: none;
  DFS by first-cut range: the nearest found, distance 23 t).
- **G1 31 45 64 88 108 138 163 181 195** (from 30 48 64 91 109 139 163 180 196): best per period
  `1:1 2:1 3:3 4:4 5:3 6:3 7:3 8-14:3 3 3 2 2 3 3 3 15:4 16-18:3 19:4 20-24:3 25:4 26-28:2 29-32:3 3 3 2 33:4 34-40:2` (4 at 4 / 15 / 19 /
  25 / 33 t: 27 / 65 / 39 / 22 / 14 starts).
- **G2 28 46 66 89 112 127 151 170 189 205 219** (from 27 41 58 91 113 128 152 169 190 206 220): best 4 at 3-8, 12-23, 31 t, 3 or
  less elsewhere (892 of ~17 000 (period, start) pairs reach 4); never 5.
- Rows written from the strikes (`api._g1_rows` / `_g2_rows`), judges 220 / 242, dives 202 / 224; G2's extra vanish 96; bolts
  G1 34 96 166 218, G2 70 160 195 240 (off the locks).
- test_metro rewritten to the new rule: periods 1-40, starts from T - 200, at most 4 in both (33 / 33).
- Removed the dead `tag=rlk_hr_sw` line from `player/def/beat/st/tp_on` (lane WP's file, the coordinator's request; the trail's
  riding cards carry `rlk_mb_part`).
- Gates on the re-timed tree: regeneration twice clean (pack `376a5321ea53` both rounds), rplint 0, atlas 13.109 M, check 0,
  loadcheck `wbfin2` 0 failures + `Done (`; test_metro 33/33; chainparry 624/624 (G1 9/9, G2 11/11, smallest gap 14, 0
  exceptions); test_cb 400/400; test_blade 347, pat_p1 559, pat_p2 70, pat_ghost 65, test_scarlet 48, test_flow 40,
  test_clips_h1c 297, test_kit 15 313, test_rig 162, test_bal_hr 79, test_gauge 33, test_vi 208, ident_hr pass; gen_check_hr 28 / 28.
- hrfair 2.0 `--only g,metro,chain`, seeds 11 / 22 / 33 (`<S>/wb/hrfair_g/run.log`): T5 40.3 / T5b 49.3 %; T6 s0 100 % of the F in
  the window, cleared 100 %; T6 s1 in the window 100 %, perfect per timed F 85.0-91.2 % (ceiling 86.6), cleared 100 % (8 / 8 per
  seed); T7 sloppy 0, masher (F every 4 t) 0 (was: G2 cleared in all 3 seeds), dodger 0; T7m metronome 8-30 every phase 0 / 437
  clears in G1 and G2 (most segments taken 4); T13 53 / 53 perfect, 0 refused.

## Design (as built; `blade.py` header and hr_design.md §11)
Nothing is drawn where the blade is going. The trail is generated from the sword the rig SHOWS on the pattern clock (`blade.Shown`:
the clips a pattern plays at their pattern ticks; a clip's ticks before `f0` blend from the transform shown before; hidden ticks
none), the sword part's own transform (`sp` / `sq`) interpolated as the client does (translation lerp, rotation slerp):
- **band** `sw_band` (lance from the guard to the tip, 0.26 b, core 0.146 b + ink both sides): the sword part's translation and
  rotation (x the constant turn of the lance onto its +y); summoned a tick early with no size, sent the next tick's transform each
  tick (1 t interpolation = the rig's keys): exactly on the blade (test_blade: 0.000 b off). From the first known pose to the end
  of the last hit's follow-through (swing b).
- **pieces** (`sw_fan_k` wedge, chord rim; `sw_quad_k` strip): the sweep t -> t + 1 in planar pieces (<= 30 deg / 0.9 b of tip);
  summoned at t with no width at the tick's first blade line (off-plane pieces: at their own first edge), opened on t + 1 (LAG 1:
  one tick behind the blade - a planar piece cannot follow the client's slerp inside a fast tick without being ahead somewhere),
  ride 2 t (then left in the world), fade +3 / +5, gone +7. Rim wall 0.22 b (swing 0.30 b). Swing pieces mixed 55 % to white: the
  round V slash sectors are REPLACED by these (the trail's brightest stretch, one effect).
- **ribbon** `sw_rib_0..2` (0.30 b) on her body's moves that carry the blade (dashes, lunges, dives, the gauntlet approaches /
  A8.3 leap / A8.9 dive): from the hand's place at the move's start, grown on each tick to the marker `rlk_hr_trt` = the hand's place
  one tick back (`core/sw/rib`, `rib1`: length = (marker - origin) . aim): one step behind her model at any clock speed.
- **wave**: a dash-through's line (from the dash start, the probed length) and kcut's 3 lines ON the hit tick, 4 t.
- band + pieces carry `rlk_mb_part` (lane VP's beat: held ticks, the slow motion's stretch passes, the rocked-back tilt); the
  ribbon / wave do not (their origin is not at her feet; the rock would tilt them about a far point). The fight hook rides
  `rlk_hr_trr` to the rig's root part after `rig/tick` (also right after `rig/follow_now`).
- core/pp: band killed, the rest to its last fading frame; core/pat_end + core/g/end: everything left killed.
- **camera (T3-06)**: `core/cam_ok` (her body >= 1.3 b off the segment player eyes -> 4 b behind along the view, 9 sample points),
  used by every stop choice (dash stop 2.0 b / else 3.5 b, `core/near` 1.4 / 2.9 b, MX streak, the gauntlet spots' candidates);
  `core/cam_clear` after the moves (steps 1.8 b right / left / back in 2 t when she stands in that line).

## Measured (fightcam `trail`, 1080p, FOV 90, the F5 lens 3.5 b behind / 0.5 b over the avatar; `<S>/wb/trail_measure.json`)
21 hits (a1, a2, a3 h1/h4, d4 h1/h3, tri h1, rings r1, a4, a9, a10, hcut, kcut, ult cut1, mx x/dome, nb b1, q_air beam, g_rise,
g_sweep, g_vert) at 4 / 7 / 10 b on three fields (P1 floor, P1 wheat = the floor painted straw 214,196,146, P2 crimson), at the
hold (w + 2), the hit tick and 2 t after:
| D | band width px min / median | trail px (median: hold / swing / after) | contrast median (P1 / wheat / P2) | share of trail px with ratio >= 1.5 (median, P1 / wheat / P2) |
|---|---|---|---|---|
| 4 b | 15.1 / 17.6-21.5 | 5452 / 3100 / 11476 | 2.38-2.56 / 1.56-1.59 / 2.07-3.01 | 0.75-0.88 / 0.51-0.79 / 0.69-0.82 |
| 7 b | 11.7 / 13.1-14.1 | 2732 / 1196 / 4436 | 2.37-2.55 / 1.84-2.22 / 2.31-2.89 | 0.72-0.84 / 0.59-0.76 / 0.68-0.78 |
| 10 b | 8.8 / 10.1-10.6 | 1504 / 756 / 2404 | 2.48-2.68 / 1.96-2.23 / 2.36-3.01 | 0.74-0.83 / 0.59-0.76 / 0.71-0.78 |
(round V's line in play, review T3-08: 2-7 px, not separable from the wheat.) Visible share (her body / the avatar in front): 0.71-0.90.
Colour: CIE ΔE white-gold vs straw 15 (white 34, cyan 48, yellow 47, purple 90, blue 79); kept white-gold (P) / the flash colour
(N) - the cue star's family, and a pale cyan would sit next to the blue flash's meaning - and gave every bright core ink on both
sides so it reads by its border on the wheat (the wheat rows above).
test_blade: the worst point of a trail card ahead of the blade (off the way it has come by more than 0.10 b AND nearer the way it
is going) 0.100 b (limit 0.10); beside the true curved sweep at most 0.183 b; the band 0.000 b off the blade.

## Costs
- commands per tick (test_scarlet, 1200 t): P1 505, P2 523 (round V 500 / 519, the 11-11b base 435 / 441): + 5 / + 4 (1 %) over
  round V - the ride line every fight tick (1) and the pieces (2 per piece + detach / fades / kill per tick) replace round V's
  path cards, its head's per-tick tp and the target line's aims (64 x 3 on <= 6 ticks). test_flow 40/40 (budget 830).
- trail cards alive in a pattern: at most 29 (round V's sweep cards: 48).
- atlas: 13 109 184 px (13.109 M <= 13.2 M; +1 280 px over 11-12: sw_rib 3 x 256 + sw_quad 3 x 256 - sw_path 256); kit sprites
  259 584 of 260 000.

## Decisions / deviations
- **One tick behind**: the pieces open one tick after the blade passed (LAG 1), not with it: the client slerps the sword part's
  rotation (a cone, the pivot moving) and a planar piece opening with it lies up to 0.4 b ahead of the blade mid-tick in fast cuts.
  The band on the blade is exact and is the trail's head, so the trail never lags off the blade; the gap is the current tick's sweep.
- **The wedge has a chord rim** (not a circle): a sector sprite squeezed to each piece's angle bulges 10 % past the tip's way.
- **The first ticks of a pattern**: the pose she comes from is not known at build time, so the trail starts at the first clip's
  `f0` (1-3 t); every hit's wind-up (>= 10 t) is covered (test_blade `present`).
- **Kept white-gold** with ink on both sides (above).
- **`rlk_mb_part` on the band / pieces** (to be held / slowed / tilted by lane VP's beat like her rig) - not on the world cards.
- **T3-06**: the camera's real place is known only through the player's view (eyes + 4 b back, the seat's d 3.5 b); the stop is
  chosen at the move's start, the step out after it covers a player who moved since (a dodge back-step moves the camera away from her).
- **T3-11**: the slash sheet is gone (the swept piece is a bright ribbon at the tip's way, a faint fill inward, gone 7 t after it
  opened); the beat's freeze still holds it with her (w_brief §2.3: the trail follows the pattern clock).
- **T3-09**: the trail is on the blade (cannot move); the cue star stays over her hat when the blade is low (round V). Player-side
  clutter (damage numbers ~150 px, smoke, flames over her) is not this lane's file: request below.

## Requests to other lanes / the lead
- **WP**: `player/def/beat/st/tp_on`'s line for `tag=rlk_hr_sw` is dead now (no round V card rides any more); the trail's riding cards
  carry `rlk_mb_part` and are taken by the part lines. The new plain dodge moves the camera with the player: her stops are re-checked
  after each move (`core/cam_clear`).
- **Lead / player FX**: during her wind-ups the player's own effects and damage numbers (review w T3-09: up to ~150 px over her)
  hide the trail and the cue: smaller / translucent numbers near a boss, or none between the camera and her for ~12 t before her hits.

## Pack files (`<S>/rp_wb` vs `<S>/rp_rel3`; all from the generators)
- added: `assets/rlk/textures/mboss/hr_kit/{sw_rib_0,sw_rib_1,sw_rib_2,sw_quad_0,sw_quad_1,sw_quad_2}.png`, models and item
  definitions `mboss/hr_kit/{sw_band,sw_rib_0..2,sw_fan_0..2,sw_quad_0..2}.json`
- changed: `textures/mboss/hr_kit/sw_arc_{0,1,2}.png` (the wedge), `assets/minecraft/atlases/items.json`
- removed: `textures/mboss/hr_kit/sw_path.png`, models / items `mboss/hr_kit/{sw_path,sw_arc_0..2}.json`

## Strips (scratch)
- before (round V as built: `origin/wip/w`'s tree + the 11-12 pack, the same lens, FOV 90): `<S>/wb/before/{a3_D5,a9_D7,mx_D7_p2,
  g1_cuts_16-52,a10_D7}.jpg`; the recording: `<S>/cb/video3/rev_fight/evidence/E7_blade_path_line_P2.jpg`, `E3_*`, `E8_*`
- after: `<S>/wb/after/{a3_D5,a1_D4,a9_D7,a10_D7,kcut_D7,mx_D7_p2,rings_D6,g1_cuts_16-52,g1_plunge_196-222}.jpg` (the real
  patterns in the H1 world), `a1_D6_p1.jpg`, `a1_D5_p1w.jpg`, `a1_D5_p2.jpg` (one hit, the three fields)

## How to run
See vb_progress.md "How to build / run" (same tools); the debug frames for fightcam:
`node tools/build_scarlet_rig.mjs --resourcepack $S/rp_wb --debug-dp $S/wb/dbg --debug-clips $(cat $S/vb/fight_clips.txt)`;
`python3 -I tools/dev/sim/hr/vb/fightcam.py <wt> --dbg $S/wb/dbg --rp $S/rp_wb trail --json m.json` (the measure, ~40 min);
suites `<S>/wb/suites.sh [names]`, gates `<S>/wb/gates.sh` (regen twice, rplint, atlas, check, loadcheck).
