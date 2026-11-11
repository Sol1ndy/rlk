# lane HB (홍련 rebuild: the balance pass) — progress

Branch `wip/combat-hb` (from `origin/wip/combat-hi` d7da75e79), worktree `<S>/cb/wt_hb`, `<S>` = the scratchpad of
`h_common.md`. Brief: hi_todo 7 — re-run `hrfair2.py`, restate the unattainable targets of hr_design §6.4, tune with the
design's knobs in its order (numbers in `tools/mboss_scarlet/api.py` and her registry `hp` only) until every attainable
target passes on all three seeds, regenerate, gates. Reviews H-A / H-B run on d7da75e79 at the same time and fix lane HF-A
follows (it re-times the gauntlet cuts, stops the forced rings → ult at a floor, clears the counter / A6 queue around the
groggy, starts the forced rings only in the near band, takes q's grab knockback): the final balance run is after that merge.

## Steps
- [x] **1. the tool** (this commit): hrsim's F lock was a Python model with its own numbers (review H-A: the whiff window 40
      not 80 t, the long lock one press late and capped at 36 not 48 t, a refused press pushing the lock a full #parGap, any
      parry clearing the streak); the dodge cooldown numbers were defaults that only happened to equal the pack's. Now
      `hrsim.world_h1` runs the REAL `player/f_key` (press / press_re / par_use) and the REAL `dashCool` score (+ the judge's
      `dg_refund`, player/tick's − 1). `tests/test_input_hr.py` (new, 17 checks) compares the world with the README 3 rules
      written out as a reference model on 15 press / dodge sequences (whiffs 20 / 70 / 90 t apart, a held key, mashing every
      2 / 3 / 13 t, irregular, a3 parried at h − 1 / h − 7 / mixed / after a whiff, dodges with and without a perfect
      dodge). The H1 suites on the new world: pat_ghost 65, test_gauge 22, test_bal_hr 49, test_scarlet 47, pat_p1 531,
      pat_p2 67 — all pass (test_flow: see gates).
      `hrfair2.py`: 타키 and the Guardian measured by the same tool (`base` runs), every target per seed, the kill runs on all
      three seeds, the metronome agents of T7m (the lead's item 2: F every p t, p 8..30, every phase), T6 σ 1 / T12 against the
      inputs whose own error fell in the window, `--agents`, per-pattern stats (`pstat`: HP lost, P / N hits per pattern).
- [x] **2. restated targets**: hr_design §6.4, the note "Restated by HB, 11-11" (below).
- [ ] 3. tuning
- [ ] 4. regenerate, gates

## Restated targets (hr_design §6.4 note) and why
| # | was | now | why |
|---|---|---|---|
| T1 / T2 | ÷ 타키's 124.0 %/min (hrfair 1.x, recorded) | ÷ **232.3 %/min**: 타키's whole fight against hrfair2's walker on this tree (seeds 230.3 / 228.6 / 238.0) | 1.x's walker dodged on reaction; the new one never defends, so 124.0 cannot be reproduced. 타키's module runs in hrsim (its rift, intro and whole fight), so "the same tool" is possible again. Bands kept |
| T3 | ÷ the Guardian standing 164.0 (recorded) | ÷ **165.1** (re-measured: 168.4 / 159.0 / 167.9) | same tool; reproduces the old number |
| T6 σ 1 / T12 | ≥ 90 / 95 % of timed inputs | **≥ 95 % of the timed inputs whose own error fell inside the 3-t window**; raw rate shown next to the 86.6 % ceiling | P(|e| ≤ 1) at σ 1 = 86.6 % is the window's own limit, and with ~50-90 inputs per seed the raw rate swings ± 4 % by chance (seed 33's T12: 5 of 29 errors outside the window, 13.4 % expected). Diagnosed: every in-window dodge avoided, every out-of-window one failed — the fight takes nothing away |
| T7m | — | a metronome F (p 8..30, every phase) clears neither gauntlet | the lead, review H-A. Gauntlet timing is HF-A's: not tuned here |
| all | pooled | **per seed** (11 / 22 / 33) and pooled | the brief |

## Baseline (d7da75e79 + the tool fix; `review/bal/hb_base.log`)
Item-less Lv15 vs her L16, 3 600 t per phase run; seeds 11 / 22 / 33 / pooled. **Bold** = misses.

| # | band | s11 | s22 | s33 | pooled |
|---|---|---|---|---|---|
| T1 P1 walker ÷ 타키 232.3 | 1.00-1.15 | 238.1 = 1.02 | 236.9 = 1.02 | 238.8 = 1.03 | 237.9 = 1.02 |
| T1b P1 parrier σ3 ÷ walker | ≤ 0.60 | 0.54 | 0.59 | **0.61** | 0.58 |
| T1c P1 mixed σ0 %/min | ≤ 5 | 0.0 | 0.0 | 1.1 | 0.4 |
| T2 P2 walker ÷ 타키 | ≤ 1.25 | 1.06 | 1.07 | 1.03 | 1.05 |
| T3 standing ÷ Guardian 165.1 | ≤ 1.8 | 1.47 | 1.46 | 1.48 | 1.46 |
| T4 worst 40 t | ≤ 40 % | 20.5 | 20.5 | 20.5 | 20.5 |
| T5 / T5b cuts on a standing agent | ≤ 45 / 55 % | 40.3 / 49.3 | same | same | same |
| T6 σ0: perfect per timed F / in window; cleared | ≥ 95; ≥ 95 % | 100 / 100; 8 / 8 | same | same | 100 / 100; 24 / 24 |
| T6 σ1: perfect per timed F (of 86.6) / in window; cleared | — / ≥ 95; ≥ 90 % | 83.8 / 98.5; 8 / 8 | 86.2 / 98.6; 8 / 8 | 91.2 / 100; 8 / 8 | 87.1 / 99.1; 24 / 24 |
| T7 sloppy; masher; dodger clears | ≤ 35; 0; 0 % | 0; 0; 0 | 0; 0; 0 | 0; 0; 0 | 0; 0; 0 |
| T7m metronome clears G1; G2 | 0; 0 | **2 / 437 (p 15, 16); 6 / 437 (p 12, 14, 15, 28)** (no seed) | | | |
| T8 A6 in any 400 t | ≤ 1 | 1 | 1 | 1 | 1 |
| T9 walker kill, fighting s, Lv5 / 10 / 15 | 150-185 | 181 / **187 / 187** | 178 / **189 / 189** | 177 / **186** / 184 | 179 / 187 / 187 |
| T9b parrier σ1.5 kill, fighting s | 125-170 | **180** | **181** | **186** | 182 |
| T10 groggies / min: parrier σ1.5; walker | 0.8-1.3; ≤ 0.4 | **1.50**; 0 | **1.50**; 0 | **1.67**; 0 | 1.56; 0 |
| T11 U / min: walker; mixed σ0 | 0.8-1.5; 0.6-1.0 | **2.00**; 0.67 | **2.00**; 0.67 | **2.17**; 0.67 | 2.06; 0.67 |
| T12 dodger σ1: avoided per timed N hit (of 86.6) / in window | — / ≥ 95 % | 81.4 / 100 | 88.5 / 100 | 77.2 / 100 | 82.1 / 100 |
| T13 parrier σ0, every chain: perfect; refused F | 100 %; 0 | 53 / 53; 0 | | | |

The fix of the input rules moved little: H1's column B (its model) had T10 1.50, T11 2.06, T9 182 / 191 / 184, T9b 184; the σ0
parrier's refused presses 24 / 626 then, 20 / 629 now. Per pattern (P1, `pstat`): the walker takes 39 % of its intake from
rings (4.0 / min, 2.1 of them forced by the full gauge) + ult; the σ1.5 parrier's 20.6 perfect parries / min come from rings
7.3, d4 4.7, a3 3.4, a3s 1.9.

## Tuning log
(see below; every variant = this tree with an api patch, her module regenerated in a scratch copy; p1 + p2 runs of the
walker, standing, parrier σ1.5 / σ3, mixed σ0 unless said)

## How to run
```bash
S=<scratchpad>; WT=$S/cb/wt_hb/roguelike
SIM=$S/cb/hb_sim; rm -rf $SIM; cp -a $WT/tools/dev/sim $SIM; (cd $SIM && grep -rl --exclude='*.md' --exclude='*.json' \
  2f5e7b47-ba2f-58bc-b880-1598991e2f8e . | xargs sed -i "s|$S|$SIM|g")
cd $SIM/hr/review/bal && python3 -I hrfair2.py $WT --out <dir> --jobs 4 [--only p1,p2,g,kill,chain,base,metro] [--agents walker:0,parrier:1.5] [--base <a hrfair2.json with base runs>]
# full set incl. the 874 metronome runs: ~45 min on 3 shared cores; without metro ~15 min
cd $SIM/hr/tests && python3 test_input_hr.py $WT
```
