#!/usr/bin/env python3
"""test_arena_hr.py: the arena theme `hr_field` 「달빛 억새밭」 (stage S1K of the 홍련 plan; HR/PLAN.md §6, §9.3).

    python3 test_arena_hr.py <worktree>/roguelike [section ...]

 1. registry = api.ARENA_SPEC = the theme CHECK; the constants the theme copies = api's; the theme names; deterministic (a
    second interpreter gives the same layouts / look jobs / DECO)
 2. the walk disc (d <= 25): y 200 flat full opaque blocks in every look (the moon palette shares); at y 201 only
    #rlk:dash_pass plants and light; nothing else above it below y 226 but the light layer (y 206); solid below
 3. the barrier is closed: at every y 201..215 no passable cell joins the walk disc to d > 27 (4-connected flood); every
    ring cell 25 < d <= 27, y 201..215 is barrier
 4. looks: all six transitions moon <-> crimson <-> dark block-exact (look_lines applied to each source look gives the
    target layout exactly; idempotent on the target); 4 real slices, `dark` with its real slices 3 t apart (index 0, 3, 6,
    9 = api.DARK_SLICES - DARK_SLICES[0]); every fill <= 32 768, <= 8 000 commands per slice, <= 40 slices; a plant and
    its support in the same slice; the generated l/<look>/<i> and s/<i> files = the emitter; the job sizes
 5. the build slices: <= 40, disjoint, covering the box, <= 32 768 blocks; <= 8 000 commands; every key in the box
 6. light (an independent flood): the walk floor >= 12 (moon, crimson) / >= 6 (dark); every other spawnable cell >= 1;
    no non-opaque path from the box faces into the dome (no sky light, no world-time dependence)
 7. plants: every plant on a valid support in every look (vanilla 26.3 tags: supports_dry_vegetation,
    supports_crimson_roots, supports_bamboo, supports_big_dripleaf, lily pads on water, carpets on a block); the
    walk's grass shares
 8. the moon: centre / bearing / elevation = api; the disc unobstructed from C and from `start` (sight lines to 49
    points of its face); no stairway within +-20 deg of its bearing; no two block masses >= 8 b tall mirrored about it
    within +-25 deg; no text display, sign or banner, no free-standing glyph column / monolith anywhere
 9. points: DECO (the moon halo 1 b before the moon face; 8 lotus on open water; the seat rock = api.SEAT_POS on the
    field, clear of grass); POINTS; api.deco() returns the theme's DECO
10. the sim build (cmsim, the shipped tree): build -> the moon layout exactly, stamp hr_field@1:moon; look/crimson runs;
    a look/dark call during it is refused (the request waits: #hrLook as the core keeps it), then runs when the job ends
    (its real slices land 3 t apart) -> dark exactly; ensure restores moon exactly
"""
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HR = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HR / 's1k/lib'))

DP = Path(sys.argv[1]).resolve()
ONLY = set(sys.argv[2:])
sys.path.insert(0, str(DP / 'tools'))
import mboss_arena_hr_field as T  # noqa: E402
import build_mboss_arena as BA  # noqa: E402
from mboss_scarlet import api as API  # noqa: E402

FAILS, NCHK = [], [0]


def check(name, ok, info=''):
    NCHK[0] += 1
    print(('ok   ' if ok else 'FAIL ') + name, info if (info and not ok) else '')
    if not ok:
        FAILS.append(name)
    return ok


REG = json.loads((DP / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
A = REG['arenas']['hr_field']
BX = A['box']
F = DP / 'data/rlk/function'
LOOKS = ('moon', 'crimson', 'dark')
LAY = {lk: T.arena_layout(lk) for lk in LOOKS}
B = 'minecraft:'
VAN = HR / 's1k/vanilla/data/minecraft/tags/block'


def want(n):
    return not ONLY or str(n) in ONLY


def bid(b):
    return b.split('[', 1)[0].replace(B, '') if b else None


def d_of(x, z):
    return math.hypot(x + 0.5 - A['cx'], z + 0.5 - A['cz'])


def bearing_of(x, z):
    return math.degrees(math.atan2(x - A['cx'], -(z - A['cz']))) % 360


def angdiff(a, b):
    return (a - b + 180) % 360 - 180


def in_box(c):
    return BX['x0'] <= c[0] <= BX['x1'] and BX['y0'] <= c[1] <= BX['y1'] and BX['z0'] <= c[2] <= BX['z1']


def tag(name, seen=None):
    """a vanilla block tag (26.3, HR/s1k/vanilla) resolved to block ids"""
    seen = seen if seen is not None else set()
    out = set()
    for v in json.loads((VAN / f'{name}.json').read_text(encoding='utf-8'))['values']:
        v = v if isinstance(v, str) else v['id']
        if v.startswith('#'):
            n = v[1:].replace(B, '')
            if n not in seen:
                seen.add(n)
                out |= tag(n, seen)
        else:
            out.add(v.replace(B, ''))
    return out


def rlk_tag(name):
    out = set()
    for v in json.loads((DP / f'data/rlk/tags/block/{name}.json').read_text(encoding='utf-8'))['values']:
        if v.startswith('#minecraft:'):
            out |= tag(v[len('#minecraft:'):])
        elif v.startswith('#'):
            out |= rlk_tag(v.split(':', 1)[1])
        else:
            out.add(v.replace(B, ''))
    return out


# light / opacity classes (vanilla: opaque full blocks stop light; leaves and water dampen it by one more; the thin
# blocks, plants, light, barrier pass it); spawning (free: no collision, no fluid)
PLANTS = {'short_dry_grass', 'tall_dry_grass', 'crimson_roots'}
FREE = {'air', 'light'} | PLANTS
THIN = ('_wall', '_stairs', '_slab', 'iron_bars', 'moss_carpet', 'lily_pad', 'big_dripleaf', 'bamboo')
DAMP = ('_leaves', 'water')
EMIT = {'ochre_froglight': 15, 'pearlescent_froglight': 15}


def opaque(b):
    if b is None:
        return False
    n = bid(b)
    return not (n in FREE or n == 'barrier' or n.endswith(THIN) or n.endswith(DAMP))


def damp(b):
    return b is not None and bid(b).endswith(DAMP)


def emits(b):
    if b.startswith(B + 'light['):
        return int(b.split('level=')[1].split(',')[0].rstrip(']'))
    return EMIT.get(bid(b), 0)


def flood(cells):
    lv = {}
    buckets = [[] for _ in range(16)]
    for c, b in cells.items():
        e = emits(b)
        if e:
            lv[c] = max(lv.get(c, 0), e)
            buckets[e].append(c)
    for L_ in range(15, 1, -1):
        for c in buckets[L_]:
            if lv.get(c) != L_:
                continue
            x, y, z = c
            for n in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
                if not in_box(n) or opaque(cells.get(n)):
                    continue
                nl = L_ - 1 - (1 if damp(cells.get(n)) else 0)
                if nl > lv.get(n, 0):
                    lv[n] = nl
                    buckets[nl].append(n)
    return lv


def spawnable(cells):
    out = []
    for (x, y, z), b in cells.items():
        if not opaque(b) or y + 2 > BX['y1']:
            continue
        f1, f2 = cells.get((x, y + 1, z)), cells.get((x, y + 2, z))
        if (f1 is None or bid(f1) in FREE) and (f2 is None or bid(f2) in FREE):
            out.append((x, y + 1, z))
    return out


WALK = [(x, z) for z in range(A['cz'] - 26, A['cz'] + 26) for x in range(A['cx'] - 26, A['cx'] + 26) if d_of(x, z) <= A['walk']]


def apply_cmds(state, cmds):
    """fill / setblock (strict) on a {cell: block} dict"""
    for c in cmds:
        t = c.split()
        if t[0] == 'setblock':
            x, y, z = map(int, t[1:4])
            if bid(t[4]) == 'air':
                state.pop((x, y, z), None)
            else:
                state[(x, y, z)] = t[4]
        elif t[0] == 'fill':
            x0, y0, z0, x1, y1, z1 = map(int, t[1:7])
            blk = t[7]
            assert len(t) == 9 and t[8] == 'strict', c
            for x in range(min(x0, x1), max(x0, x1) + 1):
                for y in range(min(y0, y1), max(y0, y1) + 1):
                    for z in range(min(z0, z1), max(z0, z1) + 1):
                        if bid(blk) == 'air':
                            state.pop((x, y, z), None)
                        else:
                            state[(x, y, z)] = blk
        else:
            raise ValueError(c)


# ================================================================================================== 1
if want(1):
    print('== 1. registry, constants, names, determinism')
    spec = {k: v for k, v in API.ARENA_SPEC.items()}
    check('1a registry arenas.hr_field = api.ARENA_SPEC = the theme CHECK', all(A.get(k) == v for k, v in spec.items())
          and all(A.get(k) == v for k, v in T.CHECK.items()) and set(T.CHECK) <= set(A), (T.CHECK, A))
    check('1b the copied constants = api (MOON_POS, MOON_BEARING / ELEV / R, SEAT_POS, LOOK_ID, DARK_SLICES, DARK_LIGHT)',
          T.MOON_POS == API.MOON_POS and (T.MOON_BEARING, T.MOON_ELEV, T.MOON_R) == (API.MOON_BEARING, API.MOON_ELEV, API.MOON_R)
          and T.SEAT_POS == API.SEAT_POS and T.LOOK_ID == API.LOOK_ID and T.DARK_SLICES == API.DARK_SLICES
          and T.DARK_LIGHT == API.DARK_LIGHT)
    names = ('THEME', 'AID', 'SENTINEL', 'POINTS', 'CHECK', 'DECO', 'slices', 'arena_layout', 'look_lines', 'props')
    check('1c the theme names', all(hasattr(T, n) for n in names) and T.THEME == T.AID == 'hr_field' and T.props() == [])
    check('1d api.theme_ready() and the look lines (request / job) are on', API.theme_ready()
          and API.arena_look('dark') == 'scoreboard players set #hrLook hr 3'
          and API.look_job('crimson') == 'function rlk:mboss/arena/hr_field/look/crimson')

    def digest():
        h = hashlib.sha1()
        for lk in LOOKS:
            h.update(json.dumps(sorted(LAY[lk].items())).encode())
            h.update(json.dumps(T.look_lines(lk)).encode())
        h.update(json.dumps(T.DECO, sort_keys=True).encode())
        return h.hexdigest()
    code = ('import sys, json, hashlib; sys.path.insert(0, sys.argv[1]); import mboss_arena_hr_field as T\n'
            'h = hashlib.sha1()\n'
            'for lk in T.LOOKS:\n'
            '    h.update(json.dumps(sorted(T.arena_layout(lk).items())).encode())\n'
            '    h.update(json.dumps(T.look_lines(lk)).encode())\n'
            'h.update(json.dumps(T.DECO, sort_keys=True).encode())\n'
            'print(h.hexdigest())')
    other = subprocess.run([sys.executable, '-c', code, str(DP / 'tools')], capture_output=True, text=True).stdout.strip()
    check('1e deterministic: a second interpreter gives the same layouts, look jobs and DECO', other == digest(), other)

# ================================================================================================== 2
if want(2):
    print('== 2. the walk disc')
    dash = rlk_tag('dash_pass')
    sh = {}
    for lk in LOOKS:
        lay = LAY[lk]
        bad_floor = [(x, z, lay.get((x, 200, z))) for x, z in WALK if not opaque(lay.get((x, 200, z)))]
        check(f'2a {lk}: every walk cell has a full opaque floor block at y 200 ({len(WALK)} cells)', not bad_floor, bad_floor[:4])
        y201 = [(x, z, lay[(x, 201, z)]) for x, z in WALK if (x, 201, z) in lay]
        bad = [c for c in y201 if bid(c[2]) not in dash or bid(c[2]) not in (PLANTS | {'light'})]
        check(f'2b {lk}: at y 201 only plants of #rlk:dash_pass and light ({len(y201)} cells)', not bad, bad[:4])
        over = [(x, y, z, lay[(x, y, z)]) for x, z in WALK for y in range(202, 226) if (x, y, z) in lay
                and not (y == T.LIGHT_Y and bid(lay[(x, y, z)]) == 'light')]
        check(f'2c {lk}: nothing over the walk below y 226 but the light layer (y 206)', not over, over[:4])
        layer = [lay.get((x, T.LIGHT_Y, z)) for x, z in WALK]
        lv = {'moon': 15, 'crimson': 15, 'dark': 6 if T.DARK_LIGHT else 15}[lk]
        check(f'2d {lk}: the light layer y 206 over every walk cell, level {lv}', all(b == f'{B}light[level={lv}]' for b in layer))
        below = [(x, y, z) for x, z in WALK for y in range(BX['y0'], 200) if not opaque(lay.get((x, y, z)))]
        check(f'2e {lk}: solid below the walk floor (y 190..199)', not below, below[:3])
        sh[lk] = {}
        for x, z in WALK:
            n = bid(lay[(x, 200, z)])
            sh[lk][n] = sh[lk].get(n, 0) + 1
    tot = len(WALK)
    share = {k: round(v / tot, 3) for k, v in sh['moon'].items()}
    check('2f moon floor shares: mycelium 70 %, pale moss 12 %, coarse dirt 10 %, tuff 8 % (+-1 %)',
          abs(share.get('mycelium', 0) - 0.70) <= 0.01 and abs(share.get('pale_moss_block', 0) - 0.12) <= 0.01
          and abs(share.get('coarse_dirt', 0) - 0.10) <= 0.01 and abs(share.get('tuff', 0) - 0.08) <= 0.01, share)
    check('2g crimson / dark floor: mycelium -> crimson nylium, pale moss -> nether wart block, coarse dirt / tuff kept',
          sh['crimson'] == sh['dark'] and sh['crimson'].get('crimson_nylium') == sh['moon'].get('mycelium')
          and sh['crimson'].get('nether_wart_block') == sh['moon'].get('pale_moss_block')
          and sh['crimson'].get('tuff') == sh['moon'].get('tuff'), sh['crimson'])

# ================================================================================================== 3
if want(3):
    print('== 3. the barrier')
    for lk in LOOKS:
        lay = LAY[lk]
        ring = [(x, z) for z in range(A['cz'] - 28, A['cz'] + 28) for x in range(A['cx'] - 28, A['cx'] + 28)
                if A['walk'] < d_of(x, z) <= T.BARRIER_R]
        holes = [(x, y, z) for x, z in ring for y in range(T.BARRIER_Y[0], T.BARRIER_Y[1] + 1) if bid(lay.get((x, y, z))) != 'barrier']
        check(f'3a {lk}: every ring cell 25 < d <= 27, y 201..215 is barrier ({len(ring)} columns)', not holes, holes[:4])
        leak = []
        for y in range(T.BARRIER_Y[0], T.BARRIER_Y[1] + 1):
            seen = {(x, z) for x, z in WALK}
            todo = list(seen)
            while todo:
                x, z = todo.pop()
                for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)):
                    if n in seen:
                        continue
                    b = lay.get((n[0], y, n[1]))
                    if b is not None and bid(b) not in FREE:
                        continue
                    seen.add(n)
                    if d_of(*n) > T.BARRIER_R + 0.01:
                        leak.append((n[0], y, n[1]))
                        todo = []
                        break
                    todo.append(n)
        check(f'3b {lk}: closed: no passable path from the walk disc past the ring at any y 201..215', not leak, leak[:3])

# ================================================================================================== 4
if want(4):
    print('== 4. looks')
    em = BA.emit('hr_field')
    lines = {lk: T.look_lines(lk) for lk in LOOKS}
    for src in LOOKS:
        for dst in LOOKS:
            st = dict(LAY[src])
            for g in lines[dst]:
                apply_cmds(st, g)
            diff = [c for c in set(st) | set(LAY[dst]) if st.get(c) != LAY[dst].get(c)]
            check(f'4a {src} -> {dst}: block-exact', not diff, [(c, st.get(c), LAY[dst].get(c)) for c in diff[:3]])
    lc = T.look_cells()
    check(f'4b the job writes every changed cell ({len(lc)} cells in the union)', len(lc) > 10000)
    for lk in LOOKS:
        gs = lines[lk]
        real = [i for i, g in enumerate(gs) if g]
        want_idx = [0, 1, 2, 3] if lk != 'dark' else [s - T.DARK_SLICES[0] for s in T.DARK_SLICES]
        check(f'4c {lk}: real slices at {real} (= {want_idx}); {len(gs)} slices <= 40', real == want_idx and len(gs) <= 40)
        nc = [len(g) for g in gs]
        big = [c for g in gs for c in g if c.startswith('fill ') and (lambda t: (abs(int(t[4]) - int(t[1])) + 1)
                                                                       * (abs(int(t[5]) - int(t[2])) + 1)
                                                                       * (abs(int(t[6]) - int(t[3])) + 1))(c.split()) > 32768]
        check(f'4d {lk}: <= 8 000 commands per slice ({nc}), every fill <= 32 768 blocks', max(nc) <= 8000 and not big)
        check(f'4e {lk}: the emitter (build_mboss_arena.emit) gives the same groups', em['looks'][lk] == gs)
        for i, g in enumerate(gs):
            p = F / f'mboss/arena/hr_field/l/{lk}/{i}.mcfunction'
            body = [ln for ln in p.read_text(encoding='utf-8').split('\n') if ln and not ln.startswith('#')]
            body = [ln for ln in body if not ln.startswith('function rlk:mboss/arena/hr_field/done')]
            if body != g:
                check(f'4f {lk}: l/{lk}/{i} = the emitter', False)
                break
        else:
            check(f'4f {lk}: the generated l/{lk}/<i> files = the emitter', True)
        print(f'   {lk}: {sum(nc)} commands in {len(real)} real slices {nc}')
    # a plant and its support change in the same slice (every source look), floor rows first
    for lk in LOOKS:
        where = {}
        for i, g in enumerate(lines[lk]):
            for c in g:
                t = c.split()
                if t[0] == 'setblock':
                    where[tuple(map(int, t[1:4]))] = i
                else:
                    x0, y0, z0, x1, y1, z1 = map(int, t[1:7])
                    for x in range(x0, x1 + 1):
                        for y in range(y0, y1 + 1):
                            for z in range(z0, z1 + 1):
                                where[(x, y, z)] = i
        split = [c for c in where if bid(LAY[lk].get(c)) in PLANTS and (c[0], c[1] - 1, c[2]) in where
                 and where[(c[0], c[1] - 1, c[2])] != where[c]]
        check(f'4g {lk}: every changing plant shares its slice with its changing support', not split, split[:3])

# ================================================================================================== 5
if want(5):
    print('== 5. build slices')
    sl = T.slices()
    vol = lambda b: (b[1][0] - b[0][0] + 1) * (b[1][1] - b[0][1] + 1) * (b[1][2] - b[0][2] + 1)  # noqa: E731
    boxv = (BX['x1'] - BX['x0'] + 1) * (BX['y1'] - BX['y0'] + 1) * (BX['z1'] - BX['z0'] + 1)
    check(f'5a {len(sl)} slices <= 40, each <= 32 768 blocks, together the box', len(sl) <= 40 and all(vol(b) <= 32768 for b in sl)
          and sum(vol(b) for b in sl) == boxv)
    em = BA.emit('hr_field')
    nc = [len(s) for s in em['build']]
    check(f'5b build slices <= 8 000 commands (max {max(nc)}, total {sum(nc)})', max(nc) <= 8000)
    files = sorted((F / 'mboss/arena/hr_field/s').glob('*.mcfunction'))
    check('5c s/<i> files = the emitter', len(files) == len(em['build']) and all(
        [ln for ln in (F / f'mboss/arena/hr_field/s/{i}.mcfunction').read_text(encoding='utf-8').split('\n')
         if ln and not ln.startswith('#') and not ln.startswith('function rlk:mboss/arena/hr_field/done')] == em['build'][i]
        for i in range(len(em['build']))))
    out = [c for lk in LOOKS for c in LAY[lk] if not in_box(c)]
    check('5d every block key inside the registry box', not out, out[:4])
    (sx, sy, sz), sb = T.SENTINEL
    check('5e the sentinel in every look', all(LAY[lk].get((sx, sy, sz)) == sb for lk in LOOKS))
    print('   blocks per slice (moon):', [sum(1 for c in LAY['moon'] if b[0][1] <= c[1] <= b[1][1]) for b in sl])

# ================================================================================================== 6
if want(6):
    print('== 6. light and the sky')
    for lk in LOOKS:
        lay = LAY[lk]
        lv = flood(lay)
        walk = [lv.get((x, 201, z), 0) for x, z in WALK]
        need = T.FLOOR_MIN[lk]
        check(f'6a {lk}: the walk floor (y 201) has block light >= {need} (min {min(walk)})', min(walk) >= need, min(walk))
        sp = [c for c in spawnable(lay) if not (c[1] == 201 and d_of(c[0], c[2]) <= A['walk'])]
        dark = [c for c in sp if lv.get(c, 0) < 1]
        check(f'6b {lk}: every other spawnable cell has block light >= 1 ({len(sp)} cells)', not dark, dark[:4])
    lay = LAY['moon']
    start = [(x, y, z) for x in (BX['x0'], BX['x1']) for y in range(BX['y0'], BX['y1'] + 1) for z in range(BX['z0'], BX['z1'] + 1)]
    start += [(x, y, z) for z in (BX['z0'], BX['z1']) for y in range(BX['y0'], BX['y1'] + 1) for x in range(BX['x0'], BX['x1'] + 1)]
    start += [(x, BX['y1'], z) for x in range(BX['x0'], BX['x1'] + 1) for z in range(BX['z0'], BX['z1'] + 1)]
    seen = set(c for c in start if not opaque(lay.get(c)))
    todo = list(seen)
    reached = []
    while todo:
        x, y, z = todo.pop()
        for n in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
            if n in seen or not in_box(n) or opaque(lay.get(n)):
                continue
            seen.add(n)
            if T._dome_in(*n):
                reached.append(n)
            todo.append(n)
    check('6c no non-opaque path from the box faces (sky / outside) into the dome', not reached, reached[:4])
    print(f'   hidden lights (level {T.HIDDEN_LV}, all looks): {len(T.hidden_lights())}')

# ================================================================================================== 7
if want(7):
    print('== 7. plants')
    SUP = {'short_dry_grass': tag('supports_dry_vegetation'), 'tall_dry_grass': tag('supports_dry_vegetation'),
           'crimson_roots': tag('supports_crimson_roots'), 'bamboo': tag('supports_bamboo') | {'bamboo'},
           'big_dripleaf': tag('supports_big_dripleaf')}
    for lk in LOOKS:
        lay = LAY[lk]
        bad, n = [], 0
        for (x, y, z), b in lay.items():
            name = bid(b)
            below = bid(lay.get((x, y - 1, z)))
            if name in SUP:
                n += 1
                if below not in SUP[name]:
                    bad.append(((x, y, z), name, below))
            elif name == 'lily_pad':
                n += 1
                if below != 'water':
                    bad.append(((x, y, z), name, below))
            elif name == 'moss_carpet':
                n += 1
                if below is None or below in FREE:
                    bad.append(((x, y, z), name, below))
        check(f'7a {lk}: every plant ({n}) on a valid support (vanilla 26.3 tags)', not bad, bad[:4])
        water = [(c, b) for c, b in lay.items() if bid(b) == 'water']
        flow = [c for c, _b in water for q in ((c[0] + 1, c[1], c[2]), (c[0] - 1, c[1], c[2]), (c[0], c[1], c[2] + 1),
                                               (c[0], c[1], c[2] - 1), (c[0], c[1] - 1, c[2]))
                if lay.get(q) is None or bid(lay.get(q)) in FREE]
        check(f'7b {lk}: the pond water ({len(water)} cells) cannot flow (water / solid round and below)', not flow, flow[:3])
    myc = [(x, z) for x, z in WALK if bid(LAY['moon'][(x, 200, z)]) == 'mycelium']
    short = sum(1 for x, z in myc if bid(LAY['moon'].get((x, 201, z))) == 'short_dry_grass')
    tall = sum(1 for x, z in myc if bid(LAY['moon'].get((x, 201, z))) == 'tall_dry_grass')
    other = [(x, z) for x, z in WALK if bid(LAY['moon'].get((x, 201, z))) in PLANTS and (x, z) not in set(myc)]
    check(f'7c the walk grass: short dry grass on 25 % and tall on 12 % of the mycelium cells only ({short}, {tall} of {len(myc)})',
          abs(short / len(myc) - 0.25) <= 0.01 and abs(tall / len(myc) - 0.12) <= 0.01 and not other, (short, tall, other[:3]))

# ================================================================================================== 8
if want(8):
    print('== 8. the moon, the composition')
    mx, my, mz = T.MOON_POS
    cx, cz = A['cx'], A['cz']
    br = math.degrees(math.atan2(mx - cx, -(mz - cz))) % 360
    el = math.degrees(math.atan2(my - A['cy'], math.hypot(mx - cx, mz - cz)))
    mc = T.moon_cells()
    check(f'8a the moon disc: centre api.MOON_POS, bearing {br:.1f} ~ 12, elevation {el:.1f} ~ 22, r 5, facing south',
          abs(br - API.MOON_BEARING) < 0.5 and abs(el - API.MOON_ELEV) < 0.6 and len(mc) >= 70
          and all(c[2] == T.MOON_Z for c in mc) and T.MOON_Z + 1 == mz)
    for lk in LOOKS:
        lay = LAY[lk]
        blocked = []
        for eye_name, eye in (('C', (cx, A['cy'] + 1.62, cz)), ('start', (A['start']['x'], A['start']['y'] + 1.62, A['start']['z']))):
            for i in range(-3, 4):
                for j in range(-3, 4):
                    tx, ty = mx + i * 4.6 / 3 * (1 if abs(i) < 3 else 0.97), my + j * 4.6 / 3
                    if math.hypot(tx - mx, ty - my) > 4.7:
                        continue
                    tgt = (tx, ty, mz + 0.001)
                    v = [tgt[k] - eye[k] for k in range(3)]
                    n = math.sqrt(sum(a * a for a in v))
                    steps = int(n / 0.05)
                    for s in range(1, steps):
                        p = [eye[k] + v[k] * s / steps for k in range(3)]
                        c = (math.floor(p[0]), math.floor(p[1]), math.floor(p[2]))
                        if c in mc:
                            break
                        b = lay.get(c)
                        if b is not None and bid(b) not in ('air', 'light', 'barrier'):
                            blocked.append((eye_name, (round(tx, 1), round(ty, 1)), c, bid(b)))
                            break
        check(f'8b {lk}: the moon disc unobstructed from C and from start (sight lines to its face)', not blocked, blocked[:4])
    lay = LAY['moon']
    stairs = {c: b for c, b in lay.items() if bid(b).endswith('_stairs')}
    fac = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}
    runs = []
    for (x, y, z), b in stairs.items():
        if abs(angdiff(bearing_of(x + 0.5, z + 0.5), API.MOON_BEARING)) > 20 or 'half=top' in b:
            continue
        f = fac[b.split('facing=')[1].split(',')[0]]
        n, cx_, cy_, cz_ = 1, x, y, z
        while True:
            q = (cx_ + f[0], cy_ + 1, cz_ + f[1])
            if q in lay and (opaque(lay[q]) or bid(lay[q]).endswith('_stairs')):
                n += 1
                cx_, cy_, cz_ = q
            else:
                break
        if n >= 3:
            runs.append((x, y, z))
    check('8c no stairway (>= 3 rising steps) within +-20 deg of the moon bearing', not runs, runs[:3])
    # block masses above the ground (not the dome, the moon, the ground, plants, light, barrier)
    tops = T._build()[3]
    dome = {c for c, v in T.base_markers().items() if v[0] in ('sky', 'skin')}
    cand = {c for c, b in lay.items() if c[1] > tops.get((c[0], c[2]), 200) and c not in dome and c not in mc
            and bid(b) not in FREE | {'barrier', 'water'} and T._dome_in(*c) and d_of(c[0], c[2]) > A['walk']}
    masses, seen = [], set()
    for c in sorted(cand):
        if c in seen:
            continue
        comp, todo = [], [c]
        seen.add(c)
        while todo:
            x, y, z = todo.pop()
            comp.append((x, y, z))
            for n in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
                if n in cand and n not in seen:
                    seen.add(n)
                    todo.append(n)
        h = max(p[1] for p in comp) - min(tops.get((p[0], p[2]), 200) for p in comp)
        brs = [angdiff(bearing_of(p[0] + 0.5, p[2] + 0.5), API.MOON_BEARING) for p in comp]
        masses.append((h, min(brs), max(brs), len(comp)))
    tall = [m for m in masses if m[0] >= 8 and m[1] <= 25 and m[2] >= -25]
    pairs = [(a, b) for i, a in enumerate(tall) for b in tall[i + 1:]
             if (a[2] < 0 < b[1] or b[2] < 0 < a[1]) and max(a[1], -b[2]) <= min(a[2], -b[1]) + 6]
    check(f'8d no two block masses >= 8 b tall mirrored about the moon bearing within +-25 deg ({len(tall)} tall masses touch the '
          f'sector)', not pairs, pairs[:2])
    words = ('sign', 'banner', 'lectern', 'text', 'glyph', 'item_frame', 'map')
    texty = sorted({bid(b) for lk in LOOKS for b in LAY[lk].values() if any(w in bid(b) for w in words)})
    cols = []
    for (x, z), top in tops.items():
        run, last = 0, None
        for y in range(top + 1, 230):
            b = lay.get((x, y, z))
            n = bid(b)
            if b is not None and opaque(b) and not n.endswith(('_log', '_leaves')) and (x, y, z) not in dome and (x, y, z) not in mc:
                run = run + 1 if n == last else 1
                last = n
                free_side = sum(1 for q in ((x + 1, y, z), (x - 1, y, z), (x, y, z + 1), (x, y, z - 1)) if lay.get(q) is None)
                if run >= 6 and free_side >= 3:
                    cols.append((x, y, z, n))
                    break
            else:
                run, last = 0, None
    check('8e no sign / banner / text block, no free-standing glyph column or monolith (>= 6 b of one stone block)',
          not texty and not cols, (texty, cols[:3]))

# ================================================================================================== 9
if want(9):
    print('== 9. points')
    D = T.DECO
    lay = LAY['moon']
    check('9a api.deco() returns the theme DECO (same shape as DECO_DEFAULT)', API.deco() is T.DECO
          and set(D) == set(API.DECO_DEFAULT) and len(D['lotus']) == len(API.DECO_DEFAULT['lotus']) == 8)
    hx, hy, hz = D['moon_halo']
    check('9b the moon halo 1 b before the moon face (south of it, on the moon axis), in open air',
          (hx, hy) == (T.MOON_POS[0], T.MOON_POS[1]) and hz == T.MOON_POS[2] + 1.0
          and (math.floor(hx), math.floor(hy), math.floor(hz)) not in lay
          and (math.floor(hx), math.floor(hy), math.floor(hz) - 2) in T.moon_cells())
    bad = []
    cells = set()
    for x, y, z in D['lotus']:
        c = (math.floor(x), math.floor(z))
        cells.add(c)
        ok = y == A['cy'] - 0.1 and all(bid(lay.get((c[0] + dx, 200, c[1] + dz))) == 'water' for dx in (-1, 0, 1) for dz in (-1, 0, 1)) \
            and (c[0], 201, c[1]) not in lay and d_of(*c) > T.BARRIER_R
        if not ok:
            bad.append((x, y, z))
    check('9c 8 lotus points on open pond water (the cell and its 8 neighbours water, nothing above), distinct, outside the ring',
          not bad and len(cells) == 8, bad)
    sx, sy, sz = D['seat_rock']
    near = [(x, z) for x, z in WALK if math.hypot(x + 0.5 - sx, z + 0.5 - sz) <= T.SEAT_CLEAR
            and bid(lay.get((x, 201, z))) in PLANTS]
    check('9d the seat rock = api.SEAT_POS on the field (walk disc, solid floor), clear of grass',
          D['seat_rock'] == API.SEAT_POS and d_of(math.floor(sx), math.floor(sz)) <= A['walk'] - 1
          and opaque(lay.get((math.floor(sx), 200, math.floor(sz)))) and not near, near)
    P = T.POINTS
    check('9e POINTS: centre / spawn = C, start = the registry start, moon = api.MOON_POS, seat facing the moon',
          P['spawn'][:3] == (880.0, 201.0, 8.0) and P['start'] == (A['start']['x'], A['start']['y'], A['start']['z'], A['start']['yaw'])
          and P['moon'][:3] == API.MOON_POS and P['seat'][:3] == API.SEAT_POS)

# ================================================================================================== 10
if want(10):
    print('== 10. the sim build / looks / the waiting request / restore (cmsim, the shipped tree)')
    import cmsim as M  # noqa: E402
    s, pl = M.setup(DP)
    M.PLAYER_LOAD[0] = 0
    C0 = M.C0
    s.call('rlk:mboss/ar/hr_field/fl_on', C0)
    M.run(s, 5)

    def world_of(s):
        return {k: v for k, v in s.blocks.items() if in_box(k)}

    def norm(lay):
        return {k: bid(v) + (('[' + v.split('[', 1)[1]) if '[' in v else '') for k, v in lay.items()}

    def run_job(limit=80, each=None):
        n = 0
        while (M.mb(s, '#mbArBuild') or 0) > 0 and n < limit:
            if each:
                each(n)
            M.world(s)
            n += 1
        return n
    s.call('rlk:mboss/arena/hr_field/build', C0)
    n = run_job(200)
    st = s.storage.get('rlk:mboss', {})
    w = world_of(s)
    NM = norm(LAY['moon'])
    diff = [c for c in set(w) | set(NM) if w.get(c) != NM.get(c)]
    check(f'10a the build job ({n} ticks) leaves the moon layout exactly; stamp hr_field@1:moon', not diff
          and st.get('built_hr_field') == 'hr_field@1:moon', (len(diff), [(c, w.get(c), NM.get(c)) for c in diff[:3]]))
    # the core's request: #hrLook hr keeps the wanted look; a job starts at the first tick with #mbArBuild 0
    req = {'look': None}
    started = []

    def core_tick(k):
        if req['look'] and (M.mb(s, '#mbArBuild') or 0) == 0:
            r = s.call(f'rlk:mboss/arena/hr_field/look/{req["look"]}', C0)
            if r:
                started.append((k, req['look']))
                req['look'] = None
    s.call('rlk:mboss/arena/hr_field/look/crimson', C0)
    r = s.call('rlk:mboss/arena/hr_field/look/dark', C0)
    check('10b a look call while a job runs is refused (the job keeps running)', not r and s.storage['rlk:mboss']['arjob']['look']
          == 'crimson')
    req['look'] = 'dark'
    ticks, last = [], {}

    def watch(k):
        core_tick(k)
        i = s.storage.get('rlk:mboss', {}).get('arjob', {}).get('i')
        if i is not None:
            last[k] = i
    n = 0
    for k in range(80):
        watch(k)
        before = dict(world_of(s))
        M.world(s)
        after = world_of(s)
        if before != after:
            ticks.append(k)
        if (M.mb(s, '#mbArBuild') or 0) == 0 and not req['look'] and k > 2:
            n = k
            break
    w = world_of(s)
    ND = norm(LAY['dark'])
    diff = [c for c in set(w) | set(ND) if w.get(c) != ND.get(c)]
    check(f'10c the request waits for the crimson job, then runs: dark exactly (started at {started})', not diff and started
          and started[0][1] == 'dark' and s.storage['rlk:mboss'].get('built_hr_field') == 'hr_field@1:dark',
          (len(diff), [(c, w.get(c), ND.get(c)) for c in diff[:3]]))
    dark_ticks = [t for t in ticks if t >= started[0][0]] if started else []
    gaps = [b - a for a, b in zip(dark_ticks, dark_ticks[1:])]
    check(f'10d the dark job changes the world on 4 ticks 3 t apart ({dark_ticks})', len(dark_ticks) == 4 and gaps == [3, 3, 3])
    r = s.call('rlk:mboss/arena/hr_field/ensure', C0)
    n = run_job(50)
    w = world_of(s)
    diff = [c for c in set(w) | set(NM) if w.get(c) != NM.get(c)]
    check(f'10e ensure (the next prep) restores moon with the look job ({n} ticks), not a rebuild; then ensure returns 1',
          not r and not diff and s.storage['rlk:mboss'].get('built_hr_field') == 'hr_field@1:moon'
          and s.call('rlk:mboss/arena/hr_field/ensure', C0) == 1, len(diff))
    M.PLAYER_LOAD[0] = 96

print(f'test_arena_hr: {NCHK[0] - len(FAILS)}/{NCHK[0]} passed' + (f', {len(FAILS)} FAILED: {FAILS}' if FAILS else ''))
sys.exit(1 if FAILS else 0)
