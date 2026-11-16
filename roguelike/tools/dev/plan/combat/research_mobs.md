# Balance gauge (균형치) — enemy-side research (rlk, branch claude/exciting-pascal-ek1vuy @ 2dcc742)

Read-only research. Nothing in the repo was edited. `F:x` = `roguelike/data/rlk/function/x.mcfunction`, `T:x` = `roguelike/tools/x`,
`R:n` = `roguelike/README.md` line n. Line numbers are per file at 2dcc742.

## 0. TL;DR

- **Every enemy damage path already funnels through 3 choke points**: player→enemy `F:combat/apply` (+ `F:combat/apply_mods`),
  enemy→player `F:cm/hit_pl` (cm mobs, Raiden) / `F:mboss/hurt` (all registry bosses), and per-tick `F:mob/tick` (every non-pet
  living enemy, from `F:tick:36`). A balance layer can hook those with ~10 one-line hooks plus a new `bal/` folder.
- **Groggy already exists in 9 shapes** (catalogue in 1.12). Bosses: guardian 220 t, butterfly 300 t, fieldgen 200 t, Arlecchino
  stun 140 t, Tachy G3 stagger 50 t / mantle stun 120 t, Scarlet down 200 t, Raiden stun 100 t / exhausted 300 t. Mobs: elite
  "punish windows" 20–30 t, shield-break 30 t, element freeze ~34–60 t, hit stagger 2 t (5 t ch2/ch3 swarm). Most boss modules have a
  test path that forces their groggy/stun cleanly (guardian/butterfly/fieldgen id 40, Arlecchino 29, Scarlet 25; none for
  azhdaha/apep/Tachy) — those are the templates for a balance groggy.
- **cm mobs**: one state score `cmS` per brain; `F:cm/cancel` + the elite `reset` (triggered by `cmS 0` + tag `rlk_c2_busy`) is
  exactly what element freeze uses, so a groggy = "freeze without ice": cancel, `#free 0`, hold movement, pose hold (every rig tick
  already has a `frzT → rig/frozen` branch, 22 files).
- **UI**: head bar = 5 display passengers riding the mob (`F:mob/hb_spawn:3-7`), redrawn every tick in `F:mob/tick:16-31`. Add a
  6th passenger: one `text_display` row of PUA diamond glyphs (new font `rlk:bal`, band U+ED00 which 0-7 reserves as next free, `R:289`),
  redrawn **only on change** (≈0 per-tick cost). Bosses: add an optional third glyph row to the shared `bossui/draw` line 2
  (`T:build_bossbar.py`), 5 px tall, in the 6 px band between the under-bar (rows 10–13) and line 3 (row 19) — one generator, covers
  Raiden + every registry boss, byte-identical for callers that do not set it.
- **Architecture**: integer points (100 = 1 pip), regen after a delay, groggy = tier duration, full refill + short immunity after;
  bosses get it through an optional registry-flagged module hook (same technique as `SPECIAL_OPT_HOOKS`/`rwHook`), never during
  `#mbSt≠1`, `#mbCine 1`, `rlk_mb_inv`, transitions, scripted mechanics. Per-tick idle cost ≈ +2 commands/mob, +3/boss.

---

## 1. Enemy roster, tiers, AI, groggy plug points

### 1.1 Shared mob layer (`F:mob/**`) and who gets a gauge

- `F:tick:35` runs `mob/setup` once for every non-display, non-item living entity without `rlk_mob`/`rlk_pet`/`rlk_mapv`;
  `F:tick:36` runs `mob/tick` every tick for every `rlk_mob`. `F:mob/setup:3` skips non-living, `:14` spawns the head bar except for
  Raiden, `rlk_rd_object`, `rlk_mb_body`; `:19` adds `rlk_mob`. Setup re-runs whenever `rlk_mob` is re-added (3ch burrowers), so a
  gauge init there must be idempotent (`unless score @s balM matches 0..`).
- `F:mob/tick:1-2` skips Raiden death and dying mid-bosses; `:6-7` stun countdown → `mob/unstun`; `:16-21` HP fill width;
  `:23-26` HP numbers **rewritten every tick** via macro `mob/hb_num`; `:28-31` level only when changed; `:33` element tick.
- **Tier rule proposal** (decided in `bal/init` from tags, override table in storage for exceptions):

| Tier | Pips | Who (tags) |
|---|---|---|
| boss | 12 (boss bar, no head row) | `boss` tag **and** (`rlk_mb_body` or `rlk_raiden`) |
| elite | 7 | `rlk_c2e` / `rlk_c3e` except `rlk_cm_ci` → kr nj cc / cs rv pc |
| normal | 4 | every other `rlk_mob` living enemy: ch1 sw ar fm im sh cn, ch2 ns sl ss sp dr, ch3 fu em sb cw, vanilla husk/skeleton/vindicator (`#mobTmp`, `F:room/mob_summon:9-11`) |
| none | — | see exclusions below |

- **Exclusions (must never get a gauge or groggy)**:
  - `rlk_pet` (everything summoned for the player or as a prop): avatar mannequin `rlk_av`/`rlk_body` (`F:view/spawn:8`,
    `F:view/spawn2:1`), view seat (`F:view/seat_new:1`), cm lure mannequin (`F:cm/lure_new:1`), item hound wolf
    (`F:items/proc/hound_start:2`), doll armor stand (`F:items/proc/doll_place:2`), Nefer shadow (`F:char/nefer/shadow_summon:1`),
    all rig display parts. `rlk_mapv` map views.
  - Boss mechanic objects that carry `boss`/`rlk_mob`: mboss aux husks `rlk_mb_aux`/`rlk_mb_hit` (`F:mboss/aux/spawn:8`: guardian
    stars, Apep org creatures, fx demo armor stands), Raiden objects `rlk_rd_object` (`F:boss/raiden/object/create:3`, has
    `rlk_mob`!), chapter-boss hit proxies `rlk_mb_px` (interaction type, never reach mob/tick anyway).
  - ch3 spore pod `rlk_c3pod` (`F:cm/fp/spawn:2`, not an enemy), burrowed brood `rlk_c3bur` (no `rlk_mob` while underground),
    cicin summons `rlk_cm_ci` (2 HP "한 대", no `rlk_zmob`, `F:cm/spawn/ci:3`) — optional: give them 0 pips.
  - Lobby `rlk_lobby` zombies (tutorial target `F:lobby/tut/target:2`, try-room dummy `F:lobby/try/dummy_at:2`; NoAI, get head bars).
    Exclude by default (they never attack, so a parry cannot be practised on them).
  - Apep org creatures (`F:boss/apep/org/**`, aux objects that do hazards) are a **user decision**: default exclude (mechanic adds of
    the revival phase; they are aux, so their HP pipeline is `aux_hit`, not `combat/apply` tail).

### 1.2 ch1 custom mobs (`cm/{sw,ar,fm,im,sh,cn}`, hand-written + `T:build_mobs.mjs`/`T:build_swordsman.mjs` poses) — normal

- Structure (`R:841`): invisible husk brain `rlk_cmb` + mannequin/display visual + shared lure; all attacks call
  `cm/hit_me`/`cm/hit_pl` → `player/take_damage`.
- Loop: `F:tick:48` → `F:cm/world:15` → `F:cm/tick` per brain: `:5-6` cooldowns flow even when stunned, `:7-9` `#free 0` while
  `stunT`/`frzT`, `:12` freeze cancels a running attack (`cm/cancel`), `:13` player down → `cm/down` (cancel + hold),
  `:15-29` per-mob tick, `:31-33` hold (movement −100 %), `:34` `cm/vis` (rig sync).
- State: `cmS` (0 idle, 1.. windup/charge), `cmT` timer, `rlk_cmch` tag = charging (stagger-immune, `F:mob/stun:5`).
  `F:cm/cancel:1-10` resets `cmS`, kills trajectory lines/fireballs/cannon aim, re-poses, calls c2/c3 cancel.
- **Caveat**: archer/fire mage/ice mage/cannon start attacks while stunned by design (`R:836` "쿨이 끝나면 경직 중이어도 바로
  차지를 시작"): `F:cm/ar/tick:4`, `F:cm/fm/tick:5`, `F:cm/im/tick:4`, `F:cm/cn/tick:5` only check `unless frzT`. A groggy must
  block them too (either add `unless score @s balG matches 1..` to those 4 lines, or hold `cmCd ≥ 1` during groggy — all four
  require `cmCd matches ..0`).
- Cannon `rlk_cm_cn` is excluded from hit stun and knockback (`F:mob/stun:3`, `F:mob/basic_hit:3`, `F:mob/knock:2`) — groggy must
  bypass those early returns (do not reuse `mob/stun` as-is).
- Shield bearer `sh`: shield break = 1.5 s stagger precedent (`F:cm/sh/break:2-9`: `cm/cancel` + `mob/stun` + slowness 2 s +
  `stunT 30`); its light-blue shield bar rides the brain at y 0.15 (`F:cm/sh/init:6`) — pip row must sit below it.
- Rig ticks with a freeze branch: `F:cm/sw/rig/tick:24` (+ ar fm im sh cn rig/tick).
- Never interrupt: nothing scripted. Groggy start = `cm/cancel` is always safe (it is what freeze does).

### 1.3 ch2 swarm (`cm/{ns,sl,ss,sp,dr}`, generated by `T:build_ch2_mobs.py` → `T:ch2mob/swarm.py`) — normal

- Same brain + rig (`rlk_c2`, swarm `rlk_c2a`); `F:cm/c2/tick:1-11` (age, drummer haste `#c2X`, dispatch). Hit stagger 0.25 s
  (`F:cm/c2/hurt:3`, `#c2Stun 5` in `F:cm/c2/load:24`), knockback 0.42 b/t.
- Group starts pick members that are not stunned/frozen: `F:cm/ns/pack_go:4`, `F:cm/sp/line_go:4` (check `stunT`/`frzT`, not
  `#free`) → keeping `stunT ≥ 1` during groggy auto-excludes a groggy member.
- Drummer `dr`: hurt → `cm/dr/interrupt` (`F:cm/c2/hurt:8`); groggy should call it (else `rlk_dr_drum` keeps hasting others).
- `F:cm/c2/cancel:1-4` (glow off, rings). Rig: generated `rig_frozen` branch (`T:ch2mob/swarm.py:64`).
- Small slime `ss` (3 HP, `rlk_c2lite`): normal 4 pips, practically never matters.

### 1.4 ch2 elites (`cm/{kr,nj,cc,ci}`, `T:ch2mob/elite.py` + `T:ch2mob/elite_lib.py`) — elite 7 (ci excluded)

- Per-mob state machine on `cmS`; every elite tick starts with `lib/pre` (haste) and
  `execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/<m>/reset` (`F:cm/kr/tick:4`,
  `F:cm/nj/tick:4`, `F:cm/cc/tick:4`, `F:cm/ci/tick:5`) — so `cm/cancel` (cmS 0) + one more tick of the elite = a clean reset
  (`F:cm/kr/reset:1-6` kills dash targets, clears busy/fix/cmch). This is the freeze path.
- Existing **punish windows** (= ready-made groggy poses): kr `a_rest` cmS 3 24 t (`F:cm/kr/a_rest_start:1-10`), nj `tired` cmS 4
  (`cm/nj/tired_start`), cc `dazed` cmS 4 (`cm/cc/b_land`), and their rigs pick poses by `cmS`
  (`F:cm/kr/rig/choose:3`, `F:cm/rv/rig/choose:4-23`).
- Special visibility states: nj vanished (cmS 1–3; reset makes it visible again, `R:874`), cc owns cicins (`rlk_cmlink`).
- Rig tick freeze branch generated by `T:ch2mob/elite_lib.py` `rig()` → `rig/tick` (`F:cm/kr/rig/tick:7`).
- Tell windows are stagger-immune (`rlk_cmch`); groggy must override (cancel removes `rlk_cmch`, `F:cm/cancel:4`).

### 1.5 ch3 swarm (`cm/{fu,em,sb,cw}` + pod `fp`, `T:build_ch3_mobs.py` → `T:ch3mob/swarm.py`) — normal

- Same frame as ch2 (`rlk_c3`, `rlk_c3a`), `F:cm/c3/cancel:1-5` (stops the healer `cw/stop`). Group start `F:cm/em/pair_go:6`
  checks stunT/frzT. Brood `sb`: burrowed = `rlk_c3bur` + `rlk_pet` + invulnerable, no `rlk_mob` (`R:893`); `F:cm/sb/tick:4` returns
  when frozen. Pod `fp` handled at `F:combat/apply:9` (exclude).

### 1.6 ch3 elites (`cm/{cs,rv,pc}`, `T:ch3mob/elite.py` + `T:ch3mob/elite_lib.py`) — elite 7

- Same `reset`-on-busy pattern (`F:cm/cs/tick:5`, `F:cm/rv/tick:5`, `F:cm/pc/tick:5`).
- cs burrow: underground = `rlk_c3_under`, `rlk_pet`, invulnerable, no `rlk_mob` (`R:911`); reset surfaces it. Punish `stuck` cmS 4
  (`cm/cs/erupt`).
- rv: NoAI NoGravity flying brain moved by `cm/rv/fly` (`F:cm/rv/tick:15`; `F:cm/rv/fly:2` returns while frozen → it hangs in the air,
  `R:913`). Punish `grounded` cmS 4 only reachable after a dive (`cm/rv/d_land`). A groggy in the air = hang like freeze, or force a
  drop to safe ground first.
- pc: punish `overheat` cmS 7 exposes the core (`rlk_c3_core`, ×1.5 damage via `F:combat/apply:34` → `cm/pc/core_hit`;
  `F:cm/pc/overheat:1-8`, start `cm/pc/oh_start`).
- Rig freeze branch generated by `T:ch3mob/elite_lib.py:104`.

### 1.7 Vanilla-AI mobs (`#mobTmp room 1` only) — normal

- husk/skeleton/vindicator from `F:room/mob_summon:8-12`; vanilla AI; only `mob/**` applies (0.1 s stun `F:mob/stun` via
  slowness 250 + team `rlk_stun`; `F:mob/basic_hit:6` `stunT = #stunBasic` 2 (`F:load:807`), knock `#kbBasic` 180 (`F:load:808`)).
- Slowness does not stop a skeleton shooting or a husk hitting an adjacent target → groggy must use `NoAI 1b` like freeze
  (`F:element/frz_on:5-6` sets NoAI and tags pre-NoAI mobs `rlk_noai`; `F:element/frz_end:8` restores). **Conflict**: freeze ending
  during groggy would re-enable AI → add `unless entity @s[tag=rlk_bal_grog]` to `F:element/frz_end:8` and mirror the `rlk_noai`
  logic in groggy end.
- Their hits reach the player through vanilla damage → `F:player/vanilla_hit:10` / advancement `element_hurt` (attacker is
  `on attacker`, for the parry researcher).

### 1.8 Mid-boss framework + mid-bosses (`F:mboss/**` by `T:build_mboss_core.py`, modules `mboss/<id>/`) — boss 12

- Framework loop: `F:tick:58` → `F:mboss/main:7` → `F:mboss/world` (`:7-13` pause when no player / dead / Ronova revival /
  selection screen / no body → `pause_tick`, module timers freeze) → `:21` `body_tick` (`F:mboss/body_tick:4-6`: `#mbSt` 0 intro,
  1 fight, 2 dying) → `F:mboss/fight_tick:1` `d/tick` (dispatcher by `#mbId`, `F:mboss/d/tick`) → `:27` `mboss/bars` every tick.
- Framework-wide "never": `#mbSt≠1`, `#mbCine 1` (cine: hazards refuse), tag `rlk_mb_inv` (intro, module invulnerable moves;
  `F:combat/apply:23`), `rlk_mb_dying` (`F:combat/apply:22`), `#mbBarOff 1` (scarlet cines). Boss body gets `boss` → immune to
  `mob/stun` (`F:mob/stun:2`), freeze (`F:element/frz_start:2`), knockback (`F:mob/knock:5`).
- Hooks every module implements (`T:mboss_lib.py:21-22`, 17 hooks + `test/help`, checked by `T:check_mboss_pack.py`); optional
  registry-flagged hooks exist (`T:mboss_lib.py:41` `SPECIAL_OPT_HOOKS = {'rwHook': 'reward'}`, emitted as literal lines only for
  entries with the flag, `T:build_mboss_core.py:4507-4508`) — **the right technique for an optional `bal` hook** (other outputs stay
  byte-identical).
- Body init: `F:mboss/body_setup` (`T:build_mboss_core.py:669`) reads registry `cur.*` (lvAdd, scale, res) → place to init `balM`.

**guardian** (`mboss/guardian/`, `T:mboss_guardian/core.py`): `F:mboss/guardian/ai/state:2-8` `#gdSt` 0 idle, 2 close, 3 guard
mode (element recording 100 t), 4 chaos (17.5 s star timer), 5 groggy, 6 approach, 8 backstep; pattern slot `#gdPat`
(`F:mboss/guardian/p/run`), `p/cancel` (`F:mboss/guardian/p/cancel:3-12`, removes `rlk_mb_inv`). Existing groggy:
`groggy/begin` (sets `#gdSt 5`, 220 t, clips `groggy_a`/`groggy_b`/`getup`), `groggy/end` (`chaos/reset` + 4–5 patterns + `ai/enter`),
no damage bonus (`F:mboss/guardian/incoming:1-2`), test id 40 (`F:mboss/guardian/test/run:24`). Groggy-safe: `#gdSt` 0/2/6/8 (cancel
the slot first). Never: 3 (guard record), 4 (chaos), 5. A balance groggy must NOT call `groggy/end` as-is (it resets the chaos cycle)
→ needs its own end that returns to `ai/enter` keeping `#gdLeft`.

**butterfly** (`mboss/butterfly/`): `F:mboss/butterfly/ai/state:3-7` `#bfSt` 0 idle, 2 close, 3 groggy, 4 recover, 5 prep; forms
`#bfForm` 1 human / 2 butterfly; slot ids (`F:mboss/butterfly/p/start`) 1–4 human, 11–15 butterfly (14 coco, 15 release = cocoon
mechanic), 20 transform (service). Existing groggy 300 t after 달빛 해제 (`groggy/begin`: back turned, clip `groggy_h`, forces
human form, `R:1427`). Clean stop template: `F:mboss/butterfly/test/cut:1-9` (`lib_clear`, `p/cancel`, prop clear, idle clip,
`ai/enter`). Never: transform (20), coco/release (14/15), groggy/recover, intro seq.

**fieldgen** (`mboss/fieldgen/`): `F:mboss/fieldgen/ai/state:2-5` `#fgSt` 0 idle, 3 groggy, 4 recover, 6 break; field stage `#fgField`;
20-hit break meter counted in `on_hit`, resolved in `F:mboss/fieldgen/tick:9-10` (cancels the running pattern) → break 40 t → groggy
200 t (`groggy/begin`, `R:1475`). Clean stop template `F:mboss/fieldgen/test/cut:1-17` (also finishes a half-open field). Never:
warp/fold services (`p/field_in`, `p/field_out`), break/groggy/recover. **Design note**: while the field is up, balance damage could
feed the 20-hit meter instead of pips (the field is already its "balance").

**proto** (n 99, test only): 7 patterns, uses every library — keep a minimal hook for tests.

### 1.9 Chapter bosses (`boss/<id>/`, chapter mode `#mbMode 1`) — boss 12

**야타용왕 azhdaha** (n 10, `T:mboss_azhdaha/`): `F:boss/azhdaha/tick:13-17` four concurrent slots: idle AI `#azPat 0`, main
pattern slot `#azPat`, cast slot `#azCast`, background slots `#azBgL`/`#azBgT`. Slot ids (`F:boss/azhdaha/p/start_d`):
patterns 1–10, 41–46; services 20 slide/landslide, 21–22 absorb (phase transitions), 23 burrow3 (= B3, invulnerable from 8 t,
`api.B3_INV`), 27/28 turn/walk, 30 cast host. Cancel `F:boss/azhdaha/p/cancel:1-12` / `p/cut`. HP floor + reserved transition
(`R:1712-1714`). **No stun clip** in `T:mboss_azhdaha_rig_manifest.json` (49 clips: idle … `roar_low`, `absorb`, `death`) →
needs a new `groggy` clip in `T:build_mboss_azhdaha_rig.mjs` (px proxies follow clips: regen `mboss/px/azhdaha/**`). Never: 20–23,
30, intro seq, B3, transition reserved (`#mbFloorHit`), death.

**아펩 apep** (n 11, `T:mboss_apep/`): `F:boss/apep/tick:8-14` phase `#apPh` 1/2/3, slot `#apPid`; ids (`F:boss/apep/p/start_d`)
1–7 P1, 31/33–36 P3, 10 move, 20 T1 (sink to revival), 32 aftermath (Q2 shield mechanic, lethal later casts), 40 fail, 60 CS,
61 stance. Phase 2 = boss parked, not hittable (`R:1580`) → no gauge shown. Cancel `F:boss/apep/p/cancel:1-14`. Test 22
`test/h_down`. **No groggy clip** (36 clips; closest `crouch_p3`, `sink_p1`) → new clip. Never: 20, 32, 40, 60, phase 2, intro E,
CS, death D.

**아를레키노 arlecchino** (n 12, `T:mboss_arlecchino/`, s3lib architecture): `F:boss/arlecchino/core/fight:13-18` `#pat` 1–13 / 20
(E70) / 41–48 patterns, 50 stun, 51 transition, 52 replay; `#ph` (`T:mboss_arlecchino/api.py:155`). Existing stun (best template in
the pack): `F:boss/arlecchino/core/break:1-15` (cancel_d, win_off, true dmg, `stun_start`) → `F:boss/arlecchino/core/stun_start:1-11`
(stop_move, ground, looks_rest, `#pat 50`, clip `brk` 20 t then `stun`/`stun2` 140 t, tag `rlk_kn_stun`) → `stun_end:1-12`
(rescheduling, `ai/rec_start`). Force guard `F:boss/arlecchino/core/force:1-6` (refuses `#pat ≥ 51`). Test 29 `test/stun`. No
damage bonus (`F:boss/arlecchino/incoming`). Never: E70 (20), F1 Banquet break window (10, `core/run/f1:2-3` win_on/off 22–160),
Q5a/Q5b (46/47), transition 51, replay 52, intro, death. Airborne Q0/Q6: `stun_start` already grounds her.

**cproto** (n 98, test only).

### 1.10 Special bosses (`boss/<id>/`, chapter mode via `mboss/sp`) — boss 12

**타키 tachy** (n 20, s3lib): `F:boss/tachy/core/fight:13-23` `#stag` (G3 stagger) first, `#pat` 1–11 patterns, 50 element swap,
51 mantle, 52 mantle break, 53 nova, 54 transition, 55 replay, 56 close; `#ph` (`T:mboss_tachy/api.py:118`). Damage-taken knob
`#taken tk` read by `F:boss/tachy/incoming:1-5` (100; mantle 20, stun 150, stagger 130). Existing staggers: G3 backfire
`F:boss/tachy/el/backfire:1-16` (cancel_pat, 3 % true, `#stag 50`, `#taken 130`, clip `stagger`); mantle break stun
`F:boss/tachy/mantle/break_tick:3-7` (120 t, `#taken 150`, clip `stun`). Clips `flinch stagger stun` available. Force guard
`F:boss/tachy/core/force:1-7`. Blink/L: invulnerable windows. Never: 51–56, L (13 b up), blink invulnerable ticks, intro/death.

**홍련 scarlet** (n 21, s3lib, from Stellar Blade): `F:boss/scarlet/core/state:2-9` replay `#rp`, `#ph` 1/7 fight, 4/9 gauntlets
A8/A13, 6 down, revive `#rvw`, sequences `#sqn`; `#pat` 1–7/11–13 patterns. Invulnerability `F:boss/scarlet/core/inv:1-6` (`#inv`,
ghost `rlk_hr_ghost`, A6 ticks 0–4). Existing: flinch every 4th hit in recovery (`F:boss/scarlet/core/flinch:1-5`, 6 t clip),
down window 200 t (`F:boss/scarlet/core/down/start:1-8`, test 25), counter A1/A2 after 4 hits in 40 t. **Her 자영 연참 (A8/A13)
already is a parry-like gauge**: 5 shield cells, each slash whose hit tick finds the dash i-frames on breaks one cell, 0 cells at
the final strike = deflect (`R:2068-2072`, `R:2113-2141`). Never: CS0–CS4, SQ1, A8/A13, ghost, lead-ins, kipup, down (already a
groggy), A6 0–4, replay, event. Cancel `F:boss/scarlet/core/cancel_pat:1-3`, force `F:boss/scarlet/core/force:1-9`.

**spproto** (n 97, test only).

### 1.11 나루카미 Raiden (`boss/raiden/`, outside the registry, `T:build_raiden_all.py`, encounter `T:raiden_enc/`) — boss 12

- `F:tick:53` → `F:boss/raiden/world:2-10` (pause on death/revival/selection) → `F:boss/raiden/tick`: `rdPhase` 0 Shogun, 1 transform
  (60 t, invulnerable), 2 Tenma (armour 750), 3 exhausted (300 t, ×2 damage); `rdPat` patterns 1–10/21–28 (Shogun), 11–20 (Tenma),
  98 stun, 99 finish; `rdBlink`, `rdGo`, `rdDeath`.
- Existing stun: `sg/stun_begin` (rdPat 98, 100 t; `rdSgStun` 1 clone found, 2 eye broken, 3 guard broken) →
  `F:boss/raiden/sg/stun_tick:4-9` (clip `stagger`, `recover` at 72, end at 100). Guard meter (`sg/guard_parry`, 14 to break, ×1.5).
  Exhausted: `F:boss/raiden/exhausted_start:1-26`, `exhausted_tick:1-4`. Generator: `T:raiden_enc/shogun.py` (stun, `:405`),
  `T:raiden_enc/tenma.py`, bars in `T:raiden_enc/core.py:405`.
- Damage-immune states (`F:combat/apply:16-20`): transform with armour, rdPat 5 (hidden illusion), 15 (만겁), blink, death. Click
  shield off in the same states (`F:mob/shield_ensure:1-4`).
- Groggy plug: phase 0 → new `rdSgStun 4` through `stun_begin` (same 100 t stagger). Never: rdPhase 1/3, rdPat 5 (찰나의 포영),
  7 (몽상의 일심 set-piece), 15 (만겁), 98, 99, blink, death. Phase 2 (Tenma): **user decision** — no groggy (armour is the gauge;
  balance damage could chip armour instead), or allow outside 15/18/20.

### 1.12 Existing stun / stagger / flinch / freeze catalogue

| Mechanic | Where | Length | Effects |
|---|---|---|---|
| hit stagger (any `#stunHit` hit) | `F:combat/apply:60` → `F:mob/stun:1-9` | 2 t | slowness 250, team `rlk_stun`; boss / cannon / charging immune |
| basic-attack stagger + push | `F:combat/apply:62` → `F:mob/basic_hit:6-7`, `F:load:807-808` | `#stunBasic` 2 t | knock 0.18 b/t |
| ch2/ch3 swarm stagger | `F:cm/c2/hurt:3`, `F:cm/c2/load:24` | 5 t | knock 0.42 b/t, drummer interrupt |
| shield break | `F:cm/sh/break:2-9` | 30 t | cancel + stun + slowness |
| elite punish windows | kr a_rest 24 t, nj tired 1.5 s, cc dazed 1 s, cs stuck 1.2 s, rv grounded 1.5 s, pc overheat 1.5 s (core ×1.5) | 20–30 t | stunnable, pose by `cmS` |
| element freeze | `F:element/frz_start:1-8`, `frz_on:5-6`, `frz_end:8`; cm cancel `F:cm/tick:12` | 1.7–3 s | NoAI, ice passenger; boss immune |
| player-down hold | `F:cm/down:1-2` | while down | cancel + hold |
| guardian groggy | `mboss/guardian/groggy/*` | 220 t | no bonus |
| butterfly groggy | `mboss/butterfly/groggy/begin` | 300 t | no bonus |
| fieldgen break + groggy | `mboss/fieldgen/groggy/begin`, `R:1475` | 40 + 200 t | no bonus |
| Arlecchino brk + stun | `boss/arlecchino/core/stun_start` | 20 + 140 t | no bonus |
| Tachy G3 stagger / mantle stun | `boss/tachy/el/backfire`, `mantle/break_tick` | 50 t / 120 t | ×1.3 / ×1.5 |
| Scarlet flinch / down | `boss/scarlet/core/flinch`, `core/down/start` | 6 t / 200 t | none |
| Raiden stun / exhausted | `boss/raiden/sg/stun_*`, `exhausted_*` | 100 t / 300 t | guard ×1.5 / ×2 |

---

## 2. UI

### 2.1 Head bar today (normal + elite mobs, mid-boss aux stars)

- Spawned once per mob by `F:mob/hb_spawn:3-7`, all **passengers** of the mob (`ride … mount`, `:8`), `billboard:"center"`:
  - `rlk_hb_bg` black block_display, translation y 0.25, scale 1.6 × 0.13 (bar spans y 0.25–0.38 above the passenger anchor);
  - `rlk_hb_fg` red fill, width = HP × 1.6 (`F:mob/tick:17-21`, every tick);
  - `rlk_hb_num` text_display "h/mh" scale 0.42 at y 0.25 (on the bar), **rewritten every tick** by macro (`F:mob/tick:23-26`,
    `F:mob/hb_num:1`);
  - `rlk_hb_lv` "Lv.N" bold #FFD86B scale 0.95 at y 0.43, only on change (`F:mob/tick:28-31`, `F:mob/hb_lv:2`);
  - `rlk_hb_icon` element icons scale 1.4 at y 0.82, rebuilt only when a bit key changes (`F:element/display:1-14` key `icKey`,
    `:22` adds "[빙결]", `:28-29` writes the text through `element/set_icon`).
- Orphans killed by `F:mob/hb_cleanup:1-17` (runs every tick while mobs exist, `F:tick:42-43`).
- Things already drawn **under** the bar: shield bearer's light-blue durability bar y 0.15–0.22 (`F:cm/sh/init:6`); Ronova's
  erosion gauge y 0.15–0.44 incl. a magenta 45°-rotated block_display **diamond** marker at y 0.223
  (`F:element/void/er_gauge_new:4-7`, `er_gauge_set:1-4`, driven from `F:element/display:27`).
- Fonts: everything is default font (no custom font on head bars).

### 2.2 Proposal: diamond row on the head bar

- **One extra passenger** `rlk_hb_bal`: `text_display`, billboard center, `see_through:true`, `background:0`, `shadow:false`,
  translation **y ≈ 0.02–0.04**, scale ≈ 0.5 (a 7 px glyph ≈ 0.09 b tall; 7 pips at 9 px advance ≈ 0.79 b wide, inside the 1.6 b bar),
  i.e. just below the shield/erosion band (0.15). text_display renders 0.025 b per font px × scale; translation y is the bottom of
  the text box (the HP numbers at y 0.25 sit on the bar the same way).
- Spawn it in `F:mob/hb_spawn` (one summon line, only when `balM ≥ 1`, or always and leave empty), kill orphans in
  `F:mob/hb_cleanup` (2 lines, same pattern as `rlk_hb_er` at `:16-17`).
- **Glyphs**: new RP font `rlk:bal` (`assets/rlk/font/bal.json`), PUA band **U+ED00–ED3F** (`R:289` "다음 대역 U+ED00"):
  ED00 filled diamond, ED01 empty (outline only), ED02 white flash (just lost / just regenerated), ED03 cracked (partial pip, if
  partial points are shown), ED04 groggy (red/orange, all pips during groggy), each 7×7 white bitmap tinted by component colour;
  1 px space via a `space` provider; `minecraft:default` reference last. Per 0-6 rules (`R:243-244`): **every component names its
  font, root text empty and unstyled**, resource ids lowercase (`rplint`). Owner: a new generator (`T:build_balance.py
  --resourcepack`), like `T:build_bossbar.py`.
  - No-RP fallback: default-font ◆ U+25C6 / ◇ U+25C7 (unifont; already used by the guardian's `기록 ◇◆`,
    `F:mboss/guardian/hud/extra:3-4`).
  - Colours: filled #FFD23F, empty #6B5A24 (or a dark outline glyph tinted #FFD23F), groggy #FF5A3C, flash #FFFFFF.
- **Update cadence**: event-driven only. Precompute every row string once (normal 0–4, elite 0–7, + groggy/locked variants: ~16
  rows) as tiny functions `bal/row/m4/c3` (no macro, no string building) or storage entries; call
  `execute on passengers if entity @s[tag=rlk_hb_bal] run function rlk:bal/row/…` from the writers (hit, regen step, groggy start/end,
  setup). Per-tick cost of the row: **0** (vs. the HP numbers which already pay a macro `data modify` every tick).
- Optional: a "[그로기]" status in the element icon line via a new `icKey` bit (like "[빙결]" `F:element/display:22`) — cheap, uses
  the existing key mechanism.
- Visual collisions to watch: guardian line-1 `◇◆` slots and Arlecchino's `◆선혈의 충격` badge (`T:mboss_arlecchino/api.py:177`) use
  diamonds; Ronova's magenta diamond marker under the head bar. Keep balance pips yellow and use a distinct glyph shape.

### 2.3 Boss bars today

- Mid/chapter/special bosses: 3 vanilla boss bars made transparent (white bar sprites replaced by blank PNGs,
  `T:build_bossbar.py:103-106`), created in `F:mboss/init:81-83`, shown in order by `F:mboss/bars_show:2-8`, drawn every fight tick by
  `F:mboss/bars` (called from `F:mboss/world:27`):
  1. `rlk:mboss` name: `Lv.N  title` + aura icons + module `extra[]` badges (`F:mboss/bars:9`);
  2. `rlk:mboss_state`: the `bossui` line (`F:mboss/bars:10-20`): module `bars` hook fills `#buSub/#buSubMax/#buSubCol`, then
     `function rlk:bossui/draw` builds storage `rlk:bu line`;
  3. `rlk:mboss_sub`: module `sub[]` text (pattern name, meters, e.g. fieldgen's 20-pip meter `R:1489`).
- Raiden: 2 bars `rlk:narukami` / `rlk:narukami_state` (`F:boss/raiden/init:58-59`), same `bossui/draw`
  (`F:boss/raiden/bars:10-29`).
- `bossui` line 2 geometry (`T:build_bossbar.py:44-53`): 200 px bar, font `rlk:bossbar` U+E400 band (`:66-71`); HP row height 9,
  ascent 8 → rows −1…8 of the text line; under-row height 3, ascent −3 → rows 10–13 ("2 px under the HP bar"); numbers centred in
  default font; cursor ends at the bar end. Options `#buHpCol`/`#buNoNum` are read by one draw and reset at its end (`:233-237`), so
  callers that never set them stay byte-identical — **copy this for the pip option**.
- Vanilla layout: each boss bar is 19 px below the previous one (text at bar_y − 9), and vanilla stops drawing bars at 1/3 of the
  screen height → a 4th permanent bar risks being cut when Arlecchino's banner (`rlk:kn_banner`) or Scarlet's warning (`rlk:hr_warn`)
  bars are up. Don't add a bar.
- Precedent for pip meters on the boss bar: fieldgen's 20 pips in line 3 (font `rlk:mboss_fg` U+E700, empty E701 / full E702 / just
  counted E703, `T:build_mboss_fg_fx.py:296`), redrawn from 21 **precomputed strings** (`F:mboss/fieldgen/fx/hud/e/rebuild`), flash
  ended by a 4 t schedule; Scarlet's 5 shield cells drawn as the under-bar (`R:2179`).

### 2.4 Where the 12 boss diamonds go

- **Recommended**: a third glyph row in line 2, drawn by `bossui/draw` when `#buPipM bu ≥ 1` (current `#buPipN`, state `#buPipS`:
  0 normal, 1 groggy, 2 locked/immune), all three reset to 0 at the end of the draw like `#buHpCol`. Glyphs in the `rlk:bossbar`
  font (owned by `T:build_bossbar.py`, new chars after E438, e.g. E440 filled / E441 empty / E442 flash / E443 groggy), height 5,
  ascent −7 → rows 14–18, i.e. exactly in the free 6 px band between the under-row (≤13) and line 3's glyph tops (row 19).
  12 pips × 16 px pitch ≈ 192 px centred under the 200 px bar. Draw: from the bar end move back `(200+W)/2` (`bossui/space_neg`),
  append one precomputed 12-pip string (13 × 4 variants), move forward `(200−W)/2` (`space_pos`). Cost ≈ 6–8 commands per draw,
  only when set.
- The module `bars` hooks (`mboss/<id>/bars`) keep the under-row for their own gauges (armour, groggy timer, shield cells, record
  progress) — the pip row does not compete with them.
- Hook: one line in `F:mboss/bars` before `function rlk:bossui/draw` (`:19`, generated by `T:build_mboss_core.py`, around `:1469`)
  `execute if score @s balM matches 1.. run function rlk:bal/bu`, and the same line in `F:boss/raiden/bars` before `:28`
  (`T:raiden_enc/core.py:405`).
- Fallbacks if the in-game check shows a clash with line 3: (a) put the row **above** the HP bar (free band rows −10…−2 between the
  name line and the HP row, 8 px), (b) prefix line 3 (`rlk:mboss sub[]`) with the pips (centred text, so pips shift with the text).
  Client-side only → add to "게임에서 확인할 것".

---

## 3. Balance damage sources besides perfect parry (candidates; user decides)

Hook point for all player→enemy sources: `F:combat/apply` after `element/on_hit` (`:27`, `#rx` known) and `apply_mods` (`:33`,
final `#dmg`), one gated line `execute if score @s balM matches 1.. run function rlk:bal/on_hit`. Flags available there:
`#stunHit` (skills via `F:char/dmg_calc:14-15`, bursts too — no burst-specific flag exists; ronova echo, lumine javelin, skirk/melee
extra, yoimiya rocket, `F:combat/find_immediate:48`), `#skillDmg`, `#basic itv`, `#bowHit`, `#crit`, `#rx` (reaction id table
`F:element/react:3-4`), `#tfm` (transformative reaction damage), `#lunar`, `#trueDmg`.

| # | Candidate | Where it is detected | Suggested points (100 = 1 pip) |
|---|---|---|---|
| 1 | Perfect parry (given) | player pipeline → `bal/parry` | 100 |
| 2 | Plain (non-perfect) parry / block | same | 25–50 |
| 3 | Perfect dodge (dash i-frames ate a ≥12 t telegraphed hit) | `#dodged tmp` in `F:cm/hit_pl2:5`, chapter events `#mbDodgeEv/#mbDodgeOk` (`R:1555`) | 0 (SB) or a "next hit within 20 t +50" buff |
| 4 | Skill hits (`#skillDmg 1`) | apply | 20 per hit, cap 1 pip per cast |
| 5 | Burst | needs a new `#burstDmg` flag in each character's burst path (none exists today) | 100–200 per cast |
| 6 | Charged / heavy hits: bow aim/full (`aKind` 2/3, `R:483-487`), last hit of a combo (`comboStep` finisher), Arlecchino/Skirk/Navia finishers | char paths | 25–50 |
| 7 | Crit | `#crit 1` | +10 |
| 8 | Reactions: overload (launch), superconduct, shatter (breaks freeze), freeze start, swirl, Ronova 단죄 | `#rx` 3, 4, 7, 6, 8, 19 | shatter 100, overload 50, freeze 50, others 20 |
| 9 | Existing "break" events: sh shield break (`F:cm/sh/break`), pc core exposure (`rlk_c3_core`), Tachy G3 backfire / mantle break, Arlecchino 선혈의 충격 (in or out of a break window), Raiden guard break / eye broken / real clone found, guardian star broken, fieldgen meter hit, butterfly cocoon cure | each module | treat as "instant groggy" or big balance damage; most already cause their own stun — avoid double groggy |
| 10 | Hits during an elite punish window or a boss flinch | `cmS` punish states, Scarlet `#flq` | ×2 balance multiplier |
| 11 | Scarlet A8/A13: dash-broken shield cells | `boss/scarlet` gauntlet | let a perfect parry also break a cell (parry researcher) |
| 12 | Spore pod burst on swarm, slime chain zap | `cm/fp/burst`, c2 slime zap | 50 |
| 13 | Falling/environment (vanilla_hit) | `F:mob/vanilla_hit` | 0 |

---

## 4. Proposed architecture

### 4.1 Data model (names: prefix `bal` is unused — checked `scoreboard objectives add bal*`, `rlk_bal*`, `rlk:bal`)

Per enemy (scores on the brain / body): `balM` max pips (0 = no gauge), `balP` points (0…balM×100), `balG` groggy ticks left,
`balR` regen countdown, `balI` immunity ticks after groggy, `balT` "active" flag (any timer running → per-tick work needed),
`balK` last drawn key. Tags: `rlk_bal_grog` (groggy), `rlk_bal_lock` (immune now). Storage `rlk:bal` for tunables and the
per-id override table. Global one-shots: `#balDmg tmp` (points of the current event), `#balSrc tmp` (last attacker id, 4.4).
Tunables in `load` (조절 지점) like `#cmD_*`: `#balPip_n 4 / _e 7 / _b 12`, groggy `#balG_n 60 / _e 80 / _b 120`, regen delay
`#balRD_n 100 / _e 120 / _b 160`, regen step `#balRS_n 40 / _e 60 / _b 80`, immunity `#balIm 60`, damage-taken `#balAmp_* %`.

### 4.2 Regen rule (Stellar Blade: slow recovery when not pressured)

- Any balance damage sets `balR = delay` (and `balT 1`). When `balR` reaches 0: +1 pip, `balR = step`; stop when full (`balT 0`).
- No regen during groggy; groggy end = full refill + `balI` immunity (pips drawn "locked"), so a normal mob cannot be chain-grogged.
- Points granularity lets partial sources work (a cracked glyph if `balP mod 100 ≠ 0`, or round up).

### 4.3 Groggy

- Durations (shorter than the mechanic groggies so those stay the big payoff): normal 60 t, elite 80 t, boss 120 t (Arlecchino stun
  140, fieldgen 200, guardian 220 for scale).
- Effect options (user decides; defaults): stun (no attacks, no movement) + damage taken bonus via one line in
  `F:combat/apply_mods` before the module `incoming` (`:16-18`) — normal +50 %, elite +30 %, boss +20 % (note: every existing boss
  groggy except Tachy/Raiden has **no** bonus by design, `F:mboss/guardian/incoming:1-2`, `F:boss/arlecchino/incoming`, `R:1345`,
  `R:1427`, `R:1475`); HP floors still clip after it (`F:mboss/cb/inc/tachy:2-3`).
- Optional finisher ("처형", SB Retribution): the first basic hit on a groggy normal mob kills it / on an elite deals X % max HP true
  damage / on a boss deals X % true damage via `mboss/true_pct` and ends the groggy. Needs an input decision (F is now parry).
- Deferred groggy: if pips hit 0 while the enemy is in a committed-but-interruptible-later section (airborne, burrowed, dashing),
  set a pending flag and start the groggy at the module's next decision (same convention as reserved phase transitions,
  `R:1712-1714`, Tachy `R:1884-1891`). In never-interrupt states balance damage is ignored (row drawn locked).

### 4.4 API

- `function rlk:bal/hit` (@s = enemy, at @s; input `#balDmg tmp` points): returns early if `balM 0`, groggy, immune, `rlk_mb_inv`,
  `rlk_mb_dying`, Raiden immune states, boss `#mbSt≠1`/`#mbCine 1`, or module veto; subtracts; redraws; at 0 → `bal/grog/start`.
- `function rlk:bal/parry` (for the parry pipeline): resolves the attacker from `#balSrc` and runs `bal/hit {100}` as it.
  Attacker capture (1 line each): `F:cm/hit_pl` top (`@s` = brain or projectile; projectiles carry the owner's `cmId`, e.g.
  `F:cm/ar/start:6`, `F:cm/fm/ball:2`) → `#balSrc = @s cmId`; `F:mboss/hurt` (`@s` = hazard/projectile/body; the target is always
  the single `rlk_mb_body`) → `#balSrc -1`; `F:boss/raiden/hurt` → `-2`; vanilla → `on attacker` in the advancement path.
- Every family's groggy start/end lives behind `bal/grog/start` → family dispatch: `cm` / `vanilla` / `mboss` (registry hook) /
  `raiden`.

### 4.5 Plug-in per family (fewest edits)

**Core (new `bal/**` + RP font, new generator `T:build_balance.py` that inserts its hook lines idempotently with a marker comment,
exactly like `T:build_rift.py` does with `# rift (build_rift.py)`, `R:1831`):**
- `F:mob/setup` +1 line (`bal/init`: tier from tags, exclusions, `balM`, full `balP`).
- `F:mob/tick` +1 line `execute if score @s balT matches 1.. unless entity @s[tag=boss] run function rlk:bal/tick`
  (regen, groggy countdown, immunity; bosses tick in `fight_tick` so pauses freeze them).
- `F:mob/hb_spawn` +1 summon, `F:mob/hb_cleanup` +2 lines.
- `F:combat/apply_mods` +1 line (groggy damage bonus); `F:combat/apply` +1 line only if sources 4–10 are adopted.
- `F:cm/hit_pl` +1, `F:mboss/hurt` +1 (generated by core), `F:boss/raiden/hurt` +1 (raiden generator) — attacker capture.
- `F:element/frz_end:8` guard (vanilla groggy vs freeze), `F:load` objectives/tunables, `F:uninstall` cleanup.

**cm mobs (all 3 chapters):**
- `F:cm/tick` +2 lines after `:9`: `execute if score @s balG matches 1.. run scoreboard players set #free tmp 0` and a cancel on the
  first groggy tick (mirror of `:12`). Groggy start (`bal/grog/cm`): `#cid = cmId`, `cm/cancel` (`F:cm/cancel:1-10`, removes
  `rlk_cmch`), slowness + team `rlk_stun` (body of `F:mob/stun:6-9` without its early returns), `stunT` re-asserted each groggy tick
  (overrides basic_hit 2 / c2 hurt 5), `cmCd/cmCd2 ≥ 1` while groggy (blocks the ch1 casters `F:cm/ar/tick:4` etc. without editing
  them), `cm/dr/interrupt` for drummers, `cm/hold_on`. Elites reset themselves on their next tick (cmS 0 + `rlk_c2_busy` →
  `<m>/reset`), surfacing cs and revealing nj exactly as freeze does.
- Pose: OR the freeze branch in the 22 rig ticks (`execute if score @s balG matches 1.. run return run function …/frozen`):
  ch1 hand files `F:cm/{sw,ar,fm,im,sh,cn}/rig/tick`, ch2/ch3 generators `T:ch2mob/swarm.py:64`, `T:ch2mob/elite_lib.py` `rig()`
  (`rig/tick`), `T:ch3mob/elite_lib.py:104`, ch3 swarm rig; + a groggy particle (dizzy stars) from `bal/tick`.
  Option B (nicer, more code): elites enter their own punish state with `cmT = groggy ticks` (kr cmS 3, nj 4, cc 4, cs 4, pc 7 (core
  exposed!), rv only when grounded) — they then resume through their normal `idle` path.
- Generators must stay idempotent in any order (`R:394`, `regen_all.sh --mobs`).

**Vanilla AI**: NoAI groggy (mirror `F:element/frz_on:5-6` with its own tag), slowness, restore at end unless frozen/originally NoAI.

**Registry bosses (`T:build_mboss_core.py` + `T:mboss_lib.py` + `T:mboss_registry.json`):**
- Registry field per entry, e.g. `"bal": {"pips": 12, "grog": 120, "hook": true}`; validated in `load_registry`.
- `body_setup` init; `fight_tick` +1 line (boss `bal/tick`, so `mboss/world` pauses stop it); `bars` +1 line (`bal/bu`).
- Optional module hooks, emitted only for entries with `bal.hook` (the `SPECIAL_OPT_HOOKS` technique): `bal_ok` (return 1 = may go
  groggy now; module knows its never-interrupt states) and `bal_grog` (start its own groggy using its existing stun/clip),
  `bal_end` (resume). Without the hook: framework default = immune (no pip loss) → modules opt in one by one.
  `T:check_mboss_pack.py` gets a rule: flagged entries implement the hooks; unflagged produce no lines.
- Per module (each a separate stage/worktree, owner = its generator):
  - guardian: `bal_ok` = `#gdSt` ∈ {0,2,6,8}; grog = `p/cancel` + `lib_clear` + clip `groggy_a`/`getup` for 120 t; end → `ai/enter`
    keeping the guard/chaos counters (do not call `groggy/end`).
  - butterfly: ok = `#bfSt` ∈ {0,2} and `#bfPat` ∉ {14,15,20}; grog = `test/cut` steps + clip `groggy_h` (without the form change?
    in butterfly form a fall is needed — decision), end → `ai/enter`.
  - fieldgen: ok = cruise only (`#fgField 0`, `#fgSt 0`); in the field, balance damage → meter count (or ignored); grog = `test/cut`
    + `groggy/rig` clip.
  - Arlecchino: ok = `#pat` ∈ 1–9, 11–13, 41–45, 48 or idle, not `#stun`, no window open; grog = `cancel_pat` minus `rec_start`, then
    `stun_start` with a duration parameter (`#stun_t`), end through `stun_end` without the Banquet reschedule.
  - Tachy: ok = `#pat` 0–11 (not L / blink invulnerable ticks), `#stag 0`; grog = `cancel_pat` + `#stag N` + `#taken` + clip
    `stagger` (short) or `stun` (long).
  - Scarlet: ok = `#ph` 1/7 with `#pat` ∈ {0,1–4,6,7,11–13}, no `#inv`, not ghost, no `#rp`/`#sqn`/`#rvw`; grog = `cancel_pat0` +
    a stand-in (clip `flinch` held, or `down` for long groggy — but `down` is the CS2 window; prefer a new short clip).
  - azhdaha / apep: need a new clip (rig `.mjs` + manifest + px regen) or hold `idle_p1`/`crouch_p3`; ok = `#azPat` ∈ 1–10, 41–46 or
    idle, `#azCast`/`#azBg*` cancelled too; apep `#apPh` 1/3 and `#apPid` ∈ 1–7, 31, 33–36.
  - proto / cproto / spproto: trivial hook for tests.
- **Raiden** (`T:raiden_enc/shogun.py`, `core.py`): phase 0 only → `rdSgStun 4` + `sg/stun_begin` (100 t stagger/recover),
  ok = `rdPhase 0`, `rdPat` ∉ {5,7,15,98,99}, `rdBlink 0`, `rdDeath 0`; bars line in `boss/raiden/bars`.

### 4.6 Per-tick cost

- Idle, full gauge: cm mob +2 commands/tick (`mob/tick` gate, `cm/tick` gate), vanilla +1; regen/groggy adds ~5–10 only on the
  ticks it runs; row redraw only on change. A 14-mob room ≈ +28/tick against `mob/tick` ≈ 25–30 per mob plus the cm brain.
- Boss: +1 `fight_tick`, +1 `bars`, +1 in `bossui/draw` check, +~8 for the pip row when set → ≈ +10/tick (the bars are redrawn every
  tick anyway). Budget refs: fight average ≤ Apep ≈ 830 (`R:200`; Arlecchino P1a 445 / P1b ≈ 505, `R:496-498`). **`test_m0diff` is
  already over its +6.5 budget** (`R:511-512`: proto +6.57, butterfly +6.70, fieldgen +6.98) → the user must raise that budget or
  the framework lines must be gated by a flag the mid-bosses don't set.
- Cheaper alternative worth doing alongside: make `F:mob/tick:23-26` (HP numbers macro every tick) change-driven too.

### 4.7 Tests (README 0-8, `tools/dev/sim`)

- No ch1/ch2/ch3 mob suite exists in the repo (`ch2/tests_a|b`, `ch3/tests_a|b` were not carried over, `R:425-426`) → **new suite**
  `tools/dev/sim/bal/tests/` modelled on `sim/hr/tests` (newest libs: `hrsim.py` resolves real block tags, `R:518-524`), run from a
  copy outside the datapack (`R:402-405`, sim README 1):
  - `test_bal_core`: tier init per tag (all 22 single-mob `cm/spawn/<id>` + 6 `g_*` group spawners + vanilla + exclusions), points/regen/immunity math, row redraw only on
    change, groggy damage bonus, freeze overlap (NoAI restore), uninstall.
  - `test_bal_cm`: per id: spawn, `bal/hit` to 0 → `cmS 0`, no attack start for the whole groggy (sw/ar/fm/im/cn/ns/sp/em/kr/nj/cc/
    cs/rv/pc), elites visible/surfaced, resumes, no leftover lines/targets; per-tick command delta.
  - `test_bal_boss`: per module: forced groggy only in `bal_ok` states, refused in intro/cine/transition/mechanic states, resume
    correctness, pause freezes timers, reload mid-groggy.
- Extend: `sim/ar/tests/test_arlecchino.py` (stun path, tick cost), `pat_p1/pat_p2` (cancel at every tick still clean — they already
  test "매 틱 취소"), `sim/hr/tests/test_scarlet.py` (state/stop/tick cost), `sim/az/tests_cm/test_m0diff.py` (budget),
  `test_px.py` (new clips), `gen_check.py` / `gen_check_hr.py` (generation order/idempotence with the new generator),
  `ident_hr.py`/`ident.py` (non-balance outputs byte-identical where intended), `T:check_mboss_pack.py` (hook rule), static
  checkers `check_refs` / `check_macro` / `check_nbtpath` / `lint_mc`, gates `loadcheck.sh` (negative add/remove literal kills a whole
  function, `R:242`), `rplint.py` (font ids), `atlas_px.py` (fonts are not item atlas, glyph PNGs tiny).
- In-game checks (client only): head row position over each rig (sh 1.25×, rv flying, cn), boss pip row vs line 3, glyph colours.

### 4.8 Build order (suggested)

1. D0 contract (frozen names: scores/tags/storage/font codepoints, registry schema, `bal/hit`, `bal/parry`, `#balSrc`, hook names,
   tunables) — shared with the parry researcher.
2. Core `bal/**` + `T:build_balance.py` + RP font; vanilla + dummy test target; `test_bal_core`. Loadcheck / rplint.
3. cm integration (cm/tick, hit_pl, ch1 rig ticks by hand, ch2/ch3 generators, `regen_all.sh --mobs`); `test_bal_cm`.
4. Boss bar row in `T:build_bossbar.py` (option reset → byte-identical for non-users).
5. mboss framework in `T:build_mboss_core.py` + `mboss_lib` + registry + `check_mboss_pack`; `test_m0diff` budget decision.
6. Modules in parallel worktrees (max 3 at a time, `R:295-299`): Arlecchino / Tachy / Scarlet (have stun clips) first, then guardian /
   butterfly / fieldgen, then azhdaha / apep (new clips → rig + px regen), test bosses; then Raiden.
7. Parry pipeline hookup (`bal/parry`), sources 2–12 the user picked.
8. Balance probe pass (`sim/ar/review/bal` style), README §5 / boss sections / 0-x, release gates (`R:185-224`).

### 4.9 Decisions for the user

- Mid-bosses 12 pips like chapter bosses? Cicins / Apep org creatures / lobby dummies get a gauge?
- Groggy damage bonus (and per tier), finisher yes/no and its input.
- Raiden Tenma phase: groggy, armour chip, or immune.
- Fieldgen field: balance → 20-hit meter?
- Scarlet A8/A13: should a perfect parry also break a shield cell?
- Which extra balance sources (table 3) and their weights.
- Generic hold pose vs elite punish-pose reuse vs new groggy clips (azhdaha/apep need a clip either way for a good look).
- Boss pip row under the HP bar (5 px band) vs above it (8 px band).
