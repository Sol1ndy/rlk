#!/usr/bin/env python3
"""test_blade.py: 홍련's blade trail against the rig's blade (round W, lane WB; w_brief.md §2 WB; round V's wind-up rules kept).

    python3 test_blade.py <roguelike dir> [-v]          (run from a copy outside the datapack, tools/dev/sim/README.md §1)

Reads what ships: tools/scarlet_blade_track.json (the rig build's sidecar), the rig's anchor table (rig/an/load) and the pattern
functions p/<key>/** as generated. It replays every trail card of every pattern on the pattern clock (summon, the one-tick
interpolation of a data merge, the fading frames, the ride / detach, the kill) and compares it with the blade the rig shows
(the sword part's transform per clip tick, interpolated as the client does: translation lerp, rotation slerp), with the clips
the pattern's own files play (rig/play/*, rig/state/hidden). It fails when
  track    the sidecar is not the built rig's blade, a fight clip is missing, its sword transforms (sp / sq) do not carry the blade
  windup   a hit's wind-up pose is reached later than the rule (h - 10 single / first, h - 6 chain) or not held (round V's rule);
           a gauntlet cut: the pose shown before it counts
  ahead    any point of a trail card lies, at any instant, where the blade has not been: farther than AHEAD_TOL from every blade
           position shown since the card's tick - 2 (nothing may show where the blade is going to go)
  removed  any card of round V's drawn path (sw_path / sw_head cards, rlk_hr_swh / swl / swt, core/sw/aim / march / head)
  present  for any hit, a tick from the trail's start to the end of its follow-through without the band on the blade
  size     a band / ribbon / wave thinner than MIN_THICK (its bright core), a piece's rim wall or chord thinner
  life     a piece not gone LIFE t after it began to open, not fading through FADE; a card alive after the pattern's end; a band
           that is not killed when its run ends
  colour   a band / piece not in the colour of the hit the blade is on its way to (white-gold P, the flash colour N; a swing's
           pieces mixed toward white)
  ribbon   a ribbon that grows before the move began or aims anywhere but the hand's place one tick back; a wave before its hit
  clock    a trail command outside the pattern-tick files, a schedule, a game-time read
"""
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

WT = Path(sys.argv[1]).resolve()
VERBOSE = '-v' in sys.argv[2:]
sys.path.insert(0, str(WT / 'tools'))
sys.dont_write_bytecode = True
from mboss_scarlet import api, blade as B  # noqa: E402

MOD = WT / 'data/rlk/function/boss/scarlet'
FAILS, N = [], [0]
AHEAD_TOL = 0.10          # b: a point of a trail card nearer the blade's coming positions than its past ones, farther than this from
#                           the past ones, is ahead (a planar piece lies up to ~0.2 b beside the client's curved sweep: not ahead)
ON_BLADE_TOL = 0.03       # b: the band against the blade
MIN_THICK = 0.12
STATS = dict(ahead=0.0, ahead_at='', band=0.0, pieces=0, bands=0, ribs=0, waves=0, cards_max=0)


def check(ok, msg, detail=''):
    N[0] += 1
    if not ok:
        FAILS.append(msg)
        print('FAIL', msg, detail)
    elif VERBOSE:
        print('ok  ', msg, detail)


# ----------------------------------------------------------------------------- track
TJ = json.loads((WT / 'tools/scarlet_blade_track.json').read_text())
T = TJ['clips']
LO, HI = TJ['blade']
fight = [k for k in api.CLIPS if k not in api.CINE_CLIPS]
check(sorted(T) == sorted(fight), 'track: one row per fight clip', sorted(set(fight) ^ set(T)))
check(all(len(T[k]['t']) == api.CLIPS[k][0] + 1 == len(T[k]['b']) == len(T[k]['sp']) == len(T[k]['sq']) for k in T),
      'track: ticks 0 .. len per clip (b, t, sp, sq)')
MAN = json.loads((WT / 'tools/scarlet_rig_manifest.json').read_text())
AN = {}
for line in (MOD / 'rig/an/load.mcfunction').read_text().splitlines():
    m = re.match(r'data modify storage rlk:hr rig\.an\[(\d+)\]\.(\w+) set value (\[.*\])$', line)
    if m and m.group(2) in ('blade_tip', 'blade_mid'):
        AN[(int(m.group(1)), m.group(2))] = [[float(v.lstrip('^') or 0) for v in s_.split()] for s_ in json.loads(m.group(3))]


def qrot(q, v):
    x, y, z, w = q
    u = (x, y, z)
    c1 = B.cross(u, v)
    c2 = B.cross(u, c1)
    return tuple(v[i] + 2 * (w * c1[i] + c2[i]) for i in range(3))


def qslerp(a, b, u):
    d = sum(x * y for x, y in zip(a, b))
    if d < 0:
        b, d = tuple(-x for x in b), -d
    if d > 0.9995:
        r = tuple(x + (y - x) * u for x, y in zip(a, b))
    else:
        th = math.acos(min(1.0, d))
        s = math.sin(th)
        r = tuple((math.sin((1 - u) * th) * x + math.sin(u * th) * y) / s for x, y in zip(a, b))
    n = math.sqrt(sum(x * x for x in r))
    return tuple(x / n for x in r)


def blade_of(sp, sq, lo=LO):
    return B.add(sp, qrot(sq, (0, lo, 0))), B.add(sp, qrot(sq, (0, HI, 0)))


worst, worst2 = 0.0, 0.0
for k in T:
    cid = MAN['clips'][k]['id']
    for t in range(api.CLIPS[k][0] + 1):
        tip, mid = AN[(cid, 'blade_tip')][t], AN[(cid, 'blade_mid')][t]
        base = [2 * m_ - t_ for m_, t_ in zip(mid, tip)]
        worst = max(worst, math.dist(tip, T[k]['t'][t]), math.dist(base, T[k]['b'][t]) / 3)
        if t >= T[k]['f0'] + 2 and all(T[k]['on'][t - 2:t + 1]):      # (a sword just shown again: its key comes from the hidden pose)
            b2, t2 = blade_of(T[k]['sp'][t], T[k]['sq'][t])
            worst2 = max(worst2, math.dist(t2, tip))
check(worst <= 0.012, f'track: the sidecar is the built rig\'s blade (worst {worst:.4f} b against rig/an/load)')
check(worst2 <= 0.05, f'track: the shown sword transforms (sp / sq) carry the blade of the anchor table (tip worst {worst2:.3f} b, from f0)')


# ----------------------------------------------------------------------------- the pattern files
def pattern_ticks(key):
    """{pattern tick: [command lines]} of p/<key>: start (0), the tick file's own lines and ranges, the k/<t> files."""
    out = {}
    d = MOD / 'p' / key

    def add(t, ln):
        out.setdefault(t, []).append(ln)
    for ln in (d / 'start.mcfunction').read_text().splitlines():
        add(0, ln)
    for ln in (d / 'tick.mcfunction').read_text().splitlines():
        m = re.match(r'execute if score #pt hr matches (\d+)(?:\.\.(\d+))? (.*)$', ln)
        if not m or '/k/' in m.group(3) or '/b/' in m.group(3):
            continue
        ln = m.group(3)[4:] if m.group(3).startswith('run ') else 'execute ' + m.group(3)
        for t in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
            add(t, ln)
    if (d / 'k').is_dir():
        for f in (d / 'k').glob('*.mcfunction'):
            for ln in f.read_text().splitlines():
                add(int(f.stem), ln)
    return out


COND = re.compile(r'^execute ((?:(?:if|unless) score #\w+ hr matches \S+ ?)+)(?:run )?')


def cond_ok(ln, scen):
    """strip the leading score conditions of a line when they hold in the scenario (#ph, #q_hit); None when they do not"""
    m = COND.match(ln)
    if not m:
        return ln
    for neg, name, rng in re.findall(r'(if|unless) score (#\w+) hr matches (\S+)', m.group(1)):
        v = scen.get(name, 0)
        lo, _, hi = rng.partition('..')
        ok = (int(lo) if lo else -10 ** 9) <= v <= (int(hi) if hi else 10 ** 9) if '..' in rng else v == int(rng)
        if ok != (neg == 'if'):
            return None
    rest = ln[m.end():]
    return rest if m.group(0).endswith('run ') else 'execute ' + rest


def nums(s_, k):
    return [float(v.rstrip('f')) for v in re.search(k + r':\[([^\]]*)\]', s_).group(1).split(',')]


def xf_of(s_):
    return (tuple(nums(s_, 'translation')), tuple(nums(s_, 'left_rotation')), tuple(nums(s_, 'scale')))


class Card:
    def __init__(self, t, tags, model, xf, col, ipd, world):
        self.t, self.tags, self.model, self.col, self.ipd, self.world = t, tags, model, col, ipd, world
        self.keys = [(t, xf, xf, 0)]          # (tick, from, to, duration): the shown transform from instant tick on
        self.models = {t: model}
        self.cols = {t: col}
        self.kill = None
        self.detach = None

    def shown(self, tau):
        """the transform at the instant tau"""
        k = [x for x in self.keys if x[0] <= tau + 1e-9][-1]
        t0, a, b, d = k
        if d <= 0 or tau >= t0 + d:
            return b
        u = (tau - t0) / d
        return (B.lerp(a[0], b[0], u), qslerp(a[1], b[1], u), B.lerp(a[2], b[2], u))

    def merge(self, t, xf, ipd):
        cur = self.shown(t)
        self.keys.append((t, cur, xf, ipd))


def replay(key, scen):
    """The trail cards of p/<key> in scenario scen ({#ph, #q_hit}): [Card], the clips played {tick: clip}, hidden ticks, the
    ribbon / wave / other trail lines [(tick, line)], the pattern's end tick."""
    ticks = pattern_ticks(key)
    cards, live, plays, hidden, other = [], {}, {}, [], []
    end = None
    for t in sorted(ticks):
        for ln0 in ticks[t]:
            ln = cond_ok(ln0, scen)
            if ln is None:
                continue
            m = re.search(r'rig/play/(\w+)$', ln)
            if m:
                plays[t] = m.group(1)
            if ln.endswith('rig/state/hidden'):
                hidden.append(t)
            if re.search(r'#done hr 1$', ln) and end is None:
                end = t
            if 'rlk_hr_tr' not in ln and 'core/sw/' not in ln and 'rlk_hr_sw' not in ln:
                continue
            m = re.search(r'summon minecraft:item_display ~ ~ ~ (\{.*\})\s*$', ln)
            if m and '"rlk_hr_tr"' in ln:
                s_ = m.group(1)
                tags = re.search(r'Tags:\[([^\]]*)\]', s_).group(1).replace('"', '').split(',')
                c = Card(t, tags, re.search(r'hr_kit/(\w+)"', s_).group(1), xf_of(s_), int(re.search(r'colors:\[(\d+)\]', s_).group(1)),
                         int(re.search(r'interpolation_duration:(\d+)', s_).group(1)), world=not ln.startswith('summon'))
                c.where = ln[:ln.index('summon')]
                cards.append(c)
                for tg in tags:
                    live.setdefault(tg, []).append(c)
                continue
            sel = re.search(r'@e\[type=minecraft:item_display,tag=(\w+)(?:,tag=(\w+))?\]', ln)
            tg = [x for x in (sel.groups() if sel else ()) if x]

            def of(tg=tg):
                return [c for c in cards if all(x in c.tags for x in tg) and c.kill is None and c.t <= t]
            if ln.startswith('kill @e[type=minecraft:item_display') and tg:
                for c in of():
                    c.kill = t
                continue
            if ' run data merge entity @s {start_interpolation:0' in ln and tg:
                body = ln[ln.index('{start_interpolation'):]
                ipd = re.search(r'interpolation_duration:(\d+)', body)
                for c in of():
                    c.merge(t, xf_of(body), int(ipd.group(1)) if ipd else c.ipd)
                    cm = re.search(r'colors:\[(\d+)\]', body)
                    if cm:
                        c.cols[t] = int(cm.group(1))
                continue
            m = re.search(r'item_model" set value "rlk:mboss/hr_kit/(\w+)"', ln)
            if m and tg:
                for c in of():
                    c.models[t] = m.group(1)
                continue
            if re.match(r'tag @e\[type=minecraft:item_display,tag=\w+\] remove rlk_hr_trr$', ln):
                for c in of():
                    c.detach = t
                continue
            other.append((t, ln))
    end = end if end is not None else max(ticks)
    for c in cards:
        c.cut = c.kill is None or c.kill > end      # alive at the pattern's end: core/pat_end / core/g/end kill it (checked below)
        if c.cut:
            c.kill = end
    return cards, plays, hidden, other, end


# ----------------------------------------------------------------------------- the blade the rig shows (the test's own model)
class Rig:
    def __init__(self, plays, hidden, last):
        self.st = {}
        segs = sorted(plays.items())
        prev = None
        for i, (t0, clip) in enumerate(segs):
            tr = T[clip]
            n, f0 = len(tr['sp']) - 1, tr['f0']
            t1 = segs[i + 1][0] if i + 1 < len(segs) else last
            hid = min((h for h in hidden if t0 <= h and (h < t1 or i + 1 == len(segs))), default=None)
            for t in range(t0, t1 + 1):
                ct = min(n, t - t0)
                if hid is not None and t >= hid:
                    s = None
                elif ct >= f0:
                    s = (tuple(tr['sp'][ct]), tuple(tr['sq'][ct])) if tr['on'][ct] else None
                elif prev is not None and tr['on'][min(f0, n)]:
                    s = (B.lerp(prev[0], tr['sp'][f0], ct / f0), qslerp(prev[1], tuple(tr['sq'][f0]), ct / f0))
                else:
                    s = None
                self.st[t] = s
            prev = self.st[t1]

    def blade(self, tau, lo=0.0):
        """(from, tip) at the instant tau: from the sword's pivot (lo 0: the band grows from her hand) or the blade's base (LO)"""
        i = int(math.floor(tau + 1e-9))
        f = tau - i
        a = self.st.get(i)
        if a is None:
            return None
        if f < 1e-6:
            return blade_of(*a, lo=lo)
        b = self.st.get(i + 1)
        if b is None:
            return None
        return blade_of(B.lerp(a[0], b[0], f), qslerp(a[1], b[1], f), lo=lo)


def card_points(c, xf, model):
    """points of the visible geometry of a card (its frame) for the transform xf"""
    tr, q, s = xf
    pts = []
    if model.startswith(('sw_band', 'sw_rib')):
        b0 = 0.1031 if model == 'sw_band' else 0.0
        for k in range(9):
            z = b0 + (1 - b0) * k / 8
            pts.append((0.0, 0.0, z * s[2]))
    elif model.startswith('sw_fan'):
        for f in np.linspace(-1, 1, 9):
            for bb in (0.45, 0.7, 0.93, 1.0):
                # the wedge sprite: edges a = +-b / 2, the rim the chord b = 1
                pts.append((-f * 0.5 * bb * s[0], 0.0, bb * s[2]))
    elif model.startswith('sw_quad'):
        for a in (-0.5, -0.25, 0, 0.25, 0.5):
            for bb in (0.45, 0.7, 1.0):
                pts.append((-a * s[0], 0.0, bb * s[2]))
    return [B.add(tr, qrot(q, p)) for p in pts]


def seg_dist(P, A, Bv):
    """distance of points P (n x 3) to the segments A[i] - B[i] (m x 3): (n,) of the min over segments"""
    d = Bv - A
    L2 = np.maximum((d * d).sum(1), 1e-12)
    w = P[:, None, :] - A[None, :, :]
    u = np.clip((w * d[None]).sum(2) / L2[None], 0, 1)
    proj = A[None] + u[..., None] * d[None]
    return np.sqrt(((P[:, None, :] - proj) ** 2).sum(2)).min(1)


def swept(rig, t0, tau, step=0.05):
    us = np.arange(max(t0, 0.0), tau + 1e-9, step)
    if len(us) == 0 or us[-1] < tau - 1e-9:
        us = np.append(us, tau)
    bl = [rig.blade(u) for u in us]
    bl = [x for x in bl if x]
    if not bl:
        return None
    return np.array([x[0] for x in bl]), np.array([x[1] for x in bl])


def check_trail(lab, key, scen, hits, wind_from=None):
    """hits = [(hit pattern tick, Swing, colour int, clip t0)]"""
    cards, plays, hidden, other, end = replay(key, scen)
    last = max([c.kill or 0 for c in cards] + [end])
    rig = Rig(plays, hidden, last)
    body = [c for c in cards if not c.world]
    bands = [c for c in body if c.model == 'sw_band']
    pieces = [c for c in body if c.model.startswith(('sw_fan', 'sw_quad'))]
    STATS['pieces'] += len(pieces)
    STATS['bands'] += len(bands)
    # --- removed
    check(not any(c.model in ('sw_path', 'sw_head') for c in cards) and not any(re.search(r'rlk_hr_sw[hlt]\b|core/sw/(aim|march|head)', ln) for _t, ln in other),
          f'{lab}: no card of round V\'s drawn path (path, head, target line, mark)')
    # --- life: nothing outlives the pattern; pieces fade and go; bands are killed
    cut = [c for c in pieces if c.cut and c.t + 1 + B.LIFE < end - 1]
    check(not cut, f'{lab}: no trail card is left to the pattern\'s end ({end}) that should have gone before it', [(c.model, c.t) for c in cut][:3])
    bad = [c for c in pieces if not c.cut and c.kill != c.t + 1 + B.LIFE or sorted(c.models) != [c.t] + [c.t + 1 + dt for dt, _f in B.FADE]
           or c.detach != c.t + B.RIDE_T]
    check(not bad, f'{lab}: every piece ({len(pieces)}) opens one tick after its summon, rides {B.RIDE_T} t, fades at +{B.FADE[0][0]} / '
          f'+{B.FADE[1][0]} and is gone {B.LIFE} t after it began to open', [(c.model, c.t, c.kill, sorted(c.models), c.detach) for c in bad[:3]])
    # --- size
    check(all(c.keys[0][2][2] == (0.0, 0.0, 0.0) for c in bands) and all(c.keys[1][2][2][0] * B.RIB_CORE >= MIN_THICK - 1e-6 for c in bands if len(c.keys) > 1)
          and all(c.kill <= c.t + 2 for c in bands if len(c.keys) == 1), f'{lab}: the band is summoned with no size, its bright core then >= {MIN_THICK} b')
    thin = []
    for c in pieces:
        xf = c.keys[-1][2]
        wall = xf[2][1] * B.RIB_CORE
        if c.model.startswith('sw_fan'):
            chord, ribbon = xf[2][0], B.RIBBON * xf[2][2]
        else:
            chord, ribbon = xf[2][0], B.RIBBON * xf[2][2]
        if min(wall, chord, ribbon) < MIN_THICK - 1e-6:
            thin.append((c.t, round(wall, 3), round(chord, 3), round(ribbon, 3)))
    check(not thin, f'{lab}: every piece\'s rim wall, chord and bright ribbon >= {MIN_THICK} b', thin[:3])
    # --- ahead: every card point, at every instant of its life while it rides (her frame), where the blade has been
    worst, at = 0.0, ''
    for c in bands + pieces:
        t_end = min(c.kill, c.detach if c.detach is not None else c.kill)
        k0 = c.t
        taus = [k0 + i / 4 for i in range(int((t_end - k0) * 4) + 1)]
        for tau in taus:
            if tau >= c.kill:
                continue
            xf = c.shown(tau)
            if xf[2][0] < 1e-6:
                continue                        # (no width yet: nothing drawn)
            sw = swept(rig, tau - 2.0, tau)
            if sw is None:
                worst, at = 99.0, f'{c.model} t{c.t} at {tau}: no blade shown'
                continue
            P = np.array(card_points(c, xf, c.model))
            dp = seg_dist(P, sw[0], sw[1])
            fu = swept(rig, tau + 0.05, tau + 1.5)
            raw = float(dp.max())
            if raw > STATS.get('beside', 0.0):
                STATS['beside'], STATS['beside_at'] = raw, f'{lab} {c.model} t{c.t} at {tau:.2f}'
            if fu is not None:
                df = seg_dist(P, fu[0], fu[1])
                dp = np.where(df < dp, dp, 0.0)        # ahead = off the way it has come AND nearer the way it is going
            else:
                dp = dp * 0.0                          # (the blade goes nowhere from here: she vanishes)
            d = dp.max()
            if c.model == 'sw_band' and tau >= c.t + 1 and c.shown(tau)[2][0] > 0.01:
                bl = rig.blade(tau)
                if bl:
                    on = seg_dist(P, np.array([bl[0]]), np.array([bl[1]])).max()
                    STATS['band'] = max(STATS['band'], on)
                    if on > ON_BLADE_TOL:
                        worst, at = max(worst, 9.0), f'band t{c.t} at {tau}: {on:.3f} b off the blade'
            if d > worst:
                worst, at = d, f'{c.model} t{c.t} at {tau:.2f}'
    if worst > STATS['ahead']:
        STATS['ahead'], STATS['ahead_at'] = worst, f'{lab} {at}'
    check(worst <= AHEAD_TOL, f'{lab}: nothing ahead of the blade - every point of the band and the pieces lies where the blade has '
          f'been at every instant (worst {worst:.3f} b, tol {AHEAD_TOL}; the band on the blade within {ON_BLADE_TOL})', at)
    # --- present: the band on the blade from the trail's start (or the wind-up) through every follow-through
    alive = set()
    for c in bands:
        alive |= {c.t + i / 2 for i in range(int((c.kill - c.t) * 2))}
    first = min((c.t + 1 for c in bands), default=None)      # (summoned a tick early with no size)
    for h, sw, col, c0 in hits:
        lo = max(first or 0, wind_from if wind_from is not None else c0 + sw.w)
        need = [lo + i / 2 for i in range(int((min(c0 + sw.b, end - 1) - lo) * 2) + 1)]
        miss = [x for x in need if x not in alive and rig.blade(x) is not None]
        check(first is not None and first <= c0 + sw.w and not miss,
              f'{lab} hit@{h}: the trail is on the blade from its wind-up ({c0 + sw.w}; the trail from {first}) to the end of its '
              f'follow-through ({c0 + sw.b})', miss[:4])
    # --- colour
    hs = sorted(hits, key=lambda x: x[0])

    def want(t):
        return next((h[2] for h in hs if h[0] >= t + 1), hs[-1][2])
    badc = []
    for c in pieces:
        t = c.t + 1 - B.LAG                   # the sweep t -> t + 1 opens on t + LAG
        hot = any(h[3] + h[1].a <= t and t + 1 <= h[3] + h[1].b for h in hs)
        w_ = B.hot(want(t)) if hot else want(t)
        if c.col != w_:
            badc.append((c.t, hex(c.col), hex(w_)))
    for c in bands:
        for t, col in c.cols.items():
            if col != want(t if t > c.t else c.t):
                badc.append(('band', t, hex(col), hex(want(t))))
    check(not badc, f'{lab}: the trail\'s colour is the next hit\'s (white-gold parryable, the flash colour unparriable; a swing\'s pieces '
          'mixed toward white)', badc[:3])
    # --- ribbons and waves
    ribs = [c for c in cards if c.world and c.model == 'sw_rib_0' and B.TR_GROW in c.tags]
    waves = [c for c in cards if c.world and B.TR_NEW in c.tags]
    STATS['ribs'] += len(ribs)
    STATS['waves'] += len(waves)
    for c in ribs:
        grows = sorted(t for t, ln in other if ln.endswith('core/sw/rib') and c.t < t <= (c.kill or 999))
        check(bool(grows) and grows[0] == c.t + 1 and c.keys[0][2][2][2] == 0.0 and c.keys[0][2][2][0] * B.RIB_CORE >= MIN_THICK - 1e-6,
              f'{lab}: the ribbon born at {c.t} starts with no length at her hand and grows from the next tick on (to the hand\'s place '
              f'one tick back: core/sw/rib)', grows[:2])
    for c in waves:
        check(any(c.t == h for h, *_r in hits) and c.kill == c.t + B.WAVE_LIFE and c.keys[0][2][2][0] * B.RIB_CORE >= MIN_THICK - 1e-6,
              f'{lab}: the struck line born at {c.t} appears ON a hit tick (never before) and is gone {B.WAVE_LIFE} t later')
    STATS['cards_max'] = max(STATS['cards_max'], max((sum(1 for c in cards if c.t <= t < (c.kill or 999)) for t in range(end + 1)), default=0))
    return cards


# ----------------------------------------------------------------------------- P1 / P2
def lead_rule(first):
    return B.LEAD_FIRST if first else B.LEAD_CHAIN


def hits_of(key, scen):
    out, seen, prev = [], set(), None
    for i, row in enumerate(api.HITS[key]):
        clip, ev = row[0], row[1]
        ph = api.HIT_PH.get(key, {}).get(i)
        if (clip, ev) in seen or (ph is not None and ph != scen['#ph_n']) or (clip == 'q_air' and not scen.get('#q_hit')):
            continue
        seen.add((clip, ev))
        t0 = api.Q_AIR_T0 if clip == 'q_air' else 0
        h = t0 + api.ev(clip, ev)
        first = prev is None or h - prev > 24 or key == 'ult'
        out.append((i, clip, ev, h, t0, row[6], first))
        prev = h
    return out


PH = api.PH
for key in api.P1 + tuple(k for k in api.P2 if k not in api.GAUNTLETS):
    if not api.HITS.get(key):
        continue
    scens = [dict({'#ph': PH['p1'], '#ph_n': 1})] if key in api.P1 else [dict({'#ph': PH['p2'], '#ph_n': 2})]
    if key == 'rings':
        scens.append(dict({'#ph': PH['p2'], '#ph_n': 2}))
    if key == 'q':
        scens = [dict({'#ph': PH['p2'], '#ph_n': 2, '#q_hit': 1}), dict({'#ph': PH['p2'], '#ph_n': 2, '#q_hit': 0})]
    for scen in scens:
        lab = f'{key} P{scen["#ph_n"]}' + ('' if '#q_hit' not in scen else (' grab landed' if scen['#q_hit'] else ' grab missed'))
        hs = hits_of(key, scen)
        trail_hits = []
        for idx, clip, ev, h, t0, par, first in hs:
            sw = B.swing_of(clip, ev)
            if key != 'a3s' and (clip, ev) != ('q_grab', 'grab'):
                lead = sw.h - sw.w
                check(lead >= lead_rule(first), f'{lab} {clip}.{ev}@{h}: the wind-up is reached {lead} t before the hit and held '
                      f'(rule {lead_rule(first)}; swing {sw.a}-{sw.b})')
            # (rings in P1: the pattern ends 10 t after r4, r5 is P2's)
            trail_hits.append((h, sw, B.colour_of(key, idx)[0], t0))
        if key == 'q' and not scen['#q_hit']:
            trail_hits = trail_hits[:1]
        check_trail(lab, key, scen, trail_hits)

# ----------------------------------------------------------------------------- the gauntlets
for key in api.GAUNTLETS:
    rows = [r for r in api.SCRIPTS[key] if r[0] >= 0 and r[2]]
    cut_rows = [r for r in rows if r[1].startswith('A8.') and r[1] not in ('A8.T', 'A8.9')]

    def shown(tau):
        """(clip, clip tick) the rig shows at pattern tick tau (the clip started last; held past its end)"""
        r = [x for x in rows if x[0] <= tau]
        if not r:
            return None
        c = r[-1][2]
        return c, min(api.CLIPS[c][0], tau - r[-1][0])
    hits = []
    for t, step, clip, _c in cut_rows:
        s = t + api.ev(clip, 'hit')
        lab = f'{key} {step} {clip}@{s}'
        sw = B.swing_of(clip, 'hit')
        tau = t + sw.a if sw.a >= 3 else t - 1
        cc = shown(tau)
        ref_b, ref_t = T[cc[0]]['b'][cc[1]], T[cc[0]]['t'][cc[1]]
        check(math.dist(ref_t, sw.T[sw.h]) >= 0.8, f'{lab}: the wind-up holds the blade away from where the cut lands ({math.dist(ref_t, sw.T[sw.h]):.2f} b)')
        while tau - 1 >= 0:
            cc = shown(tau - 1)
            if not cc or not T[cc[0]]['on'][cc[1]]:
                break
            if math.dist(T[cc[0]]['t'][cc[1]], ref_t) > B.WIND_TOL or math.dist(T[cc[0]]['b'][cc[1]], ref_b) > B.WIND_TOL:
                break
            tau -= 1
        lead = s - tau
        check(lead >= B.LEAD_CHAIN, f'{lab}: the wind-up pose is shown {lead} t before the cut and held (rule {B.LEAD_CHAIN}: a gauntlet cut is a chain hit)')
        hits.append((s, sw, B.COL['P'], t))
    dive = [r for r in rows if r[1] == 'A8.9'][0]
    hj = dive[0] + api.ev('g_dive', 'hit')
    check(hj == api.JUDGE_T[key], f'{key}: the dive ends on the judge tick')
    check(hj - dive[0] >= 12, f'{key}: the dive reappears {hj - dive[0]} t before the judge (>= 12: nothing hits from an empty screen)')
    hits.append((hj, B.Swing('g_dive', api.ev('g_dive', 'hit')), B.COL['purple'], dive[0]))
    # the trail must be on the blade from where it can be known: a cut whose clip starts from a shown pose (not after a vanish)
    cards = check_trail(f'{key} (G)', key, {'#ph': PH[key], '#ph_n': 2, '#gres': 1}, [h for h in hits], wind_from=None)
    # the station: nothing at the station before she is there (round V's standing path is gone)
    st = [c for c in cards if 'rlk_hr_gst' in getattr(c, 'where', '')]
    check(not st, f'{key}: no trail card stands at a cut\'s station (round V drew the cut there before she came)')

# ----------------------------------------------------------------------------- the clock, the core
bad = []
for p in MOD.rglob('*.mcfunction'):
    rel = p.relative_to(MOD).as_posix()
    if rel.startswith(('fx/', 'rig/')):
        continue
    txt = p.read_text()
    # round W integration: lane WC's sequence starts / skips kill the fight's blade cards (seq.KILL_FIGHT_FX: `kill @e[...,tag=rlk_hr_sw]`),
    # a clean-up on a sequence's first tick, not a trail command; only the other lines naming the trail's tags count here
    drawn = [l for l in txt.split('\n') if ('rlk_hr_tr' in l or 'rlk_hr_sw' in l) and not l.startswith('#')
             and not re.search(r'(?:^|\brun )kill @e\[', l)]
    if drawn and not re.match(r'p/\w+/(k/\d+|start|tick|cancel|fail)$|core/sw/|core/pp$|core/pat_end$|core/g/end$|tick$|ult/fail60$|g/', rel[:-11]):
        bad.append(rel)
    if ('rlk_hr_tr' in txt or 'rlk_hr_sw' in txt) and 'schedule ' in txt:
        bad.append(rel + ' (schedule)')
check(not bad, 'clock: every trail command sits in a pattern-tick file (a pure function of #pt hr; no schedule)', str(bad[:5]))
rt = ''.join((MOD / f'core/sw/{n}.mcfunction').read_text() for n in ('rib', 'rib1'))
check('gametime' not in rt and 'schedule' not in rt, 'clock: the ribbon\'s run-time part reads no game time')
check(not any((MOD / f'core/sw/{n}.mcfunction').exists() for n in ('aim', 'march', 'head')), 'removed: round V\'s target line run-time files are gone')
hook = (MOD / 'tick.mcfunction').read_text().splitlines()
check(hook[-1] == B.RIDE_CMD and hook[-2].endswith('rig/tick'), 'the fight hook rides the trail\'s cards to her model right after rig/tick', hook[-2:])
pp = (MOD / 'core/pp.mcfunction').read_text()
pe = (MOD / 'core/pat_end.mcfunction').read_text()
ge = (MOD / 'core/g/end.mcfunction').read_text()
check(all(x in pp for x in B.stop_lines()) and all(x in pe and x in ge for x in B.end_lines()),
      'a perfect parry\'s flinch stops the trail (the band goes, the rest fades); the pattern\'s / gauntlet\'s end takes what is left')
rib = (MOD / 'core/sw/rib.mcfunction').read_text().splitlines()
check(rib[-2].startswith('execute as @e[type=minecraft:item_display,tag=rlk_hr_trg] at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_trt')
      and rib[-1] == 'tp @e[type=minecraft:marker,tag=rlk_hr_trt,limit=1] ~ ~ ~',
      'the ribbon grows to the marker (the hand\'s place one tick back) BEFORE the marker comes to the hand\'s place now: never ahead of her')

print(f'test_blade: worst point of a trail card ahead of the blade {STATS["ahead"]:.3f} b ({STATS["ahead_at"]}); beside its way at most '
      f'{STATS.get("beside", 0):.3f} b ({STATS.get("beside_at", "")}); the band off the blade '
      f'{STATS["band"]:.3f} b; {STATS["bands"]} bands, {STATS["pieces"]} pieces, {STATS["ribs"]} ribbons, {STATS["waves"]} waves; at most '
      f'{STATS["cards_max"]} trail cards alive in a pattern')
print(f'test_blade: {N[0] - len(FAILS)}/{N[0]} passed' + (f', {len(FAILS)} FAILED' if FAILS else ''))
sys.exit(1 if FAILS else 0)
