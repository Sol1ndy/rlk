#!/usr/bin/env python3
"""fightcam.py — 홍련's attacks as the player sees them: frame strips from the real fight camera (round V, lane VB; round W,
lane WB: the blade's trail instead of round V's drawn path, FOV 90 by default - the user plays at 90 - and the `trail` measure).

The fight is played in F5 (README §13): the vanilla third-person camera rides a seat 0.5 b over the avatar's head, 3.5 b
behind it along the view (view/ride_set default d 3.5, s 1.0; FOV 70). With the player aiming at her chest from D blocks:
the pivot (0, 2.3, 0) over the avatar at the origin, the lens 3.5 b behind it on the line to her chest (D 7: 3.40 b behind,
3.13 b up, looking 13.6 deg down). 1080p: focal 771 px, 1 b at 10 b = 77 px.

Her figure is her rig as built (the rig builder's --debug-dp frames hr_dbg/<clip>/<t>; the blade look `edge` as in the
fight), the avatar is the pack's own (hr_dbg/avatar: Skirk's idle), the trail cards are the commands
tools/mboss_scarlet/blade.py generates (the same lines the patterns run), all drawn by the pack's item models through
tools/dev/sim/preview/raiden_preview.py (a z-buffer rasteriser). Fields: p1 = the moon field (grey-violet, pale straw grass
tufts), p2 = the crimson field.

  python3 -I fightcam.py <roguelike> --dbg <debug dp> --rp <rp> strip --clip a3 --event h1 [--dist 7] [--field p1]
          [--from T --to T] [--no-fx] [--w 480] -o out.jpg
  python3 -I fightcam.py <roguelike> --dbg <debug dp> --rp <rp> measure [--clips a,b] [--json out.json]
      per hit of api.HITS (+ the gauntlet cuts): at 4 / 7 / 10 b on both fields the wind-up pose against idle (silhouette
      pixels that differ), the blade's width in px, the cue star's / the flash's visible share
  python3 -I fightcam.py <roguelike> --dbg <debug dp> --rp <rp> trail [--clips a,b] [--json out.json]
      round W: per hit, at 4 / 7 / 10 b, on both fields, at the instants of the wind-up's hold, the swing and the hit: the trail's
      pixels (the band on the blade, the pieces), the band's width in px (its area / its length on screen), the swing's bright
      ribbon width in px, the luminance contrast of the trail against the field / her behind it
  (the frame of pattern tick t: her rig at clip tick t, the trail cards as the commands of the ticks before t left them - the
  state the client shows at that instant: a card sent on tick t - 1 arrives there on t)
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
_floor0 = PV.floor_quad


def _floor(assets, opts, view=None):
    """(the preview caches its one floor texture by name: a name per colour, so the fields really differ)"""
    V, UV, T_, TI, SG = _floor0(assets, opts, view)
    key = 'rlk:__floor_' + opts.floor.replace(',', '_') + '__'
    PV.SPECIAL_TEXTURES[key] = (*(int(v) for v in opts.floor.split(',')), 255)
    return V, UV, np.full(len(T_), assets.texture(key)), TI, SG


PV.floor_quad = _floor

FOV, CAM_D, PIVOT_Y, CHEST_Y = 90.0, 3.5, 2.3, 1.2          # round W: FOV 90 (the user's)
FLOOR_Y = 201.0                     # the hr_field arena floor (api.CY)
FIELD = {'p1': dict(floor='96,84,92', bg_top=(34, 26, 48), bg_bottom=(70, 58, 80), grass=(214, 196, 146)),
         # round W (review w T3-08): the P1 field where her trail stands over the pale straw wheat (the worst case for a pale trail)
         'p1w': dict(floor='214,196,146', bg_top=(34, 26, 48), bg_bottom=(70, 58, 80), grass=(214, 196, 146)),
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
        img, z = render_lit(geo, view, w, h, opts, self.assets)
        return img, z, view

    def cards_of(self, cmds, ticks, her_pos, her_yaw=180.0):
        """The trail cards as the client shows them at the instant of each pattern tick: {tick: [entities]} (cmds: {tick:
        [command]}, run at her feet): the commands of the ticks before it (a card sent on t - 1 arrives on t)."""
        import copy
        sc = PV.Scene(self.dbg, (0, 0, 0), scores={}, macros={}, max_depth=2, follow=False)
        out = {}
        for t in range(0, max(ticks) + 1):
            if t in ticks:
                out[t] = [copy.deepcopy(e) for e in sc.entities if e.alive]
            c = PV.Ctx(her_pos, her_yaw, 0.0)
            for line in cmds.get(t, []):
                sc.command(line, c, 0)
            # (the fight hook's ride: the riding cards to her model, her yaw - a summon takes no rotation)
            sc.command(f'tp @e[tag=rlk_hr_trr] {her_pos[0]} {her_pos[1]} {her_pos[2]} {her_yaw} 0', c, 0)
        return out


def render_lit(geo, view, w, h, opts, assets):
    """The frame with the trail's cards (rlk_hr_tr: brightness 15, shade false) drawn unlit and everything else under the vanilla
    entity light (the rasteriser lights every quad alike): the lit frame, with the pixels the cards change taken from a flat one."""
    import copy
    img, z = PV.render_view(geo, view, w, h, opts, assets)
    if not any('rlk_hr_tr' in e.tags for e, *_r in geo.items):
        return img, z
    fl = SimpleNamespace(**{**vars(opts), 'light': 'flat'})
    flat = PV.render_view(geo, view, w, h, fl, assets)[0]
    g2 = copy.copy(geo)
    g2.items = [x for x in geo.items if 'rlk_hr_tr' not in x[0].tags]
    bare = PV.render_view(g2, view, w, h, fl, assets)[0]
    m = np.abs(flat - bare).max(axis=2) > 0.004
    return np.where(m[..., None], flat, img), z


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
    """The trail commands of one hit (round W: the band and the pieces of blade.trail, the clip played at pattern tick 0, its
    hit's colours), her standing still (pattern tick = clip tick)."""
    B = st.blade
    sw = B.swing_of(clip, event)
    sh = B.Shown([(0, clip)], last=sw.b + 1)
    t0 = next(t for t in range(0, sw.b + 1) if sh.known(t))
    col = col or B.COL['P']
    out = B.Out()
    B.trail(out, 'x', 'a', sh, t0, sw.b, lambda t: col, lambda t: sw.a <= t and t + 1 <= sw.b)
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
    look = None if a.look == 'none' else a.look
    tr = st.blade.track(a.clip) if not a.no_fx or a.tells else None
    for t in ticks:
        cs = list(cards.get(t, ()))
        if a.tells and a.flash is None and sw.h - api.CUE_LEAD <= t < sw.h:
            cs.append(_card('rlk:mboss/hr_kit/cue_0', her_point(st.blade.cue_point(a.clip, sw.h - api.CUE_LEAD), a.dist), 1.9 + 0.4 * (t - sw.h + api.CUE_LEAD) / 6))
        if a.tells and a.flash is not None and a.flash <= t < a.flash + 8:
            cs.append(_card('rlk:mboss/hr_kit/yellow_tell_0', her_point(tr['h'][t], a.dist), 2.4))
            cs.append(_card('rlk:mboss/hr_kit/sw_head', her_point(tr['h'][t], a.dist), 1.3, 0xFFE14A, idx=8001))
        if a.crop:
            x0, y0, x1, y1 = (int(v) for v in a.crop.split(','))
            img, _z, _v = st.frame(a.clip, t, a.dist, a.field, cs, w=1920, look=look)
            img = img[y0:y1, x0:x1]
        else:
            img, _z, _v = st.frame(a.clip, t, a.dist, a.field, cs, w=a.w, look=look)
        mark = ' HIT' if t == sw.h else ' swing' if sw.a < t <= sw.b else ' wound' if sw.w <= t <= sw.a else ''
        panels.append(label(img, f'{a.clip} {a.event} t{t}{mark} D{a.dist:g} {a.field}', img.shape[1]))
    sheet(panels, a.cols, a.out)


# ----------------------------------------------------------------------------- measure: readability on the rendered pixels
def _mask(a, b, thr=0.06):
    return np.abs(a - b).max(axis=2) > thr


def _card(model, pos, scale, col=0xFFFFFF, bb='center', idx=8000):
    return PV.Entity('item_display', pos, 0.0, 0.0, {
        'Tags': ['m_card'], 'billboard': bb, 'item': {'components': {'minecraft:item_model': model, 'minecraft:custom_model_data': {'colors': [col]}}},
        'transformation': {'translation': [0, 0, 0], 'left_rotation': [0, 0, 0, 1], 'scale': [scale] * 3, 'right_rotation': [0, 0, 0, 1]}}, idx)


def her_point(p, dist):
    """A track point [left, up, forward] of her standing `dist` b before the avatar, facing it (yaw 180) -> world"""
    return (-p[0], p[1], dist - p[2])


def contrast(c1, c2):
    def lum(c):
        v = [x / 255 for x in c]
        v = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    a, b = sorted((lum(c1), lum(c2)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def measure_hit(st, clip, event, dist, idle='idle', lead_rule=10):
    """One hit at one distance (1080p, the p1 field: geometry only): dict of pixel measures."""
    B, api = st.blade, st.api
    sw = B.swing_of(clip, event)
    W = 1920
    f = (1080 / 2) / math.tan(math.radians(FOV) / 2)
    pos, _yaw, pitch = camera(dist)
    out = dict(clip=clip, event=event, h=sw.h, swing=(sw.a, sw.b), wound=sw.w, lead=sw.h - sw.w, dist=dist)
    # (a) the wind-up pose against the stance: pixels that differ, the avatar in the frame
    tw = max(0, min(sw.a, sw.h - 1))
    wind = st.frame(clip, tw, dist, 'p1', w=W)[0]
    base = st.frame(idle, 0, dist, 'p1', w=W)[0]
    none = st.frame(idle, 0, dist, 'p1', w=W, her=False)[0]
    her_px = int(_mask(base, none).sum())
    out['pose_px'] = int(_mask(wind, base).sum())
    out['her_px'] = her_px
    out['pose_share'] = round(out['pose_px'] / max(1, her_px), 2)
    # (b) the blade (its edge sheath alone) at the wind-up: mean width = area / length on screen
    with_g = st.frame(clip, tw, dist, 'p1', w=W, avatar=False)[0]
    no_g = st.frame(clip, tw, dist, 'p1', w=W, avatar=False, look=None)[0]
    area = int(_mask(with_g, no_g, 0.04).sum())
    view = PV.View('camera', 0.0, pitch, True, pos, FOV)
    tr = B.track(clip)
    pb, pt_ = (view.screen(view.cam(np.array(her_point(tr[k][tw], dist))), 1920, 1080) for k in ('b', 't'))
    ln = float(np.linalg.norm(pb - pt_))
    out['blade_len_px'] = round(ln, 1)
    out['blade_w_px'] = round(area / ln, 1) if ln > 25 else None           # (end-on to the lens: no width to speak of)
    out['blade_w_min_px'] = round(0.092 * f / math.dist(pos, her_point(tr['t'][tw], dist)), 1)      # the sheath's least width, any side
    b_ = st.frame(clip, tw, dist, 'p1', (), w=W, her=False, avatar=False)[0]
    nop = st.frame(clip, tw, dist, 'p1', (), w=W)[0]
    # (d) the cue star (parryable: at blade_mid, hit - 7): the share of it her hat / body / the avatar leave visible
    tc = max(0, sw.h - api.CUE_LEAD)
    cue = _card('rlk:mboss/hr_kit/cue_0', her_point(B.cue_point(clip, tc), dist), 2.1)
    alone = _mask(st.frame(clip, tc, dist, 'p1', [cue], w=W, her=False, avatar=False)[0], b_, 0.04)
    seen = _mask(st.frame(clip, tc, dist, 'p1', [cue], w=W)[0], st.frame(clip, tc, dist, 'p1', (), w=W)[0], 0.04)
    out['cue_px'] = int(alone.sum())
    out['cue_seen'] = round(int((seen & alone).sum()) / max(1, int(alone.sum())), 2)
    # the star against her hat: the share of the star's pixels that lie over her hat (white on white without the dark rim)
    hat_only = _mask(st.frame(clip, tc, dist, 'p1', (), w=W, avatar=False)[0], b_, 0.04)
    out['cue_on_her'] = round(int((alone & hat_only).sum()) / max(1, int(alone.sum())), 2)
    # (e) the flash of an unparriable hit (the yellow sphere 2.4 b at her head at the wind-up)
    fl = _card('rlk:mboss/hr_kit/yellow_tell_0', her_point(tr['h'][tw], dist), 2.4)
    alone = _mask(st.frame(clip, tw, dist, 'p1', [fl], w=W, her=False, avatar=False)[0], b_, 0.04)
    seen = _mask(st.frame(clip, tw, dist, 'p1', [fl], w=W)[0], nop, 0.04)
    out['flash_px'] = int(alone.sum())
    out['flash_seen'] = round(int((seen & alone).sum()) / max(1, int(alone.sum())), 2)
    # (f) the slash against the blade: the largest angle between a piece's plane and the blade that bounds it
    worst = 0.0
    for pc in sw.pieces():
        if pc['kind'] != 'arc':
            continue
        for (b0, t0) in zip(pc['bases'], pc['tips']):
            worst = max(worst, abs(90 - B.angle(B.sub(t0, b0), pc['n'])))
    out['slash_deg'] = round(worst, 2)
    return out


def cmd_measure(st, a):
    api, B = st.api, st.blade
    rows, seen = [], set()
    todo = []
    for key, hs in api.HITS.items():
        prev = None
        for row in hs:
            clip, ev = row[0], row[1]
            if (clip, ev) in seen:
                continue
            seen.add((clip, ev))
            h = api.ev(clip, ev)
            first = prev is None or prev[0] != clip or h - prev[1] > 24 or key == 'ult'
            prev = (clip, h)
            todo.append((key, clip, ev, row[6], first))
    if a.clips:
        todo = [t for t in todo if t[1] in a.clips.split(',')]
    for key, clip, ev, par, first in todo:
        idle = 'idle2' if clip in ('mx', 'nb', 'q_grab', 'q_air') or clip.startswith('g_') else 'idle'
        for d in (4.0, 7.0, 10.0):
            if a.dist and d != a.dist:
                continue
            r = measure_hit(st, clip, ev, d, idle, B.LEAD_FIRST if first else B.LEAD_CHAIN)
            r.update(key=key, parry=par, first=first)
            rows.append(r)
            print(f"{key:6s} {clip:7s} {ev:6s} {par} D{d:<4g} lead {r['lead']:2d} pose {r['pose_px']:6d} px ({r['pose_share']:.2f} of her) "
                  f"blade {r['blade_w_px']} px (min {r['blade_w_min_px']}) "
                  f"cue seen {r['cue_seen']:.2f} on her {r['cue_on_her']:.2f} flash seen {r['flash_seen']:.2f} slash {r['slash_deg']} deg", flush=True)
    ink, core = (0x1C, 0x0B, 0x2E), (255, 233, 168)
    con = {f: dict(rim_vs_grass=round(contrast(ink, FIELD[f]['grass']), 1), rim_vs_hat=round(contrast(ink, HAT), 1),
                   rim_vs_floor=round(contrast(ink, tuple(int(v) for v in FIELD[f]['floor'].split(','))), 1),
                   core_vs_floor=round(contrast(core, tuple(int(v) for v in FIELD[f]['floor'].split(','))), 1),
                   core_vs_grass=round(contrast(core, FIELD[f]['grass']), 1)) for f in FIELD}
    print('contrast (WCAG ratio) of the tells\' dark rim / white-gold core:', json.dumps(con))
    if a.json:
        Path(a.json).write_text(json.dumps(dict(rows=rows, contrast=con), indent=1))


# ----------------------------------------------------------------------------- trail: round W's measure on the rendered pixels
TRAIL_HITS = (('a1', 'hit'), ('a2', 'hit'), ('a3', 'h1'), ('a3', 'h4'), ('d4', 'h1'), ('d4', 'h3'), ('tri', 'h1'), ('rings', 'r1'),
              ('a4', 'hit'), ('a9', 'cut'), ('a10', 'hit'), ('hcut', 'cut'), ('kcut', 'cut'), ('ult', 'cut1'), ('mx', 'x'), ('mx', 'dome'),
              ('nb', 'b1'), ('q_air', 'beam'), ('g_rise', 'hit'), ('g_sweep', 'hit'), ('g_vert', 'hit'))


def lum(img):
    v = np.where(img <= 0.03928, img / 12.92, ((img + 0.055) / 1.055) ** 2.4)
    return 0.2126 * v[..., 0] + 0.7152 * v[..., 1] + 0.0722 * v[..., 2]


def measure_trail(st, clip, event, dist, field, w=960):
    """The trail of one hit at one distance / field: at the hold (the wind-up held), one tick after the hit (the swing's pieces):
    its visible pixels, the band's width (px at 1080p), the luminance contrast against what is behind it."""
    B, api = st.blade, st.api
    key = next(k for k, hs in api.HITS.items() if any(r[0] == clip and r[1] == event for r in hs))
    idx = next(i for i, r in enumerate(api.HITS[key]) if r[0] == clip and r[1] == event)
    col = B.colour_of(key, idx)[0]
    sw, cmds = hit_cmds(st, clip, event, col)
    k2 = 1080 / round(w * 9 / 16)
    hp = (0.0, 0.0, float(dist))
    res = dict(clip=clip, event=event, dist=dist, field=field, col=hex(col))
    for name, tau in (('hold', max(sw.w + 2, 2)), ('swing', sw.h), ('after', min(sw.h + 2, sw.b + 3))):
        cards = st.cards_of(cmds, [tau], hp)[tau]
        band = [e for e in cards if 'rlk_hr_trb' in e.tags]
        alone = st.frame(clip, tau, dist, field, cards, w=w, her=False, avatar=False)[0]
        empty = st.frame(clip, tau, dist, field, (), w=w, her=False, avatar=False)[0]
        full = st.frame(clip, tau, dist, field, cards, w=w)[0]
        none = st.frame(clip, tau, dist, field, (), w=w)[0]
        m_all = _mask(alone, empty, 0.04)
        seen = _mask(full, none, 0.04)
        r = dict(px=int(round(seen.sum() * k2 * k2)), seen=round(float(seen.sum()) / max(1, int(m_all.sum())), 2))
        if seen.sum():
            la, lb = lum(full)[seen], lum(none)[seen]
            ratio = (np.maximum(la, lb) + 0.05) / (np.minimum(la, lb) + 0.05)
            r['contrast_med'] = round(float(np.median(ratio)), 2)
            r['contrast_ok'] = round(float((ratio >= 1.5).mean()), 2)
        if band:
            bm = _mask(st.frame(clip, tau, dist, field, band, w=w, her=False, avatar=False)[0], empty, 0.04)
            pos, _y, pitch = camera(dist)
            view = PV.View('camera', 0.0, pitch, True, pos, FOV)
            tr = B.track(clip)
            ct = min(tau, len(tr['t']) - 1)
            pb, pt_ = (view.screen(view.cam(np.array(her_point(tr[k][ct], dist))), w, round(w * 9 / 16)) for k in ('b', 't'))
            ln = float(np.linalg.norm(pb - pt_))
            r['band_w_px'] = round(bm.sum() / ln * k2, 1) if ln > 12 else None
        res[name] = r
    return res


def cmd_trail(st, a):
    rows = []
    todo = TRAIL_HITS if not a.clips else [x for x in TRAIL_HITS if x[0] in a.clips.split(',')]
    for clip, ev in todo:
        for d in (4.0, 7.0, 10.0):
            for fld in ('p1', 'p1w', 'p2'):
                r = measure_trail(st, clip, ev, d, fld)
                rows.append(r)
                print(f"{clip:7s} {ev:5s} D{d:<4g} {fld} " + ' | '.join(
                    f"{n} px {r[n]['px']} seen {r[n]['seen']} band {r[n].get('band_w_px')} contrast {r[n].get('contrast_med')} "
                    f"(>=1.5: {r[n].get('contrast_ok')})" for n in ('hold', 'swing', 'after')), flush=True)
    if a.json:
        Path(a.json).write_text(json.dumps(rows, indent=1))


# ----------------------------------------------------------------------------- the real pattern (the module in the H1 world)
def run_pattern(st, sim, key, ph, dist, strafe=0.0, seed=7, limit=260):
    """Run pattern `key` through the generated functions in lane H1's world (hr/tests/lib/hrsim.py of the sim copy `sim`) with the
    player `dist` b before her; per pattern tick a record: her body (pos, yaw), the rig's clip and tick, hidden?, the player's
    body (pos, yaw) and every live sweep card (pos, yaw, pitch, nbt). The sim keeps no display NBT: this wrapper replays the
    summon / data merge / data modify lines of the sweep cards beside it."""
    sys.path.insert(0, str(Path(sim) / 'hr/tests'))
    import pat_lib as PL
    H = PL.H
    api, S_ = PL.load_api(st.wt)
    base_cmd = H.H1Sim.cmd
    NB = {}

    def cmd(self, t, ctx):
        n0 = len(self.ents)
        r = base_cmd(self, t, ctx)
        try:
            if t and t[0] == 'summon' and '"rlk_hr_tr"' in ' '.join(t):         # round W: the trail's cards
                for e in self.ents[n0:]:
                    NB[e.id] = PV.parse_snbt(' '.join(t[5:]))
            elif t and t[0] == 'data' and t[1] == 'merge' and t[2] == 'entity' and ctx.ex is not None and ctx.ex.id in NB:
                PV.deep_merge(NB[ctx.ex.id], PV.parse_snbt(' '.join(t[4:])))
            elif t and t[0] == 'data' and t[1] == 'modify' and ctx.ex is not None and ctx.ex.id in NB and 'item_model' in t[4]:
                NB[ctx.ex.id]['item']['components']['minecraft:item_model'] = t[-1].strip('"')
        except Exception as ex:      # noqa: BLE001
            print('replay', ex, t[:4])
        return r
    H.H1Sim.cmd = cmd
    base_call = H.H1Sim.call
    RIG = dict(clip=None, ct=0, pend=None, hidden=False)
    RP = 'rlk:boss/scarlet/rig/'

    def call(self, fid, ctx, macro=None):
        if fid.startswith(RP):
            k = fid[len(RP):]
            if k.startswith('play/'):
                RIG.update(pend=k[5:], hidden=False)
            elif k.startswith('start/'):
                RIG.update(clip=k[6:], ct=0, pend=None, hidden=False)
            elif k == 'tick':
                if RIG['pend']:
                    RIG.update(clip=RIG['pend'], ct=0, pend=None)
                else:
                    RIG['ct'] += 1
            elif k == 'state/hidden':
                RIG['hidden'] = True
            elif k == 'state/normal':
                RIG['hidden'] = False
        return base_call(self, fid, ctx, macro)
    H.H1Sim.call = call
    s, pl = H.setup_h1(str(st.wt), seed=seed)
    assert H.fight_sc(s)
    if ph == 2:
        H.test_id(s, 33)
        H.run_h1(s, 2)
    H.heal(s)
    H.facing_setup(s, dist)
    tid = S_.TID[key]
    H.start_pattern(s, tid)
    if key == 'ult':
        assert H.until_h1(s, lambda s: (H.hr(s, '#pat') or 0) == tid, 160)
    ids = {v['id']: k for k, v in json.loads((st.wt / 'tools/scarlet_rig_manifest.json').read_text())['clips'].items()}
    recs, LEN = [], {}
    for _ in range(limit):
        if (H.hr(s, '#pat') or 0) != tid:
            break
        if strafe:
            p = s.player()
            H.place_player(s, p.pos[0] + strafe, p.pos[2])
        H.heal(s)
        H.world_h1(s)
        if (H.hr(s, '#pat') or 0) != tid:
            break
        b = H.body_of(s)
        p = s.player()
        clip_name, ct, hid = RIG['clip'], RIG['ct'], RIG['hidden']
        n = H.hr(s, '#sw_x')
        cards = []
        for e in s.ents:
            if e.alive and e.id in NB:
                nb = json.loads(json.dumps(NB[e.id], default=float))
                # (the sim keeps no display NBT: a ribbon's length is core/sw/rib1's #sw_x, a struck line's the dash's probe)
                if 'rlk_hr_trg' in e.tags and n:
                    LEN[e.id] = n * 1e-6
                if 'rlk_hr_tri' in e.tags and 'rlk_hr_trg' not in e.tags and e.id not in LEN and any(t.endswith('w') for t in e.tags):
                    LEN[e.id] = 0.5 * (H.hr(s, f'#{key}_n') or 0)
                if e.id in LEN:
                    nb['transformation']['scale'][2] = LEN[e.id]
                cards.append((tuple(e.pos), e.rot[0], e.rot[1], nb))
        recs.append(dict(pt=H.hr(s, '#pt') or 0, body=(tuple(b.pos), b.rot[0]), clip=clip_name, ct=ct, hidden=bool(hid),
                         player=(tuple(p.pos), p.rot[0]), cards=cards))
    H.H1Sim.cmd = base_cmd
    H.H1Sim.call = base_call
    return recs


def fight_frame(st, rec, cam, field, w=480, look='edge'):
    """One frame of a recorded pattern tick from the fixed lens cam = (pos, yaw, pitch)."""
    sc = PV.Scene(st.dbg, (0, 0, 0), scores={}, macros={}, max_depth=4, follow=True)
    (bp, byaw) = rec['body']
    if rec['clip'] and not rec['hidden']:
        c = PV.Ctx(bp, byaw, 0.0)
        n = st.api.CLIPS[rec['clip']][0]
        sc.run_file('rlk:boss/scarlet/rig/spawn', c)
        sc.run_file(f"rlk:hr_dbg/{rec['clip']}/{max(0, min(n, (rec['ct'] or 0) + 1))}", c)     # (the instant the cards' targets show)
        sc.command(f'tp @e[tag=rlk_hr_part] {bp[0]:.3f} {bp[1]:.3f} {bp[2]:.3f} {byaw:.2f} 0', c, 0)
        for e in sc.entities:
            if 'rlk_hr_sword_glow' in e.tags and look:
                e.nbt.setdefault('item', {}).setdefault('components', {})['minecraft:item_model'] = f'rlk:mboss/scarlet/glow_{look}'
    (pp, pyaw) = rec['player']
    n0 = len(sc.entities)
    sc.run_file('rlk:hr_dbg/avatar', PV.Ctx((pp[0] - 1.4, pp[1], pp[2]), 0.0, 0.0))
    for e in sc.entities[n0:]:
        e.yaw = pyaw
    for i, (pos, yaw, pitch, nb) in enumerate(rec['cards']):
        sc.entities.append(PV.Entity('item_display', pos, yaw, pitch, nb, 9000 + i))
    view = PV.View('camera', cam[1], cam[2], True, cam[0], FOV)
    F = FIELD[field]
    opts = SimpleNamespace(alpha_scale=1.0, bg_top=F['bg_top'], bg_bottom=F['bg_bottom'], flat=False, light='mc', floor=F['floor'],
                           floor_half=30.0, translucent=True, tex_mode='uv')
    # the rasteriser's floor is the plane y 0 round the origin: shift the scene so the lens' ground point is the origin
    org = np.array((cam[0][0], FLOOR_Y, cam[0][2]))
    for e in sc.entities:
        e.pos = np.array(e.pos, float) - org
    view.pos = view.pos - org
    geo = PV.Geometry(sc, st.assets)
    for i, (e, baked, tints, M, name) in enumerate(geo.items):
        cmd = (e.nbt.get('item') or {}).get('components', {}).get('minecraft:custom_model_data')
        if cmd and cmd.get('colors'):
            c = int(cmd['colors'][0])
            geo.items[i] = (e, baked, [np.array([(c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255])] * max(1, len(tints)), M, name)
    h = round(w * 9 / 16)
    img, z = render_lit(geo, view, w, h, opts, st.assets)
    return img, z, view, geo


def fight_cam(rec0):
    """The F5 lens of the player of record rec0, aiming at her chest as she stands then (fixed for the pattern)."""
    (pp, _pyaw), (bp, _b) = rec0['player'], rec0['body']
    dx, dz = bp[0] - pp[0], bp[2] - pp[2]
    d = math.hypot(dx, dz)
    yaw = math.degrees(math.atan2(-dx, dz))
    pitch = math.atan2(PIVOT_Y - CHEST_Y, d)
    back = CAM_D * math.cos(pitch)
    pos = (pp[0] - dx / d * back, pp[1] + PIVOT_Y + CAM_D * math.sin(pitch), pp[2] - dz / d * back)
    return pos, yaw, math.degrees(pitch)


def cmd_fight(st, a):
    recs = run_pattern(st, a.sim, a.key, a.ph, a.dist)
    cam = fight_cam(recs[0])
    t0 = a.t0 or 0
    t1 = a.t1 if a.t1 is not None else recs[-1]['pt']
    panels = []
    for r in recs:
        if not (t0 <= r['pt'] <= t1) or (r['pt'] - t0) % a.step:
            continue
        if a.zoom and a.zoom > 1:
            img = fight_frame(st, r, cam, a.field, w=1920)[0]
            hw, hh = int(960 / a.zoom), int(540 / a.zoom)
            cy = 540 - int(120 / a.zoom)
            img = np.asarray(Image.fromarray((np.clip(img[cy - hh:cy + hh, 960 - hw:960 + hw], 0, 1) * 255).astype(np.uint8)).resize(
                (a.w, round(a.w * 9 / 16)), Image.LANCZOS)).astype(float) / 255
        elif a.crop:
            x0, y0, x1, y1 = (int(v) for v in a.crop.split(','))
            img = fight_frame(st, r, cam, a.field, w=1920)[0][y0:y1, x0:x1]
        else:
            img = fight_frame(st, r, cam, a.field, w=a.w)[0]
        panels.append(label(img, f"{a.key} P{a.ph} pt{r['pt']} {r['clip']} {r['ct']} D{a.dist:g} {a.field}", img.shape[1]))
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
    s.add_argument('--look', default='edge', help="the blade look (none: a rig built before round V has no `edge`)")
    s.add_argument('--tells', action='store_true', help='draw the cue star (a parryable hit, h - 7 .. h - 1) / the flash sphere at her head')
    s.add_argument('--flash', type=int, help='with --tells: the tick the flash of an unparriable hit starts (shown 8 t)')
    s.add_argument('--w', type=int, default=480)
    s.add_argument('--crop', help='x0,y0,x1,y1 in 1920 x 1080 px: render at 1080p and cut this window (detail strips)')
    s.add_argument('--cols', type=int, default=6)
    s.add_argument('-o', '--out', required=True)
    f = sub.add_parser('fight')
    f.add_argument('--sim', required=True, help='the sim copy (tools/dev/sim outside the datapack)')
    f.add_argument('--key', required=True)
    f.add_argument('--ph', type=int, default=1)
    f.add_argument('--dist', type=float, default=7.0)
    f.add_argument('--field', default='p1', choices=list(FIELD))
    f.add_argument('--from', dest='t0', type=int)
    f.add_argument('--to', dest='t1', type=int)
    f.add_argument('--step', type=int, default=1)
    f.add_argument('--w', type=int, default=480)
    f.add_argument('--cols', type=int, default=6)
    f.add_argument('--crop')
    f.add_argument('--zoom', type=float, default=2.0, help='render at 1080p and show the middle 1/zoom of the screen (0: the whole screen)')
    f.add_argument('-o', '--out', required=True)
    tm = sub.add_parser('trail')
    tm.add_argument('--clips')
    tm.add_argument('--json')
    m = sub.add_parser('measure')
    m.add_argument('--clips')
    m.add_argument('--dist', type=float)
    m.add_argument('--json')
    a = ap.parse_args()
    st = Stage(a.wt, a.dbg, a.rp)
    if a.cmd == 'measure':
        return cmd_measure(st, a)
    if a.cmd == 'trail':
        return cmd_trail(st, a)
    if a.cmd == 'strip':
        cmd_strip(st, a)
    elif a.cmd == 'fight':
        cmd_fight(st, a)


if __name__ == '__main__':
    main()
