"""Display side of the Narukami hazard / FX kit v2 (plan rd/plan.md B.0, B.3, C.6, D.1; owner S1-KIT).

Called by build_raiden_hazards.py (build(ROOT, OUT)). Writes
  RP   assets/rlk/models/item/raiden/fx_hazard/*  + items/raiden/fx_hazard/*   (unit-size meshes, tintable)
  DP   boss/raiden/hazard/vis/*   hazard-bound visuals: decal, strike, travelling cards, small impacts
       boss/raiden/hazard/vfx_world + fx_*   the display clock (orphans, one-shot interpolation, countdown frames)
       boss/raiden/fx/*            D.1 cues (visual + vanilla sound recipe), fx/snd/*, fx/decal/* (state decals)

MESHES. Every mesh is unit-size and scaled per hazard by the display transformation (no per-size models):
  model coordinate = 8 + 16 * u for x and z (u in units: radius 1, or width 1 x length 1 along +z),
  model y = 8 + 16 * (blocks / yu): decals and travelling cards yu = 1, strike meshes yu = 8 (display scale y = yu).
  right_rotation [0,1,0,0] cancels the item flip, so model +z = the hazard's forward. Cards are flat (zero thickness),
  faces on both sides, shade off, tintindex 0: the item definition tints them with minecraft:custom_model_data
  (index 0, default white), which the frames use for flicker / residue / fade without extra models.
  Layer heights: decal 0.02 < strike area 0.03 < floor bolts 0.07+ (>= 0.02 apart, translucent sort by centroid).

DISPLAY CLOCK (vfx_world, every tick after the hazards):
  rlk_rd_hvis   bound to a hazard (decal, travelling cards, field crackle): it sits exactly on the hazard origin, so a
                visual with no hazard within 0.05 b is an orphan and is killed (pause / transform kill the markers).
  rlk_rd_fx     free-running timed card (strike visuals, cues, state decals): rdHLife counts down, killed at 0; strike
                frames by remaining life (raiden_kit.FLASH / AFTER_AT / FADE_AT).
  rlk_rd_fxa    one-shot interpolation: the tick after its summon, transformation := custom_data.to over custom_data.d
                ticks (travelling cards launch this way exactly on the hazard's launch tick; rings expand in).
"""
from pathlib import Path
import json
import math
import shutil
import sys

from build_raiden_fx_textures import catalogue, build_fx_textures, TEX_SUBDIR, NS, KIT_QEXT
from raiden_kit import (DECALS, DECAL_INTRO, STRIKES, STRIKE_YU, STRIKE_LIFE, SM_SWEEP, FLASH, AFTER_AT, AFTER_TINT, FADE_AT,
                        FADE_TINT, SOUNDS, SEG_DEG, KINDS)

FX = {c["name"] for c in catalogue()}
ALLOWED = (-45.0, -22.5, 0.0, 22.5, 45.0)
AXES = {"+x": (0, 1), "-x": (0, -1), "+y": (1, 1), "-y": (1, -1), "+z": (2, 1), "-z": (2, -1)}
FACE_PAIR = {0: ("east", "west"), 1: ("up", "down"), 2: ("south", "north")}
ABC = "abc"
H = "rlk:boss/raiden/hazard/"
F = "rlk:boss/raiden/fx/"
MODEL_NS = "rlk:raiden/fx_hazard/"
WHITE = 0xFFFFFF
SEG_CHORD = 2 * math.tan(math.radians(SEG_DEG / 2)) * 1.08      # chord / radius of one ring card (8 % overlap)


def face_corners(face, lo, hi):
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
    """Face uv [u1,v1,u2,v2] + rotation so that every corner shows fn(corner) (vanilla FaceInfo order)."""
    D = [fn(c) for c in face_corners(face, lo, hi)]
    for k in range(4):
        u = [D[(j + k) % 4] for j in range(4)]
        if (abs(u[0][1] - u[1][1]) < 1e-6 and abs(u[1][0] - u[2][0]) < 1e-6 and
                abs(u[2][1] - u[3][1]) < 1e-6 and abs(u[3][0] - u[0][0]) < 1e-6):
            return [round(u[0][0], 4), round(u[0][1], 4), round(u[2][0], 4), round(u[2][1], 4)], k * 90
    raise ValueError(f"no uv solution for {face}")


class Model:
    """Unit mesh: x/z in units (model 8 + 16 u), y in blocks / yu."""

    def __init__(self, yu=1.0):
        self.yu = yu
        self.textures = {}
        self.elements = []

    def var(self, name):
        assert name in FX, name
        tid = NS + name
        for k, v in self.textures.items():
            if v == tid:
                return k
        k = f"t{len(self.textures)}"
        self.textures[k] = tid
        return k

    def card(self, center, normal, uaxis, vaxis, su, sv, tex, angle=0.0, uv=(0, 0, 16, 16), origin=None):
        """Flat card centred on center = (x units, y blocks, z units), lying across `normal`; texture u runs from uv[0]
        at the -uaxis edge to uv[2] at the +uaxis edge (likewise v). su / sv are in units (y extents in blocks).
        `angle` turns it about +Y around `origin` (default its centre)."""
        n = "xyz".index(normal)
        ua, us = AXES[uaxis]
        va, vs = AXES[vaxis]
        assert len({n, ua, va}) == 3, (normal, uaxis, vaxis)
        scale = (16.0, 16.0 / self.yu, 16.0)
        c = [8 + center[i] * scale[i] for i in range(3)]
        half = [0.0, 0.0, 0.0]
        half[ua] = su * scale[ua] / 2
        half[va] = sv * scale[va] / 2
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
            spec = {"texture": "#" + var, "uv": fuv, "tintindex": 0}
            if rot:
                spec["rotation"] = rot
            faces[f] = spec
        el = {"from": lo, "to": hi, "shade": False, "faces": faces}
        if angle:
            assert angle in ALLOWED, angle
            o = c if origin is None else [8 + origin[i] * scale[i] for i in range(3)]
            el["rotation"] = {"origin": [round(v, 4) for v in o], "axis": "y", "angle": angle}
        self.elements.append(el)

    def json(self):
        tex = dict(self.textures)
        if tex:
            tex["particle"] = next(iter(self.textures.values()))
        return {"ambientocclusion": False, "gui_light": "front", "textures": tex, "elements": self.elements}


def heading(theta):
    """Direction theta (deg, from +z toward +x) -> (u axis along it, v axis across, element Y angle)."""
    for base, ua, va in ((0, "+z", "-x"), (90, "+x", "+z"), (180, "-z", "+x"), (-90, "-x", "-z")):
        a = (theta - base + 180) % 360 - 180
        for al in ALLOWED:
            if abs(a - al) < 1e-6:
                return ua, va, al
    return None


def polar(r, ang):
    return (r * math.sin(math.radians(ang)), r * math.cos(math.radians(ang)))


def strip(m, p0, p1, width, tex, y=0.06, wall=None, uv=(0, 0, 16, 16)):
    """Card along p0 -> p1 (x, z units; direction a multiple of 22.5 deg). wall=None: flat at height y (blocks),
    `width` units across; wall=(y0, y1) blocks: standing on the segment (texture v top -> bottom)."""
    dx, dz = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dz)
    theta = math.degrees(math.atan2(dx, dz))
    q = round(theta / 22.5) * 22.5
    assert abs(theta - q) < 1e-3, theta
    ua, va, ang = heading(q)
    cx, cz = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    if wall is None:
        m.card((cx, y, cz), "y", ua, va, L, width, tex, ang, uv)
    else:
        y0, y1 = wall
        m.card((cx, (y0 + y1) / 2, cz), "x" if ua in ("+z", "-z") else "z", ua, "-y", L, y1 - y0, tex, ang, uv)


def quarters(m, tex, y, ext=KIT_QEXT, r=1.0):
    """Quarter-texture circle (centre at texel 0,0), radius r units: 4 mirrored cards."""
    e = ext * r
    for sx in (1, -1):
        for sz in (1, -1):
            m.card((sx * e / 2, y, sz * e / 2), "y", "+x", "+z", e, e, tex, 0,
                   (0 if sx > 0 else 16, 0 if sz > 0 else 16, 16 if sx > 0 else 0, 16 if sz > 0 else 0))


def radial(m, size, tex, y, flip=False, x=0.0, z=0.0):
    m.card((x, y, z), "y", "+x", "+z", size, size, tex, 0, (16, 0, 0, 16) if flip else (0, 0, 16, 16))


def pillar(m, x, z, y0, height, width, texs, planes=4, split=2.4):
    """Crossed vertical cards (width in units, heights in blocks); tall ones are cut at y0 + split so the low part's
    centroid sorts after the floor cards."""
    spec = (("+z", "x", 0.0), ("+x", "z", 0.0), ("+z", "x", 45.0), ("+z", "x", -45.0))
    cut = y0 + split
    for k in range(planes):
        ua, normal, ang = spec[k]
        uv = (16, 0, 0, 16) if k % 2 else (0, 0, 16, 16)
        tex = texs[k % len(texs)]
        if height <= split + 1.0:
            m.card((x, y0 + height / 2, z), normal, ua, "-y", width, height, tex, ang, uv)
            continue
        vcut = 16 * (y0 + height - cut) / height
        m.card((x, (cut + y0 + height) / 2, z), normal, ua, "-y", width, y0 + height - cut, tex, ang, (uv[0], 0, uv[2], vcut))
        if k < 2:
            m.card((x, (y0 + cut) / 2, z), normal, ua, "-y", width, cut - y0, tex, ang, (uv[0], vcut, uv[2], 16))


def crescent(m, y, tex, theta=0.0, scale=1.0, crop=1.0, flip=False):
    """Blade-light crescent lying flat: pivot at the origin, bright edge radius `scale` units toward theta (a multiple
    of 22.5); crop < 1 keeps the central part (narrower arc)."""
    Hh = scale / 0.94
    base = round(theta / 90) * 90
    rest = theta - base
    ua_v = {0: ("+x", "-z"), 90: ("-z", "-x"), 180: ("-x", "+z"), -90: ("+z", "+x"), 270: ("+z", "+x")}[int(base) if base != -180 else 180]
    cx, cz = polar(Hh / 2, base)
    du = 8 * crop
    uv = (8 - du, 0, 8 + du, 16)
    if flip:
        uv = (uv[2], 0, uv[0], 16)
    m.card((cx, y, cz), "y", ua_v[0], ua_v[1], 2 * Hh * crop, Hh, tex, rest, uv, origin=(0, y, 0))


def bolts_radial(m, angles, r0, r1, width, y, texs):
    for i, a in enumerate(angles):
        strip(m, polar(r0, a), polar(r1, a), width, texs[i % len(texs)], y=y,
              uv=(16, 0, 0, 16) if i % 2 else (0, 0, 16, 16))


def ring_walls(m, r, y0, y1, texs, n=8):
    for i in range(n):
        a = 360 / n * i
        half = 180 / n
        p0, p1 = polar(r, a - half), polar(r, a + half)
        strip(m, p0, p1, 0, texs[i % len(texs)], wall=(y0, y1), uv=(16, 0, 0, 16) if i % 2 else (0, 0, 16, 16))


# --------------------------------------------------------------------------- meshes
def models():
    M = {}
    # ---- B.3 decals (yu 1; unit radius / unit band)
    for name, tex in (("dk_ring", "dk_ring"), ("dk_ring_s", "dk_ring_s"), ("dk_rings3", "dk_rings3"), ("dk_disc", "dk_disc")):
        m = Model()
        quarters(m, tex, 0.02)
        M[name] = m
    m = Model()
    m.card((0, 0.02, 0.5), "y", "+x", "+z", 1, 1, "dk_band")
    M["dk_band"] = m
    m = Model()
    radial(m, 2 / 0.9, "dk_pool", 0.02)
    M["dk_pool"] = m
    m = Model()
    quarters(m, "dk_ring_s", 0.02)
    ring_walls(m, 1.0, 0.0, 0.32, ["rim_crackle_a", "rim_crackle_b"])
    M["dk_aura"] = m
    m = Model()
    radial(m, 2 / 0.9, "dk_pool", 0.02)
    quarters(m, "dk_ring_s", 0.04)
    M["dk_stagger"] = m
    m = Model()
    radial(m, 2.0, "dk_tint", 0.05)
    M["dk_tint"] = m

    # ---- strike meshes (yu 8)
    def burst(bolt):
        m = Model(STRIKE_YU)
        radial(m, 2 / 0.92, "shockwave", 0.03)
        radial(m, 1.0, "flash", 0.05, flip=bolt)
        bolts_radial(m, [45 * i for i in range(8)], 0.08, 0.95, 0.16, 0.07, ["bolt_a", "bolt_b"])
        if bolt:
            pillar(m, 0, 0, 0.0, 10.0, 0.5, ["vbolt_a", "vbolt_b", "vbolt_c"], 4)
        else:
            pillar(m, 0, 0, 0.0, 2.2, 0.4, ["vbolt_b", "vbolt_c"], 2)
        return m
    M["st_burst"] = burst(False)
    M["st_bolt"] = burst(True)
    m = Model(STRIKE_YU)
    radial(m, 2 / 0.88 * 0.95, "scorch", 0.03)
    bolts_radial(m, [45 * i + 22.5 for i in range(0, 8, 2)], 0.1, 0.85, 0.18, 0.07, ["bolt_after_c"])
    M["st_burst_af"] = m
    for name, half in (("st_arc45", 45), ("st_arc72", 72), ("st_arc112", 112.5), ("st_arc180", 180)):
        m = Model(STRIKE_YU)
        if half == 45:
            crescent(m, 1.0, "crescent_b", crop=0.75)
            crescent(m, 0.4, "crescent_a", scale=0.85, crop=0.75, flip=True)
        elif half == 72:
            crescent(m, 1.0, "crescent_b")
            crescent(m, 0.4, "crescent_a", scale=0.85, flip=True)
        elif half == 112.5:
            for i, t in enumerate((-45.0, 45.0)):
                crescent(m, 1.0 + 0.04 * i, "crescent_b", theta=t)
            crescent(m, 0.4, "crescent_a", scale=0.85, flip=True)
        else:
            for i, t in enumerate((0, 90, 180, -90)):
                crescent(m, 0.9 + 0.04 * i, "crescent_b" if i % 2 == 0 else "crescent_a", theta=t)
        rays = [a for a in (-112.5, -90, -67.5, -45, -22.5, 0, 22.5, 45, 67.5, 90, 112.5) if abs(a) <= half - 10] \
            if half < 180 else [45 * i for i in range(8)]
        rays = rays[::2] if len(rays) > 5 else rays
        bolts_radial(m, rays, 0.1, 0.92, 0.12, 0.07, ["bolt_a", "bolt_c"])
        M[name] = m
    m = Model(STRIKE_YU)                                         # rect: x in [-0.5, 0.5], z in [0, 1]
    strip(m, (0, 0.02), (0, 0.98), 0.55, "bolt_a", y=0.07)
    strip(m, (0, 0.03), (0, 0.97), 0, "blade_a", wall=(0.3, 2.0))
    strip(m, (0, 0.02), (0, 0.98), 1.0, "slash_wave", y=1.1)
    M["st_slash"] = m
    m = Model(STRIKE_YU)
    strip(m, (0, 0.02), (0, 0.98), 0.6, "scorch_strip", y=0.03)
    strip(m, (0, 0.04), (0, 0.96), 0.45, "bolt_after_c", y=0.07)
    M["st_slash_af"] = m
    m = Model(STRIKE_YU)                                         # 단절 slam: wall of light along the band
    strip(m, (0, 0.01), (0, 0.99), 0.6, "bolt_b", y=0.07)
    for x in (-0.42, 0.42):
        strip(m, (x, 0.01), (x, 0.99), 0, "slash_wave", wall=(0.0, 4.5))
    for z in (0.15, 0.4, 0.65, 0.9):
        pillar(m, 0, z, 0.0, 7.0, 0.5, ["vbolt_a", "vbolt_b"], 2)
    M["st_wall"] = m
    m = Model(STRIKE_YU)                                         # field: cracked glowing floor + low crackle rim
    radial(m, 2 / 0.88, "scorch", 0.03)
    ring_walls(m, 1.0, 0.0, 0.5, ["rim_crackle_a", "rim_crackle_c"])
    bolts_radial(m, [0, 90, 180, 270], 0.15, 0.9, 0.14, 0.07, ["bolt_c", "bolt_a"])
    M["st_field"] = m

    # ---- travelling cards (yu 1)
    for v, (cr, flip) in enumerate((("crackle_a", False), ("crackle_b", True))):
        m = Model()                                              # x along the chord, z in [-1, 0] (front at 0)
        m.card((0, 0.05, -0.5), "y", "+x", "-z", 1, 1, "tr_band", 0, (16, 0, 0, 16) if flip else (0, 0, 16, 16))
        m.card((0, 0.35, -0.12), "z", "+x", "-y", 1, 0.7, cr, 0, (16, 0, 0, 16) if flip else (0, 0, 16, 16))
        M["tr_seg_" + "ab"[v]] = m
    m = Model()                                                  # slab: wall at z 0, footprint z in [-1, 0]; y unit = height
    m.card((0, 0.5, 0), "z", "+x", "-y", 1, 1, "crackle_a")
    m.card((0, 0.5, -0.02), "z", "-y", "+x", 1, 0.9, "obj_wave_band")
    m.card((0, 0.02, -0.5), "y", "+x", "-z", 1, 1, "tr_band")
    M["tr_slab"] = m
    m = Model()                                                  # orb: flat electric disc radius 1
    radial(m, 2.5, "chakra_a", 0.0)
    radial(m, 1.0, "orb_core", 0.02)
    m.card((0, 0, 0), "z", "+x", "-y", 1.6, 1.6, "chakra_b")
    M["tr_orb"] = m

    # ---- cue cards (fx/*)
    m = Model()
    m.card((0, 0, 0), "z", "+x", "-y", 1.0, 1.0, "glint")      # billboard star, 1 b
    M["fx_star"] = m
    m = Model()
    radial(m, 2 / 0.92, "shockwave", 0.03)
    M["fx_ring"] = m
    m = Model()
    m.card((0, 0, 0), "z", "+x", "-y", 2.5, 2.5, "chakra_b")   # billboard hoop / halo / twirl ring, radius 1
    M["fx_hoop"] = m
    m = Model(4)
    radial(m, 2 / 0.92, "shockwave", 0.05)
    for k, ang in enumerate((0.0, 45.0, -45.0)):
        m.card((0, 2.0, 0), "x", "+z", "-y", 2.0, 4.0, "flash", ang)
    m.card((0, 2.0, 0), "z", "+x", "-y", 2.0, 4.0, "flash")
    m.card((0, 2.0, 0), "z", "+x", "-y", 2.0, 4.0, "chakra_b")
    M["fx_dome"] = m
    m = Model(8)
    pillar(m, 0, 0, 0.0, 12.0, 2.2, ["pillar_a", "pillar_b"], 4)
    M["fx_pillar"] = m
    m = Model(8)
    pillar(m, 0, 0, 0.0, 11.0, 1.0, ["vbolt_a", "vbolt_b", "vbolt_c"], 4)
    radial(m, 1.2, "flash", 0.05)
    M["fx_bolt"] = m
    m = Model(4)                                                 # crystal line: x in [-0.5, 0.5], z in [0, 1]
    for i in range(9):
        z = 0.06 + 0.11 * i
        x = (-0.2, 0.15, -0.05, 0.25, -0.25, 0.05, 0.2, -0.15, 0.0)[i]
        h = (1.6, 2.3, 1.2, 2.0, 1.5, 2.6, 1.4, 2.1, 1.8)[i]
        m.card((x, h / 2, z), "x", "+z", "-y", 0.09, h, "rig_shard", (22.5, -22.5, 0.0)[i % 3])
        m.card((x, h / 2, z), "z", "+x", "-y", 0.18, h, "rig_shard")
    M["fx_crystal_line"] = m
    m = Model(4)
    for i in range(12):
        x, z = polar(1.0, 30 * i)
        h = (1.5, 2.2, 1.2, 1.9)[i % 4]
        m.card((x, h / 2, z), "x", "+z", "-y", 0.16, h, "rig_shard", (22.5, -22.5, 45.0, 0.0)[i % 4])
        m.card((x, h / 2, z), "z", "+x", "-y", 0.16, h, "rig_shard")
    M["fx_crystal_ring"] = m
    m = Model()
    crescent(m, 0.0, "crescent_a")
    M["fx_crescent"] = m
    m = Model()
    m.card((0, 0, 0), "z", "-y", "+x", 2.4, 0.3, "rift_a")     # billboard dark vertical line (u along the height)
    M["fx_line"] = m
    m = Model()
    m.card((0, 0, 0), "z", "+x", "-y", 2.0, 2.0, "impact_sparks")
    m.card((0, 0, 0), "z", "+x", "-y", 1.4, 1.4, "flash")
    M["fx_burst"] = m
    m = Model()
    m.card((0, 0, 0), "z", "+x", "-y", 1.0, 1.0, "flash")
    M["fx_flash"] = m
    return M


TINTED_DEFAULT = WHITE


def save_models(rp, M):
    modeldir = rp / "assets/rlk/models/item/raiden/fx_hazard"
    itemdir = rp / "assets/rlk/items/raiden/fx_hazard"
    for d in (modeldir, itemdir):
        if d.exists():
            shutil.rmtree(d)        # this generator owns fx_hazard (drops the 165 v1 frames)
        d.mkdir(parents=True, exist_ok=True)
    for name, m in M.items():
        (modeldir / (name + ".json")).write_text(json.dumps(m.json(), separators=(",", ":")) + "\n", encoding="utf-8")
        node = {"type": "minecraft:model", "model": "rlk:item/raiden/fx_hazard/" + name,
                "tints": [{"type": "minecraft:custom_model_data", "index": 0, "default": TINTED_DEFAULT}]}
        (itemdir / (name + ".json")).write_text(json.dumps({"model": node}, separators=(",", ":")) + "\n", encoding="utf-8")
    return len(M), max(len(m.elements) for m in M.values())


# --------------------------------------------------------------------------- datapack side
def nbt_tf(tx="0", ty="0", tz="0", sx="1", sy="1", sz="1", lr="[0f,0f,0f,1f]"):
    return (f'{{translation:[{tx}f,{ty}f,{tz}f],left_rotation:{lr},scale:[{sx}f,{sy}f,{sz}f],'
            f'right_rotation:[0f,1f,0f,0f]}}')


def display(tags, model, tf, *, custom=None, color=WHITE, billboard="fixed", tp_dur=0, view=2):
    comps = f'"minecraft:item_model":"{model}","minecraft:custom_model_data":{{colors:[{color}]}}'
    if custom:
        comps += f',"minecraft:custom_data":{custom}'
    tl = ",".join(f'"{t}"' for t in tags)
    return (f'summon minecraft:item_display ~ ~ ~ {{Tags:[{tl}],billboard:"{billboard}",item_display:"none",'
            f'view_range:{view}f,width:0f,height:0f,shadow_radius:0f,brightness:{{block:15,sky:15}},interpolation_duration:0,'
            f'teleport_duration:{tp_dur},transformation:{tf},item:{{id:"minecraft:paper",count:1,components:{{{comps}}}}}}}')


def build(root, out):
    rp = root.parent / "resourcepack"
    if "--resourcepack" in sys.argv:
        rp = Path(sys.argv[sys.argv.index("--resourcepack") + 1])
    from build_raiden_materials import build_materials
    build_materials(rp)
    texdir = rp / TEX_SUBDIR
    if not all((texdir / (n + ".png")).exists() for n in FX):
        build_fx_textures(rp)
    M = models()
    nmodels, maxel = save_models(rp, M)
    fxdir = root / "data/rlk/function/boss/raiden/fx"
    if fxdir.exists():
        shutil.rmtree(fxdir)

    def write(name, lines, base=out):
        path = base / (name + ".mcfunction")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def wfx(name, lines):
        write(name, lines, fxdir)

    def mid(name):
        assert name in M, name
        return MODEL_NS + name

    OWN = 'scoreboard players operation #rdOwner rd = @s rdHId'
    VNEW = '@e[tag=rlk_rd_vnew,limit=1]'
    # ---------------------------------------------------------------- the display clock
    write("vfx_world", [
        '# Every tick after the hazards (and from pause / transform after killing them).',
        f'execute if entity @e[tag=rlk_rd_hvis,limit=1] run function {H}vis/orphans',
        f'execute if entity @e[tag=rlk_rd_fx,limit=1] run function {H}fx_tick',
        f'execute if entity @e[tag=rlk_rd_fxa,tag=!rlk_rd_fxnew,limit=1] as @e[tag=rlk_rd_fxa,tag=!rlk_rd_fxnew] run function {H}fx_anim',
        'tag @e[tag=rlk_rd_fxnew] remove rlk_rd_fxnew',
    ])
    write("vis/orphans", [
        '# A hazard-bound display sits exactly on its hazard origin; one without a hazard there is an orphan.',
        'tag @e[tag=rlk_rd_hvis] add rlk_rd_orph',
        'execute as @e[tag=rlk_rd_hazard] at @s run tag @e[tag=rlk_rd_orph,distance=..0.05] remove rlk_rd_orph',
        'kill @e[tag=rlk_rd_orph]',
    ])
    write("fx_anim", [
        '# One-shot interpolation, the tick after the summon (travelling cards: exactly the launch tick).',
        'data modify entity @s transformation set from entity @s item.components."minecraft:custom_data".to',
        'data modify entity @s interpolation_duration set from entity @s item.components."minecraft:custom_data".d',
        'data modify entity @s start_interpolation set value 0',
        'tag @s remove rlk_rd_fxa',
    ])
    cm = 'item.components."minecraft:custom_model_data".colors[0]'
    write("fx_tick", [
        '# Timed cards: countdown (not on their summon tick), kill at 0, strike frames by remaining life.',
        'scoreboard players remove @e[tag=rlk_rd_fx,tag=!rlk_rd_fxnew] rdHLife 1',
        'kill @e[tag=rlk_rd_fx,scores={rdHLife=..0}]',
    ] + [f'execute as @e[tag=rlk_rd_strike,tag=rlk_rd_fx,scores={{rdHLife={life}}}] run data modify entity @s {cm} set value {col}'
         for life, col in sorted(FLASH.items(), reverse=True)] + [
        f'execute as @e[tag=rlk_rd_strike,tag=rlk_rd_fx,scores={{rdHLife={AFTER_AT}}}] run function {H}fx_after',
        f'execute as @e[tag=rlk_rd_fx,scores={{rdHLife={FADE_AT}}}] run function {H}fx_fade',
    ])
    write("fx_after", [
        'data modify entity @s item.components."minecraft:item_model" set from entity @s item.components."minecraft:custom_data".after',
        f'data modify entity @s {cm} set value {AFTER_TINT}',
    ])
    write("fx_fade", [f'data modify entity @s {cm} set from entity @s item.components."minecraft:custom_data".fade'])

    # ---------------------------------------------------------------- hazard-bound visuals
    # decal: storage rlk:rd v {m, kt, sx, sz, sx0, sz0, tz, d}
    dec = ['# @s = hazard at its origin (rotated as it). The B.3 decal, sized to the hazard; rings open with an expand.',
           'data modify storage rlk:rd v set value {tz:0f,d:1}']
    for dk, (kt, model, sizing) in DECALS.items():
        dec.append(f'execute if score @s rdHDk matches {dk} run function {H}vis/dk/{dk}')
        write(f"vis/dk/{dk}", [f'data modify storage rlk:rd v.m set value "{model}"',
                               f'data modify storage rlk:rd v.kt set value "{kt}"',
                               f'data modify storage rlk:rd v.d set value {DECAL_INTRO.get(dk, 1)}'])
    dec += [
        '# radius: annulus = r (B); every other radial kind = A. band: width 2B x length A (rect / to_wall), offset C.',
        'scoreboard players operation #rdSx rd = @s rdHA',
        'execute if score @s rdHK matches 2 run scoreboard players operation #rdSx rd = @s rdHB',
        'scoreboard players operation #rdSz rd = #rdSx rd',
        f'execute if score @s rdHDk matches 5 run function {H}vis/decal_band',
        'execute store result storage rlk:rd v.sx float 0.001 run scoreboard players get #rdSx rd',
        'execute store result storage rlk:rd v.sz float 0.001 run scoreboard players get #rdSz rd',
        'execute store result storage rlk:rd v.sx0 float 0.001 run scoreboard players get #rdSx rd',
        'execute store result storage rlk:rd v.sz0 float 0.001 run scoreboard players get #rdSz rd',
    ] + [f'execute if score @s rdHDk matches {dk} store result storage rlk:rd v.sx0 float 0.00025 run scoreboard players get #rdSx rd'
         for dk in DECAL_INTRO] + [
        f'execute if score @s rdHDk matches {dk} store result storage rlk:rd v.sz0 float 0.00025 run scoreboard players get #rdSz rd'
        for dk in DECAL_INTRO] + [
        f'function {H}vis/decal_summon with storage rlk:rd v',
        f'tp {VNEW} ~ ~ ~ ~ 0',
        f'scoreboard players operation {VNEW} rdVId = @s rdHId',
        'tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew',
    ]
    write("vis/decal", dec)
    write("vis/decal_band", [
        'scoreboard players operation #rdSx rd = @s rdHB',
        'scoreboard players operation #rdSx rd += @s rdHB',
        'scoreboard players operation #rdSz rd = @s rdHA',
        'execute if score @s rdHK matches 3..4 store result storage rlk:rd v.tz float 0.001 run scoreboard players get @s rdHC',
    ])
    write("vis/decal_summon", ['$' + display(
        ["rlk_rd_hvis", "rlk_rd_decal", "rlk_rd_decal_$(kt)", "rlk_raiden_aux", "rlk_room", "rlk_rd_vnew", "rlk_rd_fxa",
         "rlk_rd_fxnew"], MODEL_NS + "$(m)", nbt_tf(tz="$(tz)", sx="$(sx0)", sz="$(sz0)"),
        custom='{d:$(d),to:' + nbt_tf(tz="$(tz)", sx="$(sx)", sz="$(sz)") + '}', tp_dur=1)])
    write("vis/decal_off", [OWN, 'execute as @e[tag=rlk_rd_decal,distance=..0.05] if score @s rdVId = #rdOwner rd run kill @s'])

    # strike: storage rlk:rd v {m, a, sx, sz, tz, sx0, sz0, d}
    st = ['# @s = hazard at its origin. The strike visual of a static hazard, sized to it (life 10: flash, flicker,',
          '# residue, fade). Field crackle stays bound to the hazard instead. rdHSm (rd-sync) starts it where the swing',
          '# came from: swept in from one side, dropped from above, run out from the origin or grown up from the floor.',
          'data modify storage rlk:rd v set value {tz:0f,d:1,ty0:0f,sy0:%sf,lr0:"[0f,0f,0f,1f]"}' % STRIKE_YU]
    for sv, (_, hot, after) in STRIKES.items():
        st.append(f'execute if score @s rdHSv matches {sv} run function {H}vis/sv/{sv}')
        write(f"vis/sv/{sv}", [f'data modify storage rlk:rd v.m set value "{hot}"',
                               f'data modify storage rlk:rd v.a set value "{after}"'])
    st += [
        'scoreboard players operation #rdSx rd = @s rdHA',
        'execute if score @s rdHK matches 2 run scoreboard players operation #rdSx rd = @s rdHB',
        'scoreboard players operation #rdSz rd = #rdSx rd',
        f'execute if score @s rdHK matches 3..4 run function {H}vis/decal_band',
        'execute store result storage rlk:rd v.sx float 0.001 run scoreboard players get #rdSx rd',
        'execute store result storage rlk:rd v.sz float 0.001 run scoreboard players get #rdSz rd',
        'execute store result storage rlk:rd v.sx0 float 0.00075 run scoreboard players get #rdSx rd',
        'execute store result storage rlk:rd v.sz0 float 0.00075 run scoreboard players get #rdSz rd',
        'execute if score @s rdHK matches 3..4 run function %svis/strike_full' % H,
        f'execute if score @s rdHSm matches 1.. run function {H}vis/strike_motion',
        f'execute if score @s rdHK matches {KINDS["field"]} run function {H}vis/field_summon with storage rlk:rd v',
        f'execute unless score @s rdHK matches {KINDS["field"]} run function {H}vis/strike_summon with storage rlk:rd v',
        f'tp {VNEW} ~ ~ ~ ~ 0',
        f'scoreboard players set {VNEW} rdHLife {STRIKE_LIFE}',
        f'scoreboard players operation {VNEW} rdVId = @s rdHId',
        'tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew',
    ]
    write("vis/strike", st)
    write("vis/strike_full", ['# rect / to_wall: no expand (a slash is instant along its whole length)',
                              'data modify storage rlk:rd v.sx0 set from storage rlk:rd v.sx',
                              'data modify storage rlk:rd v.sz0 set from storage rlk:rd v.sz'])
    half = math.radians(SM_SWEEP) / 2
    qs = {1: f'[0f,{math.sin(half):.5f}f,0f,{math.cos(half):.5f}f]', 2: f'[0f,{-math.sin(half):.5f}f,0f,{math.cos(half):.5f}f]'}
    write("vis/strike_motion", [
        '# rdHSm 1 / 2: the strike starts turned SM_SWEEP deg toward her left / right (model +X = her left) and sweeps',
        '# into place behind the blade; 3 drops 1 b; 4 runs out from the origin (rect / to_wall); 5 grows up from the floor.',
        f"execute if score @s rdHSm matches 1 run data modify storage rlk:rd v.lr0 set value \"{qs[1]}\"",
        f"execute if score @s rdHSm matches 2 run data modify storage rlk:rd v.lr0 set value \"{qs[2]}\"",
        'execute if score @s rdHSm matches 3 run data modify storage rlk:rd v.ty0 set value 1.0f',
        'execute if score @s rdHSm matches 4 store result storage rlk:rd v.sz0 float 0.00015 run scoreboard players get #rdSz rd',
        f'execute if score @s rdHSm matches 5 run data modify storage rlk:rd v.sy0 set value {STRIKE_YU * 0.15:.2f}f',
    ])
    write("vis/strike_summon", ['$' + display(
        ["rlk_rd_fx", "rlk_rd_strike", "rlk_rd_fxa", "rlk_rd_fxnew", "rlk_raiden_aux", "rlk_room", "rlk_rd_vnew"],
        MODEL_NS + "$(m)", nbt_tf(ty="$(ty0)", tz="$(tz)", sx="$(sx0)", sy="$(sy0)", sz="$(sz0)", lr="$(lr0)"),
        custom='{d:3,after:"' + MODEL_NS + '$(a)",fade:' + str(FADE_TINT) + ',to:' +
               nbt_tf(tz="$(tz)", sx="$(sx)", sy=str(STRIKE_YU), sz="$(sz)") + '}')])
    write("vis/field_summon", ['$' + display(
        ["rlk_rd_hvis", "rlk_rd_strike", "rlk_raiden_aux", "rlk_room", "rlk_rd_vnew"],
        MODEL_NS + "$(m)", nbt_tf(sx="$(sx)", sy=str(STRIKE_YU), sz="$(sz)"))])

    # travelling cards
    tr = ['# @s = travelling hazard, one tick before its launch: summon its cards at the start state; the display clock',
          '# gives them their ONE interpolation (to the end state over F ticks) on the launch tick.',
          'execute store result storage rlk:rd v.d int 1 run scoreboard players get @s rdHF',
          'scoreboard players operation #rdR1 rd = @s rdHB',
          'scoreboard players operation #rdR1 rd *= @s rdHF',
          'scoreboard players operation #rdR1 rd /= #rdK1000 rd',
          'scoreboard players operation #rdR1 rd += @s rdHA',
          'execute store result storage rlk:rd v.tz0 float 0.001 run scoreboard players get @s rdHA',
          'execute store result storage rlk:rd v.tz1 float 0.001 run scoreboard players get #rdR1 rd',
          f'execute if score @s rdHK matches {KINDS["sweep"]} run function {H}vis/travel_sweep',
          f'execute if score @s rdHK matches {KINDS["slab"]} run function {H}vis/travel_slab',
          f'execute if score @s rdHK matches {KINDS["orb"]} run function {H}vis/travel_orb',
          'scoreboard players operation @e[tag=rlk_rd_vown] rdVId = @s rdHId',
          'tag @e[tag=rlk_rd_vown] remove rlk_rd_vown']
    write("vis/travel", tr)
    chord_k = round(SEG_CHORD, 6)
    write("vis/travel_sweep", [
        f'execute store result storage rlk:rd v.cx0 float {chord_k / 1000:.9f} run scoreboard players get @s rdHA',
        f'execute store result storage rlk:rd v.cx1 float {chord_k / 1000:.9f} run scoreboard players get #rdR1 rd',
        'execute store result storage rlk:rd v.bz float 0.001 run scoreboard players get @s rdHC',
    ] + [f'execute if score @s rdHSv matches {n} run function {H}vis/seg/n{n}' for n in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 24]])
    for n in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 24]:
        ks = list(range(24)) if n == 24 else list(range(-(n // 2), n // 2 + 1))
        lines = [f'# {n} ring cards, {SEG_DEG} deg apart, centred on the yaw.']
        for k in ks:
            lines.append(f'execute rotated ~{k * SEG_DEG} 0 run function {H}vis/seg_{"ab"[k % 2]} with storage rlk:rd v')
        write(f"vis/seg/n{n}", lines)
    for v in "ab":
        write(f"vis/seg_{v}", ['$' + display(
            ["rlk_rd_hvis", "rlk_rd_strike", "rlk_rd_trv", "rlk_rd_fxa", "rlk_rd_fxnew", "rlk_raiden_aux", "rlk_room",
             "rlk_rd_vnew"], mid("tr_seg_" + v), nbt_tf(tz="$(tz0)", sx="$(cx0)", sz="$(bz)"),
            custom='{d:$(d),to:' + nbt_tf(tz="$(tz1)", sx="$(cx1)", sz="$(bz)") + '}'),
            f'tp {VNEW} ~ ~ ~ ~ 0', f'tag {VNEW} add rlk_rd_vown', 'tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew'])
    write("vis/travel_slab", [
        'scoreboard players operation #rdSx rd = @s rdHC',
        'scoreboard players operation #rdSx rd += @s rdHC',
        'execute store result storage rlk:rd v.sx float 0.001 run scoreboard players get #rdSx rd',
        'execute store result storage rlk:rd v.sy float 0.001 run scoreboard players get @s rdHE',
        'execute store result storage rlk:rd v.sz float 0.001 run scoreboard players get @s rdHD',
        f'function {H}vis/slab_summon with storage rlk:rd v',
        f'tp {VNEW} ~ ~ ~ ~ 0', f'tag {VNEW} add rlk_rd_vown', 'tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew'])
    write("vis/slab_summon", ['$' + display(
        ["rlk_rd_hvis", "rlk_rd_strike", "rlk_rd_trv", "rlk_rd_fxa", "rlk_rd_fxnew", "rlk_raiden_aux", "rlk_room",
         "rlk_rd_vnew"], mid("tr_slab"), nbt_tf(tz="$(tz0)", sx="$(sx)", sy="$(sy)", sz="$(sz)"),
        custom='{d:$(d),to:' + nbt_tf(tz="$(tz1)", sx="$(sx)", sy="$(sy)", sz="$(sz)") + '}')])
    write("vis/travel_orb", [
        'execute store result storage rlk:rd v.sx float 0.001 run scoreboard players get @s rdHC',
        'execute store result storage rlk:rd v.ty float 0.001 run scoreboard players get @s rdHE',
        f'function {H}vis/orb_summon with storage rlk:rd v',
        f'tp {VNEW} ~ ~ ~ ~ 0', f'tag {VNEW} add rlk_rd_vown', 'tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew'])
    write("vis/orb_summon", ['$' + display(
        ["rlk_rd_hvis", "rlk_rd_strike", "rlk_rd_trv", "rlk_rd_fxa", "rlk_rd_fxnew", "rlk_raiden_aux", "rlk_room",
         "rlk_rd_vnew"], mid("tr_orb"), nbt_tf(ty="$(ty)", tz="$(tz0)", sx="$(sx)", sz="$(sx)"),
        custom='{d:$(d),to:' + nbt_tf(ty="$(ty)", tz="$(tz1)", sx="$(sx)", sz="$(sx)") + '}')])
    write("vis/impact", [
        '# At the body: a travelling / follow / field hazard reached the player (dodged or not).',
        display(["rlk_rd_fx", "rlk_rd_strike", "rlk_rd_fxnew", "rlk_raiden_aux", "rlk_room", "rlk_rd_vnew"],
                mid("fx_burst"), nbt_tf(ty="1", sx="1.4", sy="1.4", sz="1.4"), billboard="center",
                custom='{after:"' + mid("fx_flash") + f'",fade:{FADE_TINT}}}'),
        f'scoreboard players set {VNEW} rdHLife 6',
        'tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew',
        'playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.35 1.8 0.1',
    ])

    # ---------------------------------------------------------------- D.1 cues (fx/<cue>) and sounds (fx/snd/<cue>)
    def snd_lines(cue):
        return [f'playsound minecraft:{ev} hostile @a[tag=player] ~ ~ ~ {vol} {pit} 0.25' for ev, vol, pit in SOUNDS[cue]]

    for cue in SOUNDS:
        wfx(f"snd/{cue}", [f'# D.1 sound recipe "{cue}" (vanilla only).'] + snd_lines(cue))

    def card(model, life, *, y=0.0, s0=(1, 1, 1), s1=None, d=4, color=WHITE, billboard="fixed", fade=None):
        tags = ["rlk_rd_fx", "rlk_rd_fxnew", "rlk_raiden_aux", "rlk_room", "rlk_rd_vnew"] + (["rlk_rd_fxa"] if s1 else [])
        custom = []
        if s1:
            custom.append(f'd:{d},to:' + nbt_tf(ty=f"{y:g}", sx=f"{s1[0]:g}", sy=f"{s1[1]:g}", sz=f"{s1[2]:g}"))
        if fade is not None:
            custom.append(f'fade:{fade}')
        return [display(tags, mid(model), nbt_tf(ty=f"{y:g}", sx=f"{s0[0]:g}", sy=f"{s0[1]:g}", sz=f"{s0[2]:g}"),
                        custom='{' + ','.join(custom) + '}' if custom else None, color=color, billboard=billboard),
                f'tp {VNEW} ~ ~ ~ ~ 0', f'scoreboard players set {VNEW} rdHLife {life}',
                'tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew']

    DARK, GOLD, CYAN, PINK, PALE = 0x4A3270, 0xFFD27A, 0x9FE6FF, 0xFFA8E8, 0xE8E0FF
    CUES = {
        'star': card('fx_star', 8, s0=(0.4, 0.4, 0.4), s1=(1.3, 1.3, 1.3), d=2, billboard="center")
        + card('fx_ring', 8, s0=(0.2, 1, 0.2), s1=(1, 1, 1), d=4),
        'blink_out': card('fx_flash', 5, y=1.0, s0=(1.6, 2.2, 1.6), s1=(0.3, 2.6, 0.3), d=4, color=0xB48CFF, billboard="center"),
        'blink_in': card('fx_flash', 5, y=1.0, s0=(0.3, 2.6, 0.3), s1=(1.4, 1.8, 1.4), d=3, color=0xB48CFF, billboard="center"),
        'switch_hoop': card('fx_hoop', 10, y=1.2, s0=(1.25, 1.25, 1.25), color=DARK, billboard="center"),
        'switch_burst': card('fx_dome', 10, s0=(1, 4, 1), s1=(6, 4, 6), d=4)
        + card('fx_ring', 10, s0=(1, 1, 1), s1=(6.5, 1, 6.5), d=5),
        'bolt': card('fx_bolt', 7, s0=(1.2, 8, 1.2)) + card('fx_ring', 8, s0=(0.5, 1, 0.5), s1=(3, 1, 3), d=4),
        'bolt_big': card('fx_bolt', 8, s0=(2.4, 8, 2.4)) + card('fx_ring', 10, s0=(1, 1, 1), s1=(6, 1, 6), d=5),
        'crystal': card('fx_crystal_ring', 14, s0=(2.5, 4, 2.5), s1=(3, 4, 3), d=3),
        'parry': card('fx_crescent', 6, y=1.0, s0=(1.2, 1, 1.2), color=GOLD),
        'counter_cue': card('fx_line', 10, y=1.2, s0=(1, 1, 1), color=0x24123C, billboard="center"),
        'guard_shatter': card('fx_burst', 8, y=1.2, s0=(1.5, 1.5, 1.5), s1=(3.2, 3.2, 3.2), d=4, billboard="center")
        + card('fx_pillar', 100, s0=(1.6, 8, 1.6), color=GOLD),
        'eye_spawn': card('fx_pillar', 10, s0=(0.7, 8, 0.7), color=CYAN),
        'eye_break': card('fx_burst', 10, s0=(1, 1, 1), s1=(3.4, 3.4, 3.4), d=4, color=0xFFD6F4, billboard="center"),
        'eye_blast': card('fx_dome', 10, s0=(2, 4, 2), s1=(5, 4, 5), d=4, color=0xD8B8FF),
        'musou_slash': card('fx_crescent', 12, y=1.6, s0=(4, 1, 4), s1=(19, 1, 19), d=6, color=PALE)
        + card('fx_flash', 8, y=2.0, s0=(6, 6, 6), billboard="center"),
        'glaive_throw': card('fx_pillar', 6, s0=(0.5, 8, 0.5), color=PINK),
        'bomb': card('fx_burst', 8, y=1.0, s0=(1.2, 1.2, 1.2), s1=(3.5, 3.5, 3.5), d=3, billboard="center")
        + card('dk_pool', 14, s0=(1, 1, 1), s1=(3.5, 1, 3.5), d=4),
        'iai_charge': card('fx_ring', 8, y=1.0, s0=(1.2, 1, 1.2), s1=(0.2, 1, 0.2), d=8, color=PALE),
        'danjeol_halo': card('fx_hoop', 14, y=2.6, s0=(0.6, 0.6, 0.6), s1=(1.4, 1.4, 1.4), d=4, color=PALE, billboard="center"),
        'danjeol_column': card('fx_pillar', 30, s0=(1.4, 8, 1.4), color=0xC8A8FF),
        'clap_star': card('fx_star', 14, s0=(0.5, 0.5, 0.5), s1=(1.6, 1.6, 1.6), d=3, color=0xFFE8FF, billboard="center"),
        'shadow_palm': card('dk_pool', 12, s0=(2, 1, 2), s1=(5, 1, 5), d=4)
        + card('fx_burst', 6, y=0.8, s0=(2.5, 2.5, 2.5), color=0xB070FF, billboard="center"),
        'vajra_pulse': card('fx_flash', 4, y=3.6, s0=(1.4, 1.4, 1.4), billboard="center"),
        'mangeop_dome': card('fx_ring', 8, s0=(1, 1, 1), s1=(8, 1, 8), d=8, color=0xBFE8FF),
        'mangeop_slash': card('fx_crescent', 8, y=2.5, s0=(6, 1, 6), s1=(24, 1, 24), d=6, color=PALE)
        + card('fx_flash', 6, y=2.5, s0=(10, 10, 10), billboard="center"),
        'transform_burst': card('fx_dome', 12, s0=(1, 4, 1), s1=(7, 4, 7), d=5),
    }
    for cue in SOUNDS:
        wfx(cue, [f'# D.1 cue "{cue}": visual (if any) + sound recipe. Run it at the cue spot.'] +
            CUES.get(cue, []) + [f'function {F}snd/{cue}'])
    # cues with a run-time size or life (macro)
    tw = card('fx_hoop', 0, y=1.8, s0=(0.75, 0.75, 0.75), color=0xF2E8FF, billboard="center")
    wfx("twirl", ['# Polearm twirl: the bright vertical ring (1.5 b) for {life} ticks; call fx/snd/twirl_beat every 6 t.',
                  tw[0], tw[1], f'$scoreboard players set {VNEW} rdHLife $(life)', tw[3], f'function {F}snd/twirl'])
    eg = card('fx_dome', 0, s0=(1, 4, 1), color=CYAN)
    wfx("eye_glow", ['# Cyan dome glow (danger) over a surviving eye: {r} blocks, {life} ticks.',
                     '$' + eg[0].replace('scale:[1f,4f,1f]', 'scale:[$(r)f,4f,$(r)f]'), eg[1],
                     f'$scoreboard players set {VNEW} rdHLife $(life)', eg[3], f'function {F}snd/eye_glow'])
    cl = card('fx_crystal_line', 0, s0=(1.6, 4, 1))
    wfx("crystal_line", ['# Crystal wall along the yaw: {len} blocks long, 1.6 wide (판결의 검, 26 hit 2).',
                         '$' + cl[0].replace('scale:[1.6f,4f,1f]', 'scale:[1.6f,4f,$(len)f]'), cl[1],
                         f'scoreboard players set {VNEW} rdHLife 16', cl[3], f'function {F}snd/crystal'])
    cr = card('fx_crystal_ring', 0, s0=(1, 4, 1))
    wfx("crystal_ring", ['# Crystal spikes on a circle of radius {r} (수천수만의 염원, transformation).',
                         '$' + cr[0].replace('scale:[1f,4f,1f]', 'scale:[$(r)f,4f,$(r)f]'), cr[1],
                         f'scoreboard players set {VNEW} rdHLife 16', cr[3], f'function {F}snd/crystal'])
    # state decals (not hazards) and the field tint
    for dk, (kt, model, sizing) in DECALS.items():
        c = card(model, 0, s0=(1, 1, 1))
        summon = c[0].replace('"rlk_rd_fx",', f'"rlk_rd_fx","rlk_rd_sdecal","rlk_rd_sdecal_{kt}",')
        summon = summon.replace('scale:[1f,1f,1f]', 'scale:[$(sx)f,1f,$(sz)f]')
        wfx(f"decal/d{dk}", [f'# State decal {kt} ({model}): {{sx, sz}} blocks, {{life}} ticks (99999 = until killed).',
                             '$' + summon, c[1], f'$scoreboard players set {VNEW} rdHLife $(life)', c[3]])
    c = card('dk_tint', 0, s0=(24.6, 1, 24.6))
    wfx("decal/tint", ['# Whole-field tint (time stop, 만겁): a uniform 35 % violet over the arena floor (r 24.6: its edge is under the wall), {life} ticks.',
                       '# Run it at the arena centre.',
                       c[0].replace('"rlk_rd_fx",', '"rlk_rd_fx","rlk_rd_sdecal","rlk_rd_sdecal_tint",'), c[1],
                       f'$scoreboard players set {VNEW} rdHLife $(life)', c[3]])
    wfx("musou_dark", ['# Time-stop darkening: the field tint for {life} ticks + the sonic charge. Run at the arena centre.',
                       f'$function {F}decal/tint {{life:$(life)}}', f'function {F}snd/musou_dark'])
    wfx("mangeop_tint", ['# 만겁 arena tint for {life} ticks. Run at the arena centre.',
                         f'$function {F}decal/tint {{life:$(life)}}', f'function {F}snd/mangeop_tint'])
    print(f"Built {nmodels} unit display meshes (largest {maxel} cards), {len(SOUNDS)} sound recipes, "
          f"{len(CUES) + 6} visual cues.")
