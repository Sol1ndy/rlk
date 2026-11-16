#!/usr/bin/env python3
"""Domain-entrance rooms of the chapter bosses (챕터 보스 입구; AZ-CM, scratchpad az/contract/cm.md 5.2, theme.md 5).

    python3 tools/build_cboss_rooms.py

For every enabled chapter boss of tools/mboss_registry.json (kind "chapter") whose arena theme module
tools/mboss_arena_<theme>.py exists, from the theme's entrance_layout():
  F:room/cboss/<id>/layout   the boss map's room record: data modify storage rlk:room cur set value {...} (+ the door
                             lintel blocks th.lb / th.lb2); every zone carries boss_id:"<id>", cboss:1b, fn:"cboss_<id>"
  F:room/cboss/<id>/build    as a zone marker (room/zone_build): its blocks (F:room/cboss/<id>/z<k>); the kind-9 zone
                             then runs mboss/cb/prep at itself (the arena prep and the module's prep)
  F:room/cboss/build         the dispatcher on the zone's data.boss_id (literal lines)
Owns F:room/cboss/** only (stale files there are removed). A chapter boss whose theme module is missing (az_cavern
before wip/az-arena is merged) gets the full set from the built-in default entrance (theme.md 1 / 5: the recommended
geometry in plain stone bricks, no glyph spots), with a WARN line, so every reference resolves and test/chapter works.
"""
import mboss_lib as L

REG = L.load_registry()
ZONE_KEYS = {'id', 'kind', 'x0', 'z0', 'x1', 'z1', 'cx', 'cz', 'mn', 'mx', 'nc', 'ncm', 'cells', 'by', 'cy', 'sd', 'pits'}
CELL_KEYS = {'x0', 'z0', 'x1', 'z1', 'ix0', 'iz0', 'ix1', 'iz1', 'ex0', 'ez0', 'ex1', 'ez1', 'sx0', 'sz0', 'sx1', 'sz1'}
DOOR_KEYS = {'a', 'b', 'x0', 'x1', 'z0', 'z1', 'mx', 'mz', 'ya', 'yb', 'h', 'y0', 'y1', 'l0', 'l1', 'my', 'tx0', 'tx1',
             'tz0', 'tz1', 'tm'}
MAX_FILL = 32768


def snbt(v):
    if isinstance(v, bool):
        return '1b' if v else '0b'
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return L.num(v)
    if isinstance(v, str):
        return L.snbt_str(v)
    if isinstance(v, (list, tuple)):
        return '[' + ','.join(snbt(x) for x in v) + ']'
    if isinstance(v, dict):
        return '{' + ','.join(f'{k}:{snbt(x)}' for k, x in v.items()) + '}'
    raise TypeError(v)


def _cell(x0, z0, x1, z1, m=3):
    return {'x0': x0, 'z0': z0, 'x1': x1, 'z1': z1, 'ix0': x0 + 1, 'iz0': z0 + 1, 'ix1': x1 - 1, 'iz1': z1 - 1,
            'ex0': (x0 + m) * 100, 'ez0': (z0 + m) * 100, 'ex1': (x1 - m + 1) * 100, 'ez1': (z1 - m + 1) * 100,
            'sx0': x0 + m, 'sz0': z0 + m, 'sx1': x1 - m, 'sz1': z1 - m}


def _zone(zid, kind, x0, z0, x1, z1, m):
    return {'id': zid, 'kind': kind, 'x0': x0, 'z0': z0, 'x1': x1, 'z1': z1, 'cx': (x0 + x1 + 1) // 2, 'cz': (z0 + z1 + 1) // 2,
            'mn': 1, 'mx': 1, 'nc': 1, 'ncm': 0, 'cells': [_cell(x0, z0, x1, z1, m)], 'by': 0, 'cy': 201, 'sd': 0, 'pits': []}


def default_entrance():
    """The built-in entrance (theme.md 5, recommended geometry) for a chapter boss whose theme module is missing: zone 1 =
    Raiden's foyer box x -6..5, z 24..39, its door x -2..1, z 23..24, zone 2 = one kind-9 cell x -10..9, z 4..23 with the
    gate at (0, 201, 14); plain stone bricks, no glyph spots."""
    cur = {'n': 2, 'zones': [_zone(1, 0, -6, 24, 5, 39, 2), _zone(2, 9, -10, 4, 9, 23, 3)],
           'doors': [{'a': 1, 'b': 2, 'x0': -2, 'x1': 1, 'z0': 23, 'z1': 24, 'mx': 0, 'mz': 24, 'ya': 0, 'yb': 180, 'h': 0,
                      'y0': 201, 'y1': 205, 'l0': 206, 'l1': 207, 'my': 201, 'tx0': -2, 'tx1': 1, 'tz0': 24, 'tz1': 24, 'tm': 210}],
           'spawn': {'x': 0, 'z': 33, 'yaw': 180}, 'spot': {'x': 0, 'z': 33}}
    blocks = {1: {}, 2: {}}
    for zid, (x0, z0, x1, z1) in ((1, (-6, 24, 5, 39)), (2, (-10, 4, 9, 23))):
        bl = blocks[zid]
        for z in range(z0, z1 + 1):
            for x in range(x0, x1 + 1):
                bl[(x, 199, z)] = 'minecraft:polished_blackstone'
                bl[(x, 200, z)] = 'minecraft:stone_bricks'
                if x in (x0, x1) or z in (z0, z1):
                    for y in range(201, 208):
                        bl[(x, y, z)] = 'minecraft:stone_bricks'
        for z in range(z0 + 1, z1):
            for x in range(x0 + 1, x1):
                bl[(x, 218, z)] = 'minecraft:light[level=15]'
    return {'cur': cur, 'blocks': blocks, 'clear': {1: [(-6, 199, 24, 5, 230, 39)], 2: [(-10, 199, 4, 9, 230, 23)]},
            'gate': (0, 201, 14), 'th': {'lb': 'minecraft:stone_bricks', 'lb2': 'minecraft:stone_bricks'}}


def check_layout(bid, ent):
    cur = ent['cur']
    assert set(cur) >= {'n', 'zones', 'doors', 'spawn', 'spot'}, f'{bid}: cur keys {sorted(cur)}'
    zs = cur['zones']
    assert cur['n'] == len(zs) and [z['id'] for z in zs] == list(range(1, len(zs) + 1)), f'{bid}: zone ids'
    assert zs[0]['kind'] == 0 and sum(1 for z in zs if z['kind'] == 9) == 1, f'{bid}: zone 1 kind 0 and one kind-9 zone'
    for z in zs:
        assert set(z) == ZONE_KEYS, f'{bid}: zone {z["id"]} keys {sorted(set(z) ^ ZONE_KEYS)}'
        assert z['nc'] == len(z['cells']) and z['ncm'] == z['nc'] - 1, f'{bid}: zone {z["id"]} nc / ncm'
        for c in z['cells']:
            assert set(c) == CELL_KEYS, f'{bid}: cell keys {sorted(set(c) ^ CELL_KEYS)}'
            assert z['x0'] <= c['x0'] <= c['ix0'] <= c['ix1'] <= c['x1'] <= z['x1'], f'{bid}: cell x inside its zone'
            assert z['z0'] <= c['z0'] <= c['iz0'] <= c['iz1'] <= c['z1'] <= z['z1'], f'{bid}: cell z inside its zone'
        for k in ('x0', 'x1', 'z0', 'z1'):
            assert -64 <= z[k] <= 63, f'{bid}: zone {z["id"]} outside the dungeon square'
    for d in cur['doors']:
        assert set(d) == DOOR_KEYS, f'{bid}: door keys {sorted(set(d) ^ DOOR_KEYS)}'
    kz = next(z for z in zs if z['kind'] == 9)
    assert tuple(ent['gate'][:1]) + tuple(ent['gate'][2:]) == (kz['cx'], kz['cz']), f'{bid}: gate != the kind-9 zone centre'
    for zid, blocks in ent['blocks'].items():
        z = zs[zid - 1]
        for (x, y, zz) in blocks:
            assert z['x0'] <= x <= z['x1'] and z['z0'] <= zz <= z['z1'] and 199 <= y <= 230, f'{bid}: zone {zid} block {(x, y, zz)}'
    for zid, boxes in ent['clear'].items():
        for b in boxes:
            x0, y0, z0, x1, y1, z1 = flat_box(b)
            assert (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1) <= MAX_FILL, f'{bid}: zone {zid} clear box too big'


def flat_box(b):
    """A theme `clear` box as the flat int tuple (x0, y0, z0, x1, y1, z1) (theme.md 5); the nested ((x0, y0, z0),
    (x1, y1, z1)) form of `slices()` is accepted too. Corners are sorted per axis."""
    if len(b) == 2:
        b = tuple(b[0]) + tuple(b[1])
    assert len(b) == 6 and all(isinstance(v, int) for v in b), f'clear box {b!r}: six ints'
    x0, y0, z0, x1, y1, z1 = b
    return (min(x0, x1), min(y0, y1), min(z0, z1), max(x0, x1), max(y0, y1), max(z0, z1))


def span_lines(cells):
    by_y = {}
    for (x, y, z), b in cells.items():
        by_y.setdefault(y, {}).setdefault(z, []).append((x, b))
    out = []
    for y in sorted(by_y):
        for z in sorted(by_y[y]):
            row = sorted(by_y[y][z])
            start, prev, cur = row[0][0], row[0][0], row[0][1]
            for x, b in row[1:] + [(None, None)]:
                if x is not None and x == prev + 1 and b == cur:
                    prev = x
                    continue
                out.append(f'setblock {start} {y} {z} {cur} strict' if start == prev else f'fill {start} {y} {z} {prev} {y} {z} {cur} strict')
                if x is not None:
                    start, prev, cur = x, x, b
    return out


def main():
    out = L.Out(owned_dirs=['room/cboss'])
    disp = ['# GENERATED by tools/build_cboss_rooms.py: @s = a chapter-entrance zone marker (data.cboss) at room/zone_build;',
            "# its boss's own build (literal lines on data.boss_id)."]
    made = []
    for b in L.chapter_bosses(REG):
        bid = b['id']
        a = L.arena_of(b, REG)
        th = L.theme_module(a['theme'])
        if th is None or not hasattr(th, 'entrance_layout'):
            print(f'WARN theme {a["theme"]} missing: chapter boss {bid} gets the built-in default entrance')
            ent, src = default_entrance(), 'the built-in default entrance (theme module missing)'
        else:
            ent, src = th.entrance_layout(), f'tools/mboss_arena_{a["theme"]}.py entrance_layout()'
        check_layout(bid, ent)
        cur = dict(ent['cur'])
        cur['boss_id'] = bid
        cur['zones'] = [dict(z, boss_id=bid, cboss=True, fn=f'cboss_{bid}') for z in ent['cur']['zones']]
        thd = ent.get('th', {'lb': 'minecraft:polished_blackstone', 'lb2': 'minecraft:polished_blackstone'})
        order = ['n', 'boss_id', 'zones', 'doors', 'spawn', 'spot'] + [k for k in cur if k not in ('n', 'boss_id', 'zones', 'doors', 'spawn', 'spot')]
        rec = {k: cur[k] for k in order}
        out.write(f'room/cboss/{bid}/layout', [
            f'# GENERATED by tools/build_cboss_rooms.py from {src}: the boss map of {bid}',
            '# (zone 1 = the foyer, the kind-9 zone = the domain entrance with the gate; every zone carries boss_id and cboss).',
            'data modify storage rlk:room cur set value ' + snbt(rec)]
            + [f'data modify storage rlk:room th.{k} set value {L.snbt_str(v)}' for k, v in thd.items()])
        kind9 = next(z['id'] for z in cur['zones'] if z['kind'] == 9)
        build = [f'# GENERATED: @s = a zone marker of the {bid} entrance (room/zone_build): its blocks; the entrance zone then runs',
                 '# the chapter prep at itself (mboss/cb/prep: cprep, the arena forceload and sliced build, the module prep).']
        for z in cur['zones']:
            zid = z['id']
            lines = [f'# Zone {zid} of the {bid} entrance: clear boxes, then its blocks as row spans (strict: no updates).']
            lines += ['fill %d %d %d %d %d %d minecraft:air strict' % flat_box(b) for b in ent['clear'].get(zid, [])]
            lines += span_lines(ent['blocks'].get(zid, {}))
            out.write(f'room/cboss/{bid}/z{zid}', lines)
            build.append(f'execute if score @s zid matches {zid} run function rlk:room/cboss/{bid}/z{zid}')
        build.append(f'execute if score @s zid matches {kind9} at @s run function rlk:mboss/cb/prep')
        out.write(f'room/cboss/{bid}/build', build)
        disp.append(f'execute if data entity @s data{{boss_id:"{bid}"}} run return run function rlk:room/cboss/{bid}/build')
        made.append(bid)
    out.write('room/cboss/build', disp)
    removed = out.clean()
    print(f'cboss rooms: {len(made)} entrance(s) ({", ".join(made) or "none"}), {removed} stale removed.')


if __name__ == '__main__':
    main()
