#!/usr/bin/env python3
"""built_shots.py — 홍련's cutscene frames through the cameras AS BUILT, with her real rig and the real actor (fix lane HF-B).

  python3 -I built_shots.py <roguelike> --dbg <debug dp> --rp <rp> --seq intro|cs1|repel60|repel5|ending|event
                            (--ticks a,b,c | --lines | --shots) [--actor skirk] [--ortho az,el,ext] [--stage c|n|e|s|w]
                            [--rec <cache.json>] [--cols 3] [--w 640] [-o out.jpg]

The camera is the one the sequence functions really place: <roguelike>'s seq/<name>/** run in lane H2's world (hr/h2/
seqsim.py, the stage placement of hr/h2/sheets.py; `c` = the avatar 12 b south of the centre facing her at it), the live stand's
pose at each tick (its eye = its position: a marker armour stand). Her figure is her rig as built (the rig builder's
--debug-dp frames hr_dbg/<clip>/<t> of the clip tick the sequence shows) on her body as the sequence moved it; the actor is
lane H3's (the player rig builder's --cine-debug-dp frames cine_dbg/<clip>/<t> and cine_dbg/spawn_<character>, copied into the
same debug dp), in the stage frame the actor's root stands in (ST; ST2 from ending 344 and in the coda, char/cine/face).
Everything is drawn in that frame (origin 0 0 0, f = +Z, r = -X, u = +Y): no arena blocks, a flat floor.

  --ticks   the #sq ticks to draw;  --lines: the first, middle and last tick of every line this sequence plays (api.LINE_AT);
  --shots   every shot's cut tick and middle tick
  --ortho   instead of the shot camera an orthographic view "az,el,extent" centred between her and the actor (a side view)
  --cam     instead of the shot camera a fixed one "r,u,f,lr,lu,lf" (eye, look point; the actor's stage frame)
  --rec     cache of the sequence run (the records this tool needs), re-used when it exists (delete it after a seq.py change)

Each panel's label: the sequence, #sq, the shot, her clip tick, the line on screen (if any) and `head d=` the lens's distance
to her head. Building the debug dp:
  node tools/build_scarlet_rig.mjs --resourcepack <rp copy> --datapack <scratch dp> --only <clips> --debug-dp <dbg> --debug-clips <clips>
  node tools/build_player_rig.mjs --datapack <scratch dp2> --resourcepack <rp copy> --cine-debug-dp <cdbg> --cine-debug-clips <clips>
  cp -r <cdbg>/data/rlk/function/cine_dbg <dbg>/data/rlk/function/
(both into scratch datapacks: --only writes a partial rig; never into the tree; a rig build into a pack copy reorders its
items atlas list, so use a throwaway pack copy.)
"""
import argparse
import importlib
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
SIM = HERE.parent.parent
sys.path.insert(0, str(HERE.parent / 'h2'))
CY = 201.0
ACLIP = {'intro': 'cs0', 'cs1': 'cs1', 'repel': 'repel', 'ending': 'ending', 'event': 'coda'}
FACE2_AT = 344                    # ending: the actor's root has turned to ST2 (char/cine/face 338-350)
HEAD_H = 0.25                     # her head anchor = the centre of the 0.5-b head box


def frame_of(seq, rec):
    """The frame the actor stands in at this record: (origin, yaw)."""
    st = rec['stage']
    if seq == 'ending' and rec['sq'] >= FACE2_AT and rec.get('stage2'):
        st = rec['stage2']
    if seq == 'event' and rec.get('stage2'):
        st = rec['stage2']
    return st


def to_frame(p, fr):
    """A world point -> (r, u, f) in frame fr = ((x, y, z), yaw)."""
    (ox, oy, oz), yaw = fr
    a = math.radians(yaw)
    fw, lf = (-math.sin(a), math.cos(a)), (math.cos(a), math.sin(a))
    dx, dz = p[0] - ox, p[2] - oz
    return (-(dx * lf[0] + dz * lf[1]), p[1] - oy, dx * fw[0] + dz * fw[1])


def render_xyz(st):
    return (-st[0], st[1], st[2])


def her_clip(seq, t, branch='ev_give'):
    if seq == 'intro':
        return ('intro', t) if t < 1290 else ('intro_end', t - 1290)
    if seq == 'event':
        return (branch, t)
    return (seq, t)


def run_records(dp, name, stage, cache):
    if cache and Path(cache).exists():
        return json.loads(Path(cache).read_text())
    import sheets as SHE
    _s, by = SHE.run(str(dp), name, stage)
    out = {}
    for sq_name, recs in by.items():
        out[sq_name] = {str(t): dict(sq=r['sq'], live=r['live'], cam={str(k): v for k, v in r['cam'].items()}, body=r['body'],
                                     stage=r['stage'], stage2=r['stage2'], held=r['held']) for t, r in recs.items()}
    if cache:
        Path(cache).write_text(json.dumps(out))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dp')
    ap.add_argument('--dbg', required=True)
    ap.add_argument('--rp', required=True)
    ap.add_argument('--seq', required=True, choices=['intro', 'cs1', 'repel60', 'repel5', 'ending', 'event'])
    ap.add_argument('--ticks')
    ap.add_argument('--lines', action='store_true')
    ap.add_argument('--shots', action='store_true')
    ap.add_argument('--actor', default='skirk')
    ap.add_argument('--no-actor', action='store_true')
    ap.add_argument('--ortho')
    ap.add_argument('--cam', help='instead of the shot camera a fixed camera "r,u,f,lr,lu,lf": eye and look point in the frame of the actor\'s root (ST)')
    ap.add_argument('--stage', default='c')
    ap.add_argument('--rec')
    ap.add_argument('--cols', type=int, default=3)
    ap.add_argument('--w', type=int, default=640)
    ap.add_argument('--fov', type=float, default=70.0)
    ap.add_argument('-o', '--out', required=True)
    a = ap.parse_args()
    dp = Path(a.dp).resolve()
    sys.path.insert(0, str(dp / 'tools'))
    api = importlib.import_module('mboss_scarlet.api')
    SEQ = importlib.import_module('mboss_scarlet.seq')
    seq = {'repel60': 'repel', 'repel5': 'repel'}.get(a.seq, a.seq)
    run_name = 'ending' if seq == 'event' else a.seq
    recs = run_records(dp, run_name, a.stage, a.rec)[seq]
    tr = SEQ.tracks()[seq]
    lines = {i: (s, t0, n) for i, (s, t0, n) in api.LINE_AT.items() if s == seq or (seq == 'intro' and s == 'intro_end')}
    lines = {i: ((t0 + api.SKIP_T) if s == 'intro_end' else t0, n) for i, (s, t0, n) in lines.items()}

    def line_at(t):
        return [i for i, (t0, n) in lines.items() if t0 <= t < t0 + n]
    if a.ticks:
        ticks = [int(x) for x in a.ticks.split(',')]
    elif a.lines:
        ticks = sorted({x for t0, n in lines.values() for x in (t0, t0 + n // 2, t0 + n - 1)})
    else:
        ticks = sorted({x for s in tr.shots for x in (s.t, (s.t + s.end) // 2)})
    ticks = [t for t in ticks if str(t) in recs]
    dbg = Path(a.dbg)
    fdir = dbg / 'data/rlk/function/hr_shot'
    fdir.mkdir(parents=True, exist_ok=True)
    seat = (dbg / 'data/rlk/function/hr_dbg/seat.mcfunction').read_text().splitlines()
    tracks = json.loads((dp / 'tools/dev/sim/hr/cine/her_tracks.json').read_text())['clips']
    pw = a.w
    ph = round(pw * 9 / 16)
    panels = []
    with tempfile.TemporaryDirectory() as td:
        for i, t in enumerate(ticks):
            r = recs[str(t)]
            fr = frame_of(seq, r)
            clip, ct = her_clip(seq, t)
            bpos, byaw = r['body']
            hb = to_frame(bpos, fr)
            hyaw = byaw - fr[1]
            hw = render_xyz(hb)
            ln = [f'tp @e[tag=rlk_hr_part] {hw[0]:.3f} {hw[1]:.3f} {hw[2]:.3f} {hyaw:.2f} 0']
            if not a.no_actor and (dbg / f'data/rlk/function/cine_dbg/{ACLIP[seq]}/{t}.mcfunction').exists():
                ln += [f'function rlk:cine_dbg/spawn_{a.actor}', f'function rlk:cine_dbg/{ACLIP[seq]}/{t}']
            if seq == 'intro' and t < 1052:
                sp = to_frame(api.SEAT_POS, fr)
                sw = render_xyz(sp)
                ln += [x.replace('~ ~ ~', f'{sw[0]:.3f} {sw[1]:.3f} {sw[2]:.3f}') for x in seat if 'tuff' in x]
            (fdir / f'p{i}.mcfunction').write_text('\n'.join(ln) + '\n')
            out = Path(td) / f'p{i}.png'
            if not (dbg / f'data/rlk/function/hr_dbg/{clip}/{ct}.mcfunction').exists():
                print(f'no debug frame hr_dbg/{clip}/{ct}: build it with --debug-clips {clip}')
                continue
            cmd = [sys.executable, '-I', str(SIM / 'az/understand/rigtech_render.py'), '--dp', str(dbg), '--rp', a.rp,
                   '--spawn', 'rlk:boss/scarlet/rig/spawn', '--apply', f'rlk:hr_dbg/{clip}/{ct}', f'rlk:hr_shot/p{i}',
                   '--origin', '0', '0', '0', '--yaw', f'{hyaw:.2f}', '--light', 'mc', '-q', '--width', str(pw * 2), '--no-grid',
                   '--floor', '70,40,48', '--floor-half', '30', '-o', str(out)]
            head = None
            hc = tracks.get(clip, {})
            if hc.get('staged') and hc['head'][ct]:
                # her head in the frame: her clip's stage-frame head relative to her root track, on her real body
                rt = hc['root'][ct]
                hd = hc['head'][ct]
                d0 = [hd[0] - rt[0], hd[1] - rt[1], hd[2] - rt[2]]
                ya = math.radians(hyaw - rt[3])
                c, s_ = math.cos(ya), math.sin(ya)
                head = (hb[0] + d0[0] * c + d0[2] * s_, hb[1] + d0[1], hb[2] - d0[0] * s_ + d0[2] * c)
            if a.cam:
                c = [float(x) for x in a.cam.split(',')]
                ew, lw = render_xyz(c[:3]), render_xyz(c[3:])
                dx, dy, dz = (lw[i] - ew[i] for i in range(3))
                yaw, pitch = math.degrees(math.atan2(-dx, dz)), -math.degrees(math.atan2(dy, math.hypot(dx, dz)))
                cmd += ['--views', 'camera', '--camera', f'{ew[0]:.3f}', f'{ew[1]:.3f}', f'{ew[2]:.3f}', f'{yaw:.2f}', f'{pitch:.2f}',
                        '--fov', str(a.fov), '--aspect', '0.5625']
                sid, dist = 'cam', (math.dist(c[:3], head) if head else None)
            elif a.ortho:
                az, el, ext = a.ortho.split(',')
                cmd += ['--views', f'az:{az},{el}', '--extent', ext, '--center', f'{hw[0] / 2:.3f}', '1.1', f'{hw[2] / 2:.3f}', '--aspect', '0.5625']
                sid, dist = 'ortho', None
            else:
                cam = r['cam'][str(r['live'])]
                if cam is None:
                    print(f'{t}: no live stand')
                    continue
                (cpos, crot) = cam
                e = to_frame(cpos, fr)
                ew = render_xyz(e)
                yaw = crot[0] - fr[1]
                cmd += ['--views', 'camera', '--camera', f'{ew[0]:.3f}', f'{ew[1]:.3f}', f'{ew[2]:.3f}', f'{yaw:.2f}', f'{crot[1]:.2f}',
                        '--fov', str(a.fov), '--aspect', '0.5625']
                sid = tr.shot_at(t).name
                dist = math.dist(e, head) if head else None
            res = subprocess.run(cmd, capture_output=True, text=True)
            if not out.exists():
                print(res.stdout[-1500:], res.stderr[-1500:])
                raise SystemExit(f'render failed at {t}')
            im = Image.open(out).convert('RGB')
            W, H = im.size
            im = im.crop((0, H - int(W * 9 / 16), W, H)).resize((pw, ph), Image.LANCZOS)
            d = ImageDraw.Draw(im)
            lab = ''.join(ch for ch in sid if ord(ch) < 128).strip()
            ls = line_at(t)
            txt = f'{a.seq} #{t} {lab} [{clip} {ct}]' + (f' line {ls[0]}' if ls else '') + (f' head d={dist:.2f}' if dist else '')
            d.rectangle((0, 0, pw, 14), fill=(0, 0, 0))
            d.text((3, 1), txt, fill=(255, 235, 120))
            panels.append(im)
            print(txt, flush=True)
    rows = (len(panels) + a.cols - 1) // a.cols
    sheet = Image.new('RGB', (pw * a.cols, ph * max(1, rows)), (16, 16, 20))
    for i, im in enumerate(panels):
        sheet.paste(im, ((i % a.cols) * pw, (i // a.cols) * ph))
    sheet.save(a.out, quality=86)
    print(a.out, len(panels), 'panels')


if __name__ == '__main__':
    main()
