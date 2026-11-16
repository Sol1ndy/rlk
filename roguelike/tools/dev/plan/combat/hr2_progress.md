# lane H2 (홍련 rebuild: cutscenes, camera, control lock) — progress

Branch `wip/combat-hr2` (from `origin/wip/combat` c7dcc4fbf; merged: H1 interface 15fad96a9, H3 0c762626b, H1 final
c1e53b116, `origin/wip/combat` 8fe44f516 = fix lane FB + the Opus 5.5 trailer), worktree `<S>/cb/wt_hr2`, pack copy `<S>/rp_hr2`
(`<S>` = the scratchpad of `h_common.md`). Contract: `hr_design.md` (§8 wins), `hr_brief.md` 「조작 잠금 · 카메라」.
Owner of FN-cam (`build_mboss_core.py`, `mboss_lib.py`), the RIGLIB look target (`mboss_rig_compile.mjs`),
`tools/mboss_scarlet/{seq,cam}.py`, the hand-file lines in `tick` / `view/tick` / `lvup/tick`, the suites
`hr/tests/{test_cam,test_seq,ev_dry}.py` and the lane's sim + shot-sheet tools `hr/h2/**`.

## Steps
- [x] **FN-cam** (§5.2): the framework lock (2ae07b240).
- [x] **RIGLIB look target** (§5.4): `writeFace({target})`, 홍련 = `@e[tag=rlk_body,limit=1]`.
- [x] **`cam.py` + `seq.py`** (`CONTRACT = 2`, §3): all eight sequences with their cameras (fed31119c).
- [x] **the actor wired** (H3 merged, 0a0633b83) and H3's six points taken in.
- [x] **H1's final core merged**; its six points taken in (`ev_dry` rebased).
- [x] `origin/wip/combat` (fix lane FB) merged: `bal/boss/may` keeps H1's `#mbBalOff` and FB's `rlk_mb_inv` refusals.
- [x] suites, shot sheets on five stage placements, gates (below).
- [ ] waits for H2c: her 8 cinematic clips are placeholders (static poses of the contract length); the sheets' stand-in
      for her is a box figure with the design's postures. Everything timed is in place.

## How to run
```bash
S=<scratchpad>; WT=$S/cb/wt_hr2/roguelike; cd $WT
bash tools/dev/regen_all.sh .                                  # datapack: core, kit (--skip-rp), module, pack check
node tools/build_scarlet_rig.mjs --resourcepack $S/rp_hr2      # her rig (the look target lives in rig/face/*)
node tools/build_player_rig.mjs --datapack . --resourcepack $S/rp_hr2   # lane H3's actor (+ its pack files)
RLK_DEV=$S bash tools/dev/loadcheck.sh $WT h2
SIM=$S/cb/h2sim; rm -rf $SIM; cp -a $WT/tools/dev/sim $SIM     # suites never run inside the tested tree
cd $SIM/hr/tests && python3 test_cam.py $WT && python3 test_seq.py $WT && python3 ev_dry.py --dp $WT
python3 test_seq.py $WT run skip        # sections: static run stages skip life actor frames
cd $SIM/hr/h2 && python3 sheets.py $WT <out dir> [intro cs1 repel60 repel5 ending] [--stage=c|n|e|s|w|all] [--no-img]
python3 $SIM/hr/tests/test_seq.py $WT frames --frames <out dir>   # asserts on that run's frames.json instead of rendering
```

## FN-cam as built (§5.2)
| piece | what |
|---|---|
| request | `#mbCam mb` 1 from the module's tick + `#mbCamId mb` 1 / 2; `mboss/main` zeroes `#mbCam` at its top (so do `cleanup_fight`, `init`) |
| `rlk:tick` (hand file) | right after `mboss/main`: `#mbCam` 1 → `mboss/cam/hold` as the tagged player; else `mboss/cam/release` as every player carrying `rlk_mb_camh`. The two-player guard at the top releases too |
| `mboss/cam/spawn` | at the execution position, idempotent: two **marker armour stands** `rlk_mb_cam1` / `rlk_mb_cam2` (+ `rlk_mb_cam`, `rlk_room`, `rlk_mb_aux`, `rlk_pet`), invisible, no gravity, `camera_distance` 0. From the jar: `ArmorStand.MARKER_DIMENSIONS = fixed(0, 0)` → eye height 0: **the stand's position is the eye point** (`mboss_lib.CAM_EYE = 0.0`) |
| `mboss/cam/hold` (+ `hold_in`) | first tick: tag `rlk_mb_camh`, the game mode kept as a tag (`rlk_mb_cgS` / `rlk_mb_cgC`; neither = adventure), the avatar's place into `rlk:mboss camret` (a `/reload` removes the avatar), sprint FOV modifier off, the crosshair title blanked unless an overlay is up, `gamemode spectator`. Every tick: `spectate` the live stand |
| `mboss/cam/release` (+ `back`, `ret`) | no-op without the tag (idempotent): un-spectate, the stored game mode, the tags and `camret` gone; unless dead / in the selection space: the player to the avatar (no avatar: the stored point, written as offsets from the origin so a whole x / z is not block-centred, +0.02 b), `rotate` to the boss as seen from the seat, the avatar turned to her, `view/ride_mount`; then `char/cine/stop` (lane H3's actor) |
| `mboss/cam/kill` | both stands |
| `view/tick` (hand file) | one line after the housekeeping (vBig, fresh, the G menu, the burst camera): a held player's view rests |
| `lvup/tick` (hand file) | one line: a held player's sneak press is no F5 sneak-tap (a skip = Shift held) |
| explicit releases | `cleanup_fight` (first line), `mboss/init` (before the helper entities die), `rlk:tick`'s two-player guard; `mboss/uninstall` through its `cleanup` |

Rules the hold follows beyond the design text (each in `test_cam.py`):
- the live stand missing (killed) → `release` at once (never a free spectator); the lock comes back when the stands do.
- developer mode (the player is the body, no avatar) → never locked: the cutscene plays from the player's own eyes.
- a request with no fight (`#mbLive` 0), a player who became the body, or no avatar (the first tick after a relog) → released.

Costs (per tick): `mboss/main` +1, `rlk:tick` +2 always; a held tick 12, the first held tick 30, the release 44 (29 + the
actor's `stop` 15).

## The sequences as built (§3)
`seq.py` writes 1392 functions under `F:boss/scarlet/seq/`: per sequence `start` / `tick` / `cancel`, the timeline leaves
`k/<t>` or `k/<a>_<b>` (a run of equal ticks is one file) under a dispatch tree `kb/`, the body moves `m/<key>`; a locked
sequence also `lock` / `unlock` / `fin` / `cam` + the camera leaves `c/`, `cb/`; shared `seq/lib/{ok,lift,over}`.

| sequence | length | lock | shots | what |
|---|---|---|---|---|
| `intro` (CS0) | 1440 | 0-1439 | 20 | fixed stage `api.CS0_P0`, the one avatar teleport at tick 0; lines 1-11; the walk, the leap, `intro_end` at 1290; title 1356, music 1 at 1420; `skip` → 1290 |
| `cs1` | 720 | 0-719 | 12 | the clash, lines 13-16, the petal, 홍련일섬, crimson look 660, music 2 at 676; `skip` → 566 (her clip moved to 565, the looks of 566) |
| `lead60` | 56 | — | — | refill effect + sound at 0 (the refill itself is the core's) |
| `repel {at}` | 140 | 0-139 | 8 | the gold deflect at 0, `hp1` 49 / `hp2` 101 / `hp3` 129; bars stay on; `at:5`: the kick is the kill |
| `lead5` / `lead_re {g}` | 116 / 60 | — | — | signal `refill` at 60 / 10 with its effect and sound, the banner there while `#warn hr 1` |
| `ending` | 1372 | 0-1372 | 21 | stage ST then ST2 (toward the moon when that passes `mv/ok`), lines 17-23, music 3 at 420 |
| `event` (the coda) | 120 | 0-117 (inherited) | 1 | camera B live at E4; unchanged content (the thrown sword / the moonlight orb, the grant at E56, the black at E110) |

How the lock behaves (`seq/<name>/lock`, every tick of the span):
- `#sq_h hr` 1 once the run has seen the player held. Released after that (pause, `/reload`, relog, a killed stand) or never
  held by tick 3 → `unlock`: `#sq_cx hr 1`, the stands and the actor go, the sequence plays on unlocked with its timing
  and signals. (The hold arrives in the tick of the first request when the sequence starts inside `mboss/main`, one tick
  later for a start outside it — a kill by a hit — which is why the guard waits for the hold instead of assuming it.)
- `cancel` (the core's on pause / reload / `stop_all`) takes the request back, kills the stands, the stage, the props, stops
  the actor, clears the kit's line / overlay and the HUD hold: the framework releases the player in that tick.
- the lethal repel: at the kick `#sq_keep hr 1`; its `cancel` then leaves the actor standing and the ending's start plays
  `ending` on it without a new spawn (H3: repel 129 = ending 0); the coda does the same after the ending. If no ending
  follows, the framework's release stops the actor in the next tick.

Camera (`cam.py`): two stands, hard cuts alternate A / B, the idle stand is placed 4 t before its cut (`PRE`), moves are a
`tp` per tick, look points in her frame or on her eyes are aimed again every tick. Eyes of a dynamic stage are pulled into
the walk disc (`mboss/ar/clampw`), a low eye (< 1.05 b) is lifted out of a floor plant in its own cell or the next one
(`seq/lib/lift`), and an eye the clamp brought within 1 b of the stage origin goes 2.5 b up, over the actor's head
(`seq/lib/over`).

## What H3 and H1 asked, and where it is
| ask | done |
|---|---|
| H3-1 frame from the manifest | `hr/h2/sheets.py` builds the actor's stand-in (root, head, blade) per tick from `manifest.json`; R2 / R5 / R6 / S8 moved after it (below) |
| H3-2 cs0 steps on `steps` | `actor_steps('cs0', …)`: 24 … 96, 102, 1255, 1259, 1395, 1400, 1434, 1438 (`test_seq` A0) |
| H3-3 the repel pass / KA2 at r −0.5 | framed from the manifest's `shift`; all 608 frames pass |
| H3-4 no new spawn after `repel {at:5}`; absolute `face` yaw | `#sq_keep`, `actor_spawn(carry=True)`; `face` gets ST2's `Rotation[0]` (`test_seq` A5, A7) |
| H3-5 `#cavT` jumps on sync ticks | the skips land on 1290 / 566, clips start at 0; a run that lost its lock never resumes the actor (A0, A6) |
| H3-6 `tick` stops itself, `stop` idempotent | relied on: `stop` at `fin`, `unlock`, `cancel` and in the framework's release |
| H1-1 `CONTRACT = 2` on its own line | `seq.py` line 46 (`ev_dry` build) |
| H1-2 `seq/intro/skip`, `seq/cs1/skip` | both; the state after a skip = the uninterrupted run's (`test_seq` skip, 5 window ticks each) |
| H1-3 signals | `refill` at lead5 60 / lead_re 10, `hp1`-`hp3` at 49 / 101 / 129, nothing else (`ev_dry` signal) |
| H1-4 refill effect + sound, the gold deflect, the banner while `#warn hr 1` | in lead60 0 / lead5 60 / lead_re 10 and repel 0 (`ev_dry` refill, repel, banner) |
| H1-5 `cancel` releases everything | request, stands, stage, actor, props, kit line / overlay, HUD hold (`ev_dry` cancel, `test_seq` L1 / L4) |
| H1-6 `ev_dry` | rebased on contract 2: 82 checks |

## Gates (the final tree)
| gate | result |
|---|---|
| `regen_all.sh` twice | identical; `check_mboss_pack` 0 problems |
| loadcheck (26.3 server) | `h2a` 0, `h2b` 0, `h2c` 0, `h2d` 0, `h2e` 0 (the final tree, after the FB merge) |
| rplint / atlas | 0 problems / 12 935 424 px (= H3's number; `rp_hr2` = `rp_base` + H3's actor files only) |
| `test_cam.py` | 110 / 110 |
| `test_seq.py` | 392 / 392 (static 34, run 96, stages 60, skip 45, life 118, actor 34, frames 5), 14 min |
| `ev_dry.py` | 82 / 82 |
| `ident_hr.py` | passes (groups `LANE_H2` + `LANE_H3`) |
| other lanes' suites on this tree | test_scarlet 47 / 47, test_gauge 22 / 22, test_bal_hr 48 / 48, pat_p2 67 / 67, pat_ghost 65 / 65, test_special_hr pass, test_actor 167 / 167 (run without `--rebuild`) |
| `gen_check_hr.py --rp` | all but one: G4's stray probe in `p/r1/` survives (lane H1 removed pattern r1; the generator owns
  `p/<current key>/` only, as H1's notes say). The probes in `seq/` and `core/` are removed |
| `test_rig.py` | the two look-target checks pass; the suite as a whole still pins the 11-06 clip set (47 clips, old cine events): H1c / H2c's |
| tick cost of the sequences' own files (avg / max commands) | intro 51 / 98, cs1 40 / 200, repel 47 / 235, ending 47 / 191, coda 42 / 115, lead60 27 / 29, lead5 71 / 122, lead_re 31 / 142 |

Shot sheets: 608 frames (every shot at its cut tick, the end of each move, its middle and its last tick; `intro` on its
fixed stage, `cs1` / `repel60` / `repel5` / `ending` + coda on five placements: `c` the centre, `n e s w` the avatar at
radius 24 with her 6 b along the wall). Verdict of the final run: **0 lens problems** (no lens in a block, a plant or the
barrier ring, none under 0.2 b, none beyond the walk disc, none nearer than 0.3 b to a figure), **0 shots that never
show a subject**. All sheets of stage `c` and of stage `n` were looked at, the other walls by the numbers.

## Decisions / deviations (and why)
Framework / hand files
- Hand-file lines beyond `view/tick`'s guard: `rlk:tick` (3 lines: hold, release, the two-player release) and `lvup/tick` (1).
- A dead player or one in the selection space is released without being moved (those flows own the player's place).
- Developer mode is never locked (the player is the body); a request without an avatar is dropped.

Sequences
- The stands are killed and made again at every locked start (a new entity does not glide into its first frame).
- On-axis points of hers are checked with `seq/lib/ok` (the floor inside the barrier ring) where `mv/ok`'s safe disc
  would refuse a contact point next to an avatar near the wall; `mv/ok` itself where the design names it.
- A sequence whose lock is lost plays on unlocked (it does not stop): the core decides whether to end it (§3.6); both
  paths are tested.
- `cancel` also clears the kit's line / overlay / banner (`fx/hud/clear`) and the HUD hold (asked by H1).
- Camera moves end one tick before the next cut (a move and a cut never share a tick).
- The coda's camera B goes live at E4 (it is placed from E0; a stand moved in the cut's own tick would glide 3 t).
- Raw vanilla sounds where the kit has no recipe; `gold` overlays are white until the kit has the glyph (H2c).
- `ev_dry.py`'s old sections on the 11-06 sequences (sq1, lead_down, lead_stand, the dark looks, the E1b band) are gone
  with those sequences.

Shots moved from the design's table (each after a shot sheet; the eye / look are in `seq.py` with the reason)
| shot | design | built | why |
|---|---|---|---|
| I1 | starts at f −9.0 | f −7.4 | −9.0 is a barrier cell of the ring |
| I16 | r 0.8 | r −0.8 | a dry-grass cell on the fixed stage |
| S8 | `ST(0.5, 1.5, 1.8)` | `ST(−0.7, 1.5, 2.1)` | the actor's blade point comes up 0.15 b from the lens in the half guard 350-370 (H3 manifest) |
| S13 | r 0.4 | `ST(1.2, 2.1, −4.2)`, look `ST(0.2, 1.2, 4.0)` | the actor hid her |
| R2 / R3 | `ST(1.9, 1.5, −0.4)` | `ST(2.2, 1.5, 0.1)`, look `ST(0, 1.4, 0.8)` | the actor stepping in to f 0.5 stood before her |
| R5 | `ST(0, 1.6, 3.6)` head-on | `ST(2.1, 1.6, 2.7)` | she stands behind the actor: head-on its head covers hers |
| R6 | `ST(−2.8, 0.7, 1.8)` → `ST(0, 1.2, 2.0)` | `ST(−3.6, 0.8, 2.2)` → `ST(0, 1.7, 2.2)` | her arc (2.2 b up at 88) left the top of the frame |
| E6 | static | tilt up 204-216 | the spring |
| E15 | `ST2(0.5, 1.6, 8.0)` | `HR(1.3, 1.5, −2.2)` | 1 b behind her head the brim hid the moon; in her frame it also holds when ST2 could not point at the moon |

Shots without a figure subject (nothing asserted but the lens): I7 the cup, I14 the field, S5 the grass, S11 the petal.
S5 looks at `ST(0, 0, 4.55)` from `ST(0, 5.0, 4.5)`: straight down with the stage's forward up the screen.

At the wall (the avatar within about 1.5 b of the walk disc's edge, its back to it) a shot from behind the actor cannot
be given from inside the arena: S4, S13, E14 and the coda then show her without the actor's shoulder (S4 and the coda
from over its head). Those four mark the actor as an optional subject (`'actor?'`), required on the centre stage only.
A floor plant of the field (20-30 % of the floor cells, 1 b sprites) may stand between a low lens and a figure lying on
the floor; it is not counted as hiding her unless it is within 0.5 b of the lens.

## Requests to other lanes
- **H2c** (her cinematic clips, kit glyph): the eight clips at the contract lengths with their events; `cs1` needs a key at
  566 that sets every part (the skip seeks the clip to 565); seated head ≈ 1.37 b, standing 1.73 b were used for framing;
  her body path is the sequence's (`m/*` moves: CS0 walk f 20.73 → 13.5 and leap → 6.5; cs1 lunge → 1.5, back → 9.0; repel
  drop → 1.3, in → 1.1, stagger → 1.2, the throw arc to 3.0 (apex 2.2), the slide → 8.0, up → 9.0; ending lie 4.2, up 4.6,
  lunge 2.9, shove 6.0, away 11, run 4.0, the air at u 6.0 ± 0.4, the arc to ST2 f 9.0, the walk → 4.5): the clips animate
  in place. The `gold` overlay glyph (white stands in).
- **HI**: `README.md` lines 421 / 2600 / 2612 name `ev_dry` with the old counts; `test_rig.py` / `gen_check_hr.py` /
  `test_kit.py` still pin the 11-06 clip and kit sets (H1's list). The pack: nothing from this lane.
- **H1**: nothing open. For the record: `cs1` and `repel` set `#mbNoLeash mb 1` and clear it at `fin` / `cancel`; the lead-in
  starts turn the banner off; a locked sequence started by `death_start` outside `mboss/main` is locked one tick late (under
  the ending's white frame).
- **H3**: nothing open. `face` is called once, at ending 338, with ST2's yaw.

## Pack files
None added or changed by this lane (`rp_hr2` differs from `rp_base` only by lane H3's actor files, built by its generator).

## Only a person in the game can check
The spectate camera was never seen in a client. The mechanism keeps to the brief's checked facts (re-read in the 26.3
server jar: `spectate` needs spectator mode and a tracked entity; a spectating player is snapped to the camera every tick
and leaves it on sneak; leaving spectator mode resets the camera; the marker stand's eye height is 0).
1. **The held view**: no hotbar, hearts, crosshair or hand; the picture exactly at the stand; no F5 pull-back; no
   "spectating" overlay text.
2. **Hard cuts**: the idle stand is moved 4 t before its cut; a cut should show no glide. The first frame of each cutscene
   is a freshly made stand under a white / gold frame (CS1, repel, ending) — look for a one-frame jump of the view there
   and at the intro's first frame (no overlay).
   (HF-B HB-03, 11-11: the stands are now summoned at their first shots with the shot's rotation in the summon NBT
   (`cam/spawn_at`), and the intro opens under a black mask 0-1 too: the first frame shown is tick 2 of a stand that has stood
   at its eye since tick 0.)
3. **Pans**: rotation reaches the client in 1.4° steps. Slow pans to look at: intro I1 20-59 (0.07°/t), I3 the moon
   110-169 (0.13), I5 250-319 (0.07), I19 1350-1400 (0.10); cs1 S2 10-22 (0.13). If they step, they need a faster move or
   a static frame.
4. **Shift**: held during a cutscene the view should stay on the stand (the hold re-issues `spectate` every tick): look
   for a flicker to the free spectator view; in the skip windows (CS0 20-1270, CS1 40-560) the hold skips.
   (HF-B HB-02, 11-11: not so — the game ends a sneaking spectator's camera after the functions, every tick, so while Shift is
   held the hold now teleports the player onto the live stand's eye each tick (`cam/hold`, `L.CAM_SNEAK_DY`): the view is the
   shot's at each tick and loosens between ticks until Shift is released; README 홍련 절 FN-cam.)
5. **Hand-back**: back on the F5 seat behind the avatar in the same tick, facing her, the game mode as before, no
   "F5" chat hint again, the HUD back; after CS0 the avatar stands at the fixed stage point, not where the rift left it.
6. **Interruptions inside a cutscene**: death, 로노바's revive, `/reload`, a relog, opening the selection space — each
   must leave the player in their own game mode at the avatar with the actor gone and the avatar visible.
7. **The actor swap**: the avatar hidden and the actor shown from the first frame; at the repel's lethal kick the actor
   carries on into the ending without a blink; avatar back at each hand-back.
8. **Framing with the real models** (her clips are placeholders, her stand-in was a box): R0 / R1 the blade lock at 1 b,
   R5 back to back, E2 / E5 the locks, S10 / E10 / E17 her face under the brim, E15 the moon beside her hat, the coda
   over the actor's shoulder; with the avatar's back at a wall: S4, S13, E14 and the coda.
9. **Sound**: with the listener at the camera, CS0's wind and the step sounds at the right loudness.
