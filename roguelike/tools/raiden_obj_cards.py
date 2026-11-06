"""Flat textured VFX cards for the Narukami object, orb and blink generators.

Shared by build_raiden_object_vfx.py, build_raiden_orb.py and build_raiden_movement.py.
Every element is a zero-thickness card with a face on both sides ("shade": false)
showing a painted gradient sprite of build_raiden_fx_textures.py (rlk:raiden/fxg/*),
so nothing is built from stair-stepped cubes or flat colour swatches any more.

Frame: all three generators summon their displays with right_rotation [0,1,0,0],
which cancels the item renderer's 180 degree turn, so model axes are the display's
local axes: +x = the owner's left (screen right when facing it), +y = up,
+z = the owner's forward. model = 8 + local * 16 / scale.

Rules kept by Model.card (from the texture library's catalogue):
  * from/to stay within -16..32, element rotations are single-axis 0/+-22.5/+-45
    about the card's own centre;
  * the face uv is solved per face with the vanilla vertex order and uv-rotation
    rule, so texture u/v follow the requested local axes on both sides;
  * translucent quads are sorted by centroid and write depth in vanilla, so callers
    keep overlapping cards' halos tight and stack layers >= 0.02 block apart.
"""
from pathlib import Path
import json
import math

NS = "rlk:raiden/fxg/"
TEX_SUBDIR = "assets/rlk/textures/raiden/fxg"
ALLOWED = (-45.0, -22.5, 0.0, 22.5, 45.0)
AXES = {"+x": (0, 1), "-x": (0, -1), "+y": (1, 1), "-y": (1, -1), "+z": (2, 1), "-z": (2, -1)}
FACE_PAIR = {0: ("east", "west"), 1: ("up", "down"), 2: ("south", "north")}
FULL = (0, 0, 16, 16)
MIRROR_U = (16, 0, 0, 16)


def fx_names():
    """Sprite names of the texture library (imported lazily: painting is not triggered)."""
    from build_raiden_fx_textures import catalogue
    return {c["name"] for c in catalogue()}


def ensure_textures(rp, names):
    """Paint the library into `rp` when any sprite this generator uses is missing."""
    texdir = Path(rp) / TEX_SUBDIR
    if not all((texdir / (n + ".png")).exists() for n in names):
        from build_raiden_fx_textures import build_fx_textures
        build_fx_textures(rp)


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


def heading(theta):
    """Horizontal direction theta (deg, from +z toward +x) -> (unrotated axis, Y angle)."""
    for base, axis in ((0, "+z"), (90, "+x"), (180, "-z"), (-90, "-x")):
        a = (theta - base + 180) % 360 - 180
        for al in ALLOWED:
            if abs(a - al) < 1e-6:
                return axis, al
    raise ValueError(f"direction {theta} is not a multiple of 22.5 degrees")


def perp(axis):
    """Horizontal axis 90 degrees to the right (toward +x from +z) of `axis`."""
    return {"+z": "+x", "+x": "-z", "-z": "-x", "-x": "+z"}[axis]


class Model:
    def __init__(self, scale, known=None):
        self.scale = scale
        self.known = known
        self.textures = {}
        self.elements = []
        self.tint = None

    def var(self, name):
        tid = name if ":" in name else NS + name
        if self.known is not None and ":" not in name:
            assert name in self.known, name
        for k, v in self.textures.items():
            if v == tid:
                return k
        k = f"t{len(self.textures)}"
        self.textures[k] = tid
        return k

    def card(self, center, normal, uaxis, vaxis, su, sv, tex, uv=FULL, rot=None, tint=False):
        """Card centred on `center` (local blocks) lying across `normal` ('x'|'y'|'z').
        Texture u runs from uv[0] at the -uaxis edge to uv[2] at the +uaxis edge (likewise
        v). rot=(axis, angle) turns the card about its own centre (right-handed, degrees)."""
        n = "xyz".index(normal)
        ua, us = AXES[uaxis]
        va, vs = AXES[vaxis]
        assert len({n, ua, va}) == 3, (normal, uaxis, vaxis)
        k = 16.0 / self.scale
        c = [8 + v * k for v in center]
        half = [0.0, 0.0, 0.0]
        half[ua] = su * k / 2
        half[va] = sv * k / 2
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
            fuv, r = solve_uv(f, lo, hi, fn)
            spec = {"texture": "#" + var, "uv": fuv}
            if r:
                spec["rotation"] = r
            if tint:
                spec["tintindex"] = 0
            faces[f] = spec
        el = {"from": lo, "to": hi, "shade": False, "faces": faces}
        if rot and rot[1]:
            axis, angle = rot
            assert axis in "xyz" and angle in ALLOWED, rot
            el["rotation"] = {"origin": [round(v, 4) for v in c], "axis": axis, "angle": angle}
        self.elements.append(el)

    # ------------------------------------------------------------------ helpers
    def anchored(self, anchor, point, normal, uaxis, vaxis, su, sv, tex, uv=FULL, rot=None, tint=False):
        """Card placed so that texture point anchor=(a, b) (fractions 0..1 of the card from
        its -uaxis / -vaxis edges) lands on local `point` after the rotation `rot`."""
        du = [0.0, 0.0, 0.0]
        ua, us = AXES[uaxis]
        va, vs = AXES[vaxis]
        du[ua] += (anchor[0] - 0.5) * su * us
        du[va] += (anchor[1] - 0.5) * sv * vs
        if rot and rot[1]:
            du = rotate(du, *rot)
        center = [point[i] - du[i] for i in range(3)]
        self.card(center, normal, uaxis, vaxis, su, sv, tex, uv, rot, tint)
        return center

    def vcard(self, center, theta, su, sv, tex, uv=FULL, tint=False):
        """Vertical card whose texture u points along horizontal direction theta (deg from
        +z toward +x, multiple of 22.5) and whose texture v runs top -> bottom."""
        axis, ang = heading(theta)
        normal = "x" if axis in ("+z", "-z") else "z"
        self.card(center, normal, axis, "-y", su, sv, tex, uv, ("y", ang), tint)

    def hcard(self, center, theta, su, sv, tex, uv=FULL, tint=False):
        """Horizontal card: texture u along direction theta, texture v along theta + 90
        (to the right of u seen from above), lying at center[1]."""
        axis, ang = heading(theta)
        self.card(center, "y", axis, perp(axis), su, sv, tex, uv, ("y", ang), tint)

    def crossed(self, center, size, tex, planes=4, uv=FULL, flip=False, tint=False, sv=None):
        """Radial sprite on 2-4 crossed vertical planes (z-facing, x-facing, two diagonals)."""
        sv = size if sv is None else sv
        for k, theta in enumerate((90.0, 0.0, 45.0, 135.0)[:planes]):
            u = uv if (k + flip) % 2 == 0 else (uv[2], uv[1], uv[0], uv[3])
            self.vcard(center, theta, size, sv, tex, u, tint)

    def json(self):
        tex = dict(self.textures)
        if tex:
            tex["particle"] = next(iter(self.textures.values()))
        return {"ambientocclusion": False, "textures": tex, "elements": self.elements}


def save(rp, folder, name, model):
    """Write models/item/raiden/<folder>/<name>.json and items/raiden/<folder>/<name>.json."""
    root = Path(rp) / "assets/rlk"
    p = root / "models/item/raiden" / folder / (name + ".json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(model.json(), separators=(",", ":")) + "\n", encoding="utf-8")
    node = {"type": "minecraft:model", "model": f"rlk:item/raiden/{folder}/{name}"}
    if model.tint is not None:
        node["tints"] = [{"type": "minecraft:constant", "value": model.tint}]
    p = root / "items/raiden" / folder / (name + ".json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"model": node}, separators=(",", ":")) + "\n", encoding="utf-8")
    return len(model.elements)


def rotate(p, axis, angle):
    """Right-handed rotation of local vector p about +axis by angle degrees (vanilla element rotation)."""
    a = math.radians(angle)
    c, s = math.cos(a), math.sin(a)
    x, y, z = p
    if axis == "x":
        return [x, y * c - z * s, y * s + z * c]
    if axis == "y":
        return [x * c + z * s, y, -x * s + z * c]
    return [x * c - y * s, x * s + y * c, z]


def polar(r, theta, y=0.0):
    """Local point at radius r, direction theta (deg from +z toward +x)."""
    t = math.radians(theta)
    return (r * math.sin(t), y, r * math.cos(t))
