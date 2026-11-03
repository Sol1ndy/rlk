# 야타용왕 (Azhdaha) — binding plan

Status: the full plan (patterns, mechanics, stages) is written after the video analyses land. This file starts with the
decisions that the rig work needs now. Later sections are appended; earlier decisions only change by an explicit note.

## User requirements (from az/src/wiki.md)
- Chapter 1 end boss (Raiden stays for the other chapters except chapter 3, which gets the Apep Warden).
- Element pair rolled on entry: one of 불/물 (phase 2, legs + chest) and one of 얼음/번개 (phase 3, back + tail).
- RES: Physical 30, Geo 30, the two rolled elements 30 (from the start), all other elements 10.
- The model gets a lot of care (big boss).

## Rig decisions (binding for stage R)
R1. **Scale H = 7.0 b** (tallest dorsal-plate tip in the rest pose); proportions from `understand/model.md` §1.2 with the
    resolutions of §9: nose→rump 1.46 H (10.2 b), wheelbase 0.72 H (5.0 b), tail ≈ 14.5 b in 8 segments
    (2.3, 2.1, 1.9, 1.8, 1.7, 1.6, 1.6, 1.5), head carried low (snout ≈ 0.85 b, crest ≈ 2.65 b), red eyes.
    `motion.md` joint heights scale by 0.91 where they assumed 7.6 b.
R2. **Skeleton**: `motion.md` 36-bone proposal minus the back-tree bones (the leafy branch is the tail tip, `model.md` §0):
    spine segments, two-segment neck, head, jaw, beard bones, 3 bones per leg with build-time foot IK, 8 tail segments +
    tip, spike-group flare bones.
R3. **Part budget 44–48 display parts (hard cap 56)**; the detail goes into elements per part and into textures
    (`rigtech.md` TL;DR 1–2). Display scale per part so every part passes `checkBounds` (torso 2.5–3, head ≈ 2.2,
    legs/tail 1.2–2).
R4. **Culling box `width:30f,height:12f`** on every part, `view_range` 3 (rigtech TL;DR 3).
R5. **Hit proxies**: the rig exposes ≈ 11–12 proxy points on bones (7 spine/neck/head/tail + 4 legs) for the framework's
    interaction-entity hit proxies (rigtech §3.3). The framework side comes later; the rig publishes the points per pose.
R6. **Element looks**: base Geo look; the legs + chest regions switch to a Pyro or Hydro look (phase 2) and the back +
    tail regions to a Cryo or Electro look (phase 3), independently (4 combos). Implement as per-part texture / model
    variants selected per region (palette: `model.md` §4).
R7. **Burrow support** (rigtech §4): root can sink below an opaque floor; unused parts can go to scale 0; a tail-only state
    (sunk root, tail chain raised).
R8. **Textures ≤ 1.2 M px** for the rig (rigtech TL;DR 7), sprite sides multiples of 16, ≤ 512.
R9. **Files** (rigtech §5.3, split by region so several authors can refine in parallel):
    `tools/build_mboss_azhdaha_rig.mjs` (entry: PARTS, budget check, UUIDs, RP write, compile, API, proxies, manifest),
    `tools/azhdaha_pose.mjs` (PART_SCALE, FK + foot IK, proxy points), `tools/azhdaha_clips.mjs` (DEFAULT_POSE, CLIPS),
    `tools/azhdaha_geometry.mjs` + `tools/azhdaha_paint.mjs` as thin aggregators over region modules
    `tools/azhdaha_{head,body,legs,tail}.mjs` (each exports its parts' geometry, sprites and looks),
    `tools/mboss_azhdaha_rig_api.md`, `tools/mboss_azhdaha_rig_manifest.json`.
    Namespace `rlk:mboss/azhdaha/rig`, tags `rlk_mb_azhdaha_part`, `rlk_mb_az_<part>`, objectives `azRig*`,
    UUID block `524c4b4d-415a-4400-8000-0000000000NN`.
R10. Shared rig libraries may be extended, but the Guardian, butterfly and field generator outputs must stay
    byte-identical (prove it as the earlier lib moves did).
R11. Renderer: `S:az/understand/rigtech_render.py` (wraps `S:preview/raiden_preview.py`).

## Full plan (v1)

Status: **binding** from 2026-10-18. It replaces `S:az/plan_draft.md` and applies every decision of `S:az/plan_ledger.md`
(the review of the four critiques). R1-R11 above stay in force except where a numbered "Rig decision change" below adds to
them. Later changes need an explicit, numbered change note appended at the end of this file. Nothing here is built yet.

### 0. Conventions

| short | meaning |
|---|---|
| `S:` | `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad` |
| `DP` | `/home/user/rlk/roguelike` (main line; Guardian + butterfly + the 10-19 butterfly tuning) |
| `FG` | `S:mb3/wt_fg/roguelike`, branch `wip/fg` (aa8cd73; merged into main within about 2 h) |
| `M0` | main after the `wip/fg` merge. Every framework / module branch starts from `M0` (exceptions in §7) |
| `T:` / `F:x` / `AZ:x` | `DP/tools/` / `DP/data/rlk/function/x.mcfunction` / `F:mboss/azhdaha/x` |
| `[ch] [mech] [mot] [mod] [rig] [vN]` | `S:az/understand/{chapter,mechanics,motion,model,rigtech,vN}.md` |
| `[AP]` | the Apep draft `S:ap/plan_draft.md` (its §1.3 FW-1..19 list is the other client of the chapter mode) |
| `t` / `b` | ticks (20/s) / blocks; body frame `f` (+ toward the head) and `s` (+ the boss's left), from the anchor |

**Conversion rules** (they implement the earlier bosses' binding feedback, `S:mb2/plan.md`, `S:mb3/plan.md`):

- **Sizes**: footage metres × 7.0/9.0 (H = 7.0 b vs the consensus 9 m, R1) × 1.2 (areas +20 %) = **× 0.93**, rounded to
  0.1 b. Rig-anchored distances (nose, paws, tail) come from the rig manifest, never from footage.
- **Ticks**: footage ticks are 20 tps. Every wind-up (the anticipation before the first hit of a clip) is **−25 %**:
  clips are authored at footage speed and compressed by the shared `RETIME` knots (retime only compresses); lock-on
  telegraphs use `tell_rt(t) = max(F, round(0.75 t))` with **F = 12 t for dodgeable hits, 20 t for `#hzNoDodge` hits**.
  Strikes, follow-throughs and the dodge-rhythm gaps the wiki names (stomp 15 t, triple stomp 23 t) keep full speed.
  Settles −20 %, absorb holds −30 %, roar holds −25 %. Sequence gaps that are not a named dodge rhythm (landslide waves,
  lightning rounds, ice circles, icicle volleys) are × 0.75.

**Global rules** (binding for every pattern; the generator checks the first five, §8.4):

1. **Decal = hazard.** Every hazard's tested area equals its drawn area within 0.3 b (the hit pad); moving hazards are
   drawn as the union of their per-tick samples.
2. **Burst budget.** On any spot, the coefficients of the distinct volley groups that can land within 40 t sum to
   **≤ 2.9** (= 45 % of an item-less Lv5's 148 HP at L6). Lingering ticks count once.
3. **Dash budget.** A pattern needs ≤ 2 timed dodges in any 20-t window; a chain of ≥ 3 timed dodges must offer a
   walk-out or a dash-covered alternative that works while swinging (no jump-only answer except the landslide's wave 6).
4. **Telegraph floors** 12 t (dodgeable) / 20 t (`#hzNoDodge`), measured from the first visible decal to the hit.
5. **Front band ≥ per-tick advance** for every expanding front (no gaps between samples).
6. **Undodgeable look.** Every `#hzNoDodge` decal shares one look (red-amber rim + the kit's "回" glyph); low-band
   (jumpable) ones add a jump chevron.
7. **Lingering caps**: fire ≤ 4, hail ≤ 2, element strip ≤ 1 alive; total lingering area ≤ 220 b² (oldest cancelled).
8. Carried rules: no FOV zoom (no slowness, speed or camera effect on the player; player-side Freeze is suppressed by
   `NoRx`, §4.10), the shared swing rules unchanged (no jump during a swing), vanilla sounds only, Korean UI text,
   generators only (never hand-edit generated files), balance within about 20 % of the targets of §6.2 with the fairness
   simulator.

### Rig decision changes (additions to R1-R11)

**Rig decision change 1 (adds to R7, burrow support).** While the body is hidden (`visBody 0`), a clip may carry a root
**z offset** so that the tail-only pillar stands exactly on the anchor (rig x 0, z 0 ± 0.3 b at the floor cut). The offset
is 0 on every tick where any body part is visible; the builder checks it. Reason: the committed `tail_only` pose puts the
pillar 4.4-4.8 b behind the anchor, so the body husk, the tail proxies and every burrow telegraph would disagree
(`plan_crit_feasibility.md` F7d). The module keeps one point (the anchor) for the pillar, the crater, the safe circle on
the tail and the emergence.

**Rig decision change 2 (adds to R10, shared libraries).** Shared rig-library edits go through one **RIGLIB** stage (§7):
`tol.tp` per part, per-rig culling box and view range, `follow_y<k>` sink offsets, the static-anchor follow skip,
per-state follow lists, the shadow helper, and `T:mboss_shape_lib.mjs` (promoted from `azhdaha_shape.mjs`, which stays as a
re-export shim). The Azhdaha rig branches consume RIGLIB and no longer edit `T:mboss_*.mjs` themselves (Apep's rig does
the same). Byte-identity of the Guardian, butterfly and field-generator rig outputs is proven once, on `M0`.

**Rig decision change 3 (clarifies R9, UUIDs).** Part UUIDs come from a fixed, append-only name → index table in the
builder (not from `PARTS` order), so adding a part never renumbers others. Allocation inside `524c4b4d-415a-4400-8000-
0000000000NN`: parts 0x01-0x3F, shadow 0x40 (as committed), **hit proxies 0x41-0x4C**, 0x60-0x8F reserved for module props
that need a fixed id (the intro seal prism 0x80, the B3 crater 0x81; all other props are tagged fight entities). Written
into the rig API and `S:az/contract/cm.md` in the same commit.

---------------------------------------------------------------------------------------------------

### 1. Architecture

#### 1.1 Fight flow

```
boss map (#mapIdx 5): room/pick/boss -> mboss/cb/route (generated from registry ch + route)
   ch1 -> azhdaha (route:true from I2) | ch3 -> apep (later) | else -> Raiden (unchanged)
foyer (zone 1) -> domain entrance (zone 2, kind 9, data{boss_id:"azhdaha",cboss:1b})
   zone_build -> room/cboss/azhdaha/build -> mboss/cb/prep (generated; literal boss_id lines)
      -> mboss/azhdaha/prep: roll the pair, light the stele glyphs, write the gate label storage,
         forceload the arena and start its sliced ensure (<= 40 slices, #mbArBuild)
   zone_enter (chapter zone) -> room/obj/k_cboss (gate object, oact 16), no combat_start
gate click -> mboss/cb/gate: guards (peaceful, zst 3, no body, arena still building -> "준비 중"), title,
   then room/combat_start with #spawnT 30 -> mob_wave -> room/boss_spawn -> mboss/cb/spawn_route
   -> mboss/cb/start {id}: cur <- cbyid.<id> (no roll, no met, never #mbForce), #mbMode 1, #mbAr,
      arena ensure must report built -> marker -> module spawn (body WITHOUT miniboss, husk scale 0.1,
      rlk_mb_noshield, rlk_mb_big, proxies) -> tp_in (blindness) -> intro -> fight
   -> kill: combat/apply (heal orb 5 %, XP 40, gold 2..4 x chapter x 15, 2 sapphires) -> death shell
-> combat_clear (kind 9) -> mboss/cb/won: gold absorb in the arena box, cleanup_fight, tp_out, forget,
   killed ? room/obj/k_chapter : the gate again (same pair)
player death -> pause -> respawn -> run/fail (or test/defeat); room/clear -> mboss/cleanup (forceload released)
```

Raiden keeps chapter 2 and 4+ exactly as today (`boss/raiden/test/start` sets chapter 2 and stays green). Apep (chapter 3)
builds on the same mode later; everything in §1.2 is generic.

#### 1.2 Chapter mode (AZ-CM; generic; `T:build_mboss_core.py` + small shared edits)

This is the deliverable of stage **S1-CM** (§7). It is merged into main as **AZ-CM** before the Azhdaha module (nothing
routed: chapter 1 stays Raiden until I2). It is the union of Azhdaha's needs and Apep's MUST / SHOULD list (`[AP]` §1.3,
FW-1..19, except FW-13 minion extensions, which stay Apep's). Names below are final; Apep adopts them.

| R | item | decision (binding for S1-CM) |
|---|---|---|
| R1 | **Registry** | New boss fields: `kind` (`"chapter"`; default `"mid"`), `ch` (chapters it ends), `route` (bool, default true; Azhdaha **false until I2**), `arena` (aid; default `"plaza"`), `music` (map, R11), `res` (map, R7), `phases` (pool split in % of `#mbTot`, default `[100]`), `px` (bool: proxy boss, R8), `picks 0`, `goldMul 1`, `sap 0`, `w 0`. Top level: **`arena` stays** (the plaza, unchanged); **`arenas`** is added beside it: `{aid: {theme, ver, cx, cy, cz, r, walk, safe, start, box, looks:[...]}}`; `L.arena_of(b)` returns `arenas[b.arena]` or `arena` for `plaza`. **Chapter entries are enabled from their first stage** and are generated into `rlk:mboss creg[]` + `cbyid.<id>`, never into `reg[]` / `byid` (the pinned `reg == [guardian, butterfly, fieldgen, proto]` asserts stay green, the roll never sees them). Hook dispatchers on `#mbId` include them. `snbt_entry` emits `kind ch arena route px` and takes `start` from the boss's arena. `check_mboss_pack.py` checks the 17 hooks + `prep` for chapter bosses. |
| R2 | **Entry, gate, start** | `F:room/zone_enter`: a zone with `data.cboss:1b` spawns `room/obj/k_cboss` (new **oact 16**) at the zone centre instead of `combat_start`. `k_cboss` is a dedicated label (not `make_node2`): two icons + three text-component lines read from `rlk:mboss cprep.<id>` (written by `prep`). Click → `mboss/cb/gate`: the guards of `mboss/gate` (peaceful, `zst 3`, body discarded) + "준비 중" while `#mbArBuild ≥ 1`; title / subtitle / sound from storage; `combat_start` with `#spawnT 30`. **`mboss/cb/prep`, `mboss/cb/spawn_route`** are generated with one literal line per chapter boss (`execute if data entity @s data{boss_id:"azhdaha"} run return run function rlk:mboss/azhdaha/prep`), so no `$(id)` function names (pack check). `mboss/cb/start {id}` copies `cur` from `cbyid.$(id)` (a storage macro), sets `#mbId` from `cur.n`, `#mbMode 1`, `#mbAr`; no roll, no `met` append, never `#mbForce`; refuses to spawn until the arena's `ensure` reports built (no 7-miss cancel while `#mbArBuild ≥ 1`); same `ret_save` / `tp_in` / `bars_show`. |
| R3 | **Per-arena constants and builds** | `#mbAr` = arena number. Every baked token (`CX CY CZ WALK SAFE RAD`, `@OOB@ @BOX@ @FL@ @SAFE1@ @WALK2@ @SAFEP@`, `[ch]` R3 table) becomes a per-arena function under `F:mboss/ar/<aid>/{oob,sweep,clamp,clamp_step,leash,full_rim,tp_in,box_absorb,test}` behind one-line dispatchers on `#mbAr`. `T:build_mboss_arena.py` generalised: per arena `F:mboss/arena/<aid>/{ensure,build,build_slice,rebuild,clear,sweep,look/<look>}`; **stamp per arena and look** `rlk:mboss built_<aid>` = `"<aid>@<ver>:<look>"` + a sentinel block per arena; multi-tick builds in slices (≤ 32 768 blocks per fill, ≤ 40 slices, one per tick), `#mbArBuild` = slices left, `ensure` returns fail while building; `look/<look>` swaps blocks in slices and restamps; `ensure` restores the default look. **The plaza keeps its legacy names, stamp `plaza@2` and output byte for byte.** Themes are discovered from the registry: `theme` → `T:mboss_arena_<theme>.py` exporting `arena_layout()`, `slices()`, `props()`, `entrance_layout()` and constants (Apep plugs in without a generator edit). `ar/switch` and multi-arena fights are **not** built (Apep uses one arena with two looks). Module generators read their arena via `L.arena_of(boss)`. |
| R4 | **Death → chapter clear** | `mboss/cb/won` (from `F:room/combat_clear` for chapter zones): gold absorb in the arena box, `cleanup_fight`, `tp_out` to the entrance, **no `reward`**, `forget`, forceload released; returns 1 if `#mbKilled 1` → `combat_clear` spawns `room/obj/k_chapter`; else the gate returns. Test mode prints the chapter replay links. |
| R5 | **×15 economy** | `mboss/cb/body` = `mboss/body` without `miniboss`; `F:combat/gold_drop:15,23-24` get `tag=miniboss` (2-line shared edit), so a chapter body pays Raiden's ×15 × chapter and 2 sapphires; XP from the registry `xp`; level from `#mapIdx 5` (L6 / L12 / L18). |
| R6 | **Pools, floors, title** | `#mbTot` stored at spawn; `mboss/repool {pct}` (sets `mhpM/mhpC`, bar ramp 30 t; Apep); `test/level` re-applies `phases`. **Floor**: the module keeps `#mbFloor mb` (absolute HP, 0 = none); the generated `d/incoming` wrapper runs `mboss/floor` **after** the module hook: it saves `#mbFloorRaw = #dmg`, clamps `#dmg` so `mhpC − #dmg ≥ #mbFloor`, and sets `#mbFloorHit 1` whenever `mhpC − raw ≤ #mbFloor` (≤, so an exact-floor hit queues too). True damage (`true_hit`, `test/kill`) bypasses it. `mboss/title {title,sub,color}` writes `cur.title/cur.sub`. |
| R7 | **Per-element RES** | Per-entity scores `mbRes0..mbRes8` on the body (from registry `res`, `"*"` = default) and on aux husks (`#auxResEl/#auxResElV` at `aux/spawn`). Entities with RES carry `rlk_mb_resel`; one shared line at `F:combat/apply:23` (before `apply_mods`) runs `mboss/res_pre` for them: `mres = mbRes<#elem>` by 9 generated lines, **before** the module `on_hit`, so a module may override. Covers player hits, amplified hits, transformative reactions and DoTs (they re-enter with the reaction element). Mid-bosses have no `res` → no tag → `mres 0` (butterfly "equal damage" test stays green). |
| R8 | **Hit proxies** (framework runtime, data from the rig manifest) | Interaction entities `rlk_room rlk_mb_aux rlk_mob boss rlk_mb_px rlk_mb_px_<name>` (**never `rlk_zmob`, never `rlk_mshield`**), `response:false`, score `mbPart`, UUIDs from the boss block (registry `pxBase`, Azhdaha 0x41). Generated from the manifest: `mboss/px/{spawn,follow,park,state {set},hit,dup,poll}` + per-clip key functions that store offsets in storage when a proxy moves > 0.15 b; `px/follow` = one macro per tick (`tp` per proxy at `^x ^ ^z` from the anchor, y = the anchor floor, `height` = column top). A proxy whose top ≤ 0.3 b or that is outside the current state set is parked (8 b under the floor, `rlk_mob` removed). State sets come from the manifest; the module maps its states onto them; `px/state` also calls the rig's visibility `state/*` named in the manifest. **Redirect**: one line at the top of `F:combat/apply` → `mboss/px/hit` (dedupe on gametime + `#atkSeq`, then `execute as <body>` at the proxy → `combat/apply`, number shown at the proxy); `px/dup` on direct body hits for `rlk_mb_big` bodies. **`#atkSeq tmp` +1** in `F:combat/melee_begin`, `F:combat/clear_atkflags`, **`F:element/rx_run` (top)**, **`F:element/lunar/hit`**, `F:element/dot` (`element/core_*` not touched). Clicks polled by the framework every tick from `mboss/main` (`px/poll`), and `attack` / `interaction` data cleared while paused. Proxy bodies (`px:true`) are husks at **scale 0.1** with `rlk_mb_noshield` (one-line gate in `F:mob/shield_ensure`): no click box, no arrow block, no collision at any state. Audit fixes: Navia pellet counts go to the body (`F:char/navia/pellet`, `pellet_go`); the minimap excludes `rlk_mb_px` (`F:room/map_mobs`). |
| R9 | **Minions** | Not in AZ-CM (Apep's own FW-13 stage). `aux/*` unchanged except the RES fields of R7. |
| R10 | **Objective entity** | Not built. Reserved names `#hzVictim`, `#mbObj`. |
| R11 | **Music** | Registry `"music": {"<ph>": {"ev": "<event>", "len": <t>}}`; the module calls `mboss/music/set {ph}` (0 stops). Played at the player in the **`record`** category; looped by a timer of `len` (0 = once); `stopsound @a[tag=player] music` every 100 t while playing so vanilla background music never overlaps. Stopped (no fade; a short sting) in `cleanup_fight`, `death_start`, `pause_tick`, `uninstall`, `cb/won`. Events must be **stereo `music.*` tracks** (stereo sources are not spatialised, so the track does not fade as the player crosses the arena); S1-CM measures `len` from the vanilla asset index and checks the non-positional playback in game once (fallback: `music_disc.*` at volume 4, re-anchored at each loop start). |
| R12 | **Bars** | The three framework bars; module `extra[]` badges, `sub[]`, under-bar. `T:build_bossbar.py` gets the **`#buHpCol`** option (default red; outputs byte-identical with the default). |
| R13 | **Cleanup** | `#mbMode`, `#cbForce`, `#mbFloor`, `#mbCine` resets; music stop; arena forceload on demand (added by `prep`, released by `cb/won`, `cleanup`, `room/remove`, `uninstall`); `arena/<aid>/clear` for every arena in `room/remove`; **`arena/<aid>/sweep {y0,y1}`** clears barriers in a band (Apep's walls; FW-18). Arena display props are per-fight entities (`rlk_mb_aux rlk_mb_ar_<aid>`) and die with `cleanup_aux`. |
| R14 | **Lose** | A plain player death needs nothing new. `mboss/cb/lose` (objective loss → `curHealth 0`) + its test variant are generated and **tested on cproto**. |
| R15 | **Tests** | §8. A **chapter proto boss** `cproto` (`T:build_mboss_cproto.py` → `F:mboss/cproto/**`, `kind chapter`, `ch []`, `route false`, forced only by `test/chapter {id:"cproto"}`) exercises every generic path: two pools + floor + repool, title swap, lose, music in two phases, two proxies from a static stub manifest, the RES table, cine, the push ring and capsule, `lockv`, `local`, the mask hazard, `pl_dot`, `#pjNoDodge`, and a two-look swap of its own test arena `cp_test`. |
| R16 | **Player-status and motion helpers** (framework) | N3 `lockv`, N4 mask, N7 hit / dodge / DoT / NoRx, N8 `local`, N12 push capsule, N18 push ring, N19 cine, N20 `#pjNoDodge`, N21 `hz/extend` (§1.4). |

Shared hand-written files touched by S1-CM (each listed in the README shared-edit table with its line): `F:room/pick/boss`,
`F:room/boss_spawn`, `F:room/zone_build`, `F:room/zone_patch`, `F:room/zone_floor`, `F:room/wave_start` (narukami-only
checks → any `boss_id`), `F:room/zone_enter`, `F:room/obj/click` (oact 16), `F:room/obj/k_cboss` (new),
`F:room/combat_clear`, `F:combat/gold_drop`, `F:combat/apply` (proxy line, RES pre-step line), `F:combat/melee_begin`,
`F:combat/clear_atkflags`, `F:element/rx_run`, `F:element/lunar/hit`, `F:element/dot` (`#atkSeq`), `F:player/take_damage`
(the `NoRx` gate at the `element/player_hit` line), `F:mob/shield_ensure` (`rlk_mb_noshield`), `F:char/navia/pellet`,
`F:char/navia/pellet_go`, `F:room/map_mobs`, `F:room/remove`, `F:room/setup`, `F:load` (arena ensure lines only),
`F:uninstall`, `F:run/start`, `F:run/end`; optional polish `F:room/end_boss` + `F:room/gen_title` (the boss name on the
"보스전" object and the map title). Raiden's own files (`F:boss/raiden/**`, its generators) are not touched.

#### 1.3 Routing

- `F:room/pick/boss` → `function rlk:mboss/cb/route` (generated from `ch` and `route`):
  ```
  execute if score #mbTest mb matches 1 if score #cbForce mb matches 1.. run return run function rlk:mboss/cb/route_force
  execute if score #chapter room matches 1 run return run function rlk:mboss/cb/layout {id:"azhdaha"}   # only when route:true
  function rlk:room/raiden/layout
  ```
  `#cbForce` is honoured only while `#mbTest 1` and is reset by `run/start`, `run/end`, `test/stop`, `test/defeat` and
  `test/won` (a dead az test can never route Raiden's own test). `cb/layout {id}` loads `F:room/cboss/<id>/layout`
  (generated by `T:build_cboss_rooms.py`), sets the zones' `data.boss_id` and `data.cboss:1b`, and **never sets
  `#mbForce`**.
- `F:room/boss_spawn` → `mboss/cb/spawn_route` (literal lines per chapter boss) else Raiden.
- `zone_build` dispatches `room/cboss/<id>/build` for chapter zones and `room/raiden/build` for `narukami`; `zone_patch`,
  `zone_floor`, `wave_start` test "any `boss_id`".

#### 1.4 Helpers (N-numbers used in §4-§5)

| id | helper | level | owner | sketch |
|---|---|---|---|---|
| N1 | runtime element on hazards / pj / decals | module | S1-MOD (`api.py`) | `#hzEl` / `#pjEl` set by `operation` from `#azE` (the leg or tail element per the phase rule of §4.6); kit decals called `with storage rlk:mboss az.el`; presets dispatched per element by generated lines |
| N2 | element palettes + the undodgeable look | kit | S1-FX | every `tele/*` takes `el` 0-8 (Geo, Hydro, Pyro, Cryo, Electro, violet, physical) and `nd` (undodgeable rim + glyph, jump chevron for low bands) |
| N3 | predictive lock `mboss/mv/lockv {lead}` | framework | S1-CM | 6-tick ring buffer of the player's position (kept by `mboss/main` while live); a lock marker at pos + v × lead clamped to the walk disc; `#mbVx #mbVz` (mb/t) and `#mbV` stored |
| N4 | mask hazard `hz/mask` (kind 6) | framework | S1-CM | hits a player whose feet are not within `R0 + 0.3` of any `rlk_mb_hzsafe` marker with `mbHzI` = the hazard id; **horizontal score test per marker** (like `hz/hit_full`); no radius limit; volley groups, `#hzNoDodge`, height band as other kinds; drawing is the kit's |
| N5 | orbit mover | module | S1-MOD | prop + `hz/disc` moved by a plain `tp` every tick (no `hz/aim`); angle += ω about a centre that follows the anchor at ≤ 0.2 b/t and freezes during `mv/leap`; band switch for the eye of the vortex (§5 31) |
| N6 | lingering field | module + kit + framework | S1-MOD / S1-FX / S1-CM | `hz/disc` or `hz/line` with `#hzAct` = life, `#hzRearm 10`, `#hzQuiet`; one volley group per family; module field table (id, pos, r, element, end tick); kit **field-decal pool** `tele/field {id,r,el,life}`, `tele/strip {id,...}`, `tele/field_end {id}` (not counted against the attack-telegraph cap), redrawn from the table on resume; refresh = `hz/extend` (N21) up to 2× base life; caps of §0 rule 7 |
| N7 | hit / dodge event, player DoT, no reaction | framework | S1-CM | `mboss/hurt` sets `#mbHitEv`, `#mbHitEl`, `#mbHitSh` (shield before the hit), `#mbHitRA` (1 if the hazard re-arms / lingers) on a landed hit and `#mbDodgeEv` + `#mbDodgeOk` (1 only for a one-shot strike with tell ≥ 12 t, not nododge, or a pj) on a dodged one; **`mboss/pl_dot`** (`#mbDotPct` ‰ of max HP, `#mbDotEl`, `#mbDotLethal`), modelled on `F:player/hurt_elem` (guard then element shield, 250 % same element, no defence), `dashInvT` saved / zeroed / restored, 1-HP floor unless lethal, refused while dead / reviving / in a selection screen; **NoRx**: per-hazard `mbHzNR` and per-pj `mbPjNR` options plus a one-shot `#mbNoRx` for direct calls; `F:player/take_damage` skips `element/player_hit` for them (colour kept) |
| N8 | local frame `mboss/mv/local` | framework | S1-CM | `#mbLf #mbLs` (milliblocks) of the player in the anchor frame (the `hz/hit` projection), ≈ 25 commands |
| N9 | proxies | framework (+ rig data) | S1-CM | R8 |
| N10 | front builder `wave(centre, r0, r1, spd, ease, band, tell, coef, nd, el, grp)` | module | S1-MOD (`api.py`) | `hz/ring` + `hz/resize_s` per tick + kit `tele/wave` + band (the fieldgen front); band ≥ advance asserted; one code path for the landslide, jump, stomp and the Cryo ring |
| N11 | background emitter slots `bgL` / `bgT` | module | S1-MOD (`core.py`) | an emitter runs on its own clock beside the pattern slot; paused with the fight; cancelled by death / cleanup / test stop / a queued transition (`bgT`); **at most one emitter in phase 3** |
| N12 | body push `mboss/push/capsule` | framework (+ module rules) | S1-CM / S1-MOD | each tick while `#mbPushOn 1`, a player inside one of ≤ 2 capsules (storage `rlk:mboss push[]`: f0, f1, half-width in the anchor frame) is moved out horizontally with `player/knockback/check` steps (collision-checked, no velocity, no FOV); the exit is the nearest of side / front end / back end whose end point is not inside a live `rlk_mb_hz` disc or line; the module sets `#mbPushOn` (§4.12) |
| N13 | addon points | module | S1-MOD (dispatch, scheduler) / S2 (bodies) | `api.ADDON_POINTS` (§4.6): each point has a fixed **lead 12 t** (called at event − 12) and a declared context; `api.after(delay, fn)` schedules addon tails on the module clock (16 slots; frozen by pause; cleared by death, cleanup, test stop); the core emits a dispatcher line only for a body written in the same run |
| N14 | `mboss/floor`, `mboss/title`, `repool` | framework | S1-CM | R6 |
| N15 | per-element RES | framework | S1-CM | R7 |
| N16 | music | framework | S1-CM | R11 |
| N17 | arena element looks `AZ:arena/look {el}` | module | S1-MOD (calls by S2-S) | §2.6; kit looks from S1-FX, placement from S1-ARENA |
| N18 | push ring `mboss/push/ring {r,kb}` | framework | S1-CM | radial push-only ring (no damage, no hit event, not dodgeable); skips players whose landing point is inside a live hazard |
| N19 | cine `mboss/cine/start|end` | framework | S1-CM | `#mbCine 1` refuses boss hits on the player (`mboss/hurt`, `pl_dot`); the module freezes its AI clock; bars stay |
| N20 | `#pjNoDodge` | framework | S1-CM | per projectile `mbPjND`, honoured in `pj/hit` like `#hzNoDodge` (Apep) |
| N21 | `hz/extend {n}` | framework | S1-CM | `mbHzL += n` on a live hazard (field refresh) |

#### 1.5 Module layout (mirrors `tools/mboss_fieldgen/`)

```
T:build_mboss_azhdaha.py         entry: core.build()
T:mboss_azhdaha/__init__.py      PATTERN_MODULES = ('geo_a','geo_b','leg','tail','trans','seq')
T:mboss_azhdaha/api.py           STABLE contract: ids, scores, DMG / KB tables (pre-filled for every §5 hazard), element
                                 plumbing (N1), zone names, Pattern record (zones, weights, cooldowns, phases, kinds
                                 normal / special / cast / service / bg; hooks pause / resume / reload / cancel_bg), Gen
                                 helpers (lockp / lockb / lockv, keep, clamps, bstep, tag_last_hz, at / every), TL,
                                 wave() N10, field() N6, orbit() N5, addon() + after() N13, tell_rt(), B3 frame constants,
                                 the manifest clip table (ev, ev_or, clip_len, anchors, tracks, schedules), kit builders
                                 (api.K, a no-op set until I1); re-exports h_<stage>.py at the end
T:mboss_azhdaha/core.py          17 hooks + prep; state machine (intro, phases 1-3, transition queue, B3 frame call,
                                 death); RES at spawn; #mbFloor upkeep; services dispatch; bg slots; push rules; addon
                                 dispatchers; HUD; music calls; arena looks; pause / reload / uninstall; tests
T:mboss_azhdaha/ai.py            zones (via N8), FLANK rule with dwell, exit tests, weighted tables built from the
                                 PATTERNS of the pattern modules, no-repeat, cooldowns, anti-stall, leash, field-area gate
T:mboss_azhdaha/brand.py         brand (§4.10): apply / refresh / stacks / decay, DoT clock, cleanse, shards, HUD lines
T:mboss_azhdaha/geo_a.py         S2-A: P1 chin, P2 jump, P3 charge, P4 spikes
T:mboss_azhdaha/geo_b.py         S2-B: P5 stomp, P5b stomp3, P6 feint, P7 whip, P8 tail slam, P9 burrow charge
T:mboss_azhdaha/leg.py           S2-L: 31 orbs, 32 meteors, 33 fire rule, Hydro / Pyro addons AZ:xl/**
T:mboss_azhdaha/tail.py          S2-T: 41 frost, 42 lightning, 43 천화, 44 가루, 45 / 46 spikes, tail addons AZ:xt/**
T:mboss_azhdaha/trans.py         S2-S: 20 landslide, 21 absorb 1, 22 absorb 2, 23 B3 (incl. the surfacing)
T:mboss_azhdaha/seq.py           S2-S: 26 intro, 24 death
T:mboss_azhdaha/h_<stage>.py     per-author helpers (h_core, h_pa, h_pb, h_pl, h_pt, h_ps), re-exported by api.py
T:mboss_azhdaha/stub_rig.py      per-clip fallbacks only (clips missing from the real manifest); the I2b build asserts the
                                 fallback list is empty
T:build_mboss_az_fx.py           S1-FX kit (+ T:mboss_az_fx_paint.py, T:mboss_az_fx_manifest.json)
T:mboss_arena_az_cavern.py       S1-ARENA theme (arena + entrance; discovered via registry theme)
T:build_cboss_rooms.py           S1-CM: F:room/cboss/<id>/{layout,build}
T:build_mboss_cproto.py          S1-CM: the chapter proto boss (+ T:mboss_arena_cp_test.py)
rig: T:build_mboss_azhdaha_rig.mjs, T:azhdaha_{pose,clips,geometry,paint,shape,materials,head,body,legs,tail}.mjs,
     T:mboss_azhdaha_rig_api.md, T:mboss_azhdaha_rig_manifest.json (R9)
```

Outputs: the module generator owns `AZ:**` except `AZ:rig/**` (rig) and the kit's owned paths (`AZ:fx/{card,cardx,look,
clear,uninstall}` + `AZ:fx/{e,p,tele,snd,hud,prop,test}/**`) and cleans only what it owns; `foreign()` also spares
`AZ:fx/**` while the kit is absent. A pattern module writes only `AZ:p/<key>/**` (+ `AZ:xl/**` leg.py, `AZ:xt/**` tail.py).
Prefixes: module `#az*` (objective `mb`), objectives `azT azPT azBr azF…`, tags `rlk_mb_az_*`, `rlk_az_shard`, storage
`rlk:mboss az.*`; kit `#ak*`, `rlk_ak*`, storage `rlk:azkit`, font `rlk:mboss_az` **U+E800-E8FF** (E100 hud, E300 minimap,
E400 bossbar, E500 gd, E600 bf, E700 fg; **Apep E900** and Apep's font check includes `mboss_az`), item models
`rlk:mboss/az_kit/*`; rig `rlk:mboss/azhdaha/rig`, `rlk_mb_azhdaha_part`, `rlk_mb_az_<part>`, `azRig*`, UUIDs per Rig
decision change 3.

Generator order (README "등록 · 모듈"): core → arena (plaza, cp_test, az_cavern) → cboss rooms → proto → cproto → rig
generators (Guardian, butterfly, fieldgen, azhdaha) → guardian → bf kit → butterfly → fg kit → fieldgen → az kit →
azhdaha → `check_mboss_pack.py`.

#### 1.6 Registry entry

```json
{ "id": "azhdaha", "n": 10, "kind": "chapter", "ch": [1], "route": false, "enabled": true, "w": 0,
  "minCh": 1, "maxCh": 1, "name": "야타용왕", "sub": "봉인된 바위 용의 왕", "color": "#F2B53A", "el": 5,
  "hp": 260, "xp": 40, "atk": 12, "lvAdd": 0, "dmgMul": 140, "goldMul": 1, "sap": 0, "picks": 0,
  "scale": 0.1, "px": true, "pxBase": 65, "intro": 160, "death": 140, "deathSnd": false,
  "arena": "az_cavern", "theme": "az_cavern", "res": {"0": 30, "5": 30, "*": 10}, "phases": [100],
  "music": {"1": {"ev": "minecraft:music.end", "len": 0}, "2": {"ev": "minecraft:music.dragon", "len": 0}},
  "icon": {"item": "minecraft:raw_gold_block", "model": "rlk:mboss/az_kit/gate_icon"} }
```

- `route: true` at I2 (the only change that makes chapter 1 Azhdaha). `hp` / `dmgMul` are starting values; §6.2 decides.
- Element numbering (`#elem`): 0 physical, 1 Pyro, 2 Hydro, 3 Electro, 4 Cryo, 5 Geo, 6 Anemo, 7 Dendro, 8 Void.
- Music: phase 1 `music.end` (C418 "The End": long, ancient, sealed), phases 2-3 `music.dragon` (C418 "Boss"); both
  single-track stereo events. Switching off = deleting `music` (Q9). The phase-3 call reuses `"2"`.

#### 1.7 Test commands

| command | effect |
|---|---|
| `/function rlk:mboss/test/chapter {id:"azhdaha"}` | `#mbTest 1`, `#cbForce` = 10, chapter 1, `#mapIdx 5`, `#mapType 8`, `room/gen`; the entrance built and entered, the gate pressed as soon as the arena is built |
| `/function rlk:mboss/test/chapter_ch {id:"azhdaha",ch:3}` | the same in chapter 3 (L18) |
| `/function rlk:mboss/test/chapter {id:"cproto"}` | the chapter proto boss (framework checks) |
| `/function rlk:mboss/test/pattern {id:N}` | 1-9 phase-1 patterns (P1-P9); 10 P5b triple stomp (phase 3); 20 landslide; 21 absorb 1; 22 absorb 2; 23 B3 with the pair's tail special; 24 death; 25 B3 from the tail sink (surfacing); 26 intro; 31 orbs; 32 meteors; 33 one fire field under the player; 41 frost / 42 lightning (inside a forced B3); 43 천화; 44 가루; 45 / 46 spikes ice / electro; 60 phase 2 (no sequence); 61 phase 3 at tail-up; 62 phase 3 surfaced; 70 brand (current element); 71 brand clear; 72 shard; 80 HP to the current floor + 1; 90-93 force the pair (90 불/번개, 91 물/얼음, 92 불/얼음, 93 물/번개; recolours a live rig, badges and RES); 99 idle; anything else prints the help |
| `test/lock {id:N}`, `test/level {lv:N}`, `test/kill` (lethal true hit → chapter clear → `k_chapter`), `test/abort` (→ the gate returns, same pair), `test/stop` | as for the mid-bosses |
| `/function rlk:boss/raiden/test/start` | Raiden regression (chapter 2, L12), unchanged |
| full real path (from I2) | `/function rlk:run/start`, `#mapIdx room` 4, `#mapType room` 8, `/function rlk:run/next_map` → chapter 1 → Azhdaha; chapter 2 / 4+ → Raiden |

---------------------------------------------------------------------------------------------------

### 2. Scale and arena

#### 2.1 Scale (R1 unchanged)

H = 7.0 b. The footage consensus is 8.3-9.5 m with consistent ratios (claw span 1.1-1.2 H, eye ≈ 2 m head-low,
nose → rump ≈ 1.46 H, tail 1.5-1.7 L); v2 / v9's 5.4-5.7 m reading is rejected ([mod] §1.1). 7.0 b reads as huge
(≈ 3.9 player heights to the plates) and fits the r 28 floor with the tail laid out. Known deviation: the head-low eye
height is 1.5 b (just under the player's eyes) instead of the footage's 1.29 player heights; melee reach is horizontal to
the head column (§3.3), so only the look changes.

#### 2.2 Arena `az_cavern` ("「복룡목」 아래", the earth-core rock bed)

| item | spec |
|---|---|
| centre / radii | (320, 201, 8), stand height 201; **walk 28**, **safe 26** (body leash, ground-target clamp); rough rock wall 28 < d ≤ 33 with noise; box x 280..360, z −32..48, y 190..240 |
| build | theme `T:mboss_arena_az_cavern.py`; per-arena `ensure/build/build_slice/rebuild/clear/sweep` under `F:mboss/arena/az_cavern/`; stamp `rlk:mboss built_az_cavern = "az_cavern@<ver>:default"` + sentinel; **≤ 40 slices** (one per tick, each fill ≤ 32 768 blocks) started by `prep` at entrance build, so it is done long before the gate can be pressed; forceload on demand (36 chunks) |
| arrival | (320.5, 201, 34.5) yaw 180, facing the boss spawn at the centre (the body faces south) |
| boss body disc | anchor ≤ 8 b from the centre at idle and for jump / burrow destinations; ≤ 12 b during a charge (the next decisions leash it back at 0.13 b/t); **P7 and P8 are only picked while the anchor is ≤ 8 b from the centre** (tail tip ≤ 16.75 / 17.75 b from the anchor, so ≤ 25.8 b from the centre) |
| ceiling | dome of tuff / deepslate / smooth basalt, apex y ≈ 238, rim y ≈ 214; **no solid block below y 216 inside r 28** (rear-ups reach 9-10 b, the tail column 9 b, the jump apex ≈ 3.5 b); barrier cap on the wall ring as on the plaza |
| floor (opaque, burrow-safe) | walk disc: **full opaque blocks only** at y 200 (mud, packed mud, polished tuff, tuff, smooth basalt, andesite, mossy cobblestone, yellow-terracotta Geo cracks) and **solid fill y 192..199 under r ≤ 14** (the rig sinks to −7.5 b = y 193.5; nothing hollow or lit may show through). No glass, water, slabs, leaves or other light-transmitting block inside r 28. Real 1-deep water only in rim pools beyond r 28 |
| "shallow water" look | **4 × 4 tiles of 14 b** (one sprite, display scale) of translucent water sheet at **y 201.005** (the kit's decal layers sit at ≥ +0.03, so ≥ 0.025 b clear), about 40 % alpha, element-tinted (§2.6); splash / `bubble_pop` / `dripping_water` on impacts |
| pillars | 6 massive irregular pillars (r 2.5-3.5; deepslate bricks, polished blackstone, tuff bricks with gold vein lines) half sunk in the wall at r 29-31; 2-3 broken stubs (h 1-2) at r 25-27 (decor only: hazards ignore cover) |
| steles | 8 carved tablets (3 × 5; chiseled tuff bricks, chiseled stone bricks, polished tuff, gold inlays) at r 29-30; **the two at the arrival repeat the entrance glyphs** of the rolled pair (kit glyph props, per fight) |
| hanging gold crystals | 20-30 stalactite clusters (raw gold / gold blocks with yellow / orange stained glass shells, ochre froglight / shroomlight cores, pointed dripstone fringes), tips ≥ y 216; golden roots (stripped jungle log, mangrove roots) down the north wall |
| per-fight props | **all display props are fight entities** (`rlk_mb_aux rlk_mb_ar_az`, never `rlk_room`): 16 water-sheet tiles, 16 `arena_crystal` element crystals on the clusters and the rim, the 2 arrival glyphs, the 6 intro seal steles + the seal prism (spawned by `seq.py`, §5 E). Spawned by `AZ:arena/props` at fight start (≥ 40 t after the forceload, guarded by "none alive"), killed by `cleanup_aux`, re-made by the module `reload` |
| light | hidden `light` blocks at y 206 over the disc, level 9 (dark but legible) in every phase; crystal glow; drifting gold `dust` motes |
| intro dressing | the floor glyph circle (kit decal) and the per-fight seal props (§5 E) |

#### 2.3 Domain entrance (chapter-1 dungeon, zone 2, kind 9)

- A Liyue stone arch (stone bricks, polished andesite, dark-oak beams, gold trim) of normal zone size, gold Geo cracks on the
  floor, the gate object `k_cboss` in the middle.
- **Glyph stele** (the original tell, [v1] §1): a tall dark stele left of the gate with a small gold emblem and two coloured
  glyphs, **upper = tail element (Cryo `#9FE8F5` / Electro `#A291D0`), lower = leg element (Pyro `#FF8A3D` / Hydro
  `#8CCCDE`)**, kit glyph props (snowflake / bolt / flame / water curl) with a soft glow particle every 10 t (`rlk_room`
  entities of the zone).
- Generated by `T:build_cboss_rooms.py` with `entrance_layout()` from the theme.

#### 2.4 Kit deliverables (S1-FX; frozen at S1 start; S1-FX stays on call as S2-FX)

| kind | item | used by | `test_az_fx.py` case |
|---|---|---|---|
| telegraph | `disc`, `ring`, `sector` (any half-angle in 7.5° steps), `line`, `wave`, `mline` (moving lanes with ids) | all | shapes, sizes, `el` palettes, `nd` look |
| telegraph | `lane_side` (flank strip, undodgeable look) | P6 | |
| telegraph | `wedge_union {id}` (annular-sector polygon from stacked cards, arbitrary angles; draws the union of the whip's per-tick wedges) | P7 | decal = generator union |
| telegraph | `heptagram {r}` (star {7/2} with meander tips and the central rune) | 41 | |
| telegraph | `hexagram {r}` (+ the 번개 rune) | 46 | |
| telegraph | `seal8 {r}` (two squares, 火 runes) | 32 | |
| telegraph | `mask_wash {r}` (one floor-wide violet card) + `safe_rim {id,r}` (green rim + glyph) + `safe_beam {id}` (particle column) | 42 | ≤ 6 cards per round |
| telegraph | `crater {r}` (rubble ring at the floor cut) | B3 | |
| telegraph | `halo {r}` (air ring over a landing spot) | 32 small meteors | |
| field pool | `tele/field {id,r,el,life}`, `tele/strip {id,len,w,yaw,el,life}`, `tele/field_end {id}`, `field_redraw` (from the module table) — **not counted against the attack-telegraph cap** (TCAP 40 / skip ≥ 34 stays for attack telegraphs; field pool 16 cards) | N6, 33, 45, P7 / P8 strips | zero skipped attack telegraphs on each pair's worst concurrent timeline |
| preset | per element (Geo, Hydro, Pyro, Cryo, Electro): impact burst, crack fan, blade crown, dust ring, slab / boulder throw, footfall, brand rune, absorb vortex, recolour wave, sigil cards (火 / 水 / ❄ / ⚡) | all | callable, budgets |
| preset | water geyser, water blade trail, fire lump trail, meteor fall (big / small), fire dome, frost burst, ice-wall piece, hail, bolt (single / round), shell dive, icicle trail, ice sphere aura, orb ribbon, spark column, stele shatter, seal-prism shatter, seal reform, petrify pulse | §5 | |
| prop | `arena_crystal` and `water_sheet` (looks geo / hydro / pyro / cryo / electro), `glyph_<el>` (pyro, hydro, cryo, electro, geo), `seal_stele` (+ shatter chunks), `seal_prism`, `gate_icon`, `orb`, `meteor_big`, `meteor_small`, `lump`, `shell`, `icicle`, `ice_sphere`, `spike_<geo/cryo/electro>`, `cone`, `shard` (응결 결정), `crater` | §2, §4, §5 | models + sprite rules |
| HUD | font `rlk:mboss_az` U+E800-E8FF: badges ◈ per element (dim `#707070` / lit), brand badge, under-bar glyphs, banners (transition message, absorb, brand tutorial), "점프!" cue, safe-zone line, hint lines | §4.11 | glyphs present |
| sound | the recipes named in §5 (vanilla events only) | §5 | callable |

Budget: ≤ 64 fx / 40 attack telegraph cards and 16 field cards at the worst concurrent timeline of each pair; atlas
≤ 0.6 M px; sprite sides multiples of 16, ≤ 512.

#### 2.5 Lighting

No resource-pack fog or shaders. The hidden light layer stays level 9 in every phase; the phase colour is carried by props
and particles (§2.6).

#### 2.6 Element recolour of the arena (N17, `AZ:arena/look {el}`, owned by S1-MOD, called by S2-S)

| moment | change |
|---|---|
| fight start | all `arena_crystal` and `water_sheet` props → `geo` look (warm gold); drifting gold motes |
| absorb 1 burst | a recolour wave from the boss outward over 20 t: props → the leg element look (Hydro blue / Pyro red-orange); ambient particles: Hydro `dripping_water` + `falling_water` + blue dust; Pyro `lava` + `flame` + ember dust |
| absorb 2 burst | props → the tail element look (Cryo cyan + falling `snowflake` / white dust; Electro violet + `electric_spark` + `witch`); the leg-element particles stay at half rate |
| footfalls (every phase) | per-element footfall preset on the `walk` / `turn*` plant events: Geo dust, Hydro splash, Pyro flame splash (v9 A), plus the tail element frost / spark at the tail tip in phase 3 |
| death | props fade back to `geo` during the seal; the next fight starts from `geo` |

---------------------------------------------------------------------------------------------------

### 3. Rig follow-up

#### 3.1 Stages and rules (§7 has the graph)

- **R1** (done, `wip/az-rig` 7c3e9fe: 46 parts, 0.95 M px, 12 proxy points, 11 debug poses).
- **R2** (running since R1, on the layout this plan wants): four refiners on **`wip/az-rig-<head|body|legs|tail>`** (all
  from 7c3e9fe) with their own worktrees `S:az/wt_rig_<region>` and RP sandboxes `S:az/rp_rig_<region>`. Each edits only
  `T:azhdaha_<region>.mjs` (its geometry, sprites, looks) and commits sources + renders. `azhdaha_pose.mjs` joint or
  PART_SCALE edits are allowed only as small changes listed in the commit message (the R3 merger reconciles them); the
  builder, the aggregators, `azhdaha_clips.mjs`, `azhdaha_shape.mjs` and `azhdaha_materials.mjs` are not edited in R2
  (requests to R3). **Per-region budgets** (respected now, asserted by the builder from R3): parts head ≤ 8, body ≤ 14,
  legs ≤ 16, tail ≤ 10 (total ≤ 48, cap 56); atlas head 0.30, body 0.30, legs 0.32, tail 0.28 M px (≤ 1.2 M). The
  generated `AZ:rig/**` and the manifest are rebuilt by the merger, never hand-merged.
- **R3 integrate** (one owner, `wip/az-rig`): merges the four region branches, fixes seams, runs the full critique; then
  merges `M0` and **RIGLIB** (Rig decision change 2; RIGLIB must land before R3a because the clips need `tol.tp`,
  `follow_y` and the per-state follow lists); adds the per-region budget asserts, the UUID name table (Rig decision
  change 3) and the hidden-state root offset check (Rig decision change 1).
- **R2 review items** (from the critiques): Cryo tail = ice coral + frost on the tail and white-cyan blossoms; Electro tail =
  violet slits + lilac blossoms; phase-1 gold is **matte** (brightness 13, no glow) and flares to 15 only through
  `glow/gold_on|off` (the 천동만상 tell, the absorbs); eyes red at 15 in every phase; `look/petrify` exists (mandatory).
- **U1**: after the R3 integrate step the user gets the model renders (rest in 4 views, the 4 element combos, the player for scale,
  the head close-up). U1 does **not** block R3a; proportion feedback that moves joints becomes a numbered change note.
- **R3a — manifest v1** (before S2 starts): every clip of §3.2 blocked out on the frozen skeleton with its final length,
  event ticks, anchors, per-tick proxy and tail tracks, yaw schedules, hidden spans and root offsets (§3.6). The manifest
  schema and the event ticks are frozen from here.
- **R3b — polish** (parallel to S2): poses only; any change of a length, event tick or anchor needs a change note and
  triggers the affected S2 suites.
- Whole-body yaw is the module's (the anchor turns by the exported schedule, `teleport_duration` carries it); clips carry
  no horizontal root travel and no root yaw, except the hidden-state root offset of Rig decision change 1.

#### 3.2 Clip list (binding names, lengths and events; authored at footage speed, RETIME → played; events in played ticks)

| clip | authored | RETIME knots (authored → played) | played | events (played) | module |
|---|---|---|---|---|---|
| `idle` | 80 loop | — | 80 | `snarl 30` | ≤ 3°/t tracking |
| `walk` | 40 loop | — | 40 | `lh 0 lf 10 rh 20 rf 30` | glide 0.13 b/t; footfall fx |
| `walk_stop` | 16 | — | 16 | `plant 4` | |
| `turn45_l/_r` | 24 | — | 24 | plants 10, 17; `yaw0 4 yaw1 18` | yaw 45° by the exported schedule |
| `turn90_l/_r` | 36 | — | 36 | plants 12, 18, 24, 30; `yaw0 6 yaw1 30` | yaw 90° by schedule |
| `turn180` | 60 | — | 60 | plants 12 … 54; `yaw0 6 yaw1 54` | yaw 180° by schedule |
| `intro` | 150 | — | 150 | `eyes 25 rise 30 crack1 50 crack2 70 seal 112 land 116 roar 120 blast 130` | untargetable |
| `pose_ref` | 20 loop | — | 20 | | renders |
| `roar_low` | 50 | [0,0][10,8][50,40] | 40 | `roar 8 blast 10` | |
| `roar_rear` | 100 | [0,0][20,20][76,62][100,82] | 82 | `rise 8 roar 20 drop 62 land 74` | specials start from `roar` |
| `chin_slam` | 84 | [0,0][47,35][84,65] | 65 | `lift 2 rear 14 top 23 drop 32 impact 35` + impact anchor | tracks until 10; head low 35-55 |
| `jump_slam` | **60 (re-authored: crouch 0-6, take-off 8, apex 18, land 28, wave 2 39, per [v2] B)** | [0,0][28,21][60,53] | 53 | `crouch 0 takeoff 6 apex 13 land 21 wave2 32` | `mv/leap` 6 → 21 |
| `charge_coil` | 34 | [0,0][32,24][34,26] | 26 | `coil 6 launch 24` | lane locks at 14 |
| `charge_run` | 12 loop | — | 12 | `plant 6` | glide 1.0 b/t |
| `charge_stop` | 24 | [0,0][8,8][24,21] | 21 | `skid 0 stop 8` | skid yaw ≤ 30° |
| `spikes` | 48 | [0,0][18,14][24,20][48,40] | 40 | `brace 0 launch 14 launch_last 20` + 4 launch-point anchors; `gold_on 0 gold_off 22` | |
| `stomp_fl/_fr/_hl/_hr` | 72 | [0,0][22,17][52,47][72,63] | 63 | `lift 5 slam 13 w1 17 w2 32 w3 47` + paw anchor | wave gaps 15 kept |
| `stomp3_fl/_fr` **(new)** | 90 (paw A lift 0-20, slam 22; paw B lift 30-40, slam 45; paw A lift 52-62, slam 68) | [0,0][22,17][90,85] | 85 | `lift 3 s1 17 s2 40 s3 63` + the paw anchor per slam | gaps 23 kept; phase 3 front stomps |
| `feint` | 56 | [0,0][22,22][56,50] | 50 | `sway 0 swayback 12 drop 18 burst 22` | undodgeable floor |
| `tail_whip_l/_r` | **64 (re-authored)** | — | 64 | `raise 0 cock 12 pivot 20 sweep 23 sweep_end 31 erupt 33 settle 42` + per-tick tail-root / tail-tip tracks t20-35 | yaw schedule 0 → 115° (t20 → 31, smoothstep), 122° at t35, 115° at t42 |
| `tail_slam` | 90 | [0,0][52,39][58,45][90,70] | 70 | `raise 0 hold 9 slam 36 impact 39 spikes 41` + tail root / tip anchors | then `turn180` if needed |
| `burrow_dive` | 44 | [0,0][18,14][44,40] | 40 | `snarl 3 dive 14 under 40` | glide 3 b, 14 → 36 |
| `burrow_travel` | 20 loop | — | 20 | | hidden (scale 0), 0.3 b/t |
| `burrow_breach` | 36 | — | 36 | `ring 0 burst 8 hit 10 under 30` | decal ≥ 12 t before |
| `burrow_emerge` | 56 | [0,0][40,40][56,53] | 53 | `rumble 0 burst 8 fore 24 out 38 shake 40` | decal ≥ 12 t before |
| `landslide` | 270 | [0,0][76,57][104,77][132,98][156,118][186,139][212,159][240,179][270,203] | 203 | `tell 0 w1 57 w2 77 w3 98 w4 118 w5 139 rear 159 w6 179 end 203` | turns in place 0-45; anchor fixed |
| `absorb` | 108 | [0,0][12,12][60,46][108,94] | 94 | `press 0 rise 46 burst 47 stamp1 62 stamp2 86`; `gold_on 0 gold_off 60` | untargetable |
| `absorb_p3` | 70 | [0,0][60,42][70,52] | 52 | `orb 0 burst 42 gather 42`; `gold_on 0 gold_off 50` | untargetable |
| `p3_sink` | 80 | [0,0][8,8][50,40][80,66] | 66 | `sink 8 under 40 tail 40 pillar 58`; root z offset applied while hidden (RDC 1) | hidden glide 40 → 56 |
| `tail_pillar` | 80 loop | — | 80 | `pulse 0 pulse 40` | tail-only state |
| `tail_pillar_strike` | 24 | — | 24 | `strike 10` | cue per lightning round / ice circle |
| `tail_pillar_sink` | 20 | — | 20 | `gone 18` | |
| `tail_cast` **(new)** | 40 | [0,0][24,18][40,34] | 34 | `raise 0 charge 12 fire 18 lower 26` + tail-tip anchor | replaces `[mot]` `tail_shells` |
| `death` | 120 | — | 120 | `stagger 0 chin 34 tail 66 last 80 head 92 still 96` | `look/petrify` at 96 |

41 entries (35 authored + 6 mirrors: `turn45_r`, `turn90_r`, `stomp_fr`, `stomp_hr`, `stomp3_fr`, `tail_whip_r`). The module
reads every tick from the manifest; S1-MOD keeps a per-clip fallback only for clips missing from the current manifest
(`stub_rig.py`), and the I2b build asserts the fallback list is empty.

#### 3.3 Hit proxies (12 ground columns; data from `azhdaha_pose.mjs` PROXIES, runtime from the framework)

| proxy | UUID | bone | rest (s, f) b | w | vulnerable in |
|---|---|---|---|---|---|
| head | 0x41 | head | 0, +4.3 | 2.8 | normal |
| chest | 0x42 | chest | 0, +2.1 | 4.6 | normal |
| belly | 0x43 | belly | 0, −0.5 | 4.6 | normal |
| hips | 0x44 | pelvis | 0, −3.4 | 4.4 | normal |
| tail1-tail4 | 0x45-0x48 | t1, t3, t5, t7 | 0, −6.35 / −10.12 / −12.86 / −11.9 (curled) | 2.6 / 2.2 / 1.8 / 1.4 | normal, **tail_only** |
| paw_l / paw_r | 0x49 / 0x4A | paws | ±3.15, +2.95 | 1.8 | normal |
| foot_l / foot_r | 0x4B / 0x4C | hind feet | ±2.5, −2.55 | 1.8 | normal |

- **Columns stand on the anchor floor** (y offset 0) with `height` = the bone's top + margin; melee distance is therefore
  horizontal, and arrows / camera aim hit the box. A proxy whose top is ≤ 0.3 b, or whose bone is hidden, is parked.
- **Per-tick tracks** for every moving clip (keys + linear interpolation in the manifest); the framework compiles them into
  key functions that update the `px/follow` storage when a proxy moves > 0.15 b.
- **Framework state sets** (from the manifest `states`): `normal` (all 12), `jump` (none), `inv` (none; body
  `rlk_mb_inv`), `tail_only` (tail1-4 on their tail-only tracks: all at the anchor, stacked), `dead` (none). Vulnerable =
  carries `rlk_mob`. `px/state {set}` also calls the rig visibility function the manifest names (`state/normal|burrowed|
  tail_only`).
- **Hit flash** outlines only the part group of the hit proxy (head / front / rear / tail), never all parts.
- **Coverage check** before the R3a merge: a 3-D variant of `rigtech_cover.py` on the real rest and clip boxes (distance
  from the feet of a player standing 0.4 b outside the outline to the nearest column position); target 100 % of the
  outline within 3.0 b in `normal`, and every tail-only point within 3.0 b of a tail column.

#### 3.4 Burrow and tail-only states

- The root sinks below the opaque floor (§2.2); fully buried parts at scale 0 (`visBody` / `visTail`); hidden parts are
  skipped in `follow` (per-state follow lists, RIGLIB); the husk never goes into blocks (anchor on the floor, `NoGravity`).
- **Tail-only pose** (re-authored by R3a with Rig decision change 1): body hidden, root sunk ≥ 6.4 b with the z offset that
  puts the pillar base on the anchor; the tail a pillar ≈ 8-9 b tall; a crater prop (kit `crater`, UUID 0x81) at the floor
  cut; the anchor is moved to the arena centre during the hidden glide of `p3_sink`.
- The body husk is scale 0.1 with no shield in every state (R8), so nothing invisible blocks arrows or pushes players in
  the burrow states. The body push (N12) is off in every hidden state (§4.12).
- `follow_y<k>` sink offsets (RIGLIB) for zero-key straight descents ([rig] §2.8).

#### 3.5 Element looks per phase (R6, [mod] §4.2)

| channel | phase 1 | phase 2 | phase 3 | parts |
|---|---|---|---|---|
| legs (`look/legs/<geo\|hydro\|pyro>`) | geo | leg element | leg element (kept) | bracers, paws, gaiters, feet, apron, belly cracks + the 5 tinted glow overlays (brightness 15) |
| tail (`look/tail/<geo\|cryo\|electro>`) | geo | geo | tail element | plate groups, neck ruff, tail spikes, branch; leaves → **Cryo: ice coral + frost, white-cyan blossoms; Electro: violet slits + lilac blossoms** |
| gold | matte (13) | matte | matte | horns, crystals, studs; `glow/gold_on|off` lifts them to 15 for the 천동만상 tell and the absorbs |
| always | red eyes (15) | | | |

`look/petrify` (death seal: base looks at brightness −3 and a gold rim pulse) is mandatory. Absorb clips switch the look at
their `burst` event; reload and tests re-apply both channels from `#azPh` + the pair.

#### 3.6 Rig API additions and manifest schema v1 (frozen at R3a; checked by `check_az_manifest.py`)

API: `state/<normal|burrowed|tail_only>` (visibility), `look/legs/*`, `look/tail/*`, `look/petrify`, `glow/gold_on|off`,
`flash/<head|front|rear|tail>`, `face/*`, `play/<clip>`, the shadow display (`shadow_radius` 4.5) following the anchor, and
the fixed UUIDs of Rig decision change 3. The rig no longer owns any proxy runtime (`px/*` is the framework's).

Manifest, per clip: `id`, `len`, `loop`, `next`, `retime` knots, `events` (played ticks), `anchors` per event (named points
in the anchor frame: `nose`, `impact`, `paw_fl|fr|hl|hr`, `tail_root`, `tail_tip`, `launch_1..4`, `back`), `tracks`
(per-tick `tail_root` / `tail_tip` for `tail_whip_*`, `tail_slam`, `tail_cast`, `tail_pillar*`), `px` (per-tick proxy
columns `{x,z,top}` as keys + `lerp`), `yaw` (the schedule for `turn*` and `tail_whip_*`), `hidden` spans, `root_z` spans
(Rig decision change 1), `state` changes. Global: `states` (with the proxy sets and visibility functions), `capsules` (push
capsules per state: torso |s| < 2.8, f −3.8 … +2.6; head |s| < 1.6, f +2.6 … +5.4 while the head proxy top ≤ 3.5),
`flash_groups`, `looks`, `proxies.layout`, `uuids`, `budgets`, `culling`. The schema is shared with the S1-MOD stub
fallbacks, so S2 codes against the same structure from day 1.

---------------------------------------------------------------------------------------------------

### 4. Mechanics

#### 4.1 Element roll and display

- **Roll** in the module `prep` hook (entrance build; "on entry", Q1): `random value 0..3` → pair 0 불/번개
  (`#azLeg 1`, `#azTail 3`), 1 물/얼음 (2, 4), 2 불/얼음 (1, 4), 3 물/번개 (2, 3) (the wiki's weekly order). Stored in
  `#azLeg mb`, `#azTail mb`, storage `rlk:mboss az.pair {leg,tail}` and the zone marker `data.az_pair`. The module `spawn`
  re-reads them from storage (its `ai/vars` reset never touches them). Kept for retries of the same boss map (abort,
  a test death); cleared by `run/start`, `run/end`, `test/stop`. `test/pattern 90-93` forces a pair.
- **Display**:
  1. the entrance stele glyphs (upper = tail, lower = leg; §2.3);
  2. the gate label `k_cboss` (text components from `rlk:mboss cprep.azhdaha`): line 1 **야타용왕** (gold), line 2
     "흡수 원소: 물 (다리 · 2페이즈) · 번개 (꼬리 · 3페이즈)" in the element colours, line 3 "내성: 물리 · 바위 · 물 ·
     번개 30% · 그 외 10%";
  3. gate click title "야타용왕", subtitle "봉인된 바위 용의 왕 · 물 / 번개";
  4. the two arrival glyph props in the arena;
  5. boss bar name line `Lv.6 야타용왕` + `extra[]` badges `◈물` `◈번개` (kit glyphs), **dim `#707070` until absorbed**,
     then the element colour (Pyro `#FF8A3D`, Hydro `#4FB8FF`, Electro `#C58BFF`, Cryo `#9FE8F5`).

#### 4.2 RES (user, binding)

Physical 30 · Geo 30 · the rolled 불-or-물 30 · the rolled 얼음-or-번개 30 · every other element 10 (Anemo, Dendro, Void
and the two non-rolled elements), **flat from the entry**. The registry `res` gives 0 / 5 / `*`; the module `spawn` writes
`mbRes<#azLeg>` and `mbRes<#azTail>` = 30 on the body (R7). Reactions are resisted as their element (Overload on a
Pyro-leg Azhdaha = Pyro 30). A generator switch `RES_BY_PHASE` (default off) gates the rolled two on `#azPh` (Q2). No RES
numbers on the bar; the gate label carries them.

#### 4.3 Phases, floors, transitions

| | phase 1 | transition 1 | phase 2 | transition 2 | phase 3 (B3) | phase 3 (surfaced) |
|---|---|---|---|---|---|---|
| element | Geo | Geo | + leg element | leg element | + tail element | both |
| `#mbFloor` | F1 = ⌈mhpM × 2/3⌉ | F1 until the absorb-1 end | F2 = ⌈mhpM / 3⌉ | F2 until the absorb-2 burst, then **1** | 1 | 0 from B3 `out` |
| looks (legs / tail) | geo / geo | legs at the absorb burst | leg / geo | tail at the absorb burst | leg / tail | leg / tail |
| music | `"1"` | `"1"` | `"2"` | `"2"` | `"2"` | `"2"` |

- **Floor** (R6): the module keeps `#mbFloor`; the core clamps after the module `incoming`. A hit with
  `mhpC − raw ≤ #mbFloor` (`#mbFloorHit 1`) in phases 1-2 queues the transition (`#azTr 0 → 1`); the module tick also
  queues when `mhpC ≤ #mbFloor` (DoTs, reactions). While clamped the module shows the popup **"흡수 중"** with the
  unclamped value in grey (`#mbFloorRaw`) at most once per 10 t.
- **Queue → start**: the transition service starts at the next decision point instead of a pick; a running pattern is never
  cut (its hazards stay fair) but ends at its `release` point if it has one. At the queue the bg-T emitter is cancelled;
  live orbs (bg-L) stay but ride harmlessly high (§5 31) for the whole transition (landslide and absorb).
- **Transition 1** (services 20 → 21): message → walk to the centre → 파멸의 산사태 (Geo) → absorb 1 (leg) + `roar_rear`
  → the leg special at the roar → phase 2.
- **Transition 2** (32 / 31 → 20 → 22 → 23): message (the tail element named) → **the leg special first** (32 meteors
  always cast with their `roar_rear`; 31: live orbs are refreshed to full life with a `roar_low` cue and no new roar, else
  cast with `roar_rear`) → walk to the centre → 파멸의 산사태 (the leg element + brand, no fire-rule fields) → absorb 2
  (tail) + `roar_rear` → B3.
- **Message** (kit banner 60 t + `block.bell.resonate` p 0.6 + `block.respawn_anchor.charge` p 0.5):
  **"야타용왕이 곧 물 원소의 힘을 흡수합니다…"** (transition 1 = leg element, 2 = tail element).
- **Untargetable** only during the absorbs (`px/state inv` + cine). The landslide is targetable but floored, so the wiki's
  "stop attacking and move away" stays the right play; true damage still works.
- **Reload** re-derives the step from `#azTr` / `#azPh` / `#azBur` and the service clocks (fieldgen precedent): a cut
  landslide resumes at its next wave, a cut absorb finishes at once (looks applied), a cut B3 resumes at its frame tick
  (the tail special restarts its schedule from the current B3 tick).

#### 4.4 Absorb "cut-scene" and recolours

No camera control (no FOV change; the player keeps control): the boss's clip + the kit's absorb preset (element vortex,
sigil cards 火 / 水 / ❄ / ⚡, rune glow) + `glow/gold_on` + the banner **"물 원소 흡수"** (phase 3: **"번개 원소 흡수"** with
the sub-line "원소를 추가로 하나 더 흡수합니다"). `mboss/cine/start` at the absorb start (no boss hit can land on the
player; orbs and fields are harmless), `cine/end` at the following `roar_rear`'s `roar` event. At the `burst` event: the
looks switch (§3.5), the arena props recolour (§2.6), and a **push-only ring r 8** (`mboss/push/ring {r:8,kb:4}`, no
damage, skipped for players whose landing point is inside a live hazard) clears players off the body. The phase-2 brand
banner shows once when gameplay resumes after absorb 1 (the `roar_rear` start).

#### 4.5 Element rule per phase (N1)

- **Phase 1**: every hazard is Geo.
- **Phase ≥ 2**: every **ground-eruption** hazard takes the leg element and brands: crack discs and fans (P1), landing
  and wave fronts (P2, P5, P5b), spike landings and explosions (P4), flank strips and end discs (P6), the whip's eruption
  discs (P7), the tail-slam spike line (P8), the B3 emergence burst, the second landslide. **Body-contact** hazards stay
  Geo: the charge disc (P3) and the whip's sweep wedges (P7). The charge gets no extra (the wiki's "lure this one").
- **Phase 3**: tail-borne hazards take the tail element: the P7 / P8 phase-3 addons, 41-46. The leg rule continues.

#### 4.6 Addon points (N13; `api.ADDON_POINTS`, the contract between the host and element authors)

Every point is called at **event − 12 t** (lead 12) as the boss, at a context marker `rlk_az_ctx` (position and rotation
given below) with the context scores listed; the body schedules its own hits relative to the event and uses `api.after`
for tails that outlive the host. The host authors (S2-A, S2-B) must call every point; `pat_leg.py` / `pat_tail.py` call
them directly with a synthetic context. Missing bodies emit no dispatcher line.

| point | host event (played) | context | Hydro (xl) | Pyro (xl) | Cryo (xt) | Electro (xt) |
|---|---|---|---|---|---|---|
| `chin/impact` | P1 impact t35 | impact point, crack-line yaw | geyser disc r 3.0 on a random side 5-7 b off the impact (perpendicular to the crack line), decal from the call, **hit t45** (tell 22), 0.8, own group; curved stream decals (cosmetic) | 3 lumps, **one group, 0.6**: launch t43, land t69 (flight 26), decals r 2.2 from the launch; targets 1 × `lockv` (lead 8) + 2 random 7-14 b from the impact, each moved out of the clear melee points; each leaves a fire field r 4.0 / 160 t | frost ring front r 1.5 → 6 (0.75 b/t, band 1.5) from t37, own group, 0.6 + stack | 3 bolt discs r 1.8 at 4 / 7 / 10 b along the crack line, hits t47 / 50 / 53, decals from the call, **one group**, 0.6 |
| `jump/land` | P2 land t21 | landing point, yaw to the player | 8 water blades from r 2 at 2.0 b/t, launched t25, life 6 t, hr 1.6, prop 0.9 b up, **in the landing group**, 0.5; lane decals from the call | — | frost ring front r 1.5 → 6 from t23, **in the landing group** | — |
| `jump/wave2` | P2 wave 2 t32 | landing point | — | 3 lumps, one group, 0.6: launch t32, land t58; fields r 4.0 / 160 t | — | 3 bolt discs r 1.8 at 4 / 7 / 10 b along the line to the player, hits t34 / 36 / 38, **in the wave-2 group** |
| `stomp/w1` | P5 w1 t17 | paw point, paw id | 8 blades from r 2 at 2.0 b/t, launched t21, life 6 t, **in w1's group**, 0.5; lanes from the call | — | frost ring in w1's group (hind stomps in phase 3) | — |
| `stomp/w3` | P5 w3 t47 | paw point | — | 3 lumps, one group, 0.6: launch t49, land t75; fields r 4.0 | — | 3 bolt discs in w3's group (hind stomps in phase 3) |
| `stomp3/s1` | P5b s1 t17 | paw A point | blades as `stomp/w1`, in s1's group | — | frost ring in s1's group | — |
| `stomp3/s3` | P5b s3 t63 | paw A point | — | 3 lumps, one group, 0.6: launch t65, land t91; fields r 4.0 | — | 3 bolt discs in s3's group |
| `whip/sweep` | P7 sweep t23 | tail root, side, swept range `#azCtxA0/A1` | — | — | ice-wall pieces on the swept arc (annular band r 5-12 from the tail root), erupting 2 t behind the tail at t25 / 27 / 29 / 31, own group, 0.8 + stack; hail strip on the band 60 t, 0.15 / 10 t | — |
| `whip/end` | P7 eruption t33 | end-line point and yaw | — | — | — | 3 bolt discs r 1.8 at 4 / 8 / 12 b along the end line at t36 + a crystal line `hz/line` len 12 w 2.4 at t46, **all one group**, 0.6; Electro strip (N6 line len 12, w 4, 80 t, 0.2 / 10 t + brand) from t48 |
| `tailslam/impact` | P8 impact t39 | tail root, line yaw | — | — | Cryo strip along the line (len 13, w 3.5, 60 t, 0.15 / 10 t + brand) | Electro strip, same size |

Phase-2 extras that are not addons (host rule, §4.5): P4, P6 and the whip / tail-slam eruptions simply carry the leg
element (Hydro adds a cosmetic water spray, Pyro gets fields through the fire rule 33).

#### 4.7 Lingering fields and the fire rule (N6, 33)

- Families: **fire** (Pyro), **hail** (Cryo), **strip** (Cryo / Electro). Caps: fire ≤ 4, hail ≤ 2, strip ≤ 1 alive;
  total lingering area ≤ 220 b²; the oldest of the family (or overall) is cancelled (hazard + kit field slot).
- **One volley group per family**: one tick per 10 t however many fields of that family overlap; `#hzRearm 10`; coef 0.2
  (fire), 0.15 (hail, strips); entering or standing inside refreshes the brand at most once per 20 t, never adds Cryo
  stacks.
- **Clear melee points**: pattern fields (P1 / P2 / P5 lumps, meteors, 45's hail) are never centred within r_field + 1.5 b
  of the **head-front point** (the head column's floor point + 2.5 b forward) or the **tail-lane point** (tail2's floor
  point); a target inside is pushed radially outward. Fire-rule fields under a hit player are exempt (they are the
  punishment).
- **Refresh** = `hz/extend` up to 2× the base life; the kit field slot is redrawn with the same id.
- **Field-area gate**: while the total lingering area is ≥ 150 b², the picker skips field-making patterns (Pyro P2 / P5
  extras, P4 → 45, P8's strip, the chin's Pyro lumps, 32).
- **33 화염 잠식** (phase ≥ 2, Pyro legs): whenever a Pyro brand is applied or refreshed **by a strike hit** (not by a
  field, not during the landslide), a fire field r 4.5 / 160 t appears under the player; if a fire field lies within 4 b it
  is extended instead. The hook is `p/firefield/on_brand`, called by `brand.py` when the file exists.

#### 4.8 Phase-3 opening (B3) and death

- B3 (service 23, §5 B3): dig in place → hidden glide to the centre → the tail rises (`tail_only`, floor 1, `#azBur 1`) →
  ≈ 14 s tail window with the tail element's burrow special (41 / 42) while the phase-2 hazards keep going → the tail sinks
  → emergence burst at the centre → `px/state normal`, floor 0. If `mhpC` is 1 at the surfacing: sub-line **"마지막
  일격!"**, a gold glow on the proxies, and the next hit kills through the normal path.
- Death (service 24, §5 D): hazards, fields, emitters, orbs, shards and the brand cleared; music stopped with a sting;
  typed lines; the seal re-forms and the rig petrifies, then scales out (registry `death` 140).

#### 4.9 Pause, reload, cleanup

- **Pause** (framework `pause_tick`: dead, reviving, selection screen, no tagged player): the module clock, the AI, the
  background emitters, the `api.after` timers, the brand clocks and the shard life freeze; the kit's attack telegraphs are
  cleared and the field-decal pool is redrawn from the module field table on resume; music stops and the phase track
  restarts on resume.
- **/reload**: scores survive; the rig respawns through `rig/tick`; proxies are respawned by `px/spawn` (fixed UUIDs) and
  re-stated from the module's state score; arena props are re-made (`AZ:arena/props`); orbs and fields are re-made from
  the module tables (positions, remaining life); shards die (accepted); the transition / B3 step is re-derived (§4.3).
- **Cleanup, death, abort, uninstall**: hazards, fields and their kit slots, emitters, orbs, shards, the brand and its
  sidebar line, arena and seal props, the crater, music, the forceload, `#mbFloor`, `#mbCine`, `#mbPushOn` are cleared;
  the element pair survives an abort (same boss map) and is cleared at the run's end.

#### 4.10 The brand (낙인) — our fair rule

Our players rarely have shields (4 items, 1 engraving, the Geo crystallize shard) and have no cleanse, so the Genshin
version ("DoT unless shielded", ≈ 25 % max HP per brand, [v7] §A2) would make phases 2-3 a damage race. Rule:

1. **Apply.** A landed strike hit (`#mbHitEv`, not dodged) of an **absorbed element** brands: the leg element from phase 2;
   **both** absorbed elements in phase 3. A lingering field brands on entry and refreshes once per 20 t inside. Geo and
   physical hits never brand. A new element replaces the brand; the same element refreshes it (remaining ticks =
   max(remaining, 3)).
2. **DoT.** First tick 20 t after the brand (footage ≈ 26 t), then every 20 t, **5 ticks** for a new brand; each tick
   **3 % max HP** (≈ 4 HP at Lv5, ≈ 20 HP per brand) through `mboss/pl_dot`: **non-lethal** (floor 1 HP), dash i-frames do
   not block it, defence does not apply, **a shield absorbs it** (guard first, then the element shield, 250 % against its
   own element). **Cryo stacks** 1-3 (each Cryo *strike* +1; the tick ×1 / ×1.5 / ×2); every DoT tick without a new Cryo
   strike since the previous tick drops one stack (3 → 2 → 1).
3. **Cleanse** (any one ends the brand and its stacks, with the butterfly-style cure fx and a chime):
   - **healing**: a cure meter (`#mbHealAmt`, the butterfly's cumulative rule) reaching **6 % max HP** while branded;
     HUD "회복 3/6%";
   - **perfect dodge**: a dash whose i-frames make a **one-shot strike** hazard (no `#hzRearm`, tell ≥ 12 t, not
     `#hzNoDodge`) or a projectile miss (`#mbDodgeEv` with `#mbDodgeOk 1`), at most once per 40 t. Fields, orbs, strips
     and hail never count;
   - a shield of any kind absorbs the ticks (the brand times out normally).
4. **응결 결정 (crystal shard, in-arena counterplay, Q4).** When a brand lands on a player with no shield, Azhdaha's back
   sheds one shard: cooldown 300 t, at most 1 alive, life 200 t (frozen while paused); placed 4-6 b from the player,
   outside the push capsules, live fields, orbit bands and telegraphs, on the side away from the anchor when the player is
   within 10 b of it. Own tag `rlk_az_shard rlk_mb_aux` and its own copy of the crystallize pickup (not counted against the
   crystal cap of 3): a shield of **12 % max HP** for 15 s with `#shEl` = the brand element (absorbs it at 250 %); the
   element is set only if the new amount is ≥ the current shield. The sim decides 12 vs 8 % (§6.2). Gold-amber prop with
   the element colour inside.
5. **Show.** A rune glyph over the player's chest (kit rune per element: Hydro "ccc / |||", Pyro ")火(", Cryo "大巛",
   Electro square rune) every 4 t; the sidebar line "낙인(물) 4초"; a third badge "◈낙인" on the name line; the first brand
   of a fight types the hint (§4.13).
6. **Lifecycle.** Brand, stacks and DoT clocks live in the module tick (frozen by pause; cine does not freeze them); cleared
   on death, abort, cleanup, uninstall, fight end; scores survive `/reload`, shards (`rlk_mb_aux`) do not.

**Player-side reactions** from the boss's elements are skipped (NoRx on every Azhdaha hazard and projectile by the api
default, N7): the brand replaces them. This also removes Freeze on the player (movement 0, against the "no FOV zoom" rule)
and Melt ×1.5-2 / Superconduct ×1.4 doubling the punishment (Q5).

#### 4.11 HUD

| line | content |
|---|---|
| name | `Lv.6 야타용왕` + `◈물` `◈번개` (dim until absorbed) + `◈낙인` while branded |
| sub-line | "봉인된 바위 용의 왕" (intro); the transition message; "꼬리만 공격할 수 있습니다" (B3); "안전 지대 7칸" (42, distance to the nearest safe circle, a chime inside); "점프!" (landslide cue); "마지막 일격!"; "옆구리 금지 — 머리 정면 · 꼬리 끝" (after the second flank punishment within 30 s); first-time hints |
| under-bar | fight: `mhpC − #mbFloor` of the phase pool (element colour: Geo 5 → leg → tail); transition: sequence progress (gold); B3: tail window left (tail element) |
| banners (kit) | transition message, "물 원소 흡수", the phase-2 brand tutorial |

#### 4.12 Targeting, facing, zones, push, picks

**Body frame** from `mboss/mv/local`; every threshold below is computed by the generator from the rig manifest's rest
anchors (numbers here at R1 rest: nose f +5.5, head column +4.3, chest +2.1, hips −3.4, tail root −4.75, fore paws
(±3.15, +2.95), hind feet (±2.5, −2.55), torso half-width 3.0).

| zone | condition | meaning |
|---|---|---|
| HEAD | f ≥ 3.6 and \|s\| ≤ 4 + 0.6 (f − 3.6) | in front (recommended) |
| FLANK-near | 3.0 ≤ \|s\| ≤ 9.0 and −4.8 ≤ f < 3.6 | 옆구리 (punished) |
| FLANK-far | \|s\| > 9.0 and −4.8 ≤ f < 3.6 | far side (ranged; not the rule) |
| TAIL-lane | f < −4.8 and \|s\| ≤ 3.5 | behind the rump along the tail (recommended) |
| TAIL-off | f < −4.8 and \|s\| > 3.5 | rear quarter |
| PAW | horizontal distance to paw / foot k ≤ 2.8 (also every point with \|s\| < 3.0 and −4.8 ≤ f < 3.6) | stomp trigger |
| band | anchor distance near ≤ 9, mid 9-15, far > 15 | |

Zones are classified per decision and every 4 t (dwell, HUD, turning); the last 40 t of hit proxies (`#mbPart`) are a
second signal.

**FLANK rule** (FLANK-near only): it fires only if the player was in FLANK-near for ≥ 16 of the last 24 t (sampled every
4 t) **or** hit a flank proxy (chest, belly, hips, paws, feet from \|s\| ≥ 3) in the last 40 t. Then with 90 %: if the
previous pattern was not P6 → **P6 feint**; if it was P6 and the player is still in FLANK-near or TAIL-off → **P7 whip**
(only if the anchor is ≤ 8 b from the centre and an exit exists, §5 P7), else P8 (TAIL) or P2. The other 10 % use the
FLANK-near column. **Skipped once** after P2, P7, P8 + `turn180`, P9, the B3 surfacing, the transitions and the absorbs
(the player did not choose the flank). After P3 the rule applies, but P3's recover is ≥ 30 t (time to leave). The first
punishment types "옆구리는 위험합니다 — 머리 정면 · 꼬리 끝으로".

**Weights** (phase 1; 0 = never; recover after each pattern 14-24 t, heavy ones +6, specials +30, P3 ≥ 30):

| id | pattern | HEAD near | HEAD mid | HEAD far | FLANK-near (10 %) | FLANK-far | TAIL-lane | TAIL-off | PAW | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | chin slam | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 2 (front paws) | |
| 2 | jump slam | 1 | 3 | 3 | 1 | 2 | 1 | 2 | 1 | repeat at half weight |
| 3 | charge | 0 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | only within ±35° of the front |
| 4 | back spikes | 2 | 3 | 3 | 2 | 2 | 2 | 2 | 1 | phase 3 → 45 / 46 |
| 5 | stomp | 1 | 0 | 0 | 2 (paw ≤ 2.8) | 0 | 0 | 1 (hind ≤ 2.8) | 5 | ≤ 2 in a row; phase 3 front paws → P5b |
| 6 | feint | 0 | 0 | 0 | rule | 0 | 0 | 0 | 0 | |
| 7 | tail whip | 0 | 0 | 0 | rule | 1 (exit test) | 0 | 2 | 0 | anchor ≤ 8 b |
| 8 | tail slam | 0 | 0 | 0 | 0 | 0 | 4 | 1 | 0 | anchor ≤ 8 b |
| 9 | burrow charge | 1 | 2 | 2 | 0 | 1 | 1 | 1 | 0 | phase 1 only, cooldown 600 t |

Phase 2: as phase 1 without 9, plus the leg special (31 or 32) weight 2 in every zone (cooldown 600 t after its end, never
while its own hazards live). Phase 3: 4 → 45 / 46 with the same weights; **43** (background) weight 3 in HEAD mid / far,
FLANK-far, TAIL-lane, TAIL-off (cooldown 400 t; only while no background emitter lives); **44** (foreground) weight HEAD
near 1, mid 2, far 2, FLANK-far 2, TAIL-lane 2, TAIL-off 2 (cooldown 400 t); the leg special weight 1 (31 only while no
background emitter lives).

**Decision order**: test request > lock > queued transition > B3 frame > forced specials at phase start > FLANK rule >
weighted pick > no immediate repeat (except P2 at half weight and P5 up to 2) > cooldowns > field-area gate > fallbacks.

**Turning**: idle tracking ≤ 3°/t while \|Δyaw\| ≤ 45°; beyond that a `turn45` / `turn90` step (scripted yaw); front
patterns get a pre-turn lead ≤ 10 t (≤ 4°/t) and lock their aim at the wind-up start; side, tail and area patterns do not
turn. **Locomotion**: mostly stationary; `walk` 0.13 b/t toward a target beyond 15 b when no far pattern was picked
(≤ 40 t); leash to the body disc r 8. **Anti-stall**: a player in TAIL-lane for 3 decisions without a tail pattern →
`turn180`, then a front pattern.

**Body push (N12)**: `#mbPushOn 1` only while the proxy state is `normal`, the anchor moved ≤ 0.15 b/t and turned ≤ 6°/t
since the last tick, and no 42 mask round has markers; never in `jump`, `inv`, `tail_only`, `dead`, during the charge run,
`mv/leap`, the whip pivot (t20-42), or `burrow_emerge` before `out`. Capsules from the manifest (torso; the head only while
it is low).

#### 4.13 Korean text and lines (typed with `line/say`, speaker "야타용왕" in gold; no voice)

| when | line |
|---|---|
| intro roar (t120) | "인간 주제에, 선을 넘지 마라!" |
| first P3 or P9 of the fight | "모락스…!! 빚을 청산할 때가 왔다!" |
| P2 jump (first per phase) | "갈라져라! 부서져라!" |
| P7 whip (first per phase) | "버러지 같은 것들! 교활한 놈!" |
| landslide 1 | "천 년의 원한을 어찌 갚을까!" (w1), "대지의 진노는 잠재울 수 없다!" (rear) |
| landslide 2 | "오늘이야말로 묵은 원한을 전부 청산하지!" (w1), "천 년의 원한을 어찌 갚을까!" (w3), "대지의 진노는 잠재울 수 없다!" (rear) |
| absorb 1 roar | "으윽…! 넌 이번에도 날 배신할 셈인가!" |
| absorb 2 burst | "모락스! 너 정말 날 파멸시킬 작정이냐!" |
| absorb 2 roar | "이 곳이 네놈들이 묻힐 곳이다! 받거라… 천 년의 분노를…!" |
| tail emitters (first of 43 / 44) | "가루로… 만들어주마! 흙으로… 돌아가라!" |
| death | "난… 사라지지 않아!" (t0), "모…락스…!" (t80) |
| brand hint (first brand) | "낙인 — 보호막이 막아 줍니다 · 공격을 대시로 피하거나 6% 회복하면 지워집니다 · 결정을 주우면 보호막" |
| brand banner (phase-2 start, once) | "야타용왕의 {물} 원소 공격에 맞고 보호막이 없으면 계속 {물} 원소 피해를 받습니다" |
| shard | "응결 결정 — 주우면 보호막" |
| first flank punishment | "옆구리는 위험합니다 — 머리 정면 · 꼬리 끝으로" (first feint adds "대시로 바깥쪽으로") |
| first whip | "꼬리를 높이 들면: 머리 정면으로 들어가거나 꼬리 반대편으로 넘어가세요" |
| floor | popup "흡수 중 (1234)" (grey number) |

---------------------------------------------------------------------------------------------------

### 5. Pattern specs

Conventions: `t` = the pattern clock (0 = the clip start after any pre-turn lead); sizes in blocks (§0); coefficient = % of
the base hit (atk 12 × dmgMul 140: **1.0 = 23 HP** on an item-less Lv5 player, 15.5 % of 148); "nododge" = `#hzNoDodge 1`;
every hit is a framework `hz/*` or `pj/*` paired with the kit decal of the same size and time, quiet (`#hzQuiet 1`,
`#hzSfx 0`: the patterns compose their own vanilla sounds), NoRx on all; KB in framework units; "leg element" / "tail
element" per §4.5; "burst" = the §0 rule-2 check (Σ coef per 40 t on one spot, worst element pair); "dash" = the rule-3
check. E = existing helper, N = §1.4. Every row's sizes and ticks are binding for the pattern authors; the fairness fixer
may change coefficients only (§7).

#### P1 갈라지는 봉인의 땅 (chin slam), id 1, `chin_slam` (65 t), geo_a

| field | spec |
|---|---|
| trigger | HEAD near 4 / mid 2; PAW (front) 2 |
| footage | [v2] C: sway 0-11, roar 11-17, rear 17-22, hold 22-41, drop 41-44, **impact +44.7**, head down 19 t, total 76 t; disc r 5-6 m at the head point + crack fan r 6 m; [v4] C Hydro geyser +13 t after the impact, 6-8 m to the side; [v8] B Cryo ring from the impact point |
| timeline | pre-turn ≤ 8 t; t10 lock the impact point (on the line to the player, f clamped 5.5-7.5); decal t10; **impact t35** (tell 25); head-down window t35-55 (head column low); end 65; recover 18 |
| hazards | disc r 5.0 at the impact point + sector r 5.6 / ±30° forward from it (cracks), one group, **1.4**; Geo (phase ≥ 2: leg element + brand); KB heavy away; dodgeable (one dash at the impact) |
| element extras | `chin/impact` (§4.6) |
| checks | burst ≤ 2.8 (Hydro + Cryo: 1.4 + 0.8 + 0.6); dash ≤ 2 in 20 t (impact, then the geyser at +10 by a step or a 2nd dash) |
| fx / sound | kit crack disc + fan, `blade_crown` burst in the element, slab props, dust ring, flash; rear: `entity.ravager.roar` p 0.6 + `entity.ender_dragon.growl` p 0.7 v 0.5; impact: `item.mace.smash_ground_heavy` p 0.5 + `entity.generic.explode` p 0.5 + `block.amethyst_cluster.break` p 0.6 |
| helpers | E `hz/disc`, `hz/sector`, groups, `lockb`; N1, N13 |

#### P2 바위 분쇄 충돌 (jump slam), id 2, `jump_slam` (53 t), geo_a

| field | spec |
|---|---|
| trigger | HEAD near 1 / mid 3 / far 3, FLANK-near 1, FLANK-far 2, TAIL-lane 1, TAIL-off 2, PAW 1; may repeat at half weight |
| footage | [v2] B: front lifts +1…+3, airborne +8…+23, **wave 1 +28 (landing), wave 2 +38.7**, ground rings r 9-12 m, jump 3.5-5 m high; [v4] J lands on the player's position, pulses +3 / +14; [v5] S Pyro: 4-6 lumps, flight 30-40 t, ring fields r ≈ 5 m |
| timeline | t1 lock (`lockb` = the player's feet, travel clamp(dist − 3, 4, 14), into the body disc r 8); decals from t1: landing disc r 4.5 + outline ring r 10.5 (tell 20); `mv/leap` t6 → 21 (apex ≈ 3 b), `px/state jump` t6-21, push off; **land t21**; **wave 2 t32**; end 53; recover 16. The Hydro orbit centre freezes during the leap |
| hazards | landing: disc r 4.5 + front r 3 → 10.5 in 5 t (1.5 b/t, band 2.5, low band `#hzY1` 0.7), one group, **1.1**; wave 2: the same front, own group, **1.1**; Geo (phase ≥ 2: leg element + brand); dodge = two dashes 11 t apart, two jumps (not while swinging), or > 11 b away; the landing disc needs a dash or a jump (a sprint covers 4.2 of the 4.8 b) |
| element extras | `jump/land` (Hydro blades and the Cryo ring inside the landing group), `jump/wave2` (Pyro lumps, Electro bolts in the wave-2 group) |
| checks | burst ≤ 2.8 (Pyro: 1.1 + 1.1 + 0.6); dash 2 in 11 t, then free |
| fx / sound | shadow decal, dust, crack rings, slab props; take-off `entity.ravager.attack` p 0.5 + `item.trident.riptide_3` p 0.5 v 0.5; landing `item.mace.smash_ground_heavy` p 0.6 + `entity.generic.explode` p 0.6 + `block.anvil.land` p 0.5 v 0.5; wave 2 `block.deepslate.break` p 0.5 + `block.pointed_dripstone.land` p 0.6 |
| line | "갈라져라! 부서져라!" (first per phase) |
| helpers | E `mv/leap`, `lockb`, `clamp_body`, `pj/launch` blade; N10, N13 |

#### P3 바위 용왕의 돌진 (charge), id 3, `charge_coil` (26) → `charge_run` → `charge_stop` (21), geo_a

| field | spec |
|---|---|
| trigger | HEAD far 5 / mid 1, only within ±35° of the front |
| footage | [v3] B: visible tell ≥ 33 t (growl, 14 t coil), launch, ≈ 25 t run at ≈ 1 b/t, 25-30 m, straight at the launch-time position, skid ≈ 10 t; body 7-10 m wide; caption "빠르게 옆으로 빠져주세요" |
| timeline | pre-turn ≤ 10 t; lane decal from t4 following the player until **t14 (lock)**; launch t24; run ≤ 24 t at 1.0 b/t along the locked line, stopping at the lane end or the anchor clamp r 12; `charge_stop` 21; **recover ≥ 30** (time to leave the flank before the FLANK rule) |
| hazards | lane len 26 (from the body front), w 8, clamped to the safe radius (the decal shows the clamped lane); the hit is a disc r 4.0 moved onto the body every run tick (plain `tp`, one hit), **1.8**, Geo in every phase, KB heavy sideways from the lane axis; dodgeable: a sprint sidestep of ≥ 4.3 b (≥ 20 t between the lock and the arrival at 15 b) or one dash (the first touch consumes it) |
| element extras | none (wiki: the pattern to lure in phase 2) |
| checks | burst 1.8; push off during the run |
| fx / sound | lane decal, dust trail, skid gouge; growl `entity.ravager.roar` p 0.6 + `entity.ender_dragon.growl` p 0.8 v 0.5; gallop `entity.ravager.step` p 0.5 + `entity.iron_golem.step` p 0.4 every 4 t + `block.gravel.break` p 0.6; skid `block.gravel.hit` p 0.5 + `block.grindstone.use` p 0.4 |
| line | "모락스…!! 빚을 청산할 때가 왔다!" (the first P3 or P9 of the fight) |
| helpers | E `mv/glide`, `hz/line` (telegraph-only lane), `clamp` |

#### P4 천동만상 (back spikes), id 4 (phases 1-2), `spikes` (40), geo_a

| field | spec |
|---|---|
| trigger | every zone 1-3 (table) |
| footage | [v1] S: tell 12 + 3 t, launch +4…+9, markers 18 t before each landing, landings S+47 / 53 / 57 / 64, marker r 1.6 m, line through the target 3.5-4.5 m spacing; [v2] A: explosions ≈ 40 t after landing, from the boss outward 3-4 t apart, r 2.5-3 m |
| timeline | `gold_on` t0-22; launch t14 (4 spike props up out of view); t18 choose points: P1 = head + 3 b toward the target, P2 = `lockv` (lead 28), P3 / P4 = P2 + 4 / + 8 b along the player's velocity (if \|v\| > 0.08 b/t) else along head → P2; clamp r 27; marker each 14 t before its landing; **landings t46 / 51 / 54 / 59**; planted spike props glow from t64; **explosions t76 / 79 / 82 / 85** (boss outward); end 90 |
| hazards | landing discs r 1.6, one group, 0.9; explosion discs r 2.5, one group, 0.9; Geo (phase 2: leg element + brand, Hydro water spray / Pyro fire puff cosmetic); dodgeable (step off the line, dash the explosion) |
| checks | burst 1.8 |
| fx / sound | gold plume, marker crack rings, falling shard props (4 t), crystal-blade bursts; bristle `entity.breeze.charge` p 0.6 + `block.respawn_anchor.charge` p 0.7; launch `entity.blaze.shoot` p 0.5 + `entity.firework_rocket.launch` ×4 p 0.6; landing `entity.generic.explode` p 1.2 v 0.5 + `block.pointed_dripstone.land` + `block.amethyst_cluster.break` p 0.8; explosion `entity.generic.explode` + `block.amethyst_block.break` |
| helpers | N3, E groups, prop timetable (butterfly B2 template) |

#### P5 산명곡응 (foot stomp, 3 waves), id 5, `stomp_fl/_fr/_hl/_hr` (63), geo_b

| field | spec |
|---|---|
| trigger | PAW 5, FLANK-near 2 (paw ≤ 2.8), TAIL-off 1 (hind paw), HEAD near 1; ≤ 2 in a row; in phase 3 a front-paw stomp plays P5b |
| footage | [v3] G/H: rear ≥ 15-25 t, slam, **3 waves 15 / 13.3 t apart**, each r 1 → 9 m in ≈ 3 t then to 10.4 m over ≈ 10 t, ankle-to-knee band, slam crystal cluster r ≈ 3 m; [v4] Q Hydro: hit at the slam + a second hit 6 t later, brand |
| timeline | paw = the one nearest the player (front for HEAD / PAW front, hind for TAIL); decal (paw disc r 2.8 + outline r 9.7) from t3 (tell 14); **w1 t17 / w2 t32 / w3 t47**; end 63 |
| hazards | slam disc r 2.8 (in w1's group); fronts r 1.5 → 7.5 in 3 t (2 b/t), then → 9.7 by +12 t (ease-out), band 2.0, low band 0.7, three groups, **0.9 each**; Geo (phase ≥ 2: leg element + brand); dodgeable by dash or jump; > 10 b is safe |
| element extras | `stomp/w1` (Hydro blades inside w1's group, Cryo ring for hind stomps in phase 3), `stomp/w3` (Pyro lumps, Electro bolts) |
| checks | burst 2.7 (lumps land at t75, outside w1's window); dash 2 per 20 t (15-t gaps); known deviation: our 2-charge dash with a 20-t regen chains all three fronts, which the wiki says is impossible (Q) |
| fx / sound | paw crystal cluster, element disc front with radial cracks, boulders; slam `entity.generic.explode` p 0.6 + `entity.iron_golem.damage` p 0.5 + `block.amethyst_block.break`; waves `block.respawn_anchor.deplete` p 0.6 + `entity.warden.sonic_charge` p 1.4 v 0.3 |
| helpers | N10, rig paw anchor, N13 |

#### P5b 산명곡응 – 연속 발구르기 (phase-3 triple stomp, front paws), id 10, `stomp3_fl/_fr` (85), geo_b

| field | spec |
|---|---|
| trigger | phase 3, whenever P5 is picked for a fore paw |
| footage | [v9] C (phase 3, Hydro legs): three separate stomps, **alternating fore paws, 22-23 t apart**; each a water disc r 6-7 m at once, a splash wall at the ring edge 3-8 t later expanding to ≈ 10 m, then crescent water waves |
| timeline | paw A = the nearest fore paw; per slam a decal (paw disc r 2.8 + outline r 9.7 at the slamming paw) from slam − 14; **s1 t17 (A), s2 t40 (B), s3 t63 (A)**; end 85 |
| hazards | per slam: slam disc r 2.8 + front r 1.5 → 9.7 (as P5 w1), own group per slam, **0.9**; leg element + brand |
| element extras | `stomp3/s1` (Hydro blades, Cryo ring in s1's group), `stomp3/s3` (Pyro lumps, Electro bolts in s3's group) |
| checks | burst 1.8 per 40 t (2 slams), 1.5 with the lumps; dash: 23-t gaps (a charge regenerates between slams) |
| fx / sound | as P5, alternating paws; the leg-element splash wall preset at +5 |

#### P6 성동격서 (side feint), id 6, `feint` (50), geo_b

| field | spec |
|---|---|
| trigger | the FLANK rule (§4.12) |
| footage | [v3] C: sway 8 + 14 → **eruption +23.5…25**, strips along both flanks ≈ body length (10-13 m), 4-6 m out, dust walls, nose and tail tip clear; wiki: front and back also get a little hit; caption "살짝만 닿아도 피격 · 아예 빠져야" |
| timeline | t0 flank strips (undodgeable look, `lane_side`) + front / back discs; **burst t22**; dust walls t22-40; end 50; recover 14 |
| hazards | two flank strips `hz/line` along the body axis at s = ±5.3, f −6.0 … +5.0 (len 11), **w 6.6 (\|s\| 2.0 … 8.6)**, **nododge**, **1.2**, KB outward 4; front disc r 2.5 at the nose (f +6.5) and back disc r 2.5 at the tail root (f −5.5), dodgeable, 0.6; all one group; Geo (phase ≥ 2: leg element + brand on all) |
| checks | escape from \|s\| 3.2 needs 5.7 b in 22 t: a sprint gives 4.8 b, a dash + sprint 7.0 b (the dash cancels the swing) → the first feint adds the hint "대시로 바깥쪽으로" |
| fx / sound | element blades out-and-up along the flanks, dust walls, thrown rocks; sway `entity.warden.heartbeat` p 0.6 ×2 + `block.deepslate.step`; burst `entity.generic.explode` p 0.9 + `block.amethyst_block.break` p 0.6 + `block.basalt.break` ×4 |
| helpers | E `hz/line`, `#hzNoDodge`, groups; first-time hints |

#### P7 교활한 통수 (tail whip), id 7, `tail_whip_l/_r` (64), geo_b

| field | spec |
|---|---|
| trigger | the FLANK rule; TAIL-off 2, FLANK-far 1; **only while the anchor is ≤ 8 b from the centre and an exit exists**: at decision time at least one of {the unswept half across the rear axis, the HEAD lane (within 65° of the front axis), a walk-disc point beyond the tip (> 17.05 b from the anchor)} lies within 3 + (23 − 8) × 0.281 = **7.2 b** of the player; otherwise the rule takes P6, P8 or P2 |
| footage | [v3] E: high-tail hold, **drop / twist 3 t, sweep ≈ 5 t**, hit +4.7, ≈ 150-200° around the player's side, reach 12-14 m from the tail root, band 3 m, **25.6 % max HP**, caption "괴랄한 범위 · 회피 불가능"; [v8] B reach 15-18 m from the hips, the front quarter grazed |
| timeline | side = the player's side; **t0 decal = the union of the per-tick swept wedges** (computed by the generator from the manifest's tail-root / tip track and the yaw schedule) + the tail raise; anchor yaw 0 → **+115°** t20 → 31 (exported schedule), harmless overshoot to 122° at t35, back to 115° by t42; **sweep t23-31**; eruption t33; end 64; recover 18 |
| hazards | per-tick **swept wedge** (annular sector between the previous and the current tail-line angle about the current tail root, r 0 … **12** from the root, so ≤ 16.75 b from the anchor), all wedges one volley group, **nododge**, **1.5**, KB tangential 4; the hazard ends **65° from the front axis** (115° of sweep), so the HEAD lane is never in it; eruption discs r 1.6 ×4 along the end line at t33 (the footage's "grazed front"), dodgeable, same group (max one hit); sweep Geo, eruption leg element (phase ≥ 2) |
| safe | the HEAD lane (head-on, within 65° of the front axis), the unswept half (cross behind the rump before t23), beyond 16.75 b |
| element extras | `whip/sweep` (Cryo wall on the swept arc), `whip/end` (Electro bolts + crystal line + strip) |
| checks | decal = union of the samples (rule 1, generator check); burst ≤ 2.45 (1.5 + Cryo wall 0.8 + hail 0.15); exit test as above; known deviation: 115° of sweep instead of 150-200° (Q24) |
| fx / sound | tail lane, blades and boulders along the arc; raise `entity.warden.ambient` p 0.6 v 0.4; sweep `entity.breeze.wind_burst` p 0.6 + `item.trident.riptide_3` p 0.7 v 0.6; eruption `entity.generic.explode` p 1.0 + `block.amethyst_cluster.break` |
| line / hint | "버러지 같은 것들! 교활한 놈!" (first per phase); first whip: "꼬리를 높이 들면: 머리 정면으로 들어가거나 꼬리 반대편으로 넘어가세요" |
| helpers | E `hz/sector` per tick (wedges), `#hzNoDodge`; the rig yaw schedule; N6, N13 |

#### P8 꼬리찍기 (rear tail slam; footage only, not named in the wiki), id 8, `tail_slam` (70), geo_b

| field | spec |
|---|---|
| trigger | TAIL-lane 4, TAIL-off 1; only while the anchor is ≤ 8 b from the centre |
| footage | [v3] F: tail vertical ≥ 2.1 s, swing 3 t, impact; line ≥ 11 m (13.7-14.7 m from the hind foot), ≈ 3 m wide; spikes 3-5 m; cones stay ≈ 60 t; 25.6 % max HP; caption "준비모션이 길어서 충분히 옆으로 피할 수 있습니다" |
| timeline | lane decal t9 (tell 30), direction = the rear axis (pre-turn ≤ 15° in the first 10 t); **impact t39**; spikes t41; cones 60 t (props); end 70 → `turn180` if the player is still behind |
| hazards | `hz/line` from the tail root straight back, **len 13**, w 3.5, **1.4**, KB sideways 3, dodgeable (a 2.05-b sidestep in 25 t); Geo (phase ≥ 2: the spike line in the leg element + brand) |
| element extras | `tailslam/impact` (phase-3 strip) |
| checks | burst 1.55 |
| fx / sound | spike line, leaf burst, cones; raise `block.pointed_dripstone.drip_lava` + `entity.warden.ambient`; impact `entity.generic.explode` p 0.6 + `block.anvil.land` p 0.5 v 0.5 + `block.pointed_dripstone.land` ×3 + `block.cherry_leaves.break` p 0.7 |

#### P9 잠복 돌진 (burrow charge; phase 1 only), id 9, `burrow_dive` (40) → `burrow_travel` → `burrow_breach` ×2 → `burrow_emerge` (53), geo_b

| field | spec |
|---|---|
| trigger | HEAD near 1 / mid 2 / far 2, FLANK-far 1, TAIL 1 / 1; cooldown 600 t; phase 1 only |
| footage | [v2] D + [v3] A: dive 48 t to gone; underground ≈ 31 s; marker pairs every 93 t (2nd 33 t after the 1st), rings r 3.6-4.2 m on the player, impact 25 t later; **2 surfacing rushes** (dust wall 6-8 m wide, ≈ 0.6 b/t) + the final emergence (caption "2~3회 잠시 올라오며"); final emergence from the centre when the target hugs the wall, burst r 3-4 m |
| timeline (≈ 273 t) | dive t0-40 (`px/state inv` from t30, hidden at t40); **edge flag sampled at the dive (t40)**: target farther than 20 b from the centre; underground u = t − 40 for **180 t**, the anchor gliding hidden toward the player at 0.3 b/t (clamp r 12); **rock pair A** at u 10 (ring under `lockv` lead 6, tell 19) and u 35 (2nd ring), with 3 small rocks r 1.4 along the velocity line (+3 / +6 / +9 b, tell 14, one group) at u 10; **rush 1** at u 45: lane decal 20 t from a breach point 6 b beside the player toward them, then a disc r 3.0 travelling the lane at 0.6 b/t (`burrow_breach`); **rock pair B** at u 80 / u 105; **rush 2** at u 115 (with the edge flag: from the centre straight at the target); **final emergence** at u 160: edge flag → emerge at the centre (burst) and run the lane centre → target (len dist + 4, w 6, decal 20 t) at 1.0 b/t; else a ring under `lockv` (lead 8), tell 19, emergence at the ring; `burrow_emerge` (53), `px/state normal` at `out` |
| hazards | rock rings disc r 3.4, 0.9 each (own groups); small rocks 0.6 (one group); rush disc r 3.0 moving, 1.1; emergence burst r 3.7, 1.5; centre run disc r 4 on the body, 1.3; Geo; all dodgeable; the boss is untargetable underground |
| checks | burst ≤ 2.9 (ring A1 + A2 + rush 1 in 40 t); dash ≤ 2 per 20 t (pairs 25 t apart) |
| fx / sound | gold zig-zag ring markers, light shaft, gold crystal bursts, dust mound plume, rock rain; dive `entity.warden.dig` p 0.8 + `block.rooted_dirt.break` p 0.6; underground loop `entity.warden.dig` p 0.6 v 0.4 every 30 t; ring `block.respawn_anchor.charge` p 1.4 v 0.5 + `block.amethyst_block.chime` p 0.8; rock `item.mace.smash_ground_heavy` p 0.8 + `block.amethyst_cluster.break` p 0.8; rush / emerge `entity.warden.emerge` p 0.9 + `entity.ravager.roar` p 0.6 v 0.6 + `entity.generic.explode` p 0.7 |
| line | "모락스…!! 빚을 청산할 때가 왔다!" (the first P3 or P9 of the fight) |
| helpers | N3, E bombs-along-a-line (fieldgen C1 template), `mv/glide`, moving disc by `tp`, proxies `inv` |

#### T1 파멸의 산사태 (6 hits), service 20, `landslide` (203), trans

| field | spec |
|---|---|
| trigger | a queued transition |
| footage | [v4] L / [v5] T: message ≈ 20 t before the tell; tell 28-60 t (slow right fore + right hind lift); **waves +0 / +26 / +54 / +80 / +108 / +162** (v5 gaps 26 / 28 / 27 / 28 / 53); fronts reach r ≈ 20 m in ≈ 4 t (≥ 2.5 b/t, "effectively instant"), ground level; **wave 6 bigger (≥ 30 m, the whole domain)** after a 20-t rear-up; HP frozen at the floor; wave 6 ≈ 25 % max HP; captions "저 발구르기 맞고 죽는게 태반 · 범위 진짜 엄청넓으니 쭉 빠져계세요" |
| timeline | the message at the service start; the boss `walk`s to ≤ 2 b from the arena centre (≤ 40 t; the clip starts ≥ 20 t after the message) and the **anchor stays fixed from t0** (it only turns in place to face the target during t0-45); **w1 t57 / w2 77 / w3 98 / w4 118 / w5 139 / rear 159 / w6 179**; end 203 |
| hazards | fronts from the anchor, own group each, **nododge**, low band 0.7 (jumpable): **waves 1-5** r 4 → 18 at **3 b/t** (5 t), band 3.5, **0.8**; **wave 6** r 4 → 30 (the whole walk disc) at **4 b/t** (7 t), band 4.5, **1.0**; element Geo at transition 1, the leg element + brand at transition 2 (no fire-rule fields during the landslide) |
| tells | from t0 persistent rim rings at r 18 (bright) and at the wall (dim, "wave 6 reaches everywhere"); each front's outline ≥ 20 t before it; jump cue: sub-line **"점프!"** + `block.note_block.bell` p 1.2 at each wave − 8 for players inside r 18 (waves 1-5) and for everyone at wave 6 − 10; the rear-up hang t159-175 is the visual wave-6 cue; the first-wave typed line |
| safe | waves 1-5: beyond r 18 or a jump; wave 6: a jump (or a shield). Stop swinging: the HP is floored (the message and the floor popup teach it) |
| checks | front band ≥ advance; tell floors 20; lethality at transition 1: 5 × 19 + 23 = 118 HP (80 % of a full Lv5); lethal only at transition 2 (brand) or after earlier damage (Q6) |
| fx / sound | element streak fronts + rock slabs + dust walls (Hydro water walls, Pyro fire walls at transition 2); lift `entity.ravager.step` p 0.5 + `block.deepslate.step` p 0.6; wave `entity.generic.explode` p 0.5 v 2 + `block.basalt.break` p 0.6 + `block.amethyst_cluster.break` p 0.7 + late `block.pointed_dripstone.land` ×3; wave 6 + `entity.warden.emerge` p 0.8 |
| helpers | N10, N14 floor |

#### T2 Absorb 1 + roar, service 21, `absorb` (94) → `roar_rear` (82), trans

| field | spec |
|---|---|
| footage | [v4] A Hydro (vortex, ring flash +61, recolour +63…74, ≈ 107 t visible), [v5] A Pyro (≥ 85 t, 火 sigils, ember rocks); [v4] R roar: rear 8, roar 16, hold ≈ 58, orbs at +82, land +97 |
| timeline | t0 `cine/start`, `px/state inv`, `glow/gold_on`, vortex preset of the leg element; **burst t47**: `look/legs/<el>`, arena recolour wave (§2.6), push-only ring r 8, banner "물 원소 흡수"; t94: `#azPh 2`, `#mbFloor` F2, `roar_rear`, music `"2"`, the phase-2 brand banner; roar at +20: typed line, dome rings, `cine/end`, `px/state normal`; the leg special starts from the roar (31 orbs at `drop` − 2, 32 meteors per its row) |
| sound | Hydro vortex `block.bubble_column.whirlpool_ambient` + `entity.player.splash.high_speed` p 0.7, burst `block.conduit.activate` p 0.8 + `block.beacon.power_select` p 0.6; Pyro swirl `item.firecharge.use` + `entity.blaze.shoot` p 0.6, burst `entity.ghast.shoot` p 0.5 + `block.lava.pop` ×3; roar `entity.ender_dragon.growl` p 0.55 + `entity.ravager.roar` p 0.5 |

#### T3 Absorb 2 + roar, service 22, `absorb_p3` (52) → `roar_rear` (82), trans

| field | spec |
|---|---|
| footage | [v6] A Electro ≈ 210 t (orb 76, discharge 14, bolt 5, roar with ≈ 7 shock rings), [v7] C Cryo ≈ 211 t (gather 36, burst +37, shard rain, rear, roar with 2 domes) |
| timeline | t0 `cine/start`, `px/state inv`, `glow/gold_on`, element orb / cloud over the back; **burst t42**: `look/tail/<el>`, arena recolour, banner "번개 원소 흡수" + "원소를 추가로 하나 더 흡수합니다", typed line "모락스! 너 정말 날 파멸시킬 작정이냐!", `#azPh 3`, **`#mbFloor 1`**, cosmetic shard rain / bolts t42-90, push-only ring r 8; t52 `roar_rear`: typed line at the roar, `cine/end` at the roar, `px/state normal` (floor 1 keeps the boss alive); then service 23 |
| sound | Electro charge `block.beacon.ambient` p 0.6 + `item.trident.thunder` p 1.4 v 0.4, discharge `entity.lightning_bolt.impact` + `entity.lightning_bolt.thunder` p 0.8 v 0.8; Cryo gather `block.amethyst_block.chime` + `block.powder_snow.step`, burst `block.glass.break` p 0.6 + `entity.player.hurt_freeze` + `entity.generic.explode` p 1.2; roar + `entity.warden.sonic_boom` p 1.6 v 0.25 per ring |

#### B3 Phase-3 opening burrow, service 23 (+ the special 41 / 42 from tail.py), trans (≈ 433 t)

| field | spec |
|---|---|
| footage | [v6] B: slabs / mounds 8 t, sink 72 t, tail rise 14 t; tail stance ≈ 370 t; **first lightning eruption 86 t after tail-up, then every ≈ 104 t; the 4th after the tail has gone under**; tail sink 2 t; under the dust 70 t; emergence 12 + 26 t; whole ≈ 568 t; [v7] D / [v8] A Cryo: dig 16, turn + sink 60 → tail at +76, circles every ≈ 46 t (tell 24), tail sinks 22 t, emergence ≈ 65 t (earth-spike cluster r ≈ 6 m); wiki: in the middle of the arena, only the tail hittable, HP ≥ 1 while burrowed, the phase-2 hazards stay active |
| frame (binding ticks; `api.B3_*`) | t0 `p3_sink` (66 t): dig in place (mounds / ice puffs / violet slabs per element), crater decal r 7.5 at the arena centre, `px/state inv` from t8; hidden glide of the anchor to the arena centre t40 → 56 (the root z offset of Rig decision change 1 puts the pillar on the anchor); **t58 tail-up**: `px/state tail_only`, `#azBur 1`, sub-line "꼬리만 공격할 수 있습니다", `tail_pillar` loop from t66, **the special starts** (`p/<frost|bolt>/start`); **t335 tail sink** (`tail_pillar_sink`, gone t353; `px/state inv`); t353-380 dust mound at the centre; emergence decal r 5.2 from **t360**; t380 `burrow_emerge`, **burst t388** (tell 28; the special's `stop`), `out` t418 → `px/state normal`, `#mbFloor 0`, `#azBur 0`, "마지막 일격!" if `mhpC` = 1; end t433 |
| hazards | emergence burst disc r 5.2 at the centre, 1.4, leg element (ground rule) + brand, dodgeable (step away from the surfacing spot); the phase-2 hazards (orbs at their normal band with the placement rules of 42, fire fields) keep running |
| tail window | t58-335 (≈ 13.9 s), tail1-4 hittable, floor 1 |
| fx / sound | mounds / ice puffs / violet slabs per element, crater prop (UUID 0x81), dust mound, earth-spike cluster; sink `entity.warden.dig` p 0.8 + `block.gravel.break` p 0.5 ×3; tail rise `entity.warden.emerge` p 1.0 + `block.pointed_dripstone.break` p 0.6; emergence `entity.generic.explode` p 0.6 + `entity.warden.emerge` p 0.8 + `block.basalt.break` ×4 |
| interface | `trans.py` owns the clock (`#azB3T`) and calls `p/<frost|bolt>/start` at t58 and `p/<frost|bolt>/stop` at t388; `tail.py` schedules relative to its start and never past `B3_BURST − 31` (t357); S1-MOD ships this frame as a working stub so S2-T can test 41 / 42 before I2 |

#### 31 격류 범람 (Hydro special), leg.py (background slot L)

| field | spec |
|---|---|
| trigger | forced at the absorb-1 roar and first at transition 2 (live orbs: refreshed, no new roar); then weight 2 (phase 2) / 1 (phase 3), cooldown 600 t after the orbs end, never while orbs live; in phase 3 only while no other background emitter lives |
| footage | [v4] R/O, [v9] C: orbs appear at the end of the upright hold (roar + 82); ≥ 4 orbs (2 per side) on **two rings r 6-8 m and 9-12 m**, Ø 1.4-3.4 m, 0.5-1.4 m up (chest height: not jumpable), ≈ one body length per 1-1.5 s, the centre-front (the head) is safe ("정중앙을 제외하곤 어디든 피격될 수 있습니다"); persist ≥ 17 s and into phase 3; wiki: multi-hit + brand, "usually clockwise; in multiplayer the inner orbs sometimes go clockwise" (inner normally counter-rotates), "watch the angle" |
| timeline | spawn at `roar_rear` `drop` − 2 (≈ t60 of the roar clip; when picked normally it plays `roar_rear` first); orbs grow from the boss's sides over 10 t (harmless), then orbit for **600 t**, fade 10 t |
| hazards | N5: **2 inner orbs r 6.5 counter-clockwise ω 3.5°/t + 2 outer orbs r 10.5 clockwise ω 2.4°/t** (offset 90°), centre = the anchor (follows at ≤ 0.2 b/t, frozen during `mv/leap`); each `hz/disc` r 1.3, band 0-2.2 (not jumpable), `#hzRearm 10`, 0.35 + brand; **all four one volley group** (≤ one hit per 10 t overall); dodgeable |
| eye of the vortex | while an orb is inside the front sector (±30° about the facing) and closer than 11 b to the anchor, its band rises to 2.6-4.6 b (it rides visibly over the head lane and cannot touch a standing player); during the transitions (landslide, absorb) every orb rides high; during a 42 marker window an orb that would cross a safe circle rides high over it |
| checks | head-lane melee uptime ≥ 70 % of phase 1 (sim); tail lane stays swept ("watch the angle") |
| fx / sound | orb props (cyan sphere + ribbon tail), no orbit ring decals (the props are the tell); `item.trident.riptide_1` p 0.8 + `entity.dolphin.splash` on spawn / pass; loop `block.bubble_column.whirlpool_ambient` + `block.conduit.ambient` p 1.4; hit `entity.player.splash` |

#### 32 운석 낙하 (Pyro special), leg.py

| field | spec |
|---|---|
| trigger | as 31 (cast fresh at transition 2, always with its roar) |
| footage | [v5] M: rear-up roar ≈ 60 t; seal glyph (≈ 7 m r) at the player area at roar +36; big impact glyph + 32-37 t, dome r 5-6 m + field; ≈ 6 small meteors, halo tells 6-10 t, every ≈ 6 t, r 3-4 m, fields; [v9] B bursts in sequence, patches persist; wiki: "a meteor that cannot be shaken off"; "stay near Azhdaha" |
| timeline (inside `roar_rear`, R = its `roar` event) | seal decal at R+7 under `lockp` (locked); the big meteor prop falls in the last 6 t; **impact R+35** (tell 28); **small meteors at R+44 / 50 / 56 / 62 / 68 / 74**, each with a halo ring 12 t before |
| hazards | big: disc r 5.2, **1.4** Pyro + brand, KB 3, leaves a fire field r 4.5 / 200 t; small ×6: targets alternate `lockv` (lead 10) and random points 6-14 b from the anchor (moved out of the clear melee points), disc r 2.8, **0.8**, **one group of 6**, each leaves a fire field r 2.8 / 160 t (within the caps of §0 rule 7); dodgeable (walking out of r 5.5 in 28 t works; a dash makes it easy) |
| checks | burst 2.2 (1.4 + 0.8) |
| fx / sound | `seal8` decal (two squares, 火 runes), meteor props with flame trails, fire domes; glyph `block.respawn_anchor.charge` p 0.7 + `block.beacon.activate` p 0.6; fall `entity.blaze.shoot` p 0.5; impact `entity.generic.explode` p 0.6 + `entity.dragon_fireball.explode` + `block.fire.extinguish`; small `entity.firework_rocket.blast` p 0.6 + `entity.generic.explode` p 1.1 v 0.4 |

#### 33 화염 잠식 (Pyro rule, phase 2 → end), leg.py — §4.7

Footage: [v5] fire rings r ≈ 5 m, [v9] the seal field covering the foreground; wiki "where the brand lands, a wide
persistent Pyro field". Fields r 4.5 / 160 t under a player branded by a strike hit; fx flame ring decal + `flame` /
`lava` / ember dust; loop `block.fire.ambient` / `block.campfire.crackle` every 20 t.

#### 41 서리 습격 (Cryo burrow special), tail.py, inside B3

| field | spec |
|---|---|
| footage | [v8] A: a new star circle every ≈ 46 t (often 2 alive), outline → icicle → **burst at +24 t**, heptagram {7/2} circumradius ≈ 12 m, inner heptagon ≈ 8.3 m, on or ahead of the running player; [v7] D first circle ≈ 5 m from the player; wiki: random or at the player biased to the movement direction; "keep moving one way, reverse when a circle appears"; Cryo stacks |
| timeline (B3 clock) | circles at **t70 + 34 k (k = 0 … 8, last at t342)**; each: heptagram outline t0, icicle t18, **burst t22**; at most 2 alive |
| hazards | centre: 70 % `lockv` (lead 15) + 2 b along the velocity (if \|v\| > 0.08 b/t; a standing player's circle is centred 4 b off them in a random direction), 30 % random 8-20 b from the tail; centres nudged ≤ 4 b to reduce overlap with live fields and orbit bands; disc **r 7.5** (decal the same size), **0.9** Cryo + stack, own group; dodgeable (from the centre a dash at the burst; a standing player 4 b off-centre walks out) |
| checks | ≥ 34-t cadence = one dash per circle within the 20-t regen; burst 0.9 (+ orb 0.35) |
| fx / sound | heptagram decal with meander tips and the central rune, icicle comet, ice-spike burst, frost mist; draw `block.amethyst_block.resonate` p 1.4 + `block.beacon.activate` p 1.8 v 0.3; icicle `item.trident.throw` p 0.6 → `block.glass.break` p 0.6; burst `block.powder_snow.break` ×3 + `entity.generic.explode` p 1.6 v 0.3 |

#### 42 벼락 습격 (Electro burrow special), tail.py, inside B3

| field | spec |
|---|---|
| footage | [v6] B2: 4 rounds, the first 86 t after tail-up, then every ≈ 104 t; markers ≈ 64 t ahead; two-wave eruptions over a very wide area; a player 1-3 m from the tail is never hit ("중앙 근처에 있으면 피하기 쉽습니다"); sky bolts between rounds; **round 4 fires after the tail has gone under**; wiki: safe groups 5 → 4 → 3 → 2, strike zones marked with purple light, the range expands at the end, step away from the surfacing spot |
| timeline (B3 clock) | rounds strike at **t123 / 201 / 279 / 357** (the last after the tail sink at t335); markers 48 t before each; sky bolts at round + 30 and + 42 (rounds 1-3) |
| hazards | **N4 mask** over everything outside the safe circles (no radius limit, so the wall is not safe), **nododge**, **1.2** Electro + brand, height 0-3, one group per round; safe circles R1 5 / R2 4 / R3 3 / R4 2 of r 3.2 (R4 r 2.8), safe within R0 + 0.3; R1-R3 include **one circle centred on the tail** (the anchor; the push is off during mask rounds); **one circle per round placed relative to the player** (`lockp` moved ≤ 5 b toward the centre, clamped to r ≤ 24); the rest on rings r 9-16 ≥ 50° apart, nudged off orbit bands and fields; R4: both circles ≥ 8 b from the emergence spot (the centre), one of them relative to the player; sky bolts: disc r 1.6 at `lockp`, tell 12, 0.5 + brand, KB 2, dodgeable |
| tells | one floor-wide violet wash card (the "purple light" = the strike area) + a green rim, a glyph and a particle column on each safe circle; sub-line "안전 지대 N칸" (distance to the nearest circle) with a chime when inside |
| checks | reachability: every round has a circle within 48 t of walking (≈ 10.5 b) from the player; burst 2.2 (1.2 + 0.5 + 0.5) |
| fx / sound | violet wash, green-rimmed safe circles with a glyph, floor-wide crackle, two-wave bolt fx 8 t apart; markers `block.respawn_anchor.charge` p 1.6 v 0.5 + `block.beacon.power_select` p 1.8 v 0.4; strike `entity.lightning_bolt.thunder` p 1.0 v 0.8 + 6-8 × `entity.lightning_bolt.impact` p 1.1-1.4 over 20 t + `block.amethyst_cluster.break` |
| fallback | if N4 slips: the module checks the safe circles itself (Raiden `dome_contains` idea) and calls `mboss/hurt` with `#hzNoDodge`; the drawing is unchanged |

#### 43 쏟아지는 천화 (Cryo emitter), tail.py (background slot T, phase 3)

| field | spec |
|---|---|
| trigger | weight 3 (HEAD mid / far, FLANK-far, TAIL), cooldown 400 t, only while no background emitter lives |
| footage | [v8] D: tail coral 13 t → sphere → spiky 26 t, 5 homing icicles; [v9] A: lances every ≈ 49 t, flight 6-8 t, impact r 1.5 m, aimed at the launch position, "그냥 좀 뛰면 다 피해집니다"; wiki: 5 volleys, the boss keeps attacking |
| timeline | `tail_cast` (34 t) as a short pattern; at `fire` the sphere prop spawns over the back (anchor + (0, 9, +2) in the body frame, follows) and the emitter takes slot T: icicles at **+30 / 66 / 102 / 138 / 174**; the sphere fades at +200 |
| hazards | each icicle: `lockp` at launch, decal r 1.6 at the aim from the launch, pj sphere hr 0.5, flight = max(12, dist / 1.6) t, no steering; impact disc r 1.6, **0.7** Cryo + stack, own group; dodgeable by moving |
| checks | one emitter at a time (N11); burst 0.7 per 36 t |
| fx / sound | ice coral on the tail, spiky ice sphere, lance trails, frost bursts; sphere `block.beacon.power_select` p 1.6 + `block.amethyst_block.chime` ×3, loop `block.conduit.ambient` p 1.6; lance `item.trident.riptide_1` p 1.6 → `block.glass.break` + `entity.generic.explode` p 1.4 v 0.4 |
| line | "가루로… 만들어주마! 흙으로… 돌아가라!" (first of 43 / 44) |

#### 44 번개의 가루 (Electro shells), tail.py (foreground pattern, phase 3)

| field | spec |
|---|---|
| trigger | HEAD near 1 / mid 2 / far 2, FLANK-far 2, TAIL 2; cooldown 400 t |
| footage | [v7] A1: tail-up tell 30 t (spark column), 8 shells every 7 t into a hover cloud 5-10 m up, ≈ 20 t later dives one by one every 7 t, each 8 t, r 2.5-3 m, aimed at the player's position at its launch; the boss only turns to track meanwhile; wiki: all fall in sequence, "much more damage time than Cryo" |
| timeline | `tail_cast` (34 t); 8 shell props leave the tail tip from `fire` every 5 t into a cloud 6-9 b up over the boss's front; dives from +70 every 6 t; ends ≈ +125; **the body only idles and tracks (≤ 2°/t) until the last dive**, then recovers 20 t |
| hazards | each dive: lock the player's feet 4 t before launch (decal r 2.4), flight 8 t (tell 12); impact disc r 2.4, **0.6** Electro + brand; 2 groups of 4 (max 2 hits); dodgeable by sprinting or dashing |
| checks | burst 1.2 |
| fx / sound | spark column, shell props (violet sphere + glyph), dive streaks, violet domes; spawn `entity.evoker.cast_spell` p 1.6 + `block.amethyst_block.resonate` p 1.4; hover `block.beacon.ambient` p 1.8; dive `entity.phantom.swoop` p 1.6 v 0.4; impact `entity.lightning_bolt.impact` p 1.3 v 0.6 + `entity.generic.explode` p 1.5 v 0.35 |

#### 45 천동만상 – 얼음 가시 (Cryo, replaces P4 in phase 3), tail.py, `spikes` (40) + tail flare

| field | spec |
|---|---|
| footage | [v8] D: back glow 4 t → 3 spikes up → star / hail field under the player ≈ 20 t after launch → spikes land ≈ 76 t after launch (≈ 56 t after the field), eruption r 2-2.5 m; [v9] A: eruption 1-2 t after landing, hail keeps falling in the white seal; wiki: field → delayed Cryo hit → hail on that spot, "lure the fields" |
| timeline | `gold_on` t0-22; launch t14 (3 dark spikes); star fields at **t26**: F1 = `lockv` (lead 30), F2 = F1 + 5 b along the velocity (or the boss → player line), F3 = random 6-10 b from the player; **bursts t68 / 74 / 80** (spike lands, eruption 1 t later); hail in F1 and F2 for 100 t |
| hazards | burst = the field disc r 4.0, **1.0** Cryo + stack, own group each; hail N6 disc r 4.0 / 100 t, 0.15 / 10 t, never adds stacks (hail cap 2); dodgeable |
| checks | burst 2.15 (F1 + F2 overlap + hail); field-area gate |
| fx / sound | star seal decals (white lines + rune), dark spike props with ice rims, ice-spike eruptions, hail particles; launch `entity.breeze.shoot` ×3 p 0.7 + `block.pointed_dripstone.break`; landing `item.trident.hit_ground` p 0.5 + `block.basalt.break` p 0.6; eruption `block.amethyst_cluster.place` p 0.6 + `block.glass.break` p 0.8; hail `block.powder_snow.step` / `block.glass.hit` p 1.5 v 0.2 |

#### 46 천동만상 – 번개 가시 (Electro, replaces P4 in phase 3), tail.py, `spikes` (40) + tail flare

| field | spec |
|---|---|
| footage | [v7] A2: flare 10 t → launch 12 t → hexagram r 5-6 m at / ahead of the player ≥ 20 t before; 6-7 lumps, each after a bolt (2-3 t), fall 5 t, burst r 3-4 m, lumps 1-4 every 0.3-0.6 s, 5-6 ≈ 32 t apart; "범위밖으로 피한다고 피해지지 않습니다 · 땅에 꽂히는 타이밍에 대시"; one burst = 9 % max HP + brand |
| timeline | `gold_on` t0-22; launch t14; hexagram 1 (r 4.8) at `lockv` (lead 10) at t26; **lumps 1-4 impact t44 / 54 / 64 / 74**; **lumps 5-6 impact t98 / 122**; before each lump, if the player is > 8 b from the current hexagram centre, a new hexagram is drawn under the player; end 140 |
| hazards | each lump: **locks the player's feet 13 t before impact wherever they are** (decal r 3.0), bolt fx at −3 t; burst disc r 3.0, **0.7** Electro + brand; groups (1, 2), (3, 4), 5, 6; dodgeable: keep running (a 13-t sprint covers 3.65 b > 3.3) or dash on the bolt |
| checks | burst 1.4 per 40 t; dash ≤ 2 per 20 t |
| fx / sound | hexagram seal decals with the 번개 rune, lump props, bolt cards, violet crystal bursts; hexagram `block.respawn_anchor.set_spawn` p 1.6 + `block.enchantment_table.use` p 1.2; bolt `entity.lightning_bolt.thunder` p 1.6 v 0.25; impact `block.pointed_dripstone.land` p 0.5 + `block.amethyst_block.break` p 0.8 + `entity.lightning_bolt.impact` v 0.5 |

#### E Intro, service 26, `intro` (150), seq

- [v1] I: sealed in a gold glyph prism inside a ring of 6 steles, eyes light (+25), two steles shatter (+79, +111), the seal
  shatters (+152), close-up roar (+155 … +193); the boss bar shows during the intro; untargetable.
- Ours: `seq.py` spawns the per-fight seal props (6 steles at r 8 around the spawn from the theme's position list, the
  prism UUID 0x80) and the floor glyph circle decal; the player arrives at the south edge; eyes t25, rise t30, cracks t50 /
  t70 (two steles shatter into chunk displays), **seal shatter t112** (prism shatter + white flash), land t116, roar t120
  with radial gold leaves + the line "인간 주제에, 선을 넘지 마라!", blast t130 (push-only ring r 8, no damage; the
  remaining steles crumble); music `"1"` from t120; fight at t150; registry intro 160.
- Sounds: sealed drone `block.respawn_anchor.ambient` p 0.5 + thumps `entity.ravager.step` p 0.5; stele break
  `block.deepslate_bricks.break` ×3 p 0.6 + `entity.generic.explode` p 0.8 v 0.4; seal shatter `block.glass.break` p 0.6 +
  `block.amethyst_block.break` p 0.7 + `block.beacon.deactivate`; roar `entity.ender_dragon.growl` p 0.6 +
  `entity.ravager.roar` p 0.5 + `entity.warden.roar` p 0.8 v 0.6.

#### D Death, service 24, `death` (120), seq

- No footage; [mot] §5.19. Clears every hazard, field, emitter, orb, shard and the brand; music stopped with a sting
  (`block.beacon.deactivate` p 0.6); lines at t0 / t80; chin t34, tail t66, head t92; the kit's `seal_reform` (gold glyph
  prism) and **`look/petrify`** from t96; the rig scales out t120 → 140. Sounds: `entity.iron_golem.death` p 0.5,
  `entity.ravager.death` p 0.6, `block.amethyst_block.resonate` for the seal. Rewards and the chapter clear follow the
  framework path (§1.1).

---------------------------------------------------------------------------------------------------

### 6. Numbers

#### 6.1 HP, attack, damage, rewards (starting values; §6.2 decides the final ones)

| field | value | why |
|---|---|---|
| hp | ~~260~~ **135** (FIX balance pass, Change note 5: the sim's sword-walker kill time; 260 gave 329 s) → about 1355 HP at L6, three pools of about 452; was: 260 → 2610 HP at L6, three pools of 870 | [ch] §5.4's 360 ignored the RES. The kill-time model ([ch] `calc.py`: the Guardian sim's 104 s for an item-less Lv4 sword agent, scaled by HP, player atk and `lv_mult`) gives at hp 260: 128 s raw → **183 s for a physical attacker** (RES 30), 143 s for a RES-10 element, plus ≈ 40 s of floored transitions; the B3 tail window counts as damage time |
| atk / dmgMul | 12 / **140** | 1.0 = 23 HP on an item-less Lv5 (15.5 %) vs the Guardian's ≈ 11 %; the biggest single hit (charge 1.8 = 44 HP, 30 %) equals Raiden's `damage:19` at chapter 1; Raiden's `damage:34` (80 HP) has no equal here |
| xp | 40 | = Raiden |
| gold / sapphires / picks | ×15 × chapter (2..4 random) / 2 / 0 | R5 (Raiden economy) |
| level | L6 in chapter 1 (L18 if forced to chapter 3) | `#mapIdx 5` |

Hit sizes at L6 vs an item-less Lv5 (HP 148, def 18), dmgMul 140:

| coef | 0.15 | 0.2 | 0.35 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0 | 1.1 | 1.2 | 1.4 | 1.5 | 1.8 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HP | 3 | 4 | 6 | 11 | 14 | 15 | 19 | 21 | 23 | 26 | 29 | 33 | 36 | 44 |

Landslide at transition 1, all six landed: 5 × 19 + 23 = 118 HP (80 %). Brand: 5 × 4 ≈ 20 HP (Cryo ×2 at 3 stacks).

#### 6.2 Fairness targets (the sim of record, §8.5; acceptance ±20 % unless a bound is given)

The per-kill damage is the binding target (`plan_crit_fairness.md` M9): the Guardian's melee walker loses ≈ 2.0 Lv4 HP
pools per kill (158-163 HP/min × 104 s); a chapter-end boss may cost up to **1.6×** that.

| metric | target |
|---|---|
| **damage per kill**, melee walker (HP lost per minute × kill time, in max-HP pools of the item-less Lv5) | **≤ 3.2 pools** |
| HP lost per minute **in % of max HP**, stand / melee walk / ranged walk | **0.8 ×** the Guardian's % rate for the same behaviour (Guardian re-measured on `M0` in the same harness) |
| perfect dasher (dash policy) | ≤ 0.3 × the Guardian's walker |
| positional teaching | a melee walker that keeps to the head or the tail loses ≥ 25 % less than one that stays at the flank |
| undodgeable share (walker avoiding the flank; and the `ranged_flank` policy at 10-14 b) | ≤ 30 % of its damage taken |
| brand DoT share | ≤ 15 % of damage taken |
| largest burst in 2 s (outside the landslide) | ≤ 45 % of max HP (the static rule-2 check guarantees it per pattern) |
| melee uptime in Pyro phase 2 and with Hydro orbs | ≥ 70 % of the phase-1 value (ticks with a vulnerable proxy in reach while outside every field / orb) |
| kill time, real HP, item-less Lv5 sword agent (physical, the worst element) | **200 s** (160-240) incl. transitions and B3 |
| kill time per character (sword, Navia, bow, catalyst) | each character's Azhdaha ÷ Guardian kill-time ratio within ±25 % of the sword's ratio |
| transitions and the B3 window | reported apart (avoidable or free damage) |
| shard size | 12 % or 8 % max HP, whichever keeps the brand share and the per-kill target |
| performance | ≤ 3 000 commands per tick on each pair's worst concurrent timeline; ≤ 400 entities in the arena box |

Raiden chapter 1 cannot run in the harness (his hazards are not framework hazards), so that comparison stays analytic:
the hit-size table against his `damage:` values ×160 % at L6 ([ch] §5.2) and the kill-time model (Q19).

#### 6.3 Coefficients (pre-filled into `api.DMG` by S1-MOD; only the balance fixer changes them, §7)

| hazard | coef (I2 → FIX) | hazard | coef (I2 → FIX) |
|---|---|---|---|
| P1 chin disc + fan | 1.4 → **0.48** | P1 extras: Hydro geyser · Pyro lumps · Cryo ring · Electro bolts | 0.8 / 0.6 / 0.6 / 0.6 → **0.71 / 0.3 / 0.5 / 0.5** |
| P2 landing / wave 2 | 1.1 / 1.1 → **0.44 / 0.44** | P2 extras: blades · lumps · Cryo ring · Electro bolts | 0.5 / 0.6 / 0.6 / 0.6 → **0.9 / 0.3 / 0.5 / 0.5** |
| P3 charge disc | 1.8 → **1.58** | P4 landing / explosion | 0.9 / 0.9 → **0.34 / 0.34** |
| P5 fronts (×3, slam disc in w1) | 0.9 → **0.36** | P5 extras: blades · lumps · ring · bolts | 0.5 / 0.6 / 0.6 / 0.6 → **0.9 / 0.3 / 0.5 / 0.5** |
| P5b per slam | 0.9 → **0.36** | P6 strips / end discs | 1.2 / 0.6 → **1.01 / 0.5** |
| P7 sweep / eruption | 1.5 / 0.8 → **1.29 / 0.71** | P7 extras: Cryo wall · hail strip · Electro bolts / line · Electro strip | 0.8 / 0.15 / 0.6 / 0.6 / 0.2 → **0.71 / 0.13 / 0.5 / 0.5 / 0.16** |
| P8 line | 1.4 → **1.22** | P8 strip | 0.15 → **0.13** |
| P9 rings / small rocks / rush / burst / centre run | 0.9 / 0.6 / 1.1 / 1.5 / 1.3 → **0.5 / 0.29 / 0.58 / 0.79 / 0.45** | T1 waves 1-5 / wave 6 | 0.8 / 1 → **0.71 / 0.86** |
| B3 emergence | 1.4 → **1.22** | 31 orb | 0.35 → **0.29** |
| 32 big / small | 1.4 / 0.8 → **1.1 / 0.66** | fire field (32, 33, lumps) | 0.2 → **0.08** |
| 41 circle | 0.9 → **0.79** | 42 round / sky bolt | 1.2 / 0.5 → **1.01 / 0.44** |
| 43 icicle | 0.7 → **0.4** | 44 shell | 0.6 → **0.58** |
| 45 burst / hail | 1 / 0.15 → **0.4 / 0.13** | 46 lump | 0.7 → **0.5** |
| brand tick (`pl_dot`, per mille max HP; floor 1 HP) | 30 → **5** | shard shield (per mille max HP) | 120 → **120** |

FIX balance pass (Change note 5): the bold values are `api.DMG` now; the I2 values are kept on the left of each arrow.

---------------------------------------------------------------------------------------------------

### 7. Stages (parallel worktrees, strict file ownership)

#### 7.1 Graph

```
D0   day-0 contracts (S:az/contract/{cm,theme,fx,manifest,s2}.md; §7.2) - the defaults of §9 are binding from here;
     user answers become numbered change notes
M0   main after the wip/fg merge (check #mbHealAmt survived the merge before S1 starts)
 |- RIGLIB    wip/riglib (from M0)         shared rig-lib extras + mboss_shape_lib.mjs, identity on M0 -> main (early)
 |- S1-CM     wip/az-cm (from M0)          chapter mode + cproto + cp_test + generic suites
 |              -> CM-REVIEW (state, identity) -> merged into main = AZ-CM (chapter 1 still Raiden)   <- Apep branches here
 |- S1-HARN   (scratchpad)                 real-engine azsim, azfair agent, Guardian re-measure on M0
 |- S1-MOD    wip/az-mod (from wip/az-cm commit 1; rebases on wip/az-cm daily, then on AZ-CM)
 |              module core / ai / brand + working frame stubs (trans B3, seq) + test_azhdaha; uses the R1 rig + fallbacks
 |- S1-FX     wip/az-fx (from wip/fg@aa8cd73 now; merges M0 later)     the kit per §2.4 + test_az_fx
 |- S1-ARENA  wip/az-arena (from wip/fg@aa8cd73 now; merges M0 later)  theme (flat-floor version on day 1) + test_arena_az
 |- R2        wip/az-rig-<region> (running) -> R3 integrate on wip/az-rig (+ M0 + RIGLIB) -> U1 renders to the user
 |- R3a       wip/az-rig: manifest v1 (every §3.2 clip blocked out: events, anchors, tracks, schedules, offsets)
I1   wip/az = main@AZ-CM + az-mod + az-fx + az-arena + az-rig@R3a; I1-WIRE; contract freeze
 |- S2-A wip/az-pa (geo_a) | S2-B wip/az-pb (geo_b) | S2-L wip/az-pl (leg) | S2-T wip/az-pt (tail) | S2-S wip/az-ps (trans, seq)
 |      per-stage test copies; S2-FX on call; requests applied the same day on wip/az; S2 branches merge wip/az daily
 |- R3b       clip polish (schema and event ticks frozen; change notes trigger re-runs)
I2a  ps -> pa -> pb -> pl -> pt merged, tests folded into S:az/tests, test_az_flow  -> REVIEW state + fairness
I2b  rig R3b merged (fallback list empty); each S2 author re-greens its own suite   -> REVIEW fidelity + fx/audio + rig
FIX  core -> rig -> kit -> patterns, then one balance fixer until §6.2 holds
VERIFY  rebuild x2, run_all, identity, fairness re-run, renders -> user -> merge into main with route:true
```

#### 7.2 Day-0 contracts (written before code; Apep adopts `cm.md`)

| file | owner | content |
|---|---|---|
| `S:az/contract/cm.md` | S1-CM | every AZ-CM function, score, storage path and registry field of §1.2 / §1.4 (the union with `[AP]` FW-1..19 minus FW-13), the proxy and state-set schema, the UUID allocation, the music map, the shared-edit table |
| `S:az/contract/theme.md` | S1-CM + S1-ARENA | the theme-module interface (`arena_layout()`, `slices()`, `props()`, `entrance_layout()`, constants), the prop position lists the module and `seq.py` read |
| `S:az/contract/fx.md` | S1-FX | the kit call list with macro args (= `az_fx_api.md` §0 skeleton) and the deliverable table of §2.4 |
| `S:az/contract/manifest.md` | S1-MOD + R3 | the manifest schema v1 of §3.6 (the stub fallbacks and R3a use it) |
| `S:az/contract/s2.md` | S1-MOD | `ADDON_POINTS` (§4.6), the leg-special and B3 start / stop protocol, `api.B3_*` constants, the Pattern hooks (`pause`, `resume`, `reload`, `cancel_bg`), `p/firefield/on_brand`, the request protocol (registry fields, `api.DMG` keys, pack-check families) |

#### 7.3 Ownership

| stage | owns (writes) | may touch (shared) | must not touch |
|---|---|---|---|
| **RIGLIB** | `T:mboss_rig_compile.mjs`, `T:mboss_rig_clips.mjs`, `T:mboss_model_lib.mjs`, `T:mboss_paint_lib.mjs`, `T:mboss_shape_lib.mjs` (new; the content of `azhdaha_shape.mjs` @7c3e9fe promoted), `S:riglib/**` | — | the per-boss rig files |
| **S1-CM** | `T:build_mboss_core.py`, `T:mboss_lib.py`, `T:mboss_registry.json` (schema, the cproto entry and the Azhdaha entry of §1.6; later edits by request), `T:build_mboss_arena.py`, `T:mboss_arena_cp_test.py`, `T:build_cboss_rooms.py`, `T:build_mboss_cproto.py`, `T:check_mboss_pack.py`, `T:build_bossbar.py` (`#buHpCol`), all core outputs `F:mboss/{d,hz,pj,pull,mv,aux,cb,ar,px,music,push,cine,…}/**`, `F:mboss/arena/**`, `F:mboss/cproto/**`, `F:room/cboss/**`, `S:az/tests_cm/**` (test_chapter, test_px, test_fw_az, run_all, gen_check, ident, vcheck, baseline), `S:az/contract/{cm,theme}.md`, README "챕터 보스" | the hand-written shared files of §1.2 (each edit in the README shared-edit table) | the Guardian / butterfly / fieldgen / proto module generators, the kits, the rig files, `mboss_arena_az_cavern.py` |
| **S1-HARN** | `S:az/harness/**` (`azsim.py` with the real-engine list of §8.1, `azfair.py`, `batch.py`, `analyze.py`, `guardian_m0.txt`) | — | the tree |
| **S1-MOD** | `T:build_mboss_azhdaha.py`, `T:mboss_azhdaha/{__init__,api,core,ai,brand,h_core,stub_rig}.py`, the **working frame stubs** `trans.py` (services 20-23 with the real clocks, the special start / stop calls, the B3 frame) and `seq.py` (ownership passes to S2-S at I1), empty stubs `geo_a geo_b leg tail` (ids, PATTERNS, no-op start / tick / cancel; pass to S2 at I1), `AZ:**` minus rig / kit paths, `S:az/tests_mod/**` (test_azhdaha, test_e2e_azhdaha, check_az_manifest), `S:az/contract/{manifest,s2}.md`, README "야타용왕" (core parts) | registry fields of its entry by request to S1-CM | the framework, the kit, the rig |
| **S1-FX** | `T:build_mboss_az_fx.py`, `T:mboss_az_fx_paint.py`, `T:mboss_az_fx_manifest.json`, `AZ:fx/{card,cardx,look,clear,uninstall}` + `AZ:fx/{e,p,tele,snd,hud,prop,test}/**`, RP `assets/rlk/{textures,models/item,items}/mboss/az_kit/*`, `assets/rlk/font/mboss_az.json`, `assets/rlk/textures/font/mboss_az/*`, `S:az/contract/fx.md` (= `az_fx_api.md`), `S:az/fxtests/**`, `S:az/fxrender/**` | the atlas list (append through the generator's merge) | everything else |
| **S1-ARENA** | `T:mboss_arena_az_cavern.py` (from its first commit), `S:az/tests_arena/test_arena_az.py`, `S:az/arenarender/**` | `S:az/contract/theme.md` (with S1-CM) | generators, kits |
| **R2** (running) | one `T:azhdaha_<region>.mjs` each + its renders under `S:az/rigwork/r2_<region>/**` | listed small joint edits in `azhdaha_pose.mjs` | builder, aggregators, clips, shape, materials, libs |
| **R3 / R3a / R3b** | `T:build_mboss_azhdaha_rig.mjs`, `T:azhdaha_{pose,clips,geometry,paint,materials,shape}.mjs` (shape = shim), the region files after the R2 merge, `T:mboss_azhdaha_rig_api.md`, `T:mboss_azhdaha_rig_manifest.json`, `AZ:rig/**`, RP `assets/rlk/{textures,models/item,items}/mboss/azhdaha/*`, `S:az/rigwork/**`, `S:az/tests_rig/test_az_rig.py` | the atlas list (append) | module / kit / framework / shared libs (requests to RIGLIB) |
| **S2-A** | `T:mboss_azhdaha/geo_a.py`, `h_pa.py` → `AZ:p/{chin,jump,charge,spikes}/**`; `S:az/tests_pa/pat_geo_a.py`; renders `S:az/renders/pa_*` | requests in `S:az/requests/pa.md` | api.py (except its re-export line), core.py, other pattern files |
| **S2-B** | `geo_b.py`, `h_pb.py` → `AZ:p/{stomp,stomp3,feint,whip,tailslam,burrow}/**`; `pat_geo_b.py` | as S2-A (`requests/pb.md`) | |
| **S2-L** | `leg.py`, `h_pl.py` → `AZ:p/{orbs,meteor,firefield}/**`, `AZ:xl/**`; `pat_leg.py` | as S2-A (`requests/pl.md`) | |
| **S2-T** | `tail.py`, `h_pt.py` → `AZ:p/{frost,bolt,icicle,shell,icespike,elspike}/**`, `AZ:xt/**`; `pat_tail.py` | as S2-A (`requests/pt.md`) | |
| **S2-S** | `trans.py`, `seq.py`, `h_ps.py` → `AZ:p/{slide,absorb1,absorb2,burrow3}/**`, `AZ:seq/**`; `pat_trans.py` | as S2-A (`requests/ps.md`) | |
| **S2-FX** | (= S1-FX) kit changes requested by S2, served the same day | | |
| **I1-WIRE / I2a / I2b** | merge commits; applying `S:az/requests/*` to api / core the same day; wiring the kit hooks (uninstall → `fx/uninstall`, cleanup → `fx/clear` + `fx/hud/clear`, pause → `fx/tele/clear` + field redraw on resume, death_start → `fx/tele/clear`, HUD lines → `fx/hud/put_extra` / `put_sub`), switching `api.K` to the kit and dropping the fallbacks, checking prop names against the kit manifest, building a fresh RP, folding the test copies, `test_wire_az.py`, `test_az_flow.py`, README integration notes, registry `route: true` at VERIFY | all of the above (conflict resolution, requests) | |
| **REVIEW** (state, fidelity, fairness, fx/audio, rig) | `S:az/review/<area>/**` (findings.json + repro scripts); the fairness reviewer extends the sim of record in place (`S:az/harness/**`, one sim) | read-only on worktrees | the tree |
| **FIX** | the files named by the confirmed findings, in the order core → rig → kit → patterns; then **one balance fixer** with write access to `api.DMG`, the AI weights in `ai.py` and the pattern files' coefficients, until §6.2 holds | | |

#### 7.4 Green per stage

| stage | green when |
|---|---|
| RIGLIB | the Guardian, butterfly and fieldgen rig outputs byte-identical on `M0`; builder self-checks |
| S1-CM | `tests_cm` (on cproto) + the `M0` suites (`S:mb/int_tests`, `S:mb2/tests`, `S:mb2/fxtests`, `S:mb3/tests`) + `ident.py` (Guardian / butterfly / fieldgen / proto outputs and the plaza byte-identical to `M0`) + `gen_check.py`; then CM-REVIEW (state + identity) |
| S1-HARN | the agent reproduces the Guardian numbers of `S:mb3/fgfix/sim` within 5 % on `M0` |
| S1-MOD | `tests_mod` on the latest CM (arena ensure stubbed until it merges `wip/az-arena`), `check_az_manifest.py` on the current manifest + fallbacks |
| S1-FX | `test_az_fx` + the `M0` suites |
| S1-ARENA | `test_arena_az` + the `M0` suites |
| R2 / R3 integrate | builder checks, per-region budgets, renders; `test_az_rig` |
| R3a | `check_az_manifest.py` (against §3.2), `test_az_rig`, the 3-D proxy coverage, identity of the other rigs |
| I1 | `test_wire_az` + `run_all` once after the wiring |
| S2 | its own `pat_*.py` + `run_all` on `wip/az` |
| I2a / I2b | `test_az_flow` + `run_all`; I2b also the empty fallback list |

#### 7.5 Merge order

1. RIGLIB → main (pure library change, identity proven).
2. S1-CM → CM-REVIEW → main as **AZ-CM** (no routing change; chapter 1 still Raiden).
3. I1: `wip/az` from main@AZ-CM; merge `wip/az-mod` (rebased) → `wip/az-fx` → `wip/az-arena` → `wip/az-rig`@R3a (which
   merged M0 + RIGLIB; the three other rigs byte-identical) → I1-WIRE → `run_all` → contract freeze.
4. I2a: `wip/az-ps` → `pa` → `pb` → `pl` → `pt` (pattern files disjoint; the services first so the transitions exist when
   the pattern suites run); requests were applied the same day, so no merge waits for a request.
5. I2b: `wip/az-rig`@R3b.
6. FIX, VERIFY, the user, then `wip/az` → main with `route: true` (the only change that makes chapter 1 Azhdaha).

---------------------------------------------------------------------------------------------------

### 8. Tests

#### 8.1 Suites

| suite | owner | covers |
|---|---|---|
| `test_chapter.py` | S1-CM | **on cproto** (generic, reusable by Apep): routing ch 1 / 2 / 3 / 4+ with `route` flags, `#cbForce` only under `#mbTest`, entrance build → `cb/prep` → storage; gate (oact 16, guards, "준비 중" while building) → sliced ensure → spawn → kill → ×15 gold × chapter + 2 sapphires, **no boxes**, `k_chapter`; abort → gate back; `cb/lose` (+ test variant); title swap; repool + `#mbTot` + `test/level`; music set / loop / stop / no overlap; the two-look swap of `cp_test` with per-look stamps; every cleanup path (room/clear, wipe, remove, uninstall, reload) incl. the forceload released and the barrier sweep; **Raiden smoke** (a narukami zone builds, `boss_spawn` reaches `boss/raiden/spawn` (stubbed), `combat_clear` still spawns `k_chapter`) |
| `test_px.py` | S1-CM | the framework proxy runtime on the stub manifest (S1) and the real one (I1, I2b): spawn / respawn after `/reload` (12 proxies + the shadow), tracks, parking, state sets; **every one of the 17 `combat/apply` call sites** plus the `apply_reset` / `melee_apply` loops: one attack event → exactly one hit on the body; a reaction in the same tick as its trigger → its own hit; DoTs; lunar hits; numbers at the proxy; RES / `on_hit` / `incoming` / kill on the body; Navia pellets counted on the body; minimap exclusion; clicks polled every tick and cleared while paused; the husk at scale 0.1 with no shield; the push capsule and every gate of §4.12 |
| `test_fw_az.py` | S1-CM | N4 mask (inside any safe circle with the 0.3 pad → no hit, horizontal test, groups, nododge, no radius limit), N7 events (`#mbDodgeOk` only for one-shot strikes ≥ 12 t and pj), `pl_dot` (non-lethal, shields absorb at 250 %, no defence, i-frames ignored, refused while dead), NoRx (no `player_hit`, colour kept), floor (clamp, `#mbFloorHit` on ≤, `#mbFloorRaw`, true damage bypass), per-element RES on body and aux, cine, push ring (no damage, skips hazard landings), `lockv`, `local`, `hz/extend`, `#pjNoDodge`, `#buHpCol` default byte-identity, mid-boss `mres 0` unchanged |
| `test_arena_az.py` | S1-ARENA | on `arena_layout()` without a game: opaque full blocks only inside r 28, solid fill y 192-199 under r ≤ 14, no solid block below y 216 inside r 28, no light-transmitting block inside r 28, every fill ≤ 32 768 blocks, ≤ 40 slices, the entrance fits a zone, every prop name exists in the kit manifest |
| `test_az_rig.py` | R3 | mcsim: spawn / respawn of the 46 parts + shadow, looks (all 4 combos + petrify), visibility states, flash groups, `glow/gold_*`, every clip plays to its end, hidden spans, the root-offset rule |
| `check_az_manifest.py` | S1-MOD | the manifest against §3.2 / §3.6: names, lengths, played events, anchors, tracks, yaw schedules, hidden spans, root offsets, proxy layout, UUIDs; run in `run_all` from I1 |
| `test_azhdaha.py` | S1-MOD | the module core: pair roll, persistence and display storage; RES for the 4 pairs × elements 0-8 (×0.70 / ×0.90); floors F1 / F2 / 1 / 0 and the queue (clamp and exact-floor), "흡수 중 (raw)"; transition order (leg special first at transition 2, orb refresh), cine windows; looks per phase; the B3 frame ticks and "마지막 일격"; HUD lines and badges; AI over 9 000 t (zones, dwell, FLANK rule 90 %, exit test, skip list, no repeats except P2 / P5 ≤ 2, cooldowns, phase sets, one bg emitter in phase 3, field-area gate, leash, anti-stall); brand (apply on landed strikes only, both elements in phase 3, refresh to max(rem, 3), Cryo stacks and decay, ticks non-lethal, shields, heal meter 6 %, perfect dodge rules and its 40-t limit, shard drop / placement / cap / pickup / larger-shield rule / pause freeze, cleanup); lingering caps, family groups, clear melee points, refresh limit; bg slots; addon dispatch with lead and context, `api.after`; pause, reload ×5 (re-derivation), locks, test commands, death → chapter clear, uninstall; **the per-pattern tables** imported from each `pat_*.py` `TABLE` |
| `test_e2e_azhdaha.py` | S1-MOD | boss map → entrance → gate → arena → intro → phase 1 → transition 1 → phase 2 → transition 2 → B3 → surfacing → kill → gold / sapphires → `k_chapter` → `run/next_chapter` → `pick/boss` = Raiden (the full `run/start` path stays an in-game checklist line) |
| `test_wire_az.py` | I1-WIRE | the kit hooks wired, `foreign()` spares the kit, `api.K` = the kit, every prop and preset name resolves, the fresh RP builds |
| `test_az_flow.py` | I2a | the cross-author flows for **each of the 4 pairs**: transition 1, transition 2 (leg special → landslide → absorb 2 → B3 → 41 / 42 → surfacing), the addons per pair and phase, rule 33 on a Pyro brand, plus a reload and a pause inside every step |
| `pat_geo_a.py` … `pat_trans.py` | S2 authors | per pattern: hit ticks against the manifest, coefficients, element per phase, shapes and sizes, groups, telegraph pairing (decal = hazard size and time, ≥ 12 / ≥ 20 t), the addon calls at event − 12 with their context, clamps to the walk disc, cancel / pause / reload cleanliness, the sounds and kit calls present; each exports a `TABLE` |
| `test_az_fx.py` | S1-FX | every preset / telegraph / sound / HUD glyph callable; element palettes and the undodgeable look; the field pool; **zero skipped attack-telegraph calls** when replaying each pair's worst concurrent timeline (fields at cap + a strip + the phase-3 spike variant + a bg emitter + P1 / P4); card peaks ≤ 64 fx / 40 telegraph / 16 field; sprite rules; atlas ≤ 0.6 M px |
| perf probe | S1-MOD (in `test_azhdaha.py`) | mcsim command count per tick over the worst timeline of each pair (≤ 3 000) and the arena entity count (≤ 400) |

`azsim.py` (S1-HARN) runs these engine functions **for real**: `combat/apply` (+ the proxy and RES lines), `apply_mods`,
`res`, `gold_drop`, `clear_atkflags`, `melee_begin`, `element/rx_run` + `element/run/*` + `aoe_hit`, `element/dot`,
`element/lunar/hit`, `player/take_damage`, `player/hurt_elem`, `engravings/guard/absorb`, `element/shield_absorb`,
`room/pick/boss`, `boss_spawn`, `zone_build`, `zone_enter`, `combat_clear`, `obj/click`, `run/next_chapter`; the rest stays
stubbed as in `fgsim.py`.

#### 8.2 `run_all.sh <worktree>/roguelike [tag]`

Per-stage copies (`S:az/tests_<stage>/`, baselines under `baseline/<tag>/`) until I2a folds them into `S:az/tests/`
(the union of the baselines, as FGI2 did). Same shape as `S:mb3/tests/run_all.sh`: the az suites + the fieldgen,
butterfly, framework / Guardian suites, `gen_check.py` (documented generator order, a second run, reverse order, `AZ:`
wiped and rebuilt core ↔ kit, the ownership probes, `RP=` builds every kit and rig RP twice and prints the stitched atlas
size; **I1 fails above 15.5 M px**), `ident.py` (**`F:mboss/{guardian,butterfly,fieldgen,proto}/**` and the plaza
byte-identical to `M0`**, the three other rigs byte-identical after the RIGLIB merge) and the validators (check_refs,
check_macro from the root, check_nbtpath, check_mboss_pack, lint_mc; only new findings fail). Three suites at a time,
one line per step, exit 1 on any failure.

#### 8.3 Static generator checks (in the module build; a failure stops the build)

1. Decal = hazard (§0 rule 1): every hazard sample lies inside its decal + 0.3 b, and every decal cell is hit by some
   sample (P7's wedge union in particular).
2. Burst budget Σ ≤ 2.9 per 40 t per spot, per pattern and element pair (§0 rule 2).
3. Dash budget (§0 rule 3).
4. Telegraph floors 12 / 20 t; front band ≥ advance.
5. Exits: P7's exit test is generated, not hand-written; every 42 round has a safe circle reachable within the marker
   window from any player position the placement rule allows.

#### 8.4 Fairness simulator (the sim of record: `S:az/harness/azfair.py` + `batch.py` + `analyze.py`)

- Agent: attacks the **nearest vulnerable proxy** in reach (never the body point); swing speed 0.108 b/t with no sprint
  and no jump while swinging, the dash cancelling the swing; jumps the low fronts when not swinging and **stops attacking
  at a transition message**; reads N4 safe-circle markers and walks / dashes into the nearest; steers around orb discs;
  the N12 push; the brand (no heals: the DoT runs unless a perfect dodge cleanses it); picks up shards within 6 b when
  safe; real shields (both shield functions unstubbed); Lv5 item-less player (HP 148, def 18, atk 18); attack element per
  character (sword 0, Navia 5, bow 1, catalyst 8).
- Policies: stand, melee walk, ranged walk, `melee_head`, `melee_tail`, `melee_flank`, `ranged_flank` (orbits at 10-14 b),
  dash.
- Presets: `azbase` (stand / melee walk / ranged walk × 3 seeds × 3 min × the 4 pairs, Azhdaha forced into each phase for
  equal time) + the Guardian (force 1) on the same harness; `azpos` (head / tail / flank melee, ranged flank); `azdash`;
  `azttk` (real HP to the kill: sword / Navia / bow / catalyst / sword-dash × 3 seeds); output per phase and per pattern
  (HP lost in % of max HP, hits, undodgeable share, brand share, deaths per minute, dealt per minute, uptime, pools per
  kill, largest 2-s burst).
- Run by S1-HARN (smoke on cproto + the Guardian on `M0`), by the fairness reviewer on I2a, and by the balance fixer until
  §6.2 holds.

#### 8.5 Renders and in-game checks

Rig sheets (U1: rest in 4 views, the 4 combos, the player for scale, the head close-up; then key poses per clip vs the
footage frames listed in [mod] §8), kit sheets, telegraph renders per pattern, integration storyboards on the real rig. In
game once (checklist in the README): the stereo music plays non-positionally and loops; wave 6 of the landslide can be
jumped on the cue; the burrow cut line shows no buried part through the floor or the water sheet; proxy clicks register on
the head and the tail; the four looks; the full `run/start` path to chapter 1 → Azhdaha and chapter 2 → Raiden.

---------------------------------------------------------------------------------------------------

### 9. Open questions (the default in bold is binding until the user says otherwise)

1. Pair roll **at the entrance build** (shown on the stele and the gate; "on entry") — or one map earlier on the "보스전"
   object so the last shop / node choices can prepare shields and heals (a one-element player faces a 22 % swing)?
2. RES **flat from the entry** (the user's final table) — or raised on absorb (the original; `RES_BY_PHASE`)?
3. Brand: **3 % × 5 ticks, non-lethal; cleansed by 6 % healing or a perfect dodge of a strike; shields absorb; Cryo stacks
   decay** — or lethal / heal-only / 4 ticks?
4. **응결 결정 shards ON** (new, not in Genshin: the in-arena shield source, the butterfly's 달빛 이슬 idea), 12 % (the sim
   may set 8 %).
5. **Player-side reactions from Azhdaha's hits skipped** (no Freeze, no Melt / Superconduct doubling).
6. Landslide: **wave 6 covers the whole arena (jump or shield only), coef 1.0; six fronts deal 80 % at transition 1 and can
   kill only at transition 2 or after damage** — or keep a safe rim beyond r 22?
7. Second landslide element: **the leg element with the brand**.
8. Burrow lengths: **B3 ≈ 21.7 s with a ≈ 14 s tail window** (footage ≈ 28 s), the charge burrow **≈ 9 s underground**
   (footage ≈ 31 s).
9. **Music ON**: phase 1 `music.end` (C418 "The End"), phases 2-3 `music.dragon` (C418 "Boss"), stereo, vanilla music
   suppressed — or off, or other single-track events (`music.credits`)?
10. **Body push ON** for the torso and the low head, with the gates of §4.12 — or walk-through?
11. **Gate object** (time to prepare, shows the glyphs) — or Raiden-style auto start on entering the zone?
12. Lines: **the wiki's lines verbatim as typed lines**, including the Morax lines — or drop the Morax mentions?
13. **H 7.0 b and walk r 28** (R1) — or 7.5 b with r 30?
14. **Difficulty knob: a long fight with a gentler rate** (kill time 200 s, ≤ 3.2 HP pools per kill ≈ 0.8× the Guardian's
    % rate) — or a shorter, sharper one (kill time ≈ 150 s, hp ≈ 190, 1.3× the Guardian's rate)?
15. **천화 (43) in the background slot** (the boss keeps attacking, as the wiki says) and **가루 (44) in the foreground**
    (the boss only tracks, as the footage shows).
16. Hydro orbs: **600 t per cast, recast after a 600-t cooldown** — or the whole phase (the footage shows them persisting)?
17. **One Cryo whip sweep** — or a 30 % chance of the second, opposite sweep that v8 C shows?
18. 벼락 습격: **5 / 4 / 3 / 2 safe circles, one on the tail in rounds 1-3, one placed relative to the player every round,
    round 4 away from the surfacing spot**.
19. Raiden comparison: **analytic only** — or a Raiden reader for the agent (a separate small task)?
20. Entrance room: **a Liyue stone arch with the glyph stele**.
21. Phase-3 extras on the phase-1 patterns: **chin, jump and stomp (inside their own volley groups), whip and tail slam**;
    the feint and the charge get none — add more only if the playtest wants it.
22. **P8 꼬리찍기 (seen in v3, not named in the wiki) kept as its own pattern** for players behind the rump.
23. Atlas: **I1 fails above 15.5 M px**; the 6.9 M px Raiden `fxg` reclaim is a separate task before Apep's rig lands.
24. Whip sweep: **115° (the head lane stays clear)** — or the footage's 150-200° (it then hits the front quarter that the
    wiki calls safe-ish and that our flank hint sends players to)?
25. **Phase-3 triple stomp (P5b, v9) on the fore paws** — or the phase-1 single slam in every phase?
26. Wiki line "Phase-transition shockwaves come regularly in phase 2 and 3": **read as "at each transition"** (the footage
    never shows 파멸의 산사태 outside them).
27. **The chapter mode is merged into main before the Azhdaha module** (AZ-CM: no gameplay change, chapter 1 stays Raiden
    until the final merge), so Apep can start on it.
28. Known deviation: **our dash chains all three stomp fronts** (the wiki says chained dodges cannot) — accept, or make the
    fronts non-jumpable (rejected by the fairness review: it breaks the dash budget)?

### Change notes

(append numbered notes here.)

**Change note 1 — 10-20 Telegraph rule (user).** Binding from 2026-10-20 for every S2 author, S2-FX and the tests.

User (verbatim, 2026-10-20): "역장 발생 장치의 계수를 많이 올려야될 것 같아. 그리고 이건 공통된 얘긴데 보스의 모든 공격에
바닥의 예고를 보여줄 필요는 없어. 영상에 없다면 그냥 보스의 동작을 보고 회피해야 하는 거니까 그대로 구현해줘."
(The first sentence is the field generator's damage, done in the repo; the second is a rule for every boss, this note.)

**The rule.** A hazard gets a ground telegraph (decal, outline, ring, line, glow, crack, shadow, charging circle on the
floor before the hit) **only when the reference footage shows one** before that hit (*keep*: shaped and timed like the
footage; where ours shows clearly more, e.g. a progress fill over a faint ring, it is trimmed toward the footage). When the
footage shows none, or the attack is not in the footage, or the footage is ambiguous (*none*), there is no pre-hit ground
telegraph: no kit decal and no framework outline (`#hzQuiet 1` stays on every hazard, as §5 already says). Not
telegraphs, so they stay: the boss's motion and wind-up clip, sounds, fx on the boss's own body, projectiles and props
visibly in flight or in the air (halo rings, falling rocks, hovering shells), the attack's own visual at / after the hit
(fronts, bursts, eruptions, lingering fields that are themselves the hazard), HUD lines / banners / hints / the "점프!" cue,
and mechanic markers the footage shows. With the decal gone, the kit's strike flash goes too, so every *none* row shows
its impact preset at the hit tick (all rows below already name one in their §5 fx row). No damage, size or timing changes;
the readability requirements in the table are visuals / clip poses on existing ticks.

**What changes in the rules.**
- §0 rule 1 (decal = hazard) and §8.3 check 1 apply **only to rows marked *keep***. *none* rows have no decal to check.
  The 46 hexagram is a *keep* zone marker (the footage says leaving it does not help), exempt from the size match, like
  42's wash.
- §0 rule 4 / §8.3 check 4: the **12 t (dodgeable) / 20 t (`#hzNoDodge`) floors** are measured from the first visible
  decal for *keep* rows and **from the motion tell** (the first distinguishable clip pose + its sound, or the visible
  projectile / prop precursor named in the table) for *none* rows. `api.tell_rt` is unchanged. The `TABLE` of each
  `pat_*.py` (s2.md §12) gets `tele` = `'keep'` | `'none'` and, for *none* rows, `tell_src` = the clip event or prop that
  starts the readable tell; `kit` = None for *none* rows; `test_azhdaha.py` checks decal = hazard on *keep* rows and the
  floors from `tell_src` on the others.
- §0 rule 6 (the shared undodgeable look, `nd ≥ 1`) loses its users: P6, P7 and T1 have no decal now; 42 keeps its own
  wash / rim look. `nd` stays 0 everywhere.
- N10 fronts (P2, P5, P5b, T1, Cryo rings): the travelling front is the hazard's own visual (`p/front` + the moving ring);
  the pre-strike fill / outline is dropped (call `tele/wave` with the shortest tell or `p/front` alone; S2-FX picks).
- §8.4 sim: timings are unchanged; the agent's "first readable tick" per hazard becomes the decal tick (*keep*) or the
  motion-tell tick (*none*); re-run once S2 lands. The brand's perfect-dodge test and N7 `#mbDodgeOk` keep using the
  hazard's internal `tell`.

**Per hazard** (footage times are video seconds; frames from `understand/vN/`; the "own crops" were extracted into
`S:tele/notes/frames/` and deleted after use).

| pattern / hazard | ground telegraph | footage evidence | keep: shape and timing / none: what the player reads |
|---|---|---|---|
| P1 chin slam disc + crack fan | none | v2 C 8.40-10.65 s (`sheet_C_chin`, `k_f0600`): sway, roar, rear, hold; cracks only after the impact | rear-up + hold (≈ t13 → t35 = 22 t), roar + growl; impact `blade_crown`, cracks, flash |
| P1 Hydro geyser (`chin/impact`) | **keep** (trim) | v4 C 29.0-29.3 s (`full/f1758`, `zoom_floor_glyphs`): a blue water-swirl field on the floor before the geyser at 29.30; caption "범위는 랜덤한 위치에 표시됩니다" | water-swirl field outline r 3.0 at the spot from the call (22 t, as planned), no progress fill; the curved stream decals only from the hit on |
| Pyro lumps (chin, jump w2, stomp w3, stomp3 s3) | none | v5 S 14.7-16.5 / 18.3-20.1 s (`m_lumps_a/b`): lumps arc through the air, fields form after landing | lump props visible in flight (26 t); fireball + fire field at the hit |
| Cryo rings (chin, jump land, stomp w1, stomp3 s1) | none | v8 B 25.10-25.73 s: cyan ring expands from the chin point, no marker | the host impact + the travelling Cryo front |
| Electro bolt discs (chin, jump w2, stomp w3, stomp3 s3) | none | not in the footage (no Electro chin / jump / stomp take); v7 B shows bolts only on the whip line, +1 t after the tail lands | host impact ≥ 12 t before; chin bolts sit on the drawn crack line; **concern**: jump / stomp bolts on "the line to the player" have nothing that shows the line |
| Hydro blades (jump land, stomp w1, stomp3 s1) | none | v4 J 33.50-34.15 s, v9 C 10.60-11.10 s: streaks radiate at / after the landing, no lanes | blade props in flight, inside the host's group |
| P2 landing disc + outline r 10.5 + landing shadow decal; wave 2 | none | v2 B 1.70-5.70 s (`sheet_B_jump`): take-off, airborne overhead, cracks only after the landing; v4 J the same | take-off t6 → land t21 (15 t; was 20 t of decal), the body overhead, take-off sounds; wave 2 rides the landing (one move, "dash twice", take-off → wave 2 = 26 t); the rig's own body shadow may stay, no pattern-drawn landing shadow |
| P3 charge lane (`mline`) | none | v3 B 7.20-8.95 s (`sheet_charge_a`): growl, coil, launch; no lane | pre-turn + `charge_coil` 26 t + growl; the body is the hit |
| P4 spike landings r 1.6 | **keep** (trim) | v1 S 38.05-39.81 s: gold zig-zag crack ring Ø 3.2 m at each point, 18 t before the rock, no growth | zig-zag crack ring outline 14 t before each landing (as planned), no progress fill |
| P4 explosions r 2.5 | none | v2 A 0.00-1.05 s: planted spikes' veins glow ≥ 12 t; the gold ground rings appear with the bursts | planted spike props glowing from t64 (12 t to t76), explosion sounds, boss-outward order |
| P5 stomp: paw disc + outline r 9.7, 3 fronts | none | v3 G 29.72-30.47 s (`sheet_stomp_a`), H 34.12-35.10 s, v4 Q, v9 C: rear / paw lift, the rings are the fronts themselves | paw lift from t0 (17 t to w1), slam sound; w2 / w3 ride the slam (the named 15-t rhythm) |
| P5b triple stomp | none | v9 C 9.6-12.45 s: a paw lift before each stomp, no marker | each slam's paw lift; **requirement**: the clip lifts the next paw ≥ 12 t before s2 / s3 (gaps 23 t) |
| P6 flank strips (nododge) + front / back discs | none | v3 C 12.90-14.10 s (`sheet_side_detail`): two sways, eruption, no floor strips | two sways t0 → t22 (≥ 20), heartbeat sounds; the first-feint hint (HUD) stays; blades + dust walls at the hit |
| P7 swept wedges (nododge) + end-line eruption discs | none | v3 E 19.40-20.63 s (`sheet_tail_a`): high tail, drop, sweep, no marker; v8 B 22.18-22.62 s | tail raise t0-20 + turn (t23 sweep, ≥ 20), `entity.warden.ambient`; whip line + hint (HUD) stay; the generated exit test stays (AI), the `wedge_union` decal goes |
| P7 Cryo ice wall (+ hail strip) | none (the strip is a lingering hazard: field pool) | v8 C 25.80-26.90 s: walls erupt 2 t behind the passing tail | the sweep itself |
| P7 Electro end bolts + crystal line (+ strip) | none (strip: field pool) | v7 B 20.85-22.25 s: the tail lies on the line, bolts +1 t, crystal waves; violet arcs run along the raised tail at −28 t (body fx) | arcs on the tail + the tail lying on the end line |
| P8 tail-slam lane | none | v3 F 24.33-26.83 s (`sheet_slam_a`): tail vertical ≥ 2.1 s, swing, spikes only at the impact | tail raised from t0 (39 t), straight back along the rear axis |
| P9 rock rings r 3.4 | **keep** (trim) | v2 D 16.77-39.98 s (R1-R11), v3 A 2.72 s (R12): gold chevron ring on the player, 25 t before the rock | chevron ring outline, tell 19 (as planned), no progress fill |
| P9 small rocks r 1.4 | none | v2 25.85 / 35.40 s (`sheet_D_shaft`, `sheet_H_far`): far impacts with no ring in view; rocks visible in the air | **requirement**: falling-rock props visible over each point for the 14 t |
| P9 rushes (lane decal 20 t) | none | v2 D 18.50-18.85 s (`sheet_D_surf1`), 20.20 s: a bulge, then the dust wall | **requirement**: the travelling dust mound + a bulge / dust plume and rumble at the breach point for the old 20 t |
| P9 final emergence burst + centre-run lane | none (uncertain) | v3 A 1.9-2.7 s (own crops): a faint dashed ring far off, not at the later emergence spot; 3.30-3.90 s rock spires + dust column 22 t before the burst at 4.40 | **requirement**: dust mound + rock spires at the spot ≥ 19 t; the centre run reads like P3 (emerged boss facing + growl, 20 t) |
| T1 landslide fronts (nododge) + rim rings r 18 / wall | none | v4 L 3.00-12.12 s, v5 T 27.4-36.93 s: foot lifts 7-9 t and the wave-6 rear-up; no floor rings | banner, typed line, "점프!" + bell (HUD) stay; **requirement**: each wave's lift pose spans ≥ 20 t (it starts at the previous wave; gaps 20-21 t); wave 6 rear-up hang 20 t |
| B3 emergence burst r 5.2 (`B3_EMERGE_DECAL`) | none | v6 B3 34.85-36.40 s stationary dust mound; v8 A 18.10-18.89 s dirt mound ("the tell") | dust mound t353-380 (35 t) + rumble; `api.B3_EMERGE_DECAL` retired. The B3 crater (t0) is decor from the footage (v6 10.55-11.15 s), not a hit: stays |
| 31 orbs | none (already) | v4 O, v9 C | the orb props |
| 32 big meteor r 5.2 | **keep** (trim) | v5 M 7.20-9.07 s: 8-point seal glyph at the player 32-37 t before | `seal8` glyph + rim, tell 28, no progress fill |
| 32 small meteors r 2.8 | none on the ground; the air halo stays | v5 M 9.6-11.5 s: gold halo rings in the air 6-10 t before; meteors visible | halo 12 t (air) + the falling prop |
| fields (33 fire, hail, strips) | n/a: the field is the hazard (field pool stays) | v5 / v8 / v9 | — |
| 41 frost circles r 7.5 | **keep** (trim) | v8 A 8.40-9.55 s: star outline draws, burst +24 t; v7 D 39.37 s | heptagram lines + rune, no progress fill; the icicle comet at +18 is the timing cue |
| 42 lightning rounds (mask, nododge) | **keep** | v6 B2 15.50-34.85 s: violet glyph discs ≈ 64 t ahead; wiki "purple light" | violet wash + safe rims with the glyph, 48 t (as planned); `safe_beam` dropped (no column in the footage) |
| 42 sky bolts r 1.6 | none | v6 B2 15.90-16.45, 21.70-22.00, 26.25-26.60, 30.25-31.70 s: single bolts, crackle only after | lock sound 12 t before + "keep moving" (it lands where the player stood); **concern**: no visible precursor in the footage |
| 43 icicle lances r 1.6 | none | v9 A 1.85-2.30 / 4.10-4.70 s, v8 D 33.88 / 39.20-39.50 s: lances dive, no marker at the aim | the ice sphere + the lance in flight (≥ 12 t) |
| 44 shells r 2.4 | none | v7 A1 4.85-8.38 s: hover cloud, dives, no marker | hover cloud + dive; **requirement**: a flash + sound on the shell at its lock (launch − 4), so 12 t stay readable |
| 45 ice star fields r 4.0 | **keep** (trim) | v8 D 37.25-37.50 s: star field under the player ≈ 20 t after the launch, lands ≈ 56 t later; v9 A | star seal lines + rune, no progress fill |
| 46 hexagram r 4.8 | **keep** (zone marker) | v7 A2 10.0-10.2 / 13.30 s: hexagram r 5-6 at / under the player | hexagram + rune as planned; exempt from decal = hazard |
| 46 per-lump decal r 3.0 | none | v7 A2 10.83-15.55 s: the lump visible high, a bolt down it 2-3 t before, no per-lump ring | **requirement**: the lump prop visible over the lock point from the lock (13 t) + the bolt at −3 |
| E intro glyph circle | decor (no hazard) | v1 I | stays |

**Built kit assets (`wip/az-fx`, read only here) left without a user:** `tele/sector` (+ `e/sector_disc`, `e/sec_loop`,
`e/sec_edges`), `tele/wedge` and the §3.1 union protocol, `tele/ring`, `tele/line`, `tele/lane_side`, `tele/mline` /
`mline_aim` / `mline_turn` / `mline_end`, `tele/safe_beam`, the `nd 1 / 2` branch (`t_nd`, `t_ndj`, red-amber rims), the
pre-strike fills of `tele/disc` / `tele/wave` / the four seals (`t_fill`), and the sprites `t_sf15 t_sf30 t_sa15 t_sa15l
t_sa15r t_sa15b t_sa30`, `t_bo25 t_bi25 t_bo50 t_bi50 t_bo71 t_bi71 t_bo84 t_bi84`, `t_bar`, `t_wall`, `t_lane` (left only
as the non-Cryo / Electro strip fallback); plus the matching `K.tele_*` helpers, demos and `test_az_fx.py` cases. Still
used: `tele/disc` rims (P4, P9, geyser), the `tele/wave` ring (optional), `heptagram`, `hexagram`, `starseal`, `seal8`,
`mask_wash`, `safe_rim` / `safe_end`, `crater`, `halo`, `glyph_circle`, the field pool, `tele/clear`. Nothing is deleted
now; S2-FX may drop them after I2 (a request).

**Fairness concerns** (no change made; for the user / the fairness fixer): P6 and P7 are undodgeable and now show no
area (sways / tail raise + hints only); T1's r 18 reach is no longer drawn; 42's sky bolts have no precursor; the
Electro jump / stomp bolts on "the line to the player"; P9 rushes, small rocks and the non-edge emergence appear away from
the body and depend on the precursors required above; 44 and 46 need their on-projectile cues; P2's readable time drops
from 20 t to 15 t.

**Change note 2 — 10-20 Per-region atlas budgets rebalanced (R3 integrate).** Replaces the atlas figures of §3.1
"Per-region budgets" (the part budgets head ≤ 8, body ≤ 14, legs ≤ 16, tail ≤ 10 and the totals ≤ 48 parts / ≤ 1.2 M px
are unchanged). The R2 body refiner spent 0.397 M px (the three 384 × 128 plate sheets of the leaf plates, the apron and
its mask, the five light-corrected hide wraps) against its 0.30 M, while the head used 0.187 M of 0.30 and the tail
0.146 M of 0.28; the material tiles shared by several regions belonged to none. Repainting the body at lower resolution
would cost visible detail on the most prominent forms for no runtime gain, so the builder now asserts (`REGION_BUDGET`,
manifest `budgets.regions`): **head 0.24, body 0.42, legs 0.32, tail 0.16, shared material tiles 0.06 M px (sum 1.20)**.
R3 use: 0.187 / 0.397 / 0.314 / 0.146 / 0.053 = 1.097 M px; only the sprites some model uses are painted (8 unused R1
sprites dropped). Raising one region later means lowering another in a new note.

**Change note 3 — 2026-10-20 I1 freeze (I1 + I1-WIRE on `wip/az`).** Binding for S2 (S2-A/B/L/T/S), S2-FX, R3b and
I2a from here; the contract text is `S:az/contract/s2.md` §18 (with manifest.md §6.1 / §8 / §9 updated the same day).

- **Branch.** `wip/az` (worktree `S:az/wt_az`) = `wip/az-cm` 4de0873 (AZ-CM = the 10-20 release 22ba247 merged; §7.5
  step 3 asks for main@AZ-CM, which does not exist yet) + `wip/az-mod` b7c062d + `wip/az-fx` 6eff3cd + `wip/az-arena`
  174aeef + `wip/az-rig` 6635fe1 (R3a: 41 clips, manifest v1), all `--no-ff` merges without conflict, every output
  regenerated in the documented order (never hand-merged), then I1-WIRE. **Pending:** AZ-CM's PERF-2 / PERF-4 fix commit
  (staged in `S:az/wt_cm`, not committed when I1 ran). `S:az/tests_cm` already carries its regression tests (test_chapter
  §17, test_fw_az §16), which fail on `wip/az` until that commit is merged into `wip/az` (a plain merge of `wip/az-cm`;
  `S:az/tests/cmknown.py` marks exactly those two sections KNOWN and refuses as soon as the tree has the fix). The
  Guardian / butterfly / fieldgen / proto outputs and the plaza stay byte-identical to the release (ident.py).
- **Fallback list (what R3a lacks): empty** — 0 clips from the stub manifest, 0 events, 0 rig API functions
  (`api.fallback_list()`, printed by every build). The stand-in rig `AZ:rig_stub/**` is no longer written
  (`api.stub_rig_needed()`), `kstub/` and `cmstub/` are gone, the module tick calls `rig/tick` only. The I2b check (empty
  list) already holds; R3b must keep it empty (a clip or event it removes comes back as a fallback and a build note).
- **Proxies (contract §6.1, manifest.md).** The rig keeps `proxies.rest` pinned to the R1 columns (the zone /
  melee-point reference: `api.P_TAIL_LANE` = tail2's floor point (0, −10.12)) and adds `proxies.rest_pose`, the real idle
  columns (the idle tail is curled up over the back: tail1-4 at z −5.86 / −8.59 / −7.90 / −4.46, tops 4.5 / 7.2 / 10.4 /
  11.7). manifest.md §6.1 now lists the R3a bone-local points (head [0, −0.6, −0.6], tail1 [0, 0, 1.2], tail4 [0, 0, 1.5],
  paws [0, −0.3, −0.55], feet [0, −1.18, −0.35]) and `rest_pose`; the stub and `check_az_manifest.py` check both. The
  runtime only ever uses the per-clip `clips[].px` keys. R1's tail5 stays dropped (12 proxies).
- **Kit hooks** (fx.md §0.2, plan §7.3): uninstall → `fx/uninstall` (+ `rig/kill`, `rig/uninstall`); cleanup →
  `fx/clear` + `fx/hud/clear`; pause → `fx/tele/clear` + `fx/tele/field_clear` + `fx/hud/flash_end`, resume → the field
  table redrawn (`fld/redraw`); death_start → `fx/tele/clear` (+ `field_clear`, `hud/clear`). **HUD lines (records fx.md
  decision 9, departing from §7.3):** there is no `fx/hud/put_extra` / `put_sub`; the core builds the name line and the
  sub-line itself with the kit font `rlk:mboss_az` (`K.badge`, `K.brand_badge`), patterns add their own sub-line part
  through `rlk:mboss az.subx` (s2.md §16).
- **Arena theme** wired: `api.POINTS / PROPS / ENTRANCE_GLYPHS / ENTRANCE_GLOW` come from `mboss_arena_az_cavern.py`
  (34 props, the entrance glyphs, the water sheets unrotated with the kit model); the build asserts the real theme
  whenever the rig and the kit are present.
- **10-20 telegraph rule in the shared helpers (Change note 1).** `g.wave(..., tele='none')` is the default for the N10
  fronts (all *none* rows): no pre-strike `tele/wave` fill; the kit ring is called 1 t before the strike with tell 1 and
  nd 0, so only the travelling front shows; the hazard keeps its internal `tell` (N7 / perfect dodge). `tele='keep'`
  restores the old pairing. The working `trans.py` stub (handed to S2-S now) no longer draws the T1 rim rings (r 18 and
  the wall) nor the B3 emergence decal: `api.B3_EMERGE_DECAL` is retired and replaced by `api.B3_EMERGE_HZ = 360` (the
  tick the emergence hazard is made, internal tell 28, no decal; the dust mound of `B3_MOUND` is the tell). No tick,
  size or coefficient changed.
- **Ownership** passes as §7.3 says: `trans.py`, `seq.py` → S2-S; `geo_a.py` → S2-A; `geo_b.py` → S2-B; `leg.py` → S2-L;
  `tail.py` → S2-T. api / core stay I1-WIRE's (requests).
- **Tests.** `S:az/tests/run_all.sh <wt>/roguelike [tag]` (RP = `S:az/rp_az`) = tests_cm/run_all.sh (+ `vjudge.py`
  for the validators: only the accepted I1 classes — the rig's and px/azhdaha's fixed-UUID targets, `with storage`
  macro calls, `time query`, the kit's e/spawn shapes; `identjudge.py` for ident 3b: the only new tools files besides
S1-CM's are the az stages' own generator sources; `cmknown.py` for the pending PERF sections) → tests_mod/run_all.sh
  → test_az_rig, test_az_fx, test_arena_az, `test_wire_az.py` (43 checks: real manifest and rig, hooks, api.K, foreign,
  names, theme, the telegraph defaults, contract agreement, routing, RP / atlas). The rebuild-twice gate is
  `S:az/i1/rebuild.sh` (every generator incl. the four rigs and the az kit into the RP). tests_mod was adapted for the
  real rig (the harness stubs `AZ:rig/**` and logs the calls: looks from `rig/look/<channel>/<el>` calls, the respawn
  from `rig/spawn` calls); check_az_manifest and v_az know the real rig's output; gen_check_az's "module alone" wipe
  spares the rig's and the kit's folders. Result on `wip/az` 564035e: ALL GREEN (tests_cm 38 steps ok + the 2 KNOWN PERF
  sections; tests_mod 16 PASS + the KNOWN harness item of requests/mod.md 7c; rig 604, kit 2283, arena, wire 43); two
  rebuilds in the documented order byte-identical (datapack+json 82129c48, RP de1e631c).
- **Budgets.** Stitched items atlas 14.41 M px of the 15.5 M px I1 limit (1.09 M px left for S2-FX / R3b); kit
  0.568 M of 0.6; rig 1.098 M of 1.2 (change note 2 regions held).
- Routing unchanged: `azhdaha.route` false, chapter 1 stays Raiden until VERIFY.

**Change note 4 — 2026-10-20 I2 (I2a + I2b on `wip/az`).** For FIX / VERIFY.

- **Merges** (all `--no-ff`, §7.5 steps 4-5): `wip/az-ps` 44f09b8 → `pa` 75a80c7 → `pb` a0e2ca4 → `pl` 82db4ce → `pt`
  0f2b57a → `wip/az-r3b` a99f32e. Generated outputs never hand-merged: the module regenerated after each pattern merge
  (conflicts only in generated files: `p/resume_d`, `p/pause_d`, `aft/fn`, `x/*`), every generator in the documented
  order after R3b (P7's wedges and the whip addon pieces follow R3b's tail sweep).
- **Shared files reconciled.** `api.Gen.wave`: REQ ps-1 = REQ pa-1, one copy. `ai.py`: REQ pa-3 and pt-1 are one rule,
  "no immediate repeat of a replacement while its swap-in condition holds" (`swap_in()`, the same conditions as the
  `ai/cand` gates and `ai/go`); pt-1's weights for a replaced pattern outside its own phases stay. `core.after()`: REQ pt-2
  kept (the due marker re-tagged before its target runs).
- **Requests served.** Rpl-1 (`core.addons`: the leg dispatcher lines without `return`; in phase 3 the tail body of the
  same point runs after the leg body). Rpl-2 (the core `orb/step` high-band line removed; 31's `p/orbs/band` owns the band).
  Rps-2 (`api` re-exports `h_ps`). Rps-3 (the brand banner at absorb 1's roar t114 + its reload + `test/p2`, no longer in
  `svc/phase_2`). Rpa-2 / Rpb-1 / Rpl-3 / Rpt-3 (kit `tele/disc_o`, `tele/{heptagram,hexagram,starseal,seal8}_o`: the same
  macro arguments, no progress fill; Python `fill=0`; every keep row and its resume redraw switched: P4 landing rings, P9
  rock rings, the P1 Hydro geyser, 32's seal8, 41's heptagram, 45's star seals, 46's hexagram; 42's wash / safe rims
  unchanged). Rpb-3 (`stomp_fl` / `stomp_hl` foot keys only: the paw is up ≥ 0.15 b at the `lift` event t5; events and
  lengths unchanged). **Not served:** Rpb-2 (tangential knockback: a framework hz option of the released AZ-CM).
- **Perf (§8.1 probe ≤ 3 000 commands / tick)**, exceeded once every pattern and both addon bodies ran (4 438 in pair 0:
  three Pyro lumps landing in one tick; 3 176 in pair 1: Hydro blades + a second dust ring): the lumps of a volley land
  one tick apart (lump i: flight 26 + i = its hazard's tell, fireball + field at its own landing), the blade launch plays
  the water `splash` preset, the 31 orbs' ribbons alternate even / odd orbs per tick (each orb still every 2 t). The probe's
  timeline is now the pair's own (its leg special, P4 replacement, 43 / 44); the S1-MOD script forced every special into
  every pair. Worst ticks: 2 648 / 2 959 / 2 648 / 2 400 (pair 1 has the least headroom).
- **Tests.** `S:az/tests/run_all.sh` folds `pat_geo_a`, `pat_geo_b`, `pat_leg`, `pat_tail`, `pat_trans` and
  `test_az_flow.py` (a whole fight per pair: entrance → intro → every phase-1 pattern → T1 → absorb 1 → phase 2 + the leg
  special → T2 (30 → 20 → 22 → 23 + the tail special) → phase 3 (10, 45 / 46, 43 / 44, the leg special) → death →
  rewards → nothing left → uninstall; RES Phys / Geo / the two rolled elements 30, the rest 10 in every phase; the brand;
  every addon body of the pair; a pause and a /reload in every phase). The rig step reads `AZ_RIG_DBG` (default
  `S:az/rigwork/i2/dbg`, built from `wip/az`). Harness fixes: Rpa-4 (trans "no new cast" only during the transition),
  Rpa-5 (`S:mb/int_tests/mcsim.py` seeds Python's RNG at import; suites that seed themselves are unchanged; every M0
  suite passes), Rpl-4 (t_brand clears rule 33's field before the DoT measurement), Rpl-5 (gen_check_az: a `mkdtemp` per
  run). The stage suites were adapted to the merged tree only where another stage's real code now runs next to theirs
  (rule 33's fire fields and the field pool are not telegraphs, the outline variants, the phase-3 tail body next to the leg
  body, the B3 tail special's own keep decals, the lump stagger).


**Change note 5 — 2026-10-21 FIX round (review STATE / FAIR / FID on `wip/az`).** For VERIFY. Five commits: core, rig,
kit, module, balance.

- **Core (framework).** Volley groups keep a second memory `#mbGrpL2` (the last group landed by a one-shot hit), so a
  lingering field re-arming every 10 t no longer re-opens a one-shot group (FAIR-3: 32's six small meteors hit twice).
- **Rig.** Contact-true slam keys: tail_slam lies flat and stiff at the impact t39 (FID-2); jump_slam's left hind stays
  up after the fore landing and comes down on wave 2 (FID-3); the landslide tell lifts the right fore (FID-5) and every
  wave's fore leaves the floor right after the previous slam and stays up to its own (FID-6 / FAIR-12). Events, lengths
  and RETIME unchanged; the core is rebuilt after the rig (the px tracks read the manifest).
- **Kit.** Shaped keep outlines `tele/crack_o` (P4), `tele/chev_o` (P9), `tele/swirl_o` (P1 Hydro geyser) with
  `disc_o`'s arguments (FID-4). Trail presets skip from 36 live cards (TSOFT) so hit-tick impacts always fit the 64 cap;
  frost_burst / ice_wall / boulders / tail_lane / leaf_burst / impact cut (STATE-14). Fast cards `fx/e/cardf`: a card
  with constant stage numbers costs about 25 commands instead of 63 (STATE-2).
- **Module.** State: STATE-1 (leg-special host restarts on /reload, `tr/resume` from `ai/next`), STATE-3 (geyser outline
  redrawn on resume), STATE-4 (B3 reload snaps from the glide start), STATE-5 (orbs back to their band in the B3),
  STATE-6 (absorb-1 reload requeues the leg special), STATE-7 (music 1 when the intro is cut), STATE-8 / STATE-17 (fire
  and hail ambience chains restart after /reload; their clock flags reset at fight start and cleanup), STATE-15
  (re-made fields of a family share one group and keep sequence / start / base life), STATE-16 (B3 emergence re-made
  with the ticks left). Perf (STATE-2): the heavy hit-tick visuals spread over 1-4 ticks (P5 crown / cracks, P6 dust
  walls, P7 one impact + three slab throws, P8 dust ring + leaves, P9 rush dust, absorb 1 / 2 bursts, landslide wave 6),
  orb ribbons every 4 t, Hydro blades in four pairs, Pyro lumps launched one per tick (same landings). Natural
  whole-fight soak (tests_mod soak_az, the perf check of record now): worst tick 2932 / 2983 / 2895 / 2931 per pair (was
  3487 / 4349 / 3973 / 3777), no card skipped. Patterns: FID-1 (slam sound on the paw contact), FAIR-7 (vanilla lift
  sound 14 t before P5 w1), FAIR-11 (dust off both flanks with each P6 sway), FID-8 (grit off the tail root during the
  P7 raise), FID-7 (P3 only with >= 12 b of run inside the leash), FAIR-13 (fields near the player block the P7 exits),
  FAIR-6 (46's locked lumps 15 t apart), FAIR-8 (45 fields piled by the wall clamp share one group), FAIR-22 (a new
  rule-33 fire field at most every 100 t), FAIR-5 (N10 fronts carry their first-tick speed on the marker).
- **Harness (scratchpad, not in git).** FAIR-5: azfair reads a front's speed from its marker and the dash policy dashes
  through dodgeable fronts (FRONTS=1). FAIR-17: one seed per pair (seed + 101 x pair). STATE-9: azsim reads quoted NBT
  path keys (music checks in test_az_flow).
- **Balance (FAIR-1 / FAIR-14, the one balance pass).** `api.DMG` (6.3, the table above), registry hp 260 -> 135 (6.1;
  FAIR-14: no DMG set reaches the 200-s kill time) and FAIR-21's AI weights. Brand ticks sit at `pl_dot`'s 1-HP floor
  (brand_pm 5), so the brand share is a count of ticks: the ranged walker must lose >= 7x its brand HP, which fixes the
  ranged row near 0.9x; the stand row is brought down through the stand-heavy hazards (P4 0.34, 45 0.4, 43 0.4, lumps
  0.3, P9 run 0.45) and the ranged row held up through the hazards that reach a moving ranged player (Hydro blades 0.9,
  P9 rings 0.5, 46 0.5, 32 1.1 / 0.66, 44 0.58). Static rule 2 now counts a lingering family 4 x per 40 t (FAIR-9).
  Sim of record (azbase / azdash / azpos / azttk, 4 pairs x 3 seeds, Guardian rows on the same harness; F = the set
  before the perf follow-up, G = the committed tree):

  | plan 6.2 row | target | I2 (review) | C | D | E5 | F | G |
  |---|---|---|---|---|---|---|---|
  | stand x | 0.64-0.96x | 2.23x | 1.07x FAIL | 0.96x | 0.89x | 0.88x | 0.87x |
  | melee x | 0.64-0.96x | 2.72x | 0.95x | 0.84x | 0.96x | 0.88x | 0.81x |
  | ranged x | 0.64-0.96x | 2.08x | 0.88x | 0.76x | 0.94x | 0.93x | 0.88x |
  | dasher x | <= 0.3x | 1.47x | 0.13x | - | 0.15x | 0.14x | 0.16x |
  | brand melee | <= 15% | 18% | 11% | 12% | 11% | 11% | 11% |
  | brand ranged | <= 15% | 24% | 15% | 16% FAIL | 14% | 14% | 13% |
  | brand stand | <= 15% | 21% | 10% | 12% | 12% | 13% | 13% |
  | burst melee | <= 45% | 62% | 28% | 25% | 32% | 32% | 30% |
  | burst ranged | <= 45% | 64% | 28% | 25% | 32% | 32% | 32% |
  | burst stand | <= 45% | 73% | 32% | 29% | 36% | 36% | 43% |
  | P2 uptime p0 | >= 70% | 65% | 101% | 101% | 101% | 101% | 84% |
  | P2 uptime p2 | >= 70% | 65% | 93% | 93% | 93% | 93% | 80% |
  | kill time sword | 160-240 s | 329 s | 197 s | - | 197 s | 197 s | 199 s |
  | pools / kill | <= 3.2 | 13.65 | 2.78 | - | 2.66 | 2.52 | 2.45 |
  | ttk ratio navia | 0.75-1.25 | 0.82 | 0.83 | - | 0.83 | 0.83 | 0.80 |
  | ttk ratio bow | 0.75-1.25 | 0.92 | 0.94 | - | 0.94 | 0.94 | 0.93 |
  | ttk ratio catalyst | 0.75-1.25 | 0.58 | 0.62 FAIL | - | 0.62 FAIL | 0.62 FAIL | 0.61 FAIL |
  | head vs flank | >= 25% less | -2% less | - | - | -19% less FAIL | -14% less FAIL | -7% less FAIL |
  | tail vs flank | >= 25% less | 29% less | - | - | 0% less FAIL | -1% less FAIL | 5% less FAIL |

  G vs F: the perf follow-up changes when the body pushes and when the AI samples, so the fights differ a little:
  the stander's largest 2-s burst rose 36 -> 43 % (the thinnest margin now, limit 45 %) and the phase-2 melee uptime
  fell 101 / 93 -> 84 / 80 % (limit 70 %); every row F met still holds.

  Not met: the positional row (FAIR-21) and the catalyst kill-time ratio (FAIR-16, RES-bound: plan owner). The flank
  is not punished: the FLANK rule's P6 runs 5.9 of 30 pattern-minutes for a flank player and costs it 0.4 HP per
  pattern-minute (the dash clears the strips), and the harness's "head" / "tail" agents spend 24-26 % of their time in
  other zones. Weights cannot reach "head >= 25 % below flank" (it needs a flank zone rate about 1.8x the head's);
  FAIR-21's design alternative (P6 not dash-escapable in one charge) is a pattern change for the plan owner.
- **Perf follow-up of the balance pass (same commit).** The new HP, weights and coefficients moved the soak timelines
  into new coincidences: the balance gate failed the soak (worst 3004 / 3078 / 3271 / 3059 per pair) and the perf
  probe (pair 2 3057; budget 3000). Module-only fixes, each with a check in test_azhdaha's fixr section or pat_leg:
  `ai/sample` bands by the squared anchor distance from the anchor frame (no `mv/dist` square root; the P7 beyond-tip
  exit reads the same square) and `ai/next` re-samples only off the `ai/sample4` ticks; `push/req` requests no body
  push on a tick that made hazards (`#hzId` moved since the last request; the next tick pushes), and P2 holds
  `#azNoPush` from the take-off through wave 2 (t6-32), P1 on its addon tick (t23) (a push near the body costs about
  430 commands); rule 33's new field comes one tick after the branding hit, at the same floor point
  (`p/firefield/arm`, the cooldown armed on the hit tick); a 43 impact sheds its frost burst from 44 live kit fx
  cards (a 43 + 45 / P1 coincidence the new timelines found cut 2-5 cards at the 64 cap; the shatter sounds stay).
  Soak now 2621 / 2808 / 2679 / 2899, no card skipped, no timer dropped; perf probe 2334 / 2794 / 2334 / 2758.
- **Deferred.** FAIR-2 (pacing: pattern time 78 % vs the Guardian's 37 %; the coefficient route was used, so the
  signature hits are small), FAIR-4 (readable-tick rule in azfair), FAIR-10 timing (P9 ring / 32 / 46 locks; handled
  by coefficients here), FAIR-16, FAIR-18 (32's seal at the absorb-1 roar is plan 5 T2; B3 41 cost reported apart),
  FAIR-21 (above). FAIR-15 is reduced, not closed: melee walk per pair within 13 % of the mean; the stander's Pyro pairs
  stay about 1.7x the Hydro pairs (rule-33 fields and fire ticks at the 1-HP floor).

**Change note 6 — 2026-10-21 VERIFY + routing (`wip/az` 2a59b10).** Plan 7.5 step 6 done: chapter 1 is Azhdaha.

- **Verified on 9235da1** (FIX round head), independently:
  - Rebuild: the generated outputs (`F:mboss/**`, `F:room/cboss/**`, the az rig / kit RP parts) were wiped in a private
    worktree and rebuilt twice in the documented order. The result is byte-identical to the committed tree
    (datapack+json 04024d4b, RP d6605abf).
  - Release identity: the Guardian / butterfly / fieldgen / proto / cproto outputs, the plaza, their generators and
    their RP parts are identical to the release b255669. Raiden (`F:boss/raiden/**`, `F:room/raiden/**`, the raiden
    tools) is untouched.
  - Full gate ALL GREEN in 1781 s, including `test_az_flow` for all 4 pairs. Soak worst ticks 2621 / 2808 / 2679 / 2899;
    perf probe 2334 / 2794 / 2334 / 2758.
  - Fairness sim of record (azbase / azttk / azdash / azpos): re-run on the private copy, it reproduces column G of
    Change note 5 exactly. 21 of 24 6.2 rows pass. The 3 FAILs are the deferred FAIR-21 head / tail vs flank
    (-7 % / 5 %) and FAIR-16 catalyst (0.61).
- **Per-pattern table re-derived from the generated functions** (`S:az/vfy/tools/derive.py` + `vtable.py`): a static
  walk of every pattern clock file through module calls and after() timers.
  - Every hazard's make tick, tell, hit tick, size, coefficient (= `api.DMG` = 6.3 FIX), `#hzQuiet 1`, `#hzNoDodge`,
    and kit telegraph calls match the S2 TABLEs and §5. Keep rows: P4 crack_o, P9 chev_o, the P1 geyser swirl_o,
    32 seal8_o, 41 heptagram_o, 42 wash + safe rims, 45 starseal_o, and the 46 hexagram zone marker; decal r = hazard r.
  - No other ground telegraph: the 32 small-meteor halos are in the air, and the N10 fronts call `tele/wave` with
    tell 1 at strike − 1.
  - Motion-tell wind-ups are ≥ 12 t, and ≥ 20 t for nododge: P6 22, P7 23, T1 20-21, 42 mask 48 (keep).
  - No fix was needed.
- **Routing (the only change):** registry `azhdaha.route` false → true. The generated `cb/route`, `cb/peek` and
  `register` changed; nothing else. Two rebuilds are identical (datapack+json 20b4fcb4, RP d6605abf unchanged).
  - `tests_cm/test_chapter.py` with the real registry: 153 ok, chapter 1 → azhdaha, chapters 2 / 3 / 4 / 7 → Raiden.
  - `test_wire_az` H now asserts route true, no other route:true chapter entry, and the cb/route lines (46 checks).
  - Full gate ALL GREEN in 1664 s.
  - Chapter 3 stays Raiden until Apep's entry (`ch [3]`, route true) lands.
- **README:** the 챕터 보스 intro and the 나루카미 note now say chapter 1 → 야타용왕. The 야타용왕 section gets a player
  summary (where, the element roll, RES, hit columns and the flank rule, phases, the keep list, undodgeable attacks,
  brand / shards, kill time). It also gets the FIX values: hp 135, brand 0.5 %.
- **Deliverables (scratchpad):** `S:az/renders/final_sheet.jpg` (entrance, P1 / P7 / 32 / 45, T1 + absorb 1, the 4 looks;
  real rig, harness runs of the committed tree) and `S:az/final_summary.md` (Korean summary: patterns, keep list,
  balance, known limits).
- **Open for the user / plan owner:**
  - FAIR-21: the positional row; P6 is dash-escapable.
  - FAIR-16: the catalyst ratio, which is RES-bound.
  - FAIR-2: the pacing.
  - Change note 1's fairness concerns.
  - The in-game checklist of 8.5.
