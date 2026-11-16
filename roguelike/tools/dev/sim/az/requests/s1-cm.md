# Requests and notes from S1-CM (the chapter-boss mode, branch wip/az-cm)

Nothing here blocks S1-CM: every item below has its stand-in on wip/az-cm, marked where it lives.

## Needs (from other stages)

1. **S1-MOD: the rig visibility functions named by the stub manifest's states** (`states.<set>.vis` of
   `T:mboss_azhdaha/stub_rig_manifest.json`, today `rlk:mboss/azhdaha/rig_stub/state/normal` and `.../tail_only`).
   Why: the framework's `F:mboss/px/azhdaha/s/<set>` now calls them literally (never depending on generator order,
   cm.md 9.3); `check_mboss_pack` reports a missing one. Verified on wip/az-cm (uncommitted variant build with
   `azhdaha.enabled = true` and the wip/az-mod 83230b4 stub manifest): 135 px functions, 12 proxies, 41 clips (ids >= 1000),
   46 key files, five `px/state` lines for `#mbId 10`; only these two vis paths are external.
2. **I1 (integration): `arenas.az_cavern.ver`** stays 1 here (cm.md 2.3 day-0 value). S1-ARENA's item 3 (a dev world
   built from its day-1 commit keeps the flat arena under the same stamp `az_cavern@1:default`): bump `ver` to 2 at I1 or
   run `/execute in minecraft:overworld run function rlk:mboss/arena/az_cavern/rebuild` once in such a world.
3. **Contract owner (D0 checker): theme.md 5 `clear` boxes** - S1-ARENA's item 1. `build_cboss_rooms.py` now accepts both a
   flat `(x0, y0, z0, x1, y1, z1)` int tuple and the nested `((x0, y0, z0), (x1, y1, z1))` form (`flat_box`, corners
   sorted); please state the flat form in theme.md 5 so both readings stop being possible.

4. **I1 (integration): validator baseline once `azhdaha` is enabled.** `S:az/tests_cm/baseline/` accepts the chapter mode's
   findings on wip/az-cm (listed with the reason in `baseline/ACCEPTED.md`: macro `with storage` calls, the per-arena
   `full_rim` macro name, `stopsound` / `time` / `playsound $(ev)`, the proxies' fixed-UUID targets in `px/cproto/**`).
   With the entry enabled, `px/azhdaha/**` adds the same classes (fixed-UUID targets in its key / on / off / poll files,
   `px/state` called `with storage`); add them to the baseline the same way (`vcheck.py <kind> <out> --save` only after
   checking that every new line is one of those classes).

## Answers to requests addressed to S1-CM

- S1-MOD 1 / 2 (px runtime, `px/state` lines for azhdaha): done on wip/az-cm commit 2 (the core compiles `F:mboss/px/<id>/**`
  for every enabled `px:true` chapter boss from the merged manifest of cm.md 9.2 / manifest.md 1, and `px/state` carries
  literal lines per boss and set). Drop `core.px_target_stubs()` and `AZ:cmstub/px_state` after merging.
- S1-MOD 3 (`push/ring`): implemented (`push/ring {r,to,kb}`: radial to `to` over `kb` ticks, no damage, skips hazard landings).
- S1-MOD 4 (missing theme -> no prep): `build_cboss_rooms.py` writes the built-in default entrance (WARN line) when the
  theme module is missing, so `room/cboss/azhdaha/build` ends with `cb/prep` and `k_cboss2` falls back to the registry
  gate record (`k_cboss_fb`) if `cprep` is ever absent. The WORKAROUND in the S1-MOD tests can go after merging.
- S1-ARENA 1: see Needs 3; S1-ARENA 3: see Needs 2.
