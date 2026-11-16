#!/usr/bin/env python3
"""actor_sheet.py: rendered sheets of the cutscene actor's clips (lane H3; hr_design.md §4.2), for looking at them.

Run from a copy of tools/dev/sim outside the datapack (sim README 1). It drives the offline rasteriser
(preview/raiden_preview.py) panel by panel: every panel is one tick of a clip from the builder's debug datapack
(`node tools/build_player_rig.mjs ... --cine-debug-dp <dbg>` writes cine_dbg/<clip>/<t> and cine_dbg/spawn_<character>),
framed on the actor's root of that tick (the manifest's shift), with the stage origin, the floor grid, the clip's contact
points (yellow crosses while their ticks run) and a 2-block post where the shot table puts her (the clip's `her` marks:
a rough stand-in for the distance only, magenta).

  python3 -I actor_sheet.py --dbg <dbg dp> --rp <rp> --man <roguelike>/tools/player_motion/cine/manifest.json \
      --clip repel --ticks 0..140:4 [--char skirk] [--view right|front|back|left|top|iso|az:A,E] [--extent 1.7]
      [--cols 8] [--width 1600] [--no-follow] [--center r,u,f] -o out.jpg

--ticks takes a..b[:step] and comma lists (0..40:4,49,56,62). Views as the rasteriser: right = seen from the actor's right
side (forward is screen right), front = looking at its face. --no-follow keeps the frame on --center (stage coordinates).
"""
import argparse
import importlib.util
import json
import math
import re
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('preview', HERE.parent / 'preview' / 'raiden_preview.py')
PV = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PV)
UUID = re.compile(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')
_sel0 = PV.Scene.select


def _select(self, sel, ctx):
    if UUID.fullmatch(sel):
        h = sel.replace('-', '')
        want = [int(h[8 * i:8 * i + 8], 16) for i in range(4)]
        want = [v - (1 << 32) if v >= (1 << 31) else v for v in want]
        return [e for e in self.entities if e.alive and [int(x) for x in (e.nbt.get('UUID') or [])] == want]
    return _sel0(self, sel, ctx)


PV.Scene.select = _select


def ticks_of(s):
    out = []
    for part in s.split(','):
        m = re.fullmatch(r'(\d+)\.\.(\d+)(?::(\d+))?', part)
        if m:
            out += list(range(int(m.group(1)), int(m.group(2)) + 1, int(m.group(3) or 1)))
        else:
            out.append(int(part))
    return out


def W(p):
    """stage (r, u, f) -> the renderer's world (the actor at the origin, yaw 0 = +Z): (-r, u, f)"""
    return [-p[0], p[1], p[2]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dbg', required=True)
    ap.add_argument('--rp', required=True)
    ap.add_argument('--man', required=True)
    ap.add_argument('--clip', required=True)
    ap.add_argument('--ticks', required=True)
    ap.add_argument('--char', default='skirk')
    ap.add_argument('--view', default='right')
    ap.add_argument('--extent', type=float, default=1.7)
    ap.add_argument('--cols', type=int, default=8)
    ap.add_argument('--width', type=int, default=1600)
    ap.add_argument('--no-follow', action='store_true')
    ap.add_argument('--center', default=None)
    ap.add_argument('--aspect', type=float, default=1.0)
    ap.add_argument('-o', '--out', required=True)
    a = ap.parse_args()
    man = json.loads(Path(a.man).read_text(encoding='utf8'))
    clip = man['clips'][a.clip]
    ticks = [t for t in ticks_of(a.ticks) if 0 <= t <= clip['len']]
    assets = PV.Assets([a.rp], None)
    opts = SimpleNamespace(floor=None, floor_half=40.0, bg_top=(36, 38, 48), bg_bottom=(58, 60, 72), tex_mode='uv', translucent=True, flat=False,
                           light='mc', alpha_cutout=0.1, blend='mc', alpha_scale=1.0)
    cols = min(a.cols, len(ticks))
    pw = a.width // cols
    ph = int(pw * a.aspect)
    ss = 2
    rows = math.ceil(len(ticks) / cols)
    sheet = Image.new('RGB', (pw * cols, ph * rows + 18), (20, 20, 26))
    font = PV.load_font(11)
    ImageDraw.Draw(sheet).text((4, 3), f'actor {a.clip} ({clip["len"]} t) · {a.char} · view {a.view} · extent {a.extent:g} b' + ('' if a.no_follow else ' · framed on the root'), fill=(230, 230, 235), font=font)
    her = clip.get('her') or []
    contacts = {k: c for k, c in man['contact'].items() if c['clip'] == a.clip}
    for k, t in enumerate(ticks):
        sc = PV.Scene(Path(a.dbg), (0, 0, 0), scores={}, macros={}, max_depth=4, follow=True)
        ctx = PV.Ctx((0, 0, 0), 0.0, 0.0)
        sc.run_file(f'rlk:cine_dbg/spawn_{a.char}', ctx)
        sc.run_file(f'rlk:cine_dbg/{a.clip}/{t}', ctx)
        geo = PV.Geometry(sc, assets, hide=(), only=(), translucent=True)
        view = PV.make_views([a.view], 0.0)[0]
        shift = clip['tick']['shift'][t]
        c = [float(x) for x in a.center.split(',')] if a.center else [0, 1.0, 0]
        if not a.no_follow:
            c = [shift[0] + c[0], shift[1] + c[1], shift[2] + c[2]]
        view.scale = min(pw, ph) * ss / (2 * a.extent)
        view.center = view.cam(np.array(W(c), float))[:2]
        lines = []
        g = np.arange(-8, 8 + 1e-9, 1)
        for v in g:
            col = (92, 96, 110) if abs(v) > 1e-9 else (140, 146, 160)
            lines.append(([[v, 0, -8], [v, 0, 8]], col, 1, None))
            lines.append(([[-8, 0, v], [8, 0, v]], col, 1, None))
        lines.append(([[0, 0.01, 0], [0, 0.01, 1.0]], (255, 170, 40), 3, (140, 95, 30)))
        for name, cc in contacts.items():
            if cc['ticks'][0] - 2 <= t <= cc['ticks'][-1] + 2:
                p = W(cc['p'])
                for d in ([.12, 0, 0], [0, .12, 0], [0, 0, .12]):
                    lines.append(([[p[i] - d[i] for i in range(3)], [p[i] + d[i] for i in range(3)]], (255, 235, 60), 2, (255, 235, 60)))
        for i in range(len(her) - 1, -1, -1):
            if her[i][0] <= t:
                t0, p0 = her[i]
                p = p0
                if i + 1 < len(her):
                    t1, p1 = her[i + 1]
                    u = (t - t0) / (t1 - t0)
                    p = [p0[j] + (p1[j] - p0[j]) * u for j in range(3)]
                b, top = W(p), W([p[0], p[1] + 2.0, p[2]])
                lines.append(([b, top], (255, 80, 220), 3, (150, 50, 130)))
                lines.append(([[top[0] - .25, top[1], top[2]], [top[0] + .25, top[1], top[2]]], (255, 80, 220), 3, (150, 50, 130)))
                break
        img, _z = PV.render_view(geo, view, pw * ss, ph * ss, opts, assets, lines)
        pim = Image.fromarray((img * 255).astype(np.uint8)).resize((pw, ph), Image.LANCZOS)
        d = ImageDraw.Draw(pim)
        d.rectangle([0, 0, 118, 13], fill=(0, 0, 0))
        d.text((3, 0), f't={t} [{shift[0]:g},{shift[1]:g},{shift[2]:g}]', fill=(255, 255, 255), font=font)
        sheet.paste(pim, ((k % cols) * pw, 18 + (k // cols) * ph))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() in ('.jpg', '.jpeg'):
        sheet.save(out, quality=88)
    else:
        sheet.save(out)
    print(f'wrote {out} ({sheet.size[0]}x{sheet.size[1]}, {len(ticks)} panels)')


if __name__ == '__main__':
    main()
