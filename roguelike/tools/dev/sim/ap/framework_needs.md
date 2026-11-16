# 아펩의 오아시스 파수꾼: shared chapter-mode hooks Apep needs from AZ-CM

This is the exact list of shared framework pieces the Apep Warden (chapter-3 end boss, `S:ap/plan.md`) needs from the
Azhdaha chapter-mode stage (AZ `S1-CM` on `wip/az-cm`, reviewed and merged into main as **AZ-CM**), so that each piece is
built once. It is written for the S1-CM owner and its day-0 contract (`az_contract.md` §CM, AZ ledger ST-1 step 2).

`S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`. `AZL` = `S:az/plan_ledger.md`.

## Rules for every item

- **Opt-in, default = today's behaviour.** Guardian, butterfly, fieldgen and proto outputs stay byte-identical (`ident.py`);
  only core outputs change.
- **One owner per shared file**: AZ S1-CM. Apep never edits `build_mboss_core.py`, `mboss_lib.py`, `build_mboss_arena.py`,
  `build_bossbar.py`, `check_mboss_pack.py` or the hand-written shared room / combat files on its own branches. A gap left
  after AZ-CM is merged goes into one reviewed `wip/cm-ap` stage (plan §10 AP-FW) with cproto tests.
- **Names**: the ones AZL AP-3 settled. Where this list adds something AZL does not have yet, the row says **NEW**.
- **Tests** live in the generic `test_chapter.py` / `test_px.py` / `test_fw_az.py` on the chapter-mode proto boss `cproto`
  (AZL ST-1, AP-6), so Apep runs them unchanged on its branch.
- Priority: **MUST** = AP-CORE cannot start without it; **SHOULD** = Apep has a module fallback (named), but the shared
  version is cleaner and Azhdaha uses most of them too; **CAN** = nice to have.

## Summary

| FN | hook | prio | AZL status |
|---|---|---|---|
| FN-1 | registry chapter fields (`kind ch arena res phases music route`, `creg` / `cbyid`) | MUST | accepted (R1, F1, AP-3) |
| FN-2 | routing, `cb/prep`, gate object, `cb/gate`, `cb/start {id}`, entrance rooms from the theme | MUST | accepted (R2, F5, F6, F24-F26, AP-7) |
| FN-3 | arenas from the registry, theme modules, **looks** (sliced, stored, restored from `prep`), per-fight arena props | MUST | accepted (AP-2, AP-7, F8-F10); details NEW |
| FN-4 | `#mbTot`, `mboss/repool {pct}`, `test/level` re-split | MUST | accepted (AP-3) |
| FN-5 | `#mbFloor` + `mboss/floor` + `#mbFloorHit` | MUST | accepted (R6, m17, F16) |
| FN-6 | `mboss/title {title,sub,color}` | MUST | accepted (AP-3) |
| FN-7 | per-entity RES `mbRes0..8` (body from the registry; aux opt-in) | MUST (body) / SHOULD (aux) | accepted (R7, AP-4) |
| FN-8 | hit proxies generated from the rig manifest (any state names, ≤ 16) | MUST | accepted (R8, F3, F7, F33, ST-6) |
| FN-9 | `mboss/cb/lose` (+ test variant) | MUST | accepted (R14, AP-6) |
| FN-10 | chapter test commands, generic `test_chapter.py` on cproto, the real-engine harness | MUST | accepted (AP-6, F14, m-10) |
| FN-11 | `cb/won`, `cb/body`, chapter rewards | MUST | accepted (R4, R5) |
| FN-12 | cleanup / forceload / music stop on every path | MUST | accepted (R13) |
| FN-13 | body burrow support: `rlk_mb_noshield`, husk scale while hidden | MUST | accepted (F15) |
| FN-14 | `hz/mask` + **safe group** `#hzSafeG` | SHOULD | mask accepted (N4, F22); safe group **NEW** |
| FN-15 | hazards in **‰ of max HP** `#hzPm` + `#hzLethal` → `pl_dot` | SHOULD | **NEW** |
| FN-16 | `mboss/pl_dot` (`#mbDotPct` ‰, lethal flag, cine refusal) | SHOULD | accepted (N7, F28, AP-3); lethal / cine explicit |
| FN-17 | no-reaction: `#hzNR` / `#pjNR` + one-shot `#mbNoRx` | SHOULD | accepted (F29, AP-3) |
| FN-18 | `#pjNoDodge` | SHOULD | accepted (AP-4) |
| FN-19 | `mboss/mv/lockv {lead}` with a **dash filter and a sprint cap** | SHOULD | accepted (AP-4); filter / cap **NEW** |
| FN-20 | `mboss/mv/local` | SHOULD | accepted (AP-4) |
| FN-21 | `mboss/push/capsule` (capsules per state from the manifest) + `mboss/push/ring` | SHOULD | accepted (AP-4, B2, F11) |
| FN-22 | `mboss/cine/start|end` | SHOULD | accepted (AP-4) |
| FN-23 | music map + `mboss/music/set {ph}` | SHOULD | accepted (R11, AP-3, F17) |
| FN-24 | bossui `#buHpCol` + **`#buNoNum`** | SHOULD | `#buHpCol` accepted (AP-4); `#buNoNum` **NEW** |
| FN-25 | RIGLIB (`mboss_shape_lib.mjs`, `tol.tp`, px compile, culling per rig, …) + **park** | SHOULD | accepted (AP-5); park **NEW** |
| FN-26 | barrier safety sweep from a **per-row span table** | SHOULD | accepted (AP-4); span table **NEW** |
| FN-27 | atlas size print + gates; command-per-tick probe; entity count | SHOULD | accepted (F35, F36); the two-boss gate **NEW** |
| FN-28 | font U+E900-E9FF for `rlk:mboss_ap`; `mboss_az` in the checks | SHOULD | accepted (AP-8) |
| FN-29 | aux presentation: click-shield size, HP-bar offset | CAN | **NEW** |
| FN-30 | `mboss/mv/step_flat {spd}` | CAN | **NEW** |
| FN-31 | hit / dodge events `#mbHitEv` / `#mbDodgeEv` | CAN | accepted (N7) |
| FN-32 | fractional pj speeds | not needed | — |

---------------------------------------------------------------------------------------------------

## MUST (AP-CORE cannot start without these)

### FN-1 Registry chapter fields
- Fields on a boss entry: `"kind": "chapter"`, `"ch": [3]`, `"arena": "ap_oasis"`, `"res": {"7": 30, "*": 10}`,
  `"phases": [53, 47]`, `"music": {...}` (FN-23), `"route": false|true`, `"picks": 0`, `"goldMul": 1`, `"sap": 0`.
- Chapter entries live in `creg` / `cbyid` (never `reg[]`; the mid-boss roll never sees them); `snbt_entry` emits
  `kind ch arena phases`; `check_mboss_pack.py` checks the 17 hooks + `prep` for chapter bosses; `route: false` keeps
  player routing to the boss off while `test/chapter {id}` still works.
- Apep use: plan §3.7 (its entry is data-only under its own key; no generator edit).

### FN-2 Routing, entrance, gate, start
- `room/pick/boss` → generated `mboss/cb/route` (from the registry `ch`; `#cbForce` honoured only while `#mbTest 1`) →
  `mboss/cb/layout {id}` (entrance layout from the theme's `entrance_layout()`, zones get `data.boss_id`, `data.cboss:1b`).
- Generated `mboss/cb/prep` dispatches on the zone's `boss_id` to the module's `prep` hook (no `$(id)` function names).
- Gate object oact 16 (`room/obj/k_cboss`, label lines from the module's `prep` storage), `mboss/cb/gate` (with the peaceful
  / `zst` / no-body guards of `mboss/gate`), then `combat_start`; `room/boss_spawn` → `mboss/cb/start {id}` (`#mbMode 1`, the
  boss's own arena, `ret_save` / `tp_in` / `bars_show`, no mid-boss roll, no `met` append).
- Apep use: chapter-3 routing, the Sumeru oasis gate, gate label "아펩의 오아시스 파수꾼 — 내성: 풀 30% · 그 외 10%".

### FN-3 Arenas, themes and looks
- Registry `arenas{aid:{theme, ver, cx, cy, cz, r, walk, safe, start, looks:[default, …]}}` beside the plaza's `arena`
  (plaza output byte-identical); `L.arena_of(boss)` for module generators.
- Themes discovered from the registry: `theme` → `tools/mboss_arena_<theme>.py` exporting:
  - `arena_layout()` (blocks; importable for offline renders),
  - `entrance_layout()` (the domain entrance room),
  - **`look_lines(look)`**: the diff against the default look as `fill … replace` boxes, each ≤ 32 768 blocks,
  - **`props(look)`**: per-fight display entities with fixed UUIDs (spawned at fight start for the default look, by the
    look call for the others; killed by cleanup; tags `rlk_mb_arena_prop rlk_mb_ar_<short>`, never `rlk_room` /
    `rlk_mb_aux`),
  - constants.
- Generated per arena: `F:mboss/arena/<aid>/{ensure, build, rebuild, clear}` (multi-tick build in ≤ 40 slices, per-arena
  stamp key `<aid>@<ver>` + sentinel) and **`look/<look>`** for every look (one slice per tick, a done flag, the current look
  stored in `rlk:mboss arena.<aid>.look`; the stamp itself never carries the look, so a look change never triggers a
  rebuild).
- `ensure` and the **default-look restore start from `prep`** (the entrance build); `cb/start` waits for a running build or
  restore (the gate shows "준비 중", its own timeout instead of the 3 × 10 t retry).
- Per-arena constants behind `#mbAr` (`ar/oob`, `ar/sweep`, `ar/clamp`, `ar/leash`, `ar/tp_in`, …); forceload on demand.
- No `ap_cave`, no `mboss/ar/switch` (AZL AP-2).
- cproto test: a two-look swap (slice count, done flag, restore at the next `prep`, props per look).
- Apep use: `ap_oasis` with looks `withered` / `lush`, swapped inside the CS white-out (≤ 24 slices over 40 t), restored for
  the next fight; lush water tiles / lily pads / bulb flowers as per-fight props (plan §4).

### FN-4 Phase pools
- `#mbTot` = the body's `mhpM` right after `mob/level_apply` at spawn.
- `mboss/repool {pct}`: `mhpM = mhpC = #mbTot × pct / 100`, the bar ramps over 30 t; remembers `#mbPoolPct`.
- `test/level` re-runs `level_apply`, updates `#mbTot` and re-applies `#mbPoolPct`.
- Apep use: 53 % at spawn, 47 % inside the CS white-out (two bars, as Genshin).

### FN-5 Floor
- The module `incoming` sets `#mbFloor mb` (absolute HP) and calls `mboss/floor`: clamps `#dmg` so `mhpC − #dmg ≥ #mbFloor`,
  sets `#mbFloorHit 1` when it clamped; true damage bypasses (tests).
- Apep use: the 1 % floor of the phase-1 pool; reaching it queues the T1 transition.

### FN-6 Title
- `mboss/title {title,sub,color}` writes `cur.title` / `cur.sub` / the name colour; the bars redraw.
- Apep use: 종막 오아시스 파수꾼 / 긴 「종말」을 걸쳐 진화한 생명 → 「오아시스의 심장」 → 기원 오아시스 파수꾼 /
  「불씨」를 받아 소생한 생명.

### FN-7 Per-element RES per entity
- The core writes `mbRes0..8` on the body at spawn from the registry `res` (`"*"` = the rest).
- The module may write `mbRes0..8` on any aux and set `mbResSet 1`.
- A generic pre-step `mres = mbRes<#elem>` runs before the module `on_hit` (body) and before `aux_hit` (only aux with
  `mbResSet 1`, so the Guardian's stars and every existing aux stay byte-identical). Reactions and DoTs use their element.
- Mid-bosses without `res` keep `mres 0` (the butterfly "equal damage for every element" test stays green).
- Apep use: the body Dendro 30 / rest 10; organisms Dendro 20 / rest 10. Aux fallback if missing: `#auxRes 10` + ×8/9 on
  Dendro in `aux_hit`.

### FN-8 Hit proxies
- ≤ 16 interaction proxies per boss, generated by the framework from the rig manifest: per-tick px tracks, **state sets
  with any names the manifest declares** (Apep: `p1`, `p3u`, `p3c`, `burrowed`, `aloft`, `parked`, `dead`), the
  framework compiles `px/follow` and `px/state/<name>` (stub and real manifests share the schema).
- Tags `rlk_room rlk_mb_aux rlk_mob boss rlk_mb_px rlk_mb_px_<name>`; never `rlk_zmob` / `rlk_mshield`; **proxies in a
  disabled state lose `rlk_mob`**.
- Proxy hit → body: one line at the top of `combat/apply` → `mboss/px/hit` (de-dupe on gametime + `#atkSeq`; `#atkSeq`
  incremented at all call sites incl. `element/rx_run` and `element/lunar/hit`), then `combat/apply` as the body at the
  proxy's position; `px/dup` for direct body hits; proxy clicks polled by the framework every tick (cleared while paused);
  the minimap excludes `rlk_mb_px`; Navia pellets count on the body.
- A module hook for the hit flash per part group (`flash/<group>` from the proxy name).
- Apep use: 11 proxies per stance with rebinding (plan R7).

### FN-9 Lose
- `mboss/cb/lose`: an objective loss → the normal death path (`curHealth 0` → `player/die`; Ronova's revive applies); in
  test mode → `test/defeat`. Tested on cproto.
- Apep use: the second Heart failure.

### FN-10 Tests and harness
- `test/chapter {id}`, `test/chapter_ch {id,ch}`; chapter wording in `test/won` / `test/defeat`.
- Generic `test_chapter.py` on cproto (route, gate, ensure, looks, kill, lose, title, repool, music, cleanup / forceload,
  proxies, RES, floors, a Raiden smoke case).
- The real-engine harness (S1-HARN) with: passengers (`ride`, `execute on passengers | vehicle`), `rotate`, a block map with
  `fill` / `setblock` and collision for the agent, a per-tick command counter, level / pool parameters (L18) and a Lv15
  player, interaction entities.
- Apep use: its suites run on the same harness (`S:ap/tests/apsim.py`).

### FN-11 Chapter death and rewards
- `mboss/cb/won` (gold absorb in the arena box, `cleanup_fight`, `tp_out`, `k_chapter` on a kill, the gate back otherwise,
  test-mode links); `mboss/cb/body` without `miniboss`; `combat/gold_drop` `tag=miniboss` edit (×15 gold × chapter,
  2 sapphires); XP from the registry.

### FN-12 Cleanup paths
- `#mbMode` / `#cbForce` resets, music stop, arena forceload released and `mboss/arena/<aid>/clear` on `cb/won`, cleanup,
  `room/remove`, `uninstall`, wipe.

### FN-13 Body burrow support
- `rlk_mb_noshield` gate in `mob/shield_ensure`; the body husk's scale option (0.1) while hidden; the body never enters
  blocks.
- Apep use: every short burrow (P1 잠복 돌진, 발광, relocate, T1 sink, Q1, Q3s). For the ≈ 100 s of phase 2 Apep also
  parks the body 30 b above the arena centre (module code: `#mbNoLeash 1` re-set by the module reload, since the core
  reload resets it).

---------------------------------------------------------------------------------------------------

## SHOULD (Apep has a fallback, but the shared version is cleaner)

### FN-14 `hz/mask` with a safe group — mask accepted, **safe group NEW**
- Hazard kind 6 (AZ N4): hits a player whose feet are not within `R0` (+ 0.3 b margin, a **horizontal score test**) of any
  `rlk_mb_hzsafe` marker of the hazard's safe group.
- **NEW: `#hzSafeG N`** on the hazard (stored `mbHzSG`) and `mbHzSG` on the safe markers; default 0 = "the hazard's own id"
  (AZ's design), so one set of dome markers can serve several hazards (Apep's field ticks and its blast).
- Works with `#hzRearm`, `#hzAct` (active window), `#hzNoDodge`, `#hzNR`, `#hzQuiet`, volley groups and the height band;
  the fairness agent reads the markers.
- Apep use: 종말의 여파 (3 domes r 4.5; ticks with re-arm 15 from t80; the blast with a 20 t window).
- Fallback: a `dmg 0` mask for the agent + the module's horizontal dome test calling `pl_dot` on the tick and blast ticks.

### FN-15 Hazards in ‰ of the player's max HP — **NEW**
- Options `#hzPm N` (‰ of max HP; default 0 = off) and `#hzLethal 0|1` (default 1). With `#hzPm > 0`, `hz/hurt` calls
  `mboss/pl_dot` (FN-16) with `#mbDotPct = N`, `#mbDotEl` = the hazard element, `#mbDotLethal = #hzLethal`, `#mbNoRx` from
  `mbHzNR`, i-frames per `#hzNoDodge`, instead of `mboss/hurt`. Same shape optional on pj (`#pjPm`), not needed by Apep.
- Apep use: 종말의 여파 ticks 30 ‰ (non-lethal) and the blast 800 ‰ (lethal; non-lethal on the first cast of each fight).
- Fallback: as FN-14.

### FN-16 `mboss/pl_dot` — accepted; lethal flag and cine refusal explicit
- `#mbDotPct` = **‰ of max HP** (the AZL AP-3 name; document the unit), `#mbDotEl`, `#mbDotLethal 0|1` (0 floors at 1 HP).
- I-frames ignored (zeroed as in `hurt_nd`); guard + element shields absorb as in `hurt_elem` (no defence); refused while
  dead, reviving, in a selection screen, or while `#mbCine 1`.
- Apep use: FN-15's hazards; the 「소생 실패」 wither (250 ‰, non-lethal). Fallback: `mboss/hurt` with a large `#mbHitPct`
  and `#mbNoDodge 1` (level-dependent, worse).

### FN-17 No player-side reaction — accepted
- Per-hazard `#hzNR` (stored `mbHzNR`), per-pj `#pjNR` (`mbPjNR`), and a one-shot `#mbNoRx 1` for direct calls
  (`pl_dot`, `hurt`): skips `element/player_hit`, keeps the element colour of the number.
- Apep use: the 종말의 여파 hits and the failure wither.

### FN-18 `#pjNoDodge` — accepted
- Per-prop `mbPjND`, copied in `pj/launch`, honoured in `pj/hit` like `#hzNoDodge` (around `mboss/hurt`, reset after).
- Apep use: the homing thorn wheels (0.5 b/t, 8°/t, life 22 t, coefficient 0.15).
- Fallback: a visual pj + a follower `#hzNoDodge` disc re-aimed onto it every module tick (1 t lag).

### FN-19 `mboss/mv/lockv {lead}` — accepted; **dash filter and sprint cap NEW**
- A ring buffer of the player body's position over the last 6 t; marker at pos + v × lead, clamped to the walk disc − 0.7;
  `|v|` and the unit velocity stored.
- **NEW**: samples taken while `dashMoveT > 0` are ignored, and the measured speed is capped at sprint (0.28 b/t), so a
  dash is never projected 10 b ahead into the next landing (Apep fairness review F7).
- Apep use: 잠복 돌진 (lead 10), 생명의 손 (6), 이동 돌진 (10), 증폭의 풀 shell 2 (8). Fallback: a module copy.

### FN-20 `mboss/mv/local` — accepted
- The player's position in the anchor frame → `#mvF` / `#mvS` (tenths of a block).
- Apep use: FRONT / SIDE / UNDER / BACK zones and the BACK dwell. Fallback: a module copy.

### FN-21 `mboss/push/capsule` + `mboss/push/ring` — accepted
- Capsules per state from the rig manifest; a horizontal, collision-checked push (no velocity, no FOV effect); never in
  hidden or moving states or during a mask round.
- `push/ring {r0,r1}`: a push-only ring (no damage) for cut-scenes.
- Apep use: P1 / P3-crawl capsules (sac + thorax column, hips) and the P3 robe-stem capsule; the CS push of players within
  8 b of the centre out to 12 b.

### FN-22 `mboss/cine/start|end` — accepted
- `#mbCine 1` refuses boss hits on the player (`mboss/hurt`, `pl_dot`, hazards, pj) and freezes the AI clock; bars stay;
  every cleanup path resets it.
- Apep use: T1, the CS, the death.

### FN-23 Music — accepted
- Registry `"music": {"<ph>": {"ev": "<sound event>", "len": N}}`; `mboss/music/set {ph}` stops the previous track and plays
  `ev` at the player in the `record` category, looped by `len` (0 = once); vanilla music suppressed while it plays; stopped
  on every path. Stereo `music.*` events (AZL F17).
- Apep use: phases 1 / 2 / 3 (`music.overworld.deep_dark`, `music.nether.soul_sand_valley`, `music.overworld.lush_caves`;
  plan Q17), set at the fight start, T1 t106 and CS t132.

### FN-24 bossui options — `#buHpCol` accepted, **`#buNoNum` NEW**
- `#buHpCol` (the bar's fill colour; default red) and **`#buNoNum 1`** (hide the "hp/max" text), both default off.
- Apep use: the Heart progress bar in gold `#EDCF63` with `#buMax 1000` and no "270/1000" text.
- Fallback: `#buMax 100` (reads as a percent) on the red bar.

### FN-25 RIGLIB — accepted; **park NEW**
- One stage (`wip/riglib` from M0, one owner, merged into main early): `tools/mboss_shape_lib.mjs` (promoted from
  `azhdaha_shape.mjs`, the old file kept as a re-export shim), per-part `tol.tp`, the px track compiler, culling `width` /
  `height` and `view_range` per rig, `follow_y` sink offsets, the static-anchor follow skip, per-state follow lists, the
  shadow helper; identity proofs of the other rigs on M0.
- **NEW: park support**: a parked flag that makes the generated `rig/tick` skip follow keys and makes the respawn check keep
  the parts at scale 0.
- Apep use: the whole rig (plan R16, R19, R20); park for the ≈ 100 s of phase 2.
- Fallback: until RIGLIB lands, Apep keeps a temporary `apep_shape.mjs` copy; park can be built in Apep's own builder
  output. Apep never edits a shared rig library.

### FN-26 Barrier safety sweep — accepted; **span table NEW**
- `mboss/arena/<aid>/sweep_barrier`, generated from a **per-row span table** limited to r ≤ walk − 0.5 and the y band
  floor + 1 … floor + 2. **Never rectangular quadrant fills**: those reach r 26-37 near the diagonals and would delete an
  arena's own rim barrier (r 27-28), which `ensure` never repairs.
- Called by `cb/won`, cleanup, `room/remove`; modules may call it.
- Apep use: the safety net behind the 둥지 walls (the module clears its own recorded blocks first).
- Fallback: module-only recorded clears in every exit hook.

### FN-27 Budget probes and gates — accepted; **two-boss atlas gate NEW**
- The RP build prints the stitched items-atlas size. Gates: Azhdaha alone ≤ 15.5 M px (AZL F36); **both chapter bosses
  ≤ 15.8 M custom px** (measured today: 12.74 M custom; Azhdaha ≈ 0.95 rig + ≤ 0.6 kit; Apep ≤ 0.9 rig + ≤ 0.2 objects +
  ≤ 0.35 kit).
- The command-per-tick probe (≤ 3000 per tick on the worst timelines; Apep's phase 2 at the organism cap ≤ 800 average) and
  the arena entity count (≤ 400) (AZL F35).
- If the two-boss gate fails, the Raiden `fxg` reclaim (AZL F36's open question) is decided before Apep's integration.

### FN-28 Font allocation — accepted
- `rlk:mboss_ap` at U+E900-E9FF; the font checks list `hud`, `bossbar`, `minimap`, `mboss_gd`, `mboss_bf`, `mboss_fg`,
  `mboss_az`, `mboss_ap`.

---------------------------------------------------------------------------------------------------

## CAN

### FN-29 Aux presentation options — **NEW**
- `#auxShW` / `#auxShH` (tenths): the click-shield size for this aux, read by `mob/shield_ensure` when set (default
  1.2 × 2.2 unchanged). `#auxHbY` (tenths): the HP-bar y offset at `mob/hb_spawn`.
- Apep use: organisms from 1.15 b basics to the 4.4 b 수호 spire.
- Fallback: `data merge` the `rlk_mshield` after its first tick and the `rlk_hb_*` passengers after spawn.

### FN-30 `mboss/mv/step_flat {spd}` — **NEW**
- A cheap ground stepper (≈ 5 commands): face the target, `tp ^ ^ ^v`, snap y to the arena floor, clamp to the walk disc.
- Apep use: up to 6 organisms walking every tick. Fallback: a module copy.

### FN-31 Hit / dodge events — accepted (AZ N7)
- `mboss/hurt` sets `#mbHitEv`, `#mbHitEl`, `#mbHitSh` on a landed hit and `#mbDodgeEv` on a dodged one (pj too).
- Apep use: the first-hit hints (homing wheels, tail). Fallback: module counters.

### FN-32 Fractional pj speeds — not needed
- `pj/tick` moves (spd·4 + 9) / 10 steps of 0.25 b; Apep uses only speeds that are multiples of 0.25 b/t (wheels 0.75 /
  0.5, bolts 0.75). Listed so nobody builds it for Apep.

---------------------------------------------------------------------------------------------------

## Not requested (Apep module code, plan §3.3)

The organism runtime and the six kinds; the Heart objective and the revival stage; the 둥지 walls (the module records and
clears its own barrier blocks); the dome placement and the option-b dome test; the phase-2 body park position; the two
forms and the two stances; chains and the 종말의 여파 schedule; the swept-wedge helper `api.wedges()` over `hz/sector`;
the arena theme content (`tools/mboss_arena_ap_oasis.py`).

## Dropped from Apep's draft list

- Passengers on aux husks (already true: every aux carries its 5 HP-bar passengers).
- `ap_cave` and `mboss/ar/switch` (phase 2 is played on the same field).
- "The core clamps after the module `incoming`" (Apep uses AZ's "`incoming` calls `mboss/floor`").
- The names `#mbDotPm`, `title {text,color,sub}`, the music list schema (AZL AP-3 settled the names above).

## What Apep's integration checks on AZ-CM (before AP-CORE starts)

| check | how |
|---|---|
| every MUST item exists with these names | `check_refs` + a grep list in `S:ap/tests/fw_needs_check.py` |
| cproto passes the generic suites | `test_chapter.py`, `test_px.py`, `test_fw_az.py` on main |
| defaults are byte-identical | `ident.py` (Guardian / butterfly / fieldgen / proto) |
| SHOULD items present or missing | the same script prints which fallbacks AP-CORE must enable, and which gaps go to AP-FW |
