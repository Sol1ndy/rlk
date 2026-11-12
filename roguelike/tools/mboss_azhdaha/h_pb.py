"""Helpers of S2-B (geo_b.py: P5 stomp, P5b triple stomp, P6 feint, P7 tail whip, P8 tail slam, P9 burrow charge).
Pure Python on the rig manifest (api.CLIPS) and the plan numbers (plan.md 5, Change note 1), so geo_b.py and its suite
compute the same geometry. Local frame of manifest.md 2: x = s (the boss's left), z = f (forward); yaws in Minecraft
degrees relative to a facing (+ = clockwise from above = toward the boss's right).

    Sub(g, key, sub)            per-tick sub-functions p/<key>/<sub>/<t> run at a marker (the paw, the whip frame ...)
    STOMP_PAW / STOMP3_PAW      the slamming paw's floor point per clip (manifest anchors)
    whip_geom(side)             P7: per-tick wedges (sector apex / mid yaw / half angle), the eruption points, the
                                addon contexts, all in the START frame of the whip (the anchor before the yaw schedule)
    P6 / P8 / P9 numbers        the sizes, ticks and coefficient keys of plan.md 5 (binding)
"""
import math

from . import api as _A
from .h_core import rot_local, dir_yaw, whip_wedges

__all__ = ['Sub', 'STOMP_PAW', 'STOMP3_PAW', 'whip_geom', 'P5', 'P5B', 'P6', 'P7', 'P8', 'P9', 'eased']


class Sub:
    """Lines per tick written to p/<key>/<sub>/<t>; call(t) is the function line (the host wraps it in its execute)."""

    def __init__(self, g, key, sub):
        self.g, self.key, self.sub, self.ev = g, key, sub, {}

    def at(self, t, *lines):
        for ln in lines:
            for one in _A._flat([ln]):
                self.ev.setdefault(int(t), []).append(one)

    def ticks(self):
        return sorted(self.ev)

    def fn(self, t):
        return f'function {_A.NS}p/{self.key}/{self.sub}/{t}'

    def write(self):
        for t, lines in sorted(self.ev.items()):
            self.g.pw(self.key, f'{self.sub}/{t}', [f'# {self.key} {self.sub} #azPT {t}'] + lines)


def _paw(clip, event):
    a = _A.anchor(clip, event, 'paw')
    return (round(a[0], 3), round(a[2], 3))


# ---------------------------------------------------------------------------------------------------- P5 / P5b
P5 = dict(ev=_A.CLIPS['stomp_fl']['events'], strikes=(17, 32, 47), tell=14, r0=1.5, r1=9.7, band=2.0, low=0.7,
          slam_r=2.8, dmg='p5', end=63, wid=(5, 6, 7))
# the front: r 1.5 -> 7.5 in 3 t (2 b/t), then -> 9.7 by +12 t with an ease-out (linear segments, plan 5 P5)
P5['ease'] = [(3, 7.5), (6, 8.6), (9, 9.3), (12, 9.7)]
STOMP_PAW = {c: _paw(c, 'w1') for c in ('stomp_fl', 'stomp_fr', 'stomp_hl', 'stomp_hr')}
for _c in STOMP_PAW:
    assert all(_paw(_c, e) == STOMP_PAW[_c] for e in ('w2', 'w3')), _c
assert tuple(P5['ev'][e] for e in ('w1', 'w2', 'w3')) == P5['strikes'] and _A.clip_len('stomp_fl') == P5['end']

P5B = dict(ev=_A.CLIPS['stomp3_fl']['events'], strikes=(17, 40, 63), tell=14, slam_r=2.8, dmg='p5b', end=85,
           wid=(5, 6, 7), splash=5)
STOMP3_PAW = {c: tuple(_paw(c, e) for e in ('s1', 's2', 's3')) for c in ('stomp3_fl', 'stomp3_fr')}


def paw_lifts(clip, slams, paws, rise=0.15):
    """The first tick after the previous slam at which the slamming paw's proxy column top is `rise` b above its rest:
    the visible paw lift, the readable tell of P5 / P5b (Change note 1)."""
    out, prev = [], 0
    for t, pr in zip(slams, paws):
        rest = _A.px_at(clip, prev, pr)[2]
        out.append(next(k for k in range(prev + 1, t) if _A.px_at(clip, k, pr)[2] - rest >= rise))
        prev = t
    return tuple(out)


P5B['lifts'] = paw_lifts('stomp3_fl', P5B['strikes'], ('paw_l', 'paw_r', 'paw_l'))      # (4, 25, 48)
assert P5B['lifts'] == paw_lifts('stomp3_fr', P5B['strikes'], ('paw_r', 'paw_l', 'paw_r'))
assert all(s - t >= 12 for s, t in zip(P5B['strikes'], P5B['lifts'])), P5B['lifts']
assert tuple(P5B['ev'][e] for e in ('s1', 's2', 's3')) == P5B['strikes'] and _A.clip_len('stomp3_fl') == P5B['end']


def eased(r0, knots):
    """The per-tick radii of an N10 front from r0 through the ease knots [(dt, r)] (as api.Gen.wave computes them)."""
    pts = [(0, r0)] + list(knots)
    out = []
    for (t0, a), (t1, b) in zip(pts, pts[1:]):
        for k in range(t0 + 1, t1 + 1):
            out.append(a + (b - a) * (k - t0) / (t1 - t0))
    return out


# ---------------------------------------------------------------------------------------------------- P6 feint
# Flank strips: plan 5 P6 = hz/line along the body axis at s = +-5.3, f -6.0 .. +5.0 (len 11), w 6.6 (|s| 2.0 .. 8.6).
# Built as the SAME rectangle aimed outward (start |s| 2.0, len 6.6 outward, w 11 centred on f -0.5), so the
# framework's line knockback "along the aim" (#hzKBDir 1) is the plan's "KB outward 4"; the hit test is identical
# (pad 0.3 on every side either way).
P6 = dict(ev=_A.CLIPS['feint']['events'], burst=22, made=0, strip=dict(s0=2.0, s1=8.6, f0=-6.0, f1=5.0),
          end_r=2.5, nose_f=6.5, back_f=-5.5, dmg_strip='p6_strip', dmg_end='p6_end', kb='p6_out', end=50)
P6['strip']['len'] = round(P6['strip']['s1'] - P6['strip']['s0'], 3)                   # 6.6 outward
P6['strip']['w'] = round(P6['strip']['f1'] - P6['strip']['f0'], 3)                     # 11 along the body
P6['strip']['fc'] = round((P6['strip']['f0'] + P6['strip']['f1']) / 2, 3)              # -0.5
assert P6['ev']['burst'] == P6['burst'] and _A.clip_len('feint') == P6['end']


# ---------------------------------------------------------------------------------------------------- P7 whip
P7 = dict(made=3, tell=20, erupt_tell=20, sweep=23, sweep_end=31, erupt=33, end=64, reach=_A.WHIP_REACH, erupt_r=1.6, erupt_d=(4.0, 7.0, 10.0, 13.0),
          dmg_sweep='p7_sweep', dmg_erupt='p7_erupt', kb='p7_tan', nopush=(20, 42), root_r=2.0)


def whip_sweep_samples(clip, k, n=10, step=0.25):
    """Points the tail line (root .. root + reach) passes between ticks k-1 and k: the root and the line yaw
    interpolated (start frame)."""
    (r0, a0), (r1, a1) = _whip_line(clip, k - 1), _whip_line(clip, k)
    while a1 - a0 > 180:
        a1 -= 360
    while a1 - a0 < -180:
        a1 += 360
    out = []
    for i in range(n + 1):
        u = i / n
        rs, rf, a = r0[0] + (r1[0] - r0[0]) * u, r0[1] + (r1[1] - r0[1]) * u, a0 + (a1 - a0) * u
        for j in range(int(P7['reach'] / step) + 1):
            d = j * step
            out.append((rs - d * math.sin(math.radians(a)), rf + d * math.cos(math.radians(a))))
    return out


def _whip_line(clip, t):
    root, tip = _A.track(clip, 'tail_root'), _A.track(clip, 'tail_tip')
    d = _A.yaw_at(clip, t)
    rs, rf = rot_local(root[t][0], root[t][2], d)
    ts, tf = rot_local(tip[t][0], tip[t][2], d)
    return (rs, rf), dir_yaw(ts - rs, tf - rf)


def whip_geom(side):
    """P7 in the whip's START frame for side 1 (the player on the boss's left: tail_whip_l) or -1 (tail_whip_r).
    wedges: [{t, s, f, mid, half}] (sector apex at the tail root of tick t, aim = mid yaw, half angle int >= 1, r 12);
    erupt: [(s, f)]; ctx_sweep / ctx_end: the addon contexts (position, rotation yaw, the A0 / A1 yaws, all relative to
    the start facing; A0 -> A1 continuous: +115 deg for the left whip, -115 for the right)."""
    clip = 'tail_whip_l' if side == 1 else 'tail_whip_r'
    ev = _A.CLIPS[clip]['events']
    assert (ev['sweep'], ev['sweep_end'], ev['erupt']) == (P7['sweep'], P7['sweep_end'], P7['erupt']), ev
    root, tip = _A.track(clip, 'tail_root'), _A.track(clip, 'tail_tip')

    def line(t):
        d = _A.yaw_at(clip, t)
        rs, rf = rot_local(root[t][0], root[t][2], d)
        ts, tf = rot_local(tip[t][0], tip[t][2], d)
        return dir_yaw(ts - rs, tf - rf), (rs, rf), (ts, tf)

    # The plan's wedge (between the tail-line angles of ticks k-1 and k about the root of tick k) misses ~30 % of the
    # ground the tail really passes, because the root swings around the body (~1 b/t). Each wedge's angles are
    # therefore widened to every sampled point of the true sweep between k-1 and k that lies >= root_r from the root
    # of k, and a disc r root_r at the root of k (same group) takes the rest (misses < 1 %).
    wedges = []
    for w in whip_wedges(clip):
        (rs, rf), ak = _whip_line(clip, w['t'])
        # the root disc stays out of the HEAD zone (f >= 3.6 with both 0.3 pads): smaller near the end of the sweep
        rr = round(max(0.0, min(P7['root_r'], _A.HEAD_F - 0.6 - rf)), 2)
        angs = [dir_yaw(x - rs, z - rf) for x, z in whip_sweep_samples(clip, w['t']) if math.hypot(x - rs, z - rf) >= max(rr, 0.5)]
        angs = [ak + ((a - ak + 180) % 360 - 180) for a in angs]
        lo, hi = min(angs), max(angs)
        half = max(1, int(math.ceil((hi - lo) / 2.0 + 0.5)))
        wedges.append(dict(t=w['t'], s=round(rs, 3), f=round(rf, 3), mid=round((lo + hi) / 2.0, 2), half=half,
                           a0=w['a0'], a1=w['a1'], lo=lo, hi=hi, rr=rr))
    # the continuous line yaw from the sweep start to its end (+ for the left whip, - for the right)
    y0, r23, _ = line(P7['sweep'])
    y1, r31, _ = line(P7['sweep_end'])
    while side * (y1 - y0) < 0:
        y1 += 360 * side
    ux, uz = -math.sin(math.radians(y1)), math.cos(math.radians(y1))
    erupt = [(round(r31[0] + d * ux, 3), round(r31[1] + d * uz, 3)) for d in P7['erupt_d']]
    tips = {t: tuple(round(v, 3) for v in line(t)[2]) for t in range(P7['sweep'], P7['sweep_end'] + 1)}
    return dict(clip=clip, wedges=wedges, erupt=erupt, end_yaw=round(y1, 2), tips=tips,
                ctx_sweep=dict(pos=(round(r23[0], 3), round(r23[1], 3)), yaw=0.0, a0=round(y0, 2), a1=round(y1, 2)),
                ctx_end=dict(pos=(round(r31[0], 3), round(r31[1], 3)), yaw=round(y1, 2)))


# ---------------------------------------------------------------------------------------------------- P8 tail slam
P8 = dict(ev=_A.CLIPS['tail_slam']['events'], made=9, impact=39, spikes=41, end=70, len=13.0, w=3.5, turn_max=15.0,
          turn_ticks=(1, 9), dmg='p8', kb='p8_side')
P8['root_f'] = round(_A.anchor('tail_slam', 'impact', 'tail_root')[2], 3)          # -4.75: the line starts here
assert (P8['ev']['impact'], P8['ev']['spikes']) == (P8['impact'], P8['spikes']) and _A.clip_len('tail_slam') == P8['end']
# the line as two outward half-lines (KB "sideways" = along each half's aim, #hzKBDir 1); same hit test as one line w 3.5
P8['half'] = dict(s0=0.05, len=round(P8['w'] / 2 - 0.05, 3), fc=round(P8['root_f'] - P8['len'] / 2, 3), w=P8['len'])


# ---------------------------------------------------------------------------------------------------- P9 burrow charge
# Ticks of the pattern clock (u = t - 40 underground, plan 5 P9). Rings: decision at the tick, hit + 19 (keep: the
# chevron ring outline from the decision). Rushes: decision at the tick (dust mound / bulge / rumble at the breach
# point, no decal), the burrow_breach clock (its events time the burst and the hits; the clip itself is not played:
# the body stays hidden underground, user 10-21) so that its `hit` lands 20 t later, the disc r 3.0 riding the body for
# 20 t at 0.6 b/t. Final emergence: decision at u160, the mound / spires from 19 t before the burst at the clip's
# `burst` (the clip starts at u180 = t220: 180 t underground).
P9 = dict(dive=_A.CLIPS['burrow_dive']['events'], breach=_A.CLIPS['burrow_breach']['events'],
          emerge=_A.CLIPS['burrow_emerge']['events'], under=40, inv=30, glide=(14, 36, 3.0), u_len=180,
          ring_tell=19, ring_r=3.4, ring_lead=6, rings=(10, 35, 80, 105), rock_u=10, rock_tell=14, rock_r=1.4,
          rock_d=(3.0, 6.0, 9.0), rush_u=(45, 115), rush_tell=20, rush_r=3.0, rush_spd=0.6, rush_off=6.0,
          final_u=160, burst_r=3.7, burst_tell=19, emerge_lead=8, edge_r=20.0, travel=0.3, travel_r=12.0,
          run_r=4.0, run_tell=20, run_spd=1.0, run_max=24, run_r_max=24.0, safe_r=24.0,
          dmg=dict(ring='p9_ring', rock='p9_rock', rush='p9_rush', burst='p9_burst', run='p9_run'))
P9['u0'] = P9['dive']['under']                                     # 40
P9['emerge_t'] = P9['u0'] + P9['u_len']                            # 220: burrow_emerge starts
P9['burst_t'] = P9['emerge_t'] + P9['emerge']['burst']             # 228
P9['out_t'] = P9['emerge_t'] + P9['emerge']['out']                 # 258
P9['end'] = P9['emerge_t'] + _A.clip_len('burrow_emerge')          # 273
P9['final_t'] = P9['u0'] + P9['final_u']                           # 200: the emergence spot is chosen
P9['mound_t'] = P9['burst_t'] - P9['burst_tell']                   # 209: the burst hazard + its mound / spires
P9['run_face'] = P9['out_t'] - P9['run_tell']                      # 238: edge flag: facing + growl, the run at out
P9['ring_t'] = tuple(P9['u0'] + u for u in P9['rings'])            # 50 75 120 145 (hits + 19)
P9['rock_t'] = P9['u0'] + P9['rock_u']                             # 50 (hits + 14)
P9['rush_t'] = tuple(P9['u0'] + u for u in P9['rush_u'])           # 85 155: decisions
P9['rush_hit'] = tuple(t + P9['rush_tell'] for t in P9['rush_t'])  # 105 175: the disc starts hitting
P9['rush_clip'] = tuple(h - P9['breach']['hit'] for h in P9['rush_hit'])          # 95 165: burrow_breach starts
P9['rush_end'] = tuple(c + P9['breach']['under'] for c in P9['rush_clip'])        # 125 195: back under
P9['rush_act'] = P9['breach']['under'] - P9['breach']['hit'] + 1                  # 21 ticks of hits
assert P9['emerge']['burst'] == 8 and P9['breach']['hit'] == 10 and P9['end'] == 273
