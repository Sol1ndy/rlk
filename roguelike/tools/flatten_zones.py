#!/usr/bin/env python3
"""Flat zone floors (구역 높이 없앰): every zone of every room layout stands on the same floor, every door is cut at floor
level on both sides, so no zone needs a hill or a ramp to reach a door.

    python3 tools/flatten_zones.py            rewrite F:room/data + F:room/lz/* in place, print a summary
    python3 tools/flatten_zones.py --check    the same, but write nothing; exit 1 when a file would change

The room layouts (F:room/data, storage rlk:room L.*) and the zone builds (F:room/lz/<fn>_<theme>) are the output of
build/layouts3.py, which is not in this repository. That generator gave every zone a floor height `by` (0..5: floor
block y 200 + by, walls y 201..210 + by), cut each door at the higher zone's floor (door data h = the higher by,
y0 y1 l0 l1 my = 201..207 + h, wall-top marker tm = 210 + the lower by) and raised a hill (`hill_for`) in the lower zone
from its floor up to that door. This tool takes the feature out of that output and is a no-op on flat output (running
it twice changes nothing):

  F:room/data   every zone by:0 cy:201, every door h:0 y0:201 y1:205 l0:206 l1:207 my:201 tm:210.
  F:room/lz/*   a zone with by = b > 0 is lowered by b: its cell walls / light / wall top end at y 210 / 209 / 210,
                floor / wall patterns, inner terrain (gentle mounds, cliffs + ramps, rock pillars, rocks from the walls),
                pits, water, props and torches keep their place relative to the floor (wall patterns that lay below
                the raised floor are dropped), and the raised base itself (the columns up to y 200 + b) is gone.
                In front of every door that used to be higher than the zone, the hill is removed: the raised terrain
                reachable from the door's front row going only downhill (each step to a neighbour that is still above
                the zone's floor and not higher than where it comes from) - its columns, the stairs / plants / fences
                on it are dropped and the props standing on it move down onto the floor.
  Zones with by 0 and no hill are left alone, and so is everything outside the zones' own build files (lz files that
  no layout references, the chapter-boss / Raiden layouts, which are flat already).

Rerun this after regenerating with build/layouts3.py (better: give that generator by = 0 and no hill_for).
"""
import json
import re
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FN = ROOT / 'data/rlk/function/room'
DATA = FN / 'data.mcfunction'
LZ = FN / 'lz'
THEMES = (1, 2, 3, 4, 5, 7)
CAPS = {'minecraft:tuff', 'minecraft:podzol', 'minecraft:red_sand'}   # the themes' u / u2 (the terrain columns' top)
DATA_NOTE = ' (그 뒤 tools/flatten_zones.py 로 구역 높이를 없앰)'
FLAT_DOOR = 'h:0,y0:201,y1:205,l0:206,l1:207,my:201'

LAYOUT_RE = re.compile(r'^data modify storage rlk:room L\.(\w+) append value (\{.*\})$')
FILL_RE = re.compile(r'^fill (-?\d+) (-?\d+) (-?\d+) (-?\d+) (-?\d+) (-?\d+) (\S+)$')
SET_RE = re.compile(r'^setblock (-?\d+) (-?\d+) (-?\d+) (\S+)( keep)?$')
EXE_RE = re.compile(r'^execute positioned (-?\d+) (-?\d+) (-?\d+) (run function rlk:room/prop/\w+)$')


def snbt_to_json(s):
    s = re.sub(r'([{,])(\w+):', r'\1"\2":', s)
    return json.loads(re.sub(r':(-?\d+)b\b', r':\1', s))


# ------------------------------------------------------------------------------------------------------- the layouts
def load_layouts(text):
    out = []
    for ln in text.splitlines():
        m = LAYOUT_RE.match(ln)
        if m:
            out.append(snbt_to_json(m.group(2)))
    return out


def flat_data(text):
    lines = text.splitlines()
    out = []
    for i, ln in enumerate(lines):
        if i == 0 and ln.startswith('#') and DATA_NOTE not in ln:
            ln += DATA_NOTE
        m = LAYOUT_RE.match(ln)
        if m:
            rec = snbt_to_json(m.group(2))
            nz, nd = len(rec['zones']), len(rec['doors'])
            ln, kz = re.subn(r',by:\d+,cy:\d+,', ',by:0,cy:201,', ln)
            ln, kd = re.subn(r',h:\d+,y0:\d+,y1:\d+,l0:\d+,l1:\d+,my:\d+,', ',' + FLAT_DOOR + ',', ln)
            ln, kt = re.subn(r',tm:\d+\}', ',tm:210}', ln)
            assert (kz, kd, kt) == (nz, nd, nd), (m.group(1), kz, kd, kt, nz, nd)
            chk = snbt_to_json(LAYOUT_RE.match(ln).group(2))
            assert all(z['by'] == 0 and z['cy'] == 201 for z in chk['zones'])
            assert all((d['h'], d['y0'], d['y1'], d['l0'], d['l1'], d['my'], d['tm']) == (0, 201, 205, 206, 207, 201, 210)
                       for d in chk['doors'])
        out.append(ln)
    return '\n'.join(out) + ('\n' if text.endswith('\n') else '')


# ------------------------------------------------------------------------------------------------------- a zone build
def interior(z):
    s = set()
    for c in z['cells']:
        for x in range(c['ix0'], c['ix1'] + 1):
            for zz in range(c['iz0'], c['iz1'] + 1):
                s.add((x, zz))
    return s


def pit_cells(z):
    s = set()
    for p in z['pits']:
        for x in range(p['x0'], p['x1'] + 1):
            for zz in range(p['z0'], p['z1'] + 1):
                s.add((x, zz))
    return s


def rect_cells(x0, z0, x1, z1):
    return {(x, zz) for x in range(x0, x1 + 1) for zz in range(z0, z1 + 1)}


def door_front(d, inside):
    """the zone's cells right inside door d (the row against the wall opening)"""
    if d['x1'] - d['x0'] == 1:          # the opening crosses a wall plane at x (two walls thick), the door runs along z
        cells = [(x, zz) for zz in range(d['z0'], d['z1'] + 1) for x in (d['x0'] - 1, d['x1'] + 1)]
    else:
        assert d['z1'] - d['z0'] == 1, d
        cells = [(x, zz) for x in range(d['x0'], d['x1'] + 1) for zz in (d['z0'] - 1, d['z1'] + 1)]
    return [c for c in cells if c in inside]


def parse(lines):
    """[(kind, data, raw)]: kind f (fill: x0 y0 z0 x1 y1 z1 block), s (setblock: x y z block keep), e (prop), c (other)"""
    out = []
    for ln in lines:
        m = FILL_RE.match(ln)
        if m:
            v = list(map(int, m.groups()[:6]))
            x0, x1 = sorted((v[0], v[3]))
            y0, y1 = sorted((v[1], v[4]))
            z0, z1 = sorted((v[2], v[5]))
            out.append(('f', (x0, y0, z0, x1, y1, z1, m.group(7)), ln))
            continue
        m = SET_RE.match(ln)
        if m:
            out.append(('s', (int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4), m.group(5) or ''), ln))
            continue
        m = EXE_RE.match(ln)
        if m:
            out.append(('e', (int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)), ln))
            continue
        assert ln.startswith('#') or not ln.strip(), ln
        out.append(('c', None, ln))
    return out


def terrain_start(cmds, b):
    """index of the first terrain line: after the last wall-top cap (polished deepslate at y 210 + b) and its air lines"""
    k = max(i for i, (t, d, _) in enumerate(cmds) if t == 'f' and d[6] == 'minecraft:polished_deepslate')
    assert cmds[k][1][1] == cmds[k][1][4] == 210 + b, cmds[k]
    k += 1
    while k < len(cmds) and cmds[k][0] == 'f' and cmds[k][1][6] == 'minecraft:air' and cmds[k][1][1] == cmds[k][1][4] == 210 + b:
        k += 1
    return k


def columns(cmds, k0, b):
    """terrain columns from index k0: {line index: (rect, t, its line indices)}; a column = body y 201..t-1 + cap (a
    theme's u block) at t on the same rectangle, or the cap alone when t = 201"""
    cols = {}
    i = k0
    while i < len(cmds):
        t, d, _ = cmds[i]
        if t == 'f':
            x0, y0, z0, x1, y1, z1, blk = d
            nx = cmds[i + 1] if i + 1 < len(cmds) else None
            if (y0 == 201 and nx and nx[0] == 'f' and nx[1][6] in CAPS and (nx[1][0], nx[1][2], nx[1][3], nx[1][5]) == (x0, z0, x1, z1)
                    and nx[1][1] == nx[1][4] == y1 + 1):
                cols[i] = cols[i + 1] = ((x0, z0, x1, z1), y1 + 1, (i, i + 1))
                i += 2
                continue
            if y0 == y1 == 201 and blk in CAPS and b <= 1:
                cols[i] = ((x0, z0, x1, z1), 201, (i,))
        i += 1
    return cols


def heightmap(cols, z, inside, pits):
    """top block y of every interior cell off the pits: the zone's floor (200 + by) or its highest terrain column"""
    b = z['by']
    H = {c: 200 + b for c in inside if c not in pits}
    for i, (r, t, idx) in cols.items():
        if i != idx[0]:
            continue
        for c in rect_cells(*r):
            if c in H:
                H[c] = max(H[c], t)
    return H


def hills(H, z, doors):
    """the cells of the hills in front of the doors that are higher than the zone (see the module doc)"""
    b = z['by']
    base = 200 + b
    U = set()
    for d in doors:
        if d['h'] <= b:
            continue
        fr = [c for c in door_front(d, H) if H[c] > base]
        comp = set(fr)
        q = deque(fr)
        while q:
            c = q.popleft()
            for n in ((c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)):
                if n in H and n not in comp and base < H[n] <= H[c]:
                    comp.add(n)
                    q.append(n)
        U |= comp
    return U


def fill_line(x0, y0, z0, x1, y1, z1, blk):
    return f'fill {x0} {y0} {z0} {x1} {y1} {z1} {blk}'


def split_rect(r, U):
    """rectangle r minus the cells U, as rectangles (row runs along x merged down z; small and deterministic)"""
    x0, z0, x1, z1 = r
    runs = {}
    for zz in range(z0, z1 + 1):
        x = x0
        while x <= x1:
            if (x, zz) in U:
                x += 1
                continue
            s = x
            while x <= x1 and (x, zz) not in U:
                x += 1
            runs.setdefault(zz, []).append((s, x - 1))
    out, open_ = [], {}
    for zz in range(z0, z1 + 2):
        cur = set(runs.get(zz, []))
        for run in list(open_):
            if run not in cur:
                out.append((run[0], open_.pop(run), run[1], zz - 1))
        for run in sorted(cur):
            open_.setdefault(run, zz)
    return sorted(out, key=lambda q: (q[1], q[0]))


def flatten_zone(lines, z, doors, stats):
    b = z['by']
    cmds = parse(lines)
    inside = interior(z)
    pits = pit_cells(z)
    k0 = terrain_start(cmds, b)
    cols = columns(cmds, k0, b)
    H = heightmap(cols, z, inside, pits)
    U = hills(H, z, doors)
    if b == 0 and not U:
        return lines, 0
    s = 200 + b
    out = []
    done = set()
    for i, (t, d, raw) in enumerate(cmds):
        if t == 'c':
            out.append(raw)
            continue
        if i < k0:                                            # cells, floor / wall patterns, the wall top
            if t != 'f':
                raise AssertionError(('pattern section', raw))
            x0, y0, z0, x1, y1, z1, blk = d
            if y0 == y1 == 200:
                out.append(raw)
            elif y0 == y1 and rect_cells(x0, z0, x1, z1) <= inside:
                assert y0 - b >= 200, raw
                out.append(fill_line(x0, y0 - b, z0, x1, y1 - b, z1, blk))
            else:
                assert y0 >= 201, raw
                lo, hi = max(y0 - b, 201), y1 - b
                if hi >= lo:
                    out.append(fill_line(x0, lo, z0, x1, hi, z1, blk))
                else:
                    stats['wall_below'] += 1
            continue
        if i in cols:                                         # terrain columns
            r, top, idx = cols[i]
            if i in done:
                continue
            done.update(idx)
            assert top >= s, raw
            cells = rect_cells(*r)
            if top == s:
                stats['base'] += 1
                continue
            parts = [r]
            if cells & U:
                parts = split_rect(r, U)
                stats['hill'] += 1 if not parts else 0
                stats['hill_part'] += 1 if parts else 0
            for (x0, z0, x1, z1) in parts:
                if len(idx) == 2:
                    body = cmds[idx[0]][1][6]
                    if top - 1 - b >= 201:
                        out.append(fill_line(x0, 201, z0, x1, top - 1 - b, z1, body))
                cap = cmds[idx[-1]][1][6]
                out.append(fill_line(x0, top - b, z0, x1, top - b, z1, cap))
            continue
        if t == 'f':                                          # pits, water, shores, floors of houses
            x0, y0, z0, x1, y1, z1, blk = d
            cells = rect_cells(x0, z0, x1, z1)
            if y0 <= 199:
                hi = y1 - b if y1 > 200 else y1
                assert not (cells & U) or y1 <= 200, raw
                out.append(fill_line(x0, y0, z0, x1, hi, z1, blk))
            else:
                assert y0 == y1 and y0 - b >= 199, raw
                if cells & U:
                    stats['flat_on_hill'] += 1
                out.append(fill_line(x0, y0 - b, z0, x1, y1 - b, z1, blk))
            continue
        if t == 's':                                          # ramps, plants, fences, torches, sea grass
            x, y, zz, blk, keep = d
            if (x, zz) in U and y > s and not blk.startswith('minecraft:wall_torch'):
                stats['set_on_hill'] += 1
                continue
            out.append(f'setblock {x} {y - b} {zz} {blk}{keep}')
            continue
        x, y, zz, fn = d                                      # props
        if (x, zz) in U:
            stats['prop_on_hill'] += 1
            y = s + 1
        out.append(f'execute positioned {x} {y - b} {zz} {fn}')
    return out, 1


def main():
    check = '--check' in sys.argv[1:]
    text = DATA.read_text(encoding='utf-8')
    layouts = load_layouts(text)
    stats = {k: 0 for k in ('zones', 'files', 'lowered', 'hill_zones', 'base', 'hill', 'hill_part', 'wall_below',
                            'flat_on_hill', 'set_on_hill', 'prop_on_hill')}
    changed = []
    seen = set()
    for lay in layouts:
        for z in lay['zones']:
            if z['fn'] in seen:
                continue
            seen.add(z['fn'])
            stats['zones'] += 1
            doors = [d for d in lay['doors'] if z['id'] in (d['a'], d['b'])]
            hit = 0
            for th in THEMES:
                p = LZ / f"{z['fn']}_{th}.mcfunction"
                src = p.read_text(encoding='utf-8')
                lines, did = flatten_zone(src.splitlines(), z, doors, stats)
                new = '\n'.join(lines) + ('\n' if src.endswith('\n') else '')
                if new != src:
                    changed.append(p)
                    if not check:
                        p.write_text(new, encoding='utf-8')
                hit |= did
            if hit:
                stats['lowered'] += z['by'] > 0
                stats['hill_zones'] += any(d['h'] > z['by'] for d in doors)
    new = flat_data(text)
    if new != text:
        changed.append(DATA)
        if not check:
            DATA.write_text(new, encoding='utf-8')
    stats['files'] = len(changed)
    print('flatten_zones:', ' '.join(f'{k} {v}' for k, v in stats.items()))
    if check and changed:
        print('would change', len(changed), 'files')
        sys.exit(1)


if __name__ == '__main__':
    main()
