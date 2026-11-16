# Round W, lane WI (the integration of lanes WC / WP / WB) — progress and report

Branch `wip/w-int` (from `origin/wip/w` 02a162a03), worktree `<S>/cb/wt_wi`, pack `<S>/rp_wi` (from `<S>/rp_rel3`, the 11-12 release
pack); `<S>` = the scratchpad of `w_brief.md`. Contract: the lead's brief for lane WI, `w_brief.md`, the three lanes' progress files
(`wc_progress.md`, `wp_progress.md`, `wb_progress.md`). The release entries (README 0-1, 0-10, the build stamp, the pack's version
line) are the lead's and are NOT written. The scratch (`<S>/wi/`: the regeneration / suite scripts, a trial-merge worktree, logs)
was deleted at the end; "How to run" has the commands.

## Steps
- [x] merges (merge commits): `wip/w-cam` c9a427f4e, `wip/w-player` 47ad3b270, `wip/w-boss` final head 8ab0f2e91 (its re-timing
      c4afc07c4; it had merged `wip/w-player` as d42aa0373)
- [x] full regeneration in README 0-4 order after each merge (below)
- [x] the cross-lane requests (below) and what the seams showed (below; three fixes)
- [x] `tools/dev/sim/hr/tests/test_wi.py`: the round W seams (dodgecam, trailcut, dodgelock, dmgnum); `test_vi.py` keeps round V's
- [x] hrfair 2.0 on the final tree (all 175 runs) and on the 11-12 release tree for the comparison
- [x] docs (README 2 / 3 / 0-4 / 0-8 / 0-9 / 홍련, `hr_design.md` §12, the pack's README + `wi_rp_readme.diff`), gates

## How to run
```bash
S=<scratchpad>; W=$S/cb/wt_wi/roguelike; RP=$S/rp_wi; cd $W
# the whole regeneration (README 0-4; `git status` empty, the pack hash the same from the second round on)
node tools/build_scarlet_rig.mjs --resourcepack $RP && python3 tools/build_mboss_hr_fx.py --resourcepack $RP \
  && python3 tools/build_bossbar.py --resourcepack $RP && python3 tools/build_combat_fx.py --resourcepack $RP \
  && node tools/build_player_rig.mjs --datapack . --resourcepack $RP && python3 tools/build_player_audio.py \
  && python3 tools/build_blank_tex.py --resourcepack $RP && bash tools/dev/regen_all.sh . --mobs \
  && python3 tools/build_mboss_bf_fx.py --skip-rp && python3 tools/build_mboss_fg_fx.py --skip-rp
(cd $RP && find . -type f -print0 | sort -z | xargs -0 sha1sum) | sha1sum
# the suites: from a copy of tools/dev/sim outside the tree, the old scratchpad paths rewritten (tools/dev/sim/README.md 1 B)
SIM=<work>/sim; cp -a $W/tools/dev/sim $SIM; (cd $SIM && grep -rl --exclude='*.md' --exclude='*.json' 2f5e7b47-ba2f-58bc-b880-1598991e2f8e . \
  | xargs sed -i "s|/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad|$SIM|g")
cd $SIM/hr/tests && python3 test_wi.py $W [trailcut|dodgelock|dmgnum|dodgecam]   # 3.5 min; --keys=a8,ult narrows dodgecam
cd $SIM/hr/review/bal && python3 hrfair2.py $W --out <dir> --jobs 3                 # 175 runs, 10 min on an idle machine
```

## Merge notes
| merge | conflicts | resolution |
|---|---|---|
| `wip/w-cam` c9a427f4e | none | |
| `wip/w-player` 47ad3b270 | none (README auto-merged) | |
| `wip/w-boss` 8ab0f2e91 | none (README, `api.py` — lane WC's cutscene `CONTACT` rows and lane WB's gauntlet tables are different hunks — and `test_vi.py` auto-merged; WB had merged WP's `test_vi` line itself) | |

Regeneration (`<S>/wi/fullregen.sh`, the order above): after WC + WP, round 1 and 2: `git status` empty, pack hash `c0ec2341…` both
rounds. After WB: round 1 and 2 `git status` empty (the merged generated outputs were already what the merged generators write); the
pack's first round on the WC + WP pack re-sorted `items.json` (hash `cfec2abb…` -> `4fdebef2…`), rounds 3 and 4 on the final tree:
see "Gates". `diff -rq rp_rel3 rp_wi`: lane WC's four `hr_cine` half-petal files, lane WP's `cb/tint.png` + 31 `_hot` sprites,
lane WB's `hr_kit` trail sprites / models (below), `items.json`, the pack's README.

## The cross-lane requests
| request | what was done |
|---|---|
| WB -> WP: the dead `tag=rlk_hr_sw` line in `player/def/beat/st/tp_on` | removed by lane WB in its re-timing commit (c4afc07c4); `test_vi beatpat` checks the trail's riding cards carry `rlk_mb_part` and that `tp_on` / `pass` take that tag |
| WB -> lead (T3-09): damage numbers / smoke / flames hide her during wind-ups | measured and changed for the numbers (below); the skills' smoke / flames / pillars are each character's own effect files: listed (README 0-9 「홍련 — 남긴 것」) |
| WB: her stops re-checked after each move (`core/cam_clear`) assume the player's position when the move starts | checked with the player moving (`test_wi dodgecam`, below): nothing to fix |
| WC -> lead: the release pack is built with `build_blank_tex.py` (the half petals) | in the regeneration order above and README 0-4 (the line and a round W note) |
| WC -> VB/WB: `api.CONTACT` cutscene rows changed; the fight's blade cards killed at every cutscene start (`seq.KILL_FIGHT_FX`) | kept both sides of `api.py`; WB's trail no longer uses `rlk_hr_sw` (its cards carry `rlk_hr_tr` + `rlk_hr_p`): every path that starts a sequence in the fight kills them already (`core/cs1/start` `kill @e[tag=rlk_hr_p]`, `death_start` -> `core/stop_all`, the repel after `core/g/end`) — `test_wi trailcut` proves it, so `KILL_FIGHT_FX` was not changed |
| WP -> lead: `test_metro` fails without the whiff ladder (mashers clear G1 / G2) | lane WB's re-timing (c4afc07c4): `test_metro` 33 / 33 on the merged tree (below) |
| WP -> lead: the old fair sims of the chapter bosses (`mb3/fgfix`, `tk/review`, `ap/balance`, `tele/fg`, `mb2/balance`) model the pre-11-10 dash | not gated, not changed (listed) |

## What the seams showed (found by `test_wi.py` / the gates, fixed here)
1. **The cartwheel's stand-in rig never played without a beat** (lane WP; `test_wi dodgelock`). A mannequin character's (루미네,
   클로린드, 로노바, 네페르) double dodge starts the stand-in rig `lite/f` (`char/motion/dash2` -> `lite/start_f`: plActive 1, the
   mannequin hidden with infinite invisibility), but `rlk:tick` ran `lite/tick` only inside `player/def/beat/post`, i.e. while a beat
   runs: a plain cartwheel left a frozen stand-in figure at the cartwheel's start and the avatar invisible until the next dodge or
   beat. Fix: `rlk:tick` runs `lite/tick` at the same place when no beat runs (one gated line).
2. **A dodge in flight when a locked sequence starts kept moving the hidden avatar** (lane WP x lane WC; `test_wi dodgelock`):
   player/tick's move line runs before the fight tick, so the twist / lunge-step / back-step / cartwheel went on for up to 5 ticks
   under the actor (the hand-back puts the player at the avatar's place: up to 1.6 b off where the lock took them), and the
   mannequin's crouch and the cartwheel's stand-in rig carried into the lock. Fix: `player/tick` -> `player/dodge/cut` while the
   player carries the hold tag `rlk_mb_camh`: no move, the crouch stood up, the stand-in rig stopped (not while a beat runs: the beat
   ends itself one tick into the lock, round V); the avatar it shows is hidden again by `char/cine/tick` later in the same tick.
3. **test_cam D1** read only the round V groups of `ident_hr.py`: lane WP's round W files failed it on the merged tree; it reads the
   round V and round W groups now (lane WP's `player/f_key` added to its group; the integration's group `LANE_WI`).

## T3-09: the player's damage numbers over her
Measured (`test_wi dmgnum`; the fight camera 8 b from her: the player 4 b in front of her + the F5 camera 4 b behind the eyes; FOV 90,
1080p; the font's advances x 0.025 b x the display scale): a normal number (`combat/text_normal_macro`, scale 1.35) "259" ≈ 41 px
wide, a crit (`text_crit_macro`, 1.9, ✧✦ … ✦✧ bold) ≈ 215 px, spawned on her chest / head (± 0.8 b, 1.6–2.6 b up) and rising 1.9 b
in 16 t (the review: up to ~150 px over her). A small change in the number code, so done: on her body (`rlk_mb_scarlet`) the two
number lines of `combat/apply` are skipped and `combat/text_normal_side` shows the number at 2/3 size (0.9 / crit 1.2 without the
outer ✧: ≈ 27 / 99 px), beside her as seen from the player (1.1–1.5 b off the her -> player line, left or right at random) at
shoulder / head height (1.9–2.4 b); life and rise unchanged. Every other target keeps the old numbers. Cost: one self-tag test per
hit (`test_m0diff` A: named apart as `LANE_WI_CMD` 0.2; its failing set is the release's 40). The function names start with
`text_normal` / `text_crit` on purpose: the suites' worlds stub those prefixes as leaves (azsim `LEAF_PREFIX`), as they do the old
numbers.

## The seam tests (`tools/dev/sim/hr/tests/test_wi.py`, 215 checks) and the round V ones (`test_vi.py`, 208)
| seam | how | result |
|---|---|---|
| (a) the dodge set against her: the F5 camera, her stop rule vs the back-step | `dodgecam`: every pattern of `api.P1` + `api.P2` and both gauntlets in the H1 world; the player presses the REAL `player/dash` one tick before every hit (and again 3 t later: the cartwheel), moves by player/tick's own line, the judge's `dg_refund` turns an avoided hit into the back-step; the view on her chest every tick / frozen / 60° off; a standing player with perfect dodges and the same view as the reference. At the end of every tick: the vanilla F5 camera 4 b behind the eyes against her body (cylinder r 0.6, 2.1 high), her body against the camera line (lane WB's 1.3 b), her body against the player's, her `cam_clear` steps | 120 runs, 159 back-steps, 120 cartwheels, 853 b travelled: **the camera inside her on 0 of 8 274 ticks**; she never moved onto the player; her `cam_clear` step out of the line never fired (moving 0, standing 0: her stops already avoid the line, so the rule cannot fight a back-step); her body within 1.3 b of the camera line on 138 ticks, all in runs where the player's own double dodge put them next to her (a direction-less double dodge goes along the view: `ult` / `rings` 46 / 4 ticks, 0.58 b) or her hit knocked them across her landing (G1's dive after a missed answer, view 60° off: 36 ticks, one tick at 0.47 b); the standing reference: 0 in every view |
| (b) the beat with the trail and with the cutscene starts | `test_vi beatpat` (every pattern and both gauntlets beat on = off world tick by world tick, now with lane WB's trail cards; nothing of hers moves on a held tick), `beatseq` / `swap` / `skip` (the beat running when CS1 / the repel / lead5 start); `test_wi trailcut`: CS1 started while a trail is alive (a1 a3 a9 tri hcut kcut), the ending (mx nb q), the repel after G1 / G2 cleared — each with no beat, a perfect parry's freeze and a perfect dodge's slow motion running | `test_vi` 208 / 208; trailcut: 90 trail entities alive at the starts, 0 one tick later; the repel at 220 / 242 with none left |
| (c) the chains and the re-timed gauntlets | `chainparry` (the ideal parrier through the real `f_key`, 7 bosses + her chains + G1 / G2), `test_metro` (periods 1-40, every start), `pat_ghost`, hrfair T6 / T7 / T13 | chainparry 624 / 624 perfect (G1 9 / 9, G2 11 / 11: both cleared), 0 refused; test_metro 33 / 33 (at most 4 perfects anywhere, 5 clear); T6 cleared 100 %, T7 masher / sloppy / dodger 0, T13 53 / 53 |
| (d) the cutscenes with the new dodge | `dodgelock`: the 7 characters x the twist / lunge-step / back-step / cartwheel x a lock starting at each of the move's ticks 0-9 (the real `char/cine/**`, `char/motion/lite/**`, `player/dash*`, `player/dodge/**`) | after fixes 1 and 2: one visible body at the end of every tick, the hidden avatar never travels during the lock, nothing of the dodge left after the hand-back; without a lock the cartwheel's stand-in rig plays its 9 ticks and goes (89 checks) |
| T3-09 | `dmgnum` | above |

## Balance (hrfair 2.0, all 175 runs, seeds 11 / 22 / 33; logs `tools/dev/sim/hr/review/bal/wi_rel1112.log` = the 11-12 release tree `origin/wip/w`, `wi_final.log` = the final tree)
The dodge's travel is not in the model (hrsim's player stands; the real `dashCool` and the double dodge's cooldown are); what moved
the rows is the F without the whiff ladder and the re-timed gauntlets. No damage or other balance value was changed.
| row | band (§6.4 as amended) | 11-12 release | final tree |
|---|---|---|---|
| T1 P1 walker / 타키 | 1.00-1.15 | 1.02 / 1.03 / **0.97** (pooled 1.01) | 1.02 / 1.03 / **0.97** (pooled 1.01) — the same miss on seed 33 as the release (the lead's reading at 11-12) |
| T1b parrier σ3 / walker | <= 0.60 | 0.51 / 0.59 / 0.59 | 0.50 / 0.58 / 0.59 |
| T1c mixed σ0 | <= 5 %/min | 0 | 0 |
| T2 P2 walker / 타키 | <= 1.25 | 1.03 / 1.01 / 1.04 | 1.06 / 1.05 / 1.02 |
| T3 standing / the Guardian | <= 1.8 | 1.47 / 1.50 / 1.51 | 1.47 / 1.50 / 1.51 |
| T4 worst 40 t | <= 40 % | 19.0 | 19.0 |
| T5 / T5b | <= 45 / 55 % | 40.3 / 49.3 | 40.3 / 49.3 |
| T6 σ0; σ1 in window; cleared | >= 95; >= 95; >= 95 / 90 % | 100; 97.1-100 (raw 82.5-91.2); 24 / 24 | 100; 100 (raw 85.0-91.2); 24 / 24 |
| T7 sloppy; masher; dodger | <= 35; 0; 0 | 0; 0; 0 | 0; 0; 0 |
| T8 / T13 | <= 1 / 100 %, 0 | 1 / 53 of 53, 0 | 1 / 53 of 53, 0 |
| T9 walker kill Lv5 / 10 / 15 (pooled) | 150-185 s | 160 / 169 / 168 | 159 / 170 / 169 |
| T9b parrier σ1.5 kill | 125-170 s | 164 / 162 / 163 | 164 / 164 / 167 |
| T10 groggies / min | 0.8-1.6; <= 0.4 | 1.50 / 1.50 / 1.50; 0 | 1.50 / 1.33 / 1.50; 0 |
| T11 U / min | 0.8-1.5; 0.6-1.0 | 1.33; 0.67 | 1.33; 0.67 |
| T12 dodger σ1 (in window) | >= 95 % | 100 (raw 96.2 / 92.9 / 73.2) | 100 (raw 92.2 / 90.4 / 78.2) |
| W35 unparriable share | <= 35 % | 35 35 34 35 / 35 35 35 32 | the same |
Without the ladder the free-fight masher (F every 4 t; no band: T7 looks at the gauntlets only) blocks more: intake 191 / 190 ->
118 / 129 %/min (P1 / P2), perfect parries 30 / 36 -> 93 / 84, groggies 0 -> 0.67 / 0.44 per minute. Lane WB's `--only g,metro,chain`
rows (T7m: metronome 8-30 from every phase, 0 of 437 clears in G1 and G2) are the same tree's.

## Budgets
- **Items atlas**: 13 109 184 px (13.109 M <= 13.2 M; 1 510 sources) = 11-12 13.108 M + lane WB 1 280 px (`sw_rib_*` 3 x 256 +
  `sw_quad_*` 3 x 256 - `sw_path` 256); lane WC's half petals and lane WP's `tint` / `_hot` keep their sizes. 0.091 M left.
- **Commands per tick** (budget 830): test_scarlet P1 505, P2 524 (11-12: 500 / 519); test_flow the whole fight 381 (p1 451, p2 472,
  G1 402, G2 414, cs1 342, repel 395, lead5 431, ending 286). The integration adds: one gated line in `rlk:tick` (the stand-in rig
  without a beat), one self-tag test in `player/tick` (the dodge cut), one per `combat/apply` hit (her numbers; `test_m0diff` A
  +0.18-0.20 per tick against the release, its 40 failures unchanged).
- **Displays**: her rig 29 parts (`test_rig` 162 / 162, the elements budget unchanged); trail cards alive in a pattern <= 29
  (`test_blade`; round V's sweep cards 48), her kit cards <= 52 alive (`test_vi`, the ultimate), kit sprites 259 584 of 260 000 px.

## Gates (the final tree 1ac1e1cde + docs; suites from fresh copies of tools/dev/sim outside the tree)
| gate | result |
|---|---|
| regeneration (README 0-4 order) | after the WB merge rounds 1-4: `git status` empty every round; pack hash `4fdebef21ccd9807` in rounds 2, 3, 4 (round 1 re-sorted `items.json` of the WC + WP pack) |
| `check_mboss_pack.py` | 0 problems (4 mid-boss, 4 chapter, 3 special modules, 7 arenas) |
| loadcheck `wi_a` (WC + WP + fixes) and `wi_fin` (the final data) on the 26.3 server | 0 function load failures; `Starting minecraft server version 26.3`, `Loaded 1871 advancements`, `Done (1.439s)!` |
| `rplint.py rp_wi` / `atlas_px.py` | 0 problems / 13 109 184 px |
| hr: test_wi / test_vi | 215 / 215 / 208 / 208 |
| hr: test_cine / test_cam / test_seq / test_contact / test_actor / test_rig | 172 / ALL (164) / ALL (572) / 102 / 157 / 162 |
| hr: test_flow / ev_dry / test_scarlet / pat_p1 / pat_p2 / pat_ghost | 40 / 82 / 48 / 559 / 70 / 65 |
| hr: test_gauge / test_bal_hr / test_metro / test_input_hr / test_clips_h1c | 33 / 79 / 33 / 19 / 297 |
| hr: test_kit / test_blade / test_moon / test_hwamu / test_arena_hr | 15 361 / 347 (after the clock-check fix below) / 55 / 283 / 94 |
| hr: test_special_hr / test_reward / ident_hr / gen_check_hr (`--rp`) | ALL (98) / ALL (61) / passes / 28 of 28 (1352 s) |
| cb: test_cb / test_np / test_rm / chainparry | 400 / 125 / ALL (72) / 624 of 624 perfect, 0 refused, 117 patterns |
| bal: test_bal / test_bal_boss | 117 / 117 |
| 아를레키노: test_arlecchino / pat_p1 / pat_p2 / test_cm_ar / test_arena_fl | ALL / ALL / ALL / ALL / ALL |
| 아를레키노: test_rig | 67 of 67 with the 11-12 pack as `--ref-rp`; its source skin `S:ar/src/skin_33.png` is gone from this container, so the run used the 11-12 pack's `skin_p2.png` as that file (the two checks that compare against it then pin the pack's texture). `test_kit`: not runnable (the branch `wip/ar-s3` is missing, as before) |
| `az/tests_cm/run_all.sh` | the known statuses of README 0-9: fails `test_m0diff` (40, the release's 40), `test_px` 4e, `ident` (stale), the M0 suites that were never moved (files missing), the validators' missing baselines (`macro` / `lint`); ok `test_chapter`, `test_fw_az`, `test_fw_ap`, `gen_check`, `check_nbtpath` (invalid 0), `check_mboss_pack` |
| validators against the 11-12 release tree | `check_refs`: the same findings (only the function count differs); `lint_mc`: 53 011 problems on both, the same lines; `check_macro`: 3 878 -> 3 753 problems, every new one of the known "called with storage" kind (the new dodge clips' `pose/N {step}`, `dash_face` / `lite/face`, the side-number macros); `check_nbtpath` invalid 0 on both |

Found by the gates and fixed: **`test_blade`'s clock check** (lane WB) counted lane WC's `kill @e[…,tag=rlk_hr_sw]` lines at the
sequence starts / skips (`seq.KILL_FIGHT_FX`) as trail commands outside a pattern-tick file; a `kill` (also behind `execute … run`)
is a clean-up and no longer counts — every other line naming the trail's tags still must sit in a pattern-tick file.

## Files outside 홍련 (`boss/scarlet/**`), the camera (`mboss/cam/**`, `char/cine/**`) and the player (`player/**`, `char/motion/**`) that differ from `origin/wip/w`
| files | why |
|---|---|
| `combat/apply`, new `combat/text_normal_side`, `text_normal_side_n`, `text_crit_side` | the integration: her damage numbers (T3-09) |
| `tick` | the integration: the stand-in rig's tick without a beat |
| `combat/rc_hold`, `load` | lane WP: the held right-click's repeat flag (no double dodge from a held F5 press); the dodge set's constants (`#dgChW`, the cooldown pair), the ladder's constants gone |
| tools: `mboss_lib.py` | lane WC: the camera texts live on the live camera only (`mboss/cam/text`) |
| tests: `test_m0diff.py`, `ident_hr.py`, `test_cam.py`, `test_blade.py` | the integration: `LANE_WI_CMD`, the group `LANE_WI` (+ lane WP's `player/f_key`), D1 reads the round W groups, the clock check's kills |
No file of 파수꾼, the proto bosses, 나루카미, the other chapter / special bosses, the chapter 1-3 mobs, the arenas or the rooms differs.

## Pack files (`<S>/rp_wi` against `<S>/rp_rel3`, all from the generators; + the README)
Lane WC: `items/hr_cine/petal_half_{a,b}.json`, `models/item/hr_cine/petal_half_{a,b}.json` (`build_blank_tex.py`). Lane WP:
`textures/font/cb/tint.png`, the 31 `textures/player_motion/weapons/*_hot.png`. Lane WB: `textures/mboss/hr_kit/sw_rib_0..2`,
`sw_quad_0..2` (new), `sw_arc_0..2` (repainted), `sw_path.png` gone; models / item definitions `mboss/hr_kit/{sw_band, sw_rib_0..2,
sw_fan_0..2, sw_quad_0..2}` new, `{sw_path, sw_arc_0..2}` gone. Shared: `atlases/items.json`. The integration: `README.md` (rows for
the half petals, the trail kit, `tint` / `_hot`, the atlas total; diff `wi_rp_readme.diff`; the version line is the lead's).

## Open (for the lead)
- **T1 on seed 33 is 0.97** on the final tree, as on the 11-12 release tree (pooled 1.01): no balance value changed.
- **(Resolved by the lead, `wip/w-fix` 9bf091333: sideways-and-back, alternating sides; a held direction stops short of an enemy.)** Was: a direction-less double dodge goes along the view (lane WP's `dash_dir`): facing her, the cartwheel goes into her (0.58 b in
  `dodgecam`). The reference's double dodge is a sideways cartwheel; whether to send it sideways / back when no direction is held is a
  design call (README 0-9 「홍련 — 남긴 것」).
- **T3-09's rest**: the skills' smoke / flames / pillars over her are each character's own effects: not touched.
- **The free-fight masher** blocks more without the ladder (intake 191 -> 118 %/min in P1, 30 -> 93 perfect parries): no band
  covers it (T7 looks at the gauntlets, which no metronome clears).
- **`test_m0diff`**: the integration's per-hit line is named apart (`LANE_WI_CMD` 0.2); the budget decision stays the lead's.
- The old chapter-boss fair sims model the pre-11-10 dash (lane WP's list): not gated, not changed.
- The pack's version line, README 0-1 / 0-10 and the build stamp: the lead's.

## Only a person in the game can check
The merged, deduplicated list is README 0-9 「홍련 — 게임에서 확인할 것」, the 11-12 round W line W①-W⑳ (the cutscenes W①-W⑧, the
player W⑨-W⑭, the fight W⑮-W⑳); it replaces round V's ⑩ (the petals), ⑫ ⑬ (the drawn path and the slash pieces), ⑱'s path part and
⑳ (the beat with the path).
