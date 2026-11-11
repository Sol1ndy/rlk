# lane HI-1 (홍련 rebuild: integration) — progress

Branch `wip/combat-hi` (from `origin/wip/combat` f73a49f94), worktree `<S>/cb/wt_hi`, pack copy `<S>/rp_hi` (from the
11-11 release pack `<S>/rp_rel`, read-only), `<S>` = the scratchpad of `h_common.md`. Brief: merge H1 → H1c → H2 → H2c →
H3, close `hi_todo.md` 1-6 and 9-12 (7 balance and 8 the in-game list are not this lane's), every gate on the merged tree,
one full fight in the simulator. A fresh agent resumes from "Next".

## Steps
- [x] merges (406020d0f H1, d1862654f H1c, fa50785d8 H2, bee653a81 H2c; H3 0c762626b was already in H2: "Already up to date")
- [x] regenerate in README 0-4's order (f97c1cb90): rig → kit → player rig + actor → `regen_all.sh --mobs`; a fresh build
      into an empty `boss/scarlet` + `char/cine` (scratch copy) gives the same file set and the same pack (no stale file)
- [ ] hi_todo items (below)
- [ ] gates on the final tree, the full-fight run, README, pack list

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

## hi_todo items
| # | item | state |
|---|---|---|
| 1 | kcut's big yellow `{t:110}` | `p1.py` `flash_args['yellow'] = {'t': 110}` (uncommitted at the time of writing) |
| 2 | P1 rings: the stance at 49 | open |
| 3 | test_kit's first-person deflect pins | open |
| 4 | gen_check_hr's stray `p/r1/` | H1c moved the probe to `p/q/`; no `p/r1` in the tree; gen_check_hr to run |
| 5 / 10 | test_rig rebased (cinematic rows from test_cine §4.1) | open |
| 6 | README (홍련 section rewrite, ev_dry counts, 0-4 / 0-8, pack README lines) | open |
| 9 | I18 brim at the lens | open |
| 11 | small clip items | open |
| 12 | gold overlay live | done by the regeneration (the sequences' `white` stand-in → `gold` at cs1 10, repel 0, ending 70 / 190 / 286) |
| — | raw-sound stand-ins → kit recipes | `seq.py`: cs1 drink → `cs0_sip`, cs1 slash → `iai_slash`, repel 139 → `land_grass`, ending lock → `blade_lock`; the actor's three cuts stay raw sweeps (no kit recipe for the player's cut) |

## How to run
```bash
S=<scratchpad>; WT=$S/cb/wt_hi/roguelike; cd $WT
node tools/build_scarlet_rig.mjs --resourcepack $S/rp_hi          # ~2 min
python3 tools/build_mboss_hr_fx.py --resourcepack $S/rp_hi
node tools/build_player_rig.mjs --datapack . --resourcepack $S/rp_hi
bash tools/dev/regen_all.sh --mobs
bash $S/hi_tools/simcopy.sh        # the suites run from a copy: $S/hi_sim (old scratch path rewritten)
```

## Pack files that differ from `<S>/rp_rel` (all from the generators)
- changed: `assets/minecraft/atlases/items.json` (H3: `rlk:skin/{lumine,clorinde,ronova,nefer}`), `assets/rlk/font/mboss_hr.json`
- added: `assets/rlk/textures/font/mboss_hr/{gold,gold_1..4,web,web_1..4}.png`, `assets/rlk/textures/skin/lumine.png`,
  `assets/rlk/{items,models/item}/player_motion/{lumine,clorinde,ronova,nefer}/**`, `assets/rlk/items/player_motion/weapons/cine_sword.json`

## Next
- close the open items above, then the gates and the full-fight run.
