# Requests and notes from S1-ARENA (az_cavern theme, `tools/mboss_arena_az_cavern.py`, branch wip/az-arena)

Each item: what, why, exact names. Nothing here blocks S1-ARENA; the module works with the current wip/az-cm
consumer (built through it in `S:az/arenawork/cmtree`, `test_arena_az.py` green there and on wip/az-arena).

## To S1-CM (theme.md owner)

1. **theme.md §5, `clear` box format.** Say explicitly that a `clear` box is a flat int tuple
   `(x0, y0, z0, x1, y1, z1)`. Why: `build_cboss_rooms.py` (wip/az-cm 51fc332) unpacks six values, while `slices()`
   uses nested `((x0, y0, z0), (x1, y1, z1))` pairs, so the contract reads both ways. az_cavern now returns flat
   tuples (`{1: [(-6, 199, 24, 5, 230, 39)], 2: [(-10, 199, 4, 9, 230, 23)]}`); `test_arena_az.py` requires them.
2. **theme.md §6.2 / plan §2.2, broken stubs.** The plan puts 2-3 stubs (h 1-2) at r 25-27, which contradicts the
   clearance rule (no solid block below y 216 inside r 28, plan §8.1). az_cavern keeps the clearance rule: the three
   stubs (`STUBS`, compass 32 / 122 / 304) are broken drums at the wall foot, all cells beyond r 28. Needs a numbered
   plan change note (or tell S1-ARENA to move them inside if the user prefers decor over the rule).
3. **Registry `ver`.** The day-1 commit (c8000fa) and the full geometry (8540889) both stamp `az_cavern@1:default`
   with the same sentinel `(320, 195, 8) minecraft:smooth_basalt`, so a dev world built from the day-1 commit keeps its
   flat arena. Either bump `arenas.az_cavern.ver` to 2 at I1 or run `function rlk:mboss/arena/az_cavern/rebuild`
   once in such a world. Release worlds never had the day-1 build.

## To S1-FX (the kit's prop models)

4. **Prop model frames** that the arena records assume (theme.md §4.1 records). Checked against wip/az-fx d57bb8d
   (`rp_fx` models `az_kit/crystal`, `water`, `glyph_*`): they match, nothing to do unless the models change:
   - `arena_crystal/<el>`: base at the display origin, growing along local +y, at most 1 b tall per scale unit.
     Hanging records use `scale (s, -s, -s)` (a 180 deg turn about x, no mirror) and `pos` = the block tip of the
     cluster, so the crystal hangs down; `s <= tip - 216.2` keeps its tip at y >= 216 (plan §2.2). Rim records stand
     upright (`scale s`, pitch -12..-22) on alcove floors at r 28.9.
   - `water_sheet/<el>`: a horizontal 1 x 1 plane centred on the origin (scale 14 = one 14-b tile), drawn at the
     record's y 201.005, about 40 % alpha.
   - `glyph/<el>`: a vertical plane centred on the origin facing the record's yaw (yaw 180 = the plane faces -z),
     about 1 b per scale unit (records use scale 0.9); arrival glyph points sit 0.03 b in front of the stele face.
5. **Brightness.** Under the binding light layer (light[level=9] at y 206) the floor-level block light is 3-4 (9 minus
   the distance), so anything without a brightness override renders dark. The kit props already set
   `brightness {sky:15, block:15}` (d57bb8d); the rig and the decals should do the same (R3 / S1-FX).

## To S1-MOD (api.py fallback, prep)

6. **Moved points** (keys unchanged; commit 8540889): the 6 rim crystal props stand at r 28.9 (were r 29.4); the
   entrance stele is a 1-wide obelisk at x -4, so `entrance_layout()['glyphs']` = upper `(-3.5, 205.3, 15.03, 0.0)`,
   lower `(-3.5, 203.9, 15.03, 0.0)`, `stele_glow` `(-3.5, 204.6, 15.4)`. If `api.py`'s `_THEME_FALLBACK` copies these,
   refresh it (or read the module once wip/az-arena is merged).
7. `entrance_layout()` returns the optional `th` lintels `{'lb': 'minecraft:stone_bricks', 'lb2':
   'minecraft:polished_andesite'}` (theme.md §5), matching the Liyue walls of the entrance.
8. **Water sheet orientation at I1-WIRE.** `core.py arena()` (wip/az-mod d1c6e68) gives `water_sheet` records a
   `left_rotation [0.7071, 0, 0, 0.7071]` (90 deg about x), right for the vertical vanilla pane stand-in but wrong for
   the kit model, which is already a horizontal plane (`az_kit/water`: one element at y 8/16). Drop the rotation when
   the kit look replaces the stand-in item, or the 14-b tiles stand on edge. Checked: S1-MOD's generator builds with
   this theme (870 functions, the 34 prop summons, hanging crystals with scale (2.2, -2.2, -2.2)), check_mboss_pack 0.
