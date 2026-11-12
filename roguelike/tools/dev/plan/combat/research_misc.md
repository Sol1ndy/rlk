# research_misc — bow / Yoimiya removal, view removal, pick subtitle gate, late-game TPS

Tree: `/home/user/rlk` @ `2dcc742` (branch `claude/exciting-pascal-ek1vuy`), datapack `roguelike/`, functions under
`F:` = `roguelike/data/rlk/function/`. Read-only research: nothing in the repo was changed. Measurements were made with a
scratch harness in `cb/misc/perf/` (section 4.1). Line numbers are for `2dcc742`.

---------------------------------------------------------------------------------------------------------------------

## 1. Remove 요이미야 (`yoimiya`) and every bow-weapon plan

### 1.1 What the bow code is shared with (do not delete blindly)
`F:char/bow/` is two things: the bow weapon (Yoimiya only) and the **projectile framework** that Ronova and Clorinde use.

| keep (shared) | used by | after removal |
|---|---|---|
| `char/bow/arrow_tick` (13) · `arrow_step` (14) · `arrow_hit` (42) · `arrow_end` (8) · `arrow_home` (4) | `F:tick.mcfunction:32` for every `rlk_arrow`; Ronova's orbs (`aKind` 7) and echoes (`aKind` 8, `arrow_home` for 8) via `char/ronova/proj_spawn` | strip the `aKind` 1–6 branches: `arrow_tick:4-5` (염초 homing), `arrow_step:4-5` (kinds 1/5 trails), `arrow_hit:4` (kind 6) and everything after `:4` except the `#jend` line (kinds 7/8 return at `:3` into `ronova/proj_hit`; the generic damage/`#basic`/blaze/firework part serves only kinds 1–6), `arrow_end:4` (kind 6) and `:6` (fire lava), `arrow_trail` becomes empty (only kinds 1–6) → drop it and its call `arrow_tick:13` |
| `char/bow/assist` (16) | `char/clorinde/shoot:24`, `char/ronova/proj_spawn:25` | unchanged |
| `char/bow/calc` (11) | `char/clorinde/shoot:19`, `char/ronova/na:13`, `char/ronova/echo_fire:3` | unchanged |

Optional: move the kept 7 files to `char/proj/` and fix the 6 call sites + README 1087 (`char/bow/arrow_*`). Keeping the
folder name avoids touching Ronova/Clorinde; either is fine. `#bowHit tmp` is the generic "ranged hit" flag
(`combat/apply:62,64`, clorinde `shoot:39,43`, ronova `proj_hit:11,20`, and generated `cm/c2|c3/true_hit:11`,
`mboss/true_hit:14` from `tools/ch2mob/common.py:431` · `tools/build_mboss_core.py:1315`) — keep the name (renaming forces
regeneration of mob / mboss output for no gain).

### 1.2 Delete
- `F:char/yoimiya/**` — 17 files, 194 lines.
- Bow-only `F:char/bow/` files — 18 files, 184 lines: `na` `na_shot` `flurry_fire` `queue_fire` `queue_tick` `rdash`
  `release` `shot_aim` `shot_full` `spawn` (only bow/yoimiya call it; Ronova has its own `proj_spawn`) `stage1` `start` `tick`
  `toggle` `charge_tick` `av_pull` `hand_pull` `cancel`.
- `F:char/weapon_item_bow.mcfunction` (1 line).
- The 연격 (`flurry`) engraving's bow branch goes with `bow/na:33-34` + `flurry_fire` + `queue_tick`; the engraving itself
  (melee `char/melee/extra`) is untouched; its icon `minecraft:arrow` (`engravings/register:62`) is just an icon.

### 1.3 Edit (hand files)
| file:line | change |
|---|---|
| `char/setup:2` | comment "bow(활) … 활 = char/bow/*" |
| `char/setup:5` | drop `function rlk:char/yoimiya/def` |
| `char/setup:15` | comment example `start_char … "yoimiya"` → another id |
| `char/load_cur:5-10` | drop the `weaponType:"bow"` → `#wType 2` line (`:7`) and `#bowAim`/`#bowFull` (`:9-10`); comment `:5` |
| `char/reg_items:3,5,9` | `pool` starts with skirk (`:3` `[{id:"yoimiya"…}]` → `[]` then the skirk append at `:7` stays), drop `:5`, codex list `:9` without `"char_yoimiya"` |
| `char/tick:12-15` | drop yoimiya tick (`:12`), bow tick (`:14`) and the `#bowChg` reset (`:15`) |
| `char/cast_skill:19` · `char/burst_go:12` | drop the `#charN 2` lines |
| `char/player_init:22-43,89,90,99` | drop the "활 · 요이미야" block (`:23-43`: bow*/yoi* scores, `#bowChg`, sidebar resets 염초정화/소매불/염초화살), `aurEnd` reset `:89`, `kill rlk_iq iqK=4` `:90`, `rlk:bow_aim` remove `:99`. **Keep `:44 kill @e[tag=rlk_arrow]`** (Ronova's projectiles) |
| `char/burst_wind:10` · `room/fall/player:10` | drop `bowT … char/bow/cancel` |
| `combat/on_attack:43-44,49` | drop the bow `release` / `na` lines; `:45` (`unless #wType 2..`) still means "melee" for {1,3} — may simplify to `if #wType 1` |
| `combat/rclick_do:12-13` | `:12` drop `unless #wType 2`; delete `:13` (`bow/rdash`); comment `:2` |
| `player/f_key:7-9` | drop the bow aim toggle lines (`:8-9`) and comment |
| `player/hotbar/fix_attack:1-4` | always `char/weapon_item`; comment |
| `combat/apply:86` · `combat/apply_mods:6-7` · `room/fall/mob_reward:5` | drop the `#charN 2` (유금화광) lines |
| `items/q/run:4` | drop `iqK 4 → char/yoimiya/aur_boom` (unknown kinds are killed at `:6` anyway) |
| `items/hook/stat_buffs:39-40` | drop 소매불 passive |
| `codex/labels:104` | drop `lab.char_yoimiya` |
| `tick.mcfunction:31` | comment "화살(활 캐릭터)" → "투사체(로노바 …)"; keep `:32` |
| `mob/tick:5` · `view/tick:27-29` | `#bowChg` gates become unconditional (the shield summon/tp/msync) |
| `view/move:8,77-78` · `view/slow:5-6` | drop the `bowT` aim slow / hand-copy guards |
| `view/hand_wrap:14-15,18-23` · `view/av_unwrap:8,10-12` | drop `minecraft:bow` / `rlk:bow_pull_*` lines |
| `player/swing/tick:6` · `player/swing/jump:2` | comments mentioning 활 |
| `load:346-358,414` | bow objectives (`bowT … bowPm`, `bowQo`) |
| `load:367-373` | `yoiSk yoiPcCd yoiPcN yoiP yoiPT aurEnd` |
| `load:792-805` | `#bowCdN #bowQGap #bowT1 #bowTap #bowSlow`, `#yoi*` constants |
| `load:361-365` | keep `aKind aEl aSub aLife aIcd` (Ronova uses them) |
| `uninstall:138,153-165,508-512` | keep one release for old worlds, or move them into the migration (1.6) |

Generated output: `tools/build_mboss_core.py:3974` (`PX_DB` row `aurEnd`) → regenerate core: `mboss/px/db.mcfunction:5`
loses the line and `mboss/px/db/aurend.mcfunction` disappears (core deletes its stale files, README 0-4). Nothing else
generated mentions the bow.

### 1.4 Character select · codex · lobby · items · help · engravings
- Character select is data-driven: `char/select` + `{id:"help"}` (`char/select_help`) and the lobby's 「캐릭터 바꾸기」
  (`lobby/char` = codex tab 5) read `rlk:codex chars` / `rlk:chars registry` → fixed by `char/reg_items` + `char/setup`.
  `items/give|drop {id:"help"}` list characters from the same list.
- Level-up character offer: `lvup/roll_char` draws from `rlk:chars pool` (fixed by `reg_items:3`).
- Items "tied to her": the character item `char_yoimiya` (player head, `char/reg_item` macro) — gone with the registry
  entry. No regular item, shop entry, mob drop or engraving references bows or Yoimiya (`grep` of items/ engravings/
  items.md engravings.md: only Demonomicon's "서리 화살", unrelated).
- Legacy bow item shim: `player/tick:14-15` + `items/migrate_p` · `items/migrate_loop` replace an old item id
  `favonius_bow` (페보니우스 활 → 비전). Harmless (1 `if items` per tick); remove only if pre-10-15 saves no longer matter.
- Lobby: nothing Yoimiya-specific (`lobby/ct/*` tutorial reads `rlk:chars cur`).
- Engravings: none tied to bows (see 1.2 for 연격's bow branch).

### 1.5 README · docs · RP · tests · sims
- README rows: `34` (8명 list), `85` (0-3 table "캐릭터 8명"), `483-487` (0-9 open question about the bow aimed shot
  counting as a normal attack — delete), `699` (RP "당긴 활" model note), `737-739` (swing table: 요이미야 row + "활의 조준
  사격" in `737`), `1074-1075` (§11: 8명 list, `bow`(요이미야), `#wType` `bow` 2, "2 는 char/bow/*"), `1087` (Ronova's
  "화살 틀 `char/bow/arrow_*`"), `1638` (aurEnd audit row), `1985` (Arlecchino normal-attack list: "요이미야의 평타 화살 …
  세지 않음: 활의 조준 / 충전 사격"). Release-time: 0-1 / 0-10 / RP README version lines.
- RP (git-external, `rlk_hud_resourcepack.zip`, not in this container — check against the user's zip):
  `assets/rlk/textures/skin/yoimiya.png` (profile `rlk:skin/yoimiya`, `char/yoimiya/def:9`), item models
  `rlk:bow_pull_0..2` (avatar pull, `char/bow/av_pull`), `rlk:h/bow`, `rlk:h/bow_pull_0..2` (hand wrap,
  `view/hand_wrap:14-23`, `char/bow/hand_pull`). All hand-made (no generator writes them). Then `rplint` + `atlas_px`
  (saving is small, a 64×64 skin if `skin/` is in the item atlas).
- Tests that break: `tools/dev/sim/ar/tests/test_arlecchino.py:356-357` read `char/bow/na_shot` / `char/bow/release`
  (FileNotFoundError once deleted) → replace with Ronova / Clorinde rows; `az/tests_cm/test_px.py:311,461-469` list
  `aurEnd` in the px/db audit → drop it. Stale but harmless: `ar/s3/lib/knsim.py:252-253` + `test_arlecchino.py:324`
  attack kinds `bow_na` / `bow_aim` (abstract flag sets; rename to `ranged_na` or drop `bow_aim`), `hr/tests/test_hwamu.py:904`
  sets `#bowChg 1` to skip the avatar-shield lines of `view/tick` — once those lines lose the gate the sim runs them
  (summon / tp: supported); re-run `test_hwamu view` to confirm.
- Balance probes use a "ranged walk **bow**" policy as the generic ranged player (`hr/review/bal/*`, `ar/review/bal/analyze5.py:45`,
  `mb3/fgfix/sim`, `tele/fg/sim`, `ap/balance/azfair_core.py:106`): historical records; a new ranged baseline (Ronova /
  Clorinde) belongs to the balance work, not here. Plan docs mentioning Yoimiya (`navia/plan.md:223`, `ar/PLAN.md:280`,
  `az/understand/*`) are history — leave.

### 1.6 Saved-world migration (a player saved as 요이미야 loads as 루미네)
Why it is needed: `char/load_cur:2` does `cur set from registry.$(id)`; with `registry.yoimiya` gone that command fails
and `cur` keeps the **old full Yoimiya compound** (`n:2`, `weaponType:"bow"`) → `#charN 2`, `#wType 2` with no handlers.
1. `char/setup`, before `load_cur` (`:12`): `execute if data storage rlk:chars cur{id:"yoimiya"} run data modify storage
   rlk:chars cur set value {id:"lumine"}` + set a flag `rlk:mig yoi 1b`; and
   `execute if data storage rlk:config {start_char:"yoimiya"} run data modify storage rlk:config start_char set value "lumine"`.
2. Player side, once (like `player/tick:15` favonius): `execute if data storage rlk:mig {yoi:1b} run function
   rlk:char/migrate_yoi` → `function rlk:char/select {id:"lumine"}` (clears `rlk_ui`/`rlk_char` items — needed because a
   server restart runs load before the player joins, so `load_cur`'s `clear @a` misses the old 활 weapon — re-inits, reskins
   the avatar), plus what `player_init` no longer does: `attribute @s minecraft:movement_speed modifier remove rlk:bow_aim`,
   `kill @e[tag=rlk_arrow,scores={aKind=1..6}]`, reset sidebar `염초정화 · 소매불 · 염초화살`, then `data remove storage rlk:mig yoi`.
3. Pending picks: `rlk:lvpick choices` (kept across exits, `lvup/toggle:22`) and `rlk:lvpick dropq` may hold
   `"char_yoimiya"` (string lists: filter with the `items/migrate_loop` pattern, or empty `choices` → one free reroll).
4. Ground drops: a dropped character item is an `item` entity `rlk_ditem` with `custom_data.rlk_ditem.id:"char_yoimiya"` +
   group entities and `rlk:ditems records.k<dgid>` → kill the group (`ditem/kill_group {dg}`) once at load.
5. Optional cleanup in the same migration: `scoreboard objectives remove` the bow*/yoi*/aurEnd objectives,
   `data remove storage rlk:codex lab.char_yoimiya`. Mobs' `aurEnd` and `rlk_iq` iqK 4 markers are harmless (q/run kills them).
- Test (psim harness, 4.1, runs `rlk:load` in 0.8 s): put the old compound in `rlk:chars cur`, `start_char "yoimiya"`,
  `choices ["char_yoimiya", …]`, a bow item in hotbar.0 and the `rlk:bow_aim` modifier → run load + 2 player ticks →
  `cur.id lumine`, `#charN 1`, `#wType 1`, hotbar.0 = Lumine's weapon, choices without `char_yoimiya`, no `rlk:bow_aim`.

**Size**: delete ≈ 36 files / ≈ 380 lines; edit ≈ 30 hand files (≈ 90 lines) + 1 generator row; migration ≈ 2 new
functions (≈ 25 lines) + 3 lines; 2 test fixes; README ≈ 10 rows; RP 7 files (manual). ~½ day incl. loadcheck/rplint.

---------------------------------------------------------------------------------------------------------------------

## 2. Remove the first-person mode and the shoulder view (F5 위쪽 시점 stays)

### 2.1 Decide first: developer mode
`view/tick:18-20`: the view is "effective" only if `#on view 1` **and not `devMode`**; otherwise `view/fps_tick` (player
= `rlk_body`, `view/teardown` of the avatar). Developer mode (`/function rlk:dev/toggle`, README 9) relies on this
no-avatar path for free building. Recommendation: **keep `fps_tick` + `teardown` as the devMode-only path** (and for
`uninstall:58`), remove only the player-facing first-person / shoulder modes. Then every "body = player" branch below
stays reachable (devMode) and need not be touched. If devMode should also use F5, the list in 2.4 becomes dead code.

### 2.2 view/** (hand files, `F:view/`)
| what | files |
|---|---|
| mode switch / commands → delete | `mode` (5) `mode_do` (6) `mode_help` (5) `on` (6) `off` (4) `ride` (2, alias of `mode {m:2}`) |
| shoulder camera → delete | `rot` (46) `rot_lead` (5) `cam_go` (1) `cam_step` (12) `cam_put` (5) `cam_y` (25) `cam_calc` (18) `dur_set` (3) `dur_set2` (1) `set` (5) `tune` (6) `tune_apply` (3) — 158 lines with the mode files |
| `view/tick:17-20` | `#eff` = `unless devMode` (no `#on`); `:38-39` → always `ride_tick` (drop `rot`) |
| `view/spawn:19` · `view/sync:5` | the `rlk_camv` item_display (shoulder camera mount) — drop |
| `view/burst_camera_apply:1-3` | drop `cam_calc`; keep `ride_apply` |
| `view/burst_camera_tick:12` | drop `unless #on view` (devMode line `:13` covers the off case) |
| `view/rays:1-11` | keep only the 3rd-person ray lengths (27/21/23/28/27) as constants |
| `view/hold:8` · `view/ttl_blank:2-3` | drop `#on`/`#vmode` conditions |
| keep | `ride_tick` `seat_new` `ride_mount` `ride_off` `ride_apply(2)` `ride_set` `hand_wrap` `av_unwrap` `xhair` `sel_xhair` `move` `turn(_go)` `aim(_step)` `face_aim` `face_lock` `dash_dir` `spawn(2)` `av_tick` `av_hurt` `slow` `sprint_fov` `mob_aggro` `mob_join` `stop_h` `sync` `fresh` `teardown` `fps_tick`(devMode) `map_*` `menu_do` `input_*` `shield_*` `burst_camera_*` `reskin` |

### 2.3 Lobby settings
- `lobby/build:159` 「시점」 button (k 20) — drop; `:147` desc "시점 · 카메라" → "카메라". Bump the build version
  `lobby/build:175` + `lobby/tick:3` (`built:11` → 12) so saved worlds rebuild the lobby without the button.
- `lobby/act:11,13,15,16` (k 20/22/24/25) and `lobby/set/s20` (11), `s22` (7), `s24` (6), `s25` (6) — delete (22/24/25
  have no button in `build` already; dead).
- `lobby/set/labels:3-5,9-10,14-21,24-27` — drop view / side / smooth / lead labels.
- `lobby/set/cam:1-10` — drop the shoulder `cam.*` part, keep `:11-18` (F5 `ride.d` / `ride.s`). Note: the comment
  `:11` says 2.5/3.5/4.5 b while README 2443 says 3.5/4.5/6 — fix the README to the code.

### 2.4 Other systems that branch on `#on view` / `#vmode` / the view kind
- `load:1203-1206` (`#on` kept if 0..1, `#vmode 2`), `:1216-1224` (`rlk:view cam`/`opt`/`optv`, `cam_calc`,
  `tune_apply`). Set `#on view 1` unconditionally (or delete `#on` after the guardian change below).
- `lvup/pick_sub:13-15` → only the 「웅크리기(Shift) 로 선택」 line (`:14-15` Shift+F variants are for first person).
- `lvup/tick:8-10` → sneak tap always (drop `#on`/`#vmode`).
- **Generated**: `mboss/guardian/p/pull/scr_end:6` tests `#on view 1 … #vmode view 2` (from
  `tools/mboss_guardian/p34.py:716`). Either keep `#on view 1` / `#vmode view 2` as constants in `load` (no regeneration —
  recommended) or edit the generator and regenerate guardian (byte-identity of guardian output changes).
- `player/level/up:9` chat text "(1인칭에서는 무기를 들고 Shift + F …)" → drop the parenthesis.
- Selection-space UI texts "Shift + F" (`lvup/ui/draw:17`, `invd/draw:76`) stay (Shift+F still exits there: not riding).

### 2.5 First-person adaptations (all reachable only with no avatar = devMode under 2.1)
Engine "body = player" branches (keep under 2.1): `combat/on_attack:23,28,35`, `combat/rclick_do:11`,
`combat/atkblock_manage:8`, `combat/apply:67-68`, `cm/aggro:5`, `mob/unstun:5-7`, `char/ronova/mob_back:3-4`,
`player/vanilla_hit:2`, `player/dash_dir:15`, `player/swing/tick:26-33,38-40` (jump modifier `rlk:swing_hold`),
`player/swing/jump`, `char/skirk/dash_start:1` (1st-person speed modifier), `char/burst_wind:11`,
`char/arlecchino/skill:4` · `skill_dash:10-11` · `motion/control/cancel:4` (invisibility), `char/nefer/dash_step:11-14`,
`char/navia/sh_tick:2`, `char/ronova/ec_tick:2` · `cat_tick:2` · `na:24` · `echo_fire:13`, `char/nefer/cat_tick:2` ·
`dw_tick:2`, `view/map_open:28-30`, `char/motion/sheath/tick:16` + the clip starts (`char/motion/clips/**/start`, 48
files, generated by `build_player_rig.mjs`), `char/motion/{tick,stop,combat_tick}`.
Visual first-person adaptations (only devMode would see them; leave generated ones alone):
- Navia's block umbrella gun / first-person muzzle: `char/navia/tap:5`, `tick:20`, `aim_start:11`, `fire:32,37`,
  `muzzle_fp`; rig fx flag `#pmFxFP` (47 files: `char/motion/**` from `tools/build_player_rig.mjs:307,423`, `fx/nv/card`
  from `tools/build_navia_fx_cards.py:481`); quick stow in first person (`tools/build_player_locomotion.mjs:223-242`).
- Scarlet: `FIRST_PERSON = 'if entity @a[tag=rlk_body]'` anchors (`tools/mboss_scarlet/seq.py:197`, `p_ghost.py:71`,
  `shield.py:37`) → 14 lines in 6 files under `boss/scarlet/`; tests `hr/tests/test_kit.py:1116-1145` check the
  first-person cards.
- Butterfly: eye-level cards suppressed when no avatar (`tools/mboss_butterfly/seq_b.py:198-228`, `core.py:920`) →
  `mboss/butterfly/wx/cure/*`, `wx/coc/fx`.
- Guardian: cage cubes below eye height in first person (`tools/mboss_guardian/p34.py:417,518`).
- Azhdaha: a first-person cue only (`tools/mboss_azhdaha/geo_b.py:305`), no branch.
- Items: `items/proc/hw_slash_q:40-42` vignette is view-agnostic (vBig). None else.
Recommendation: do not regenerate bosses for this; mark these as devMode-only in README.

### 2.6 README
§13 (`2437-2476`): retitle "13. 시점 (`view/`) — F5 위쪽 시점", drop `2438` mode sentence, `2448` "시점 버튼 … 숄더뷰 코드는
남아 있음", the whole §13-1 (`2456-2470`) except the avatar notes of "구조" (`2471-2476`, rewrite the camera line for the
seat). Also `95` (0-3 table "1인칭 · 숄더뷰 · F5"), `732-736`, `746-751` (swing: 1인칭 rows and "1인칭에서 걷기를 늦추지 않는
이유" → devMode note or delete), 9절 help table row `rlk:view/mode {m:"help"}` (`990`) and the `view/mode_do` mention in `997`, `537,540,549` (0-9 Scarlet
first-person checks), `2540-2541`, `2589`, `2600-2601`, `2626` (Navia / sheath first-person notes → "devMode (no avatar)").

### 2.7 Tests
`hr/tests/test_hwamu.py:885-960` (`view_world(on=0)` first person, `vmode=1` shoulder cases; the static check
`first_ret` looks for `return run function rlk:view/fps_tick` — keep that line under 2.1 or update), `hr/tests/test_special_hr.py:800-801`
(sets `#on`/`#vmode`: fine as constants). Most sims run "first person" worlds (player = `rlk_body`) because they don't
model the avatar — unaffected.

### 2.8 Migration of saved players into F5
- `#on view 0` saved by a first-person player survives `load:1204` today → set `#on view 1` unconditionally (or drop it).
- The rest heals by itself: the first tick after load runs `view/fresh` → `teardown` (`#vFresh 1`, `load:1208`), then
  `view/tick:24` spawns the avatar and `:25` removes `rlk_body` from the player; `kill @e[tag=rlk_view]` at `load:1230`
  removes a leftover `rlk_camv`; `ride_off` dismounts. `#vmode` is forced to 2 at every load already.
- First-person modifiers: `rlk:swing_hold` (jump) is recomputed every tick and removed when the body is the avatar
  (`player/swing/tick:31-34`) — if that branch is ever deleted, keep a one-shot remove like `player/swing/legacy`.
- Lobby button: version bump (2.3). Optional: `data remove storage rlk:view cam` / `opt` / `optv` / `st` / `pr` / `tr`.

### 2.9 What the client's own F5 key still does
The server cannot set or read the client perspective. F5 still cycles all three vanilla views:
- **back 3rd person** — the intended view (distance = the seat's `camera_distance`, `view/ride_apply2`);
- **first person** — the camera sits at the tiny (scale 0.0625) player's eyes on the seat, i.e. ≈ 0.25–1 b above the
  avatar's head (`ride.s`); the avatar is not visible, the hand shows the real weapon model (`rlk:h/*` renders the
  original in first person), aiming still works (all aim rays start at the player's eyes: `view/aim`), and the vanilla
  crosshair plus the pack's title crosshair overlap. A playable "pseudo first person from above the head";
- **front 3rd person** — looks back at the seat; useless but harmless.
Nothing to block; `seat_new` already tells the player to press F5 (`key.togglePerspective`).

**Size**: delete 18 view files (158 lines) + 4 lobby files (30 lines); edit ≈ 15 hand files (≈ 45 lines); README §13 /
§13-1 rewrite + ≈ 12 rows; 1–2 test edits; no generator change if `#on`/`#vmode` stay as constants. ~½ day.

---------------------------------------------------------------------------------------------------------------------

## 3. 「고를 아이템 N개 …」 must not show in combat

### 3.1 Where it comes from
`player/tick:66` → `lvup/tick:16` → `lvup/pick_sub` every tick: `#ps 1` when `pkPending ≥ 1`, not in the selection
space, alive (`:3`); refreshed every 20 ticks with `title times 0 30 5` + subtitle (`:12-15`) + `view/ttl_blank`
(the F5 crosshair as the title); it waits while another line is up (`ttlT`, `:5`) and clears once when `#ps` drops (`:7`).
Nothing looks at combat, so kills that level you up mid-fight bring the line back every second.

### 3.2 The pack's combat states
| state | set | cleared | covers |
|---|---|---|---|
| room combat `#combat room = zid` (with `#active room 1`) | `room/combat_start:2` (zone kinds 1 and 9: `room/zone_enter:7,10`) | `room/combat_clear:3`, `room/clear:17`, `room/wipe:5` | combat rooms, **나루카미** (boss zone 9, `boss/raiden/spawn` tags `rlk_zmob`), and through the same call every registry boss: mid boss `mboss/gate:10` (zone 15), chapter bosses `mboss/cb/g/<id>:8`, special bosses `mboss/sp/g/<id>:13`; test commands (`mboss/test/*_ch`, `boss/raiden/test/start`) set `#active room 1` and use the same flow |
| boss engine live `#mbLive mb 1` | `mboss/start_go:5`, `mboss/reload:2` | `mboss/cleanup_fight:17`, `mboss/main:10` | mid / chapter / special bosses from the fight start (incl. intro `#mbSt 0`) until cleanup; a safety net for boss fights that are not in a room |
The existing refusals use the first form: `lvup/toggle:9` 「전투 중에는 이동할 수 없습니다」, `codex/open:7`, `invd/open:7`,
`view/map_open:8`.

### 3.3 Gate (2 lines, `lvup/pick_sub` after `:3`)
```
execute if score #active room matches 1 if score #combat room matches 1.. run scoreboard players set #ps tmp 0
execute if score #mbLive mb matches 1 run scoreboard players set #ps tmp 0
```
On the first combat tick `#ps 0` with `pkSubT ≥ 1` → `:7 title @s clear` removes a line already on screen (the room's
「적 출현」 `room/msg` sets `ttlT` 38 first, so usually the line is just replaced and `pkSubT` is 0). When combat ends the
line returns after 「구역 정리」 (`ttlT`). Optional polish: in the combat case send `title @s subtitle ""` instead of
`clear` so the F5 crosshair title is not blanked for up to 10 ticks (`view/ride_tick:16-18` resends it).
Also consider the level-up chat line `player/level/up:9` (chat, not the subtitle; it already says 「전투 중에는 불가」).

### 3.4 Test (prototype run in `cb/misc/perf/picksub.py`)
Real `lvup/pick_sub` with `view/ttl_blank` stubbed, `pkPending 2`, titles logged per tick; script: combat starts at
t 30 (`#combat room 3`), ends at t 70, `#mbLive 1` at t 90. Today: subtitle at 1, 21, 41, 61, 81, 101 (never cleared).
With the gate: subtitle at 1, 21, 70; `title clear` at 30 and 90; nothing in 30–69 and from 90. For the suite: same
script on srsim (`tools/dev/sim/hr/sr/srsim.py` logs `title`), plus: no subtitle while `pkMode ≥ 1`, while dead, while
`ttlT ≥ 1`; the subtitle comes back ≤ 20 ticks after `#combat 0`; a level-up during combat shows nothing until the clear.
**Size**: 2 lines + 1 comment; test ≈ 60 lines.

---------------------------------------------------------------------------------------------------------------------

## 4. Late-game TPS drop on combat entry

### 4.1 Measurement setup (`cb/misc/perf/`, scratch, ≈ 120 KB)
- `psim.py`: a copy of `tools/dev/sim/ar/tests/lib/mcsim.py` (unset scores read as 0, `\` line continuation,
  `reset *`) + srsim's real SNBT + **a player inventory model** (slots, `if|unless items`, `clear`, `item replace|modify`,
  `give`, `store result … if items` counts) that fires the `inventory_changed` advancement (`rlk:player/inv/dirty`)
  right after any command that changes a player slot — as the game does (ItemCommands / clear / give call
  `containerMenu.broadcastChanges()`, the trigger fires, the reward function is queued right after the running command)
  — + per-function inclusive / self command counts and macro instantiations / substituted macro lines per function.
- `scen.py`: runs the **real `rlk:load`** (all 95 items, engravings, tune), gives items through the real
  `items/give`, then per tick: F5 `view/ride_tick` consumable lines (`:23-25`, view/tick runs before player/tick) →
  the **real `rlk:player/tick`**. Inventories: small = 3 commons; late = 18 items (invCap max; 2 mythic weapons, legendary
  weapons/books, mythic trinkets, ★★★ on all but one). "Combat churn" = the skill goes on cooldown (18 s) when ready and
  energy +3 pt every 15 ticks until the burst is cast — what combat does to the hotbar. (30 *different* items cannot be
  held: `invCap` ≤ 18; per-item scaling below.)
- `pass.py` one dirty pass broken down; `hit.py` per-hit cost through the real `combat/apply`; `fdash.py` one F press;
  `fix1.py` / `fixA.py` the fixes below; `picksub.py` topic 3.

### 4.2 Results (commands per tick, player side)
| scenario | avg | p50 | max | `equip_scan` runs |
|---|---|---|---|---|
| small(3) out of combat | 688 | 669 | 8 691 | 0.20/s (10-s fallback) |
| small(3) combat churn | **3 122** | 669 | 8 717 | **6.2/s** |
| late(18 ★★★) out of combat | 739 | 682 | 12 797 | 0.20/s |
| late(18 ★★★) combat churn | **4 402** | 682 | 12 827 | **6.2/s** |

Per function, late combat churn: `items/equip_scan` 2 890/tick (of which `engravings/scan` 1 630, `engravings/info_build`
1 492, `items/scan_loop` 1 095), `player/inv/manage` 896/tick (`inv/sync` 762, `collect_loop` 587); everything else ≈ the
idle numbers (`items/hook/tick_player` 189, `stat_light` 89, `player/hotbar/tick` 54, `update_item` 52, `char/tick` 39).

**One dirty pass** (`player/inv/manage` + `items/equip_scan`), run twice per event (`invDirty 2`, `player/tick:21-32`):
| part | small(3) | late(18) |
|---|---|---|
| `inv/sync` → `collect_loop` over **all 95 registry ids** (`collect_check` → `order_count` → `order_count2`, 3 macros/id) | 2 058 | 1 893 |
| `inv/sync` → `order_rebuild` (held) | 94 | 559 |
| `inv/place_items` (+ frame, sweep) | 213 | 618 |
| `equip_scan` → `scan_loop` over **all 95 ids** (`scan_fetch` + `scan_count` macros/id) | 1 777 | 3 532 |
| … of which `scan_add_prep` + `scan_add` (held; `scan_add` = 100-line macro, 20 macro lines) | 348 | 2 088 |
| `items/slate/scan` | 0 | 377 |
| `engravings/scan` per-item loop | 65 | 380 |
| `engravings/info_build` 12-pass sort (`info_pass` × 12, 288 `info_pass_one` macro calls) | 3 202 | 3 232 |
| `engravings/info_build` groups + items | 430 | 1 509 |
| `stat_light` | 122 | 129 |
| **total** | **8 117** | **12 402** |
| macro instantiations / macro lines re-parsed | 842 / 1 508 | 1 082 / 2 221 |
Macro functions re-parse their `$` lines per new argument set (the game caches only the last few instantiations per
function); `scan_count`, `collect_check`, `order_count(2)`, `scan_fetch` see 95 different ids every pass, `info_pass_one`
24 ids × 12, `scan_add` one per held item — all cache misses. So a pass costs ~12 k commands plus ~2 k command parses:
two passes on consecutive ticks match the reported 118 ms max, a few per second the 31 ms average.

Per hit (`hit.py`, real `combat/apply` + `combat/on_hit`): 301 (small) vs 357 (late) commands for an elemental hit,
217 vs 258 physical — item hooks add ~+19 %. Per-tick hooks: +~50 commands (+7 %). **Neither explains the jump.**

### 4.3 Root cause: combat makes the F5 hotbar re-arm the inventory scan every second
1. In combat the skill item (cooldown seconds as the stack count) is rebuilt every second and the burst item on every
   energy point / cooldown second (`char/hotbar:20-29,38-44` → `char/skill_item_cd`, `char/burst_item(_cd|_ready)`).
   These run inside `player/tick`, whose own inventory events are consumed at `player/tick:98` — fine so far.
2. The rebuilt items lack `minecraft:consumable` (and a rebuilt weapon lacks the `rlk:h/*` wrap). The **next tick**
   `view/ride_tick:23-25` (and `view/hand_wrap`) add it with `item modify` — in `view/tick`, which runs **before**
   `player/tick` (`tick.mcfunction:23,25`) → `inventory_changed` → `invEvt 1` → `player/tick:24` → `invDirty 2` → a full
   `inv/manage` + `equip_scan` on this tick and the next.
3. An F press (the pack's dash, `player/hotbar/tick:9-10` → `player/f_key`) swaps the weapon into the off hand: a player
   action, so its `inventory_changed` lands between ticks → dirty (2 passes); `fix_attack` rebuilds the weapon, and the
   next tick's consumable / hand wrap → dirty again: **3 full passes per dash** (`fdash.py`: late 41 028 commands over 6
   ticks, ticks 1–3 ≈ 13 k each).
Out of combat the skill is ready and energy full → no rebuilds → only the 10-s fallback (`player/tick:26-28`). The pass
cost grows with held items (+~286 commands and ~+48 re-parsed macro lines per item per pass), so late runs feel it most.
(F5 became the default view; first person never ran `ride_tick`, which is why the old consume window looked sufficient.)

### 4.4 Fixes (behaviour-preserving) and measured / estimated savings
**A1 — finish the hotbar items inside the consume window** (root cause, ~6 lines): run the consumable lines
(`view/ride_tick:23-25`) and `view/hand_wrap` right after the rebuild — e.g. at the end of `player/hotbar/place` (or in
`char/hotbar` / `fix_attack` when `#mk 1`), gated like ride_tick (`if entity @e[tag=rlk_vseat]` or `unless devMode`) — or
bake `minecraft:consumable={consume_seconds:1000000f,animation:"none",sound:"minecraft:intentionally_empty",has_consume_particles:false}`
into `char/weapon_item`, `skill_item*`, `burst_item*`. ride_tick keeps its lines as a no-op safety net.
**A2 — an F swap of a UI item is not an inventory edit** (1 line): `player/tick:24` →
`execute if score @s invEvt matches 1.. unless items entity @s weapon.offhand *[minecraft:custom_data~{rlk_ui:{}}] run scoreboard players set @s invDirty 2`
(the swapped UI item is still in the off hand at line 24; `hotbar/tick` returns it at `:10`; real rlk-item moves are
still caught by the count probe `:18-22` and by later events). Edge: F pressed over a UI slot in the inventory screen
while an rlk item sits in the off hand moves that rlk item into `hotbar.*` — the probe (`inventory.*` + `hotbar.*`, off
hand excluded) sees the count rise and marks the pass at `:21` anyway, so nothing is lost.
Measured (`fixA.py`): F-dash 41 028 → **4 691** commands over 6 ticks (0 passes; weapon back in hotbar.0 with
consumable + `rlk:h/iron_sword`); late combat churn **4 402 → 799** avg (−82 %), small 3 122 → 748; `equip_scan` 6.2/s →
0.2/s (= idle). A1 alone (`fix1.py`): late 4 402 → 748 avg without F-dashes.

Optional (A3): the advancement `inv_changed` could carry an item condition (only fire when the changed stack has
`custom_data.rlk`) — broader, but it also drops events for the first-row info items (`player/inv/frame` then waits for the
10-s fallback) — not behaviour-preserving without a second criterion; A1 + A2 are enough.

**B — make the remaining dirty passes cheap** (item pickups, swaps, room changes, the 10-s fallback). Estimates from the
measured parts (late 12 402 → ≈ 4 900 commands, macro instantiations 1 082 → ≈ 360, re-parsed lines 2 221 → ≈ 600;
small 8 117 → ≈ 1 450):
- **B1 items sync fast path** (`player/inv/sync:9-10`): after `order_rebuild_loop`, if the count of physical rlk items
  (`if items … inventory.*|hotbar.* *[custom_data~{rlk:{}}]`) equals the length of `neworder`, skip `collect_loop` —
  every physical item is already matched (`order_keep` consumed one `pcnt` per entry), so collect could add nothing.
  Saves ≈ 1 900–2 060 commands, 285 macro instantiations (665 lines) per pass.
- **B2 scan held ids, not the registry** (`items/equip_scan:25-26`): iterate the deduped `rlk:pinv order` and zero the
  `it_<id>` of ids held at the previous scan (keep that list); keep the full-registry loop in devMode (manage is skipped
  there, the inventory may hold unordered items). Saves ≈ 1 150–1 340 commands, ≈ 154–184 macro instantiations.
- **B3 macro-free `scan_add`** (`items/scan_add_prep` + `scan_add`): replace the 100-line macro (20 `$` lines, one
  instantiation per held item) by 20 `execute if data storage rlk:scan def.stats.<k> run function rlk:items/scan_s/<k>`
  lines, each body `execute store result score #v tmp run data get storage rlk:scan def.stats.<k>` + the same 4
  operations; absent stats contributed `(0·f+500)/1000 = 0` before, so sums are identical. Late: 2 088 → ≈ 750, −360
  re-parsed lines.
- **B4 single-pass engraving sort** (`engravings/info_build:6-42`): one pass over the 24 engravings appends `{id,n}` to
  bucket `b<min(n,12)>` (registry order kept inside a bucket = today's tie order; 0 is skipped as today), then append
  `b12[] … b1[]` into `sorted`. 3 232 → ≈ 160 commands, 288 → 24 macro calls (0 if unrolled per engraving).
- **B5 (optional) skip identical rebuilds**: keep a signature (order + `enh` + `mir` + `engDev`) and skip
  `engravings/info_build` (and the scan) when unchanged — the classic `store success … data modify storage … set from`
  compare. Saves the remaining ≈ 1 500 (info items) on passes that change nothing; needs care (devMode, load).
Out of scope here but measured: per-hit item hooks (+56 commands at 18 items) and per-tick hooks (+~50) are small.

### 4.5 How to re-run
```
cd /tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/cb/misc/perf
python3 scen.py [dp]     # 4.2 tables (≈ 75 s)      python3 pass.py   # one pass by part
python3 fdash.py; python3 fixA.py; python3 fix1.py; python3 hit.py; python3 picksub.py
```
Model limits: entities, mobs and the avatar are not simulated (player = `rlk_body`, the F5 step is the three ride_tick
lines + hand_wrap); `health_tick` / `hunger` read vanilla NBT the sim lacks (errors counted, ~15 commands/tick missing);
command counts, not milliseconds — the macro re-parse counts are the proxy for parse cost. Wave spawns (one-off) were not
modelled. In-game check after A1 + A2: `/debug start` or the F3 tick graph during a late-run fight with F-dashes.

**Size**: A1 + A2 ≈ 7 lines (+ a test in the psim style: combat churn keeps `equip_scan` at the fallback rate; F-dash
→ 0 passes). B1–B4 ≈ 4 small new functions + ≈ 60 changed lines in `player/inv/sync`, `items/equip_scan`, `items/scan_*`,
`engravings/info_build`; verify with a before/after `scan` that `eq*`, `it_*`, `engN`, `rlk:eng sorted` and the info
items are identical for several inventories (the psim harness can diff them).
