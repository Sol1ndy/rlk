"""Native display meshes for all thirteen Narukami hazard volumes.

Called by build_raiden_hazards.py. One owned display holds a whole warning or
strike. The hit generator remains the authority for positions, yaw, timing,
and the jumpable ring radius; this file only rebuilds model/item JSON in the
resource pack (the datapack functions it writes are unchanged).

Every mesh is a handful of flat textured cards (zero-thickness elements with a
face on each side, shade off) using the painted gradient sprites of
build_raiden_fx_textures.py (rlk:raiden/fxg/*):
  warning  feathered telegraph decal tele_<s>: dark underlay, magenta/violet rim
           with inner glow, bright centre line, soft chevrons, faint inner veins.
           Decals are mirrored symmetry pieces (half / quadrant / one card per fan
           ray) so they hold >= 32 texels per block.
  charge   white-hot decal charged_<s>, dimmed by a constant item tint on the first
           of the two steps; the second step adds crisp boundary crackle strips;
           both add rising charge sparks standing on the boundary.
  strike   area flash (charged decal, or for disks a centred shockwave ring whose
           bright edge is the hit radius plus an impact flash), jagged floor bolts
           (bolt_a/b/c, one variant per flicker frame), crossed vertical bolts
           (pillars split at 2.4 blocks, lightning walls) and blade-light crescents;
           the two flicker frames mirror the sprites and dim the area by tint.
  after    afterglow bolts (bolt_after_c, vbolt_after_c) over scorch streaks;
  fade     dissolving embers (bolt_fade_c) over the scorch.
  ring     exact +-0.7 band: four mirrored quarter textures + 16 low crackle
           walls (all below 0.75 so jumping visibly clears it).
Layer heights: decal 0.02 < crackle 0.045 < scorch 0.065 < floor bolts 0.09+ (each
>= 0.02 apart). Vanilla sorts translucent quads by centroid and writes depth, so
overlay sprites keep tight halos (see the texture library notes).
Model coordinates: model = 8 + world/2 (display scale 32; right_rotation cancels
the item flip, so model +z = hazard forward). All cards stay inside -16..32 and
only use single-axis Y rotations of 0/+-22.5/+-45 degrees.
"""
from pathlib import Path
import json
import math
import sys

from build_raiden_fx_textures import (HAZARD_SHAPES, DECALS, DECAL_SYM, RING_R, RING_HALF, RING_END, RING_FRAMES, ring_extent, shape_outline,
                                      build_fx_textures, catalogue, TEX_SUBDIR, NS)

SCALE = 32
# Display culling width (blocks) for hazard meshes: the outermost ring frame must fit.
CULL_W = 2*math.ceil(ring_extent(len(RING_R)-1)*RING_END/RING_R[-1])+2
# Shapes 13 (illusion sword wave) and 14 (몽상의 일심 disk) are appended; shapes 1-12 keep
# their hit volumes.
SHAPES = range(1, 15)
LINES = {2: (12, 2.2), 5: (20, 3.6), 7: (8, 8), 10: (18, 7), 13: (22, 2.4)}
DISKS = {3: 3, 6: 5, 8: 6, 12: 12, 14: 19}
SECTORS = {1: (6, 60), 4: (12, 70)}
for _s, (_L, _W) in LINES.items():
    assert HAZARD_SHAPES[_s] == dict(kind="rect", length=_L, width=_W), _s
for _s, _r in DISKS.items():
    assert HAZARD_SHAPES[_s] == dict(kind="disk", r=_r), _s
for _s, (_r, _a) in SECTORS.items():
    assert HAZARD_SHAPES[_s] == dict(kind="sector", r=_r, half=_a), _s
assert HAZARD_SHAPES[9]["angles"] == (-40, -20, 0, 20, 40) and HAZARD_SHAPES[9]["length"] == 18
assert HAZARD_SHAPES[11] == dict(kind="annulus", r0=1.3, r1=2.7)

FX = {c["name"] for c in catalogue()}
ALLOWED = (-45.0, -22.5, 0.0, 22.5, 45.0)
AXES = {"+x": (0, 1), "-x": (0, -1), "+y": (1, 1), "-y": (1, -1), "+z": (2, 1), "-z": (2, -1)}
FACE_PAIR = {0: ("east", "west"), 1: ("up", "down"), 2: ("south", "north")}
# Constant item tints (multiply RGB only): dim first charge step and the flicker decay.
# Card heights: decal < crackle < scorch < floor bolts (>= 0.02 apart against z-fighting).
Y_DECAL = 0.02
Y_CRACKLE = 0.045
Y_SCORCH = 0.065
Y_BOLT = 0.09
TINT_CHARGE0 = 0xC8B6EA
TINT_FLASH1 = 0xDCD0F2
TINT_FLASH2 = 0xA897D2
TINT_RESIDUE = 0x8C74BE
ABC = "abc"


def face_corners(face, lo, hi):
    """TL, TR, BR, BL of a face seen from outside (vanilla FaceInfo vertex order)."""
    x0, y0, z0 = lo
    x1, y1, z1 = hi
    return {
        "north": [(x1, y1, z0), (x0, y1, z0), (x0, y0, z0), (x1, y0, z0)],
        "south": [(x0, y1, z1), (x1, y1, z1), (x1, y0, z1), (x0, y0, z1)],
        "east": [(x1, y1, z1), (x1, y1, z0), (x1, y0, z0), (x1, y0, z1)],
        "west": [(x0, y1, z0), (x0, y1, z1), (x0, y0, z1), (x0, y0, z0)],
        "up": [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
        "down": [(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)],
    }[face]


def solve_uv(face, lo, hi, fn):
    """Face uv [u1,v1,u2,v2] + rotation so that every corner shows fn(corner) (vanilla
    rule: corner i takes the (i - rotation/90)-th entry of (u1v1, u2v1, u2v2, u1v2))."""
    D = [fn(c) for c in face_corners(face, lo, hi)]
    for k in range(4):
        u = [D[(j + k) % 4] for j in range(4)]
        if (abs(u[0][1] - u[1][1]) < 1e-6 and abs(u[1][0] - u[2][0]) < 1e-6 and
                abs(u[2][1] - u[3][1]) < 1e-6 and abs(u[3][0] - u[0][0]) < 1e-6):
            return [round(u[0][0], 4), round(u[0][1], 4), round(u[2][0], 4), round(u[2][1], 4)], k * 90
    raise ValueError(f"no uv solution for {face}")


class Model:
    def __init__(self):
        self.textures = {}
        self.elements = []
        self.tint = None

    def var(self, name):
        assert name in FX, name
        tid = NS + name
        for k, v in self.textures.items():
            if v == tid:
                return k
        k = f"t{len(self.textures)}"
        self.textures[k] = tid
        return k

    def card(self, center, normal, uaxis, vaxis, su, sv, tex, angle=0.0, uv=(0, 0, 16, 16), tint=False):
        """Flat card centred on `center` (world, hazard frame) lying across `normal` ('x'|'y'|'z').
        Texture u runs from uv[0] at the -uaxis edge to uv[2] at the +uaxis edge (likewise v);
        `angle` turns the whole card about +Y (positive = from +z toward +x)."""
        n = "xyz".index(normal)
        ua, us = AXES[uaxis]
        va, vs = AXES[vaxis]
        assert len({n, ua, va}) == 3, (normal, uaxis, vaxis)
        c = [8 + v * 16 / SCALE for v in center]
        half = [0.0, 0.0, 0.0]
        half[ua] = su * 8 / SCALE
        half[va] = sv * 8 / SCALE
        lo = [round(c[i] - half[i], 4) for i in range(3)]
        hi = [round(c[i] + half[i], 4) for i in range(3)]
        assert all(-16 <= v <= 32 for v in lo + hi), (tex, lo, hi)

        def fn(p):
            tu = (1 if p[ua] > c[ua] else -1) * us
            tv = (1 if p[va] > c[va] else -1) * vs
            return (uv[0] + (uv[2] - uv[0]) * (tu + 1) / 2, uv[1] + (uv[3] - uv[1]) * (tv + 1) / 2)
        var = self.var(tex)
        faces = {}
        for f in FACE_PAIR[n]:
            fuv, rot = solve_uv(f, lo, hi, fn)
            spec = {"texture": "#" + var, "uv": fuv}
            if rot:
                spec["rotation"] = rot
            if tint:
                spec["tintindex"] = 0
            faces[f] = spec
        el = {"from": lo, "to": hi, "shade": False, "faces": faces}
        if angle:
            assert angle in ALLOWED, angle
            el["rotation"] = {"origin": [round(v, 4) for v in c], "axis": "y", "angle": angle}
        self.elements.append(el)

    def json(self):
        tex = dict(self.textures)
        if tex:
            tex["particle"] = next(iter(self.textures.values()))
        return {"ambientocclusion": False, "gui_light": "front", "textures": tex, "elements": self.elements}

# --------------------------------------------------------------------------- placement helpers


def heading(theta):
    """Direction theta (deg, from +z toward +x) -> (u axis, v axis, element Y angle), or None."""
    for base, ua, va in ((0, "+z", "-x"), (90, "+x", "+z"), (180, "-z", "+x"), (-90, "-x", "-z")):
        a = (theta - base + 180) % 360 - 180
        for al in ALLOWED:
            if abs(a - al) < 1e-6:
                return ua, va, al
    return None


def strip(m, p0, p1, width, tex, y=0.06, wall=None, uv=(0, 0, 16, 16), maxjog=0.35, tint=False):
    """Card along p0 -> p1 (x, z). wall=None: lying flat at height y, `width` across.
    wall=(y0, y1): standing vertical on the segment (texture v = top -> bottom).
    Directions that are not multiples of 22.5 deg are split into quantised pieces that
    follow the exact segment (lateral jog per piece <= maxjog); u is split to match."""
    dx, dz = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dz)
    theta = math.degrees(math.atan2(dx, dz))
    q = round(theta / 22.5) * 22.5
    dev = math.radians(abs(theta - q))
    n = 1 if dev < 1e-6 else max(1, math.ceil(L * math.sin(dev) / maxjog))
    for i in range(n):
        a = (p0[0] + dx * i / n, p0[1] + dz * i / n)
        b = (p0[0] + dx * (i + 1) / n, p0[1] + dz * (i + 1) / n)
        ua, va, ang = heading(q)
        seg = L / n * math.cos(dev) + (0.18 if n > 1 else 0.0)
        cx, cz = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        u0 = uv[0] + (uv[2] - uv[0]) * i / n
        u1 = uv[0] + (uv[2] - uv[0]) * (i + 1) / n
        if wall is None:
            m.card((cx, y, cz), "y", ua, va, seg, width, tex, ang, (u0, uv[1], u1, uv[3]), tint)
        else:
            y0, y1 = wall
            m.card((cx, (y0 + y1) / 2, cz), "x" if ua in ("+z", "-z") else "z", ua, "-y", seg, y1 - y0, tex, ang,
                   (u0, uv[1], u1, uv[3]), tint)


def radial(m, x, z, size, tex, y, tint=False, flip=False):
    m.card((x, y, z), "y", "+x", "+z", size, size, tex, 0, (16, 0, 0, 16) if flip else (0, 0, 16, 16), tint)


PILLAR_SPLIT = 2.4


def pillar(m, x, z, y0, height, width, texs, planes=4, flip=0):
    """Crossed vertical cards (planes along z, x, then the two diagonals) sharing one axis.
    Tall pillars are cut at PILLAR_SPLIT: vanilla sorts translucent quads by centroid and
    writes depth, and a low segment (centroid near eye height) sorts after the floor cards
    instead of hiding them; the diagonal planes only exist above the cut."""
    spec = (("+z", "x", 0.0), ("+x", "z", 0.0), ("+z", "x", 45.0), ("+z", "x", -45.0))
    cut = y0 + PILLAR_SPLIT
    split = height > 5.5
    for k in range(planes):
        ua, normal, ang = spec[k]
        uv = (16, 0, 0, 16) if (k + flip) % 2 else (0, 0, 16, 16)
        tex = texs[k % len(texs)]
        if not split:
            m.card((x, y0 + height / 2, z), normal, ua, "-y", width, height, tex, ang, uv)
            continue
        vcut = 16 * (y0 + height - cut) / height
        m.card((x, (cut + y0 + height) / 2, z), normal, ua, "-y", width, y0 + height - cut, tex, ang,
               (uv[0], 0, uv[2], vcut))
        if k < 2:
            m.card((x, (y0 + cut) / 2, z), normal, ua, "-y", width, cut - y0, tex, ang, (uv[0], vcut, uv[2], 16))


def decal(m, shape, kind, y=Y_DECAL, tint=None):
    """Telegraph decal from its mirrored symmetry pieces (see DECAL_SYM in the texture library)."""
    t = tint is not None
    if t:
        m.tint = tint
    sym = DECAL_SYM[shape]
    if sym == "ray":
        for a in HAZARD_SHAPES[shape]["angles"]:
            q = round(a / 22.5) * 22.5
            d = a - q
            name = f"{kind}_{shape}_{int(round(abs(d) * 10))}"
            spec = DECALS[name]
            sgn = 1 if d >= 0 else -1           # the texture is painted for a +slant; mirror u for -
            cx, cz = sgn * (spec["x0"] + spec["x1"]) / 2, (spec["z0"] + spec["z1"]) / 2
            c, s_ = math.cos(math.radians(q)), math.sin(math.radians(q))
            # rotate the card about its own centre by q, centre placed so local (0,0) = hazard origin
            m.card((cx * c + cz * s_, y, -cx * s_ + cz * c), "y", "+x", "+z", spec["x1"] - spec["x0"],
                   spec["z1"] - spec["z0"], name, q, (0, 0, 16, 16) if sgn > 0 else (16, 0, 0, 16), t)
        return
    name = f"{kind}_{shape}"
    d = DECALS[name]
    cx, cz = (d["x0"] + d["x1"]) / 2, (d["z0"] + d["z1"]) / 2
    sx, sz = d["x1"] - d["x0"], d["z1"] - d["z0"]
    for mx in (1, -1):
        for mz in ((1, -1) if sym == "quad" else (1,)):
            uv = (0 if mx > 0 else 16, 0 if mz > 0 else 16, 16 if mx > 0 else 0, 16 if mz > 0 else 0)
            m.card((mx * cx, y, mz * cz), "y", "+x", "+z", sx, sz, name, 0, uv, t)


def crescent(m, R, y, tex, flip=False, z0=0.0, tint=False):
    """Blade-light crescent lying flat, pivot at (0, z0), cutting edge radius R bulging forward (+z)."""
    H = R / 0.94
    m.card((0, y, z0 + H / 2), "y", "+x", "-z", 2 * H, H, tex, 0, (16, 0, 0, 16) if flip else (0, 0, 16, 16), tint)


def outline_points(shape, spacing, limit):
    pts = []
    for poly in shape_outline(HAZARD_SHAPES[shape]):
        acc = spacing / 2
        for a, b in zip(poly, poly[1:]):
            L = math.dist(a, b)
            while acc < L:
                t = acc / L
                pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
                acc += spacing
            acc -= L
    if len(pts) > limit:
        step = len(pts) / limit
        pts = [pts[int(i * step)] for i in range(limit)]
    return pts


def charge_sparks(m, shape, phase):
    g = HAZARD_SHAPES[shape]
    perim = sum(math.dist(a, b) for poly in shape_outline(g) for a, b in zip(poly, poly[1:]))
    count = 10 if phase else 7
    pts = outline_points(shape, max(1.0, perim / count), count)
    h = 0.62 if phase == 0 else 1.0
    for i, (x, z) in enumerate(pts):
        hh = h * (0.8 + 0.4 * ((i * 7919) % 5) / 4)
        planes = (("+z", "x"), ("+x", "z"))
        for k, (ua, normal) in enumerate(planes):
            uv = (16, 0, 0, 16) if (i + k + phase) % 2 else (0, 0, 16, 16)
            m.card((x, hh / 2, z), normal, ua, "-y", hh * 0.5, hh, "charge_spark", 0, uv)

def edge_segments(shape):
    """Boundary pieces (world x,z pairs) for crisp crackle strips; circles become chords whose
    directions are multiples of 22.5 deg, so each chord is a single card."""
    g = HAZARD_SHAPES[shape]
    k = g["kind"]
    segs = []
    if k == "rect":
        L, hw = g["length"], g["width"] / 2
        n = max(1, math.ceil(L / 7))
        for x in (-hw, hw):
            segs += [((x, L * i / n), (x, L * (i + 1) / n)) for i in range(n)]
        segs += [((-hw, 0), (hw, 0)), ((-hw, L), (hw, L))]
    elif k in ("disk", "annulus"):
        for r in ((g["r"],) if k == "disk" else (g["r0"], g["r1"])):
            n = 16 if r >= 3 else 8
            half = 180 / n
            re = r * 2 / (1 + math.cos(math.radians(half)))
            segs += [(polar(re, 360 * i / n - half), polar(re, 360 * i / n + half)) for i in range(n)]
    elif k == "sector":
        r, a = g["r"], g["half"]
        segs += [((0, 0), polar(r, -a)), ((0, 0), polar(r, a))]
        re = r * 2 / (1 + math.cos(math.radians(11.25)))
        k = int((a - 11.25) // 22.5)
        segs += [(polar(re, 22.5 * i - 11.25), polar(re, 22.5 * i + 11.25)) for i in range(-k, k + 1)]
        edge = 22.5 * k + 11.25
        if a - edge > 1.0:
            segs += [(polar(r, edge), polar(r, a)), (polar(r, -a), polar(r, -edge))]
    elif k == "fan":
        segs += [(polar(0.8, a), polar(g["length"] - 0.3, a)) for a in g["angles"]]
    return segs


def edge_crackle(m, shape, v):
    width = 0.75 if shape in (4, 5, 9, 10, 12, 13) else 0.55
    for i, (a, b) in enumerate(edge_segments(shape)):
        tex = "rim_crackle_" + ABC[(i + v) % 3]
        uv = (16, 0, 0, 16) if (i + v) % 2 else (0, 0, 16, 16)
        strip(m, a, b, width, tex, y=Y_CRACKLE, uv=uv, maxjog=0.4)


# --------------------------------------------------------------------------- frames


class Style:
    """What one strike-family frame draws. v = flicker index (0, 1, 2); kind = hot|after|fade."""

    def __init__(self, kind, v=2):
        self.kind, self.v = kind, v
        self.hot = kind == "hot"
        if self.hot:
            self.bolt = "bolt_" + ABC[v]
            self.alt = "bolt_" + ABC[(v + 1) % 3]
            self.vbolts = ["vbolt_" + ABC[(v + k) % 3] for k in range(3)]
        else:
            self.bolt = self.alt = "bolt_" + kind + "_c"
            self.vbolts = ["vbolt_after_c"] if kind == "after" else []
        # flicker frames mirror the same sprites differently; after/fade reuse frame 2's mapping
        self.flip_v = v == 1 and self.hot
        self.flip_u = v == 2 or not self.hot

    def uv(self):
        u0, u1 = (16, 0) if self.flip_u else (0, 16)
        v0, v1 = (16, 0) if self.flip_v else (0, 16)
        return (u0, v0, u1, v1)


def floor_bolt(m, st, p0, p1, width, layer, alt=False, maxjog=0.35):
    """Bolt lying on the floor; afterglow frames add a scorch streak beneath it."""
    y = Y_BOLT + 0.025 * layer
    if not st.hot:
        strip(m, p0, p1, width * 0.55, "scorch_strip", y=Y_SCORCH, maxjog=maxjog)
    strip(m, p0, p1, width, st.alt if alt else st.bolt, y=y, uv=st.uv(), maxjog=maxjog)


def wall_bolt(m, st, p0, p1, y0, y1, alt=False, maxjog=0.35):
    """Vertical bolt standing over the decal. Hot frames use the tight-glow blade sprites so the
    depth-writing footprint stays small; the afterglow keeps the wide dissolving residue."""
    if st.kind == "fade":
        return
    # match the sprite's aspect: long low walls take the 8:1 blade strip, tall ones the 4:1 bolt
    long_low = math.dist(p0, p1) / (y1 - y0) > 5
    if st.hot:
        tex = ("blade_" if long_low else "bolt_") + ABC[(st.v + (1 if alt else 0)) % 3]
    else:
        tex = st.bolt
    strip(m, p0, p1, 0, tex, wall=(y0, y1), uv=st.uv(), maxjog=maxjog)


def column(m, st, x, z, y0, height, width, planes=4):
    if not st.vbolts:
        return
    pillar(m, x, z, y0, height, width, st.vbolts, planes, st.v)


def area(m, st, shape):
    """Area flash of a strike frame. Disks use single centred cards (shockwave ring whose bright
    edge is the hit radius + impact flash) instead of their four mirrored decal quadrants: a
    quadrant sorted after a centred overlay would be hidden under it (vanilla depth writes)."""
    if not st.hot:
        return
    tint = (None, TINT_FLASH1, TINT_FLASH2)[st.v]
    if shape in DISKS:
        r = DISKS[shape]
        radial(m, 0, 0, r / 0.46, "shockwave", Y_DECAL, tint is not None, st.v == 1)
        radial(m, 0, 0, {3: 6.0, 6: 5.0, 8: 5.5, 12: 8.0, 14: 11.0}[shape], "flash", Y_DECAL + 0.045, flip=st.v == 2)
        m.tint = tint
    else:
        decal(m, shape, "charged", Y_DECAL, tint)
    if st.v == 0 and shape not in (9, 12, 14):
        edge_crackle(m, shape, 1)


def polar(r, ang):
    return (r * math.sin(math.radians(ang)), r * math.cos(math.radians(ang)))


def strike(shape, st):
    m = Model()
    area(m, st, shape)
    if shape in SECTORS:
        r, half = SECTORS[shape]
        angs = (-45, 0, 45) if shape == 1 else (-45, -22.5, 0, 22.5, 45)
        for i, a in enumerate(angs):
            floor_bolt(m, st, polar(0.4, a), polar(r - 0.25, a), 1.5 if shape == 1 else 2.4, i, i % 2 == 1)
        if st.hot:
            top, low = ("crescent_b", "crescent_a") if st.v != 1 else ("crescent_a", "crescent_b")
            crescent(m, r, 1.05 if shape == 1 else 1.6, top, st.v == 2)
            crescent(m, r * 0.82, 0.45 if shape == 1 else 0.7, low, st.v != 0)
        elif st.kind == "after":
            # the slash leaves a dim, sinking blade-light residue for the afterglow ticks
            crescent(m, r * 0.9, 0.3, "crescent_a", True, tint=True)
            m.tint = TINT_RESIDUE
        if shape == 4:
            for i, a in enumerate((-35, 0, 35)):
                x, z = polar(r * 0.86, a)
                column(m, st, x, z, 0.0, 3.4, 1.6, 2)
    elif shape in DISKS:
        r = DISKS[shape]
        dirs = (0, 90, 180, 270) if shape == 3 else (0, 45, 90, 135, 180, 225, 270, 315)
        width = {3: 1.0, 6: 1.4, 8: 1.5, 12: 2.4, 14: 3.0}[shape]
        for i, a in enumerate(dirs):
            floor_bolt(m, st, polar(min(0.6, r * 0.08), a), polar(r - 0.25, a), width, i, i % 2 == 1)
        if shape != 6:
            height, w = {3: (9.5, 2.8), 8: (7.0, 2.6), 12: (10.0, 3.4), 14: (12.0, 4.0)}[shape]
            column(m, st, 0, 0, 0.0, height, w, 4)
        if shape == 6:
            for a in (45, 135, 225, 315):
                x, z = polar(2.6, a)
                column(m, st, x, z, 0.0, 2.8, 1.3, 2)
        if shape == 12:
            for k in range(6):
                x, z = polar(7.2, 30 + 60 * k)
                column(m, st, x, z, 0.0, 4.6, 1.8, 2)
        if shape == 14:
            for k in range(8):
                x, z = polar(11.5, 22.5 + 45 * k)
                column(m, st, x, z, 0.0, 6.0, 2.2, 2)
        if st.kind == "after":
            radial(m, 0, 0, r * 0.9, "scorch", Y_CRACKLE)
    elif shape == 9:
        L = 18
        for i, a in enumerate((-40, -20, 0, 20, 40)):
            floor_bolt(m, st, polar(0.5, a), polar(L - 0.4, a), 1.2, i % 2, i % 2 == 1, maxjog=0.5)
            if st.hot:
                wall_bolt(m, st, polar(0.6, a), polar(L - 0.6, a), 0.15, 1.65, i % 2 == 0, maxjog=0.5)
        if st.hot:
            radial(m, 0, 0.4, 3.2, "flash", 0.12)
    elif shape in (2, 13):
        L, W = LINES[shape]
        floor_bolt(m, st, (0, 0.2), (0, L - 0.2), W, 0)
        wall_bolt(m, st, (0, 0.3), (0, L - 0.3), 0.25 if shape == 2 else 0.3, 2.15 if shape == 2 else 1.9, True)
        if st.hot:
            strip(m, (0, 0.3), (0, L - 0.1), 0.75, "blade_" + ABC[st.v], y=1.2 if shape == 2 else 1.0, uv=st.uv())
            if shape == 2:
                pillar(m, 0, L - 0.2, 0.1, 2.2, 2.2, ["flash"], 2)
            else:
                # forward-bulging sword-wave crescents along the corridor
                for i, z in enumerate((2.4, 7.9, 13.4, 18.9)):
                    crescent(m, 1.45, 1.0 + 0.04 * i, "crescent_" + "ab"[(i + st.v) % 2], (i + st.v) % 2 == 1, z)
    elif shape == 5:
        L, W = LINES[5]
        floor_bolt(m, st, (0, 0.2), (0, L - 0.2), W, 0)
        floor_bolt(m, st, (0.9 if st.v % 2 else -0.9, 0.6), (0, L - 0.6), 2.4, 1, True)
        wall_bolt(m, st, (0, 0.4), (0, L - 0.4), 0.3, 2.7, True)
        if st.hot:
            strip(m, (0, 0.15), (0, L - 0.15), 0, "slash_wave", wall=(0.15, 4.5), uv=(16, 0, 0, 16) if st.v == 1 else (0, 0, 16, 16))
        for z in (5, 10, 15):
            column(m, st, 0, z, 0.0, 3.6, 1.6, 2)
    elif shape == 7:
        L, W = LINES[7]
        for i, z in enumerate((1.2, 3.2, 4.8, 6.8)):
            wall_bolt(m, st, (-W / 2 + 0.1, z), (W / 2 - 0.1, z), 0.15, 2.7, i % 2 == 1)
        for i, z in enumerate((2.2, 5.8)):
            floor_bolt(m, st, (-W / 2 + 0.2, z), (W / 2 - 0.2, z), 2.2, i, i == 1)
        column(m, st, 0, 4, 0.0, 6.5, 2.4, 4)
        if st.hot:
            radial(m, 0, 4, 4.5, "flash", 0.12)
    elif shape == 10:
        L, W = LINES[10]
        for i, x in enumerate((-2.4, 0, 2.4)):
            floor_bolt(m, st, (x, 0.2), (x, L - 0.2), 2.2, i, i == 1)
        if st.kind != "fade":
            for i, z in enumerate((3, 9, 15)):
                arc = "arc_" + "ab"[(i + st.v) % 2] if st.hot else "crackle_" + "ab"[i % 2]
                strip(m, (-W / 2 - 0.2, z), (W / 2 + 0.2, z), 0, arc, wall=(0.0, 2.6 if st.hot else 0.8))
        if st.hot:
            for i, z in enumerate((1.6, 7.6, 13.6)):
                crescent(m, 3.55, 0.95 + 0.04 * i, "crescent_" + "ba"[(i + st.v) % 2], (i + st.v) % 2 == 1, z)
    return m


def ring(frame):
    """Ring band of radius r +- 0.7 (exact damage band) at frame 0..RING_FRAMES-1."""
    m = Model()
    r = 2 + (RING_END - 2) * frame / (RING_FRAMES - 1)
    k = min(range(len(RING_R)), key=lambda i: abs(math.log(r / RING_R[i])))
    E = ring_extent(k) * r / RING_R[k]
    for sx in (1, -1):
        for sz in (1, -1):
            # circle centre at the texture's (0,0) corner; mirror the uv for each quadrant
            m.card((sx * E / 2, 0.05, sz * E / 2), "y", "+x", "+z", E, E, f"ringq_{k}", 0,
                   (0 if sx > 0 else 16, 0 if sz > 0 else 16, 16 if sx > 0 else 0, 16 if sz > 0 else 0))
    chord = 2 * r * math.tan(math.radians(11.25)) * 1.12
    for i in range(16):
        a = 22.5 * i
        x, z = polar(r, a)
        tang = a + 90
        ua, va, ang = heading((tang + 180) % 360 - 180)
        tex = "crackle_" + "ab"[(i + frame) % 2]
        uv = (16, 0, 0, 16) if (i + frame // 2) % 2 else (0, 0, 16, 16)
        m.card((x, 0.36, z), "x" if ua in ("+z", "-z") else "z", ua, "-y", chord, 0.72, tex, ang, uv)
    return m

# --------------------------------------------------------------------------- build


def build(root, out):
    rp = root.parent / "resourcepack"
    if "--resourcepack" in sys.argv:
        rp = Path(sys.argv[sys.argv.index("--resourcepack") + 1])
    from build_raiden_materials import build_materials
    build_materials(rp)
    texdir = rp / TEX_SUBDIR
    if not all((texdir / (n + ".png")).exists() for n in FX):
        build_fx_textures(rp)
    modeldir = rp / "assets/rlk/models/item/raiden/fx_hazard"
    itemdir = rp / "assets/rlk/items/raiden/fx_hazard"
    modeldir.mkdir(parents=True, exist_ok=True)
    itemdir.mkdir(parents=True, exist_ok=True)

    def write(name, lines):
        path = out / (name + ".mcfunction")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    stats = {"models": 0, "max": 0}

    def save(name, model):
        (modeldir / (name + ".json")).write_text(json.dumps(model.json(), separators=(",", ":")) + "\n", encoding="utf-8")
        node = {"type": "minecraft:model", "model": "rlk:item/raiden/fx_hazard/" + name}
        if model.tint is not None:
            node["tints"] = [{"type": "minecraft:constant", "value": model.tint}]
        (itemdir / (name + ".json")).write_text(json.dumps({"model": node}, separators=(",", ":")) + "\n", encoding="utf-8")
        stats["models"] += 1
        if len(model.elements) > stats["max"]:
            stats["max"], stats["maxname"] = len(model.elements), name

    for shape in SHAPES:
        m = Model()
        decal(m, shape, "tele")
        save(f"warning_{shape}", m)
        for phase in (0, 1):
            m = Model()
            decal(m, shape, "charged", Y_DECAL, TINT_CHARGE0 if phase == 0 else None)
            if phase:
                edge_crackle(m, shape, 0)
            charge_sparks(m, shape, phase)
            save(f"charge_{shape}_{phase}", m)
        if shape != 11:
            save(f"strike_{shape}", strike(shape, Style("hot", 0)))
            save(f"strike_{shape}_1", strike(shape, Style("hot", 1)))
            save(f"strike_{shape}_2", strike(shape, Style("hot", 2)))
            save(f"after_{shape}", strike(shape, Style("after")))
            save(f"after_{shape}_fade", strike(shape, Style("fade")))
    for frame in range(RING_FRAMES):
        save(f"ring_{frame:02}", ring(frame))

    owned='@e[type=minecraft:item_display,tag=rlk_rd_hvfx]'
    new='@e[tag=rlk_rd_vnew,limit=1]'
    modelset=lambda name: 'data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_hazard/'+name+'"'
    write("vfx_init",[
        '# One display per fixed hazard origin; all geometry is in its local coordinates.',
        '# Native ItemDisplayRenderer applies Y=180deg after display transformations.',
        '# Right-rotate 180deg to cancel that item-only flip: mesh +Z now equals ^ ^ ^forward.',
        'scoreboard players add #rdHazardSerial rd 1',
        'scoreboard players operation @s rdHId = #rdHazardSerial rd',
        '# Culling box: wide enough for the outermost ring frame (radius RING_END plus its band).',
        'summon minecraft:item_display ~ ~ ~ {Tags:["rlk_rd_hvfx","rlk_rd_vnew","rlk_raiden_aux","rlk_room"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:0,teleport_duration:0,view_range:3f,width:'+str(CULL_W)+'f,height:22f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[32f,32f,32f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_hazard/warning_1"}}}',
        f'data modify entity {new} Rotation set from entity @s Rotation',
        f'scoreboard players operation {new} rdVId = @s rdHId',
        f'scoreboard players operation {new} rdShape = @s rdShape',
        f'scoreboard players set {new} rdWind 0',
        f'scoreboard players set {new} rdHAge 0',
        f'execute as {new} run function rlk:boss/raiden/hazard/vfx_warning',
        'tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew',
    ])
    write("vfx_warning",[f'execute if score @s rdShape matches {s} run {modelset("warning_"+str(s))}' for s in SHAPES])
    write("charge",[
        '# Four ticks before impact: charged borders, no full-path strike yet.',
        'scoreboard players operation #rdVfxOwner rd = @s rdHId',
        'scoreboard players set #rdChargeFrame rd 0',
        'execute if score #rdUntil rd matches 1..2 run scoreboard players set #rdChargeFrame rd 1',
        f'execute as {owned} if score @s rdVId = #rdVfxOwner rd run function rlk:boss/raiden/hazard/vfx_charge',
    ])
    write("vfx_charge",['scoreboard players set @s rdWind 2']+[
        f'execute if score @s rdShape matches {s} if score #rdChargeFrame rd matches {p} run {modelset(f"charge_{s}_{p}")}'
        for s in SHAPES for p in (0,1)
    ])
    write("warning",['# Warning display persists; no repeated particle burst or entity allocation.'])
    for shape in SHAPES:
        write(f"warning/s{shape}",['# Mesh: rlk:raiden/fx_hazard/warning_'+str(shape)])
    write("strike",[
        'scoreboard players operation #rdVfxOwner rd = @s rdHId',
        f'execute as {owned} if score @s rdVId = #rdVfxOwner rd run function rlk:boss/raiden/hazard/vfx_strike',
        'playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.50 1.25 0.2',
        'execute if score @s rdShape matches 4..8 run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.60 1.35 0.25',
        'execute if score @s rdShape matches 12 run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.55 1.5 0.25',
        'function rlk:boss/raiden/hazard/hit',
    ])
    write("vfx_strike",[
        '# Whole path flashes on the exact damage tick; this is instantaneous lightning.',
        'scoreboard players set @s rdWind 1',
        'scoreboard players set @s rdHAge -1',
    ]+[f'execute if score @s rdShape matches {s} run {modelset("strike_"+str(s))}' for s in SHAPES if s!=11])
    for phase in (1,2):
        write(f"vfx_flash_{phase}",[
            '# The whole area remains lit; only branch topology changes, not hit travel.',
        ]+[f'execute if score @s rdShape matches {s} run {modelset(f"strike_{s}_{phase}")}' for s in SHAPES if s!=11])
    write("vfx_after",[f'execute if score @s rdShape matches {s} run {modelset("after_"+str(s))}' for s in SHAPES if s!=11])
    write("vfx_fade",[f'execute if score @s rdShape matches {s} run {modelset("after_"+str(s)+"_fade")}' for s in SHAPES if s!=11])
    for shape in SHAPES:
        if shape!=11:
            write(f"strike/s{shape}",['# Strike mesh is selected by vfx_strike on the owning display.'])
    for frame in range(RING_FRAMES):
        write(f"ring/f{frame:02}",[
            f'# Exact ring radius {2+(RING_END-2)*frame/(RING_FRAMES-1):.6f}; visible band half-width0.7.',
            'scoreboard players operation #rdVfxOwner rd = @s rdHId',
            f'execute as {owned} if score @s rdVId = #rdVfxOwner rd run {modelset("ring_"+f"{frame:02}")}',
        ])
    write("ring_tick",[
        'scoreboard players operation #rdElapsed rd = @s rdHAge',
        'scoreboard players operation #rdElapsed rd -= @s rdWind',
        f'execute if score #rdElapsed rd matches {RING_FRAMES}.. run return run function rlk:boss/raiden/hazard/expire',
        f'execute unless score #rdElapsed rd matches 0..{RING_FRAMES-1} run return 0',
        '# Every damage radius receives its matching model in the same tick.',
        'function rlk:boss/raiden/hazard/ring_draw',
        'execute if score #rdElapsed rd matches 0 run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.35 1.6 0.2',
        'execute unless score @s rdHHit matches 1 run function rlk:boss/raiden/hazard/hit',
    ])
    write("vfx_world",[
        '# Call after hazard updates and from pause: removes canceled/orphan effects immediately.',
        f'execute as {owned} run function rlk:boss/raiden/hazard/vfx_tick',
    ])
    write("expire",[
        f'# Cancel the display and its parent together; the ring ends at frame{RING_FRAMES}.',
        'scoreboard players operation #rdVfxOwner rd = @s rdHId',
        f'execute as {owned} if score @s rdVId = #rdVfxOwner rd run kill @s',
        'kill @s',
    ])
    write("vfx_tick",[
        'scoreboard players operation #rdVfxOwner rd = @s rdVId',
        'scoreboard players set #rdVfxExists rd 0',
        'execute as @e[tag=rlk_rd_hazard] if score @s rdHId = #rdVfxOwner rd run scoreboard players set #rdVfxExists rd 1',
        'execute if score #rdVfxExists rd matches 0 run return run kill @s',
        'execute unless score @s rdWind matches 1 run return 0',
        'scoreboard players add @s rdHAge 1',
        'execute if score @s rdHAge matches 1 run function rlk:boss/raiden/hazard/vfx_flash_1',
        'execute if score @s rdHAge matches 2 run function rlk:boss/raiden/hazard/vfx_flash_2',
        'execute if score @s rdHAge matches 3 run function rlk:boss/raiden/hazard/vfx_after',
        'execute if score @s rdHAge matches 6 run function rlk:boss/raiden/hazard/vfx_fade',
        'execute if score @s rdHAge matches 9.. run kill @s',
    ])
    # The base generator owns the damage math and lifecycle. Attach creation
    # only after forward-axis caching, preserving its original command order.
    initpath=out/"init.mcfunction"
    original=initpath.read_text(encoding="utf-8")
    original=original.replace('function rlk:boss/raiden/hazard/warning\n',
                              'function rlk:boss/raiden/hazard/vfx_init\n')
    initpath.write_text(original,encoding="utf-8")
    tickpath=out/"tick_at.mcfunction"
    original=tickpath.read_text(encoding="utf-8")
    original=original.replace('run return run kill @s',
                              'run return run function rlk:boss/raiden/hazard/expire')
    original=original.replace('scoreboard players operation #rdMod rd = @s rdHAge',
                              'scoreboard players operation #rdUntil rd = @s rdWind\n'
                              'scoreboard players operation #rdUntil rd -= @s rdHAge\n'
                              'execute if score #rdUntil rd matches 1..4 run function rlk:boss/raiden/hazard/charge\n'
                              'scoreboard players operation #rdMod rd = @s rdHAge')
    tickpath.write_text(original,encoding="utf-8")
    print(f"Built {stats['models']} textured display meshes (largest {stats['maxname']}: {stats['max']} cards): 13 gradient telegraph decals, 26 charge frames, 36 strike frames, 24 afterglows, {RING_FRAMES} exact ring frames.")
