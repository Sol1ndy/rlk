# lane HB (홍련 rebuild: the balance pass) — progress

Branch `wip/combat-hb` (from `origin/wip/combat-hi` d7da75e79), worktree `<S>/cb/wt_hb`, `<S>` = the scratchpad of
`h_common.md`. Brief: hi_todo 7 — re-run `hrfair2.py`, restate the unattainable targets of hr_design §6.4, tune with the
design's knobs in its order (numbers in `tools/mboss_scarlet/api.py` and her registry `hp` only) until every attainable
target passes on all three seeds, regenerate, gates. Reviews H-A / H-B run on d7da75e79 at the same time and fix lane HF-A
follows (it re-times the gauntlet cuts, stops the forced rings → ult at a floor, clears the counter / A6 queue around the
groggy, starts the forced rings only in the near band, takes q's grab knockback): the final balance run is after that merge.

## Steps
- [x] **1. the tool** (2843e218a): hrsim's F lock was a Python model with its own numbers (review H-A: the whiff window 40
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
- [x] **2. restated targets** (2843e218a): hr_design §6.4, the note "Restated by HB, 11-11" (below).
- [x] merged fix lane HF-A (`origin/wip/combat-hfa` a5ce6faf9, the lead's message: tune on what ships) — 1e53d40df
- [x] **1b. the agents** (this commit): hrfair2's agents planned every hit of a pattern at its start and pressed even when the
      pattern was cancelled first (a groggy, A6's back-blink, a flinch): 22 of the mixed σ0 agent's 101 presses at seed 33 were
      for hits that never came, the whiff streak then refused real presses (its T1c 6.5 %/min). An input whose cue never showed
      is now withdrawn (`Agent.withdraw`); the free-fight σ0 parrier's refused presses went 17 → 0 (T13f).
- [x] **3. tuning** (this commit): the numbers below; the final measurement passes every target on seeds 11 / 22 / 33.
- [x] **4. regenerate, gates** (f4b88a44d): below ("Final" — superseded by step 6).
- [x] **5. the lead's re-tune (11-11, after f4b88a44d)**: the P2 shift to the flashed attacks (88 % of P2's near weight) cannot
      ship (the user: 「패링 불가 공격: 보스의 일부 큰 공격만」). New binding rules: in every band of both phases (and the far
      rule) the unparriable entries take ≤ 35 % of the pick weight (mx / q count half), parried chains the majority; T10
      relaxed to 0.8-1.6 (hr_design §6.4 "Relaxed by the lead, 11-11"). Kept: the tool and agent fixes, `GAUGE['hit']` 1, the
      tiers, the P1 cooldowns, `hp` 225 (T9 / T9b re-checked). Merged `origin/wip/combat-hfb` (HF-B, 0651d1123) first: 05945c3b2.
- [x] **6. final** (this commit): the section "Re-tune under the 35 % rule" below; the full gate set on that tree.

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
Every variant = the tree with an api patch appended, her module regenerated in a scratch copy (`<S>/cb/hb_var/<v>`), then
hrfair2's phase runs (walker, standing, parrier σ1.5 / σ3, mixed σ0; seeds 11 / 22 / 33). `v*` ran on d7da75e79 + the tool
fix, `m*` on the tree merged with fix lane HF-A (the lead's message: the final balance is the one that ships). A run is
deterministic per configuration and seed; any change of the AI's numbers reshuffles the sequences. Per seed: T1b, the P1 /
P2 groggies of the σ1.5 parrier (counts per 3-min run; T10 per seed = their sum / 6, so the band 0.8-1.3 holds 5-7), U / min.

| v | change (cumulative where said) | T1 | T1b s11/22/33 | groggies P1 · P2 per seed | U walker | note |
|---|---|---|---|---|---|---|
| base | — | 1.02 | 0.54/0.59/0.61 | 4.5/4.5/5 · 4.5/4.5/5 (1.50/1.50/1.67) | 2.06 | |
| v1 | `GAUGE['hit']` 1, rings P1/P2 near 10, d4 15/12, a3 20/15 | 0.97 | 0.59/0.64/0.62 | 5/4/4 · 4/4/5 | 1.39 | T11 fixed; T1 / T1b broken |
| v2 | hit 1, rings 5/5, **T1 29 → 31** | 1.10 | 0.52/0.58/0.59 | 5/4/4 · 5/5/6 | 1.39 | raw 4 → 5 restores T1 |
| v4 / v5 | v2 + P chain cooldowns × 1.7 (+ `PP_FLINCH` 10) | 1.06 | 0.58/0.64/0.64 | 5/3/4 · 5/5/5 | 1.33 | cooldowns do not slow her (a3s fills in); `PP_FLINCH` 10 drops the mixed agent's U to 0.50 |
| v6 | v2 + P1 / P2 near weight to the unparriable singles | 1.06 | 0.63/0.66/0.64 | 4/4/3 · 4/4/4 | 1.33 | T10 down, T1b over |
| v7 / v8 | a3 → a3s; a3 up, d4 / rings down | 1.04-1.09 | 0.50-0.65 | 3-5 · 4-5 | | moving weight between parried chains changes nothing |
| v12-v16 | v2 + **P2 near band to the flashed attacks** (a3 5, a3s 10, d4 4, rings 0; a9 35, blue 30, kcut 35, mx 35) | 1.08-1.10 | 0.52/0.58/0.58 | 5/4/4 · 2/2/2 | 1.33 | P2 carries T10 |
| m18 | v16 on the merged tree (P2 cooldowns dropped: no effect) | 1.08 | 0.54/**0.64**/0.58 | 5/4/5 · 2/2/2 | 1.33 | T1b seed 22 |
| m20 / m21 | a3 P1 15 (a3s 45) | 1.03-1.04 | 0.59-0.71 | 4-5 · | | a3 is the walker's heaviest parried chain: worse |
| m22 | P1 unparriable weights a9 15, a10 / kcut 12, **T3 54, T4 61** | 1.06 | 0.45/0.52/0.58 | 6/5/5 · | | T1b fixed, P1 groggies up |
| m23 / m24 | m18 + T3 54 / T4 61 (m24: a9 20, a10 / kcut 16) | 1.02-1.04 | 0.53/0.63/0.57 · 0.52/0.60/0.57 | 5/4/5 · 4/4/6 | 1.33-1.44 | |
| m28 | m24 + A1 / A2 P1 cooldown 200 | 1.04 | 0.52/0.56/0.55 | 4/4/6 · | 1.44 | |
| m29-m34 | a3s cd 100, d4 20, rings 0, kcut 20, m23 / m18 + A1 / A2 200 | | 0.52-0.63 | 4-5/4/5-6 | | |
| m35 / m36 | m28 + T2 50 (+ P1 near cooldowns × 1.4) | 1.12-1.19 | 0.51-0.57 | 4-5/4/5-6 | | T1 over at seed 22 |
| **m40** | m28 + P1 near cooldowns × 1.4 (a3 / d4 200, a3s 110, rings 220, a9 220, a10 170, blue 250, kcut 280) | 1.01/1.06/1.02 | 0.53/0.55/0.57 | 5/4/5 · 2/2/2 | 1.33-1.5 | **chosen** |
| m40 kill | hp 260 / **225** | | | | | T9 175-197 s / 158-175 s; T9b 183-186 / 162-166 s |

What decided it:
- **T11** (the walker's ultimates): `GAUGE['hit']` 2 → 1 is enough (2.06 → 1.33-1.5 / min); the mixed agent keeps 0.67.
- **T1 / T1b**: fewer ultimates cost the walker ~25 %/min (rings + ult are 35 % of max HP); T1 29 → 31 (raw 4 → 5) gives it
  back on the parried chains and lowers T1b. T1b ≈ 0.44 + 0.44 × (the unparriable share of the walker's intake): the σ3
  parrier keeps 44 % of the parried damage and ~90 % of the unparriable; every P1 shift toward the flashed singles pushed it
  over 0.60, so the unparriable tiers go to their floor inside ± 20 % (T3 → raw 8, T4 → raw 9) and P1's unparriable weights
  down a little.
- **T10**: the σ1.5 parrier's perfect parries track the parried hits per minute (~31-35 in P1 whatever the mix of chains),
  cooldowns do not slow her (another candidate is always ready; recovery is already at the knob's +4 limit), so P1 stays at
  ~4.5 groggies per 3 min and **P2 carries the reduction** (2 per 3 min): P2's near band now leans on the flashed attacks.
  Together 6-7 per seed = 1.0-1.17 / min.
- **T9 / T9b**: the groggy's pay-off is the boss tier's (`build_balance.py` TIERS, no per-boss value), so the parrier only
  gains ~4 s on the walker; `hp` 260 → 225 (− 13.5 %) brings the parrier under 170 s and keeps the walker at 158-175 s.
- Not used: recovery (H1 already at + 4), `PP_FLINCH` (it lowers the mixed agent's ultimates under T11's 0.6), G2's cut
  count (off-limits, HF-A).

## Final of f4b88a44d (superseded by the re-tune below; kept for the record) — (the merged tree + the HB numbers; `review/bal/hb_final.log`) — before / after per seed
"Before" = the merged tree (HF-A) with the numbers as they came (H1's column B), measured with the fixed tool (hrsim's real F,
the withdrawn inputs). Gauntlet rows (T5-T7m) do not depend on the HB numbers (TC, the scripts, the gauge size unchanged).

| # | band | before s11 / s22 / s33 | **after s11 / s22 / s33** | after pooled |
|---|---|---|---|---|
| T1 P1 walker ÷ 타키 232.3 | 1.00-1.15 | 1.02 / 1.02 / 1.01 | 1.01 / 1.06 / 1.02 | 1.03 |
| T1b P1 σ3 ÷ walker | ≤ 0.60 | 0.52 / **0.64** / 0.58 | 0.51 / 0.55 / 0.59 | 0.55 |
| T1c P1 mixed σ0 %/min | ≤ 5 | 0 / 0 / 0 | 0 / 0 / 0 | 0 |
| T2 P2 walker ÷ 타키 | ≤ 1.25 | 1.06 / 1.07 / 1.03 | 0.91 / 0.97 / 0.95 | 0.95 |
| T3 standing ÷ Guardian 165.1 | ≤ 1.8 | 1.47 / 1.46 / 1.48 | 1.49 / 1.55 / 1.53 | 1.53 |
| T4 worst 40 t | ≤ 40 % | 20.5 | 19.0 | 19.0 |
| T5 / T5b | ≤ 45 / 55 % | 40.3 / 49.3 | 40.3 / 49.3 | |
| T6 σ0 in window; cleared | ≥ 95; ≥ 95 % | 100; 8 / 8 each | 100; 8 / 8 each | 24 / 24 |
| T6 σ1 raw (of 86.6) / in window; cleared | ≥ 95; ≥ 90 % | 82.5 / 97.1, 87.5 / 100, 91.2 / 100; 8 / 8 each | same | 87.1 / 99.1; 24 / 24 |
| T7 sloppy; masher; dodger | ≤ 35; 0; 0 % | 0; 0; 0 | 0; 0; 0 | |
| T7m metronome clears (most segments) | 0 | G1 0 / 437 (3), G2 0 / 437 (4) | same (HF-A's timing) | |
| T8 A6 in 400 t | ≤ 1 | 1 | 1 | |
| T9 walker kill s, Lv5 / 10 / 15 | 150-185 | 178 / **187** / **187**, 178 / **189** / **186**, 173 / **189** / **186** | 169 / 168 / 173, 158 / 170 / 166, 162 / 175 / 175 | 163 / 171 / 171 |
| T9b σ1.5 kill s | 125-170 | **182 / 182 / 183** | 162 / 165 / 166 | 165 |
| T10 groggies / min σ1.5; walker | 0.8-1.3; ≤ 0.4 | **1.67 / 1.67 / 1.67**; 0 | 1.17 / 1.00 / 1.17; 0 | 1.11 |
| T11 U / min walker; mixed σ0 | 0.8-1.5; 0.6-1.0 | **2.00**; 0.67 / **2.00; 0.50** / **2.00; 0.50** | 1.33; 0.67 / 1.33; 0.67 / 1.50; 0.83 | 1.39; 0.72 |
| T12 avoided per timed N (of 86.6) / in window | ≥ 95 % | 81.4 / 100, 88.5 / 100, 78.9 / 100 | 88.3 / 100, 90.0 / 100, 74.0 / 100 | 83.9 / 100 |
| T13 chains; refused | 100 %; 0 | 53 / 53; 0 | 53 / 53; 0 | |
| T13f free fight σ0: perfect; refused | (report) | 100 % of 550; 0 | 100 % of 426; 0 | |

Groggies of the σ1.5 parrier per 3-min run, P1 · P2: before 5 / 5 / 5 · 5 / 5 / 5, after 5 / 4 / 5 · 2 / 2 / 2.

**Robustness** (the same tree on seeds 44 / 55 / 66, phase runs only): T1 1.02 / 1.03 / 1.02, T1b 0.50 / 0.60 / **0.62**, T10 **1.33** /
1.00 / 1.17, T11 1.33 / 0.67 each, T2 0.95-0.97, T3 1.46-1.49, T4 19.0 — pooled all in band, but one seed of three misses T1b
(by 0.015) and one misses T10 (by one groggy). Per seed, T1b and T10 sit at the noise floor of a 3-minute run: T1b moves by
± 0.06 with the σ3 agent's timing draws and the ultimates' count (each one is 15.6 % of max HP), T10 is a count (5-7
groggies in 6 minutes pass, 8 does not). The pooled values (0.55-0.57, 1.11-1.17) are the stable reading.

### Every number changed (old → new) and why
| knob (§6.4 order) | change | why |
|---|---|---|
| weights | P1 near: `rings` 20 → 5, `a9` 25 → 20, `a10` 20 → 16, `kcut` 20 → 16 | T10 (the free rings are 4 parried hits; the gauge still forces them before every U); T1b (less unparriable share) |
| weights | P2 near: `a3` 25 → 5, `a3s` 30 → 10, `d4` 20 → 4, `rings` 20 → 0; `a9` 15 → 35, `blue` 15 → 30, `kcut` 20 → 35, `mx` 20 → 35 | T10: P2 carries the groggy reduction (P1 is pinned by T1 / T1b); P2 has no T1b, T2 has no floor |
| cooldowns (P1) | `a1` / `a2` 100 → 200, `a3` / `d4` 140 → 200, `a3s` 80 → 110, `rings` 160 → 220, `a9` 160 → 220, `a10` 120 → 170, `blue` 180 → 250, `kcut` 200 → 280 | the counter's parried singles (T10, T1b: m24 → m28); the near band × ~1.4 settled P1 at 5 / 4 / 5 groggies with T1b ≤ 0.60 on every seed (m28 → m40; it does not slow her: patterns / min unchanged) |
| recovery | — | already at the knob's + 4 (H1) |
| `GAUGE` | `hit` 2 → 1 | T11 (2.06 → 1.39 U / min for the walker; the mixed agent's 0.67 stays) |
| tiers | T1 29 → 31 (raw 4 → 5), T3 62 → 54 (raw 10 → 8), T4 71 → 61 (raw 11 → 9); T2 / TC unchanged | T1 back over 1.00 after fewer ultimates; T1b: raise the parried, lower the unparriable. Each is the smallest coefficient of its raw step (`12 × coef × 135 / 10000` floored) |
| `hp` | registry 260 → 225 (− 13.5 %) | T9 / T9b: the parrier's kill 182 → 165 s, the walker 158-175 s |
| G2 cut count, `PP_FLINCH` | — | G2: off-limits (HF-A); `PP_FLINCH` 10 dropped the mixed agent's U under 0.6 (v9) |
| groggy pay-off | — | the boss tier's (`build_balance.py` TIERS), no per-boss value |

### Gates (the final tree)
| gate | result |
|---|---|
| `regen_all.sh --mobs` twice | the first run changed only `boss/scarlet/**` (45 files) and `mboss/register` (her hp); the second changed nothing; `check_mboss_pack` 0 problems |
| rig / kit / pack | untouched (no number they read changed) |
| loadcheck `hb` (26.3) | 0 function load failures, `Starting minecraft server version 26.3`, `Done` |
| hr suites | test_input_hr 17, test_gauge 33, test_bal_hr 79, pat_ghost 65, test_scarlet 47, test_metro 30, pat_p1 559, pat_p2 70, test_flow 40, test_special_hr all, ident_hr all, test_reward all — every one passes. No pin was changed: the suites read `api` (tiers, `GAUGE`, weights); `hrsim.setup_h1`'s default 5834 HP is a test-world HP, not the registry's |

### Only a person playing can judge
- P2 now leans on the flashed attacks (yellow / blue / purple: about half of her P2 near attacks), and the parried chains are
  rarer there: whether P2 still feels like a parry fight, or like a dodge test.
- The groggy rate: an average parrier breaks her ~1.5 × / min in P1 and ~0.7 × / min in P2 (4 breaks in a kill); whether the
  break comes often enough to feel earned, and the 100-t window with × 1.30 (shared by every boss) pays enough.
- How often the ultimate comes: ~1.3-1.5 / min for a player who is hit a lot, ~0.7 / min for a clean one (it is armed by her
  pattern ends more than by hits now).
- The kill: 158-175 s of fighting (+ ~50 s of cutscenes after CS0) for an item-less player; ~165 s for an average parrier.
- The heavier chain hits (T1 raw 5) and the lighter flashed hits (T3 raw 8, kcut raw 9).

## Re-tune under the 35 % rule (the release candidate; `review/bal/hb_final.log`)
Variants (phase runs, merged tree HF-A + HF-B, hp 225), per seed 11 / 22 / 33:

| v | weights (near band; mid / far / far rule as the final in all) | T1 | T1b | groggies P1 · P2 / 3 min | T10 | U walker P1 · P2 |
|---|---|---|---|---|---|---|
| W1 | chains kept: P1 a3 30 a3s 30 d4 25 rings 5 · a9 16 a10 14 blue 12 kcut 15; P2 a3 20 a3s 40 d4 15 rings 5 mx 20 · a9 12 blue 12 kcut 14 | 1.06 / 1.02 / 1.04 | 0.53-0.54 | 5/4/6 · 5/5/5 | 1.67 / 1.50 / **1.83** | 1.33 · 1.33-1.67 |
| W2 | light parried chain: P1 a3 20 a3s 45 d4 15 rings 5; P2 a3 12 a3s 50 d4 10 rings 5 | 1.05 / 1.09 / 1.03 | 0.51-0.56 | 4/4/5 · 4/4/5 | 1.33 / 1.33 / **1.67** | **2.00** (s33) |
| W3 | W2 without the free rings (rings 0; d4 12 / 8) | 1.01 / **0.99 / 0.99** | 0.50-0.60 | 4/4/4 · 4/4/4 | 1.33 each | 1.33 |
| **W4** | W3 + a3s cooldown P1 110 → 140, P2 70 → 100 | 1.01 / 1.03 / 1.01 | 0.50 / 0.52 / 0.58 | 4/4/4 · 4/4/4 | 1.33 each | 1.33-1.67 · 1.33 |

The free rings (4-5 parried hits each, ~0.8 / min) were the cheapest groggy lever; the gauge still forces them before every ult,
so rings stays in the fight (≈ 1.0-1.5 / min). The a3s cooldown keeps the walker's ultimates in T11 (short patterns charge
the gauge faster). The 35 % rule moved the mid / far bands and the far rule too (they were 46-72 % unparriable in the design's
start values): the far band and the far rule now close the gap mostly with a4's leap (P1) and nb (P2).

### Final weights per band (`api.WEIGHTS`, `FAR_RULE`) and the unparriable share
| phase · band | parried (weight) | unparriable (weight; mx / q half) | share |
|---|---|---|---|
| P1 near | a1 8, a2 8, a3 20, a3s 45, d4 12, rings 0 = 93 | a9 14, a10 12, blue 11, kcut 13 = 50 | 35.0 % |
| P1 mid | a3 10, a3s 15, tri 30, a4 20 = 75 | a9 6, a10 12, hcut 8, blue 7, kcut 7 = 40 | 34.8 % |
| P1 far | a4 50 | a10 12, hcut 14 = 26 | 34.2 % |
| P1 far rule | a4 65 | hcut 20, a10 15 | 35.0 % |
| P2 near | a3 12, a3s 50, d4 8, rings 0, mx ½ 10 = 80 | a9 11, blue 11, kcut 11, mx ½ 10 = 43 | 35.0 % |
| P2 mid | a3 10, a3s 15, tri 20, a4 15, nb 20, q ½ 8, mx ½ 7.5 = 95.5 | a9 6, a10 9, hcut 7, blue 7, kcut 6, q ½ 8, mx ½ 7.5 = 50.5 | 34.6 % |
| P2 far | a4 20, nb 35, q ½ 10, mx ½ 5 = 70 | a10 10, hcut 12, q ½ 10, mx ½ 5 = 37 | 34.6 % |
| P2 far rule | nb 50, q ½ 15 | hcut 15, q ½ 15 | 31.6 % |

Realised picks (the σ1.5 parrier, per min): P1 a3s 3.6, a3 2.3, a9 1.8, a10 1.6, kcut 1.6, rings 1.6 (forced), blue 1.4, d4 1.2,
a1 1.1, a2 1.0, ult 1.0; P2 a3s 4.9, mx 2.3, blue 2.1, a9 1.7, kcut 1.6, a3 1.3, d4 1.1, rings 1.1 (forced), ult 1.0. Hits that
found it: P1 269 parried-type vs 77 unparriable, P2 253 vs 89 (in 9 min each).

### Final table (seeds 11 / 22 / 33; pooled)
| # | band | s11 | s22 | s33 | pooled |
|---|---|---|---|---|---|
| T1 | 1.00-1.15 | 1.01 | 1.03 | 1.01 | 1.02 |
| T1b | ≤ 0.60 | 0.50 | 0.52 | 0.58 | 0.54 |
| T1c | ≤ 5 | 0 | 0 | 0 | 0 |
| T2 | ≤ 1.25 | 1.06 | 0.99 | 1.03 | 1.02 |
| T3 | ≤ 1.8 | 1.47 | 1.50 | 1.51 | 1.49 |
| T4 | ≤ 40 % | 19.0 | 19.0 | 19.0 | 19.0 |
| T5 / T5b | ≤ 45 / 55 % | 40.3 / 49.3 | = | = | = |
| T6 σ0; σ1 in window (raw); cleared | ≥ 95; ≥ 95; ≥ 95 / 90 % | 100; 97.1 (82.5); 8 / 8 | 100; 100 (87.5); 8 / 8 | 100; 100 (91.2); 8 / 8 | 100; 99.1 (87.1); 24 / 24 |
| T7 | ≤ 35; 0; 0 | 0; 0; 0 | = | = | = |
| T7m metronome (most segments) | 0 | G1 0 / 437 (3), G2 0 / 437 (4) | | | |
| T8 | ≤ 1 | 1 | 1 | 1 | 1 |
| T9 Lv5 / 10 / 15 | 150-185 s | 161 / 168 / 168 | 156 / 171 / 171 | 167 / 165 / 165 | 161 / 168 / 168 |
| T9b | 125-170 s | 162 | 162 | 162 | 162 |
| T10 σ1.5; walker | 0.8-1.6; ≤ 0.4 | 1.33; 0 | 1.33; 0 | 1.33; 0 | 1.33; 0 |
| T11 walker; mixed | 0.8-1.5; 0.6-1.0 | 1.50; 0.67 | 1.33; 0.67 | 1.50; 0.67 | 1.44; 0.67 |
| T12 in window (raw) | ≥ 95 % | 100 (94.2) | 100 (96.4) | 100 (74.6) | 100 (88.0) |
| T13 | 100 %; 0 | 53 / 53; 0 | | | |
| W35 unparriable share, every band | ≤ 35 % | max 35.0 | | | |

**Robustness** (the same tree, seeds 44 / 55 / 66, phase runs): T1 1.02 / 1.02 / 1.00, T1b 0.47 / 0.55 / **0.61**, T1c 0, T2 1.00-1.09,
T3 1.43-1.45, T4 19.0, T10 1.50 / **1.67** / 1.50 (groggies 4 + 5, 5 + 5, 5 + 4), T11 1.33; 0.67. Pooled in band; one seed of three
misses T1b by 0.009 and one T10 by one groggy: per seed, both sit at the noise floor of a 3-minute run (the pooled reading is
the stable one).

### Every number changed against d7da75e79 (old → new) and why
| knob (§6.4 order) | change | why |
|---|---|---|
| weights | the table above (every band; the far rule P1 hcut 45 / a4 30 / a10 25 → 20 / 65 / 15, P2 nb 40 / q 30 / hcut 30 → 50 / 30 / 15) | the lead's 35 % rule; inside it the parried weight leans on a3s, the free rings are gone (T10) |
| cooldowns (P1) | a1 / a2 100 → 200, a3 / d4 140 → 200, rings 160 → 220, a9 160 → 220, a10 120 → 170, blue 180 → 250, kcut 200 → 280; a3s P1 80 → 140, P2 70 → 100 | the counter's parried singles and the near band (T10 / T1b, from the first pass); a3s: T11 |
| recovery | — | already at the knob's + 4 (H1) |
| `GAUGE` | `hit` 2 → 1 | T11 |
| tiers | T1 29 → 31 (raw 4 → 5), T3 62 → 54 (raw 10 → 8), T4 71 → 61 (raw 11 → 9) | T1 after fewer ultimates; T1b |
| `hp` | 260 → 225 (− 13.5 %) | T9 / T9b (re-checked on this mix: 156-171 s, 162 s) |
| `NP_SHARE` / `NP_SHARE_MAX` (new data in `api.py`) + an import-time assert | — | the lead's rule, checked at every build (`api.py` refuses to load if a band goes over) |
| not used | G2's cut count (HF-A's), `PP_FLINCH` (drops the mixed agent's U under 0.6), the groggy pay-off (the boss tier's) | |

### Gates (the release candidate)
| gate | result |
|---|---|
| rig → kit → player rig + actor (+ audio) → `regen_all.sh --mobs` (README 0-4), on `<S>/rp_hb` (a copy of `rp_hi`) | round 1 changed only her AI files (`ai/pick/*`, `ai/far_p*`, `core/start/a3s`); rounds 2 and 3 changed nothing in the tree, pack hash 44f657ac… both; the pack differs from `rp_hi` only by HF-A's `cue_0` sprite and the items atlas |
| `check_mboss_pack` | 0 problems |
| loadcheck `hb2` (26.3) | 0 function load failures, `Starting minecraft server version 26.3`, `Done` |
| rplint / atlas_px (`rp_hb`) | 0 problems / 12.940 M (≤ 13.2 M) |
| hr suites | test_input_hr 17, test_gauge 33, test_bal_hr 79, pat_ghost 65, test_scarlet 47, test_metro 30, pat_p1 559, pat_p2 70, test_flow 40, test_special_hr all, ident_hr all, test_reward all, test_moon 55, test_hwamu 283, test_arena_hr 94, test_clips_h1c 297, ev_dry 82, test_cam all, test_cine 159, test_contact 94, test_seq all, test_kit 16 081, test_rig 162, test_actor 167, gen_check_hr 28 / 28 (the generators re-run on a copy: no diff) — every one passes |
| combat suites | test_cb 296, test_rm all, test_np 125, test_bal 117, test_bal_boss 117 |

### Only a person playing can judge
- Whether both phases now read as parry fights: about 3 of 4 of her picks are parried patterns; the flashed attacks (yellow /
  blue / purple) are ~1 in 4, rings only comes before the ultimate.
- The groggy: an average parrier breaks her ~1.3 × / min (4 times in 3 minutes of either phase, 2-3 in a kill); whether it
  feels earned and the shared 100-t × 1.30 window pays enough.
- The ultimate: ~1.3-1.5 / min for a player who is hit a lot, ~0.7 / min for a clean one.
- The kill: 156-171 s of fighting (+ ~50 s of mid-fight cutscenes) for an item-less player, ~162 s for an average parrier.
- From far she now closes mostly with a4's leap (P1) and nb (P2), less with the yellow dash cuts; the chain hits are heavier
  (T1 raw 5), the flashed hits lighter (T3 raw 8, kcut raw 9).

## How to run
```bash
S=<scratchpad>; WT=$S/cb/wt_hb/roguelike
SIM=$S/cb/hb_sim; rm -rf $SIM; cp -a $WT/tools/dev/sim $SIM; (cd $SIM && grep -rl --exclude='*.md' --exclude='*.json' \
  2f5e7b47-ba2f-58bc-b880-1598991e2f8e . | xargs sed -i "s|$S|$SIM|g")
cd $SIM/hr/review/bal && python3 -I hrfair2.py $WT --out <dir> --jobs 4 [--only p1,p2,g,kill,chain,base,metro] [--agents walker:0,parrier:1.5] [--base <a hrfair2.json with base runs>]
# full set incl. the 874 metronome runs: ~45 min on 3 shared cores; without metro ~15 min
cd $SIM/hr/tests && python3 test_input_hr.py $WT
```
