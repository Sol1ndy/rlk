# 아를레키노 (chapter-4 boss) — D0 contract (frozen)

Branch `wip/ar-d0`, commit **eb0a38a** (parent = release head fc21fe4, stamp 10-30d). Design: `S:ar/PLAN.md` (§ numbers
below refer to it). Source of truth for every number / name: **`tools/mboss_arlecchino/api.py`** (import it; never copy
values). This file is the prose around it. Changes only through a request file `S:ar/requests/<stage>.md` (what, why,
who is affected); the lead applies requests at integration (I1). `S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`.
User decisions recorded at D0: the real game's Banquet banner is shown, adapted to "일반 공격" (the standing rule allows
messages the real game shows); forced bonds drop heal orbs; scale 1.4 × the player avatar.

## 0. What D0 committed
| file | content |
|---|---|
| `tools/mboss_registry.json` | entry `arlecchino` (n 12, `kind:"chapter"`, `fn:"boss/arlecchino"`, `ch [4]`, **`route:false`, `enabled:false`**, `px:false` + `shield:true`, `hit {w:1.2,h:2.9}`, `scale 1.4`, `res {"*":10}` (no Pyro resistance), `phases [64,36]`, music 1 `music.nether.crimson_forest` `len 0` until S1 measures the pool, music 2 `music.dragon` 6883, icon vanilla `netherite_hoe` until the kit exists) + 2 `_doc` lines. **No `arenas.fl_ruins` yet** (S1 adds exactly `api.ARENA_SPEC`) |
| `tools/mboss_lib.py` | a **disabled** chapter entry may name an arena not yet in `arenas{}`; a routed chapter entry (`route` true with `ch`) must have its arena. Nothing else changed |
| `tools/mboss_arlecchino/__init__.py` | package doc + ownership |
| `tools/mboss_arlecchino/api.py` | the frozen API (sections 1–9; `python3 tools/mboss_arlecchino/api.py --write-stub` = lead only) |
| `tools/mboss_arlecchino/stub_rig_manifest.json` | the D0 rig manifest (schema 1, source stub): 26 parts with parents and models, 41 clips (id = order, len, loop, events, form), looks, arm layout, anchors, calls |
| `tools/mboss_arlecchino/{seq,p2}.py` | empty stubs (`SERVICES = []`, `PATTERNS = []`) owned by S2 / S4 from now on |
Checked at D0: every registry-reading Python generator (core, arena, cboss rooms, proto, cproto, spproto, guardian,
butterfly, fieldgen, az / ap / tk kits `--skip-rp`, azhdaha, apep, rift, tachy) regenerates **byte-identical** outputs
(`git status` clean but for the D0 files); `check_mboss_pack.py` 0 problems; `bash S:mcsrv/loadcheck.sh … ar_d0` →
**0 function load failures**. The JS rigs read only their own registry entries (unchanged).

## 1. Ownership (write / delete only your own; tests and scratch under `S:ar/<stage>/`, `S:ar/tests/`)
| stage | repository files | generated outputs |
|---|---|---|
| **S1** framework + arena + routing | `tools/build_mboss_core.py`, `tools/mboss_lib.py`, `tools/mboss_registry.json` (arena entry + music len only), `tools/check_mboss_pack.py`, `tools/build_cboss_rooms.py` (only if needed), new `tools/mboss_arena_fl_ruins.py`, README rows of "챕터 보스" (routing, FN-1, px:false chapters, arena) | everything the core writes (`F:mboss/**` except module trees, `F:boss/test/**`), `F:mboss/arena/fl_ruins/**`, `F:room/cboss/arlecchino/**` |
| **S1K** kit | new `tools/build_mboss_kn_fx.py`, `tools/mboss_kn_fx_paint.py`, `tools/mboss_kn_fx_manifest.json` (generated) | `F:boss/arlecchino/fx/**`, RP `assets/rlk/{textures,models/item,items}/mboss/kn_kit/**` + atlas entries, font `rlk:mboss_kn` (+ `textures/font/mboss_kn/*`) |
| **S2** rig + sequences | new `tools/build_arlecchino_rig.mjs`, `tools/arlecchino_{pose,geometry,paint,clips}.mjs`, `tools/arlecchino_skin_p2.mjs`, `tools/arlecchino_rig_manifest.json` (generated), `tools/arlecchino_rig_api.md`, `tools/mboss_arlecchino/seq.py` | `F:boss/arlecchino/rig/**`, RP `mboss/arlecchino/**` + atlas entries; `F:boss/arlecchino/seq/**` (written by S3's generator from `seq.py`) |
| **S3** core, AI, bond, phase 1 | new `tools/build_mboss_arlecchino.py`, `tools/mboss_arlecchino/{core,ai,bond,p1,s3lib}.py` (+ more S3 modules if needed, named in the request log) | `F:boss/arlecchino/**` prefixes of `api.OWN['S3']`: the 17 hooks, `prep`, `init`, `core/ ai/ bond/ hud/ test/ rig_stub/ gate/`, `p/<key>/` for `api.P1` = a2 a4 a5 b1 b2 c1 c2 d1 d2 e1 f1 g1 h1 e70 |
| **S4** phase 2 | `tools/mboss_arlecchino/p2.py` | `F:boss/arlecchino/p/<key>/**` for `api.P2` = q0 q1 q2 q3 q4 q5a q5b q6 (written by S3's generator) |
| lead (D0 / I1) | `api.py`, `stub_rig_manifest.json`, `__init__.py`, this file | registry `enabled` + `route` true, icon model, merges, README boss section |
Shared-file edits outside this table are forbidden; if one is needed, write a request. The player avatar files
(`tools/build_player_rig.mjs`, `tools/player_motion/**`, `F:char/**`, `F:player/**`) are **read-only** for everyone.

## 2. Names (api §5–6)
- Module state: objective **`kn`** (dummy; S3 creates in `boss/arlecchino/init`, removes in `uninstall`). Core fake
  players `api.CORE_FP` (`#ph #pat #pt #done #clk #rigc #rigt #sq #sqdone #bonded #given #shock #shk_hit #brk #stun #stun_t
  #e70 #win #sch_f #sch_q5 #lines #last #last2 #rear #far #dec #rec #fl #tst #lock #dot_t #orbs #q0_ok`); a pattern
  `#<key>_<x>`; sequences `#sq_<x>`.
- Rig objectives `knRig*` (S2's `rig/init` / `rig/uninstall`); kit objectives `knFx*` (S1K's `fx/uninstall`).
- Tags (`api.TAGS`): `rlk_kn_part` (rig parts), `rlk_kn_prop` (rig props: cup, saucer), `rlk_kn_anchor` (rig anchor
  marker), `rlk_kn_fx` (kit cards), `rlk_kn_orb` (heal orbs she dropped, added right after `combat/heal_orb_spawn`),
  `rlk_kn_p` + `rlk_kn_p_<key>` (pattern markers), `rlk_kn_win` (body inside a break window), `rlk_kn_stun` (body
  stunned). Everything spawned in the world also carries `rlk_room rlk_mb_aux`.
- Storage `rlk:kn` keys `core.*` (S3), `rig.*` (S2), `fx.*` (S1K), `p2.*` (S4), `seq.*` (S2).
- UUIDs: rig parts `524c4b4d-4b4e-4100-8000-0000000000NN` (NN 00–25 = `api.PARTS` order), shadow `…40`.
- Resource ids (lowercase only): `rlk:mboss/arlecchino/*` (rig: P2 skin + parts, wing / leg cards, cup, saucer),
  `rlk:mboss/kn_kit/*` (kit; gate icon `api.GATE_ICON_MODEL` = `rlk:mboss/kn_kit/gate_icon`), font `rlk:mboss_kn`.
  Reused, never written: `api.AVATAR_MODEL` (`rlk:player_motion/arle/<part>`), `api.SCYTHE_MODEL`
  (`rlk:player_motion/weapons/scythe`), `rlk:skin/arlecchino`.
- **FN-1 names** (S1 implements; frozen in `api` §2): `mboss_lib.hz_opts(bol=N)` / `pj_opts(bol=N)` (N 1..100, % max HP)
  → one-shot scores `#hzBol mb` / `#pjBol mb`; `hz/hurt`, `pj/hit`, `hz/hurt_pm` copy the hazard's / prop's value into
  `#mbBolIn mb` for one call of `mboss/hurt` / `pl_dot`; multiplier `#mbBolRe mb` (module-owned %, default 100);
  event `#mbHitBol mb` = N after a landed bol hit (module reads and clears). `api.fn1_ready()` tells whether S1's
  `mboss_lib` has the option. Arena `fl_ruins` (n 4), `#mbAr 4`.
- Test ids (`boss/test/pattern {id:N}`, `api.TEST_IDS`; `test/help` prints `api.TEST_HELP_NAMES`):
  1 a2 · 2 a5 · 13 a4 · 3 b1 · 4 b2 · 5 c1 · 6 c2 · 7 d1 · 8 d2 · 9 e1 · 10 f1 · 11 g1 · 12 h1 · 20 E70 · 21 forced bond ·
  22 heal 30 % · 23 arm shock · 24 break now · 25 intro replay · 26 transition · 27 death · 28 heal orbs · 29 stun ·
  30 phase 1b · 31 phase 2 (skip T) · 41 q0 · 42 q1 · 43 q2 · 44 q3 · 45 q4 (3 shots) · 46 q5a · 47 q5b · 48 q6 ·
  80 HP = next floor + 1 · 99 hold. `test/lock {id}` for `api.LOCK_IDS` (1–13, 41–48).
- Dialog subtitles: `api.LINES` (17 wiki lines, ids 1–17), `api.LINE_OF[key]` (the lines a cast picks from); the banner
  `api.BANNER` (「생명의 계약을 제거하고 일반 공격으로 「붉은 피의 연회」를 중단시키세요」), the badge `api.BADGE` (`◆선혈의 충격`).

## 3. Interfaces
### 3.1 Framework ↔ module (S1 ↔ S3 / S4)
- Ordinary chapter module: 17 hooks + `prep` + `test/help` under `boss/arlecchino/`, dispatched by `#mbId 12`. Chapter
  mode as Apep (arena, floors `#mbFloor`, `mboss/repool`, `mboss/title`, music, `cine`, `res`); body = husk scale 1.4,
  click shield `hit {w:1.2,h:2.9}`, **no proxies** (`px:false`; FN-3: S1 proves the whole chapter path with it).
- **FN-1 Bond-of-Life hazards** (as built by S1, R1; amended at I1 / S5): a hazard / projectile / ‰ hazard created with
  `bol=N` carries N in the per-entity objective **`mbBol`** (`hz/init` / `pj/launch` copy `#hzBol` / `#pjBol` in a branch
  `hz/init_bol` / `pj/init_bol` that also resets the one-shot option). `hz/hurt` and `pj/hit` are unchanged: `mboss/hurt`
  checks its attacker (`@s mbBol 1..` → `mboss/hurt_bol`, +1 command per hit) and `hz/hurt_pm` branches the same way into
  `hz/hurt_pm_bol`; `#mbBolIn mb` = `mbBol` for that one call. A bol **hazard / projectile** multiplies its raw damage by
  `#mbBolRe mb` / 100 (an unset `#mbBolRe` reads as 100); a bol **‰ hazard** keeps its per mille (**S5: per-mille hazards
  are not multiplied**, the Q5B final is an execution of fixed weight). When the hit reaches the player (not dodged, not
  refused by `#mbCine`) `#mbHitBol mb` = N in the same tick, once per landed hit. Options are removed with
  `scoreboard players reset`; `cleanup_fight` and `mboss/init` set `#mbBolRe` to 100 **only when it exists** (a mid-boss
  fight never holds the name) and reset `#mbHitBol` / `#mbBolIn` / `#hzBol` / `#pjBol`. Mid-boss fights unchanged
  (`test_m0diff.py`), ≤ +1 command per hit.
  Until S1's FN-1 is on a stage's branch (`api.fn1_ready()` false), S3 / S4 mark bol hazards with a pattern flag and
  set `#mbHitBol` themselves from `#mbHitEv` (documented stand-in, removed at I1); the ×`#mbBolRe` then waits for I1.
- Fight start / end / reward / routing are the framework's; the module never teleports the player out, never touches
  `room` scores, never drops rewards. On death it runs `seq/death` and lets `death_tick` finish.
- Routing: `ch [4]` with `route:true` only at I1. Until then the boss is reached with `boss/test/chapter {id:"arlecchino"}`
  after a local uncommitted `enabled:true` (+ S1's arena entry).

### 3.2 Rig (S2 → S3 / S4 / S2 seq)
- Calls (`api.RIG_CALLS`): `rig/{init,spawn,spawn_hidden,tick,kill,uninstall,flash,state/normal,state/hidden,
  face/player,face/track}`, `rig/look/form/{p1,p2}`, `look/wings/{off,open}`, `look/weapon_r/{hand,gone,world}`,
  `look/weapon_l/{hand,gone,world}`, `look/glow/{normal,crimson}`, `look/props/{none,tea}`,
  `rig/anchor/{hand_r,hand_l,blade_r,blade_l,palm_r,chest,spine}` (moves the one `rlk_kn_anchor` marker there; effects run
  `at` it), macro `rig/face/set {yaw}`, and `rig/play/<clip>` / `rig/start/<clip>` for every `api.CLIPS` key. Semantics as
  the Raiden / Apep / Tachy rig APIs: `play` = tick 0 at the next `rig/tick`, event *e* lands on the *e*-th `rig/tick`
  after the call; `rig/tick` is called by the core every tick `at @s`; the rig never moves the anchor except `face/*`,
  never reads module scores, never goes below the floor (build gate); `state/hidden` scales parts to 0 in place.
- Body parts reference `api.AVATAR_MODEL` in form p1 and `api.P2_MODEL` (`rlk:mboss/arlecchino/p2/<part>`) in form p2;
  arm layout `api.ARM_LAYOUT` (p1 slim 3 px, p2 classic 4 px: skin_33); the scythes reference `api.SCYTHE_MODEL`.
  Scale `api.SIZE` 1.4 (`HEIGHT` 2.8, `HIP_Y` 1.05). Clips, events, loops and forms exactly `api.CLIPS` / `api.CLIP_FORM`.
- Manifest `tools/arlecchino_rig_manifest.json` = the stub's schema + transforms / budgets / sprites; `api.check_manifest`
  must pass (same parts and order, same clip lens / loops / events / forms, same anchors). Until it exists S3 generates
  `boss/arlecchino/rig_stub/**` (every call name; `play/<clip>` sets `#rigc kn` to the clip id) and `api.rig()` points
  there.

### 3.3 Kit (S1K → S2 / S3 / S4)
- Calls only through `api.K` (`p`, `prop`, `decal`, `hud`, `snd`, `fixed`) with the names and macro args of
  `api.KIT_PRESETS` / `KIT_PROPS` / `KIT_DECALS` / `KIT_HUD` / `KIT_SOUNDS` / `KIT_FIXED`; values in tenths of a block /
  degrees / ticks; `c` 1 = Pyro orange-gold, 2 = crimson BoL; `on` 0/1; `id` = an `api.LINES` key. `K` returns `''`
  while `tools/mboss_kn_fx_manifest.json` is missing → wrap with `api.lines(...)`.
- Presets `fx/p/<name>` (position / rotation as the effect): `slash_arc {r,yaw,pitch,roll,c}`, `spin_ring {r,c}`,
  `twirl_ring`, `scythe_form`, `embers_puff`, `wheel_trail {len}`, `dash_trail {len,c}`, `leap_flare`, `dive_streak {len}`,
  `impact_burst {r,c}`, `claw {r}`, `wing_burst`, `zig_streak {len}`, `brand_ring`, `brand_x`, `threads {r}`,
  `thorns {r}`, `blast {r}`, `web`, `clone_trail`, `blade_rise`, `blade_burst`, `shock_gain`, `shock_aura`,
  `shock_hit`, `break_burst`, `stun_motes`, `pillar {r}`, `legs_burst`, `moon_flare`, `aim_line {len}`, `reticle`,
  `beam {len}`, `x_mark`, `rapid_slash`, `final_burst {r}`, `feather_hit`, `orb_gather`, `orb_burst {r}`,
  `death_flames`, `wisp_turn {c}`, `gate_flames`, `ambient_petals`.
- Props `fx/prop/<name>` (`@s` = the projectile display or pattern marker): `wheel`, `crescent`, `feather`, `orb`,
  `blade`, `clone`, `wisp {c}`, `moon_halo`.
- **Decals** `fx/decal/<name>` — only these, only for `api.DECALS` keys (PLAN §1.5): `flood {r,t}` / `cracks {r}` (f1),
  `strip {len,w,yaw,t}` / `rim_tint {r0,r,t}` (g1), `pool {r,t}` (e70, cosmetic), `ring_o {r,t}` / `donut_o {r0,r,t}`
  (q5a); each flashes `api.DECAL_FLASH` (6) ticks before its hit tick `t`; all at floor y + 0.02.
- Sounds `fx/snd/<name>`: every name of `api.KIT_SOUNDS` (vanilla events only, `mboss_lib.sound` min-volume rule).
- HUD (font `rlk:mboss_kn`, glyph root text always empty + unstyled): `fx/hud/badge {on}` (`api.BADGE` on the boss-bar third
  line), `fx/hud/banner {on}` (`api.BANNER` as **its own bossbar line `rlk:kn_banner`** under the framework's bars, white,
  the first phrase salmon-red as the real game; S1K K1, accepted at I1; `fx/uninstall` removes the bossbar),
  `fx/hud/line {id}` (dialog subtitle with letter reveal), `fx/hud/clear`.
- Kit wiring by S3: `cleanup` → `fx/clear` + `fx/hud/clear`; `pause` / `death_start` → `fx/clear`; `uninstall` →
  `fx/uninstall`.

### 3.4 Patterns and sequences (S3 core ↔ S3 p1 / S4 p2 / S2 seq)
- `api.Pattern` / `api.Service` dataclasses (docstrings = the runtime contract), writers `api.Writer(owner, api.OWN[..])`.
- Hit ticks from `api.ev(clip, event)`, shapes / tiers / bol flags from `api.HITS` (shape vocabulary in its comment:
  sector, disc, disc_ahead, ring, line, dash_line, full, pj_wheel, pj_cres, pj_bolt, pj_burst, pm_disc, orb_discs),
  coefficients `api.dmg(tier, phase)` (P2 × `api.P2_MUL` / 100), dash lengths `api.DASH_LEN`, heights `api.LEAP_H`
  (≤ `api.AIR_MAX`).
- All hazards `#hzQuiet 1` except the `api.DECALS` keys; tells: first visible motion → hit ≥ `api.TELL_MIN` (12 t), big ≥
  `api.TELL_BIG` (20 t), combo follow-ups ≥ `api.COMBO_GAP` (10 t). End points via the framework `mv/ok` + leash inside
  `api.MOVE_R` (walk − 1.5).
- Break windows `api.BREAK_WINDOWS = {'f1': (22, 159), 'q5a': (22, 121), 'q5b': (22, 96)}` on the pattern clock `#pt`
  (= the clip ticks; each opens at its `brand` event = `api.FORCE_TICK`): the core tags the body `rlk_kn_win` inside them
  and resolves a shock hit there (cancel → `p/<key>/cancel` → break). Patterns make `cancel` idempotent and remove all
  their markers, props and decals.
- Forced bond, heal orbs, BoL bookkeeping only through S3's `bond.py`; S2 / S4 call the frozen lines
  `api.BOND_CALLS['force']` / `['orbs']` (= `function rlk:boss/arlecchino/bond/force` / `bond/orbs`, any executor).
- The core includes only patterns present in `p1.PATTERNS + p2.PATTERNS` and sequences in `seq.SERVICES` (`api.SEQS` =
  intro, t_p2, death); missing ones fall back to a stand-in (pattern skipped; sequence = wait for the clip length, titles at
  its events).
- **No cross-stage function reference before it exists** (a missing function fails the server load): use `api.rig`,
  `api.K`, `api.arena_look` (empty until S1's arena entry) — each returns the right line or `''`.

### 3.5 Bond of Life and 선혈의 충격 (S3 runtime rules; PLAN §4)
- BoL hit (`#mbHitBol`) → `bol += api.BOL_HIT %` max HP (`player/bol/add_pct`), `#bonded 1`, `#given += …`, her
  `mhpC += api.BOL_HEAL_PM ‰` of `mhpM` (capped). `#mbBolRe` = `api.BOL_REHIT_PCT` while `#bonded 1` and `bol ≥ 1`, else
  100 (set every tick).
- DoT: `pl_dot api.BOL_DOT_PM ‰` every `api.BOL_DOT_T` while `#bonded 1` and `bol ≥ 1` (non-lethal).
- Forced bond (`bond/force`): her part of the bond becomes `api.BOL_FORCE %` (S5: what she gave before is taken back first, so two orbs always clear it), no damage, no dodge, skipped while dead / selecting / map screen /
  respawning; + `bond/orbs` (`api.ORBS` heal orbs via `combat/heal_orb_spawn`, tagged `rlk_kn_orb`, `api.ORB_R` from
  the centre, 120° apart, ≤ `api.ORB_MAX` alive).
- Clear (`bol` → 0 with `#bonded 1`): `#bonded 0`, `#given 0`, `#shock 1` + kit `shock_gain` + badge.
- Normal-attack predicate in `on_hit`: `execute <api.NORMAL_HIT_IF> run …` (`#icd tmp 1`, not `#skillDmg`, not `#tfm`,
  not `#sub itv`, not `#trueDmg`). `on_hit` only sets `#shk_hit kn 1`; `tick` resolves: in a window → break
  (`api.BREAK_PM[phase]` ‰ of `mhpM` true damage clamped to stay ≥ floor + 1, `brk` → `stun` / `stun2` `api.STUN_T`), else
  `api.SHOCK_BONUS_PCT` % crimson burst (same clamp); `#shock 0`, badge off.
- Cleanup / won / cancel / defeat: remove `min(bol, #given)` from the player (`player/bol/on_change` only, no on_clear),
  shock off, `rlk_kn_orb` removed.
- **Ranged immunity and Pyro resistance do not exist anywhere** (tests assert no projectile filter or evasion and
  `res {"*":10}`).

## 4. Standing rules (every stage)
No negative `scoreboard players add/remove` literals; lowercase resource ids; text components never inherit a glyph font
(empty unstyled root); nothing below the floor; no teleport into blocks; vanilla sounds only; no tutorial / advice text
(allowed: names, phase titles, pattern names, the badge, the wiki dialog lines, the one real-game banner, refusal
messages); floor decals only the §3.3 list; tells ≥ 12 t / ≥ 20 t for big hits; held weapons point the right way (check
side renders); big swings keyed densely (every tick over the swing); generators own their paths, write deterministically
(run twice → identical), never hand-edit generated files.

## 5. Gates (each stage before hand-off)
`bash S:mcsrv/loadcheck.sh <worktree>/roguelike ar_<stage>` → 0 failures · `python3 -I S:mcsrv/rplint.py <RP>` clean
(stages that touch the RP) · regenerate twice byte-identical · `python3 tools/check_mboss_pack.py` green · existing
generator outputs unchanged except the files the stage owns (the D0 check script `S:ar/tools/regen_d0.sh <wt>/roguelike`
reruns every registry-reading Python generator) · budgets (atlas: S2 ≤ 0.15 M, S1K ≤ 0.70 M; elements at rest ≤ 6 500).
RP for stage work: a plain copy of the current release RP (`cp -r S:tk/rp S:ar/rp_<stage>`; never hard links: generators
rewrite files in place); only S1K and S2 need one. Delete scratch renders you do not deliver (disk ≈ 2.8 GB free; at most
three worktrees at a time).

## 6. Change log
- D0 (eb0a38a): as §0. (The lead records accepted requests here at I1.)
- I1 (wip/ar 9245812): S1 R1 (FN-1 as built, §3.1), R2 (walk floor light 10); S1K K1 (banner bossbar line, §3.3), K3
  (`dive_streak` colour as built); S2 R-S2-1 (h1 drop 64 / wing 72 / sweep 84 / end 124), R-S2-5 (culling 10 x 10, wings /
  legs 1.25x / 1.35x); S4 R-S4-6 (incl. `DASH_LEN['q2']` 20); `DMG` x 0.8 (T1 26 / T2 36 / T3 50 / T4 64); registry
  `enabled` + `route` true; gate icon `rlk:mboss/kn_kit/gate_icon`; R-S3-7: the bow's aimed shot is not a normal attack.
- S5 (review / balance on wip/ar): `s3lib.TID` keyed on the test name's first word (R-S4-1), test 45 through `#q4_t3`
  (R-S4-2); K2: the four vertical P1 slashes pass pivot 2.0 b; FN-1 per-mille hazards are not multiplied by `#mbBolRe`;
  the forced bond resets her part to `BOL_FORCE` (§3.5); the body is the chapter body `mboss/cb/body`; balance: `BOL_REHIT_PCT`
  150, `P2_MUL` 100, Q5B final 300 per mille, P2 near weights Q1 25 / Q4 15 / Q6 15, `COOLDOWN` Q1 240, `DASH_LEN['q2']` 20,
  tiers f1 hit1 / hit2 T2, g1 field T1, a4 / a5 h4 T2, q1 h2 / h5 T1 (S5 report).
