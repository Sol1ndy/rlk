# Mid-boss (중간보스) module contract

Worktree: `wip/mb-core`. `DP` = `roguelike/`, `F:` = `DP/data/rlk/function/`. Everything here is implemented and
was exercised in an offline simulator (hazard geometry, roll, lifecycle, pause, cancel, reload, out-of-bounds).
A boss module is a set of functions `F:mboss/<id>/*` written by its own generator `tools/build_mboss_<id>.py`
(model: `tools/build_mboss_proto.py`, the placeholder boss "proto").

---------------------------------------------------------------------------------------------------

## 1. Files and generators

| file | owner | role |
|---|---|---|
| `tools/mboss_registry.json` | hand-edited | single source: arena constants + one entry per boss |
| `tools/mboss_lib.py` | hand-edited | side-effect-free helpers: `load_registry`, `enabled_bosses`, `Out` (owned-dir writer with macro-line assertions), `HOOKS`, colour tables, call builders `hz_disc/ring/sector/line/full`, `hz_opts`, `say`, `sound` (vanilla `hostile` playsound; minVolume per layer `min_volume(vol)` = vol / 3 capped at 0.4, 0 for layers <= 0.25, so loud hits carry past their 16 x vol range and quiet layers fade), affine matrices for display rigs |
| `tools/build_mboss_core.py` | generator | everything in `F:mboss/` except `arena/` and the module dirs: registry, roll, gate, start/won, reward item boxes `box/*`, teleports, world tick, pause, bars, lines, dispatchers `d/*`, libraries `hz pj pull mv aux`, true damage, tests |
| `tools/build_mboss_arena.py` | generator | `F:mboss/arena/{ensure,build,build_<theme>,rebuild,clear}`; `layout()` is importable for renders |
| `tools/build_mboss_proto.py` | generator | `F:mboss/proto/**` (test boss) |
| `tools/check_mboss_pack.py` | checker | hooks present (macro/non-macro), dispatcher targets, literal and `$(n)` function families, `$` discipline, arena version |

Build order (any order works; all are deterministic):
```
python3 tools/build_mboss_core.py && python3 tools/build_mboss_arena.py && python3 tools/build_mboss_<id>.py ... && python3 tools/check_mboss_pack.py
```
`build_mboss_core.py` must be re-run whenever the registry changes (it bakes the registry, the dispatchers and
the arena constants). Never hand-edit generated files.

## 2. Registering a boss

Add an entry to `tools/mboss_registry.json` `boss[]`:

| field | meaning |
|---|---|
| `id` | module directory name `F:mboss/<id>/`, tag `rlk_mb_<id>` on the body |
| `n` | stable numeric id (1..9999) used by the generated dispatchers (`#mbId mb`); never reuse |
| `enabled` | `false` keeps the entry out of the game (no runtime registry, no dispatch). The Guardian entry (`n 1`) ships disabled; flip it to `true` when `F:mboss/guardian/` has every hook |
| `w` | roll weight. `0` = reachable only through `#mbForce` (tests). The 중간보스 node is offered only while at least one enabled entry has `w >= 1` (`#mbRoll mb`) |
| `minCh` / `maxCh` | chapter range for the roll |
| `name`, `sub`, `color` | HP bar / gate / titles (`cur.title` = `{text:name,color,bold:true}`) |
| `el` | default element of the boss's hits (`#elem` numbering 0 phys 1 pyro 2 hydro 3 electro 4 cryo 5 geo 6 anemo 7 dendro) |
| `hp`, `xp` | level-1 base HP and kill XP (`room/mob_init` → `mboss/base_stats`); level = zone formula + `lvAdd` |
| `atk` | base hit (raw damage before the hit coefficient); `dmgMul` % applies to every hit on the player |
| `goldMul`, `sap` | kill gold multiplier (normal ×1, chapter boss ×15) and sapphire shards |
| `picks` | item boxes dropped on kill (default 2); each box, when first clicked, grants one chapter-rarity item selection without character cards and stays (opened) until that selection is used |
| `scale` | body husk `scale` attribute; `hit {w,h}` click-shield size |
| `intro`, `death` | maximum ticks of the intro (untargetable) and of the death sequence |
| `deathSnd` (optional) | `true` (default): `mboss/death_start` plays the generic death roar (`entity.wither.death`); `false`: no framework death sound, the module composes its own (the Guardian: non-vocal stings only) |
| `icon {item,model}` | gate object display |
| `start` (optional) | arrival spot `{x,y,z,yaw,pitch}`, default `arena.start` (200.5 201 25.5, facing north) |

Arena (`arena`): theme `plaza` ver 2, centre corner (200, 201, 8), radius 22, walk 21 (wall ring beyond),
safe 19 (leash / movement clamp). Stand height y 201 (floor blocks y 199-200). Floor: calcite marble, three faint
white-concrete grooves, a rose four-point star (long thin points, thin crimson outline) and eight slender rose
blades swirling around it, detached from the star (bumping `ver` makes `arena/ensure` rebuild it). Its chunks
(forceload 176 -16 223 31) are forceloaded by `load`, `room/setup` and, if they are ever missing, `mboss/start`.

## 3. Lifecycle (who calls what)

```
zone kind 15 entered ─ room/obj/k_mboss: mboss/roll (rlk:mboss cur, #mbId) → gate object (oact 14) named after cur
gate clicked ─ mboss/gate: room/combat_start (#combat = zid), #spawnT 30, title cur.title / cur.sub
#spawnT 0 ─ room/mob_wave → mboss/start (as the zone marker):
     arena not loaded → start_unloaded: forceload again, retry every 10 t, 7th miss = cancel (start_cancel)
     living player (else #spawnT 10 retry) → #mbLive 1 → cleanup_aux → fight_vars → arena/ensure
     → summon rlk_mb_arena marker → d/spawn (as the marker) → verify a body exists
        (no body: retry 10 t later, 3rd failure = start_cancel through room/combat_clear, no reward)
     → ret_save (rlk_safe) → met += id → #mbOn 1, #mbSt 0 → player tp to cur.start (+ view/sync, rlk_safe) → bars
every tick ─ rlk:tick → mboss/main only while #mbLive mb is 1 (start / reload set it; cleanup_fight clears it;
     main itself clears it, with cleanup_aux + bars_hide, the first tick no body exists) → mboss/world:
     pause gate → resume edge → out-of-bounds → mv/all → body_tick:
        #mbSt 0: d/intro_tick, intro_end forced at cur.intro
        #mbSt 1: d/tick, then mv/leash unless #mbNoLeash mb 1
        #mbSt 2: d/death_tick, death_finish at cur.death
     → hz/all → pj/all → pull/all → bars (states 0-1) → line/tick
     (each */all runs only while its flag #mbMvOn/#mbHzOn/#mbPjOn/#mbPlOn is 1: the create call sets it, every
      live entity's tick keeps it, so the selector scan stops one tick after the last one is gone)
lethal hit ─ combat/apply pays heal orb / XP / gold, then mboss/death_start (instead of kill):
     tags rlk_mb_dying + rlk_mb_inv, mhpC 0, #mbKilled 1, #mbSt 2, lib_clear, bars hidden, d/death_start
     (from then on hz/make, pj/launch and pull/start refuse, so nothing a module still creates in that tick lingers)
death_finish ─ kill body → room/combat_tick sees no rlk_zmob → room/combat_clear → mboss/won (as the zone marker):
     absorb arena gold → cleanup_fight (d/cleanup, aux, arena sweep, bars, line) → tp back to ret (+ view/sync, rlk_safe)
     → #mbKilled 1: reward (kill title, subtitle "아이템 상자 N개", no sound, NO screen) → box/drop_all: cur.picks chests
        fall onto the gate spot      else: "취소" message + gate re-created
     → forget (cur, ret, #mbId)
reward boxes ─ box/drop_all (as the zone marker): row across the zone→player line (yaw snapped to the room axes), 1.5 b
     apart, latch toward the player → box/drop per box: item_display minecraft:chest ×1.1, rlk_room rlk_mb_box rlk_mb_boxfall,
     6 b up, 4 t stagger, #mbBoxOn mb 1
every tick ─ room/tick → mboss/box/all only while #mbBoxOn (reset there, kept by every box) → box/tick → box/fall: stepped tp
     14 t (teleport_duration 1, light acceleration, ease-out quarter turn), trail; landing tick: box/land (thud, puff,
     squash) → room/obj/k_mbox at the floor (marker oact 15 + label/hint; the display joins the group) → idle shimmer
box clicked ─ room/obj/click (refused in combat) → room/obj/do_mbox:
     closed box: pkMb +1, lvup/add {n:1}, box/open (rlk_mb_boxopen on the whole group, oarg = open age: the new box 1,
        older opened boxes +1; chest Glowing + glow_color_override 0xFFD24A; label "아이템 상자 / (열림) / 다시 눌러 선택"),
        lvup/toggle unless pkMode ≥ 1
     opened box: lvup/toggle only (no pick; the offer stays: rlk:lvpick choices is kept by lvup/exit and toggle rolls
        only when it is empty, so backing out is never a free reroll); with no pkMb left (guard) box/gone, no pick
pick used ─ lvup/act/resolve on an mbSet with pkMb ≥ 1 (choose, skip, swap): box/spend (as the player) before pkMb -1:
     the opened box with the highest oarg (= opened first) → box/gone at its marker (chest open + chime played at
     the player, who is in the selection screen 40+ b away; gold dust, end rod, poof at the box; room/obj/kill_group).
     No opened box (its room was left, the pick stayed pending): nothing.
     Invariant: opened boxes ≤ pkMb ≤ pkPending. The state lives only on the box entities (no global counter), so
     room/clear (map change, run end, death), wipe and uninstall leave nothing behind; an unused pick stays pending
     (Shift+F). Unopened boxes go with every other rlk_room entity.
```
State: `#mbLive` (fight entities may exist: world tick runs), `#mbOn` (fight entered), `#mbSt` (0 intro / 1 fight / 2 dying), `#mbT` (clock of the current state,
1 on the first tick of the state), `#mbPause`, `#mbKilled`, `#mbId`, `#mbLv` (body level), `#mbEl`, `#mbAtk`,
`#mbDmgMul`, `#mbGoldMul`, `#mbSap` (all in objective `mb`).

## 4. Hooks (`F:mboss/<id>/<hook>.mcfunction`, all required; empty stubs are fine; 17 hooks)

| hook | called from | executor / position | contract |
|---|---|---|---|
| `spawn` | `mboss/start` via `d/spawn` | the arena marker at (200, 201, 8), rotated 180 (north) | call `function rlk:mboss/body` at the wanted spot with the wanted yaw (`execute positioned … rotated … run …`), then build the rig/fx. Exactly one body |
| `intro_tick` | world, `#mbSt 0` | body, at body (rotation = body) | entrance. Call `function rlk:mboss/intro_end` when done (the shell forces it at `cur.intro`). The body is untargetable (`rlk_mb_inv`) |
| `tick` | world, `#mbSt 1` | body, at body | AI, rig, own timers; may use every library. A lethal `true_hit`/`true_pct` (star break) runs `death_start` and your `death_start` **before it returns**: right after such a call put `execute unless score #mbSt mb matches 1 run return 0` so the rest of the tick does not drive a dying body (proto: `tick` after `star_tick`) |
| `on_hit` | `combat/apply` (body hit, not true damage) | body | `#elem #elU #rx #tfm #dmg #crit` known. **Scores/flags only**; never call `combat/apply` or spawn hazards here |
| `aux_hit` | `mboss/aux_hit` (aux with `rlk_mb_hit` hit inside `combat/apply`, after reactions and `combat/apply_mods`: engravings, items, level factor, Ronova, its own `mres`, exactly like a body hit) | the aux | adjust `#dmg tmp` (e.g. 0 = immune → "면역" popup) or take over with `scoreboard players set #mbAuxDone mb 1`. Default afterwards: `#dmg` off the aux's `mhpC`, number, `rlk_mb_broken` + `#mbAuxBroke mb +1` at 0. Flags only |
| `incoming` | `combat/apply_mods` (after items, level factor and `mres`) | body | change `#dmg tmp` (groggy bonus, shields …) |
| `pause` / `resume` | world, on the pause edges | body | optional (everything is frozen anyway); drop what would hang in the world meanwhile (e.g. screen layers in front of the eyes) |
| `death_start` | `mboss/death_start` | body | stop own mechanics, death clip, line. Libraries are already cleared |
| `death_tick` | world, `#mbSt 2` | body, at body | death animation; the shell kills the body at `cur.death` |
| `cleanup` | `cleanup_fight` (won, cancel, run end, map change, wipe, uninstall, test stop) | none (server) | reset own fake players; must be idempotent. Own entities die with `rlk_mb_aux` |
| `reload` | `mboss/reload` after `/reload` (aux entities are already dead, arena marker re-summoned) | body, at body | reset AI to idle, rebuild rig, keep HP |
| `bars` | `mboss/bars` every tick (states 0-1) | body | fill `#buSub #buSubMax #buSubCol bu` (under-bar; 0 colour = none) and optionally `rlk:mboss extra` (name-line suffix) / `rlk:mboss sub` (third line) |
| `hz_vis` | `hz/init` / `hz/strike` / `hz/expire` (also through `hz/cancel`) for hazards with `#hzVis` ≥ 1 | the hazard marker, at it (rotation = aim, always) | `#hzEv mb` 0 create / 1 strike / 2 end; `@s mbHzV` visual id, `@s mbHzI` hazard id. Tag your decals `rlk_mb_hzfx` + `rlk_mb_aux` + `rlk_room` |
| `pj_end` | `pj/*` | the prop | `#pjEv mb` 1 wall / 2 life over / 3 back at the body (or its return time ran out) / 4 hit the player. `#pjKeep mb` is preset to the default and you may flip it: ev 4 preset 1 = the prop pierces and flies on (harmless, one hit per prop), 0 = removed at once; ev 1/2 of a `#pjRet 1` prop preset 1 = it turns and flies back, 0 = removed; ev 1/2 of other props and ev 3 preset 0 = removed, 1 = kept as a plain entity (stops being a projectile) |
| `test` | `/function rlk:mboss/test/pattern {id:N}` via `d/test` | the player | macro `{id}`; meaning is the module's (proto: 1..7 pattern, 90 star) |
| `uninstall` | `mboss/uninstall` (from `rlk:uninstall`) via `d/uninstall`, which calls **every enabled module** (none is running) | none (server) | remove what the module itself created beyond `mb` and `rlk_mb_aux` (Guardian: `rig/uninstall` = parts, props, `gdRig*` objectives); proto: empty |

Module rules: tags `rlk_mb_<id>_*` and, on every entity, `rlk_mb_aux` + `rlk_room` (+ `rlk_mb_part` for rig
displays; select them with `type=`); fake players with your own prefix in objective `mb` (proto: `#pr*`,
Guardian: `#gd*`); no writes to `rlk:room` storage; positions from the arena marker `@e[tag=rlk_mb_arena]` or the
registry constants, floor at y 201; read `#mbLock mb` (test lock) in the pattern choice.

## 5. Libraries

Units at the runtime boundary: distances in **tenths of a block** (r:50 = 5 b) unless a key says otherwise,
ticks, damage as **% of the base hit** (dmg:160 = 1.6 × `atk`). Python helpers in `mboss_lib` take blocks.

### 5.1 Body, states
- `function rlk:mboss/body` — at the spawn point; NoAI/NoGravity/invisible husk with `rlk_room rlk_zmob rlk_newmob
  rlk_m_mboss boss miniboss rlk_mb_body rlk_mb_<id> rlk_mb_inv`, `mob_init` stats from the registry, `mob/setup`,
  knockback immunity, `scale`, click shield `hit {w,h}`. Move it only with `tp`/`mv`. `boss` gives stun/freeze/
  knockback immunity; `miniboss` switches the economy to `goldMul`/`sap`.
- `function rlk:mboss/intro_end` — callable from anywhere; removes `rlk_mb_inv`, `#mbSt 1`.
- Untargetable on demand: `tag @e[tag=rlk_mb_body] add rlk_mb_inv` (no click shield, `combat/apply` ignores
  everything but true damage); remove it yourself.

### 5.2 Ground hazards (`hz`)
Call as anything, **positioned on the floor point, rotated = aim** (pitch ignored); the aim is locked at creation.
| call | shape |
|---|---|
| `function rlk:mboss/hz/disc {r,tell,dmg}` | filled circle |
| `function rlk:mboss/hz/ring {r0,r,tell,dmg}` | annulus (hole safe); jumpable wave: `#hzY1 7` |
| `function rlk:mboss/hz/sector {r,a,tell,dmg}` | sector, half-angle `a` degrees 1..180 (180 = full 360 swing); arc with option `#hzR0` |
| `function rlk:mboss/hz/line {len,w,tell,dmg}` | rectangle forward `len`, full width `w`; `#hzBack` starts it behind |
| `function rlk:mboss/hz/full {tell,dmg}` | whole arena; `#hzR0` = safe circle around the call point |

`tell` = ticks of telegraph; the hit is tested from age `tell` for `#hzAct` ticks, at most once (a dash dodge also
consumes it). One-shot options (fake players in `mb`, set just before the call, reset after it):
`#hzAct` (1) active ticks · `#hzEl` (-1 = boss el) · `#hzKB` (3) knockback steps · `#hzKBDir` (-1 = shape default:
along the aim for lines, away from the origin otherwise; 0 away from the hazard origin, 1 along the aim, both
honoured for every shape) · `#hzY0/#hzY1` (-5/35) height gate in tenths relative to the
hazard y · `#hzR0` · `#hzBack` · `#hzSfx` (1 slam, 2 slash, 3 thrust, 4 heavy, 0 none) · `#hzVis` (0 = framework
particles only; ≥1 = also call your `hz_vis`) · `#hzCol` (-1 = element colour; 0..8 element palette, 9 white,
10 green) · `#hzLinger` (8) · `#hzQuiet` (1 = no particles). After the call `#hzLast mb` = the hazard id
(`@s mbHzI`; 0 when refused because the boss is dying); `function rlk:mboss/hz/cancel` cancels the hazard whose
id is in `#hzLast` (your `hz_vis` gets event 2 with the hazard's own rotation).
Hit test: body feet (`rlk_body`), never the camera, with a 0.3 b body pad on the dangerous side; telegraph =
particle outline + a progress outline that reaches the rim at the strike, every 4 ticks; strike = white flash.
Python: `L.hz_opts(el=5, sfx=2) + [L.hz_sector(5.5, 75, 16, 130)]`.

### 5.3 Damage to the player
`function rlk:mboss/hurt` as the attacker (it is the knockback source). Inputs: `#mbHitPct mb` (coefficient %),
`#cmEl tmp` (element), `#mbKB mb` (steps, 0 none), `#mbKBDir mb` (0 away from @s, 1 along @s's yaw). Raw damage =
`atk × pct × dmgMul / 10000`, then `cm/hit_pl2` → `player/take_damage` (dash i-frames → `#dodged tmp 1`, defence,
level scaling by `#mbLv`, element on the player, item/engraving shields). Refused while the player is dead, in
Ronova revival, on a selection screen, or the boss is dying. Hazards and projectiles call it themselves; direct
swings must handle one-hit-per-swing themselves.

### 5.4 Projectile props (`pj`)
Summon your prop (display/marker) tagged as you like, then as the prop, positioned at the launch point, rotated =
flight direction (pitch counts): `function rlk:mboss/pj/launch {spd,life,dmg,hr}` — `spd` tenths/tick (0.25 b
sub-steps), `life` ticks, `dmg` % (0 = visual only), `hr` hit radius tenths (1..40). Options: `#pjEl`, `#pjKB` (2),
`#pjRet` (1 = fly back to the body at the end), `#pjWall` (1 = stop at non-`#rlk:cm_pass` blocks). Events → `pj_end`
(see §4 for `#pjKeep`). A returning prop steers at the body's eyes at its own speed and arrives when it touches the
body's hitbox (event 3); the return leg is capped at the outward flight time + 40 t (then event 3 wherever it is),
so a fast-moving body cannot strand it. The return leg never hurts. Refused while the boss is dying (the prop is
killed).

### 5.5 Pull (`pull`)
`execute store success score #ok mb run function rlk:mboss/pull/start {t:N}` as anything positioned at the
destination (e.g. `positioned ^ ^ ^1.6` in front of the body, y 201). Glides the player's body over `t` ticks
(0 = instant), collision-checked like knockback, not cancelled by dashing; refused (fail) while dead / reviving /
selecting / map view / the boss is dying. `#pullFace mb 1` (default) turns the player to the boss at the end. Line of sight and tells
are the module's job.

### 5.6 Movement (`mv`, as the entity to move)
- `mv/glide {t}` / `mv/leap {t,h}` — positioned at the destination; straight / parabolic (apex `h` tenths) over `t`
  ticks; ticked by world before the body tick; `mv/stop` cancels. Works on any entity.
- `mv/face`, `mv/turn {max}` (degrees per call), `mv/step {d}`, `mv/toward {d}`, `mv/away {d}` (`d` in **blocks**,
  decimal) — steps only into free cells inside the safe disc (`mv/ok`).
- `mv/leash` — automatic each fight tick: beyond safe+1 slide back 0.45 b/t, beyond walk+2 back to the centre;
  disable with `#mbNoLeash mb 1` during scripted flights. `mv/home`, `mv/clamp` (pull a marker inside the safe disc).
- `mv/dist` → `#mbDist mb` horizontal distance to the player body in tenths. Range bands are cheaper with
  `if entity @e[tag=rlk_body,distance=..4]`.

### 5.7 Helper objects (stars) and true damage
- `scoreboard players set #auxHpPct mb P` (pool = P % of the body's max HP, 1..100, so it scales with the boss level
  and chapter; preferred) or `#auxHp mb N` (fixed pool, used when `#auxHpPct` is 0), + `#auxRes mb R`, then
  `function rlk:mboss/aux/spawn` at the spot: invisible NoAI husk `rlk_room rlk_mb_aux rlk_mb_hit boss rlk_mob`,
  overhead HP bar, click shield, boss level, own `mhpC/mhpM` pool, `mres` R; never `rlk_zmob`. The new one carries
  `rlk_mb_auxlast` until the next spawn — add your tags and visuals. It receives auras and reactions (refresh a
  permanent aura in your tick: `scoreboard players set @s aThunder 1000` + `elAct 1`). Player hits route:
  `combat/apply` → reactions → `combat/apply_mods` (the same engravings, items, level factor, Ronova boost and RES as
  a body hit) → `mboss/aux_hit` → your `aux_hit` → default pool. Act on `rlk_mb_broken` in your tick (kill it,
  punish the boss).
- Sizing (K8): because star hits are modified exactly like body hits, a pool of P % breaks in P % of the body's kill
  time T (seconds of full damage), corrected by the RES difference: break time t = P/100 × T × f_body / f_star, with
  f = the RES factor above (×0.238 at R 80, ×1 at R 0). Two stars in about 11 s → per star P ≈ 100 × 5.5 / T ×
  f_star / f_body. Example T 90 s, body R 0: inert star (R 80) P ≈ 1.5, active star (R 0, hit with other elements) P ≈ 6.
  (The Guardian's active stars take their own element at 40 % RES, ×0.6 in its `aux_hit`, not the mres curve: see
  gd_contract.md §9.)
  Measure T with `test/start` + a typical character and keep the result in the module generator.
- `function rlk:mboss/true_hit` as the target (`#mbTrue mb` damage, `#mbTrueEl mb` number colour) or
  `function rlk:mboss/true_pct {pct:N}` (N % of max HP, overflow-safe): goes through `combat/apply` (kill, rewards,
  death) but skips elements, modifiers, RES and module hooks. Never from inside `combat/apply`. A lethal one runs
  the death sequence before it returns (see the `tick` hook rule in §4).
- `mres` (objective, %): generic Genshin RES in `combat/apply_mods` (R ≤ 75: ×(100−R)/100, R > 75: ×100/(100+4R),
  R < 0: ×(100−R/2)/100). Set it on the body or on aux objects; 0/unset = none.

### 5.8 Bars and lines
- Bars (three white RP bars): `rlk:mboss` = `Lv.N name` + aura glyphs of the body + `rlk:mboss extra[]`;
  `rlk:mboss_state` = bossui HP bar (fills over 1.5 s in the intro) with the under-bar from your `bars` hook
  (`#buSubCol` codes: 1 electro 2 pyro 3 hydro 4 cryo 5 geo 6 anemo 7 dendro 8 gold 9 green; convert `#elem` with
  `scoreboard players operation #mbE mb = …` + `function rlk:mboss/elem_to_bu`); `rlk:mboss_sub` = `rlk:mboss sub[]`
  (text components; persists until you change it; reset at fight start/end). Hidden on death/dead player/cleanup.
- Typed subtitle: `function rlk:mboss/line/say {t:"…",c:"#RRGGBB",gap:2,hold:40,snd:1}` (two characters per step,
  quiet tick, `snd` 0 none / 1 soft / 2 stern sting). Python `L.say(text, colour, gap, hold, snd)`.

## 6. Timers and pause
Pause = player dead, Ronova revival (`rnDie`), selection screen (`pkMode`), or no `rlk_body`. While paused the world
returns before the out-of-bounds guard, the body tick, `mv`, `hz`, `pj` and `pull`: **everything freezes** (module
timers in the body tick, hazard ages, projectiles). `d/pause` / `d/resume` fire on the edges. Bars hide while the
player is dead. Lines keep typing unless the player is dead. Keep all module timers inside the body tick so they
freeze too. `#mbT` counts per state; module pattern clocks are the module's.

## 7. Tests
`/function rlk:mboss/test/start {id:"proto"}` (chapter 1) or `test/start_ch {id:"proto",ch:2}`: needs `player` tag,
`room/setup`, no run, difficulty ≥ easy. Builds a real node map with zone 15, presses the gate. Then
`test/kill` (lethal true hit = reward path), `test/abort` (`/kill`-style cancel, no reward, gate returns),
`test/pattern {id:N}` (module hook), `test/lock {id:N}` (`#mbLock`, 0 unlocks), `test/level {lv:N}`,
`test/stop` (run end + lobby), `test/arena` (rebuild + look, outside a run), `test/help`. Player death in a test
returns to the lobby without failing the character. Full node path: `/data modify storage rlk:room next set value
[15]`, `/scoreboard players set #mapType room 1`, `/function rlk:run/next_map` (needs a rollable boss).

## 8. Engine hook points (hand-edited, outside F:mboss)
`combat/apply` (dying/inv returns, `#trueDmg` gates, aux route, body `on_hit`, `apply_mods`, `death_start`) ·
new `combat/apply_mods`, `combat/res*` · `combat/clear_atkflags` (`#trueDmg 0`) · `combat/gold_drop` (boss economy
skips `miniboss`; `#mbGoldMul`, `#mbSap`) · `mob/setup` (knockback, no overhead bar for the body) ·
`mob/shield_ensure` (no shield while `rlk_mb_inv`, size from `cur.hit`) · `mob/vanilla_hit`, `mob/knock`
(body/aux immune) · `mob/tick` (dying) · `room/mob_init` (`base_stats`) · `room/zone_enter`, new
`room/obj/k_mboss`, `room/obj/click` (oact 14 gate, oact 15 item box), new `room/obj/{k_mbox,do_mbox}` (item box object
and click: open / reopen), `room/tick` (`mboss/box/all` while `#mbBoxOn`), `room/mob_wave`, `room/combat_clear`, `room/zone_patch`
(red terracotta) · `room/node/register` (k15, weight 7), `room/node/cand_loop` (chapter rule, `#mbRoll`) ·
`room/clear`, `room/wipe`, `room/remove` (releases the arena forceload), `room/setup` (adds it back) · `run/start`,
`run/end`, `player/hook_respawn` · `lvup/roll`, `lvup/act/resolve` (`pkMb`; `mboss/box/spend` when an mbSet is used),
`lvup/init` (`pkMb`) · `tick` (`mboss/main` while
`#mbLive`, `bars_hide` otherwise), `load` (forceload 176 -16 223 31, `mboss/init`), `uninstall` ·
`tools/build_minimap.py` (kind 15 colour, hidden while `#mbOn`).

## 9. Notes for the Guardian module
- Registry entry `guardian` (n 1) is enabled: hp 250, xp 30, atk 12, dmgMul 110, goldMul 5, sap 1, el 5, scale 1.5,
  hit 1.6×3.4, intro 90, death 90 (raised for the entrance and death clips; see gd_contract.md §6).
- Star break punishment = `true_pct {pct:6}` then `{pct:18}`; follow each with `execute unless score #mbSt mb matches 1
  run return 0` (the 18 % one can kill, and groggy must not start on a dying body). Inert stars = `aux/spawn` with
  `#auxRes 80`; pools with `#auxHpPct` per §5.7; active stars take their own element at 40 % RES (×0.6, at least 1) in
  `aux_hit`, and a hit that is still 0 is swallowed so no "면역" popup shows (user decision); record counting in
  `on_hit` (flags only).
- Hover with the body: the rig may hover but keep the body (hitbox) reachable; use `#mbNoLeash` during flights.
- Fail spears / P5 slam / P3 slam = `hz/disc`; P1/P2 = `hz/line`; P4 swings = `hz/sector a:180`; P6 sweeps =
  `hz/sector a:100`; pull = `pull/start`; javelin prop = `pj/launch` with `#pjRet 1` (K23: damage from the line hazard,
  the prop `dmg:0`). Telegraph rule (10-20, plan.md): every Guardian hazard is `#hzQuiet 1`; the only ground telegraphs
  are the module's own P3 ring (`#hzVis 31`), P5 ring and fail-spear star, as in the footage (gd_contract.md §6).
