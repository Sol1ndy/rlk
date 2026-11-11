#!/usr/bin/env python3
"""sheets.py: the shot sheets and the framing report of 홍련's cutscenes (lane H2; hr_design §6.2).

    python3 sheets.py <datapack root> <out dir> [sequence ...] [--stage c|n|e|s|w|all] [--no-img] [--w 320]

For each sequence (intro, cs1, repel60, repel5, ending) and each stage placement it runs the real sequence functions in
the lane's world (seqsim), takes for every shot its cut tick, the end of each of its moves, its middle (16 t and more) and (60 t and more)
its last tick, and from the live stand's real pose renders what the camera sees (shots.py) with the stand-in figures. Per frame
it reports (frames.json; test_seq.py asserts on it):
  eye      the lens: its cell (air / light required), its height over the floor, its distance from the arena axis
  look     the first block or plant between the lens and the look point (None = clear)
  sub      for each subject of the shot (cam.Shot.sub: her / the actor / the moon): on screen (sx, sy in -1..1), the share of
           the frame its stand-in fills, and what hides its head from the lens (None = nothing)
Stage placements: `c` the avatar 12 b south of the centre facing her at the centre (CS0 has its own fixed stage); n / e /
s / w: the avatar at radius 24 on that bearing with her 6 b further along the wall (the stage then faces the centre).
The stand-ins: her posture per beat is the design's table (§3), written out below; the actor's figure (root, head, sword)
comes per tick from lane H3's manifest (tools/player_motion/cine/manifest.json), from the design's displacement table
(§4.2) without it. Per frame also `near`: the distance from the lens to the nearest figure (never inside one), and
`look_hidden`: the first solid block between the lens and the shot's look point.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'tests' / 'lib'))
import seqsim as Q  # noqa: E402
import camsim as CS  # noqa: E402
import shots as SH  # noqa: E402
import hrsim as H  # noqa: E402

CY = 201.0


def lerp_keys(keys, t):
    """Piecewise-linear value of [(tick, value)] at t (values: numbers or tuples)."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            u = (t - t0) / (t1 - t0) if t1 > t0 else 1.0
            if isinstance(v0, tuple):
                return tuple(a + (b - a) * u for a, b in zip(v0, v1))
            return v0 + (v1 - v0) * u
    return keys[-1][1]


# the actor's displacement from the stage origin (r, u, f), hr_design §4.2
ACTOR_SHIFT = {
    'intro': [(0, (0, 0, -6.0)), (20, (0, 0, -6.0)), (100, (0, 0, 0)), (1250, (0, 0, 0)), (1258, (0, 0, -0.3)), (1390, (0, 0, -0.3)),
              (1400, (0, 0, 0))],
    'cs1': [(0, (0, 0, 0)), (34, (0, 0, 0)), (44, (0, 0, -1.2)), (60, (0, 0, -1.2)), (80, (0, 0, 0)), (652, (0, 0, 0)),
            (664, (0, 0, -0.5)), (694, (0, 0, -0.5)), (716, (0, 0, 0))],
    'repel': [(0, (0, 0, 0)), (30, (0, 0, 0)), (36, (0, 0, 0.5)), (62, (0, 0, 0.5)), (68, (0, 0, 1.8)), (132, (0, 0, 1.8)),
              (139, (0, 0, 0))],
    'ending': [(0, (0, 0, 1.8)), (4, (0, 0, 1.8)), (16, (0, 0, 0.8)), (50, (0, 0, 0.8)), (54, (0, 0, 1.3)), (80, (0, 0, 1.3)),
               (90, (0, 0, -0.6)), (94, (0, 0, -0.6)), (104, (0, 0, -1.5)), (118, (0, 0, -1.5)), (124, (0, 0, 1.0)),
               (150, (0, 0, 1.0)), (188, (0, 0, 2.5)), (204, (0, 0, 2.5)), (216, (0, 6.0, 1.5)), (304, (0, 6.0, 1.5)),
               (330, (0, 0, 0))],
    'event': [(0, (0, 0, 0))],
}
ACTOR_POSE = {'cs1': [(664, 694, 'kneel')], 'ending': [(104, 116, 'crouch')]}
# her posture per beat (her body position is the sequence's own; the clip gives the pose)
HER_POSE = {
    'intro': [(0, 800, 'sit'), (1230, 1234, 'crouch'), (1258, 1290, 'crouch')],
    'cs1': [],
    'repel': [(101, 133, 'lie')],
    'ending': [(0, 10, 'lie'), (334, 340, 'crouch')],
    'event': [],
}
HEAD = {'stand': 1.73, 'sit': 1.37, 'crouch': 1.05, 'kneel': 1.0}   # the rig's head anchor: standing 1.73, seated 1.37
ROCK_UNTIL = 1052           # CS0: the seat rock is there until she steps off it


def pose_of(table, name, t):
    for a, b, p in table.get(name, []):
        if a <= t < b:
            return p
    return 'stand'


def world_of(frame, r, u, f):
    (ox, oy, oz), yaw = frame
    a = math.radians(yaw)
    fw, lf = (-math.sin(a), math.cos(a)), (math.cos(a), math.sin(a))
    return (ox - r * lf[0] + f * fw[0], oy + u, oz - r * lf[1] + f * fw[1])


def actor_state(seq_name, rec):
    """(feet position, yaw, posture) of the actor's stand-in at a recorded tick."""
    key = {'repel60': 'repel', 'repel5': 'repel'}.get(seq_name, seq_name)
    t = rec['sq']
    st = rec['stage']
    if key == 'ending' and t >= 338 and rec['stage2']:
        st = rec['stage2']
    if key == 'event' and rec['stage2']:
        st = rec['stage2']
    if st is None:
        return None
    r, u, f = lerp_keys(ACTOR_SHIFT[key], t)
    return world_of(st, r, u, f), st[1], pose_of(ACTOR_POSE, key, t)


CLIP_OF = {'intro': 'cs0', 'cs1': 'cs1', 'repel': 'repel', 'ending': 'ending', 'event': 'coda'}
FACE2_AT = 344              # ending: the actor's root is turned to ST2 over 338-350 (char/cine/face)
_MAN = {}


def manifest(dp):
    """Lane H3's actor manifest of the tested tree (None without it)."""
    if dp not in _MAN:
        f = Path(dp) / 'tools/player_motion/cine/manifest.json'
        _MAN[dp] = json.loads(f.read_text(encoding='utf-8')) if f.exists() else None
    return _MAN[dp]


def actor_frame(key, rec):
    st = rec['stage']
    if key == 'ending' and rec['sq'] >= FACE2_AT and rec['stage2']:
        st = rec['stage2']
    if key == 'event' and rec['stage2']:
        st = rec['stage2']
    return st


def actor_fig(dp, seq_name, rec):
    """(stand-in boxes, the head point, the root's floor point) of the actor at a recorded tick; ([], None, None) without a
    stage. With the manifest: the root's shift, the head and the sword of that clip tick; else the design's table."""
    key = {'repel60': 'repel', 'repel5': 'repel'}.get(seq_name, seq_name)
    st = actor_frame(key, rec)
    if st is None:
        return [], None, None
    man = manifest(dp)
    if not man:
        pos, yaw, pose = actor_state(seq_name, rec)
        return SH.fig_boxes('actor', pos, yaw, pose), head_of(pos, yaw, pose), pos
    tk = man['clips'][CLIP_OF[key]]['tick']
    i = max(0, min(rec['sq'], len(tk['head']) - 1))
    W = lambda p: world_of(st, *p)                                    # noqa: E731
    head, sh = W(tk['head'][i]), tk['shift'][i]
    root = W(sh)
    lo = st[0][1] + min(tk['foot_r'][i][1], tk['foot_l'][i][1], sh[1] + 0.0)
    hi = head[1] - 0.25
    cx, cz = (root[0] + head[0]) / 2, (root[2] + head[2]) / 2
    boxes = [SH.box((cx, (lo + hi) / 2, cz), (0.55, max(0.2, hi - lo), 0.3), st[1], (214, 196, 150), 'actor'),
             SH.box(head, (0.5, 0.5, 0.5), st[1], (240, 214, 190), 'actor_head')]
    hilt, tip = W(tk['hilt'][i]), W(tk['tip'][i])
    for k in range(6):
        u = (k + 0.5) / 6
        boxes.append(SH.box(tuple(a + (b - a) * u for a, b in zip(hilt, tip)), (0.1, 0.1, 0.1), st[1], (230, 230, 240), 'sword'))
    return boxes, head, root


def her_state(seq_name, rec):
    key = {'repel60': 'repel', 'repel5': 'repel'}.get(seq_name, seq_name)
    pos, yaw = rec['body']
    return pos, yaw, pose_of(HER_POSE, key, rec['sq'])


def head_of(pos, yaw, posture):
    if posture == 'lie':
        a = math.radians(yaw)
        return (pos[0] + math.sin(a) * 1.7, pos[1] + 0.25, pos[2] - math.cos(a) * 1.7)
    return (pos[0], pos[1] + HEAD[posture], pos[2])


VIS_MIN = 0.5               # a subject's stand-in must show at least half of what it would with nothing before it
NEAR_MIN = 0.3              # the lens is never nearer than this to a figure
FIELD_PLANTS = ('minecraft:short_dry_grass', 'minecraft:tall_dry_grass', 'minecraft:crimson_roots')
PLANT_NEAR = 0.5            # a plant of the field nearer than this to the lens always counts as hiding


def flagged(v):
    """A subject entry of a frame that fails: off screen, its head hidden, or less than VIS_MIN of its figure showing. The
    field's own floor plants (1 b sprites, 20-30 % of its floor cells) before a figure low on the floor are not a hiding
    block when they are not right at the lens: the renderer draws them half transparent, a figure standing in them shows
    45 % and more through them."""
    hid = v['hidden']
    if hid and hid[0] == 'block' and hid[1] in FIELD_PLANTS and hid[2] >= PLANT_NEAR:
        return bool(v['sx'] is None or abs(v['sx']) > 1 or abs(v['sy']) > 1 or (v['vis'] is not None and v['vis'] < VIS_MIN - 0.05))
    return bool(hid or v['sx'] is None or abs(v['sx']) > 1 or abs(v['sy']) > 1 or (v['vis'] is not None and v['vis'] < VIS_MIN))


STAGES = {
    'c': ((880.0, 20.0), (880.0, 8.0)),
    'n': (Q.polar(24.0, 0), Q.polar(24.0, 15)),
    'e': (Q.polar(24.0, 90), Q.polar(24.0, 105)),
    's': (Q.polar(24.0, 180), Q.polar(24.0, 195)),
    'w': (Q.polar(24.0, 270), Q.polar(24.0, 285)),
}
PLAN = {'intro': ('intro', None, None), 'cs1': ('cs1', None, None), 'repel60': ('repel', {'at': 60}, None),
        'repel5': ('repel', {'at': 5}, None), 'ending': ('ending', None, ('event', None))}


def frame_ticks(track):
    out = []
    for s in track.shots:
        ts = {s.t}
        for m in s.moves:
            ts.add(m[1])
        if s.end - s.t >= 60:
            ts.add(s.end - 1)
        if s.end - s.t >= 16:
            ts.add((s.t + s.end) // 2)
        for t in sorted(ts):
            out.append((t, s))
    return out


def run(dp, name, stage='c'):
    """The recorded ticks of one sequence run ({sq: rec} per driven sequence name) and the sim."""
    s, pl = Q.setup(dp)
    assert Q.fight(s, park=(name != 'intro') or True)
    seq_name, args, then = PLAN[name]
    if name == 'intro':
        # the core's own spawn state: her seated at SEAT_POS facing the moon; the avatar at the arena's start
        import importlib
        sys.path.insert(0, str(Path(dp) / 'tools'))
        api = importlib.import_module('mboss_scarlet.api')
        b = H.body_of(s)
        b.pos = list(api.SEAT_POS)
        mp = api.MOON_POS
        b.rot = [math.degrees(math.atan2(-(mp[0] - b.pos[0]), mp[2] - b.pos[2])), 0.0]
        st = api.ARENA['start']
        s.avatar().pos = [st['x'], st['y'], st['z']]
    else:
        av, her = STAGES[stage]
        Q.place(s, av, her)
    stop_at = (lambda s: False)
    if name == 'repel5':
        stop_at = (lambda s: (s.sc('#sq', 'hr') or 0) >= 129 and s.drive and s.drive['name'] == 'repel')
    rec = Q.play(s, seq_name, args=args, then=then, until=stop_at)
    by = {}
    for r in rec:
        by.setdefault(r['seq'], {})[r['sq']] = r
    return s, by


def frames_of(dp, name, stage, arenas, img=True, w=320):
    sys.path.insert(0, str(Path(dp) / 'tools'))
    from mboss_scarlet import seq as SEQ, api, cam as CAM
    s, by = run(dp, name, stage)
    out, pics = [], []
    seqs = [PLAN[name][0]] + ([PLAN[name][2][0]] if PLAN[name][2] else [])
    for sn in seqs:
        tr = SEQ.tracks()[sn]
        for t, shot in frame_ticks(tr):
            rec = by.get(sn, {}).get(t)
            if rec is None or rec['cam'][shot.cam] is None:
                continue
            if name == 'repel5' and t > 129:
                continue
            (eye, rot) = rec['cam'][shot.cam]
            look = 'crimson' if (sn in ('repel', 'ending', 'event') or (sn == 'cs1' and t >= 664)) else 'moon'
            ar = arenas[look]
            hp, hy, hpose = her_state(sn, rec)
            boxes = SH.fig_boxes('her', hp, hy, hpose)
            aboxes, ahead, _aroot = actor_fig(dp, sn, rec)
            boxes += aboxes
            near = min(SH.box_dist(eye, b) for b in boxes)
            if sn == 'intro' and t < ROCK_UNTIL:
                sp = api.SEAT_POS
                boxes.append(SH.box((sp[0], sp[1] + 0.12, sp[2]), (1.2, 0.24, 0.64), hy, (120, 118, 112), 'rock'))
            cell, cls = ar.cell(eye)
            fr = {'ENT': {SEQ.BODY: (hp[0], hp[1] + Q.HUSK_EYE, hp[2])}, 'HR': (hp, hy)}
            for k, v in (('ST', rec['stage']), ('ST2', rec['stage2'])):
                if v:
                    fr[k] = v
            _e, lk = shot.at(t)
            ok_lk = lk[0] == 'W' or (lk[0] == 'ENT' and lk[1] in fr['ENT']) or (lk[0] != 'ENT' and lk[0] in fr)
            lw = CAM.to_world(lk, fr) if ok_lk else None
            lh = SH.ray_clear(ar, eye, lw, (), margin=0.5, solid_only=True) if lw else None
            row = dict(seq=name, sq=t, shot=shot.name, cam=shot.cam, stage=stage, eye=[round(v, 3) for v in eye],
                       rot=[round(v, 2) for v in rot], cell=cell, cell_ok=cls == SH.AIR, near=round(near, 3), look_hidden=lh,
                       height=round(eye[1] - CY, 3), radius=round(math.hypot(eye[0] - 880.0, eye[2] - 8.0), 2), sub={})
            rgb = depth = who = None
            if img or shot.sub:
                rgb, depth, who = SH.render(ar, eye, rot[0], rot[1], boxes, w=w, h=round(w * 9 / 16))
            for sub0 in shot.sub:
                sub = sub0.rstrip('?')
                if sub == 'moon':                      # the disc against the sky: a figure may stand before it (I12)
                    pt, own, tagset = api.MOON_POS, tuple(b['tag'] for b in boxes), ()
                elif sub == 'her':
                    pt, own, tagset = head_of(hp, hy, hpose), ('her', 'her_head', 'her_hat'), ('her', 'her_head', 'her_hat')
                else:
                    if ahead is None:
                        continue
                    pt, own, tagset = ahead, ('actor', 'actor_head', 'sword'), ('actor', 'actor_head')
                sx, sy, z = SH.project(eye, rot[0], rot[1], pt)
                hid = SH.ray_clear(ar, eye, pt, boxes, skip_tags=own, margin=0.3) if z > 0 else ('behind', '', 0)
                frac = vis = None
                if tagset:
                    frac = SH.visible_fraction(who, boxes, tagset)
                    alone = SH.alone_fraction(eye, rot[0], rot[1], [b for b in boxes if b['tag'] in tagset], w, round(w * 9 / 16))
                    vis = round(frac / alone, 3) if alone > 0 else 0.0
                row['sub'][sub] = dict(opt=sub0.endswith('?'), sx=None if sx is None else round(sx, 3), sy=None if sy is None else round(sy, 3),
                                       dist=round(z, 2), hidden=hid, frac=None if frac is None else round(frac, 4), vis=vis)
            out.append(row)
            if img:
                bad = (not row['cell_ok']) or near < NEAR_MIN or any(flagged(v) for v in row['sub'].values())
                label = ''.join(ch for ch in shot.name if ord(ch) < 128).strip()
                pics.append((f'{"! " if bad else ""}{name} {t} {label}', rgb))
    return out, pics


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    opt = {a.split('=')[0]: (a.split('=')[1] if '=' in a else True) for a in sys.argv[1:] if a.startswith('--')}
    dp, outd = Path(args[0]).resolve(), Path(args[1])
    outd.mkdir(parents=True, exist_ok=True)
    names = args[2:] or list(PLAN)
    st = opt.get('--stage', 'c')
    stages = ['c', 'n', 'e', 's', 'w'] if st == 'all' else [st]
    img = '--no-img' not in opt
    w = int(opt.get('--w', 320))
    arenas = {lk: SH.Arena(dp, lk) for lk in ('moon', 'crimson')}
    if arenas['moon'].unknown:
        print('unknown block colours:', arenas['moon'].unknown[:12])
    rows = []
    for name in names:
        for stg in (['c'] if name == 'intro' else stages):
            out, pics = frames_of(dp, name, stg, arenas, img=img, w=w)
            rows += out
            if img:
                per = 12
                for i in range(0, len(pics), per):
                    f = outd / f'{name}_{stg}_{i // per + 1}.jpg'
                    SH.sheet(pics[i:i + per], f, cols=3, w=w, h=round(w * 9 / 16), title=f'{name} · stage {stg} · sheet {i // per + 1}')
                    print('wrote', f)
    (outd / 'frames.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    eye_bad, sub_bad = verdict(rows)
    print(f'{len(rows)} frames; lens problems {len(eye_bad)}; shots with a subject never shown {len(sub_bad)}')
    for r in eye_bad:
        print('  LENS', r['seq'], r['stage'], r['sq'], r['shot'], 'cell', r['cell'], 'h', r['height'], 'r', r['radius'], 'near', r.get('near'))
    for r in rows:
        if r.get('look_hidden'):
            print('  LOOK', r['seq'], r['stage'], r['sq'], r['shot'], r['look_hidden'])
    for (seq, stage, shot, sub), frames in sub_bad.items():
        print('  SUBJECT', seq, stage, shot, sub, [(t, v['sx'], v['sy'], v['hidden'], v['vis']) for t, v in frames])


def verdict(rows):
    """(frames whose lens is in a block / plant, under 0.2 b over the floor, beyond the walk disc or nearer than NEAR_MIN to
    a figure; {(seq, stage, shot,
    subject): [(tick, entry)]} of the shots that never show a subject: on screen, its head unhidden, >= VIS_MIN of it)."""
    eye_bad = [r for r in rows if not r['cell_ok'] or r['height'] < 0.2 or r['radius'] > 25.0 or r.get('near', 9) < NEAR_MIN]
    seen, never = {}, {}
    for r in rows:
        for sub, v in r['sub'].items():
            k = (r['seq'], r['stage'], r['shot'], sub)
            seen.setdefault(k, []).append((r['sq'], v))
    for k, frames in seen.items():
        if all(flagged(v) for _t, v in frames) and not (k[1] != 'c' and frames[0][1].get('opt')):
            never[k] = frames               # (an optional foreground figure, cam.Track.cut: required on the centre stage only)
    return eye_bad, never


if __name__ == '__main__':
    main()
