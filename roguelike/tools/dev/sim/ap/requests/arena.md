# Requests and notes from AP-ARENA (`ap_oasis` theme, `tools/mboss_arena_ap_oasis.py`, branch `wip/ap-arena`)

Protocol: `S:ap/ap_contract.md` §0.11 (append-only, `## R<stage>-<n> <type>: <title>`, what / why / needed by, status).
Nothing here blocks another stage: the theme builds through the AZ-CM generators (`wip/az-cm` 51fc332) in a throw-away
sandbox (`S:ap/tests_arena/cm_sandbox_build.sh`: arena 22 build slices + 2 × 24 look slices, `ar/ap_oasis/*`, the
`room/cboss/apep/*` entrance, lint_mc 0, check_mboss_pack 0, `test_ap_arena.py` green with the generator's `emit()`).

## RARENA-1 note: contract §0.6.7 `entrance_layout()` carries two AZ-CM details (for AP-CORE / the contract owner)

- what: the dict has the theme.md §5 keys **plus the optional `th`** door-lintel blocks
  `{'lb': 'minecraft:cut_sandstone', 'lb2': 'minecraft:mud_bricks'}` (the Sumeru `#th 5` lintels; `build_cboss_rooms.py`
  writes them after the layout, default polished blackstone); the `clear` boxes are **flat int tuples**
  `(x0, y0, z0, x1, y1, z1)` from y 199 (`{1: [(-6, 199, 24, 5, 230, 39)], 2: [(-10, 199, 4, 9, 230, 23)]}`), because
  `build_cboss_rooms.py` unpacks six values. Both as `az_cavern` (wip/az-arena 174aeef).
- why: §0.6.7 says "exactly the theme.md §5 dict"; the generator that consumes it reads `th` and flat boxes.
- needed by: AP-CORE (contract §0.12 change note), AP-I1. status: open (informational; no code change asked).

## RARENA-2 answer: O5 — `fill … replace <filter> strict` on pack format 121

- what: `lint_mc.py` accepts `fill … <block> replace <filter> strict`, but it only checks the first mode token after
  the block, so the lint proves nothing about the game's parser; no server or commands report is available offline.
  The theme therefore emits **plain `replace <filter>`** (`LOOK_STRICT = False`, one switch). Every swapped block is a
  full block, a persistent leaf, stained glass, a `light` block or a plant on an unchanged dirt-tag support, so the
  neighbour updates of a plain fill change nothing else.
- needed by: whoever measures the slices on a server (§0.6.5 "ms per slice"); flip `LOOK_STRICT` only after the game
  parses it. status: done (9a0f360).

## RARENA-3 note: the look swap (for AP-CORE / AP-REV, CS t24)

- `look_lines(look)` = **24 ticks** (both directions), 57 `fill … replace` commands: ≤ 3 commands, ≤ ~3 000 swapped
  cells and ≤ 48 000 scanned blocks per tick (`test_ap_arena.py` prints the table). Started at CS t24 it ends at t47,
  inside the white-out and before t64. The commands commute and are idempotent: any mix of the two looks (an aborted
  job, a reload mid-CS calling `look/lush` again) converges to the target.
- Swapped pairs (withered → lush), each exclusive to its cells: yellow → lime stained glass (leaf windows), pale oak →
  azalea leaves (persistent; margins, foliage, bushes, the forest curtain), pale moss block → flowering azalea leaves
  (crown clumps under the vault, y ≥ 222 only), ochre → verdant froglight (bulbs at the tree feet), dead bush → azalea,
  tall dry grass → flowering azalea, short dry grass → dandelion, leaf litter → moss carpet (bank plants), the light
  layer y 206 level 12 → 14. The floor (y ≤ 200 inside r 26) and `SENTINEL` (440, 193, 8) packed mud never change.
- status: informational.

## RARENA-4 note: registry `ver` (for AP-CORE / AP-I1)

- what: the day-1 commit (b344b18) and the full geometry (4b44cfa, 9a0f360) stamp the same `ap_oasis@1:<look>` with the
  same sentinel, so a dev world that built the day-1 arena keeps it. Either register `"ver": 1` only from the full
  geometry on (no release world ever had the day-1 build) or run `function rlk:mboss/arena/ap_oasis/rebuild` once in
  such a world. status: open.

## RARENA-5 note: prop records (for AP-FX models and AP-CORE `arena/props/<look>`)

- 64 records (`props('lush')`), 12 in `props('withered')` (the bank crystals, kept across the swap by name and UUID):
  - `water_sheet` ×16, UUID 0x00-0x0F, scale 14, pitch 0, y 201.005, z-major grid (contract §0.6.3): a horizontal
    1 × 1 plane centred on the origin (no extra rotation at spawn);
  - `lily_pad` ×20 (0x10-0x23), y 201.012 at r 22.6-25.4, scale 0.9-1.5: a flat pad centred on the origin, floating
    on the sheet (below the decal layer 201.035);
  - `bell_flower` ×10 (0x24-0x2D) on the bank lip (cell centre r 26.05-26.85, inside the barrier ring, y = the lip top
    + 1, scale 0.8-1.2) and `bulb_flower` ×6 (0x2E-0x33) behind the ring (r 28.35-29.5): standing props, **origin at the
    base**;
  - `bank_crystal` ×12 (0x40-0x4B) on the bank behind the ring (r 28.35-29.5, on the 1-3-high rocks), yaw facing the
    centre, pitch −8..−22, scale 1.1-1.8: a gold crystal spike cluster with its base at the origin, growing along +y.
- The entrance gate crystals (`entrance_layout()['glyphs']`, `crystal_w` / `crystal_e` at (±3.5, 201.0, 12.5), yaw 0)
  stand on the hall floor (the green-tile / chiseled-stud ring around the gate), origin at the base.
- status: informational (AP-FX: `prop/<kind>` frames as above).

## RARENA-6 note: no hostile spawns, lighting (for AP-CORE / AP-REVIEW)

- The pack never turns natural spawning off. The theme floods block light over both looks and puts hidden
  `light[level=15]` blocks in every still-dark spawn cell outside the disc (≈ 130: tree tops, root arches, the forest
  floor, the canopy top, the outer wall); `test_ap_arena.py` re-checks it with an independent numpy flood (0 dark spawn
  cells in either look). Nothing for the module to do.
- Floor block light under the light layer: 7 (withered, level 12) / 9 (lush, level 14); daylight reaches the floor
  through the leaf windows (stained glass) and the open shaft. Props and decals should set their own `brightness` as
  the fg / az kits do.
- status: informational.

## RARENA-7 note: constants and points the theme adds (all importable; keys of §0.6.2-§0.6.3 unchanged)

- `BARRIER_D = (26.9, 28.3)` (the barrier cells' centre-distance band, y 201..215, closed 8-connected ring), `BANK_D`
  29.6 (tree parts below `ROOT_Y` 207 stay beyond it), `LIGHT_R` 25.5 (the light layer), `LOOK_STRICT`, `LOOK_CELLS`.
- `POINTS['ember_twig']` unchanged (432.6, 203.5, −19.6): a `mangrove_roots` twig in cell (432, 203, −20) on a
  rooted-dirt bank column 2 high, cell centre r 28.5 (outside the ring cells). `POINTS['trees']` = 9 × (x, z, R) at
  r 33-36.5 (contract: 8-10 at r 30-38). `pond_props` 36, `bank_crystals` 12, `motes` 12.
- status: informational.
