#!/usr/bin/env python3
"""Offline renders of the 아를레키노 fx kit (tools/build_mboss_kn_fx.py): the sprite sheet and one strip per preset / prop / decal.

The card ray caster of the Apep kit renderer (scratchpad ap/fxrender/render_ap.py: SimCard, the stage merges and their
interpolation, billboards, tints, particles as soft dots) copied with the tk names (tkS / tkG / tkF / tkC, the wave
plane), driven by the kit test's harness (scratchpad tk/tests/lib/tkfxsim.py): every strip runs the kit's own preset
function at its executor point next to a dark stand-in body (2.25 b) on a sand floor and draws the cards at 4 ticks.

    python3 render_fx.py <worktree roguelike dir> <resource pack> <out dir>
"""
import math
import random
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad')
sys.path.insert(0, str(S / 'ar/tests/lib'))
import mcsim  # noqa: E402
import knfxsim  # noqa: E402

WT = Path(sys.argv[1]).resolve()
RP = Path(sys.argv[2]).resolve()
OUT = Path(sys.argv[3]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(WT / 'tools'))
import build_mboss_kn_fx as G  # noqa: E402
from mboss_arlecchino import api  # noqa: E402

FN = WT / 'data/rlk/function'
TAG = G.TAG
FY = 201.0
P0 = np.array((760.5, FY, 8.5))
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def font(sz):
    return ImageFont.truetype(FONT, sz) if Path(FONT).exists() else ImageFont.load_default()


_PL = re.compile(r'^particle (minecraft:[a-z_]+)(\{.*?\})? ((?:\S+ ){3})([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+) (\d+)')


class RSim(knfxsim.FxSim):
    def cmd(self, t, ctx):
        if t and t[0] == 'particle':
            m = _PL.match(' '.join(t))
            if m:
                name, nbt, pos, dx, dy, dz, sp, n = m.groups()
                try:
                    p = self.coords(pos.split(), ctx)
                except Exception:          # noqa: BLE001
                    p = ctx.pos
                self.parts.append((self.gt, name.split(':')[1], nbt or '', np.array(p, float), float(dx), float(dy),
                                   float(dz), float(sp), int(n)))
            return 1
        return super().cmd(t, ctx)


def fresh():
    s = RSim(FN)
    s.player = mcsim.Ent('player', (760.5, FY, 30.5), tags=('player',))
    s.ents.append(s.player)
    s.setsc(('e', s.player.id), 'dead', 0)
    s.setsc(('e', s.player.id), 'rnDie', 0)
    return s


def _h(a, b, k=0):
    v = (a.astype(np.int64) * 73856093) ^ (b.astype(np.int64) * 19349663) ^ (k * 83492791)
    v = (v ^ (v >> 13)) * 1274126177
    return ((v ^ (v >> 16)) & 0xFFFF) / 65535.0


STONE = [(0.66, 0.68, 0.64), (0.70, 0.72, 0.68), (0.62, 0.64, 0.60), (0.72, 0.73, 0.70)]


def floor_colour(x, z, look):
    """the fl_ruins plaza: pale grey-green stone slabs, carved rings around the centre (760, 8)"""
    bx, bz = np.floor(x), np.floor(z)
    px = _h(np.floor(x * 16), np.floor(z * 16), 7)[..., None] * 0.05 - 0.025
    col = np.array(STONE)[np.clip((_h(bx, bz, 2) * 4).astype(int), 0, 3)]
    r = np.hypot(x - 760.0, z - 8.0)
    groove = np.zeros_like(r, bool)
    for g in (4, 9, 15, 21):
        groove |= np.abs(r - g) < 0.35
    col = np.where(groove[..., None], np.array((0.40, 0.42, 0.40)), col)
    return np.clip(col * 0.9 + px, 0, 1)


# ----------------------------------------------------------------------------- cards
TEX = {}


def tex(texid):
    if texid not in TEX:
        ns, path = texid.split(':')
        im = Image.open(RP / f'assets/{ns}/textures/{path}.png').convert('RGBA')
        TEX[texid] = np.asarray(im).astype(float) / 255
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
    """[(P0, P1, P2, (u0, u1, v0, v1)), ...]: local points at texture (u0,v0), (u1,v0), (u0,v1); v up"""
    plane, _px, (a0, a1, b0, b1), _n, texid, _d = G.kind_info(kind)
    P = lambda x, y, z: np.array([x, y, z], float)       # noqa: E731
    full = (0, 1, 0, 1)
    if plane == 'face':
        q = [(P(-a0, b0, 0), P(-a1, b0, 0), P(-a0, b1, 0), full)]
    elif plane == 'flat':
        q = [(P(-a0, 0, b0), P(-a1, 0, b0), P(-a0, 0, b1), full)]
    elif plane == 'cross':
        q = [(P(-a0, b0, 0), P(-a1, b0, 0), P(-a0, b1, 0), full), (P(0, b0, a0), P(0, b0, a1), P(0, b1, a0), full)]
    elif plane == 'lance':
        q = [(P(-a0, 0, b0), P(-a1, 0, b0), P(-a0, 0, b1), full), (P(0, a0, b0), P(0, a1, b0), P(0, a0, b1), full)]
    elif plane == 'wave':
        q = [(P(-a0, b0, 0), P(-a1, b0, 0), P(-a0, b1, 0), full), (P(-a0, 0, b0), P(-a1, 0, b0), P(-a0, 0, b1), full)]
    elif plane == 'band':
        q = [(P(-a0, 0, b0), P(-a1, 0, b0), P(-a0, 0, b1), (0, 1, 0.5, 1)),
             (P(-a0, 0, b1), P(-a1, 0, b1), P(-a0, G.WALL_H, b1), (0, 1, 0, 0.5))]
    elif plane == 'box':
        hx, hy, hz = G.BOX
        q = [(P(hx, hy, -hz), P(-hx, hy, -hz), P(hx, hy, hz), full), (P(hx, -hy, -hz), P(-hx, -hy, -hz), P(hx, -hy, hz), full),
             (P(hx, -hy, hz), P(-hx, -hy, hz), P(hx, hy, hz), full), (P(hx, -hy, -hz), P(-hx, -hy, -hz), P(hx, hy, -hz), full),
             (P(hx, -hy, -hz), P(hx, -hy, hz), P(hx, hy, -hz), full), (P(-hx, -hy, -hz), P(-hx, -hy, hz), P(-hx, hy, -hz), full)]
    else:
        raise ValueError(plane)
    return q, texid


def _vec(v):
    return np.array([float(x) for x in v], float)


def _aa(r, default_axis=(0, 0, 1)):
    """an SNBT rotation (axis-angle {angle, axis} or a quaternion [x, y, z, w]) as (angle, axis)"""
    if isinstance(r, dict):
        return float(r['angle']), tuple(float(v) for v in r['axis'])
    x, y, z, w = (float(v) for v in r)
    w = max(-1.0, min(1.0, w))
    ang = 2 * math.acos(w)
    sn = math.sqrt(max(0.0, 1 - w * w))
    if sn < 1e-9:
        return 0.0, default_axis
    return ang, (x / sn, y / sn, z / sn)


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
        col = comp.get('minecraft:custom_model_data', {}).get('colors', [0xFFFFFF])[0]   # the item default: white
        start, target, g0, d = cur, None, 0, 0

        def at(tt):
            if target is None:
                return start
            f = 1.0 if d <= 0 else min(1.0, max(0.0, (tt - g0) / d))
            out = {k: start[k] + (target[k] - start[k]) * f for k in ('t', 's', 'spin', 'roll')}
            out['ax'], out['lax'] = target['ax'], target['lax']
            return out
        for gg, ev in sorted((gg, ev) for gg, i, ev in s.events if i == e.id):
            if gg > t:
                break
            if ev == 'hit':
                if cd.get('knC', -1) >= 0:
                    col = cd['knC']
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
        if np.allclose(st['s'], 0):
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
        return [([self.pos + E @ (st['t'] + M @ p) for p in (A, B, C)], uv, self.col, texid) for A, B, C, uv in qs]


class StaticCard(SimCard):
    """a card placed by hand (sprite sheets): kind, position, yaw / pitch, uniform or xyz scale, tint"""

    def __init__(self, kind, pos, yaw=0.0, pitch=0.0, scale=1.0, col=0xFFFFFF, bb='fixed', spin=0.0):
        self.kind, self.pos, self.yaw, self.pitch, self.bb, self.col = kind, np.array(pos, float), yaw, pitch, bb, col
        sc = np.array(scale if isinstance(scale, (list, tuple)) else (scale,) * 3, float)
        self.st = {'t': np.zeros(3), 's': sc, 'spin': spin, 'ax': (0, 1, 0), 'roll': 0.0}


class Cam:
    def __init__(self, pos, yaw, pitch, w, h, fov=70.0, ortho=None):
        self.pos, self.yaw, self.pitch, self.w, self.h, self.ortho = np.array(pos, float), yaw, pitch, w, h, ortho
        y, p = math.radians(yaw), math.radians(pitch)
        self.F = np.array([-math.sin(y) * math.cos(p), -math.sin(p), math.cos(y) * math.cos(p)])
        self.R = np.cross(self.F, [0, 1, 0])
        self.R /= np.linalg.norm(self.R)
        self.U = np.cross(self.R, self.F)
        self.f = (h / 2) / math.tan(math.radians(fov) / 2)

    def rays(self):
        i, j = np.meshgrid(np.arange(self.w) + 0.5, np.arange(self.h) + 0.5)
        if self.ortho:
            x = (i - self.w / 2) / self.ortho
            y = (self.h / 2 - j) / self.ortho
            O = self.pos + x[..., None] * self.R + y[..., None] * self.U
            return O, np.broadcast_to(self.F, O.shape)
        x = (i - self.w / 2) / self.f
        y = (self.h / 2 - j) / self.f
        D = self.F + x[..., None] * self.R + y[..., None] * self.U
        D = D / np.linalg.norm(D, axis=-1, keepdims=True)
        return np.broadcast_to(self.pos, D.shape), D

    def project(self, P):
        rel = np.array(P, float) - self.pos
        if self.ortho:
            return self.w / 2 + (rel @ self.R) * self.ortho, self.h / 2 - (rel @ self.U) * self.ortho
        dep = rel @ self.F
        return self.w / 2 + (rel @ self.R) / dep * self.f, self.h / 2 - (rel @ self.U) / dep * self.f


def look_at(pos, tgt):
    d = np.array(tgt, float) - np.array(pos, float)
    return math.degrees(math.atan2(-d[0], d[2])), -math.degrees(math.atan2(d[1], math.hypot(d[0], d[2])))


def top_cam(centre, size, px):
    return Cam((centre[0], FY + 40, centre[2]), 0.0, 89.99, px, px, ortho=px / size)


def view_cam(eye, tgt, w, h, fov=70):
    yaw, pitch = look_at(eye, tgt)
    return Cam(eye, yaw, pitch, w, h, fov=fov)


# ----------------------------------------------------------------------------- particles
PART_LOOK = {   # size, colour, alpha, drift / tick, life
    'end_rod': (0.10, (1.0, 1.0, 0.94), 0.95, 0.0, 30), 'happy_villager': (0.10, (0.45, 0.85, 0.35), 0.95, 0.0, 16),
    'wax_on': (0.08, (0.96, 0.72, 0.25), 1.0, 0.0, 15), 'explosion': (1.3, (0.92, 0.92, 0.88), 0.45, 0.0, 8),
    'crit': (0.08, (0.95, 0.92, 0.85), 1.0, 0.0, 10), 'composter': (0.08, (0.55, 0.75, 0.25), 1.0, 0.0, 14),
    'spore_blossom_air': (0.05, (0.85, 0.55, 0.8), 0.8, 0.0, 40), 'smoke': (0.2, (0.3, 0.3, 0.3), 0.6, 0.03, 16),
    'small_flame': (0.08, (1.0, 0.72, 0.25), 0.9, 0.012, 12), 'firework': (0.07, (1.0, 1.0, 0.95), 1.0, 0.0, 12),
    'bubble_pop': (0.1, (0.8, 0.95, 1.0), 0.7, 0.0, 6), 'white_ash': (0.05, (0.9, 0.9, 0.9), 0.9, 0.0, 30),
    'sweep_attack': (1.2, (0.95, 0.95, 0.95), 0.5, 0.0, 6), 'lava': (0.16, (1.0, 0.45, 0.1), 1.0, 0.05, 16),
    'flame': (0.15, (1.0, 0.62, 0.18), 0.9, 0.012, 12), 'falling_honey': (0.08, (0.95, 0.7, 0.2), 1.0, -0.06, 20),
    'dripping_honey': (0.08, (0.95, 0.7, 0.2), 1.0, -0.02, 20), 'electric_spark': (0.07, (0.85, 0.95, 1.0), 1.0, 0.0, 8),
    'splash': (0.1, (0.7, 0.85, 1.0), 0.8, -0.04, 10), 'block': (0.12, (0.42, 0.33, 0.24), 1.0, -0.04, 20),
}


class Dot:
    def __init__(self, pos, vel, size, c0, c1, alpha, drift, life, t0):
        self.pos, self.vel, self.size, self.c0, self.c1 = np.array(pos, float), np.array(vel, float), size, c0, c1
        self.alpha, self.drift, self.life, self.t0 = alpha, drift, life, t0

    def draw(self, img, cam, t, depth):
        tt = t - self.t0
        if tt < 0 or tt >= self.life:
            return
        P = self.pos + self.vel * tt * 0.85 ** tt + np.array([0, self.drift * tt, 0])
        rel = P - cam.pos
        dep = rel @ cam.F
        if dep <= 0.05:
            return
        if cam.ortho:
            sx, sy, rad = rel @ cam.R * cam.ortho, rel @ cam.U * cam.ortho, self.size / 2 * cam.ortho
        else:
            sx, sy, rad = (rel @ cam.R) / dep * cam.f, (rel @ cam.U) / dep * cam.f, self.size / 2 / dep * cam.f
        x, y = cam.w / 2 + sx, cam.h / 2 - sy
        rad = max(rad, 0.7)
        rr = 1.2 * rad + 1          # the soft dot reaches 1.2 rad
        x0, x1 = int(max(0, x - rr)), int(min(cam.w, x + rr + 1))
        y0, y1 = int(max(0, y - rr)), int(min(cam.h, y + rr + 1))
        if x0 >= x1 or y0 >= y1:
            return
        if np.linalg.norm(rel) > depth[int(min(cam.h - 1, max(0, y))), int(min(cam.w - 1, max(0, x)))] + 0.05:
            return
        yy, xx = np.mgrid[y0:y1, x0:x1]
        d = np.hypot(xx + 0.5 - x, yy + 0.5 - y) / rad
        f = 1 - tt / max(1, self.life)
        a = np.clip(1.2 - d, 0, 1) ** 1.5 * self.alpha * (0.4 + 0.6 * f)
        c = np.array(self.c0) + (np.array(self.c1) - np.array(self.c0)) * (1 - f)
        img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a[..., None]) + c * a[..., None]


def dots(s, seed=1):
    out = []
    rnd = random.Random(seed)
    for gt, name, nbt, p0, dx, dy, dz, sp, n in s.parts:
        if name in ('dust', 'dust_color_transition', 'flash'):
            cols = [tuple(float(v.rstrip('f')) for v in c.split(','))[:3] for c in re.findall(r'\[([^\]]*)\]', nbt)]
            cols = cols or [(1.0, 1.0, 1.0)]
            sc = re.search(r'scale:([-\d.]+)', nbt)
            sc = float(sc.group(1)) if sc else 1.0
            look = (0.11 * sc * 1.6, cols[0], 0.95 if name != 'flash' else 0.5, 0.0, 14 if name != 'flash' else 3)
            c1 = cols[1] if len(cols) > 1 else cols[0]
            if name == 'flash':
                look = (1.6, cols[0], 0.45, 0.0, 3)
        else:
            look = PART_LOOK.get(name, (0.1, (1.0, 1.0, 1.0), 0.8, 0.0, 12))
            c1 = look[1]
        size, c0, alpha, drift, life = look
        for _k in range(min(n, 40)):
            off = np.array([rnd.gauss(0, 1) * dx, rnd.gauss(0, 1) * dy, rnd.gauss(0, 1) * dz])
            vel = np.array([rnd.gauss(0, 1), rnd.gauss(0, 1), rnd.gauss(0, 1)]) * sp
            out.append(Dot(p0 + off, vel, size * rnd.uniform(0.7, 1.2), c0, c1, alpha, drift,
                           int(life * rnd.uniform(0.6, 1.2)), gt))
    return out


# ----------------------------------------------------------------------------- the ray caster
def render(cam, cards, t, look='withered', bg=(0.62, 0.68, 0.52), dts=(), floor=True, extra=None):
    O, D = cam.rays()
    img = np.zeros((cam.h, cam.w, 3)) + np.array(bg)
    depth = np.full((cam.h, cam.w), np.inf)
    if floor:
        with np.errstate(divide='ignore', invalid='ignore'):
            tf = (FY - O[..., 1]) / D[..., 1]
        m = np.isfinite(tf) & (tf > 0)
        H = O + D * np.where(m, tf, 0)[..., None]
        img[m] = floor_colour(H[..., 0][m], H[..., 2][m], look)
        if look == 'withered':          # a dim yellow haze with distance, as in the footage
            fog = np.clip((tf[m] - 10) / 40, 0, 0.55)[:, None]
            img[m] = img[m] * (1 - fog) + np.array([0.70, 0.72, 0.42]) * fog
        else:
            fog = np.clip((tf[m] - 10) / 40, 0, 0.55)[:, None]
            img[m] = img[m] * (1 - fog) + np.array([0.55, 0.80, 0.62]) * fog
        depth[m] = tf[m]
    if extra is not None:
        extra(img, cam, depth)
    items = []
    for c in cards:
        for (C0, C1, C2), uv, col, texid in c.quads(cam):
            A, B = C1 - C0, C2 - C0
            N = np.cross(A, B)
            if np.linalg.norm(N) < 1e-9:
                continue
            centre = C0 + 0.5 * A + 0.5 * B
            key = np.linalg.norm(centre - cam.pos) if not cam.ortho else -centre[1]
            items.append((key, texid, C0, A, B, N, uv, col))
    items.sort(key=lambda x: -x[0])
    for _d, texid, C0, A, B, N, (u0, u1, v0, v1), col in items:
        dn = D @ N
        with np.errstate(divide='ignore', invalid='ignore'):
            tt = ((C0 - O) @ N) / dn
        Hp = O + D * np.nan_to_num(tt)[..., None]
        rel = Hp - C0
        BN, NA = np.cross(B, N), np.cross(N, A)
        u = (rel @ BN) / (A @ BN)
        v = (rel @ NA) / (B @ NA)
        ok = np.isfinite(tt) & (tt > 0) & (u >= 0) & (u < 1) & (v >= 0) & (v < 1) & (tt < depth + 1e-3)
        if not ok.any():
            continue
        T = tex(texid)
        th, tw = T.shape[:2]
        uu = u0 + u[ok] * (u1 - u0)
        vv = v0 + v[ok] * (v1 - v0)
        px = np.clip((uu * tw).astype(int), 0, tw - 1)
        py = np.clip(((1 - vv) * th).astype(int), 0, th - 1)
        smp = T[py, px]
        a = smp[:, 3]
        keep = a >= 0.1
        tint = np.array([(col >> 16) & 255, (col >> 8) & 255, col & 255]) / 255
        rgb = smp[:, :3] * tint
        idx = np.argwhere(ok)[keep]
        a = a[keep][:, None]
        img[idx[:, 0], idx[:, 1]] = img[idx[:, 0], idx[:, 1]] * (1 - a) + rgb[keep] * a
    for d in dts:
        d.draw(img, cam, t, depth)
    return Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))




def sim_cards(s):
    out = []
    for e in s.ents:
        if e.etype != 'item_display' or e.id not in s.nbt:
            continue
        comp = s.nbt[e.id].get('item', {}).get('components', {})
        if not str(comp.get('minecraft:item_model', '')).startswith(('rlk:mboss/kn_kit/', 'rlk:mboss/fg_kit/')):
            continue
        n = s.nbt[e.id]
        n.setdefault('transformation', {'translation': [0, 0, 0], 'left_rotation': [0, 0, 0, 1], 'scale': [1, 1, 1],
                                        'right_rotation': [0, 0, 0, 1]})
        out.append(SimCard(s, e, s.gt))
    return out
