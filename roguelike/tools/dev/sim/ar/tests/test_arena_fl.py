#!/usr/bin/env python3
"""test_arena_fl.py: the arena theme `fl_ruins` (S1 of the 아를레키노 plan; scratchpad ar/PLAN.md §8, §11.3; theme.md).

    python3 test_arena_fl.py <worktree>/roguelike [section ...]

 1. registry = api.ARENA_SPEC = the theme CHECK; the theme names (THEME AID SENTINEL POINTS CHECK slices arena_layout
    props look_lines entrance_layout); deterministic (a second interpreter gives the same layouts / look jobs / entrance)
 2. the walk disc (d <= 26): y 200 full opaque blocks of the plaza palette, identical in both looks; nothing above it
    below y 226 but the light layer (y 206, level 15, over every walk cell); solid below (y 190..199)
 3. the barrier is closed: at every y 201..216 no passable cell joins the walk disc to d > 27.6 (4-connected flood);
    the ring holds a barrier or a balustrade block in every cell 26 < d <= 27.6, y 201..216
 4. both looks reachable and reversible: look_lines applied (fill replace / fill / setblock semantics) turn the day
    layout into crimson and back, idempotent on the target look; the generated l/<look>/<i> files = the emitter; <= 4
    slices, every fill <= 32 768 blocks, <= 8 000 commands; the job size (cells changed, cells scanned)
 5. the build slices: <= 40, disjoint, covering the box, <= 32 768 blocks each; s/<i> <= 8 000 commands, every fill
    <= 32 768; every block key inside the box (= the spec)
 6. light: an independent block-light flood of each look: every spawnable cell inside the dome >= 12, the walk floor
    >= 10 (the y-206 layer's maximum), every spawnable cell outside the dome >= 1; no world-time dependence: no
    non-opaque path from the box faces (the sky) into the dome
 7. points: the wisp posts at bearings 0 / 150 / 210, r 28, outside the barrier ring, on a post; spawn / start / moon
 8. the sim build (cmsim, the shipped tree): forceload + arena/fl_ruins/build -> the day layout exactly in the block
    world, the sentinel, the stamp; look/crimson -> the crimson layout exactly; ensure restores day exactly
 9. the entrance: build_cboss_rooms.check_layout, zones / door / gate, the gravestone, the flame point above it, the gate
    column free, blocks inside their zones and y 199..230, clear boxes <= 32 768; the generated room/cboss/arlecchino
    files in a variant with the entry enabled
"""
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE / 'lib'))
import cmsim as M  # noqa: E402
import knsim as K  # noqa: E402

DP = Path(sys.argv[1]).resolve()
ONLY = set(sys.argv[2:])
sys.path.insert(0, str(DP / 'tools'))
import mboss_lib as L  # noqa: E402
import mboss_arena_fl_ruins as T  # noqa: E402
import build_mboss_arena as BA  # noqa: E402
import build_cboss_rooms as BR  # noqa: E402
import mboss_arlecchino.api as API  # noqa: E402

check = M.check
REG = json.loads((DP / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
A = REG['arenas']['fl_ruins']
BX = A['box']
F = DP / 'data/rlk/function'
LOOKS = ('day', 'crimson')
LAY = {lk: T.arena_layout(lk) for lk in LOOKS}
B = 'minecraft:'


def want(n):
    return not ONLY or str(n) in ONLY


def bid(b):
    return b.split('[', 1)[0].replace(B, '')


def d_of(x, z):
    return math.hypot(x + 0.5 - A['cx'], z + 0.5 - A['cz'])


def in_box(c):
    return BX['x0'] <= c[0] <= BX['x1'] and BX['y0'] <= c[1] <= BX['y1'] and BX['z0'] <= c[2] <= BX['z1']


# light / opacity classes by block id (vanilla): what passes block light, what a mob may spawn on / in
TRANSPARENT = ('air', 'light', 'barrier', 'short_grass', 'cornflower', 'allium', 'azure_bluet', 'oxeye_daisy',
               'lily_of_the_valley', 'lilac')
FREE = ('air', 'light', 'short_grass', 'cornflower', 'allium', 'azure_bluet', 'oxeye_daisy', 'lily_of_the_valley', 'lilac')
EMIT = {'shroomlight': 15}


def opaque(b):
    if b is None:
        return False
    n = bid(b)
    return not (n in TRANSPARENT or n.endswith(('_leaves', '_stained_glass', '_wall')))


def emits(b):
    if b.startswith(B + 'light['):
        return int(b.split('level=')[1].rstrip(']'))
    return EMIT.get(bid(b), 0)


def flood(cells, inside=None):
    """{(x, y, z): level} of block light inside `inside` (default: the arena box), BFS from the emitters"""
    inside = inside or in_box
    lv = {}
    buckets = [[] for _ in range(16)]
    for c, b in cells.items():
        e = emits(b)
        if e:
            lv[c] = e
            buckets[e].append(c)
    for L_ in range(15, 1, -1):
        for c in buckets[L_]:
            if lv.get(c) != L_:
                continue
            x, y, z = c
            for n in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
                if not inside(n) or opaque(cells.get(n)) or lv.get(n, 0) >= L_ - 1:
                    continue
                lv[n] = L_ - 1
                buckets[L_ - 1].append(n)
    return lv


def spawnable(cells, ytop=None):
    out = []
    for (x, y, z), b in cells.items():
        if not opaque(b) or bid(b) == 'barrier' or y + 2 > (ytop or BX['y1']):
            continue
        f1, f2 = cells.get((x, y + 1, z)), cells.get((x, y + 2, z))
        if (f1 is None or bid(f1) in FREE) and (f2 is None or bid(f2) in FREE):
            out.append((x, y + 1, z))
    return out


def dome_in(c):
    return T._dome_in(*c)


def apply_cmds(state, cmds):
    """fill / setblock semantics on a {cell: block} dict (vanilla: replace <filter> matches the block id, states free)"""
    for c in cmds:
        t = c.split()
        if t[0] == 'setblock':
            x, y, z = map(int, t[1:4])
            if bid(t[4]) == 'air':
                state.pop((x, y, z), None)
            else:
                state[(x, y, z)] = t[4]
            continue
        assert t[0] == 'fill', c
        x0, y0, z0, x1, y1, z1 = map(int, t[1:7])
        blk = t[7]
        flt = t[9] if len(t) > 9 and t[8] == 'replace' else None
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    if flt is not None:
                        cur = state.get((x, y, z))
                        if cur is None or bid(cur) != bid(flt):
                            continue
                    if bid(blk) == 'air':
                        state.pop((x, y, z), None)
                    else:
                        state[(x, y, z)] = blk


def fill_vol(cmd):
    t = cmd.split()
    x0, y0, z0, x1, y1, z1 = map(int, t[1:7])
    return (abs(x1 - x0) + 1) * (abs(y1 - y0) + 1) * (abs(z1 - z0) + 1)


def cmds_file(rel):
    p = F / f'{rel}.mcfunction'
    return [x for x in p.read_text(encoding='utf-8').split('\n') if x.strip() and not x.startswith('#')] if p.exists() else None


# ================================================================================================== 1
if want(1):
    print('== 1. registry, spec, names, determinism')
    check('1a registry arenas.fl_ruins == api.ARENA_SPEC (n 4, every key)', {k: A[k] for k in API.ARENA_SPEC} == API.ARENA_SPEC
          and set(A) == set(API.ARENA_SPEC), {k: (A.get(k), v) for k, v in API.ARENA_SPEC.items() if A.get(k) != v})
    check('1b the theme CHECK = the registry values; THEME / AID fl_ruins; looks day (default) + crimson',
          all(A[k] == v for k, v in T.CHECK.items()) and T.THEME == T.AID == 'fl_ruins' and A['looks'] == ['day', 'crimson'])
    names = ('SENTINEL', 'POINTS', 'CHECK', 'slices', 'arena_layout', 'props', 'look_lines', 'entrance_layout')
    check('1c theme names present', all(hasattr(T, n) for n in names), [n for n in names if not hasattr(T, n)])
    check('1d props(look) = [] in both looks (the wisps / the moon halo are kit props at POINTS)', T.props('day') == [] == T.props('crimson'))
    code = ('import sys,json,hashlib; sys.path.insert(0, sys.argv[1]); import mboss_arena_fl_ruins as T\n'
            'h=hashlib.sha256()\n'
            'for lk in T.LOOKS:\n'
            '    lay=T.arena_layout(lk); h.update(json.dumps(sorted((list(k),v) for k,v in lay.items())).encode())\n'
            '    h.update(json.dumps(T.look_lines(lk)).encode())\n'
            'e=T.entrance_layout(); h.update(json.dumps({str(z):sorted((list(k),v) for k,v in b.items()) for z,b in e["blocks"].items()}).encode())\n'
            'print(h.hexdigest())')
    hs = [subprocess.run([sys.executable, '-c', code, str(DP / 'tools')], capture_output=True, text=True).stdout.strip() for _ in range(2)]
    check('1e deterministic: two fresh interpreters give the same layouts, look jobs and entrance', hs[0] == hs[1] and len(hs[0]) == 64, hs)

# ================================================================================================== 2
WALK = [(x, z) for x in range(BX['x0'], BX['x1'] + 1) for z in range(BX['z0'], BX['z1'] + 1) if d_of(x, z) <= A['walk']]
if want(2):
    print('== 2. the walk disc')
    PLAZA = {'polished_diorite', 'calcite', 'smooth_stone', 'polished_andesite', 'stone_bricks', 'chiseled_stone_bricks',
             'cracked_stone_bricks', 'mossy_stone_bricks', 'moss_block'}
    bad = [(x, z, LAY['day'].get((x, 200, z))) for x, z in WALK if bid(LAY['day'].get((x, 200, z), 'air')) not in PLAZA
           or not opaque(LAY['day'].get((x, 200, z)))]
    check(f'2a every walk cell ({len(WALK)}) is a full opaque plaza block at y 200', not bad, bad[:5])
    diff = [(x, z) for x, z in WALK for y in range(190, 226) if LAY['day'].get((x, y, z)) != LAY['crimson'].get((x, y, z))]
    check('2b the walk disc (y 190..225) is identical in both looks', not diff, diff[:5])
    over = [(x, y, z, LAY[lk].get((x, y, z))) for lk in LOOKS for x, z in WALK for y in range(201, 226)
            if (x, y, z) in LAY[lk] and not (y == T.LIGHT_Y and LAY[lk][(x, y, z)] == B + 'light[level=15]')]
    check('2c nothing above the walk disc below y 226 but the light layer (both looks)', not over, over[:5])
    miss = [(x, z) for x, z in WALK if LAY['day'].get((x, T.LIGHT_Y, z)) != B + 'light[level=15]']
    check('2d the light layer: light[level=15] at y 206 over every walk cell', not miss, miss[:5])
    holes = [(x, y, z) for x, z in WALK for y in range(190, 200) if not opaque(LAY['day'].get((x, y, z)))]
    check('2e solid under the walk disc (y 190..199, the sentinel layer y 196)', not holes and LAY['day'].get(T.SENTINEL[0]) == T.SENTINEL[1]
          and LAY['crimson'].get(T.SENTINEL[0]) == T.SENTINEL[1], holes[:5])
    ceil = min((y for (x, y, z), b in LAY['day'].items() if d_of(x, z) <= A['walk'] and y > 200 and y != T.LIGHT_Y), default=None)
    check(f'2f the first block over the walk disc above y 200 (but the light layer) is the dome at y {ceil} >= 226', ceil and ceil >= 226, ceil)

# ================================================================================================== 3
if want(3):
    print('== 3. the barrier')
    bad = []
    ring = [(x, z) for x in range(BX['x0'], BX['x1'] + 1) for z in range(BX['z0'], BX['z1'] + 1) if A['walk'] < d_of(x, z) <= T.RIM_R]
    for lk in LOOKS:
        lay = LAY[lk]
        for x, z in ring:
            for y in range(T.BARRIER_Y[0], T.BARRIER_Y[1] + 1):
                b = lay.get((x, y, z))
                if b is None or bid(b) in ('light',) + FREE:
                    bad.append((lk, x, y, z, b))
    check(f'3a every ring cell (26 < d <= 27.6, {len(ring)} columns) y 201..216 holds a barrier or a balustrade block (both looks)',
          not bad, bad[:5])
    leaks = []
    for lk in LOOKS:
        lay = LAY[lk]
        for y in range(201, 217):
            seen = {(760, 8)}
            todo = [(760, 8)]
            while todo:
                x, z = todo.pop()
                if d_of(x, z) > T.RIM_R:
                    leaks.append((lk, y, x, z))
                    break
                for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)):
                    b = lay.get((n[0], y, n[1]))
                    if n in seen or (b is not None and bid(b) not in ('light',) + FREE):
                        continue
                    seen.add(n)
                    todo.append(n)
    check('3b closed: a 4-connected flood of passable cells from the centre never passes d 27.6 at any y 201..216', not leaks, leaks[:3])

# ================================================================================================== 4
if want(4):
    print('== 4. looks')
    em = BA.emit('fl_ruins')
    for lk in LOOKS:
        groups = T.look_lines(lk)
        check(f'4a look {lk}: the generated l/{lk}/<i> files = the emitter = look_lines ({len(groups)} slices <= {T.MAX_LOOK_SLICES})',
              em['looks'][lk] == groups and 1 <= len(groups) <= T.MAX_LOOK_SLICES
              and all(cmds_file(f'mboss/arena/fl_ruins/l/{lk}/{i}')[:len(g)] == g for i, g in enumerate(groups)), len(groups))
        fills = [c for g in groups for c in g if c.startswith('fill ')]
        big = [c for c in fills if fill_vol(c) > 32768]
        check(f'4b look {lk}: every fill <= 32 768 blocks, <= 8 000 commands per slice', not big and all(len(g) <= 8000 for g in groups),
              big[:2])
    other = {'day': 'crimson', 'crimson': 'day'}
    for lk in LOOKS:
        st = dict(LAY[other[lk]])
        for g in T.look_lines(lk):
            apply_cmds(st, g)
        diff = [c for c in set(st) | set(LAY[lk]) if st.get(c) != LAY[lk].get(c)]
        check(f'4c {other[lk]} -> {lk}: the job gives the {lk} layout exactly', not diff, [(c, st.get(c), LAY[lk].get(c)) for c in diff[:4]])
        st = dict(LAY[lk])
        for g in T.look_lines(lk):
            apply_cmds(st, g)
        diff = [c for c in set(st) | set(LAY[lk]) if st.get(c) != LAY[lk].get(c)]
        check(f'4d {lk} -> {lk}: idempotent', not diff, diff[:4])
    lc = T.look_cells()
    scanned = sum(fill_vol(c) for g in T.look_lines('crimson') for c in g if ' replace ' in c)
    spans = sum(1 for g in T.look_lines('crimson') for c in g if ' replace ' not in c)
    check(f'4e the crimson job: {len(lc)} cells change (dome / backdrop / moon ~ 16 k), {scanned} cells scanned by the replaces, '
          f'{spans} span commands', 12000 <= len(lc) <= 22000, len(lc))
    moon = [c for c, b in LAY['crimson'].items() if bid(b) in ('redstone_block', 'shroomlight')]
    check('4f the crimson moon on the north dome wall (redstone rim, shroomlight glow ring)', len(moon) >= 40
          and all(abs(T._angdiff(T._bearing(c[0], c[2]), 0)) < 20 for c in moon), len(moon))
    pal_day = {bid(b) for b in LAY['day'].values()}
    pal_cr = {bid(b) for b in LAY['crimson'].values()}
    check('4g the pair blocks are one-to-one and disjoint: no crimson pair block in the day layout, no day pair block in the crimson one',
          not (set(T.PAIRS.values()) & pal_day) and not (set(T.PAIRS) & pal_cr) and len(set(T.PAIRS.values())) == len(T.PAIRS),
          (set(T.PAIRS.values()) & pal_day, set(T.PAIRS) & pal_cr))

# ================================================================================================== 5
if want(5):
    print('== 5. build slices, the box')
    sl = T.slices()
    vol = lambda b: (b[1][0] - b[0][0] + 1) * (b[1][1] - b[0][1] + 1) * (b[1][2] - b[0][2] + 1)  # noqa: E731
    boxv = (BX['x1'] - BX['x0'] + 1) * (BX['y1'] - BX['y0'] + 1) * (BX['z1'] - BX['z0'] + 1)
    check(f'5a {len(sl)} slices <= 40, each <= 32 768 blocks, covering the box ({boxv})', len(sl) <= 40 and all(vol(b) <= 32768 for b in sl)
          and sum(vol(b) for b in sl) == boxv)
    counts = []
    for i in range(len(sl)):
        c = cmds_file(f'mboss/arena/fl_ruins/s/{i}')
        counts.append(len(c))
        assert all(fill_vol(x) <= 32768 for x in c if x.startswith('fill '))
    check(f'5b s/<i>: <= 8 000 commands each (max {max(counts)}), every fill <= 32 768', max(counts) <= 8000, counts)
    out = [c for lk in LOOKS for c in LAY[lk] if not in_box(c)]
    check('5c every block key inside the registry box (= the spec)', not out, out[:4])
    print('   blocks per slice (day):', [sum(1 for c in LAY['day'] if b[0][1] <= c[1] <= b[1][1]) for b in sl])

# ================================================================================================== 6
if want(6):
    print('== 6. light and the sky')
    for lk in LOOKS:
        lay = LAY[lk]
        lv = flood(lay)
        sp = spawnable(lay)
        low_in = [(c, lv.get(c, 0)) for c in sp if dome_in(c) and not (d_of(c[0], c[2]) <= A['walk'] and c[1] == 201) and lv.get(c, 0) < 12]
        walk = [lv.get((x, 201, z), 0) for x, z in WALK]
        low_out = [c for c in sp if not dome_in(c) and lv.get(c, 0) < 1]
        check(f'6a {lk}: every spawnable cell inside the dome but the walk floor has block light >= 12 ({len(sp)} spawn cells)', not low_in,
              low_in[:5])
        check(f'6b {lk}: the walk floor (y 201) has block light >= 10 everywhere (min {min(walk)}; 15 - 5 from the y-206 layer)',
              min(walk) >= 10, min(walk))
        check(f'6c {lk}: every spawnable cell outside the dome (its roof) has block light >= 1 (no spawns)', not low_out, low_out[:5])
    lay = LAY['day']
    start = [c for c in ((x, y, z) for x in (BX['x0'], BX['x1']) for y in range(BX['y0'], BX['y1'] + 1) for z in range(BX['z0'], BX['z1'] + 1))]
    start += [(x, y, z) for z in (BX['z0'], BX['z1']) for y in range(BX['y0'], BX['y1'] + 1) for x in range(BX['x0'], BX['x1'] + 1)]
    start += [(x, BX['y1'], z) for x in range(BX['x0'], BX['x1'] + 1) for z in range(BX['z0'], BX['z1'] + 1)]
    start += [(x, BX['y0'], z) for x in range(BX['x0'], BX['x1'] + 1) for z in range(BX['z0'], BX['z1'] + 1)]
    seen = set(c for c in start if not opaque(lay.get(c)))
    todo = list(seen)
    reached = []
    while todo:
        x, y, z = todo.pop()
        for n in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
            if n in seen or not in_box(n) or opaque(lay.get(n)):
                continue
            seen.add(n)
            if dome_in(n):
                reached.append(n)
            todo.append(n)
    check('6d no world-time dependence: no non-opaque path from the box faces (sky / outside) into the dome interior', not reached,
          reached[:4])

# ================================================================================================== 7
if want(7):
    print('== 7. points')
    W = T.POINTS['wisps']
    ok = len(W) == 3
    for (x, y, z, yaw), br in zip(W, (0, 150, 210)):
        d = math.hypot(x - A['cx'], z - A['cz'])
        b = math.degrees(math.atan2(x - A['cx'], -(z - A['cz']))) % 360
        post = LAY['day'].get((math.floor(x), math.floor(y) - 1, math.floor(z)))
        ok &= abs(d - 28.0) < 0.7 and abs(T._angdiff(b, br)) < 2.0 and d > T.RIM_R and post is not None and opaque(post) \
            and (math.floor(x), math.floor(y), math.floor(z)) not in LAY['day']
    check('7a three wisp points at bearings 0 / 150 / 210, r 28 (api.WISP_POSTS), outside the barrier ring, floating on a post',
          ok and tuple((b, r) for b, r in API.WISP_POSTS) == ((0, 28.0), (150, 28.0), (210, 28.0)), W)
    check('7b spawn = the centre (760, 201, 8) facing south; start = the registry start', T.POINTS['spawn'][:3] == (760.0, 201.0, 8.0)
          and T.POINTS['start'] == (A['start']['x'], A['start']['y'], A['start']['z'], A['start']['yaw']))
    mx, my, mz, _ = T.POINTS['moon']
    check('7c the moon point: north (bearing 0), inside the dome near the wall, above the north ruins (y >= 222)',
          abs(mx - 760) < 1 and mz < -25 and my >= 222 and T._dome_in(math.floor(mx), math.floor(my), math.floor(mz)), T.POINTS['moon'])

# ================================================================================================== 8
if want(8):
    print('== 8. the sim build / look / restore (cmsim, the shipped tree)')
    s, pl = M.setup(DP)
    M.PLAYER_LOAD[0] = 0
    C0 = M.C0
    s.call('rlk:mboss/ar/fl_ruins/fl_on', C0)
    M.run(s, 5)
    s.call('rlk:mboss/arena/fl_ruins/build', C0)
    n = 0
    while (M.mb(s, '#mbArBuild') or 0) > 0 and n < 200:
        M.world(s)
        n += 1

    def world_of(s):
        return {k: v for k, v in s.blocks.items() if in_box(k)}

    def norm(lay):
        return {k: bid(v) + (('[' + v.split('[', 1)[1]) if '[' in v else '') for k, v in lay.items()}
    ND, NC = norm(LAY['day']), norm(LAY['crimson'])
    w = world_of(s)
    diff = [c for c in set(w) | set(ND) if w.get(c) != ND.get(c)]
    st = s.storage.get('rlk:mboss', {})
    check(f'8a the build job ({n} ticks) leaves the day layout in the block world exactly; stamp fl_ruins@1:day, look day',
          not diff and st.get('built_fl_ruins') == 'fl_ruins@1:day' and st.get('look_fl_ruins') == 'day',
          (len(diff), [(c, w.get(c), ND.get(c)) for c in diff[:3]], st.get('built_fl_ruins')))
    s.call('rlk:mboss/arena/fl_ruins/look/crimson', C0)
    n = 0
    while (M.mb(s, '#mbArBuild') or 0) > 0 and n < 50:
        M.world(s)
        n += 1
    w = world_of(s)
    diff = [c for c in set(w) | set(NC) if w.get(c) != NC.get(c)]
    check(f'8b look/crimson ({n} ticks): the crimson layout exactly; stamp fl_ruins@1:crimson', not diff
          and st.get('built_fl_ruins') == 'fl_ruins@1:crimson', (len(diff), [(c, w.get(c), NC.get(c)) for c in diff[:3]]))
    r = s.call('rlk:mboss/arena/fl_ruins/ensure', C0)
    n = 0
    while (M.mb(s, '#mbArBuild') or 0) > 0 and n < 50:
        M.world(s)
        n += 1
    w = world_of(s)
    diff = [c for c in set(w) | set(ND) if w.get(c) != ND.get(c)]
    check(f'8c ensure (the next prep) restores day with the look job ({n} ticks), not a rebuild; then ensure returns 1', not diff
          and st.get('built_fl_ruins') == 'fl_ruins@1:day' and s.call('rlk:mboss/arena/fl_ruins/ensure', C0) == 1, len(diff))
    M.PLAYER_LOAD[0] = 96

# ================================================================================================== 9
if want(9):
    print('== 9. the entrance')
    ent = T.entrance_layout()
    try:
        BR.check_layout('arlecchino', ent)
        check('9a build_cboss_rooms.check_layout accepts entrance_layout() (key sets, zones, door, gate, blocks, clear boxes)', True)
    except AssertionError as e:
        check('9a build_cboss_rooms.check_layout', False, str(e))
    z1, z2 = ent['blocks'][1], ent['blocks'][2]
    gx, gy, gz = ent['gate']
    g0, g1 = T.GRAVE_CELL
    stone = [z2.get((x, y, g1)) for x in (g0, g0 + 1) for y in (202, 203, 204)]
    check('9b the gravestone (2 wide, behind the gate, north): polished deepslate slab, chiseled polished blackstone base and top',
          all(b is not None for b in stone) and bid(z2[(g0, 201, g1)]) == 'chiseled_polished_blackstone'
          and bid(z2[(g0, 204, g1)]) == 'chiseled_polished_blackstone' and bid(z2[(g0, 202, g1)]) == 'polished_deepslate' and g1 < gz, stone)
    fx, fy, fz = ent['stele_glow']
    zone = next(z for z in ent['cur']['zones'] if z['kind'] == 9)
    rel = tuple(round(a - b, 3) for a, b in zip(ent['stele_glow'], (zone['cx'], zone['cy'], zone['cz'])))
    check('9c the crimson flame point (stele_glow) centred on the slab top (y 205), in a free cell; GRAVE = that point relative '
          'to the kind-9 zone marker (room/gen_zone: (cx.0, cy, cz.0)) = entrance_layout()["grave"]', 205.0 < fy < 205.6
          and (math.floor(fx), math.floor(fy), math.floor(fz)) not in z2 and math.floor(fz) == g1 and abs(fx - (g0 + 1.0)) < 0.01
          and T.GRAVE == rel == tuple(ent['grave']), (ent['stele_glow'], T.GRAVE, rel))
    col = [(x, y, z) for x in (gx - 1, gx) for z in (gz - 1, gz) for y in range(201, 206) if (x, y, z) in z2]
    check('9d the gate column is free (k_cboss stands there)', not col, col)
    dung = lambda c: -64 <= c[0] <= 63 and 199 <= c[1] <= 230 and -64 <= c[2] <= 63  # noqa: E731
    lit = flood({**z1, **z2}, dung)
    dark = [c for c in spawnable({**z1, **z2}, 230) if lit.get(c, 0) < 1]
    check('9e every spawnable cell of the entrance is lit (no spawns)', not dark, dark[:4])
    V, stubbed = K.variant_ar(DP, route=True, label='ent')
    try:
        files = sorted(p.name for p in (V / 'data/rlk/function/room/cboss/arlecchino').glob('*.mcfunction'))
        lay = (V / 'data/rlk/function/room/cboss/arlecchino/layout.mcfunction').read_text(encoding='utf-8')
        disp = (V / 'data/rlk/function/room/cboss/build.mcfunction').read_text(encoding='utf-8')
        check('9f with the entry enabled build_cboss_rooms writes room/cboss/arlecchino/{layout,build,z1,z2} from the theme and the '
              'dispatcher line', files == ['build.mcfunction', 'layout.mcfunction', 'z1.mcfunction', 'z2.mcfunction']
              and 'mboss_arena_fl_ruins.py entrance_layout()' in lay and 'boss_id:"arlecchino"' in lay
              and 'run function rlk:room/cboss/arlecchino/build' in disp, files)
    finally:
        M.drop_variant(V)

M.summary('ARENA_FL')
