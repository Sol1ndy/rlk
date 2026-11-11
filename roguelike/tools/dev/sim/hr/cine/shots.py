#!/usr/bin/env python3
"""shots.py — rendered sheets of 홍련's cinematic clips from the design's camera points (lane H2c drawing tool).

  python3 -I shots.py --dbg <debug dp> --rp <rp> --roots <roots.json> --seq cs1 [--ticks 0,8,10,..] [--per 3] [--cols 6]
                      [--width 2000] [--no-actor] [--markers] -o out.jpg

<debug dp>   the rig builder's --debug-dp folder (hr_dbg/<clip>/<t>, hr_dbg/avatar)
<roots.json> her root per sequence tick: `node tools/dev/sim/hr/cine/roots.mjs > roots.json` (scarlet_cine.mjs rootAt)
The shot tables below are hr_design.md §3 (eye -> look per shot; frames ST = the stage, HR = her body, W = a stage point given
directly). World of the render: the stage origin at 0 0 0, f = +Z, r = -X, u = +Y. The actor is a stand-in: the debug avatar
(Skirk's idle pose) at the stage origin + the shift of hr_design.md §4.2, facing +f; it does not play H3's clips. Contact points
(§4.3) are drawn as markers with --markers. Renderer: az/understand/rigtech_render.py (this copy of tools/dev/sim).
"""
import argparse, json, math, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
SIM = HERE.parent.parent

MOON = ('W', 0.0, 17.0, 60.0)
# (t0, t1, id, eye0, eye1 | None, (move t0, move t1) | None, look)
SHOTS = {
 'intro': [
  (0, 60, 'I1', ('ST', .6, 1.9, -9), ('ST', .6, 1.7, -4.5), (20, 60), ('ACT', 0, 1.4, 3)),
  (60, 110, 'I2', ('ST', -7, 1.2, -3.5), ('ST', -7, 1.2, -.5), (60, 100), ('ACTR', 0, 1.2, 0)),
  (110, 170, 'I3', ('ST', -3, 1.5, 14), None, None, MOON),
  (170, 250, 'I4', ('HR', .9, .75, .9), None, None, ('HR', .25, .62, .35)),
  (250, 320, 'I5', ('HR', 1.1, 1.45, .25), None, None, ('HR', 0, 1.6, .05)),
  (320, 410, 'I6', ('HR', -.55, .5, -.7), None, None, ('HR', -.35, 1.05, .5)),
  (410, 460, 'I7', ('HR', .9, .6, .5), None, None, ('HR', .45, .28, 0)),
  (460, 536, 'I8', ('HR', .75, 1.0, -.9), None, None, MOON),
  (536, 666, 'I9', ('HR', -1.6, 1.5, -2.2), ('HR', -1.3, 1.45, -1.8), (536, 666), ('HR', .2, 1.3, .6)),
  (666, 750, 'I10', ('ST', .45, 1.75, -.9), None, None, ('ST', 0, 1.5, 20.7)),
  (750, 790, 'I11', ('HR', .7, .85, .6), None, None, ('HR', .3, .8, .1)),
  (790, 910, 'I12', ('ST', 0, .25, 16), None, None, ('HR', 0, 1.5, 0)),
  (910, 970, 'I13', ('ST', .25, 1.75, 19.3), None, None, ('HR', 0, 1.7, 0)),
  (970, 1040, 'I14', ('ST', -6.3, 3.5, 22.9), None, None, ('ST', -24.6, 2, 8.4)),
  (1040, 1230, 'I15', ('ST', 0, 1.3, 9.5), None, None, ('HR', 0, 1.4, 0)),
  (1230, 1260, 'I16', ('ST', .8, .3, 8.5), None, None, ('HR', 0, 1.6, 0)),
  (1260, 1290, 'I17', ('ST', 1.6, .5, 4.2), None, None, ('HR', 0, .9, 0)),
  (1290, 1350, 'I18', ('HR', .15, 1.35, 1.0), None, None, ('HR', 0, 1.62, 0)),
  (1350, 1406, 'I19', ('HR', .4, 1.4, 1.6), ('HR', .6, 1.3, 3.2), (1350, 1400), ('HR', 0, 1.3, 0)),
  (1406, 1441, 'I20', ('ST', .6, 1.8, 3.0), ('ST', 0, 2.6, -3.4), (1406, 1436), ('ST', 0, 1.5, 6.5)),
 ],
 'cs1': [
  (0, 6, 'S1', ('ST', -9, 2.2, 4.5), None, None, ('ST', 0, 1.2, 4.5)),
  (6, 34, 'S2', ('ST', -2.6, 1.3, .8), ('ST', -1.3, 1.4, .8), (10, 22), ('ST', 0, 1.45, .75)),
  (34, 84, 'S3', ('ST', -13, 3, 4), None, None, ('ST', 0, 1, 4)),
  (84, 180, 'S4', ('ST', .55, 1.75, -1.3), None, None, ('ST', 0, 1.4, 9)),
  (180, 220, 'S5', ('ST', 0, 5, 4.5), None, None, ('ST', 0, 0, 4.51)),
  (220, 276, 'S6', ('HR', .5, 1.6, -1.6), None, None, ('ST', 0, 1.2, 0)),
  (276, 340, 'S7', ('HR', .2, 1.45, 1.9), None, None, ('HR', 0, 1.45, 0)),
  (340, 380, 'S8', ('ST', .5, 1.5, 1.8), None, None, ('ST', 0, 1.45, 0)),
  (380, 500, 'S9', ('HR', -.3, 1.5, 1.5), None, None, ('HR', 0, 1.5, 0)),
  (500, 610, 'S10', ('HR', .1, 1.38, .95), None, None, ('HR', 0, 1.6, 0)),
  (610, 648, 'S11', ('ST', .3, 1.5, 2.0), None, None, ('ST', .3, 1.5, 2.9)),
  (648, 721, 'S13', ('ST', .4, 2.1, -4.2), None, None, ('ST', 0, 1.2, 4)),
 ],
 'repel': [
  (0, 26, 'R0-1', ('ST', -1.2, .9, .65), ('ST', -1.0, 1.0, .65), (4, 26), ('ST', 0, 1.55, .65)),
  (26, 52, 'R2-3', ('ST', 1.9, 1.5, -.4), None, None, ('ST', 0, 1.3, .8)),
  (52, 68, 'R4', ('ST', -2.2, 1.2, 2.4), None, None, ('ST', 0, 1.2, .8)),
  (68, 78, 'R5', ('ST', 0, 1.6, 3.6), None, None, ('ST', 0, 1.3, 1.4)),
  (78, 102, 'R6', ('ST', -2.8, .7, 1.8), None, None, ('ST', 0, 1.2, 2)),
  (102, 128, 'R7', ('ST', 1.6, 1.2, 4.6), None, None, ('ST', 0, .6, 2.6)),
  (128, 132, 'R8', ('ST', -2.4, .8, 2.6), None, None, ('ST', 0, .5, 2.8)),
  (132, 141, 'R9', ('ST', -5, 2.4, -2), None, None, ('ST', 0, 1, 4)),
 ],
 'ending': [
  (0, 50, 'E1', ('ST', -3.2, 1.3, 2.6), None, None, ('ST', 0, 1.1, 3)),
  (50, 94, 'E2', ('ST', 1.3, 1.5, 2.2), None, None, ('ST', 0, 1.5, 2.1)),
  (94, 118, 'E3a', ('ST', 1.2, .35, 1.2), None, None, ('ST', 0, 1, -.4)),
  (118, 150, 'E3b', ('ST', -1.8, .5, 3.6), None, None, ('ST', 0, 1.1, 1)),
  (150, 190, 'E4', ('ST', -14, 2.2, 5.5), None, None, ('ST', 0, 1, 5.5)),
  (190, 204, 'E5', ('ST', 1.4, 1.5, 3.3), None, None, ('ST', 0, 1.5, 3.25)),
  (204, 240, 'E6a', ('ST', -3.5, 3, 2.8), None, None, ('ST', 0, 6.3, 2.8)),
  (240, 276, 'E6b', ('ST', 2.6, 6.8, 5.6), None, None, ('ST', 0, 6.4, 2.6)),
  (276, 314, 'E6c', ('ST', -1.6, 6.2, .2), None, None, ('ST', 0, 6.5, 2.8)),
  (314, 338, 'E7', ('ST', -16, 3, 2), None, None, ('HR', 0, 1.6, 0)),
  (338, 378, 'E8', ('ST', -1, 5, -5), None, None, MOON),
  (378, 470, 'E9', ('ST', .8, 1.2, 4.6), None, None, ('HR', 0, 1.3, 0)),
  (470, 556, 'E10', ('HR', .2, 1.5, 1.3), None, None, ('HR', 0, 1.6, 0)),
  (556, 616, 'E11', ('ST', .4, 1.5, 1.7), None, None, ('ST', 0, 1.45, 0)),
  (616, 700, 'E12a', ('HR', .5, 1.4, 2.4), None, None, ('HR', 0, 1.35, 0)),
  (700, 846, 'E12b', ('ST', -.8, 1.5, 7.2), None, None, ('HR', 0, 1.4, 0)),
  (846, 882, 'E13', ('ST', -.4, 1.5, 1.6), None, None, ('ST', 0, 1.45, 0)),
  (882, 972, 'E14', ('ST', -2.2, 1.6, -2.6), None, None, ('ST', 1.2, 1.2, 9)),
  (972, 1072, 'E15', ('ST', .5, 1.6, 8), None, None, MOON),
  (1072, 1212, 'E16', ('ST', .6, 1.3, 2), None, None, ('HR', 0, 1.3, 0)),
  (1212, 1373, 'E17', ('HR', .15, 1.5, 1.15), None, None, ('HR', 0, 1.6, 0)),
 ],
}
# E12a: the camera is given in HR while the sequence turns her: it stays where it stood at the shot's first tick (a static camera)
STATIC_HR = {'E12a', 'I18', 'I19', 'E17', 'E10', 'S6', 'S7', 'S9', 'S10', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I11'}
# the actor stand-in's shift (r, u, f) per sequence: hr_design.md §4.2 (linear between the listed ticks)
ACTOR = {
 'intro': [(0, (0, 0, -6)), (20, (0, 0, -6)), (100, (0, 0, 0)), (1250, (0, 0, 0)), (1258, (0, 0, -.3)), (1390, (0, 0, -.3)), (1400, (0, 0, 0))],
 'cs1': [(0, (0, 0, 0)), (34, (0, 0, 0)), (44, (0, 0, -1.2)), (60, (0, 0, -1.2)), (80, (0, 0, 0)), (652, (0, 0, 0)), (664, (0, 0, -.5)), (694, (0, 0, -.5)), (716, (0, 0, 0))],
 'repel': [(0, (0, 0, 0)), (30, (0, 0, 0)), (36, (0, 0, .5)), (62, (0, 0, .5)), (68, (0, 0, 1.8)), (132, (0, 0, 1.8)), (139, (0, 0, 0))],
 'ending': [(0, (0, 0, 1.8)), (4, (0, 0, 1.8)), (16, (0, 0, .8)), (50, (0, 0, .8)), (54, (0, 0, 1.3)), (80, (0, 0, 1.3)), (90, (0, 0, -.6)), (94, (0, 0, -.6)),
            (104, (0, 0, -1.5)), (118, (0, 0, -1.5)), (124, (0, 0, 1.0)), (150, (0, 0, 1.0)), (188, (0, 0, 2.5)), (204, (0, 0, 2.5)), (216, (0, 6, 1.5)),
            (304, (0, 6, 1.5)), (330, (0, 0, 0))],
}
CONTACTS = {
 'cs1': [(10, 30, 'K1', (0, 1.45, .75))],
 'repel': [(0, 26, 'KR', (0, 1.55, .65)), (36, 48, 'KW', (.15, 1.95, .85)), (49, 49, 'KH', (0, 2.2, 1.1)), (70, 78, 'KS', (.2, 1.5, 1.6)), (88, 88, 'KT', (0, 2.95, 1.9)),
           (101, 101, 'KT', (0, .25, 3)), (129, 129, 'KK', (0, .35, 2.7))],
 'ending': [(52, 52, 'KG', (0, 2.05, 2.35)), (56, 80, 'KE2', (0, 1.5, 2.1)), (190, 204, 'KE5', (0, 1.5, 3.25)), (228, 228, 'KA1', (0, 6.9, 2.55)),
            (262, 262, 'KA2', (0, 7.3, 2.6)), (286, 286, 'KA3', (0, 6.8, 2.5)), (298, 304, 'KA4', (0, 6.9, 2.6))],
}
CLIP_OF = {'intro': lambda t: ('intro', t) if t < 1290 else ('intro_end', t - 1290), 'cs1': lambda t: ('cs1', t), 'repel': lambda t: ('repel', t),
           'ending': lambda t: ('ending', t)}


def lerp3(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


def actor_shift(seq, t):
    rows = ACTOR[seq]
    for (t0, p0), (t1, p1) in zip(rows, rows[1:]):
        if t0 <= t <= t1:
            return lerp3(p0, p1, (t - t0) / max(1, t1 - t0))
    return rows[-1][1] if t > rows[-1][0] else rows[0][1]


def world(st):                       # stage (r, u, f) -> render world
    return (-st[0], st[1], st[2])


def hr_point(root, p):               # HR(r, u, f) -> stage
    r, u, f = p
    a = math.radians(root[3])
    return (root[0] + r * math.cos(a) + f * math.sin(a), root[1] + u, root[2] - r * math.sin(a) + f * math.cos(a))


def resolve(spec, seq, t, roots, t_static=None):
    kind, a, b, c = spec
    if kind in ('ST', 'W'):
        return (a, b, c)
    if kind == 'HR':
        return hr_point(roots[t_static if t_static is not None else t], (a, b, c))
    sh = actor_shift(seq, t)
    if kind == 'ACT':                # ahead of the actor
        return (sh[0] + a, b, sh[2] + c)
    if kind == 'ACTR':               # beside the actor (same f)
        return (sh[0] + a, b, sh[2] + c)
    raise ValueError(kind)


def camera(seq, t, roots):
    for t0, t1, sid, e0, e1, mv, look in SHOTS[seq]:
        if t0 <= t < t1:
            ts = t0 if sid in STATIC_HR else None
            eye = resolve(e0, seq, t, roots, ts)
            if e1 is not None:
                u = min(1.0, max(0.0, (t - mv[0]) / max(1, mv[1] - mv[0])))
                eye = lerp3(eye, resolve(e1, seq, t, roots, ts), u)
            return sid, eye, resolve(look, seq, t, roots)
    raise ValueError(f'{seq} {t}: no shot')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dbg', required=True); ap.add_argument('--rp', required=True); ap.add_argument('--roots', required=True)
    ap.add_argument('--seq', required=True, choices=sorted(SHOTS)); ap.add_argument('--ticks'); ap.add_argument('--per', type=int, default=3)
    ap.add_argument('--range'); ap.add_argument('--cols', type=int, default=6); ap.add_argument('--width', type=int, default=1920)
    ap.add_argument('--actor', help='the real actor (lane H3): the character whose cine_dbg/spawn_<character> and cine_dbg/<clip>/<t> frames lie in the same debug dp (the actor builder\'s --cine-debug-dp, copied in); else the stand-in avatar'); ap.add_argument('--rp2', help='a second resource pack layered under --rp (the actor\'s models)')
    ap.add_argument('--no-actor', action='store_true'); ap.add_argument('--markers', action='store_true'); ap.add_argument('--fov', type=float, default=70.0)
    ap.add_argument('--ortho', help='instead of the shot camera: an orthographic view "az,el,extent" centred on her'); ap.add_argument('-o', '--out', required=True)
    a = ap.parse_args()
    roots = json.loads(Path(a.roots).read_text())[a.seq]
    L = len(roots) - 1
    if a.ticks:
        ticks = [int(x) for x in a.ticks.split(',')]
    else:
        lo, hi = (0, L) if not a.range else [int(x) for x in a.range.split('..')]
        ticks = []
        for t0, t1, *_ in SHOTS[a.seq]:
            t1 = min(t1, L + 1)
            if t1 <= lo or t0 > hi: continue
            n = a.per
            ticks += sorted({max(lo, min(hi, t0 + round((t1 - 1 - t0) * i / max(1, n - 1)))) for i in range(n)})
        ticks = sorted(set(ticks))
    dbg = Path(a.dbg)
    av = (dbg / 'data/rlk/function/hr_dbg/avatar.mcfunction').read_text().splitlines()
    seat = (dbg / 'data/rlk/function/hr_dbg/seat.mcfunction').read_text().splitlines()
    fdir = dbg / 'data/rlk/function/hr_shot'; fdir.mkdir(parents=True, exist_ok=True)
    pw = a.width // a.cols; ph = int(pw * 9 / 16)
    panels = []
    with tempfile.TemporaryDirectory() as td:
        for i, t in enumerate(ticks):
            clip, ct = CLIP_OF[a.seq](t)
            root = roots[t]
            hw = world(root[:3])
            # her parts to her root with her yaw (the debug frames only set the transformations; yaw 0 faces +Z = +f)
            lines = [f'tp @e[tag=rlk_hr_part] {hw[0]:.3f} {hw[1]:.3f} {hw[2]:.3f} {root[3]:.2f} 0']
            if a.actor and not a.no_actor:
                ACLIP = {'intro': 'cs0', 'cs1': 'cs1', 'repel': 'repel', 'ending': 'ending'}[a.seq]
                lines += [f'function rlk:cine_dbg/spawn_{a.actor}', f'function rlk:cine_dbg/{ACLIP}/{t}']
            elif not a.no_actor:
                sh = actor_shift(a.seq, t); w = world(sh)
                lines += [l.replace('~1.4 ~ ~', f'{w[0]:.3f} {w[1]:.3f} {w[2]:.3f}') for l in av]
            if a.seq == 'intro' and t < 1052:
                sw = world((0, 0, 20.73))
                # the seat stone stands where she sat (its long side across the stage axis); drawn turned as she sat (yaw 0)
                lines += [l.replace('~ ~ ~', f'{sw[0]:.3f} {sw[1]:.3f} {sw[2]:.3f}') for l in seat if 'tuff' in l]
            (fdir / f'p{i}.mcfunction').write_text('\n'.join(lines) + '\n')
            out = Path(td) / f'p{i}.png'
            cmd = [sys.executable, '-I', str(SIM / 'az/understand/rigtech_render.py'), '--dp', str(dbg), '--rp', a.rp, '--spawn', 'rlk:boss/scarlet/rig/spawn',
                   '--apply', f'rlk:hr_dbg/{clip}/{ct}', f'rlk:hr_shot/p{i}', '--origin', '0', '0', '0', '--yaw', f'{root[3]:.2f}',
                   '--light', 'mc', '-q', '--width', str(pw * 2), '--no-grid', '--floor', '70,40,48', '--floor-half', '30', '-o', str(out)]
            if a.rp2: cmd += ['--rp', a.rp2]
            if a.ortho:
                az, el, ext = a.ortho.split(',')
                cmd += ['--views', f'az:{az},{el}', '--extent', ext, '--center', f'{hw[0]:.3f}', f'{hw[1] + 1.1:.3f}', f'{hw[2]:.3f}', '--aspect', '0.5625']
                sid = 'ortho'
            else:
                sid, eye, look = camera(a.seq, t, roots)
                e, l = world(eye), world(look)
                dx, dy, dz = l[0] - e[0], l[1] - e[1], l[2] - e[2]
                yaw = math.degrees(math.atan2(-dx, dz)); pitch = -math.degrees(math.atan2(dy, math.hypot(dx, dz)))
                cmd += ['--views', 'camera', '--camera', f'{e[0]:.3f}', f'{e[1]:.3f}', f'{e[2]:.3f}', f'{yaw:.2f}', f'{pitch:.2f}', '--fov', str(a.fov), '--aspect', '0.5625']
            if a.markers:
                for t0, t1, kid, p in CONTACTS.get(a.seq, []):
                    if t0 - 2 <= t <= t1 + 2:
                        w = world(p); cmd += [f'--marker={w[0]:.3f},{w[1]:.3f},{w[2]:.3f},{kid}']
            r = subprocess.run(cmd, capture_output=True, text=True)
            if not out.exists():
                print(r.stdout[-2000:], r.stderr[-2000:]); raise SystemExit(f'render failed at {t}')
            im = Image.open(out).convert('RGB')
            # crop the renderer's title rows (the panel is the bottom pw*2 x ph*2 block)
            W, H = im.size
            im = im.crop((0, H - int(W * 9 / 16), W, H)).resize((pw, ph), Image.LANCZOS)
            d = ImageDraw.Draw(im)
            d.rectangle((0, 0, pw, 13), fill=(0, 0, 0)); d.text((3, 1), f'{a.seq} #{t} {sid} [{clip} {ct}]', fill=(255, 235, 120))
            panels.append(im)
    rows = (len(panels) + a.cols - 1) // a.cols
    sheet = Image.new('RGB', (pw * a.cols, ph * rows), (16, 16, 20))
    for i, im in enumerate(panels):
        sheet.paste(im, ((i % a.cols) * pw, (i // a.cols) * ph))
    sheet.save(a.out, quality=88)
    print(a.out, len(panels), 'panels')


if __name__ == '__main__':
    main()
