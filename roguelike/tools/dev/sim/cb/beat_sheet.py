#!/usr/bin/env python3
"""beat_sheet.py: rendered sheets of the avatar's perfect-parry / perfect-dodge clips (round V, lane VP), every tick.

Run from a copy of tools/dev/sim outside the datapack (sim README 1). It drives the offline rasteriser
(preview/raiden_preview.py) panel by panel: one panel = one tick of a clip from the builder's debug datapack
(`node tools/build_player_rig.mjs ... --beat-debug-dp <dbg>` writes beat_dbg/spawn_<char>[_i][_glow] and
beat_dbg/<char>/<clip>/<t>; <dbg>/rp holds the stand-in sword of the mannequin characters), framed on the avatar's feet with
the floor grid and a forward mark (orange: where the attacker stands).

  python3 -I beat_sheet.py --dbg <dbg dp> --rp <rp> --char arle --clip pparry [--ticks 0..16] [--glow]
      [--view right|back|front|left|iso|az:A,E] [--extent 1.6] [--cols 9] [--width 1800] -o out.jpg

--char: arle skirk navia (add _i via --clip pparry_i / pdodge_i) lumine clorinde ronova nefer. --view as the rasteriser:
right = seen from the avatar's right side (forward is screen right), back = from behind (the fight camera's side).
--view takes a comma list of two views for two rows per clip (e.g. right,back).
"""
import argparse
import importlib.util
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


def ticks_of(s):
    out = []
    for part in s.split(','):
        m = re.fullmatch(r'(\d+)\.\.(\d+)(?::(\d+))?', part)
        if m:
            out += list(range(int(m.group(1)), int(m.group(2)) + 1, int(m.group(3) or 1)))
        else:
            out.append(int(part))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dbg', required=True)
    ap.add_argument('--rp', required=True)
    ap.add_argument('--char', required=True)
    ap.add_argument('--clip', required=True)
    ap.add_argument('--ticks', default=None)
    ap.add_argument('--glow', action='store_true')
    ap.add_argument('--view', default='right,back')
    ap.add_argument('--extent', type=float, default=1.6)
    ap.add_argument('--cols', type=int, default=9)
    ap.add_argument('--width', type=int, default=1800)
    ap.add_argument('-o', '--out', required=True)
    a = ap.parse_args()
    dbg = Path(a.dbg)
    cdir = dbg / 'data/rlk/function/beat_dbg' / a.char / a.clip
    n = len(list(cdir.glob('*.mcfunction')))
    ticks = ticks_of(a.ticks) if a.ticks else list(range(n))
    assets = PV.Assets([a.rp, str(dbg / 'rp')], None)
    opts = SimpleNamespace(floor=None, floor_half=40.0, bg_top=(36, 38, 48), bg_bottom=(58, 60, 72), tex_mode='uv', translucent=True, flat=False,
                           light='mc', alpha_cutout=0.1, blend='mc', alpha_scale=1.0)
    views = a.view.split(',') if not a.view.startswith('az:') else [a.view]
    cols = min(a.cols, len(ticks))
    pw = a.width // cols
    ph = int(pw * 1.25)
    ss = 2
    rows = math.ceil(len(ticks) / cols)
    sheet = Image.new('RGB', (pw * cols, (ph * rows) * len(views) + 18), (20, 20, 26))
    font = PV.load_font(11)
    suf = ('_i' if a.clip.endswith('_i') else '') + ('_glow' if a.glow else '')
    ImageDraw.Draw(sheet).text((4, 3), f'beat {a.char}/{a.clip} ({n - 1} t) · views {a.view} · extent {a.extent:g} b · orange = forward (the attacker)', fill=(230, 230, 235), font=font)
    for vi, vname in enumerate(views):
        for k, t in enumerate(ticks):
            sc = PV.Scene(dbg, (0, 0, 0), scores={}, macros={}, max_depth=4, follow=True)
            ctx = PV.Ctx((0, 0, 0), 0.0, 0.0)
            sc.run_file(f'rlk:beat_dbg/spawn_{a.char}{suf}', ctx)
            sc.run_file(f'rlk:beat_dbg/{a.char}/{a.clip}/{t}', ctx)
            geo = PV.Geometry(sc, assets, hide=(), only=(), translucent=True)
            view = PV.make_views([vname], 0.0)[0]
            view.scale = min(pw, ph) * ss / (2 * a.extent)
            view.center = view.cam(np.array([0, 1.05, 0], float))[:2]
            lines = []
            for v in np.arange(-4, 4 + 1e-9, 1):
                col = (92, 96, 110) if abs(v) > 1e-9 else (140, 146, 160)
                lines.append(([[v, 0, -4], [v, 0, 4]], col, 1, None))
                lines.append(([[-4, 0, v], [4, 0, v]], col, 1, None))
            lines.append(([[0, 0.01, 0], [0, 0.01, 1.0]], (255, 170, 40), 3, (140, 95, 30)))
            img, _z = PV.render_view(geo, view, pw * ss, ph * ss, opts, assets, lines)
            pim = Image.fromarray((img * 255).astype(np.uint8)).resize((pw, ph), Image.LANCZOS)
            d = ImageDraw.Draw(pim)
            d.rectangle([0, 0, 60, 13], fill=(0, 0, 0))
            d.text((3, 0), f't={t} {vname[:5]}', fill=(255, 255, 255), font=font)
            sheet.paste(pim, ((k % cols) * pw, 18 + vi * ph * rows + (k // cols) * ph))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=88) if out.suffix.lower() in ('.jpg', '.jpeg') else sheet.save(out)
    print(f'wrote {out} ({sheet.size[0]}x{sheet.size[1]}, {len(ticks)} ticks x {len(views)} views)')


if __name__ == '__main__':
    main()
