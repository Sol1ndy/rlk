#!/usr/bin/env python3
"""Navia's gold Geo VFX cards: painted sprites, flat item models and the rlk:fx/nv engine.

Roses, starbursts and crescent ribbons read badly as dust particles, so these shapes are
short-lived `item_display` cards (plan D7). This tool owns, and regenerates on every run:

  resource pack  assets/rlk/textures/navia_fx/<kind>.png   procedural sprites (stdlib only)
                 assets/rlk/models/item/navia_fx/<kind>.json one zero-thickness card
                 assets/rlk/items/navia_fx/<kind>.json       item definition
                 assets/minecraft/atlases/items.json         adds rlk:navia_fx/* (merges)
  datapack       data/rlk/function/fx/nv/**                  the card engine (owner tag rlk_nvfx)

Hand-maintained hooks (one line each, outside this tool): `function rlk:fx/nv/world` in
rlk:tick, `function rlk:fx/nv/init` in rlk:load, `function rlk:fx/nv/clear` in
rlk:run/field_clear. Cards also carry rlk_room, so room/clear, room/wipe and uninstall
remove them with the room.

Display frame. Every card is summoned with right_rotation identity; the item renderer's
own 180-degree turn about Y is baked into the model coordinates instead, so the display's
local axes are the summoning frame's: +x = left, +y = up, +z = forward. That keeps
right_rotation free for the spin. "face" kinds lie in the local XY plane (they face
forward, or the camera with billboard "center"); the "flat" crescent lies in the local XZ
plane with its arc bulging forward. Painters draw in card coordinates (a, b): +a is the
local -x (the player's right, i.e. screen right seen from behind or from above), +b is up
(face) or forward (flat). Texture u follows +a and v follows -b on both faces, so the
picture keeps one 3D orientation and is mirrored only when seen from the other side.

Run: python3 tools/build_navia_fx_cards.py --resourcepack <unpacked RP> [--datapack <dp>]
     (--datapack defaults to the datapack that contains this tool).
Other generators can import card_call() to write card commands.
"""
from pathlib import Path
import argparse
import json
import math
import struct
import zlib

HERE = Path(__file__).resolve().parent
NS_TEX = "rlk:navia_fx/"
FN = "rlk:fx/nv/"
TAG = "rlk_nvfx"
CAP = 48            # live cards; further spawns are skipped until some expire

# ----------------------------------------------------------------------------- colours


def hexc(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


WHITE = (1.0, 1.0, 1.0)
WARM = hexc("#FFFDF0")      # warm white highlight
CORE = hexc("#FFF3C4")      # pale gold core
GOLD = hexc("#F6D57A")      # gold body
DEEP = hexc("#E9B949")      # deep gold
AMBER = hexc("#D39A35")     # shadowed gold
YELLOW = hexc("#FFE27A")    # saturated lit gold (slash body)
OUTLINE = hexc("#9E6C31")   # dark gold outline (rose emblem, crystal edges)


def mix(a, b, t):
    t = 0.0 if t < 0 else 1.0 if t > 1 else t
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def ramp(stops, t):
    """Piecewise-linear colour ramp; stops = [(t, rgb), ...] ascending."""
    if t <= stops[0][0]:
        return stops[0][1]
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t <= t1:
            return mix(c0, c1, (t - t0) / (t1 - t0))
    return stops[-1][1]


def smooth(e0, e1, x):
    t = (x - e0) / (e1 - e0)
    t = 0.0 if t < 0 else 1.0 if t > 1 else t
    return t * t * (3 - 2 * t)


def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


HOT = [(0.0, AMBER), (0.25, DEEP), (0.5, GOLD), (0.75, CORE), (0.92, WARM), (1.0, WHITE)]

# ----------------------------------------------------------------------------- sprites
# Each painter takes card coordinates (a, b) and returns (r, g, b, alpha), straight alpha.


def paint_rose(a, b):
    """Stylised flat gold rose emblem: three rings of petals, a swirled bud, two leaves,
    dark-gold outlines (v7 dash rose, v5 FX-1/FX-7)."""
    cx, cy = 0.0, 0.14
    sw = 0.055                                   # outline width (card units, 64 px -> ~1.8 px)
    x, y = a - cx, b - cy
    light = 0.10 * (y - x) / 1.4                 # soft top-left light
    # bud swirl strokes (drawn over the bud)
    rb = math.hypot(x, y - 0.02)
    if rb < 0.19:
        for (ox, oy, r, a0, a1) in ((0.025, 0.03, 0.115, 200, 470), (-0.012, 0.055, 0.058, 20, 300)):
            d = abs(math.hypot(x - ox, y - oy) - r)
            if d < sw * 0.5:
                ang = math.degrees(math.atan2(y - oy, x - ox)) % 360
                if any(a0 <= ang + k <= a1 for k in (0, 360)):
                    return OUTLINE + (1.0,)
        if rb < 0.19 - sw:
            t = rb / 0.19
            return mix(ramp([(0, DEEP), (0.55, GOLD), (1, CORE)], 1 - t * 0.6), WARM, light) + (1.0,)
        return OUTLINE + (1.0,)
    # petal rings, front to back: (count, ring radius, petal radius, start angle)
    rings = ((3, 0.12, 0.215, 30.0), (5, 0.25, 0.27, 136.0), (5, 0.41, 0.355, 100.0))
    for depth, (n, dist, pr, a0) in enumerate(rings):
        best = None
        for k in range(n):
            th = math.radians(a0 + 360.0 * k / n)
            px, py = dist * math.cos(th), dist * math.sin(th)
            d = math.hypot(x - px, y - py)
            if d < pr and (best is None or d - pr < best[0]):
                best = (d - pr, d / pr)
        if best is not None:
            if best[0] > -sw:
                return OUTLINE + (1.0,)
            t = best[1]
            base = ramp([(0, DEEP), (0.55, GOLD), (0.9, CORE), (1, WARM)], t)
            base = mix(base, AMBER, 0.12 * depth * (1 - t))
            return mix(base, WARM, max(0.0, light)) + (1.0,)
    # two leaves behind the head, pointing down-outward
    for sx in (-1, 1):
        lx, ly = 0.40 * sx, -0.60
        ang = math.radians(-90 + 52 * sx)
        ux, uy = math.cos(ang), math.sin(ang)
        s = (x + cx - lx) * ux + (y + cy - ly) * uy      # along the leaf (card coords)
        t = -(x + cx - lx) * uy + (y + cy - ly) * ux     # across
        hl, hw = 0.34, 0.15
        if abs(s) < hl:
            m = hw * (1 - (s / hl) ** 2) - abs(t)
            if m > 0:
                if m < sw * 0.8:
                    return OUTLINE + (1.0,)
                if abs(t) < 0.018 and s < hl * 0.75:
                    return CORE + (1.0,)                  # midrib
                return mix(DEEP, GOLD, 0.5 + 0.5 * t / hw * sx) + (1.0,)
    return (0.0, 0.0, 0.0, 0.0)


def paint_star(a, b):
    """Four-point star glint with two faint diagonal rays and a hot core."""
    r = math.hypot(a, b)

    def ray(u, v, length, width):
        f = 1 - abs(u) / length
        if f <= 0:
            return 0.0
        return f ** 1.4 * math.exp(-(v / (width * f + 0.012)) ** 2)
    i = max(ray(a, b, 0.98, 0.075), ray(b, a, 0.98, 0.075))
    d1, d2 = (a + b) / math.sqrt(2), (a - b) / math.sqrt(2)
    i = max(i, 0.55 * ray(d1, d2, 0.42, 0.05), 0.55 * ray(d2, d1, 0.42, 0.05))
    i = max(i, math.exp(-(r / 0.13) ** 2))
    i = max(i, 0.22 * math.exp(-(r / 0.22) ** 2))
    col = ramp([(0, YELLOW), (0.35, CORE), (0.7, WARM), (1, WHITE)], i)
    return col + (clamp01(i * 1.3),)


BURST_SPIKES = (   # (angle deg from +b toward +a, length, half-width at the root)
    (8, 0.98, 0.115), (98, 0.94, 0.11), (188, 0.97, 0.115), (278, 0.92, 0.11),
    (52, 0.70, 0.085), (143, 0.66, 0.08), (233, 0.72, 0.085), (322, 0.64, 0.08),
    (30, 0.46, 0.06), (120, 0.50, 0.06), (208, 0.44, 0.06), (300, 0.48, 0.06),
    (75, 0.36, 0.05), (255, 0.38, 0.05))


def paint_burst(a, b):
    """White-gold starburst flash: uneven sharp radial spikes, white core, warm fringe
    (v2 hit stars, v3 FX-3/FX-E1, v4 FX6)."""
    r = math.hypot(a, b)
    phi = math.atan2(a, b)
    inside = 0.0
    edge = 1.0
    for deg, length, w0 in BURST_SPIKES:
        if r >= length:
            continue
        dphi = (phi - math.radians(deg) + math.pi) % (2 * math.pi) - math.pi
        if abs(dphi) > math.pi / 2:
            continue
        perp = r * math.sin(abs(dphi))
        w = w0 * (1 - r / length) + 0.004
        if perp < w:
            inside = 1.0
            edge = min(edge, (w - perp) / w)
    core = r < 0.21
    if core or inside:
        t = 1 - r
        col = ramp([(0, DEEP), (0.25, GOLD), (0.45, CORE), (0.7, WARM), (0.82, WHITE)], t)
        if not core and edge < 0.22:
            col = mix(col, DEEP, (0.22 - edge) / 0.22 * 0.55)
        return col + (1.0,)
    haze = 0.36 * math.exp(-(r / 0.36) ** 2)
    return mix(CORE, WARM, haze) + (haze,)


CRESCENT_SPAN = 80.0      # half-angle of the arc, degrees either side of forward


def paint_crescent(a, b):
    """Thick tapered crescent slash ribbon lying in the swing plane. Circle centre = the
    card origin (the swing pivot), outer radius 0.97 of the card's half-width. The head
    (leading end, thick and bright) is at -a (the player's left), the tail fades toward +a,
    so roll 0 is a right-to-left swing (v2 N1, v3 FX-2/FX-12)."""
    r = math.hypot(a, b)
    if r < 0.45 or r > 1.0:
        return (0.0, 0.0, 0.0, 0.0)
    phi = math.degrees(math.atan2(a, b))              # 0 forward, + toward +a (right)
    s = (CRESCENT_SPAN - phi) / (2 * CRESCENT_SPAN)   # 0 tail (right) .. 1 head (left)
    if s <= 0 or s >= 1:
        return (0.0, 0.0, 0.0, 0.0)
    ro = 0.97 - 0.035 * (1 - s)                       # outer edge (blade tip path)
    thick = 0.36 * math.sin(math.pi * s ** 1.55) ** 0.75
    ri = ro - thick
    if r > ro or r < ri or thick < 0.01:
        return (0.0, 0.0, 0.0, 0.0)
    w = (ro - r) / thick                              # 0 outer edge .. 1 inner edge
    col = ramp([(0, WHITE), (0.1, WARM), (0.22, CORE), (0.42, YELLOW), (0.75, GOLD), (1, DEEP)], w)
    col = mix(col, DEEP, 0.45 * (1 - s) ** 2)          # tail warms toward deep gold
    streak = 0.10 * math.sin(w * 29.0 + 1.3) + 0.06 * math.sin(w * 53.0)
    col = mix(col, CORE, max(0.0, streak))
    alpha = (1 - 0.6 * smooth(0.35, 1.0, w)) * (0.22 + 0.78 * smooth(0.0, 0.6, s))
    alpha *= 0.93 + 0.07 * math.cos(w * 23.0)
    return col + (clamp01(alpha * 1.05),)


def paint_petal(a, b):
    """Small gold petal / leaf flake: teardrop with a pale midrib and a darker rim."""
    t = (b + 0.92) / 1.84                              # 0 at the stem tip .. 1 at the round end
    if t <= 0 or t >= 1:
        return (0.0, 0.0, 0.0, 0.0)
    half = 0.50 * math.sin(math.pi * t ** 0.75) ** 0.9
    x = a - 0.10 * math.sin(math.pi * t)              # slight curl
    m = half - abs(x)
    if m <= 0:
        return (0.0, 0.0, 0.0, 0.0)
    if m < 0.07:
        return mix(DEEP, AMBER, 0.6) + (1.0,)
    if abs(x) < 0.05 and 0.12 < t < 0.85:
        return CORE + (1.0,)
    col = mix(ramp([(0, DEEP), (0.6, GOLD), (1, CORE)], t), WARM, 0.25 * clamp01(-x / max(half, 1e-6)))
    return col + (1.0,)


def paint_shard(a, b):
    """Geo crystal spike: a long thin diamond, pale lit facet on the left, deep gold facet
    on the right, white ridge, dark-gold edges, warm glow at the root (v3 FX-6, v4 FX7)."""
    if b <= 0 or b >= 1:
        return (0.0, 0.0, 0.0, 0.0)
    wide = 0.20
    half = 0.92 * (b / wide if b < wide else (1 - b) / (1 - wide))
    m = half - abs(a)
    if m <= 0:
        return (0.0, 0.0, 0.0, 0.0)
    if m < 0.16:
        return OUTLINE + (1.0,)
    if abs(a) < 0.08:
        return mix(WARM, WHITE, 1 - b) + (1.0,)
    lit = ramp([(0, CORE), (0.7, GOLD), (1, CORE)], b) if a < 0 else ramp([(0, DEEP), (0.6, AMBER), (1, GOLD)], b)
    if b < 0.12:
        lit = mix(lit, WARM, (0.12 - b) / 0.12 * 0.7)
    return lit + (1.0,)


def paint_ring(a, b):
    """Thin white-gold ring with a gold glow band and one brighter leading sector
    (v3 FX-4/FX-7 hit and orbit rings, v5 FX-4, v6 shell-impact arc)."""
    r = math.hypot(a, b)
    R = 0.86
    d = abs(r - R)
    phi = math.atan2(a, b)
    lead = 0.55 + 0.45 * max(0.0, math.cos(phi - 0.6)) ** 3
    core = math.exp(-(d / 0.022) ** 2)
    glow = 0.75 * math.exp(-(d / 0.075) ** 2)
    i = max(core, glow) * (0.65 + 0.35 * lead)
    col = ramp([(0, DEEP), (0.4, GOLD), (0.75, CORE), (0.95, WHITE)], max(core * lead, glow * 0.6))
    return col + (clamp01(i * 1.15),)


def paint_glow(a, b):
    """Soft gold glow disc for flashes, ground glow and hand charge."""
    r = math.hypot(a, b)
    if r >= 1:
        return (0.0, 0.0, 0.0, 0.0)
    al = 0.95 * (1 - r) ** 1.3
    return ramp([(0, YELLOW), (0.5, CORE), (0.85, WARM), (1, WHITE)], 1 - r) + (al,)


# kind -> plane, texture size (w, h), card extent in blocks at scale 1 (a0, a1, b0, b1),
# painter coordinate box (a0, a1, b0, b1), painter, one-line description
KINDS = {
    "rose":     ("face", (64, 64),   (-0.5, 0.5, -0.5, 0.5),   (-1, 1, -1, 1), paint_rose,
                 "gold rose emblem"),
    "star":     ("face", (64, 64),   (-0.5, 0.5, -0.5, 0.5),   (-1, 1, -1, 1), paint_star,
                 "four-point star glint"),
    "burst":    ("face", (128, 128), (-0.5, 0.5, -0.5, 0.5),   (-1, 1, -1, 1), paint_burst,
                 "white-gold starburst flash"),
    "crescent": ("flat", (256, 128), (-0.5, 0.5, 0.0, 0.5),    (-1, 1, 0, 1),  paint_crescent,
                 "thick crescent slash ribbon (swing plane)"),
    "petal":    ("face", (32, 32),   (-0.5, 0.5, -0.5, 0.5),   (-1, 1, -1, 1), paint_petal,
                 "gold petal flake"),
    "shard":    ("face", (32, 128),  (-0.125, 0.125, 0.0, 1.0), (-1, 1, 0, 1), paint_shard,
                 "geo crystal spike (pivot at its root)"),
    "ring":     ("face", (128, 128), (-0.5, 0.5, -0.5, 0.5),   (-1, 1, -1, 1), paint_ring,
                 "thin ring / shockwave arc"),
    "glow":     ("face", (64, 64),   (-0.5, 0.5, -0.5, 0.5),   (-1, 1, -1, 1), paint_glow,
                 "soft gold glow disc"),
}

# ----------------------------------------------------------------------------- textures


def render(kind, ss=4):
    plane, (w, h), _ext, (a0, a1, b0, b1), fn, _ = KINDS[kind]
    px = bytearray()
    for j in range(h):
        px.append(0)                                   # PNG filter: none
        for i in range(w):
            ar = ag = ab = aa = 0.0
            for sj in range(ss):
                v = (j + (sj + 0.5) / ss) / h
                bb = b1 - v * (b1 - b0)
                for si in range(ss):
                    u = (i + (si + 0.5) / ss) / w
                    r, g, bl, al = fn(a0 + u * (a1 - a0), bb)
                    ar += r * al
                    ag += g * al
                    ab += bl * al
                    aa += al
            n = ss * ss
            alpha = aa / n
            if alpha < 0.1:                            # vanilla item shaders discard < 0.1
                px += bytes((0, 0, 0, 0))
                continue
            px += bytes((round(255 * clamp01(ar / aa)), round(255 * clamp01(ag / aa)),
                         round(255 * clamp01(ab / aa)), round(255 * clamp01(alpha))))
    return w, h, bytes(px)


def png_bytes(w, h, raw):
    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data +
                struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))

# ----------------------------------------------------------------------------- models


def model_json(kind):
    """One zero-thickness double-sided card. Display-local p (blocks) is written at model
    m = (8 - 16 px, 8 + 16 py, 8 - 16 pz): the item renderer's 180-degree turn about Y
    maps it back to p. Card coordinate +a is local -x, i.e. model +x."""
    plane, _size, (a0, a1, b0, b1), _box, _fn, _ = KINDS[kind]
    x0, x1 = 8 + 16 * a0, 8 + 16 * a1
    if plane == "face":
        y0, y1 = 8 + 16 * b0, 8 + 16 * b1
        frm, to = [x0, y0, 8], [x1, y1, 8]
        # u along +x (= +a) and v along -y (top = +b) on both faces
        faces = {"south": {"uv": [0, 0, 16, 16], "texture": "#0"},
                 "north": {"uv": [16, 0, 0, 16], "texture": "#0"}}
    else:
        z_near, z_far = 8 - 16 * b0, 8 - 16 * b1       # forward (+b) is model -z
        frm, to = [x0, 8, z_far], [x1, 8, z_near]
        # u along +x (= +a), v along +z (top of the texture = far end = +b)
        faces = {"up": {"uv": [0, 0, 16, 16], "texture": "#0"},
                 "down": {"uv": [0, 16, 16, 0], "texture": "#0"}}
    for v in frm + to:
        assert -16 <= v <= 32, (kind, frm, to)
    tex = NS_TEX + kind
    return {"ambientocclusion": False, "textures": {"0": tex, "particle": tex},
            "elements": [{"from": [round(v, 4) for v in frm], "to": [round(v, 4) for v in to],
                          "shade": False, "faces": faces}]}


def build_resourcepack(rp):
    rp = Path(rp)
    root = rp / "assets/rlk"
    for sub in ("textures/navia_fx", "models/item/navia_fx", "items/navia_fx"):
        d = root / sub
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob("*"):
            if old.stem not in KINDS:
                old.unlink()
    for kind in KINDS:
        w, h, raw = render(kind)
        (root / "textures/navia_fx" / f"{kind}.png").write_bytes(png_bytes(w, h, raw))
        (root / "models/item/navia_fx" / f"{kind}.json").write_text(
            json.dumps(model_json(kind), separators=(",", ":")) + "\n", encoding="utf-8")
        item = {"model": {"type": "minecraft:model", "model": f"rlk:item/navia_fx/{kind}"}}
        (root / "items/navia_fx" / f"{kind}.json").write_text(
            json.dumps(item, separators=(",", ":")) + "\n", encoding="utf-8")
    atlaspath = rp / "assets/minecraft/atlases/items.json"
    atlas = json.loads(atlaspath.read_text(encoding="utf-8")) if atlaspath.exists() else {"sources": []}
    atlas["sources"] = [s for s in atlas["sources"]
                        if not str(s.get("resource", "")).startswith(NS_TEX) or
                        s["resource"][len(NS_TEX):] in KINDS]
    have = {s.get("sprite", s.get("resource")) for s in atlas["sources"]}
    for kind in KINDS:
        if NS_TEX + kind not in have:
            atlas["sources"].append({"type": "minecraft:single", "resource": NS_TEX + kind})
    atlaspath.parent.mkdir(parents=True, exist_ok=True)
    atlaspath.write_text(json.dumps(atlas, indent=2) + "\n", encoding="utf-8")

# ----------------------------------------------------------------------------- datapack


def num(v):
    return f"{v:.4f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


def card_call(kind, pos, rot="~ ~", bb="fixed", roll=0, spin=0, s0=0.0, s1=1.0,
              move=(0.0, 0.0, 0.0), life=8, fade=0):
    """The mcfunction line that spawns one card (see scratchpad cards_api.md / README).
    pos: "^x ^y ^z" (or ~/absolute), rot: rotation for fixed cards ("~ ~" = the executor's),
    roll/spin: integer degrees, s0/s1: size in blocks, move: end offset in blocks (display
    frame), life/fade: ticks."""
    assert kind in KINDS and bb in ("fixed", "center", "vertical", "horizontal")
    mv = ",".join(num(float(v)) + "f" for v in move)
    return (f'function {FN}card {{kind:"{kind}",pos:"{pos}",rot:"{rot}",bb:"{bb}",'
            f'roll:{int(roll)},spin:{int(spin)},s0:{num(float(s0))},s1:{num(float(s1))},'
            f'move:"{mv}",life:{int(life)},fade:{int(fade)}}}')


# preset name -> (comment, card_call kwargs without pos); presets take {pos:"..."}
PRESETS = {
    "rose_trail": ("Dash rose behind the hips (billboard), rises a little and shrinks out.",
                   dict(kind="rose", bb="center", roll=-8, spin=24, s0=0.12, s1=0.46,
                        move=(0, 0.22, 0), life=14, fade=5)),
    "rose_pop": ("Small rose that pops at a canopy rim or on a hit (billboard).",
                 dict(kind="rose", bb="center", spin=-30, s0=0.05, s1=0.24, life=10, fade=4)),
    "glint": ("Four-point star glint (billboard).",
              dict(kind="star", bb="center", spin=45, s0=0.05, s1=0.55, life=6, fade=3)),
    "hit_star": ("Impact starburst on a target (billboard).",
                 dict(kind="burst", bb="center", roll=12, spin=14, s0=0.45, s1=1.5, life=5, fade=2)),
    "muzzle_burst": ("Big parasol muzzle / shell flash (billboard).",
                     dict(kind="burst", bb="center", spin=18, s0=0.9, s1=2.8, life=5, fade=2)),
    "flash_glow": ("Soft glow under a flash (billboard).",
                   dict(kind="glow", bb="center", s0=0.6, s1=1.8, life=6, fade=3)),
    "hit_ring": ("Thin ring expanding on a hit (billboard).",
                 dict(kind="ring", bb="center", spin=60, s0=0.35, s1=1.1, life=6, fade=2)),
    "ground_ring": ("Shockwave ring flat on the ground; pos at floor height (fixed).",
                    dict(kind="ring", rot="~ 90", s0=0.6, s1=4.2, life=8, fade=3)),
    "slash_h": ("Horizontal right-to-left crescent around the body; pos at the pivot, chest height.",
                dict(kind="crescent", spin=40, s0=3.6, s1=4.3, life=6, fade=2)),
    "petal": ("Petal flake that tumbles down (billboard).",
              dict(kind="petal", bb="center", roll=30, spin=150, s0=0.16, s1=0.12,
                   move=(0, -0.7, 0), life=24, fade=6)),
}

HEADER = "# Generated by tools/build_navia_fx_cards.py — edit the generator, not this file.\n"


def kind_axes():
    # spin axis = the card's normal: z for face cards, y for the flat crescent
    return {k: ("0f,1f,0f" if v[0] == "flat" else "0f,0f,1f") for k, v in KINDS.items()}


def datapack_files():
    f = {}
    f["init"] = [
        "# Navia card engine objectives (called from rlk:load).",
        "scoreboard objectives add nvfx dummy",
        "scoreboard objectives add nvfxT dummy",
        "scoreboard objectives add nvfxD dummy",
        "scoreboard objectives add nvfxK dummy",
        "scoreboard players set #nvfxN nvfx 0",
    ]
    f["card"] = [
        "# Spawn one gold Geo card at the executing position/rotation.",
        "# {kind, pos:\"^x ^y ^z\", rot:\"~ ~\", bb:fixed|center|vertical|horizontal, roll:<int deg>,",
        "#  spin:<int deg over the life, -170..170>, s0:<start size>, s1:<end size>,",
        "#  move:\"dx,dy,dz\" (end offset, display frame), life:<ticks>, fade:<shrink-out ticks>}",
        "# Kinds: " + ", ".join(KINDS) + ". Full reference: README (나비아 금빛 카드 효과).",
        "# Clip fx in first person (#pmFxFP, set around the fx call by char/motion/apply and the clip starts):",
        "# no cards, they would sit at the player's own eye. Gameplay calls (first-person muzzle cards) still draw.",
        "execute if score #pmFxFP tmp matches 1 run return 0",
        f"execute if score #nvfxN nvfx matches {CAP}.. run return 0",
        "scoreboard players add #nvfxN nvfx 1",
        '$data modify storage rlk:nvfx a set value {kind:"$(kind)",pos:"$(pos)",rot:"$(rot)",bb:"$(bb)",'
        's0:$(s0),s1:$(s1),move:"$(move)",ax:"0f,0f,1f",rr:0f,sr:0f,d:1,f:0}',
        "$function rlk:fx/nv/k/$(kind)",
        "$scoreboard players set #r nvfx $(roll)",
        "$scoreboard players set #s nvfx $(spin)",
        "$scoreboard players set #l nvfx $(life)",
        "$scoreboard players set #f nvfx $(fade)",
        "execute if score #l nvfx matches ..1 run scoreboard players set #l nvfx 2",
        "execute if score #f nvfx matches ..-1 run scoreboard players set #f nvfx 0",
        "scoreboard players operation #d nvfx = #l nvfx",
        "scoreboard players remove #d nvfx 2",
        "scoreboard players operation #f nvfx < #d nvfx",
        "execute if score #s nvfx matches 171.. run scoreboard players set #s nvfx 170",
        "execute if score #s nvfx matches ..-171 run scoreboard players set #s nvfx -170",
        "scoreboard players operation #d nvfx = #l nvfx",
        "scoreboard players operation #d nvfx -= #f nvfx",
        "scoreboard players remove #d nvfx 1",
        "execute store result storage rlk:nvfx a.rr float 0.017453292 run scoreboard players get #r nvfx",
        "execute store result storage rlk:nvfx a.sr float 0.017453292 run scoreboard players get #s nvfx",
        "execute store result storage rlk:nvfx a.d int 1 run scoreboard players get #d nvfx",
        "execute store result storage rlk:nvfx a.f int 1 run scoreboard players get #f nvfx",
        "function rlk:fx/nv/spawn with storage rlk:nvfx a",
        "execute store result score #t nvfx run time query gametime",
        "execute as @e[tag=rlk_nvfx_new,limit=1] run function rlk:fx/nv/born",
        "tag @e[tag=rlk_nvfx_new] remove rlk_nvfx_new",
    ]
    end_tr = ("translation:[$(move)],left_rotation:{angle:$(rr)f,axis:[0f,0f,1f]},"
              "scale:[$(s1)f,$(s1)f,$(s1)f],right_rotation:{angle:$(sr)f,axis:[$(ax)]}")
    f["spawn"] = [
        "# Internal: rlk:fx/nv/card resolves the arguments into storage rlk:nvfx a.",
        "$summon minecraft:item_display $(pos) {Tags:[\"rlk_nvfx\",\"rlk_nvfx_go\",\"rlk_nvfx_new\",\"rlk_room\"],"
        "billboard:\"$(bb)\",item_display:\"none\",brightness:{sky:15,block:15},view_range:1.5f,"
        "shadow_radius:0f,teleport_duration:0,interpolation_duration:0,"
        "transformation:{translation:[0f,0f,0f],left_rotation:{angle:$(rr)f,axis:[0f,0f,1f]},"
        "scale:[$(s0)f,$(s0)f,$(s0)f],right_rotation:[0f,0f,0f,1f]},"
        "item:{id:\"minecraft:paper\",count:1,components:{\"minecraft:item_model\":\"rlk:navia_fx/$(kind)\","
        "\"minecraft:custom_data\":{nvfx:{start_interpolation:0,interpolation_duration:$(d),"
        "transformation:{" + end_tr + "}},"
        "nvfz:{start_interpolation:0,interpolation_duration:$(f),transformation:{scale:[0f,0f,0f]}}}}}}",
        "$execute positioned $(pos) rotated $(rot) run tp @e[tag=rlk_nvfx_new,limit=1] ~ ~ ~ ~ ~",
    ]
    f["born"] = [
        "# Internal, as the new card: spawn tick, death tick and fade tick (gametime).",
        "scoreboard players operation @s nvfxT = #t nvfx",
        "scoreboard players operation #t nvfx += #l nvfx",
        "scoreboard players operation @s nvfxD = #t nvfx",
        "scoreboard players operation #t nvfx -= #f nvfx",
        "scoreboard players operation @s nvfxK = #t nvfx",
        "execute if score #f nvfx matches 1.. run tag @s add rlk_nvfx_fd",
    ]
    f["world"] = [
        "# Per-tick aging and cleanup of Navia cards (hooked once from rlk:tick).",
        "execute unless entity @e[tag=rlk_nvfx,limit=1] run return run scoreboard players set #nvfxN nvfx 0",
        "execute if entity @a[tag=player,scores={dead=1}] run return run function rlk:fx/nv/clear",
        "execute if entity @a[tag=player,scores={rnDie=1..}] run return run function rlk:fx/nv/clear",
        "execute store result score #now nvfx run time query gametime",
        "execute as @e[tag=rlk_nvfx] run function rlk:fx/nv/tick",
        "execute store result score #nvfxN nvfx if entity @e[tag=rlk_nvfx]",
    ]
    f["tick"] = [
        "# As one card: expire, start the main interpolation one tick after the spawn, then the fade.",
        "execute unless score @s nvfxD = @s nvfxD run return run kill @s",
        "execute if score #now nvfx >= @s nvfxD run return run kill @s",
        "execute if entity @s[tag=rlk_nvfx_go] if score #now nvfx > @s nvfxT run function rlk:fx/nv/go",
        "execute if entity @s[tag=rlk_nvfx_fd] if score #now nvfx >= @s nvfxK run function rlk:fx/nv/fade",
    ]
    f["go"] = [
        "# start -> end transformation over life-fade-1 ticks (stored on the item at spawn)",
        'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".nvfx',
        "tag @s remove rlk_nvfx_go",
    ]
    f["fade"] = [
        "# shrink to nothing over the last <fade> ticks",
        'data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".nvfz',
        "tag @s remove rlk_nvfx_fd",
    ]
    f["clear"] = [
        "# Remove every Navia card (run end, next field, death).",
        "kill @e[tag=rlk_nvfx]",
        "scoreboard players set #nvfxN nvfx 0",
    ]
    for kind, axis in kind_axes().items():
        f[f"k/{kind}"] = [f"# {KINDS[kind][5]}: spin axis = card normal",
                          f'data modify storage rlk:nvfx a.ax set value "{axis}"']
    for name, (comment, kw) in PRESETS.items():
        f[f"p/{name}"] = [f"# {comment}", "# {pos:\"^x ^y ^z\"}",
                          "$" + card_call(pos="$(pos)", **kw)]
    # test / preview: every kind in a row 3 blocks ahead, plus crescent orientations
    test = ["# Every kind in a row 3 blocks ahead of the executor, 3 s each:",
            "# /execute as @p at @s rotated ~ 0 run function rlk:fx/nv/test/all"]
    for i, kind in enumerate(KINDS):
        x = 3.15 - 0.9 * i
        if kind == "crescent":
            continue
        y = 0.4 if kind == "shard" else 1.2
        test.append(card_call(kind, f"^{num(x)} ^{num(y)} ^3", bb="fixed", s0=0.1, s1=0.8,
                              spin=0 if kind in ("rose", "petal", "shard") else 90, life=60, fade=10))
    test.append(card_call("crescent", "^0 ^1.2 ^0", s0=2.5, s1=4.0, spin=60, life=60, fade=10))
    f["test/all"] = test
    sl = ["# Crescent orientations (roll) around the executor, 3 s each:",
          "# /execute as @p at @s rotated ~ 0 run function rlk:fx/nv/test/slashes"]
    for k, (roll, y) in enumerate(((0, 0.6), (180, 1.1), (-40, 1.6), (90, 2.1))):
        sl.append(card_call("crescent", f"^0 ^{num(y)} ^0", roll=roll, s0=4.0, s1=4.0, life=60, fade=10))
    f["test/slashes"] = sl
    return f


def build_datapack(dp):
    root = Path(dp) / "data/rlk/function/fx/nv"
    files = datapack_files()
    if root.exists():
        for p in root.rglob("*.mcfunction"):
            if p.relative_to(root).with_suffix("").as_posix() not in files:
                p.unlink()
    for name, lines in files.items():
        p = root / f"{name}.mcfunction"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(HEADER + "\n".join(lines) + "\n", encoding="utf-8")
    return len(files)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--resourcepack", help="unpacked resource pack root (assets/...)")
    ap.add_argument("--datapack", default=str(HERE.parent), help="datapack root (data/...)")
    ap.add_argument("--skip-rp", action="store_true", help="only write the datapack functions")
    a = ap.parse_args()
    n = build_datapack(a.datapack)
    msg = f"navia fx cards: {n} functions"
    if not a.skip_rp:
        if not a.resourcepack:
            ap.error("--resourcepack is required unless --skip-rp")
        build_resourcepack(a.resourcepack)
        msg += f", {len(KINDS)} sprites/models ({', '.join(KINDS)})"
    print(msg)


if __name__ == "__main__":
    main()
