#!/usr/bin/env python3
"""framing.py: per-tick framing of 홍련's cutscenes through the cameras as built (fix lane HF-B; test_seq.py `frame` / `lines`).

    python3 framing.py <datapack root> [intro cs1 repel60 ending] [--stage c]

For every tick of a locked sequence run in lane H2's world (seqsim, the stage placement of sheets.py) it takes the live stand's
real pose and projects into its picture (70 degrees vertical, 16 : 9): her head and pelvis (her rig's own points: lane H2c's
tools/dev/sim/hr/cine/her_tracks.json, relative to her root track, put on her body as the sequence moved it) and the actor's
head (lane H3's tools/player_motion/cine/manifest.json, in the stage frame its root stands in). Per tick:
  shot      the live shot's name and subjects (cam.Shot.sub)
  her       (sx, sy, depth) of her head (None: behind the lens), her pelvis likewise, `d` = the lens's distance to her head
  actor     (sx, sy, depth) of the actor's head
  line      the line ids on screen (api.LINE_AT spans)
  gone      the coda after she has left (E40, state/hidden): nothing of her to frame (her points in the coda: the ending's
            last pose, H_POSE, where the coda's clips start and stay)
Used by test_seq.py: `frame` (no tick of a shot with a figure subject shows none of its subjects: HB-04) and `lines` (every tick
of every line is on a shot close on her: her head inside the frame's middle, the lens within CLOSE b of it: HB-06).
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'tests' / 'lib'))
import shots as SH  # noqa: E402

CLOSE = 2.2              # b: the lens to her head while a line plays (a 70-degree frame 3.1 b tall there: head and shoulders
                         # with the hat, about 1 b, fill a third of it and more)
INNER = 0.85             # her head inside this part of the frame (sx, sy in -INNER..INNER) while a line plays
ACLIP = {'intro': 'cs0', 'cs1': 'cs1', 'repel': 'repel', 'ending': 'ending', 'event': 'coda'}
FACE2_AT = 344           # the ending: the actor's root has turned to ST2 (char/cine/face 338-350)
LAND2 = 334              # the ending: her root track is in ST2 from her landing on


def world_of(frame, p):
    (ox, oy, oz), yaw = frame
    a = math.radians(yaw)
    fw, lf = (-math.sin(a), math.cos(a)), (math.cos(a), math.sin(a))
    r, u, f = p
    return (ox - r * lf[0] + f * fw[0], oy + u, oz - r * lf[1] + f * fw[1])


def to_frame(p, frame):
    (ox, oy, oz), yaw = frame
    a = math.radians(yaw)
    fw, lf = (-math.sin(a), math.cos(a)), (math.cos(a), math.sin(a))
    dx, dz = p[0] - ox, p[2] - oz
    return (-(dx * lf[0] + dz * lf[1]), p[1] - oy, dx * fw[0] + dz * fw[1])


def her_clip(seq, t):
    if seq == 'intro':
        return ('intro', t) if t < 1290 else ('intro_end', t - 1290)
    if seq == 'event':
        return ('ending', 1372)        # the coda's clips start from the ending's last pose (H_POSE) and keep her in place
    return (seq, t)


def her_point(tracks, seq, rec, kind):
    """Her `kind` point (her_tracks: head / pelvis / ...) in world coordinates at a recorded tick, or None."""
    clip, ct = her_clip(seq, rec['sq'])
    c = tracks.get(clip)
    if not c or not c.get('staged') or ct >= len(c[kind]) or c[kind][ct] is None or rec['body'] is None:
        return None
    fr = rec['stage2'] if (seq == 'ending' and rec['sq'] >= LAND2 and rec['stage2']) else rec['stage']
    if fr is None:
        return None
    if seq == 'event':
        fr = rec['stage2'] or rec['stage']
    rt, P = c['root'][ct], c[kind][ct]
    d = (P[0] - rt[0], P[1] - rt[1], P[2] - rt[2])
    (bpos, byaw) = rec['body']
    hb = to_frame(bpos, fr)
    ya = math.radians((byaw - fr[1]) - rt[3])
    co, si = math.cos(ya), math.sin(ya)
    return world_of(fr, (hb[0] + d[0] * co + d[2] * si, hb[1] + d[1], hb[2] - d[0] * si + d[2] * co))


def actor_head(man, seq, rec):
    if not man or rec['stage'] is None:
        return None
    tk = man['clips'][ACLIP[seq]]['tick']
    fr = rec['stage']
    if seq == 'ending' and rec['sq'] >= FACE2_AT and rec['stage2']:
        fr = rec['stage2']
    if seq == 'event' and rec['stage2']:
        fr = rec['stage2']
    i = max(0, min(rec['sq'], len(tk['head']) - 1))
    return world_of(fr, tk['head'][i])


def lines_of(api, seq):
    out = {}
    for i, (s, t0, n) in api.LINE_AT.items():
        if s == seq:
            out[i] = (t0, n)
        elif seq == 'intro' and s == 'intro_end':
            out[i] = (t0 + api.SKIP_T, n)
        elif seq == 'event' and s == 'event':
            out[i] = (t0, n)
    return out


def analyse(dp, name, stage='c', recs=None):
    """[{sq, shot, sub, her, pelvis, d, actor, line}] for every held tick of sequence run `name` (sheets.PLAN key)."""
    dp = Path(dp)
    sys.path.insert(0, str(dp / 'tools'))
    from mboss_scarlet import seq as SEQ, api
    import sheets as SHE
    tracks = json.loads((dp / 'tools/dev/sim/hr/cine/her_tracks.json').read_text())['clips']
    mf = dp / 'tools/player_motion/cine/manifest.json'
    man = json.loads(mf.read_text()) if mf.exists() else None
    if recs is None:
        _s, recs = SHE.run(str(dp), name, stage)
    out = []
    for sn, by in recs.items():
        tr = SEQ.tracks().get(sn)
        if tr is None:
            continue
        lines = lines_of(api, sn)
        for t in sorted(by):
            r = by[t]
            if not r.get('held') or r['cam'].get(r['live']) is None:
                continue
            if name == 'repel5' and t > 129:
                continue
            (eye, rot) = r['cam'][r['live']]
            sh = tr.shot_at(t)
            hp = her_point(tracks, sn, r, 'head')
            pp = her_point(tracks, sn, r, 'pelvis')
            ah = actor_head(man, sn, r)
            pj = (lambda p: SH.project(eye, rot[0], rot[1], p) if p else None)  # noqa: E731
            gone = sn == 'event' and t >= api.EV_T['hide']          # the coda: she has left (state/hidden at E40)
            out.append(dict(seq=sn, sq=t, gone=gone, shot=sh.name if sh else None, sub=tuple(sh.sub) if sh else (), her=pj(hp), pelvis=pj(pp),
                            d=math.dist(eye, hp) if hp else None, actor=pj(ah), ad=math.dist(eye, ah) if ah else None,
                            line=[i for i, (t0, n) in lines.items() if t0 <= t < t0 + n]))
    return out


def inside(p, k=1.0):
    return p is not None and p[0] is not None and abs(p[0]) <= k and abs(p[1]) <= k and p[2] > 0.05


def empty_ticks(rows):
    """Ticks of a shot with a figure subject whose picture holds none of them (her head / pelvis, the actor's head)."""
    bad = []
    for r in rows:
        if r['gone']:
            continue
        subs = [x.rstrip('?') for x in r['sub']]
        if not any(x in ('her', 'actor') for x in subs):
            continue
        seen = (('her' in subs and (inside(r['her']) or inside(r['pelvis']))) or ('actor' in subs and inside(r['actor'])))
        if not seen:
            bad.append(r)
    return bad


def far_lines(rows):
    """Ticks of a line not on a shot close on her: her head off the frame's middle or the lens farther than CLOSE from it."""
    return [r for r in rows if r['line'] and not r['gone'] and not (inside(r['her'], INNER) and r['d'] is not None and r['d'] <= CLOSE)]


def spans(rows):
    """[(seq, shot, t0, t1)] runs of consecutive ticks."""
    out = []
    for r in rows:
        if out and out[-1][0] == r['seq'] and out[-1][1] == r['shot'] and out[-1][3] == r['sq'] - 1:
            out[-1][3] = r['sq']
        else:
            out.append([r['seq'], r['shot'], r['sq'], r['sq']])
    return [tuple(x) for x in out]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    opt = {a.split('=')[0]: (a.split('=')[1] if '=' in a else True) for a in sys.argv[1:] if a.startswith('--')}
    dp = Path(args[0]).resolve()
    names = args[1:] or ['intro', 'cs1', 'repel60', 'ending']
    for name in names:
        rows = analyse(dp, name, opt.get('--stage', 'c'))
        print(f'== {name}: {len(rows)} held ticks')
        for sp in spans(empty_ticks(rows)):
            print('  EMPTY', sp)
        fl = far_lines(rows)
        for sp in spans(fl):
            ds = [r['d'] for r in fl if r['seq'] == sp[0] and sp[2] <= r['sq'] <= sp[3] and r['d'] is not None]
            print('  LINE-FAR', sp, 'lines', sorted({i for r in fl if r['seq'] == sp[0] and sp[2] <= r['sq'] <= sp[3] for i in r['line']}),
                  f'd {min(ds):.2f}-{max(ds):.2f}' if ds else 'd -')


if __name__ == '__main__':
    main()
