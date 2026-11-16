# Accepted validator findings of the chapter mode (S1-CM)

`refs.txt`, `macro.txt` and `lint.txt` here = scratchpad `mb3/tests/baseline/*.txt` (M0's, unchanged lines) + the lines
below, found on wip/az-cm (fd88e33) and checked one by one. Every one is a known false-positive class of the validator; none
is a real missing function, a real missing macro argument or a real syntax error. `check_nbtpath` (invalid 0) and
`tools/check_mboss_pack.py` (0 problems) have no baseline: they must stay clean.

The "gone" lines vcheck prints (refs 3, macro 6 since the CM fix round: the `test/won` -> `test/cwon_msg` line moved to
`test/cwon`; lint 124) are mb3 baseline lines this tree does not produce: the M0
`mboss/hz/d/full`, `mboss/oob` and `test/defeat_msg` findings, whose source became the per-arena `ar/<aid>/full_rim`,
`ar/<aid>/oob` and `test/cdefeat_msg` (cm.md 6.2 / 12), and lines the mb3 baseline carried from its own tree that 039b911 does
not produce either (the `room/deco/op`, `room/deco/p` refs; butterfly `rig/c/*/k/<n>` key files absent at 039b911, e.g.
`coco/k/24`; ident.py proves the butterfly outputs byte-identical to 039b911). They are kept so the baseline stays a
superset of M0's.

Merge prep (wip/az-cm merged the 10-20 release 22ba247): `macro.txt` also takes the release's seven accepted lines of
the `function ... with storage ...` class (butterfly `p/sweep/ember` -> `fx/card`; fieldgen `fx/tele/{dark,rim}` ->
`tele/e/*`, `fx/p/rim_flare` -> `p/e/rim_flare`, `p/burst/redraw1` -> `fx/tele/{dark,rim}`, `p/fzone/rd` ->
`fx/tele/dark`), exactly the lines the shared `mb3/tests/baseline/macro.txt` gained with that release; the 25+ lines of
its removed decals stay as "gone".

## refs (3)

| finding | why it is fine |
|---|---|
| `rlk:mboss/ar/{az_cavern,cp_test,plaza}/full_rim -> rlk:mboss/hz/p/c/` | `function rlk:mboss/hz/p/c/$(kp)`: the name is built by the macro; `hz/p/c/1..60` exist. The M0 `hz/d/full` line it replaces had the same finding. |

## macro (39)

`check_macro` reads `function <f> with storage ...` / `with entity ...` as "called without args". Each line was checked to
be such a call (the args come from the storage / entity compound the line names):

| caller | callee | args from |
|---|---|---|
| `ar/{az_cavern,cp_test,plaza}/tp_in`, `ar/plaza/oob` | `safe_start`, `tp_start` | `with storage rlk:mboss cur.start` (the arena's start point) |
| `ar/{az_cavern,cp_test,plaza}/full_rim` | `hz/p/c/<n>` (+ "unknown `hz/p/c/`") | `with storage rlk:mboss hzp` (`col`, `sc`; plus the macro-built `$(kp)` name, see refs) |
| `arena/cp_test/s/1`, `arena/cp_test/l/{plain,lit}/0` | `arena/cp_test/done` | `with storage rlk:mboss arjob` (`look`) |
| `cb/won_kill`, `cb/won_cancel` | `test/won` | `with storage rlk:mboss cur` (`id`) |
| `test/won`, `test/cwon` (CM fix round: the chapter branch of `test/won` moved there), `test/defeat` | `test/cwon_msg`, `test/cdefeat_msg` | `with storage rlk:mboss tlast` (`ch`, `id`) |
| `music/set`, `music/loop`, `music/halt`, `music/stop` | `music/play`, `music/off` | `with storage rlk:mboss mus` (`ev`) |
| `resume`, `start_body`, `test/level`, `push/ring_land` | `music/set`, `repool`, `push/ring_go` | `with storage rlk:mboss a` (`ph`, `pct`, `t`; the line before fills it) |
| `push/cap_one` | `push/cap_top` | `with storage rlk:mboss pc` (`px`, the copy of `pq[0]`) |
| `px/cproto/spawn` | `px/state` | `with storage rlk:mboss px` (`set`) |
| `px/cproto/tick` | `px/cproto/follow` | `with storage rlk:mboss px.o` (`core_*`, `tail_*`) |
| `room/obj/k_cboss` | `room/obj/k_cboss2` | `with entity @s data` (`boss_id` of the entrance marker) |
| `room/obj/k_cboss2` | `room/obj/k_cboss3`, `room/obj/k_cboss_fb` | `with storage rlk:mboss cprep.$(boss_id).gate` / `cbyid.$(boss_id)` (the gate record, its registry fallback) |
| `room/obj/k_cboss_fb` | `room/obj/make_node` | `with storage rlk:mboss cbyid.$(id).gate` (`color`, `desc`, `item`, `model`, `name`) |

## lint (65)

| finding | why it is fine |
|---|---|
| `mboss/px/cproto/{clear_input,follow,poll,spawn,on/1,on/2,off/1,off/2}`, `mboss/px/cproto/k/<clip>/<tick>` (49 key files): `bad target '<uuid>'` | the hit proxies are addressed by their fixed UUIDs (`524c4b4d-...`, cm.md 9.1 / 14); a UUID is a valid target in vanilla. Same class as the M0 butterfly rig lines. |
| `mboss/music/{off,play,tick}`: `unknown command 'stopsound'` | `stopsound @a[tag=player] record $(ev)` / `... music`: a vanilla command the linter does not know |
| `mboss/px/{hit,dup}`, `mboss/mv/plpos`: `unknown command 'time'` | `execute store result score #pxG mb run time query gametime` (the de-dupe stamp, cm.md 9.6) and `... #plG mb run time query gametime` (the per-tick body position cache, cm.md 13.2, merge prep PERF-4); the M0 fieldgen lines have the same finding |
| `mboss/music/play`: `playsound id` | `$playsound $(ev) record ...`: a macro event id the linter cannot resolve; the ids are vanilla `minecraft:music.*` (registry `music`) |
| `mboss/cproto/test`: `execute without run` | `... run execute store success score #cpPush mb unless score #cpPush mb matches 1`: a condition ends the chain, valid |

## Tachy I1 (10-29): the rift hook lines (S1 request R1)
`shared_edits.diff` got `S:tk/tests/baseline/shared_edits_s1.diff` appended (the 13 `# rift (build_rift.py)` hook lines in 11
engine files, written by tools/build_rift.py; previous pin kept as `shared_edits.diff.pre_tk_i1`). Accepted by the lead at
the Tachy integration I1.
