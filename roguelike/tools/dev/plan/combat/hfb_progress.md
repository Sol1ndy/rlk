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
- [ ] HB-01 the repel throw (both clips + mutual contact rows in both builders and test_contact)
- [ ] docs (hr_design §3 / §4.3, README 홍련 절, hr2 text), final gates, frames for the lead

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

## Tools added
- `tools/dev/sim/hr/cine/built_shots.py`: frames through the cameras as built (seqsim's live stand) with her real rig (`--debug-dp`
  frames) and the real actor (`--cine-debug-dp` frames), `--ortho` side views, `--lines` / `--shots` tick sets.
- `tools/dev/sim/hr/h2/framing.py`: the per-tick framing report (test_seq F1 / F2).

## Next
HB-01 (below when done), then docs and the final gates.

## Real-server probes (26.3, a copy of the server dir under the shared lock; `<S>/cb/hfb_work/probe/probe.sh`)
- `execute positioned 3.5 120 3.5 rotated 137.25 -12.5 run function rlk:mboss/cam/spawn_at {id:1}` → the stand at
  `[3.5d, 120.0d, 3.5d]` with `Rotation [137.25f, -12.5f]`; `{id:2}` likewise; a second `{id:1}` returns 0 and leaves it; the helper
  marker and the `camsp` storage are gone. Issued in the tick right after `forceload add` (chunk not loaded yet) the helper could not be
  selected and the stand came out with yaw 0 (the old behaviour, no worse); the fight's arena chunks are forceloaded.
- loadcheck `hfb_a`: 0 function load failures, `Loaded 1870 advancements`.
