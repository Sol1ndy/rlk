# Day-0 contract: the arena theme-module interface (`theme.md`)

Owners: **S1-CM** (the interface, the arena generator `T:build_mboss_arena.py`, the room generator
`T:build_cboss_rooms.py`, the `cp_test` theme) and **S1-ARENA** (`T:mboss_arena_az_cavern.py`). Readers: S1-MOD
(`AZ:arena/props`, `AZ:arena/look`), S2-S (`seq.py`: the intro seal props, the B3 crater), S1-FX (prop names), Apep
(`T:mboss_arena_ap_oasis.py` uses the same interface). Binding inputs: `S:az/plan.md` §1.2 R3, §2.2-§2.3, §2.6, §5 E,
§5 B3, §8.1 (`test_arena_az.py`); `S:az/contract/cm.md` §2.3, §6. Grounded in M0 `T:build_mboss_arena.py` (the plaza:
`layout()`, `spans()`, `sentinel()`, the four-quadrant clears) and `F:room/raiden/layout` (the room record).

---------------------------------------------------------------------------------------------------

## 1. Discovery and files

- A registry arena `arenas.<aid>` names its theme: `"theme": "<theme>"` → the module `T:mboss_arena_<theme>.py`
  (`L.theme_module(theme)`). No generator edit is needed for a new theme (Apep plugs in by adding its file and its
  registry entry).
- The plaza is not a theme module (its legacy code stays inside `build_mboss_arena.py`, output byte-identical).
- A theme module is plain Python 3, **stdlib only** (it may import `mboss_lib` for `num`), deterministic (seeded noise
  only), and has **no side effects on import** (renders and tests import it). It never writes files.
- Importers: `build_mboss_arena.py` (`arena_layout`, `slices`, `look_lines`, `SENTINEL`), `build_cboss_rooms.py`
  (`entrance_layout`), the module generators (`props`, `POINTS`, `PROP_UUIDS`, and `entrance_layout()['glyphs']` /
  `['stele_glow']` for the `prep` glyph props), the tests and renderers (everything).
- **Missing module** (`L.theme_module` returns None, e.g. `az_cavern` on `wip/az-cm` and on `wip/az-mod` before it
  merges `wip/az-arena`): the arena generator writes stubs (cm.md §6.3); `build_cboss_rooms.py` still writes the full
  `room/cboss/<id>/*` set from its built-in default entrance (the recommended geometry of §5 in plain stone bricks, no
  `glyphs` / `stele_glow`) and prints a WARN, so every reference resolves and `test/chapter` works; a module generator
  uses its own copy of the §6.3 / §6.4 values (s2.md §5.1) and summons no entrance glyph props.

## 2. Interface

### 2.1 Required names

| name | type | contract |
|---|---|---|
| `THEME` | str | equals the file suffix |
| `AID` | str | the registry arena key this theme builds (one theme, one arena) |
| `SENTINEL` | `((x, y, z), 'minecraft:<block>')` | one block inside the box, never air, **identical in every look**; `ensure` tests it |
| `POINTS` | dict | named positions the module and the sequences read (§4.2); every value absolute world coordinates |
| `arena_layout(look=None)` | → `{(x, y, z): str}` | every **non-air** block of the arena box for `look` (`None` = the registry's `looks[0]`); block strings with states (`'minecraft:light[level=9]'`); every key inside the registry `box` |
| `slices()` | → `[((x0, y0, z0), (x1, y1, z1)), …]` | the build slices in build order: inclusive boxes, pairwise disjoint, their union = the registry `box` exactly, each ≤ **32 768** blocks, **≤ 40** slices |
| `props(look=None)` | → `[dict]` | the per-fight display props of that look (§4.1) |
| `entrance_layout()` | → dict | the domain entrance room (§5) |

### 2.2 Optional names

| name | contract |
|---|---|
| `look_lines(look)` | → `[[str]]`: sliced commands that turn **any** built look into `look` (one inner list = one tick). When absent the generator computes the cell diff (§3.3). Every `fill` ≤ 32 768 blocks, ≤ 8 000 commands per slice, ≤ 40 slices (Apep's own target ≤ 24) |
| `CHECK` | dict of registry values the theme was written for (`cx cy cz r walk safe box start`); the generator asserts equality when present |
| `PROP_UUIDS` | `[i0, i1, i2]`: the first three ints of a theme-owned UUID block for fixed-id props (Apep's arena-prop block `524c4b4d-4150-4100-8000-…` = `[1380731725, 1095778560, -2147483648]`). Absent = a record's `uuid` low byte lives in the boss's own block (cm.md §14). `az_cavern` has none (all its props are `uuid None`) |
| `render_hints()` | camera presets for the offline renderer (free form) |

## 3. Generator emission (S1-CM implements; S1-ARENA's test reproduces it)

`T:build_mboss_arena.py` exposes `emit(aid) -> {'build': [[cmd]], 'looks': {look: [[cmd]]}, 'clear': [cmd]}` (importable,
no file writes), used by its `main()` and by `test_arena_az.py`. Until S1-CM's generator is merged into S1-ARENA's branch,
the test carries a copy of the reference emitter below (same output).

### 3.1 Build slices (`F:mboss/arena/<aid>/s/<i>`)

For slice `i` with box `B` (from `slices()`, in order):
1. `fill <B> minecraft:air strict` (one command; `B` ≤ 32 768 blocks);
2. the blocks of `arena_layout(looks[0])` inside `B`, layer by layer (y ascending), rows by z ascending, as **row spans**
   of equal blocks along x: `fill x0 y z x1 y z <block> strict` (x0 < x1) or `setblock x y z <block> strict`;
3. the last slice ends with `function rlk:mboss/arena/<aid>/done` (stamp `built_<aid>` = `"<aid>@<ver>:<looks[0]>"`,
   sentinel check).
Every slice ≤ **8 000** commands (asserted). `strict` everywhere: no block updates, so unsupported decor (dripstone,
roots, lanterns) stays where it is placed and rim water never flows.

### 3.2 Clear (`F:mboss/arena/<aid>/clear`)

`fill <B_i> minecraft:air strict` for every slice box (only when the box is loaded) + `data remove storage rlk:mboss
built_<aid>`.

### 3.3 Looks (`F:mboss/arena/<aid>/look/<look>` + `l/<look>/<i>`)

- `look_lines(look)` when defined; else the generated diff: the cells where `arena_layout(look)` and
  `arena_layout(looks[0])` differ (a block only in one of them included), grouped by the `slices()` boxes (empty groups
  skipped), each group emitted as row spans of `arena_layout(look)` (cells that become air: `fill … minecraft:air
  strict` spans). The look `looks[0]` from another look is the same diff the other way.
- The job's last slice stamps `"<aid>@<ver>:<look>"`. `ensure` restores `looks[0]` (cm.md §6.4).
- A theme with one look (`az_cavern`: `["default"]`) has no look functions.

### 3.4 What the theme never does

No markers, no entities, no scores, no forceload, no light updates beyond the listed `light` blocks; no blocks outside
the box; no real water, glass, slabs, leaves or other light-transmitting or non-full block inside the walk disc.

## 4. Props and named points

### 4.1 `props(look)` records (per-fight display entities, spawned by the boss module)

```python
{'name': 'water_3_1',          # unique within the theme
 'kind': 'water_sheet',        # a kit prop name (fx.md §6) without the element suffix, or 'item:<item id>' for a
                               # plain vanilla item_display (cp_test; no kit needed)
 'group': 'water',             # the module's handle (az: 'water', 'crystal', 'glyph_upper', 'glyph_lower')
 'pos': (327.0, 201.005, 15.0),# absolute; floats
 'yaw': 0.0, 'pitch': 0.0,     # degrees, Minecraft convention (yaw 0 faces +z / south)
 'scale': 14.0,                # float or (sx, sy, sz)
 'el': 'fight',                # 'fight' = the module picks the look at runtime per group (az: water / crystal follow
                               # plan §2.6 geo -> leg -> tail; glyph_upper / glyph_lower show the rolled tail / leg
                               # element from the start); an int = a fixed #elem look
 'uuid': None}                 # None, or a low byte: inside PROP_UUIDS when the theme has it, else inside the boss
                               # UUID block (cm.md §14)
```

The module spawns every record as an `item_display` with tags `rlk_mb_arena_prop rlk_mb_ar_<aid> rlk_mb_<p>_ap_<group>`
(`<p>` = the boss module's tag prefix: Azhdaha `az` → `rlk_mb_az_ap_water`, reserved in s2.md §12; Apep `ap`), plus
`rlk_mb_aux` when the module wants it (Azhdaha: yes; cm.md §12 kills `rlk_mb_arena_prop` anyway), never `rlk_room`;
`brightness` as the kit prop sets it, at fight start (≥ 40 t after the forceload, guarded by "none alive"), and re-makes
them in its `reload`. A record with `uuid` is summoned with that fixed `UUID` (an entity already holding it is killed
first). **Look change** (a theme with several looks): the module calls `arena/<aid>/look/<look>`, kills
`@e[tag=rlk_mb_ar_<aid>]` and spawns `props(<look>)`; the framework never spawns or swaps props. `test_arena_az.py`
checks every `kind` against the kit manifest (`T:mboss_az_fx_manifest.json` `props`); `item:` kinds are not checked.

### 4.2 `POINTS` (az_cavern keys; other themes choose their own)

| key | value | read by |
|---|---|---|
| `spawn` | `(x, y, z, yaw)` boss spawn point (the anchor) | module `spawn` |
| `water_tiles` | 16 × `(x, y, z)` tile centres | `props()` (same values) |
| `crystals` | 16 × `(x, y, z)` crystal prop points | `props()` |
| `steles` | 8 × `(x, y, z, yaw)` carved tablets (block-built decor; centre of the carved face, yaw = the face's direction) | renders |
| `arrival_glyphs` | `{'upper': (x, y, z, yaw), 'lower': (x, y, z, yaw)}` glyph spots on the two steles at the arrival | `props()` groups `glyph_upper` / `glyph_lower` |
| `seal_steles` | 6 × `(x, y, z, yaw)` intro seal steles, r 8 around `spawn` (bearings in this file are compass bearings from the arena centre: 0 = north −z, 90 = east +x, the arrival at 180; the yaw of a centre-facing prop at bearing b is b) | `seq.py` (§5 E) |
| `seal_prism` | `(x, y, z)` the prism centre (UUID 0x80) | `seq.py` |
| `crater` | `(x, y, z)` the B3 crater prop at the floor cut (UUID 0x81) | `trans.py` (B3) |
| `motes` | `[(x, y, z)]` gold mote emitter points (≤ 12) | module ambience (optional) |

## 5. `entrance_layout()` (the domain entrance in the dungeon)

```python
{'cur': {...},                     # the rlk:room cur record (below), WITHOUT boss ids
 'blocks': {1: {(x, y, z): str}, 2: {...}},   # non-air blocks placed per zone id
 'clear': {1: [box, ...], 2: [...]},          # air boxes cleared first, each <= 32 768 blocks
 'gate': (x, y, z),                # = zone 2's (cx, cy, cz): where k_cboss stands
 'glyphs': {'upper': (x, y, z, yaw), 'lower': (x, y, z, yaw)},   # glyph prop spots on the entrance stele
 'stele_glow': (x, y, z),          # particle point for the glyph glow
 'th': {'lb': str, 'lb2': str}}    # optional: door-lintel overrides written into rlk:room th after cur (as Raiden's
                                   # layout does); absent = the chapter theme's own lintels
```

- `cur` has exactly the key sets of `F:room/raiden/layout` minus its Raiden-only `arena` record and the generator-added
  ids (`n`, `zones[]`, `doors[]`, `spawn{x,z,yaw}`, `spot{x,z}`;
  zone keys `id kind x0 z0 x1 z1 cx cz mn mx nc ncm cells by cy sd pits`; cell keys `x0 z0 x1 z1 ix0 iz0 ix1 iz1 ex0 ez0 ex1
  ez1 sx0 sz0 sx1 sz1`; door keys `a b x0 x1 z0 z1 mx mz ya yb h y0 y1 l0 l1 my tx0 tx1 tz0 tz1 tm`), following its value
  conventions (cells inside their zone, inner / entry / spawn boxes inside the cell). `build_cboss_rooms.py` adds
  `boss_id:"<id>"`, `cboss:1b` and `fn:"cboss_<id>"` to **every** zone and `boss_id` to `cur`, asserts the key sets, and
  writes `F:room/cboss/<id>/layout` (one `data modify storage rlk:room cur set value <SNBT>`).
- Zones: zone 1 = kind 0 (the first zone, the player's `spawn`), zone 2 = **kind 9** (the entrance with the gate), one
  door 1 ↔ 2. Everything inside the dungeon square x / z −64..63 and y 199..230 (the band `room/erase_cell` clears),
  each zone's blocks inside its own `x0..x1 × z0..z1`, the door opening's cells left to the door system.
- `F:room/cboss/<id>/build` (as the zone marker): the `clear` boxes and `blocks` of `zid` (absolute coordinates); for
  the kind-9 zone it ends with `execute at @s run function rlk:mboss/cb/prep` (M0's `zone_build` callers run it **as**
  the marker, not **at** it; cm.md §5.2). The glyph props are the **module's** (`<id>/prep` summons them at `glyphs` as
  `rlk_room` entities); the theme only gives the spots.
- Recommended az geometry (S1-ARENA may refine inside these bounds): zone 1 = Raiden's foyer (x −6..5, z 24..39,
  spawn (0, 33) yaw 180), the door of Raiden's layout (x −2..1, z 23..24), zone 2 = one cell x −10..9, z 4..23
  (cx 0, cz 14, cy 201); the gate at (0, 201, 14); the glyph stele 3-4 b west of the gate, its carved face south (toward
  the entering player, glyph yaw 0); upper glyph = tail element, lower = leg element (plan §2.3).

## 6. `az_cavern` (S1-ARENA; values binding from plan §2.2, §2.3, §2.6)

### 6.1 Registry values (cm.md §2.3)

Centre (320, 201, 8) (a block corner; floor blocks at y 200), `walk 28`, `safe 26`, `r 33`, box x 280..360, y 190..240,
z −32..48, start (320.5, 201, 34.5) yaw 180, `looks ["default"]`, `oob {198, 237}`, arena n 1, ver 1.

### 6.2 Layout rules (checked by `test_arena_az.py`)

| rule | value |
|---|---|
| walk disc (cell centre distance ≤ 28) at y 200 | **full opaque blocks only**: mud, packed mud, polished tuff, tuff, smooth basalt, andesite, mossy cobblestone, yellow terracotta (Geo cracks) |
| solid fill | y 192..199 under every cell with centre distance ≤ 14 (the rig sinks to y 193.5) |
| clearance | no non-air, non-`light` block with y ≤ 215 inside distance 28 (above the floor y 201..215) |
| light-transmitting blocks | none inside distance 28 at any y ≤ 200 (no glass, water, slabs, leaves, carpets, ice); real 1-deep water only in rim pools beyond 28 |
| wall | rough rock 28 < d ≤ 33 with noise; barrier cap on the wall ring as the plaza (y 208..215 where the rock does not reach) |
| dome | tuff / deepslate / smooth basalt, apex y ≈ 238, rim y ≈ 214 |
| pillars | 6 irregular pillars r 2.5-3.5 half sunk in the wall at r 29-31; 2-3 broken stubs (h 1-2) at r 25-27 (decor) |
| steles | 8 tablets 3 × 5 at r 29-30 (`POINTS['steles']`), two of them at the arrival (south) carrying `arrival_glyphs` |
| crystals | 20-30 hanging clusters, tips ≥ y 216; golden roots down the north wall |
| light | hidden `minecraft:light[level=9]` at y 206 over the disc (distance ≤ 27.5) |
| sentinel | a block of the solid fill under the centre, e.g. `((320, 195, 8), 'minecraft:smooth_basalt')` |
| fills / slices | every fill ≤ 32 768 blocks; ≤ 40 slices; ≤ 8 000 commands per slice (suggested: 13 y-slabs of 4 layers, 81 × 81 × 4 = 26 244 blocks) |

### 6.3 Props (`props('default')`, 34 records)

- 16 `water_sheet` tiles (`group 'water'`, `el 'fight'`, scale 14, pitch 0): centres x ∈ {299, 313, 327, 341},
  z ∈ {−13, 1, 15, 29}, **y 201.005** (the kit's decals sit at ≥ +0.03).
- 16 `arena_crystal` (`group 'crystal'`, `el 'fight'`) on the clusters (tips ≥ y 216) and on the rim (r 28-31).
- 2 `glyph` (`group 'glyph_upper'` / `'glyph_lower'`, `el 'fight'` = the module sets the rolled tail / leg element look)
  at `POINTS['arrival_glyphs']`.
- The seal steles and the prism are **not** in `props()` (seq.py spawns them from `POINTS`).

### 6.4 Points

`spawn` = (320.0, 201.0, 8.0, yaw 0) (the body faces south, toward the arrival); `seal_steles` 6 × r 8 around it at
bearings 30° + 60° k (none on the arrival line), facing the centre; `seal_prism` (320.0, 201.0, 8.0); `crater`
(320.0, 201.0, 8.0); `steles`, `arrival_glyphs`, `crystals`, `water_tiles` as built.

### 6.5 Day-1 flat-floor version (S1-ARENA's first commit)

The full interface with simple geometry, so S1-CM and S1-MOD can integrate on day 1: a flat polished-tuff floor at y 200
over distance ≤ 28, solid tuff y 192..199 under distance ≤ 14, a smooth-basalt wall ring 28 < d ≤ 33 up to y 214 + the
barrier cap, the light layer, the 16 + 16 + 2 props at their final positions, all `POINTS`, `SENTINEL`, `slices()` (13
slabs), and an `entrance_layout()` with the recommended zones (plain stone-brick room, a 3-high stele block). Later
commits change only blocks; the names, the points and the props keep their keys (positions may move with a note in the
commit message).

## 7. `cp_test` (S1-CM, `T:mboss_arena_cp_test.py`)

Centre (540, 201, 8), walk 11, safe 9, r 12, box x 524..556, y 196..216, z −8..24, looks `["plain", "lit"]`: a flat
smooth-stone floor at y 200 over a polished-deepslate base at y 199; `lit` swaps the ring 6 < d ≤ 10 of the floor to
`minecraft:gold_block` and the light layer (y 206) from level 9 to level 15; a 3-high stone-brick wall 11 < d ≤ 12;
`SENTINEL = ((540, 199, 8), 'minecraft:polished_deepslate')`; `POINTS = {'spawn': (540.0, 201.0, 8.0, 0.0)}`;
`props(look)` = 2 test props per look with vanilla kinds (`plain`: `item:minecraft:glass`, `lit`:
`item:minecraft:gold_block`; `group 'test'`, `el 5`, `uuid None`), so cproto's "props per look" check needs no kit on
`wip/az-cm` (S1-CM's cproto module spawns them, tag prefix `rlk_mb_cp_ap_test`); an `entrance_layout()` with a
12 × 16 foyer and a one-cell kind-9 zone (the routing test target). 2 build slices, a 1-slice generated look diff.

## 8. `ap_oasis` (Apep)

Same interface; Apep's plan §4: two looks `withered` / `lush`, `look_lines(look)` as `fill … replace` boxes in ≤ 24
slices, `props(look)` per look with fixed UUIDs in Apep's arena-prop block, the entrance from `entrance_layout()`. The
look state is read from the stamp (`built_ap_oasis`), not from a separate storage key (cm.md §17.2).

## 9. Tests (`S:az/tests_arena/test_arena_az.py`, S1-ARENA)

On the module without a game: every rule of §6.2 on `arena_layout()`; `slices()` disjoint, covering the box, ≤ 32 768
blocks each, ≤ 40; the emitter output (§3) ≤ 8 000 commands per slice and every fill ≤ 32 768; `SENTINEL` inside the box,
non-air, present in `arena_layout()`; `props()` kinds in the kit manifest (skipped with a warning before I1 when the kit
manifest is absent), water tiles at y 201.005 covering the walk disc; `POINTS` keys present, `seal_steles` at r 8 ± 0.5,
none within 20° of the arrival bearing; `entrance_layout()`: key sets, the zone / cell / door conventions, everything
inside the dungeon square and y 199..230, `gate` = zone 2 centre. Determinism: two imports give equal layouts.
Renders: top / iso views of the arena and the entrance into `S:az/arenarender/**`.

## 10. Shared edits

None for S1-ARENA (it adds one new file). S1-CM's are in cm.md §16.

## 11. Decisions (D0)

1. **`slices()` returns boxes, not commands**: the generator owns emission (spans, limits), the theme owns geometry; only
   looks may override with commands (`look_lines`, Apep's request), and the generator diffs when they do not.
2. **One theme = one arena** (`AID`); `props(look)` and `look_lines(look)` take the look (Apep), `arena_layout(look)` too.
3. **Limits**: ≤ 40 slices per job, ≤ 32 768 blocks per fill, ≤ 8 000 commands per slice (a tick budget the plan did not
   state; the 13-slab plan fits easily).
4. **Props are data**: the theme lists them, the boss module spawns them with the kit looks; tag set fixed in §4.1
   (`rlk_mb_arena_prop` is Apep's name, adopted).
5. **The generator, not the theme, stamps boss ids** on the entrance zones (`boss_id`, `cboss:1b`, `fn`), so a theme
   never needs to know which boss uses it.
6. **Glyph props are the module's** (spawned by `prep` at `glyphs`); the theme builds only the stele blocks.
7. **Seal steles, prism and crater come from `POINTS`**, not from `props()` (they belong to sequences, not to the
   fight-start prop set).
8. **Water tiles at y 201.005**, 16 tiles of 14 b on the 4 × 4 grid centred on the arena centre (plan §2.2, FEA F19 / F20).
9. **Prop tag prefix** is the module's (`rlk_mb_az_ap_<group>`), not the boss id; fixed prop UUIDs may come from a
   theme-owned block (`PROP_UUIDS`, Apep); the module, never the framework, spawns and swaps props.
10. **A missing theme never leaves a dangling reference**: stub arena functions (cm.md §6.3) and a built-in default
    entrance; module generators carry their own fallback values.
11. **`kind 'item:<id>'`** allows kit-free props (cp_test).
