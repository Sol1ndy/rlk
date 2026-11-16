# HR/review/bal — the balance tools of 홍련 (Scarlet) for S5

Written 11-05 by the S5-prep agent. Nothing is tuned here: S5 tunes with these tools. Scratch tools, never shipped.
`HR` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr`, this folder = `HR/review/bal`.
PLAN = `HR/PLAN.md` (§4.8 targets, §5.1 pips, §4.1-§4.7 patterns, §7.4-§7.6 item / buff / the reward_ev row).

| file | what |
|---|---|
| `hrfair.py` | the PLAN §4.8 fairness probe: one run = one boss (`scarlet` / `tachy` / `guardian`) x mode x agent x seed → one JSON |
| `batch.py` | runs presets or lists of hrfair runs, one process at a time by default, resumable (skips existing JSONs) |
| `analyze.py` | `base`: the 타키 baseline aggregate (`base_tachy.json`); `hr`: the 홍련 §4.8 table, every target next to 타키 measured by the same tool, ratio, PASS / FAIL |
| `reward_ev.py` | PLAN §7.6's row: `HR/plan/calc/ev.py` + `ev_cd40.py` (imported unchanged) fed with hrfair-measured rates; gates G1-G3 PASS / FAIL |
| `run_base.sh` | how `base_tachy.json` / `.log` were made: 0d65e87 snapshot (disk-guarded) → `tk` + `gd` presets → `analyze.py base` → snapshot deleted |
| `run_hr.sh` | the same for 홍련: `bash run_hr.sh [<commit> [<label> [<preset>]]]` (default `wip/hr hr hr`) → batch → `reward_ev.py --dp` → snapshot deleted → `analyze.py hr` (`<label>_summary.log/json`, `<label>_reward_ev.log/json`) |
| `lib/` | vendored, unchanged: `HR/tests/lib/{mcsim,fgsim,azsim,cmsim,hrsim}.py` (S3's harness; ScSim with the dash model) + `S:ap/balance/azfair_core.py` (the sim of record's agent); md5s at the end |
| `base_tachy.json`, `base_tachy.log` | **the 타키 baseline**: 45 runs (0d65e87, `claude/exciting-pascal-ek1vuy`) + 6 Guardian runs |
| `smoke_hr.json`, `smoke_hr.log` | **the 홍련 smoke run** (wip/hr 66dafec, seed 11, 6 runs) — proves the tool end to end; **NOT the final measurement** |
| `smoke_reward_ev.json`, `.log` | reward_ev on the smoke runs — **NOT final** (one 2600-t walker run) |
| `out/base_tachy/`, `out/gd/`, `out/hr_smoke/` | the raw run JSONs; `out/*_runs.log` one summary line per run, `out/*_guard.log` the snapshot / disk events |

## 0. Rules
- Never run in `/home/user/rlk` or a worktree: run on a **snapshot** (git archive of a commit) outside the repo. `run_base.sh` /
  `run_hr.sh` do it: `git -C /home/user/rlk archive <commit> roguelike/data roguelike/tools | tar -x -C <tmp>/snap_<label>`,
  `tools/dev` and the other bosses' function trees (`boss/{apep,azhdaha,arlecchino,raiden}`, `mboss/{fieldgen,butterfly}`)
  removed → 124 MB (0d65e87) / 143 MB (wip/hr). mcsim raises on a missing function, so pruning can only crash a run, never
  change a number. The snapshot is made only while ≥ 950 MB are free; if `df` falls under 800 MB while the batch runs, the
  scripts stop it, delete the snapshot and resume (batch.py skips finished runs) once ≥ 950 MB are free; the snapshot is
  deleted at the end. (Happened once at 05:30: the first baseline attempt was stopped; see `out/base_tachy_runs.raw.log`.)
- One simulation process at a time while other agents share the 4 CPUs (`batch.py --jobs 1`, the default).
- `python3 -I` everywhere; the tools set `sys.dont_write_bytecode` (nothing written into a snapshot or into `HR/plan/calc`).
- hrfair imports the snapshot's `tools/mboss_scarlet/api.py` (the gauntlets' cut table) — our own generator code.

## 1. How to run
```bash
B=HR/review/bal
bash $B/run_hr.sh wip/hr hr hr                 # the full 홍련 set (99 runs, ~25 min) + the §4.8 table + reward_ev
bash $B/run_hr.sh <commit> hr_after hr_phase   # e.g. after a tuning commit: only p1 / p2 / whole
bash $B/run_base.sh                            # re-make the 타키 baseline (only if the tool / levels / agents change)
# by hand, on an existing snapshot <dp> = <snapshot>/roguelike:
python3 -I $B/hrfair.py <dp> scarlet whole:melee:walk:sword:stand 11 --out /tmp/x.json
python3 -I $B/batch.py <dp> <label> <preset | boss=spec[@n],...> [--seeds 11,22,33] [--reps 4] [--plv 15] [--jobs 1] [--force] [--dry]
python3 -I $B/analyze.py hr <label...> --base $B/base_tachy.json [--gd gd] [--out <json>]
python3 -I $B/analyze.py base <label> --gd gd --out $B/base_tachy.json
python3 -I $B/reward_ev.py --runs <label...> [--dp <dp>] [--json <json>]   # --help: every override
```
Presets (`batch.py`): `tk` (타키 baseline, 45 runs), `gd` (Guardian, 6), `hr` (홍련 full, 99), `hr_phase` (p1 / p2 / whole,
33), `hr_g` (gauntlets, 60), `hr_smoke` (6); or `scarlet=p1:melee:walk:sword@1200,tachy=whole:...`.

### hrfair
`hrfair.py <dp> <boss> <spec> <seed> [--n 3600] [--plv 15] [--reps 4] [--out run.json]`, spec = `mode:policy:dodge:char[:g[:skill]]`
- `scarlet`: `p1` (100000 HP, n ticks of P1) · `p2` (100000 HP, test 33 → n ticks of P2) · `whole` (real HP; the intro ended at
  once by `core/intro/done`; until the kill = `#mbSt 2` at CS3's kick, or n = 12000 in the presets) · `a8` / `a13` (100000 HP;
  the gauntlet by test 21 / 27, `--reps` times; before each rep the player is healed, given 2 dash charges and put at its
  home ring 6 / 8 / 10 / 13 b south of C — pat_ghost.py's HOME).
- `tachy`: `p1` · `p2` (test 30) · `p3` (test 31) · `whole` (its 190-t intro played, not counted).
- `guardian`: `p1` = azfair's own mid-boss fight (azsim's plaza world), Lv plv vs L plv, 100000 HP, n ticks (the T3 reference).
- Every run ends at her death (end `dead`; 1.1 — the 1.0 baseline's 타키 p3 ranged runs went on dead, analyze leaves those
  ticks out, so its numbers equal 1.1's).
- env: `HR_LEAD` 12 · `HR_OFF0` -2 · `HR_JIT` 2 · `HR_RJIT` 8 · `HR_REV` 60 · `HR_LVADD` (registry lvAdd) · `HR_HPPCT` 100 (the
  `hp` knob, whole runs) · `HR_DMGMUL` (unset = the registry's 135; a uniform tier what-if as knfair5's `KN_DMGMUL`, e.g.
  108 = -20 %, 162 = +20 %) · `HR_DP_REV` (a label stored in the JSON; the scripts set it).
- JSON: every player damage event `[t, pct, el, lost, pat, phase, nododge, src, shield, srcin, dist, pt]` (src `hit` / `dot` /
  `brand` / `fail60` / `fatal`; srcin 1 hazard, 2 projectile; dist = feet to her body; pt = `#pt`), dodges, every landed
  player hit `[t, dealt, phase, pat, basic|skill]`, the phase timeline, pattern starts, HP samples every 10 t (player, boss),
  deaths, instant deaths, the gauntlets (per cut: lock, strike, dash offset, refused, pip taken, hit, dodged, feet-to-lock
  distance at the strike; per gauntlet: pips at the judge, result, HP lost to cuts / discs / the fail hit), agent stats,
  commands / tick, wall time.

## 2. The world, the agents, the seeds
- **World**: S3's `hrsim.ScSim` (vendored) for both bosses — the REAL special path (rift zone → `mboss/sp/gate` → arena →
  intro → fight), REAL `combat/apply`, `player/take_damage`, the framework hazards, her module and rig; the dash model
  (`dashInvT` 6..1 over the 6 world ticks after a dash, as `player/dash_go` + `player/tick`; `shield/pip` reads it).
  `hrfair.world_probe` = `hrsim.world_sc` + the player's element-tick HP loss recorded as `dot` (azsim.world records it,
  world_sc does not). `ProbeSim` adds (nothing in `lib/` edited): `HR_LEAD`; the hit source, feet-to-body distance and `#pt`
  on every hit / dodge; the A8 fail hit labelled `fail60`; the A13 instant death (`ult/fatal`) recorded as `fatal` (whole
  mode: a Ronova-style revive of `HR_REV` t, then her own revive path → lead-in → A13 again; gauntlet mode: recorded and
  skipped); a normal death = a counter + full HP (azfair's convention).
- **Levels**: item-less Lv15 player (HP 268, def 38, atk 38) vs the boss at Lv15 + lvAdd = **L16** (both lvAdd 1); real HP =
  250 x LV_HP(16) / 100 = **5610** (`mob/level_apply` is stubbed: the harness sets the HP). The Guardian: Lv15 vs L15.
- **Human reading** (`HR_LEAD` 12, as knfair5 / tkfair): a quiet hazard made ≤ 2 t before its hit (every P1 / R1-R3 hazard of
  홍련, every 타키 pattern hazard: they are made 1 t before the hit) gets 12 more tell ticks; only for `#pat hr` 1-13 /
  `#pat tk` 1-11, never the gauntlets (the cut builder makes its cuts ≥ 12 t ahead).
- **Agents** (azfair's, unchanged): `melee:walk:sword` (the melee walker), `stand:none:sword` (standing: never moves, dodges or
  attacks), `ranged:walk:bow`, `melee:dash:sword` (azfair's dash timing), `melee:none:sword`. `skill` (spec field 6): every N
  ticks the next landed hit on her body is a skill hit (`#skillDmg 1`, 200 % ATK) — the only way A6 can fire (azfair never
  casts skills); the hr preset uses 150 t.
- **Gauntlet agents** (spec field 5; PLAN §4.8 / §5.1; S4's pat_ghost agents in a real fight): in each counting cut's window
  [lock, strike + 1] (lock = strike - 7) `stand` stands, `out22 out28 side22 side28 in22 in28` walk outward / sideways /
  inward (from C; the direction fixed at the lock) at 0.22 / 0.28 b/t; all dash at strike + off, off = -2 + U{-2..2} (seeded
  per run), the dash along the movement (stand: toward C = the look). Between windows the moving agents walk back to their
  ring; stand / rand leave the tick to the base agent (stand:none = idle; the walker in whole mode walks and dodges as azfair).
  `rand` = stand-then-dash at strike - 2 + U{-8..8}. `none` = the base agent alone. Dashes use azfair's economy (2 charges,
  20 t each, 5-t cooldown); a press without a charge is "refused" and counts as a miss. Whole mode's default is `stand` (so
  the walker can clear A8 / A13 and the kill time exists). The dash agents ignore the A13 moon discs (not cuts).
- **Seeds** 11 22 33 (knfair5 / tkfair); 3600 t per phase run; `--reps 4` gauntlets per seed per agent.

## 3. Metrics (analyze.py; per group, pooled over the seeds as analyze5.py)
- **%max HP / min** = 100 x Σ HP lost / max HP / (Σ live ticks / 1200); live = all ticks but phase `x` (after her death);
  phase runs: that phase; whole runs: from the fight start incl. the transitions and cutscenes (as 타키's README figure).
  Per phase = that phase's damage / its ticks (≥ 200 t). The A13 instant death counts as a death, not as damage.
- **Worst 40-t window** = the most HP lost (% max) inside any 40 ticks; also without the designed A8 fail hit.
- **Standing** = `stand:none:sword` in p1 / p2 (타키 p1-p3).
- **Gauntlets**: per agent the shield clears (0 pips at the judge, `#gres 1`), the pip rate of correctly timed dashes
  (planned offset in -2 ± 2; refused presses are misses; also shown without them), pips taken / cuts, cut hits, HP lost to
  the 9 counting cuts per gauntlet (% max HP; = "the 9 cuts on a standing agent" for `stand:none:sword:none`), the discs,
  the fail hit, pips left, the feet-to-lock distance at the strike.
- **A6**: starts / min, the most starts in any 400 t (20 s), the shortest gap (skill runs).
- **Kill time** (whole runs ending `dead`): from the fight start; 홍련 "incl. the cutscenes" = + the 640-t intro (32 s; with
  the skip + 126 t), "fighting" = ticks outside intro / CS1 / SQ1 / A8 / CS2 / lead-in / A13 / CS3. 타키: from its fight start
  (its intro excluded, as its README 202-216 s).
- Also deaths, hits taken / min, the player's hits / s and DPS, the damage share by pattern, commands / tick, wall time.

## 4. Targets (PLAN §4.8 / §7.6) and how they are read
| id | PLAN | measured as | verdict |
|---|---|---|---|
| T1 | P1 melee walker 1.0-1.15 x 타키 | 홍련 `p1:melee:walk:sword` / 타키 **whole-fight** `melee:walk:sword` (the README figure PLAN §4.8 quotes); the phase-matched ratio (타키 p1) and a by-agent table are printed too | ratio in [1.0, 1.15] |
| T2 | P2 ≤ 1.25 x 타키 | 홍련 `p2:melee:walk:sword` / 타키 whole-fight walker (vs 타키 p2 / p3 printed) | ≤ 1.25 |
| T3 | standing ≤ 1.8 x the guardian standing | max(홍련 p1, p2 standing) / the Guardian's `stand:none:sword` (gd runs: same agent, Lv15 vs L15); without gd: / (타키 standing x 144 / 216) | ≤ 1.8 |
| T4 | worst 40-t window ≤ 40 % | the melee walker's runs (p1, p2, whole) without the A8 fail hit; every agent printed | ≤ 40 % |
| T5 | all 9 gauntlet cuts on a standing agent ≤ 45 % max HP | `a8` (T5) / `a13` (T5b) `stand:none:sword:none`, the HP lost to the counting cuts in one gauntlet, max | ≤ 45 % |
| T6 | the four dash agents: ≥ 90 % of correctly timed dashes score, clear the shield in ≥ 90 % | per agent (stand, out22/28, side22/28, in22/28), A8 + A13 pooled (per gauntlet printed) | ≥ 90 % each |
| T7 | a random dasher (± 8 t) clears in ≤ 50 % | `rand`, A8 + A13 | ≤ 50 % |
| T8 | A6 at most once per 20 s | skill runs (p1, p2): ≤ 1 start in any 400 t and ≤ 3 / min | both |
| T9 | item-less sword kill 230-270 s incl. the cutscenes (≈ 150-185 s fighting) | `whole:melee:walk:sword:stand` + the 640-t intro; vs 타키's kill (both from the fight start) printed | in [230, 270] s |
| G1 | item ★★★ within ±10 % of 불씨의 맹약 | reward_ev: DPS multipliers, median counter rate | |ratio - 1| ≤ 0.10 |
| G2 | ★★★ ≤ 키리온 at the 90th-percentile counter rate | p90 over 30-s windows of the runs (≥ 5 windows, else the fastest run) | ≤ |
| G3 | B1 within ±5 % of the item at ★★ net | net = gross x (1 - slot 4 %) x (1 - exposure 2 %) (`--slot`, `--exposure`); prints the `#hrMoonAtk` that equalises | |ratio - 1| ≤ 0.05 |
reward_ev measures from the runs (melee walk / dash sword, p1 / p2 / whole): basic hits / s → K = hits x 1.10 / 0.55
ATK-multiples / s (ev.py's own split); 「육참골단」 stacks and 「검신합일」 counters replayed per star on the runs' hit and
hit / dodge events (12-b range, the per-star cooldown); the share of time at HP ≤ 60 % / ≤ 50 % with the item's own HP cost.
Arguments (not measurable by a boss probe): the burst interval (`--burst-every`, default the slash cooldown), slash targets
(`--aoe 1`, rooms `--aoe-room 2` at the counter cap). `--dp` reads the knobs from the tree; `--k 4.4` reproduces ev.py.

## 5. The knobs
| knob (PLAN) | where | how to try it |
|---|---|---|
| tiers ±20 % (§4.8) | `api.DMG` T1-T4 29 / 42 / 56 / 71 → the generated hazard `dmg` args | uniform: `HR_DMGMUL` (×135); per tier: regenerate |
| `hp` ±15 % (§4.8) | registry `scarlet.hp` 250 | `HR_HPPCT` 85-115 (whole runs) |
| `DOWN_T` 160-260 (§4.8) | `api.DOWN_T` 200 | regenerate |
| `CUT_R` 2.8-3.6 (§4.8) | `api.CUT_R` 3.2 **and** `api.PIP_R` (= CUT_R + 3.0, computed at import) | regenerate |
| recoveries ±4 t (§4.8) | `api.RECOVER` {1: (16, 24), 2: (12, 18)} | regenerate |
| `#hwStkAtk` `#hwSlCoef` `#hwCtrCdT` `#hwFloor` (§7.4.7) | `F:items/tune/b10` (6 / 849 / 40 / 50) | `reward_ev.py --dp <tree>` reads them; edit the copy |
| `#hrMoonAtk` (§7.5.4) | `F:load` (20) | `reward_ev.py --moon-atk N` (G3 prints the value that equalises) |
"Regenerate" = on a snapshot copy, never the worktree: `hrsim.dry_build('<copy>/roguelike', patch='api.CUT_R = 3.6\napi.PIP_R = 6.6')`
(`lib/hrsim.py`: regenerates only `F:boss/scarlet/**` inside that tree with the api patched), then `batch.py` on it; or tune
in S5's own worktree, commit, and `run_hr.sh <commit>`.

## 6. Run times here (4 CPUs shared with the integration agent; one process)
| run | wall |
|---|---|
| 타키 3600-t phase run | 31-37 s (≈ 105 t/s; ≈ 520 commands / tick) |
| 타키 whole fight (melee ≈ 4300 t, ranged ≈ 2500 t) | ≈ 40 s / ≈ 25 s |
| 홍련 3600-t phase run | 24-34 s (≈ 410 commands / tick) |
| 홍련 whole fight to the kill (≈ 4000 t incl. both gauntlets) | ≈ 27 s |
| 홍련 gauntlet run, 4 reps (a8 / a13) | ≈ 5 / 7.5 s |
| Guardian 3600 t | ≈ 11 s |
| **`tk` preset (45 runs)** | **1530 s of runs ≈ 26 min** (measured) |
| `gd` preset (6 runs) | 68 s (measured) |
| `hr_smoke` via `run_hr.sh` | 50 s incl. the snapshot (measured) |
| **`hr` preset (99 runs)** | **≈ 25 min** (estimate from the timings above), + ≈ 1 min snapshot / analysis |

## 7. Results (11-05)
### 7.1 타키 baseline — `base_tachy.log` (0d65e87 snapshot, hrfair 1.0 = 1.1 for these runs, Lv15 vs L16, seeds 11 22 33)
| agent | P1 | P2 | P3 | whole fight | worst 40 t | kill (from the fight start) | deaths / fight |
|---|---|---|---|---|---|---|---|
| melee walker | 137.2 | 140.8 | 109.0 | **124.0 %/min** (per phase p1 132 · m1 121 · p2 150 · m2 142 · p3 104) | 33.2 % | **214 s** (207-218) | 4.0 |
| standing | 195.9 | 204.1 | **222.8** | — | 32.1 % | — | — |
| ranged walk (bow) | 62.9 | 75.6 | 53.0 | 68.2 | 25.0 % | 124 s | 0.7 |
| melee dasher | 24.3 | 0.0 | 0.0 | 22.5 | 25.0 % | 208 s | 0.0 |
**Guardian** (same agent, Lv15 vs L15): standing **164.0**, melee walker 123.1 %/min (the azfair reference: 159.6 / 119.8 at
Lv4 vs L4). 타키's README (tkfair, Lv5 vs L6): whole 134, standing 216 (210-251 per phase), worst 40 t 35 %, kill 202-216 s —
the same tool here gives 124 / 196-223 / 33 % / 207-218 s; 타키 standing / Guardian standing = 1.36 (its target ≤ 1.8).

### 7.2 홍련 smoke — `smoke_hr.log` — NOT the final measurement
wip/hr **66dafec** (before S1K's kit / arena merge: stub arena, no kit), seed 11 only, short runs, hrfair 1.1:
- `whole:melee:walk:sword:stand`, 2600 t: P1 1186 t → **CS1 213 → SQ1 60 → A8 206** (stand-then-dash: 9/9 pips, shield
  cleared) → CS2 104 → down 220 → P2 611 t (limit). 46.0 %/min over the run (P1 42, P2 114 per phase), worst 40 t 14.2 %,
  no death; damage by pattern A9 43 % · A3 32 % · R3 20 % · A2 6 %.
- A8 gauntlets (2 reps each): `stand` 18/18 pips, 2/2 clears; `out28` 18/18, 2/2 (feet ≤ 4.68 b from the lock point);
  `rand` 5/18 pips (3 refused presses), 0/2 clears; `none` (standing) 0/18 pips, **the 9 cuts = 135 HP = 50.4 % max HP per
  gauntlet** (15 HP per T2 cut), then the fail hit (49.3 %, clamped by `#mbDotLethal 0` to leave 1 HP).
- `p1:stand:none:sword`, 600 t: 134.3 %/min.
- On the smoke the table gives T3 PASS (0.82 x the Guardian), T4 PASS (14.2 %), **T5 FAIL (50.4 %)**, T6 PASS (stand, out28:
  100 % / 100 %), T7 PASS (0 %); T1 / T2 / T5b / T8 / T9 n/a (no such runs in the smoke).
- `smoke_reward_ev.log` (one 2600-t walker run): 1.64 basic hits/s → K 3.28, stacks 4.4, counters 0.14/s (cap 0.50/s), HP ≤
  60 % 78 % of the time with the item's cost; mid profile ★/★★/★★★ +37.4 / +48.6 / +61.0 % (net ★★ +39.8 %), 불씨의 맹약
  +60.7 %, 키리온 +77.7 %, B1 +25.5 %: G1 PASS (x1.00), G2 PASS, **G3 FAIL** (x0.90; B1 needs `#hrMoonAtk` 34 to equal the
  item ★★ net); late: G1 / G2 PASS, G3 FAIL (x0.95; `#hrMoonAtk` 27).
- Development runs on the same snapshot (same tool, not kept as JSON — indications only): a whole fight seed 22 killed her
  at **201 s from the fight start = 233 s incl. the intro** (fighting 150 s; A8 and A13 cleared 9/9; 2 deaths, the walker is
  hit by the three A13 discs); `p2:melee:walk:sword` seed 22 **100.9 %/min** (R3 / R1 cuts and A9 dominate); `p1:melee:dash`
  0.0; `p2:ranged:walk:bow` 131.8; A13 standing: cuts 50.4 % + discs 16.8 % + the instant death; a skill run (150 t) gave 2
  A6 starts in 1600 t (479 t apart); the A13 fail → revive → A13 path and the A8 fail hit were exercised at 10 % HP.

### 7.3 What the smoke already suggests (S5 must confirm with the full `hr` set after the kit / arena merge)
- **P1 is far below the T1 band**: the walker's P1 ≈ 42-48 %/min vs 타키 124 (≈ 0.35-0.4 x, target 1.0-1.15) — far more than
  the §4.8 knobs (tiers ±20 %, recoveries ±4 t) can move; P2 ≈ 101 (≈ 0.8 x, T2 ≤ 1.25 passes). Why (from the runs): she hits
  the walker ~7 times / min in P1 (smoke: 7 hits in 1186 t) vs 타키's ~22; the walker escapes most P1 sectors with the 12-t pose reading, while the P2
  cut-builder hazards (R1 / R3) follow it until the lock and only a dash escapes them.
- **T5 fails at the D0 tiers**: 9 x 15 HP = 50.4 % > 45 %; a T2 of ≈ 37 % (−12 %, inside the ±20 % knob) or a lower cut tier
  would pass.
- The dash agents score 100 % in the smoke (all directions, 0.22 / 0.28 b/t); the random dasher clears 0/2.
- Kill time ≈ 233 s incl. the intro (one run) sits inside 230-270 s.

## 8. Assumptions S5 should check (where PLAN and the precedents differ)
1. **"x 타키" base** of T1 / T2 = 타키's whole-fight melee-walker %/min (the README figure PLAN §4.8 quotes); the 아를레키노
   precedent compared phase to phase — analyze prints both; switch the verdict if S5 prefers phase-matched.
2. **The Guardian standing** (T3) is measured by azfair in its own plaza world at Lv15 vs L15 (`gd`), not by hrsim.
3. **Levels**: Lv15 vs L16 (player level + lvAdd) for both bosses; knfair5 used Lv15 vs L18 (a chapter-4 boss). Ratios are
   robust to this, absolute kill times are not (`HR_LVADD`, `--plv`).
4. **Kill time incl. the cutscenes** adds the full 32-s intro to the fight-start-to-kill time (the PLAN's 83 s of invulnerable
   time includes it); the run itself ends the intro at once. The kill = `#mbSt 2` at CS3's kick (CS4 is after the kill).
5. **Gauntlet agents** act from the lock only (the cut follows the player until then) and walk home between windows; they
   ignore the A13 discs; refused presses count as misses; the gauntlet runs heal and refill the charges before each rep
   (pat_ghost style), the whole runs do not.
6. **A6** cannot fire without skill hits (azfair has none): T8 uses the skill runs (a 200 % skill hit every 150 t).
7. **The A13 instant death** in whole runs: unlimited Ronova-style revives (her own revive path), each counted as a death.
8. **reward_ev**: K comes from the measured basic hits (ev.py's 1.10 / 0.55 split); ev.py's rough refs (키리온 2.2 x 0.60 / K,
   불씨의 맹약 0.25 / K) grow as K drops, so G2 gets easier at boss-fight hit rates — `--k 4.4` reproduces ev.py; the probe's HP
   never heals, so the HP shares (and the item's cost) are a pessimistic boss-fight case; bursts are not modelled by the
   agent (`--burst-every`).
9. **Phase `x`** (after her death in a phase run) is left out of every rate; hrfair 1.1 stops such runs at the death.

## 7.4 S5 results (11-06) — `hr_s5a` (3741fc4), `hr_s5b` (ed2e175), **`hr_s5` (005f00a, the S5 head: the final
measurement)**, the dense rooms `rooms_s5` / `rooms_s5h`, what-ifs `w_*` (HR/s5/progress.md lists them)
- 3741fc4: T1 99.9 %max/min = 0.81 × 타키 (FAIL), T2 1.06 ×, T3 1.44 ×, T4 19.8 %, T5 / T5b 40.3 %, T6 100 %, T7 29 %, T8 1,
  T9 Lv5 / 10 / 15 229.6 (FAIL) / 234.9 / 240.8 s; reward_ev G1 PASS, G2 FAIL, G3 FAIL.
- 005f00a: T1 130.6 = **1.05 ×**, T2 138.0 = 1.11 ×, T3 244.0 = 1.49 × the Guardian, T4 20.5 %, T5 / T5b 40.3 %, T6 100 %,
  T7 29 %, T8 1 (gaps ≥ 457 t), T9 **240.7 / 242.8 / 245.4 s**; ranged whole 92.6 (completes); G1 ×0.972 / ×0.964, G2 all
  eight readings ≤ 키리온 (tightest: late, rooms' K, cap, 2 targets 57.5 vs 58.8), G3 ×0.976 / ×1.032 — all PASS.

## 9. S5 changes (11-06) — the probe fixes of the review (HR-36, HR-37, HR-39 tool part, HR-40, HR-21)
- **HR-36**: `lib/hrsim.py` re-vendored from wip/hr 3741fc4 (63638ed7, I1b's block tags); `run_hr.sh` refuses a commit whose
  own copy differs (checked before the pruning; `HR_LIB_ANY=1` skips it), `hrfair.py` does the same when its tree has the
  file; every JSON records `lib_hrsim`. The other four `lib/` files equal the commit's.
- **HR-37**: `HrAgent.position()` (hrfair 1.2) skips the ranged walker's positioning step when the horizontal distance to
  its reference point is < 1e-3 b (A8.9 puts her straight above the player; `azfair_core.py` stays unchanged); the three
  `whole:ranged:walk:bow` runs complete. `batch.py` writes `out/<label>/ERR_<run>.txt` for a failed run (removed by a later
  good run) and exits 1; `run_hr.sh` logs it and exits with that code; `analyze.py` prints a WARNING line per ERR file
  before and after the table (and `meta.errors` in the JSON).
- **HR-39 (tool part)**: hrfair 1.2 records the body's `rlk_mb_inv` on every event (dmg `[12]`, dodges `[8]`, the field
  `inv`); `reward_ev.counter_events` counts only src `hit` (no `dot`: element ticks never pass `player/take_damage`) and
  drops every event at an invulnerable body (the game's `hw_ctr` selects `tag=!rlk_mb_inv`: no counter, no cooldown spent;
  F3's rule, `HR/f/f3_requests.md` r3); the log prints how many events it left out.
- **HR-40**: the `hr` / `hr_phase` presets add `whole:melee:walk:sword:stand` at `--plv 5` and `--plv 10` (files `*_lv5` /
  `*_lv10`); groups are keyed by the player level; `analyze.py` prints one T9 row per level and a T9 row over the levels
  (every level's mean in 230-270 s; the headline = the lowest level). `hr` also gains `p2:melee:walk:sword:none:60` (a
  dense skill cadence, D5-06: T8 by design). `hr` = 108 runs, `hr_phase` = 39.
- **HR-21 — the dense rooms** (`room/roomfair.py`, `room/run_rooms.sh <roguelike> <label>`): the chapter-2 / 3 swarm
  harness (`S:ch2/tests_a/c2sim.py` + `S:ch3/tests_a/c3sim.py`, imported unchanged) runs the REAL `cm/world`, `cm/tick`,
  every custom mob's brain and attacks, `cm/pj/world` (projectiles), the room plans (`cm/c2/plan`, `cm/c3/plan`; chapter 1
  = `cm/summon_c1`'s weights, a cannoneer without a flat site re-rolls as there), `mob/level_apply`, the REAL
  `combat/apply` for the player's hits; brains walk toward the player (c2sim), elites are dummy brains (walk, never
  attack); riding is not modelled (`execute on passengers` selects nothing: the shield bearer's bar). A room = #mobN 8 at
  map 5 of chapters 1-3 (L5 / L11 / L17), the mobs on a 7-11-b ring; the player = the probe's sword walker without
  dodging (reach 3.5, swings 6 / 10 t at 100 / 120 %, atk 10 + 2 x (L - 1), stops 2.5 b from the nearest mob) - a
  standing-in-melee player, the most hits a room gives. JSON: every hit that reached the player (`cm/hit_pl`) with the
  nearest live mob's distance, 5-t samples of the mobs within 12 / 20 b, kills. `reward_ev.py --rooms <label>` replays the
  counter on them, pools their 30-s windows with the boss runs' (rooms and boss fights weigh half each) for the p90, and
  judges **G2 in four readings**: at that p90 and at the cooldown's cap (20 / #hwCtrCdT per s), each with the slash on 1
  and on 2 targets (all must be <= 키리온); it prints the measured slash target count. `--set name=value,...` = knob
  what-ifs (e.g. `hwCtrCdT=80,hwSlCoef=700,hrMoonAtk=28`). `run_hr.sh` passes `HR_ROOMS=<label>` to reward_ev.
- Collision (checked for T1): in the default F5 view the player's body is the avatar mannequin (`view/spawn`), and it
  carries the camera seat as a passenger (`view/ride_tick`: `ride @e[tag=rlk_vseat] mount @e[tag=rlk_av]`), so vanilla's
  `Entity.push` never moves it (a vehicle is not pushed); her husk (`mboss/body`: NoAI, scale 1 = a 0.6-b box, team
  `rlk_cam` vs the avatar's `rlk_stun`, both collision `always`) is no solid collider either. In first person (the real
  player is the body) the client pushes the player softly out of her box (~0.035-0.05 b/t per tick against walking).
  So the walker's overlap of her box is what the default view allows: the walker is unchanged.

## md5 (11-05)
`hrfair.py`, `batch.py`, `analyze.py`, `reward_ev.py`: see `md5sum *.py` (the README is not updated per edit).
`lib/`: `mcsim.py` 7ac6cf81…, `fgsim.py` fa9456c9…, `azsim.py` e9ccb446…, `cmsim.py` 7de1dd2c…, `azfair_core.py` 8804cc7f…
(= S:ap/balance/azfair_core.py = R:tools/dev/sim/ap/balance/azfair_core.py), **`hrsim.py` 63638ed7…** (S5, 11-06, HR-36:
re-vendored from wip/hr 3741fc4's `R:tools/dev/sim/hr/tests/lib/hrsim.py` = I1b's block tags: dry grass / crimson roots pass
`#rlk:dash_pass`; the 05:02 copy was 44af1b59…). The four others equal 3741fc4's `R:tools/dev/sim/hr/tests/lib/` copies.
`run_hr.sh` refuses a commit whose `tools/dev/sim/hr/tests/lib/hrsim.py` differs from `lib/hrsim.py` (checked before the
pruning; `HR_LIB_ANY=1` skips it), and `hrfair.py` does the same when the tree it runs on still has that file; every run
JSON records `lib_hrsim`. base_tachy.json stays valid: 타키's world has no plant cells (D5-04 verified the 05:02 baseline
with this hrsim: identical). If the tree's hrsim changes again, re-vendor it here (and re-run the baseline if 타키's world
changes).
