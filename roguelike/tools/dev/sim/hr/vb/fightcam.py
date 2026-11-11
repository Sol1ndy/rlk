#!/usr/bin/env python3
"""fightcam.py — 홍련's attacks as the player sees them: frame strips from the real fight camera (round V, lane VB).

The fight is played in F5 (README §13): the vanilla third-person camera rides a seat 0.5 b over the avatar's head, 3.5 b
behind it along the view (view/ride_set default d 3.5, s 1.0; FOV 70). With the player aiming at her chest from D blocks:
the pivot (0, 2.3, 0) over the avatar at the origin, the lens 3.5 b behind it on the line to her chest (D 7: 3.40 b behind,
3.13 b up, looking 13.6 deg down). 1080p: focal 771 px, 1 b at 10 b = 77 px.

Her figure is her rig as built (the rig builder's --debug-dp frames hr_dbg/<clip>/<t>; the blade look `edge` as in the
fight), the avatar is the pack's own (hr_dbg/avatar: Skirk's idle), the path / head / slash cards are the commands
tools/mboss_scarlet/blade.py generates (the same lines the patterns run), all drawn by the pack's item models through
tools/dev/sim/preview/raiden_preview.py (a z-buffer rasteriser). Fields: p1 = the moon field (grey-violet, pale straw grass
tufts), p2 = the crimson field.

  python3 -I fightcam.py <roguelike> --dbg <debug dp> --rp <rp> strip --clip a3 --event h1 [--dist 7] [--field p1]
          [--from T --to T] [--no-fx] [--w 480] -o out.jpg
  python3 -I fightcam.py <roguelike> --dbg <debug dp> --rp <rp> measure [--clips a,b] [--json out.json]
      per hit of api.HITS (+ the gauntlet cuts): at 4 / 7 / 10 b on both fields the wind-up pose against idle (silhouette
      pixels that differ), the blade's and the path's width in px, the cue star's / the flash's visible share
"""
import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
SIM = HERE.parent.parent
spec = importlib.util.spec_from_file_location('preview', SIM / 'preview/raiden_preview.py')
PV = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PV)
PV.LOG.quiet = True

# the UUID-addressed rig parts (the same patch as az/understand/rigtech_render.py)
import re  # noqa: E402
_UUID = re.compile(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')
_sel0 = PV.Scene.select


def _uuid_ints(u):
    h = u.replace('-', '')
    out = []
    for i in range(4):
        v = int(h[8 * i:8 * i + 8], 16)
        out.append(v - (1 << 32) if v >= (1 << 31) else v)
    return out


def _select(self, sel, ctx):
    if _UUID.fullmatch(sel):
        want = _uuid_ints(sel)
        return [e for e in self.entities if e.alive and [int(x) for x in (e.nbt.get('UUID') or [])] == want]
    return _sel0(self, sel, ctx)


PV.Scene.select = _select

FOV, CAM_D, PIVOT_Y, CHEST_Y = 70.0, 3.5, 2.3, 1.2
FIELD = {'p1': dict(floor='96,84,92', bg_top=(34, 26, 48), bg_bottom=(70, 58, 80), grass=(214, 196, 146)),
         'p2': dict(floor='112,26,34', bg_top=(60, 12, 20), bg_bottom=(120, 30, 40), grass=(150, 30, 40))}
HAT = (236, 233, 244)


def camera(dist):
    """(pos, yaw, pitch) of the F5 lens for a player at the origin aiming at her chest `dist` b ahead (+z)."""
    pitch = math.atan2(PIVOT_Y - CHEST_Y, dist)
    return (0.0, PIVOT_Y + CAM_D * math.sin(pitch), -CAM_D * math.cos(pitch)), 0.0, math.degrees(pitch)


class Stage:
    def __init__(self, wt, dbg, rp):
        self.wt, self.dbg = Path(wt).resolve(), Path(dbg).resolve()
        self.assets = PV.Assets([str(rp)])
        sys.path.insert(0, str(self.wt / 'tools'))
        sys.dont_write_bytecode = True
        from mboss_scarlet import api, blade
        self.api, self.blade = api, blade

    def frame(self, clip, ct, dist, field, cards=(), her=True, avatar=True, look='edge', her_pos=None, her_yaw=180.0, w=480,
              ghost=False):
        """One rendered frame (H x W x 3 floats, the z image): her clip tick ct, `dist` b before the avatar."""
        sc = PV.Scene(self.dbg, (0, 0, 0), scores={}, macros={}, max_depth=4, follow=True)
        hp = her_pos or (0.0, 0.0, float(dist))
        if her:
            c = PV.Ctx(hp, her_yaw, 0.0)
            sc.run_file('rlk:boss/scarlet/rig/spawn', c)
            sc.run_file(f'rlk:hr_dbg/{clip}/{ct}', c)
            sc.command(f'tp @e[tag=rlk_hr_part] {hp[0]:.3f} {hp[1]:.3f} {hp[2]:.3f} {her_yaw:.2f} 0', c, 0)
            for e in sc.entities:
                if 'rlk_hr_sword_glow' in e.tags and look:
                    e.nbt.setdefault('item', {}).setdefault('components', {})['minecraft:item_model'] = f'rlk:mboss/scarlet/glow_{look}'
        if avatar:
            sc.run_file('rlk:hr_dbg/avatar', PV.Ctx((-1.4, 0, 0), 0.0, 0.0))
        sc.entities += list(cards)
        geo = PV.Geometry(sc, self.assets)
        # the cards' tint (custom_model_data colors[0]; the rasteriser knows no item tints) and their full brightness: a card
        # (brightness 15, shade false) is drawn unlit, her rig and the avatar under the vanilla entity light
        self.lit = []
        for i, (e, baked, tints, M, name) in enumerate(geo.items):
            cmd = (e.nbt.get('item') or {}).get('components', {}).get('minecraft:custom_model_data')
            if cmd and cmd.get('colors'):
                c = int(cmd['colors'][0])
                geo.items[i] = (e, baked, [np.array([(c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255])] * max(1, len(tints)), M, name)
        pos, yaw, pitch = camera(dist)
        view = PV.View('camera', yaw, pitch, True, pos, FOV)
        F = FIELD[field]
        opts = SimpleNamespace(alpha_scale=1.0, bg_top=F['bg_top'], bg_bottom=F['bg_bottom'], flat=False, light='mc', floor=F['floor'],
                               floor_half=30.0, translucent=True, tex_mode='uv')
        h = round(w * 9 / 16)
        img, z = PV.render_view(geo, view, w, h, opts, self.assets)
        return img, z, view

    def cards_of(self, cmds, ticks, her_pos, her_yaw=180.0):
        """The sweep cards alive after each pattern tick: {tick: [entities]} (cmds: {tick: [command]}, run at her feet)."""
        sc = PV.Scene(self.dbg, (0, 0, 0), scores={}, macros={}, max_depth=2, follow=False)
        out = {}
        for t in range(0, max(ticks) + 1):
            c = PV.Ctx(her_pos, her_yaw, 0.0)
            for line in cmds.get(t, []):
                sc.command(line, c, 0)
            if t in ticks:
                import copy
                out[t] = [copy.deepcopy(e) for e in sc.entities if e.alive]
        return out


def label(img, txt, w):
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, 13), fill=(0, 0, 0))
    d.text((3, 1), txt, fill=(255, 235, 120))
    return im


def sheet(panels, cols, out):
    w, h = panels[0].size
    rows = (len(panels) + cols - 1) // cols
    sh = Image.new('RGB', (w * cols, h * rows), (16, 16, 20))
    for i, im in enumerate(panels):
        sh.paste(im, ((i % cols) * w, (i // cols) * h))
    sh.save(out, quality=88)
    print(out, len(panels), 'panels')


def hit_cmds(st, clip, event, col=None, lead=None):
    """The path + slash commands of one hit as a melee swing riding her (pattern tick = clip tick)."""
    B = st.blade
    sw = B.swing_of(clip, event)
    out = B.Out()
    lead = lead or B.SHOW_FIRST
    B.path_ride(out, 'x', sw, 0, sw.h - lead, col or B.COL['P'], 'a')
    B.slash(out, 'x', sw, 0, B.SLASH[st.api.C_LILAC], 'a')
    return sw, out.t


def cmd_strip(st, a):
    api = st.api
    sw, cmds = hit_cmds(st, a.clip, a.event) if not a.no_fx else (st.blade.swing_of(a.clip, a.event), {})
    t0 = a.t0 if a.t0 is not None else max(0, sw.h - 13)
    t1 = a.t1 if a.t1 is not None else min(sw.n, sw.h + 5)
    ticks = list(range(t0, t1 + 1))
    hp = (0.0, 0.0, float(a.dist))
    cards = st.cards_of(cmds, ticks, hp)
    panels = []
    for t in ticks:
        if a.crop:
            x0, y0, x1, y1 = (int(v) for v in a.crop.split(','))
            img, _z, _v = st.frame(a.clip, t, a.dist, a.field, cards.get(t, ()), w=1920)
            img = img[y0:y1, x0:x1]
        else:
            img, _z, _v = st.frame(a.clip, t, a.dist, a.field, cards.get(t, ()), w=a.w)
        mark = ' HIT' if t == sw.h else ' swing' if sw.a < t <= sw.b else ' wound' if sw.w <= t <= sw.a else ''
        panels.append(label(img, f'{a.clip} {a.event} t{t}{mark} D{a.dist:g} {a.field}', img.shape[1]))
    sheet(panels, a.cols, a.out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('wt')
    ap.add_argument('--dbg', required=True)
    ap.add_argument('--rp', required=True)
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('strip')
    s.add_argument('--clip', required=True)
    s.add_argument('--event', required=True)
    s.add_argument('--dist', type=float, default=7.0)
    s.add_argument('--field', default='p1', choices=list(FIELD))
    s.add_argument('--from', dest='t0', type=int)
    s.add_argument('--to', dest='t1', type=int)
    s.add_argument('--no-fx', action='store_true')
    s.add_argument('--w', type=int, default=480)
    s.add_argument('--crop', help='x0,y0,x1,y1 in 1920 x 1080 px: render at 1080p and cut this window (detail strips)')
    s.add_argument('--cols', type=int, default=6)
    s.add_argument('-o', '--out', required=True)
    a = ap.parse_args()
    st = Stage(a.wt, a.dbg, a.rp)
    if a.cmd == 'strip':
        cmd_strip(st, a)


if __name__ == '__main__':
    main()
