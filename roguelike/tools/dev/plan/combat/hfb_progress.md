# fix lane HF-B (홍련 rebuild: the cutscenes, review H-B) — progress

Branch `wip/combat-hfb` (from `origin/wip/combat-hi` d7da75e79), worktree `<S>/cb/wt_hfb`, pack copy `<S>/rp_hfb` (from `<S>/rp_hi`),
`<S>` = the scratchpad of `h_common.md`. Brief: fix HB-01 … HB-07 of `review/findings_HB.json` as ruled in `review/rulings_HB.md`
(both on `origin/wip/combat`). Owns: `tools/mboss_scarlet/{seq,cam}.py`, `tools/scarlet_cine.mjs`, the actor
(`tools/player_motion/cine/**`, `tools/build_player_cine.mjs`), FN-cam (`mboss/cam/*` in `build_mboss_core.py` / `mboss_lib.py`),
the cutscene suites and tools. Not this lane's: `core.py`, `p1.py`, `p_ghost.py`, `ai.py`, `shield.py`, `scarlet_clips.mjs` (HF-A),
the numbers in `api.py` (lane HB).

## Steps
- [x] reproduce HB-01 … HB-07 (numbers below; HB-01 also rendered through the built R6 camera)
- [x] HB-02 the Shift snap, HB-03 the stands made at their first shots, HB-04 E2, HB-05 the coda black, HB-06 the line shots,
      HB-07 I18: sequence side + tests (test_seq R9 / R10 / F1 / F2 / F3 / S2, test_cam K4 / K6, ev_dry)
- [x] HB-01 the repel throw (both clips + mutual contact rows in both builders and test_contact)
- [x] docs (hr_design §3 / §4.3, README 0-4 / 0-8 / 0-9 / 홍련 절, hr2 text), final gates, frames for the lead

## Reproduced (head d7da75e79)
| id | how | what |
|---|---|---|
| HB-01 | her_tracks.json vs the actor manifest, ticks 74-100; `built_shots.py --seq repel60` R6 | nothing of the actor within 1.0 b of her pelvis / head / hands / left elbow 84-96 (1.16-2.25 b); her pelvis at u 2.96 over a bent actor (shoulder u 0.83) |
| HB-02 | test_cam K4 (camsim) | while Shift is held the player ends every tick as its own camera at the stand's feet (eye 0.10 b over the stand's eye), its free view drifting between ticks |
| HB-03 | camsim's new client model (spawn pose, then a 3-tick glide) | the first held frame of every locked sequence shows the stand gliding from the stage marker (yaw 0): 1.1-6.9 b and 60-120° off at tick 0 |
| HB-04 | `hr/h2/framing.py` (per tick, the built cameras, her rig's points, the actor's head) | E2 84-93: neither figure in the picture |
| HB-05 | seq/event/k/110 | black in 10 from E110 = opaque at E120, the hand-back at E118 |
| HB-06 | framing.py, lens to her head ≤ 2.2 b and her head in the frame's middle at every line tick | lines 4, 5, 6, 7 (tail), 8, 9, 10, 13, 15 (tail), 16, 17, 19, 21, 22 off (24 / 25 the coda over the actor's shoulder) |
| HB-07 | her_tracks intro_end head / brim vs the built I18 lens (eye rows hidden behind the brim disc or not) | her eyes in sight from 1296; the brim lift at 1330-1346 shows nothing new |

## What changed (sequence side)
- **HB-02** (FN-cam `cam/hold`): while `rlk:in_sneak` the hold teleports the player to the live stand's eye (`tp @s ~ ~-0.10125 ~ ~ ~`
  at / rotated as the stand: the player's eye is 1.62 × the F5 seat's scale 0.0625 over its feet; `L.CAM_SNEAK_DY`) and returns before
  `spectate` (a teleport ends a spectate; the game ends it after the functions anyway). The snapped view each tick is the shot's; the
  free view still turns / sinks between ticks until Shift is released (README 0-9 / 홍련 절). +2 commands per held tick (test_cam C2 14).
- **HB-03**: `mboss/cam/spawn_at {id}` (+ `spawn_in`): a one-tick marker takes the execution rotation, the stand is summoned with it in
  its NBT (`Rotation:[$(yaw)f,$(pitch)f]`). `cam.Track.spawn()` makes each stand at its first shot (a helper placed and aimed as the
  shot, clamp / over / lift included); every locked start uses it (`seq.stands()`); the coda's `alone` path too. CS0 gets an opening
  mask `black 0/2/6` (the arrival blindness does not reach a stand's view): every locked sequence now opens on a full mask over ticks 0-1
  (CS0 black, CS1 / ending white, repel gold), so the first frame shown is tick 2 of a stand that has stood at its eye since tick 0.
  camsim models the client: the spawn packet's pose, then a 3-step interpolation to each change (`client_tick`, `client_view`).
- **HB-04**: E2 pulls back and pans with the shove (80-90, `io`) to `ST(4.5, 1.8, 2.2)` looking at `ST(0, 1.3, 2.7)`.
- **HB-05**: the coda black `6 / 16 / 0` at E110: opaque from E116, the hand-back at E118, held to E132 as before (the item / buff
  title's own time still ends at E110).
- **HB-06** — reframed shots (old → new; every line now has her head in the frame's middle and the lens ≤ 2.2 b from it):
  | line(s) | old | new |
  |---|---|---|
  | 4 | I9 over her shoulder 2.4-2.5 b | I9 pushed in: `HR(-1.2, 1.55, -1.6)` → `HR(-1.0, 1.5, -1.3)`, 2.0-1.7 b |
  | 5 | I10 the guest (her 21.7 b away), I11 her hands, I12 silhouette | I10 to 690; **I10b** her face 1.5 b (690-750); I11 framing face + hands 1.0 b; **I12a** close as she stands up (790-820) |
  | 6, 7 | I12 silhouette 5 b; I13 from 910 | the silhouette kept where no line plays (820-838); **I13** from 838: her turn to the actor and the smile, 1.35 b |
  | 8 | I14 the empty field | I14 960-980 (no line); **I14b** her on the rock 1.5 b (980-1040) |
  | 9, 10 | I15 static, her 11 → 4 b away | **I15** walks back before her, 1.75 b (an HR eye moved onto itself: placed in her frame every tick) |
  | 13 | S4 over the actor's shoulder, her 10 b | S4 to 110; **S4b** her 1.6 b (110-180) |
  | 15 tail, 16 | S11 the petal (her 6.5 b), S13 wide from 648 | **S11** her iai 1.35 b with the petal low in the foreground, through the draw and the slash to 654; S13 from 654 |
  | 17 | E9 4.4 b | E9 to 420; **E9b** her sheathing 1.4 b (420-470) |
  | 19 | E12 2.3-2.5 b | E12 pushed in to 1.9 b |
  | 20 | E12b behind her, 1.8 b | E12b from her left side-back 1.3 b: the look back over her left shoulder turns her face to the lens |
  | 21 | E14 the two (her 11.9 b), E15 behind her 2.6 b | E14 882-910 (no line); **E14b** before her 1.7 b, drifting to her right as she looks up (910-1038); E15 the moon 1038-1072 |
  | 22 | E16 static, her 7 → 2.5 b | **E16** 1.75 b before her: her face comes round in the pivot, the lens walks back with her |
  | 24 / 25 | the coda over the actor's shoulder, her 5.8 b | E4 her face 1.7 b; E30 over her right shoulder (the gift to the actor); E52 the old coda shot (line cleared) |
  Cut list: CS0 23 shots, CS1 13, the ending 23, the coda 3 (test_seq `CUTS`).
- **HB-07**: I18 opens at `HR(0.15, 1.95, 1.9)` on the crouched figure and pushes in (1298-1312) to `HR(0.15, 1.85, 1.4)`, looking at
  `HR(0, 1.55, 0)`: the lens a little over her eye line, so her low brim covers every eye row until the lift; the mouth shows under the
  brim edge from 1302; the eyes from 1332; the lens ≥ 0.58 b from the brim. Her clip unchanged (its head is already 25-44° down 0-40).
  The brim is the 84 %-opaque weave of the hat (paint): the eyes are behind it, not black.

## What changed (HB-01, the repel throw)
- **Her clip** (`scarlet_cine.mjs` R6, every tick 79-100): her pelvis rides `THROW.P` onto the actor's back and over its right
  shoulder, head first, face up, pitched back on `THROW.PT` (6 → 108 degrees); the root arcs only `THROW_H` 0.6 b (`seq.py` `toss`
  `leap(..., THROW_H)`; before: 2.2 b with her pelvis 2.96 b up over a bent actor). Her sword hand is held on `THROW.G` to 96 (the
  actor's hands are on that forearm), the blade turned over 79-82 from the hook's line to `THROW.D` (out to her left past the
  actor's right side, level, a little back: across the held forearm, so the wrist is within the held-prop limit and the hilt keeps
  out of her torso — gripClear pushes ≤ 0.20 b); let go at 96 it swings up (17 degrees to her left of vertical: through the vertical
  the rig's sword channels turn it over) and down beside her (97-100) to LIE's blade at 101. The hat leaves at 84 as before
  (lower toss). R6 camera kept as designed (`ST(-2.8, 0.7, 1.8)`).
- **The actor** (`player_motion/cine/clips.mjs` repel 78-102): its right fist hooked over her sword forearm 78-96 (0.22 b from her
  grip toward the elbow), its left hand round her wrist 86-91 (reaching for it 79-85, letting go 92-97), the hips back under her and
  the back bent forward, rolled left with the head ducked left of her body (`BEND` keys, `throwFit` per tick against her tracks:
  both holds 0.52 b from the shoulders, the head ≥ 0.44 b off her body's line where reachable); its own blade out past its right
  side `[.38, -.48, .79]` (the old `.55` down put the point under the floor at 96-97 with her new forearm).
- **Mutual contact rows** `MUTUAL` (`scarlet_cine.mjs`, read by both builders and test_contact): KW.grip 36-48, KH.hilt 49,
  KS.hook 70-78, KT.grip_r 78-96, KT.grip_l 86-91, KT.over 84-92 (her pelvis 0-0.6 b over the actor's right shoulder, ≤ 0.5 b off
  it), KK.kick 129. The rig builder fails on them (against the actor manifest; `--mutual-allow` while re-authoring) and the actor
  builder fails on them (against `her_tracks.json`; `RLK_CINE_HER_TRACKS` for a scratch copy); both write the measured values
  (`scarlet_rig_manifest` / actor `manifest.json` `mutual`). `api.CONTACT['KT1']` is the new over-the-shoulder point
  `ST(0.28, 1.4, 2.0)` (a separate line in api.py). hr_design §4.2 / §4.3 / R6 and the actor manifest's beats rewritten.
- Measured (final build): KT.grip_r ≤ 0.082 b (t78), KT.grip_l ≤ 0.006 b (t86), KT.over her pelvis 0.345 b over the shoulder and
  0.086 b off it at 88; the actor's head ≥ 0.40 b from her torso 79-96; held props right everywhere (the tip ≥ 1.45 b from her
  elbow at 81-84, need 1.34); test_contact fails 4 mutual rows on the old head (d7da75e79), passes now.
- test_rig: the hat's first flying tick (repel 84) moves 0.37 b (the guard lifts it off her head box while her head turns into
  it; the worn hat already moves 0.27-0.41 b a tick at 79-83): the KNOWN bound for that tick 0.21 → 0.38 with the measured
  alternatives in the comment (leaving later moves the clip event, its sound and the state spans; 89+ breaks KT.over).

## Tools added
- `tools/dev/sim/hr/cine/built_shots.py`: frames through the cameras as built (seqsim's live stand) with her real rig (`--debug-dp`
  frames) and the real actor (`--cine-debug-dp` frames), `--ortho` side views, `--lines` / `--shots` tick sets.
- `tools/dev/sim/hr/h2/framing.py`: the per-tick framing report (test_seq F1 / F2).

## Gates (final tree)
| gate | result |
|---|---|
| rig → kit → player rig (+ audio) → `regen_all.sh --mobs`, twice | identical (hash of every changed / new tree file and of the whole pack copy the same after both runs); `regen_all` failures 0; check_mboss_pack 0 problems; the pack copy = `rp_hi` byte for byte |
| loadcheck `hfb` | 0 function load failures |
| rplint / atlas_px (pack copy) | 0 problems / 12.935 M (≤ 13.2 M) |
| hr suites | test_seq all (incl. the five-stage lens checks), test_cam all, test_cine 159/159, test_contact 94/94 (8 mutual rows), test_actor 167/167, test_rig 162/162, test_kit 15798/15798, ev_dry 82/82, test_flow 40/40, pat_p1 531/531, pat_p2 67/67, pat_ghost 65/65, gen_check_hr 28/28 (the generators re-run on a copy: no diff), ident_hr all (byte-identical to 35b82e5 outside the allow-list) |
| combat suites | test_cb 296/296, test_rm all, test_np 125/125, test_bal 117/117, test_bal_boss 117/117 |
| cost | test_flow: every phase / sequence ≤ 429 a tick on average (seq repel 389, intro 284), the fight 355 (≤ 830) |

## Frames for the lead (`<S>/cb/hfb_frames/`, built cameras, her rig and the actor as built)
`hb01_r6_throw.jpg` (R6 78-101), `hb01_side.jpg` (the same from the side), `hb06_intro_lines.jpg` / `hb06_cs1_lines.jpg` /
`hb06_ending_lines.jpg` (the middle tick of every line; the ending sheet opens with E1 2 and E2 84-92) / `hb06_coda.jpg`,
`hb03_hb06_intro_new_shots.jpg` (intro 2 and the new I10b / I12a / I14b / I15), `hb07_i18.jpg` (I18 1292-1348: the eyes under
the brim until the lift).

## Real-server probes (26.3, a copy of the server dir under the shared lock; `<S>/cb/hfb_work/probe/probe.sh`)
- `execute positioned 3.5 120 3.5 rotated 137.25 -12.5 run function rlk:mboss/cam/spawn_at {id:1}` → the stand at
  `[3.5d, 120.0d, 3.5d]` with `Rotation [137.25f, -12.5f]`; `{id:2}` likewise; a second `{id:1}` returns 0 and leaves it; the helper
  marker and the `camsp` storage are gone. Issued in the tick right after `forceload add` (chunk not loaded yet) the helper could not be
  selected and the stand came out with yaw 0 (the old behaviour, no worse); the fight's arena chunks are forceloaded.
- loadcheck `hfb_a`: 0 function load failures, `Loaded 1870 advancements`.
