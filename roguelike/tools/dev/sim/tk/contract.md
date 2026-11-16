# 타키 (Tachy) + rift — D0 contract (frozen)

Branch `wip/tk-d0` (worktree `S:tk/wt_d0`, base = release head 72ecf78). Design: `S:tk/PLAN.md` (§ numbers below).
Source of truth for every number / name: **`tools/mboss_tachy/api.py`** (import it; never copy values). This file is the
prose around it. Changes only through a request file `S:tk/requests/<stage>.md` (what, why, who is affected); the lead
applies requests at integration (I1). `S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`.

## 0. What D0 committed
| file | content |
|---|---|
| `tools/mboss_registry.json` | entry `tachy` (n 20, `kind:"special"`, `fn:"boss/tachy"`, **`enabled:false`**, numbers of PLAN §8; music 1 `len 0` until S1 measures the pool; icon vanilla until the kit exists) + 3 `_doc` lines. **No `arenas.tk_lift` yet** (S1 adds exactly `api.ARENA_SPEC`) |
| `tools/mboss_lib.py` | accepts `kind:"special"` (validation: picks 1..3, lvup 0/1, own arena required when enabled, no ch/route/px; `fn` may be `boss/<id>`), `SPECIAL_HOOKS = []`, `SPECIAL_PICKS_MAX = 3`, `special_bosses()`. Nothing else changed: every existing generator output is byte-identical (checked) |
| `tools/mboss_tachy/__init__.py` | package doc + ownership |
| `tools/mboss_tachy/api.py` | the frozen API (sections 1–9) |
| `tools/mboss_tachy/stub_rig_manifest.json` | the D0 rig manifest (schema 1, source stub): 40 parts with parents, 41 clips (id = order, len, loop, events, form), looks, props, call list. Generated from api.py |
| `tools/mboss_tachy/{seq,p_air,p_mantle}.py` | empty stubs (`SERVICES = []`, `PATTERNS = []`) owned by S2 / S4 from now on |

## 1. Ownership (write / delete only your own; tests and scratch under `S:tk/<stage>/`)
| stage | repository files | generated outputs |
|---|---|---|
| **S1** framework + rift | `tools/build_mboss_core.py`, `tools/mboss_lib.py`, `tools/mboss_registry.json`, `tools/check_mboss_pack.py`, new `tools/build_rift.py`, README sections "특수 보스 · 균열" + help rows, `roguelike/README.md` (only those sections) | everything the core writes (`F:mboss/**` except module trees, `F:boss/test/**`), `F:room/rift/**`, `F:room/obj/k_rift`, the 11 hook lines of PLAN §7.8 (inserted by `build_rift.py`, marker `# rift (build_rift.py)`), RP `assets/rlk/{textures,models/item,items}/rift/**` |
| **S1K** kit + arena theme | new `tools/build_mboss_tk_fx.py`, `tools/mboss_tk_fx_paint.py`, `tools/mboss_tk_fx_manifest.json` (generated), `tools/mboss_arena_tk_lift.py` | `F:boss/tachy/fx/{card,cardx,look,clear,uninstall}`, `F:boss/tachy/fx/{e,p,tele,snd,hud,prop,test}/**`, RP `mboss/tk_kit/**`, font `rlk:mboss_tk` (+ `textures/font/mboss_tk/*`), the items atlas entries `rlk:mboss/tk_kit/*`. (`F:mboss/arena/tk_lift/**` is written by `build_mboss_arena.py` from the theme module once S1's arena entry exists) |
| **S2** rig + sequences | new `tools/build_tachy_rig.mjs`, `tools/tachy_{pose,geometry,paint,materials,clips}.mjs`, `tools/tachy_rig_manifest.json` (generated), `tools/tachy_rig_api.md`, `tools/mboss_tachy/seq.py` | `F:boss/tachy/rig/**`, RP `mboss/tachy/**` + atlas entries; `F:boss/tachy/seq/**` (written by S3's generator from `seq.py`) |
| **S3** core, AI, gimmicks, melee | new `tools/build_mboss_tachy.py`, `tools/mboss_tachy/{core,ai,elem,p_melee}.py` (+ more S3 modules if needed, named in the request log) | `F:boss/tachy/**` prefixes of `api.OWN['S3']` (17 hooks, `init`, `core/ ai/ el/ mantle/ hud/ test/ rig_stub/`, `p/{a1,b1,b2,b3,c1,c2,c3}/`) |
| **S4** aerial + mantle hazards | `tools/mboss_tachy/{p_air,p_mantle}.py` | `F:boss/tachy/p/{k,w1,w2,l,mantle}/**` (written by S3's generator) |
| lead (I1) | `tools/mboss_tachy/api.py`, `stub_rig_manifest.json`, `__init__.py`, this file | registry `enabled:true`, icon model, merges |

Shared-file edits outside this table are forbidden; if one is needed, write a request.

## 2. Names (api §6)
- Module state: objective **`tk`** (dummy, S3 creates in `boss/tachy/init`, removes in `uninstall`), fake players: core
  `api.CORE_FP`; a pattern `#<key>_<x>`; sequences `#sq_<x>`; the pattern clock `#pt`, end flag `#done`, sequence clock
  `#sq`, end flag `#sqdone`.
- Rig objectives `tkRig*` (S2's `rig/init` / `rig/uninstall`); kit objectives `tkFx*` (S1K's `fx/uninstall`); rift
  objectives `rift*` and fake players `#rift*` in objective `room` (S1); framework fake players `#sp*` in `mb` (S1).
- Tags: `rlk_tk_part` (rig parts), `rlk_tk_prop` (rig props), `rlk_tk_fx` (kit cards), `rlk_tk_core` (G3 window on the
  body, core), `rlk_tk_mantle` (body while mantled, core), `rlk_tk_air` (S4 markers), `rlk_tk_p` + `rlk_tk_p_<key>`
  (pattern markers); rift `rlk_rift`, `rlk_rift_part`, `rlk_riftz` / `rlk_riftdone` (zone markers). Everything spawned
  in the world also carries `rlk_room` (rift) or `rlk_room rlk_mb_aux` (fight).
- Storage `rlk:tk` keys `core.*` (S3), `rig.*` (S2), `fx.*` (S1K), `air.*` (S4), `seq.*` (S2). Framework `rlk:mboss
  sreg[] / sbyid / sprep / spmet` (S1).
- UUIDs: rig parts `524c4b4d-544b-4900-8000-0000000000NN` (NN 00–27 = `api.PARTS` order), shadow `…40`.
- Resource ids (lowercase only): `rlk:mboss/tachy/*` (rig), `rlk:mboss/tk_kit/*` (kit, gate icon
  `rlk:mboss/tk_kit/gate_icon`), `rlk:rift/*` (rift), font `rlk:mboss_tk`.
- Test ids (`boss/test/pattern {id:N}`): `api.TEST_IDS`; `test/help` prints `api.TEST_HELP_NAMES` (S3).

## 3. Interfaces
### 3.1 Framework ↔ module (S1 ↔ S3)
- The module is an ordinary registry module: 17 hooks + `test/help` under `boss/tachy/`, dispatched by `#mbId 20`. No
  special hooks. The framework sets `#mbMode 1` (chapter features: arena, floors `#mbFloor`, `mboss/repool`, music,
  `cine`, `res`), **`#mbKind mb 2`** (0 mid, 1 chapter, 2 special; wording only), `#mbAr 3`. Body: husk scale 1.25,
  click shield `hit {w:1.1,h:2.6}`, tag `miniboss` (gold × `goldMul`, sapphire `sap` via `combat/gold_drop`), no proxies.
- Fight start / end / reward / rift are the framework's; the module never teleports the player out, never touches
  `room` scores, never drops boxes. On death it runs the death sequence and lets `death_tick` finish as every module.
- S1's runtime names (frozen): `mboss/sp/{roll,prep,gate,start_zone,start,wait,ret_rift,won,won_kill,won_cancel,clear,
  reward,lvup,forget,run_reset}`, `mboss/test/{rift,rift_id,rift_id_do,special,special_ch,help_special}`,
  `boss/test/{rift,rift_id,special,special_ch}`, `room/rift/{init,roll,arm,show,open,reopen,close,tick,enter,click,
  forget,uninstall}`, `room/rift/spot/*`, `room/obj/k_rift` (`oact 17`), scores `#riftPm #riftUsed #riftForce #riftOn`
  (room), `#spOn #spAuto` (mb).

### 3.2 Rig (S2 → S3 / S4)
- Calls: `api.RIG_CALLS` + `play/<clip>` / `start/<clip>` for every `api.CLIPS` key + `face/set {yaw}`; semantics as the
  Raiden / Apep rig APIs (`play` = tick 0 at the next `rig/tick`; event *e* lands on the *e*-th `rig/tick` after the
  call). `rig/tick` is called by the core every tick, `at @s`. The rig never moves the anchor except `face/*`, never
  reads module scores, never goes below the floor (build gate), `state/hidden` scales parts to 0 in place.
- Manifest `tools/tachy_rig_manifest.json` = the stub's schema plus transforms / budgets; `api.check_manifest` must pass
  (same parts and order, same clip lens / loops / events). Until it exists S3 generates `boss/tachy/rig_stub/**` with
  every call name (each `play/<clip>` sets `#rigc tk` to the clip id; no visuals) and `api.rig()` points there.

### 3.3 Kit (S1K → S2 / S3 / S4)
- Calls only through `api.K` (`p`, `snd`, `prop`, `hud`, `fixed`) with the names and macro args of `api.KIT_*`; values
  in tenths of a block / degrees / ticks / el 1|3 / c 1 amber 2 red 3 gold / pct 0–100. `K` returns `''` while
  `tools/mboss_tk_fx_manifest.json` is missing → wrap with `api.lines(...)`. Executor / position: presets at the
  effect position, rotated as the effect (`slash_arc` uses its own yaw/pitch/roll args), `prop/<name>` as `@s` = the
  projectile display, `hud/*` as any (the HUD reads nothing; badge on the boss-bar name line, gauge on the under-line
  through the framework's `bars` → module `bars` hook, S3 wires).
- Kit wiring by S3: `cleanup` → `fx/clear` + `fx/hud/clear`; `pause` / `death_start` → `fx/clear`; `uninstall` →
  `fx/uninstall`. Every sound named in PLAN §3–5 is a `fx/snd/<name>` recipe (vanilla events only, `mboss_lib.sound`
  min-volume rule).

### 3.4 Patterns and sequences (S3 core ↔ S3 melee / S4 / S2 seq)
- `api.Pattern` / `api.Service` dataclasses (docstrings = the runtime contract), writers `api.Writer(owner, api.OWN[..])`.
- Hit ticks from `api.ev(clip, event)`, shapes / tiers / elements from `api.HITS`, dash lengths `api.DASH_LEN`; current
  blade element = `#el tk` (1 / 3; `'cur'` in HITS). All hazards `#hzQuiet 1` (no ground telegraph, `api.NO_DECALS`).
  Tells: first visible motion → hit ≥ `api.TELL_MIN` (12 t), big ≥ `api.TELL_BIG` (20 t), combo follow-ups ≥
  `api.COMBO_GAP` (10 t). End points (blink, landing, dash ends) via the framework `mv/ok` + leash inside `api.MOVE_R`.
- G3: the core tags the body `rlk_tk_core` during `api.G3_WINDOWS[key]` on `#pt`; on a backfire it calls
  `p/<key>/cancel`. Patterns must make `cancel` idempotent and remove all their markers.
- The core includes only patterns present in `p_melee.PATTERNS + p_air.PATTERNS + p_mantle.PATTERNS` and sequences in
  `seq.SERVICES`; missing ones fall back to a stand-in (pattern skipped, sequence = wait for the clip length).
- **No cross-stage function reference before it exists** (a missing function fails the server load): use `api.rig`,
  `api.K`, `api.arena_look` (empty until S1's arena entry) — each returns the right line or `''`.

### 3.5 Rift look (S1) and arrival tear (S1K)
`rlk:rift/{void,rim,crack,arc_0..3}` belong to S1; the arena arrival tear `fx/p/arrive_rift` (S1K) references the same
item models (`rlk:rift/void`, `rlk:rift/rim`, `rlk:rift/arc_*`) — S1K's build must not fail if they are absent (uses its
own fallback card until I1).

## 4. Standing rules (every stage)
No negative `scoreboard players add/remove` literals; lowercase resource ids; text components never inherit a glyph font
(empty unstyled root); nothing below the floor; no teleport into blocks; vanilla sounds only; no tutorial / advice text
(allowed: names, pattern names, phase titles, badges, gauge, the rift label + "▶ 좌클릭", refusal messages); no floor
telegraphs for Tachy; generators own their paths, write deterministically (run twice → identical), never hand-edit
generated files.

## 5. Gates (each stage before hand-off)
`bash S:mcsrv/loadcheck.sh <worktree>/roguelike tk_<stage>` → 0 failures · `python3 -I S:mcsrv/rplint.py <RP>` clean
(stages that touch the RP) · regenerate twice byte-identical · `python3 tools/check_mboss_pack.py` green · existing
generator outputs unchanged except the files the stage owns · budgets (atlas: S2 ≤ 0.52 M, S1K ≤ 0.18 M, S1 ≤ 0.03 M).
RP for stage work: the current release RP is `S:ch3/rp` (44 MB). S1, S1K and S2 each make a plain copy
`cp -r S:ch3/rp S:tk/rp_<stage>` (never hard links: generators rewrite files in place and would change the release RP);
S3 / S4 need no RP. Delete scratch renders you do not deliver (disk is tight).

## 6. I1 (integration, 10-29): accepted requests and changes
Merged in order S1 (already on the branch) -> S1K (82c5e86) -> S2 (af2a8b8) -> S3 (85a483f) -> S4 (2c5bded); no conflicts.
Accepted as written (contract text): S1 R2 (the extra S1 names), R3 (`#mbKind mb` init / fight_vars / kept by
cleanup_fight); S3 R1 (core fake players beyond `api.CORE_FP`: `#clk #cd_<key> #ai_* #t #t2 #t3 #t4 #c<n> #cn1 #cn1000
#fl70 #fl35 #hud_g #hud_c #rigc #rigt`; core extras never start with a pattern key + `_`), R2 (module `s3lib.py`, named in
`__init__`), R3 (tags `rlk_tk_dp rlk_tk_dl`, storage `rlk:tk core.dl`), R4 (pattern ids = `api.TEST_IDS`; core `#pat` 50 swap,
51 mantle, 52 break + stun, 53 nova, 54 transition, 55 intro replay), R5; S4 R4 (tags `rlk_tk_pj rlk_tk_new rlk_tk_klock
rlk_tk_kspot rlk_tk_w2lock rlk_tk_w2p rlk_tk_aim rlk_tk_llock rlk_tk_nova`), R5 (`#k_* #w1_* #w2_* #l_* #mantle_t`, storage
`rlk:tk air.k` / `air.nova`); S1K K5 (objectives `tkFx tkFxS tkFxG tkFxH tkFxK tkFxD`, tags `rlk_tk_fx_c rlk_tk_fx_coc
rlk_tk_fx_new/_go/_sh/_fd/_hit rlk_tk_fx_demo(_p<i>)`, storage `rlk:tk fx.*`); S2 R1-R6 (culling 8 x 10, intro-only sheath +
short holster, the stun hold span, rig-keyed tell looks, the title at the intro ignite only on the boss bar, 2 201 rig functions).
Applied in the owning generators:
- api.py: `KIT_SOUNDS += 'wave_charge'` (K1); kit `EXTRA_SOUNDS = ()`. p_air.py W1 charge = `K.snd('wave_charge')` (S4 R3).
- core.py: `pj_end` also dispatches `p/mantle/pj_end` (S4 R1); `resume` calls `p/mantle/nova/resume` at `#pat` 53 (S4 R2) and,
  at `#pat` 51, redraws the cocoon card (`#hud_c -1` + `mantle/gauge`, K4).
- elem.py: the mantle gauge is shown once, as the boss-bar under-bar (`bars` -> `hud/bar_gauge`); the kit's name-line gauge
  cells (`fx/hud/gauge`) are no longer called (the function stays in the kit).
- p_melee.py B3 bangs: `slash_arc roll 90, pitch -62` (K3; `roll 90, pitch 15` measured 2 b under the floor); s3lib
  `fx_slash` fits every slash above the floor (`arc_fit`: vertical sweeps raise the aim, diagonals flatten their tilt; 37
  arc configurations, lowest painted point >= 0.05 b over the floor).
- registry: `tachy` enabled (w 10), icon `{item:"minecraft:netherite_sword", model:"rlk:mboss/tk_kit/gate_icon"}` (K2).
- S2 generators (lead's model fix + the user's face request): the cape (layered feather field, lining, overlapping halves,
  two wrap facets, pitch sign fixed so it trails back clear of the hips, falls with gravity when the torso tips over;
  holster moved under it) and the unmasked face (anime style, folded face / fringe cards, rounder crown).
- Scratchpad suites: S1 R1 appended `tk/tests/baseline/shared_edits_s1.diff` to `az/tests_cm/baseline/shared_edits.diff`;
  R4 taught `ap/tests/test_boss_alias.py` the 4 aliases; S2's note: test_tachy's tp rule excludes `rig/**` and the kit's
  display tps (and its font / text rules follow the contract: glyph font only on a leaf sibling of an empty root);
  test_rift / test_special expect tachy enabled (`#spN 2`, `#spRoll 1`, sreg `[tachy, spproto]`) and force `spproto` for the
  framework E2E; harness paths point at the integrated tree (`TK_DP`, default /home/user/rlk/roguelike).
