# tests_cm: the chapter-boss mode's suites (S1-CM, AZ-CM)

    ./run_all.sh <worktree>/roguelike [tag]                 # everything (3 jobs; JOBS=n), outputs out/<tag>_*.txt
    RP=<unpacked resource pack> ./run_all.sh ...            # + the kits' and the boss bar's RP built twice (gen_check)

| file | what |
|---|---|
| `test_chapter.py` | cm.md 15.1 on cproto (every routing / registry expectation read from the registry under test, so Apep runs it unchanged): registry storage, routing (shipped registry + a variant with `route:true`), `#cbForce` resets, entrance -> prep -> cprep / forceload / sliced job, gate guards, spawn, kill economy (x15 x chapter, 2 sapphires, no boxes, k_chapter), abort -> same cprep, lose, title / repool / test/level, the test commands, music, cp_test looks / verify / sentinel / abort, cleanup paths (incl. a variant with `sweep`), Raiden smoke (in a chapter no `route:true` entry claims), and the CM fix round's regressions (test-session state after a chapter fight, a job of the fight arena at fight end / cleanup, the auto press after a manual press, the dev view's forceload, uninstall's scratch keys), and the recheck's every-chunk `ar/<aid>/loaded` (PERF-1); merge prep: `ar/<aid>/fl_off` aborts a running job of its arena, never another arena's (PERF-2, 17) |
| `test_px.py` | cm.md 15.2: proxy spawn / tracks / parking / state sets / pxinv, one attack event -> one body hit for the loops and every engine `combat/apply` call site (read from the files), reactions / DoT / lunar, RES / hooks / floor on the body, Navia, minimap, polls, push capsule, the target-side audit (README "챕터 보스"), /reload, a registry variant with `shield:true` beside the proxies (Apep O2, recheck APEP-10) |
| `test_fw_az.py` | cm.md 15.3: mask hazard, hit / dodge events, pl_dot, NoRx, floor, aux RES, cine, push ring, lockv, local, hz/extend, #pjNoDodge, bossui options vs the M0 draw, mid-boss fights unchanged; recheck regressions: a NoRx set for a pl_dot is spent (3j / 3k), push ring without int32 overflow, r / to clamps, the centre bearing (8d-8f); merge prep: the per-tick body position cache `mv/plpos` (one player-body NBT read per live chapter tick, same-tick reuse, re-read next tick, dropped by a push that moved the player and by the chapter `tp_in`; PERF-4, 16) |
| `test_fw_ap.py` | cm.md 22 (AP-FW, wip/cm-ap): per-mille hazards `#hzPm` / `#hzPmL` (pl_dot share, no defence, element shields, lethal flag, dash dodge / `#hzNoDodge`, events, re-arm, volley group, a per-mille mask with a dome, one-shot resets), mask safe groups from `hz/safe_new` (negative ids; the APEP-04 collision repro), the look record `look_<aid>` (build / look / reload / done / restore / abort / clear / stub / uninstall), music pools (track table, `music_len`, the registry check), the real + stub manifest merge (fallback ids >= 1000, unique), cine refusal without consuming (hazard, projectile, volley group), `#auxShW` / `#auxShH` / `#auxHbY` (hb_y checked as text: `execute on passengers` is beyond mcsim) and `mv/step_flat`. A tree without AP-FW (no `mboss/hz/safe_new`) is skipped with rc 0 |
| `gen_check.py` | generator order / second run / reverse / ownership probes incl. arena, build_cboss_rooms, cproto (S1-CM copy of mb3/tests/gen_check.py) |
| `test_m0diff.py` | the mid-boss fights against the base by behaviour (CM fix round; base = the release 22ba247 = M0 039b911 + the 10-20 release since the merge prep): the base commit's data/ + registry (git archive from S1-CM's worktree into tmp/) and the tree run the same azsim scenarios with the same seed for proto / Guardian / butterfly / fieldgen: a 1200-t fight with strikes (per-tick trace, damage / dodge / hazard / projectile / rig / line logs, commands per tick within +6.5), kill / cancel / pause / reload (traces, end-state scores / entities / storage with allow-lists of the chapter-mode names), and the bossui/draw line for 6 inputs (byte-identical, at most +6 commands per draw) |
| `ident.py` | byte identity against the release 22ba247 (= M0 039b911 + the 10-20 release, which changed no plaza / framework / engine text; re-pinned from 039b911 at the merge prep): F:mboss/{guardian,butterfly,fieldgen,proto}/**, the plaza (2b: every plaza per-arena function = its M0 lines, incl. marker / full_rim / box_absorb / fl_on / fl_off / loaded; 2c: mv/ok, mv/leash, mv/clamp = one chapter line + M0's), tools/ outside S1-CM's files, engine files outside the cm.md 16 table, and 4d: the content of every shared edit pinned in `baseline/shared_edits.diff` (`--save` rewrites it after a reviewed cm.md 16 change) |
| `vcheck.py`, `baseline/` | validator comparison; baselines = M0's (mb3/tests/baseline) + the accepted chapter-mode findings (`baseline/ACCEPTED.md`) |
| `lib/cmsim.py` | the chapter-mode sim: block world, chunk loading (forceload + load delay), tellraw / title / stopsound capture, quoted NBT keys, `data modify storage ... set from entity <sel> Pos|Rotation`, `moved(s)` (a test teleport inside one sim tick drops the `mv/plpos` cache), interaction click NBT, `difficulty`, oversize engine fills fail as in vanilla, room-gen emulation (`boss_map`), variant trees (`variant`) |

Vendored, unchanged copies of the S1-HARN harness (so later edits there cannot move these suites):
`lib/azsim.py` 10d5d16c4a71746ff6b336f80c2f08c0 (= scratchpad harness/azsim.py), `lib/fgsim.py` fa9456c918b23c394f55993971bbf62b,
`lib/mcsim.py` 7ac6cf819479d32684e236f37b67547e.

Sim limits worked around in the suites (each marked at its line): `combat/melee_front` (a `tp ... facing` the sim cannot
run) is stubbed to "in front" in test_px 4c; the dash i-frames are set right before each `cm/hit_pl2` (the harness tick
resets the score) in test_fw_az; `execute store success ... unless ...` (cproto test 30's toggle) is not stored on a fail
by mcsim, so test_px sets `#cpPush` directly; M0's `room/wipe` has an 81 920-block fill, which fails in vanilla and is
recorded (`s.big_fills`) instead of raising.

Temporary trees (the variants, gen_check) live in `tmp/` and are removed after each use.

11-03 deliberate deviations (`tools/dev/sim/README.md` section 2, "11-03 에 고친 곳"): `lib/cmsim.py` `variant()` and
`gen_check.py` `light_copy()` skip `tools/dev` (a harness inside the tested tree made the walk copy its own tmp/ without
end), and both copy `F:boss/test` for real (`real` / `REAL_DP`; as a hard link the core run in the copy rewrote the tested
tree's 13 boss/test files, the old check-9 failure). `ident.py` is stale (pinned to 22ba247 and S1-CM's file lists).
