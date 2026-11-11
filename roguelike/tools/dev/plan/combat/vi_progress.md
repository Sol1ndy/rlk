# Round V, lane VI (the integration of lanes VC / VP / VB) — progress and report

Branch `wip/v-int` (from `origin/wip/v` 2793b54cd), worktree `<S>/cb/wt_vi`, pack `<S>/rp_vi` (from `<S>/rp_fin`, the 11-11b
release pack); `<S>` = the scratchpad of `v_brief.md`. Contract: `v_brief.md`, the three lanes' progress files (`vc_progress.md`,
`vp_progress.md`, `vb_progress.md`). The release entries (README 0-1, 0-10, the build stamp, the pack's version line) are the
lead's and are NOT written.

## Steps
- [x] merges (merge commits): `wip/v-cam` 303407e78, `wip/v-player` 477b8977a, `wip/v-boss` 252f88ca3 and its final head 1163bba57
- [x] full regeneration in README 0-4 order, twice: no change in the tree, the same pack hash
- [x] the cross-lane requests (below) and what the seams showed (below)
- [x] `tools/dev/sim/hr/tests/test_vi.py`: the three lanes together (208 checks)
- [x] hrfair 2.0 on the merged tree and on the final tree; T1 restored
- [x] docs (README 0-4 / 0-8 / 0-9 / 3 / 홍련, `hr_design.md` §10, the pack's README + `vi_rp_readme.diff`), gates

## How to run
```bash
S=<scratchpad>; W=$S/cb/wt_vi/roguelike; RP=$S/rp_vi; cd $W
# the whole regeneration (README 0-4; twice: `git status` empty, the pack hash the same)
node tools/build_scarlet_rig.mjs --resourcepack $RP && python3 tools/build_mboss_hr_fx.py --resourcepack $RP \
  && python3 tools/build_bossbar.py --resourcepack $RP && python3 tools/build_combat_fx.py --resourcepack $RP \
  && node tools/build_player_rig.mjs --datapack . --resourcepack $RP && python3 tools/build_player_audio.py \
  && python3 tools/build_blank_tex.py --resourcepack $RP && bash tools/dev/regen_all.sh . --mobs \
  && python3 tools/build_mboss_bf_fx.py --skip-rp && python3 tools/build_mboss_fg_fx.py --skip-rp
(cd $RP && find . -type f -print0 | sort -z | xargs -0 sha1sum) | sha1sum
# the suites: from a copy of tools/dev/sim outside the tree, the old scratchpad paths rewritten (tools/dev/sim/README.md 1 B)
SIM=<work>/sim; cp -a $W/tools/dev/sim $SIM; (cd $SIM && grep -rl --exclude='*.md' --exclude='*.json' 2f5e7b47-ba2f-58bc-b880-1598991e2f8e . \
  | xargs sed -i "s|/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad|$SIM|g")
cd $SIM/hr/tests && python3 test_vi.py $W [beatpat|follow|swap|beatseq|skip]      # 4 min; --keys=a1,a9 narrows beatpat
cd $SIM/hr/review/bal && python3 hrfair2.py $W --out <dir> --jobs 3                 # 175 runs, about 20 min (the tree must not change meanwhile)
```

## Merge notes
| merge | conflicts | resolution |
|---|---|---|
| `wip/v-cam` | none | |
| `wip/v-player` | `README.md` 0-4 (the player-rig line), `hr_design.md` (both appended a section) | README: lane VP's wording of the line, lane VC's `build_blank_tex.py` line kept after it; hr_design: both sections kept |
| `wip/v-boss` (252f88ca3, then 1163bba57) | `hr_design.md` (a third appended section) | all three kept |

`tools/build_mboss_core.py` (lane VC's FN-cam block and lane VP's `# VP beat` hooks) and every generated file merged without a
textual conflict; the first full regeneration of the merged tree changed nothing (`git status` empty after round 1 and round 2:
the merge of the generated outputs was already what the merged generators write). The pack's hash differs between the first
round on a copy of the 11-11b pack and the second (the order of `items.json`, README 0-9); from then on it is stable.

## The cross-lane requests
| request | what was done |
|---|---|
| VP -> VB: her effect kit on the beat's clock | `tools/build_mboss_hr_fx.py`: `fx/e/make` and `fx/e/world` read the game time minus `#btLag cb`, `fx/e/world` re-schedules itself on a held tick (its second command), the ambient firefly phase too. **Not** the five HUD reads (the typed line `#lnE`, the overlay `#ovS..#ovE`, `#now2`): they mirror `title` timers that run on the client in real time; on the beat's clock the server would think a line / an overlay is still up after the client dropped it. The kit harness `hr/s1k/lib/hrfxsim.py` starts with the beat at rest (`#btLag` / `#btHold` 0). Proof: `test_vi beatpat` (the kit's live cards and their remaining life equal beat on / off on every world tick; on the pure merge the same check fails: a card dies 5 / 7 ticks early and ages on held ticks) |
| ... "the path head still arrives on the hit tick under the beat" | lane VB's path / head / slash are literal commands on pattern ticks, so they were already right; `test_vi beatpat` checks it for every pattern: each head disappears on a world tick a hit lands (beat on), the sweep cards are identical beat on / off on every world tick and do not move on a held tick |
| VB -> VP: stretch the sweep cards in the slow motion | `player/def/beat/st/tp_on` also takes `rlk_hr_sw` (the `teleport_duration` x 3 pass at beat tick 5, undone by `tp_off`); cards born during the slow motion are not stretched (they step once per world tick) |
| VC -> VB: the core's Shift skip | kept parked (`#skip hr -1`, set by `seq/<name>/skipin`), and `core/skip` / `core/skip_cs1` now read `rlk:in_jump`; `api.SKIP_HINT` = ' · Space 길게' (the kit's `fx/hud/skip` text). No function of her module reads `rlk:in_sneak` (`test_vi follow`) |
| VC -> VB: `rig/follow_now` wherever the core teleports her body inside a hook | `s3lib.RIG_NOW` after the gauntlets' reappearances (`p_ghost.tp_spot`: d1-d4, the drop, the dive), a cancelled leap's landing (`core/ground_to`, used by `core/ground` and `g/ground`), the revive's placing (`core/place8`), the replay's seat (`core/replay/start`). Measured with seqsim's follow model in the fight (`test_vi follow`): on the pure merge (and on 11-11b) her model stood up to 13.6 b from her body for 34 ticks of G1 and 65 of G2 (3-16 ticks after every reappearance, 16 during the dive's wind-up, 29 after the revive's placing); now 0. Incremental moves (walk, dash steps) keep the one-tick trail (0.12 b typical, <= 0.3 b): see Open |
| VC -> lead: the developer fallback mob | `room/mob_summon` (hand file): a zombie with an unbreakable leather helmet (the skeleton's sun rule), tag `rlk_m_husk` kept (its stats); `ident_hr.py` allows the file |
| VC -> lead: the pack is built with `build_blank_tex.py` | in the regeneration order above and README 0-4 |
| VP -> lead: the pack's README | `<S>/rp_vi/README.md`: the `rlk:cb` row (U+EE00-EE0D + EE1E / EE1F, every cell <= 256 px), `rlk:bossbar` + U+E440, the blank textures, the weapon glow / `_hot` sprites / `wg`, the part models' tint, the kit's `sw_*` and `glow_edge`, the generator table, the font-cell rule, the atlas total. The diff against the 11-11b pack's README is `vi_rp_readme.diff` (the pack is not in git). The version line is the lead's |
| VP -> lead: README 0-9's `test_m0diff` numbers | written (0-9 「틀 · 시험」) |
| VP -> lead / VB -> VC: the ident lists | `ident_hr.py` + the integration's group; `test_cam.py` D1 / D2 read the other lanes' files from `ident_hr.py`'s round V groups and know the beat's words in `rlk:tick` |
| VB open: hrfair 2.0 in full | below |
| VP -> VB (optional): her own rocked-back pose | not done (the generic 16-degree tilt applies): listed in README 0-9 |
| VC -> VB (optional): `fx/hud/line`, VC -> VP (optional): rplint and the blank textures | nothing needed (rplint passes them) |

## What the seams showed (found by `test_vi.py` and the gates, fixed here)
1. **The stand-in rig next to the actor.** A beat that is running when a locked sequence starts ends one tick later
   (`beat/clock` at the head of the next tick); for that one tick lane VP's stand-in rig of a mannequin character (`rlk_pl`,
   posed by `beat/post` after the fight tick) stood beside lane VC's actor: two bodies. `char/cine/hide` now takes `rlk_pl` out
   of view like the rig characters' displays (`tools/build_player_cine.mjs`).
2. **Her model in the gauntlets** (the follow_now row above): the drawn path, the cue and the hit were at her body, her model
   was where she had vanished.
3. **`az/tests_cm/gen_check` 9** failed on the merged tree: since lane VC `build_mboss_core.py` writes
   `data/rlk/advancement/mboss/cam_post.json`, which the suites' variant trees hard-linked, so the core run in a copy rewrote the
   tested tree's file in place (same bytes). `REAL_DP` and the five `cmsim.variant` lists copy that folder for real now.
4. **`test_m0diff` C** (the boss bar draw against the 10-20 release): lane VB's `#buSubSeg bu` costs every boss bar draw 2
   commands; the draw stood exactly at its budget (+6), so 12 checks failed on the merged tree. Not reduced (the option is lane
   VB's design: a per-draw reset like `#buHpCol`); named apart as `LANE_VB_DRAW` 2, as lane VP did for its own line (README 0-9).
5. **`ar/tests/test_rig`** (아를레키노): her P1 body names the avatar's `arle` part models, which lane VP gave `tintindex 0` + a
   tint defaulting to white (no visible change: her rig sets no colour). The box comparison ignores `tintindex` now; the
   byte-comparison with the previous release pack fails by design for `arle/{head,body,right_arm}` (67 / 67 against the round V pack).
6. **hrfair**: T1 on seed 33 (below).

## The interaction checks (`tools/dev/sim/hr/tests/test_vi.py`, 208 / 208)
| section | what | result |
|---|---|---|
| `beatpat` (116) | every pattern of `api.P1` + `api.P2` (a1 a2 a3 a3s a4 a6 a9 a10 d4 tri rings ult hcut blue kcut mx nb q) and both gauntlets in the H1 world with the REAL kit, answered perfectly (F one tick before each parryable hit; a second run perfect-dodges the unparriable ones), beat off and on | beat on = beat off on every world tick: the pattern clock and every `# hr` / `# mb` score, her body, the rig calls, the sweep cards (<= 53 alive), the kit cards with their remaining life (<= 52), the hazards, the judged hits, both health pools; held = 5 x parries + 7 x dodges = `#btLag`; nothing of hers changes on a held tick; every path head is gone on a hit tick; G1 9 / G2 11 perfect parries, the gauge and the result as with the beat off. 28 beat-on runs, 353 held ticks, 58 perfect parries, 9 perfect dodges |
| `follow` (6) | her model against her body in G1, G2 (failed, with the revive's placing) and 900 t of free P1 / P2 | within 0.5 b at the end of every tick (the farthest 0.30 b) |
| `swap` (30) | the avatar / the stand-in rig / the actor with the real `char/cine/**`, `char/motion/beat/**`, `char/motion/lite/**`, `player/def/beat/**` in `rlk:tick`'s order: 7 characters x (perfect parry, perfect dodge) x (no lock, a lock starting at every beat age 0-17 / 0-27) | exactly one visible body at the end of each of 36 960 ticks (outside the lock the avatar, its stand-in rig or its own rig; inside it the actor alone, the avatar invisible and blank); one tick into the lock nothing of the beat is left; after the hand-back the avatar / rig is back as it was (profile, hand), no glow, no tint, no stand-in part |
| `beatseq` (34) | the real core, sequences and lock (test_flow's world) on the beat's clock: CS0, P1 with the parrier (12 beats), then a beat started by the judge 0-7 world ticks before CS1 (the 60 % floor), before the repel (G1 cleared: 9 beats in the gauntlet) and before lead5 (the 5 % floor) | CS1 and the repel: the sequence starts on the same world tick with the beat at age 0 / 6 / 9 (parry) and 0 / 2 / 4 / **8 / 11 (inside the slow motion)** / 14 (dodge); one real tick later nothing is held and no tick is held after; the camera holds the player from the first tick with the client on the live camera on every tick; the same end tick, a clean hand-back, the same state afterwards. `lead5` is a lead-in of the fight (no lock): the beat runs its own length and the lead-in still starts and ends on the same world ticks |
| `skip` (22) | the Space skip of CS0 and CS1 with a parry / dodge beat started when Space goes down, 10 ticks into the hold and on the skip tick itself; with W + A + sprint, S + D, Shift, Shift + W + a dodge beat held; with Space held since before the window | the skip fires on the same tick and lands in the plain skip's state (test_seq's K1 state) with the client on the live camera on every tick; the beat is over one tick after it started and never holds a tick; nothing is counted before the window (the skip fires on its 20th tick) |

A beat cannot naturally be running when CS1 or the repel starts (CS1 comes at the next AI decision, at least 20 world ticks
after a pattern's last hit; the repel at the judge, 24 ticks after the last cut): the cases above are forced through the beat's
own start functions. Not covered: the F key itself during a locked sequence (seqsim has no F input; `player/f_key` is the
suites' `test_cb` / `test_input_hr`).

## Budgets
- **Items atlas**: 13 107 904 px (13.108 M <= 13.2 M; 1 505 sources) = 11-11b 12.940 M + lane VP 0.149 M + lane VB 0.019 M.
  Nothing had to be cut; 0.092 M is left (the cheapest cut later: the 31 `_hot` weapon sprites).
- **Commands per tick** (budget 830): test_scarlet P1 500, P2 519; test_flow the whole fight 377 (p1 447, p2 469, G1 397, G2 407,
  cs1 333, repel 392, lead5 429); the worst sustained case stays lane VP's estimate (a gauntlet answered perfectly: about 405-440).
  The integration adds: her kit's world + 2 commands on a tick with cards and + 1 per card made; `rig/follow_now` (36 commands)
  on the 5-6 reappearance ticks of a gauntlet; one selector line in `beat/st/tp_on` (a dodge beat's tick 5); one line in
  `char/cine/hide`.
- **Displays**: her rig 29 parts (elements budget 6 500 unchanged), kit pools 96 / 48 / 4, sweep cards <= 48 in a pattern
  (rings; 53 for one tick when the ultimate follows), kit cards <= 52 alive (the ultimate).

## Balance (hrfair 2.0, all 175 runs; logs `tools/dev/sim/hr/review/bal/vi_merged.log`, `vi_final.log`; 11-11b = `hb_final.log`)
| row | band | 11-11b | merged tree (8c9d657b2) | final tree |
|---|---|---|---|---|
| T1 P1 walker / 타키 | 1.00-1.15 | 1.01 / 1.03 / 1.01 | 1.02 / 1.03 / **0.97** | 1.07 / 1.08 / 1.02 |
| T1b parrier s3 / walker | <= 0.60 | 0.50 / 0.52 / 0.58 | 0.514 / 0.594 / 0.593 | 0.509 / 0.595 / 0.590 |
| T1c | <= 5 | 0 | 0 | 0 |
| T2 P2 walker / 타키 | <= 1.25 | 1.06 / 0.99 / 1.03 | 1.03 / 1.01 / 1.04 | 1.08 / 1.06 / 1.09 |
| T3 standing / the Guardian | <= 1.8 | 1.47 / 1.50 / 1.51 | 1.47 / 1.50 / 1.51 | 1.54 / 1.57 / 1.58 |
| T4 worst 40 t | <= 40 % | 19.0 | 19.0 | 20.1 |
| T5 / T5b | <= 45 / 55 % | 40.3 / 49.3 | = | = |
| T6 s0; s1 in window (raw); cleared | >= 95; >= 95; >= 95 / 90 % | 100; 97.1-100 (82.5-91.2); 24 / 24 | = | = |
| T7 | <= 35; 0; 0 | 0; 0; 0 | = | = |
| T8 / T13 | <= 1 / 100 %, 0 | 1 / 53 of 53, 0 | = | = |
| **T9** walker kill Lv5 / 10 / 15 | 150-185 s | 161 168 168 / 156 171 171 / 167 165 165 | 164 171 168 / 162 166 166 / 155 171 171 | the same |
| T9b parrier s1.5 kill | 125-170 s | 162 / 162 / 162 | 164 / 162 / 163 | the same |
| T10 groggies / min | 0.8-1.6; <= 0.4 | 1.33; 0 | 1.50 / 1.50 / 1.50; 0 | the same |
| T11 U / min | 0.8-1.5; 0.6-1.0 | 1.50 / 1.33 / 1.50; 0.67 | 1.33 / 1.33 / 1.33; 0.67 | the same |
| T12 in window (raw) | >= 95 % | 100 (94.2 / 96.4 / 74.6) | 100 (96.2 / 92.9 / 73.2) | the same |
| W35 unparriable share | <= 35 % | 35 35 34 35 / 35 35 35 32 | = | = |

Lane VB changed no hit tick, shape, tier or weight, but where she stands after a move (2 b before the player after a dash, the
dives 1.4 b short, the lower leaps) shifts the band the next pick starts from. On the merged tree every row passes except
**T1 on seed 33** (0.974; pooled 1.008). Restored with one constant: `api.DMG['T2']` 42 -> 44 (raw 6 -> 7, 15 -> 17 HP on the
item-less Lv15 player; the smallest coefficient of raw 7): a damage tier changes no pick, no clock and no hit tick, so the
dynamics are bit-identical (the pattern mix lines of the two logs are the same) and only the intake rows move. Hit ticks and
`api.NP_SHARE_MAX` are untouched. The tier is within §6.4's knob range (+ 4.8 %).

## Gates (the final tree; suites from a copy outside the tree)
| gate | result |
|---|---|
| regeneration twice (the order above) | round 1 and round 2: `git status` empty; pack hash `2fb1f3897247c768…` both rounds (the pack's README included); a third round on the committed head: the same |
| `check_mboss_pack.py` | 0 problems (4 mid-boss, 4 chapter, 3 special modules, 7 arenas) |
| loadcheck `vi_1`, and `vi_2` on the pushed head (26.3 server) | 0 function load failures; `Starting minecraft server version 26.3` and `Done (` in the log; 1871 advancements |
| `rplint.py $S/rp_vi` / `atlas_px.py` | 0 problems / 13 107 904 px |
| hr: test_cam / test_seq / ev_dry / test_flow | ALL (ident D1 / D2 on the merged tree) / ALL (749 s) / 82 of 82 / 40 of 40 |
| hr: test_cine / test_contact / test_actor / test_rig | 159 / 94 / 158 / 162 |
| hr: test_scarlet / pat_p1 / pat_p2 / pat_ghost | 48 / 559 / 70 / 65 |
| hr: test_gauge / test_bal_hr / test_metro / test_input_hr | 33 / 79 / 30 / 17 |
| hr: test_moon / test_hwamu / test_arena_hr / test_clips_h1c | 55 / 283 / 94 / 297 |
| hr: test_kit / test_blade / test_special_hr / test_reward | 15 284 / 7 812 / ALL / ALL |
| hr: ident_hr / gen_check_hr (`--rp`) | passes / 28 of 28 (1331 s) |
| hr: **test_vi** | 208 of 208 |
| cb: test_cb (beat 49, beatloop 25 + 9 for 홍련, the rest) / test_np / test_rm | 383 / 125 / ALL |
| bal: test_bal / test_bal_boss | 117 / 117 |
| 아를레키노: test_arlecchino / pat_p1 / pat_p2 / test_cm_ar / test_arena_fl | ALL / ALL / ALL / ALL / ALL |
| 아를레키노: test_rig | 67 of 67 with the round V pack as `--ref-rp`; 66 of 67 against the 11-11b pack (the avatar models' tint, by design); `test_kit`: not runnable here (the branch `wip/ar-s3` is missing, as before) |
| `az/tests_cm/run_all.sh` | the step statuses of the base tree `origin/wip/v`: fails test_m0diff (40 checks: the base's 38 + the A budget of proto and 나비 with lane VP's line), test_px 4e, ident, the suites that were never moved, the validators' missing baselines; ok test_chapter, test_fw_az, test_fw_ap, **gen_check** (after fix 3), check_nbtpath, check_mboss_pack |
| validators against the base tree (`check_refs`, `check_macro`, `check_nbtpath`, `mb/lint_mc`) | no new kind: refs 70 missing references on both trees (one line number moved), nbt invalid 0, macro + 380 of the known "called without args" kind (`function … with storage` in the new 홍련 / avatar files), lint 53 007 -> 53 011 problems, all of the known kinds (`time`, `spectate`, `gamemode`, `advancement`, `return run schedule`) |

## Files outside 홍련 (`boss/scarlet/**`), the camera (`mboss/cam/**`, `char/cine/**`) and the player (`player/def/**`, `char/motion/**`) that differ from `origin/wip/v`
| files | why |
|---|---|
| `boss/{apep,arlecchino,azhdaha,tachy}/fx/e/{make,world}`, `mboss/{butterfly,fieldgen}/fx/e/{make,world}`, apep `fx/p/{beam_rain,gold_motes,helix_trail,whirl_leaves,e/tether}` + `fx/prop/e/spin`, arlecchino `fx/decal/e/flood_re`, azhdaha `fx/e/cardf` + `fx/tele/wave_to` | lane VP: the six kits' card clocks on the beat's clock (`- #btLag cb`, the hold line of `e/world`) |
| `boss/azhdaha/{ai/sample4,on_hit}`, `mboss/fieldgen/{on_hit,field/banner,hud/banner_cut}` | lane VP: game-time stamps of the modules minus `#btAdj cb` |
| `mboss/main`, `mboss/np_gate`, `mboss/pl_dot2`, new `mboss/d/beat_{parried,release,rock}` | lane VP: the hold hook (first line of `mboss/main`), the glint spacing clock, the untouchable test, the beat dispatchers (`build_mboss_core.py`) |
| `bossui/draw`, `bossui/sub` | lane VB: the under bar's segment dividers (`build_bossbar.py`) |
| `tick`, `load`, `uninstall`, `mob/tick`, `player/{tick,hurt_elem,dash_go}`, `combat/{do_swing,on_skill}`, new tag `entity_type/beat_disp` | lane VP: the beat's clock and gates (hand files) |
| `combat/sap_absorb`, `cm/lure_new`, `lvup/tick` (a comment), new `advancement/mboss/cam_post.json` | lane VC: the loot line held back during a lock, the lure's blank skin, the tick advancement |
| `room/mob_summon` | the integration: the fallback mob is a zombie |
No file of 파수꾼, the proto bosses, 나루카미, the chapter 1-3 mobs, the arenas or the rooms differs.

## Pack files (`<S>/rp_vi` against `<S>/rp_fin`: the union of the three lanes' lists, all from the generators; 235 files differ + the README)
Lane VC: the three blank textures. Lane VP: `font/cb.json` + 14 `textures/font/cb/*.png` (the old four gone), the 31 `_hot`
sprites + `wglow_{blade,orb}`, the five `weapons/*_glow` and the `wg/**` models / item definitions, every part model and item
definition of the seven characters. Lane VB: `hr_kit/{sw_path,sw_head,sw_arc_0..2}` (+ models, item definitions), `cue_0`,
`scarlet/glow_edge` and the four crossed glow models, `font/bossbar.json` + `seg.png`. Shared: `atlases/items.json`. The
integration: `README.md`.

## Open (for the lead)
- **The one-tick trail of her model** behind her body on incremental moves (README 0-9 「홍련 — 남긴 것」): `execute at @s run
  function …rig/tick` in her four hooks would end it at no cost, but makes `seq.RIG_NOW` redundant and needs test_seq's mutation
  check changed. Not done.
- **The balance sits near its edges**: T1 seed 33 1.016, T1b 0.595 / 0.590, T10 1.50 (band to 1.6). T2 44 is one constant if the
  lead prefers the 11-11b damage and accepts T1 0.97 on one seed.
- **`test_m0diff`**: lane VB's 2 commands per boss bar draw (allowance `LANE_VB_DRAW`), lane VP's hold line and kit clock lines
  (README 0-9 numbers): a budget decision, as before.
- 홍련's own rocked-back pose for the beat (lane VP's optional request): not built.
- The pack's version line, README 0-1 / 0-10 and the build stamp: the lead's.

## Only a person in the game can check
The merged, deduplicated list is README 0-9: 「전투 개편 C」 the 11-12 line ①-⑨ (every enemy: the beat's feel, the retimed
interpolation, the rocked-back attacker, the weapon glow, the overlays without a box, the stand-in rig, the pull-in, the NoAI
hold, tier 2 / 1 reading as "blocked") and 「홍련 — 게임에서 확인할 것」 the 11-12 line ①-㉔ (the camera ①-⑪, the wind-ups /
path / slash ⑫-⑲, the fight under the beat ⑳-㉒, the T2 hits and the zombie ㉓-㉔).
