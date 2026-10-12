"""Painted lightning VFX textures for Narukami (sprites rlk:raiden/fxg/<name>).

Pure standard library (math, random, struct, zlib) and deterministic: every texture
is painted from fixed seeds, so the resource pack can be regenerated anywhere
(~30 s in CPython). `build_fx_textures(rp)` writes
<rp>/assets/rlk/textures/raiden/fxg/<name>.png, appends each sprite to
assets/minecraft/atlases/items.json and prunes fxg sprites it no longer paints
(other atlas entries are never touched). The machine-readable catalogue is
tools/raiden_fx_textures.json (name, texture, w, h, kind, along, core, use, notes,
plus the hazard decal rectangles); JS generators should read that file.
Run alone: python tools/build_raiden_fx_textures.py --resourcepack <rp> [--only a,b]

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
  decal    top-view floor decal; u = world +x (local left/right), v = world +z
           (local forward). Hazard decals are symmetry pieces, see DECALS / DECAL_SYM.
  quarter  ring quadrant: circle centre at the texture's top-left corner (u=0,v=0);
           mirror it (uv [16,0,0,16] etc.) for the other quadrants.

CATALOGUE (all sizes are multiples of 16 so the atlas keeps its mipmap levels;
total ~5.4 Mpx)
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
  orb_rim               256x256 radial  eye/orb electric rim: smooth bright rim at
                                         0.37*w + crackles + soft inner gradient.
  orb_core              128x128 radial  soft radial glow, white centre -> violet.
  crescent_a            512x256 crescent clean blade-light crescent (bright edge,
                                         lavender->violet gradient tail inward).
  crescent_b            512x256 crescent crescent with a jagged bolt along its edge.
  slash_wave            512x128 strip   straight slash wave: bright leading edge at
                                         v~0.3 (moving toward -v), lens-shaped gradient
                                         tail toward v~0.9, tapered ends.
  rift_a/_b             512x64  strip   rift/cut ribbon: thin white jagged tear along
                                         u inside a dark void band with violet lips.
  shockwave             512x512 radial  annulus: bright leading edge at r=0.46*w,
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
  tele_<s>, charged_<s> decal           hazard telegraph / charged decal pieces of hazard
  (tele_9_<0|25|50>)                     shape s (fan rays per slant); see DECALS.
  ringq_<k>             quarter         expanding-ring band for ring radius RING_R[k].
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
  obj_frag_a/_b/_fade   128x32  strip   blink silhouette strip: glowing top edge (v=0.2), dim bottom
                                         edge (v=0.8), ragged ends (build_raiden_movement.py).
  obj_shard             64x64   strip   flying shard: tip at u~0.93, motion streak toward u=0.
  obj_gauge_on/_off     64x64   quarter orb gauge quadrant arc r=0.74*w, 9..81 deg (build_raiden_orb.py).
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

# --------------------------------------------------------------------------- tables
# Hazard shapes (local frame: +z forward from the origin, x sideways). Must equal the
# hit volumes in build_raiden_hazards.py; build_raiden_hazard_vfx.py asserts this.
HAZARD_SHAPES = {
    1: dict(kind="sector", r=6, half=60),
    2: dict(kind="rect", length=12, width=2.2),
    3: dict(kind="disk", r=3),
    4: dict(kind="sector", r=12, half=70),
    5: dict(kind="rect", length=20, width=3.6),
    6: dict(kind="disk", r=5),
    7: dict(kind="rect", length=8, width=8),
    8: dict(kind="disk", r=6),
    9: dict(kind="fan", length=18, width=0.9, angles=(-40, -20, 0, 20, 40)),
    10: dict(kind="rect", length=18, width=7),
    11: dict(kind="annulus", r0=1.3, r1=2.7),
    12: dict(kind="disk", r=12),
    13: dict(kind="rect", length=22, width=2.4),
}
# Hazard decals are painted only once per symmetry piece and mirrored by the cards, which
# doubles the texel density for the same memory (all >= 32 texels/block):
#   half  rects/sectors: texture covers x >= 0, the x < 0 half is the u-mirrored card;
#   quad  disks/annulus: texture covers x >= 0, z >= 0, mirrored into all four quadrants;
#   ray   the five fan rays: one card per ray turned by the nearest allowed 22.5-deg step,
#         the remaining 0 / 2.5 / 5 deg slant is painted into the texture (mirror u for -).
DECAL_SYM = {1: "half", 2: "half", 3: "quad", 4: "half", 5: "half", 6: "quad", 7: "half", 8: "quad",
             9: "ray", 10: "half", 11: "quad", 12: "quad", 13: "half"}
DECAL_TPB = {1: 36, 2: 36, 3: 40, 4: 32, 5: 34, 6: 38, 7: 36, 8: 36, 9: 32, 10: 32, 11: 40, 12: 32, 13: 32}
FAN_SLANTS = (0.0, 2.5, 5.0)
MARGIN = 0.9


def decal_rect(shape, geom=None):
    """Painted world rectangle (x0, x1, z0, z1) of a decal piece (see DECAL_SYM)."""
    g = geom or HAZARD_SHAPES[shape]
    m = MARGIN
    k = g["kind"]
    if k == "sector":
        return (0.0, g["r"] * math.sin(math.radians(g["half"])) + m, -m, g["r"] + m)
    if k == "rect":
        return (0.0, g["width"] / 2 + m, -m, g["length"] + m)
    if k == "disk":
        return (0.0, g["r"] + m, 0.0, g["r"] + m)
    if k == "annulus":
        return (0.0, g["r1"] + m, 0.0, g["r1"] + m)
    if k == "fan":            # one ray, slanted toward +x by angles[0] degrees
        a = math.radians(g["angles"][0])
        hw = g["width"] / 2
        return (-hw - m, g["length"] * math.sin(a) + hw + m, -m, g["length"] + m)
    raise ValueError(k)


DECALS = {}
for _s in HAZARD_SHAPES:
    if DECAL_SYM[_s] == "ray":
        pieces = [(f"_{int(sl * 10)}", dict(HAZARD_SHAPES[_s], angles=(sl,))) for sl in FAN_SLANTS]
    else:
        pieces = [("", None)]
    for _suffix, _geom in pieces:
        _x0, _x1, _z0, _z1 = decal_rect(_s, _geom)
        _w = int(math.ceil((_x1 - _x0) * DECAL_TPB[_s] / 16.0)) * 16
        _h = int(math.ceil((_z1 - _z0) * DECAL_TPB[_s] / 16.0)) * 16
        for _kind in ("tele", "charged"):
            DECALS[f"{_kind}_{_s}{_suffix}"] = dict(shape=_s, sym=DECAL_SYM[_s], w=_w, h=_h, x0=_x0, x1=_x1, z0=_z0, z1=_z1,
                                                     geom=_geom)

# Expanding ring (hazard shape 11): band radius r +- 0.7, r = 2 .. 18. Quarter textures
# are painted for these centre radii; a frame uses the nearest one scaled by r/RING_R[k].
RING_R = [2.3, 2.9, 3.6, 4.5, 5.6, 7.0, 8.8, 11.0, 13.8, 17.2]
RING_HALF = 0.7
RING_PAD = 0.9


def ring_extent(k):
    """World half-size covered by quarter texture k (circle centre at the corner)."""
    return RING_R[k] + RING_HALF + RING_PAD


def ring_px(k):
    return max(64, int(math.ceil(ring_extent(k) * 24 / 16.0)) * 16)

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


def tex_orb_rim(seed):
    w = h = 256
    rng = random.Random(seed)
    R = 0.37 * w
    nz = WaveNoise(seed, 5, 2.0)
    G = GAUSS

    def f(r, th):
        d = (r - R) / 3.2
        q = d * d
        rim = 0.95 * G[int(q * 256)] if q < 9 else 0.0
        d2 = (r - R) / 11.0
        q2 = d2 * d2
        glow = 0.45 * G[int(q2 * 256)] if q2 < 9 else 0.0
        inner = 0.32 * smooth(R * 0.2, R, r) * (1.0 if r < R else 0.0) * (0.75 + 0.25 * nz(th * 3, r * 0.05))
        return rim + glow + inner
    base = radial_field(w, h, f)
    paths = []
    for _ in range(9):
        a = rng.uniform(0, 6.28)
        da = rng.uniform(0.18, 0.4)
        out = rng.choice((1, 1, -1))
        p0 = (w / 2 + R * math.cos(a), h / 2 + R * math.sin(a))
        p2 = (w / 2 + R * math.cos(a + da), h / 2 + R * math.sin(a + da))
        mid = a + da / 2
        p1 = (w / 2 + (R + out * rng.uniform(10, 24)) * math.cos(mid), h / 2 + (R + out * rng.uniform(10, 24)) * math.sin(mid))
        paths.append(attrib(jag_curve(rng, bezier(p0, p1, p2, 6), 2), 1.2, 0.8, 0.9, 0.6, rng, 0.3))
    return render_bolt(w, h, paths, (), glow=(2.3, 2.0, 0.55), halo=(5.0, 6.0, 0.28), extra=base)


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


def tex_crescent(seed, bolt):
    w, h = 512, 256
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
        q = (d / (1.6 + 2.2 * env)) ** 2
        edge = (1.05 * G[int(q * 256)] if q < 9 else 0.0) * (0.35 + 0.65 * env)
        q = (d / (6 + 8 * env)) ** 2
        glow = 0.4 * env * G[int(q * 256)] if q < 9 else 0.0
        body = 0.0
        if d < 0:
            t = -d / thick
            if t < 1.6:
                streak = 0.7 + 0.3 * nz(phi * 22, r * 0.06)
                body = 0.62 * env * math.exp(-2.2 * t) * streak
        return edge + glow + body
    E = sample_fn(w, h, f, 1)
    if not bolt:
        img = Img(w, h)
        img.over(ELECTRO, E, 1.0, window(w, h, 6, 6))
        return img
    base = [(cx + R * 0.985 * math.sin(p), cy - R * 0.985 * math.cos(p)) for p in [-phimax * 0.92 + 2 * phimax * 0.92 * i / 24 for i in range(25)]]
    main = jag_curve(rng, base, 3, (0.35, 0.3, 0.22))
    paths = [attrib(main, 1.8, 1.8, 1.0, 1.0, rng, 0.3, 0.06)]
    add_branches(rng, paths, main, 1.6, 0.85, 2, 9, length=(0.03, 0.08), bounds=(4, w - 4, 4, h - 4))
    sp = spark_points(rng, main, 4, (8, 24))
    return render_bolt(w, h, paths, sp, glow=(2.3, 2.5, 0.6), halo=(5.5, 8.0, 0.3), extra=E.d)


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
    w = h = 512
    R = 0.46 * w
    nz = WaveNoise(seed, 6, 1.0)
    G = GAUSS

    def f(x, y):
        dx, dy = x - w / 2, y - h / 2
        r = math.hypot(dx, dy)
        d = r - R
        q = (d / 2.6) ** 2
        edge = 1.0 * G[int(q * 256)] if q < 9 else 0.0
        q = (d / 9.0) ** 2
        glow = 0.42 * G[int(q * 256)] if q < 9 else 0.0
        body = 0.0
        if d < 0:
            t = -d / (0.18 * w)
            if t < 2.0:
                th = math.atan2(dy, dx)
                body = 0.55 * math.exp(-2.0 * t) * (0.65 + 0.35 * nz(th * 30, r * 0.05))
        return edge + glow + body
    img = Img(w, h)
    img.over(ELECTRO, sample_fn(w, h, f, 2), 1.0, window(w, h, 8, 8))
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

# --------------------------------------------------------------------------- hazard decals


def sd_box(x, z, hx, hz):
    qx, qz = abs(x) - hx, abs(z) - hz
    ox, oz = max(qx, 0.0), max(qz, 0.0)
    return math.hypot(ox, oz) + min(max(qx, qz), 0.0)


def sd_seg(x, z, ax, az, bx, bz):
    dx, dz = bx - ax, bz - az
    L2 = dx * dx + dz * dz
    t = ((x - ax) * dx + (z - az) * dz) / L2 if L2 > 0 else 0.0
    t = 0.0 if t < 0 else (1.0 if t > 1 else t)
    return math.hypot(x - ax - t * dx, z - az - t * dz)


def shape_sdf(g):
    k = g["kind"]
    if k == "disk":
        r = g["r"]
        return lambda x, z: math.hypot(x, z) - r
    if k == "annulus":
        rm, hw = (g["r0"] + g["r1"]) / 2, (g["r1"] - g["r0"]) / 2
        return lambda x, z: abs(math.hypot(x, z) - rm) - hw
    if k == "rect":
        L, hw = g["length"], g["width"] / 2
        return lambda x, z: sd_box(x, z - L / 2, hw, L / 2)
    if k == "sector":
        r, a = g["r"], math.radians(g["half"])
        cs, cc = math.sin(a), math.cos(a)

        def f(x, z):
            px = abs(x)
            l = math.hypot(px, z) - r
            t = px * cs + z * cc
            t = 0.0 if t < 0 else (r if t > r else t)
            m = math.hypot(px - cs * t, z - cc * t)
            sgn = 1.0 if cc * px - cs * z > 0 else -1.0
            return max(l, m * sgn)
        return f
    if k == "fan":
        L, hw = g["length"], g["width"] / 2
        rots = [(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in g["angles"]]

        def f(x, z):
            best = 1e9
            for c, s in rots:
                # rotate (x, z) by -angle: ray direction (sin a, cos a)
                lx = x * c - z * s
                lz = x * s + z * c
                v = sd_box(lx, lz - L / 2, hw, L / 2)
                if v < best:
                    best = v
            return best
        return f
    raise ValueError(k)


def chevron(cx, cz, ux, uz, half, depth):
    """Chevron polyline pointing along (ux, uz) with its tip at (cx, cz)."""
    px, pz = uz, -ux
    return [(cx - ux * depth + px * half, cz - uz * depth + pz * half), (cx, cz), (cx - ux * depth - px * half, cz - uz * depth - pz * half)]


def shape_marks(g):
    """(centre polylines, chevron polylines, rings[(r, weight)]) in world units."""
    k = g["kind"]
    lines, chev, rings = [], [], []
    if k == "rect":
        L, w = g["length"], g["width"]
        lines.append([(0, 0.45), (0, L - 0.45)])
        hw = min(0.62, w * 0.28)
        for z in range(2, int(L), 3):
            chev.append(chevron(0, z, 0, 1, hw, min(0.42, hw * 0.75)))
    elif k == "sector":
        r, a = g["r"], g["half"]
        lines.append([(0, 0.5), (0, r - 0.35)])
        for ang in (-a * 0.55, a * 0.55):
            s, c = math.sin(math.radians(ang)), math.cos(math.radians(ang))
            chev.append([(s * r * 0.22, c * r * 0.22), (s * (r - 0.6), c * (r - 0.6))])
        for f in (0.42, 0.72):
            hw = 0.5 if r < 8 else 0.8
            chev.append(chevron(0, r * f, 0, 1, hw, hw * 0.7))
        rings.append((r * 0.57, 0.45, -a, a))
    elif k == "fan":
        L = g["length"]
        for ang in g["angles"]:
            s, c = math.sin(math.radians(ang)), math.cos(math.radians(ang))
            lines.append([(s * 0.6, c * 0.6), (s * (L - 0.4), c * (L - 0.4))])
            for z in (5, 11, 16):
                chev.append(chevron(s * z, c * z, s, c, 0.3, 0.26))
    elif k == "disk":
        r = g["r"]
        rings.append((r * 0.5, 0.55, -180, 180))
        tick = min(1.4, r * 0.24)
        for ang in (0, 90, 180, 270):
            s, c = math.sin(math.radians(ang)), math.cos(math.radians(ang))
            lines.append([(s * (r - tick), c * (r - tick)), (s * (r - 0.12), c * (r - 0.12))])
        cr = min(0.6, r * 0.12)
        lines.append([(-cr, 0), (cr, 0)])
        lines.append([(0, -cr), (0, cr)])
    elif k == "annulus":
        rings.append(((g["r0"] + g["r1"]) / 2, 0.6, -180, 180))
    return lines, chev, rings


def marks_distance(lines, chev, rings):
    segs = {}

    def prep(polys):
        key = id(polys)
        if key not in segs:
            out = []
            for poly in polys:
                for (ax, az), (bx, bz) in zip(poly, poly[1:]):
                    out.append((min(ax, bx) - 4, max(ax, bx) + 4, min(az, bz) - 4, max(az, bz) + 4, ax, az, bx, bz))
            segs[key] = out
        return segs[key]

    def dl(x, z, polys):
        best = 4.0
        for xa, xb, za, zb, ax, az, bx, bz in prep(polys):
            if x < xa or x > xb or z < za or z > zb:
                continue
            v = sd_seg(x, z, ax, az, bx, bz)
            if v < best:
                best = v
        return best

    def dr(x, z):
        best, wbest = 1e9, 0.0
        for r, wgt, a0, a1 in rings:
            ang = math.degrees(math.atan2(x, z))
            if a0 <= ang <= a1:
                v = abs(math.hypot(x, z) - r)
            else:
                continue
            if v < best:
                best, wbest = v, wgt
        return best, wbest
    return dl, dr


def shape_outline(g):
    """Boundary polylines (world units) used for the charged crackle."""
    k = g["kind"]
    if k == "disk":
        return [circle_pts(0, 0, g["r"], max(24, int(g["r"] * 10)))]
    if k == "annulus":
        return [circle_pts(0, 0, g["r0"], 20), circle_pts(0, 0, g["r1"], 32)]
    if k == "rect":
        L, hw = g["length"], g["width"] / 2
        return [[(-hw, 0), (-hw, L), (hw, L), (hw, 0), (-hw, 0)]]
    if k == "sector":
        r, a = g["r"], math.radians(g["half"])
        arc = [(r * math.sin(-a + 2 * a * i / 24), r * math.cos(-a + 2 * a * i / 24)) for i in range(25)]
        return [[(0, 0)] + arc + [(0, 0)]]
    if k == "fan":
        L, hw = g["length"], g["width"] / 2
        out = []
        for ang in g["angles"]:
            c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            for side in (-hw, hw):
                out.append([(s_ * z + c * side, c * z - s_ * side) for z in (2.0, L)])
        return out
    return []


def shape_veins(g, rng):
    """Faint interior lightning veins: list of (start, end, band) in world units."""
    k = g["kind"]
    out = []
    if k == "rect":
        L, hw = g["length"], g["width"] / 2
        for i in range(2 if hw < 1.5 else 3):
            x = (i - (1 if hw >= 1.5 else 0.5)) * hw * 0.55
            out.append(((x, 0.4), (x + rng.uniform(-0.2, 0.2) * hw, L - 0.4), hw * 0.35))
    elif k == "sector":
        r, a = g["r"], g["half"]
        for i in range(4):
            ang = math.radians(-a * 0.8 + 1.6 * a * (i + rng.uniform(0.2, 0.8)) / 4)
            out.append(((0.0, 0.3), (r * 0.93 * math.sin(ang), r * 0.93 * math.cos(ang)), r * 0.07))
    elif k == "disk":
        r = g["r"]
        for i in range(7):
            ang = 2 * math.pi * (i + rng.uniform(0.1, 0.9)) / 7
            r0 = r * rng.uniform(0.08, 0.2)
            out.append(((r0 * math.sin(ang), r0 * math.cos(ang)), (r * 0.92 * math.sin(ang + 0.15), r * 0.92 * math.cos(ang + 0.15)), r * 0.07))
    elif k == "fan":
        L = g["length"]
        for ang in g["angles"]:
            c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            out.append(((s_ * 0.8, c * 0.8), (s_ * (L - 0.5), c * (L - 0.5)), 0.2))
    elif k == "annulus":
        rm = (g["r0"] + g["r1"]) / 2
        for i in range(4):
            a0 = 2 * math.pi * i / 4 + rng.uniform(0, 0.5)
            out.append(((rm * math.sin(a0), rm * math.cos(a0)), (rm * math.sin(a0 + 1.4), rm * math.cos(a0 + 1.4)), 0.25))
    return out


def table(fn, lo, hi, n=2048):
    """Tabulate fn over [lo, hi] -> (values, lo, scale) for fast per-pixel lookups."""
    step = (hi - lo) / (n - 1)
    return [fn(lo + i * step) for i in range(n)], lo, (n - 1) / (hi - lo)


def gauss(d, sig):
    q = (d / sig) ** 2
    return math.exp(-q) if q < 30 else 0.0


def tex_decal(name):
    """Hazard telegraph decal. Deliberately LOW-FREQUENCY: every feature is at least ~2 texels
    wide so nearest-neighbour magnification at the player's feet stays smooth; the crisp
    electric detail of charge/strike frames comes from separate high-resolution bolt cards."""
    spec = DECALS[name]
    g = spec["geom"] or HAZARD_SHAPES[spec["shape"]]
    charged = name.startswith("charged")
    w, h = spec["w"], spec["h"]
    x0, x1, z0, z1 = spec["x0"], spec["x1"], spec["z0"], spec["z1"]
    sx, sz = (x1 - x0) / w, (z1 - z0) / h
    ppb = 1.0 / sx            # texels per block
    sdf = shape_sdf(g)
    lines, chev, rings = shape_marks(g)
    dl, dr = marks_distance(lines, chev, rings)
    vn = ValueNoise(spec["shape"] * 13 + 5)
    rng = random.Random(spec["shape"] * 31 + len(name) + (7 if charged else 0))

    def world(i, j):
        return x0 + i * sx, z0 + j * sz

    def pix(x, z):
        return (x - x0) / sx, (z - z0) / sz
    # faint interior veins (soft, >= 3 texels wide)
    veins = []
    for (ax, az), (bx, bz), band in shape_veins(g, rng):
        pts = walk(rng, pix(ax, az), pix(bx, bz), max(2.0, band * ppb), (0.5, 1.4), 55, 0.3, 1, 0.0, 0.0)
        veins.append(attrib(pts, 1.25, 1.0, 0.75, 0.45, rng, 0.45, 0.1))
        add_branches(rng, veins, pts, 1.15, 0.65, 1, 2, length=(0.06, 0.16), bounds=(2, w - 2, 2, h - 2))
    VE = render_fields(w, h, veins, (2.0, 2.5), (5.0, 5.0))
    CLOUD = sample_fn(w, h, lambda i, j: vn.fbm(world(i, j)[0] / 1.7, world(i, j)[1] / 1.7, 3), 4).d
    S = sample_fn(w, h, lambda i, j: sdf(*world(i, j)), 2).d
    DL = sample_fn(w, h, lambda i, j: min(4.0, dl(*world(i, j), lines)), 2).d
    DC = sample_fn(w, h, lambda i, j: min(4.0, dl(*world(i, j), chev)), 2).d if chev else None
    DR = sample_fn(w, h, lambda i, j: min(4.0, dr(*world(i, j))[0]), 2).d if rings else None

    core = max(0.075, 2.3 / ppb)
    lcore = max(0.06, 1.9 / ppb)
    # fan rays overlap near the origin (where the boss stands): fade each ray's rim there
    APEX = (sample_fn(w, h, lambda i, j: smooth(0.3, 2.6, math.hypot(*world(i, j))), 4).d
            if g["kind"] == "fan" else None)
    if charged:
        U = table(lambda s: smooth(0.03, -0.16, s) * (0.30 + 0.16 * gauss(s, 1.2)), -8, 4)
        RC = table(lambda s: 1.12 * gauss(s, core) + 0.62 * gauss(s, 0.26), -8, 4)
        RO = table(lambda s: 0.40 * gauss(s, 0.6) if s > 0 else 0.55 * gauss(s, 1.1), -8, 4)
    else:
        U = table(lambda s: smooth(0.03, -0.16, s) * (0.27 + 0.17 * gauss(s, 0.9)), -8, 4)
        RC = table(lambda s: 1.0 * gauss(s, core) + 0.55 * gauss(s, 0.22), -8, 4)
        RO = table(lambda s: 0.28 * gauss(s, 0.45) if s > 0 else 0.36 * gauss(s, 0.75), -8, 4)
    CIN = table(lambda s: smooth(-0.05, -0.38, s), -8, 4)
    INS = table(lambda s: smooth(0.03, -0.14, s), -8, 4)
    LL = table(lambda d: 0.85 * gauss(d, lcore) + 0.32 * gauss(d, 0.2), 0, 4)
    LC = table(lambda d: 0.62 * gauss(d, lcore) + 0.26 * gauss(d, 0.22), 0, 4)
    LR = table(lambda d: 0.42 * gauss(d, lcore * 0.9) + 0.2 * gauss(d, 0.18), 0, 4)
    n1 = 2047
    Ut, ulo, uk = U
    RCt, _, _ = RC
    ROt, _, _ = RO
    CINt, _, _ = CIN
    INSt, _, _ = INS
    LLt, _, lk = LL
    LCt, LRt = LC[0], LR[0]
    kl = 1.25 if charged else 1.0
    km = 1.3 if charged else 1.0
    kv = 0.8 if charged else 0.5
    under, fil, rim, line, mark = [], [], [], [], []
    for idx in range(w * h):
        si = int((S[idx] - ulo) * uk)
        si = 0 if si < 0 else (n1 if si > n1 else si)
        cl = CLOUD[idx]
        ap = 1.0 if APEX is None else APEX[idx]
        under.append(Ut[si] * (0.85 + 0.3 * cl) * (0.4 + 0.6 * ap))
        fil.append(INSt[si] * VE[idx] * kv)
        rim.append((RCt[si] * (0.86 + 0.22 * cl) + ROt[si]) * ap)
        cin = CINt[si]
        di = int(DL[idx] * lk)
        line.append(LLt[di if di < n1 else n1] * cin * kl)
        m = 0.0
        if DC is not None:
            di = int(DC[idx] * lk)
            m = LCt[di if di < n1 else n1]
        if DR is not None:
            di = int(DR[idx] * lk)
            v = LRt[di if di < n1 else n1]
            if v > m:
                m = v
        mark.append(m * cin * km)
    wx, wy = window(w, h, 3, 3)
    if spec["sym"] in ("half", "quad"):      # mirror seams must stay unfaded
        wx = [1.0 if x < w / 2 else v for x, v in enumerate(wx)]
    if spec["sym"] == "quad":
        wy = [1.0 if y < h / 2 else v for y, v in enumerate(wy)]
    win = (wx, wy)
    img = Img(w, h)
    img.over(solid((40, 16, 84) if charged else (24, 8, 46)), under, 1.0, win)
    img.over(ELECTRO if charged else TELE, rim, 1.0, win)
    img.over(ELECTRO, fil, 1.0, win)
    img.over(ELECTRO if charged else LINE, mark, 1.0, win)
    img.over(ELECTRO if charged else LINE, line, 1.0, win)
    return img


def tex_ring_quarter(k):
    """Quarter of the expanding ring band for centre radius RING_R[k]; circle centre at (0, 0)."""
    n = ring_px(k)
    ext = ring_extent(k)
    r0 = RING_R[k]
    sc = ext / n
    nz = WaveNoise(500 + k, 6, 1.0)
    G = GAUSS
    lead = r0 + RING_HALF
    trail = r0 - RING_HALF
    edge = max(0.1, 3.0 * sc)        # >= 3 texels: smooth when the band passes under the player

    def gs(d, sig):
        q = (d / sig) ** 2
        return G[int(q * 256)] if q < 9 else 0.0

    def f(i, j):
        x, z = i * sc, j * sc
        r = math.hypot(x, z)
        th = math.atan2(z, x)
        e = 1.05 * gs(r - lead, edge) + 0.5 * gs(r - lead, 0.24) + (0.25 * gs(r - lead, 0.42) if r > lead else 0.0)
        if trail - 0.3 < r < lead:
            t = (lead - r) / (2 * RING_HALF)
            e += 0.58 * math.exp(-1.6 * t) * (0.9 + 0.1 * nz(th * r0 * 0.6, r * 0.5))
        e += 0.38 * gs(r - trail, edge * 0.8) + 0.16 * gs(r - trail, 0.18)
        return e
    E = sample_fn(n, n, f, 1)
    img = Img(n, n)
    wx = [smooth(0, 3, n - x - 0.5) for x in range(n)]
    img.over(ELECTRO, E, 1.0, (wx, wx))
    return img

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


OBJ_FRAG_BODY = ramp([(0.0, (40, 14, 84, 0)), (0.2, (44, 16, 92, 40)), (0.6, (62, 28, 128, 120)),
                      (1.0, (92, 52, 170, 150)), (2.5, (92, 52, 170, 150))])


def tex_obj_frag(seed, fade=False):
    """Blink silhouette strip (u across the body, v top -> bottom): translucent deep-violet body
    with a glowing top edge (white core) and a dimmer bottom edge, ragged dissolving ends, faint
    horizontal streaks and a short lightning seam; fade: afterglow colours, more dissolved."""
    w, h = 128, 32
    rng = random.Random(seed)
    vn = ValueNoise(seed + 21)
    top, bot = h * 0.2, h * 0.8

    def mask(x, y):
        t = (x + 0.5) / w
        n = vn.fbm(x / 9.0, y / 5.0, 3)
        end = smooth(0.0, 0.16 + 0.08 * n, t) * smooth(0.0, 0.16 - 0.08 * n, 1 - t)
        if fade:
            end *= 0.35 + 0.65 * smooth(-0.25, 0.35, n * 1.7 + 0.1)
        return end

    def body(x, y):
        yy = y + 0.5
        inside = smooth(top - 1.5, top + 1.0, yy) * (1 - smooth(bot - 1.0, bot + 1.5, yy))
        grad = 0.75 + 0.35 * (1 - (yy - top) / (bot - top))
        streak = 0.85 + 0.15 * math.sin(yy * 1.3 + 2.0 * vn.at(x / 14.0, yy / 2.0))
        return inside * grad * streak * mask(x, y) * (0.7 if fade else 1.0)

    def edge(x, y):
        yy = y + 0.5
        dash = 0.75 + 0.25 * math.sin(x * 0.21 + 3 * vn.at(x / 11.0, 1.3))
        e = 1.05 * _obj_g(((yy - top) / 0.95) ** 2) + 0.42 * _obj_g(((yy - top) / 2.6) ** 2)
        e += 0.5 * _obj_g(((yy - bot) / 0.85) ** 2) + 0.22 * _obj_g(((yy - bot) / 2.2) ** 2)
        return e * mask(x, y) * dash * (0.62 if fade else 1.0)
    win = window(w, h, 3, 2)
    img = Img(w, h)
    img.over(OBJ_FRAG_BODY if not fade else solid((54, 24, 104)), sample_fn(w, h, body, 1),
             1.0 if not fade else 0.55, win)
    img.over(ELECTRO if not fade else AFTER, sample_fn(w, h, edge, 1), 1.0, win)
    if not fade:
        x0 = rng.uniform(0.25, 0.6) * w
        pts = jag(rng, (x0, top), (x0 + rng.uniform(10, 26), bot), 4, (0.3, 0.25, 0.2, 0.15))
        over_img(img, render_bolt(w, h, [attrib(pts, 0.6, 0.45, 0.85, 0.6, rng, 0.2)], (), glow=(1.8, 0.8, 0.45),
                                  halo=(2.5, 1.5, 0.1), win=win))
    return img


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


OBJ_GAUGE_SHADOW = solid((22, 10, 44))


def tex_obj_gauge(lit):
    """Orb gauge quarter (circle centre at texel (0,0), side = 0.5 local blocks): an arc at
    radius 0.74*w spanning 9..81 deg over a dark underlay; lit = cyan-white, else dim violet."""
    w = h = 64
    R = 0.74 * w
    a0, a1 = math.radians(9), math.radians(81)

    def arcd(x, y):
        x += 0.5
        y += 0.5
        th = math.atan2(y, x)
        if a0 <= th <= a1:
            return abs(math.hypot(x, y) - R)
        a = a0 if th < a0 else a1
        return math.hypot(x - R * math.cos(a), y - R * math.sin(a))

    under = sample_fn(w, h, lambda x, y: 0.72 * smooth(-1.0, 1.0, 5.2 - arcd(x, y)), 1)
    if lit:
        E = sample_fn(w, h, lambda x, y: 1.1 * smooth(-0.7, 0.7, 1.3 - arcd(x, y)) +
                      0.55 * _obj_g((arcd(x, y) / 3.4) ** 2), 1)
    else:
        E = sample_fn(w, h, lambda x, y: 0.75 * _obj_g((arcd(x, y) / 1.7) ** 2) + 0.25 * _obj_g((arcd(x, y) / 3.5) ** 2), 1)
    win = ([1.0] * w, [1.0] * h)
    img = Img(w, h)
    img.over(OBJ_GAUGE_SHADOW, under, 1.0, win)
    img.over(CYAN if lit else AFTER, E, 1.0, win)
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
    for v, s in (("a", 11), ("c", 37)):
        C.append(entry(f"bolt_after_{v}", 512, 128, "strip", "u", "same path as bolt_" + v,
                       "afterglow of bolt_" + v, lambda s=s: tex_bolt(s, "after")))
        C.append(entry(f"bolt_fade_{v}", 512, 128, "strip", "u", "same path as bolt_" + v,
                       "final fade of bolt_" + v + " (embers)", lambda s=s: tex_bolt(s, "fade")))
    for v, s in zip("abc", (61, 67, 71)):
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
    C.append(entry("orb_rim", 256, 256, "radial", "radial", "rim radius 0.37*w", "eye/orb electric rim",
                   lambda: tex_orb_rim(181)))
    C.append(entry("orb_core", 128, 128, "radial", "radial", "centre", "eye/orb core glow", tex_orb_core))
    C.append(entry("crescent_a", 512, 256, "crescent", "arc", "outer edge r=0.94*h around pivot (0.5,1.0), +-72deg",
                   "clean sword-light crescent / slash wave", lambda: tex_crescent(191, False)))
    C.append(entry("crescent_b", 512, 256, "crescent", "arc", "as crescent_a + bolt along the edge",
                   "lightning crescent slash", lambda: tex_crescent(193, True)))
    C.append(entry("slash_wave", 512, 128, "strip", "u", "edge at v~0.30, tail toward v~0.9",
                   "straight slash wave / sword beam (travels toward -v)", lambda: tex_slash_wave(197)))
    for v, s in zip("ab", (211, 223)):
        C.append(entry(f"rift_{v}", 512, 64, "strip", "u", "v=0.5 thin white tear in a dark void band",
                       "rift / cut ribbon, teleport tears", lambda s=s: tex_rift(s)))
    C.append(entry("shockwave", 512, 512, "radial", "radial", "leading edge r=0.46*w, tail inward to ~0.28*w",
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
    C.append(entry("charge_spark", 64, 128, "column", "v", "base at (0.5, 0.95), rises to v~0.12",
                   "small rising charge spark", lambda: tex_charge_spark(269)))
    C.append(entry("glow_soft", 64, 64, "radial", "radial", "centre", "plain soft glow", tex_glow_soft))
    C.append(entry("glow_strip", 256, 32, "strip", "u", "v=0.5", "plain soft beam glow", tex_glow_strip))
    for name, spec in DECALS.items():
        g = HAZARD_SHAPES[spec["shape"]]
        C.append(entry(name, spec["w"], spec["h"], "decal", "world",
                       f"{spec['sym']} piece: world x {spec['x0']:.3f}..{spec['x1']:.3f}, z {spec['z0']:.3f}..{spec['z1']:.3f}",
                       ("charged (white-hot) " if name.startswith("charged") else "warning ") + f"telegraph of hazard shape {spec['shape']} ({g['kind']})",
                       lambda name=name: tex_decal(name), "hazard-specific; u = local x, v = local forward z; mirrored by the cards"))
    for k in range(len(RING_R)):
        n = ring_px(k)
        C.append(entry(f"ringq_{k}", n, n, "quarter", "radial",
                       f"circle centre at (0,0); band radius {RING_R[k]}+-{RING_HALF} of {ring_extent(k):.3f} blocks per texture side",
                       "expanding ring quadrant (hazard shape 11)", lambda k=k: tex_ring_quarter(k)))
    # rig (boss body) sprites, see build_raiden_rig.mjs
    for v, s in zip("ab", (307, 311)):
        C.append(dict(entry(f"rig_katana_{v}", RIG_KW, RIG_KH, "blade", "u",
                       f"edge bolt hugs the giant-katana edge; card = model y {RIG_KY0}..{RIG_KY1} (u, hilt->tip) x "
                       f"model x {RIG_KX0}..{RIG_KX1} (v, edge side first)",
                       "blade-plane sheath card of fx_weapon/katana_*", lambda s=s: tex_rig_katana(s),
                       "spine crackle at the spine side, tip fork + bloom; the blade body hides the middle"),
                      card=dict(model_x=[RIG_KX0, RIG_KX1], model_y=[RIG_KY0, RIG_KY1])))
    C.append(dict(entry("rig_palm", RIG_PW, RIG_PH, "palm", "v",
                   f"arcs from fingertips {RIG_TIPS} and the thumb into palm centre {RIG_PALM_C}; card = model x "
                   f"{RIG_PX0}..{RIG_PX1} (u) x model y {RIG_PY1}..{RIG_PY0} (v, wrist first)",
                   "palm-parallel charge card of fx_weapon/palm_*", lambda: tex_rig_palm(313),
                   "fingertips symmetric about x=8: mirror u for the other flicker frame"),
                  card=dict(model_x=[RIG_PX0, RIG_PX1], model_y=[RIG_PY0, RIG_PY1], centre=list(RIG_PALM_C))))
    C.append(entry("rig_crown", 192, 192, "radial", "radial", "bolts from r~0.09w to 0.36..0.47w, broken ring r=0.31w",
                   "palm release crown (fx_weapon/palm_*_release_*)", lambda: tex_rig_crown(317),
                   "dark centre; rotate/mirror the uv for the second flicker frame"))
    C.append(entry("rig_shard", 48, 128, "column", "v", "lens tips at v=0.03/0.97, widest at v~0.39, ridge u~0.5",
                   "translucent crystal splinter (death_shard_*)", lambda: tex_rig_shard(331)))
    # object / blink / orb sprites (build_raiden_object_vfx.py, build_raiden_movement.py, build_raiden_orb.py)
    C.append(entry("obj_swing_band", 512, 64, "strip", "u", "line v=0.27 (u=0) -> 0.73 (u=1), brightest near u~0.9",
                   "illusion swing ribbon (u = swing start -> blade end)", lambda: tex_obj_swing_band(401),
                   "u=0 oldest (dissolving tail), u=1 newest; map onto chord cards spanning 0.9 block of height"))
    C.append(entry("obj_wave_band", 512, 64, "strip", "u", "v=0.5 white core, lens envelope sin(pi*u)",
                   "flying sword-wave front band (chord cards along the crescent edge)",
                   lambda: tex_obj_wave_band(409), "layered glow, crackle along the core, cyan sparks"))
    C.append(entry("obj_wave_fade", 512, 64, "strip", "u", "v=0.5, lens envelope", "afterglow of obj_wave_band",
                   lambda: tex_obj_wave_band(409, True), "dissolving purple with embers"))
    for v, s in zip("ab", (419, 421)):
        C.append(entry(f"obj_frag_{v}", 128, 32, "strip", "u", "glowing top edge v=0.2, dim bottom edge v=0.8",
                       "blink silhouette strip (u across the body, v top -> bottom)", lambda s=s: tex_obj_frag(s),
                       "ragged dissolving ends, short lightning seam"))
    C.append(entry("obj_frag_fade", 128, 32, "strip", "u", "as obj_frag_*", "dissolving blink strip (afterglow)",
                   lambda: tex_obj_frag(431, True)))
    C.append(entry("obj_shard", 64, 64, "strip", "u", "tip at u~0.93, body u 0.42..0.93, streak toward u=0",
                   "flying electro shard (break bursts)", lambda: tex_obj_shard(433)))
    C.append(entry("obj_gauge_on", 64, 64, "quarter", "radial", "arc r=0.74*w over 9..81 deg, centre at texel (0,0)",
                   "lit remembrance-orb gauge quadrant (side = 0.5 local blocks)", lambda: tex_obj_gauge(True),
                   "mirror the uv for the other quadrants"))
    C.append(entry("obj_gauge_off", 64, 64, "quarter", "radial", "as obj_gauge_on", "spent orb gauge quadrant",
                   lambda: tex_obj_gauge(False)))
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
            "hazard_decals": DECALS, "ring_radii": RING_R, "ring_half": RING_HALF, "ring_pad": RING_PAD}
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--resourcepack", type=Path, default=Path(__file__).resolve().parents[2] / "resourcepack")
    parser.add_argument("--only", help="comma list of texture names (development)")
    parser.add_argument("--catalogue", action="store_true", help="only rewrite tools/raiden_fx_textures.json")
    a = parser.parse_args()
    write_catalogue_json()
    if not a.catalogue:
        build_fx_textures(a.resourcepack, set(a.only.split(",")) if a.only else None)
