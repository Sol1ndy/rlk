# fix lane HFA (홍련 rebuild: review H-A, the fight) — progress

Branch `wip/combat-hfa` (from `origin/wip/combat-hi` d7da75e79), worktree `<S>/cb/wt_hfa`, pack copy `<S>/rp_hfa` (from
`<S>/rp_hi`), `<S>` = the scratchpad of `h_common.md`. Brief: fix HA-01 … HA-09, HA-11 and `test_flow.py:171` of HA-10 as
ruled in `review/rulings_HA.md` (on `origin/wip/combat`). Not this lane: hrsim's F-lock model and hrfair T7 (lane HB, at the
same time on `wip/combat-hb`: this lane's `api.py` changes are the gauntlet scripts, the q kb row, the cue sound / sprite
rows only), the cutscenes / lock / actor (review H-B).

## Steps
- [x] probes rebuilt from the findings' repro (scratch `<S>/hfa_work/probe/`): HA-01 (P1 ult 50-107 then CS1 123, P2 ult
      60-117 then lead5 135), HA-02 (A2 / A6 at 0 t after the groggy on 3 of 6 seeds), HA-03 (the real F functions: G1
      14/15/16-t beats 5 PP, G2 14-t 10 PP, mashers 3 / 6 t 5 PP in G2), HA-09 / HA-05 / HA-07 as described
- [x] HA-01, HA-02, HA-04, HA-05 (`core.py`), HA-09 (`ai.py`, `s3lib.FP_EXTRA`), HA-08 (`api.HITS['q']`), HA-06 / HA-07
      (`api.KIT_SOUND_RECIPES`, `api.KIT_SPRITES_HR['cue']`, `build_mboss_hr_fx.py` + `mboss_hr_fx_paint.paint_cue`)
- [x] G1 re-timed (HA-03)
- [ ] G2 re-timed (HA-03) — see "HA-03" below
- [ ] full gates on the final tree, the old-tree fail check of the new tests, scratch cleanup

## What changed (per finding)
| id | change | proof (new check; fails on d7da75e79) |
|---|---|---|
| HA-01 | `core/pat_end`: the forced rings → ult chain `unless #fl` (as mx's repeat) | `test_gauge`: P1 (test 80) / P2 (test 34), rings forced by test 12, the floor hit at rings pt 3 → no ult, CS1 / lead5 next |
| HA-02 | `on_hit` returns while `grgT` runs; `core/trig0` (#ctr #flq #a6q #hits = 0) at `bal_on` and `bal_off` | `test_bal_hr` HA-02: 4 seeds × (basic hits every 8 t in the last 60 t / one skill hit at grgT 30) → nothing queued, the first pattern 11 t after the groggy = the no-hit run |
| HA-04 | reload hook → `core/grog_re`: `down` at once (> 20 left), else `kipup` with `hrRigT` = 20 − grgT | `test_bal_hr` HA-04: reload at grgT 95 / 60 / 12 → down / down / kipup at the next tick, the kip-up's clip and tick = the run without reload |
| HA-05 | `bal_ok` refuses a4 28-38 (`ring` → `land`) too; `core.BAL_REFUSE` holds a list per pattern | `test_bal_hr` HA-05: every P1 / P2 pattern, every tick her body is above the floor → `bal_ok` fails (a4 26 t, a10 19, mx 11, nb 43, q 72); a break at a4 pt 31 waits and starts after the landing |
| HA-06 | `parry_cue` = `block.note_block.iron_xylophone` 0.7 p 1.8 (used nowhere else in the pack) | `test_kit`: the cue's sound family is none of the flashes' (amethyst / bell / beacon), recipe pinned |
| HA-07 | own sprite `cue_0` (64 × 64, white core, warm gold rim, four rays to the card edge + four short diagonals, painted in colour), the cue = cue_0 1.5 → 1.9 b + cue_0 0.6 → 1.0 b at 45° + a small pink glint 0.3 → 0.6 b, 7 t | `test_kit`: rays reach 0.9+ of the card (glint_0 0.4), ≥ 1.0 b visible from the first tick, white-gold, no ring; render `render_hr.py cue_p1 cue_p2 cue_far flashes`: 1.4 × 1.4 b on screen at 6 b and 10 b on both fields (was 0.7 × 0.8 b, a pink dot) |
| HA-08 | `HITS['q']` grab kb 0 (`KB_THROW` gone) | `pat_lib`: "knockback only on the last hit of the chain" for every pattern (q's grab was kb 5 at 20 of 4 hits) |
| HA-09 | full gauge: near band → `core/ult_go`; mid band → `ai/ult_close` (glide 0.3 b/t to 4 b, ≤ 40 t; `#ai_uc`), then the rings; a close that ran out of time starts them anyway (no chase) | `test_gauge`: 3 / 6 / 8 / 10.5 b → the rings start ≤ 4.5 b, all 4 rings land; a player walking away 0.32 b/t → rings after the 40-t close |
| HA-10 | `test_flow.py`: the P1 check counts every judged P hit (no `parT` filter) | — (nothing was hidden; the check can now see it) |
| HA-11 | README 0-9 (573) and §3's table (920): the rebuilt kit's unparriable set from `api.HITS` (8 / 17) | — |
| HA-03 | G1 / G2 strikes re-timed; `tests/test_metro.py` (real F functions, every period 8-30 and every start) | see below |

## HA-03
`tests/test_metro.py` (new): `world` (the judged strikes of a standing player = the script), `train` (the real
`player/f_key` / `press` / `press_re` / `par_use` / `judge` in a bare H1 world: every period 2-40, every start from T − 120 to
the last cut; ≤ 3 PP for 8-30, < 5 for 2-7 and 31-40; the cue-reader still clears), `real` (the best train of each period
played in the real gauntlet with F through `player/f_key`: segments taken = the train's PP). Search tools (scratch, C):
`<S>/hfa_work/{fm.c,dfs.c,ils3.py}`: a C model of the shipped rules, an exhaustive DFS, a local search.
- **G1** (9 cuts): 30 46 64 94 110 138 164 180 196 → **30 48 64 91 109 139 163 180 196** (c2 +2: A8.2 39; c4 −3: D2 77,
  A8.4 88; c5 −1: A8.5 103; c6 +1: D1 125, A8.1 136; c7 −1: D3 147, A8.6 160). The DFS found 33 311 strike sets with ≤ 3
  for every period 8-30 and start (s1 28-34, gaps 14-30, last ≤ 199); this one is the nearest to the old (8 ticks moved).
- **G2**: in progress.

## Pack files (`<S>/rp_hfa` vs `<S>/rp_hi`)
- added: `assets/rlk/textures/mboss/hr_kit/cue_0.png`, `assets/rlk/models/item/mboss/hr_kit/cue_0.json`, `assets/rlk/items/mboss/hr_kit/cue_0.json`
  (the kit generator; check the list with `diff -rq` at the end)

## Next
- G2's strikes; then the docs (README G2 line, hr_design §2.4), the full gates, the old-tree fail check.
