"""Helpers of S2-T (tail.py; s2.md 1): pure Python + line builders shared by the tail patterns and their tests.

    tags(pid, *extra)            the summon Tags list of a pattern entity (rlk_room rlk_mb_aux rlk_mb_az_pat rlk_mb_az_p<id>)
    xtags(*extra)                the same for an addon-body entity (rlk_mb_az_x instead of the pattern tag)
    sel(tag, kind)               a limit=1 selector of a marker / item_display by tag
    keep_lock(new, base)         re-tag the last rlk_mb_az_lock marker as a pattern-owned marker (never rlk_mb_az_kept:
                                 the core kills kept markers when any main-slot pattern finishes, which would cut the
                                 bg emitter's locks)
    tele_dyn(shape, dyn, **st)   a kit telegraph whose tell / hold come from scores (resume redraws): storage az.tl
    tail_line(clip, t)           the tail root (s, f) and the tail-line yaw at played tick t in the START frame of a whip
                                 clip (the manifest tracks composed with the yaw schedule, as h_core.whip_wedges)
    wall_pieces(clip, e)         the four P7 Cryo wall pieces (annular sectors r 5-12) of plan 4.6 whip/sweep
    flight(d)                    43: max(12, ceil(d / 1.6)) ticks for a lance of length d blocks
"""
import json
import math

from . import api as A
from .h_core import rot_local, dir_yaw

__all__ = []                       # nothing re-exported through api (tail.py imports this module directly)

MK = 'minecraft:marker'
ID = 'minecraft:item_display'


def tags(pid, *extra):
    return json.dumps(['rlk_room', 'rlk_mb_aux', 'rlk_mb_az_pat', f'rlk_mb_az_p{pid}'] + list(extra), separators=(',', ':'))


def xtags(*extra):
    return json.dumps(['rlk_room', 'rlk_mb_aux', 'rlk_mb_az_pat', 'rlk_mb_az_x'] + list(extra), separators=(',', ':'))


def sel(tag, kind=MK, extra=''):
    return f'@e[type={kind},tag={tag}{extra},limit=1]'


def keep_lock(new, base):
    """The marker made by u/lockp or the lockv lines (tag rlk_mb_az_lock) becomes `new` (+ rlk_mb_az_pat and the base
    pattern tag): the next lock call cannot kill it, the core's finish does not either."""
    s = f'@e[type={MK},tag={new}]'
    return [f'kill {s}',
            f'tag @e[type={MK},tag=rlk_mb_az_lock] add {new}',
            f'tag {s} add rlk_mb_az_pat', f'tag {s} add {base}',
            f'tag {s} remove rlk_mb_az_lock', f'tag {s} remove rlk_mb_lock']


TENTHS = {'r', 'r0', 'r1', 'len', 'w', 'back', 'h'}


def tele_dyn(shape, dyn, **static):
    """(prep lines, call line): a kit telegraph fx/tele/<shape> with the static args (blocks / ticks) and the args of
    `dyn` {arg: score} read from scores at run time (ticks). Prefix the call line with the execute position."""
    vals = ','.join(f'{k}:{int(round(v * 10)) if k in TENTHS else int(v)}' for k, v in static.items())
    prep = [f'data modify storage rlk:mboss az.tl set value {{{vals}}}']
    prep += [f'execute store result storage rlk:mboss az.tl.{k} int 1 run scoreboard players get {sc} mb' for k, sc in dyn.items()]
    return prep, f'function {A.K.FN}tele/{shape} with storage rlk:mboss az.tl'


def _line_yaw(clip, t):
    root, tip = A.track(clip, 'tail_root'), A.track(clip, 'tail_tip')
    d = A.yaw_at(clip, t)
    rs, rf = rot_local(root[t][0], root[t][2], d)
    ts, tf = rot_local(tip[t][0], tip[t][2], d)
    return (rs, rf), dir_yaw(ts - rs, tf - rf)


def tail_line(clip, t0, t1):
    """[(t, root (s, f), yaw)] for t0..t1, the yaws unwrapped to a continuous sequence (start frame)."""
    out, prev = [], None
    for t in range(t0, t1 + 1):
        r, y = _line_yaw(clip, t)
        if prev is not None:
            while y - prev > 180:
                y -= 360
            while y - prev < -180:
                y += 360
        out.append((t, r, y))
        prev = y
    return out


def wall_pieces(clip, e=None):
    """P7 whip/sweep (Cryo): piece k (0..3) erupts at E + 2 + 2k over the arc the tail swept in ticks E+2k .. E+2k+2,
    as an annular sector r 5 .. 12 about the tail root of tick E+2k+1. Returns dicts in the START frame relative to
    the context point (the tail root at E): off (ds, df), mid (yaw relative to the start facing), half (degrees,
    rounded up + 1 so the sector is never smaller than the swept arc), t (eruption offset from E)."""
    ev = A.CLIPS[clip]['events']
    e = ev['sweep'] if e is None else e
    line = {t: (r, y) for t, r, y in tail_line(clip, e, e + 8)}
    r_e = line[e][0]
    out = []
    for k in range(4):
        (r_m, _), (_, y0), (_, y1) = line[e + 2 * k + 1], line[e + 2 * k], line[e + 2 * k + 2]
        out.append(dict(k=k, t=2 + 2 * k, off=(r_m[0] - r_e[0], r_m[1] - r_e[1]), mid=(y0 + y1) / 2.0,
                        half=int(math.ceil(abs(y1 - y0) / 2.0)) + 1, span=(min(y0, y1), max(y0, y1))))
    return out


def whip_end(clip, e=None):
    """The tail root at sweep_end relative to the context point (the root at E = sweep) and the end-line yaw."""
    ev = A.CLIPS[clip]['events']
    e = ev['sweep'] if e is None else e
    line = {t: (r, y) for t, r, y in tail_line(clip, e, ev['sweep_end'])}
    (r_e, _), (r_s, y_s) = line[e], line[ev['sweep_end']]
    return (r_s[0] - r_e[0], r_s[1] - r_e[1]), y_s


def flight(d):
    """43: the lance flight max(12, ceil(d / 1.6)) ticks (plan 5 43)."""
    return max(12, int(math.ceil(d / 1.6 - 1e-9)))


def flight_lines(score_d2, score_f, nmax=40):
    """The same in commands: score_d2 = d^2 in cm^2 (d in centimetres); score_f = the ticks (12 .. nmax)."""
    lines = [f'scoreboard players set {score_f} mb 12']
    for n in range(13, nmax + 1):
        lines.append(f'execute if score {score_d2} mb matches {(160 * (n - 1)) ** 2 + 1}.. run scoreboard players set {score_f} mb {n}')
    return lines
