"""Painted lightning VFX textures for Narukami (sprites rlk:raiden/fxg/<name>).

Pure standard library (math, random, struct, zlib) and deterministic: every texture
is painted from fixed seeds, so the resource pack can be regenerated anywhere
(~30 s in CPython). `build_fx_textures(rp)` writes
<rp>/assets/rlk/textures/raiden/fxg/<name>.png, appends each sprite to
assets/minecraft/atlases/items.json and prunes fxg sprites it no longer paints
(other atlas entries are never touched). The machine-readable catalogue is
tools/raiden_fx_textures.json (name, texture, w, h, kind, along, core, use, notes,
plus the hazard decal rectangles); JS generators should read that file.
Run alone: python tools/build_raiden_fx_textures.py --resourcepack <rp> [--only a,b*] [--list]

LOOK. Electro palette with real gradients: white-hot core (#FFFFFF) -> pale lavender
(#EBDDFF) -> violet (#B07CFF) -> deep purple (#5B2BB8) -> transparent, with sparing
cyan-white sparks; telegraphs use a magenta-violet ramp. Everything is anti-aliased
and distance-field based; glows are gaussian; every texture fades to alpha 0 before
its border, so a card never shows its rectangle.

VANILLA RULES THAT SHAPED THE SPRITES (read before using them):
  * Fragments with alpha < 0.1 are discarded, so the faintest halo is invisible; the
    palettes reach that level in a muted lavender so the cut-off edge stays faint.
  * Item sprites with partial alpha go to the translucent sheet: quads are sorted
    back-to-front by CENTROID distance and drawn with depth test AND depth write.
    A translucent card drawn earlier hides any translucent card behind it wherever
    its own alpha >= 0.1. Hence hot bolts, blades, crackles and vertical bolts keep
    their visible halo tight (wide soft glow only on afterglow sprites), and cards
    laid on top of a decal should use rim_crackle_* / bolt_* rather than wide glows.
    Prefer one centred card under centred overlays; split tall vertical cards so the
    low part's centroid is near eye height.
  * Sampling is nearest-neighbour when magnified (mipmaps only when minified), so
    anything seen up close is painted at >= ~32 texels per block and floor decals
    contain no feature thinner than ~2 texels.
  * Vertical faces may receive the entity diffuse light (0.5..0.74 for walls, 1.0
    for up faces); cores are white so dimmed vertical bolts still read as lightning.

UV CONVENTIONS (texture x = u = left->right, texture y = v = top->bottom):
  strip    w >> h. The bolt/edge runs along u from u=0 (start) to u=1 (end) at v=0.5
           (centre row), soft-faded over the first/last ~5% of u, so cards can be
           chained/overlapped. Branches spread toward v=0.1..0.9.
  column   h >> w. Runs along v from v=0 (TOP, sky end) to v=1 (BOTTOM, impact end)
           at u=0.5. Map v=0 to the card's top edge.
  radial   centred at (0.5, 0.5); size noted per texture (radius as a fraction of w).
  crescent pivot (sword hand / arc centre) at the BOTTOM-CENTRE (u=0.5, v=1.0); the
           bright cutting edge is the outer arc of radius 0.94*h (v=0.06 at the
           apex), spanning +-72 deg around straight up; the gradient tail trails
           inward toward the pivot. Card: width 2H, depth H, H = edge radius / 0.94.
  decal    top-view floor decal; u = world +x (local left/right), v = world +z (local forward).
  quarter  ring quadrant: circle centre at the texture's top-left corner (u=0,v=0);
           mirror it (uv [16,0,0,16] etc.) for the other quadrants.

CATALOGUE (all sizes are multiples of 16 so the atlas keeps its mipmap levels;
total ~2.5 Mpx after the S1-KIT reclaim: tele_* / charged_* / ringq_* and unused sprites are gone)
  bolt_a..bolt_d        512x128 strip   hot bolt: jagged zig-zag white core (r~1.5px),
                                         3 levels of forks, violet glow, tight halo,
                                         1-2 cyan sparks. Floor bolts, horizontal
                                         strikes, tall walls (card ~3..10:1).
  bolt_after_a/_c       512x128 strip   afterglow of bolt_a / bolt_c (same path):
                                         dimmer, wider, purple, dissolving (wide halo).
  bolt_fade_a/_c        512x128 strip   last fade of bolt_a / bolt_c: dissolving embers.
  blade_a..blade_c      512x64  strip   blade-hugging bolt: core within v=0.5+-0.08,
                                         short frequent forks, tight glow. Weapon edges
                                         (u = hilt -> tip), long low walls (~8:1).
  rim_crackle_a..c      512x64  strip   crackle with no halo (alpha >= 0.1 only near the
                                         core) to lay on top of another translucent card.
  blade_trail_a/_b      512x64  strip   slash trail: u=0 newest/brightest -> u=1 oldest,
                                         dissolving and widening, afterglow colours.
  vbolt_a..vbolt_c      128x512 column  vertical strike: zig-zag channel top->bottom,
                                         downward forks, small impact bloom at v~0.96,
                                         narrow halo (sides fade over 30% of w).
                                         Use 2-4 crossed vertical cards (~2.5 wide).
  vbolt_after_c         128x512 column  afterglow of vbolt_c (same path).
  pillar_a/_b           128x512 column  stake/pillar current: 3 thin bolts winding
                                         around u=0.5 inside a soft violet column glow;
                                         soft top and bottom, no impact bloom.
  arc_a/_b              256x128 strip   palm/finger arc: bolt from (0.06,0.86) arching
                                         up to apex v~0.2 and down to (0.94,0.86).
  chakra_a/_b           256x256 radial  ring of electricity, radius 0.40*w, crackling
                                         arcs in/out of the ring, transparent centre.
  orb_core              128x128 radial  soft radial glow, white centre -> violet.
  crescent_a            352x176 crescent clean blade-light crescent (bright edge,
                                         lavender->violet gradient tail inward).
  crescent_b            352x176 crescent crescent with a jagged bolt along its edge.
  slash_wave            512x128 strip   straight slash wave: bright leading edge at
                                         v~0.3 (moving toward -v), lens-shaped gradient
                                         tail toward v~0.9, tapered ends.
  rift_a/_b             512x64  strip   rift/cut ribbon: thin white jagged tear along
                                         u inside a dark void band with violet lips.
  shockwave             256x256 radial  annulus: bright leading edge at r=0.46*w,
                                         soft trailing gradient inward to ~0.28*w.
  crackle_a/_b          512x64  strip   vertical lightning wall band (v=0 top, v=1 floor,
                                         floor glow line at v~0.93), chainable along u,
                                         tight halo. Ring walls, low fences.
  flash                 256x256 radial  compact strike flash: white-hot centre, short rays.
  impact_sparks         256x256 radial  shield/hit impact: radial spark streaks.
  scorch                256x256 radial  floor scorch: dark burn, ember ring, cracks.
  scorch_strip          256x64  strip   dark burn streak with embers (under floor bolts).
  spark                 32x32   radial  single spark dot (white core, cyan halo).
  glint                 64x64   radial  four-point star glint (armour shards).
  charge_spark          64x128  column  small rising spark, base at (0.5, 0.95).
  glow_soft             64x64   radial  plain soft round glow (lavender->violet).
  glow_strip            256x32  strip   plain soft beam glow along u.
  dk_ring, dk_ring_s    quarter         kit ring decals (thin r >= 6 / bold r < 6), unit radius, faint inner fill.
  dk_rings3, dk_disc    quarter         3 concentric rings (Musou orbs) / pale disc with a brighter rim (A-02).
  dk_band 64x256, dk_pool 256, dk_tint 64, tr_band 32x256: band decal, smoky pool, field tint, ring-segment
                                         band; see the "kit decals and travelling bands" section.
  rig_katana_a/_b       224x112 blade   boss blade sheath in the blade plane (u = model y 9.6..32 hilt->tip,
                                         v = model x 2.6..12 edge side first): edge bolt following the
                                         giant-katana outline, spine crackle, tip fork (build_raiden_rig.mjs).
  rig_palm              128x144 palm    five arcs (fingertips + thumb) converging into the palm centre.
  rig_crown             192x192 radial  palm release crown: radiating bolts, broken ring, dark centre.
  rig_shard             48x128  column  translucent crystal splinter (death shards).
  obj_swing_band        512x64  strip   illusion swing ribbon: u=0 oldest tail -> u=1 bright blade
                                         end, line descending v 0.27 -> 0.73 (build_raiden_object_vfx.py).
  obj_wave_band/_fade   512x64  strip   sword-wave front: lens band, white core at v=0.5, layered
                                         glow + core crackle / dissolving purple afterglow.
  obj_shard             64x64   strip   flying shard: tip at u~0.93, motion streak toward u=0.
"""
from pathlib import Path
import argparse
import json
import math
import random
import struct
import time
import zlib

NS = "rlk:raiden/fxg/"
TEX_SUBDIR = "assets/rlk/textures/raiden/fxg"
CATALOGUE_JSON = Path(__file__).resolve().parent / "raiden_fx_textures.json"

# --------------------------------------------------------------------------- legacy constants
# Legacy hazard preset s11 (the expanding stake ring of the release encounter): band radius 2 .. RING_END over
# RING_FRAMES ticks. raiden_enc/tenma.py imports these two for its timeline until S3 removes the preset; the
# ring itself is now drawn by the segment cards of build_raiden_hazard_vfx.py (sprite tr_band).
RING_END, RING_FRAMES = 32, 58

# --------------------------------------------------------------------------- palettes
EMAX = 2.5
LUTN = 1024


def ramp(stops):
    """Straight RGBA stops [(E, (r,g,b,a 0..255))] -> premultiplied float LUT over E in [0, EMAX]."""
    lut = []
    for i in range(LUTN):
        e = EMAX * i / (LUTN - 1)
        if e <= stops[0][0]:
            c = stops[0][1]
        elif e >= stops[-1][0]:
            c = stops[-1][1]
        else:
            for (e0, c0), (e1, c1) in zip(stops, stops[1:]):
                if e0 <= e <= e1:
                    t = (e - e0) / (e1 - e0) if e1 > e0 else 0
                    c = tuple(c0[k] + (c1[k] - c0[k]) * t for k in range(4))
                    break
        a = c[3] / 255.0
        lut.append((c[0] / 255.0 * a, c[1] / 255.0 * a, c[2] / 255.0 * a, a))
    return lut


ELECTRO = ramp([(0.0, (104, 76, 172, 0)), (0.05, (104, 76, 172, 0)), (0.11, (100, 66, 176, 30)),
                (0.22, (96, 48, 192, 76)), (0.38, (132, 78, 232, 150)), (0.55, (176, 124, 255, 210)),
                (0.72, (214, 188, 255, 238)), (0.86, (235, 221, 255, 250)), (1.0, (255, 255, 255, 255))])
AFTER = ramp([(0.0, (100, 80, 150, 0)), (0.06, (100, 80, 150, 0)), (0.14, (88, 52, 156, 34)),
              (0.30, (100, 52, 182, 88)), (0.52, (130, 80, 216, 132)), (0.78, (162, 116, 242, 168)),
              (1.05, (198, 164, 255, 194)), (1.5, (225, 206, 255, 214))])
FADE = ramp([(0.0, (100, 82, 146, 0)), (0.08, (100, 82, 146, 0)), (0.18, (80, 46, 146, 30)),
             (0.42, (92, 50, 170, 66)), (0.8, (122, 78, 204, 96)), (1.3, (156, 116, 232, 118))])
TELE = ramp([(0.0, (128, 84, 140, 0)), (0.05, (128, 84, 140, 0)), (0.12, (130, 64, 150, 32)),
             (0.28, (166, 50, 190, 104)), (0.50, (214, 80, 228, 186)), (0.72, (242, 134, 242, 230)),
             (0.9, (255, 198, 252, 250)), (1.05, (255, 236, 255, 255))])
LINE = ramp([(0.0, (120, 108, 180, 0)), (0.06, (120, 108, 180, 0)), (0.15, (130, 104, 232, 42)),
             (0.40, (170, 152, 250, 142)), (0.70, (216, 212, 255, 222)), (1.0, (246, 248, 255, 255))])
CYAN = ramp([(0.0, (60, 140, 255, 0)), (0.06, (60, 140, 255, 0)), (0.15, (82, 172, 255, 52)),
             (0.40, (142, 216, 255, 152)), (0.70, (206, 242, 255, 230)), (1.0, (255, 255, 255, 255))])
VOIDP = ramp([(0.0, (20, 6, 40, 0)), (1.0, (20, 6, 40, 255)), (2.5, (20, 6, 40, 255))])
BASE_RGB = (104, 76, 172)


def solid(rgb):
    """LUT whose alpha equals E (0..1) with a constant colour (underlays, scorch)."""
    return ramp([(0.0, (*rgb, 0)), (1.0, (*rgb, 255)), (2.5, (*rgb, 255))])

# --------------------------------------------------------------------------- fields
GAUSS = [math.exp(-i / 256.0) for i in range(256 * 9 + 2)]


class Field:
    __slots__ = ("w", "h", "d")

    def __init__(self, w, h, v=0.0):
        self.w, self.h = w, h
        self.d = [v] * (w * h)


def capsule(f, ax, ay, ar, aa, bx, by, br, ba, kind):
    """Max-combine one segment into field f (pixel units, pixel centres at +0.5).

    kind 0: anti-aliased solid core of radius r, value = amplitude.
    kind 1: gaussian glow amplitude*exp(-(d/r)^2)."""
    w, h, d = f.w, f.h, f.d
    rmax = ar if ar > br else br
    reach = rmax + 1.0 if kind == 0 else rmax * 3.0
    if reach <= 0:
        return
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    inv = 1.0 / L2 if L2 > 1e-12 else 0.0
    y0 = max(0, int(min(ay, by) - reach))
    y1 = min(h - 1, int(max(ay, by) + reach) + 1)
    G = GAUSS
    sqrt = math.sqrt
    dr, da = br - ar, ba - aa
    for y in range(y0, y1 + 1):
        py = y + 0.5 - ay
        if abs(dy) > 1e-6:
            t0, t1 = (py - reach) / dy, (py + reach) / dy
            if t0 > t1:
                t0, t1 = t1, t0
            t0 = 0.0 if t0 < 0 else (1.0 if t0 > 1 else t0)
            t1 = 0.0 if t1 < 0 else (1.0 if t1 > 1 else t1)
            xa, xb = ax + dx * t0, ax + dx * t1
            if xa > xb:
                xa, xb = xb, xa
            xs, xe = int(xa - reach), int(xb + reach) + 1
        else:
            xs, xe = int(min(ax, bx) - reach), int(max(ax, bx) + reach) + 1
        if xs < 0:
            xs = 0
        if xe > w - 1:
            xe = w - 1
        base = y * w
        for x in range(xs, xe + 1):
            px = x + 0.5 - ax
            t = (px * dx + py * dy) * inv
            if t < 0.0:
                t = 0.0
            elif t > 1.0:
                t = 1.0
            ex = px - t * dx
            ey = py - t * dy
            dd = ex * ex + ey * ey
            r = ar + dr * t
            if kind == 0:
                lim = r + 0.5
                if dd >= lim * lim:
                    continue
                v = lim - sqrt(dd)
                if v > 1.0:
                    v = 1.0
                v *= aa + da * t
            else:
                if r <= 1e-6:
                    continue
                q = dd / (r * r)
                if q >= 9.0:
                    continue
                v = (aa + da * t) * G[int(q * 256)]
            i = base + x
            if v > d[i]:
                d[i] = v


def stroke(f, path, kind, rk=1.0, rb=0.0, ak=1.0, scale=1.0):
    """path = [(x, y, r, a)]; radius r*rk+rb, amplitude a*ak, coordinates *scale."""
    for p, q in zip(path, path[1:]):
        capsule(f, p[0] * scale, p[1] * scale, (p[2] * rk + rb) * scale, p[3] * ak,
                q[0] * scale, q[1] * scale, (q[2] * rk + rb) * scale, q[3] * ak, kind)


def dot(f, x, y, r, a, kind, scale=1.0):
    capsule(f, x * scale, y * scale, r * scale, a, x * scale + 1e-3, y * scale, r * scale, a, kind)


def upsample(src, w, h):
    """Bilinear upsample of a low-res field to w x h (pixel-centre aligned)."""
    sw, sh, sd = src.w, src.h, src.d
    fx = sw / w
    fy = sh / h
    xs = []
    for x in range(w):
        u = (x + 0.5) * fx - 0.5
        i0 = int(math.floor(u))
        t = u - i0
        i1 = min(sw - 1, max(0, i0 + 1))
        i0 = min(sw - 1, max(0, i0))
        xs.append((i0, i1, t))
    out = []
    for y in range(h):
        v = (y + 0.5) * fy - 0.5
        j0 = int(math.floor(v))
        s = v - j0
        j1 = min(sh - 1, max(0, j0 + 1))
        j0 = min(sh - 1, max(0, j0))
        r0 = sd[j0 * sw:(j0 + 1) * sw]
        r1 = sd[j1 * sw:(j1 + 1) * sw]
        out.extend([(r0[a] + (r0[b] - r0[a]) * t) * (1 - s) + (r1[a] + (r1[b] - r1[a]) * t) * s for a, b, t in xs])
    f = Field(w, h)
    f.d = out
    return f


def sample_fn(w, h, fn, ds=2):
    """Evaluate fn(i, j) (texture pixel coordinates, floats) on a grid ds px apart, upsampled."""
    sw, sh = (w + ds - 1) // ds, (h + ds - 1) // ds
    low = Field(sw, sh)
    d = low.d
    for j in range(sh):
        y = (j + 0.5) * h / sh
        for i in range(sw):
            d[j * sw + i] = fn((i + 0.5) * w / sw, y)
    return upsample(low, w, h) if ds > 1 else low


def smooth(e0, e1, x):
    t = (x - e0) / (e1 - e0)
    t = 0.0 if t < 0 else (1.0 if t > 1 else t)
    return t * t * (3 - 2 * t)


def window(w, h, mx, my):
    """Separable soft border window (0 at the edge, 1 after mx/my pixels)."""
    wx = [smooth(0, mx, x + 0.5) * smooth(0, mx, w - x - 0.5) for x in range(w)]
    wy = [smooth(0, my, y + 0.5) * smooth(0, my, h - y - 0.5) for y in range(h)]
    return wx, wy

# --------------------------------------------------------------------------- images


class Img:
    """Premultiplied float RGBA image as four flat lists."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        n = w * h
        self.r, self.g, self.b, self.a = [0.0] * n, [0.0] * n, [0.0] * n, [0.0] * n

    def over(self, lut, E, gain=1.0, win=None):
        """Composite ramp(E*gain) OVER this image (E may be a Field or a list)."""
        e = E.d if isinstance(E, Field) else E
        k = (LUTN - 1) / EMAX * gain
        top = LUTN - 1
        if win is not None:
            wx, wy = win
            w = self.w
            px = [lut[min(top, int(v * k * wx[i % w] * wy[i // w]))] for i, v in enumerate(e)]
        else:
            px = [lut[min(top, int(v * k))] for v in e]
        R, G, B, A = self.r, self.g, self.b, self.a
        self.r = [p[0] + q * (1 - p[3]) for p, q in zip(px, R)]
        self.g = [p[1] + q * (1 - p[3]) for p, q in zip(px, G)]
        self.b = [p[2] + q * (1 - p[3]) for p, q in zip(px, B)]
        self.a = [p[3] + q * (1 - p[3]) for p, q in zip(px, A)]

    def png(self):
        w, h = self.w, self.h
        br, bg, bb = BASE_RGB
        raw = bytearray()
        R, G, B, A = self.r, self.g, self.b, self.a
        for y in range(h):
            raw.append(0)
            for i in range(y * w, (y + 1) * w):
                a = A[i]
                if a < 0.5 / 255:
                    raw += bytes((br, bg, bb, 0))
                    continue
                ia = 1.0 / a
                r, g, b = R[i] * ia, G[i] * ia, B[i] * ia
                raw += bytes((min(255, int(r * 255 + 0.5)), min(255, int(g * 255 + 0.5)),
                              min(255, int(b * 255 + 0.5)), min(255, int(a * 255 + 0.5))))
        return encode_png(w, h, bytes(raw))


def encode_png(w, h, raw):
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))


def combine(*terms):
    """Sum of (field_or_list, weight) terms -> list."""
    out = None
    for f, k in terms:
        d = f.d if isinstance(f, Field) else f
        if out is None:
            out = [v * k for v in d]
        else:
            out = [o + v * k for o, v in zip(out, d)]
    return out

# --------------------------------------------------------------------------- lightning geometry


def jag(rng, a, b, depth=6, rough=(0.24, 0.27, 0.26, 0.22, 0.18, 0.14), shift=0.14):
    """Midpoint-displaced jagged polyline from a to b (list of (x, y))."""
    pts = [a, b]
    for lvl in range(depth):
        k = rough[min(lvl, len(rough) - 1)]
        out = [pts[0]]
        for p, q in zip(pts, pts[1:]):
            dx, dy = q[0] - p[0], q[1] - p[1]
            L = math.hypot(dx, dy) or 1e-9
            off = (rng.random() * 2 - 1) * k * L
            sh = (rng.random() * 2 - 1) * shift
            out.append((p[0] + dx * (0.5 + sh) - dy / L * off, p[1] + dy * (0.5 + sh) + dx / L * off))
            out.append(q)
        pts = out
    return pts


def walk(rng, a, b, band, step=(0.45, 1.25), maxang=52, pull=0.35, fine=2, end_off=0.0, start_off=None,
         free_end=False):
    """Zig-zag lightning from a toward b: random-angle steps (step sizes in units of `band`),
    mean-reverting lateral offset kept within +-band, then fine midpoint jitter."""
    L = math.dist(a, b) or 1e-9
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    nx, ny = -uy, ux
    s = 0.0
    off = rng.uniform(-0.25, 0.25) * band if start_off is None else start_off
    seq = [(0.0, off)]
    while s < L:
        ds = rng.uniform(*step) * band
        ang = math.radians(rng.uniform(-maxang, maxang))
        off += ds * math.tan(ang) - pull * off * rng.random()
        if off > band:
            off = 2 * band - off
        if off < -band:
            off = -2 * band - off
        off = max(-band, min(band, off))
        s = min(L, s + ds)
        seq.append((s, off))
    if not free_end:
        n = len(seq)
        k0 = max(1, int(n * 0.8))
        seq = [(t, o if i < k0 else o + (end_off - seq[-1][1]) * ((i - k0 + 1) / (n - k0)))
               for i, (t, o) in enumerate(seq)]
    base = [(a[0] + ux * t + nx * o, a[1] + uy * t + ny * o) for t, o in seq]
    if not fine:
        return base
    out = []
    for p, q in zip(base, base[1:]):
        out += jag(rng, p, q, fine, (0.16, 0.12), 0.1)[:-1]
    out.append(base[-1])
    return out


def clamp_pts(pts, xlo, xhi, ylo, yhi):
    return [(min(xhi, max(xlo, x)), min(yhi, max(ylo, y))) for x, y in pts]


def plen(pts):
    return sum(math.dist(p, q) for p, q in zip(pts, pts[1:]))


def attrib(pts, r0, r1, a0, a1, rng=None, flicker=0.0, ends=0.0):
    """Attach radius/amplitude along cumulative length; optional amplitude flicker and end fades."""
    total = plen(pts) or 1.0
    out, acc = [], 0.0
    phase = rng.random() * 6.28 if rng else 0.0
    freq = (rng.uniform(3, 7) if rng else 5.0)
    for i, p in enumerate(pts):
        if i:
            acc += math.dist(pts[i - 1], p)
        t = acc / total
        a = a0 + (a1 - a0) * t
        if flicker:
            a *= 1 - flicker * (0.5 + 0.5 * math.sin(phase + freq * t * 6.28 + 2.1 * math.sin(phase * 1.7 + t * 17)))
        rr = r0 + (r1 - r0) * t
        if flicker:
            rr *= 1 - 0.45 * flicker * (0.5 + 0.5 * math.sin(phase * 2.3 + freq * 1.7 * t * 6.28))
        if ends:
            a *= smooth(0, ends, t) * smooth(0, ends, 1 - t)
        out.append((p[0], p[1], rr, a))
    return out


def add_branches(rng, paths, main, r, a, levels, count, spread=(18, 52), length=(0.10, 0.30), total=None,
                 bounds=None, bias=None, rshrink=0.58, ashrink=0.82):
    """Recursive forks off `main` (point list). Appends attrib paths to `paths`."""
    if levels <= 0 or len(main) < 8:
        return
    total = total or plen(main)
    for _ in range(count):
        i = rng.randint(2, len(main) - 6)
        p, q = main[i], main[min(len(main) - 1, i + 3)]
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy) or 1e-9
        sgn = (1 if rng.random() < 0.5 else -1) if bias is None else bias(p, rng)
        ang = math.radians(rng.uniform(*spread)) * sgn
        ux = (dx * math.cos(ang) - dy * math.sin(ang)) / L
        uy = (dx * math.sin(ang) + dy * math.cos(ang)) / L
        ln = total * rng.uniform(*length)
        if bounds:
            # shorten (never flatten) a fork that would leave the texture's safe area
            xlo, xhi, ylo, yhi = bounds
            for _ in range(8):
                ex, ey = p[0] + ux * ln, p[1] + uy * ln
                m = ln * 0.2
                if xlo + m <= ex <= xhi - m and ylo + m <= ey <= yhi - m:
                    break
                ln *= 0.7
        end = (p[0] + ux * ln, p[1] + uy * ln)
        sub = walk(rng, p, end, max(2.0, ln * 0.16), (0.5, 1.4), 55, 0.25, 2, start_off=0.0, free_end=True)
        if bounds:
            sub = clamp_pts(sub, *bounds)
        paths.append(attrib(sub, r * rshrink, r * 0.16, a * ashrink, a * 0.25, rng, 0.25))
        add_branches(rng, paths, sub, r * rshrink, a * ashrink, levels - 1, rng.randint(0, 2), spread,
                     (length[0] * 1.2, length[1] * 1.3), ln, bounds, None, rshrink, ashrink)


def render_fields(w, h, paths, glow, halo, ds=4):
    """core + glow (half resolution) + halo (1/ds) of attrib paths as one list (weights 1/0.55/0.3)."""
    core = Field(w, h)
    gl = Field(max(1, w // 2), max(1, h // 2))
    lo = Field(max(1, w // ds), max(1, h // ds))
    for p in paths:
        stroke(core, p, 0)
        stroke(gl, p, 1, glow[0], glow[1], 1.0, 0.5)
        stroke(lo, p, 1, halo[0], halo[1], 1.0, 1.0 / ds)
    return combine((core, 1.0), (upsample(gl, w, h), 0.55), (upsample(lo, w, h), 0.3))


def render_bolt(w, h, paths, sparks=(), glow=(2.3, 2.5, 0.58), halo=(6.0, 9.0, 0.30), ds=4,
                lut=ELECTRO, win=None, gain=1.0, dissolve=None, spark_lut=CYAN, extra=None):
    """Paint attrib paths into core/glow/halo fields and map through a palette.

    glow = (radius multiplier, radius bias px, weight); halo likewise at 1/ds resolution."""
    core = Field(w, h)
    gl = Field(w, h)
    lo = Field(max(1, w // ds), max(1, h // ds))
    for p in paths:
        stroke(core, p, 0)
        stroke(gl, p, 1, glow[0], glow[1])
        stroke(lo, p, 1, halo[0], halo[1], 1.0, 1.0 / ds)
    hal = upsample(lo, w, h)
    E = combine((core, 1.0), (gl, glow[2]), (hal, halo[2]))
    if extra is not None:
        E = [e + x for e, x in zip(E, extra)]
    if dissolve is not None:
        E = [e * m for e, m in zip(E, dissolve)]
    img = Img(w, h)
    win = win or window(w, h, max(4, w * 0.05), max(4, h * 0.05))
    img.over(lut, E, gain, win)
    if sparks:
        S = Field(w, h)
        Sg = Field(w, h)
        for x, y, r, a in sparks:
            dot(S, x, y, r, a, 0)
            dot(Sg, x, y, r * 3.2 + 2, a * 0.55, 1)
        img.over(spark_lut, combine((S, 1.0), (Sg, 1.0)), 1.0, win)
    return img


def spark_points(rng, main, n, off, r=(0.9, 1.5), a=(0.75, 1.0)):
    out = []
    for _ in range(n):
        i = rng.randint(1, len(main) - 2)
        p, q = main[i - 1], main[i + 1]
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy) or 1e-9
        o = rng.uniform(*off) * (1 if rng.random() < 0.5 else -1)
        out.append((main[i][0] - dy / L * o, main[i][1] + dx / L * o, rng.uniform(*r), rng.uniform(*a)))
    return out

# --------------------------------------------------------------------------- noise


class WaveNoise:
    """Cheap smooth noise: domain-warped sums of random plane waves (deterministic)."""

    def __init__(self, seed, n=5, scale=1.0):
        rng = random.Random(seed)
        self.waves = []
        for k in range(n):
            ang = rng.uniform(0, math.pi)
            f = scale * rng.uniform(0.7, 1.6) * (1.0 + 0.35 * k)
            self.waves.append((math.cos(ang) * f, math.sin(ang) * f, rng.uniform(0, 6.28), rng.uniform(0.6, 1.0)))
        self.norm = sum(w[3] for w in self.waves)

    def __call__(self, x, y):
        s = 0.0
        sin = math.sin
        warp = sin(x * 0.37 + y * 0.23) * 1.3
        for fx, fy, ph, amp in self.waves:
            s += amp * sin(fx * x + fy * y + ph + warp)
        return s / self.norm          # about -1..1


class ValueNoise:
    """Lattice value noise with smooth interpolation and fbm (deterministic, tileable period n)."""

    def __init__(self, seed, n=64):
        rng = random.Random(seed)
        self.n = n
        self.v = [rng.random() * 2 - 1 for _ in range(n * n)]

    def at(self, x, y):
        n, v = self.n, self.v
        xf, yf = math.floor(x), math.floor(y)
        fx, fy = x - xf, y - yf
        fx = fx * fx * (3 - 2 * fx)
        fy = fy * fy * (3 - 2 * fy)
        i0, j0 = int(xf) % n, int(yf) % n
        i1, j1 = (i0 + 1) % n, (j0 + 1) % n
        a, b = v[j0 * n + i0], v[j0 * n + i1]
        c, d = v[j1 * n + i0], v[j1 * n + i1]
        return (a + (b - a) * fx) * (1 - fy) + (c + (d - c) * fx) * fy

    def fbm(self, x, y, octaves=4):
        s, amp, tot = 0.0, 1.0, 0.0
        for k in range(octaves):
            s += amp * self.at(x + 17.3 * k, y - 9.1 * k)
            tot += amp
            x, y, amp = x * 2.03, y * 2.03, amp * 0.5
        return s / tot


def filaments(noise, x, y, sharp=10.0):
    """Thin bright ridges (0..1) from a noise value."""
    v = 1.0 - abs(noise(x, y))
    return v ** sharp

# --------------------------------------------------------------------------- strip bolts


def make_strip_bolt(seed, w, h, main_band=0.17, branch_band=0.40, r=1.45, levels=3, nbranch=7, sparks=2,
                    step=(0.45, 1.25), maxang=52):
    rng = random.Random(seed)
    cy = h / 2
    main = walk(rng, (-0.02 * w, cy), (1.02 * w, cy), main_band * h, step, maxang, 0.35, 2, 0.0, 0.0)
    paths = [attrib(main, r * 1.1, r * 0.85, 1.0, 0.9, rng, 0.3)]
    add_branches(rng, paths, main, r, 0.92, levels, nbranch, length=(0.08, 0.22),
                 bounds=(0, w, cy - branch_band * h, cy + branch_band * h))
    sp = spark_points(rng, main, sparks, (h * 0.10, h * 0.30), (0.7, 1.05))
    return paths, sp, main


def tex_bolt(seed, style="hot"):
    w, h = 512, 128
    paths, sp, main = make_strip_bolt(seed, w, h)
    if style == "hot":
        # tight halo: vanilla writes depth for every texel with alpha >= 0.1, so a wide halo
        # would hide whatever translucent card lies under the bolt (decals)
        return render_bolt(w, h, paths, sp, glow=(2.3, 2.2, 0.6), halo=(4.0, 5.0, 0.16))
    rng = random.Random(seed * 7 + 1)
    vn = ValueNoise(seed + 99)
    nz = lambda x, y: vn.fbm(x / 22.0, y / 22.0, 4) * 1.6
    if style == "after":
        diss = sample_fn(w, h, lambda x, y: 0.55 + 0.45 * smooth(-0.45, 0.35, nz(x, y)), 4)
        wide = [(x, y, r * 1.5 + 0.6, a * 0.85) for x, y, r, a in paths[0]]
        return render_bolt(w, h, [wide] + paths[1:], (), glow=(3.2, 4.0, 0.75), halo=(8.0, 12.0, 0.42),
                           lut=AFTER, dissolve=diss.d)
    diss = sample_fn(w, h, lambda x, y: smooth(-0.15, 0.55, nz(x, y)), 4)
    embers = spark_points(rng, main, 9, (0, h * 0.08), (0.6, 1.0), (0.45, 0.75))
    wide = [(x, y, r * 1.3 + 0.5, a * 0.85) for x, y, r, a in paths[0]]
    diss = [0.25 + 0.75 * v for v in diss.d]
    return render_bolt(w, h, [wide] + paths[1:4], embers, glow=(3.6, 5.0, 0.8), halo=(9.0, 14.0, 0.5),
                       lut=FADE, dissolve=diss, spark_lut=AFTER)


def tex_blade(seed):
    w, h = 512, 64
    paths, sp, main = make_strip_bolt(seed, w, h, main_band=0.08, branch_band=0.36, r=1.3, levels=2, nbranch=12,
                                      sparks=2, step=(0.8, 2.4), maxang=58)
    return render_bolt(w, h, paths, sp, glow=(2.2, 2.0, 0.58), halo=(4.0, 4.0, 0.16))


def tex_rim_crackle(seed):
    """Crackle for laying ON another translucent card: vanilla writes depth wherever alpha >= 0.1,
    so the visible glow stays within ~5 px of the core (no wide halo that would punch holes)."""
    w, h = 512, 64
    paths, sp, main = make_strip_bolt(seed, w, h, main_band=0.10, branch_band=0.30, r=1.25, levels=2, nbranch=10,
                                      sparks=0, step=(0.8, 2.2), maxang=58)
    return render_bolt(w, h, paths, (), glow=(1.8, 1.2, 0.55), halo=(2.5, 2.0, 0.10))


def tex_blade_trail(seed):
    w, h = 512, 64
    rng = random.Random(seed)
    vn = ValueNoise(seed + 5)
    nz = lambda x, y: vn.fbm(x / 26.0, y / 14.0, 4) * 1.6
    paths = []
    for k in range(4):
        cy = h * (0.5 + rng.uniform(-0.12, 0.12))
        pts = jag(rng, (-0.02 * w, cy), (1.02 * w, cy + rng.uniform(-0.15, 0.15) * h), 5,
                  (0.06, 0.1, 0.12, 0.14, 0.12))
        pts = clamp_pts(pts, -w, 2 * w, h * 0.22, h * 0.78)
        amp = 1.0 if k == 0 else rng.uniform(0.35, 0.6)
        paths.append(attrib(pts, (1.6 if k == 0 else 0.9), (3.0 if k == 0 else 1.6), amp, amp * 0.05, rng, 0.3))
    diss = sample_fn(w, h, lambda x, y: (1 - 0.8 * x / w) + 0.8 * x / w * smooth(-0.3, 0.6, nz(x, y)), 4)
    return render_bolt(w, h, paths, (), glow=(2.6, 3.0, 0.75), halo=(5.0, 8.0, 0.40), lut=AFTER,
                       dissolve=diss.d, win=window(w, h, w * 0.04, h * 0.12))

# --------------------------------------------------------------------------- columns


def make_vbolt(seed, w=128, h=512, r=2.2):
    rng = random.Random(seed)
    cx = w / 2
    main = walk(rng, (cx, -0.03 * h), (cx, 0.955 * h), 0.2 * w, (0.5, 1.5), 55, 0.3, 2, rng.uniform(-3, 3), 0.0)
    paths = [attrib(main, r * 0.8, r * 1.05, 0.95, 1.0, rng, 0.25)]

    def down(p, rg):
        return 1 if rg.random() < 0.5 else -1
    add_branches(rng, paths, main[:-6], r, 0.95, 3, 6, spread=(16, 40), length=(0.08, 0.22),
                 bounds=(w * 0.08, w * 0.92, 0, h * 0.97), bias=down)
    sp = spark_points(rng, main[len(main) // 3:], 2, (w * 0.08, w * 0.22), (0.7, 1.05))
    return paths, sp, main


def impact_extra(w, h, cx, cy, rx, ry, amp):
    out = [0.0] * (w * h)
    y0, y1 = max(0, int(cy - 3 * ry)), min(h, int(cy + 3 * ry) + 1)
    for y in range(y0, y1):
        dy = (y + 0.5 - cy) / ry
        for x in range(w):
            dx = (x + 0.5 - cx) / rx
            q = dx * dx + dy * dy
            if q < 9:
                out[y * w + x] = amp * GAUSS[int(q * 256)]
    return out


def tex_vbolt(seed, style="hot"):
    """Crossed vertical cards write depth wherever alpha >= 0.1 (vanilla), so the visible halo
    is kept narrow (it would otherwise hide the floor decal behind the pillar)."""
    w, h = 128, 512
    paths, sp, main = make_vbolt(seed, w, h)
    bloom = impact_extra(w, h, main[-1][0], h * 0.965, w * 0.16, h * 0.022, 0.75)
    win = ([smooth(0, w * 0.3, x + 0.5) * smooth(0, w * 0.3, w - x - 0.5) for x in range(w)],
           [smooth(0, h * 0.04, y + 0.5) * smooth(0, h * 0.015, h - y - 0.5) for y in range(h)])
    if style == "hot":
        return render_bolt(w, h, paths, sp, glow=(2.2, 2.0, 0.6), halo=(4.5, 5.0, 0.26), extra=bloom, win=win)
    vn = ValueNoise(seed + 33)
    diss = sample_fn(w, h, lambda x, y: 0.5 + 0.5 * smooth(-0.4, 0.4, 1.6 * vn.fbm(x / 18.0, y / 30.0, 4)), 4)
    wide = [(x, y, r * 1.5 + 0.6, a * 0.85) for x, y, r, a in paths[0]]
    return render_bolt(w, h, [wide] + paths[1:], (), glow=(3.0, 3.0, 0.75), halo=(5.5, 6.0, 0.36),
                       lut=AFTER, dissolve=diss.d, extra=[v * 0.6 for v in bloom], win=win)


def tex_pillar(seed):
    w, h = 128, 512
    rng = random.Random(seed)
    paths = []
    for k in range(3):
        ph = rng.uniform(0, 6.28)
        amp = w * rng.uniform(0.12, 0.2)
        turns = rng.uniform(1.6, 2.6)
        base = [(w / 2 + amp * math.sin(ph + turns * 6.28 * t), -0.02 * h + 1.04 * h * t) for t in [i / 48 for i in range(49)]]
        pts = []
        for p, q in zip(base, base[1:]):
            pts += jag(rng, p, q, 2, (0.3, 0.25))[:-1]
        pts.append(base[-1])
        paths.append(attrib(pts, 1.5 if k == 0 else 1.1, 1.5 if k == 0 else 1.1, 0.95 if k == 0 else 0.75, 0.9, rng, 0.45))
    col = [0.0] * (w * h)
    for y in range(h):
        for x in range(w):
            q = ((x + 0.5 - w / 2) / (w * 0.16)) ** 2
            if q < 9:
                col[y * w + x] = 0.32 * GAUSS[int(q * 256)]
    sp = [(w / 2 + rng.uniform(-0.3, 0.3) * w, rng.uniform(0.1, 0.9) * h, rng.uniform(0.9, 1.4), 0.9) for _ in range(4)]
    return render_bolt(w, h, paths, sp, glow=(2.4, 2.5, 0.6), halo=(6.0, 8.0, 0.28), extra=col,
                       win=window(w, h, w * 0.1, h * 0.08))


def tex_charge_spark(seed):
    w, h = 64, 128
    rng = random.Random(seed)
    main = jag(rng, (w / 2, h * 0.97), (w / 2 + rng.uniform(-8, 8), h * 0.12), 5, (0.22, 0.26, 0.24, 0.2, 0.16))
    main = clamp_pts(main, w * 0.2, w * 0.8, 0, h)
    paths = [attrib(main, 2.0, 0.5, 1.0, 0.45, rng, 0.15)]
    add_branches(rng, paths, main, 1.6, 0.85, 2, 3, spread=(20, 45), length=(0.15, 0.3),
                 bounds=(w * 0.1, w * 0.9, 0, h))
    bloom = impact_extra(w, h, w / 2, h * 0.95, w * 0.22, h * 0.05, 0.8)
    return render_bolt(w, h, paths, (), glow=(2.4, 2.0, 0.6), halo=(5.0, 6.0, 0.3), extra=bloom,
                       win=window(w, h, w * 0.12, h * 0.04))

# --------------------------------------------------------------------------- arcs / rings


def bezier(p0, p1, p2, n):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]


def jag_curve(rng, base, depth=3, rough=(0.3, 0.26, 0.2)):
    out = []
    for p, q in zip(base, base[1:]):
        out += jag(rng, p, q, depth, rough)[:-1]
    out.append(base[-1])
    return out


def tex_arc(seed):
    w, h = 256, 128
    rng = random.Random(seed)
    base = bezier((0.06 * w, 0.86 * h), (0.5 * w, -0.42 * h), (0.94 * w, 0.86 * h), 14)
    main = jag_curve(rng, base)
    main = clamp_pts(main, 4, w - 4, 6, h - 6)
    paths = [attrib(main, 1.9, 1.9, 1.0, 1.0, rng, 0.25, 0.08)]
    add_branches(rng, paths, main, 1.7, 0.9, 2, 5, length=(0.06, 0.16), bounds=(4, w - 4, 4, h - 4))
    sp = spark_points(rng, main, 3, (6, 18))
    return render_bolt(w, h, paths, sp, glow=(2.3, 2.5, 0.6), halo=(5.5, 8.0, 0.3))


def circle_pts(cx, cy, r, n, a0=0.0, a1=2 * math.pi):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def tex_chakra(seed):
    w = h = 256
    rng = random.Random(seed)
    c = w / 2
    R = 0.40 * w
    paths = []
    for k in range(2):
        ph = rng.uniform(0, 6.28)
        base = [(c + (R + rng.uniform(-3, 3)) * math.cos(ph + 6.2832 * i / 36),
                 c + (R + rng.uniform(-3, 3)) * math.sin(ph + 6.2832 * i / 36)) for i in range(37)]
        base[-1] = base[0]
        pts = jag_curve(rng, base, 2, (0.32, 0.25))
        paths.append(attrib(pts, 1.8 if k == 0 else 1.2, 1.8 if k == 0 else 1.2, 1.0 if k == 0 else 0.7, 1.0 if k == 0 else 0.7, rng, 0.35))
    for _ in range(7):
        a = rng.uniform(0, 6.28)
        da = rng.uniform(0.25, 0.5)
        out = rng.choice((1, -1))
        mid = a + da / 2
        p0 = (c + R * math.cos(a), c + R * math.sin(a))
        p2 = (c + R * math.cos(a + da), c + R * math.sin(a + da))
        p1 = (c + (R + out * rng.uniform(14, 26)) * math.cos(mid), c + (R + out * rng.uniform(14, 26)) * math.sin(mid))
        pts = jag_curve(rng, bezier(p0, p1, p2, 6), 2)
        paths.append(attrib(pts, 1.1, 0.8, 0.8, 0.6, rng, 0.3))
    sp = [(c + (R + rng.uniform(-18, 18)) * math.cos(a), c + (R + rng.uniform(-18, 18)) * math.sin(a), rng.uniform(0.9, 1.4), 0.9)
          for a in [rng.uniform(0, 6.28) for _ in range(5)]]
    return render_bolt(w, h, paths, sp, glow=(2.4, 2.5, 0.6), halo=(6.0, 8.0, 0.32))


def radial_field(w, h, fn):
    c = w / 2
    out = [0.0] * (w * h)
    for y in range(h):
        dy = y + 0.5 - h / 2
        for x in range(w):
            dx = x + 0.5 - c
            out[y * w + x] = fn(math.sqrt(dx * dx + dy * dy), math.atan2(dy, dx))
    return out


def tex_orb_core():
    w = h = 128

    def f(r, th):
        q1 = (r / 9.0) ** 2
        q2 = (r / 24.0) ** 2
        q3 = (r / 44.0) ** 2
        return sum(k * GAUSS[int(q * 256)] for q, k in ((q1, 0.9), (q2, 0.5), (q3, 0.32)) if q < 9)
    img = Img(w, h)
    img.over(ELECTRO, radial_field(w, h, f), 1.0, window(w, h, 6, 6))
    return img


def tex_glow_soft():
    w = h = 64

    def f(r, th):
        q = (r / 15.0) ** 2
        return 0.75 * GAUSS[int(q * 256)] if q < 9 else 0.0
    img = Img(w, h)
    img.over(ELECTRO, radial_field(w, h, f), 1.0, window(w, h, 4, 4))
    return img


def tex_glow_strip():
    w, h = 256, 32
    E = [0.0] * (w * h)
    for y in range(h):
        q = ((y + 0.5 - h / 2) / 6.0) ** 2
        g = 0.8 * GAUSS[int(q * 256)] if q < 9 else 0.0
        q2 = ((y + 0.5 - h / 2) / 1.6) ** 2
        g += 0.5 * GAUSS[int(q2 * 256)] if q2 < 9 else 0.0
        for x in range(w):
            E[y * w + x] = g
    img = Img(w, h)
    img.over(ELECTRO, E, 1.0, window(w, h, w * 0.08, 3))
    return img


def tex_spark():
    w = h = 32

    def f(r, th):
        q = (r / 2.2) ** 2
        q2 = (r / 7.0) ** 2
        return (1.1 * GAUSS[int(q * 256)] if q < 9 else 0) + (0.45 * GAUSS[int(q2 * 256)] if q2 < 9 else 0)
    img = Img(w, h)
    img.over(CYAN, radial_field(w, h, f), 1.0, window(w, h, 3, 3))
    return img


def tex_glint():
    w = h = 64

    def f(r, th):
        c, s = abs(math.cos(th)), abs(math.sin(th))
        ray = 0.0
        for k, cw in ((c, 1.0), (s, 1.0)):
            across = r * math.sqrt(max(0.0, 1 - k * k))
            along = r * k
            q = (across / 1.1) ** 2
            if q < 9:
                ray = max(ray, cw * GAUSS[int(q * 256)] * math.exp(-along / 11.0))
        d1 = abs(math.cos(th - math.pi / 4)) if True else 0
        dd = abs(math.sin(th - math.pi / 4)) * r
        q = (dd / 0.9) ** 2
        diag = 0.45 * GAUSS[int(q * 256)] * math.exp(-r / 6.0) if q < 9 else 0.0
        q = (r / 2.0) ** 2
        core = 1.1 * GAUSS[int(q * 256)] if q < 9 else 0
        q = (r / 8.0) ** 2
        halo = 0.3 * GAUSS[int(q * 256)] if q < 9 else 0
        dd2 = abs(math.sin(th + math.pi / 4)) * r
        q = (dd2 / 0.9) ** 2
        diag2 = 0.45 * GAUSS[int(q * 256)] * math.exp(-r / 6.0) if q < 9 else 0.0
        return core + ray + max(diag, diag2) + halo
    img = Img(w, h)
    img.over(ELECTRO, radial_field(w, h, f), 1.0, window(w, h, 3, 3))
    return img


def tex_flash(seed):
    w = h = 256
    rng = random.Random(seed)
    rays = [(rng.uniform(0, 6.28), rng.uniform(0.5, 0.9), rng.uniform(22, 44)) for _ in range(8)]

    def f(r, th):
        e = 0.0
        for q, k in (((r / 10.0) ** 2, 1.2), ((r / 30.0) ** 2, 0.6), ((r / 62.0) ** 2, 0.34)):
            if q < 9:
                e += k * GAUSS[int(q * 256)]
        for a, k, ln in rays:
            da = math.atan2(math.sin(th - a), math.cos(th - a))
            across = abs(da) * r
            q = (across / (1.2 + r * 0.03)) ** 2
            if q < 9:
                e += k * 0.7 * GAUSS[int(q * 256)] * math.exp(-r / ln)
        return e
    img = Img(w, h)
    img.over(ELECTRO, radial_field(w, h, f), 1.0, window(w, h, 10, 10))
    return img


def tex_impact_sparks(seed):
    w = h = 256
    rng = random.Random(seed)
    c = w / 2
    paths = []
    sparks = []
    for _ in range(34):
        a = rng.uniform(0, 6.28)
        r0 = rng.uniform(6, 26)
        r1 = r0 + rng.uniform(22, 92)
        bend = rng.uniform(-0.12, 0.12)
        pts = [(c + (r0 + (r1 - r0) * t) * math.cos(a + bend * t), c + (r0 + (r1 - r0) * t) * math.sin(a + bend * t)) for t in [i / 6 for i in range(7)]]
        if rng.random() < 0.4:
            sparks.append((pts[-1][0], pts[-1][1], rng.uniform(0.9, 1.5), 0.9))
        paths.append(attrib(pts, rng.uniform(0.8, 1.4), 0.3, rng.uniform(0.6, 1.0), 0.1, rng))
    flash = radial_field(w, h, lambda r, th: sum(k * GAUSS[int(q * 256)] for q, k in (((r / 8.0) ** 2, 1.1), ((r / 26.0) ** 2, 0.45)) if q < 9))
    return render_bolt(w, h, paths, sparks, glow=(2.4, 1.5, 0.55), halo=(5.0, 6.0, 0.26), extra=flash,
                       win=window(w, h, 10, 10))


def tex_scorch(seed):
    w = h = 256
    rng = random.Random(seed)
    nz = WaveNoise(seed, 6, 0.06)
    cracks = []
    for _ in range(9):
        a = rng.uniform(0, 6.28)
        p0 = (w / 2 + 14 * math.cos(a), h / 2 + 14 * math.sin(a))
        p1 = (w / 2 + rng.uniform(60, 108) * math.cos(a), h / 2 + rng.uniform(60, 108) * math.sin(a))
        cracks.append(attrib(jag(rng, p0, p1, 4), 1.1, 0.4, 0.55, 0.1, rng))
    cf = Field(w, h)
    for p in cracks:
        stroke(cf, p, 1, 1.8, 0.8)

    def burn(r, th):
        return 0.62 * (1 - smooth(w * 0.12, w * 0.44, r)) * (0.8 + 0.2 * nz(r * math.cos(th), r * math.sin(th)))

    def ember(r, th):
        d = (r - w * 0.27) / 9.0
        q = d * d
        e = 0.5 * GAUSS[int(q * 256)] if q < 9 else 0.0
        return e * (0.55 + 0.45 * nz(th * 40, 3.0))
    win = window(w, h, 10, 10)
    img = Img(w, h)
    img.over(solid((24, 8, 40)), [b + c for b, c in zip(radial_field(w, h, burn), cf.d)], 1.0, win)
    img.over(AFTER, radial_field(w, h, ember), 1.0, win)
    return img


def tex_scorch_strip(seed):
    w, h = 256, 64
    rng = random.Random(seed)
    nz = WaveNoise(seed, 6, 0.08)
    E = [0.0] * (w * h)
    for y in range(h):
        for x in range(w):
            env = math.sin(math.pi * (x + 0.5) / w) ** 0.6
            d = (y + 0.5 - h / 2) / (h * 0.22 * env + 1e-3)
            q = d * d
            E[y * w + x] = 0.55 * env * GAUSS[int(q * 256)] * (0.75 + 0.25 * nz(x, y)) if q < 9 else 0.0
    emb = [(rng.uniform(0.08, 0.92) * w, h / 2 + rng.uniform(-0.15, 0.15) * h, rng.uniform(0.8, 1.3), rng.uniform(0.4, 0.7)) for _ in range(10)]
    S = Field(w, h)
    for x, y, r, a in emb:
        dot(S, x, y, r * 2.2 + 1.5, a, 1)
    win = window(w, h, w * 0.06, 4)
    img = Img(w, h)
    img.over(solid((24, 8, 40)), E, 1.0, win)
    img.over(AFTER, S, 1.0, win)
    return img

# --------------------------------------------------------------------------- crescents / slashes / rifts


CRESCENT_W, CRESCENT_H = 352, 176       # S1-KIT reclaim (was 512 x 256); same uv convention


def tex_crescent(seed, bolt):
    w, h = CRESCENT_W, CRESCENT_H
    s = h / 256.0
    rng = random.Random(seed)
    cx, cy = w / 2, h * 1.0
    R = 0.94 * h
    phimax = math.radians(72)
    nz = WaveNoise(seed, 5, 1.0)
    G = GAUSS

    def f(x, y):
        dx, dy = x - cx, cy - y
        r = math.hypot(dx, dy)
        phi = math.atan2(dx, dy)
        u = abs(phi) / phimax
        if u >= 1:
            return 0.0
        env = (1 - u * u) ** 1.3
        thick = h * (0.06 + 0.30 * env)
        d = r - R * (1 - 0.03 * u * u)
        q = (d / ((1.6 + 2.2 * env) * max(s, 0.8))) ** 2
        edge = (1.05 * G[int(q * 256)] if q < 9 else 0.0) * (0.35 + 0.65 * env)
        q = (d / ((6 + 8 * env) * s)) ** 2
        glow = 0.4 * env * G[int(q * 256)] if q < 9 else 0.0
        body = 0.0
        if d < 0:
            t = -d / thick
            if t < 1.6:
                streak = 0.7 + 0.3 * nz(phi * 22, r * 0.06 / s)
                body = 0.62 * env * math.exp(-2.2 * t) * streak
        return edge + glow + body
    E = sample_fn(w, h, f, 1)
    if not bolt:
        img = Img(w, h)
        img.over(ELECTRO, E, 1.0, window(w, h, 5, 5))
        return img
    base = [(cx + R * 0.985 * math.sin(p), cy - R * 0.985 * math.cos(p)) for p in [-phimax * 0.92 + 2 * phimax * 0.92 * i / 24 for i in range(25)]]
    main = jag_curve(rng, base, 3, (0.35, 0.3, 0.22))
    paths = [attrib(main, 1.5, 1.5, 1.0, 1.0, rng, 0.3, 0.06)]
    add_branches(rng, paths, main, 1.3, 0.85, 2, 9, length=(0.03, 0.08), bounds=(3, w - 3, 3, h - 3))
    sp = spark_points(rng, main, 4, (6, 17))
    return render_bolt(w, h, paths, sp, glow=(2.0, 2.0, 0.6), halo=(4.0, 5.5, 0.3), extra=E.d)


def tex_slash_wave(seed):
    w, h = 512, 128
    nz = WaveNoise(seed, 5, 0.6)
    G = GAUSS

    def f(x, y):
        u = (x + 0.5) / w
        env = math.sin(math.pi * u) ** 0.8
        if env <= 0:
            return 0.0
        e0 = h * (0.30 + 0.06 * (1 - env))
        d = y - e0
        q = (d / (1.4 + 2.0 * env)) ** 2
        edge = 1.05 * env * G[int(q * 256)] if q < 9 else 0.0
        q = (d / (5 + 6 * env)) ** 2
        glow = 0.35 * env * G[int(q * 256)] if q < 9 else 0.0
        body = 0.0
        if d > 0:
            t = d / (h * 0.55 * env + 1e-3)
            if t < 1.5:
                body = 0.6 * env * math.exp(-2.4 * t) * (0.7 + 0.3 * nz(x * 0.05, y * 0.6))
        return edge + glow + body
    img = Img(w, h)
    img.over(ELECTRO, sample_fn(w, h, f, 1), 1.0, window(w, h, 8, 5))
    return img


def tex_rift(seed):
    w, h = 512, 64
    rng = random.Random(seed)
    main = walk(rng, (-0.02 * w, h / 2), (1.02 * w, h / 2), h * 0.12, (0.8, 2.6), 60, 0.3, 2, 0.0, 0.0)
    paths = [attrib(main, 1.4, 1.4, 1.0, 1.0, rng, 0.2, 0.1)]
    add_branches(rng, paths, main, 1.0, 0.7, 1, 6, length=(0.02, 0.05), bounds=(0, w, h * 0.2, h * 0.8))
    env = [math.sin(math.pi * (x + 0.5) / w) ** 0.7 for x in range(w)]
    dark = [0.0] * (w * h)
    lips = [0.0] * (w * h)
    for y in range(h):
        for x in range(w):
            d = abs(y + 0.5 - h / 2) / (h * 0.30 * env[x] + 1e-3)
            dark[y * w + x] = 0.78 * (1 - smooth(0.55, 1.0, d))
            q = ((d - 0.85) / 0.22) ** 2
            lips[y * w + x] = 0.45 * env[x] * GAUSS[int(q * 256)] if q < 9 else 0.0
    win = window(w, h, w * 0.05, 4)
    img = Img(w, h)
    img.over(VOIDP, dark, 1.0, win)
    img.over(ELECTRO, lips, 1.0, win)
    bolt = render_bolt(w, h, paths, (), glow=(2.0, 1.5, 0.5), halo=(4.0, 4.0, 0.2), win=win)
    over_img(img, bolt)
    return img


def over_img(dst, src):
    dst.r = [p + q * (1 - a) for p, q, a in zip(src.r, dst.r, src.a)]
    dst.g = [p + q * (1 - a) for p, q, a in zip(src.g, dst.g, src.a)]
    dst.b = [p + q * (1 - a) for p, q, a in zip(src.b, dst.b, src.a)]
    dst.a = [p + q * (1 - a) for p, q, a in zip(src.a, dst.a, src.a)]


def tex_shockwave(seed):
    """256 x 256 (S1-KIT reclaim; was 512): bright leading edge at r = 0.46 w, soft tail inward."""
    w = h = 256
    R = 0.46 * w
    nz = WaveNoise(seed, 6, 1.0)
    G = GAUSS

    def f(x, y):
        dx, dy = x - w / 2, y - h / 2
        r = math.hypot(dx, dy)
        d = r - R
        q = (d / 1.5) ** 2
        edge = 1.0 * G[int(q * 256)] if q < 9 else 0.0
        q = (d / 4.8) ** 2
        glow = 0.42 * G[int(q * 256)] if q < 9 else 0.0
        body = 0.0
        if d < 0:
            t = -d / (0.18 * w)
            if t < 2.0:
                th = math.atan2(dy, dx)
                body = 0.55 * math.exp(-2.0 * t) * (0.65 + 0.35 * nz(th * 30, r * 0.1))
        return edge + glow + body
    img = Img(w, h)
    img.over(ELECTRO, sample_fn(w, h, f, 1), 1.0, window(w, h, 5, 5))
    return img


def tex_crackle(seed):
    w, h = 512, 64
    rng = random.Random(seed)
    main = walk(rng, (-0.02 * w, h * 0.55), (1.02 * w, h * 0.55), h * 0.3, (0.35, 1.0), 62, 0.25, 2, 0.0, 0.0)
    paths = [attrib(main, 1.5, 1.5, 1.0, 1.0, rng, 0.35)]
    add_branches(rng, paths, main, 1.5, 0.85, 2, 12, spread=(50, 85), length=(0.02, 0.06), bounds=(0, w, h * 0.06, h * 0.95))
    floor = [0.0] * (w * h)
    for y in range(h):
        q = ((y + 0.5 - h * 0.93) / (h * 0.06)) ** 2
        g = 0.45 * GAUSS[int(q * 256)] if q < 9 else 0.0
        for x in range(w):
            floor[y * w + x] = g
    sp = spark_points(rng, main, 4, (6, 16))
    win = (window(w, h, w * 0.04, 3)[0], [smooth(0, 4, y + 0.5) for y in range(h)])
    return render_bolt(w, h, paths, sp, glow=(2.1, 1.6, 0.6), halo=(3.0, 3.0, 0.14), extra=floor, win=win)

# --------------------------------------------------------------------------- kit decals and travelling bands
# S1-KIT (plan rd/plan.md B.3, C.6). The only floor decals left are outline-like kit decals; every one is a UNIT
# sprite (radius 1 / width 1 x length 1) that build_raiden_hazard_vfx.py scales by the display transformation.
#   quarter  circle centre at texel (0, 0), radius 1 at KIT_QEXT * (1 / 1.12) of the side; mirrored into 4 cards.
#   dk_ring     thin bright ring (radius >= 6 b)        dk_ring_s  bolder ring + faint fill (radius < 6 b, stagger)
#   dk_rings3   3 concentric thin rings + violet fill (Musou orbs, footage A-09)
#   dk_disc     pale lavender fill, brighter rim (field lightning A-02)
#   dk_band     64 x 256 strip: u across the band (two edge lines at u 0.07 / 0.93), v along it (stretched)
#   dk_pool     256 x 256 centred dark smoky blot with a magenta rim (B-15 shadow pool / grown disc)
#   dk_tint     64 x 64 centred uniform violet, 35 % alpha, soft edge (time-stop / 만겁 field tint)
#   tr_band     32 x 256 ring-segment band: u along the chord (periodic, seamless), v across: bright front at
#               v ~0.05, violet tail fading to v = 1 (the expanding ring / wave cards, 24 per full ring)
KIT_QEXT = 1.12
KIT_DECALS = {
    "dk_ring": dict(w=256, h=256, kind="quarter", use="ring decal r >= 6 (eyes r 12)"),
    "dk_ring_s": dict(w=128, h=128, kind="quarter", use="ring decal r < 6 (eye 5, bomb 3.5, recovery 4.5, vajra 2.5, stagger)"),
    "dk_rings3": dict(w=256, h=256, kind="quarter", use="rings3 decal (Musou orbs r 4)"),
    "dk_disc": dict(w=128, h=128, kind="quarter", use="disc_pale decal (field lightning r 2.5)"),
    "dk_band": dict(w=64, h=256, kind="band", use="band decal (단절 w 5, to the wall)"),
    "dk_pool": dict(w=256, h=256, kind="radial", use="pool decal (shadow r 1.5 -> grown 4.5)"),
    "dk_tint": dict(w=64, h=64, kind="radial", use="tint (whole-field darkening)"),
    "tr_band": dict(w=32, h=256, kind="segment", use="travelling ring / wave segment card"),
}
VIOLET_FILL = solid((92, 46, 176))
SHADOW_FILL = solid((18, 6, 34))
TINT_FILL = solid((58, 30, 112))
PALE = ramp([(0.0, (200, 186, 255, 0)), (0.05, (200, 186, 255, 0)), (0.12, (206, 192, 255, 34)),
             (0.30, (222, 212, 255, 92)), (0.6, (238, 232, 255, 176)), (1.0, (255, 255, 255, 236))])


def _gs(d, sig):
    q = (d / sig) ** 2
    return GAUSS[int(q * 256)] if q < 9 else 0.0


def _quarter(n, fn, ds=1):
    sc = KIT_QEXT / n
    return sample_fn(n, n, lambda i, j: fn(math.hypot(i * sc, j * sc), math.atan2(j * sc, i * sc)), ds)


def _qwin(n, m=3):
    wx = [smooth(0, m, n - x - 0.5) for x in range(n)]
    return wx, wx


def tex_dk_ring(bold):
    n = 128 if bold else 256
    nz = WaveNoise(611 if bold else 607, 6, 1.0)
    core, glow, fill = (0.030, 0.085, 0.20) if bold else (0.011, 0.036, 0.16)

    def rim(r, th):
        mod = 0.86 + 0.14 * nz(th * 40, r * 9)
        return (0.92 * _gs(r - 1.0, core) + 0.50 * _gs(r - 1.0, glow) * mod)

    def body(r, th):
        if r >= 1.0:
            return 0.0
        return fill * smooth(0.72, 0.985, r) * (0.85 + 0.15 * nz(th * 18, r * 5))
    img = Img(n, n)
    win = _qwin(n)
    img.over(VIOLET_FILL, _quarter(n, body), 1.0, win)
    img.over(ELECTRO, _quarter(n, rim), 1.0, win)
    return img


def tex_dk_rings3():
    n = 256
    nz = WaveNoise(613, 6, 1.0)
    rings = ((1.0, 1.0), (0.69, 0.86), (0.38, 0.72))

    def rim(r, th):
        mod = 0.85 + 0.15 * nz(th * 36, r * 7)
        return sum(a * (1.0 * _gs(r - rr, 0.011) + 0.40 * _gs(r - rr, 0.034)) for rr, a in rings) * mod

    def body(r, th):
        return 0.0 if r >= 1.0 else 0.26 * smooth(1.0, 0.94, r) * (0.8 + 0.2 * nz(th * 12, r * 4))
    img = Img(n, n)
    win = _qwin(n)
    img.over(VIOLET_FILL, _quarter(n, body), 1.0, win)
    img.over(ELECTRO, _quarter(n, rim), 1.0, win)
    return img


def tex_dk_disc():
    n = 128
    nz = WaveNoise(617, 6, 1.0)

    def f(r, th):
        if r > 1.08:
            return 0.0
        fill = 0.23 * smooth(1.04, 0.97, r) * (0.9 + 0.1 * nz(th * 10, r * 6))
        return fill + 0.42 * _gs(r - 0.985, 0.022) + 0.14 * _gs(r - 0.985, 0.06)
    img = Img(n, n)
    img.over(PALE, _quarter(n, f), 1.0, _qwin(n))
    return img


def tex_dk_band():
    w, h = 64, 256
    nz = WaveNoise(619, 6, 1.0)

    def f(x, y):
        u = (x + 0.5) / w
        e = min(abs(u - 0.07), abs(u - 0.93))
        lines = 1.0 * _gs(e, 0.022) + 0.32 * _gs(e, 0.06)
        fill = 0.17 * (0.85 + 0.15 * nz(x * 0.2, y * 0.08)) if 0.07 <= u <= 0.93 else 0.0
        return lines * (0.88 + 0.12 * nz(y * 0.12, x * 0.05)) + fill
    img = Img(w, h)
    img.over(PALE, sample_fn(w, h, f, 1), 1.0, window(w, h, 2, 6))
    return img


def tex_dk_pool():
    n = 256
    vn = ValueNoise(623, 32)

    def edge(th):
        return 0.80 + 0.16 * vn.fbm(math.cos(th) * 2.2 + 3, math.sin(th) * 2.2 + 3, 3)

    def dark(x, y):
        dx, dy = (x - n / 2) / (n / 2), (y - n / 2) / (n / 2)
        r, th = math.hypot(dx, dy), math.atan2(dy, dx)
        re = edge(th)
        if r > re + 0.08:
            return 0.0
        smoke = 0.72 + 0.28 * vn.fbm(dx * 3.1 + 7, dy * 3.1 + 1, 4)
        return 0.88 * smooth(re + 0.06, re - 0.18, r) * smoke

    def rim(x, y):
        dx, dy = (x - n / 2) / (n / 2), (y - n / 2) / (n / 2)
        r, th = math.hypot(dx, dy), math.atan2(dy, dx)
        re = edge(th)
        return 0.55 * _gs(r - re + 0.04, 0.035) * (0.6 + 0.4 * vn.fbm(th * 3 + 11, 2.0, 2))
    img = Img(n, n)
    win = window(n, n, 4, 4)
    img.over(SHADOW_FILL, sample_fn(n, n, dark, 2), 1.0, win)
    img.over(TELE, sample_fn(n, n, rim, 2), 1.0, win)
    return img


def tex_dk_tint():
    n = 64

    def f(x, y):
        r = math.hypot(x - n / 2, y - n / 2) / (n / 2)
        return 0.36 * smooth(1.0, 0.975, r)       # nearly hard edge: the card reaches 24.6 b, under the wall
    img = Img(n, n)
    img.over(TINT_FILL, sample_fn(n, n, f, 1), 1.0)
    return img


def tex_tr_band():
    w, h = 32, 256
    rng = random.Random(631)
    ph = [rng.uniform(0, 6.283) for _ in range(4)]

    def f(x, y):
        u = (x + 0.5) / w
        t = (y + 0.5) / h
        wisp = 0.78 + 0.12 * math.sin(2 * math.pi * u + ph[0] + 9 * t) + 0.10 * math.sin(4 * math.pi * u + ph[1] - 15 * t)
        front = 1.1 * _gs(t - 0.05, 0.02) + 0.55 * _gs(t - 0.05, 0.07)
        tail = 0.82 * math.exp(-1.7 * max(0.0, t - 0.05)) * wisp if t > 0.03 else 0.0
        return (front + tail) * smooth(1.0, 0.86, t) * smooth(0.0, 0.02, t)
    img = Img(w, h)
    img.over(ELECTRO, sample_fn(w, h, f, 1), 1.0)
    return img


def kit_entries():
    fns = {"dk_ring": lambda: tex_dk_ring(False), "dk_ring_s": lambda: tex_dk_ring(True), "dk_rings3": tex_dk_rings3,
           "dk_disc": tex_dk_disc, "dk_band": tex_dk_band, "dk_pool": tex_dk_pool, "dk_tint": tex_dk_tint,
           "tr_band": tex_tr_band}
    out = []
    for name, spec in KIT_DECALS.items():
        core = {"quarter": f"circle centre at texel (0,0), unit radius at {1 / KIT_QEXT:.4f} of the side",
                "band": "u across (edge lines at u 0.07 / 0.93), v along the band",
                "radial": "centred at (0.5, 0.5), unit radius = half the side",
                "segment": "u along the chord (periodic), v across: front at v 0.05, tail to v 1"}[spec["kind"]]
        out.append(entry(name, spec["w"], spec["h"], spec["kind"], "radial" if spec["kind"] != "band" else "v", core,
                         spec["use"], fns[name], "kit sprite (build_raiden_hazard_vfx.py scales it per hazard)"))
    return out

# --------------------------------------------------------------------------- rig (boss body) sprites
# Painted for build_raiden_rig.mjs (fx_weapon/* and death_shard_* models). Card rectangles are in
# item-model pixels; the rig maps them exactly, so keep these constants in sync with the .mjs.
# Blade sheath card, in the blade plane: model y RIG_KY0..RIG_KY1 -> u (hilt -> tip),
# model x RIG_KX0..RIG_KX1 -> v (cutting edge side first).
RIG_KX0, RIG_KX1, RIG_KY0, RIG_KY1 = 2.6, 12.0, 9.6, 32.0
RIG_KW, RIG_KH = 224, 112
# Palm card, parallel to the palm: model x RIG_PX0..RIG_PX1 -> u (thumb side first),
# model y RIG_PY1..RIG_PY0 -> v (wrist at v=0, fingertips toward v=1).
RIG_PX0, RIG_PX1, RIG_PY0, RIG_PY1 = 1.6, 14.4, -6.4, 8.0
RIG_PW, RIG_PH = 128, 144
RIG_PALM_C = (8.0, 4.2)
# Fingertips of the open puppet hand, made symmetric about x=8 so a u-mirrored card swaps fingers.
RIG_TIPS = ((5.25, -3.4), (7.08, -4.8), (8.97, -4.8), (10.8, -3.4))


def rig_blade_outline(y):
    """Giant katana outline (model px) at height y -> (edge x, spine x); the shared blade fx hugs it."""
    t = min(1.0, max(0.0, (y - 11.5) / 19.9))
    c = 8 + 1.3 * t * t
    hb = (2.7 - 0.75 * t) / 2
    return c - hb + smooth(28.4, 31.4, y) * (2 * hb - 0.6), c + hb


def _rig_curve_path(rng, ys, ye, xfun, band, sx, sy, step, maxang):
    """Jagged path following x = xfun(y) for y ys..ye (model px) -> blade-card texel points (u, v)."""
    pts = walk(rng, (0.0, 0.0), ((ye - ys) * sx, 0.0), band, step, maxang, 0.35, 2, 0.0, 0.0)
    return [(s + (ys - RIG_KY0) * sx, (xfun(ys + s / sx) - RIG_KX0) * sy + o) for s, o in pts]


def tex_rig_katana(seed):
    """Blade sheath: hot bolt hugging the cutting edge (forks sweep outward and toward the tip),
    a thinner crackle along the spine, a fork leaping off the tip with a small bloom."""
    w, h = RIG_KW, RIG_KH
    sx, sy = w / (RIG_KY1 - RIG_KY0), h / (RIG_KX1 - RIG_KX0)
    rng = random.Random(seed)
    main = _rig_curve_path(rng, 9.9, 31.75, lambda y: rig_blade_outline(y)[0] - 0.38, 0.30 * sy, sx, sy, (0.5, 1.5), 56)
    paths = [attrib(main, 1.6, 1.3, 1.0, 0.95, rng, 0.28)]
    add_branches(rng, paths, main, 1.4, 0.92, 2, 8, spread=(24, 64), length=(0.07, 0.19),
                 bounds=(6, w - 6, 4, h * 0.56), bias=lambda p, rg: -1)
    spine = _rig_curve_path(rng, 10.6, 30.6, lambda y: rig_blade_outline(y)[1] + 0.32, 0.2 * sy, sx, sy, (0.6, 1.8), 58)
    paths.append(attrib(spine, 1.05, 0.85, 0.74, 0.62, rng, 0.4, 0.06))
    add_branches(rng, paths, spine, 0.95, 0.62, 1, 3, spread=(25, 60), length=(0.04, 0.1),
                 bounds=(6, w - 6, h * 0.45, h - 4), bias=lambda p, rg: 1)
    tip = main[-1]
    fork = walk(rng, (tip[0] - 6, tip[1]), (w - 7, tip[1] - rng.uniform(4, 9)), 2.5, (0.5, 1.4), 55, 0.3, 2, 0.0, 0.0)
    paths.append(attrib(fork, 1.25, 0.5, 0.95, 0.5, rng, 0.2))
    bloom = impact_extra(w, h, tip[0] - 2, tip[1], 4.5, 4.5, 0.55)
    sp = spark_points(rng, main, 2, (6, 14), (0.8, 1.1))
    return render_bolt(w, h, paths, sp, glow=(2.2, 1.8, 0.58), halo=(3.8, 4.0, 0.16), extra=bloom,
                       win=window(w, h, 8, 4))


def tex_rig_palm(seed):
    """Five arcs (four fingertips + thumb) converging into the palm centre, thin and dim at the
    tips, brighter where they gather; a small soft pool where they meet (no glowing ball)."""
    w, h = RIG_PW, RIG_PH
    sx, sy = w / (RIG_PX1 - RIG_PX0), h / (RIG_PY1 - RIG_PY0)
    px = lambda x, y: ((x - RIG_PX0) * sx, (RIG_PY1 - y) * sy)
    rng = random.Random(seed)
    cx, cy = RIG_PALM_C
    paths, sparks = [], []
    for x, y in RIG_TIPS + ((2.7, 0.2),):
        a = px(x, y)
        mid = px(x + (cx - x) * 0.25 + rng.uniform(-0.35, 0.35), (y + cy) * 0.5 - 0.6)
        pts = clamp_pts(jag_curve(rng, bezier(a, mid, px(cx + (x - cx) * 0.12, cy - 0.2), 8), 3, (0.34, 0.28, 0.2)),
                        3, w - 3, 3, h - 3)
        paths.append(attrib(pts, 1.0, 1.55, 0.72, 1.0, rng, 0.25))
        add_branches(rng, paths, pts, 1.0, 0.7, 1, 2, spread=(30, 70), length=(0.12, 0.28), bounds=(3, w - 3, 3, h - 3))
        sparks.append((a[0] + rng.uniform(-2, 2), a[1] + rng.uniform(1, 4), rng.uniform(0.8, 1.1), 0.8))
    c = px(cx, cy)
    pool = impact_extra(w, h, c[0], c[1], 5.5, 5.5, 0.42)
    return render_bolt(w, h, paths, sparks[:3], glow=(2.2, 2.0, 0.58), halo=(4.0, 5.0, 0.2), extra=pool,
                       win=window(w, h, 5, 5))


def tex_rig_crown(seed):
    """Release crown: eleven bolts radiating from r~0.09w to 0.36..0.47w with forks and end sparks,
    a broken crackling ring at r=0.31w, a faint inner ring; the centre itself stays dark."""
    w = h = 192
    rng = random.Random(seed)
    c = w / 2
    paths, sparks = [], []
    for k in range(11):
        a = 2 * math.pi * (k + rng.uniform(-0.3, 0.3)) / 11
        r0, r1 = w * rng.uniform(0.07, 0.11), w * rng.uniform(0.36, 0.47)
        da = rng.uniform(-0.15, 0.15)
        pts = walk(rng, (c + r0 * math.cos(a), c + r0 * math.sin(a)), (c + r1 * math.cos(a + da), c + r1 * math.sin(a + da)),
                   (r1 - r0) * 0.12, (0.5, 1.5), 55, 0.3, 2, 0.0, 0.0, free_end=True)
        pts = clamp_pts(pts, 5, w - 5, 5, h - 5)
        amp = rng.uniform(0.8, 1.0)
        paths.append(attrib(pts, 1.6, 0.6, amp, amp * 0.55, rng, 0.25))
        if rng.random() < 0.75:
            add_branches(rng, paths, pts, 1.2, 0.75, 1, rng.randint(1, 2), spread=(25, 55), length=(0.15, 0.3),
                         bounds=(5, w - 5, 5, h - 5))
        if rng.random() < 0.6:
            sparks.append((pts[-1][0], pts[-1][1], rng.uniform(0.9, 1.3), 0.9))
    R = w * 0.31
    a0 = rng.uniform(0, 6.28)
    for k in range(4):
        s = a0 + k * math.pi / 2 + rng.uniform(-0.15, 0.15)
        e = s + rng.uniform(0.75, 1.1)
        base = [(c + (R + rng.uniform(-2, 2)) * math.cos(s + (e - s) * i / 6),
                 c + (R + rng.uniform(-2, 2)) * math.sin(s + (e - s) * i / 6)) for i in range(7)]
        paths.append(attrib(jag_curve(rng, base, 2, (0.3, 0.24)), 1.05, 1.05, 0.7, 0.7, rng, 0.35, 0.12))
    G = GAUSS
    inner = radial_field(w, h, lambda r, th: 0.35 * G[int(((r - w * 0.085) / (w * 0.03)) ** 2 * 256)]
                         if abs(r - w * 0.085) < w * 0.09 else 0.0)
    return render_bolt(w, h, paths, sparks, glow=(2.3, 2.0, 0.6), halo=(4.5, 5.0, 0.22), extra=inner,
                       win=window(w, h, 6, 6))


def tex_rig_shard(seed):
    """Crystal splinter: pointed lens along v (tips at v=0.03 / 0.97, widest at 38% from the top),
    white core ridge, faint facet lines, lavender body, violet rim, soft outer glow."""
    w, h = 48, 128
    nz = WaveNoise(seed, 4, 0.25)
    widest = 0.38

    def half(v):
        if v <= 0.03 or v >= 0.97:
            return 0.0
        t = (v - 0.03) / 0.94
        if t < widest:
            return math.sin(0.5 * math.pi * t / widest) ** 0.9
        return math.cos(0.5 * math.pi * (t - widest) / (1 - widest)) ** 1.15
    ridge = 0.5 + 0.06 * math.sin(seed)

    def f(x, y):
        u, v = x / w, y / h
        hw = 0.40 * half(v)
        if hw <= 0:
            return 0.0
        d = abs(u - ridge) / hw
        if d > 1.6:
            return 0.0
        body = smooth(1.08, 0.86, d)
        facet = 0.18 * (1 - smooth(0.0, 0.45, abs(d - 0.55)))
        core = 0.55 * math.exp(-(d / 0.18) ** 2) * (0.6 + 0.4 * half(v))
        rim = 0.25 * math.exp(-((d - 0.95) / 0.1) ** 2)
        glow = 0.16 * math.exp(-((d - 1.0) / 0.3) ** 2)
        return (0.42 * body + facet) * (0.88 + 0.12 * nz(x * 0.5, y * 0.3)) + core + rim + glow
    img = Img(w, h)
    img.over(ELECTRO, sample_fn(w, h, f, 1), 1.0, window(w, h, 3, 3))
    return img

# --------------------------------------------------------------------------- object / blink / orb sprites
# Painted for build_raiden_object_vfx.py, build_raiden_movement.py and build_raiden_orb.py
# (cards built with tools/raiden_obj_cards.py).


def _obj_g(q):
    return GAUSS[int(q * 256)] if q < 9 else 0.0


def tex_obj_swing_band(seed):
    """Illusion swing ribbon seen from the side: u=0 oldest (swing start) -> u=1 newest (blade
    end), bright white end with a gradient tail; the edge line descends from v=0.27 at u=0 to
    v=0.73 at u=1 (the level cut drops slightly), a crackle rides its newer part."""
    w, h = 512, 64
    rng = random.Random(seed)
    vn = ValueNoise(seed + 3)

    def cy(x):
        return h * (0.27 + 0.46 * x / w)

    def f(x, y):
        t = x / w
        env = smooth(0.0, 0.8, t) * (1 - smooth(0.955, 1.0, t))
        if env <= 0:
            return 0.0
        d = y - cy(x)
        r = 0.55 + 1.9 * t ** 1.4
        core = (0.25 + 0.85 * t ** 1.3) * smooth(-0.6, 0.6, r - abs(d))
        sig = 2.2 + 4.5 * (1 - t)
        glow = 0.42 * _obj_g((d / sig) ** 2)
        wide = 0.22 * _obj_g((d / (7 + 6 * (1 - t))) ** 2)
        fil = 0.0
        for off, a in ((-4.5, 0.32), (4.0, 0.26), (-8.5, 0.16), (8.0, 0.14)):
            dd = d - off * (0.6 + 0.6 * (1 - t))
            fil = max(fil, a * _obj_g((dd / 0.9) ** 2) * (0.6 + 0.4 * math.sin(x * 0.07 + off)))
        older = 0.45 + 0.55 * smooth(0.05, 0.6, t)
        diss = 1.0 if t > 0.55 else 0.55 + 0.45 * smooth(-0.35, 0.25, vn.fbm(x / 20.0, y / 6.0, 3) * 1.6 + (t - 0.3))
        return env * (core + (glow + wide + fil) * older) * diss
    E = sample_fn(w, h, f, 1)
    main = walk(rng, (0.30 * w, cy(0.30 * w)), (0.985 * w, cy(0.985 * w)), 2.6, (0.8, 2.2), 58, 0.3, 2, 0.0, 0.0)
    paths = [attrib(main, 0.55, 0.95, 0.55, 0.95, rng, 0.3, 0.06)]
    add_branches(rng, paths, main, 0.8, 0.75, 1, 6, spread=(25, 60), length=(0.015, 0.04), bounds=(0, w, 4, h - 4))
    tail = main[-1]
    sp = [(tail[0] - rng.uniform(4, 30), tail[1] + rng.uniform(-10, 10), rng.uniform(0.8, 1.2), 0.9) for _ in range(3)]
    return render_bolt(w, h, paths, sp, glow=(2.0, 1.2, 0.5), halo=(3.0, 2.0, 0.12), extra=E.d, win=window(w, h, 6, 4))


def tex_obj_wave_band(seed, fade=False):
    """Flying sword-wave front seen face-on: lens-shaped band along u (tips at u=0/1), white
    core line at v=0.5 with layered lavender/violet glow and a crackle along the core (hot), or
    a dissolving purple afterglow with embers (fade)."""
    w, h = 512, 64
    rng = random.Random(seed)
    vn = ValueNoise(seed + 9)

    def f(x, y):
        t = (x + 0.5) / w
        env = math.sin(math.pi * t) ** 0.75
        if env <= 0:
            return 0.0
        d = y + 0.5 - h / 2
        r = 0.5 + 2.1 * env
        core = (0.55 + 0.6 * env) * smooth(-0.6, 0.6, r - abs(d))
        inner = 0.55 * env * _obj_g((d / (2.0 + 5.0 * env)) ** 2)
        outer = 0.30 * env * _obj_g((d / (5.0 + 11.0 * env)) ** 2)
        lay = 0.0
        for off, a in ((-1, 0.36), (1, 0.30)):
            dd = d - off * (5.0 + 7.5 * env)
            lay = max(lay, a * env * _obj_g((dd / (0.8 + 0.6 * env)) ** 2))
        if fade:
            diss = 0.3 + 0.7 * smooth(-0.3, 0.45, vn.fbm(x / 18.0, y / 7.0, 4) * 1.6)
            return (core * 0.55 + inner * 1.1 + outer * 1.3 + lay * 0.6) * diss
        return core + inner + outer + lay
    E = sample_fn(w, h, f, 1)
    win = window(w, h, 10, 4)
    if fade:
        img = Img(w, h)
        img.over(AFTER, E, 1.0, win)
        emb = Field(w, h)
        for _ in range(14):
            x = rng.uniform(0.12, 0.88) * w
            dot(emb, x, h / 2 + rng.uniform(-0.3, 0.3) * h * math.sin(math.pi * x / w), rng.uniform(1.6, 2.6),
                rng.uniform(0.35, 0.6), 1)
        img.over(AFTER, emb, 1.0, win)
        return img
    main = walk(rng, (0.03 * w, h / 2), (0.97 * w, h / 2), 5.0, (0.7, 2.0), 58, 0.3, 2, 0.0, 0.0)
    main = [(x, h / 2 + (y - h / 2) * (0.35 + 0.65 * math.sin(math.pi * x / w))) for x, y in main]
    paths = [attrib(main, 0.7, 0.7, 0.9, 0.9, rng, 0.35, 0.08)]
    add_branches(rng, paths, main, 0.9, 0.8, 2, 9, spread=(25, 65), length=(0.012, 0.035), bounds=(0, w, 3, h - 3))
    sp = spark_points(rng, main[len(main) // 6:-len(main) // 6], 5, (h * 0.12, h * 0.3), (0.8, 1.2))
    return render_bolt(w, h, paths, sp, glow=(2.0, 1.2, 0.5), halo=(3.0, 2.0, 0.12), extra=E.d, win=win)


def tex_obj_shard(seed):
    """Flying electro shard: u = flight direction (tip at u~0.93), a faceted diamond with a white
    leading edge and lavender -> violet body, and a fading motion streak toward u=0."""
    w, h = 64, 64
    tip, back, mid, hw = 0.93 * w, 0.42 * w, 0.66 * w, 0.15 * h
    cy = h / 2

    def f(x, y):
        x += 0.5
        y += 0.5
        d = abs(y - cy)
        body = edge = 0.0
        if back <= x <= tip:
            half = hw * ((x - back) / (mid - back) if x < mid else (tip - x) / (tip - mid))
            facet = 0.55 + 0.35 * (x - back) / (tip - back) - 0.25 * d / (hw + 1e-3)
            body = smooth(-0.8, 0.8, half - d) * facet
            edge = 0.9 * _obj_g(((d - half) / 0.9) ** 2) * (1.0 if x > mid else 0.6)
        glow = 0.35 * _obj_g(((x - mid) / 16.0) ** 2 + (d / 7.0) ** 2)
        streak = 0.0
        if x < mid:
            t = (x - 0.04 * w) / (mid - 0.04 * w)
            if t > 0:
                streak = 0.5 * t ** 1.6 * _obj_g((d / (1.0 + 2.5 * (1 - t))) ** 2)
        return max(body, edge) + glow + streak
    img = Img(w, h)
    img.over(ELECTRO, sample_fn(w, h, f, 1), 1.0, window(w, h, 3, 3))
    return img


# --------------------------------------------------------------------------- catalogue


def entry(name, w, h, kind, along, core, use, fn, notes=""):
    return dict(name=name, texture=NS + name, w=w, h=h, kind=kind, along=along, core=core, use=use, notes=notes, fn=fn)


def catalogue():
    C = []
    for v, s in zip("abcd", (11, 23, 37, 51)):
        C.append(entry(f"bolt_{v}", 512, 128, "strip", "u", "v=0.5, zig-zag core r~1.5px within v=0.33..0.67",
                       "hot lightning bolt (floor bolts, horizontal strikes, tall walls, long arcs)", lambda s=s: tex_bolt(s),
                       "forks reach v=0.1..0.9; ends fade over 5% of u; tight halo (safe on top of decals)"))
    # S3: bolt_after_a, bolt_fade_a / _c, blade_b / _c, rift_b, charge_spark, the rig_katana / rig_palm / rig_crown cards
    # and the illusion swing / wave-fade bands lost their last model and are not painted. blade_trail_a / _b and
    # glow_strip came back with the 만겁 katana (build_raiden_judgment_rig.mjs, 10-22a).
    for v, s in (("c", 37),):
        C.append(entry(f"bolt_after_{v}", 512, 128, "strip", "u", "same path as bolt_" + v,
                       "afterglow of bolt_" + v, lambda s=s: tex_bolt(s, "after")))
    for v, s in zip("a", (61,)):
        C.append(entry(f"blade_{v}", 512, 64, "strip", "u", "v=0.5+-0.08, r~1.3px",
                       "blade-hugging bolt along a weapon edge (u = hilt -> tip); long low lightning walls",
                       lambda s=s: tex_blade(s), "tight glow; short frequent forks"))
    for v, s in zip("abc", (73, 77, 79)):
        C.append(entry(f"rim_crackle_{v}", 512, 64, "strip", "u", "v=0.5+-0.10, tight glow, no halo",
                       "crackle laid on top of another translucent card (decal edges)", lambda s=s: tex_rim_crackle(s),
                       "alpha >= 0.1 only near the core, so it does not hide what lies under it"))
    for v, s in zip("ab", (81, 83)):
        C.append(entry(f"blade_trail_{v}", 512, 64, "strip", "u", "u=0 newest/brightest, fades to u=1",
                       "slash/afterimage trail behind a moving blade", lambda s=s: tex_blade_trail(s), "afterglow palette"))
    for v, s in zip("abc", (101, 107, 113)):
        C.append(entry(f"vbolt_{v}", 128, 512, "column", "v", "u=0.5, top v=0 -> small impact bloom v~0.96",
                       "vertical strike bolt (2-4 crossed vertical cards ~2.5 wide)", lambda s=s: tex_vbolt(s),
                       "narrow halo, sides fade over 30% of w"))
    C.append(entry("vbolt_after_c", 128, 512, "column", "v", "same path as vbolt_c", "afterglow of vbolt_c",
                   lambda: tex_vbolt(113, "after")))
    for v, s in zip("ab", (131, 137)):
        C.append(entry(f"pillar_{v}", 128, 512, "column", "v", "u=0.5 column glow, 3 winding bolts",
                       "stake/pillar current, eye beams", lambda s=s: tex_pillar(s), "soft top and bottom; no impact bloom"))
    for v, s in zip("ab", (151, 157)):
        C.append(entry(f"arc_{v}", 256, 128, "strip", "u", "arch from (0.06,0.86) via apex v~0.2 to (0.94,0.86)",
                       "palm/finger arcs, small jumping arcs", lambda s=s: tex_arc(s)))
    for v, s in zip("ab", (171, 173)):
        C.append(entry(f"chakra_{v}", 256, 256, "radial", "radial", "ring radius 0.40*w",
                       "circular chakra / halo ring of electricity", lambda s=s: tex_chakra(s)))
    C.append(entry("orb_core", 128, 128, "radial", "radial", "centre", "eye/orb core glow", tex_orb_core))
    C.append(entry("crescent_a", CRESCENT_W, CRESCENT_H, "crescent", "arc", "outer edge r=0.94*h around pivot (0.5,1.0), +-72deg",
                   "clean sword-light crescent / slash wave", lambda: tex_crescent(191, False)))
    C.append(entry("crescent_b", CRESCENT_W, CRESCENT_H, "crescent", "arc", "as crescent_a + bolt along the edge",
                   "lightning crescent slash", lambda: tex_crescent(193, True)))
    C.append(entry("slash_wave", 512, 128, "strip", "u", "edge at v~0.30, tail toward v~0.9",
                   "straight slash wave / sword beam (travels toward -v)", lambda: tex_slash_wave(197)))
    for v, s in zip("a", (211,)):
        C.append(entry(f"rift_{v}", 512, 64, "strip", "u", "v=0.5 thin white tear in a dark void band",
                       "rift / cut ribbon, teleport tears", lambda s=s: tex_rift(s)))
    C.append(entry("shockwave", 256, 256, "radial", "radial", "leading edge r=0.46*w, tail inward to ~0.28*w",
                   "expanding ring / shockwave (scale the card)", lambda: tex_shockwave(229)))
    for v, s in zip("ab", (233, 239)):
        C.append(entry(f"crackle_{v}", 512, 64, "strip", "u", "band v=0.22..0.86, floor glow at v=0.93",
                       "vertical lightning wall band, chainable along u", lambda s=s: tex_crackle(s)))
    C.append(entry("flash", 256, 256, "radial", "radial", "centre, visible radius ~0.3*w", "compact strike / impact flash",
                   lambda: tex_flash(241)))
    C.append(entry("impact_sparks", 256, 256, "radial", "radial", "centre", "shield / hit impact sparks",
                   lambda: tex_impact_sparks(251)))
    C.append(entry("scorch", 256, 256, "radial", "radial", "centre, burn radius ~0.44*w", "floor scorch decal",
                   lambda: tex_scorch(257), "dark (not glowing) except the ember ring"))
    C.append(entry("scorch_strip", 256, 64, "strip", "u", "v=0.5", "burn streak under floor bolts",
                   lambda: tex_scorch_strip(263)))
    C.append(entry("spark", 32, 32, "radial", "radial", "centre", "spark dot", tex_spark))
    C.append(entry("glint", 64, 64, "radial", "radial", "centre", "four-point star glint (armour shards)", tex_glint))
    C.append(entry("glow_soft", 64, 64, "radial", "radial", "centre", "plain soft glow", tex_glow_soft))
    C.append(entry("glow_strip", 256, 32, "strip", "u", "v=0.5", "plain soft beam glow", tex_glow_strip))
    C += kit_entries()
    C.append(entry("rig_shard", 48, 128, "column", "v", "lens tips at v=0.03/0.97, widest at v~0.39, ridge u~0.5",
                   "translucent crystal splinter (death_shard_*)", lambda: tex_rig_shard(331)))
    # object / blink / orb sprites (build_raiden_object_vfx.py, build_raiden_movement.py, build_raiden_orb.py)
    C.append(entry("obj_wave_band", 512, 64, "strip", "u", "v=0.5 white core, lens envelope sin(pi*u)",
                   "flying sword-wave front band (chord cards along the crescent edge)",
                   lambda: tex_obj_wave_band(409), "layered glow, crackle along the core, cyan sparks"))
    C.append(entry("obj_shard", 64, 64, "strip", "u", "tip at u~0.93, body u 0.42..0.93, streak toward u=0",
                   "flying electro shard (break bursts)", lambda: tex_obj_shard(433)))
    return C


def names():
    return [c["name"] for c in catalogue()]


def write_catalogue_json(path=CATALOGUE_JSON):
    data = {"namespace": NS, "texture_dir": TEX_SUBDIR,
            "conventions": {
                "strip": "u along the bolt (u=0 start, u=1 end, soft-faded ends), v=0.5 centre row",
                "column": "v along height: v=0 top (sky), v=1 bottom (impact), u=0.5 centre",
                "radial": "centred at (0.5,0.5)",
                "crescent": "pivot at bottom-centre (0.5,1.0); bright outer edge radius 0.94*h; +-72 deg",
                "decal": "top view: u = local +x, v = local +z (forward)",
                "quarter": "circle centre at texture corner (0,0); mirror uv for other quadrants"},
            "model_rules": "flat cards (from==to on one axis), faces on both sides, shade false, uv 0..16 "
                           "(per-face rotation 0/90/180/270, u1>u2 mirrors), single-axis element rotation "
                           "0/+-22.5/+-45, from/to within -16..32, layers >= 0.02 block apart",
            "vanilla_rules": [
                "fragments with alpha < 0.1 are discarded",
                "translucent item quads are sorted back-to-front by centroid distance and WRITE DEPTH: a card drawn "
                "earlier hides translucent cards behind it wherever its alpha >= 0.1; keep halos of overlay cards tight, "
                "prefer centred cards under centred overlays, split tall vertical cards so the low part sorts after the floor",
                "magnified sampling is nearest-neighbour: >= ~32 texels per block for things seen up close",
                "vertical faces may receive entity diffuse light 0.5..0.74 (up faces 1.0)"],
            "textures": [{k: v for k, v in c.items() if k != "fn"} for c in catalogue()],
            "kit_decals": KIT_DECALS, "kit_quarter_extent": KIT_QEXT}
    path.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")


def build_fx_textures(resourcepack, only=None, quiet=False):
    rp = Path(resourcepack)
    out = rp / TEX_SUBDIR
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    cat = catalogue()
    area = 0
    for c in cat:
        if only and c["name"] not in only:
            continue
        t = time.time()
        img = c["fn"]()
        assert (img.w, img.h) == (c["w"], c["h"]), (c["name"], img.w, img.h)
        assert img.w % 16 == 0 and img.h % 16 == 0 and max(img.w, img.h) <= 1024, c["name"]
        (out / (c["name"] + ".png")).write_bytes(img.png())
        area += img.w * img.h
        if not quiet and time.time() - t > 1.5:
            print(f"  {c['name']}: {time.time() - t:.1f}s")
    if not only:
        # this generator owns rlk:raiden/fxg/*: drop sprites it no longer paints
        current = {c["name"] for c in cat}
        for old in out.glob("*.png"):
            if old.stem not in current:
                old.unlink()
    atlaspath = rp / "assets/minecraft/atlases/items.json"
    atlas = json.loads(atlaspath.read_text(encoding="utf-8")) if atlaspath.exists() else {"sources": []}
    if not only:
        wanted = {c["texture"] for c in cat}
        atlas["sources"] = [s for s in atlas["sources"]
                            if not str(s.get("resource", "")).startswith(NS) or s["resource"] in wanted]
    known = {s.get("sprite", s.get("resource")) for s in atlas["sources"]}
    for c in cat:
        if c["texture"] not in known:
            atlas["sources"].append({"type": "minecraft:single", "resource": c["texture"]})
    atlaspath.parent.mkdir(parents=True, exist_ok=True)
    atlaspath.write_text(json.dumps(atlas, indent=2) + "\n", encoding="utf-8")
    if not quiet:
        print(f"Painted {len(cat) if not only else len(only)} lightning VFX textures "
              f"({area / 1e6:.2f} Mpx) in {time.time() - t0:.1f}s; atlas has {len(atlas['sources'])} sources.")
    return cat


def resolve_only(spec, cat=None):
    """--only value -> set of sprite names. Comma list of names or fnmatch globs ("ringq_*,tele_1?");
    every item must match at least one catalogue sprite (a typo used to paint nothing silently)."""
    import fnmatch
    all_names = [c["name"] for c in (cat or catalogue())]
    out, missing = set(), []
    for pat in (p.strip() for p in spec.split(",")):
        if not pat:
            continue
        hit = [n for n in all_names if fnmatch.fnmatchcase(n, pat)]
        if not hit:
            missing.append(pat)
        out.update(hit)
    if missing:
        raise SystemExit(f"--only: no sprite matches {missing}; names: python3 {Path(__file__).name} --list")
    return out


def px_ledger(cat=None, only=None):
    """Print every sprite (name, size, px) and the per-family totals (family = name up to the first '_')."""
    cat = cat or catalogue()
    fam, total = {}, 0
    for c in cat:
        if only and c["name"] not in only:
            continue
        px = c["w"] * c["h"]
        total += px
        f = c["name"].split("_")[0]
        n, s = fam.get(f, (0, 0))
        fam[f] = (n + 1, s + px)
        print(f"  {c['name']:<24} {c['w']:>4} x {c['h']:<4} {px / 1e6:7.3f} M px")
    print("families (count, M px):")
    for f, (n, s) in sorted(fam.items(), key=lambda kv: -kv[1][1]):
        print(f"  {f:<16} {n:>3}  {s / 1e6:6.3f}")
    print(f"total {sum(n for n, _ in fam.values())} sprites, {total / 1e6:.3f} M px (rlk:raiden/fxg)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--resourcepack", type=Path, default=Path(__file__).resolve().parents[2] / "resourcepack")
    parser.add_argument("--only", help="comma list of texture names or globs, e.g. ringq_*,tele_3 (development: "
                                       "repaints just those sprites, keeps every other sprite and atlas entry)")
    parser.add_argument("--catalogue", action="store_true", help="only rewrite tools/raiden_fx_textures.json")
    parser.add_argument("--list", action="store_true", help="print the sprite px ledger (with --only: just those) and exit")
    a = parser.parse_args()
    only = resolve_only(a.only) if a.only else None
    if a.list:
        px_ledger(only=only)
        raise SystemExit(0)
    write_catalogue_json()
    if not a.catalogue:
        build_fx_textures(a.resourcepack, only)
