# Chapter-boss integration study: Azhdaha (chapter 1), the Apep Warden (chapter 3), Raiden (the rest)

This is a read-only study. Nothing in the repo or in any worktree was changed. The only file written besides this one is the
calculator `S:az/understand/chapter_work/calc.py`, which produced the numbers in §5.

## Path shorthand

| short | meaning |
|---|---|
| `DP` | `/home/user/rlk/roguelike`, HEAD `7a6dc4f` on branch `claude/exciting-pascal-ek1vuy` (Guardian + butterfly). This is the working "main" line. Git `main` itself (`19ed248`) is an ancestor and much older. |
| `FG` | `S:mb3/wt_fg/roguelike`, branch `wip/fg` `fde9db7` (the newest framework, with the field generator). Read only. |
| `F:x/y` | `DP/data/rlk/function/x/y.mcfunction`. The shared files cited here are byte-identical in `FG`, except `tick` (+4 low-gravity lines, so `FG` tick lines are `DP` + 4), `load` (the build-stamp line) and `view/move`. |
| `T:` | `DP/tools/` |
| `core:N` | `FG/tools/build_mboss_core.py` line N. The `DP` copy is older; its line numbers are given as `dpcore:N` where they are cited. |
| `enc:N` | `T:build_raiden_encounter.py` (generates `F:boss/raiden/**` except death and the camera) |
| `cin:N` | `T:build_raiden_cinematic.py` (generates `F:boss/raiden/death/*` and the camera) |
| `S:` | `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad` |
| `t` | ticks (20/s) |
| `b` | blocks |

---------------------------------------------------------------------------------------------------

## 0. Short answers

1. **Lifecycle today.** Every chapter ends the same way:
   - map index 4 → the white end zone offers one "보스전" object;
   - its click builds the Raiden boss map: a foyer, then a 23-b-radius circle at (0,201,0) inside the dungeon square;
   - entering the circle locks the doors and spawns Raiden 1 s later;
   - his kill pays boss gold ×15 × chapter, 2 sapphires and 40 XP;
   - after a 48 t collapse the zone clears and a "다음 챕터" nether-star object appears at the arena centre.

   Every hook point is in §1.
2. **Routing.** Today there is no routing: `F:room/pick/boss:3` always loads the Raiden layout and `F:room/boss_spawn:2-3` always spawns Raiden. The cleanest switch is:
   - decide the boss once, in `room/pick/boss`, from `#chapter` (1 → `azhdaha`, 3 → `apep`, else Raiden);
   - store it as the zone's `data.boss_id`;
   - route `room/boss_spawn` (and three other `boss_id` checks) on that id, so tests can force any boss in any chapter.

   Test commands for all three bosses are in §2.3.
3. **Recommendation: build both bosses on the mid-boss framework, extended with a "chapter" mode.** Do not build them on the Raiden infrastructure. Raiden's code is a 32 MB, Raiden-only monolith with its own hazards, bars and tests, and nothing in it is reusable. The framework already gives:
   - the lifecycle, a teleport arena, hazards / projectiles / pull / move;
   - helper hit objects (`aux`), bars, typed lines;
   - the per-boss fx-kit and rig-library pattern;
   - the mcsim test harness and the fairness simulator.

   What chapter mode must add (§3.3, R1-R16):
   - entry from the zone-9 boss room, chapter clear instead of item boxes, the ×15 boss economy, a lose path;
   - per-boss arenas;
   - **proxy hitboxes for huge bodies** (melee reach is measured to the mob's feet, so a 15-b dragon with one hitbox cannot be hit at the head or tail);
   - per-element RES, HP floors and phase pools;
   - music (the game has none today);
   - **minions** (Apep's organisms) and an **objective entity** (the Heart of the Oasis);
   - tests.
4. **Arenas.** The Raiden arena is a plain circle rebuilt inside the dungeon on every boss map. The mid-boss arena is one persistent plaza at (200,201,8), built once and checked with a version string and a sentinel block.

   Proposal: each chapter boss gets its own **persistent, teleport-in arena** outside the dungeon, and the boss room in the dungeon becomes a small "domain entrance" with a gate object. The entrance is also where Azhdaha's two element glyphs are shown.

   | boss | centre | walk radius | look |
   |---|---|---|---|
   | Azhdaha | (320, 201, 8) | 28 | dark cavern with hanging gold crystals, shallow-water look floor, edge pillars and steles |
   | Apep | (440, 201, 8) | 26 | forest lake ringed by giant trees, withered in phase 1 and lush in phase 3 |
   | Apep, phase 2 | (440, 170, 8), under the lake | 16 | the golden cave with the Heart |

   Details in §4.
5. **Difficulty.**

   | boss | level today | base HP | dmgMul |
   |---|---|---|---|
   | Raiden | 6 / 12 / 18 in chapters 1 / 2 / 3 (`mlv = (ch-1)×6 + mapIdx + 1`, mapIdx 5) | 267 (2680 / 4656 / 6664 HP) | his own raw values ×160 % |
   | mid-bosses | L2-5 in chapter 1 | 230-250 | 110 |

   Proposals:
   - **Azhdaha:** `hp 360` (3612 HP at L6, three phases of 1204), `atk 12`, `dmgMul 140`, `xp 40`. That is about 1.35× Raiden's chapter-1 kill time and 1.7× the Guardian's.
   - **Apep:** `hp 320` (7984 HP at L18, split 53/47 between the two boss forms), `atk 12`, `dmgMul 150`, `xp 40`, plus the Heart stage.

   Both are to be tuned with the fairness simulator (`S:mb3/review/fairness/sim/fgfair.py`, and `S:mb2/balance/fsim.py` + `bal.py`).

---------------------------------------------------------------------------------------------------

## 1. The chapter-boss lifecycle today, with every hook point

### 1.1 Chapter structure, level, theme

| item | where | value |
|---|---|---|
| chapter = first map + 4 node maps + boss map | `DP/README.md:271`; `#mapIdx` 0 first … 4 last node map, 5 boss map (`DP/README.md:332`) | — |
| level of every spawned mob (bosses included) | `F:room/mob_init:35-40` | `mlv = (#chapter − 1) × 6 + #mapIdx + 1` → boss map = **6 / 12 / 18 / 24** in chapters 1 / 2 / 3 / 4. A framework body adds the registry `lvAdd` (`core:472-474`). |
| HP scaling | `F:mob/level_apply:1-20`, constants `F:load:856-859` | `mhpM = base × (100 + 30x + 0.05x²)% × #mobHpMul 400%`, x = lv − 1 |
| boss hit scaling on the player | `F:player/hurt_lv:1-13` + `F:player/hurt_k:1-5` (`#mobLvAtk 14`, `#mobLvAtk2 6`, `#defKLv 4`, `F:load:860-863`) | raw × (100 + 14x + 0.06x²)%; defence K = 100 + 4x |
| player → mob level factor | `F:combat/lv_mult` (`#mobLvDef 150`, `F:load:862`) | dmg × (pl + 100) / ((pl + 100) + 100 + 1.5 × mlv) |
| chapter theme | `F:room/theme:1-17` | 1 = `#th 3` plains (Mondstadt / **Liyue**); 2 = `#th 4` **Inazuma** (houses, shops, shrines); 3 = `#th 5` **Sumeru** (per zone rainforest or desert, `sd`); 4 = `#th 7` Fontaine (rivers, lakes); then odd chapters `#th 1` abandoned mine, even `#th 2` forest |

So chapter 1 (Liyue plains) fits Azhdaha, a Liyue boss, and chapter 3 (Sumeru rainforest and desert) fits Apep's oasis. Raiden's own test already treats him as "the planned chapter-2 boss" (`F:boss/raiden/test/start:20-24`, chapter 2, level 12).

### 1.2 Step by step (today, every chapter)

| # | step | file:line |
|---|---|---|
| 1 | Last node map (`#mapIdx 4`): entering the end zone (kind 2) runs `end_setup` | `F:room/zone_enter:8` → `F:room/end_setup:2` |
| 2 | One "보스전" object: `types[8]` (`minecraft:wither_skeleton_skull`, "챕터의 보스와 싸운다"), oact 7, oarg 8 | `F:room/end_boss:1-4`; types list `F:room/data:3` |
| 3 | Click: `#mapType 8` → `run/next_map` (`field_next`, `#mapIdx` +1 = 5, `room/gen`) | `F:room/obj/click:13-14`, `F:run/next_map:2-4` |
| 4 | `room/gen`: `room/clear`, theme, **`room/pick/boss`** | `F:room/gen:2,4,12` |
| 5 | **Hook: `room/pick/boss` → `room/raiden/layout`** ("임시로 모든 챕터 보스"). Writes `rlk:room cur`. Zone 1 = foyer (kind 0, x −6..5, z 24..39). Zone 2 = arena (kind 9, 4 quadrant cells −24..23). One door at z 23-24. Spawn (0, 33) yaw 180. Both zones carry `boss_id:"narukami"`. Door lintels are set to polished blackstone. | `F:room/pick/boss:1-3`, `F:room/raiden/layout:2-5` (generated, `T:build_raiden_arena.py:35-58`) |
| 6 | Zone and door markers; the first zone is built at once. **Hook: `zone_build`** checks `boss_id:"narukami"` and runs `room/raiden/build` (foyer for zid 1, arena for zkind 9) instead of `room/zb_fn`. | `F:room/gen:17-23`, `F:room/zone_build:4-5`, `F:room/raiden/build:2-3` |
| 7 | The same `narukami` gate skips the zone-kind patch, the "visited" floor wave and the floor swap. | `F:room/zone_patch:2`, `F:room/zone_floor:2`, `F:room/wave_start:4` |
| 8 | The arena is built when the player nears the door (`door_reveal` → `zone_build` of zone 2): the circle fills and the marker `rlk_raiden_arena` at (0,201,0) `{boss_id, radius:23, safe_radius:21}` | `F:room/tick:11`, `F:room/raiden/arena:3-247` (`T:build_raiden_arena.py:92-115`) |
| 9 | Entering a cell of zone 2 → `zone_enter`. Kind 9 → `combat_start`: `#combat = zid`, `#spawnT 20`, doors drawn and sealed, "적 출현" | `F:room/tick:10`, `F:room/cell_enter:3`, `F:room/zone_enter:6`, `F:room/combat_start:2-8` |
| 10 | After 20 t: `combat_wait` → `mob_wave`. **Hook: kind 9 → `room/boss_spawn`** | `F:room/combat_wait:1-3`, `F:room/mob_wave:2` |
| 11 | **Hook: `room/boss_spawn`** → `boss/raiden/spawn` at the arena marker | `F:room/boss_spawn:2-3` |
| 12 | `boss/raiden/spawn`: cleanup, then a husk with `rlk_room rlk_zmob rlk_m_boss boss rlk_raiden` (NoAI, invisible), then `setup` | `F:boss/raiden/spawn:2-5` (`enc:107`) |
| 13 | `setup`: `room/mob_init` (`rlk_m_boss` → base HP **267**, `#mad 6`, **xpDrop 40**, `F:room/mob_init:11-13`); attack 0 / speed 0; `mob/setup`; KB res; rd scores; `reload` (rig); bars `rlk:narukami` + `rlk:narukami_state` shown; title + subtitle; `vBig`/`ttlT` 84; `wither.spawn` sound | `F:boss/raiden/setup:1-22` (`enc:114`) |
| 14 | Each tick: `rlk:tick` → `boss/raiden/world` (pause on dead / `rnDie` / `pkMode`, then tick, objects, hazards, vfx, movement). Orphan cleanup when no Raiden. The bars are hidden while no Raiden exists. | `F:tick:48-52`, `F:boss/raiden/world:1-19` (`enc:151`) |
| 15 | Hits on the player: Raiden hazards set `#cmDmg` = their `damage` value (`F:boss/raiden/hazard/hit:54`), then `boss/raiden/hurt` multiplies by **`#bossDmgMul` 160 %** and calls `cm/hit_pl` | `F:boss/raiden/hurt:7-9` (`enc:614`), `F:load:865` |
| 16 | Hits on Raiden: `combat/apply`. Some states are protected (`F:combat/apply:10-14`). `apply_mods` → `boss/raiden/incoming`: armour 80 % DR, exhausted ×2, and an **HP floor** at 55 % that forces the transformation | `F:combat/apply_mods:16`, `F:boss/raiden/incoming` (`enc:577-597`) |
| 17 | Bars: `rlk:narukami` (Lv + name + state) and `rlk:narukami_state` (bossui HP bar + under-bar: rage / armour / timer) | `F:boss/raiden/bars:1-29` (`enc:546`), `T:build_bossbar.py:1-25` |
| 18 | Minimap hidden while Raiden exists, and while the player stands in a kind-9 zone | `F:minimap/tick:11,19` |
| 19 | **Kill:** `combat/apply`, HP ≤ 0: `#killBoss`, `heal_orb_roll` (5 %), `kill_xp` (xpDrop 40), **`gold_drop`**: random 2..4 × chapter (if ≥ 2) × **`#bossGoldMul` 15**, plus **`#bossSapphire` 2** sapphires, because the mob has `boss` without `miniboss`. Then `boss/raiden/death/start`. The body is not killed. | `F:combat/apply:70,72-74,78`; `F:combat/gold_drop:5-13,21-22`; `F:load:828-832` |
| 20 | `death/start`: `rdDeath 1`, `mhpC 0`, every hazard and object cleared, bars hidden, `iron_golem.death`. `death/tick` holds the collapse for **48 t**, then `death/finish`: `cleanup`, `kill @s` | `F:boss/raiden/death/start:1-31`, `F:boss/raiden/death/tick:1-5`, `F:boss/raiden/death/finish:1-2` (`cin:103,136,143`) |
| 21 | No `rlk_zmob` left → `combat_clear`: doors open, seals out, "구역 정리". **Hook: kind 9 → `room/obj/k_chapter`** (unless `#rdTest`) **at the zone marker**, i.e. the arena centre. In a test: `boss/raiden/test/won`. | `F:room/combat_tick:3`, `F:room/combat_clear:1-11` |
| 22 | `k_chapter`: a nether-star object, oact 8, "다음 챕터" | `F:room/obj/k_chapter:1-4` |
| 23 | Click → `run/next_chapter`: `#chapter` +1, `#seen*` and `seen[]` reset, `#mapIdx 0`, `#mapType 0`, `room/gen` (the new chapter's theme) | `F:room/obj/click:26`, `F:run/next_chapter:2-15` |

### 1.3 Exit, pause and cleanup paths (the same for Raiden and the framework)

| event | path | file:line |
|---|---|---|
| player dead / reviving / in a selection screen | Raiden `world` pauses and hides the bars; framework `world` → `pause_tick` | `F:boss/raiden/world:5-8`; `core:816-822,851-860` |
| player respawns after death | `#rdTest` → `boss/raiden/test/defeat`; `#mbTest` → `mboss/test/defeat`; otherwise `run/fail` → `run/end` → `room/clear`, reset, lobby | `F:player/hook_respawn:3-5`, `F:run/fail:1-11`, `F:run/end:1-22` |
| map change, run end, death | `room/clear` → `boss/raiden/cleanup` + `mboss/cleanup` (never teleports), zone erase, `kill @e[tag=rlk_room]`, loose items swept | `F:room/clear:3,5,6-8,11-14` |
| dungeon re-setup | `room/wipe` → the same two cleanups, then the y 186..230 band cleared | `F:room/wipe:2-3,6-27` |
| uninstall | `boss/raiden/cleanup`, `kill rlk_raiden`, `mboss/uninstall` (bars, forceload, objectives, every module's `uninstall`) | `F:uninstall:1-4`; `core:191-208` |
| /reload | `load` → `bossui/init`, `boss/raiden/init` (objectives, bars; a living Raiden reloads his rig and keeps his HP), `mboss/init` (a surviving body runs `mboss/reload` → module `reload`) | `F:load:1369-1375`; `enc:73-106`; `core:123-189` |
| boss bars left over (server-global) | `tick`: `#rdBar` without Raiden → hidden; `#mbBar` without `#mbLive` → hidden | `F:tick:52,55` |

### 1.4 Rewards, music, minimap, bars: current facts

- **Rewards on a chapter-boss kill:**
  - gold: random 2..4 × chapter × 15, so 30-60 in chapter 1 and 90-180 in chapter 3;
  - 2 sapphires (`F:combat/gold_drop:21-22`);
  - XP = `xpDrop` 40;
  - 5 % heal orb;
  - then the next-chapter object.

  No item selection.
- **Rewards on a mid-boss kill, for comparison:**
  - the body has `boss` **and** `miniboss`;
  - gold × registry `goldMul` 5 (`F:combat/gold_drop:15`);
  - `sap` 1 (`F:combat/gold_drop:23-24`);
  - `picks` 2 item boxes (`core:559-571`).
- **Music: none exists.**
  - No `playsound` of `music.*` / `music_disc.*` and no `stopsound` anywhere in `F:`. The only `stopsound` is per-character motion audio (`F:char/motion/audio/stop:3`).
  - `README` has no BGM section.
  - Sound effects are vanilla only, de-duplicated per tick by `rlk:snd/f<n>` (`DP/README.md:328`).
- **Minimap hiding**, `F:minimap/tick:5-21`. The minimap is hidden:
  - outside a run;
  - while dead, in a selection screen or the map screen;
  - while a Raiden exists (`:11`);
  - while a mid-boss fight is on (`#mbOn 1`, `:13`; `#mbOn` is set at `core:360`);
  - while the player is in a kind-9 zone (`:19`).
- **Bars.**

  | boss | bars | lines | made at |
  |---|---|---|---|
  | Raiden | 2 boss bars | `rlk:narukami` (name line), `rlk:narukami_state` (bossui line) | `enc:73-83` |
  | framework | 3 boss bars | `rlk:mboss` (Lv + `cur.title` + aura glyphs + `extra[]`), `rlk:mboss_state` (bossui HP bar + under-bar from the module's `bars` hook), `rlk:mboss_sub` (`sub[]`) | `core:127-129,1095-1131` |

  - The bossui draws the HP run in a fixed red: `HP_COLOR` at `T:build_bossbar.py:47,188`.
  - Under-bar colour codes are 1-9 (`T:build_bossbar.py:50-58`).

### 1.5 The Raiden code (what "Raiden infrastructure" is)

| piece | generator | runtime |
|---|---|---|
| encounter controller (init, reload, spawn, setup, cleanup, bars, world, tick, AI, 15 patterns, objects, illusions, incoming / threshold / hurt, tests) | `T:build_raiden_encounter.py` (`init 73`, `reload 84`, `spawn 107`, `setup 114`, `cleanup 138`, `bars_hide 145`, `world 151`, `tick 279`, `finish 428`, `bars 546`, `incoming 577`, `threshold 592`, `hurt 614`, `test/* 1050-1170`) | `F:boss/raiden/**` (70 entries, 2 670 functions, about 32 MB, `S:mb2/code/reuse.md` §6.3) |
| death, camera | `T:build_raiden_cinematic.py` (`death/start 103`, `death/tick 136`, `death/finish 143`) | `F:boss/raiden/death/*`, `camera/*` |
| arena + foyer + layout | `T:build_raiden_arena.py:1-116` | `F:room/raiden/{layout,build,foyer,arena}` |
| hazards (yaw-locked ground warnings, 14 shapes), hazard vfx, movement, objects, orb, signature vfx, illusions, materials, textures, rig (52 parts), judgment rig | `T:build_raiden_{hazards,hazard_vfx,movement,object_vfx,orb,signature_vfx,illusions,materials,fx_textures}.py`, `T:build_raiden_rig.mjs`, `T:build_raiden_judgment_rig.mjs` | `F:boss/raiden/**` |
| build order + pack check | `T:build_raiden_all.py:26-50`, `T:check_raiden_pack.py` | — |
| tests | `F:boss/raiden/test/*`: `start` (chapter 2, mapIdx 5 → L12, real boss map, zone 2 built and entered, wave at once), `armored`, `pattern {id}` (1-7, 11-18), `lock {id}`, `level {lv}`, `stop`, `won`, `defeat` | `enc:1050-1170` |

Hand-written hooks that Raiden owns in shared files:
- `F:room/pick/boss:3`, `F:room/boss_spawn:2-3`;
- `F:room/zone_build:4-5`, `F:room/zone_patch:2`, `F:room/zone_floor:2`, `F:room/wave_start:4`;
- `F:room/combat_clear:9,11`;
- `F:combat/apply:8-14,78`, `F:combat/apply_mods:16`;
- `F:tick:48-52`, `F:minimap/tick:11`;
- `F:room/clear:3`, `F:room/wipe:2`, `F:uninstall:1-2`;
- `F:player/hook_respawn:3`, `F:run/start:11-13`, `F:run/end:5-7`, `F:load:1371`.

---------------------------------------------------------------------------------------------------

## 2. Routing per chapter

### 2.1 Today

- `F:room/gen:12` → `F:room/pick/boss:3`: Raiden for every chapter.
- `F:room/boss_spawn:2-3`: Raiden for every boss zone.
- `F:room/pick/copy_boss` (8 legacy boss layouts `rlk:room L.boss[]`, `DP/README.md:331`) is dead code: nothing calls it.

### 2.2 Proposed routing (one decision, carried by the zone)

1. **Decide in `room/pick/boss`**. The table is generated from the registry `ch` field by `build_mboss_core.py`, e.g. `F:mboss/cb/route`:
   ```
   # GENERATED: chapter -> chapter boss (registry kind "chapter", field ch); anything else stays Raiden.
   execute if score #cbForce mb matches 1.. run return run function rlk:mboss/cb/route_force
   execute if score #chapter room matches 1 run return run function rlk:mboss/cb/layout {id:"azhdaha"}
   execute if score #chapter room matches 3 run return run function rlk:mboss/cb/layout {id:"apep"}
   function rlk:room/raiden/layout
   ```
   - `mboss/cb/layout` loads that boss's entrance layout (§4.3), sets the zones' `boss_id` to the boss id, and sets `#mbForce` to its registry `n`.
   - `#cbForce` lets the tests pick a boss for any chapter. `run/start` and `run/end` reset it, like `#mbForce` (`F:run/start:14-16`, `F:run/end:8-10`).
2. **Carry it on the zone**: `data.boss_id` is already in the layout record (`F:room/raiden/layout:2`, `"boss_id":"narukami"`). Route on it:
   - `F:room/boss_spawn`:
     `execute unless data entity @s data{boss_id:"narukami"} run return run function rlk:mboss/cb/start`
     (`@s` is the zone marker: `room/mob_wave` runs as the zone, `F:room/combat_wait:3`). Raiden stays the fallback.
   - `F:room/zone_build:4-5`: dispatch on the id, with `room/raiden/build` for `narukami` and the entrance builder for chapter bosses. `F:room/zone_patch:2`, `F:room/zone_floor:2` and `F:room/wave_start:4` need `if data entity @s data.boss_id` (any boss), not `narukami` only.
   - `F:room/combat_clear:9-11`: for a chapter-boss zone call `mboss/cb/won`. It returns whether the boss was killed: `k_chapter` only then; otherwise the gate comes back.
   - `F:room/zone_enter:6`: a chapter-boss zone does not start combat on entry. It shows the gate object (§3.3 R1). Raiden zones keep starting combat at once.
3. Optional polish:
   - the "보스전" end object (`F:room/end_boss:1`, `types[8]`) and the boss-map title (`F:room/gen_title:4`) can show the chapter boss's name and icon from the same routing (e.g. "야타용왕 — 봉인된 바위 용의 왕");
   - the minimap already hides in kind-9 zones (`F:minimap/tick:19`) and during `#mbOn` (`:13`).

### 2.3 Direct test commands

| boss | command (as the `player`-tagged player, after `/function rlk:room/setup` once per world) | what it does |
|---|---|---|
| Raiden (exists) | `/function rlk:boss/raiden/test/start` | Chapter 2, mapIdx 5 → **L12**. Real boss map, the arena built and entered, wave at once (`F:boss/raiden/test/start:20-35`). `armored`, `pattern {id:1..7 / 11..18}`, `lock {id}`, `level {lv:N}`, `stop`. Death → `test/defeat`. A win prints [다시 하기] [로비로]. **Must keep working:** it sets `#chapter 2`, which the new routing maps to Raiden, and `#cbForce` must be 0 (reset by `test/start`). |
| Azhdaha (proposed, framework) | `/function rlk:mboss/test/chapter {id:"azhdaha"}` | `#cbForce` = its `n`, chapter = its first `ch` (1), `#mapIdx 5`, `#mapType 8`, `room/gen`; the entrance zone built and entered, the gate pressed at once (as `core:2181-2217` does for zone 15). Then the shared ones: `/function rlk:mboss/test/pattern {id:N}`, `test/lock {id:N}`, `test/level {lv:N}`, `test/kill` (lethal true hit → chapter clear → next-chapter object), `test/abort` (no kill → the gate comes back), `test/stop`. Module extras through `test/pattern` ids, e.g. 1-9 phase-1 patterns, 20 / 30 jump to phase 2 / 3, 90-93 force the element pair (fire+electro, water+cryo, fire+cryo, water+electro), matching the wiki's weekly pairs. |
| Azhdaha in another chapter | `/function rlk:mboss/test/chapter_ch {id:"azhdaha",ch:3}` | the same at chapter 3 (L18) |
| Apep (proposed) | `/function rlk:mboss/test/chapter {id:"apep"}` | chapter 3 (L18). Module ids, e.g. 1-6 phase-1 patterns, 20 enter the revival stage, 21 / 22 Heart +25 % / −25 %, 30 phase 3, 31-35 phase-3 patterns. |
| Full real path (any boss) | `/function rlk:run/start`, then optionally `/scoreboard players set #chapter room 3`, then `/scoreboard players set #mapIdx room 4`, `/scoreboard players set #mapType room 8`, `/function rlk:run/next_map` | exactly what the "보스전" click does (`F:room/obj/click:13-14`, `F:run/next_map:1-4`; README "직접 맵 넘기기", `DP/README.md:337`). Chapter 1 → Azhdaha, 3 → Apep, 2 / 4+ → Raiden. |
| Next chapter after a win | click the nether star, or `/function rlk:run/next_chapter` | `F:run/next_chapter` |

---------------------------------------------------------------------------------------------------

## 3. Framework "chapter boss" mode vs the Raiden infrastructure

### 3.1 Comparison

| need | Raiden infrastructure | mid-boss framework (`core`, newest on `wip/fg`) |
|---|---|---|
| lifecycle (spawn, intro, fight, death shell, pause, reload, cleanup, uninstall) | hand-rolled per boss in `enc`/`cin`: every new boss copies about 1 200 generator lines | generic (`core:339-417,799-917`); a boss is 17 hooks (`FG/tools/mboss_lib.py:19-22`) |
| hazards | Raiden-only `hazard/create` with 14 hard-coded shapes and Raiden tags | `hz/{disc,ring,sector,line,full}` with options: element, KB, height band, volley groups, `#hzNoDodge`, aim, resize, re-arm, safe circle on `full` (`core:1242-1730`) |
| projectiles, pull, movement | Raiden-only | `pj/*` (homing steer, blade shape, return), `pull/*`, `mv/*` (generic on any entity, `core:2005-2160`) |
| helper hit objects | `rlk_rd_object` (attack counts only, `F:combat/apply:8`) | `aux/*`: an HP pool as a % of the boss, the same damage mods as the body, an `aux_hit` hook (`core:1003-1091`) |
| bars | 2 bars, Raiden text | 3 bars plus `extra[]` / `sub[]` / under-bar hook (`core:1095-1161`) |
| typed lines | Raiden captions | `line/say` (`core:1165-1213`) |
| fx / HUD / sound kit | Raiden-only generators | the butterfly / field-generator kits, copied and renamed per boss (`S:mb2/bf_fx_api.md`, `S:mb3/fg_fx_api.md`) |
| rig | `build_raiden_rig.mjs` (52 parts, skin-based) | shared `T:mboss_rig_{math,compile,clips}.mjs`, `mboss_model_lib.mjs`, `mboss_paint_lib.mjs`, `mboss_screen_lib.mjs`, with byte-identity proofs |
| tests | in-game commands only | in-game `test/*` **plus** mcsim suites (`S:mb3/tests/run_all.sh`, `fgsim.py`, `test_e2e_*.py`) **plus** the fairness simulator |
| datapack size | 32 MB for one boss | Guardian 4.6 MB; target ≤ 5 MB per boss (`S:mb2/code/reuse.md` §6.3) |
| arena | in-dungeon, rebuilt per boss map | one persistent teleport arena (registry `arena`) |
| economy | `boss` tag → ×15 gold, 2 sapphires | `boss` + `miniboss` → `goldMul`, `sap`, `picks` boxes |

**Recommendation: build both chapter bosses as framework modules (`F:mboss/azhdaha/**`, `F:mboss/apep/**`, generators `T:build_mboss_azhdaha.py` / `T:build_mboss_apep.py` + rig + fx kit), with a small chapter mode in `build_mboss_core.py`.** Raiden stays as he is, for chapter 2 and chapters 4+.

Reasons:
- three finished bosses already prove the framework;
- the mcsim and fairness tooling only understands framework hazards (the fairness agent reads `rlk_mb_hz` markers and `pj` props, `S:mb3/review/fairness/sim/fgfair.py:10-16`);
- the per-boss kit and rig libraries are exactly what "모델링에 공을 많이 들여야 해" needs.

### 3.2 Chapter mode at a glance

```
boss map (pick/boss routes by chapter) -> foyer -> boss zone (kind 9, the "domain entrance", gate object + boss props)
   gate click -> combat_start -> 1.5 s -> mob_wave -> boss_spawn -> mboss/cb/start {id}
      -> per-boss arena ensure + marker -> module spawn -> tp_in (blindness) -> intro -> fight
      -> kill (combat/apply: heal orb, XP, boss gold x15 x chapter, 2 sapphires) -> death shell -> body killed
   -> combat_clear (kind 9) -> mboss/cb/won: gold absorb, cleanup, tp_out to the entrance, #mbKilled 1 ? k_chapter : gate again
   lose (player death)           -> pause -> respawn -> run/fail (run/end -> room/clear -> mboss/cleanup) or test/defeat
   lose (objective, Apep Heart 0) -> mboss/cb/lose -> the player dies through the normal path (curHealth 0 -> player/health_tick:12 -> player/die)
```

### 3.3 Exactly what the framework needs (R1-R16)

**R1. Registry.** Add these fields (single source for core, arena and module generators: `FG/tools/mboss_lib.py:43-57`, `core:89-118`):
- `"kind": "chapter"`, so `w` stays 0 and the mid-boss roll never picks it (`core:283-298` already skips `w ≤ 0`);
- `"ch": [1]` / `[3]`, the chapters it ends;
- `"arena": "<id>"`, with `"arenas"` becoming a map;
- `"music"` (R11);
- `"picks": 0`.

`snbt_entry` (`core:89-112`) must emit `kind`, `ch` and `arena`. `check_mboss_pack.py` keeps checking the 17 hooks. Two new optional hooks:
- `prep` (chapter mode only): runs as the boss zone marker when the entrance is built. Azhdaha rolls its element pair there and lights the glyph steles.
- `lose_check`: none needed; the module calls R14 itself.

**R2. Entry and start (`mboss/cb/start`, `mboss/cb/gate`).**
- `zone_enter` for a chapter zone puts the gate object `room/obj/k_cboss`, a new **oact 16**, at the zone centre. The kind-15 gate (`F:room/obj/k_mboss:1-7`, oact 14 → `mboss/gate`, `core:318-337`) is the model.
- The click runs `combat_start` with `#spawnT 30`.
- `room/boss_spawn` → `mboss/cb/start {id}`. It is `mboss/start` (`core:339-365`) with these differences:
  - the boss is forced by id, so there is no roll and no `met` append (`core:359`);
  - the per-boss arena is used (R3);
  - `#mbMode 1` (chapter);
  - the same `ret_save` / `tp_in` / `bars_show`.
- Alternative: Raiden-style auto start on entering the zone (drop the gate). The gate is recommended: the player gets time to prepare (Shift+F picks, items) and it shows Azhdaha's element glyphs.

**R3. Per-arena constants.** Today one arena is baked into the core at generation time: `CX CY CZ WALK SAFE RAD` and the tokens `@CX@ @OOB@ @BOX@ @FL@ @SAFE1@ @WALK2@ @SAFEP@` (`core:24-40`). They are used by:

| use | core line |
|---|---|
| arena ensure on load | 178 |
| reload marker | 184 |
| uninstall forceload | 204 |
| start: loaded check and marker | 343, 353 |
| start_unloaded forceload | 370 |
| `won` gold absorb box | 548 |
| `arena_sweep` | 788-795 |
| `oob` | 861-868 |
| `hz/full` radius and rim | 1251, 1487-1492 |
| `mv/clamp_step` | 2104-2105 |
| `mv/leash` | 2122-2125 |
| `mv/clamp` | 2138 |
| `test/arena` | 2295 |

Modules also bake them, e.g. `FG/tools/mboss_fieldgen/api.py:43-44,117`.

Proposal:
- registry `"arenas": {"plaza": {...}, "az_cavern": {...}, "ap_oasis": {...}, "ap_cave": {...}}`;
- `cur.arena` → `#mbAr`;
- generate those small functions per arena under `F:mboss/ar/<aid>/…`, behind one-line dispatchers on `#mbAr`.

Guardian, butterfly and field generator keep `plaza`. Their module outputs stay byte-identical; only core outputs change. Apep needs **two arenas in one fight** (the lake, and the golden cave for the Heart stage). So the module must be able to switch `#mbAr` mid-fight with `mboss/ar/switch {aid}`: move the marker, `tp` the player with blindness, move `rlk_safe`.

**R4. Death → chapter clear instead of item boxes.**
- `mboss/cb/won` (from `F:room/combat_clear` for chapter zones) does:
  - the gold absorb in the arena box (`core:548`);
  - `cleanup_fight` (`core:763-781`);
  - `tp_out` (`core:530-537`);
  - **no `reward`**;
  - if `#mbKilled 1` (set at `core:900`), returns 1 and `combat_clear` spawns `room/obj/k_chapter` at the zone centre (`F:room/combat_clear:9`);
  - otherwise the gate comes back (like `cancelled`, `core:748-751`);
  - `forget` (`core:752-757`).
- Test mode prints the replay links instead (like `core:2285-2290`).

**R5. Reward multipliers.**
- The chapter body is summoned **without `miniboss`**. `mboss/body` (`core:460-468`) needs a variant `mboss/cb/body`, or a mode branch.
- `F:combat/gold_drop:13,21-22` then pays ×15 gold × chapter and 2 sapphires, the same as Raiden.
- `F:combat/gold_drop:15,23-24` (`rlk_mb_body` → `#mbGoldMul` / `#mbSap`) must not stack on top. Either gate those two lines with `tag=miniboss` (2-line shared edit, recommended), or set registry `goldMul 1`, `sap 0`.
- XP from the registry `xp` (`core:486-491`), 40 like Raiden (`F:room/mob_init:13`).
- The level needs nothing: `body_setup` → `room/mob_init` uses `#mapIdx 5`, so the levels are 6 / 12 / 18 (`core:469-483`).
- **Organisms (R9) must not pay rewards:** aux hits return before the kill path (`F:combat/apply:27` vs `:70-81`), which is already right.

**R6. HP floors and phase pools.** Azhdaha:
- the HP does not drop below 2/3 or 1/3 during the absorb transitions;
- it stays ≥ 1 while burrowed in phase 3 and dies on the first hit after surfacing.

Apep:
- phase 1 ends at a floor (Genshin "below 1 %");
- the revival stage has no boss HP;
- phase 3 has a new pool and a new name, "기원 오아시스 파수꾼".

Precedent: Raiden's 55 % floor in `incoming` (`enc:577-597`). Add a core helper `mboss/floor`: module `incoming` sets `#mbFloor` (‰ of max or absolute), and the helper clamps `#dmg` so `mhpC − #dmg ≥ floor`. True damage (`test/kill`) bypasses it, as intended.

Also add a title swap `mboss/title {text,color,sub}`, which writes `rlk:mboss cur.title` / `cur.sub`. The bars read `cur.title` (`core:1120`). Modules must not hand-write `cur`.

**R7. Per-element RES.** There is none today: one `mres` per entity (`F:combat/apply_mods:13-14`, `F:combat/res`), and the body is set to 0 (`core:482`).
- Azhdaha: Physical 30, Geo 30, the chosen Pyro-or-Hydro 30, the chosen Cryo-or-Electro 30, everything else 10.
- Apep: Dendro 30, others 10. Organisms: Dendro 20, others 10.

Cheapest correct place: the module `on_hit` hook (`F:combat/apply:23`), which runs **before** `apply_mods` and its RES step. It does `scoreboard players set @s mres <table[#elem]>`, which covers reactions and DoTs too (`#elem` is the reaction's element, `#tfm 1`). A generic core version reads `"res": {"0":30,"5":30,"*":10}` from the registry. For aux organisms the same goes in `aux_hit` or `#auxRes`.

The earlier contracts' rule "never read `#elem`" (`S:mb2/bf_contract.md:146`, `S:mb3/fg_contract.md:155-156`) was a per-boss user decision. It does not bind here.

**R8. Proxy hitboxes for huge bodies (new; blocking for Azhdaha).**
- Melee picks targets by the distance from the player to the mob's **feet** (`F:combat/find_immediate:60-62`: `@e[tag=rlk_mob,distance=..3.5 / ..5 / ..4.5]`).
- The click shield is one interaction box at the body (`F:mob/shield_ensure:16,20`; size `cur.hit`, `core:492-495`).
- A 14-16 b dragon with one husk under its belly cannot be hit at the **head or tail**, which are exactly the zones the wiki tells players to attack.

Need `rlk_mb_proxy` husks: invisible, NoAI, `rlk_mob` + `boss`, a shield sized per proxy, **never `rlk_zmob`**, no HP of their own. The module places them each tick at rig anchors: head, front legs, hind legs, tail root, tail tip. A rig-compile feature that exports a part's world position per clip tick would help (`T:mboss_rig_compile.mjs`).

The shared edit at the top of `F:combat/apply`, e.g.

`execute if entity @s[tag=rlk_mb_proxy] run return run execute as @e[type=husk,tag=rlk_mb_body,limit=1] positioned as <proxy> run function rlk:combat/apply`

redirects a proxy hit to the body:
- the same element / on_hit / mods / RES / incoming / kill path;
- the number is shown at the proxy.

It also needs:
- a per-swing **de-duplication**: one swing that reaches two proxies counts once (a gametime + attack-id flag);
- a body flag that hides the body's own shield but still accepts proxied hits. Azhdaha's phase-3 burrow ("only the tail is above ground and can be hit") needs proxies on the tail only. `rlk_mb_inv` cannot be used for this: it blocks at `F:combat/apply:17`.

**R9. Minions / adds (Apep's organisms).** The base exists: `aux/spawn` (`core:1049-1091`) gives
- an invisible husk with `rlk_mob` + overhead HP bar + click shield;
- an HP pool as a % of the boss max HP;
- the body's damage mods;
- an `aux_hit` hook;
- `rlk_mb_broken` on death;
- cleanup by tag;
- element auras and reactions, because `element/on_hit` runs first (`F:combat/apply:21`).

Missing:
1. Ground AI. Cheap stepping toward the Heart or the player. `mv/*` works on any entity but costs about 25 commands/tick per mover.
2. Attacks with the organism as the source: `hz`/`pj` already accept any `@s` as the knockback source.
3. A cap and spawn points (burrow fx).
4. Type records: HP %, coefficients, RES Dendro 20, behaviour.
5. Links:
   - nurturing buffs up to 3 basics with immunity (`#mbAuxDone 1` + the "면역" popup, `core:1040-1043`);
   - guarding gives a Dendro shield (absorb in `aux_hit`);
   - predatory swallows a basic;
   - nesting builds barriers and teleports;
   - destruction rolls to the Heart and explodes.
6. Kill events. The module reads `rlk_mb_broken` and `#mbAuxBroke` (`core:1044-1048`) for Heart progress, and spawns element-energy particles on some kills (wiki: destruction → +20 energy).
7. Budget: each organism is a husk + interaction + HP-bar displays + 2-6 model displays. Cap about 8 alive.

**R10. Objective entity (Apep's Heart of the Oasis).** It is new; nothing like it exists. Needs:
- A module marker + item_display model at the cave centre. **Not** `rlk_mob`: the player cannot damage it.
- Progress `#mbObj` in ‰. Starts 270. Basic kill +17.5, other kills +110. Organism hits −6 (−12 when buffed). Destruction blast −140. Win at 1000 → phase 3. **0 → lose (R14)**.
- Organisms target it first.
- A hazard victim option, e.g. `#hzVictim 1`: the strike damages the objective (`#mbObjDmg`) instead of the player. `hz/hit` (`core:1530-1566`) only knows the player today.
- HUD: during the stage the bossui HP run shows the Heart. The module `bars` hook can override `#buHp`/`#buMax` after the core sets them (`core:1121-1128`). The colour is fixed red (`T:build_bossbar.py:47,188`): add a `#buHpCol` option (green for the Heart) to `build_bossbar.py`.
- A "drags on" warning timer → destruction organisms.
- The boss body stays alive and keeps `rlk_zmob`, so the zone cannot clear. It is untargetable underground (`rlk_mb_inv`, no shield, `F:mob/shield_ensure:6`), with the leash off (`#mbNoLeash`).

**R11. Music (new, vanilla only).**
- `mboss/music/{start,tick,stop}` with registry `"music": [{"ev":"minecraft:music.dragon","len":<ticks>,"src":"music"}, …]`, per phase if wanted.
- Before starting: `stopsound @a[tag=player] music` so the vanilla background track does not overlap.
- Play at the player with volume ≥ 4 (range 64 b), or at the arena centre with `minVolume`.
- Loop on a timer (sound events have no loop flag).
- `stopsound` in `cleanup_fight`, `death_start`, `pause_tick`, `uninstall` and the `cb/won` teleport.
- Candidate vanilla events:

  | boss | moment | event |
  |---|---|---|
  | Azhdaha | phase 1 (an ominous cavern) | `music.overworld.deep_dark` |
  | Azhdaha | phases 2-3 | `music.dragon` (C418 "Boss", the vanilla boss track) or `music_disc.precipice` |
  | Apep | phase 1 | `music_disc.5` / `music_disc.13` (eerie) |
  | Apep | revival stage | `music.nether.*` |
  | Apep | phase 3 | `music_disc.creator` / `music_disc.relic` |

- Track lengths must be **measured from the client's vanilla assets** before the loop timers are set; they are not in the repo.

**R12. Bars and HUD.**
- The 3 framework bars are enough.
- The name line `Lv.6 야타용왕` plus `extra[]` element badges: the absorbed leg and tail elements.
- The under-bar: phase gauge, pattern progress or the brand timer.
- The sub-line: nameplate, pattern and "곧 원소의 힘을 흡수합니다".
- Minimap: nothing to do (`#mbOn`, `F:minimap/tick:13`).

**R13. Cleanup and wipe.**
- Fight entities and bars are covered: `room/clear` / `room/wipe` / `uninstall` → `mboss/cleanup` / `uninstall` (`F:room/clear:5`, `F:room/wipe:3`, `F:uninstall:4`; `core:782-787,191-208`).
- Add:
  - `#mbMode` reset;
  - music stop;
  - arena forceload of **every** arena: on demand at entrance build (`prep`), released in `cb/won` / `cleanup`, and in `room/remove` / `uninstall` (today's single plaza: `F:load:1228`, `F:room/setup:8`, `F:room/remove:10-11`, `core:204`);
  - `mboss/ar/<aid>/clear` for every arena in `room/remove`.

**R14. Lose path (`mboss/cb/lose`).**
- For "Heart reaches 0 %": set the player's `curHealth 0` (bypassing shields). `player/health_tick:12` → `player/die` → the normal respawn routing (`F:player/hook_respawn:3-5`), so `run/fail` or `test/defeat` follows.
- A plain player death needs nothing new: the fight pauses (`core:816-822`) and `room/clear` cleans up on `run/fail`.

**R15. Tests.**
- In-game: `test/chapter {id}`, `test/chapter_ch {id,ch}` (§2.3). They reuse `test/kill|abort|pattern|lock|level|stop`. `test/won` / `test/defeat` print chapter wording.
- mcsim: copy `S:mb3/tests/fgsim.py` → `azsim.py` / `apsim.py`, and suites `test_azhdaha.py`, `test_e2e_azhdaha.py`, `test_apep.py`, `test_e2e_apep.py`. Add one framework suite `test_chapter.py`. It covers:
  - routing: ch1 / ch3 / 2 / 4+, `#cbForce`, and the Raiden `test/start` regression;
  - gate → arena → kill → ×15 gold + 2 sapphires, no boxes → `k_chapter`;
  - abort → gate back;
  - the lose path;
  - every cleanup path, with the arena forceloads released;
  - reload ×N;
  - proxies: hits on head/tail reach the body once per swing;
  - aux minions and the objective: progress, fail, win;
  - per-element RES table;
  - HP floors.
- Wire them into `S:mb3/tests/run_all.sh` style with `gen_check.py` (idempotent generator order) and `ident.py` (Guardian / butterfly / fieldgen outputs unchanged).

**R16. Player-status helpers (Azhdaha's brand).** This is module-level, but the hooks exist:
- "elemental hits brand the player; when the brand ends and the player has **no shield**, a strong DoT":
  - the module keeps a brand timer per element;
  - it checks `shieldHP` (`F:element/shield_absorb:2`) / `gShield` (`F:engravings/guard/absorb:2`);
  - the DoT goes through `mboss/hurt` with `#mbNoDodge 1` (`core:929-962`), so a shield still absorbs it (`player/take_damage` → `shield_absorb`).
- "Healing cleanses it": count heals with `#mbHealEv` (`core:419-430`, from `items/hook/on_heal`).
- Show the brand on the sub-line or the under-bar.

### 3.4 Shared-file edits in one list (outside `F:mboss/**` and the generators)

| file | edit |
|---|---|
| `F:room/pick/boss` | call the generated route (R1/§2.2) |
| `F:room/boss_spawn` | `boss_id` ≠ narukami → `mboss/cb/start` |
| `F:room/zone_build:4-5`, `zone_patch:2`, `zone_floor:2`, `wave_start:4` | any `boss_id`, dispatch the entrance builder |
| `F:room/zone_enter:6` | chapter zone → gate object (`k_cboss`) instead of `combat_start` |
| `F:room/obj/click` | oact 16 → `mboss/cb/gate` |
| `F:room/combat_clear:9-11` | chapter zone → `mboss/cb/won`; `k_chapter` only if killed; the test message |
| `F:combat/gold_drop:15,23` | require `tag=miniboss` |
| `F:combat/apply` (top) | proxy redirect (R8) |
| `F:room/remove`, `F:room/setup`, `F:load:1226-1228`, `F:uninstall` | the arenas' clear and forceload (R13) |
| `F:run/start:14-16`, `F:run/end:8-10` | reset `#cbForce` |
| `T:build_bossbar.py:47,188` | optional `#buHpCol` |
| `T:build_mboss_arena.py` | multi-arena themes (§4) |

---------------------------------------------------------------------------------------------------

## 4. Arenas

### 4.1 How arenas are generated today

**Raiden (`T:build_raiden_arena.py`, 116 lines; outputs `F:room/raiden/*`):**
- `layout` (`:42-58`) is a fixed `rlk:room cur` record:
  - zone 1 = foyer `(-6,24)-(5,39)`;
  - zone 2 = arena `(-24,-24)-(23,23)` as **four quadrant cells** so every erase fill stays below the 32 768-block limit (`:35-40`);
  - one door, the spawn point, `arena:{x:0,y:201,z:0,radius:23,safe_radius:21}`.
- `build` (`:60-64`) dispatches by zid / zkind.
- `foyer` (`:66-76`) is a plain 12 × 16 blackstone room with a light layer at y 218.
- `arena` (`:92-115`):
  - air fill y 201-230 per quadrant;
  - per row: polished blackstone y 199, light-gray concrete y 200 (stand height 201) and the light layer y 218 for `d ≤ 24`;
  - wall `23 < d ≤ 24` from y 201 to 207;
  - the marker `rlk_raiden_arena` at (0,201,0).
- It is built during the run like any zone (`zone_build`), inside the forceloaded dungeon square x/z −64..63 (`F:room/setup:6`).
- It is erased per cell over y 186..230 (`F:room/erase_cell:1-4`, via `room/zone_erase` from `F:room/clear:6`) and by `room/wipe` (`F:room/wipe:6-27`).
- Constraints of this placement:
  - radius ≤ about 40, with a foyer;
  - **nothing above y 230**;
  - rebuilt every boss map, in one tick;
  - door lintels must match (`F:room/raiden/layout:4-5`).

**Mid-boss (`T:build_mboss_arena.py`, 326 lines; outputs `F:mboss/arena/*`):**
- Input: registry `arena` = centre (200,201,8), `r 22`, `walk 21`, `safe 19`, `start` (200.5, 201, 25.5, yaw 180), theme `plaza`, `ver 2` (`T:mboss_registry.json:13-19`).
- `layout()` (`:197-229`):
  - polished blackstone base at cy−2;
  - a patterned floor at cy−1: calcite and quartz, three engraved rings, a rose star, 8 swirl blades, gold studs (`:42-51,144-184`);
  - a wall ring 7 high with pillars;
  - 12 gold lamp spires (`:187-194,211-228`).
- `build_lines()` (`:255-291`):
  - clears the box in 4 quadrants (up to cy+35);
  - row-span fills per layer;
  - a barrier cap on the wall ring at y 208-215;
  - an invisible light layer at cy+5;
  - sets `rlk:mboss built "plaza@2"`.
- `main()` (`:294-322`) writes:
  - `arena/build_<theme>`;
  - `arena/ensure`, which rebuilds when the version string or the centre sentinel block is wrong and returns fail while the corners are not loaded;
  - `arena/build`, `arena/rebuild`, `arena/clear`.
- `ensure` runs at load (`core:178`) and at every fight start (`core:352`).
- The chunks are forceloaded permanently (`F:load:1228`, `F:room/setup:8`). They are released by `room/remove` (`F:room/remove:10-11`) and uninstall (`core:204`).

### 4.2 Recommendation: persistent teleport arenas per chapter boss, plus an in-dungeon "domain entrance"

Why not inside the dungeon (Raiden style):
1. Both themes need height. Azhdaha's cavern has a ceiling and hanging crystals well above a 6-7 b dragon; Apep has a giant-tree canopy. The dungeon band ends at y 230 (29 b above the floor) and is wiped as a whole.
2. Detailed decor (thousands of blocks, display props) should be built **once** and checked by version, not rebuilt every run in one tick.
3. Apep needs a second sub-arena (the golden cave) for the Heart stage.
4. The framework already has the teleport, return point, `rlk_safe` handling, out-of-bounds, sweep and forceload.

The boss zone in the dungeon stays: it becomes a small themed "domain entrance" room with the gate object.

For Azhdaha it matches Genshin: "two coloured glyphs at the domain entrance show the pair (upper = tail, lower = leg)". The `prep` hook rolls the pair when the entrance is built and lights two steles, e.g. a red/blue lower glyph and a cyan/violet upper glyph. Display-entity glyphs with vanilla blocks or RP sprites.

Placement: free regions in the overworld are away from the dungeon (−64..63), the lobby (80..134 × 14..64, `F:load:653`), the selection room (around 96..111 × 0..10, `F:room/remove:8`) and the mid-boss plaza (176..223 × −16..31). The proposals below sit at x ≥ 270, z −40..56. Forceload is **on demand**: at entrance build (`prep`), released after the fight. Their boxes are large (25-49 chunks), unlike the plaza's 9.

### 4.3 Azhdaha: "「복룡목」 아래" (under the Dragon-Queller tree), the earth-core rock bed

Reference:
- `S:az/src/wiki.md` "Domain image": a dark cavern, golden crystals hanging from the ceiling, a shallow water floor, dark stone pillars and steles.
- The portrait background: carved glyph steles, cracked olive stone, gold Geo streaks, a golden-leaved tree.
- Footage (e.g. `S:az/understand/model_work/ov/ov_v3.jpg`): a hazy olive-gold cavern, the boss about 6-8 character heights long, the fight spread over a wide floor.

| item | proposal |
|---|---|
| boss size (for the arena) | Nose to tail tip about **14-16 b**, shoulder about 5 b, head with horn crown about 6.5-7 b. Body footprint radius about 7 b from its centre. |
| arena id / centre | `az_cavern`, centre **(320, 201, 8)**, stand height 201 |
| radii | **walk 28** (diameter 56, about 3.5× the body length, so a player can always keep ≥ 8 b from the body and run around the tail); **safe 26** (body leash and ground-target clamp); rough rock wall `28 < d ≤ 33` with irregular noise; box ±40 (x 280..360, z −32..48), y 190..240 |
| ceiling | A dome of `tuff` / `deepslate` / `smooth_basalt`. Apex y ≈ 238 (37 b over the floor), rim about y 214. **No solid block below y 216 inside r 28**: the head plus jump-slam arcs need about 12 b of clearance. Barrier cap on the wall ring as on the plaza. |
| hanging gold crystals | 20-30 stalactite clusters from the dome, tips at y ≥ 216, denser toward the north (the "tree root" side): `raw_gold_block` + `gold_block` cores, `yellow_stained_glass` / `orange_stained_glass` shells, `ochre_froglight` / `shroomlight` glow cores, `pointed_dripstone` fringes. 4-6 hero crystals as RP item_display props in the boss's crystal palette (#F2B53A / #FFD36B, amber #C8781E edges); they can pulse during phase changes. Golden tree roots (`stripped_jungle_log`, `mangrove_roots`, gold-leaf displays) come down the north wall. |
| floor + "shallow water" | Walkable solid floor at y 200: `mud`, `packed_mud`, `smooth_basalt`, `tuff`, `polished_tuff`, cracked olive stone (`mossy_cobblestone`, `andesite`, `yellow_terracotta` streaks for Geo cracks). **Do not use real water inside the walk disc**: it changes player and avatar physics, dash and jumps. Use a visual water sheet: large flat translucent item_display planes (RP water texture, about 40 % alpha) at y 201.02, with splash / `bubble_pop` / `dripping_water` particles on steps and impacts. Real 1-deep water only in the rim pools beyond r 28. Telegraph cards then sit at y ≥ 201.05. |
| stone pillars | 6 massive irregular pillars (radius 2.5-3.5, `deepslate_bricks` / `polished_blackstone` / `tuff_bricks`, gold vein lines) half sunk into the wall at r 29-31. None inside the walk disc: framework hazards are 2-D and ignore cover, and the camera needs a clear view. 2-3 broken stubs (height 1-2) are allowed at r 25-27. |
| steles | 8 carved tablets (3 wide × 5 high: `chiseled_tuff_bricks`, `chiseled_stone_bricks`, `polished_tuff`, with gold glyph inlays `gold_block` / `yellow_glazed_terracotta`) around r 29-30. The two at the arrival point (south, z +26) repeat the entrance glyphs of the chosen pair. |
| arrival / start | (320.5, 201, 34.5) yaw 180 (south edge, facing the boss at the centre) |
| light | Hidden `light` blocks: a low layer at y 206 over the disc, level 8-10, so the floor reads dark but legible; crystal glow, and gold `glow` particles drifting from the crystals. |
| phase dressing | Phase 2 tints (water: blue `dripping_water` + `falling_water`; fire: ember `lava` + `flame` + scorched decals). Phase 3 crystal flashes in the tail element. These are module fx, not block changes. |
| entrance room (dungeon) | Chapter-1 theme (Liyue plains) zone of normal size: a Liyue stone arch (`stone_bricks`, `polished_andesite`, `dark_oak` beams, gold trim), the two glyph steles flanking the gate object, gold Geo cracks on the floor |

### 4.4 Apep: forest lake ringed by giant trees

Reference:
- `S:ap/src/wiki.md`: phase 1 in a withered olive-yellow forest with gold crystal spikes; phase 2 the Heart (a golden egg) in a dark golden cave; phase 3 a lush forest lake ringed by giant trees.
- Footage `S:ap/understand/v5/sheet4fps_0-10.jpg`: phase 2 has an orange-gold cave floor; the cut-scene goes into a bright green canopy, then phase 3.

| item | proposal |
|---|---|
| arena id / centre | `ap_oasis`, centre **(440, 201, 8)**. Box ±44 (x 396..484, z −36..52), y 190..250. |
| radii | **walk 26**, **safe 24**. The ring of giant trees sits at r 30-38 beyond the walk disc, with a root and rock wall `26 < d ≤ 29`. |
| floor | A lake look: solid `mud` / `clay` / `moss_block` at y 200 with the same translucent water-sheet planes as Azhdaha. Reed and lily props only beyond r 24. Real water only outside the walk disc. |
| giant trees | 8-10 trunks 4-6 b wide (`jungle_log`, `mangrove_log`, `pale_oak_log`, with `mangrove_roots` buttresses) at r 32-36. Canopies arch over the rim from y 225 to about 250, leaving the centre sky open (a hazy shaft of light). |
| phase 1 "withered olive forest" | Non-tinted withered blocks: `pale_oak_leaves`, `pale_hanging_moss`, `pale_moss_block` / `pale_moss_carpet`, `leaf_litter`, `short_dry_grass` / `tall_dry_grass`, `dead_bush`, `yellow_terracotta` / `brown_terracotta` patches, plus gold crystal spikes from the ground (displays). Avoid oak / jungle leaves: their colour depends on the biome. |
| phase 3 "revived" | One block-swap function, run in slices over about 20 t while the player is in the golden cave: `fill … replace pale_oak_leaves` → `azalea_leaves` / `flowering_azalea_leaves`, `leaf_litter` → `moss_carpet`, dry grass → `short_grass` / flowers, plus `glow_lichen`, `spore_blossom`. Build both looks from the generator's block lists; the builder stamps `ap_oasis@<ver>:<look>`, so `ensure` can restore phase 1 for the next fight. |
| golden cave (Heart stage) | `ap_cave`, centre **(440, 170, 8)** under the lake, box y 160..195, **walk 16**: an orange-gold cave (`raw_gold_block`, `orange_terracotta`, `red_sandstone`, `honeycomb_block`, `ochre_froglight` light), cracked earth, a shallow puddle at the centre holding the Heart egg (display model). 6-8 burrow spots at r 12-15 for organisms. The player moves down and up with `mboss/ar/switch` (blindness, R3). |
| alternative | The Heart stage in place, in the lake arena (dim the light, raise the Heart at the centre). Cheaper, but it loses the "golden cave" look. |
| entrance room (dungeon) | Chapter-3 theme (Sumeru): a sandstone and mud-brick oasis gate (`cut_sandstone`, `mud_bricks`, gold-green crystals), with the gate object |

### 4.5 Generator shape

Generalise `T:build_mboss_arena.py`:
- the registry `arenas` map;
- one theme builder per arena (`plaza`, `az_cavern`, `ap_oasis`, `ap_cave`);
- `ensure` / `build` / `rebuild` / `clear` per arena under `F:mboss/arena/<aid>/`;
- the fills split so each stays ≤ 32 768 blocks;
- for big builds, an optional multi-tick build (schedule slices; `ensure` returns fail until done);
- a render hook (`layout()` is already importable for offline renders, `:24-25`).

The plaza output must stay byte-identical. The entrance rooms need a small generator of their own, e.g. `T:build_cboss_rooms.py` → `F:room/cboss/<id>/{layout,build}`, or a mode of `build_raiden_arena.py`.

---------------------------------------------------------------------------------------------------

## 5. Difficulty

### 5.1 Formulas (all integer, `S:az/understand/chapter_work/calc.py` replicates them)

| quantity | formula | source |
|---|---|---|
| mob max HP | `(100 + 30x + ⌊5x²/100⌋) × base / 100 × 400 / 100`, x = lv − 1 | `F:mob/level_apply:2-19`, `F:load:856-859` |
| boss hit on the player (after the raw value) | `raw × (100 + 14x + ⌊6x²/100⌋) / 100 × K / (K + def)`, K = 100 + 4x | `F:player/hurt_lv:1-13`, `F:player/hurt_k:1-5`, `F:player/take_damage:7-13` |
| Raiden raw | hazard `damage` (5-34) × `#bossDmgMul` 160 / 100 | `F:boss/raiden/hurt:7-8` |
| framework raw | `atk × coef% × dmgMul / 10000` | `core:941-945` |
| player damage vs mob level | `(pl + 100) / ((pl + 100) + 100 + 1.5 mlv)`, about 0.49 at every stage | `F:combat/lv_mult` |
| player base | HP `100 + 12(lv−1)`, def `10 + 2(lv−1)`, atk `10 + 2(lv−1)` | `F:load:818-823` |

### 5.2 Current bosses

| boss | base hp / atk / dmgMul | level | max HP | notes |
|---|---|---|---|---|
| Raiden | 267 / per-hazard `damage` (13× 10, 6× 12, 4× 14, 4× 19, 3× 9, 2× each of 15 18 22 30 34, …) / ×160 % | ch1 **L6** · ch2 **L12** · ch3 **L18** | 2680 · 4656 · 6664 | Armour phase: body takes 20 % (`enc:577-605`, armour tuning `enc:28-37`). Exhausted 300 t: ×2 taken. 55 % HP floor until the first transform. xpDrop 40. README tuning target: "a level 9-10 player dies to 2-3 big attacks" at L12 (`DP/README.md:951`). |
| Guardian | 250 / 12 / 110 | node maps: ch1 L2-5 | L4 1900 | groggy 220 t, goldMul 5, sap 1, picks 2 |
| Butterfly | 240 / 12 / 110 | same | L4 1824 | |
| Field generator | 230 / 12 / 110 | same | L4 1748 | field damage cut ×0.6, 20-hit break |
| proto | 120 / 10 / 120 | — | — | test only (w 0) |

Hit sizes on an item-less player (`calc.py`; player level chosen per stage):

| raw source | boss L6 / player Lv5 (HP 148) | L12 / Lv10 (HP 208) | L18 / Lv15 (HP 268) |
|---|---|---|---|
| Raiden `damage:10` (raw 16) | 23 | 34 | 45 |
| Raiden `damage:19` (raw 30) | 44 | 65 | 86 |
| Raiden `damage:34` (raw 54) | 80 | 117 | 155 |
| mid-boss coef 1.0 at dmgMul 110 (raw 13) | 19 | 27 | 37 |
| mid-boss coef 2.2 (raw 29) | 42 | 62 | 83 |

### 5.3 The fairness simulator (mid-bosses)

- **Butterfly vs Guardian.**
  - Files: `S:mb2/balance/fsim.py` (the agent and fight loop on the real datapack through mcsim, `S:mb2/tests/{mcsim,bfsim}.py`) and `S:mb2/balance/bal.py`:

    `python3 bal.py <datapack root> <label> [seeds] [jobs]`

    It runs the three behaviours stand / melee-walk / ranged-walk (react 5) with seeds 11/22/33, for 3600 t each, and prints HP lost per minute, the BF/GD ratio and damage per pattern. `run_batch.py` adds the dash policies.
  - Logs: `S:mb2/balance/before.log`, `bf2_before.log`, `out_*`.
  - The balance rule was "within 20 % of the Guardian" (BFFIX).
- **Field generator (newest).**
  - Files: `S:mb3/review/fairness/sim/fgfair.py` (on `S:mb3/tests/fgsim.py`: attributes, Motion, low gravity, dash i-frames, `#hzNoDodge`) and `batch.py`:

    `python3 batch.py <label> <preset|spec> [jobs]`

    Presets: `base`, `dash`, `fgbase`, `fgttk`, `gdttk`, `ttk`.
  - The player hit path is the real `cm/hit_pl2` → `player/take_damage`.
  - The scripted agent walks, sprints, swing-slows, jumps (with the current gravity) and dashes (3 b / 3 t, 2 charges, i-frames). It reacts to visible `rlk_mb_hz` markers, projectiles and wave fronts after `react` ticks.
  - It **attacks** through `combat/apply`. It has character models (sword, Navia, Nefer, bow, catalyst) with real swing intervals and coefficients, a Lv4 item-less player (HP 136, def 16, atk 16), and an optional real-HP fight to the kill.
  - Results: `S:mb3/review/fairness/sim/analysis.txt`, item by item:
    - Guardian HP lost per minute: stand 217, melee-walk 158-161, ranged-walk 125-131;
    - perfect dashers lose 0;
    - Guardian kill time: sword **104 s**, Navia 163 s, bow 113 s, catalyst 174 s;
    - field generator kill time 112-188 s, at 0.20-0.74× the Guardian's HP loss.
- **For the chapter bosses**:
  - copy `fgsim.py` → `azsim.py` / `apsim.py` (module rig calls logged and stubbed) and `fgfair.py` → `azfair.py` / `apfair.py`;
  - the agent must learn to attack **proxies** (R8: head and tail, never the side for Azhdaha) and to kill **adds** while protecting the Heart (Apep);
  - Guardian runs in the same harness as the calibration (force 1).

### 5.4 Proposals for chapter 1 and chapter 3

Kill-time model: from the sim's Guardian (L4 1900 HP, 104 s for an item-less Lv4 sword agent), scaled by HP, player atk and `lv_mult` (`calc.py`; items, downtime and phase stops are not counted):

| boss | max HP | sword | Navia | bow |
|---|---|---|---|---|
| Raiden ch1 (L6, pLv5) | 2680 | 132 s | 207 | 143 (+ armour phases) |
| Raiden ch2 (L12, pLv10) | 4656 | 150 s | 235 | 162 |
| Raiden ch3 (L18, pLv15) | 6664 | 160 s | 251 | 173 |
| **Azhdaha hp 360** (L6, pLv5) | **3612** | **178 s** | 279 | 192 |
| Azhdaha hp 400 | 4016 | 198 s | 310 | 214 |
| **Apep hp 320** (L18, pLv15) | **7984** | **192 s** | 301 | 208 |
| Apep hp 360 | 8984 | 216 s | 339 | 234 |

**Azhdaha (chapter 1, L6): proposed registry entry.**
- Values: `kind chapter`, `ch [1]`, `n 10`, `w 0`, `el 5` (Geo hits by default), `hp 360`, `xp 40`, `atk 12`, `dmgMul 140`, `lvAdd 0`, `goldMul 1`, `sap 0`, `picks 0`.
- The body: `scale` about 3-4 (on the proxy plan, R8), `hit` per proxy, `intro` about 160, `death` about 140, `deathSnd false`, `arena az_cavern`.
- RES table: phys 30, geo 30, chosen pyro-or-hydro 30, chosen cryo-or-electro 30, rest 10.
- **Three equal phases of 1204 HP.** HP floors at 2/3 and 1/3 (the absorb transition: "야타용왕이 곧 원소의 힘을 흡수합니다", then 파멸의 산사태, then the absorb). Floor 1 while burrowed in phase 3 (R6).
- Expected kill time with downtime: about 3.0-3.5 min item-less, about 2-2.5 min with typical chapter-1 items. That is about 1.35× Raiden at chapter 1 and 1.7× the Guardian.
- Hit sizes at L6 vs Lv5:

  | coef | damage | share of HP |
  |---|---|---|
  | 1.0 | 23 | 16 % |
  | 1.6 | 36 | 24 % |
  | 2.2 | 52 | 35 % |

- Coefficient guidance:
  - chin slam 1.4;
  - jump-slam 2 shockwaves 1.2 each (one volley group per wave);
  - charge 1.8;
  - back spikes 1.0 each (4 points, about 60 t fuse);
  - foot-stomp 3 waves 1.0 (one group each, jumpable low band);
  - side feint 1.2 and tail whip 1.6 as `#hzNoDodge` (the wiki's "undodgeable"). Fair only with ≥ 14 t telegraphs and a clear "leave the side" read;
  - burrow charge 1.6, untargetable underground;
  - 파멸의 산사태: 6 waves 1.0-1.1 each, low band, jump or run out. Six hits ≈ 140, so a Lv5 player with 148 HP survives only at full HP: "a tank needs a big HP pool";
  - phase-2 fields 0.3 per tick-group;
  - brand DoT about 4 × 4 % max HP unless shielded or healed (R16).
- Fairness target: the HP-loss rate for a walking dodger ≤ about 1.3× the Guardian's (≤ about 210 HP/min melee-walk). Perfect dashers lose only to `#hzNoDodge` hits taken from the side.

**Apep (chapter 3, L18): proposed registry entry.**
- Values: `kind chapter`, `ch [3]`, `n 11`, `w 0`, `el 7` (Dendro), `hp 320`, `xp 40`, `atk 12`, `dmgMul 150`, `goldMul 1`, `sap 0`, `picks 0`, `arena ap_oasis` (+ `ap_cave`).
- RES: Dendro 30, others 10 (R7).
- **HP: 7984 in total.** Phase 1 pool 53 % (4232) with a floor at 47 % → the revival stage → phase 3 pool 47 % (3752), with the title swap to "기원 오아시스 파수꾼" (R6).
- **The revival stage:**
  - the Heart progress starts at 27 %; +1.75 % per basic organism kill, +11 % per other kill; −0.6 % per organism hit (−1.2 % when buffed); destruction blast −14 %; 0 % = lose (R10, R14);
  - organism pools as a % of the boss max HP: basic about 2.5 % (≈ 200 HP at L18), others 5-8 %; Dendro RES 20, others 10;
  - at most 4 basics per wave, about 8 alive in total (R9);
  - a target of about 60-90 s for the stage;
  - kill time about 3.2 min plus the Heart stage, about 4.5 min in total item-less, about 3-3.5 min with chapter-3 items.
- Hit sizes at L18 vs Lv15 (HP 268, def 38), from `hit(raw, 18, 38)`:

  | coef | damage | share of HP |
  |---|---|---|
  | 1.0 | 51 | 19 % |
  | 1.6 | 82 | 31 % |

- 종말의 여파 (end-of-days wave):
  - a `hz/full` with the safe circle = the dome (`#hzR0`, `core:1251,1487-1497`), `#hzNoDodge`;
  - coefficient about 4.5 → about 235 (88 % of HP: "near-lethal");
  - the dome lasts the whole wind-up.
- Thorn wheels (homing, "undodgeable"): `pj/steer` with a speed cap, so walking at a right angle beats them; `#hzNoDodge` on contact.
- Fairness target as for Azhdaha, measured with the organisms on.

**Raiden (chapters 2 and 4+): unchanged.** At chapter 2 (L12) he stays the reference: about 150 s plus armour phases, 2-3 big hits kill a Lv 9-10 player. The routing must not change his level or test.

---------------------------------------------------------------------------------------------------

## 6. Open points for the planner and the user

1. Azhdaha's element pair: a random roll at entry, shown on the entrance glyph steles (recommended), or a player choice at the gate? Does the 30 % RES on the two chosen elements apply from the start (the user's table), or only after each absorb (Genshin)? This study assumes from the start.
2. Gate click (recommended) or Raiden-style auto start on entering the boss zone.
3. Apep's Heart stage in the separate golden cave under the lake (recommended), or in place in the lake arena.
4. Music: the vanilla tracks to use per boss and phase. The lengths must be measured from the client assets.
5. Should organisms give XP or energy? Aux kills give no XP, gold or heal orbs today; Genshin gives energy for some kinds.
6. Numbers in §5.4 are starting points. Both bosses need a fairness-sim pass (§5.3) before release.
