"""Display-rig math for the chapter-2 mobs (shared by swarm.py; elite modules may reuse it through their own shim).

A port of the pose construction in tools/build_swordsman.mjs: skin units are 1/16 block, every part model pivots at
[8,8,8]; poses are authored with -Z forward and the right hand on -X, then mirrored to the runtime frame (+Z forward,
item_display turns the model Y180 after the transformation). Quaternions are [x, y, z, w].
"""
import math

GUARD = {'torso': [4, -8, 0], 'head': [-3, 8, 0], 'right_arm': [62, -12, -8], 'left_arm': [14, 0, 12],
         'right_leg': [-5, 0, -3], 'left_leg': [6, 0, 3], 'weapon': [-98, 5, -4]}
LIMBS = ('head', 'body', 'right_arm', 'left_arm', 'right_leg', 'left_leg')


def mul(a, b):
    x, y, z, w = a
    X, Y, Z, W = b
    return [w * X + x * W + y * Z - z * Y, w * Y - x * Z + y * W + z * X, w * Z + x * Y - y * X + z * W, w * W - x * X - y * Y - z * Z]


def q(e=(0, 0, 0)):
    x, y, z = (math.radians(a) / 2 for a in e)
    return mul(mul([0, 0, math.sin(z), math.cos(z)], [0, math.sin(y), 0, math.cos(y)]), [math.sin(x), 0, 0, math.cos(x)])


def rot(a, v):
    return mul(mul(a, [v[0], v[1], v[2], 0]), [-a[0], -a[1], -a[2], a[3]])[:3]


def add(a, b):
    return [a[i] + b[i] for i in range(3)]


def humanoid(over, attach=()):
    """Joint transforms for one pose. over: pose parameters (see GUARD; plus shift, root, rootShift, size, ropen).
    attach: extra parts, each (name, kind, offset, euler, scale):
      kind 'rhand' / 'lhand' -> held at that hand, euler = the weapon angle on top of the arm (param key in over
      overrides: over[name]); offset = shift along the weapon's own +Y (blocks, model axis) so the grip moves;
      kind 'back' -> fixed to the torso, offset = authored position from the shoulder; kind 'root' -> fixed to the
      feet origin (does not follow the torso), offset = authored position."""
    p = dict(GUARD)
    p.update(over)
    hip = add([0, .75, 0], p.get('shift', [0, 0, 0]))
    t = q(p['torso'])
    root = q(p.get('root', [0, 0, 0]))
    out = {}
    shoulder = add(hip, rot(t, [0, .75, 0]))
    out['body'] = {'t': shoulder, 'q': t}
    out['head'] = {'t': shoulder, 'q': mul(t, q(p['head']))}
    for name, sign in (('right_arm', -1), ('left_arm', 1)):
        joint = mul(q([0, p.get('ropen', 28) if name == 'right_arm' else 0, 0]), q(p[name]))
        out[name] = {'t': add(hip, rot(t, [sign * .375, .625, 0])), 'q': mul(t, joint)}
    for name, sign in (('right_leg', -1), ('left_leg', 1)):
        out[name] = {'t': add(hip, [sign * .125, 0, 0]), 'q': q(p[name])}
    size = p.get('size', 1)
    scales = {}
    for name, kind, off, euler, sc in attach:
        e = p.get(name, euler)
        if kind in ('rhand', 'lhand'):
            arm = out['right_arm' if kind == 'rhand' else 'left_arm']
            qq = mul(arm['q'], q(e))
            tt = add(arm['t'], rot(arm['q'], [0, -.535, -.015]))
            tt = add(tt, rot(qq, [0, off, 0]))
            out[name] = {'t': tt, 'q': qq, 'post': True}
        elif kind == 'back':
            out[name] = {'t': add(shoulder, rot(t, off)), 'q': mul(t, q(e))}
        else:
            out[name] = {'t': list(off), 'q': q(e), 'fixed': True}
        scales[name] = sc
    for name, a in out.items():
        if a.pop('fixed', False):      # props on the ground (the taiko) do not follow the body's root tilt
            a['t'] = [v * size for v in a['t']]
        else:
            a['t'] = [v * size for v in add(p.get('rootShift', [0, 0, 0]), rot(root, a['t']))]
            a['q'] = mul(root, a['q'])
        s = size * scales.get(name, 1)
        a['s'] = [s, s, s]
        a['t'] = [a['t'][0], a['t'][1], -a['t'][2]]
        a['q'] = [-a['q'][0], -a['q'][1], a['q'][2], a['q'][3]]
        if a.pop('post', False):
            a['q'] = mul(a['q'], q([0, 90, 0]))
    return out


# Model-pixel bounds of every part (mirrors tools/build_ch2_swarm_rigs.mjs; the scratch tests check them against the RP).
AABB = {'head': ([3.5, 7.5, 3.5], [12.5, 16.5, 12.5]), 'body': ([3.75, -4.25, 5.75], [12.25, 8.25, 10.25]),
        'right_arm': ([5.75, -2.25, 5.75], [10.25, 10.25, 10.25]), 'left_arm': ([5.75, -2.25, 5.75], [10.25, 10.25, 10.25]),
        'right_leg': ([5.75, -4.25, 5.75], [10.25, 8.25, 10.25]), 'left_leg': ([5.75, -4.25, 5.75], [10.25, 8.25, 10.25]),
        'katana': ([6.3, 3.2, 6.3], [9.7, 27.2, 9.7]), 'yari': ([6.4, -15.8, 7.2], [9.6, 32, 8.8]), 'flag': ([7.6, -6, 7.6], [15.8, 31, 8.4]),
        'stick_r': ([7.3, 2, 7.3], [8.7, 17.4, 8.7]), 'stick_l': ([7.3, 2, 7.3], [8.7, 17.4, 8.7]), 'taiko': ([-1.2, -7, 1.6], [17.2, 16, 14.4])}


def lowest(a, box):
    """Lowest world y (feet frame) of a part box under transform a (item_display turns the model Y180 first)."""
    lo = 9.0
    for x in (box[0][0], box[1][0]):
        for y in (box[0][1], box[1][1]):
            for z in (box[0][2], box[1][2]):
                v = [-(x / 16 - .5) * a['s'][0], (y / 16 - .5) * a['s'][1], -(z / 16 - .5) * a['s'][2]]
                lo = min(lo, rot(a['q'], v)[1] + a['t'][1])
    return lo


def plant(out):
    """Lift the whole pose so no leg goes below the floor (never lowers it). Returns the lift."""
    lift = max(0.0, -min(lowest(out[p], AABB[p]) for p in ('right_leg', 'left_leg')))
    for a in out.values():
        a['t'][1] += lift
    return lift


def fl(n):
    v = 0 if abs(n) < 5e-7 else round(n, 5)
    s = repr(float(v))
    if s.endswith('.0'):
        s = s[:-2]
    return s + 'f'


def arr(a):
    return '[' + ','.join(fl(v) for v in a) + ']'


def merge_line(sel, a, dur):
    return (f'data merge entity {sel} {{start_interpolation:0,interpolation_duration:{dur},transformation:'
            f'{{translation:{arr(a["t"])},left_rotation:{arr(a["q"])},scale:{arr(a["s"])},right_rotation:[0f,0f,0f,1f]}}}}')
