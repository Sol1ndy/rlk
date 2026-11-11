# lane HI-1 (홍련 rebuild: integration) — progress

Branch `wip/combat-hi` (from `origin/wip/combat` f73a49f94), worktree `<S>/cb/wt_hi`, pack copy `<S>/rp_hi` (from the
11-11 release pack `<S>/rp_rel`, read-only), `<S>` = the scratchpad of `h_common.md`. Brief: merge H1 → H1c → H2 → H2c →
H3, close `hi_todo.md` 1-6 and 9-12 (7 balance and 8 the in-game list are not this lane's), every gate on the merged tree,
one full fight in the simulator. A fresh agent resumes from "Next". (The container was replaced once, after f97c1cb90:
the scratchpad survived, nothing was lost.)

## Steps
- [x] merges (406020d0f H1, d1862654f H1c, fa50785d8 H2, bee653a81 H2c; H3 0c762626b was already in H2: "Already up to date")
- [x] regenerate in README 0-4's order (f97c1cb90): rig → kit → player rig + actor → `regen_all.sh --mobs`; a fresh build
      into an empty `boss/scarlet` + `char/cine` (scratch copy) gives the same file set and the same pack (no stale file)
- [x] hi_todo 1 / 2 / 3 / 5 / 9 / 10 / 12 + raw sounds (3477dbf81); the full-fight run `test_flow.py`, hi_todo 11, test_rig
      green (55a18e7e5); test_bal_hr's q rows rebased on FB's rule, README (this commit)
- [x] the final gates on the final tree (c762caac1 + this commit: gen_check_hr 28 / 28), pack README (`hi_rp_readme.diff`),
      the integration pack zip `<S>/hi_out/rlk_hud_resourcepack_hi.zip`

## Merge conflicts and how each was resolved
| merge | file | kind | resolution |
|---|---|---|---|
| H1 | `tools/build_balance.py` `boss/may` | source | both rules: H1's `#mbBalOff` (FN-bal) then FB's `rlk_mb_inv` (the order H1c / H2 used) |
| H1 | `bal/boss/may.mcfunction` | generated | regenerated from the merged generator |
| H2 | `tools/dev/sim/hr/tests/ident_hr.py` | source (notes) | both group notes: fix A (wip/combat) and lane H2 |
| H2 | `tools/scarlet_rig_manifest.json` | generated | H2's side, regenerated after the merges |
| H2c | `tools/build_mboss_hr_fx.py` | source | both marked blocks after the `GLYPHS` literal: H1c's `web` part 1, then H2c's `gold` block |
| H2c | `tools/build_balance.py` | source | ours (same two rules, H1c / H2 order; H2c had them swapped) |
| H2c | `bal/boss/may`, `boss/scarlet/{fx/e/init,rig/an/load,rig/init}`, kit + rig manifests | generated | ours, regenerated |
Auto-merged shared sources checked by hand: `build_scarlet_rig.mjs` (H2's look target + H1's owner map + H2c's lines),
`scarlet_retarget.mjs` (H1c's `HAT_FLIGHTS.grog_in` line + H2c's rows), `build_mboss_core.py` (FN-cam + FN-bal zero lines).

## hi_todo items
| # | item | state |
|---|---|---|
| 1 | kcut's big yellow `{t:110}` | done: `p1.py` `flash_args['yellow'] = {'t': 110}` → `p/kcut/k/3` calls `yellow_tell {t:110}` |
| 2 | P1 rings: the stance at 49 | already right on the merged tree (probe + new `pat_p1` rows): without ult the kept tail plays the recovery's move clip at r4 + 4 = 48; with ult, `ult` starts at 50 and clip tick 49 is the coil of 48 (same pose). No code change |
| 3 | test_kit's first-person deflect pins | dropped (first person = developer mode only); the deflect is now found at KR in `seq/repel/start`; the anchored check keeps the instant death's line from F5. 15 796 / 15 796 |
| 4 | gen_check_hr's stray `p/r1/` | H1c's probe uses `p/q/`; no `p/r1` in the tree; gen_check_hr run on the final tree (see gates) |
| 5 / 10 | test_rig rebased | the 11-06 cinematic rows replaced by test_cine's §4.1 versions on test_rig's replay (states, 11 hand-overs, the kick seam, swing spans from the clips' "every tick" spans); the cs1 petal coupling rebased (S10 590-605 vs the head anchor); the user's skin file optional (the embedded copy is the reference); the `float` air check skips blend-in ticks (repel 0-2 = the replay without g_dive) as its doc says; the dump runs 59 / 59. test_kit's sound-count pin was already 110 (H1c) |
| 6 | README | the 홍련 section rewritten for the rebuilt fight; 0-1 (HI line), 0-3 / 0-4 (the actor in the player rig build), 0-8 (the new suites), 0-9 (first-person anchors left). Pack README: see "Pack README" below |
| 9 | I18's brim | the shot opens at `HR(0.15, 1.2, 1.5)` and pushes in to the design's `HR(0.15, 1.35, 1.0)` over 1290-1310 (`io`): her brim stays ≥ 0.32 b from the lens (her_tracks.json; was 0.04 b at 1296). The skip still lands on the cut's eye |
| 11 | small clip items | cs1 236 brim into the head corner: fixed (head pitch −5 at 236, test_rig `hats: worn` now ≥ 1 mm; test_cine 159, test_contact 86 unchanged). Not cheap, kept as bounded `KNOWN` rows in test_rig (printed as reported): the sheathed hilt 0.016 / 0.008 b off the scabbard pivot at intro 787 / 788 (the shared rig compiler's 1-tick reappearance key — changing it touches every RIGLIB rig), the hat switch 0.198 b at repel 84 (the hat's flight speed in the throw) and 0.187 b at 139 (put-on snap), the lying fist 0.046 b (limit 0.04) in repel / ending (two contacts on one hand) |
| 12 | gold overlay live | done by the regeneration: `white` → `gold` at cs1 10, repel 0, ending 70 / 190 / 286 |
| — | raw-sound stand-ins | `seq.py`: cs1 drink → `cs0_sip`, the 홍련일섬 slash → `iai_slash`, repel 139 → `land_grass`, ending lock → `blade_lock`. The actor's three cuts (repel 56 / 62, ending 120) stay raw sweeps: the kit has no recipe for the player's cut |
| — | stand-ins left | none: rig 0 stand-ins, `api.actor_ready()` true, no `core/sq` / `core/gs` / `rig_stub` |
| 7, 8 | balance, in-game list | not this lane's (numbers as H1 committed them) |

Found at HI (not in hi_todo): `test_bal_hr` q rows failed on the merged tree — fix lane FB's rule in `bal/boss/may` refuses
balance damage on an untargetable body, and q's ghost lunge (4-20) is `rlk_mb_inv`: the break there is refused, not pending.
Rebased: refused during the ghost, pending from the grab to the pattern's end (49 / 49).

## Gates (the final tree)
| gate | result |
|---|---|
| build twice (rig → kit → player rig + actor → `regen_all.sh --mobs`, two rounds) | no file of `data/` or the generated `tools/` changed in either round; pack hash `e6b8b2dd…` after round 0, 1 and 2 (`$S/hi_tools/twice.sh`) |
| `check_mboss_pack.py` | 0 problems (4 mid, 4 chapter, 3 special, 7 arenas) |
| loadcheck (26.3 server) | `hi`: 0 function load failures, `Loaded 1870 advancements` |
| `rplint` / `atlas_px` | 0 problems / 12 935 424 px (≤ 13.2 M; +16 384 = H3's four actor skins) |
| other bosses' output vs `wip/combat` | only the shared framework lines: `mboss/{main,init,cleanup_fight,fight_vars,uninstall}` + `tick` · `view/tick` · `lvup/tick` (FN-cam), `bal/boss/may` + `fight_vars` / `cleanup_fight` (FN-bal), `mboss/register` (her registry entry intro 1450 / death 1494); no other boss module file |
| hr suites | pat_p1 531, pat_p2 67, pat_ghost 65, test_gauge 22, test_bal_hr 49, test_scarlet 47, test_special_hr all, test_reward all, test_moon 55, test_hwamu 283, test_arena_hr 94, test_kit 15 796, test_rig 162, ev_dry 82, ident_hr pass, test_seq 392 (all sections, 9.5 min), test_cam all, test_actor 217 (`--rebuild`, reference = the pack without the actor), test_cine 159, test_contact 86 (with the actor's manifest), test_clips_h1c 297, test_flow 40 — all passing; gen_check_hr: see below |
| combat suites | test_cb 296, test_rm all, test_np 125, test_bal 117, test_bal_boss 117 — all passing |
| cost | test_flow per phase / sequence ≤ 429 (budget 830), the whole fight 353 |

Suite fixes made at HI for lane interactions (none hides a defect; each now checks the merged behaviour):
- `test_bal_hr` q rows: FB's untargetable-body rule vs q's ghost lunge (above).
- `test_cb` / `bossloop_cb` (lane C): rlk:tick's near pass "right after mboss/main" — H2's FN-cam hold / release lines sit
  there too (test_cam pins them right after main); now: only FN-cam lines may stand between. `test_cb`'s 홍련 reader row:
  the rebuilt pip is `shield/tick` on a judged perfect parry (no `shield/pip`, no `q_pf` query).
- `test_bal_boss` (lane B): "every flagged boss has a case here" accepts 홍련's rows in `hr/tests/test_bal_hr.py` (H1 moved them).
- `ident_hr`: allow-list group for wip/combat's be0016710 (Azhdaha's brand cleanse comment, after the lanes branched).
- `gen_check_hr`: the rig also owns `tools/dev/sim/hr/cine/her_tracks.json` (H2c); G5 compares the items atlas as a set
  (README 0-9: its source order follows the generators' run order; with the documented order rig → kit → player rig the
  player rig's aliases come last, a rig-only build re-appends the scarlet skin entry) and requires the second build
  byte-identical. First run (before the fix, 19 min): only those two rows failed; G3 (documented and reverse order), G4
  (strays incl. `p/q/`, hi_todo 4) passed. **Second run on the final tree: 28 / 28 (18 min).**

## The full-fight run (`tools/dev/sim/hr/tests/test_flow.py`, 40 checks, ~1 min)
Real rift, core, sequences with the lock (camsim), kit; the actor's calls modelled as seqsim does (test_actor runs the real
`char/cine`). A perfect parrier (F at h − 1 for every cue). CS0 locked 1438 of 1440 t → hand-back clean → P1 1500 t (cues,
groggies, the gauge to 50) → 60 % → CS1 locked 719 t → lead60 → G1 cleared by perfect parries → repel {at:60} locked, 3 × 15 ‰,
balance 4 → 7 → P2 1500 t (mx / nb / q seen) → 5 % → lead5 → G2 failed (no parry: the instant death at T + 242) → Ronova →
lead_re → G2 cleared → repel {at:5} (kill at 129) → ending + coda locked 1489 t → reward, released, nothing left. Branches:
G1 failed (P2 at T + 240, player alive); inside CS1: death with Ronova (released at once, CS1's end state at the resume,
the chain goes on), relog, the live stand killed, /reload, abort, mboss/uninstall — all released, nothing left, the chain
goes on where it should. Cost per tick (mean): P1 429, P2 418, G1 383, G2 393, stance 366, CS0 282, CS1 303, lead60 330,
repel 386, lead5 405, lead_re 375, ending 275, coda 235; the fight 353 (≤ 830). Max: P2 1 404; the arena's build / look
slices 5 140 / 2 931 (11-06's theme, counted apart).

## How to run
```bash
S=<scratchpad>; WT=$S/cb/wt_hi/roguelike; cd $WT
node tools/build_scarlet_rig.mjs --resourcepack $S/rp_hi          # ~2 min
python3 tools/build_mboss_hr_fx.py --resourcepack $S/rp_hi
node tools/build_player_rig.mjs --datapack . --resourcepack $S/rp_hi
bash tools/dev/regen_all.sh --mobs
bash $S/hi_tools/simcopy.sh        # the suites run from a copy: $S/hi_sim (old scratch path rewritten)
bash $S/hi_tools/run_suites.sh     # every hr suite but test_seq / gen_check_hr + the combat suites -> $S/hi_suites/summary.txt
# apart (long): test_seq.py $WT (~15 min), gen_check_hr.py $WT --rp $S/rp_hi (~1 h), each from its own sim copy
```
(`$S/hi_tools/*` are scratch helpers; if gone: the sim copy is `cp -a $WT/tools/dev/sim <copy>` + the sed of h1's recipe.)

## Pack files that differ from `<S>/rp_rel` (all from the generators except README.md)
- changed: `assets/minecraft/atlases/items.json` (H3: `rlk:skin/{lumine,clorinde,ronova,nefer}`), `assets/rlk/font/mboss_hr.json`
  (+ gold, web and their fade steps)
- added: `assets/rlk/textures/font/mboss_hr/{gold,gold_1..4,web,web_1..4}.png`, `assets/rlk/textures/skin/lumine.png`,
  `assets/rlk/{items,models/item}/player_motion/{lumine,clorinde,ronova,nefer}/*` (80), `assets/rlk/items/player_motion/weapons/cine_sword.json`
- `README.md` (hand-written, not in git): the actor's folders / skin / generator row and the `mboss_hr` font row (8 overlays,
  U+EC10–EC18, steps to U+EC3F, 41 glyphs); the exact change is `tools/dev/plan/combat/hi_rp_readme.diff` (apply to the
  release pack's README). The integration pack: `<S>/hi_out/rlk_hud_resourcepack_hi.zip` (11 919 KB, 4 868 files).

## Next
- Nothing open for this lane. After HI: the independent review, then the balance pass (hi_todo 7), then the in-game list
  (hi_todo 8) and the release (README 0-5: build stamp, 0-10, the pack README's version line + `hi_rp_readme.diff`).
- For the review, first: (1) the FB / H1 interaction (q's ghost lunge takes no balance: refused, not pending); (2) the lane
  C / H2 order in rlk:tick (near pass after FN-cam's lines); (3) the camera stands outlive a pause until the resume's
  cancel (invisible markers; the player is released at once); (4) the I18 push-in (numbers from her_tracks only); (5)
  hi_todo 11's three bounded leftovers; (6) kit sound recipes the rebuilt sequences no longer call (cloth, draw_ring,
  glint_ring, black_drop, brim_ring, repel_lock, tip_over, band_*, scab_swing, moon_gaze, pivot_cloth, dark_*); (7) the
  arena build slice at 5 140 commands (11-06's theme, unchanged).
