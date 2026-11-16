# AZ-CM day-0 contract: the chapter-boss mode (`cm.md`)

Owner: **S1-CM** (`wip/az-cm` from M0). Readers: S1-MOD, S1-ARENA, S1-FX, R3, S2, I1-WIRE, Apep (adopts it as is).
Binding inputs: `S:az/plan.md` §1.2-§1.7, §3.3, §3.6, §4.9, §7, §8, §9 (defaults) and `S:az/plan_ledger.md`.
Grounded in M0 = `claude/exciting-pascal-ek1vuy` @ 99bc097 (`DP` = `/home/user/rlk/roguelike`): `T:build_mboss_core.py`,
`T:mboss_lib.py`, `T:mboss_registry.json`, `T:build_mboss_arena.py`, `T:check_mboss_pack.py`, `T:build_bossbar.py`, the
hand-written `F:` files named in §16 (line numbers are M0's). Names in this file are final; a change needs a numbered
change note in `S:az/plan.md` and an entry in §19 here.

Shorthand (plan §0): `S:` scratchpad, `DP` the datapack root, `T:` = `DP/tools/`, `F:x` = `DP/data/rlk/function/x`,
`AZ:x` = `F:mboss/azhdaha/x`. "Generated" = written by a generator, never by hand.

Contents: 0 conventions · 1 files and ownership · 2 registry · 3 storage · 4 scores · 5 chapter lifecycle ·
6 per-arena functions and builds · 7 pools, floor, title · 8 per-element RES · 9 hit proxies · 10 music · 11 bars ·
12 cleanup · 13 player-status and motion helpers · 14 UUIDs · 15 tests · 16 shared-edit table · 17 Apep coverage and the
Apep hook list · 18 what S1-CM delivers when · 19 decisions · 20 change notes (CM fix round) · 21 open items ·
22 change notes (AP-FW, `wip/cm-ap`).

---------------------------------------------------------------------------------------------------

## 0. Conventions (unchanged from the mid-boss framework unless stated)

- Units at the runtime boundary: distances in **tenths of a block** (`r:50` = 5 b), times in ticks (20/s), damage as
  **% of the boss base hit** (`dmg:140` = 1.4 × `atk`, raw = ⌊atk × pct × dmgMul / 10000⌋, `mboss/hurt`), elements in
  `#elem` numbering **0 physical 1 Pyro 2 Hydro 3 Electro 4 Cryo 5 Geo 6 Anemo 7 Dendro 8 Void**. New in this contract:
  **‰ of the player's max HP** (`maxHealth`) for `pl_dot`; **milliblocks** (mb, 1/1000 b) for `mv/local` and `mv/lockv`
  outputs (the `hz/hit` projection unit).
- Body frame: `f` = forward along the anchor yaw (+ toward the head), `s` = sideways (+ the boss's left), from the anchor
  (the body husk on the floor). Minecraft local coordinates `^s ^y ^f` are exactly this frame.
- Every framework fake player lives in objective `mb` unless another objective is named (`tmp`, `bu`, `room`).
- Python helpers (`mboss_lib`, imported as `L`) take blocks / degrees and emit tenths.
- Mid-boss behaviour is unchanged: Guardian, butterfly, fieldgen, proto never see a chapter field; their module outputs
  and the plaza arena output stay byte-identical to M0 (`ident.py`).

## 1. Files, ownership, generator order

### 1.1 Files S1-CM owns (writes)

| file | role |
|---|---|
| `T:build_mboss_core.py` | framework generator: everything of §5-§13 under `F:mboss/*.mcfunction` and `F:mboss/{d,hz,pj,pull,mv,aux,line,test,box,cb,ar,px,music,push,cine}/**` (`L.Out` owned dirs extended by `cb ar px music push cine`) |
| `T:mboss_lib.py` | registry loader + new helpers (§2.5, §13.10) |
| `T:mboss_registry.json` | schema v2 (§2), the `cproto` entry, the `azhdaha` entry (§2.4); later edits only by request |
| `T:build_mboss_arena.py` | the plaza (legacy, byte-identical) + every `arenas{}` entry: `F:mboss/arena/**` (§6.3) |
| `T:mboss_arena_cp_test.py` | the theme of cproto's test arena `cp_test` (theme.md §7) |
| `T:build_cboss_rooms.py` | domain-entrance rooms: `F:room/cboss/**` (§5.3) |
| `T:build_mboss_cproto.py` | the chapter proto boss `F:mboss/cproto/**` + `T:mboss_cproto_rig_manifest.json` (static stub manifest, schema v1) |
| `T:check_mboss_pack.py` | + chapter hooks, `creg`, arenas, px families (§15.4) |
| `T:build_bossbar.py` | `#buHpCol`, `#buNoNum` (§11) |
| hand-written shared files | only the edits of §16 |
| `S:az/tests_cm/**` | `test_chapter.py`, `test_px.py`, `test_fw_az.py`, `run_all.sh`, `gen_check.py`, `ident.py`, `vcheck.py`, `baseline/` |
| `S:az/contract/{cm,theme}.md` | this file; theme.md with S1-ARENA |
| README "챕터 보스" | the chapter-mode section and the shared-edit table (§16) |

S1-CM must not touch: the Guardian / butterfly / fieldgen / proto module generators and outputs, any kit, any rig file,
`T:mboss_arena_az_cavern.py` (S1-ARENA), `T:mboss_azhdaha/**` (S1-MOD).

### 1.2 Generator order (README "등록 · 모듈", plan §1.5)

core → arena (plaza, cp_test, az_cavern: every `arenas{}` entry; an entry whose theme module is missing gets the stub
function set of §6.3, never nothing) → `build_cboss_rooms.py` →
proto → cproto → rig generators (Guardian, butterfly, fieldgen, azhdaha) → guardian → bf kit → butterfly → fg kit →
fieldgen → az kit → azhdaha → `check_mboss_pack.py`. Every generator writes and cleans only its own paths; a second run
and the reverse order give the same bytes (`gen_check.py`).

Cross-reads (data only, no imports of other stages' code): the core reads every px boss's manifest (§9.2) and every
arena's registry entry; the arena generator and `build_cboss_rooms.py` import theme modules (theme.md §1).
The manifests the core reads are written by generators that run **after** it (rig generators, S1-MOD's `stub_rig.py`):
the core always reads the committed file, every commit that changes a manifest also commits the regenerated core
outputs (`F:mboss/px/**`), and `gen_check.py`'s second run fails on a stale `px` output.

## 2. Registry schema v2 (`T:mboss_registry.json`)

### 2.1 Top level

| key | type | rule |
|---|---|---|
| `_doc` | [str] | updated by S1-CM for every new field |
| `arena` | object | **unchanged** (the plaza: theme `plaza`, ver 2, cx 200 cy 201 cz 8, r 22, walk 21, safe 19, start). Read by the fieldgen / butterfly / guardian / proto generators; never extended |
| `arenas` | {aid: object} | **new**: every non-plaza arena (§2.3). `plaza` is not a key here |
| `boss` | [object] | mid-boss and chapter-boss entries (§2.2) |

### 2.2 Boss entry fields

Existing fields keep their meaning (`id n enabled w minCh maxCh name sub color el hp xp atk lvAdd dmgMul goldMul sap picks
scale hit intro death deathSnd icon start`). New fields (all optional for mid-bosses; defaults in brackets):

| field | type [default] | meaning |
|---|---|---|
| `kind` | `"mid"` / `"chapter"` [`"mid"`] | chapter entries go to `creg[]` / `cbyid` (§3.1), never to `reg[]` / `byid`; the roll never sees them |
| `ch` | [int] [`[]`] | chapters this boss ends (routing, §5.1). `[]` = never routed (cproto) |
| `route` | bool [`true`] | false = generated routing skips it (only `#cbForce` in a test reaches it). Azhdaha **false until I2** |
| `arena` | aid [`"plaza"`] | the arena id: `"plaza"` or a key of `arenas` |
| `music` | {ph: {ev: str, len: int}} [none] | §10. `ph` = "1".."9" (string keys); `ev` a `minecraft:music.*` sound event; `len` ticks (0 = play once) |
| `res` | {el: int} [none] | per-element RES % (§8): keys `"0"`..`"8"` and `"*"` (default for the rest). None = no RES scores (mid-bosses) |
| `phases` | [int] [`[100]`] | pool split in % of `#mbTot`; `phases[0]` applied at spawn (§7.1) |
| `px` | bool [`false`] | hit-proxy boss (§9): proxies from the manifest, `rlk_mb_big` body (`px/dup`) |
| `pxBase` | int [`65`] | low byte of the first proxy UUID inside the boss's UUID block (§14); at most 16 proxies (`pxBase` … `pxBase + 15`) |
| `shield` | bool [`not px`] | false = the body carries `rlk_mb_noshield` from spawn (no click shield in any state; Azhdaha, cproto). Apep sets `true` (torso shield `hit` + proxies, plan FN-8 / FN-13). Modules may add / remove `rlk_mb_noshield` at runtime; the click shield of a tagged body dies on the next `combat/mshield_tick` (no `rlk_msync`) |
| `hit` | {w,h} [`{w:1.0,h:1.0}` when `shield` is false] | M0 field, **required by M0's `snbt_entry`**; S1-CM gives it this default (Azhdaha's plan §1.6 entry has none) |
| `theme` | str | **informational only** on a boss entry (plan §1.6 lists it); the arena's own `theme` rules |

Validation (`L.load_registry`, asserts): `kind` in {mid, chapter}; a chapter entry has `goldMul 1`, `sap 0`, `picks 0`,
`w 0`, an `arena` that exists, `minCh`/`maxCh` covering `ch`; `n` unique across mid and chapter entries; `px:true` only
on chapter entries; `shield:true` needs `hit`; `res` keys ⊂ {"0".."8","*"}; `sum(phases)` ≤ 100; no chapter c is
claimed by two enabled `route:true` entries; `icon` is an object `{item, model}` (M0's `snbt_entry` reads
`icon["item"]` / `icon["model"]` and indexes `minCh maxCh name sub color el` directly, so every entry carries them).

### 2.3 Arena entry (`arenas.<aid>`)

| field | type | meaning |
|---|---|---|
| `n` | int ≥ 1, unique, never reused | arena number = `#mbAr` (the plaza is 0) |
| `theme` | str | the theme module `T:mboss_arena_<theme>.py` (theme.md) |
| `ver` | int | build version; part of the stamp |
| `cx cy cz` | int | centre (a block **corner**, as the plaza) and stand height (floor blocks at `cy − 1`) |
| `r`, `walk`, `safe` | number | outer radius, walkable radius, body leash / ground-target clamp radius (blocks) |
| `start` | {x,y,z,yaw,pitch} | arrival (doubles / floats as the plaza's) |
| `box` | {x0,y0,z0,x1,y1,z1} | inclusive block box: built, cleared, swept, forceloaded |
| `looks` | [str] | look names, `looks[0]` = the default look restored by `ensure` |
| `oob` | {y0,y1} [`{cy−3, cy+16}`] | out-of-bounds band (feet inside y0..y1 and within `walk + 1.5` = inside) |
| `sweep` | {y0,y1} [none] | when present, `cb/won`, `mboss/cleanup` and `cb/remove` run `arena/<aid>/sweep` with it (module barrier walls; Apep: `{201,202}`); Azhdaha has none |

Entries at day 0:

```json
"arenas": {
  "az_cavern": {"n": 1, "theme": "az_cavern", "ver": 1, "cx": 320, "cy": 201, "cz": 8, "r": 33, "walk": 28, "safe": 26,
                "start": {"x": 320.5, "y": 201.0, "z": 34.5, "yaw": 180.0, "pitch": 0.0},
                "box": {"x0": 280, "y0": 190, "z0": -32, "x1": 360, "y1": 240, "z1": 48},
                "looks": ["default"], "oob": {"y0": 198, "y1": 237}},
  "cp_test":   {"n": 9, "theme": "cp_test", "ver": 1, "cx": 540, "cy": 201, "cz": 8, "r": 12, "walk": 11, "safe": 9,
                "start": {"x": 540.5, "y": 201.0, "z": 17.5, "yaw": 180.0, "pitch": 0.0},
                "box": {"x0": 524, "y0": 196, "z0": -8, "x1": 556, "y1": 216, "z1": 24},
                "looks": ["plain", "lit"]}
}
```

Apep adds `"ap_oasis"` with `"n": 2` (its plan §3.7 values + `n` + `box` x 396..484, y 190..250, z −36..52).

`mboss_lib.load_registry` rejects a `box` that spans more than 256 chunks (one `forceload add`) or shares a chunk with
another arena's box or with a fixed forceload (`mboss_lib.FIXED_FORCELOADS`: dungeon, lobby, item room, plaza), since
its `fl_off` would release those chunks too (change note 20.16).

### 2.4 Entries written by S1-CM

- `cproto` (n **98**, kind chapter, `ch []`, `route false`, `enabled true` from the commit that adds
  `T:build_mboss_cproto.py` (false before it: an enabled entry without its module fails the pack check), `arena
  "cp_test"`, `px true`, `pxBase 65`, `res {"0":30,"5":30,"*":10}`, `phases [60,40]`, `music {"1":{"ev":"minecraft:
  music.end","len":0},"2":{"ev":"minecraft:music.dragon","len":0}}`, hp 120, xp 20, atk 10, dmgMul 120, goldMul 1,
  sap 0, picks 0, scale 0.1, hit {w 1.0, h 1.0} (never used: no shield), intro 40, death 40, deathSnd false, `w 0`,
  `minCh 1`, `maxCh 99`, `lvAdd 0`, name "시험용 수호자", sub "챕터 보스 틀 점검용", color `#9FC6E8`, el 0, icon
  `{"item": "minecraft:lodestone", "model": "minecraft:lodestone"}` (an object: §2.2 validation)).
- `azhdaha`: exactly plan §1.6 **with `"enabled": false`** on `wip/az-cm` and in AZ-CM on main (no dispatch line, no
  `creg` entry, the pack check passes without the module). **S1-MOD flips it to `true` in its first commit** (the only
  registry line S1-MOD edits; S1-CM never touches that line again). `route` stays false until VERIFY. This departs
  from plan §1.2 R1 / §1.6 (`enabled: true`, "enabled from their first stage") and from §7.3 (S1-MOD edits the
  registry only by request); it needs a numbered plan change note (§19 decision 1). Layout rule (no merge conflicts
  on S1-MOD's daily rebase): the entry's first line holds `id n kind ch route enabled w` (as written in commit 1);
  only S1-MOD (`enabled`, first commit) and VERIFY (`route`) edit that line; S1-CM's later edits of the entry (e.g. the
  measured music `len`, §10) touch other lines only.
- `apep` (n 11) is Apep's; S1-CM leaves a `_doc` line reserving n 11 and arena n 2.

### 2.5 `mboss_lib` helpers (new)

| helper | returns |
|---|---|
| `L.mid_bosses(reg)` / `L.chapter_bosses(reg)` | enabled entries of that kind (`L.enabled_bosses` keeps returning both) |
| `L.arena_of(b, reg)` | the arena dict of boss `b` with `aid` and `n` added; `plaza` → `reg['arena']` + `aid:'plaza'`, `n:0`, `box` = the legacy box (x 176..223, y 190..240, z −16..31) |
| `L.arenas(reg)` | `[(aid, dict)]`, plaza first, then by `n` |
| `L.theme_module(theme)` | `importlib.import_module('mboss_arena_' + theme)` (tools/ on sys.path), or `None` when the file is missing |
| `L.CHAPTER_HOOKS` | `['prep']` (added to the 17 `L.HOOKS` for chapter entries) |

## 3. Runtime storage (`rlk:mboss`)

### 3.1 Registry

| path | shape | written by |
|---|---|---|
| `reg[]`, `byid.<id>{n}`, `#mbN`, `#mbRoll` | unchanged: **mid-boss entries only** | `F:mboss/register` |
| `creg[]` | chapter entries as SNBT records (same record as `reg[]` + the fields below) | `register` |
| `cbyid.<id>` | the full record of chapter boss `<id>` (`cb/start` copies it into `cur`) | `register` |
| `#mbCN mb` | number of enabled chapter bosses | `register` |

Record fields added by `snbt_entry` (every entry, mid-boss defaults in brackets): `kind:"chapter"|"mid"`, `ch:[I;..]`,
`route:1b|0b`, `arena:"<aid>"` [`"plaza"`], `ar:<n>` [0], `px:1b|0b` [0b], `pxBase:<int>` [65], `shield:1b|0b` [1b],
`hit` (the default of §2.2 when absent), `res:[I;r0,..,r8]` (only
when the entry has `res`; missing keys = `"*"` or 0), `phases:[I;..]` [`[I;100]`], `music:{"1":{ev:"..",len:N},..}`
(only when present). `start` comes from the boss's arena (`L.arena_of`) unless the entry has its own.
The generated hook dispatchers `F:mboss/d/<hook>` (the 17 `L.HOOKS`) get one line per enabled chapter boss as for the
mid-bosses (`#mbId` = n; `d/incoming` routes a chapter boss through `cb/inc/<id>`, §7.2); `prep` has no `d/` dispatcher
(only `cb/prep`, §5.3). Disabled entries get no line anywhere.

### 3.2 Per fight

| path | shape | meaning |
|---|---|---|
| `cur` | the record (mid: from the roll; chapter: from `cbyid`) | as today; `cur.title` / `cur.sub` rewritten by `mboss/title` (§7.3) |
| `ret`, `sub[]`, `extra[]`, `aura[]`, `ln` | unchanged | |
| `px` | `{set:"<state>", o:{<p>_x:d,<p>_z:d,<p>_y:d,...}, top:{<p>:f}}` | proxy runtime (§9); removed by `cleanup_fight` |
| `push[]` | `[{f0:i,f1:i,hw:i,px:"<proxy>",top:i}]` tenths | capsules of the current proxy state (§13.5) |
| `mus` | `{ph:i, ev:"..", len:i}` | the playing track (§10) |
| `lv[]` | 6 × `{x:i,z:i}` mb | the `lockv` ring buffer (§13.1) |

### 3.3 Per boss map / run

| path | shape | lifetime |
|---|---|---|
| `cprep.<id>` | `{gate:{item,model,item2,model2,l1,l2,l3,n}, title:<text>, sub:<text>, ...module keys}` | written by `<id>/prep` at entrance build; **survives fights, cancels, aborts and /reload**; removed by a new `prep` of the same id (the framework clears it first), `cb/run_reset` (run start / end, test end) and `uninstall` |
| `built_<aid>` | `"<aid>@<ver>:<look>"` | arena stamp (§6.4); removed by `arena/<aid>/clear`, `rebuild`, uninstall |
| `look_<aid>` | `"<look>"` | the look the arena shows, or the one the running job turns it into (§6.4, change note 22.3): set when a build (`looks[0]`) or a look job starts, kept by `done`; removed by `arena/abort` (of that arena's job), `clear`, uninstall; a stub arena's `ensure` writes `looks[0]` |
| `arjob` | `{aid:"..", kind:"build"|"look"|"verify", look:"..", i:int, n:int, wait:int}` | the one running sliced arena job (§6.5) |
| `tlast` | `{id:"..", ch:i, cb:1b|0b}` | test replay (adds `cb`) |
| `cbpeek` | `{id:"..", name:"..", color:".."}` | optional: who the next boss map routes to (§5.10) |

`cprep.<id>.gate` keys (all required): `item`, `model` (icon 1: an item id + an `item_model`), `item2`, `model2` (icon 2),
`l1`, `l2`, `l3` (SNBT text components, a compound or a list of compounds, substituted verbatim into the label),
`n` (the registry n). `title` / `sub`: text components for the gate-click title (`interpret:true`).
A module keeps any per-boss-map state it needs under `cprep.<id>.*` (Azhdaha: `cprep.azhdaha.pair {leg,tail}`, s2.md §4).
A test death does **not** keep `cprep`: M0's `test/defeat` runs `test/end` → `run/end` (→ `cb/run_reset`) and the
replay link builds a new boss map (a new `prep`, a new roll). Plan §4.1's "kept for retries (abort, a test death)"
therefore holds for aborts / cancels only; tests force a pair with `test/pattern 90-93` (needs a plan change note).

## 4. Scores

### 4.1 Fight-level fake players (`mb` unless stated). New in AZ-CM

| name | values | set by | meaning |
|---|---|---|---|
| `#mbMode` | 0 / 1 | `fight_vars` from `cur.kind` | 1 = chapter fight; reset in `cleanup_fight` |
| `#mbAr` | arena n | `fight_vars` from `cur.ar` | per-arena dispatch (§6.1) |
| `#mbArW10 #mbArS10` | tenths | `fight_vars` | the fight arena's walk / safe radius (hz/full, lockv clamp) |
| `#mbPx` | 0 / 1 | `fight_vars` from `cur.px` | proxies on |
| `#mbArBuild` | slices left, 0 = idle | arena jobs (§6.5) | ≥ 1 while a job runs or waits for chunks |
| `#cbForce` | registry n / 0 | `test/chapter*` | honoured only while `#mbTest 1`; reset by `cb/run_reset`, `test/stop`, `test/defeat`, `test/won` after a chapter fight (`test/cwon`) and `test/start_ch` (change note 20.1) |
| `#cbAuto` | 0 / 1 | `test/chapter*` | press the gate as soon as the arena is built (§5.9); cleared by every gate press (`cb/g/<id>`), the resets of `#cbForce` (change notes 20.1, 20.3) |
| `#mbTot` | HP | `cb/start` (and `test/level`) | the body's full `mhpM` at spawn (before any split) |
| `#mbPoolPct` | 1..100 [100] | `mboss/repool` | last applied split (re-applied by `test/level`) |
| `#mbRamp` | 0..30 | `repool` | bar refill countdown |
| `#mbFloor` | HP ≥ 0 [0] | **the module** | absolute HP floor; 0 = none (§7.2) |
| `#mbFloorRaw` | dmg | `mboss/floor` | the last unclamped `#dmg` |
| `#mbFloorHit` | 0 / 1 | `mboss/floor` | a hit with `mhpC − raw ≤ #mbFloor` (module clears) |
| `#mbCine` | 0 / 1 | `cine/start|end` | boss hits on the player refused (§13.7) |
| `#mbPushOn` | 0 / 1 | **the module, every tick** | per-tick request (cleared at the start of every chapter-fight world tick by `mboss/world_cm_pre`, before `mv/all` and `body_tick`; change note 20.6) |
| `#mbMusPh #mbMusT #mbMusLen` | | `music/*` | §10 |
| `#mbHitEv #mbHitEl #mbHitSh #mbHitRA #mbHitSrc` | | `mboss/hurt` | §13.3 |
| `#mbDodgeEv #mbDodgeOk` | | `mboss/hurt` | §13.3 |
| `#mbDotPct #mbDotEl #mbDotLethal #mbDotDmg` | | caller / `pl_dot` | §13.4 |
| `#mbNoRx` | 0 / 1 one-shot | caller | no player-side reaction for the next direct `mboss/hurt` (§13.4) |
| `#mbNRNow` | 0 / 1 | `mboss/hurt` (around the call) | read by `F:player/take_damage` |
| `#mbLf #mbLs` | mb | `mv/local` | §13.2 |
| `#mbVx #mbVz #mbV` | mb/t | `mv/lockv` | §13.1 |
| `#mbQi` | 0..5 | `mboss/main` | lockv ring index (buffer in `lv[]`) |
| `#mbPart #mbPartGT` | proxy index / gametime | `px/hit` | the last proxy hit (0 for a direct body hit) |
| `#pxGT #pxSeq #pxIn` | | `px/hit`, `px/dup` | proxy de-dupe (§9.6) |
| `#mbLost` | 0 / 1 | `cb/lose` | §5.8; reset to 0 by `fight_vars` and `cleanup_fight` (a module that sees a living player with `#mbLost 1` knows a revive followed the lose, Apep §3.4) |
| `#cbWait` | retries | `cb/start` | spawn retries while the arena is not ready (§5.5); reset by `cb/gate` (every press), `start_cancel`, `cleanup_fight` and a successful spawn, **not** by `fight_vars` (which `cb/start` runs on every retry, so the 60-retry cap would never fire) |
| `#hzNR #pjNR #pjNoDodge #hzSafeG #hzPm #hzPmL` | one-shot options | caller | §13.4, §13.6, §13.8, §13.11 (`#hzPm` / `#hzPmL` are reset, not set to 0: a mid-boss fight never holds them) |
| `#mbSafeG #mbSafeN` | safe group ≤ −1 / its counter | `hz/safe_new` | §13.6 (change note 22.2) |
| `#auxShW #auxShH #auxHbY` | tenths, one-shot | caller of `aux/spawn` | §13.12 (reset after the spawn) |
| `#auxResEl #auxResElV` | el / % one-shot | caller of `aux/spawn` | §8 (`-1` = none) |
| `#atkSeq tmp` | counter | the five shared lines of §9.6 | attack sequence |
| reserved | `#hzVictim`, `#mbObj` | — | plan R10 (objective entity, not built) |

### 4.2 Per-entity objectives (added to `PER_ENTITY`, created by `mboss/init`, removed by `mboss/uninstall`)

| objective | on | meaning |
|---|---|---|
| `mbRes0` … `mbRes8` | body / aux with `rlk_mb_resel` | RES % per `#elem` |
| `mbHzNR` | hazard marker | 1 = no player-side reaction (from `#hzNR`) |
| `mbHzSG` | hazard marker (kind 6), `rlk_mb_hzsafe` markers | safe group (§13.6) |
| `mbHzPm`, `mbHzPmL` | hazard marker | per mille of the player's max HP / lethal 0-1 (§13.11; only on a hazard made with `#hzPm`) |
| `mbPjND`, `mbPjNR` | projectile prop | no dash dodge / no reaction (from `#pjNoDodge` / `#pjNR`) |
| `mbPart` | proxy interaction | proxy index 1..N (manifest `proxies.layout` order) |

### 4.3 Boss UI (`bu`): `#buHpCol bu`, `#buNoNum bu` (§11).

## 5. Chapter lifecycle (functions, contexts, contracts)

```
room/gen -> room/pick/boss -> mboss/cb/route ---------------------------- (#mapType 8)
   -> mboss/cb/layout {id} -> F:room/cboss/<id>/layout        (zones carry data.boss_id:"<id>", data.cboss:1b)
zone_build (zone 2) -> room/cboss/build -> room/cboss/<id>/build -> mboss/cb/prep (as the zone marker)
   -> mboss/cb/pp/<id>: clear cprep.<id>, ar/<aid>/fl_on, arena/<aid>/ensure (starts the sliced job), <id>/prep
zone_enter (zone 2) -> mboss/cb/enter: zst 3, room/obj/k_cboss (oact 16)
gate click -> room/obj/click oact 16 -> mboss/cb/gate -> room/combat_start, #spawnT 30, title/subtitle/sound
#spawnT 0 -> room/mob_wave (zkind 9) -> room/boss_spawn -> mboss/cb/spawn_route -> mboss/cb/start {id}
   -> shared mboss/start path with #mbMode 1 (no roll, no met, never #mbForce) -> <id>/spawn -> px/spawn -> tp_in -> bars
kill -> combat/apply (heal orb, XP, gold x15 x chapter, 2 sapphires) -> death shell -> death_finish
room/combat_clear (zkind 9, data.cboss) -> mboss/cb/clear -> mboss/cb/won -> killed ? room/obj/k_chapter : k_cboss again
```

### 5.1 Routing (`F:mboss/cb/route`, generated)

Called by `F:room/pick/boss` (its only line). Lines, in order:
1. `execute if score #mbTest mb matches 1 if score #cbForce mb matches 1.. run return run function rlk:mboss/cb/route_force`
2. one line per enabled chapter boss with `route:true` and per chapter c in its `ch`, ascending n:
   `execute if score #chapter room matches <c> run return run function rlk:mboss/cb/layout {id:"<id>"}`
3. `function rlk:room/raiden/layout`

`cb/route_force`: one line per enabled chapter boss (any `route`): `execute if score #cbForce mb matches <n> run return
run function rlk:mboss/cb/layout {id:"<id>"}`, then `function rlk:room/raiden/layout`. **No path sets `#mbForce`.**

`cb/layout {id}` (macro): `$data modify storage rlk:mboss cbl set value "$(id)"`, then one literal line per chapter boss
`execute if data storage rlk:mboss {cbl:"<id>"} run return run function rlk:room/cboss/<id>/layout` (no `$(id)` in a
function name: pack check).

### 5.2 Domain entrance rooms (`T:build_cboss_rooms.py` → `F:room/cboss/**`)

For every enabled chapter boss: `F:room/cboss/<id>/layout` (writes `rlk:room cur` from the theme's
`entrance_layout()['cur']`), `F:room/cboss/<id>/build` (as a zone marker: zone blocks per zid; for the kind-9 zone it ends
with `execute at @s run function rlk:mboss/cb/prep`: M0's `zone_build` callers (`room/gen:22`, `room/door_reveal:4-5`,
the test commands) run it **as** the marker but not **at** it), helper files `F:room/cboss/<id>/z<k>`. Plus the dispatcher `F:room/cboss/build`
(literal lines `execute if data entity @s data{boss_id:"<id>"} run return run function rlk:room/cboss/<id>/build`). Every
zone of a chapter layout carries `boss_id:"<id>"` and `cboss:1b` (so `zone_patch`, `zone_floor`, `wave_start` skip them
and `zone_build` dispatches here). Schema and checks: theme.md §5.

### 5.3 `prep` (generated `mboss/cb/prep` + `cb/pp/<id>`; module hook `F:mboss/<id>/prep`)

- `cb/prep`: as the kind-9 zone marker, at it; one line per enabled chapter boss
  `execute if data entity @s data{boss_id:"<id>"} run return run function rlk:mboss/cb/pp/<id>`.
- `cb/pp/<id>`: `data remove storage rlk:mboss cprep.<id>`; `function rlk:mboss/ar/<aid>/fl_on`;
  `function rlk:mboss/arena/<aid>/ensure` (starts the sliced job; its result is ignored here); `function rlk:mboss/<id>/prep`.
- **Module hook `<id>/prep`** (required for chapter bosses, not a macro): @s = the zone marker, at it (the zone centre
  at stand height y 201, the floor blocks at y 200). Must write `cprep.<id>.gate`, `.title`, `.sub` (§3.3); may roll per-map state into `cprep.<id>.*`; may
  summon `rlk_room` display entities inside the zone (the glyph props); must not touch `cur`, `#mbId`, the arena, or start a
  fight. It runs once per entrance build (a retry of the same boss map does not re-run it).
- **No zone tick**: outside a fight nothing runs the module (`mboss/main` only runs while `#mbLive 1`). Decor that must
  animate in the entrance (Azhdaha's stele glow every 10 t, plan §2.3) is a self-rescheduling `schedule function
  rlk:mboss/<id>/<own path> 10t replace` chain started by `prep`; the chain stops itself when its `rlk_room` props are
  gone (`room/clear` kills them) and `uninstall` clears it (`schedule clear`).

### 5.4 Entering the zone and the gate

- `cb/enter` (from `F:room/zone_enter`, as the zone marker, at it): `scoreboard players set @s zst 3`,
  `function rlk:room/obj/k_cboss`, the zone-enter sound (`execute unless score #k10 snd matches 1 run function rlk:snd/f10`).
  No `combat_start`.
- `F:room/obj/k_cboss` (hand-written, new; + `k_cboss2`, `k_cboss3`): reads `cprep.<data.boss_id>.gate` (macro `with
  entity @s data`, then `with storage rlk:mboss cprep.$(boss_id).gate`). If `cprep.<id>.gate` is absent (prep never
  ran or failed, storage wiped) the gate still appears, never nothing (a gateless boss map is a soft-lock): `#oact tmp
  16`, `#oarg tmp` = n, `room/obj/make_node with storage rlk:mboss cbyid.<id>.gate` (the M0 `snbt_entry` record: icon,
  name, colour) and a gray `tellraw` warning. Otherwise it summons, at the execution
  position: two `item_display` icons (`item_model` = `model` / `model2`, translations −0.45 / +0.45, scale 1.0, vertical
  billboard), the `rlk_obj` marker (`oact 16`, `oarg` = `n`), the label `text_display` at +2.55 with
  `text:[$(l1),{text:"\n"},$(l2),{text:"\n"},$(l3)]` (scale 0.9) and the hint display at +2.2, all `rlk_room` and in one
  `ogid` group (the `make_node2` structure, own label).
- `mboss/cb/gate` (from `F:room/obj/click` oact 16; @s = the object marker, at it): the guards of `mboss/gate` (peaceful →
  gray message; no `rlk_zone` with `zkind 9`, `zst 3` and `data.cboss` → return; a body exists → return); while
  `#mbArBuild ≥ 1` → `tellraw` gray "경기장을 준비하는 중입니다. 잠시 뒤 다시 누르세요." and return (the object stays);
  else `#cbWait 0`, `ar/<aid>/fl_on` of the boss's arena (idempotent; re-adds the forceload a cancelled `cb/won`
  released, so the chunks load during the 30-t delay), `room/obj/kill_group`, `room/combat_start` as that zone, `#spawnT room 30`,
  `title times 6 46 14`, subtitle
  `cprep.<id>.sub`, title `cprep.<id>.title` (both `{nbt:..,storage:"rlk:mboss",interpret:true}`), `vBig`/`ttlT` 66,
  the two gate sounds of `mboss/gate` (bell.resonate 0.7 0.6, warden.heartbeat 1 0.7).

### 5.5 Spawn (`cb/spawn_route`, `cb/start {id}`, `cb/body`)

- `cb/spawn_route` (from `F:room/boss_spawn`, @s = the zone marker): one literal line per enabled chapter boss
  `execute if data entity @s data{boss_id:"<id>"} run return run function rlk:mboss/cb/start {id:"<id>"}`; its last line
  is `function rlk:mboss/start_cancel` (a `data.cboss` zone whose `boss_id` is no enabled chapter boss: the fight is
  cancelled and the gate returns). There is **no fall-through to Raiden**: the `boss_spawn` line is a `return run`.
- `cb/start {id}` (macro; @s = zone marker): `$data modify storage rlk:mboss cur set from storage rlk:mboss cbyid.$(id)`
  (missing → `start_cancel`), then the shared `mboss/start` body with these chapter rules (`fight_vars` sets `#mbMode 1`
  from `cur.kind`, and `#mbAr` from `cur.ar` **before** any arena check; M0's hard-coded `loaded 200 201 8` test becomes
  `ar/loaded`): **no roll, no `met` append, never `#mbForce`**; `ar/fl_on` (idempotent), then arena = `ar/ensure` of
  `#mbAr`: while it fails, `#cbWait +1` and retry with `#spawnT room 10`; the 7-miss cancel of `start_unloaded` counts
  only ticks with `#mbArBuild 0` (a running or waiting job never cancels), and a hard cap cancels after **60 retries
  (600 t)** whatever `#mbArBuild` says (`start_cancel`: the gate returns, `cprep` kept); the marker is summoned by
  `ar/<aid>/marker`; after `d/spawn` and the body check:
  `#mbTot` = the body's `mhpM`, `repool {pct: phases[0]}` when `phases[0] < 100`, `px/spawn` when `#mbPx 1` (state `inv`);
  `#cbWait 0`, `ret_save`, `#mbOn 1`, `#mbSt 0`, `tp_in`, `bars_show` as today.
- `mboss/cb/body` (for the module's `spawn`, at the spawn point, yaw = facing): `mboss/body` with the tag list **without
  `miniboss`**, `rlk_mb_big` when `cur.px:1b`, `rlk_mb_noshield` when `cur.shield:0b` (default for px bosses, §2.2).
  `body_setup` adds RES (§8). The husk scale comes from the registry `scale` (Azhdaha 0.1); a module changes it at
  runtime with M0's `mboss/body_scale {s}` (Apep FN-13). Without a shield the body has no click box in any state
  (`F:mob/shield_ensure`).
- Rewards on the kill: `combat/apply` pays the heal orb, XP (`cur.xp`), and through `F:combat/gold_drop` (edited, §16)
  the boss economy: `#bossGoldMul` 15 × chapter and `#bossSapphire` 2 (the body has `boss`, not `miniboss`). Level from
  `room/mob_init` with `#mapIdx 5`: L6 / L12 / L18 for chapters 1 / 2 / 3.

### 5.6 Win / cancel (`cb/clear`, `cb/won`)

- `cb/clear` (from `F:room/combat_clear`, as the zone marker, at it): `execute store result score #cbW mb run function
  rlk:mboss/cb/won`, then `execute if score #cbW mb matches 1 run function rlk:room/obj/k_chapter`.
- `cb/won`: `#mbWas = #mbOn`; gold absorb in the arena box (`ar/box_absorb`); `cleanup_fight`; `ret_here` if no `ret`;
  `tp_out` if `#mbWas 1`; `ar/fl_off` of the fight arena; **no `reward`, no boxes**; killed (`#mbKilled 1`): title
  `[cur.title, " 처치"]`, subtitle "다음 챕터로 가는 길이 열렸습니다" (#FFE08A), `vBig/ttlT` 72; test mode prints the chapter
  replay links (`test/chapter_ch` with `tlast`); then `forget`; returns 1. Not killed: the gray cancel message,
  `room/obj/k_cboss` at the zone centre (the same `cprep`, same pair), `forget`, returns 0.

### 5.7 Death and pause

Unchanged framework paths (`death_start`, `death_shell`, `death_finish`, `pause_tick`, `resume`) plus the chapter
additions: `death_start` runs `px/state {set:"dead"}` and `music/stop` before `d/death_start`; `pause_tick` runs
`px/clear_input` on **every** paused tick (a click made while paused never becomes an attack at the resume; M0's
`pause_tick` runs each paused tick, its first line only on the edge) and `music/halt` on the edge (`#mbPause 0`);
`resume` restarts the phase track (`music/set` with `#mbMusPh`). `/reload`: M0's `mboss/init` kills every
`rlk_mb_aux` (proxies, arena props, cards) and then runs `mboss/reload` as a surviving body; the generated `reload`
summons the marker with `ar/marker` (not the plaza literal) and, when `#mbPx 1`, runs `px/spawn` as the body before
`d/reload` (`px.set` / `px.o` survive in storage, so the module only re-states when its own state changed).

### 5.8 Lose (`cb/lose`, `test/lose`)

`mboss/cb/lose` (callable from anywhere): `#mbLost 1`; `scoreboard players set @a[tag=player] curHealth 0` (the normal
death path: `run/fail`, or `test/defeat` in a test; a Ronova revive applies as for any death). `test/lose` = the command
form for tests. Tested on cproto (§15.1).

### 5.9 Test commands (generated `F:mboss/test/*`)

| command | effect |
|---|---|
| `test/chapter {id}` | = `test/chapter_ch {id,ch:<the boss's first ch, else 1>}` |
| `test/chapter_ch {id,ch}` | guards of `test/start_ch` (player tag, room ready, no run, difficulty); refuses an id without `cbyid.<id>`; `#mbTest 1`, `#mbLock 0`, `#cbForce` = n, `#cbAuto 1`, `tlast {id,ch,cb:1b}`, `#active room 1`, `#chapter room` = ch, `#mapIdx room 5`, `#mapType room 8`, `#stDefer room 0`, `rnRev 0`, `room/gen` (→ route_force → layout), `zone_build` of the kind-9 zone (→ prep), the player `tp` into it facing the gate, `zone_enter` (→ `k_cboss`), full health; then `test/cwait` |
| `test/cwait` | scheduled every 5 t (≤ 300 t: a build job may wait 200 t for chunks, then run 40 slices): when `#mbArBuild 0` and `#cbAuto 1` it presses the gate (`cb/gate` as the oact-16 object), `#cbAuto 0`; on time-out a gray "경기장 준비 시간 초과 — 문을 직접 누르세요" line and `#cbAuto 0` (the gate stays). Any successful press (by hand too) clears `#cbAuto` in `cb/g/<id>`, so cwait stops at its next poll (change note 20.3) |
| `test/lose` | `cb/lose` |
| `test/kill`, `test/abort`, `test/pattern {id}`, `test/lock {id}`, `test/level {lv}`, `test/stop` | as for mid-bosses; `test/level` also sets `#mbTot` and re-applies `#mbPoolPct` (§7.1) |
| `test/defeat`, `test/won` | chapter wording when the fight that ended is a chapter fight (`cur.kind "chapter"`; `tlast.cb` follows it, the session does not decide); the replay link is `test/chapter_ch {id,ch}`. After a chapter fight (killed or cancelled) `test/won` → `test/cwon` resets `#cbForce 0`, `#cbAuto 0` (change note 20.1) |

`test/end` and `test/start_ch` reset `#cbForce 0`, `#cbAuto 0` (and `run/end` → `cb/run_reset`).

### 5.10 Run hooks and optional polish

- `mboss/cb/run_reset` (from `F:run/start` and `F:run/end`): `#cbForce 0`, `#cbAuto 0`, `data remove storage rlk:mboss
  cprep`, `data remove storage rlk:mboss cbpeek`.
- `mboss/cb/remove` (from `F:room/remove`): every chapter arena's `arena/<aid>/clear` + `ar/<aid>/fl_off`.
- Optional (S1-CM decides, README lists it): `mboss/cb/peek` writes `cbpeek` from the routing rules for `#chapter room`;
  `F:room/end_boss` / `F:room/gen_title` may show `cbpeek.name` instead of "보스전".

## 6. Per-arena functions and builds

### 6.1 Numbering and dispatch

`#mbAr` = the arena `n` (plaza 0). Every former baked token becomes a per-arena function behind a one-line dispatcher
`F:mboss/ar/<fn>` (`execute if score #mbAr mb matches <n> run return run function rlk:mboss/ar/<aid>/<fn>` per arena,
the plaza line first). The plaza's per-arena functions contain exactly the M0 text of the function they replace, so a
mid-boss fight behaves as on M0.

### 6.2 `F:mboss/ar/<aid>/*` (core, generated for the plaza and every `arenas{}` entry)

| fn | context | replaces (M0) | does |
|---|---|---|---|
| `marker` | any, `in overworld` | the marker summons in `start`, `reload` | summon `rlk_room rlk_mb_aux rlk_mb_arena` at `cx cy cz`, rotation 180 in every arena (the M0 plaza value; `d/spawn` runs rotated as it, so a module that wants another facing sets it itself: Azhdaha faces `POINTS['spawn']` yaw 0, theme.md §6.4) |
| `oob` | as `rlk_body`, at it | `mboss/oob` | inside = feet in `oob.y0..y1` at its x/z and within `walk + 1.5` of the axis; else back to `cur.start` (+ view/sync, rlk_safe, actionbar) |
| `sweep` | any | `mboss/arena_sweep` | kill arrows, items, XP orbs, heal orbs, gold in the box |
| `box_absorb` | as zone marker | the gold line of `won` | `rlk_gold` in the box → `combat/gold_absorb` |
| `ok` | at a proposed feet position | `mv/ok` | inside `safe − 0.5` + free feet and head; return 1 / fail |
| `clamp`, `clamp_step` | as a marker | `mv/clamp*` | pull inside `safe − 0.5` |
| `clampw`, `clampw_step` | as a marker | (new) | pull inside `walk − 0.7` (lockv targets) |
| `leash` | as the body | `mv/leash` | beyond `safe + 1` slide back 0.45 b/t; beyond `walk + 2` home |
| `full_rim` | as a hazard marker | the rim line of `hz/d/full` | the rim circle bucket `walk × 2` |
| `tp_in` | as the player | (new) | `tp` to `start` + `view/sync` + `rlk_safe` (used by `oob`) |
| `fl_on`, `fl_off` | any, `in overworld` | the `@FL@` forceload lines | `forceload add/remove x0 z0 x1 z1` of the box |
| `loaded` | any | the loaded checks | chapter arenas: return 1 when every chunk of the box is loaded (the centre first; change note 20.18); the plaza: M0 `start`'s single test of the centre (`200 201 8`), so the plaza functions are all M0 text (change note 20.8) |
| `ensure` | any, `in overworld` | `arena/ensure` call sites | plaza → `arena/ensure`; others → `arena/<aid>/ensure` |
| `test` | as the player | `test/arena` | rebuild + look (outside a run) |

Two different "sweep" functions keep the plan's names: `ar/<aid>/sweep` (no args, core: entity sweep of the box, the
old `mboss/arena_sweep`) and `arena/<aid>/sweep {y0,y1}` (arena generator: barrier band, §6.3, §12).
`hz/full` reads `#mbArW10` instead of the baked `WALK × 10`. `mboss/init`, `reload`, `uninstall` call the plaza
functions directly (load-time ensure stays plaza-only); `uninstall` releases every arena's forceload.

### 6.3 `F:mboss/arena/**` (arena generator)

- Plaza (legacy, byte-identical): `arena/{ensure,build,build_plaza,rebuild,clear}`, stamp `rlk:mboss built` = `"plaza@2"`.
- Per `arenas{}` entry: `arena/<aid>/ensure`, `build` (start a full build job), `s/<i>` (build slice i, i = 0..n−1),
  `rebuild` (drop the stamp + build), `clear` (drop the stamp; air over the box when loaded, ≤ 32 768 blocks per fill),
  `sweep {y0,y1}` (barriers → air in per-row spans inside `walk − 0.5`, absolute y, never a rectangle), `look/<look>`
  (start a look job), `l/<look>/<i>` (look slice i), `done` (job end: stamp, sentinel check).
- Shared: `arena/job_tick` (the scheduler: one slice per tick, re-scheduled `1t replace` while a job runs) and
  `arena/clear_all` (plaza `clear` + every `<aid>/clear`; not called by M0 files).
- **Missing theme module** (`L.theme_module` returns None: `az_cavern` on `wip/az-cm`, on main@AZ-CM and on
  `wip/az-mod` until it merges `wip/az-arena`): the generator still writes the full function set of that arena as
  stubs, so every reference resolves: `ensure` stamps `"<aid>@0:stub"` and returns 1 (nothing built; the module's tests
  stub the floor), `build` / `rebuild` / `clear` / `sweep` / `done` are no-ops, no `s/*` or `look/*`. It prints
  `WARN theme <theme> missing: stub arena <aid>`; the pack check passes; `test_chapter.py` never uses a stub arena.
  The `F:mboss/ar/<aid>/*` functions need only registry values and are always real.

### 6.4 Stamp, sentinel, ensure

`built_<aid>` = `"<aid>@<ver>:<look>"`; the sentinel = the theme's `SENTINEL` block (identical in every look).
A job removes the stamp while it runs, so a module reads the current look from **`look_<aid>`** (§3.3; change note 22.3):
the look the arena shows, or during a job the look it turns the arena into; none after an abort (a half-swapped arena).
`arena/<aid>/ensure` returns **1** only when no job runs, the box is loaded, the stamp is `"<aid>@<ver>:<looks[0]>"` and
the sentinel matches. Otherwise it returns **fail** and makes sure a job runs: stamp version wrong or missing → `build`;
version right, look ≠ default → `look/<looks[0]>`; stamp right but box not loaded → a `verify` job (waits for the
chunks, checks the sentinel, ends or switches to `build`). A call while another arena's job runs returns fail and starts
nothing.

### 6.5 Sliced jobs (`#mbArBuild`, `arjob`)

- One job at a time. `#mbArBuild` = slices left (≥ 1 while waiting for chunks). `arena/job_tick` runs from a
  `schedule function rlk:mboss/arena/job_tick 1t replace` chain; it waits while `ar/<aid>/loaded` fails (≤ 200 t, then
  the job aborts: `#mbArBuild 0`, stamp removed). `mboss/init` re-arms the schedule when `#mbArBuild ≥ 1` after /reload.
- Limits (generator asserts): ≤ 40 slices per job, every `fill` ≤ 32 768 blocks, ≤ 8 000 commands per slice (theme.md §3).
- A build job's slices come from the theme's `slices()`; a look job's from `look_lines(look)` or the generated diff
  (theme.md §3.3). The last slice runs `done`: stamp + sentinel check (a wrong sentinel restarts a full build once).
- `cb/prep` starts the job at entrance build (≤ 40 t), so it ends long before the gate can be pressed.

## 7. Pools, floor, title (N14, plan R6)

### 7.1 Pools

- `#mbTot` = the body's `mhpM` right after `d/spawn` (chapter fights; mid-bosses also get it, unused).
- `mboss/repool {pct}` (macro, as anything; 1..100): `mhpM = #mbTot × pct / 100` (overflow-safe as `aux/pool_pct`),
  `mhpC = mhpM`, `#mbPoolPct = pct`, `#mbRamp 30` (the bar refills over 30 t: `#buHp × (30 − ramp) / 30`).
- `cb/start` applies `phases[0]` when < 100. Later phases are the module's calls. `test/level` (after `level_apply`):
  `#mbTot = mhpM`, then `repool {pct:#mbPoolPct}` when `#mbPoolPct < 100`.

### 7.2 Floor (`mboss/floor`)

- The module sets `#mbFloor` (absolute HP, 0 = none). `F:mboss/d/incoming` gets, for every chapter boss, the line
  `execute if score #mbId mb matches <n> run return run function rlk:mboss/cb/inc/<id>`; `cb/inc/<id>` =
  `function rlk:mboss/<id>/incoming` then `function rlk:mboss/floor`. Mid-boss lines are unchanged.
- `mboss/floor` (as the body, inside `combat/apply_mods`): when `#mbFloor ≥ 1`: `#mbFloorRaw = #dmg`; if
  `mhpC − #dmg ≤ #mbFloor` → `#mbFloorHit 1`; `#dmg = max(0, min(#dmg, mhpC − #mbFloor))`.
- True damage (`true_hit`, `test/kill`) never reaches `apply_mods`, so it bypasses the floor. **Modules never call
  `mboss/floor` themselves** (the framework already runs it after their `incoming`).

### 7.3 Title

`mboss/title {title,sub,color}` (macro): `cur.title = {text:"$(title)",color:"$(color)",bold:true}`, `cur.sub = "$(sub)"`;
the bars pick it up on the next tick.

## 8. Per-element RES (N15, plan R7)

- `body_setup` (shared by `body` and `cb/body`): when `cur.res` exists → `mboss/res_set`: `mbRes<k> = cur.res[k]`
  (k = 0..8), `tag @s add rlk_mb_resel`, `mres = mbRes0`.
- `aux/spawn` options `#auxResEl` (−1 = none, default) / `#auxResElV`: when `#auxResEl ≥ 0`: `mbRes0..8 = #auxRes`,
  `mbRes<#auxResEl> = #auxResElV`, tag `rlk_mb_resel`. Both reset by `opts_reset` (`-1`, `0`).
- `mboss/res_pre` (from the new `F:combat/apply` line before the body `on_hit`, for `rlk_mb_resel` entities, not for
  true damage): 9 generated lines `execute if score #elem tmp matches <k> run scoreboard players operation @s mres = @s
  mbRes<k>`. It runs after `element/on_hit` and before the module `on_hit`, so a module may override `mres`; reactions,
  amplified hits and DoTs re-enter `combat/apply` with their own `#elem`.
- A module may rewrite `mbRes<k>` on its body at any time (Azhdaha: the rolled pair 30, s2.md §4.4), and may opt any
  aux in by itself: write `mbRes0..8` and add `rlk_mb_resel` (Apep FN-7's `mbResSet 1` is this tag).
- Mid-bosses: no `res` → no tag → `mres` 0 (the butterfly "equal damage" test stays green).

## 9. Hit proxies (N9, plan R8, §3.3)

### 9.1 Entities

At most **16** proxies per boss. Per proxy one `minecraft:interaction`: `UUID` fixed (the boss block from the
manifest's `uuids.ints` + low byte `pxBase + k`, k = 0..N−1 in `proxies.layout` order, §14), `Tags:["rlk_room","rlk_mb_aux",
"rlk_mob","boss","rlk_mb_px","rlk_mb_px_<name>"]` (**never `rlk_zmob`, never `rlk_mshield`**), `response:false`,
`width` = the layout `w`, `height` = the current column top, score `mbPart` = k + 1 (1..N; 0 is reserved for a
direct body hit, §9.6). A **live** proxy stands at the
anchor floor (`^x ^ ^z` from the anchor, y = anchor y) and carries `rlk_mob`; a **parked** proxy is 8 b under the floor
and has no `rlk_mob`. A proxy is live iff it is in the current state set **and** its top > 0.3 b.

### 9.2 Manifest input

The core reads `T:mboss_<id>_rig_manifest.json` **only when it is schema v1 from the rig** (`"schema": 1`,
`"source": "rig"`; the R1 file of `wip/az-rig`@7c3e9fe has no `schema` and counts as absent) and
`T:mboss_<id>/stub_rig_manifest.json`, and merges them exactly as `api.py` does (manifest.md §1): every clip of the real
file, stub clips only for names the real file lacks (their ids ≥ 1000, never a rig id), the global keys (`proxies`,
`uuids`, `states`, `capsules`, `runtime`) from the real file when present, else from the stub. cproto:
`T:mboss_cproto_rig_manifest.json` (static, `"source": "stub"`). Schema v1 (manifest.md): `proxies.layout`, `uuids`,
`states`, `capsules`, `runtime.{clip_obj,tick_obj}`, every clip's `px` keys. Disabled entries are not read (on
`wip/az-cm` and main@AZ-CM Azhdaha needs no manifest). The build fails when an enabled px boss has neither
file, when the proxy UUIDs disagree with `pxBase`, when a state named below is missing (`inv` and `dead` are
required in every px manifest), or when two clips of the merged manifest share an id (a stub fallback clip that reuses
a rig id; change note 20.15).

### 9.3 Generated functions (`F:mboss/px/**`)

| function | context | does |
|---|---|---|
| `px/spawn` (dispatcher) → `px/<id>/spawn` | as the body, at it | kill the boss's proxies by UUID, summon all, apply `px.set` (default `inv` when absent); when `px.o` is absent it is written from the manifest `proxies.rest` (a clip id with no key functions, e.g. an R1 debug pose, keeps the last offsets, so the proxies start at rest) |
| `px/state {set}` (macro) | anywhere | `px.set = set`; re-park / un-park by membership; `push[]` from the state's capsules; the rig visibility function named by the state (`vis`, may be null); entering an `inv:true` set: if the body has no `rlk_mb_inv` yet, add `rlk_mb_inv` + `rlk_mb_pxinv` (a body that is already `rlk_mb_inv`, e.g. in the intro, gets neither); leaving it: if `rlk_mb_pxinv` is present remove both, else touch nothing. So px never removes an `rlk_mb_inv` it did not add. An unknown set name prints a `tellraw` warning and changes nothing. Literal per-boss-per-set lines (no `$(..)` function names) |
| `px/tick` (dispatcher) → `px/<id>/tick` | from `mboss/world` after `body_tick` (so after the module tick and the rig tick) | reads the anchor's `clip_obj` / `tick_obj`; runs the key function of that clip and tick if one exists (`px/<id>/c/<clip id>` → binary tree → `px/<id>/k/<clip id>/<t>`), then `px/<id>/follow with storage rlk:mboss px.o` |
| `px/<id>/k/<c>/<t>` | | writes `px.o` offsets and `data merge`s `height` for every proxy whose sampled column moved > 0.15 b (x, z or top) since the last write; re-evaluates live / parked |
| `px/<id>/follow` (macro) | | one `tp` per proxy: `execute as <uuid> at <anchor> rotated as <anchor> rotated ~ 0 run tp @s ^$(<p>_x) ^$(<p>_y) ^$(<p>_z)` (`_y` = 0 live, −8 parked) |
| `px/park` | anywhere | every proxy parked (the set is kept) |
| `px/hit` | from `F:combat/apply` top, as the proxy, at it | §9.6 |
| `px/dup` | from `F:combat/apply`, as an `rlk_mb_big` body | §9.6 |
| `px/poll` | from `mboss/world` (live ticks) | each proxy with `attack` data → `combat/input/poll_attack` |
| `px/clear_input` | from `pause_tick`, every paused tick (§5.7) | `data remove entity <proxy> attack` / `interaction` for every proxy |

Tick `t` of a clip: the rig's `tick_obj` value after the rig tick of this game tick (the pose the client sees); a
negative value (queued) keeps the last offsets. Keys are sampled with `lerp` between manifest keys.

### 9.4 State sets

From the manifest `states` (manifest.md §6.2): Azhdaha `normal` (all 12), `jump` (none), `inv` (none, `inv:true`),
`tail_only` (tail1-4), `dead` (none, `inv:true`). `burrowed` is **not** a framework set (it is a rig visibility state,
manifest.md decision 7): the burrow phases use `inv`. The module maps its own states onto them with
`px/state {set:"<name>"}`. The framework itself sets `inv` at spawn and `dead` at `death_start`; the module switches to
`normal` when its intro ends.

### 9.5 Husk, shield, flash

Proxy bodies (`px:true`) are husks at scale 0.1 with `rlk_mb_noshield` (no click box, no arrow block, no collision in
any state) unless the entry sets `shield: true` (§2.2; Apep): then the body keeps M0's click shield of the entry's `hit`
size beside its proxies, and the de-dupe of §9.6 still gives one body hit per attack event (`test_px.py` 12, change
note 20.17). The last proxy hit is in `#mbPart` / `#mbPartGT`; the module flashes the manifest's flash group of that
proxy (`proxies.layout[k].flash`), never all parts.

### 9.6 De-dupe and redirect

- `#atkSeq tmp` +1 at the top of `F:combat/melee_begin`, `F:combat/clear_atkflags`, `F:element/rx_run`,
  `F:element/lunar/hit`, `F:element/dot` (one line each; `element/core_*` untouched).
- `px/hit` (as the proxy): gametime `g`; if `g = #pxGT` and `#atkSeq = #pxSeq` → return 0 (swallowed: no number, no
  reaction); else `#pxGT = g`, `#pxSeq = #atkSeq`, `#mbPart = @s mbPart`, `#mbPartGT = g`, `#pxIn 1`,
  `execute at @s as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:combat/apply` (the number shows at
  the proxy), `#pxIn 0`.
- `px/dup` (as an `rlk_mb_big` body hit directly, `#pxIn 0`, not true damage): same test and record with `#mbPart 0`;
  returns 1 = proceed, fail = swallow. One attack event → exactly one body hit across all proxies and the body; a
  reaction in the same tick gets its own `#atkSeq` (rx_run) and its own hit.
- Audits (§16): Navia pellet counts go to the body (`F:char/navia/pellet_go`, once per pellet; change note 20.10); the minimap ignores proxies
  (`F:room/map_mobs`).
- Target-side state written **outside** `combat/apply` lands on the proxy, not the body. Known at M0:
  `F:char/arlecchino/skill_hit:25` (`arDir` on `@e[tag=rlk_hit]`, later read on the body by `apply`'s `dir_death`
  line and by `dir_take`), `F:char/ronova/na_aim_hit:2-3` (`rnId` on the aimed mob). S1-CM greps every
  `@e[tag=rlk_hit]` / aimed-`rlk_mob` score write outside `combat/apply`, either mirrors it onto the body
  (`execute if entity @s[tag=rlk_mb_px] …`, a §16 line) or records it as accepted in the README audit table;
  `test_px.py` covers each listed case.

## 10. Music (N16, plan R11)

- `mboss/music/set {ph}` (macro, int `ph`): `ph 0` or no `cur.music."<ph>"` → `music/stop`. Else `mus = {ph, ev, len}`,
  `#mbMusPh = ph`, `#mbMusT 0`, `#mbMusLen = len`, stop the previous track, play: `execute as @a[tag=player] at @s run
  playsound <ev> record @s ~ ~ ~ 1 1 1`. The phase-3 call of Azhdaha reuses `{ph:2}`.
- While playing (live, unpaused world ticks): `#mbMusT +1`; `len ≥ 1` and `#mbMusT ≥ len` → replay from the start;
  every 100 t `stopsound @a[tag=player] music` (vanilla background music never overlaps).
- `music/stop`: `stopsound @a[tag=player] record <ev>`, `#mbMusPh 0`, `mus` removed (no fade; a sting is the caller's).
  `music/halt` (pause): stop the sound, keep `#mbMusPh`; `resume` restarts the track from 0.
- Stopped in `cleanup_fight`, `death_start`, the pause edge (halt), `uninstall`, `cb/won`.
- Events: stereo single-track `music.*` events (non-positional). S1-CM measures each `len` from the vanilla asset index
  (rounded down to ticks) and writes it into both chapter entries itself (its own file, the `music` line, §2.4 layout
  rule); until then `len 0` (= play once, no loop); in game once (README checklist): no fade across the
  arena, the loop. Fallback (only if the in-game check fails): `music_disc.*` at volume 4, re-anchored at each loop start.
- **Random-track pools** (change note 22.5): many vanilla `music.*` events pick one of several tracks on every
  `playsound` (`mboss_lib.MUSIC_TRACKS`, measured from the 26.3 .ogg files: `music.overworld.deep_dark` 2 tracks
  6068 / 6870 t, `music.nether.soul_sand_valley` 5 tracks 4789-6376 t, `music.overworld.lush_caves` 15 tracks
  4031-6881 t; single tracks `music.end` 18 090 t, `music.dragon` 6883 t). A pool cannot be looped exactly: its `len` is
  `0` (play once) or a **re-pick period** ≥ its longest track (`L.music_len(ev)`): each replay stops the old sound and
  picks a new random track, never cutting one; after a shorter track there is a silence until the period ends (as
  vanilla's own music gaps). `load_registry` rejects a pool `len` in 1 .. longest − 1.

## 11. Bars (plan R12)

The three framework bars unchanged; the module fills `extra[]`, `sub[]`, the under-bar. `T:build_bossbar.py` options,
both **reset to 0 by `mboss/bars` before `d/bars` on every chapter-fight call** (`mboss/bars_cm`, behind `#mbMode 1`) and by
`bossui/draw` after every draw, so a mid-boss fight and Raiden, which never set them, always draw the M0 line (change
note 20.7):
- `#buHpCol bu`: 0 = the default HP colour `#E0484B`; 1..9 = the under-bar colour codes (`SUB_COLORS`); 10 = `#EDCF63`
  (Apep's Heart gold). With 0 the drawn line is identical to M0.
- `#buNoNum bu`: 1 = no "hp/max" numbers (the cursor goes straight to the bar end). 0 = M0 output. (Apep FN-24.)

## 12. Cleanup (plan R13)

- `cleanup_fight` adds: `#mbMode 0`, `#mbFloor 0`, `#mbFloorHit 0`, `#mbCine 0`, `#mbPushOn 0`, `#mbPoolPct 100`,
  `#mbRamp 0`, `#mbHitEv 0`, `#mbDodgeEv 0`, `#mbDodgeOk 0`, `#mbPart 0`, `music/stop`, `data remove storage rlk:mboss px`,
  `push`, `lv`. `#mbAr` keeps its value until the next `fight_vars` (cb/won still needs it).
- Forceload of a chapter arena: added by `cb/pp/<id>` (prep) and the dev view `ar/<aid>/test`; the dev view's goes again
  when its job ends outside a run (`arena/<aid>/done` / `vdone` with `#active room` and `#mbLive` not 1; a stub arena's
  `rebuild`; change note 20.4); released by `cb/won`, `mboss/cleanup` (generated lines for
  every chapter arena), `cb/remove` (room/remove) and `mboss/uninstall`.
- `room/remove` → `cb/remove` → every `arena/<aid>/clear`. Barrier band sweep: `arena/<aid>/sweep {y0,y1}` (callers:
  modules at will; `cb/won`, `mboss/cleanup` and `cb/remove` for arenas whose entry has `sweep`, §2.3 — Apep's walls;
  Azhdaha never places barriers).
- A running arena job is aborted first by `cb/remove` (its arena), `mboss/uninstall` (any) and by `ar/<aid>/fl_off` of
  a chapter arena itself (a job of that arena, whoever releases the forceload: `cb/won`, `mboss/cleanup`, a direct
  `ar/fl_off`; change notes 20.2, 20.20): `#mbArBuild 0`,
  `arjob` removed, `schedule clear rlk:mboss/arena/job_tick`, the stamp of a half-built arena removed.
- Arena display props are per-fight entities tagged `rlk_mb_arena_prop rlk_mb_ar_<aid>` (never `rlk_room`); the
  framework kills `@e[tag=rlk_mb_arena_prop]` in `cleanup_aux` and in `mboss/init` next to its `kill @e[tag=rlk_mb_aux]`
  (M0 `F:mboss/init:127`, i.e. before a surviving body's `reload`, and also when no body survived), so `rlk_mb_aux` on
  them is the module's choice (Azhdaha: yes, plan §2.2; Apep's FN-3 asks for props without `rlk_mb_aux`). The framework
  never spawns props: the module spawns `props(look)` at fight start and after its own `arena/<aid>/look/<look>` call
  (theme.md §4.1).
- `run/start`, `run/end`, `test/stop` → `cb/run_reset` (§5.10); `#cbForce` never survives a test.

## 13. Player-status and motion helpers (plan R16)

### 13.1 `mboss/mv/lockv {lead}` (N3)

- Ring buffer `lv[0..5]` (mb, x/z of the player's body), written by `mboss/main` every tick while `#mbLive 1`; a sample
  is skipped while `dashMoveT ≥ 1` (the buffer keeps the last non-dash positions; Apep §7.11 rule 7).
- `lockv {lead}` (as anything): `v = (p_newest − p_oldest) / 5` mb/t, `|v|` capped at 280 mb/t (sprint);
  `#mbVx #mbVz` = v, `#mbV` = |v| (integer sqrt); kills the old `rlk_mb_lock` marker and summons
  `rlk_room rlk_mb_aux rlk_mb_lock` at `p + v × lead`, y = the arena `cy`, pulled inside `walk − 0.7` (`ar/clampw`).
  Modules re-tag it (`keep`): a module that keeps the marker **removes `rlk_mb_lock`** from it, otherwise the next
  `lockv` call kills it. `L.lockv(lead)` returns the call line.

### 13.2 `mboss/mv/local` (N8)

As the anchor (the body): `#mbLf` / `#mbLs` = the player body's position in the anchor frame in mb (f forward, s left),
computed with the `hz/hit` projection (≈ 25 commands). No arguments.

`mboss/mv/plpos` (anywhere; change note 20.21): `#mbPX` / `#mbPZ` mb = the player body's x / z in mb, read with one
entity NBT read (`Pos` -> `rlk:mboss plp`; a player's NBT read saves the whole player) at most once per game tick
(`#mbPlG` = the game time of the read); fails without a body. `mv/lv_sample`, `mv/local`, `mv/lockv`, `push/capsule`,
`push/ring` and `hz/hit_mask` read the body position only through it; modules should too. A chapter-runtime teleport of
the player in the tick drops it (`#mbPlG -1`: `push/capsule` after a move, `ar/<aid>/tp_in` of a chapter arena), so the
next call reads again; a module that teleports the player and reads the position again in the same tick sets
`#mbPlG mb -1` itself. M0 text (`hz/hit`, `hz/hit_full`, `pull/tick`, `mv/clamp_step`, `ret_save`) keeps its own reads.

### 13.3 Hit and dodge events (N7)

`mboss/hurt` (and therefore `hz/hurt`, `pj/hit`, `hz/mask` hits) sets after every call that reached the player:
- landed (not dodged, damage applied): `#mbHitEv += 1`, `#mbHitEl` = the element, `#mbHitSh` = 1 if `shieldHP ≥ 1` or
  `gShield ≥ 1` before the hit, `#mbHitRA` = 1 if the source hazard has `mbHzRA ≥ 1` (a re-arming / lingering hazard),
  `#mbHitSrc` = 1 hazard, 2 projectile, 3 direct call;
- dodged (`#dodged 1`): `#mbDodgeEv += 1`; `#mbDodgeOk 1` only for a one-shot strike hazard (`mbHzRA 0`, tell `mbHzW ≥ 12`,
  `mbHzND 0`) or a projectile.
Refused hits (dead, reviving, selection, dying boss, `#mbCine 1`) set nothing. The module reads and clears `#mbHitEv`,
`#mbDodgeEv`, `#mbDodgeOk` in its tick.

### 13.4 `mboss/pl_dot` and NoRx (N7)

- Inputs: `#mbDotPct` (‰ of `maxHealth`), `#mbDotEl` (element for the shield efficiency), `#mbDotLethal` (0/1). As
  anything. Refused while dead, reviving, in a selection screen, `#mbSt 2`, `#mbCine 1`.
- Effect (modelled on `F:player/hurt_elem`): dmg = ⌊maxHealth × pct / 1000⌋ ≥ 1; `dashInvT` saved, zeroed, restored
  (i-frames do not block it); guard shield (`engravings/guard/absorb`) then the element shield (`element/shield_absorb`
  with `#elem` = `#mbDotEl`, 250 % against its own element); **no defence**; non-lethal → the player keeps ≥ 1 HP;
  `player/hurt_do` fx. Output `#mbDotDmg` (HP lost; 0 when refused or fully absorbed). No hit event. Every input is
  reset after the call, refused or not (`#mbDotPct 0`, `#mbDotEl 0`, `#mbDotLethal 0`), so a stale value never leaks
  into the next caller; a one-shot `#mbNoRx 1` set for the DoT (FN-15: `#mbNoRx` from `#hzNR`) is spent there too
  (`#mbNoRx 0`: pl_dot runs no player reaction), and `cleanup_fight` clears it (change note 20.13).
- NoRx: hazard option `#hzNR 1` → `mbHzNR`, projectile option `#pjNR 1` → `mbPjNR`, one-shot `#mbNoRx 1` for a direct
  `mboss/hurt`. `mboss/hurt` sets `#mbNRNow 1` around the `cm/hit_pl2` / `hurt_nd` call when any applies, then resets
  `#mbNRNow 0` and `#mbNoRx 0`. `F:player/take_damage` skips `element/player_hit` while `#mbNRNow 1` (the hit keeps its
  element for colour, sound and shields). `L.hz_opts(norx=1)`, `L.pj_opts(norx=1)`.

### 13.5 Body push (N12) and push ring (N18)

- `mboss/push/capsule`: run by `mboss/world_cm_post` after `body_tick` while `#mbPushOn 1` (a per-tick request:
  `mboss/world_cm_pre` clears it every chapter-fight tick before the module tick; change note 20.6). Capsules = `push[]` (tenths in the anchor frame: `f0 ≤ f ≤ f1`, `|s| < hw`; an entry with `px`
  is active only while that proxy's current top ≤ `top`). A player inside is moved toward the nearest exit (side, front
  end, back end) whose end point is not inside a live `rlk_mb_hz` disc or line, by ≤ 0.6 b per tick in 0.1-b
  `player/knockback/check` steps (no velocity, no FOV); refused while dead, reviving, selecting, map view or dashing.
- `mboss/push/ring {r,to,kb}` (as anything, at the centre): every player whose body is within `r` (**tenths**,
  horizontal) is moved radially outward to the distance `to` (tenths, `to ≥ r`) on its bearing over `kb` ticks (1..10,
  collision-checked steps; a player exactly at the centre goes toward the arena `start`); skipped when the landing point
  is inside a live hazard; no damage, no hit event, not dodgeable. Azhdaha's plan `{r:8,kb:4}` = `{r:80,to:85,kb:4}`;
  Apep's CS "within 8 b → 12 b" = `{r:80,to:120,kb:…}` (its plan §7.7). `r` is clamped to 320 and `to` to 600 (tenths)
  and a player more than 32 b from the centre on x or z is outside (the squared distance stays inside int32; change
  note 20.14).

### 13.6 Mask hazard `hz/mask` (N4, kind 6)

`function rlk:mboss/hz/mask {tell,dmg}` with `#hzR0` = the safe radius R0 (tenths) and `#hzSafeG` = the safe group
(0 = the hazard's own id `mbHzI`). Hits a player whose feet are not within `R0 + 0.3 b` (horizontal score test) of any
`rlk_mb_hzsafe` marker with `mbHzSG` = the hazard's group; no radius limit; volley groups, `#hzNoDodge`, `#hzRearm`, the
height band and NoRx as the other kinds; the framework never draws it (the kit does). The hazard stores the
**resolved** group: `mbHzSG` = `#hzSafeG`, or its own `mbHzI` when `#hzSafeG` is 0 (never 0 on a live mask). Safe markers:
`rlk_room rlk_mb_aux rlk_mb_hzsafe` + `mbHzSG` = that resolved value (default case: `#hzLast`), made by the module
right after the call (same tick). `hz/expire` of a mask with
`#hzSafeG 0` kills its own markers; shared groups are the module's. `L.hz_mask(r0, tell, dmg)`, `L.hz_opts(safe_g=)`.
**Shared groups come from `mboss/hz/safe_new`** (change note 22.2): it writes a new group to `#mbSafeG mb` (−1, −2, …,
back to −1 after −999 999), a number space apart from the hazard ids (≥ 1), so no default-group mask (own id) can match
or kill a shared group's markers. The module copies it into `#hzSafeG` before each mask of the group
(`L.hz_opts(safe_g='cur')`) and into `mbHzSG` of the group's markers (`L.hz_safe_new()`). Only `#hzSafeG 0` resolves to
the own id; a positive explicit group (the AZ-CM form) still works but may collide with a hazard id and is not for new
code.

### 13.7 Cine (N19)

`mboss/cine/start` / `cine/end`: `#mbCine 1/0`. While 1, `mboss/hurt` and `pl_dot` refuse; the bars stay; the module
freezes its own AI clock. Reset by `cleanup_fight`. A hazard or projectile that reaches the player during a cine is
**refused without being consumed** (`hz/hurt` and `pj/hit` return before marking it hit; no event, no volley-group mark,
no `pj_end` event 4), so a live one can still hit once the cine ends (change note 22.4).

### 13.8 `#pjNoDodge` (N20) and `hz/extend` (N21)

- `#pjNoDodge 1` (one-shot) → `mbPjND`; `pj/hit` sets `#mbNoDodge` from it around `mboss/hurt` (as `hz/hurt` does).
  `L.pj_opts(nododge=1)`.
- `mboss/hz/extend {n}` (as a live hazard): `mbHzA += n` and `mbHzL += n` (the active window and the life grow
  together). `L.hz_extend(n)`.

### 13.9 Misc

`mboss/mv/lockv`, `mv/local`, `push/*`, `cine/*`, `pl_dot`, `hz/mask`, `hz/extend`, `repool`, `title`, `music/*`,
`px/state` exist for every boss; mid-boss modules never call them.

### 13.10 `mboss_lib` call builders (new)

`L.hz_opts(..., norx=None, safe_g=None)`, `L.pj_opts(..., nododge=None, norx=None)`, `L.hz_mask(r0, tell, dmg)`,
`L.hz_extend(n)`, `L.lockv(lead)`, `L.local()`, `L.pl_dot(pm, el, lethal=0)` (lines),
`L.push_ring(r_blocks, kb, to_blocks=None)` (`to` defaults to `r + 0.5`),
`L.cine(on)`, `L.repool(pct)`, `L.title(title, sub, color)`, `L.music(ph)`, `L.px_state(name)`. Modules set `#mbFloor`
with plain score lines. Every builder asserts its ranges.

### 13.11 Per-mille hazards `#hzPm` / `#hzPmL` (FN-15; change note 22.1)

One-shot options of the next hazard (any kind, the mask too): `#hzPm N` (1..1000 per mille of the player's
`maxHealth`; unset = a normal % hit) and `#hzPmL 0` (that hit never kills; unset = 1, lethal). `hz/init_pm` stores
`mbHzPm` / `mbHzPmL` on the hazard and spends `#hzPmL`; `opts_reset` resets `#hzPm`, `cleanup_fight` `#hzPmL` (resets,
not zeros: mid-boss fights never hold the names). The hit (`hz/hurt` → `hz/hurt_pm`) is a `mboss/pl_dot` of `mbHzPm`
per mille with `#mbDotEl` = the hazard element (element shields at 250 % against their own element) and `#mbDotLethal` =
`mbHzPmL`: no defence, no level factor, never a player-side reaction (`#hzNR` is implied), no knockback. Without
`#hzNoDodge` the dash i-frames dodge it (`player/dash_iframe`, `#dodged 1`, consumed as any dodged hazard); with it the
i-frames are ignored. Refused while dead, reviving, selecting, the boss dying (as `mboss/hurt`) and during a cine
(§13.7). Hit / dodge events (§13.3, source 1), `#hzRearm` and volley groups as for any hazard. `L.hz_opts(pm=N,
pm_lethal=0)`. Apep: the 종말의 여파 ticks `pm=30, pm_lethal=0, rearm=15, nododge=1, norx=1`; the blast a mask with
`pm=800` (lethal; `pm_lethal=0` on the first cast of a fight).

### 13.12 Aux presentation options and `mv/step_flat` (FN-29, FN-30; change note 22.7)

- `aux/spawn` one-shot options (reset after the spawn; `L.aux_opts(shield_w, shield_h, bar_y)`, blocks in, tenths
  out): `#auxShW` / `#auxShH` = the aux's click shield made at once by `aux/shield_pre` (an `rlk_mshield` interaction of
  that size, linked by `msid`, marked synced; `#auxShH` unset = 2.2 b), which `mob/shield_ensure` then keeps instead of
  making its 1.2 × 2.2 default; `#auxHbY` = the HP-bar passengers (`mob/hb_spawn`) moved up by that many tenths
  (`aux/hb_y`, at the spawn only; a later `mob/hb_spawn` would not keep it).
- `mboss/mv/step_flat {spd}` (blocks, a decimal; `L.step_flat(spd)`), as a ground walker rotated = its heading (the
  caller faces the target): yaw-only turn, one step, y = the fight arena marker's y (the floor), pulled inside walk − 0.7
  (`ar/clampw`). No collision test (flat arena floors). About 8 commands.

## 14. UUID allocation

Azhdaha block `524c4b4d-415a-4400-8000-0000000000NN` = `[I;1380731725,1096434688,-2147483648,NN]`:

| NN | use |
|---|---|
| 0x01-0x3F | rig parts (fixed name → index table in the rig builder, append-only; R1 uses 0x01-0x2E) |
| 0x40 | the rig's shadow helper (R1) |
| **0x41-0x4C** | hit proxies head 0x41, chest 0x42, belly 0x43, hips 0x44, tail1 0x45, tail2 0x46, tail3 0x47, tail4 0x48, paw_l 0x49, paw_r 0x4A, foot_l 0x4B, foot_r 0x4C (`pxBase 65`) |
| 0x4D-0x50 | reserved for up to 4 more proxies |
| 0x51-0x5F | unassigned |
| 0x60-0x8F | module props with a fixed id: **seal prism 0x80**, **B3 crater 0x81**; the rest reserved |
| 0x90-0xFF | unassigned |

cproto block `524c4b4d-4350-4400-8000-0000000000NN` = `[I;1380731725,1129333760,-2147483648,NN]`: proxies 0x41-0x42
(`core`, `tail`). Apep block `524c4b4d-4150-4400-8000-…` (`1095779328`): Apep's plan §3.6 (proxies 0x41-0x50).

## 15. Tests (S1-CM)

### 15.1 `test_chapter.py` (on cproto; reusable by Apep)

Routing ch 1 / 2 / 3 / 4+ with the `route` flags (cproto never routed; azhdaha `route:false` → Raiden); `#cbForce` only
under `#mbTest 1` and reset by every listed path; entrance build → `cb/prep` → `cprep` + forceload + the sliced job;
gate (oact 16, peaceful / zst / body guards, "준비 중" while `#mbArBuild ≥ 1`) → spawn → kill → ×15 gold × chapter + 2
sapphires, **no boxes**, `k_chapter`; abort → the gate returns with the same `cprep`; `cb/lose` + `test/lose`; title
swap; `repool` + `#mbTot` + `test/level`; music set / loop / stop / pause halt / no overlap; the two-look swap of
`cp_test` with per-look stamps and the default restored by `ensure`; every cleanup path (room/clear, wipe, remove,
uninstall, reload) incl. the forceload released and `sweep {y0,y1}`; **Raiden smoke** (a narukami zone builds,
`boss_spawn` reaches `boss/raiden/spawn` (stubbed), `combat_clear` still spawns `k_chapter`).

### 15.2 `test_px.py`

The proxy runtime on cproto's stub manifest (S1) and on Azhdaha's real one (I1, I2b): spawn / respawn after `/reload`,
tracks, parking (top ≤ 0.3, out of set), every state set, `rlk_mb_pxinv`; **every one of the 17 `combat/apply` call
sites** plus the `apply_reset` / `melee_apply` loops: one attack event → exactly one hit on the body; a reaction in the
same tick → its own hit; DoTs; lunar hits; numbers at the proxy; RES / `on_hit` / `incoming` / kill on the body; Navia
pellets counted on the body; the minimap exclusion; clicks polled every tick and cleared while paused; the husk at scale
0.1 with no shield; the push capsule and its gates.

### 15.3 `test_fw_az.py`

N4 mask (inside any safe circle with the 0.3 pad → no hit; horizontal test; groups; nododge; no radius limit; shared
`#hzSafeG`), N7 events (`#mbDodgeOk` only for one-shot strikes ≥ 12 t and pj), `pl_dot` (non-lethal, shields at 250 %,
no defence, i-frames ignored, refused while dead / cine), NoRx (no `player_hit`, colour kept), floor (clamp,
`#mbFloorHit` on ≤, `#mbFloorRaw`, true damage bypass), per-element RES on body and aux, cine, push ring (no damage,
skips hazard landings), `lockv` (dash samples skipped, sprint cap, clamp), `local`, `hz/extend`, `#pjNoDodge`,
`#buHpCol` / `#buNoNum` default byte-identity, mid-boss `mres 0` unchanged.

### 15.4 Pack check additions (`T:check_mboss_pack.py`)

Chapter entries: the 17 hooks + `prep` (not a macro); `creg` / `cbyid` lines match the registry; every arena has its
`ensure` with the right stamp string; the dynamic families `fx/p/<name>/<k>`, `px/<id>/k/...` are contiguous; no
`$(id)`-style function names (literal dispatch lines only).

### 15.5 Harness

`S:az/tests_cm/run_all.sh <wt>/roguelike [tag]` (shape of `S:mb3/tests/run_all.sh`): the three suites above (+
`test_fw_ap.py`, the AP-FW gaps of §22, skipped with rc 0 on a tree without them) + the M0
suites (`S:mb/int_tests`, `S:mb2/tests`, `S:mb2/fxtests`, `S:mb3/tests`), `gen_check.py`, `ident.py`
(`F:mboss/{guardian,butterfly,fieldgen,proto}/**` and the plaza files byte-identical to M0; the content of every §16
edit pinned in `baseline/shared_edits.diff`), `test_m0diff.py` (the mid-boss fights against the M0 archive by behaviour:
same seed, traces, logs, end states, commands per tick; the boss bar line; change note 20.9), the validators against
`baseline/`. Green = all of them, then CM-REVIEW (state + identity).

## 16. Shared-edit table (hand-written files S1-CM may edit; every edit listed in README "챕터 보스")

| file (M0 line) | edit (exact) |
|---|---|
| `F:room/pick/boss:3` | `function rlk:room/raiden/layout` → `function rlk:mboss/cb/route` (comments updated) |
| `F:room/boss_spawn` (new line 1) | `execute if data entity @s data.cboss run return run function rlk:mboss/cb/spawn_route` |
| `F:room/zone_build:4-5` | new line before 4: `execute if data entity @s data.cboss run function rlk:room/cboss/build`; line 5 condition → `unless data entity @s data.boss_id` |
| `F:room/zone_patch:2`, `F:room/zone_floor:2`, `F:room/wave_start:4` | `data{boss_id:"narukami"}` → `data.boss_id` |
| `F:room/zone_enter` (new line before 6) | `execute if score @s zkind matches 9 if data entity @s data.cboss run return run function rlk:mboss/cb/enter` |
| `F:room/obj/click` (after 25) | `execute if score @s oact matches 16 run return run function rlk:mboss/cb/gate` |
| `F:room/obj/k_cboss`, `k_cboss2`, `k_cboss3` | new files (§5.4) |
| `F:room/obj/k_cboss_fb` | new file: the gate from the registry gate record when `cprep.<id>.gate` is missing (§19.27, §19.33) |
| `F:room/combat_clear` (new line before 9) | `execute if score @s zkind matches 9 if data entity @s data.cboss run return run function rlk:mboss/cb/clear` |
| `F:combat/gold_drop:15,23,24` | `@s[tag=rlk_mb_body]` → `@s[tag=rlk_mb_body,tag=miniboss]` |
| `F:combat/apply` (after 8, the Raiden object line; §19.34) | `execute if entity @s[tag=rlk_mb_px] run return run function rlk:mboss/px/hit` and `execute if entity @s[tag=rlk_mb_big] unless score #pxIn mb matches 1 unless score #trueDmg tmp matches 1 unless function rlk:mboss/px/dup run return 0` |
| `F:combat/apply` (before 23) | `execute if entity @s[tag=rlk_mb_resel] unless score #trueDmg tmp matches 1 run function rlk:mboss/res_pre` |
| `F:combat/melee_begin`, `F:combat/clear_atkflags`, `F:element/rx_run` (top), `F:element/lunar/hit` (top), `F:element/dot` (top) | `scoreboard players add #atkSeq tmp 1` |
| `F:player/take_damage:22` | append `unless score #mbNRNow mb matches 1` before `run function rlk:element/player_hit` |
| `F:mob/shield_ensure` (after 6) | `execute if entity @s[tag=rlk_mb_noshield] run return 0` |
| `F:char/navia/pellet` | **no edit** (M0 text; change note 20.10) |
| `F:char/navia/pellet_go` (after 6, before the `nvHit` line) | `execute if entity @e[tag=rlk_np,tag=rlk_mb_px,limit=1] run tag @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] add rlk_np` and `tag @e[tag=rlk_np,tag=rlk_mb_px] remove rlk_np` (a pellet that hit a proxy counts once on the body; proxies are never counted) |
| `F:char/arlecchino/skill_hit` (after 22) | `execute as @e[tag=rlk_hit,tag=rlk_mb_px] run function rlk:mboss/px/to_body` (§9.6 audit, §19.32) |
| `F:room/map_mobs:5` | `@e[tag=rlk_mob,limit=48]` → `@e[tag=rlk_mob,tag=!rlk_mb_px,limit=48]` |
| `F:room/remove` (after 11) | `execute in minecraft:overworld run function rlk:mboss/cb/remove` |
| `F:run/start` (after 13), `F:run/end` (after 6) | `function rlk:mboss/cb/run_reset` |
| `F:room/setup`, `F:load`, `F:uninstall` | **no edit** (the generated `mboss/init`, `uninstall`, `cleanup` cover the arenas); allowed only for arena forceload / ensure lines if CM-REVIEW finds a gap |
| `F:room/end_boss`, `F:room/gen_title` | optional one line each reading `rlk:mboss cbpeek` (§5.10) |

Raiden's own files (`F:boss/raiden/**`, its generators) and every other shared file are not touched. Other stages'
shared edits: none (S1-MOD, S1-ARENA, S2: none; S1-FX and R3: append to `assets/minecraft/atlases/items.json` through
their generator's merge only).

## 17. Apep coverage

### 17.1 `[AP]` FW-1..19 minus FW-13 (Apep `plan_draft.md` §1.3) → this contract

| FW | item | here |
|---|---|---|
| FW-1 | registry chapter fields | §2 |
| FW-2 | multi-arena + per-arena looks, sliced looks, stamp `<aid>@<ver>:<look>`, ensure restores the default | §6 (+ theme.md §3.3) |
| FW-3 | `#mbTot`, `repool {pct}`, `#mbFloor` after the module `incoming`, `test/level` re-split | §7 |
| FW-4 | `mboss/title {title,sub,color}` | §7.3 |
| FW-5 | `#buHpCol` | §11 |
| FW-6 | per-element RES body + aux | §8 (per-entity `mbRes0..8` on aux, not `mbResE/mbResV`) |
| FW-7 | hit proxies, any state names, `#atkSeq`, capsule per state | §9, §13.5 |
| FW-8 | `#pjNoDodge` | §13.8 |
| FW-9 | `pl_dot` + one-shot `#mbNoRx` | §13.4 |
| FW-10 | mask hazard | §13.6 (with the safe group) |
| FW-11 | `mv/lockv` | §13.1 |
| FW-12 | `mv/local` | §13.2 |
| FW-14 | `cb/lose` + test variant | §5.8 |
| FW-15 | music | §10 |
| FW-16 | cine | §13.7 |
| FW-17 | rig-lib extras | **RIGLIB stage**, not S1-CM (plan Rig decision change 2) |
| FW-18 | barrier sweep `arena/<aid>/sweep {y0,y1}` | §6.3, §12 |
| FW-19 | chapter tests | §5.9, §15 |

### 17.2 Apep hook list (from `S:ap/framework_needs.md` FN-1..32 and Apep's binding `S:ap/plan.md`)

Marked **[in AZ-CM]** where this contract already delivers it, **[reserved]** where only the name is fixed and S1-CM
builds it only on request while `wip/az-cm` is open (afterwards Apep's AP-FW stage owns it, on its own reviewed branch).
**Adopt** = Apep must change a name or a value of its own plan to use this contract (its `fw_needs_check.py` greps the
names below, not the ones of its draft).

| Apep ref | need | status / name |
|---|---|---|
| FN-1 | registry chapter fields | **[in AZ-CM]** §2. **Adopt**: Apep's entry adds `"px": true`, `"pxBase": 65` (its proxies 0x41-0x50) and `"shield": true` (its torso click shield `hit` + the proxies; §2.2) |
| FN-2 | routing, gate, `cb/start` waiting for a running build / restore with its own time-out | **[in AZ-CM]** §5.1-§5.5 (the wait: `#cbWait`, 60 retries = 600 t, then `start_cancel`; the gate shows "준비 중" while `#mbArBuild ≥ 1`) |
| FN-3 | theme interface `arena_layout()`, `entrance_layout()`, `look_lines(look)`, `props(look)`, constants; per-fight arena props with fixed UUIDs, tag `rlk_mb_arena_prop` | **[in AZ-CM]** theme.md (union of both plans); props §12: the framework kills `rlk_mb_arena_prop` itself, so Apep's props need no `rlk_mb_aux`; the **module** spawns `props(look)` at fight start and after its own look call (the framework spawns no prop); fixed prop UUIDs come from the theme's optional `PROP_UUIDS` block (theme.md §2.2: Apep's arena-prop block `…4150-4100…`). **Adopt**: the per-arena prop tag is `rlk_mb_ar_<aid>` = `rlk_mb_ar_ap_oasis` (Apep plan §3.6 / §4.2 say `rlk_mb_ar_ap`) |
| FN-3 / M9 | look state in `rlk:mboss arena.<aid>.look` | the stamp carries the built look (`built_<aid>` = `"<aid>@<ver>:<look>"`, §6.4); a look change never triggers a rebuild (version right, look wrong → a look job). **[AP-FW]** read **`look_<aid>`** (§3.3, change note 22.3): right during a job too, when the stamp is gone |
| FN-4 | `#mbTot`, `repool`, `test/level` re-split | **[in AZ-CM]** §7.1 |
| FN-5 | "the module `incoming` calls `mboss/floor`" | **[in AZ-CM, changed]** the framework calls it after the module's `incoming` (§7.2). **Adopt**: Apep removes its own call (a second call in the same hit would overwrite `#mbFloorRaw` with the already clamped value); Apep's `framework_needs.md` ("Dropped": "the core clamps after the module `incoming`") and its plan §5 floor row assume the opposite, plan R6 / N14 bind this side |
| FN-6 | `mboss/title` | **[in AZ-CM]** §7.3 |
| FN-7 | per-entity RES on organisms | **[in AZ-CM]** §8 (`#auxResEl/#auxResElV` + `#auxRes`; or the module tags an aux `rlk_mb_resel` itself = Apep's `mbResSet`) |
| FN-8 | px schema (≤ 16, any state names), disabled proxies lose `rlk_mob`, framework click polling, flash per group | **[in AZ-CM]** §9. **Adopt**: Apep's manifest adds the two required sets `inv` (set by the framework at spawn) and `dead`; the call is the macro `px/state {set:"<name>"}` (no `px/state/<name>` files) |
| FN-9 | `cb/lose` | **[in AZ-CM]** §5.8 (`#mbLost` stays 1 through a Ronova revive, reset at the next fight) |
| FN-10 | chapter test commands, generic suites, the real-engine harness (passengers, `rotate`, block map, command counter, L18 / Lv15) | commands and suites **[in AZ-CM]** §5.9, §15; the harness is **S1-HARN's** (`S:az/harness/**`, plan §7.1), not S1-CM's: Apep's harness list is forwarded there |
| FN-11 | `cb/won`, `cb/body`, rewards | **[in AZ-CM]** §5.5, §5.6 |
| FN-12 | forceload on demand, cleanup on every path | **[in AZ-CM]** §5.4 (re-added on every gate press), §6.2, §12; arenas are cleared only by `room/remove` (`cb/remove`), not after each fight (plan R13) |
| FN-13 | husk scale 0.1 + `rlk_mb_noshield` while hidden | **[in AZ-CM]** §2.2 (`shield`), §5.5: the module toggles `rlk_mb_noshield` and calls M0's `mboss/body_scale {s}`; `#mbNoLeash` stays the module's (re-set in its `reload`) |
| FN-14 | mask safe group `mbHzSG` | **[in AZ-CM]** §13.6 (`#hzSafeG`) |
| FN-15 | ‰-of-max-HP hazards | **[AP-FW]** §13.11: one-shot `#hzPm` (‰, unset = off) + `#hzPmL` (lethal 0/1, **default 1** as Apep asks): a hazard hit routes to `pl_dot` instead of `mboss/hurt`; per-entity `mbHzPm`, `mbHzPmL`. **Adopt**: the lethal flag is `#hzPmL` (Apep's plan §5 / framework_needs say `#hzLethal`) |
| FN-16 / FN-17 | `pl_dot`, NoRx (`#hzNR`, `#pjNR`, `#mbNoRx`) | **[in AZ-CM]** §13.4 |
| FN-18 | `#pjNoDodge` | **[in AZ-CM]** §13.8 |
| FN-19 | `lockv` ignores dash samples, sprint cap | **[in AZ-CM]** §13.1 |
| FN-20 | `mv/local` | **[in AZ-CM]** §13.2. **Adopt**: outputs `#mbLf` / `#mbLs` in **milliblocks** (Apep's draft: `#mvF` / `#mvS` in tenths) |
| FN-21 | capsules per state + push-only ring "within 8 b → out to 12 b" | **[in AZ-CM]** §13.5: `push/ring {r,to,kb}` (`{r:80,to:120,kb:…}`). **Adopt**: the args are `{r,to,kb}` in tenths / ticks (Apep's draft: `{r0,r1}`) |
| FN-22 | cine | **[in AZ-CM]** §13.7; `#mbCine` refuses `mboss/hurt` (so every `hz/*` and `pj/*` hit) and `pl_dot`. The AI-clock freeze is the **module's** (the framework cannot see a module clock): Apep's AI checks `#mbCine 1` itself |
| FN-23 | music schema | **[in AZ-CM]** §10 (Apep's `"3"` key works: `ph` 1..9). **[AP-FW]** Apep's three events are random-track pools: `len` 0 or a re-pick period ≥ the longest track (6870 / 6376 / 6881 t, `L.music_len`), checked by `load_registry` (§10, change note 22.5) |
| FN-24 | `#buNoNum` (+ `#buHpCol` gold) | **[in AZ-CM]** §11 (code 10 = `#EDCF63`) |
| FN-25 | RIGLIB + park | RIGLIB stage (not S1-CM). **Open**: RIGLIB merged into main as 039b911 **without** the park flag (its commit has follow lists, `follow_y`, `fitTrack`, culling, `tol.tp`, the shape lib); Apep builds park in its own rig builder (its FN-25 fallback) or asks for a RIGLIB follow-up stage |
| FN-26 | barrier safety sweep (row spans, r ≤ walk − 0.5) | **[in AZ-CM]** §6.3. **Adopt**: the name is `arena/<aid>/sweep {y0,y1}` (not `sweep_barrier`), run by `cb/won` / `cleanup` / `cb/remove` when the arena entry has `sweep` (Apep: `{201,202}`) |
| FN-27 / FN-28 | atlas gates, probes, font allocation | I1 gate (15.5 M px, plan Q23; Apep's two-boss 15.8 M gate is Apep's integration check) / font U+E900 for Apep (fx.md §0) |
| FN-29 | aux click-shield size, HP-bar offset | **[AP-FW]** §13.12: one-shot `#auxShW` / `#auxShH` (tenths): the aux's shield made at once in that size by `aux/setup`; `#auxHbY` (tenths) at the HP-bar spawn |
| FN-30 | `mv/step_flat {spd}` | **[AP-FW]** §13.12 (`spd` in blocks, a decimal) |
| FN-31 | hit / dodge events | **[in AZ-CM]** §13.3 |
| FN-32 | fractional pj speeds | not needed (Apep) |
| FW-13 a/b | aux kinds, passengers | not in AZ-CM (Apep's own stage; ledger m2 dropped b) |
| — | `rig/park` (body park), `px` state `parked` | module + rig (a px state named `parked` with no proxies works with §9.4 as is) |

## 18. What S1-CM delivers when

1. **Commit 1** (day 1): the registry schema v2 + `mboss_lib` helpers + the `cproto` and disabled `azhdaha` entries +
   empty but valid chapter dispatch (S1-MOD branches here).
2. Chapter lifecycle (§5) + per-arena functions + sliced arena jobs + `cp_test`, then RES, floor, pools, title, music,
   bars, cleanup.
3. Proxies (§9) on cproto's stub manifest, then the helpers of §13; tests of §15 throughout.
4. CM-REVIEW → main as **AZ-CM** (chapter 1 still Raiden).

## 19. Decisions (D0, S1-CM)

1. **Azhdaha enabled flag**: `enabled:false` in AZ-CM, flipped to true by S1-MOD's first commit (reason: a chapter entry
   that is enabled without its module breaks dispatch and the pack check on main; plan R1 "enabled from their first
   stage" = the module's first stage).
2. **Arena number `n`** added to every `arenas{}` entry (stable, never reused; plaza 0); `#mbAr` = n.
3. **`oob` band** optional per arena (default cy−3 .. cy+16 as the plaza; az_cavern 198..237 for the dome).
4. **`cb/layout {id}`** keeps the plan's call signature but dispatches with literal lines through `rlk:mboss cbl`.
5. **Prep wrapper**: `cb/prep` lines call `cb/pp/<id>`, which does the generic arena prep (forceload, ensure) before the
   module's `<id>/prep` (plan's literal line pointed at the module directly; the wrapper keeps arena prep generic).
6. **Zone 1 of a chapter layout also carries `boss_id` + `cboss:1b`** (as Raiden's layout does), so our room builder
   builds it and the lz builder skips it.
7. **Gate object**: `oarg` = registry n; the gate guard requires a kind-9 zone with `zst 3` and `data.cboss`; the entering
   function sets `zst 3` (mirrors kind 15).
8. **`#mbMode` is derived from `cur.kind`** in `fight_vars` (no path can disagree).
9. **Test auto-press** polls by schedule (`test/cwait`) instead of hooking the arena job (no core ↔ arena coupling).
10. **`phases[0]` applied by the framework at spawn**; `#mbPoolPct` remembers the split for `test/level`.
11. **Floor**: framework-only call after the module `incoming` (modules never call `mboss/floor`).
12. **Proxy manifest source**: real manifest, else the module's stub manifest (same schema), else the build fails.
13. **Proxy state at spawn = `inv`**, at death = `dead` (framework); `inv:true` sets toggle `rlk_mb_inv` only through
    `rlk_mb_pxinv` (the intro's own inv is never removed by px).
14. **`px/dup` returns fail to swallow**; the shared line also skips true damage.
15. **Navia**: the redirect lives in `pellet_go`, once per pellet after the step loop (a proxy tagged `rlk_np` tags the
    body, the proxies' tags go before `nvHit`); `pellet` stays M0's text (changed by change note 20.10; was: in `pellet`,
    proxies excluded + body tagged on every step).
16. **`push/ring {r,to,kb}`**: `r` and `to` tenths (`to ≥ r`, `L.push_ring` defaults it to `r + 0.5 b`), `kb` = push
    duration in ticks (the plan's `{r:8,kb:4}` = `{r:80,to:85,kb:4}`; Apep's 8 → 12 b = `{r:80,to:120}`).
17. **`#mbPushOn` is a per-tick request** (like `#mbLowG`), so pause and every exit drop it without a reset path.
18. **`hz/extend` grows `mbHzA` too** (otherwise an extended field stops hitting at its old active end).
19. **Mask safe group** generalised (`#hzSafeG`, `mbHzSG`) for Apep FN-14; 0 = the hazard's own id (Azhdaha's case).
20. **Hit events** add `#mbHitSrc` (1 hazard, 2 pj, 3 direct) so brand rules can tell strikes from fields and swings.
21. **`lockv` buffer** skips dash ticks and caps at 280 mb/t (Apep's rule; harmless for Azhdaha).
22. **`#buNoNum` and `#buHpCol` code 10** are delivered with AZ-CM (same file, no extra owner).
23. **Arena props tag** `rlk_mb_arena_prop` + `rlk_mb_ar_<aid>` (plan §2.2's `rlk_mb_ar_az` reads as `rlk_mb_ar_az_cavern`).
24. **Music `ph`** is an int 0..9 addressing the string keys "1".."9"; `music/halt` on pause, restart on resume.
25. **cproto** = n 98, arena `cp_test` (n 9, centre 540 201 8), UUID block `…4350…`, two proxies.
26. **Reserved, not built**: `#hzVictim`, `#mbObj`, `ar/switch` (plan R3: not built). (`#hzPm/#hzPmL` (FN-15),
    `#auxShW/#auxShH/#auxHbY` (FN-29) and `mv/step_flat` (FN-30) were reserved here and are built by AP-FW, §22.)
27. **The gate never disappears**: `k_cboss` without `cprep.<id>.gate` falls back to the registry gate record (§5.4).
28. **`#cbWait`** is reset by the gate press, `start_cancel`, `cleanup_fight` and a successful spawn, never by `fight_vars`.
29. **Paused clicks are dropped every paused tick** (`px/clear_input`), and `/reload` re-spawns the proxies through
    `mboss/reload` → `px/spawn` (initial offsets from `proxies.rest`).
30. **`mbHzSG` is resolved when the mask is made** (`#hzSafeG`, else the hazard's own id); markers carry that value.
31. **Registry layout rule**: the chapter entry's first line (`enabled`, `route`) belongs to S1-MOD / VERIFY; S1-CM writes
    the measured music `len` itself on the `music` line (no request round-trip for its own file).
32. **Arlecchino audit line** (§9.6, §16): `F:char/arlecchino/skill_hit` gets one line after 22,
    `execute as @e[tag=rlk_hit,tag=rlk_mb_px] run function rlk:mboss/px/to_body` (a proxy hit by the skill puts `arDir`
    and the mark on the body once); listed in §16 since the CM fix round (change note 20.11).
33. **`F:room/obj/k_cboss_fb`** (new hand-written file, §16): the gate from the registry gate record when
    `cprep.<id>.gate` is missing (the file behind §19.27); listed in §16 since the CM fix round (change note 20.11).
34. **`F:combat/apply` proxy lines after M0 line 8** (the Raiden object line), not before it: `rlk_rd_object` never
    shares an entity with `rlk_mb_px` / `rlk_mb_big`, so the order is behaviour-equivalent, and Raiden-object hits keep
    M0's cost (change note 20.11).

35. **(AP-FW) Per-mille hazards hit through `pl_dot`** (§13.11): no defence and no level factor (Apep's numbers are
    shares of max HP), the dash still dodges unless `#hzNoDodge`, events and volley groups as `mboss/hurt`.
36. **(AP-FW) One-shot options that mid-boss code never sets are reset, not zeroed** (`#hzPm`, `#hzPmL`, `#auxShW`,
    `#auxShH`, `#auxHbY`): a mid-boss fight holds no new fake player (`test_m0diff.py`'s end-state check unchanged).
37. **(AP-FW) Shared safe groups are negative ids from `hz/safe_new`** (§13.6): the default (own id ≥ 1) and the legacy
    positive form stay; a separate number space instead of reserving hazard ids.
38. **(AP-FW) `look_<aid>` beside the stamp** (§3.3, §6.4): the stamp keeps meaning "built and finished in this look"
    (`ensure`), the record says which look the arena is in or heading to.
39. **(AP-FW) A cine refuses without consuming** (§13.7): only `#mbCine` changes the hazard / projectile flow; the other
    refusals (dead, reviving, selecting, dying boss) keep M0's consume-on-refuse.
40. **(AP-FW) Music pools: a checked re-pick period, no new runtime mode** (§10): `len` already replays the event, which
    re-picks; the registry check stops a period that would cut a track. No `music_disc` and no custom sound events.
41. **(AP-FW) Stub fallback ids ≥ 1000 are enforced, not renumbered** (§9.2): renumbering would change the ids the
    module's stub rig sets at runtime; the build fails with the clip names instead.

## 20. Change notes (CM fix round, 2026-10-20; review findings STATE-1/2/4/6/7, IDENTITY-1..7, APEP-01; recheck: APEP-03, APEP-06, APEP-09, APEP-10, PERF-1, PERF-9; merge prep: the 10-20 release, PERF-1 / PERF-2 / PERF-4)

Each note changes the sections it names (edited in place above); the plan's change-note list (`S:az/plan.md`) is the
orchestrator's to update from these.

1. **Test session state after a chapter fight** (STATE-1, IDENTITY-6; §4.1, §5.9). `test/won` decides the wording from
   the fight that ended (`cur.kind "chapter"`, always present there) and keeps `tlast.cb` in step with it; after a
   chapter fight (killed or cancelled) it runs the new `test/cwon`: `#cbForce 0`, `#cbAuto 0`, then the chapter
   wording. A cancelled gate still works without them (`cb/gate` / `cb/start` never read `#cbForce`); a kill's
   `k_chapter` leads the test session to the next chapter, whose boss map now routes as in a run. `test/defeat` takes
   `tlast.cb` from `cur` the same way when a fight is on. `test/start_ch` resets `#cbForce 0` and `#cbAuto 0` (a
   mid-boss test started from a chapter session routes every boss map as in a run).
2. **A job of the fight arena ends with the fight** (STATE-2; §12). `cb/won` (before `ar/fl_off`, per chapter arena:
   `execute if score #mbAr mb matches <n> if data storage rlk:mboss arjob{aid:"<aid>"} run function
   rlk:mboss/arena/abort`) and `mboss/cleanup` (before each `ar/<aid>/fl_off`: `execute if data storage rlk:mboss
   arjob{aid:"<aid>"} run function rlk:mboss/arena/abort`) abort it: without the forceload it could only wait 200 t,
   refuse every gate press ("준비 중") and abort anyway. The next press's `ensure` restarts the build or the look
   restore with the forceload back (`cb/g/<id>`). Apep: a fight that ends during the CS look swap (FN-3) rebuilds at
   the next press instead of stalling.
3. **A gate press ends the test auto press** (STATE-4; §5.9). Every `cb/g/<id>` sets `#cbAuto 0`; `test/cwait` stops at
   its next poll, so a gate that comes back inside the 300-t window is never pressed for the player and no time-out
   line appears mid-fight.
4. **The dev view releases its forceload** (STATE-6; §6.2 `test`, §12). `arena/<aid>/done` (once the sentinel is right)
   and `vdone` (when nothing is rebuilt) run `ar/<aid>/fl_off` while `#active room` and `#mbLive mb` are not 1 (only
   the dev view `ar/<aid>/test` runs a job outside a run); a stub arena's `rebuild` does the same at once. Entrance
   prep (always inside a run) keeps its forceload for the fight. New scratch score `#arOk mb` (`done`).
5. **Uninstall removes the chapter scratch keys** (STATE-7; §3). `mboss/uninstall` also removes `cbg`, `tch`, `pxq`,
   `arsw`.
6. **Chapter-only world lines behind one gate each** (IDENTITY-1; §4.1 `#mbPushOn`, §13.5). `mboss/world` calls the
   plaza's `ar/plaza/oob` directly (`unless score #mbAr mb matches 1..`) and runs `mboss/world_cm_pre` (chapter oob
   through `ar/oob`, the `#mbPushOn` clear, `mv/lv_sample`, `px/poll`) before `mv/all` and `mboss/world_cm_post`
   (`px/tick`, `push/capsule`, `music/tick`) after `body_tick`, each behind `#mbMode 1`. `mboss/main` is M0's text
   again (the `#mbPushOn` clear moved into `world_cm_pre`; the request semantics are unchanged: cleared before the
   module tick of every live chapter-fight tick, honoured only when set in that tick). `mv/leash`, `mv/ok`, `mv/clamp`
   hold the plaza lines inline behind one `execute if score #mbAr mb matches 1.. run return run function
   rlk:mboss/ar/<fn>` line (no dispatcher frame for a mid-boss). Measured (azsim, same seed, 1200 t, a strike every
   6 t, sim command count): proto +17.8 -> +5.5 commands per tick over M0; the four mid-bosses' traces and logs stay
   identical (`test_m0diff.py`).
7. **Boss-bar options** (IDENTITY-1, IDENTITY-3; §11). `mboss/bars` resets `#buHpCol` / `#buNoNum` and checks the
   repool ramp only in chapter fights (`mboss/bars_cm`, behind `#mbMode 1`); `bossui/draw` still resets both after
   every draw, so callers that never set them (Raiden, mid-bosses) draw the M0 line. `bossui/draw` tests the colour
   option once (`unless 1..10` -> the default run, `if 1..10` -> the new `bossui/hp_col` with the ten coloured runs):
   +15 -> +6 commands per draw (sim count) for Raiden and the mid-bosses, the drawn line byte-identical to M0.
8. **Plaza `loaded`** (IDENTITY-5; §6.2). `ar/plaza/loaded` is M0 `start`'s single test of the centre (`200 201 8`);
   chapter arenas keep the corners + centre test (every chunk since change note 18). The plaza functions are now all M0 text (README's claim), pinned by
   `ident.py` 2b.
9. **Identity and behaviour guards** (IDENTITY-2; §15.5). `ident.py` 2b also maps `marker`, `full_rim`, `box_absorb`,
   `fl_on`, `fl_off`, `loaded` to their M0 lines; 2c checks that `mv/ok`, `mv/leash`, `mv/clamp` are one chapter line
   + M0's lines; 4d pins the content of every §16 edit and new engine file (`baseline/shared_edits.diff`, rewritten
   only with `--save` after a reviewed §16 change). New `test_m0diff.py` in `run_all.sh`: the M0 archive and the tree,
   same seed, all four mid-bosses, fight / kill / cancel / pause / reload: per-tick traces, logs, end-state scores /
   entities / storage (allow-lists of the chapter-mode names), commands per tick (budget +6.5), the bossui line (budget
   +6 per draw).
10. **Navia redirect once per pellet** (IDENTITY-4; §9.6, §16, §19.15). `F:char/navia/pellet` is M0's text again (no
    AABB proxy query on each of the 24 steps); `F:char/navia/pellet_go` gets two lines after the step loop, before the
    `nvHit` count: a proxy tagged `rlk_np` tags the body (`limit=1`, counted once), the proxies' `rlk_np` goes. Same
    counting as before (the body once per pellet, proxies never). The remaining small per-mob / per-hit costs
    (`mob/shield_ensure` one self-tag test per mob per tick, `combat/apply` three self-tag tests per hit, five
    `#atkSeq` adds) are recorded in README "챕터 보스".
11. **§16 table completed** (IDENTITY-7; §16, §19.32-34). Rows for `F:char/arlecchino/skill_hit` (after 22) and
    `F:room/obj/k_cboss_fb` (new); the `F:combat/apply` proxy lines are placed after line 8 (the Raiden object line),
    as the code has them; README's table says the same.
12. **`test_chapter.py` reads every expectation from the registry under test** (APEP-01, FN-10; §15.1). creg / `#mbCN`
    = the enabled chapter entries; routing per chapter = the first `route:true` entry claiming it by ascending n
    (Raiden otherwise); the Raiden checks (2b, 14, 15g) use the first chapter no `route:true` entry claims; the
    azhdaha check follows its `enabled` flag; the route-variant check derives the expected `cb/route` lines from the
    variant registry. Green on the shipped registry and on an Apep sandbox (`apep` chapter 3 with `route` false and with
    `route` true); `test_px.py` / `test_fw_az.py` were already registry-driven.
13. **A NoRx set for a DoT is spent by it** (recheck APEP-03; §13.4). `mboss/pl_dot_end` also sets `#mbNoRx 0` (pl_dot
    never runs `element/player_hit`, so a caller's one-shot NoRx for it no longer leaks into the next direct
    `mboss/hurt`), and `cleanup_fight` clears `#mbNoRx`. `test_fw_az.py` 3j / 3k.
14. **`push/ring` without int32 overflow** (recheck APEP-06; §13.5). `push/ring` and `push/ring_start` return early when
    the offset is beyond ±32 000 mb on x or z (was ±40 000, where dx² + dz² wrapped and a far player was pushed);
    `r` is clamped to 320 and `to` to 600 tenths so the early return never cuts a ring and `ring_land`'s product stays
    inside int32. `ring_start` (a player at the centre) takes the bearing to the arena start in 4-mb units, so a start
    up to 128 b away on x / z still gives the bearing. `test_fw_az.py` 8d / 8e / 8f.
15. **Merged px manifest: clip ids unique** (recheck APEP-09; §9.2). `px_manifest` asserts that no two clips of the
    real + stub merge share an id (the px dispatch is keyed by clip id; a stub fallback clip reusing a rig id would
    silently replace that clip's proxy keys). The ≥ 1000 convention for stub ids stays the manifest author's; the
    build now fails instead of mis-dispatching.
16. **Forceload rectangles validated** (recheck PERF-9; §2.3). `load_registry` rejects an arena box over 256 chunks or
    sharing a chunk with another arena box or a fixed forceload (`FIXED_FORCELOADS`). No output changes.
17. **`px` + `shield: true` covered** (recheck APEP-10, Apep O2; §9.5). §9.5 now states the `shield: true` case;
    `test_px.py` 12 builds a registry variant of cproto with `shield: true`, `hit {2.0, 3.0}`: no `rlk_mb_noshield` on
    the body, one click shield of the `hit` size from `mob/shield_ensure`, all proxies, and one body hit for an attack
    event over a proxy and the body. No code change (the generator already honoured the field).
18. **A chapter arena is loaded when every chunk of its box is** (recheck PERF-1; §6.2). `ar/<aid>/loaded` of a chapter
    arena tests every chunk of the box (the centre first; 9 for cp_test, 36 for az_cavern, 49 for ap_oasis) instead of
    two corners and the centre: forced chunks load in no fixed order, so a build / look / verify job (`job_tick`,
    `ensure`, `mboss/start`) no longer starts on a half-loaded box (sim: 41 687 wrong cells of an ap_oasis look restore
    with 46 chunks 40 t late -> 0; vanilla model: 9 synchronous chunk loads on the server thread -> 0). The plaza's
    stays M0's single centre test.
19. **Merged with the 10-20 release** (merge prep; §1.2, §15.5). wip/az-cm merged 22ba247 (= M0 039b911 + the
    telegraph rule on Guardian / butterfly / fieldgen and the fieldgen DMG x1.5). No conflict; every output regenerated
    twice in the §1.2 order into `S:az/rp_cm` (= `rp_final10`): no difference. The suites' base moved from M0 039b911 to
    the release 22ba247: `ident.py` (default base 22ba247: the four mid-bosses' outputs, the plaza, the sources and the
    engine files equal the release's; the release changed none of the plaza / framework / engine text, so 2b / 2c /
    4d still compare against M0's text and `baseline/shared_edits.diff` is unchanged), `test_m0diff.py` (`--base`
    22ba247: the mid-boss fights against the release by behaviour), `test_fw_az.py` 13 (the bossui of 22ba247 =
    M0's). `baseline/macro.txt` takes the release's seven accepted `with storage` findings (the same lines as the shared
    `mb3/tests/baseline/macro.txt`). The chapter mode still changes no mid-boss gameplay.
20. **Releasing a chapter arena's forceload aborts its job** (PERF-2; §6.2, §12). `ar/<aid>/fl_off` of a chapter arena
    starts with `execute if data storage rlk:mboss arjob{aid:"<aid>"} run function rlk:mboss/arena/abort`, so no
    release path (a direct `ar/fl_off`, a module, a later caller) can leave a job waiting 200 t for chunks, refusing
    the gate and then forcing a full rebuild; a job of another arena is untouched. The per-arena abort lines of
    `cb/won` and `mboss/cleanup` (change note 2) are gone (the fl_off they call does it); `cb/remove` keeps its abort
    before the clears, `uninstall` its unconditional abort. The plaza's `fl_off` is M0's line. `done` / `vdone` call
    fl_off after the job ended (no abort). `test_chapter.py` 17.
21. **The player body position is read once per tick** (PERF-4; §13.2). New `mv/plpos` (above). Measured (sim, cproto
    fight, push requested, 40 live ticks): entity NBT reads of the player body per tick 6 -> 1 (`lv_sample` 2,
    `mv/local` 2, `push/capsule` 2 before), all entity NBT reads per tick 16 -> 11 (the rest: `mv/local`'s anchor and
    axis marker 4, the proxies' click polls 4, `mv/turn` 2). Scratch scores `#plG`, `#mbPlG`, `#mbPX`, `#mbPZ mb`;
    storage `plp` (removed by `uninstall`). Not changed: `px/db`'s four type-filtered `@e[type=interaction]` scans per
    tick and the anchor reads of `mv/local` (the anchor moves within the tick). `test_fw_az.py` 16.
22. **PERF-1 on the merged tree** (§6.2). Fixed by change note 18 (every chunk of the box, the centre first, early
    fail: n + 1 commands when loaded, called once per job tick / gate press / clear / sweep); `test_chapter.py` 16 runs
    for every `arenas{}` entry of the registry under test (cp_test 9 chunks, az_cavern 36).

## 21. Open items (not fixed; Apep is paused until next week)

Confirmed CM-REVIEW findings left open on purpose at the AZ-CM merge (none affects normal play or a mid-boss):

- **APEP-02** (minor): FN-15 per-mille hazards `#hzPm` / `#hzPmL` are reserved but not built (Apep O1); AP-FW or the
  next CM round builds them. **Fixed in AP-FW** (change note 22.1).
- **APEP-04** (minor, needs a design decision): mask safe groups share the hazard-id number space and have no allocator,
  so an unrelated mask whose id equals a group can match and kill that group's dome markers. Fix: a separate number
  space or an allocator (AP-FW or the next CM round). **Fixed in AP-FW** (change note 22.2: `hz/safe_new`, negative ids).
- **APEP-07** (minor, needs a design decision): a look job removes `built_<aid>` when it starts and an aborted one leaves
  no stamp, so Apep A2 cannot read the current look from the stamp. Workaround: `arjob.look` during a job, or the look
  kept in `cprep`. **Fixed in AP-FW** (change note 22.3: `look_<aid>`).
- **APEP-08** (minor, needs an answer for Apep O3): Apep's three music events are vanilla random-track pools, so no
  fixed `len` loops them; the contract keeps `len 0` (play once) until single-track events / discs / no loop is decided.
  **Answered in AP-FW** (change note 22.5): pools confirmed; `len` 0 or a re-pick period ≥ the longest track, checked.
- **APEP-11** (minor): during a cine, hazard, projectile and volley-group hits are consumed (`mbHzHit 1`, `mbPjHit 1`,
  the group marked landed) instead of only refused; the fix touches the shared hz / pj hit flow and needs a
  `test_m0diff.py` re-run. **Fixed in AP-FW** (change note 22.4; `test_m0diff.py` green).
- (APEP-03, -06, -09, -10 were fixed in the recheck, change notes 13-17; APEP-01 in change note 12. AP-FW adds the
  ≥ 1000 rule of APEP-09, change note 22.6.)
- **PERF-3** (minor, optimisation): the slice budget counts commands, not blocks, and look slices run beside the live
  fight tick.
- **PERF-5** (nit): the px clip dispatcher is a linear chain run every tick.
- **PERF-6** (nit, mostly fixed by change note 7): `bossui/draw` costs +6 sim commands per draw for Raiden and the
  mid-bosses (byte-identical line).
- **PERF-7** (nit, test infrastructure): `vcheck.py` normalises every `524c4b4d-…` UUID, so a wrong proxy UUID with that
  prefix would pass; the lint baseline keeps stale M0 lines.
- **PERF-8** (nit): `room/remove` (manual admin command) clears every loaded chapter arena in one tick.
- (PERF-1 change notes 18 / 22, PERF-2 change note 20, PERF-4 change note 21, PERF-9 change note 16 are fixed.)
- STATE / IDENTITY nits not listed above were fixed in the fix round (change notes 1-11).

## 22. Change notes (AP-FW, `wip/cm-ap` from b255669, 2026-10-21; Apep's FN gaps after AZ-CM: APEP-02, -04, -07, -08, -09, -11; FN-15, FN-29, FN-30)

Owner: Apep's AP-FW stage (plan §10, one reviewed branch for the shared framework files). Each note edits the sections
it names in place; tests: `S:az/tests_cm/test_fw_ap.py` (cproto in `cp_test`; skipped on a tree without AP-FW), every
other suite unchanged and green. Diff of `S:ap/framework_needs.md` against AZ-CM (MUST + accepted SHOULD): FN-1..14,
FN-16..24, FN-26, FN-31 delivered by AZ-CM (FN-13's husk scale via M0's `body_scale`; FN-21's "never during a mask
round / hidden state" and FN-22's AI freeze are the module's, it sets `#mbPushOn` per tick and owns its clock); gaps:
FN-15 (APEP-02), FN-14's allocator (APEP-04), FN-3's look state (APEP-07), FN-22's consume (APEP-11), FN-23's pools
(APEP-08), FN-8's fallback ids (APEP-09); CAN items FN-29 / FN-30 (Apep O1) built too. Not framework: FN-25 park (Apep
D11: its own rig builder), FN-27 atlas gates and probes (AZ I1 / Apep's integration), FN-28 font clashes (every kit
generator checks the RP's fonts), FN-10's real-engine harness (S1-HARN).

1. **Per-mille hazards** (APEP-02, FN-15; §4.1, §4.2, §13.11, §17.2). `hz/init` → `hz/init_pm` when `#hzPm ≥ 1`;
   `hz/hurt` → `hz/hurt_pm` for a hazard with `mbHzPm`; objectives `mbHzPm`, `mbHzPmL`; `L.hz_opts(pm=, pm_lethal=)`.
   `test_fw_ap` 1a-1r.
2. **Mask safe-group allocator** (APEP-04, FN-14; §4.1, §13.6). New `mboss/hz/safe_new` (`#mbSafeG` / `#mbSafeN`,
   negative); `hz/init` resolves only `#hzSafeG 0` to the own id (was `..0`), so a negative group is kept;
   `L.hz_safe_new()`, `L.hz_opts(safe_g='cur')`. The finding's repro (a default-group mask whose id equals the group)
   cannot match or kill the dome: `test_fw_ap` 2a-2i.
3. **Arena look record** (APEP-07, FN-3; §3.3, §6.4, §17.2). The arena generator writes `look_<aid>` in `build`
   (`looks[0]`), `look/<look>` (at the job start, after the busy check), `done` (`$(look)`), the stub `ensure`
   (`looks[0]`); `arena/abort` (for the aborted arena), `clear` and `uninstall` remove it. Apep A2 reads it instead of the
   stamp (also mid-CS after a /reload). `test_fw_ap` 3a-3l.
4. **A cine refuses without consuming** (APEP-11, FN-22; §13.7). First line of `hz/hurt` and `pj/hit`:
   `execute if score #mbCine mb matches 1 run return 0`; the volley group is not marked, no event, no `pj_end`.
   `test_fw_ap` 6a-6f.
5. **Music pools** (APEP-08, FN-23, Apep O3; §10, §17.2). `mboss_lib.MUSIC_TRACKS` (track lengths in ticks, sounds.json
   + .ogg granule positions of the 26.3 asset index 34; `music.end` / `music.dragon` match S1-CM's earlier
   measurement), `L.music_len(ev)`, the `load_registry` check. Apep's entry (`ap_contract.md` §0.3.6, Apep's file) may
   keep `len 0` (Apep plan §9.6 estimates every phase at ≤ 138 s = 2760 t, shorter than the shortest track of its
   pool: 6068 / 4789 / 4031 t) or use the re-pick periods 6870 / 6376 / 6881 (a long fight then never goes silent). `test_fw_ap` 4a-4e.
6. **Stub fallback ids ≥ 1000** (APEP-09, FN-8; §9.2). `px_manifest` fails when a stub clip that falls back beside a real
   rig manifest has an id below 1000 (uniqueness was checked since change note 20.15). Apep's day-0 stub
   (`S:ap/spec/stub_rig_manifest.json`) numbers its clips 0..35: fine while it is the only manifest, but AP-CORE must
   renumber it 1000 + k (as Azhdaha's stub) before a real rig manifest sits beside it. `test_fw_ap` 5a-5c.
7. **Aux presentation options and `mv/step_flat`** (FN-29, FN-30, Apep O1; §4.1, §13.12, §17.2, §19.26). New
   `aux/shield_pre`, `aux/hb_y`, `mv/step_flat`; `aux/spawn` resets the options, `aux/setup` applies them;
   `L.aux_opts()`, `L.step_flat()`. `test_fw_ap` 7a-7i (`aux/hb_y` checked as text: `execute on passengers` is beyond
   mcsim).
8. **Mid-boss cost and identity** (§15.5). Outputs of Guardian / butterfly / fieldgen / proto and the plaza unchanged
   (`ident.py`); behaviour unchanged (`test_m0diff.py`: traces, logs, end states). Commands per mid-boss tick in the sim
   (budget +6.5), AZ-CM → AP-FW alone → AP-FW + change note 22.11: proto +5.53 → +5.58 → +5.60, Guardian +4.91 → +4.96 →
   +4.98, butterfly +5.80 → +5.87 → +5.92, fieldgen +6.08 → +6.20 → +6.26 (AP-FW: two commands per hazard made, two per
   hazard hit, one per projectile hit, five per aux spawn). Little headroom is left for further mid-boss-path lines.
   Validators: 0 new findings. Gate: `run_all.sh` ALL GREEN, 40 steps (tag `apfw`), rebuilt twice without a difference.
9. **Already fixed, re-verified** (APEP-03, -06, -10): `pl_dot_end` spends `#mbNoRx` and `cleanup_fight` clears it
   (`test_fw_az` 3j / 3k), `push/ring`'s ±32 000 mb guard and clamps (`test_fw_az` 8d-8f), `px` + `shield: true`
   (`test_px` 12, §9.5); no code change.
11. **`#mbGrpL2` carried over from the Azhdaha fix round** (§15.5). `test_fw_az.py` section 17 (added by AZ FIX, FAIR-3)
    tests wip/az's shared-core commit 63a9250 ("volley groups survive a re-arming field tick (#mbGrpL2)": `grp_mark`,
    `hz/init`, `pj/launch`, `init`), so it fails on every tree from b255669. `wip/cm-ap` cherry-picks that commit unchanged
    (same patch, its own message) so the shared suite is green here and the later merge of the release (after Azhdaha
    lands) sees identical hunks.
12. **Notes for AP-CORE** (no framework change): the 양육 buff ("buffed organisms can't be damaged", user) is the
    module's `aux_hit`: `#dmg tmp 0` for a buffed organism → `aux/take` shows "면역" and takes nothing (reactions and DoTs
    come back through `aux_hit` too); organism RES Dendro 20 / rest 10 = `#auxRes 10`, `#auxResEl 7`, `#auxResElV 20`
    (`L.aux_opts` for the shield / bar); the body's `res {"7":30,"*":10}` is registry data.
