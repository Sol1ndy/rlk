#!/usr/bin/env python3
"""test_kit.py: the 홍련 (Scarlet) fx / sound / HUD kit (stage S1K: tools/build_mboss_hr_fx.py) against one worktree.

    python3 test_kit.py <worktree>/roguelike [<resource pack>]

mcsim (HR/s1k/lib/mcsim.py, vendored unchanged from tools/dev/sim/ar/tests/lib) runs the kit's own functions through
HR/s1k/lib/hrfxsim.py (the 아를레키노 kit harness with the hr tag: execute summon, NBT list filters, bossbars, titles,
entity merges). Vanilla order: a server tick T runs the functions (gametime T), then gametime -> T + 1 and the scheduled
functions run. Sections:
  names    every api.KIT_PRESETS / KIT_PROPS / KIT_SOUNDS / KIT_HUD / KIT_FIXED name exists with the right macro-ness and
           exactly the contract args; api.K lines resolve; the manifest lists; a demo per preset / prop; hud/l/1..25
  calls    every kit call S3 + S4 (wip/hr-s4) and S2b (wip/hr-s2b) generate (built in a temp copy with the kit manifest
           present) names an existing function with exactly its args
  engine   card / cardx stages (the first-tick fix), the ager stops; caps: fx 96, ambient 48, afterimage 4 (never skipped,
           the oldest go)
  presets  every preset with test values at its documented executor heights: cards <= the manifest count, all expire,
           every c variant; no card corner below the floor at any stage (start, end, mid-interpolation); qi_arc lifted /
           shrunk by the clamp at low heights, full reach when it fits; c tints; ambient presets in the ambient pool
  props    disc / petal_big / moon_halo / lotus / seat_rock: dressed in place, re-looked, idempotent; the disc spins and
           swaps its frames; a prop on a marker gets one follower that stays on it and goes with it; the seat rock's items
  clear    fx/clear (pause): every card and beam gone, props and followers kept; a dead player clears the cards
  uninst   fx/uninstall: nothing of the kit left (cards, followers, stand-ins, objectives, scores, storage fx only, the warn
           bossbar, schedules, tags)
  sounds   every recipe = api.KIT_SOUND_RECIPES, vanilla ids only (tools/dev/sim/rd/tests/sound_ids.txt), the
           mboss_lib.sound min-volume line
  hud      lines 1-25 verbatim (api.LINES), revealed in prefixes two syllables per 2 t with one hat each, held for
           api.LINE_AT[id][2] t; a line during an overlay keeps the overlay glyph on the title, ttl_blank once it ended;
           ovl vBig = in + hold + out; the warn bossbar lifecycle; the skip prompt (text verbatim + hint, hudHold 2, s:5
           clears it); clear
  static   no negative add / remove literals, $( only in macro lines, lowercase ids, the glyph root rule (a kit-font
           component is never a root and never inherits: every component names its font), on-screen text only api
           strings
  demos    every fx/test/<preset> and test/prop/<name> runs to its end on the stand-in; test/stop removes it
  rp       (with a pack) sprites = api.KIT_SPRITES (sizes, sum <= 0.26 M), the gate icon <= 5 000 px, models, items,
           atlas entries, the font (glyph sizes, U+EC00-ECFF, ends with minecraft:default, no collision)
"""
import json
import math
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HR = HERE.parent
sys.path.insert(0, str(HR / 's1k/lib'))
import mcsim  # noqa: E402
import hrfxsim  # noqa: E402

WT = Path(sys.argv[1]).resolve()
RP = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
sys.path.insert(0, str(WT / 'tools'))
import build_mboss_hr_fx as G  # noqa: E402
from mboss_scarlet import api  # noqa: E402
import mboss_lib as L  # noqa: E402

FN = WT / 'data/rlk/function'
FX = FN / 'boss/scarlet/fx'
TAG = G.TAG
OBJ = G.OBJ
NSF = 'rlk:boss/scarlet/fx/'
SOUND_IDS = WT / 'tools/dev/sim/rd/tests/sound_ids.txt'
FAILS, NCHK = [], [0]


def check(cond, msg):
    NCHK[0] += 1
    if not cond:
        FAILS.append(msg)
        print('FAIL', msg)


FLOOR = float(api.CY)
X0, Z0 = 884.5, 0.5


def fresh():
    s = hrfxsim.fresh(FN)
    s.player.pos = [X0, FLOOR, Z0 + 12]
    return s


def comp(s, e):
    return s.nbt[e.id]['item']['components']


def model(s, e):
    return comp(s, e)['minecraft:item_model']


def kind(s, e):
    return model(s, e).split('/')[-1]


def tint(s, e):
    return comp(s, e)['minecraft:custom_model_data']['colors'][0]


def cdata(s, e):
    return comp(s, e)['minecraft:custom_data']


def stages(s, eid):
    out = {}
    for t, i, ev in s.events:
        if i == eid and ev not in out:
            out[ev] = t
    return out


def fbody(rel):
    return (FX / f'{rel}.mcfunction').read_text(encoding='utf-8')


MAN = json.loads(api.KIT_MANIFEST.read_text(encoding='utf-8'))
TEST = dict(G.TEST_ARGS)


def targs(table, name, **over):
    a = dict(TEST, **over)
    return {k: a[k] for k in table[name]}


# ----------------------------------------------------------------------------- card geometry (the kit renderer's math)
def rot_y(a):
    c, s_ = math.cos(a), math.sin(a)
    return [[c, 0, s_], [0, 1, 0], [-s_, 0, c]]


def rot_x(a):
    c, s_ = math.cos(a), math.sin(a)
    return [[1, 0, 0], [0, c, -s_], [0, s_, c]]


def rot_axis(axis, a):
    n = math.sqrt(sum(v * v for v in axis)) or 1.0
    x, y, z = (v / n for v in axis)
    c, s_, C = math.cos(a), math.sin(a), 1 - math.cos(a)
    return [[c + x * x * C, x * y * C - z * s_, x * z * C + y * s_],
            [y * x * C + z * s_, c + y * y * C, y * z * C - x * s_],
            [z * x * C - y * s_, z * y * C + x * s_, c + z * z * C]]


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def mv(A, v):
    return [sum(A[i][k] * v[k] for k in range(3)) for i in range(3)]


def aa(r, default=(0, 0, 1)):
    if isinstance(r, dict):
        return float(r['angle']), tuple(float(v) for v in r['axis'])
    x, y, z, w = (float(v) for v in r)
    w = max(-1.0, min(1.0, w))
    ang = 2 * math.acos(w)
    sn = math.sqrt(max(0.0, 1 - w * w))
    return (0.0, default) if sn < 1e-9 else (ang, (x / sn, y / sn, z / sn))


def local_points(kd):
    plane, _px, (a0, a1, b0, b1) = G.kind_info(kd)[:3]
    if kd.startswith('qi_arc_'):          # the crescent itself: unit radius, bearings +-80 deg from +b (the clamp's model)
        return [(-math.sin(math.radians(t)), 0.0, math.cos(math.radians(t))) for t in range(-80, 81, 5)]
    if kd.startswith('qi_arcf_'):         # F2 (HR-12): the same crescent on a face quad (the bulge at +b = local +y)
        return [(-math.sin(math.radians(t)), math.cos(math.radians(t)), 0.0) for t in range(-80, 81, 5)]
    pts = []
    for a in (a0, a1):
        for b in (b0, b1):
            if plane in ('face', 'cross', 'lancex'):
                pts.append((-a, b, 0.0))
            if plane in ('flat', 'lance', 'lancex'):
                pts.append((-a, 0.0, b))
            if plane == 'cross':
                pts.append((0.0, b, a))
            if plane == 'lance':
                pts.append((0.0, a, b))
    return pts


def tstate(tr):
    roll, lax = aa(tr.get('left_rotation', [0, 0, 0, 1]))
    spin, ax = aa(tr.get('right_rotation', [0, 0, 0, 1]))
    return {'t': [float(v) for v in tr.get('translation', [0, 0, 0])], 's': [float(v) for v in tr.get('scale', [1, 1, 1])],
            'roll': roll, 'lax': lax, 'spin': spin, 'ax': ax}


def world_low(s, e, st):
    """the lowest world y of the card e in transformation state st (fixed: its yaw / pitch; billboards upright)"""
    if all(abs(v) < 1e-9 for v in st['s']):
        return None
    M = mm(mm(rot_axis(st['lax'], st['roll']), [[st['s'][0], 0, 0], [0, st['s'][1], 0], [0, 0, st['s'][2]]]),
           rot_axis(st['ax'], st['spin']))
    bb = s.nbt[e.id].get('billboard', 'fixed')
    E = mm(rot_y(math.radians(-e.rot[0])), rot_x(math.radians(e.rot[1]))) if bb == 'fixed' else rot_y(0.0)
    low = 1e9
    for p in local_points(kind(s, e)):
        q = mv(E, [st['t'][i] + mv(M, p)[i] for i in range(3)])
        low = min(low, e.pos[1] + q[1])
    return low


def card_lowest(s, e):
    """the lowest point over the card's life: spawn state, its stage snapshots (S, G, F) and the G interpolation"""
    n = s.nbt[e.id]
    st0 = tstate(n.get('transformation', {}))
    cd = cdata(s, e)
    lows = [world_low(s, e, st0)]
    cur = dict(st0)
    for key in ('hrS', 'hrG'):
        T = cd.get(key, {}).get('transformation', {})
        nxt = dict(cur)
        if 'translation' in T:
            nxt['t'] = [float(v) for v in T['translation']]
        if 'scale' in T:
            nxt['s'] = [float(v) for v in T['scale']]
        if 'left_rotation' in T:
            nxt['roll'], nxt['lax'] = aa(T['left_rotation'])
        if 'right_rotation' in T:
            nxt['spin'], nxt['ax'] = aa(T['right_rotation'])
        for f in (0.25, 0.5, 0.75, 1.0):
            mid = {k: [cur[k][i] + (nxt[k][i] - cur[k][i]) * f for i in range(3)] for k in ('t', 's')}
            mid.update({'roll': cur['roll'] + (nxt['roll'] - cur['roll']) * f, 'lax': nxt['lax'],
                        'spin': cur['spin'] + (nxt['spin'] - cur['spin']) * f, 'ax': nxt['ax']})
            lows.append(world_low(s, e, mid))
        cur = nxt
    lows = [v for v in lows if v is not None]
    return min(lows) if lows else None


# ============================================================== names
for sub, table in (('p', api.KIT_PRESETS), ('hud', api.KIT_HUD), ('prop', {k: list(v) for k, v in api.KIT_PROPS.items()})):
    for name, args in table.items():
        p = FX / f'{sub}/{name}.mcfunction'
        check(p.exists(), f'names: {sub}/{name} missing')
        if not p.exists():
            continue
        txt = p.read_text(encoding='utf-8')
        macro = any(ln.startswith('$') for ln in txt.split('\n'))
        check(macro == bool(args), f'names: {sub}/{name} macro-ness {macro} vs args {args}')
        used = set(re.findall(r'\$\((\w+)\)', txt))
        check(used == set(args), f'names: {sub}/{name} uses {sorted(used)}, contract {args}')
for name in api.KIT_PRESETS:
    line = api.K.p(name, **targs(api.KIT_PRESETS, name))
    check(line.split()[1] == f'{NSF}p/{name}', f'names: api.K.p {line}')
for name, spec in api.KIT_PROPS.items():
    line = api.K.prop(name, **{k: v[0] for k, v in spec.items()})
    check(line.split()[1] == f'{NSF}prop/{name}', f'names: api.K.prop {line}')
check(api.K.ovl('black', 0, 10, 3).split()[1] == f'{NSF}hud/ovl', 'names: api.K.ovl')
for name in api.KIT_SOUNDS:
    check((FX / f'snd/{name}.mcfunction').exists(), f'names: snd/{name}')
    check(api.K.snd(name) == f'function {NSF}snd/{name}', f'names: api.K.snd {name}')
check(tuple(G.SOUNDS) == tuple(api.KIT_SOUNDS) and len(api.KIT_SOUNDS) == 104, 'names: 104 sound recipes = api.KIT_SOUNDS')
for name in api.KIT_FIXED:
    check((FX / f'{name}.mcfunction').exists(), f'names: fx/{name}')
    check(api.K.fixed(name) == f'function {NSF}{name}', f'names: api.K.fixed {name}')
check(set(MAN['presets']) == set(api.KIT_PRESETS) and set(MAN['props']) == set(api.KIT_PROPS)
      and set(MAN['sounds']) == set(api.KIT_SOUNDS) and set(MAN['hud']) == set(api.KIT_HUD), 'names: manifest lists')
check(len(api.KIT_PRESETS) == 50 and len(api.KIT_PROPS) == 5 and len(api.KIT_HUD) == 5, 'names: 50 presets, 5 props, 5 hud')
for name in api.KIT_PRESETS:
    check((FX / f'test/{name}.mcfunction').exists(), f'names: demo test/{name}')
for name in api.KIT_PROPS:
    check((FX / f'test/prop/{name}.mcfunction').exists(), f'names: demo test/prop/{name}')
for lid in api.LINES:
    check((FX / f'hud/l/{lid}.mcfunction').exists(), f'names: line hud/l/{lid}')

# ============================================================== calls (S3 + S4, S2b: the module built with the kit on)
CALL_RE = re.compile(r'function rlk:boss/scarlet/fx/([a-z0-9_/]+)(?: (\{[^}]*\}|with storage \S+ \S+))?')
TMP = HR / 's1k/tmp/calls_test'
ncalls, calls_by = 0, {}
# I1: on the merged tree the module is already built with the kit (S3 + S4 + S2b + S1K): its own boss/scarlet tree is
# scanned (no temp build from the stage branches); a kit-only tree (S1K's branch) still builds them in a temp copy.
MERGED = (WT / 'data/rlk/function/boss/scarlet/core').is_dir() and (WT / 'data/rlk/function/boss/scarlet/seq').is_dir()
if MERGED or (shutil.which('git') and subprocess.run(['git', '-C', '/home/user/rlk', 'rev-parse', '--verify', '-q',
                                                      'wip/hr-s4'], capture_output=True).returncode == 0):
    if MERGED:
        MOD = WT / 'data/rlk/function/boss/scarlet'
        print('calls: the merged tree\'s own module (built with the kit)')
    else:
        shutil.rmtree(TMP, ignore_errors=True)
        TMP.mkdir(parents=True)
        subprocess.run(f'git -C /home/user/rlk archive wip/hr-s4 roguelike/tools | tar -x -C {TMP} '
                       "--exclude='roguelike/tools/dev'", shell=True, check=True)
        for f in ('roguelike/tools/mboss_scarlet/seq.py', 'roguelike/tools/scarlet_rig_manifest.json'):
            r = subprocess.run(['git', '-C', '/home/user/rlk', 'show', f'wip/hr-s2b:{f}'], capture_output=True)
            if r.returncode == 0:
                (TMP / f).write_bytes(r.stdout)
        shutil.copy(api.KIT_MANIFEST, TMP / 'roguelike/tools/mboss_hr_fx_manifest.json')
        (TMP / 'roguelike/data/rlk/function').mkdir(parents=True)
        out = subprocess.run(['python3', '-I', 'tools/build_mboss_scarlet.py'], cwd=TMP / 'roguelike', capture_output=True,
                             text=True)
        check(out.returncode == 0, f'calls: the merged module builds ({out.stderr[-400:]})')
        MOD = TMP / 'roguelike/data/rlk/function/boss/scarlet'
    for p in sorted(x for x in MOD.rglob('*.mcfunction') if not x.relative_to(MOD).as_posix().startswith('fx/')):
        rel = p.relative_to(MOD).as_posix()
        for ln in p.read_text(encoding='utf-8').split('\n'):
            if ln.lstrip().startswith('#'):
                continue
            for m in CALL_RE.finditer(ln):
                path, args = m.group(1), m.group(2) or ''
                f = FX / f'{path}.mcfunction'
                check(f.exists(), f'calls: {rel}: fx/{path} missing')
                if not f.exists():
                    continue
                ncalls += 1
                calls_by.setdefault(path, []).append((rel, ln.strip(), args))
                txt = f.read_text(encoding='utf-8')
                want = set(re.findall(r'\$\((\w+)\)', txt)) if any(x.startswith('$') for x in txt.split('\n')) else set()
                if args.startswith('with'):
                    continue
                got = set(re.findall(r'(\w+):', args))
                check(got == want, f'calls: {rel}: fx/{path} args {sorted(got)} vs {sorted(want)}')
    if MERGED:
        # F2 (HR-17 / HR-23 / HR-24): the module's own call lines. The instant deaths' cards (the 홍련일섬 line, the petals,
        # the bolts of that tick) and CS3's kick flash between fx/keep_on and fx/keep_off; the tells / trails that travel with
        # her between fx/follow_on and fx/follow_off; A9's streak reads the probed dash length (the hazard line's compound)
        def between(lines, i, on, off):
            return any(x.endswith(on) for x in lines[:i]) and any(x.endswith(off) for x in lines[i + 1:])
        kept, follow, a9 = [], [], []
        for p in sorted(x for x in MOD.rglob('*.mcfunction') if not x.relative_to(MOD).as_posix().startswith('fx/')):
            rel = p.relative_to(MOD).as_posix()
            LL = [x for x in p.read_text(encoding='utf-8').split('\n') if x and not x.startswith('#')]
            fatal = [i for i, x in enumerate(LL) if x.endswith('rlk:boss/scarlet/ult/fatal')]
            for i, x in enumerate(LL):
                if (fatal and i < fatal[0] and re.search(r'fx/p/(scarlet_line|petal_burst)\b', x)) or 'fx/p/kick_flash' in x:
                    kept.append((rel, between(LL, i, 'fx/keep_on', 'fx/keep_off')))
                # HR-23's list: the A13 / R2 / A10 yellow tells, A6's blink bubble, A4's ribbon (A9's tell stands before its dash)
                if re.search(r'fx/p/(yellow_tell|blink_bubble|qi_ribbon)\b', x) and rel.startswith(('p/a4/', 'p/a6/', 'p/a10/',
                                                                                                       'p/a13/', 'p/r2/')):
                    follow.append((rel, between(LL, i, 'fx/follow_on', 'fx/follow_off')))
                if 'fx/p/qi_cut' in x and rel.startswith('p/a9/'):
                    a9.append((rel, x.endswith('with storage rlk:hr core.a9')))
        check(len(kept) >= 4 and all(ok for _, ok in kept), f'calls: the instant deaths\' line / petals and CS3\'s kick flash are kept '
                                                            f'(keep_on .. keep_off) {kept}')
        check(len(follow) >= 4 and all(ok for _, ok in follow), f'calls: the yellow tells, the blink bubble and the A4 ribbon follow '
                                                                f'her (follow_on .. follow_off) {follow}')
        hz9 = [x for p in (MOD / 'p/a9').rglob('*.mcfunction') for x in p.read_text(encoding='utf-8').split('\n')
               if 'mboss/hz/line with storage rlk:hr core.a9' in x]
        check(a9 and all(ok for _, ok in a9) and hz9, f'calls: A9\'s streak (qi_cut) reads the probed dash length, the hazard line\'s '
                                                      f'compound core.a9 {a9}')
    if not MERGED:
        shutil.rmtree(TMP, ignore_errors=True)
    check(ncalls > 300, f'calls: {ncalls} kit calls checked')
else:
    print('calls: wip/hr-s4 not found, skipped')

# ============================================================== engine
s = fresh()
T0 = s.gt
s.run(G.card('glint_0', '^ ^1 ^2', '~ 0', spin=90, s0=1, s1=3, life=8, fade=3, col=0xFF00FF))
cs = s.cards()
check(len(cs) == 1, 'engine: one card')
e = cs[0]
check(model(s, e) == 'rlk:mboss/hr_kit/glint_0' and tint(s, e) == 0xFF00FF, 'engine: model / tint')
check({TAG, f'{TAG}_c', 'rlk_room', 'rlk_mb_aux'} <= set(e.tags), f'engine: tags {e.tags}')
check(OBJ in s.objectives and all(o in s.objectives for o in G.OBJECTIVES), 'engine: objectives made by the first card')
s.tick(12)
st = stages(s, e.id)
check(st.get('hrG') == T0 + 2 and st.get('hrF') == T0 + 6 and st.get('kill') == T0 + 9, f'engine: stages {st} from {T0}')
check(not s.cards() and f'{NSF}e/world' not in s.sched, 'engine: card gone, the ager stopped')
check(s.sc('#n', OBJ) == 0, 'engine: count back to 0')
s = fresh()
T0 = s.gt
s.run(G.card('glint_0', bb='center', s0=(1, 2, 1), s1=(2, 4, 2), life=10, fade=2, dly=4, dur=3, hit=6, col2=0xFF0000,
             off=(0, 0, 2.5), move=(0, 0, 3)))
e = s.cards()[0]
cd = cdata(s, e)
check(s.nbt[e.id]['transformation']['scale'] == [0, 0, 0], 'engine: cardx hidden until its delay')
check(cd['hrG']['transformation']['translation'] == [0, 0, 5.5], 'engine: cardx end translation = off + move')
check(s.nbt[e.id]['transformation']['translation'] == [0, 0, 2.5], 'engine: cardx start translation = off')
s.tick(18)
st = stages(s, e.id)
check(st.get('hrS') == T0 + 5 and st.get('hrG') == T0 + 6 and st.get('hit') == T0 + 7 and st.get('hrF') == T0 + 13
      and st.get('kill') == T0 + 15, f'engine: cardx stages {st}')
# caps: never skipped, the oldest go (spawn serial), per pool
for pool, cap, tagx in ((0, G.CAP_FX, '_c'), (1, G.CAP_AMB, '_a'), (2, G.CAP_AI, '_i')):
    s = fresh()
    for i in range(cap + 20):
        s.run(G.card('petal_0', life=60, pool=('fx', 'am', 'ai')[pool]))
        if i % 7 == 0:
            s.tick(1)
    s.tick(1)
    left = s.cards(TAG + tagx)
    check(len(left) == cap, f'engine: pool {pool} cap {len(left)} == {cap}')
    ser = sorted(s.sc(('e', e.id), 'hrFxQ') for e in left)
    check(ser == list(range(s.sc('#ser', OBJ) - cap + 1, s.sc('#ser', OBJ) + 1)), f'engine: pool {pool} keeps the newest')
check((G.CAP_FX, G.CAP_AMB, G.CAP_AI) == (api.FX_CARD_CAP, api.AMBIENT_CARD_CAP, api.AFTERIMAGE_MAX), 'engine: caps = api')
s = fresh()
for _ in range(G.CAP_FX):
    s.run(G.card('petal_0', life=60))
for _ in range(10):
    s.run(G.fx('ambient_p1'), pos=(X0, FLOOR, Z0))
s.tick(1)
check(len(s.cards(TAG + '_c')) == G.CAP_FX and len(s.cards(TAG + '_a')) == 10, 'engine: ambient cards not counted in the fx pool')
s = fresh()
for i in range(7):
    s.run(G.fx('afterimage', len=20), pos=(X0, FLOOR + 1.2, Z0))
    s.tick(1)
check(len(s.cards(TAG + '_i')) <= api.AFTERIMAGE_MAX, f'engine: afterimages <= {api.AFTERIMAGE_MAX}')
e = s.cards(TAG + '_i')[-1]
s = fresh()
T0 = s.gt
s.run(G.fx('afterimage', len=20), pos=(X0, FLOOR + 1.2, Z0))
e = s.cards(TAG + '_i')[0]
s.tick(10)
check(kind(s, e) == 'afterimage' and stages(s, e.id).get('kill') == T0 + api.AFTERIMAGE_FADE + 1,
      f'engine: the afterimage is gone after 6 t ({stages(s, e.id)})')

# ============================================================== presets
# S2d (requests/s2d.md s2d-3, I2): the call heights of the player-size body (the S2a figure's x 0.78)
HEIGHT = {'qi_arc': (1.0, 0.3), 'qi_ring': (0.8, 0.1), 'qi_band': (0.3, 1.1), 'qi_x': (0.1,), 'qi_dome': (0.0,),
          'qi_vert': (0.0, 0.15), 'qi_fan': (0.85,), 'qi_wedge': (0.85, 1.0), 'qi_ribbon': (1.0,), 'qi_line': (0.95, 0.8),
          'qi_cut': (0.8,), 'glint': (0.3, 1.5), 'star4': (1.0,), 'yellow_tell': (1.0,), 'ghost_burst': (0.8,),
          'ghost_trail': (0.45,), 'ghost_flash': (0.95,), 'afterimage': (0.0, 1.2), 'blink_bubble': (1.0,),
          'shield_refill': (1.1,), 'pip_break': (1.0,), 'dive_impact': (0.1,), 'light_column': (0.0,),
          'claw_streaks': (2.0,), 'burst_radial': (0.1,), 'dust_ring': (0.1,), 'kick_flash': (1.5,), 'clash_gold': (1.0,),
          'clash_spark': (0.5,), 'clash_arc': (1.0,), 'deco_bolt': (0.0,), 'scarlet_line': (1.3, 1.62), 'petal_burst': (0.3,),
          'petals_drift': (1.1,), 'petals_wind': (0.8,), 'petals_heart': (1.1,), 'motes_warm': (0.4,),
          'leaves_dark': (6.0,), 'leaves_swirl': (1.1,), 'ambient_p1': (0.0,), 'ambient_p2': (0.0,),
          'arrive_rift': (0.0,), 'ev_glint': (1.0,), 'ev_trail': (1.0,), 'ev_petals': (1.0,), 'ev_leave': (1.1,),
          'ev_beam': (0.0,), 'ev_wind': (0.0,), 'ev_palm': (1.0,), 'ev_take': (1.2,)}
assert set(HEIGHT) == set(api.KIT_PRESETS)
VARIANTS = {'qi_arc': [{}, {'pitch': -40, 'roll': 90}, {'pitch': 35, 'roll': -35}, {'r': 60, 'roll': 180},
                       {'r': 45, 'roll': -40}, {'r': 40, 'roll': 15}, {'r': 45, 'roll': 20}, {'r': 45, 'roll': -160},
                       {'r': 40, 'pitch': -30, 'roll': 35}], 'qi_fan': [{'h': 13}],
            'qi_ring': [{'r': 30}, {'r': 22}], 'qi_dome': [{'r': 35}], 'qi_x': [{'r': 25}],
            'qi_band': [{'len': 70, 'pitch': 35}, {'len': 120}, {'roll': 30, 'pitch': -20}, {'len': 120, 'sw': 200}],
            'qi_vert': [{}, {'yaw': 90}, {'h': 19}, {'yaw': 180}],
            'qi_wedge': [{}, {'roll': -40}, {'roll': 10}, {'roll': 90, 'r': 28}],     # F-I: roll 90's reach x 0.78 (S2d's body)
            'scarlet_line': [{}, {'roll': -13}, {'yaw': 0}, {'len': 600, 'yaw': 90, 'roll': 13}, {'len': 600, 'yaw': 90, 'roll': -13},
                             {'len': 600, 'yaw': 0, 'roll': 13}], 'leaves_dark': [{'n': 40}, {'n': -20}]}
for name in api.KIT_PRESETS:
    cvals = [1, 2, 3, 4, 5] if 'c' in api.KIT_PRESETS[name] else [None]
    for c in cvals:
        for h in HEIGHT[name]:
            for var in VARIANTS.get(name, [{}]):
                over = dict(var, **({'c': c} if c else {}))
                s = fresh()
                pos = (X0, FLOOR + h, Z0)
                s.run(G.fx(name, **targs(api.KIT_PRESETS, name, **over)), pos=pos, rot=(30.0, 0.0))
                made = s.cards()
                tag = f'{name} c {c} h {h} {var}'
                check(len(made) <= MAN['presets'][name]['cards'], f'presets: {tag}: {len(made)} cards > manifest '
                                                                   f'{MAN["presets"][name]["cards"]}')
                if name not in G.PTCL:
                    check(made, f'presets: {tag} spawns cards')
                else:
                    check(not made or name == 'ev_beam', f'presets: {tag} is particles only')
                pool = TAG + ('_a' if name in G.AMBIENT else '_i' if name == 'afterimage' else '_c')
                if name != 'afterimage':
                    check(all(pool in e.tags for e in made), f'presets: {tag} cards in the pool {pool}')
                for e in made:
                    if s.nbt[e.id].get('billboard') == 'center':
                        continue
                    low = card_lowest(s, e)
                    check(low is None or low >= FLOOR - 1e-3, f'presets: {tag}: {kind(s, e)} reaches '
                                                              f'{(low or 0) - FLOOR:.3f} b below the floor')
                    check(e.pos[1] >= FLOOR - 1e-6, f'presets: {tag}: {kind(s, e)} spawned below the floor')
                s.tick(130)
                check(not s.cards() and f'{NSF}e/world' not in s.sched, f'presets: {tag}: every card expires, the ager stops')
                check(not [e for e in s.ents if e.etype == 'marker'], f'presets: {tag}: no marker left')
# leaves_dark: n < 0 = the last -n of the 40 (I1b verification round 1: S2b's CS1 burst is spread as {n:20} then {n:-20} on the
# next tick); the halves are exactly the 40 cards of {n:40}, a positive n keeps the first n, n 0 makes none


def leaf_cards(*ns):
    s = fresh()
    for n in ns:
        s.run(G.fx('leaves_dark', n=n), pos=(X0, FLOOR + 6.0, Z0), rot=(30.0, 0.0))
    return sorted((round(e.pos[0], 4), round(e.pos[1], 4), round(e.pos[2], 4), round(e.rot[0], 3), round(e.rot[1], 3), kind(s, e))
                  for e in s.cards())


LEAVES = leaf_cards(40)
check(len(LEAVES) == G.LEAF_N and leaf_cards(20, -20) == LEAVES and leaf_cards(-40) == LEAVES and leaf_cards(10, -30) == LEAVES
      and sorted(set(LEAVES) - set(leaf_cards(20))) == leaf_cards(-20) and len(leaf_cards(8)) == 8 and not leaf_cards(0),
      'presets: leaves_dark n < 0 = the last -n leaves ({n:20} + {n:-20} = the 40 of {n:40}; n 8 -> the first 8; n 0 -> none)')
# qi_arc: lifted / shrunk near the floor, full reach when it fits; rotation = executor + offsets (pitch + = up)
for h, r, pitch, roll in ((1.3, 40, 0, 0), (1.3, 45, 0, -40), (0.3, 40, -40, 90), (0.1, 60, 0, 90), (1.3, 36, -60, 90),
                          (0.3, 40, 0, 15), (1.3, 40, 35, 0)):
    s = fresh()
    s.run(G.fx('qi_arc', r=r, yaw=20, pitch=pitch, roll=roll, c=1), pos=(X0, FLOOR + h, Z0), rot=(15.0, 0.0))
    arcs = [e for e in s.cards() if kind(s, e).startswith(('qi_arc_', 'qi_arcf_'))]
    check(len(arcs) == 4, f'qi_arc: four frames ({len(arcs)})')
    for e in arcs:
        check(abs(((e.rot[0] - 35) + 180) % 360 - 180) < 1e-6 and abs(e.rot[1] + pitch) < 1e-6,
              f'qi_arc: rotation {e.rot} (yaw 15 + 20, pitch {pitch} up)')
    sc = cdata(s, arcs[0])['hrG']['transformation']['scale'][0]
    lift = arcs[0].pos[1] - (FLOOR + h)
    check(lift <= G.ARC_LIFT / 100 + 1e-6, f'qi_arc: lift {lift:.2f} <= {G.ARC_LIFT / 100}')
    if h >= 1.3 and pitch >= 0 and roll == 0:
        check(abs(sc - r / 10) < 1e-6 and lift < 1e-6, f'qi_arc h {h} r {r} pitch {pitch} roll {roll}: full reach ({sc})')
# c tints: lilac / pink-magenta / yellow / crimson / white differ
tints = {}
for c in range(1, 6):
    s = fresh()
    s.run(G.fx('glint', c=c), pos=(X0, FLOOR + 1.5, Z0))
    tints[c] = tuple(sorted(tint(s, e) for e in s.cards()))
check(len(set(tints.values())) == 5, f'presets: glint c 1-5 tints differ {tints}')
# scarlet_line: a lancex card along executor yaw + yaw (-90 card yaw), roll lifts the + end
s = fresh()
s.run(G.fx('scarlet_line', len=600, yaw=90, roll=13), pos=(X0, FLOOR + 1.3, Z0), rot=(40.0, 0.0))
e = [e for e in s.cards() if kind(s, e) == 'scarlet_line'][0]
check(abs(((e.rot[0] - 40) + 180) % 360 - 180) < 1e-6, f'scarlet_line: yaw 90 -> card yaw executor + 0 ({e.rot})')
check(abs(cdata(s, e)['hrG']['transformation']['scale'][0] - 60) < 1e-6, 'scarlet_line: 60 b long')
ang = s.nbt[e.id]['transformation']['left_rotation']['angle']
check(ang < 0, f'scarlet_line: roll 13 -> card roll {ang:.3f} (the + end up)')
# ev_beam: a column drawn by the ager, gone after t
s = fresh()
s.run(G.fx('ev_beam', h=80, t=10), pos=(X0, FLOOR, Z0))
check(len([e for e in s.ents if e.etype == 'marker' and G.BEAM in e.tags]) == 1, 'ev_beam: one marker')
s.tick(14)
check(not [e for e in s.ents if e.etype == 'marker'], 'ev_beam: the marker is gone after t')

# ============================================================== F2 review fixes (HR-12 / HR-17 / HR-23 / HR-32 / HR-41 / HR-42 /
# HR-44 / HR-45): the executor's pitch with the module's real call arguments, the planes across the aim, the band's sweep,
# kept and following cards, and the view (every contact effect from the F5 camera and from first person)
PITCHED = getattr(G, 'PITCHED', ())    # qi_line: its pitch counts (the A8.9 dive straight down), clamped; every other preset level


def yawd(v):
    return round(((v + 180.0) % 360.0) - 180.0, 2)


def snapshot(s):
    return sorted((kind(s, e), tuple(round(v, 3) for v in e.pos), (yawd(e.rot[0]), round(e.rot[1], 2)),
                   json.dumps(s.nbt[e.id].get('transformation', {}), sort_keys=True), s.nbt[e.id].get('billboard'))
                  for e in s.cards())


def call_args(txt):
    out = {}
    for k, v in re.findall(r'(\w+):("[^"]*"|[^,}]+)', txt):
        out[k] = v.strip('"') if v.startswith('"') else (float(v) if '.' in v else int(v))
    return out


REAL = {}
for path, uses in calls_by.items():
    if path.startswith('p/') and path[2:] in api.KIT_PRESETS:
        for _rel, _ln, args in uses:
            if not args.startswith('with'):
                REAL.setdefault(path[2:], set()).add(tuple(sorted(call_args(args).items())))
# the storage calls: A9's streak at its probed length (core.a9), CS4 E1b's band sweep (her distance + 1 b)
for name, a in (('qi_cut', {'len': 40}), ('qi_cut', {'len': 120}), ('qi_band', dict(len=120, yaw=0, pitch=0, roll=0, sw=200))):
    if set(a) == set(api.KIT_PRESETS[name]):
        REAL.setdefault(name, set()).add(tuple(sorted(a.items())))
check(len(REAL) >= 30, f'pitch: the module calls {len(REAL)} presets with real arguments')
npitch = 0
for name in sorted(REAL):
    for args in sorted(REAL[name], key=str):
        a = dict(args)
        if set(a) != set(api.KIT_PRESETS[name]):
            continue
        for h in HEIGHT[name]:
            pos = (X0, FLOOR + h, Z0)
            ref = None
            for pitch in (0.0, -60.0, 60.0):
                s = fresh()
                s.run(G.fx(name, **a), pos=pos, rot=(30.0, pitch))
                snap = snapshot(s)
                npitch += 1
                tag = f'pitch: {name} {a} h {h} executor pitch {pitch:+.0f}'
                for e in s.cards():
                    if s.nbt[e.id].get('billboard') == 'center':
                        continue
                    low = card_lowest(s, e)
                    check(low is None or low >= FLOOR - 1e-3, f'{tag}: {kind(s, e)} {(low or 0) - FLOOR:.2f} b below the floor')
                if pitch == 0.0:
                    ref = snap
                elif name not in PITCHED:
                    check(snap == ref, f'{tag}: not level (the executor pitch moved / tilted its cards)')
check(npitch > 200, f'pitch: {npitch} runs')
# light_column upright, ambient_p1 / p2 level, at any look (HR-41 / HR-42): the same cards as at pitch 0
for name, h in (('light_column', 0.0), ('ambient_p1', 0.0), ('ambient_p2', 0.0)):
    s = fresh()
    s.run(G.fx(name), pos=(X0, FLOOR + h, Z0), rot=(10.0, 0.0))
    ref = snapshot(s)
    check(ref or name in G.PTCL, f'pitch: {name} makes cards')
    for pitch in (-90.0, -45.0, 45.0, 90.0):
        s = fresh()
        s.run(G.fx(name), pos=(X0, FLOOR + h, Z0), rot=(10.0, pitch))
        check(snapshot(s) == ref, f'pitch: {name} at look pitch {pitch}: the same level cards as at pitch 0')
        for e in s.cards():
            low = card_lowest(s, e) if s.nbt[e.id].get('billboard') != 'center' else None
            check(low is None or low >= FLOOR - 1e-3, f'pitch: {name} at look pitch {pitch}: {kind(s, e)} below the floor')


# ---------------------------------------------------------------- orientation: across the aim (HR-12)
def card_axes(s, e):
    """(world normal of the card plane, world long axis) of a fixed card"""
    st = tstate(s.nbt[e.id].get('transformation', {}))
    M = mm(rot_axis(st['lax'], st['roll']), rot_axis(st['ax'], st['spin']))
    E = mm(rot_y(math.radians(-e.rot[0])), rot_x(math.radians(e.rot[1])))
    plane = G.kind_info(kind(s, e))[0]
    n_loc = {'flat': (0, 1, 0), 'face': (0, 0, 1)}.get(plane, (0, 0, 1))
    n = mv(mm(E, M), n_loc)
    z = mv(mm(E, M), (0, 0, 1))
    return n, z


def facing(yaw):
    return (-math.sin(math.radians(yaw)), 0.0, math.cos(math.radians(yaw)))


Y0 = 30.0
for name, a, kinds, mode in (('qi_vert', dict(h=34, yaw=0, c=1), 'qi_arc_', 'across'),
                             ('qi_vert', dict(h=34, yaw=180, c=1), 'qi_arc_', 'across'),
                             ('qi_fan', dict(h=16, c=2), 'qi_arc_', 'across'),
                             ('qi_arc', dict(r=40, yaw=0, pitch=0, roll=35, c=1), 'qi_arcf_', 'across'),
                             ('qi_arc', dict(r=45, yaw=0, pitch=0, roll=-40, c=1), 'qi_arcf_', 'across'),
                             ('qi_wedge', dict(r=46, roll=40), 'qi_wedge', 'across'),
                             ('qi_arc', dict(r=40, yaw=0, pitch=0, roll=0, c=1), 'qi_arc_', 'flat'),
                             ('qi_arc', dict(r=40, yaw=0, pitch=0, roll=15, c=1), 'qi_arc_', 'flat'),
                             ('qi_line', dict(len=60), 'qline', 'line')):
    s = fresh()
    s.run(G.fx(name, **a), pos=(X0, FLOOR + 1.3, Z0), rot=(Y0, 0.0))
    blades = [e for e in s.cards() if kind(s, e).startswith(kinds) and s.nbt[e.id].get('billboard', 'fixed') == 'fixed']
    check(blades, f'orient: {name} {a}: its {kinds} cards')
    f_ = facing(Y0)
    for e in blades:
        n, z = card_axes(s, e)
        if mode == 'across':
            check(abs(sum(n[i] * f_[i] for i in range(3))) > 0.98, f'orient: {name} {a}: {kind(s, e)} stands across the aim '
                                                                     f'(normal . facing {sum(n[i] * f_[i] for i in range(3)):.2f})')
        elif mode == 'flat':
            check(abs(n[1]) > 0.95, f'orient: {name} {a}: {kind(s, e)} lies flat (normal {n})')
        else:
            check(abs(sum(z[i] * f_[i] for i in range(3))) < 0.02 and abs(z[1]) < 0.02,
                  f'orient: qi_line runs across the facing, level (axis {z})')
# qi_vert yaw 0 bulges to the executor's right, 180 to its left (A3 h1 / h3: PLAN §4.3)
side = {}
for yaw in (0, 180):
    s = fresh()
    s.run(G.fx('qi_vert', h=34, yaw=yaw, c=1), pos=(X0, FLOOR + 0.2, Z0), rot=(0.0, 0.0))
    e = [e for e in s.cards() if kind(s, e) == 'qi_arc_3'][0]
    _n, z = card_axes(s, e)
    side[yaw] = z[0]                   # executor yaw 0 faces +z: its right is -x
check(side[0] < -0.9 and side[180] > 0.9, f'orient: qi_vert yaw 0 bulges right, 180 left ({side})')


# ---------------------------------------------------------------- the bursts on the shape (F2 round 1, V2R-01)
def shape_point(s, e, frac):
    """the world point at frac of the card's own b extent (flat: local +z, face: local +y; the crescent's rim at 0.8, the
    wedge's point at 1) at its full size (the hrG scale), rolled as the card (view_px's math)"""
    st = tstate(s.nbt[e.id].get('transformation', {}))
    sc = [float(v) for v in cdata(s, e)['hrG']['transformation']['scale']]
    b = {'flat': (0, 0, 1), 'face': (0, 1, 0)}[G.kind_info(kind(s, e))[0]]
    v = mv(rot_axis(st['lax'], st['roll']), [b[i] * sc[i] * frac for i in range(3)])
    E = mm(rot_y(math.radians(-e.rot[0])), rot_x(math.radians(e.rot[1])))
    w = mv(E, [st['t'][i] + v[i] for i in range(3)])
    return tuple(e.pos[i] + w[i] for i in range(3))


FACE_R = getattr(G, 'FACE_ROLL', (20, 160))     # |roll| of the face mode (HR-12)
BURSTS = [('qi_arc', dict(r=40, yaw=20, pitch=0, roll=0, c=1)), ('qi_arc', dict(r=40, yaw=20, pitch=0, roll=15, c=1)),
          ('qi_arc', dict(r=36, yaw=0, pitch=0, roll=35, c=1)), ('qi_arc', dict(r=45, yaw=0, pitch=0, roll=-40, c=1)),
          ('qi_arc', dict(r=40, yaw=20, pitch=30, roll=90, c=2)), ('qi_arc', dict(r=40, yaw=-30, pitch=0, roll=140, c=3)),
          ('qi_arc', dict(r=40, yaw=0, pitch=-20, roll=-150, c=1)), ('qi_wedge', dict(r=46, roll=40)),
          ('qi_wedge', dict(r=14, roll=30)), ('qi_wedge', dict(r=30, roll=-120)), ('qi_wedge', dict(r=30, roll=0)),
          ('qi_wedge', dict(r=30, roll=10))]
BURSTS += [(n, dict(a)) for n in ('qi_arc', 'qi_wedge') for a in sorted(REAL.get(n, ()), key=str)]
nb, bmax = 0, 0.0
for name, a in BURSTS:
    face = FACE_R[0] <= abs(a["roll"]) <= FACE_R[1]
    for h in HEIGHT[name]:
        s = fresh()
        s.run(G.fx(name, **a), pos=(X0, FLOOR + h, Z0), rot=(Y0, 0.0))
        tag = f'bursts: {name} {a} h {h}'
        shp = [e for e in s.cards() if kind(s, e).startswith(('qi_arc', 'qi_wedge'))]
        check(shp and all(kind(s, e).startswith(('qi_arcf_', 'qi_wedgef')) == face for e in shp),
              f'{tag}: the {"face" if face else "flat"} kinds ({sorted({kind(s, e) for e in shp})})')
        check(s.parts, f'{tag}: its particle burst')
        if not shp or not s.parts:
            continue
        tip = shape_point(s, shp[-1], 0.8 if name == 'qi_arc' else 1.0)
        far = max(math.dist(p, tip) for _n, p in s.parts)
        nb += 1
        bmax = max(bmax, far)
        check(far <= 0.5, f'{tag}: every burst particle within 0.5 b of the {"rim" if name == "qi_arc" else "point"} '
                          f'({far:.2f} b; the {"face" if face else "flat"} mode)')
check(nb >= 20, f'bursts: {nb} runs')
print(f'bursts: {nb} runs, the farthest particle {bmax:.3f} b from its rim / point')

# ---------------------------------------------------------------- qi_line's direction at every module call (F2 round 1, VF2-1-01)
# HR-12 turned qi_line ACROSS its executor's facing (the kit's +90, pitch kept). Each module call runs in the sim (@s = her,
# yaw 0) and its line is checked by what the call is built for: `facing entity <x>` -> along the executor -> x (such a caller
# turns by -90 first: `... facing entity <x> feet rotated ~-90 ~ run ...qi_line`); pitched straight down (`rotated ~ 90`, the
# A8.9 / A13 dive) -> straight down; else (A4 / A5's slash) -> across her facing, level. Anything else fails here (decide).
QL_AT = (X0 + 3.0, FLOOR, Z0 + 4.0)           # the target of a `facing entity` call: a floor spot off her aim


def qline_axes(ln):
    """(card origin, card axis, the facing target or None) of every qi_line card the call line makes"""
    face_t = re.search(r'facing entity (@[aeps])(\[[^\]]*\])? (feet|eyes)', ln)
    s = fresh()
    s.run(f'summon minecraft:husk {X0} {FLOOR + (5.0 if face_t else 0.0)} {Z0} {{Tags:["rlk_mb_body"]}}')
    her = [e for e in s.ents if e.etype == 'husk'][0]
    tgt = None
    if face_t:
        sel = face_t.group(2) or ''
        tags = re.findall(r'tag=([\w.+-]+)', sel)
        if face_t.group(1) in ('@a', '@p'):
            ent = s.player
            ent.pos = list(QL_AT)
            ent.tags.update(tags)
        else:
            ty = (re.search(r'type=(?:minecraft:)?(\w+)', sel) or [None, 'marker'])[1]
            s.run(f'summon minecraft:{ty} {QL_AT[0]} {QL_AT[1]} {QL_AT[2]} {{Tags:{json.dumps(tags)}}}')
            ent = [e for e in s.ents if e.etype == ty and e is not her][-1]
        tgt = (ent.pos[0], ent.pos[1] + (ent.data.get('eye', 0.0) if face_t.group(3) == 'eyes' else 0.0), ent.pos[2])
    s.run(COND_Q.sub('', ln), ex=her, pos=tuple(her.pos), rot=(0.0, 0.0))
    return [(tuple(e.pos), card_axes(s, e)[1], tgt) for e in s.cards() if kind(s, e) == 'qline']


COND_Q = re.compile(r' (?:if|unless) score \S+ \S+ matches \S+')


def qline_verdict(ln):
    """(ok, what) for one call line"""
    got = qline_axes(ln)
    if not got:
        return False, 'no qi_line card'
    out = []
    for pos, z, tgt in got:
        if tgt is not None:
            d = [tgt[i] - pos[i] for i in range(3)]
            n = math.sqrt(sum(v * v for v in d)) or 1.0
            c = sum(z[i] * d[i] / n for i in range(3))
            out.append((c > 0.98, f'along the executor -> its facing target (cos {c:.2f})'))
        elif re.search(r'rotated \S+ 90\b', ln):
            out.append((z[1] < -0.98, f'straight down (axis y {z[1]:+.2f})'))
        elif re.search(r'\bfacing\b|rotated \S+ -?[1-9]', ln):
            out.append((False, 'an unclassified aim (facing / pitched): decide what the line is for and extend this check'))
        else:
            out.append((abs(z[2]) < 0.05 and abs(z[1]) < 0.05, f'across her facing, level (axis {tuple(round(v, 2) for v in z)})'))
    return all(ok for ok, _ in out), out[0][1]


# the hand-off form for an along-the-aim caller (F1's A10 dive line after the merge: f2_requests f2-7) and the bare form
DEMO = ('execute at @s positioned ~ ~1.0 ~ facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet{} run '
        'function rlk:boss/scarlet/fx/p/qi_line {{len:60}}')
ok, what = qline_verdict(DEMO.format(' rotated ~-90 ~'))
check(ok, f'qline: `facing entity <x> feet rotated ~-90 ~ run qi_line` runs along the aim to x ({what})')
ok, what = qline_verdict(DEMO.format(''))
check(not ok, f'qline: a bare `facing entity <x> run qi_line` runs across the aim, not to x ({what})')
if MERGED:
    qcalls = []
    for p in sorted(x for x in MOD.rglob('*.mcfunction') if not x.relative_to(MOD).as_posix().startswith('fx/')):
        for ln in p.read_text(encoding='utf-8').split('\n'):
            if 'fx/p/qi_line' in ln and not ln.startswith('#'):
                qcalls.append((p.relative_to(MOD).as_posix(), ln))
    check(len(qcalls) >= 3, f'qline: {len(qcalls)} module qi_line calls')
    for rel, ln in qcalls:
        ok, what = qline_verdict(ln)
        check(ok, f'qline: {rel}: the line runs {what} — `{ln[:150]}`')

# ---------------------------------------------------------------- qi_band's sweep (HR-32)
for sw in (25, 45, 200):
    s = fresh()
    s.run(G.fx('qi_band', **targs(api.KIT_PRESETS, 'qi_band', len=120, sw=sw)), pos=(X0, FLOOR + 1.1, Z0), rot=(Y0, 0.0))
    e = [e for e in s.cards() if kind(s, e) == 'qi_band_0'][0]
    t = cdata(s, e)['hrG']['transformation']['translation']
    E = mm(rot_y(math.radians(-e.rot[0])), rot_x(math.radians(e.rot[1])))
    w = mv(E, [float(v) for v in t])
    f_ = facing(Y0)
    along = sum(w[i] * f_[i] for i in range(3))
    check(abs(along - sw / 10) < 0.06 and abs(w[1]) < 0.02, f'band: sw {sw} sweeps {along:.2f} b along the aim (want {sw / 10})')

# ---------------------------------------------------------------- 홍련일섬's line: floor-safe, still through the executor (HR-44)
for h in (0.5, 1.0, 1.3, 1.62):
    for yaw in (0, 90):
        for roll in (13, -13, 30):
            for pitch in (-60.0, 0.0, 60.0):
                s = fresh()
                s.run(G.fx('scarlet_line', len=600, yaw=yaw, roll=roll), pos=(X0, FLOOR + h, Z0), rot=(Y0, pitch))
                for e in [e for e in s.cards() if kind(s, e) == 'scarlet_line']:
                    low = card_lowest(s, e)
                    tag = f'sline: h {h} yaw {yaw} roll {roll} pitch {pitch:+.0f}'
                    check(low >= FLOOR + 0.05, f'{tag}: its low corner {low - FLOOR:.2f} b over the floor (>= 0.05)')
                    st = tstate(s.nbt[e.id]['transformation'])
                    ax = mv(rot_axis(st['lax'], st['roll']), (1, 0, 0))
                    t = st['t']
                    cr = math.dist((0, 0, 0), (t[1] * ax[2] - t[2] * ax[1], t[2] * ax[0] - t[0] * ax[2], t[0] * ax[1] - t[1] * ax[0]))
                    check(cr < 0.02, f'{tag}: slid along its own length (still through the executor point; off-axis {cr:.3f})')

# ---------------------------------------------------------------- kept cards (HR-17): fx/keep_on .. keep_off
KEEP_T = getattr(api, 'KIT_KEEP_TAG', 'rlk_hr_fx_keep')
check((FX / 'keep_on.mcfunction').exists() and (FX / 'keep_off.mcfunction').exists(), 'keep: fx/keep_on and fx/keep_off exist')
if (FX / 'keep_on.mcfunction').exists():
    for clear in ('clear', 'dead', 'rnDie'):
        s = fresh()
        s.run(f'function {NSF}keep_on')
        s.run(G.fx('scarlet_line', len=600, yaw=90, roll=13), pos=(X0, FLOOR + 1.3, Z0), rot=(0.0, 0.0))
        s.run(G.fx('petal_burst', r=20), pos=(X0, FLOOR + 1.0, Z0))
        s.run(f'function {NSF}keep_off')
        s.run(G.fx('glint', c=1), pos=(X0, FLOOR + 1.5, Z0))
        kept = [e for e in s.cards() if KEEP_T in e.tags]
        rest = [e for e in s.cards() if KEEP_T not in e.tags]
        check(kept and any(kind(s, e) == 'scarlet_line' for e in kept) and rest and not any(k in ('glint_0', 'glint_1') for k in
                                                                                          [kind(s, e) for e in kept]),
              f'keep: the cards made between keep_on / keep_off carry {KEEP_T}, not the later ones')
        T0 = s.gt
        if clear == 'clear':
            s.run(f'function {NSF}clear')
        else:
            s.setsc(('e', s.player.id), clear, 1)
        s.tick(12)
        check(all(e.alive for e in kept) and not [e for e in rest if e.alive],
              f'keep: {clear}: the kept cards are alive {s.gt - T0} t after it, the others gone')
        s.setsc(('e', s.player.id), clear, 0) if clear != 'clear' else None
        s.tick(60)
        check(not s.cards() and f'{NSF}e/world' not in s.sched, f'keep: {clear}: the kept cards end with their life, the ager stops')
    s = fresh()
    s.run(f'function {NSF}keep_on')
    s.run(f'function {NSF}clear')
    s.run(G.fx('glint', c=1), pos=(X0, FLOOR + 1.5, Z0))
    check(not [e for e in s.cards() if KEEP_T in e.tags], 'keep: fx/clear ends a keep_on without keep_off')
    s.run(f'function {NSF}keep_on')
    s.run(G.fx('glint', c=1), pos=(X0, FLOOR + 1.5, Z0))
    s.run(f'function {NSF}uninstall')
    check(not s.cards(), 'keep: fx/uninstall removes the kept cards')

# ---------------------------------------------------------------- following cards (HR-23): fx/follow_on .. follow_off
check((FX / 'follow_on.mcfunction').exists() and (FX / 'follow_off.mcfunction').exists(), 'follow: fx/follow_on and fx/follow_off exist')
if (FX / 'follow_on.mcfunction').exists():
    s = fresh()
    s.run(f'summon minecraft:husk {X0} {FLOOR} {Z0} {{Tags:["rlk_mb_body"]}}')
    lead = [e for e in s.ents if e.etype == 'husk'][0]
    s.run(f'function {NSF}follow_on', ex=lead, pos=tuple(lead.pos))
    s.run(G.fx('yellow_tell', t=8), ex=lead, pos=(X0, FLOOR + 1.3, Z0))
    s.run(G.fx('blink_bubble'), ex=lead, pos=(X0, FLOOR + 1.3, Z0))
    s.run(f'function {NSF}follow_off', ex=lead, pos=tuple(lead.pos))
    s.run(G.fx('glint', c=1), pos=(X0, FLOOR + 1.5, Z0))
    fol = [e for e in s.cards() if not kind(s, e).startswith('glint')]
    still = [e for e in s.cards() if kind(s, e).startswith('glint')]
    dy = {e.id: e.pos[1] - lead.pos[1] for e in fol}
    p0 = {e.id: list(e.pos) for e in still}
    for step in range(3):
        lead.pos = [X0 + 1.5 * (step + 1), FLOOR + 0.4 * step, Z0 - 1.0 * (step + 1)]
        s.tick(1)
        check(fol and all(abs(e.pos[0] - lead.pos[0]) < 1e-6 and abs(e.pos[2] - lead.pos[2]) < 1e-6
                          and abs(e.pos[1] - lead.pos[1] - dy[e.id]) < 0.011 for e in fol if e.alive),
              f'follow: the cards made between follow_on / off stay on the lead (its x / z, their height over it) step {step}')
    check(all(e.pos == p0[e.id] for e in still if e.alive), 'follow: a card made after follow_off stays where it was made')
    lead.alive = False
    s.ents = [e for e in s.ents if e.alive]
    at = {e.id: list(e.pos) for e in fol if e.alive}
    s.tick(1)
    check(all(e.pos == at[e.id] for e in fol if e.alive and e.id in at), 'follow: a lead that is gone leaves its cards where they are')
    s.tick(60)
    check(not s.cards() and f'{NSF}e/world' not in s.sched, 'follow: the following cards expire, the ager stops')
    s = fresh()
    s.run(f'summon minecraft:husk {X0} {FLOOR} {Z0} {{Tags:["rlk_mb_body"]}}')
    lead = [e for e in s.ents if e.etype == 'husk'][0]
    s.run(f'function {NSF}follow_on', ex=lead, pos=tuple(lead.pos))
    s.run(f'function {NSF}clear')
    s.run(G.fx('glint', c=1), pos=(X0, FLOOR + 1.5, Z0))
    lead.pos = [X0 + 2, FLOOR, Z0]
    s.tick(1)
    check(all(abs(e.pos[0] - X0) < 1e-6 for e in s.cards()), 'follow: fx/clear ends a follow_on without follow_off')

# ---------------------------------------------------------------- view (HR-12 / HR-45): card pixels at 320 x 180, fov 70
VW, VH, VFOV, ALPHA_MIN, VIEW_MIN = 320, 180, 70.0, 0.05, 1500
KF = (VH / 2) / math.tan(math.radians(VFOV / 2))
F5_SEAT, F5_BACK, EYE, GAP = 2.3, 3.5, 1.62, 2.4    # README 13: the F5 seat 0.5 b over the avatar's head, camera 3.5 b back


def vdot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vcross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


class Cam:
    def __init__(self, eye, yaw, pitch, back=0.0):
        y, p = math.radians(yaw), math.radians(pitch)
        self.yaw, self.pitch = yaw, pitch
        self.f = (-math.sin(y) * math.cos(p), -math.sin(p), math.cos(y) * math.cos(p))
        self.r = (-math.cos(y), 0.0, -math.sin(y))
        self.u = vcross(self.r, self.f)
        self.c = tuple(eye[i] - back * self.f[i] for i in range(3))


_ALPHA = {}


def tex_alpha(stem):
    if stem not in _ALPHA:
        (w, h), (A0, A1, B0, B1), fn, _ss = G.TEXTURES[stem]
        _ALPHA[stem] = (w, h, [bytes(1 if fn(A0 + (i + 0.5) / w * (A1 - A0), B1 - (j + 0.5) / h * (B1 - B0))[3] >= ALPHA_MIN else 0
                                     for i in range(w)) for j in range(h)])
    return _ALPHA[stem]


QUADS = {'face': (((-1, 0, 0), (0, 1, 0)),), 'flat': (((-1, 0, 0), (0, 0, 1)),),
         'cross': (((-1, 0, 0), (0, 1, 0)), ((0, 0, 1), (0, 1, 0))), 'lance': (((-1, 0, 0), (0, 0, 1)), ((0, 1, 0), (0, 0, 1))),
         'lancex': (((-1, 0, 0), (0, 1, 0)), ((-1, 0, 0), (0, 0, 1)))}


def card_state(s, e, t):
    """the card as the client shows it half a tick after game tick t: its spawn transformation and the stage snapshots
    (custom data hrS / hrG / hrF, applied at the ager's stage events) with their interpolation"""
    n = s.nbt[e.id]
    cd = cdata(s, e)
    cur = tstate(n.get('transformation', {}))
    for t0, i, ev in s.events:
        if i != e.id or ev not in ('hrS', 'hrG', 'hrF') or t0 > t or ev not in cd:
            continue
        T = cd[ev].get('transformation', {})
        nxt = dict(cur)
        if 'translation' in T:
            nxt['t'] = [float(v) for v in T['translation']]
        if 'scale' in T:
            nxt['s'] = [float(v) for v in T['scale']]
        if 'left_rotation' in T:
            nxt['roll'], nxt['lax'] = aa(T['left_rotation'])
        if 'right_rotation' in T:
            nxt['spin'], nxt['ax'] = aa(T['right_rotation'])
        dur = int(cd[ev].get('interpolation_duration', 0))
        f = 1.0 if dur <= 0 else min(1.0, (t - t0 + 0.5) / dur)
        if f < 1.0:
            mid = {k: [cur[k][j] + (nxt[k][j] - cur[k][j]) * f for j in range(3)] for k in ('t', 's')}
            mid.update({'roll': cur['roll'] + (nxt['roll'] - cur['roll']) * f, 'lax': nxt['lax'],
                        'spin': cur['spin'] + (nxt['spin'] - cur['spin']) * f, 'ax': nxt['ax']})
            nxt = mid
        cur = nxt
    return cur


def raster(cam, P0, Va, Vb, ext, stem, mask):
    a0, a1, b0, b1 = ext
    N = vcross(Va, Vb)
    n2 = vdot(N, N)
    if n2 < 1e-14:
        return
    C = cam.c
    pts = []
    for a, b in ((a0, b0), (a1, b0), (a1, b1), (a0, b1)):
        X = tuple(P0[i] + a * Va[i] + b * Vb[i] - C[i] for i in range(3))
        pts.append((vdot(X, cam.r), vdot(X, cam.u), vdot(X, cam.f)))
    poly = []
    for k in range(4):
        p, q = pts[k], pts[(k + 1) % 4]
        if p[2] >= 0.05:
            poly.append(p)
        if (p[2] >= 0.05) != (q[2] >= 0.05):
            w = (0.05 - p[2]) / (q[2] - p[2])
            poly.append(tuple(p[i] + w * (q[i] - p[i]) for i in range(3)))
    if not poly:
        return
    xs = [VW / 2 + KF * p[0] / p[2] for p in poly]
    ys = [VH / 2 - KF * p[1] / p[2] for p in poly]
    x0, x1 = max(0, int(math.floor(min(xs)))), min(VW, int(math.ceil(max(xs))) + 1)
    y0, y1 = max(0, int(math.floor(min(ys)))), min(VH, int(math.ceil(max(ys))) + 1)
    if x0 >= x1 or y0 >= y1:
        return
    w, h, grid = tex_alpha(stem)
    CP = tuple(C[i] - P0[i] for i in range(3))
    q = -vdot(CP, N)
    VbN, NVa = vcross(Vb, N), vcross(N, Va)
    ca, cb = vdot(vcross(CP, Vb), N), vdot(vcross(Va, CP), N)
    dn0, dnr, dnu = vdot(cam.f, N), vdot(cam.r, N), vdot(cam.u, N)
    da0, dar, dau = vdot(cam.f, VbN), vdot(cam.r, VbN), vdot(cam.u, VbN)
    db0, dbr, dbu = vdot(cam.f, NVa), vdot(cam.r, NVa), vdot(cam.u, NVa)
    sa, sb = w / (a1 - a0), h / (b1 - b0)
    for py in range(y0, y1):
        sy = -(py + 0.5 - VH / 2) / KF
        rn, ra, rb = dn0 + sy * dnu, da0 + sy * dau, db0 + sy * dbu
        row = py * VW
        for px in range(x0, x1):
            sx = (px + 0.5 - VW / 2) / KF
            dn = rn + sx * dnr
            if -1e-12 < dn < 1e-12:
                continue
            lam = q / dn
            if lam <= 0.05:
                continue
            a = (ca + lam * (ra + sx * dar)) / n2
            if a < a0 or a >= a1:
                continue
            b = (cb + lam * (rb + sx * dbr)) / n2
            if b < b0 or b >= b1:
                continue
            if grid[min(h - 1, int((b1 - b) * sb))][min(w - 1, int((a - a0) * sa))]:
                mask[row + px] = 1


def view_px(s, cam):
    """the screen pixels covered by the cards (their sprites' alpha >= ALPHA_MIN) now"""
    mask = bytearray(VW * VH)
    for e in s.cards():
        st = card_state(s, e, s.gt)
        if all(abs(v) < 1e-9 for v in st['s']):
            continue
        plane, _wh, ext, _neu, tex, _d = G.kind_info(kind(s, e))
        M = mm(mm(rot_axis(st['lax'], st['roll']), [[st['s'][0], 0, 0], [0, st['s'][1], 0], [0, 0, st['s'][2]]]),
               rot_axis(st['ax'], st['spin']))
        bb = s.nbt[e.id].get('billboard', 'fixed')
        if bb == 'center':
            E = mm(rot_y(math.radians(-cam.yaw)), rot_x(math.radians(cam.pitch)))
        elif bb == 'vertical':
            E = rot_y(math.radians(-cam.yaw))
        else:
            E = mm(rot_y(math.radians(-e.rot[0])), rot_x(math.radians(e.rot[1])))
        EM = mm(E, M)
        t = mv(E, st['t'])
        P0 = tuple(e.pos[i] + t[i] for i in range(3))
        for va, vb in QUADS[plane]:
            raster(cam, P0, tuple(mv(EM, va)), tuple(mv(EM, vb)), ext, tex.split('/')[-1], mask)
    return sum(mask)


HER = (X0, FLOOR, Z0)                 # she faces +z (yaw 0) at the player standing GAP b away on her aim
PLY = (X0, FLOOR, Z0 + GAP)
# F-I (the body change): her chest = the module's default effect height at her body (s3lib.fx / fx_arc: 1.3 on S2a's 2.55-b
# body, F2's figure; 1.0 on S2d's 2.00-b player-size body, S2d's x 0.78 of every call height)
CHEST = 1.0
P5 = math.degrees(math.atan2(F5_SEAT - CHEST, GAP))    # the look at her chest: F5 (from the seat) 28.4, first person 14.5
P1 = math.degrees(math.atan2(EYE - CHEST, GAP))       # (S2a's body: 22.6 / 7.6)
CAMS = {'F5': Cam((PLY[0], PLY[1] + F5_SEAT, PLY[2]), 180.0, P5, F5_BACK), 'FP': Cam((PLY[0], PLY[1] + EYE, PLY[2]), 180.0, P1)}
COND = re.compile(r' (?:if|unless) score \S+ \S+ matches \S+')


# F2 round 1 (VF2-1-03): the deflect's judge (A13 k/255 glides her to the player's spot + 1 b): she hovers 1 b over the floor
# 0.5 b in front of the player, who looks up at her chest; first person is checked at these look pitches
JUDGE_HER = (PLY[0], FLOOR + 1.0, PLY[2] - 0.5)
JUDGE_LOOKS = (-30.0, -50.0, -70.0, -85.0)


def view_scene(first_person, look=None):
    s = fresh()
    s.player.pos = list(PLY)
    s.player.rot = [180.0, look if look is not None else P1 if first_person else P5]
    her_at = JUDGE_HER if look is not None else HER
    s.run(f'summon minecraft:husk {her_at[0]} {her_at[1]} {her_at[2]} {{Tags:["rlk_mb_body"]}}')
    her = [e for e in s.ents if e.etype == 'husk'][0]
    if first_person:
        s.player.tags.add('rlk_body')
    else:
        s.run(f'summon minecraft:armor_stand {PLY[0]} {PLY[1]} {PLY[2]} {{Tags:["rlk_body","rlk_av"]}}')
        [e for e in s.ents if e.etype == 'armor_stand'][0].rot = [180.0, P5]
    return s, her


def view_of(lines, view, look=None):
    """the most card pixels over the 7 ticks after the module's own call lines ran (@s = her) in that view's scene (look:
    the judge scene in first person at that look pitch)"""
    s, her = view_scene(view == 'FP', look)
    cam = CAMS[view] if look is None else Cam((PLY[0], PLY[1] + EYE, PLY[2]), 180.0, look)
    for ln in lines:
        m = re.search(r'tag=rlk_hr_cut,scores=\{hr=(\d+)\}', ln)
        if m and not [e for e in s.ents if 'rlk_hr_cut' in e.tags]:
            s.run(f'summon minecraft:marker {PLY[0]} {PLY[1]} {PLY[2]} {{Tags:["rlk_hr_cut"]}}')
            s.setsc(('e', [e for e in s.ents if 'rlk_hr_cut' in e.tags][0].id), 'hr', int(m.group(1)))
        s.run(COND.sub('', ln), ex=her, pos=tuple(her.pos), rot=(0.0, 0.0))
    best = 0
    for _ in range(7):
        s.tick(1)
        best = max(best, view_px(s, cam))
    return best


if MERGED:
    # every contact effect: P1's hits at her (A1, A2, A3 h1-h5, A5's slash) and the gauntlets' cuts at the cut spot (A8.1-A8.8,
    # R1 / R3 / A13 reuse them), each call line exactly as the module generates it
    by_file = {}
    for p in sorted(MOD.glob('p/**/*.mcfunction')):
        rel = p.relative_to(MOD).as_posix()
        top = rel.split('/')[1]
        for ln in p.read_text(encoding='utf-8').split('\n'):
            m = re.search(r'fx/p/(qi_\w+)', ln)
            if not m or ln.startswith('#'):
                continue
            her_hit = top in ('a1', 'a2', 'a3') or (top == 'a4' and m.group(1) == 'qi_line' and rel.endswith('tick.mcfunction'))
            if her_hit or 'tag=rlk_hr_cut' in ln:
                # a site = one file's calls of one preset with its args (the avatar / first-person variants together)
                by_file.setdefault((rel, ln.split('fx/p/')[1]), []).append(ln)
    sites = {}
    for (rel, call), lines in sorted(by_file.items()):
        sig = tuple(sorted(re.sub(r',scores=\{hr=\d+\}', '', COND.sub('', x)) for x in lines))
        sites.setdefault(sig, (f'{call} ({rel})', lines))
    check(len(sites) >= 15, f'view: {len(sites)} contact effects found in the module')
    for key, lines in sorted(sites.values()):
        fan = 'qi_fan' in key          # A1's swing fan (4 t before the hit; a 1-bh fan 4.7 b from the F5 camera)
        # F-I: F2's F5 floor 250 px was for S2a's 1.6-b fan (h 16); S2d's player-size body calls it 1.3 b tall (h 13, s2d-3),
        # so the floor scales with its area: 250 x (13 / 16)^2 = 165
        for view in ('F5', 'FP'):
            px = view_of(lines, view)
            need = 165 if fan and view == 'F5' else VIEW_MIN
            check(px >= need, f'view: {key[:110]}: {px} card px in {view} (>= {need})')
    # HR-45: the player-anchored effects (the 홍련일섬 line of CS1 C8 and of the instant deaths, the deflect's gold starburst
    # and light column) from the F5 camera and in first person (no avatar: the camera on the player's own axis)
    anchored = {}
    for p in sorted(MOD.rglob('*.mcfunction')):
        rel = p.relative_to(MOD).as_posix()
        if rel.startswith('fx/'):
            continue
        for ln in p.read_text(encoding='utf-8').split('\n'):
            m = re.search(r'fx/p/(scarlet_line|clash_gold|light_column)\b', ln)
            if m and 'at @e[tag=rlk_body,limit=1]' in ln and not ln.startswith('#'):
                anchored.setdefault((rel, m.group(1)), []).append(ln)
    check(len(anchored) >= 4, f'view: {len(anchored)} player-anchored effects')
    FULL = 0.9 * VW * VH                # a card sheet over the camera that fills the screen is not a visible effect
    for (rel, name), lines in sorted(anchored.items()):
        judge = rel == 'shield/judge.mcfunction'
        for view, need in (('F5', 300), ('FP', VIEW_MIN)):
            if judge and view == 'FP':
                continue                 # the judge: first person in its own scene below
            px = view_of(lines, view)
            check(need <= px < FULL, f'view: {rel} {name}: {px} card px in {view} (>= {need}, < 90 % of the frame; HR-45: '
                                     f'first person)')
        # VF2-1-03: the judge's starburst / column in first person where the judge happens: she 1 b over the player's spot,
        # the player looking up at her (base: 0 px at every look <= 0, or the whole screen under the leaned column)
        seen = []
        for look in (JUDGE_LOOKS if judge else ()):
            px = view_of(lines, 'FP', look)
            seen.append(f'{-look:.0f} deg {px}')
            check(VIEW_MIN <= px < FULL, f'view: {rel} {name}: {px} card px in first person at the judge, looking up '
                                         f'{-look:.0f} deg (>= {VIEW_MIN}, < 90 % of the frame)')
        if seen:
            print(f'view: the judge in first person, {name} looking up: ' + ', '.join(seen) + ' px')
    check(sum(1 for (rel, _n) in anchored if rel == 'shield/judge.mcfunction') == 2, 'view: the judge\'s starburst and column')

# ============================================================== props
for name, (doc, looks, bb, anim) in G.PROPS.items():
    spec = api.KIT_PROPS[name]
    lks = list(spec.get('look', [None]))
    s = fresh()
    s.run(f'summon minecraft:item_display {X0} {FLOOR + 1.2} {Z0} {{Tags:["rlk_hr_p","rlk_room"],teleport_duration:1}}')
    d = [e for e in s.ents if e.etype == 'item_display'][0]
    n0 = len(s.ents)
    for lk in lks:
        line = api.K.prop(name, **({'look': lk} if lk else {}))
        s.run(line, ex=d, pos=tuple(d.pos))
        if name != 'seat_rock':
            check(len(s.ents) == n0, f'props: {name} {lk} dressed in place (no extra entity)')
        nb = s.nbt[d.id]
        kd, scl, *tint = looks[lk]          # I1b: a look may carry a tint (the halo's p1 / p2 under p1b / p2b)
        if name == 'seat_rock':
            check(nb['item']['id'] == 'minecraft:tuff', f'props: seat rock is vanilla tuff {nb.get("item")}')
            items = s.cards(G.FOLLOW_STAY)
            want = {'bottle': 1, 'bare': 0, 'set': 2}[lk]
            check(len(items) == want, f'props: seat_rock {lk}: {len(items)} items, want {want}')
            for it in items:
                check(s.nbt[it.id]['item']['id'] in ('minecraft:potion', 'minecraft:bowl'), 'props: seat items vanilla')
                check(it.pos[1] >= d.pos[1] + 0.19, f'props: seat item on the stone top ({it.pos[1] - d.pos[1]:.2f})')   # S2d: top 0.24
        elif kd is None:
            check(nb['transformation']['scale'] == [0, 0, 0], f'props: {name} {lk} hidden')
        else:
            check(nb['item']['components']['minecraft:item_model'] == G.NS_TEX + kd and nb['billboard'] == bb,
                  f'props: {name} {lk} look {nb["item"]["components"].get("minecraft:item_model")} {nb.get("billboard")}')
            sc = nb['transformation']['scale']
            check(abs(sc[0] - scl) < 1e-6, f'props: {name} {lk} scale {sc} vs {scl}')
            col = nb['item']['components'].get('minecraft:custom_model_data', {}).get('colors', [None])[0]
            check(col == (tint[0] if tint else G.WHITE), f'props: {name} {lk} tint {col}')
    if name == 'moon_halo':
        # I1b (requests s1k-3 / s2b-4): p1b / p2b = the same sprites as p1 / p2, about 20 % brighter (a tint only darkens:
        # the base looks carry 1 / 1.2 of white, the bright ones white)
        for base in ('p1', 'p2'):
            kb, _sb, *tb = looks[base]
            kh, _sh, *th = looks[base + 'b']
            ratio = (th[0] if th else G.WHITE) % 256 / ((tb[0] if tb else G.WHITE) % 256)
            check(kb == kh and 1.15 <= ratio <= 1.25, f'props: moon_halo {base}b = {base}\'s sprite x {ratio:.3f} brighter')
    s.run(api.K.prop(name, **({'look': lks[-1]} if lks[-1] else {})), ex=d, pos=tuple(d.pos))
    check(len(s.ents) == n0 + (2 if name == 'seat_rock' else 0), f'props: {name} re-dress idempotent')
    if anim == 'd':
        s.tick(13)
        frames = [ev[6:] for t, i, ev in s.events if i == d.id and ev.startswith('model:')]
        check(set(frames) == {G.NS_TEX + 'disc_0', G.NS_TEX + 'disc_1'} and len(frames) >= 4,
              f'props: the disc swaps its two frames ({frames})')
        rots = [m for t, i, m in s.merges if i == d.id and 'start_interpolation' in m]
        check(len(rots) >= 4 and all('interpolation_duration:3' in m and 'left_rotation' in m for m in rots),
              'props: the disc turns a quarter per 3 t')
        d.alive = False
        s.ents = [e for e in s.ents if e.alive]
        s.tick(3)
        check(f'{NSF}e/anim' not in s.sched, 'props: the anim chain stops with the last prop')
    if anim == 'p':
        s.tick(41)
        rots = [m for t, i, m in s.merges if i == d.id and 'left_rotation' in m]
        check(len(rots) >= 2, f'props: the big petal rocks ({len(rots)})')
# a prop on a marker: one follower that stays on it and goes with it
for name, kw in (('disc', {}), ('moon_halo', {'look': 'p1'}), ('lotus', {'look': 'bud'}), ('petal_big', {'look': 'whole'})):
    s = fresh()
    s.run(f'summon minecraft:marker {X0} {FLOOR + 1} {Z0} {{Tags:["rlk_hr_pm"]}}')
    m = [e for e in s.ents if e.etype == 'marker'][0]
    line = api.K.prop(name, **kw)
    s.run(line, ex=m, pos=tuple(m.pos))
    fol = s.cards(G.FOLLOW)
    check(len(fol) == 1, f'props: {name} on a marker: one follower ({len(fol)})')
    s.run(line, ex=m, pos=tuple(m.pos))
    fol = s.cards(G.FOLLOW)
    check(len(fol) == 1, f'props: {name} re-called: still one follower')
    f = fol[0]
    m.pos = [X0 + 5, FLOOR + 3, Z0 - 2]
    s.tick(2)
    check(math.dist(f.pos, m.pos) < 1e-6, f'props: {name} follower stays on the marker {f.pos}')
    s.run(f'function {NSF}clear')
    check(f.alive, 'props: fx/clear (pause) keeps the follower')
    s.run('kill @e[type=minecraft:marker]')
    s.tick(2)
    check(not s.cards(G.FOLLOW), f'props: {name} follower gone with its marker')
# seat rock: the items go with the stone, re-look replaces them
s = fresh()
s.run(f'summon minecraft:item_display {api.SEAT_POS[0]} {api.SEAT_POS[1]} {api.SEAT_POS[2]} {{Tags:["rlk_hr_seat"]}}')
d = [e for e in s.ents if e.etype == 'item_display'][0]
s.run(api.K.prop('seat_rock', look='set'), ex=d, pos=tuple(d.pos))
check(len(s.cards(G.FOLLOW_STAY)) == 2, 'props: seat set = bottle + cup')
s.run(api.K.prop('seat_rock', look='bottle'), ex=d, pos=tuple(d.pos))
check(len(s.cards(G.FOLLOW_STAY)) == 1, 'props: seat re-look bottle: the cup goes')
d.alive = False
s.ents = [e for e in s.ents if e.alive]
s.tick(2)
check(not s.cards(G.FOLLOW_STAY), 'props: the seat items go with the stone')

# ============================================================== clear (pause / death_start / cleanup)
s = fresh()
s.run(G.fx('qi_arc', r=36, yaw=0, pitch=0, roll=0, c=1), pos=(X0, FLOOR + 1.3, Z0))
s.run(G.fx('petals_drift'), pos=(X0, FLOOR + 1.2, Z0))
s.run(G.fx('afterimage', len=20), pos=(X0, FLOOR + 1.2, Z0))
s.run(G.fx('ev_beam', h=80, t=20), pos=(X0, FLOOR, Z0))
s.run(f'function {NSF}clear')
check(not s.cards() and not [e for e in s.ents if e.etype == 'marker'], 'clear: every card (all pools) and beam')
check(s.sc('#n', OBJ) == 0 and s.sc('#na', OBJ) == 0 and s.sc('#ni', OBJ) == 0, 'clear: counts zeroed')
s = fresh()
s.run(G.fx('dive_impact', r=26), pos=(X0, FLOOR + 0.1, Z0))
s.setsc(('e', s.player.id), 'dead', 1)
s.tick(1)
check(not s.cards(), 'clear: a dead player clears the cards')

# ============================================================== uninstall
s = fresh()
s.storage.setdefault('rlk:hr', {})['core'] = {'x': 1}
s.run(f'function {NSF}test/stage', pos=(X0, FLOOR, Z0 + 10))
s.run(G.fx('light_column'), pos=(X0, FLOOR, Z0))
s.run(G.fx('ev_beam', h=60, t=30), pos=(X0, FLOOR, Z0))
s.run(f'summon minecraft:marker {X0} {FLOOR + 1} {Z0} {{Tags:["rlk_hr_pm"]}}')
s.run(api.K.prop('lotus', look='bud'), ex=[e for e in s.ents if e.etype == 'marker'][0])
s.run(f'summon minecraft:item_display {X0} {FLOOR} {Z0} {{Tags:["rlk_hr_seat"]}}')
seat = [e for e in s.ents if e.etype == 'item_display' and 'rlk_hr_seat' in e.tags][0]
s.run(api.K.prop('seat_rock', look='set'), ex=seat)
s.run(G.hud('warn', on=1))
s.run(G.hud('line', id=3))
s.run(G.hud('skip', s=2))
s.run(f'function {NSF}test/hud')
s.run(f'function {NSF}uninstall')
check(not s.cards() and not s.cards(G.FOLLOW) and not s.cards(G.FOLLOW_STAY) and not [e for e in s.ents if G.DEMO in e.tags],
      'uninstall: cards, followers, seat items, stand-ins')
check(not [e for e in s.ents if e.etype == 'marker' and G.BEAM in e.tags], 'uninstall: beams')
check(not (s.objectives & ({OBJ} | set(G.OBJECTIVES))), 'uninstall: objectives removed')
check(not [k for k in s.scores if k[1] in ({OBJ} | set(G.OBJECTIVES))], 'uninstall: no kit scores left')
check('fx' not in s.storage.get('rlk:hr', {}) and s.storage['rlk:hr'].get('core') == {'x': 1}, 'uninstall: storage fx only')
check(G.WARN_BAR not in s.bossbars, 'uninstall: the warn bossbar removed')
check(not [k for k in s.sched if 'scarlet/fx' in k], f'uninstall: schedules cleared {s.sched}')
check(not [e for e in s.ents if any(t.startswith(TAG) for t in e.tags)], 'uninstall: no kit tag left on any entity')

# ============================================================== sounds
ids = set(SOUND_IDS.read_text().split()) if SOUND_IDS.exists() else None
check(ids is not None, f'sounds: the sound list {SOUND_IDS} exists')
for name, layers in G.SOUNDS.items():
    check(tuple(layers) == tuple(api.KIT_SOUND_RECIPES[name]), f'sounds: {name} = the api recipe')
    txt = fbody(f'snd/{name}')
    for ev, vol, pitch in layers:
        check(ids is None or f'minecraft:{ev}' in ids, f'sounds: {name}: {ev} is not a vanilla sound id')
        check(0.5 <= pitch <= 2.0 and 0 < vol <= 1.0, f'sounds: {name}: vol {vol} pitch {pitch}')
        check(L.sound(ev, vol, pitch) in txt, f'sounds: {name}: mboss_lib.sound line (min volume rule)')
for p in FX.rglob('*.mcfunction'):
    for ln in p.read_text(encoding='utf-8').split('\n'):
        for m in re.finditer(r'playsound (\S+)', ln):
            check(ids is None or m.group(1) in ids, f'sounds: {p.name}: {m.group(1)}')
s = fresh()
s.run(f'function {NSF}snd/a1_hit', pos=(X0, FLOOR, Z0))
check(len(s.sounds) == len(G.SOUNDS['a1_hit']), 'sounds: a recipe plays its layers')

# ============================================================== hud
SUBS = re.compile(r'text:"([^"]*)"')


def subtitles(s):
    return [SUBS.search(t).group(1) for _g, t in s.titles if t.startswith('subtitle {')]


# F2 (HR-16): the subtitle is drawn at 2x and never wraps: every subtitle <= 192 font px (the Auto GUI width at 1920 x 1200);
# a wider line is shown as api.LINE_PAGES (consecutive subtitles, the pages joined with one space = the line verbatim)
PAGES = getattr(api, 'LINE_PAGES', {})
ADV = {' ': 4, ',': 2, '.': 2, '!': 2, '?': 6}


def font_px(t):
    return sum(8 if 0xAC00 <= ord(c) <= 0xD7AF else ADV[c] for c in t)


for lid, text in api.LINES.items():
    check(font_px(text) <= 192 or lid in PAGES, f'hud: line {lid} ({font_px(text)} px) wider than 192 px has pages')
for lid, pages in PAGES.items():
    check(' '.join(pages) == api.LINES[lid] and all(font_px(p) <= 192 for p in pages), f'hud: line {lid} pages verbatim, <= 192 px')
for lid, text in api.LINES.items():
    s = fresh()
    T0 = s.gt
    s.run(G.hud('line', id=lid))
    s.tick(api.LINE_AT[lid][2] + 20)
    subs = subtitles(s)
    pages = PAGES.get(lid, (text,))
    want = [x for pg in pages for x in G.typed(pg)]
    check(subs and subs[-1] == pages[-1], f'hud: line {lid} ends with its last page ({subs[-1:]})')
    check(subs == want, f'hud: line {lid} reveals its pages in prefixes ({len(subs)} steps, want {len(want)})')
    check(all(font_px(x) <= 192 for x in subs), f'hud: line {lid}: every subtitle <= 192 px ({max(font_px(x) for x in subs)})')
    check(len(subs) >= 2, f'hud: line {lid} {len(subs)} steps')
    hats = [x for x in s.sounds if x[0] == 'minecraft:block.note_block.hat']
    check(len(hats) == len(subs) and all(abs(x[1] - 0.3) < 1e-9 for x in hats), 'hud: one quiet hat (0.3) per step')
    gaps = sorted({g for g, t in s.titles if t.startswith('subtitle {')})
    firsts = {sum(len(G.typed(pg)) for pg in pages[:k]) for k in range(1, len(pages))}
    check(all(b - a == 2 or (k + 1 in firsts and b - a >= 2) for k, (a, b) in enumerate(zip(gaps, gaps[1:]))),
          f'hud: line {lid} steps 2 t apart (a new page at its own tick)')
    check(gaps[-1] - T0 < api.LINE_AT[lid][2] - 9, f'hud: line {lid} its last step is up >= 10 t')
    last_times = [t for g, t in s.titles if t.startswith('times ')][-1]
    _z, stay, fade = (int(x) for x in last_times.split()[1:])
    check(gaps[-1] - T0 + stay == api.LINE_AT[lid][2] and fade == G.LINE_FADE,
          f'hud: line {lid} held {gaps[-1] - T0 + stay} t = LINE_AT ({api.LINE_AT[lid][2]})')
    check(s.sc('#lnA', OBJ) == 0 and f'{NSF}hud/e/ln' not in s.sched, f'hud: line {lid} chain ends')
    check(all('font:"minecraft:default"' in t and f'color:"{api.LINE_COLOR}"' in t for g, t in s.titles
              if t.startswith('subtitle {')), 'hud: line colour #F2D0E8, font named')
# typed(): two syllables per step (Hangul syllables; punctuation rides on its syllable)
for text in api.LINES.values():
    steps = G.typed(text)
    for a, b in zip([''] + steps, steps):
        grown = len(re.sub(r'[ .,!?…]', '', b)) - len(re.sub(r'[ .,!?…]', '', a))
        check(1 <= grown <= 2 or (grown == 0 and b == text), f'hud: typed step {a!r} -> {b!r} grows {grown}')
# a line during an overlay: the overlay glyph is re-sent as the title with its remaining hold; ttl_blank once it ended
s = fresh()
T0 = s.gt
s.run(G.hud('ovl', g='black', **{'in': 0, 'hold': 10, 'out': 3}))
check(s.sc(('e', s.player.id), 'vBig') == 13, 'hud: ovl vBig = in + hold + out')
glyph = chr(api.OVERLAYS['black'])
check(any(t.startswith('title {') and glyph in t for g, t in s.titles), 'hud: ovl shows the black glyph')
s.tick(2)
s.run(G.hud('line', id=13))
s.tick(1)
after = [(g, t) for g, t in s.titles if g >= T0 + 2]
check(any(t.startswith('title {') and glyph in t for g, t in after), 'hud: a line step during the overlay re-sends the glyph')
check(not any(t == 'title {"text":""}' for g, t in after if g < T0 + 13), 'hud: no blank title while the overlay is up')
s.tick(30)
blank = [g for g, t in s.titles if t == 'title {"text":""}']
check(blank and min(blank) >= T0 + 13, f'hud: ttl_blank once the overlay ended ({[b - T0 for b in blank][:3]})')
check(subtitles(s)[-1] == api.LINES[13], 'hud: the line text comes back after the overlay')
for g in api.OVERLAYS:
    s = fresh()
    s.run(G.hud('ovl', g=g, **{'in': 2, 'hold': 4, 'out': 2}))
    tt = [t for _g, t in s.titles if t.startswith('title {')]
    check(tt and chr(api.OVERLAYS[g]) in tt[-1], f'hud: ovl {g} glyph')


# F2 (HR-30): a line is never dimmed or dropped by an overlay's fade. The vanilla client's title state (Gui: times / title /
# subtitle / clear / reset; titleTime counts down each client tick after the tick's packets; the title and the subtitle share
# one alpha: fade-in, stay, fade-out) replayed from the titles the kit sends, at the frames of every tick of the line.
def client(s, t_to):
    st = {'title': None, 'sub': None, 'tt': 0, 'fi': 10, 'stay': 70, 'fo': 20}
    byt, out = {}, {}
    for g, t in s.titles:
        byt.setdefault(g, []).append(t)
    for T in range(min(byt), t_to):
        for t in byt.get(T, []):
            if t.startswith('times '):
                st['fi'], st['stay'], st['fo'] = (int(x) for x in t.split()[1:4])
                if st['tt'] > 0:
                    st['tt'] = st['fi'] + st['stay'] + st['fo']
            elif t.startswith('title '):
                st['title'], st['tt'] = t[6:], st['fi'] + st['stay'] + st['fo']
            elif t.startswith('subtitle '):
                st['sub'] = t[9:]
            elif t in ('clear', 'reset'):
                st['title'], st['sub'], st['tt'] = None, None, 0
                if t == 'reset':
                    st['fi'], st['stay'], st['fo'] = 10, 70, 20
        if st['tt'] > 0:
            st['tt'] -= 1
            if st['tt'] <= 0:
                st['title'], st['sub'] = None, None
        alpha = 255
        for part in (0.0, 0.5, 0.99):
            if st['title'] is None or st['tt'] <= 0:
                alpha = 0
                continue
            f, lv = st['tt'] - part, 255
            if st['tt'] > st['fo'] + st['stay'] and st['fi']:
                lv = int((st['fi'] + st['stay'] + st['fo'] - f) * 255 / st['fi'])
            if st['tt'] <= st['fo'] and st['fo']:
                lv = int(f * 255 / st['fo'])
            alpha = min(alpha, max(0, min(255, lv)))
        m = SUBS.search(st['sub']) if st['sub'] else None
        out[T] = (alpha if alpha > 8 else 0, m.group(1) if m else None)
    return out


for case, calls in (('CS1 C4 black + line 15, line 16 under negative / pinkwhite / red_tint (C7-C8)',
                     [(0, G.hud('ovl', g='black', **{'in': 0, 'hold': 10, 'out': 3})), (4, G.hud('line', id=15)),
                      (44, G.hud('line', id=16)), (61, G.hud('ovl', g='negative', **{'in': 0, 'hold': 4, 'out': 0})),
                      (65, G.hud('ovl', g='pinkwhite', **{'in': 0, 'hold': 4, 'out': 10})),
                      (69, G.hud('ovl', g='red_tint', **{'in': 0, 'hold': 4, 'out': 20}))]),
                    ('the skip\'s black + line 11', [(0, G.hud('ovl', g='black', **{'in': 0, 'hold': 20, 'out': 6})),
                                                     (1, G.hud('line', id=11))]),
                    ('an overlay fading in under a line', [(0, G.hud('line', id=13)),
                                                           (6, G.hud('ovl', g='white', **{'in': 8, 'hold': 4, 'out': 8}))])):
    s = fresh()
    T0 = s.gt
    for dt, line in sorted(calls, key=lambda c: c[0]):
        while s.gt < T0 + dt:
            s.tick(1)
        s.run(line)
    s.tick(120)
    cl = client(s, s.gt)
    for dt, line in calls:
        m = re.search(r'\{id:(\d+)\}', line)
        if not m:
            continue
        lid = int(m.group(1))
        pages = PAGES.get(lid, (api.LINES[lid],))
        want = [x for pg in pages for x in G.typed(pg)]
        span = range(T0 + dt, T0 + dt + api.LINE_AT[lid][2] - 1)     # (its own fade starts in the last tick's frames)
        dim = [(T - T0, cl[T][0]) for T in span if cl[T][0] < 255 or not cl[T][1]]
        check(not dim, f'hud: {case}: line {lid} at full alpha, never dropped (dimmed / dropped at {dim[:6]})')
        seen = []
        for T in span:
            if cl[T][1] and (not seen or seen[-1] != cl[T][1]):
                seen.append(cl[T][1])
        check(seen == want, f'hud: {case}: line {lid} every typing step shown ({len(seen)} of {len(want)})')
# the warn bossbar: on, idempotent, off, on again
s = fresh()
s.run(G.hud('warn', on=1))
bb = s.bossbars.get(G.WARN_BAR)
check(bb and bb['visible'] is True and bb['players'] == '@a[tag=player]', f'hud: warn bossbar shown {bb}')
txt = ''.join(re.findall(r'text:"([^"]*)"', bb['name']))
check(txt == api.WARN_TEXT, f'hud: warn text = api.WARN_TEXT ({txt})')
check(f'text:"{api.WARN_HL[0]}",color:"{api.WARN_HL[1]}"' in bb['name'], 'hud: 즉사 highlighted')
s.run(G.hud('warn', on=1))
check(len(s.bossbars) == 1, 'hud: warn re-open is idempotent')
s.run(G.hud('warn', on=0))
check(s.bossbars[G.WARN_BAR]['visible'] is False, 'hud: warn off')
s.run(G.hud('warn', on=1))
check(s.bossbars[G.WARN_BAR]['visible'] is True, 'hud: warn on again')
# the skip prompt
s = fresh()
for k in range(5):
    s.run(G.hud('skip', s=k))
    t = [t for _g, t in s.titles if t.startswith('actionbar')][-1]
    parts = re.findall(r'text:"([^"]*)",color:"(#[0-9A-F]{6})"', t)
    check([p[0] for p in parts] == [api.SKIP_TEXT, api.SKIP_HINT], f'hud: skip text verbatim {parts}')
    check(parts[0][1] == G.SKIP_COLS[k] and parts[1][1] == api.SKIP_COLOR, f'hud: skip step {k} colours {parts}')
    check(s.sc(('e', s.player.id), 'hudHold') == 2, 'hud: skip sets hudHold 2')
s.run(G.hud('skip', s=5))
# F2 (HR-29): the prompt goes, hudHold runs out by itself (the intro holds the HUD every tick until its end)
check(s.titles[-1][1] == 'actionbar ""' and s.storage['rlk:hr']['fx']['hud']['skip'] in (0, '0b', False),
      'hud: skip s 5 clears it')
check(G.SKIP_COLS[0] == api.SKIP_COLOR, 'hud: skip starts grey #A8A8B0')
# clear
s = fresh()
s.run(G.hud('warn', on=1))
s.run(G.hud('line', id=6))
s.run(G.hud('skip', s=1))
s.run(G.hud('ovl', g='white', **{'in': 0, 'hold': 40, 'out': 5}))
s.tick(3)
s.run(G.hud('clear'))
s.tick(20)
check(s.bossbars[G.WARN_BAR]['visible'] is False, 'hud: clear: warn off')
check(not [k for k in s.sched if 'hud/e' in k] and s.sc('#lnA', OBJ) == 0, 'hud: clear: the line stops')
check(any(t == 'subtitle ""' for g, t in s.titles[-6:]) and any(t == 'clear' for g, t in s.titles[-6:]),
      'hud: clear: the line blanked and the overlay cleared')
check(any(t == 'actionbar ""' for g, t in s.titles[-6:]), 'hud: clear: the skip prompt off')

# ============================================================== static
STR_OK = set(api.LINES.values()) | {'', api.SKIP_TEXT, api.SKIP_HINT, api.WARN_HL[0], '홍련 sounds: ', '$(t)', '$(cur)',
                                    '$(ch)', '$(cs)'} | {chr(v) for v in api.OVERLAYS.values()} | {chr(api.VIG), chr(G.SP_NEG1)}
STR_OK |= {x for pages in PAGES.values() for pg in pages for x in G.typed(pg)}
for p in FX.rglob('*.mcfunction'):
    rel = p.relative_to(FX).as_posix()
    txt = p.read_text(encoding='utf-8')
    check(txt.startswith('# Generated by tools/build_mboss_hr_fx.py'), f'static: {rel} header')
    for i, line in enumerate(txt.split('\n'), 1):
        s_ = line.lstrip()
        if not s_ or s_.startswith('#'):
            continue
        check(not G.NEG_LIT.search(s_), f'static: {rel}:{i} negative literal')
        check(s_.startswith('$') == ('$(' in s_), f'static: {rel}:{i} macro-ness')
        for rid in re.findall(r'"(rlk:[^"]+)"', s_):
            check(rid == rid.lower(), f'static: {rel}:{i} uppercase id {rid}')
        # every text component names its font; a kit-font component is never a root (always inside extra:[...])
        for m in re.finditer(r'\{text:"([^"]*)"([^{}]*)\}', s_):
            if m.group(1) == '' and s_[m.end():m.end() + 0] == '' and 'extra' in s_[m.start():m.start() + 30]:
                continue
            if m.group(1) == '' and not m.group(2):
                continue
            check('font:"' in m.group(2) or m.group(1) == '', f'static: {rel}:{i} component {m.group(0)[:60]} names no font')
        for m in re.finditer(r'font:"rlk:mboss_hr"', s_):
            head = s_[:m.start()]
            check('extra:[' in head, f'static: {rel}:{i} kit font outside an extra list')
        for m in re.finditer(r'\{text:"",extra', s_):
            check(s_[m.start() - 1:m.start()] != '[', f'static: {rel}:{i} root is a list')
        if rel.startswith('test/sounds'):
            continue
        for t in re.findall(r'text:"([^"]*)"', s_):
            check(t in STR_OK or any(t and v.startswith(t) for v in api.LINES.values()) or api.WARN_TEXT.startswith(t)
                  or t in api.WARN_TEXT, f'static: {rel}:{i} text {t!r} is not an api string (no tutorial text)')
# one card per projectile (the disc prop = one display), summon then rotate (spawn: summon, then tp with rotation)
sp = fbody('e/spawn').split('\n')
summ = [i for i, ln in enumerate(sp) if ln.startswith('$summon')]
tps = [i for i, ln in enumerate(sp) if ' tp @e' in ln and 'rotated' in ln]
check(summ and tps and tps[0] > summ[0], 'static: e/spawn summons, then rotates (summon takes no rotation)')

# ============================================================== demos
lens = G.demo_lens()
allk = list(G.DEMOS) + [f'prop/{p}' for p in G.PROPS]
for name in allk:
    s = fresh()
    s.run(f'function {NSF}test/stage', pos=(X0, FLOOR, Z0 + 10), rot=(180.0, 0.0))
    stand = [e for e in s.ents if e.etype == 'armor_stand']
    check(len(stand) == 1, f'demos: {name}: one stand-in')
    s.run(f'function {NSF}test/{name}')
    seen = 0
    for _ in range(lens[name] + 4):
        s.tick(1)
        seen = max(seen, len([e for e in s.ents if e.etype == 'item_display']))
    check(seen > 0 or name in G.PTCL, f'demos: test/{name} showed something')
    check(s.sc('#demo', OBJ) == 0, f'demos: test/{name} ran to its end')
    s.run(f'function {NSF}test/stop')
    check(not [e for e in s.ents if G.DEMO in e.tags], f'demos: test/stop removes the stand-in ({name})')
for extra in ('sounds', 'hud', 'kinds', 'stage', 'stop'):
    check((FX / f'test/{extra}.mcfunction').exists(), f'demos: test/{extra}')
s = fresh()
s.run(f'function {NSF}test/kinds', pos=(X0, FLOOR, Z0), rot=(0.0, 0.0))
check(len(s.cards()) == len(G.ALL_KINDS), f'demos: test/kinds shows every kind ({len(s.cards())})')


# ============================================================== rp
def png_size(p):
    data = Path(p).read_bytes()[:24]
    return struct.unpack('>II', data[16:24])


if RP:
    tex = RP / 'assets/rlk/textures/mboss/hr_kit'
    want = {}
    for group, rows in api.KIT_SPRITES.items():
        for f, w, h in rows:
            want.setdefault((w, h), 0)
            want[(w, h)] += f
    have = {}
    px = 0
    for stem, ((w, h), *_r) in G.TEXTURES.items():
        p = tex / f'{stem}.png'
        check(p.exists() and png_size(p) == (w, h), f'rp: sprite {stem}')
        if stem != 'gate_icon':
            have[(w, h)] = have.get((w, h), 0) + 1
            px += w * h
    check(have == want, f'rp: sprite sizes = api.KIT_SPRITES ({have} vs {want})')
    check(px == api.KIT_SPRITE_PX <= api.KIT_SPRITE_CAP, f'rp: sprites {px} px <= {api.KIT_SPRITE_CAP}')
    gw, gh = png_size(tex / 'gate_icon.png')
    check(gw * gh <= api.GATE_ICON_PX_CAP, f'rp: gate icon {gw * gh} px <= {api.GATE_ICON_PX_CAP}')
    check(sorted(p.stem for p in tex.glob('*.png')) == sorted(G.TEXTURES), 'rp: no stray textures')
    for k in G.ALL_KINDS:
        if k not in G.RIFT:
            check((RP / f'assets/rlk/models/item/mboss/hr_kit/{k}.json').exists(), f'rp: model {k}')
        check((RP / f'assets/rlk/items/mboss/hr_kit/{k}.json').exists(), f'rp: item {k}')
    atlas = json.loads((RP / 'assets/minecraft/atlases/items.json').read_text(encoding='utf-8'))
    srcs = {s_.get('resource') for s_ in atlas['sources']}
    check(all(G.NS_TEX + k in srcs for k in G.TEXTURES), 'rp: atlas sources')
    gid = api.GATE_ICON_MODEL.split(':')[1]
    check((RP / f'assets/rlk/items/{gid}.json').exists(), f'rp: gate icon {api.GATE_ICON_MODEL}')
    font = json.loads((RP / 'assets/rlk/font/mboss_hr.json').read_text(encoding='utf-8'))
    check(font['providers'][-1] == {'type': 'reference', 'id': 'minecraft:default'}, 'rp: font ends with minecraft:default')
    cps = [ord(ch) for p_ in font['providers'] for row in p_.get('chars', []) for ch in row]
    cps += [int(k.lstrip('\\u'), 16) if k.startswith('\\u') else ord(k) for p_ in font['providers'] for k in p_.get('advances', {})]
    check(cps and all(0xEC00 <= c <= 0xECFF for c in cps), 'rp: glyphs in U+EC00-ECFF')
    check(set(api.OVERLAYS.values()) | {api.VIG} <= set(cps), 'rp: the six overlays and vig')
    for p_ in font['providers']:
        if p_.get('type') == 'bitmap':
            fp = RP / ('assets/rlk/textures/' + p_['file'].split(':', 1)[1])
            check(fp.exists() and png_size(fp) == api.OVERLAY_GLYPH, f'rp: glyph texture {fp.name} {api.OVERLAY_GLYPH}')
    other = set()
    for fj in (RP / 'assets').rglob('font/*.json'):
        if fj.name == 'mboss_hr.json':
            continue
        try:
            fd = json.loads(fj.read_text(encoding='utf-8'))
        except ValueError:
            continue
        for p_ in fd.get('providers', []):
            for row in p_.get('chars', []):
                other.update(ord(ch) for ch in row)
            other.update(ord(k) for k in p_.get('advances', {}) if len(k) == 1)
    check(not [c for c in cps if c in other], 'rp: no glyph collision with the other fonts')
    for p in (RP / 'assets/rlk').rglob('*hr_kit*'):
        check(p.as_posix() == p.as_posix().lower(), f'rp: lowercase path {p}')

print(f'test_kit: {NCHK[0] - len(FAILS)}/{NCHK[0]} passed' + (f', {len(FAILS)} FAILED' if FAILS else ''))
sys.exit(1 if FAILS else 0)
