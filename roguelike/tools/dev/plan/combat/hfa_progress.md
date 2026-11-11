# fix lane HFA (홍련 rebuild: review H-A, the fight) — progress

Branch `wip/combat-hfa` (from `origin/wip/combat-hi` d7da75e79), worktree `<S>/cb/wt_hfa`, pack copy `<S>/rp_hfa` (from
`<S>/rp_hi`), `<S>` = the scratchpad of `h_common.md`. Brief: fix HA-01 … HA-09, HA-11 and `test_flow.py:171` of HA-10 as
ruled in `review/rulings_HA.md` (on `origin/wip/combat`). Not this lane: hrsim's F-lock model and hrfair T7 (lane HB, at the
same time on `wip/combat-hb`: this lane's `api.py` changes are the gauntlet scripts / `EXTRA_VANISH` / `BOLTS`, the q kb
row (`KB_THROW` removed), the cue's sound recipe and `KIT_SPRITES_HR['cue']`, nothing of the balancing numbers), the
cutscenes / lock / actor (review H-B).

## Steps
- [x] probes rebuilt from the findings' repro (scratch, deleted at the end): HA-01 (P1 ult 50-107 then CS1 123, P2 ult
      60-117 then lead5 135), HA-02 (A2 / A6 at 0 t after the groggy on 3 of 6 seeds), HA-03 (real F functions: G1 14/15/16-t
      beats 5 PP, G2 14-t 10 PP, mashers 3 / 6 t 5 PP in G2), HA-05, HA-07 (render: 0.7 × 0.8 b pink dot)
- [x] HA-01, HA-02, HA-04, HA-05 (`core.py`), HA-09 (`ai.py`, `s3lib.FP_EXTRA`), HA-08 (`api.HITS['q']`), HA-06 / HA-07
      (`api.KIT_SOUND_RECIPES`, `api.KIT_SPRITES_HR['cue']`, `build_mboss_hr_fx.py` + `mboss_hr_fx_paint.paint_cue`), HA-10
      (`test_flow.py`), HA-11 (README) — 7f34eb3c7
- [x] G1 / G2 re-timed (HA-03), bolts, docs — 0ca7c0c2b
- [x] the full gates on the final tree; the new checks run on the old tree (d7da75e79) fail; scratch cleaned

## What changed (per finding)
| id | change | proof (new check; it fails on d7da75e79) |
|---|---|---|
| HA-01 | `core/pat_end`: the forced rings → ult chain `unless #fl` (as mx's repeat) | `test_gauge`: P1 (test 80) / P2 (test 34), rings forced by test 12, the floor hit at rings pt 3 → the rings end, no ult, CS1 / lead5 next (old: ult 50-108 first) |
| HA-02 | `on_hit` returns while `grgT` runs; `core/trig0` (#ctr #flq #a6q #hits = 0) at `bal_on` and `bal_off` | `test_bal_hr` HA-02: 4 seeds × (basic hits every 8 t in the last 60 t / one skill hit at grgT 30) → nothing queued at the end, the first pattern 11 t after the groggy = the no-hit run (old: A2 / A6 at 0 t) |
| HA-04 | reload hook → `core/grog_re`: `down` at once (> 20 left), else `kipup` with `hrRigT` = 20 − grgT | `test_bal_hr` HA-04: reload at grgT 95 / 60 / 12 → down / down / kipup at the next tick, the kip-up's clip and tick = the run without reload (old: idle). A pause / resume keeps the rig's clip (the rig is not respawned; probed) |
| HA-05 | `bal_ok` refuses a4 28-38 (`ring` → `land`) too; `core.BAL_REFUSE` = a list of spans per pattern | `test_bal_hr` HA-05: every P1 / P2 pattern, every tick her body (the rig's root) is above the floor → `bal_ok` fails (a4 26 t, a10 19, mx 11, nb 43, q 72 airborne ticks); a break at a4 pt 31 waits and starts after the landing (old: 6 ticks of a4 accepted, the break dropped her 1 b) |
| HA-06 | `parry_cue` = `block.note_block.iron_xylophone` 0.7 p 1.8 (used nowhere else in the pack) | `test_kit`: the cue's sound family is none of the flashes' (amethyst / bell / beacon), the recipe pinned |
| HA-07 | own sprite `cue_0` (64 × 64, a white core with a warm gold rim, four rays to the card's edge + four short diagonals, painted in colour); the cue = cue_0 1.5 → 1.9 b (turning) + cue_0 0.6 → 1.0 b at 45° + a pink glint 0.3 → 0.6 b inside, 7 t | `test_kit`: the rays reach 0.9+ of the card (glint_0 0.34), ≥ 1.0 b visible from the first tick, white core / gold rim, no ring; `render_hr.py … cue_p1 cue_p2 cue_far flashes` (F5 camera, her stand-in, the P1 moon and the P2 crimson field): 1.4 × 1.4 b on screen at 6 b and at 10 b from tick 1 (was 0.7 × 0.8 b, a pink dot) |
| HA-08 | `HITS['q']` grab kb 0 (`KB_THROW` gone) | `pat_lib`: "knockback only on the last hit of the chain" for every pattern (old: q's grab kb 5 at 20 of 4 hits) |
| HA-09 | full gauge: near band → `core/ult_go`; mid band → `ai/ult_close` (glide 0.3 b/t to 4 b, ≤ 40 t, `#ai_uc`), then the rings; a close that ran out of time starts them where she is (no chase) | `test_gauge`: 3 / 6 / 8 / 10.5 b → the rings start ≤ 4.5 b and all 4 rings land; a player walking away at 0.32 b/t → the rings after the 40-t close (old: from 8 b 3 of 4, from 10.5 b 0 of 4) |
| HA-10 | `test_flow.py`: the P1 check counts every judged P hit (no `parT` filter) | — (nothing was hidden; the check can now see it) |
| HA-11 | README 0-9 (573) and §3's table (920): the rebuilt kit's unparriable set from `api.HITS` (8 / 17, all with a flash) | — |
| HA-03 | G1 / G2 strikes re-timed; `tests/test_metro.py` (real F functions, every period 2-40, every start) | below |

## HA-03
`tests/test_metro.py` (new, 30 checks): `world` (the judged strikes of a standing player = the script), `train` (the real
`player/f_key` → `press` / `press_re`, the judge → `par_use` in a bare H1 world: every period 2-40, every start from T − 120
to the last cut, fresh F state), `real` (the best train of each worst period played in the real gauntlet, F through
`player/f_key` before each world tick: segments taken = the train's perfect parries, no repel). Search tools (in git, not
shipped): `tools/dev/sim/hr/review/metro/` — `fm.c` (a C model of the shipped rules; it matched test_metro on every period),
`dfs.c` (exhaustive DFS), `metro.py` (`table` / `search`, G2's row mapper `g2rows`).
- **G1** (9 cuts): 30 46 64 94 110 138 164 180 196 → **30 48 64 91 109 139 163 180 196** (c2 +2: A8.2 39; c4 −3: D2 77,
  A8.4 88; c5 −1: A8.5 103; c6 +1: D1 125, A8.1 136; c7 −1: D3 147, A8.6 160). The DFS found 33 311 strike sets with ≤ 3 for
  every period 8-30 and start (s1 28-34, gaps 14-30, last ≤ 199); this one is the nearest to the old (8 ticks moved).
- **G2** (11 cuts): 30 44 58 86 114 128 156 172 186 200 216 → **27 41 58 91 113 128 152 169 190 206 220** (every beat moved:
  D1 13, A8.1 24, A8.2 32, A8.3 49, D1 77, A8.1 88, vanish 97, D2 99, A8.4 110, A8.5 122, D4 138, A8.6 149, A8.7 166 / 187 / 203,
  A8.8 215; the dive 236 and the judge 242 as before). **Deviation from the ruling (≤ 3 for every period)**: with 11 cuts,
  every gap ≥ 14 and the moves' own spacing (a reappearance only after the vanish before it: the leap's gone + 2, the ring's
  vanish + 2, the X's gone + 2 — minimum gaps 14 14 24 20 14 23 14 14 14 14) the exhaustive DFS (every start ≥ T − 200,
  s1 21-32, last ≤ 221, gaps ≤ 50) finds **no** strike set that keeps every period 8-30 at ≤ 3 (9.7 M nodes, 0 solutions);
  without the spacing rule the local searches never found one either (best 4). The nearest sound thing: the set with the
  fewest 4s (local search: periods at 4, then starts at 4, then the distance to the old): 4 only at 16 t (24 of the starts
  T−200…220) and 19 t (2), 3 elsewhere in 8-30; **5 (a clear) at no period 2-40 and no start**. Old G2: 14 t 10, 12 / 28 t 6,
  mashers 3 / 6 t 5 (cleared). Knobs if the lead wants ≤ 3: 10 cuts (≤ 3 exists), or a gap minimum below the moves' spacing.
- Bolts: G1 102 → 99 (it fell on c5's new lock), G2 205 → 198 (one tick before c10's new strike); G2's `EXTRA_VANISH` 95 → 97.
- Metronome table (best perfect parries per period, any start; the real F functions, test_metro):

  | period | 2 3 4 5 6 7 | 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 | 31-40 |
  |---|---|---|---|
  | G1 old | 1 3 3 4 4 2 | 3 4 3 2 3 4 **5 5 5** 4 4 3 3 3 3 3 3 3 3 4 3 3 3 | 2 3 4 3 2 3 2 2 2 2 |
  | G1 new | 1 3 4 2 4 3 | 3 3 2 2 2 2 3 3 3 3 3 3 3 3 3 3 3 3 2 3 2 3 3 | 3 2 4 2 3 2 2 2 2 2 |
  | G2 old | 1 **5** 4 3 **5** 1 | 3 4 4 3 **6** 4 **10 5** 4 3 3 2 3 4 4 3 3 2 3 3 **6** 4 4 | 4 3 2 3 3 3 2 2 2 2 |
  | G2 new | 1 3 3 3 4 4 | 3 3 3 3 3 3 3 3 4 3 3 4 3 3 3 3 3 3 3 3 3 2 3 | 4 4 4 2 3 3 3 3 4 2 |

## Gates (the final tree, 0ca7c0c2b + the docs / tools commit)
| gate | result |
|---|---|
| build twice (`build_scarlet_rig.mjs` → `build_mboss_hr_fx.py` → `build_player_rig.mjs` + `build_player_audio.py` → `regen_all.sh --mobs`, two rounds) | round 1 = round 2: pack hash `44f657ac…`, the same git status / diff hash; the generators changed nothing but this lane's sources' outputs |
| `check_mboss_pack.py` | 0 problems (4 mid, 4 chapter, 3 special, 7 arenas) |
| loadcheck (26.3 server, tag `hfa`) | 0 function load failures, `Loaded 1870 advancements`, `Done` |
| `rplint` / `atlas_px` (`<S>/rp_hfa`) | 0 problems / 12 939 520 px (≤ 13.2 M; + 4 096 = `cue_0`) |
| hr suites | test_flow 40, pat_p1 559, pat_p2 70, pat_ghost 65, test_metro 30, test_gauge 33, test_bal_hr 79, test_scarlet 47, test_kit 15 802, test_rig 162, test_clips_h1c 297, ev_dry 82, ident_hr pass, test_actor 167, test_cine 159, test_contact 86, test_cam all, test_special_hr all, test_reward all, test_moon 55, test_hwamu 283, test_arena_hr 94, test_seq 392 (all), gen_check_hr 28 / 28 — all passing |
| combat suites | test_cb 296, test_rm 72, test_np 125, test_bal 117, test_bal_boss 117 — all passing |
| cost (test_flow, mean commands / tick) | P1 435, P2 441, G1 383, G2 398, lead 367, repel 386, the whole fight 360 (≤ 830) |
| the new checks on d7da75e79 | test_gauge 7 fail (HA-01 / HA-09), test_bal_hr 13 fail (HA-02 / 04 / 05), pat_p2 1 (HA-08), test_kit 9 (HA-06 / 07), test_metro 8 (HA-03) |

## Pack files (`<S>/rp_hfa` vs `<S>/rp_hi`; all from `build_mboss_hr_fx.py`)
- added: `assets/rlk/textures/mboss/hr_kit/cue_0.png`, `assets/rlk/models/item/mboss/hr_kit/cue_0.json`, `assets/rlk/items/mboss/hr_kit/cue_0.json`
- changed: `assets/minecraft/atlases/items.json` (the new sprite's source)

## Requests to other lanes
- **HB** (`wip/combat-hb`): HA-09 changes when the forced rings start (mid band: a glide first): T11 (U / min) and T4 may move
  a little. The gauntlet strikes changed (G1 / G2 above): T5 / T5b / T6 / T7's agents read `api.SCRIPTS`; T7's metronome
  agents should expect G2 at most 4 (16 / 19 t) and G1 ≤ 3. `api.py` merge: this lane touched `KB_THROW` / `HITS['q']`,
  `CUE_KIT` / `CUE_SND` comments, `KIT_SOUND_RECIPES['parry_cue']`, `KIT_SPRITES_HR`, `A8_SCRIPT`, `A13_SCRIPT`,
  `EXTRA_VANISH`, `BOLTS` and nothing else.

## What only a person in the game can check
- The cue: the white-gold star at her blade reads at once from the F5 camera on both fields and is not mistaken for the
  yellow / purple / blue flashes; the iron-xylophone tink is clearly not the purple flash's amethyst chime, short, not tiring.
- The gauge close (HA-09): she glides in from the mid band, then the rings; the feel of the 40-t cap.
- q's throw without a push still reads as a throw; the beam then finds the player where they stand.
- /reload during the groggy: she is lying at once; the kip-up from its tick.
- The re-timed gauntlets: the cuts' rhythm feels as intended (G2's dome three 21 / 16 t apart now), the reappearances
  after a vanish (G2: D4 2 t after the X's gone, D2 2 t after the ring's vanish) do not pop.
