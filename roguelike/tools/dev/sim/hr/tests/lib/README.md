# HR/tests/lib — the simulator library of the 홍련 (Scarlet) suites

Owner: **S1** created it (11-04); **S3 takes it over after S1's report** (`tools/mboss_scarlet/api.py` `HANDOVER`) and
extends `hrsim.py`. Every other stage only reads this folder and keeps its own helpers in `HR/<stage>/`.

Vendored, **unchanged** copies of `roguelike/tools/dev/sim/az/tests_cm/lib` at the D0 base `5d2c3ac` (= the 11-03 handover
tree; dependency order mcsim ← fgsim ← azsim ← cmsim). Never edit them: put additions in `hrsim.py` (subclass / wrap).

| file | md5 (copied 11-04) | what |
|---|---|---|
| `mcsim.py` | `7ac6cf819479d32684e236f37b67547e` | the mcfunction interpreter (scoreboard, execute, function / macro, summon, tag, tp, data, return; unknown commands counted in `s.ignored`) |
| `fgsim.py` | `fa9456c918b23c394f55993971bbf62b` | the mid-boss framework world (engine stubs outside `F:mboss`, attributes, schedules, sound / rig / kit logs) |
| `azsim.py` | `e9ccb4462191e9c22089f728c16dd502` | the engine wrapper: `combat/apply`, the kill path, element reactions, `player/take_damage`, `room/zone_build|enter|combat_clear` for real; `setup`, `world`, `room_tick`, `to_fight` |
| `cmsim.py` | `7de1dd2c194339ed40df7ac54df41a7b` | the chapter-mode world: sparse block world, chunk loading, tellraw / title capture, `variant()` trees (the 11-03 version: skips `tools/dev`, real-copies `F:boss/test`) |
| `hrsim.py` | S1's version `d8231714caedb3210f3cb277c6ff6cd8`; S3 extended it (11-05, below) | this boss's generic world (below) |

`hrsim.py` (S1):
- `HrSim` (= `Log` + `cmsim.CmSim`) for special fights, `AzLog` (= `Log` + `azsim.AzSim`) for mid-boss fights in the plaza.
  `Log` adds `s.particles` (tick, name, executor position), `s.bars` (visible flag per boss bar), `s.bar_draws` (ticks
  of the `rlk:mboss` name draw = one `mboss/bars` run), `s.watch` (put function ids in it: every call is logged with
  tick, executor type, tags, position), and `function <f> with entity <sel> data.<path>` taking the macro arguments from
  that path (mcsim passes the whole `data`).
- `setup(dp, seed)`: the chapter-mode world on a normal map with `room/rift/init` done; `rift_zone(s, sid)` a visited
  combat zone (`rlk_riftz`, `data.rift.id`) + an open rift anchor; `enter(s, anchor)` the REAL `mboss/sp/gate`;
  `special_fight(s, sid)` → fight state; `kill(s, pl)` (`mboss/test/kill`); `finish(s)` (until `#mbLive 0`,
  `#combat 0`); `boxes(s)`; `register_text(dp)`, `record(txt, id, n)` (the SNBT record of an entry).
- The room tick of a rift zone: `azsim.room_tick` is wrapped at import (module attribute; the file is unchanged): the
  spawn countdown ends in the REAL `room/mob_wave` (→ `mboss/sp/start_zone`), a zone without `rlk_zmob` runs the REAL
  `room/combat_clear` (→ `mboss/sp/clear` → `sp/won` → `sp/won_kill` → `sp/reward`); `world(s)` then runs the REAL
  `room/rift/tick` while `#riftOn room` is 1 (the 30-t collapse and `close_end`'s boxes).
- Re-exports `check`, `summary`, `variant`, `drop_variant`, `entry`, `C0`, `FAIL` from cmsim.

`hrsim.py` (S3 additions, 11-05; used by `test_scarlet.py`, `pat_p1.py`, `test_reward.py`, open to S4's `pat_ghost.py`):
- `ScSim` (= `HrSim` +): a **dash i-frame model** (`s.dash(v0=6, at=None)`: the world tick `at` (default the next one) sees
  `dashInvT v0`, then 1 less per tick, as `player/dash_go` + `player/tick:59`; `world_sc` keeps the value through
  `mboss/main`, unlike `azsim.world` which zeroes it); `if|unless predicate rlk:in_sneak` and the selector argument
  `predicate=rlk:in_sneak` (= the player's `e.data['sneak']`); `scoreboard players reset * <obj>` and
  `scoreboard objectives remove <obj>` (its scores go); per-world-tick command counts `s.cmd_hist` (every `cmd()`
  invocation, an `execute … run` counts its sub-command too: the stricter count); logs `s.hzr` (every `mboss/hz/make`:
  the options, position, yaw, `#pt / #pat / #ph hr`), `s.phits` (`cm/hit_pl2`), `s.rigl` (`rig/**` / `rig_stub/**`
  calls), `s.kitl` (calls under `rlk:boss/scarlet/fx/**`, stubbed: a dry build with the kit forced on), `s.hz_particles`
  (particles drawn inside the framework's hazard functions), `s.deaths`; `player/die` is a stub (`dead 1`, or with
  `s.revive = n` Ronova's revive: `rnDie n` counting down, then full HP).
- `world_sc(s)` (one game tick in `rlk:tick` order with the dash model), `run_sc`, `until_sc`; `setup_sc(dp, seed)`
  (`setup` with `ScSim`; the arena's missing `look/<look>` jobs become no-ops unless a test stubs them); `fight_sc(s,
  intro=False)` (her rift → the intro state, `intro=False` ends the intro at once); `test_id(s, n)` (`/function
  rlk:boss/test/pattern {id:n}` as the player); `hold(s)` (the AI hold `#lock hr 1`), `start_pattern(s, tid)`,
  `place_player`, `place_body`, `heal`, `snap`, `ents_tagged(s, prefix)`, `hr(s, k)`, `call_sc(s, rel)`, `ck` (check
  printing its detail only on failure).
- Variants: `variant_hr(dp, edit)` (`cmsim.variant` + a real copy of `F:boss/scarlet`), `enable_scarlet(reg)`,
  `dry_build(root, kit, theme, patch)` (regenerates `F:boss/scarlet` **inside a variant only** with `api.K` / the theme
  forced on and any api attribute patched, e.g. `"api.ULT5_LETHAL = False"`).

Run every suite from `HR/tests` (outside the datapack, `tools/dev/sim/README.md` §1); variant trees go to `HR/tests/tmp`
(`cmsim.variant`, removed after use, ≈ 75 MB each: `F:mboss` + `tools` copied, the rest hard links).

I1 (11-05, the lead; the vendored four are still unchanged, md5s as above): `ScSim` now runs what the merged stages'
real files use and the stand-ins never did — `tp <sel> <x y z> facing (entity <sel> [eyes|feet] | <x y z>)`, `rotate <sel>
<yaw> <pitch>` and `rotate <sel> facing …` (S2b's `seq/**`, the framework's `mboss/pull/finish`), and an absolute `execute
… facing <x> <y> <z>` (rewritten to `facing entity` of a fixed helper marker tagged `hrsim_fc_*`, never `rlk_*`; ports of S2b's
`ev_dry.py` handlers); `setup_sc(..., cls=)` takes an `ScSim` subclass (test_reward's `real` section: SR's SNBT reader from
`HR/sr/srsim.py` for the item tables, with mcsim's own macro call kept).

I1b (11-05, the lead; the vendored four still unchanged): `HrSim.block_test` resolves `#rlk:dash_pass` / `#rlk:cm_pass` from
the datapack's own tag files (`data/rlk/tags/block/*.json`; the vanilla tags they name with their 26.3 contents:
`#minecraft:replaceable` listed in `MC_BLOCK_TAGS`, small flowers / rails / buttons / wool carpets by name). The vendored
`cmsim.block_test` lets only air and light through those tags: harmless on D0's stub arena, but S1K's `hr_field` has dry grass /
crimson roots in the walk disc, so `mv/ok` refused every plant cell in the sim (the intro walk stopped at the first tuft) while
the game lets them through. The suites moved with this folder to `R:tools/dev/sim/hr/tests/lib` (I1b step 5).
