#!/usr/bin/env python3
"""Offline renders of the 홍련 fx kit (tools/build_mboss_hr_fx.py): one strip per preset call, seen from the game's raised
F5 camera (3.5 b from the seat 0.5 b over the avatar's head, looking 14 deg down past it at her).

The card ray caster of the 아를레키노 kit renderer (../../../ar/s1k/render/render_kn_core.py: SimCard, the stage merges and
their interpolation, billboards, tints, particles as soft dots) with the hr kit's names (custom data hrG / hrS / hrF /
hrC, the lancex plane) on the kit's own harness (../lib/hrfxsim.py). Every strip runs the kit's own preset function at its
executor point; she is a dark stand-in (2.0 b, the hat's brim), the player a pale one, on a crimson-grass floor.

    python3 -I render_hr.py <worktree roguelike dir> <resource pack> <out dir> [strip ...]     (no strip = all; --list)

Lane H1c (11-11) wrote it for the H1 block of the kit (flash_blue, ult_web, ult_burst, sky_mark, sky_pillar, qi_beam, the
big yellow tell, the parry cue, the chest / knee rings); STRIPS below is the list, add a row for any other preset call.
"""
import math
import random
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'lib'))
import mcsim  # noqa: E402
import hrfxsim  # noqa: E402

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
WT, RP, OUT = Path(ARGS[0]).resolve(), Path(ARGS[1]).resolve(), Path(ARGS[2]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(WT / 'tools'))
import build_mboss_hr_fx as G  # noqa: E402

FN = WT / 'data/rlk/function'
FY = float(G.FLOOR)
BOSS = np.array((760.5, FY, 8.5))          # her feet; she faces +z (yaw 0), the player stands D b before her
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def font(sz):
    return ImageFont.truetype(FONT, sz) if Path(FONT).exists() else ImageFont.load_default()


_PL = re.compile(r'^particle (minecraft:[a-z_]+)(\{.*?\})? ((?:\S+ ){3})([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+) (\d+)')


class RSim(hrfxsim.FxSim):
    def cmd(self, t, ctx):
        if t and t[0] == 'particle':
            m = _PL.match(' '.join(t))
            if m:
                name, nbt, pos, dx, dy, dz, sp, n = m.groups()
                try:
                    p = self.coords(pos.split(), ctx)
                except Exception:          # noqa: BLE001
                    p = ctx.pos
                self.dots.append((self.gt, name.split(':')[1], nbt or '', np.array(p, float), float(dx), float(dy),
                                  float(dz), float(sp), int(n)))
            return 1
        return super().cmd(t, ctx)


def fresh(dist):
    s = RSim(FN)
    s.dots = []
    s.player = mcsim.Ent('player', (BOSS[0], FY, BOSS[2] + dist), tags=('player',))
    s.ents.append(s.player)
    s.setsc(('e', s.player.id), 'dead', 0)
    s.setsc(('e', s.player.id), 'rnDie', 0)
    return s


def _h(a, b, k=0):
    v = (a.astype(np.int64) * 73856093) ^ (b.astype(np.int64) * 19349663) ^ (k * 83492791)
    v = (v ^ (v >> 13)) * 1274126177
    return ((v ^ (v >> 16)) & 0xFFFF) / 65535.0


FIELD = {'p2': [(0.36, 0.10, 0.13), (0.42, 0.12, 0.15), (0.31, 0.08, 0.11), (0.46, 0.15, 0.17)],
         # HA-07: the P1 moon field (hr_field `moon`: mycelium 70 %, pale moss, coarse dirt, tuff under the night light)
         'p1': [(0.36, 0.31, 0.34), (0.40, 0.35, 0.38), (0.52, 0.53, 0.47), (0.38, 0.29, 0.22)]}
FLOOR_LOOK = ['p2']


def floor_colour(x, z):
    """the field: P2 crimson (dark red grass blocks) or P1 moon (grey-violet mycelium, moss, dirt), a little noise"""
    base = np.array(FIELD[FLOOR_LOOK[0]])
    col = base[np.clip((_h(np.floor(x), np.floor(z), 2) * 4).astype(int), 0, 3)]
    return np.clip(col + _h(np.floor(x * 8), np.floor(z * 8), 7)[..., None] * 0.06 - 0.03, 0, 1)


# ----------------------------------------------------------------------------- cards
TEX = {}


def tex(texid):
    if texid not in TEX:
        ns, path = texid.split(':')
        TEX[texid] = np.asarray(Image.open(RP / f'assets/{ns}/textures/{path}.png').convert('RGBA')).astype(float) / 255
    return TEX[texid]


def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_x(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rot_axis(axis, a):
    x, y, z = np.array(axis, float) / (np.linalg.norm(axis) or 1)
    c, s, C = math.cos(a), math.sin(a), 1 - math.cos(a)
    return np.array([[c + x * x * C, x * y * C - z * s, x * z * C + y * s],
                     [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
                     [z * x * C - y * s, z * y * C + x * s, c + z * z * C]])


def local_quads(kind):
    """[(P0, P1, P2), ...]: local points at texture (0, 0), (1, 0), (0, 1); v up (build_mboss_hr_fx.model_json)"""
    plane, _px, (a0, a1, b0, b1), _n, texid, _d = G.kind_info(kind)
    P = lambda x, y, z: np.array([x, y, z], float)       # noqa: E731
    face = (P(-a0, b0, 0), P(-a1, b0, 0), P(-a0, b1, 0))
    flat = (P(-a0, 0, b0), P(-a1, 0, b0), P(-a0, 0, b1))
    if plane == 'face':
        q = [face]
    elif plane == 'flat':
        q = [flat]
    elif plane == 'cross':
        q = [face, (P(0, b0, a0), P(0, b0, a1), P(0, b1, a0))]
    elif plane == 'lance':
        q = [flat, (P(0, a0, b0), P(0, a1, b0), P(0, a0, b1))]
    elif plane == 'lancex':
        q = [flat, face]
    else:
        raise ValueError(plane)
    return q, texid


def _vec(v):
    return np.array([float(x) for x in v], float)


def _aa(r, default_axis=(0, 0, 1)):
    if isinstance(r, dict):
        return float(r['angle']), tuple(float(v) for v in r['axis'])
    x, y, z, w = (float(v) for v in r)
    w = max(-1.0, min(1.0, w))
    ang = 2 * math.acos(w)
    sn = math.sqrt(max(0.0, 1 - w * w))
    return (0.0, default_axis) if sn < 1e-9 else (ang, (x / sn, y / sn, z / sn))


class SimCard:
    """one item_display card of the simulator at client time t (ticks of gametime)"""

    def __init__(self, s, e, t):
        n = s.nbt[e.id]
        comp = n['item']['components']
        cd = comp.get('minecraft:custom_data', {})
        self.kind = comp['minecraft:item_model'].split('/')[-1]
        self.pos, self.yaw, self.pitch = np.array(e.pos, float), e.rot[0], e.rot[1]
        self.bb = n.get('billboard', 'fixed')
        tr = n['transformation']
        roll, lax = _aa(tr['left_rotation'])
        spin, ax = _aa(tr['right_rotation'])
        cur = {'t': _vec(tr['translation']), 's': _vec(tr['scale']), 'spin': spin, 'ax': ax, 'roll': roll, 'lax': lax}
        col = comp.get('minecraft:custom_model_data', {}).get('colors', [0xFFFFFF])[0]
        start, target, g0, d = cur, None, 0, 0

        def at(tt):
            if target is None:
                return start
            f = 1.0 if d <= 0 else min(1.0, max(0.0, (tt - g0) / d))
            out = {k: start[k] + (target[k] - start[k]) * f for k in ('t', 's', 'spin', 'roll')}
            out['ax'], out['lax'] = target['ax'], target['lax']
            return out
        self.dead = False
        for gg, ev in sorted((gg, ev) for gg, i, ev in s.events if i == e.id):
            if gg > t:
                break
            if ev == 'kill':
                self.dead = True
                continue
            if ev == 'hit':
                if cd.get('hrC', -1) >= 0:
                    col = cd['hrC']
                continue
            snap = cd.get(ev)
            if not isinstance(snap, dict):
                continue
            now = at(gg)
            tgt = dict(now)
            T = snap.get('transformation', {})
            if 'translation' in T:
                tgt['t'] = _vec(T['translation'])
            if 'scale' in T:
                tgt['s'] = _vec(T['scale'])
            if 'right_rotation' in T:
                tgt['spin'], tgt['ax'] = _aa(T['right_rotation'])
            if 'left_rotation' in T:
                tgt['roll'], tgt['lax'] = _aa(T['left_rotation'])
            start, target, g0, d = now, tgt, gg, int(snap.get('interpolation_duration', 0))
        self.st = at(t)
        self.col = col

    def quads(self, cam):
        st = self.st
        if self.dead or np.allclose(st['s'], 0):
            return []
        R = rot_axis(st['ax'], st['spin'])
        L = rot_axis(st.get('lax', (0, 0, 1)), st['roll'])
        M = L @ np.diag(st['s']) @ R
        if self.bb == 'fixed':
            E = rot_y(math.radians(-self.yaw)) @ rot_x(math.radians(self.pitch))
        elif self.bb == 'vertical':
            E = rot_y(math.radians(-cam.yaw + 180))
        else:
            E = rot_y(math.radians(-cam.yaw + 180)) @ rot_x(math.radians(-cam.pitch))
        qs, texid = local_quads(self.kind)
        return [([self.pos + E @ (st['t'] + M @ p) for p in (A, B, C)], self.col, texid) for A, B, C in qs]


class Cam:
    def __init__(self, pos, tgt, w, h, fov=70.0):
        d = np.array(tgt, float) - np.array(pos, float)
        self.yaw = math.degrees(math.atan2(-d[0], d[2]))
        self.pitch = -math.degrees(math.atan2(d[1], math.hypot(d[0], d[2])))
        self.pos, self.w, self.h = np.array(pos, float), w, h
        y, p = math.radians(self.yaw), math.radians(self.pitch)
        self.F = np.array([-math.sin(y) * math.cos(p), -math.sin(p), math.cos(y) * math.cos(p)])
        self.R = np.cross(self.F, [0, 1, 0])
        self.R /= np.linalg.norm(self.R)
        self.U = np.cross(self.R, self.F)
        self.f = (h / 2) / math.tan(math.radians(fov) / 2)

    def rays(self):
        i, j = np.meshgrid(np.arange(self.w) + 0.5, np.arange(self.h) + 0.5)
        D = self.F + ((i - self.w / 2) / self.f)[..., None] * self.R + ((self.h / 2 - j) / self.f)[..., None] * self.U
        D = D / np.linalg.norm(D, axis=-1, keepdims=True)
        return np.broadcast_to(self.pos, D.shape), D


PART_LOOK = {'end_rod': (0.10, (1.0, 1.0, 0.94), 0.95, 30), 'explosion': (1.3, (0.92, 0.92, 0.88), 0.45, 8),
             'crit': (0.08, (0.95, 0.92, 0.85), 1.0, 10), 'sweep_attack': (1.2, (0.95, 0.95, 0.95), 0.5, 6),
             'electric_spark': (0.07, (0.85, 0.95, 1.0), 1.0, 8), 'block': (0.12, (0.72, 0.52, 0.86), 1.0, 20),
             'snowflake': (0.08, (0.95, 0.97, 1.0), 0.9, 20), 'cloud': (0.3, (0.9, 0.9, 0.9), 0.5, 12)}


def dots(s, seed=1):
    out = []
    rnd = random.Random(seed)
    for gt, name, nbt, p0, dx, dy, dz, sp, n in s.dots:
        if name in ('dust', 'flash'):
            cols = [tuple(float(v.rstrip('f')) for v in c.split(','))[:3] for c in re.findall(r'\[([^\]]*)\]', nbt)] or [(1, 1, 1)]
            sc = re.search(r'scale:([-\d.]+)', nbt)
            look = (0.18 * (float(sc.group(1)) if sc else 1.0), cols[0], 0.95, 14) if name == 'dust' else (1.6, cols[0], 0.45, 3)
        else:
            look = PART_LOOK.get(name, (0.1, (1.0, 1.0, 1.0), 0.8, 12))
        size, c0, alpha, life = look
        for _k in range(min(n, 40)):
            off = np.array([rnd.gauss(0, 1) * dx, rnd.gauss(0, 1) * dy, rnd.gauss(0, 1) * dz])
            vel = np.array([rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1)]) * sp
            out.append((p0 + off, vel, size * rnd.uniform(0.7, 1.2), c0, alpha, int(life * rnd.uniform(0.6, 1.2)), gt))
    return out


def draw_dot(img, cam, t, depth, dot):
    pos, vel, size, c0, alpha, life, t0 = dot
    tt = t - t0
    if tt < 0 or tt >= life:
        return
    rel = pos + vel * tt * 0.85 ** tt - cam.pos
    dep = rel @ cam.F
    if dep <= 0.05:
        return
    x, y, rad = cam.w / 2 + (rel @ cam.R) / dep * cam.f, cam.h / 2 - (rel @ cam.U) / dep * cam.f, max(0.7, size / 2 / dep * cam.f)
    rr = 1.2 * rad + 1
    x0, x1, y0, y1 = int(max(0, x - rr)), int(min(cam.w, x + rr + 1)), int(max(0, y - rr)), int(min(cam.h, y + rr + 1))
    if x0 >= x1 or y0 >= y1 or np.linalg.norm(rel) > depth[int(min(cam.h - 1, max(0, y))), int(min(cam.w - 1, max(0, x)))] + 0.05:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1]
    a = np.clip(1.2 - np.hypot(xx + 0.5 - x, yy + 0.5 - y) / rad, 0, 1) ** 1.5 * alpha * (0.4 + 0.6 * (1 - tt / max(1, life)))
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a[..., None]) + np.array(c0) * a[..., None]


def box(img, cam, depth, O, D, lo, hi, col):
    """an axis-aligned stand-in box (ray / slab test), flat shaded"""
    with np.errstate(divide='ignore', invalid='ignore'):
        t1, t2 = (np.array(lo) - O) / D, (np.array(hi) - O) / D
    tn, tf = np.nanmax(np.minimum(t1, t2), -1), np.nanmin(np.maximum(t1, t2), -1)
    m = (tf >= tn) & (tf > 0) & (tn < depth)
    ax = np.argmax(np.minimum(t1, t2), -1)
    shade = np.array([0.8, 1.0, 0.62])[ax]
    img[m] = np.array(col) * shade[m][:, None]
    depth[m] = tn[m]


def render(cam, cards, t, dts, bodies):
    O, D = cam.rays()
    sky = np.linspace(0, 1, cam.h)[:, None, None]
    img = np.zeros((cam.h, cam.w, 3)) + np.array((0.10, 0.07, 0.13)) * (1 - sky) + np.array((0.22, 0.10, 0.16)) * sky
    depth = np.full((cam.h, cam.w), np.inf)
    with np.errstate(divide='ignore', invalid='ignore'):
        tf = (FY - O[..., 1]) / D[..., 1]
    m = np.isfinite(tf) & (tf > 0)
    H = O + D * np.where(m, tf, 0)[..., None]
    img[m] = floor_colour(H[..., 0][m], H[..., 2][m])
    fog = np.clip((tf[m] - 12) / 50, 0, 0.6)[:, None]
    img[m] = img[m] * (1 - fog) + np.array([0.20, 0.09, 0.14]) * fog
    depth[m] = tf[m]
    for lo, hi, col in bodies:
        box(img, cam, depth, O, D, lo, hi, col)
    items = []
    for c in cards:
        for (C0, C1, C2), col, texid in c.quads(cam):
            A, B = C1 - C0, C2 - C0
            N = np.cross(A, B)
            if np.linalg.norm(N) < 1e-9:
                continue
            items.append((np.linalg.norm(C0 + 0.5 * A + 0.5 * B - cam.pos), texid, C0, A, B, N, col))
    items.sort(key=lambda x: -x[0])
    for _d, texid, C0, A, B, N, col in items:
        with np.errstate(divide='ignore', invalid='ignore'):
            tt = ((C0 - O) @ N) / (D @ N)
        rel = O + D * np.nan_to_num(tt)[..., None] - C0
        BN, NA = np.cross(B, N), np.cross(N, A)
        u, v = (rel @ BN) / (A @ BN), (rel @ NA) / (B @ NA)
        ok = np.isfinite(tt) & (tt > 0) & (u >= 0) & (u < 1) & (v >= 0) & (v < 1) & (tt < depth + 1e-3)
        if not ok.any():
            continue
        T = tex(texid)
        th, tw = T.shape[:2]
        smp = T[np.clip(((1 - v[ok]) * th).astype(int), 0, th - 1), np.clip((u[ok] * tw).astype(int), 0, tw - 1)]
        keep = smp[:, 3] >= 0.1
        tint = np.array([(col >> 16) & 255, (col >> 8) & 255, col & 255]) / 255
        idx = np.argwhere(ok)[keep]
        a = smp[:, 3][keep][:, None]
        img[idx[:, 0], idx[:, 1]] = img[idx[:, 0], idx[:, 1]] * (1 - a) + (smp[:, :3] * tint)[keep] * a
    for d in dts:
        draw_dot(img, cam, t, depth, d)
    return img


def sim_cards(s):
    out = []
    for e in s.ents:
        if e.etype != 'item_display' or e.id not in s.nbt:
            continue
        comp = s.nbt[e.id].get('item', {}).get('components', {})
        if not str(comp.get('minecraft:item_model', '')).startswith(G.NS_TEX):
            continue
        s.nbt[e.id].setdefault('transformation', {'translation': [0, 0, 0], 'left_rotation': [0, 0, 0, 1], 'scale': [1, 1, 1],
                                                 'right_rotation': [0, 0, 0, 1]})
        out.append(SimCard(s, e, s.gt))
    return out


def overlay(img, name, alpha=1.0):
    """the full-screen overlay glyph `name` composited over the frame (the title glyph covers the whole screen)"""
    g = Image.open(RP / f'assets/rlk/textures/font/{G.FONT_NAME}/{name}.png').convert('RGBA')
    a = np.asarray(g.resize((img.shape[1], img.shape[0]), Image.BILINEAR)).astype(float) / 255
    al = a[..., 3:4] * alpha
    return img * (1 - al) + a[..., :3] * al


# ----------------------------------------------------------------------------- the strips
# name -> (title, player distance, her height over the floor, [(tick, where, call)], ticks drawn, overlay or None)
# where: 'chest' / 'blade' / 'feet' (her), 'lock' (the player's feet), 'pchest' (the player's chest); rotated as her (toward
# the player), `aim` = facing the lock from the executor
def fx(name, **a):
    return G.fx(name, **a)


STRIPS = {
    'flash_blue': ('flash_blue {t:15} at her chest (blue 0-19)', 7, 0, [(0, 'chest', fx('flash_blue', t=15))], (1, 3, 6, 12, 17, 19), None),
    'yellow': ('yellow_tell {t:6} and the big one {t:106} (kcut) at her chest', 6, 0,
               [(0, 'chest', fx('yellow_tell', t=6)), (10, 'chest', fx('yellow_tell', t=106))], (2, 4, 12, 14), None),
    'cue': ('parry cue: glint {c:2} at blade_mid (7 t before the hit)', 6, 0, [(0, 'blade', fx('glint', c=2))], (1, 2, 4, 6), None),
    'rings': ('qi_ring {r:26,c:1} at chest height (y + 1.1) / {r:30} / {r:45,c:2} at knee height (y + 0.7)', 6, 0,
              [(0, 'y1.1', fx('qi_ring', r=26, c=1)), (10, 'y1.1', fx('qi_ring', r=30, c=1)), (20, 'y0.7', fx('qi_ring', r=45, c=2))],
              (2, 5, 12, 15, 22, 25), None),
    'ult_web': ('ult_web {t:22} at her body 1.2 b up as the module calls it (with the overlay web 20 t), then ult_burst', 7, 0,
                [(0, 'chest', fx('ult_web', t=22)), (22, 'chest', fx('ult_burst'))], (1, 3, 10, 19, 23, 26), 'web'),
    'sky': ('sky_mark at the lock, 7 t later sky_pillar {r:24}', 8, 5, [(0, 'lock', fx('sky_mark')), (7, 'lock', fx('sky_pillar', r=24))],
            (1, 3, 6, 8, 10, 14), None),
    'sky_level': ('the same with her on the ground 10 b away (the camera level: the flash line at the feet)', 10, 0,
                  [(0, 'lock', fx('sky_mark')), (7, 'lock', fx('sky_pillar', r=24))], (1, 3, 6, 8, 10, 14), None),
    'qi_beam': ('qi_beam {len:140} from her blade 5 b up, aimed at the lock; then {len:160} called level', 7, 5,
                [(0, 'aim', fx('qi_beam', len=140)), (12, 'blade', fx('qi_beam', len=160))], (1, 2, 5, 13, 14, 17), None),
    'nb_band': ('qi_beam {len:160} as P-n calls it: at the lock point 0.6 b up, level, 30 deg off her aim (her 5 b up, 7 b away): '
                'the band through the lock', 7, 5, [(0, 'band', fx('qi_beam', len=160))], (1, 2, 3, 5, 7, 9), None),
    # HA-07 (review H-A): the parry cue at her blade from the F5 camera on both fields, at the near and the far end of a
    # chain's reach, and beside the three unparriable flashes on her chest (each frame measures the effect's on-screen size)
    'cue_p1': ('P1 (moon field): the parry cue glint {c:2} at blade_mid, her 6 b away', 6, 0, [(0, 'blade', fx('glint', c=2))],
               (1, 2, 4, 6), None, 'p1'),
    'cue_p2': ('P2 (crimson field): the parry cue glint {c:2} at blade_mid, her 6 b away', 6, 0, [(0, 'blade', fx('glint', c=2))],
               (1, 2, 4, 6), None, 'p2'),
    'cue_far': ('P2: the parry cue 10 b away (a gauntlet cut seen from afar)', 10, 0, [(0, 'blade', fx('glint', c=2))],
                (1, 2, 4, 6), None, 'p2'),
    'flashes': ('P2: the cue at her blade (0), the yellow (10), purple star4 (20) and blue (30) flashes at her chest, 6 b away',
                6, 0, [(0, 'blade', fx('glint', c=2)), (10, 'chest', fx('yellow_tell', t=6)), (20, 'chest', fx('star4')),
                       (30, 'chest', fx('flash_blue', t=15))], (1, 12, 21, 37), None, 'p2'),
}


COLS = 3
EXTENTS = {}


def extent(cam, s, bodies, t):
    """the cards' and motes' on-screen size in blocks at her distance: the bounding box of the pixels they change, over the
    pixel height of her 2.0-b stand-in"""
    base = render(cam, [], t, [], bodies)
    full = render(cam, sim_cards(s), t, dots(s), bodies)
    m = np.abs(full - base).max(-1) > 0.08
    nob = render(cam, [], t, [], [])
    hb = np.abs(base - nob).max(-1) > 0.02
    rows = np.where(hb.any(1))[0]
    ys, xs = np.where(m)
    if not len(ys) or not len(rows):
        return 0.0, 0.0
    per_b = (rows.max() - rows.min() + 1) / 2.06          # her box: feet to the brim top (2.06 b)
    return (xs.max() - xs.min() + 1) / per_b, (ys.max() - ys.min() + 1) / per_b


def run_strip(key, pw=560, ph=315):
    title, dist, up, calls, ticks, ovl = STRIPS[key][:6]
    FLOOR_LOOK[0] = STRIPS[key][6] if len(STRIPS[key]) > 6 else 'p2'
    s = fresh(dist)
    s.run(f'function {G.FN}e/init')
    her = BOSS + np.array((0, up, 0))
    ply = BOSS + np.array((0, 0, dist))
    where = {'chest': her + (0, 1.2, 0), 'blade': her + (0.6, 1.5, 0.4), 'feet': her, 'y1.1': her + (0, 1.1, 0), 'y0.7': her + (0, 0.7, 0),
             'lock': ply, 'pchest': ply + (0, 1.1, 0), 'aim': her + (0.3, 1.3, 0.4), 'band': ply + (0, 0.6, 0)}
    # the F5 camera: 3.5 b from the seat 0.5 b over the avatar's head (2.5 b up), looking 14 deg down past it (her feet show
    # over the avatar's head from about 5 b); raised toward her when she is in the air
    eye = ply + np.array((0, 2.5 + 3.5 * math.sin(math.radians(14)), 3.5 * math.cos(math.radians(14))))
    cam = Cam(eye, ply + np.array((0, 2.5 + up * 0.45, 0)) + (ply + np.array((0, 2.5, 0)) - eye) * 1.0, pw, ph)
    bodies = [(her + (-0.25, 0, -0.14), her + (0.25, 2.0, 0.14), (0.10, 0.09, 0.12)), (her + (-0.6, 2.0, -0.6), her + (0.6, 2.06, 0.6), (0.85, 0.85, 0.9)),
              (ply + (-0.25, 0, -0.14), ply + (0.25, 1.9, 0.14), (0.55, 0.62, 0.70))]
    t0 = s.gt
    frames = []
    last = max(ticks)
    web_until = None
    for k in range(last + 1):
        for tk, wh, line in calls:
            if tk == k:
                pos = where[wh]
                rot = (-30.0, 0.0) if wh == 'band' else (0.0, 0.0)
                if wh == 'aim':
                    d = ply + (0, 1.0, 0) - pos
                    rot = (0.0, -math.degrees(math.atan2(d[1], math.hypot(d[0], d[2]))))
                s.run(line, pos=tuple(pos), rot=rot)
                if 'ult_web' in line:
                    web_until = k + 20
        if k in ticks:
            im = render(cam, sim_cards(s), s.gt, dots(s), bodies)
            if ovl and web_until is not None and k < web_until:
                im = overlay(im, ovl, 1.0 if web_until - k > 3 else (web_until - k) / 4)
            fr = Image.fromarray((np.clip(im, 0, 1) * 255).astype(np.uint8))
            ex = ''
            if key.startswith(('cue', 'flashes')):
                ew, eh = extent(cam, s, [bodies[0], bodies[1]], s.gt)
                ex = f'  effect {ew:.2f} x {eh:.2f} b on screen'
                EXTENTS.setdefault(key, []).append((k, round(ew, 2), round(eh, 2)))
            ImageDraw.Draw(fr).text((4, 3), f't+{k}  ({len([c for c in sim_cards(s) if not c.dead])} cards){ex}', fill=(255, 255, 120), font=font(11))
            frames.append(fr)
        s.tick(1)
    cols = min(COLS, len(frames))
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new('RGB', (pw * cols, ph * rows + 16), (16, 16, 20))
    ImageDraw.Draw(sheet).text((4, 2), f'{key}: {title}', fill=(235, 235, 235), font=font(11))
    for i, fr in enumerate(frames):
        sheet.paste(fr, ((i % cols) * pw, 16 + (i // cols) * ph))
    return sheet


def main():
    if '--list' in sys.argv:
        print(' '.join(STRIPS))
        return
    keys = ARGS[3:] or list(STRIPS)
    sheets = [run_strip(k) for k in keys]
    W = max(sh.width for sh in sheets)
    out = Image.new('RGB', (W, sum(sh.height for sh in sheets)), (16, 16, 20))
    y = 0
    for sh in sheets:
        out.paste(sh, (0, y))
        y += sh.height
    name = OUT / ('hr_fx_' + ('all' if len(keys) == len(STRIPS) else '_'.join(keys)) + '.jpg')
    out.save(name, quality=88)
    print(name, out.size)
    for k, v in EXTENTS.items():
        print(f'extent {k}: ' + ', '.join(f't+{t} {w} x {h} b' for t, w, h in v))


if __name__ == '__main__':
    main()
