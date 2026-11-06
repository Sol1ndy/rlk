# Apep balance harness (plan 9.7 / 12.4; AP-FIX RV-03; scratch, never shipped)

| file | what it is |
|---|---|
| `azfair_core.py` | a vendored, unchanged copy of `S:az/harness/azfair.py` (the sim of record's agent; md5 `8804cc7fd2764e703f4e9badc1c02516`). Its `import azsim` resolves to the AP harness's vendored `ap/tests/lib/azsim.py` (apfair imports `apsim` first), so the agent drives the same engine functions as every Apep suite |
| `apfair.py` | `ApAgent` (azfair's Agent + the Apep parts: phase names, organisms as phase-2 targets with the plan priorities / nearest-not-immune / idle, melee cleave, the 둥지 walls as collision, the Q2 dome modes, the FRONT-mid / BACK positional policies) and `run()` per mode: `whole`, `p1`, `p3`, `p2`, `q2`, `gd` (the Guardian calibration through azfair.fight) |
| `batch.py` | presets `gd apbase apdash appos apttk aprev apaft smoke` (see its docstring) over seeds in parallel; one JSON per run in `out/<label>/` (every player damage event, dodges, dealt, deaths, failures, the Heart curve, Q2 casts, agent stats) |
| `analyze.py` | the plan 9.7 table from labels: `python3 analyze.py <label ...> [--gd gd] [--out analysis.txt]` |
| `breakdown.py` | HP lost per pattern per (mode, policy, dodge, char) group: `python3 breakdown.py <label>` |
| `analysis.txt` | the 9.7 table of the committed tree (AP-FIX) |

The player: item-less Lv15 (HP 268, def 38, atk 38) vs L18; characters = azfair's CHARS (= the plan model `p2sim_rev`'s). The
Guardian reference (label `gd`: Lv4 item-less vs L4, stand none / melee walk / ranged walk bow0, seeds 11 22 33 x 3600 t)
reproduces `S:az/harness/guardian_m0.txt` section 1 seed by seed (472 / 481 / 513, 417 / 366 / 450, 658 / 630 / 666 HP):
159.6 / 119.8 / 100.7 % max HP per minute.

Reproduce (AP-FIX, 2026-10-22): `python3 batch.py <dp> gd gd`, `... apbase,appos b1` (P1 / P3 forced at 100000 HP; the REV change
of the pass does not touch these runs), `... aprev fin`, `... apttk,apdash fin2`, `... apaft aft`, then
`python3 analyze.py b1 fin fin2 aft --out analysis.txt`. About 3 jobs x 40 min on 4 CPUs.

Earlier labels: `base0` (the tree before the balance pass, the I2 coefficients), `b1` (the committed coefficients), `rev0` (P2 / Q2
before the REV change), `aft` (the Q2 runs, copied from rev0: Q2 does not depend on api.DMG / api.REV).

Fix 10-22f (2026-10-22; P4 swing / Q2 field and domes): `python3 batch.py <dp> apaft aft1022`, `... ap1022 b1022` (apbase +
apdash + appos on the fixed tree), then `python3 analyze.py b1022 aft1022 fin ttk_prev --out analysis.txt` (`fin` = P2,
untouched by the fix; `ttk_prev` = symlinks to fin2's whole-fight runs, NOT re-run: the previous tree). apfair's late agent
now moves at #apPT 74 (dome 1 + 40 t on the B0 clock); analyze.py: the Q2 dome gate <= 3 ticks (the two pre-dome ticks +
1) with HP lost per cast, and the one-cast row excludes every pattern-32 hit above 10 % max HP as the blast (the old
>= 50 % test let a capped lethal blast through: 56.7 % on the old tree, 45.1 % on both trees with the fix). Previous
table: analysis.txt.pre_1022. New FAIL: P3 stand 186.5 %/min = 1.17x (was 1.03x): the stand agent never enters a dome and
now eats the whole field (15-20 ticks x 2 % per cast).
