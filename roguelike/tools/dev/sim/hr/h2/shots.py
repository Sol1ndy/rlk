#!/usr/bin/env python3
"""shots.py: what each camera of 홍련's cutscenes sees (lane H2; hr_design §6.2 "rendered shot sheets"): a small software
renderer of the real arena blocks (the theme's own layout, tools/mboss_arena_hr_field.py arena_layout) with stand-in
figures for her and the actor, a frame per shot, and the framing checks test_seq.py runs on the same pictures.

    python3 shots.py <datapack root> <out dir> [sequence ...] [--stage c|n|e|s|w] [--w 320]

The camera pose is the live stand's real position and rotation after the sequence's own functions ran in the lane's
world (seqsim: the stage, her body moves, the clamp into the walk disc). Field of view 70 degrees vertical, 16 : 9.
Stand-ins: her = a body box in the posture of the beat (sitting / standing / crouched / lying; her hat as a wide slab),
the actor = a body box at the stage origin + the design's displacement table (§4.2), the seat rock while it is there.
Scratch tool, never shipped. Needs numpy and Pillow.
"""
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
FOV_V = 70.0
ASPECT = 16 / 9

# ---- materials ----------------------------------------------------------------------------------------------------------
AIR, INVIS, PLANT, SOLID, WATER = 0, 1, 2, 3, 4
PAL = [  # (name fragment, rgb, class) - first match wins
    ('barrier', (0, 0, 0), INVIS), ('light', (0, 0, 0), None), ('air', (0, 0, 0), AIR),
    ('short_dry_grass', (176, 150, 104), PLANT), ('tall_dry_grass', (186, 160, 110), PLANT), ('crimson_roots', (140, 30, 50), PLANT),
    ('dead_bush', (120, 90, 50), PLANT), ('fern', (70, 110, 60), PLANT), ('lily_pad', (40, 110, 50), PLANT),
    ('dripleaf', (90, 140, 60), PLANT), ('bamboo', (100, 150, 60), PLANT), ('vine', (60, 100, 40), PLANT),
    ('moss_carpet', (90, 110, 45), SOLID), ('pale_moss', (190, 196, 182), SOLID), ('moss', (90, 110, 45), SOLID),
    ('clay', (160, 166, 179), SOLID), ('dirt', (134, 96, 67), SOLID),
    ('water', (50, 80, 150), WATER), ('mycelium', (118, 100, 118), SOLID), ('coarse_dirt', (120, 86, 60), SOLID),
    ('crimson_nylium', (130, 30, 34), SOLID), ('nether_wart', (115, 8, 10), SOLID), ('crimson_planks', (100, 48, 70), SOLID),
    ('tuff', (108, 110, 102), SOLID), ('deepslate', (80, 80, 84), SOLID), ('packed_mud', (142, 106, 80), SOLID),
    ('mud', (60, 58, 62), SOLID), ('podzol', (92, 64, 30), SOLID), ('cherry_leaves', (236, 170, 205), SOLID),
    ('cherry', (60, 34, 44), SOLID), ('spruce_leaves', (40, 66, 44), SOLID), ('dark_oak_leaves', (36, 60, 30), SOLID),
    ('leaves', (50, 80, 40), SOLID), ('spruce', (58, 38, 20), SOLID), ('dark_oak', (50, 34, 18), SOLID),
    ('light_blue_terracotta', (113, 108, 137), SOLID), ('blue_terracotta', (74, 59, 91), SOLID),
    ('black_terracotta', (37, 22, 16), SOLID), ('gray_terracotta', (57, 42, 35), SOLID), ('purple_terracotta', (118, 70, 86), SOLID),
    ('red_terracotta', (143, 61, 46), SOLID), ('terracotta', (120, 80, 70), SOLID),
    ('white_concrete', (214, 218, 220), SOLID), ('light_gray_concrete', (125, 125, 115), SOLID), ('pink_concrete', (213, 101, 142), SOLID),
    ('red_concrete', (142, 32, 32), SOLID), ('snow', (249, 254, 254), SOLID), ('pearlescent_froglight', (245, 240, 239), SOLID),
    ('ochre_froglight', (250, 245, 206), SOLID), ('froglight', (240, 240, 220), SOLID), ('cobble', (127, 127, 127), SOLID),
    ('stone', (125, 125, 125), SOLID), ('andesite', (136, 136, 136), SOLID), ('calcite', (223, 224, 220), SOLID),
    ('lantern', (230, 190, 110), SOLID), ('iron_bars', (130, 130, 130), PLANT), ('wall', (120, 120, 116), SOLID),
    ('black_concrete', (8, 10, 15), SOLID), ('obsidian', (15, 10, 24), SOLID),
]


def material(name):
    n = name.replace('minecraft:', '').split('[')[0]
    if n in ('air', 'cave_air', 'void_air'):
        return (0, 0, 0), AIR
    if n == 'light':
        return (0, 0, 0), AIR
    for frag, rgb, cls in PAL:
        if frag in n and cls is not None:
            return rgb, cls
    return (150, 60, 200), SOLID            # unknown: a loud purple


class Arena:
    def __init__(self, dp, look='moon'):
        sys.path.insert(0, str(Path(dp) / 'tools'))
        import mboss_arena_hr_field as T
        self.T = T
        lay = T.arena_layout(look)
        bx = T.BOX
        self.x0, self.y0, self.z0 = bx['x0'], bx['y0'], bx['z0']
        self.shape = (bx['x1'] - bx['x0'] + 1, bx['y1'] - bx['y0'] + 1, bx['z1'] - bx['z0'] + 1)
        names = sorted({v for v in lay.values()})
        mats = [material(n) for n in names]
        self.rgb = np.array([(0, 0, 0)] + [m[0] for m in mats], dtype=np.float32)
        self.cls = np.array([AIR] + [m[1] for m in mats], dtype=np.uint8)
        self.names = ['air'] + names
        idx = {n: i + 1 for i, n in enumerate(names)}
        self.vox = np.zeros(self.shape, dtype=np.uint16)
        for (x, y, z), b in lay.items():
            if bx['x0'] <= x <= bx['x1'] and bx['y0'] <= y <= bx['y1'] and bx['z0'] <= z <= bx['z1']:
                self.vox[x - self.x0, y - self.y0, z - self.z0] = idx[b]
        self.unknown = sorted({n for n, m in zip(names, mats) if m[0] == (150, 60, 200)})

    def cell(self, p):
        """(block name, class) of the cell holding point p."""
        i = (math.floor(p[0]) - self.x0, math.floor(p[1]) - self.y0, math.floor(p[2]) - self.z0)
        if not all(0 <= i[k] < self.shape[k] for k in range(3)):
            return 'outside', SOLID
        v = int(self.vox[i])
        return self.names[v], int(self.cls[v])

    def sample(self, P):
        """Material indices of points P (N, 3); outside the box: -1."""
        I = np.floor(P).astype(np.int64) - np.array([self.x0, self.y0, self.z0])
        ok = np.all((I >= 0) & (I < np.array(self.shape)), axis=1)
        out = np.full(len(P), -1, dtype=np.int64)
        J = I[ok]
        out[ok] = self.vox[J[:, 0], J[:, 1], J[:, 2]]
        return out


# ---- camera ---------------------------------------------------------------------------------------------------------------
def cam_basis(yaw, pitch):
    y, p = math.radians(yaw), math.radians(pitch)
    f = np.array([-math.sin(y) * math.cos(p), -math.sin(p), math.cos(y) * math.cos(p)])
    left = np.array([math.cos(y), 0.0, math.sin(y)])
    up = np.cross(f, left)
    return f, -left, up


def rays(yaw, pitch, w, h):
    f, r, u = cam_basis(yaw, pitch)
    tv = math.tan(math.radians(FOV_V) / 2)
    th = tv * ASPECT
    xs = (np.arange(w) + 0.5) / w * 2 - 1
    ys = 1 - (np.arange(h) + 0.5) / h * 2
    X, Y = np.meshgrid(xs, ys)
    D = f[None, None, :] + X[..., None] * th * r[None, None, :] + Y[..., None] * tv * u[None, None, :]
    D /= np.linalg.norm(D, axis=2, keepdims=True)
    return D.reshape(-1, 3)


def project(eye, yaw, pitch, p):
    """(sx, sy, depth) of world point p: sx / sy in -1..1 (right / up), depth along the view axis (<= 0: behind)."""
    f, r, u = cam_basis(yaw, pitch)
    d = np.array(p, dtype=float) - np.array(eye, dtype=float)
    z = float(d @ f)
    if z <= 1e-6:
        return None, None, z
    tv = math.tan(math.radians(FOV_V) / 2)
    return float(d @ r) / (z * tv * ASPECT), float(d @ u) / (z * tv), z


# ---- figures (oriented boxes) -----------------------------------------------------------------------------------------------
def box(center, size, yaw, rgb, tag):
    return dict(c=np.array(center, dtype=float), s=np.array(size, dtype=float) / 2, yaw=yaw, rgb=np.array(rgb, dtype=np.float32), tag=tag)


def fig_boxes(kind, pos, yaw, posture='stand'):
    """Stand-in boxes of a figure at feet `pos` facing `yaw`. kind 'her' (with the hat) / 'actor'."""
    x, y, z = pos
    f = (-math.sin(math.radians(yaw)), math.cos(math.radians(yaw)))
    her = kind == 'her'
    body = (58, 44, 92) if her else (214, 196, 150)
    head = (236, 206, 190) if her else (240, 214, 190)
    hat = (188, 60, 78)
    out = []
    if posture == 'lie':
        # on the back, the head away along -facing ... the design: head toward +f of the stage = behind her facing
        cx, cz = x - f[0] * 0.75, z - f[1] * 0.75
        out.append(box((cx, y + 0.2, cz), (0.6, 0.4, 1.5), yaw, body, kind))
        out.append(box((x - f[0] * 1.7, y + 0.25, z - f[1] * 1.7), (0.5, 0.5, 0.5), yaw, head, kind + '_head'))
        return out
    h = {'stand': 2.0, 'sit': 1.62, 'crouch': 1.3, 'kneel': 1.25}[posture]
    out.append(box((x, y + (h - 0.5) / 2, z), (0.55, h - 0.5, 0.3), yaw, body, kind))
    out.append(box((x, y + h - 0.25, z), (0.5, 0.5, 0.5), yaw, head, kind + '_head'))
    if her:
        out.append(box((x, y + h + 0.03, z), (1.32, 0.06, 1.32), yaw, hat, 'her_hat'))
        out.append(box((x, y + h + 0.18, z), (0.5, 0.3, 0.5), yaw, hat, 'her_hat'))
    else:
        out.append(box((x - f[1] * -0.38 + f[0] * 0.25, y + 1.0, z + f[0] * -0.38 + f[1] * 0.25), (0.08, 0.08, 1.2), yaw, (230, 230, 240), 'sword'))
    return out


def box_dist(eye, b):
    """The distance from a point to an oriented box (0 inside it)."""
    a = math.radians(b['yaw'])
    ca, sa = math.cos(a), math.sin(a)
    o = np.array(eye, dtype=float) - b['c']
    q = np.array([o[0] * ca + o[2] * sa, o[1], -o[0] * sa + o[2] * ca])
    return float(np.linalg.norm(np.maximum(np.abs(q) - b['s'], 0.0)))


def hit_boxes(eye, D, boxes):
    """Nearest box hit per ray: (t, index) with t = inf where none."""
    n = len(D)
    best = np.full(n, np.inf)
    who = np.full(n, -1, dtype=np.int64)
    for i, b in enumerate(boxes):
        a = math.radians(b['yaw'])
        ca, sa = math.cos(a), math.sin(a)
        # world -> box frame (x = right, z = forward of the yaw)
        o = np.array(eye, dtype=float) - b['c']
        ox, oz = o[0] * ca + o[2] * sa, -o[0] * sa + o[2] * ca
        dx, dz = D[:, 0] * ca + D[:, 2] * sa, -D[:, 0] * sa + D[:, 2] * ca
        O = np.array([ox, o[1], oz])
        DD = np.stack([dx, D[:, 1], dz], axis=1)
        with np.errstate(divide='ignore', invalid='ignore'):
            t1 = (-b['s'][None, :] - O[None, :]) / DD
            t2 = (b['s'][None, :] - O[None, :]) / DD
        lo = np.nanmax(np.minimum(t1, t2), axis=1)
        hi = np.nanmin(np.maximum(t1, t2), axis=1)
        ok = (hi >= lo) & (hi > 0.02)
        t = np.where(lo > 0.02, lo, hi)
        t = np.where(ok, t, np.inf)
        upd = t < best
        best[upd] = t[upd]
        who[upd] = i
    return best, who


# ---- render -----------------------------------------------------------------------------------------------------------------
def render(arena, eye, yaw, pitch, boxes=(), w=320, h=180, far=120.0):
    """(rgb uint8 [h, w, 3], depth [h, w], who [h, w]): who = -1 voxel / sky, else the box index; plants are stippled."""
    D = rays(yaw, pitch, w, h)
    n = len(D)
    eye = np.array(eye, dtype=float)
    depth = np.full(n, np.inf)
    mat = np.zeros(n, dtype=np.int64)
    axis = np.zeros(n, dtype=np.int64)
    alive = np.ones(n, dtype=bool)
    pix = np.arange(n)
    stip = ((pix % w) + (pix // w)) % 2 == 0
    step = 0.25
    t = np.full(n, 0.05)
    prev = np.floor(eye[None, :] + D * 0.05).astype(np.int64)
    k = 0
    while alive.any() and k < int(far / step):
        k += 1
        ia = np.nonzero(alive)[0]
        t[ia] += step
        P = eye[None, :] + D[ia] * t[ia, None]
        m = arena.sample(P)
        cls = np.where(m >= 0, arena.cls[np.maximum(m, 0)], SOLID)
        cellidx = np.floor(P).astype(np.int64)
        ax = np.argmax(cellidx != prev[ia], axis=1)
        prev[ia] = cellidx
        vis = (cls == SOLID) | (cls == WATER) | ((cls == PLANT) & stip[ia])
        hit = ia[vis]
        depth[hit] = t[hit]
        mat[hit] = m[vis]
        axis[hit] = ax[vis]
        alive[hit] = False
    rgb = np.zeros((n, 3), dtype=np.float32)
    got = np.isfinite(depth)
    mm = mat[got]
    col = np.where((mm >= 0)[:, None], arena.rgb[np.maximum(mm, 0)], np.array([[20, 22, 40]], dtype=np.float32))
    shade = np.array([0.82, 1.0, 0.66])[axis[got]]
    fog = np.clip(depth[got] / 90.0, 0, 1)[:, None]
    rgb[got] = col * shade[:, None] * (1 - 0.35 * fog) + np.array([[40, 44, 70]]) * 0.35 * fog
    rgb[~got] = (14, 16, 30)
    who = np.full(n, -1, dtype=np.int64)
    if boxes:
        tb, wb = hit_boxes(eye, D, list(boxes))
        front = tb < depth
        cols = np.stack([b['rgb'] for b in boxes])
        shade_b = 0.75 + 0.25 * np.clip(-D[:, 1] + 0.5, 0, 1)
        rgb[front] = cols[wb[front]] * shade_b[front, None]
        depth[front] = tb[front]
        who[front] = wb[front]
    return np.clip(rgb, 0, 255).astype(np.uint8).reshape(h, w, 3), depth.reshape(h, w), who.reshape(h, w)


def visible_fraction(who, boxes, tags):
    """The share of the frame's pixels showing boxes whose tag is in `tags`."""
    idx = [i for i, b in enumerate(boxes) if b['tag'] in tags]
    return float(np.isin(who, idx).mean()) if idx else 0.0


def alone_fraction(eye, yaw, pitch, boxes, w, h):
    """The share of the frame the boxes would fill with nothing before them (and no frame edge clipping them less)."""
    if not boxes:
        return 0.0
    tb, _wb = hit_boxes(eye, rays(yaw, pitch, w, h), list(boxes))
    return float(np.isfinite(tb).mean())


def ray_clear(arena, eye, target, boxes=(), skip_tags=(), margin=0.25, solid_only=False):
    """What a ray from the eye meets before `target`: None when clear, else ('block', name, distance) / ('box', tag, distance).
    The last `margin` blocks before the target are not counted (the target's own surface)."""
    eye = np.array(eye, dtype=float)
    d = np.array(target, dtype=float) - eye
    dist = float(np.linalg.norm(d))
    if dist < 1e-6:
        return None
    d /= dist
    ts = np.arange(0.05, max(0.05, dist - margin), 0.05)
    if len(ts):
        P = eye[None, :] + d[None, :] * ts[:, None]
        m = arena.sample(P)
        cls = np.where(m >= 0, arena.cls[np.maximum(m, 0)], SOLID)
        bad = np.nonzero((cls == SOLID) if solid_only else ((cls == SOLID) | (cls == PLANT) | (cls == WATER)))[0]
        if len(bad):
            i = bad[0]
            return ('block', arena.names[m[i]] if m[i] >= 0 else 'outside', round(float(ts[i]), 2))
    bs = [b for b in boxes if b['tag'] not in skip_tags]
    if bs:
        tb, wb = hit_boxes(eye, d[None, :], bs)
        if tb[0] < dist - margin:
            return ('box', bs[int(wb[0])]['tag'], round(float(tb[0]), 2))
    return None


def sheet(frames, path, cols=3, w=320, h=180, title=''):
    """A contact sheet: frames = [(label, rgb array)]."""
    from PIL import Image, ImageDraw
    rows = math.ceil(len(frames) / cols)
    pad = 14
    img = Image.new('RGB', (cols * w, rows * (h + pad) + (pad if title else 0)), (12, 12, 16))
    dr = ImageDraw.Draw(img)
    y0 = pad if title else 0
    if title:
        dr.text((4, 1), title, fill=(255, 230, 150))
    for i, (label, arr) in enumerate(frames):
        x, y = (i % cols) * w, y0 + (i // cols) * (h + pad)
        img.paste(Image.fromarray(arr), (x, y + pad))
        dr.text((x + 3, y + 1), label[:52], fill=(235, 235, 235))
    img.save(path, quality=88)
    return path
