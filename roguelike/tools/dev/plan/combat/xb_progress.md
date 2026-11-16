# Round X, lane XB (the bodies in the 홍련 fight and the repel) — progress

Branch `wip/x-body` (from `origin/wip/x` bfdb075dc), worktree `<S>/cb/wt_xb`, pack copy `<S>/rp_xb` (from `<S>/rp_rel4`; unchanged by this
lane: byte-identical to `rp_rel4`); `<S>` = the scratchpad of `x_brief.md`. Contract: `x_brief.md` "Rulings — lane XB" 1-5 (+ `h_common.md`,
`v_brief.md` §4, the trailer of `w_brief.md` §5). Scratch `<S>/xb/` (`sim` = a copy of `tools/dev/sim` with the paths rewritten,
`base/roguelike` = `origin/wip/x` unpacked for the before numbers, `out/` logs and tables, `shots/` the repel's sheets).

## Steps
- [x] read the brief, the investigation (`<S>/cb/collide/`), the lanes that built what changes
- [x] her side: the shared guard of every glide (`core/guard*`), `core/cam_ok`'s body clause (+ its eye anchor), the soft separation
      (`core/sep*`), kbdir 2 for the spot-centred hits, the G1 fail's push from her landing point, TRI's stop, dives at 1.6 b
- [x] the gauntlet stations: re-checked when the move starts (`g/st/ok`, `g/st/<name>`), `d2e` 2.0 b, A8.3 beside
- [x] the player's side: the walk (`view/body_rule`), the dodge set (`player/dodge/body`, her next glide step `player/body_next`),
      클로린드's nudge (`player/step_body`), 아를레키노's E (`char/arlecchino/skill_dash`)
- [x] `tools/dev/sim/hr/tests/test_body.py` (fight / sep / moves / cam); `test_wi` dodgecam at seat height and the rule; hrsim's Motion
- [x] the before / after table (walking, holding, sprinting, lunging, standing players; eye 2.11 / 2.36 / 2.85)
- [x] the repel re-staged (R0 start, R4, R6's fit, R7, the R4 camera), `test_contact` gap over every tick of every two-figure clip,
      shot sheets looked at
- [x] docs (README 홍련 / 2 / 3 / 0-8 / 0-9, hr_design §4.3 + §13)
- [ ] gates on the final tree, balance, push (see "Gates")

## What was wrong / what is built (x_brief causes 1-7, rulings 1-5)
- **Her stops** were chosen from where the player WAS (the lock 7 t before the hit; the stations 10-14 t before the cut) and nothing
  checked the live body. `core/cam_ok` did not guard the body at all, and its camera line was measured from the wrong eyes: vanilla
  `anchored eyes` adds the EXECUTOR's eye height (`EntityAnchorArgument.Anchor.apply` reads `CommandSourceStack.getEntity()`,
  disassembled from the 26.3 jar), so `execute at @a[tag=player] anchored eyes` run as her put her husk's 1.74 b on the seat rider's
  feet (~4 b over the avatar's feet; the tests' 1.62-b players hid it). Built: **one shared helper** `core/guard` (body.py) runs at the
  end of every fight tick for any glide of hers and tests the step `mboss/mv/tick` takes next tick (its own integer arithmetic) against
  the live avatar; a step that would come within 1.6 b stops her on her path (0.2-b probe) and spends the ticks left going there and to
  the glide's end height; a leap keeps its arc and only its end moves out. `core/cam_ok` has a body clause (>= 1.6 b from the avatar's
  feet, 0.05 b slack) and runs its line clause as the player. Dives land 1.6 b short (`LAND_SHORT` 1.4 -> 1.6; a standing player now
  gets her at 1.6 b, the hit discs are at the locked spot as before), TRI's lunge 1.6 b short.
- **Nothing separated the bodies** (the avatar is a vehicle: vanilla push never moves it; her husk is NoAI). Built: `core/sep`
  (radial, <= 0.25 b a tick in 0.05-b knockback-checked steps inside the arena, never through her; within 1.75 b the avatar's Motion
  loses the pull that would carry it inside 1.41 b after the tick's physics). Not while dead / reviving / map / camera hold; never on a
  beat's held tick (mboss/main does not run). Chosen over the framework's `#mbPushOn` capsule (see Decisions).
- **The player's moves**: the walk (`view/body_rule` in view/move, also on held ticks), every dodge move (`player/dodge/body`) stop at
  1.41 b from a `rlk_bodyr` body (hers), measured against where her glide puts her this tick (`player/body_next`); moves away are
  never stopped. 클로린드's lunge and 아를레키노's E stop 1.6 b from any boss body (`rlk_mb_body`).
- **Spot-centred knockback** pushed a player who stepped in past the spot into her: the framework's `#hzKBDir 2` = away from the boss
  body (`mboss/kb_src`, `hz/init`); her A9 / HCUT discs, A10, KCUT's lines, NB's bands, Q's pillar and the gauntlet cuts use it.
- **The G1 fail** pushed the player toward the arena start (the ring centred on them), through her when they faced it: the spot
  `land` is found first and `ult/fail60_push` (ring r 4 -> 5 b, 3 t) is centred on it; she lands there.
- **Gauntlet stations**: re-checked when her move to them starts (`g/st/ok`, else re-picked), `d2e` 2.0 b, A8.3 beside the player
  (2.0 b at +60 / -60 / +90 / -90, 2.5 b up). Cut ticks unchanged.
- **The repel** (R2-R6 0.04-0.7 b torso to torso): she starts 1 b above f 1.4 (was 1.0); the actor hops back to f -0.7 after the hilt
  strike and cuts from a sword's reach, passes her right side 1 b off (r -1.0), the throw's fit keeps its torso 0.3 b off hers (a
  continuity cost from the hook's pose, the torso-axis clearance, a stronger head clearance), it steps back to f 1.5 after the throw
  and in again for the kick (the kick pose at 129 = ending 0 unchanged; the compiled ending is byte-identical, `ending.json`'s weapon
  Euler angles are an equivalent representation). The R4 camera is wide on the actor's left. `api.CINE_GAP` declares the contact rows.

## Measured (test_body fight, eye 2.36 = the default seat's rider, the game's tick order; before = `origin/wip/x` with the same suite)
Each cell: the closest horizontal distance (b) / ticks nearer than 1.4 b, summed over the start distances 3 / 6 / 10 b (gauntlets: 6 b
from the south / north / east / west, their fail branch included). walk = toward her at 0.216 b/t stopping 1.5 b off (dodging before
each hit: a lunge-step while moving, else the twist); hold = W through her; sprint = W + sprint 0.28 b/t; lunge = W + the dodge before
each hit; stand = no walk, the dodge + the cartwheel.

| pattern | walk before | walk after | hold before | hold after | sprint before | sprint after | lunge before | lunge after | stand before | stand after |
|---|---|---|---|---|---|---|---|---|---|---|
| a1 P1 | 1.06 / 7 | 1.41 / 0 | 0.06 / 17 | 1.41 / 0 | 0.06 / 24 | 1.41 / 0 | 0.19 / 10 | 1.41 / 0 | 2.80 / 0 | 2.80 / 0 |
| a2 P1 | 1.07 / 5 | 1.41 / 0 | 0.07 / 15 | 1.41 / 0 | 0.06 / 20 | 1.41 / 0 | 0.09 / 8 | 1.41 / 0 | 2.80 / 0 | 2.80 / 0 |
| a3 P1 | 1.26 / 14 | 1.46 / 0 | 0.01 / 202 | 1.41 / 0 | 0.03 / 210 | 1.41 / 0 | 0.01 / 143 | 1.41 / 0 | 2.13 / 0 | 2.13 / 0 |
| a3s P1 | 1.26 / 5 | 1.46 / 0 | 0.01 / 85 | 1.41 / 0 | 0.03 / 93 | 1.41 / 0 | 0.01 / 62 | 1.41 / 0 | 2.20 / 0 | 2.20 / 0 |
| a4 P1 | 1.16 / 20 | 1.41 / 0 | 0.02 / 113 | 1.41 / 0 | 0.00 / 119 | 1.41 / 0 | 0.02 / 46 | 1.41 / 0 | 1.20 / 3 | 2.70 / 0 |
| a6 P1 | 6.78 / 0 | 6.78 / 0 | 6.78 / 0 | 6.78 / 0 | 6.72 / 0 | 6.72 / 0 | 6.78 / 0 | 6.78 / 0 | 7.00 / 0 | 7.00 / 0 |
| a9 P1 | 0.23 / 29 | 1.41 / 0 | 0.02 / 65 | 1.41 / 0 | 0.02 / 73 | 1.41 / 0 | 0.02 / 31 | 1.41 / 0 | 1.80 / 0 | 1.80 / 0 |
| a10 P1 | 0.60 / 26 | 1.41 / 0 | 0.00 / 57 | 1.41 / 0 | 0.01 / 60 | 1.41 / 0 | 0.00 / 26 | 1.41 / 0 | 1.20 / 3 | 2.70 / 0 |
| d4 P1 | 1.26 / 5 | 1.46 / 0 | 0.01 / 154 | 1.41 / 0 | 0.01 / 162 | 1.41 / 0 | 0.01 / 101 | 1.41 / 0 | 1.99 / 0 | 1.99 / 0 |
| tri P1 | 0.48 / 14 | 1.41 / 0 | 0.00 / 177 | 1.41 / 0 | 0.04 / 179 | 1.41 / 0 | 0.02 / 144 | 1.41 / 0 | 1.30 / 4 | 1.50 / 0 |
| rings P1 | 1.26 / 5 | 1.46 / 0 | 0.01 / 122 | 1.41 / 0 | 0.01 / 132 | 1.41 / 0 | 0.01 / 50 | 1.41 / 0 | 2.20 / 0 | 2.20 / 0 |
| ult P1 | 1.26 / 11 | 1.46 / 0 | 0.01 / 284 | 1.41 / 0 | 0.01 / 294 | 1.41 / 0 | 0.01 / 155 | 1.41 / 0 | 2.20 / 0 | 2.20 / 0 |
| hcut P1 | 0.23 / 25 | 1.41 / 0 | 0.01 / 61 | 1.41 / 0 | 0.02 / 68 | 1.41 / 0 | 0.02 / 32 | 1.41 / 0 | 1.80 / 0 | 1.80 / 0 |
| blue P1 | 0.08 / 20 | 1.41 / 0 | 0.01 / 48 | 1.41 / 0 | 0.06 / 54 | 1.41 / 0 | 0.02 / 30 | 1.41 / 0 | 1.80 / 0 | 1.80 / 0 |
| kcut P1 | 0.08 / 20 | 1.41 / 0 | 0.02 / 54 | 1.41 / 0 | 0.02 / 60 | 1.41 / 0 | 0.02 / 21 | 1.41 / 0 | 1.80 / 0 | 1.80 / 0 |
| mx P2 | 0.54 / 6 | 2.31 / 0 | 0.05 / 75 | 1.41 / 0 | 0.01 / 77 | 1.41 / 0 | 0.63 / 6 | 2.31 / 0 | 1.40 / 0 | 1.60 / 0 |
| nb P2 | 1.05 / 15 | 1.41 / 0 | 0.00 / 128 | 1.41 / 0 | 0.04 / 135 | 1.41 / 0 | 0.02 / 40 | 1.41 / 0 | 2.80 / 0 | 2.80 / 0 |
| q P2 | 0.07 / 19 | 1.41 / 0 | 0.02 / 290 | 1.41 / 0 | 0.00 / 294 | 1.41 / 0 | 0.02 / 25 | 1.41 / 0 | 1.80 / 0 | 1.80 / 0 |
| a8 P2 | 0.02 / 195 | 1.41 / 0 | 0.00 / 670 | 1.41 / 0 | 0.01 / 708 | 1.41 / 0 | 0.00 / 450 | 1.41 / 0 | 0.46 / 41 | 1.81 / 0 |
| a13 P2 | 0.04 / 189 | 1.41 / 0 | 0.01 / 652 | 1.41 / 0 | 0.01 / 700 | 1.41 / 0 | 0.01 / 346 | 1.41 / 0 | 1.11 / 4 | 1.81 / 0 |
| all | 0.02 / 630 | 1.41 / 0 | 0.00 / 3269 | 1.41 / 0 | 0.00 / 3462 | 1.41 / 0 | 0.00 / 1726 | 1.41 / 0 | 0.46 / 55 | 1.50 / 0 |

After at eye 2.11 / 2.85 (walk, lunge, hold; 186 runs each): 0 ticks below the rule, closest 1.408 b. Knockback toward her: 2 -> 0.
(The investigation's numbers differ a little: it moved the walking player before the functions; here the walk is the avatar's Motion
applied after them, as vanilla does.)

## The repel: torso axes per span (b; her pelvis -> 0.8 of the head vs the actor's waist -> chest; test_contact `gap`)
| ticks | what | before | after |
|---|---|---|---|
| 0-1 | R0 the dive onto the guard | 1.61 | 1.83 |
| 2-5 | R0 landing | 1.40 | 1.60 |
| 6-32 | R1 the lock, R2 her blade beaten wide, the yank begins | 1.52 | 1.52 |
| 33-48 | R2 the grab (contact row) | 0.47 | 0.47 |
| 49-51 | R3 the hilt on her hat (contact row) | 0.40 | 0.43 |
| 52-55 | R3 she reels / the actor hops back | 0.39 | 1.58 |
| 56-61 | R4 the two cuts | 0.58 | 1.78 |
| 62-66 | R4 the pass-by (row: >= 0.9) | 0.21 | 0.90 |
| 67-78 | R5 back to back, the hook (contact row) | 0.35 | 0.35 |
| 79-100 | R6 the throw (contact row) | 0.04 | 0.33 |
| 101-117 | R7 the actor over her | 1.30 | 1.54 |
| 118-129 | R8 the step in, the kick (contact row) | 1.07 | 1.07 |
| 130-140 | R9 apart | 1.91 | 1.91 |

## Decisions
- **The separation is the module's own (`core/sep`), not the framework's `#mbPushOn` capsule**: the capsule is a set of anchor-frame
  boxes left by their sides / ends at 0.6 b a tick, refused while the player dodges, and it does not touch the walk; the rule is a
  circle, radial, <= 0.25 b a tick, and the avatar's walk must stop at it (its Motion is clamped: the walk is applied after the
  functions by vanilla physics).
- **`anchored eyes` reads the executor's eye height** (above): `test_body` / `test_wi` model it (the player entity's `eye` = the rider's
  eyes 2.11 / 2.36 / 2.85, hers = the rider's feet + 1.74).
- **No fight contact is declared**: Q's grab keeps the rule too (its lunge already ended 2 b off the locked spot; the grab is the disc).
- **Dives at 1.6 b** (not 1.4): the ruling's stop is 1.6 b; `near()`'s first candidate must pass the body clause.
- **The guard checks the next step**, not the whole remaining path: the step is checked every tick against the live avatar; the
  stop choice at the move's start (the body clause) keeps the end off the avatar as it stood.
- **Contact rows of the repel include their approach** (the yank 33-35 into the grab, the hop's landing 49-51, the step in and the leg
  drawn back 118-128): they are the contacts' own motion; outside them >= 1.5 b on every tick.
- **The pass-by keeps 0.9 b** (the ruling's figure) as its own row; at 1 b off her the actor still passes between the R4 camera and her
  for 3 ticks (a wider camera: the actor no longer fills the lens).

## Files outside her module (`boss/scarlet/**`, her generators, her cine clips) that differ from `origin/wip/x`
| file | why |
|---|---|
| `view/move`, new `view/body_rule`, `view/body_sqrt` | the walk keeps the rule |
| `player/dash_move_tick`, new `player/dodge/body`, `player/body_next` | every dodge move stops short of her |
| `player/step_move_tick`, new `player/step_body` | 클로린드's nudge stops 1.6 b from a boss body |
| `char/arlecchino/skill_dash` | 아를레키노's E 1.6 / 2.1 b in front of a boss body |
| `mboss/kb_src`, `mboss/hz/init`, `mboss/hurt` (comment) — `tools/build_mboss_core.py` | knockback mode 2 (away from the boss body); no other boss sets it: their behaviour is unchanged |
| `char/cine/c/repel/**`, `tools/player_motion/cine/{clips.mjs,repel.json,ending.json,manifest.json}` | the actor's repel |
| tests: `test_body.py` (new), `test_contact.py`, `test_cine.py`, `test_wi.py`, `test_cam.py` (D1), `ident_hr.py` (group LANE_XB), `lib/hrsim.py` (Motion) | |
No other boss's output differs (ident_hr; `git diff origin/wip/x --stat` outside the files above, her module and docs: empty).

## Pack files
None (`diff -rq rp_rel4 rp_xb`: identical; atlas 13 109 184 px).

## Gates
(the final round: below once run; the checkpoint commit had test_body 331, test_vi 208, test_wi 215, test_seq ALL, test_cam ALL, test_cine 172, test_contact 106, test_actor 157, pat_p1 559, pat_p2 70, pat_ghost 65, test_scarlet 48, test_flow 40, test_blade 347, test_metro 33, test_bal_hr 79, ident_hr pass, test_rig 162, test_kit 15 361, test_cb 402, chainparry 624 / 624, gen_check_hr 28 / 28, loadcheck xb1 0 failures + Done, check 0, rplint 0, atlas 13.109 M)

## Only a person in the game can check
README 0-9 「홍련 — 게임에서 확인할 것」, the 11-16 round X block X①-X⑩.

## How to run
```bash
S=<scratchpad>; W=$S/cb/wt_xb/roguelike; RP=$S/rp_xb; cd $W
# the whole regeneration (README 0-4; twice: `git status` the same, the pack hash the same)
node tools/build_scarlet_rig.mjs --resourcepack $RP && python3 tools/build_mboss_hr_fx.py --resourcepack $RP \
  && python3 tools/build_bossbar.py --resourcepack $RP && python3 tools/build_combat_fx.py --resourcepack $RP \
  && node tools/build_player_rig.mjs --datapack . --resourcepack $RP && python3 tools/build_player_audio.py \
  && python3 tools/build_blank_tex.py --resourcepack $RP && bash tools/dev/regen_all.sh . --mobs \
  && python3 tools/build_mboss_bf_fx.py --skip-rp && python3 tools/build_mboss_fg_fx.py --skip-rp
# the suites from a copy of tools/dev/sim outside the tree (the paths rewritten; never re-copy it while a suite runs from it)
SIM=$S/xb/sim; rm -rf $SIM; cp -a $W/tools/dev/sim $SIM; (cd $SIM && grep -rl --exclude='*.md' --exclude='*.json' \
  2f5e7b47-ba2f-58bc-b880-1598991e2f8e . | xargs sed -i "s|/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad|$SIM|g")
cd $SIM/hr/tests && python3 test_body.py $W [cam|moves|sep|fight] [--keys=a9,mx] [--pols=walk,hold,sprint,lunge,stand] \
    [--dists=3,6,10] [--eye=2.36] [--json=out.json]      # fight: 310 runs, ~25 min on one CPU; the before: the same on origin/wip/x
# the repel's sheets: her clip and the actor's debug frames, then the built cameras
node tools/build_scarlet_rig.mjs --resourcepack <rp copy> --datapack <scratch dp> --only repel --debug-dp <dbg> --debug-clips repel
RLK_CINE_HER_TRACKS=$W/tools/dev/sim/hr/cine/her_tracks.json node tools/build_player_rig.mjs --datapack <scratch dp2> \
    --resourcepack <rp copy> --cine-debug-dp <cdbg> --cine-debug-clips repel      # then copy <cdbg>/data/rlk/function/cine_dbg into <dbg>
cd $SIM/hr/cine && python3 -I built_shots.py $W --dbg <dbg> --rp <rp copy> --seq repel60 --ticks 52,56,62,66 --actor arlecchino --fov 90 -o out.jpg
```
