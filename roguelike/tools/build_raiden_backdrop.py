"""Backdrop panels of the Narukami arena (Plane of Euthymia): painted textures, item models, item definitions.

Run alone:  python tools/build_raiden_backdrop.py --resourcepack <unpacked resource pack>
(build_raiden_all.py runs it; build_raiden_arena.py imports ENTITIES to summon the panels.)

Pure standard library and deterministic (fixed seeds, fixed zlib level), so two runs write identical bytes.
Writes <rp>/assets/rlk/textures/raiden/arena/<tex>.png, models/item/raiden/arena/<model>.json,
items/raiden/arena/<model>.json and appends each sprite to assets/minecraft/atlases/items.json (sprites of this
folder that are no longer painted are pruned; other atlas entries are never touched).

THE BACKDROP (world space; arena centre (0, 201, 0), the vortex on the north = -z side):
  sky_cove   4 entities x 4 quads: a 16-sided ring of star cards tilted 22.5 deg outward (r 53..59, y 209..224)
  sky_top    1 entity, 16 down-facing star cards under the dome top (y 227.4)
  fog_ring   4 entities x 4 quads: a 16-sided ring of horizon-mist cards tilted 45 deg (r 46..56, y 201..211)
  vortex_glow, vortex   the cyan vortex rising from the north horizon (glow halo behind, the swirl in front, turning)
  wisps      a low mist band at the vortex foot and two mist arcs hugging its rim
VANILLA RULES THAT SHAPED IT (see build_raiden_fx_textures.py for the long form):
  * item_display turns item models 180 deg about y; right_rotation [0,1,0,0] undoes it, so a model unit u lands at
    pos + translation + left_rotation * scale * (u / 16 - 0.5).
  * Entity items get the level's diffuse light by face normal (ambient 0.4 + 0.6 * the two sun-like directions):
    a card facing straight down shows at 0.4, a vertical card at 0.5..0.74, a card tilted >= 40 deg toward the sky at
    1.0. Hence the mist ring leans back 45 deg, the star ring 22.5 deg, the vortex 20 deg; only the zenith stars
    (down-facing) are dim, which suits the dark top of the sky.
  * Alpha < 0.1 is discarded; partial alpha goes to the translucent sheet (centroid-sorted, depth-written), so cards
    that overlap from the usual eye points are ordered far -> near by design (stars behind the vortex, the vortex
    behind the wisps and the mist ring).
  * Element rotations are single-axis multiples of 22.5 deg within +-45 and coordinates stay in -16..32; the 16-sided
    rings are four entities turned 0 / 22.5 / 45 / 67.5 deg, each carrying an N / E / S / W card.
TEXTURE BUDGET: 413,696 px (vortex 512^2, stars 256^2, wisps 256^2, glow 128^2, fog 64^2), all in the item atlas.
"""
from pathlib import Path
import argparse
import json
import math
import struct
import zlib

TOOLS = Path(__file__).resolve().parent
NS_DIR = 'raiden/arena'          # textures/<NS_DIR>, models/item/<NS_DIR>, items/<NS_DIR>
SPRITE = 'rlk:' + NS_DIR + '/'   # atlas sprite prefix


# --------------------------------------------------------------------------------------------- PNG + noise helpers
class Img:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = [[0.0, 0.0, 0.0, 0.0] for _ in range(w * h)]

    def put(self, x, y, rgb, a):
        """Premultiplied 'over' compositing of colour rgb (0..1) with alpha a onto the pixel."""
        if a <= 0 or not (0 <= x < self.w and 0 <= y < self.h):
            return
        p = self.px[y * self.w + x]
        a = min(1.0, a)
        for k in range(3):
            p[k] = rgb[k] * a + p[k] * (1 - a)
        p[3] = a + p[3] * (1 - a)

    def png(self):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            for x in range(self.w):
                r, g, b, a = self.px[y * self.w + x]
                if a < 0.1:                    # discarded in game anyway: keep the file clean
                    raw += b'\x00\x00\x00\x00'
                    continue
                # stored straight (not premultiplied)
                raw += bytes((_b(r / a), _b(g / a), _b(b / a), _b(a)))

        def chunk(kind, data):
            return (struct.pack('>I', len(data)) + kind + data
                    + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff))
        return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 6, 0, 0, 0))
                + chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b''))


def _b(v):
    return max(0, min(255, int(round(v * 255))))


def _hash(ix, iy, seed):
    h = (ix * 374761393 + iy * 668265263 + seed * 2147483647) & 0xffffffff
    h = ((h ^ (h >> 13)) * 1274126177) & 0xffffffff
    return ((h ^ (h >> 16)) & 0xffff) / 65535.0


def vnoise(x, y, seed):
    """Smooth value noise in 0..1."""
    ix, iy = math.floor(x), math.floor(y)
    fx, fy = x - ix, y - iy
    sx, sy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b = _hash(ix, iy, seed), _hash(ix + 1, iy, seed)
    c, d = _hash(ix, iy + 1, seed), _hash(ix + 1, iy + 1, seed)
    return (a + (b - a) * sx) + ((c + (d - c) * sx) - (a + (b - a) * sx)) * sy


def fbm(x, y, seed, oct=4):
    s, amp, tot = 0.0, 0.5, 0.0
    for o in range(oct):
        s += amp * vnoise(x, y, seed + o * 17)
        tot += amp
        x, y, amp = x * 2.03 + 11.7, y * 2.03 - 5.3, amp * 0.5
    return s / tot


def smooth(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def ramp(stops, t):
    """Colour ramp: stops = [(t, (r, g, b) 0..255), ...] -> rgb 0..1."""
    if t <= stops[0][0]:
        return tuple(c / 255 for c in stops[0][1])
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t <= t1:
            f = (t - t0) / (t1 - t0)
            return tuple((c0[k] + (c1[k] - c0[k]) * f) / 255 for k in range(3))
    return tuple(c / 255 for c in stops[-1][1])


# --------------------------------------------------------------------------------------------- painters
def paint_vortex():
    """512x512 swirl: white-hot core with a curling crest, two log-spiral arms of cyan mist, a soft teal rim."""
    N = 512
    im = Img(N, N)
    cols = [(0.0, (16, 70, 86)), (0.3, (34, 140, 168)), (0.55, (80, 205, 228)), (0.78, (170, 238, 248)),
            (0.95, (236, 252, 255)), (1.2, (255, 255, 255))]
    for j in range(N):
        v = (j + 0.5) / N * 2 - 1
        for i in range(N):
            u = (i + 0.5) / N * 2 - 1
            r = math.hypot(u, v)
            if r > 1.0:
                continue
            th = math.atan2(v, u)
            warp = fbm(u * 2.2 + 3.1, v * 2.2 - 1.7, 11, 4)
            mist = fbm(u * 5.0 - 2.0, v * 5.0 + 4.0, 23, 4)
            phase = 2.0 * th + 6.2 * math.log(r + 0.06) + 2.4 * warp
            arm = (0.5 + 0.5 * math.cos(phase)) ** 2.4
            env = smooth(0.97, 0.42, r)                # 1 inside 0.42, 0 at the rim
            core = math.exp(-(r / 0.12) ** 2)
            halo = math.exp(-(r / 0.42) ** 2)
            # the curling crest: a thin bright arc of the arm phase close to the core
            crest = math.exp(-((math.cos(phase - 0.9) - 1.0) / 0.10) ** 2) * smooth(0.06, 0.16, r) * smooth(0.46, 0.24, r)
            disc = smooth(0.40, 0.22, r)
            outer = arm * smooth(0.98, 0.5, r) * smooth(0.2, 0.45, r)
            I = (1.25 * core + 0.85 * crest + arm * env * (0.45 + 0.5 * mist) + 0.5 * halo + 0.32 * disc
                 + 0.45 * outer * mist + 0.16 * env * mist)
            rgb = ramp(cols, I)
            a = min(1.0, 0.18 + 0.95 * I) * smooth(1.0, 0.86, r)
            a *= 0.6 + 0.4 * smooth(0.9, 0.55, r)
            im.put(i, j, rgb, a)
    return im


def paint_glow():
    """128x128 radial cyan glow that brightens the sky behind the vortex (no structure; alpha <= 0.82)."""
    N = 128
    im = Img(N, N)
    for j in range(N):
        v = (j + 0.5) / N * 2 - 1
        for i in range(N):
            u = (i + 0.5) / N * 2 - 1
            r = math.hypot(u, v)
            g = math.exp(-(r / 0.62) ** 2) * smooth(1.0, 0.78, r)
            n = fbm(u * 3 + 7, v * 3 + 1, 41, 3)
            a = 0.82 * g * (0.75 + 0.35 * n)
            im.put(i, j, ramp([(0, (34, 132, 150)), (0.5, (76, 200, 220)), (1, (178, 242, 248))], g), a)
    return im


def paint_stars():
    """256x256 transparent star field: ~330 points (mostly 1 px), soft 3x3 glows, a few cross glints, rare pink."""
    N = 256
    im = Img(N, N)
    st = 12345
    for k in range(330):
        x = int(_hash(k, 1, st) * N)
        y = int(_hash(k, 2, st) * N)
        m = _hash(k, 3, st)                     # magnitude
        hue = _hash(k, 4, st)
        if hue > 0.94:
            c = (1.0, 0.78, 0.9)                # pink petal-stars of the Tenma shots
        elif hue > 0.6:
            c = (0.78, 0.95, 1.0)
        else:
            c = (1.0, 1.0, 1.0)
        b = 0.45 + 0.55 * m
        im.put(x, y, c, b)
        if m > 0.72:                            # soft 3x3 glow
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                im.put((x + dx) % N, (y + dy) % N, c, 0.32 * b)
        if m > 0.965:                           # cross glint
            for d in (2, 3):
                for dx, dy in ((d, 0), (-d, 0), (0, d), (0, -d)):
                    im.put((x + dx) % N, (y + dy) % N, c, 0.42 / d)
    return im


def paint_fog():
    """64x64 horizon mist card: dense pale teal at the bottom (v = 1) fading to nothing at the top, faint streaks."""
    N = 64
    im = Img(N, N)
    for j in range(N):
        v = (j + 0.5) / N                       # 0 top .. 1 bottom
        for i in range(N):
            u = (i + 0.5) / N
            streak = fbm(u * 3.0, v * 9.0, 57, 3)
            dens = smooth(0.02, 1.0, v) ** 1.5
            edge = smooth(0.0, 0.16, u) * smooth(1.0, 0.84, u)
            a = min(0.78, dens * (0.76 + 0.3 * (streak - 0.5))) * (0.35 + 0.65 * edge)
            rgb = ramp([(0, (52, 126, 138)), (0.5, (100, 178, 186)), (1, (156, 214, 218))], dens)
            im.put(i, j, rgb, a)
    return im


def paint_wisps():
    """256x256, four 256x64 bands of mist (rows 0-63: the low horizon band; 64-127: an arc curling up and over to the
    right, for the left side of the vortex; 128-191: a second, thinner arc; 192-255: a short streak), gaussian strokes
    broken by fbm, pale cyan, soft ends."""
    N = 256
    im = Img(N, N)

    def stroke(b, f, width, seed, amax):
        for j in range(64):
            v = (j + 0.5) / 64
            for i in range(N):
                u = (i + 0.5) / N
                yl = f(u)
                if yl is None:
                    continue
                wd = width * (0.7 + 0.6 * fbm(u * 3.0, b * 2.0, seed, 3))
                g = math.exp(-((v - yl) / wd) ** 2)
                n = fbm(u * 8.0 + b, v * 4.0, seed + 5, 4)
                a = amax * g * smooth(0.0, 0.22, u) * smooth(1.0, 0.78, u) * smooth(0.2, 0.7, n + 0.3 * g)
                rgb = ramp([(0, (100, 190, 206)), (0.6, (176, 234, 242)), (1, (236, 255, 255))], g)
                im.put(i, b * 64 + j, rgb, a)
    stroke(0, lambda u: 0.55 + 0.08 * math.sin(u * 7.0) + 0.05 * math.sin(u * 17.0 + 1.0), 0.20, 61, 0.62)
    # arc: a quarter-circle from the bottom-left rising to the top-right (centre (1.0, 1.25), radius 1.0)
    stroke(1, lambda u: 1.25 - math.sqrt(max(0.0, 1.0 - (u - 1.0) ** 2)), 0.15, 67, 0.5)
    stroke(2, lambda u: 1.20 - math.sqrt(max(0.0, 0.9 - (u - 1.0) ** 2)), 0.12, 71, 0.44)
    stroke(3, lambda u: 0.5 + 0.12 * math.sin(u * 5.0), 0.12, 73, 0.5)
    return im


TEXTURES = {'vortex': (512, 512, paint_vortex), 'vortex_glow': (128, 128, paint_glow), 'stars': (256, 256, paint_stars),
            'fog': (64, 64, paint_fog), 'wisps': (256, 256, paint_wisps)}


# --------------------------------------------------------------------------------------------- quads -> models
# A card in MODEL units (16 = one block before the entity scale). plane 'z' = vertical card facing +-z, 'x' = facing
# +-x, 'y' = horizontal. faces: element face names to draw. rot: (axis, angle, origin) single-axis element rotation.
# uv: [u0, v0, u1, v1] of the texture (0..16); frot: uv rotation of the face.
def card(c, hu, hv, plane, faces, tex, uv=(0, 0, 16, 16), rot=None, frot=0):
    return dict(c=c, hu=hu, hv=hv, plane=plane, faces=faces, tex=tex, uv=list(uv), rot=rot, frot=frot)


def element(cd):
    cx, cy, cz = cd['c']
    if cd['plane'] == 'z':
        fr, to = [cx - cd['hu'], cy - cd['hv'], cz], [cx + cd['hu'], cy + cd['hv'], cz]
    elif cd['plane'] == 'x':
        fr, to = [cx, cy - cd['hv'], cz - cd['hu']], [cx, cy + cd['hv'], cz + cd['hu']]
    else:
        fr, to = [cx - cd['hu'], cy, cz - cd['hv']], [cx + cd['hu'], cy, cz + cd['hv']]
    el = {'from': [round(v, 4) for v in fr], 'to': [round(v, 4) for v in to], 'shade': False, 'faces': {}}
    for f in cd['faces']:
        face = {'texture': '#t0', 'uv': [round(v, 4) for v in cd['uv']]}
        if cd['frot']:
            face['rotation'] = cd['frot']
        el['faces'][f] = face
    if cd['rot']:
        ax, ang, org = cd['rot']
        el['rotation'] = {'angle': ang, 'axis': ax, 'origin': [round(v, 4) for v in org]}
    return el


def model_json(cards, tex):
    return {'ambientocclusion': False, 'gui_light': 'front',
            'textures': {'t0': SPRITE + tex, 'particle': SPRITE + tex},
            'elements': [element(c) for c in cards]}


# --------------------------------------------------------------------------------------------- the backdrop layout
CX, CZ, FLOOR_TOP = 0.0, 0.0, 201.0


def _ring_cards(r_bot, y_bot, length, tilt, width, tex, scale, uvs, y_ref):
    """4 cards (N, E, S, W) of a 16-sided ring: bottom edge at radius r_bot / height y_bot, `length` blocks long,
    leaning `tilt` deg outward (top away from the centre). Model units: centre (8, 8, 8) = world (CX, y_ref, CZ)."""
    k = 16.0 / scale                           # model units per block
    out = []
    yb = 8 + (y_bot - y_ref) * k
    L, hw = length * k, width * k / 2
    R = r_bot * k
    # (plane, card centre before rotation, face toward the centre, rotation axis, sign of the outward tilt)
    sides = [('z', (8, yb + L / 2, 8 - R), 'south', 'x', -1, (8, yb, 8 - R)),
             ('x', (8 + R, yb + L / 2, 8), 'west', 'z', -1, (8 + R, yb, 8)),
             ('z', (8, yb + L / 2, 8 + R), 'north', 'x', 1, (8, yb, 8 + R)),
             ('x', (8 - R, yb + L / 2, 8), 'east', 'z', 1, (8 - R, yb, 8))]
    for n, (plane, c, face, ax, sg, org) in enumerate(sides):
        rot = (ax, sg * tilt, org) if tilt else None
        out.append(card(c, hw, L / 2, plane, [face], tex, uv=uvs[n % len(uvs)], rot=rot, frot=0))
    return out


def _build():
    models, ents = {}, []
    # ---- star ring: 16 cards tilted 22.5 deg outward, r 53 at y 209 -> r 59.1 at y 223.8 (16 b long, 21 b wide)
    s_cove, y_cove = 41.0, 216.0
    models['sky_cove'] = ('stars', _ring_cards(53.0, 209.0, 16.0, 22.5, 21.2, 'stars', s_cove,
                                               [(0, 0, 16, 16), (16, 0, 0, 16), (0, 16, 16, 0), (16, 16, 0, 0)], y_cove))
    for k in range(4):
        ents.append(dict(tag='sky_cove', model='sky_cove', pos=(CX, y_cove, CZ), yaw=22.5 * k, tilt=0.0,
                         scale=(s_cove,) * 3))
    # ---- zenith stars: 4 x 4 down-facing cards (each 24 b), y 227.4 (the dome top is the block above 228)
    s_top = 42.0
    k = 16.0 / s_top
    top = []
    for a in range(4):
        for b in range(4):
            cxm = 8 + (-36 + 24 * a) * k
            czm = 8 + (-36 + 24 * b) * k
            uv = [(0, 0, 16, 16), (16, 0, 0, 16), (0, 16, 16, 0), (16, 16, 0, 0)][(a * 3 + b) % 4]
            top.append(card((cxm, 8, czm), 12 * k, 12 * k, 'y', ['down'], 'stars', uv=uv, frot=90 * ((a + b) % 4)))
    models['sky_top'] = ('stars', top)
    ents.append(dict(tag='sky_top', model='sky_top', pos=(CX, 227.4, CZ), yaw=0.0, tilt=0.0, scale=(s_top,) * 3))
    # ---- horizon mist ring: 16 cards leaning back 45 deg, r 46 at the floor -> r 55.9 at y 210.9
    s_fog = 40.0
    models['fog_ring'] = ('fog', _ring_cards(46.0, FLOOR_TOP - 0.1, 14.0, 45.0, 24.0, 'fog', s_fog,
                                             [(0, 0, 16, 16), (16, 0, 0, 16)], 205.0))
    for k in range(4):
        ents.append(dict(tag='fog_ring', model='fog_ring', pos=(CX, 205.0, CZ), yaw=22.5 * k, tilt=0.0,
                         scale=(s_fog,) * 3))
    # ---- vortex: glow halo (66 x 44) behind, the swirl (34 x 34, turning; its foot sinks below the water) in front; both lean back 20 deg
    one = [card((8, 8, 8), 8, 8, 'z', ['south', 'north'], 'x')]
    models['vortex_glow'] = ('vortex_glow', [dict(c, tex='vortex_glow') for c in one])
    models['vortex'] = ('vortex', [dict(c, tex='vortex') for c in one])
    ents.append(dict(tag='vortex_glow', model='vortex_glow', pos=(CX, 210.0, -52.5), yaw=0.0, tilt=20.0,
                     scale=(66.0, 44.0, 1.0)))
    ents.append(dict(tag='vortex', model='vortex', pos=(CX, 211.5, -48.5), yaw=0.0, tilt=20.0, spin=0.0,
                     scale=(34.0, 34.0, 1.0)))
    # ---- wisps: a low mist band in front of the vortex foot, two arcs hugging its rim (lean back 25 deg)
    s_w = 40.0
    k = 16.0 / s_w
    wisp = [card((8, 8 + (-3.6) * k, 8 + 2.5 * k), 26 * k, 3.6 * k, 'z', ['south', 'north'], 'wisps', uv=(0, 0, 16, 4)),
            card((8 - 15.0 * k, 8 + 6.0 * k, 8 - 1.0 * k), 9.5 * k, 6.5 * k, 'z', ['south', 'north'], 'wisps',
                 uv=(0, 4, 16, 8)),
            card((8 + 15.5 * k, 8 + 8.0 * k, 8 - 1.0 * k), 9.0 * k, 6.0 * k, 'z', ['south', 'north'], 'wisps',
                 uv=(16, 8, 0, 12))]
    models['wisps'] = ('wisps', wisp)
    ents.append(dict(tag='wisps', model='wisps', pos=(CX, 206.0, -44.0), yaw=0.0, tilt=25.0, scale=(s_w,) * 3))
    return models, ents


MODELS, ENTITIES = _build()


# --------------------------------------------------------------------------------------------- transforms
def quat_mul(a, b):
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by, aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw, aw * bw - ax * bx - ay * by - az * bz)


def quat_axis(ax, deg):
    h = math.radians(deg) / 2
    s = math.sin(h)
    return {'x': (s, 0.0, 0.0, math.cos(h)), 'y': (0.0, s, 0.0, math.cos(h)), 'z': (0.0, 0.0, s, math.cos(h))}[ax]


def left_rotation(e, spin=None):
    """yaw about +y (turns the ring cards), then a backward lean about +x (top toward -z, i.e. away from a viewer on
    the south), then the spin about the card normal (+z)."""
    q = quat_axis('y', -e['yaw'])
    if e.get('tilt'):
        q = quat_mul(q, quat_axis('x', -e['tilt']))
    sp = e.get('spin') if spin is None else spin
    if sp:
        q = quat_mul(q, quat_axis('z', sp))
    return q


def qrot(q, v):
    x, y, z, w = q
    vx, vy, vz = v
    # v' = q v q*
    tx = 2 * (y * vz - z * vy)
    ty = 2 * (z * vx - x * vz)
    tz = 2 * (x * vy - y * vx)
    return (vx + w * tx + y * tz - z * ty, vy + w * ty + z * tx - x * tz, vz + w * tz + x * ty - y * tx)


def _elem_rot(p, rot):
    if not rot:
        return p
    ax, ang, org = rot
    q = quat_axis(ax, ang)
    d = qrot(q, (p[0] - org[0], p[1] - org[1], p[2] - org[2]))
    return (d[0] + org[0], d[1] + org[1], d[2] + org[2])


FACE_N = {'south': (0, 0, 1), 'north': (0, 0, -1), 'east': (1, 0, 0), 'west': (-1, 0, 0), 'up': (0, 1, 0),
          'down': (0, -1, 0)}


def world_cards(e, spin=None):
    """World-space faces of one entity: dicts with corners p00 (u0,v0) p10 (u1,v0) p01 (u0,v1), normal, texture, uv.
    Used by the offline renderer; mirrors the model + display-transform maths above."""
    q = left_rotation(e, spin)
    S = e['scale']
    out = []
    for cd in MODELS[e['model']][1]:
        cx, cy, cz = cd['c']
        hu, hv = cd['hu'], cd['hv']
        for f in cd['faces']:
            # face-local corners (top-left = uv origin), Minecraft side-face convention
            if cd['plane'] == 'z':
                if f == 'south':
                    tl, tr, bl = (cx - hu, cy + hv, cz), (cx + hu, cy + hv, cz), (cx - hu, cy - hv, cz)
                else:
                    tl, tr, bl = (cx + hu, cy + hv, cz), (cx - hu, cy + hv, cz), (cx + hu, cy - hv, cz)
            elif cd['plane'] == 'x':
                if f == 'east':
                    tl, tr, bl = (cx, cy + hv, cz + hu), (cx, cy + hv, cz - hu), (cx, cy - hv, cz + hu)
                else:
                    tl, tr, bl = (cx, cy + hv, cz - hu), (cx, cy + hv, cz + hu), (cx, cy - hv, cz - hu)
            else:
                if f == 'up':
                    tl, tr, bl = (cx - hu, cy, cz - hv), (cx + hu, cy, cz - hv), (cx - hu, cy, cz + hv)
                else:
                    tl, tr, bl = (cx - hu, cy, cz + hv), (cx + hu, cy, cz + hv), (cx - hu, cy, cz - hv)
            n = FACE_N[f]
            pts = []
            for p in (tl, tr, bl):
                p = _elem_rot(p, cd['rot'])
                m = ((p[0] / 16 - 0.5) * S[0], (p[1] / 16 - 0.5) * S[1], (p[2] / 16 - 0.5) * S[2])
                w = qrot(q, m)
                pts.append((e['pos'][0] + w[0], e['pos'][1] + w[1], e['pos'][2] + w[2]))
            nn = _elem_rot(n, (cd['rot'][0], cd['rot'][1], (0, 0, 0)) if cd['rot'] else None)
            nn = qrot(q, (nn[0] / S[0], nn[1] / S[1], nn[2] / S[2]))
            ln = math.sqrt(sum(c * c for c in nn)) or 1.0
            out.append(dict(p00=pts[0], p10=pts[1], p01=pts[2], n=tuple(c / ln for c in nn), tex=cd['tex'],
                            uv=cd['uv'], frot=cd['frot']))
    return out


def diffuse(n):
    """Vanilla entity diffuse light for a world normal (ambient 0.4 + 0.6 * two fixed directions)."""
    l0 = (0.2, 1.0, -0.7)
    l1 = (-0.2, 1.0, 0.7)
    acc = 0.0
    for L in (l0, l1):
        ln = math.sqrt(sum(c * c for c in L))
        acc += max(0.0, sum(a * b for a, b in zip(L, n)) / ln)
    return min(1.0, 0.4 + 0.6 * acc)


def nbt_f(v):
    s = ('%.5f' % v).rstrip('0').rstrip('.')
    return (s if s not in ('-0', '') else '0') + 'f'


def summon_line(e, tags):
    """The summon command of one backdrop entity (absolute coordinates)."""
    q = left_rotation(e)
    tg = ','.join('"%s"' % t for t in tags + ['rlk_rd_bg_' + e['tag']])
    x, y, z = e['pos']
    return ('summon minecraft:item_display %s %s %s {Tags:[%s],billboard:"fixed",item_display:"none",view_range:4f,'
            'width:0f,height:0f,shadow_radius:0f,brightness:{block:15,sky:15},interpolation_duration:0,'
            'teleport_duration:0,transformation:{translation:[0f,0f,0f],left_rotation:[%s],scale:[%s],'
            'right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":'
            '"rlk:%s/%s"}}}' % (nbt_f(x)[:-1], nbt_f(y)[:-1], nbt_f(z)[:-1], tg, ','.join(nbt_f(c) for c in q),
                                ','.join(nbt_f(c) for c in e['scale']), NS_DIR, e['model']))


def texture_px():
    return sum(w * h for w, h, _ in TEXTURES.values())


# --------------------------------------------------------------------------------------------- write the pack
def build(rp):
    A = Path(rp) / 'assets'
    tdir, mdir, idir = A / 'rlk/textures' / NS_DIR, A / 'rlk/models/item' / NS_DIR, A / 'rlk/items' / NS_DIR
    for d in (tdir, mdir, idir):
        d.mkdir(parents=True, exist_ok=True)
    for name, (w, h, paint) in TEXTURES.items():
        im = paint()
        assert (im.w, im.h) == (w, h) and w % 16 == 0 and h % 16 == 0
        (tdir / (name + '.png')).write_bytes(im.png())
    for name, (tex, cards) in MODELS.items():
        md = model_json(cards, tex)
        for el in md['elements']:
            assert all(-16 <= v <= 32 for v in el['from'] + el['to']), (name, el)
            if 'rotation' in el:
                assert el['rotation']['angle'] in (-45, -22.5, 0, 22.5, 45), (name, el['rotation'])
        (mdir / (name + '.json')).write_text(json.dumps(md, separators=(',', ':')) + '\n', encoding='utf-8')
        (idir / (name + '.json')).write_text(json.dumps(
            {'model': {'type': 'minecraft:model', 'model': 'rlk:item/' + NS_DIR + '/' + name}},
            separators=(',', ':')) + '\n', encoding='utf-8')
    # prune files of this folder that are no longer generated
    for d, ext, keep in ((tdir, '.png', TEXTURES), (mdir, '.json', MODELS), (idir, '.json', MODELS)):
        for f in d.glob('*' + ext):
            if f.stem not in keep:
                f.unlink()
    atlaspath = A / 'minecraft/atlases/items.json'
    atlas = json.loads(atlaspath.read_text(encoding='utf-8')) if atlaspath.exists() else {'sources': []}
    want = [SPRITE + n for n in TEXTURES]
    atlas['sources'] = [s for s in atlas['sources']
                        if not (s.get('resource', '').startswith(SPRITE) and s.get('resource') not in want)]
    known = {s.get('sprite', s.get('resource')) for s in atlas['sources']}
    for r in want:
        if r not in known:
            atlas['sources'].append({'type': 'minecraft:single', 'resource': r})
    atlaspath.parent.mkdir(parents=True, exist_ok=True)
    atlaspath.write_text(json.dumps(atlas, indent=2) + '\n', encoding='utf-8')
    print(f'Raiden arena backdrop: {len(TEXTURES)} textures ({texture_px():,} px), {len(MODELS)} models, '
          f'{len(ENTITIES)} panel entities.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--resourcepack', type=Path, default=TOOLS.parents[1] / 'resourcepack')
    args = ap.parse_args()
    if not args.resourcepack.is_dir():
        raise SystemExit(f'Resource pack folder not found: {args.resourcepack}')
    build(args.resourcepack)
