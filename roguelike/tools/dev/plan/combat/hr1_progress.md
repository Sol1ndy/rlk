# lane H1 (홍련 rebuild: the fight) — progress

Branch `wip/combat-hr1` (from `origin/wip/combat` c7dcc4fbf; merged 6522feef5), worktree `<S>/cb/wt_hr1`, pack copy
`<S>/rp_hr1` (`<S>` = the scratchpad of `h_common.md`; the scratch sim copy and run logs were deleted at the end). Contract: `hr_design.md` (§8 wins).
Owner of `tools/mboss_scarlet/{api,ai,p1,p_ghost,core,shield,s3lib}.py`, `tools/build_mboss_scarlet.py`, FN-bal, the
pattern / gauntlet / gauge / balance suites and `hrfair` 2.0.

## Steps
- [x] **H1 interface** (15fad96a9): §5.1 in `api.py`, the rig contract of 59 clips, FN-bal, the sequence wiring.
- [x] **build 1** (90e1eaa59): the state machine (§1.1), the gauge (§1.2), balance + the groggy (§1.3-1.4), the
      interrupts (§1.5), every pattern of §2.2 with the cue / the flashes, the AI, G1 / G2, the judge, the fails, the
      banner, the test ids.
- [x] **build 2** (ee454c554): the suites of §6.1, the reach clamps, the fixes they found.
- [x] `hrfair` 2.0 (d4befffdd) and the first T1-T13 table (below); first tuning pass (`GAUGE['hit']` 2, `RECOVER` + 4).
- [ ] HI: final balance (the knobs of §6.4), the README's 홍련 section, the old suites that pin the 11-06 fight.

## How to run
```bash
S=<scratchpad>; WT=$S/cb/wt_hr1/roguelike; cd $WT
bash tools/dev/regen_all.sh .                       # datapack (the kit with --skip-rp, the module, bal, the pack check)
node tools/build_scarlet_rig.mjs --resourcepack $S/rp_hr1 && python3 tools/build_mboss_hr_fx.py --resourcepack $S/rp_hr1
RLK_DEV=$S bash tools/dev/loadcheck.sh $WT hr1
# the suites never run inside the tested tree: a sim copy with the old scratchpad path rewritten (sim README 1-B)
SIM=$S/cb/hr1_sim; rm -rf $SIM; cp -a $WT/tools/dev/sim $SIM; (cd $SIM && grep -rl --exclude='*.md' --exclude='*.json' \
  2f5e7b47-ba2f-58bc-b880-1598991e2f8e . | xargs sed -i "s|/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad|$SIM|g")
cd $SIM/hr/tests && for t in pat_p1 pat_p2 pat_ghost test_gauge test_bal_hr test_scarlet; do PYTHONDONTWRITEBYTECODE=1 python3 $t.py $WT | tail -1; done
cd $SIM/hr/review/bal && python3 hrfair2.py $WT --out <dir> [--quick] [--only p1,p2,g,kill,chain]   # ~50 min full, 4 processes
```
After editing a suite in the worktree copy `hr/tests` and `hr/review/bal` into the sim copy again. Stale outputs of removed
pattern keys are not swept by the generator (it owns `p/<current key>/` only): `p/r1 p/r2 p/r3` were deleted by hand once.

## What is built (by design section)
- §1.1 state machine: CS0 (1440, skip → 1290) → P1 → CS1 (720, skip 40-560 → 566, cine, bars off) → `lead60` (56,
  bars on, gauge 5/5 at its tick 0) → G1 → gauge 0: `repel {at:60}` in the judge tick (140, bars on, 15 / 15 / 15 ‰) →
  P2 at once (first decision after 20 t; `#ph 6` never occurs) | fail: 500 ‰ + push, P2 at T + 240. P2 → `lead5` (116) →
  G2 → `repel {at:5}` (15 / 15 ‰, the kill at 129) → the ending (1372) → the coda | fail: the instant death → the revive
  stance 60 t → `lead_re {g:a13}`. Removed: SQ1, the down window, `lead_down`, R1-R3, the moon discs, the dark look
  requests, the dash-timed pips, test ids 25 / 31.
- §1.2 gauge `#gau hr` (0-50): +3 per pattern end (not A6 / U), +5 per landed hit (`core/ev` reads `#mbHitEv`), cap 50,
  U spends it at its second cut; full → the next near / mid decision is `rings` then `ult` (`core/ult_go`, `#ultq`);
  under bar `#gau / 10` of 5 from control to the ending. In a gauntlet: `shield/tick` takes one segment when
  `#mbDodgeOk mb 1` and `#parT tmp 3`, checked every gauntlet tick (the hazard strikes after the module tick, so the
  event is seen at strike + 1, or + 2 for the second tick of the cut's 2-t window; not "s and s + 1").
- §1.3-1.4 balance: `bal_ok` refusals (floor reserved, sequence, replay, revive wait, ghost, invulnerable, a4 2-20,
  a10 2-22, nb 2-46, q 16 → end, hcut / a9 / kcut / blue go → cut, ult cut1 → cut2, mx's streak and retreat, A6 0-4),
  `bal_on` = cancel + `grog_in`, `bal_tick` = `down` at grgT 88, `kipup` at 20, a floor reached cuts grgT to 20,
  `bal_off` = 12 t recovery; `#mbBalOff mb 1` from `lead60` / `lead5` / `lead_re` / the revive stance to P2;
  `core/bal/floor` (pending dropped, bal 3) at CS1 / `lead5`; `core/bal/repel` (+3) after `repel {at:60}`.
- §1.5 interrupts: the counter and A6 triggers as before; `core/pp` + `core/ppf` = the perfect-parry flinch on the last
  hit of a1 a2 a3 a3s d4 tri rings mx (ground patterns; a4 / nb / q end in the air or on an N hit: no flinch);
  pause in a gauntlet → `lead_re {g}`; pause / reload in CS0 / CS1 / the repel → their end state, in a lead-in → from 0
  (`#grs` 6-9).
- §2.1-2.2 patterns: `p1.py` a1 a2 a3 a3s a4 a6 a9 a10 d4 tri rings ult hcut blue kcut; `p_ghost.py` mx nb q. Every
  hazard has an explicit `noparry` (P 0 / N 1); the cue (`glint {c:2}` at `blade_mid` + `parry_cue`) exactly 7 t before
  every P hit; the flashes of `api.FLASH_AT` on her chest (`yellow_tell` / `star4` / `flash_blue` + their sounds).
  q per §8.2: purple at 8, the grab unparriable; the branch is taken at tick 21 (`api.Q_AIR_T0`), q_air's events are
  21 + their clip tick.
- §2.4 gauntlets: `A8_SCRIPT` 9 cuts / judge 220, `A13_SCRIPT` 11 cuts / judge 242, the cue at each lock, `BOLTS`,
  `EXTRA_VANISH`; gauge 0 → `#done` in the judge tick; the fails as before; the banner from the refill beat.
- AI: `WEIGHTS` / `COOLDOWN` / `MID_MAX` / `MID_MIN` (hcut ≥ 8 b) / `FAR_RULE` (fallback glide + a3s), the full-gauge
  rule before the rear / far rules, mx's repeat at ≤ 30 % HP (60 %).
- Test ids (§5.1): 1-18 patterns (12 = gauge full + rings → ult), 19 groggy, 20-24, 26-30, 32-38, 80, 90-92, 99.

## Gates
| gate | result |
|---|---|
| `regen_all.sh` twice | identical; `check_mboss_pack` 0 |
| loadcheck | `hr1_if` 0, `hr1_b2` 0, `hr1_b3` 0, `hr1_fin` 0 (the final tree) |
| rplint / atlas | 0 / 12.919 M; `diff -rq rp_base rp_hr1` empty (no pack file added or changed) |
| new suites | pat_p1 529 / 529, pat_p2 67 / 67, pat_ghost 65 / 65, test_gauge 22 / 22, test_bal_hr 48 / 48, test_scarlet 47 / 47 |
| tick cost | P1 466, P2 476 commands / tick on average over 1200 t (budget 830) |
| old hr suites | pass: test_special_hr, test_reward, test_moon 55, test_hwamu 283, test_arena_hr 94. Fail for other lanes' parts or pins of the 11-06 fight: `ev_dry` (KeyError `lead60`: lane H2's sequences), `test_kit` 13262 / 13273 (11: the sound count 104 → 110, call-site pins of removed files `p/r2` / `core.a9`, the `qi_line` axis rule on the new tri / kcut lines, the judge's deflect effects that moved to the repel), `test_rig` / `gen_check_hr` (need `--rp`; cinematic and fight clips are placeholders until H1c / H2c), `ident_hr` (pins the 11-06 tree) |

## hrfair 2.0 — measured (item-less Lv15 vs L16, seeds 11 / 22 / 33, 3 600 t per phase; 158 runs)
Column A = the design's *start* values; column B = after the first pass (`GAUGE['hit']` 5 → 2, `RECOVER` + 4 t:
P1 12-20, P2 14-20; the A6 trigger measured for real: the probe's skill hits now set `#skillDmg`). B is what is committed.

| # | target | band | A (start values) | B (committed) | |
|---|---|---|---|---|---|
| T1 | P1 walker intake ÷ 타키 whole (recorded 124.0 %/min) | 1.00-1.15 | 256.7 %/min = 2.07 × | 237.9 = 1.92 × | miss (not comparable: see below) |
| T1b | P1 parrier σ 3 ÷ walker | ≤ 0.60 | 0.59 | 0.59 | pass |
| T1c | P1 mixed σ 0 intake | ≤ 5 %/min | 0.0 | 1.4 | pass |
| T2 | P2 walker ÷ 타키 | ≤ 1.25 | 266.3 = 2.15 × | 244.0 = 1.97 × | miss (as T1) |
| T3 | standing max(P1, P2) ÷ Guardian standing (recorded 164.0) | ≤ 1.8 | 1.63 | 1.47 | pass |
| T4 | walker's worst 40-t window | ≤ 40 % | 15.7 % | 20.5 % | pass |
| T5 / T5b | every cut on a standing agent, G1 / G2 | ≤ 45 / ≤ 55 % | 40.3 / 49.3 % | same | pass |
| T6 | parrier σ 0 (stand / walk × 3): perfect per timed F; cleared | ≥ 95 % | 100 %; 24 / 24 | same | pass |
| T6 | parrier σ 1: perfect per timed F; cleared | ≥ 90 % | 87.1 %; 24 / 24 | same | first half unattainable (86.6 % is the window's own limit at σ 1); cleared passes |
| T7 | sloppy / masher / dodger clears | ≤ 35 %; 0; 0 | 8 %; 0 %; 0 % (0 damage) | same | pass |
| T8 | A6 starts in any 400 t | ≤ 1 | (0: the probe's skill hits did not flag) | 1 | pass |
| T9 | walker kill, fighting time Lv5 / 10 / 15 | 150-185 s | 174 / 179 / 177 | 182 / 191 / 184 | B: Lv10 6 s over (A6 now blinks away from the walker) |
| T9b | parrier σ 1.5 kill | 125-170 s | 174 | 184 | miss |
| T10 | groggies / min: parrier σ 1.5; walker | 0.8-1.3; ≤ 0.4 | 1.78; 0 | 1.50; 0 | miss (closer) |
| T11 | U / min: walker; mixed σ 0 | 0.8-1.5; 0.6-1.0 | 3.17; 0.67 | 2.06; 0.67 | walker miss (closer); mixed pass |
| T12 | dodger σ 1 avoids an N hit it times | ≥ 95 % | 91.3 % of 264 | 88.8 % of 269 | unattainable as T6 (86.6 %) |
| T13 | parrier σ 0, every chain in reach, F at h − 1 | 100 %, no refused F | 53 of 53; 0 | same | pass |

By agent, B (%/min intake · groggies / min · U / min): P1 walker 238 · 0 · 2.1; stand 240; parrier σ 0 63 · 2.4 · 0.8;
σ 1.5 102 · 1.6 · 1.2; σ 3 140 · 0.8 · 1.7; mixed σ 0 1.4 · 2.6 · 0.7; dodger σ 1 66; masher = walker. P2 walker 244;
stand 241; parrier σ 0 66; σ 1.5 108 · 1.4; σ 3 133; mixed 4.3; dodger 73. Patterns / min 18-20. Kill runs: cutscenes
50 s apart (CS1 36 + 7 + 7; CS0 is not in the probe), 4 groggies per parrier fight. In the free fight the σ 0 parrier
perfect-parried 99.3 % of the 561 P hits that found it; 24 of its 626 presses were refused (presses for hits that missed
lock F for 12-36 t: the whiff rule).

Reading it:
- **T1 / T2 are not measurable here**: the band divides by 타키's whole-fight walker "by the same tool", but 타키 has no
  suite in the repository and its recorded 124 %/min is hrfair 1.x's walker, which dodged on reaction. The new walker
  never defends, so it takes what the standing agent takes (238 vs 240). T3 (standing, 1.47 ×) is the comparable row.
- **T6 σ 1 / T12** ask ≥ 90 / 95 % of a 3-tick window from a press with a 1-tick normal error: 86.6 % at best.
- Left for HI (knobs of §6.4): T10 (1.5 groggies / min for the σ 1.5 parrier: 19 perfect parries / min on 12 pips) and
  T11's walker want fewer parryable hits per minute or a cheaper gauge: e.g. shift a3 (5 hits) weight to a3s (2),
  `GAUGE['hit']` 1, recovery + 2 more; T9b (184 s vs ≤ 170) needs the groggy to pay more (hp − 5 %, or tiers).

## Requests to other lanes (how your part is picked up)
- **H2 (`seq.py`)**: put `CONTRACT = 2` on a line of its own in the rewritten `seq.py`; until then every sequence runs
  as the core stand-in `core/sq/<name>`. What the core expects from the sequences: `seq/<name>/{start,tick,cancel}`,
  `seq/intro/skip` and `seq/cs1/skip` (the core counts the hold and jumps `#sq` to `SKIP[name]['to'] - 1`);
  `#sq_sig` = `refill` at the beat of `lead5` (60) / `lead_re` (10) (lead60's refill at its tick 0 is the core's
  `shield/arm`; the effect and sound of every refill are the sequence's: `shield/arm` is silent); `hp1`-`hp3` at
  `strike` / `land` / `kick` of the repel (the core applies 15 ‰ each, the kill at `kick` for `{at:5}`); the repel's
  first frames stage the gold deflect (the judge plays nothing any more: no `g_deflect`); the banner (`fx/hud/warn`)
  on at the refill beat of `lead5` / `lead_re` while `#warn hr 1`, the judge turns it off.
  On a pause / reload the core calls `seq/<name>/cancel` and goes to the end state itself (`core/re/cs1`, `core/re/repel`,
  `core/intro/reload`): cancel must release everything the sequence made.
- **H2 / H2c (`scarlet_cine.mjs`)**: nothing to mark; a clip is used when its last key = the contract length, else the
  static placeholder of `scarlet_clips.CINE_PLACEHOLDER` is built (printed; `placeholder: true` in the manifest).
- **H1c (`scarlet_clips.mjs`)**: the 12 placeholders are one marked block at the end (`// STAND-IN (H1)`, `PF(...)`).
  Poses the module relies on: `grog_in` ends in `DOWN`; `q_air` tick 0 follows `q_grab` tick 21 (not 20).
- **H1c (kit)**: `api.KIT_PRESETS` / `OVERLAYS` / `KIT_SPRITES` gain an H-lane name once `build_mboss_hr_fx.py`
  contains `@preset('<name>'` / `api.OVERLAYS['<name>']` / a sprite group `'<name>': [`. The module already calls
  `flash_blue {t:15}` (at blue's tick 0, on her chest, following her), `ult_web {t:22}` (+ ovl `web` 2 / 16 / 2) at
  ult 26, `ult_burst` at 46, `sky_mark` at q_air's lock3, `sky_pillar {r:24}`, `qi_beam {len:160|140}`; until the
  kit has them vanilla particles stand in. One more sound was added: `kcut_go` (riptide_3 0.6 p 1.4). kcut's "big"
  yellow is `yellow_tell {t:10}`: the preset has no size argument (a `s` argument would be a contract change: ask H1).
  `test_kit`'s pins listed above are the kit suite's to update.
- **H3**: `api.actor*()` turn on when `tools/player_motion/cine/manifest.json` exists.

## Decisions / deviations (and why)
- §8.4 "additively": the sequence contract was switched in the interface commit (the waiting lanes need its numbers);
  `seq.py` (11-06) is left untouched and ignored by the marker rule, so no lane gets a merge conflict from H1.
- `build_scarlet_rig.mjs` (no owner in §8.3): the owner mapping (`S2a` / `H1` fight, `S2b` / `H2` cinematic) and the
  placeholder fallback. `build_mboss_core.py` (H2's for FN-cam): FN-bal's two zeroing lines beside `#mbBarOff`'s.
- `api.DISC` stays (the kit generator's `DISC_SCALE` reads it); the module launches no disc.
- The pip is checked every gauntlet tick, not at "s and s + 1" (§1.2): the hazard strikes after the module tick.
- q: the branch at 21, not 20 (the grab's result is known one tick after its strike); the grab disc and the dash
  patterns' locked spot are pulled in to her reach (`reach_clamp`; q: 15.6 b): the design would hit a player at the
  locked spot from any distance.
- No flinch after a perfect parry on a4's second hit (she is in the air until 38) and on nb / q.
- mx: the 12-t retreat holds the pattern clock at 0 (`#mx_pre`), so the hit ticks stay the clip's.
- rings at a full gauge ends 6 t after its last ring and the core starts ult in that tick (`ULT_AFTER`).
- ult's own second cut does not charge the gauge it spent (set to 0 again at 47).
- `test_bal_boss.py`: her row was removed (the design: `test_bal_hr.py` replaces it).
- T6's band "perfect per timed F ≥ 90 % at σ 1" cannot be met by any fight: a 3-tick perfect window around a press with
  a normal error σ 1 t holds 86.6 % (P(|x| < 1.5)); measured 83.8 % (quick). The cleared rate is the usable half.
- T1 / T2 / T3 use the RECORDED 타키 / Guardian numbers of hrfair 1.x (neither boss has a suite in the repository):
  the old walker dodged on reaction, the new one never defends, so the ratios are indicative only.
- The lead's rulings of 11-11 on the player side (A-01 F lock + whiff streak, A-12 dodge cooldown 18 / 12) are modelled
  in `hrsim.H1Sim` (`INPUT_RULES`; `#parGap` / `#parChain` / `#parW1` are read from the loaded pack, the ruled numbers
  without a constant yet are defaults to be read from `load.mcfunction` once the core fix names them).

## Pack files
None added or changed (`diff -rq rp_base rp_hr1` is empty after the rig and kit generators).

## What only a person in the game can check
- The parry cue's readability (the pink glint at her blade 7 t before each cut) and that the three flashes read as
  different colours on her chest; the gauge's under bar filling in tenths (only whole segments show).
- The feel of the groggy (grog_in → down → kip-up) with the placeholder clips replaced by H1c's.
- q: the throw (kb 5) and her aerial part above a player who stays on the ground; the sky mark as a line.
- ult's two whole-arena cuts answered by two perfect dodges 22 t apart (the dodge cooldown is 12 t after a success).
