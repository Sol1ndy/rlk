"""Helpers of S1-MOD shared with the pattern authors (re-exported by api.py; s2.md 1). Pure Python (geometry in the
anchor frame of manifest.md 2: x = s, the boss's left, z = f, forward; yaw deltas in Minecraft units, + = clockwise
from above), so pattern modules and their tests compute the same numbers.

    rot_local(s, f, delta)      the local point (s, f) of the anchor turned by delta, in the start frame
    dir_yaw(s, f)               the Minecraft yaw (relative to the start facing) of the direction (s, f)
    loc(x, z, y=0)              '^x ^y ^z' (execute positioned from the anchor, rotated as it)
    whip_wedges(clip)           the P7 swept wedges per tick from the manifest track x the yaw schedule (s2.md 6.3)
    seg_dist(p, a, b)           point-to-segment distance (s, f)
    stub_emit(g, p, ...)        the empty, timing-correct pattern files of S1-MOD's stubs (replaced by S2)
"""
import math

from . import api as _A

__all__ = ['rot_local', 'dir_yaw', 'loc', 'seg_dist', 'whip_wedges', 'stub_emit']


def rot_local(s, f, delta):
    d = math.radians(delta)
    return (s * math.cos(d) - f * math.sin(d), s * math.sin(d) + f * math.cos(d))


def dir_yaw(s, f):
    """Yaw of the direction (s, f) relative to the facing: 0 = forward, -90 = the boss's left, +90 its right, 180 back."""
    return math.degrees(math.atan2(-s, f))


def loc(x, z, y=0.0, nd=3):
    n = _A.L.num
    return f'^{n(float(x), nd)} ^{n(float(y), nd)} ^{n(float(z), nd)}'


def seg_dist(p, a, b):
    px, pz = p
    ax, az = a
    bx, bz = b
    dx, dz = bx - ax, bz - az
    ll = dx * dx + dz * dz
    u = 0.0 if ll == 0 else max(0.0, min(1.0, ((px - ax) * dx + (pz - az) * dz) / ll))
    return math.hypot(px - (ax + u * dx), pz - (az + u * dz))


def whip_wedges(clip='tail_whip_l', t0=None, t1=None):
    """The swept wedges of the tail whip (plan.md 5 P7, fx.md 3.1): for every played tick k of sweep .. sweep_end,
    dict(t=k, root=(s, f) of the tail root in the START frame, a0, a1 = the tail-line yaws (relative to the start
    facing, Minecraft sense, a0 < a1) of ticks k-1 and k about that root, r1 = the reach). Computed from the manifest's
    tail_root / tail_tip tracks composed with the clip's yaw schedule; the union of these wedges is the P7 decal."""
    ev = _A.CLIPS[clip]['events']
    t0 = ev['sweep'] if t0 is None else t0
    t1 = ev['sweep_end'] if t1 is None else t1
    root, tip = _A.track(clip, 'tail_root'), _A.track(clip, 'tail_tip')

    def line_yaw(t):
        d = _A.yaw_at(clip, t)
        rs, rf = rot_local(root[t][0], root[t][2], d)
        ts, tf = rot_local(tip[t][0], tip[t][2], d)
        return dir_yaw(ts - rs, tf - rf), (rs, rf)
    out = []
    for k in range(t0, t1 + 1):
        a_prev, _ = line_yaw(k - 1)
        a_now, r = line_yaw(k)
        while a_now - a_prev > 180:
            a_now -= 360
        while a_now - a_prev < -180:
            a_now += 360
        a0, a1 = sorted((a_prev, a_now))
        out.append(dict(t=k, root=r, a0=a0, a1=a1, r1=_A.WHIP_REACH))
    return out


def stub_emit(g, p, end=None, tick=(), cast=None, bg=None, b3=False):
    """S1-MOD's empty pattern stub (no hazards): start / tick / cancel (+ the declared hooks) that only keep time, so
    the AI, the slots and the transitions run with the pattern's real length. end: the pattern clock of g.end()
    (default p.length); cast: (ctick end clock, bg slot or None, its bgtick end) for the leg specials; bg: (bg_start
    clock, slot, bgtick end) for a main-slot pattern that hands over to a background slot; b3: a B3 special."""
    head = f'# STUB (S1-MOD, s2.md 2.1): {p.label} ({p.key}, id {p.id}); the S2 author replaces this file.'
    end = p.length if end is None else end
    cancel = [head, '# nothing of its own lingers (selectors only, idempotent)']
    if p.kind == 'cast':                            # s2.md 2: cast -> cast / ctick / cancel (no main-slot start / tick)
        cend, slot, bgend = cast
        lines = [head, '# the cast slot clock #azCT = the roar_rear clip tick'] + list(tick)
        if slot:
            lines.append(g.at(cend, g.bg_start(slot), clock='#azCT'))
        lines.append(f'execute if score #azCT mb matches {cend}.. run {g.cast_end()}')
        g.pw(p.key, 'cast', [head])
        g.pw(p.key, 'ctick', lines)
        g.pw(p.key, 'cancel', cancel)
        if slot:
            clk = '#azBgLT' if slot == 'L' else '#azBgTT'
            g.pw(p.key, 'bgtick', [head, f'execute if score {clk} mb matches {bgend}.. run {g.bg_end(slot)}'])
            g.pw(p.key, 'cancel_bg', [head])
            g.pw(p.key, 'reload', [head, '# /reload while the emitter lives in its bg slot: nothing to re-make'])
    elif p.kind == 'special':                       # s2.md 2: special -> start / b3tick / stop / cancel / reload
        assert b3
        g.pw(p.key, 'start', [head])
        g.pw(p.key, 'b3tick', [head, '# B3 clock #azB3T (absolute): nothing is created after B3_LAST, nothing hits after B3_HIT_MAX']
             + list(tick))
        g.pw(p.key, 'stop', [head])
        g.pw(p.key, 'cancel', cancel)
        g.pw(p.key, 'reload', [head, '# /reload during B3: nothing to re-make'])
    else:                                           # normal / bg / service -> start / tick / cancel
        t = ['# keeps time only'] + list(tick)
        if bg:
            t.append(g.at(bg[0], g.bg_start(bg[1])))
        t.append(f'execute if score #azPT mb matches {end}.. run {g.end()}')
        g.pw(p.key, 'start', [head])
        g.pw(p.key, 'tick', [head] + t)
        g.pw(p.key, 'cancel', cancel)
        if bg:                                      # bg -> + bgtick / cancel_bg / reload
            clk = '#azBgLT' if bg[1] == 'L' else '#azBgTT'
            g.pw(p.key, 'bgtick', [head, f'execute if score {clk} mb matches {bg[2]}.. run {g.bg_end(bg[1])}'])
            g.pw(p.key, 'cancel_bg', [head])
            g.pw(p.key, 'reload', [head, '# /reload while the emitter lives in its bg slot: nothing to re-make'])
    for h in p.hooks:
        if not g.has(f'p/{p.key}/{h}'):
            g.pw(p.key, h, [head])
