"""Tinted FX cards of the butterfly module (the plan's "tinted card engine"): greyscale sprites coloured per spawn.

Navia's card engine (tools/build_navia_fx_cards.py, rlk:fx/nv) paints gold sprites and shares a 48-card cap with
Navia, so it cannot draw lime moonlight, opal, cyan or Pyro orange-magenta. These cards are the same idea (short-
lived item_display cards with a start -> end transformation run by client interpolation) with:

  * greyscale sprites (luminance + alpha) whose colour comes from the item definition's tint source
    minecraft:custom_model_data (index 0): every spawn passes its own colour (an int RGB), so any palette works
    without one item definition per colour;
  * an engine owned by the module (F:mboss/butterfly/tc/**, written by core.build): ticked by the module's own
    tick / intro_tick / death_tick while cards live (#bfTcN mb >= 1), its own cap (CAP live cards), cleared on
    pause, and every card carries rlk_mb_aux + rlk_room, so it dies with the fight.

Resource pack side (stdlib only): python3 tools/build_mboss_butterfly_fx.py --resourcepack <unpacked RP> writes
  assets/rlk/textures/mboss/bf_fx/<kind>.png, assets/rlk/models/item/mboss/bf_fx/<kind>.json (tintindex 0),
  assets/rlk/items/mboss/bf_fx/<kind>.json (custom_model_data tint, default white) and the atlas entries.

Call (Python): api.Gen.tcard(kind, pos, colour, rot='~ ~', bb='fixed', roll=0, spin=0, s0=0, s1=1,
move=(0,0,0), life=8, fade=0) -> one function line. Display frame and card coordinates are Navia's: +x left,
+y up, +z forward; "face" cards lie in the local XY plane (facing forward, or the camera with bb "center"), "flat"
cards in the local XZ plane (the crescent: a swing-plane ribbon whose head is at the player's left).
"""
import json
import math
import struct
import zlib
from pathlib import Path

NS_TEX = 'rlk:mboss/bf_fx/'
ITEM_NS = 'rlk:mboss/bf_fx/'
DIR = 'tc'
CAP = 40


def smooth(e0, e1, x):
    t = (x - e0) / (e1 - e0)
    t = 0.0 if t < 0 else 1.0 if t > 1 else t
    return t * t * (3 - 2 * t)


def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


# Each painter takes card coordinates (a, b) and returns (luminance, alpha); the tint multiplies the luminance.
def paint_star(a, b):
    """Four-point star glint (sparkles, the release's star flare, the cure emblem tip)."""
    r = math.hypot(a, b)

    def ray(u, v, length, width):
        f = 1 - abs(u) / length
        if f <= 0:
            return 0.0
        return f ** 1.4 * math.exp(-(v / (width * f + 0.012)) ** 2)
    i = max(ray(a, b, 0.98, 0.075), ray(b, a, 0.98, 0.075))
    d1, d2 = (a + b) / math.sqrt(2), (a - b) / math.sqrt(2)
    i = max(i, 0.5 * ray(d1, d2, 0.4, 0.05), 0.5 * ray(d2, d1, 0.4, 0.05), math.exp(-(r / 0.13) ** 2))
    return 0.75 + 0.25 * i, clamp01(i * 1.3)


BURST = ((8, 0.98, 0.115), (98, 0.94, 0.11), (188, 0.97, 0.115), (278, 0.92, 0.11), (52, 0.70, 0.085),
         (143, 0.66, 0.08), (233, 0.72, 0.085), (322, 0.64, 0.08), (30, 0.46, 0.06), (120, 0.50, 0.06),
         (208, 0.44, 0.06), (300, 0.48, 0.06))


def paint_burst(a, b):
    """Radial starburst flash (impacts, the cocoon burst)."""
    r = math.hypot(a, b)
    phi = math.atan2(a, b)
    edge = None
    for deg, length, w0 in BURST:
        if r >= length:
            continue
        dphi = (phi - math.radians(deg) + math.pi) % (2 * math.pi) - math.pi
        if abs(dphi) > math.pi / 2:
            continue
        perp = r * math.sin(abs(dphi))
        w = w0 * (1 - r / length) + 0.004
        if perp < w:
            e = (w - perp) / w
            edge = e if edge is None else max(edge, e)
    if r < 0.21 or edge is not None:
        return 0.72 + 0.28 * (1 - r), 1.0
    haze = 0.36 * math.exp(-(r / 0.36) ** 2)
    return 0.9, haze


def paint_ring(a, b):
    """Thin ring with a glow band and a brighter leading sector (ripple rings, ring cage, shock rings)."""
    r = math.hypot(a, b)
    d = abs(r - 0.86)
    lead = 0.6 + 0.4 * max(0.0, math.cos(math.atan2(a, b) - 0.6)) ** 3
    core = math.exp(-(d / 0.024) ** 2)
    glow = 0.7 * math.exp(-(d / 0.08) ** 2)
    i = max(core, glow) * lead
    return 0.7 + 0.3 * core, clamp01(i * 1.15)


def paint_glow(a, b):
    """Soft radial glow disc (sphere glow, ground glow, charge)."""
    r = math.hypot(a, b)
    if r >= 1:
        return 0.0, 0.0
    return 0.85 + 0.15 * (1 - r), 0.95 * (1 - r) ** 1.3


def paint_orb(a, b):
    """Translucent sphere with a bright rim and two lighter swirl bands (the coco orbs, moon dew, the sphere)."""
    r = math.hypot(a, b)
    if r >= 0.97:
        return 0.0, 0.0
    rim = math.exp(-((r - 0.9) / 0.05) ** 2)
    band = max(math.exp(-((b - 0.35 * math.sin(2.6 * a + 0.4)) / 0.09) ** 2),
               0.7 * math.exp(-((b + 0.4 + 0.25 * math.sin(3.1 * a)) / 0.07) ** 2)) * (1 - r ** 4)
    hi = math.exp(-(((a + 0.35) ** 2 + (b - 0.4) ** 2) / 0.03))
    alpha = 0.42 + 0.5 * rim + 0.35 * band + 0.3 * hi
    return 0.68 + 0.22 * band + 0.1 * rim + 0.25 * hi, clamp01(alpha)


def paint_slash(a, b):
    """Long thin streak, tapered at both ends (the X glint, slash streaks, speed lines)."""
    t = abs(a)
    if t >= 1:
        return 0.0, 0.0
    hw = 0.95 * (1 - t ** 2) ** 0.9 + 0.02
    d = abs(b) / hw
    if d >= 1:
        return 0.0, 0.0
    return 0.75 + 0.25 * (1 - d), clamp01((1 - d ** 2) * (1 - t ** 6) * 1.2)


def paint_crescent(a, b):
    """Thick tapered crescent ribbon in the swing plane (Navia's shape): pivot at the card origin, head (thick,
    bright) at -a, tail fading toward +a (wing arcs, kick crescents, fire crescents)."""
    r = math.hypot(a, b)
    if r < 0.45 or r > 1.0:
        return 0.0, 0.0
    phi = math.degrees(math.atan2(a, b))
    s = (80.0 - phi) / 160.0
    if s <= 0 or s >= 1:
        return 0.0, 0.0
    ro = 0.97 - 0.035 * (1 - s)
    thick = 0.36 * math.sin(math.pi * s ** 1.55) ** 0.75
    ri = ro - thick
    if r > ro or r < ri or thick < 0.01:
        return 0.0, 0.0
    w = (ro - r) / thick
    lum = 1.0 - 0.32 * w - 0.12 * (1 - s) ** 2 + 0.06 * math.sin(w * 29.0 + 1.3)
    alpha = (1 - 0.6 * smooth(0.35, 1.0, w)) * (0.22 + 0.78 * smooth(0.0, 0.6, s))
    return clamp01(lum), clamp01(alpha * 1.05)


def paint_moon(a, b):
    """Crescent moon (face card): the vertical kick crescents, the vacuum blade, the chain plates."""
    r1 = math.hypot(a, b)
    r2 = math.hypot(a - 0.42, b + 0.04)
    if r1 > 0.93 or r2 < 0.74:
        return 0.0, 0.0
    e = min(0.93 - r1, r2 - 0.74)
    thick = clamp01((0.42 - a) / 1.3)
    return 0.74 + 0.26 * smooth(0.0, 0.12, e) * (0.6 + 0.4 * thick), clamp01(smooth(0.0, 0.05, e) * (0.55 + 0.45 * thick) * 1.1)


def paint_shard(a, b):
    """Crystal shard (pivot at its root): the cocoon burst, the wing shatter, the death shards."""
    if b <= 0 or b >= 1:
        return 0.0, 0.0
    half = 0.92 * (b / 0.2 if b < 0.2 else (1 - b) / 0.8)
    m = half - abs(a)
    if m <= 0:
        return 0.0, 0.0
    facet = 0.95 if a < 0 else 0.72
    if abs(a) < 0.08:
        facet = 1.0
    if m < 0.14:
        facet *= 0.82
    return facet, 0.92


def paint_leaf(a, b):
    """Lens-shaped leaf with a darker midrib (Dendro leaves, leaf blades)."""
    t = (b + 1) / 2
    if t <= 0 or t >= 1:
        return 0.0, 0.0
    half = 0.9 * math.sin(math.pi * t) ** 0.9
    x = a - 0.12 * math.sin(math.pi * t)
    m = half - abs(x)
    if m <= 0:
        return 0.0, 0.0
    lum = 0.9 - 0.25 * math.exp(-(x / 0.06) ** 2) * (0.15 < t < 0.9)
    return lum, clamp01(smooth(0.0, 0.08, m) * 1.0)


def paint_flame(a, b):
    """Flame tongue (pivot at the base): the Pyro fan, the flame trail, fire crescent tails."""
    t = b
    if t <= 0 or t >= 1:
        return 0.0, 0.0
    sway = 0.12 * math.sin(4.5 * t + 0.6) * t
    half = 0.85 * (t / 0.25 if t < 0.25 else (1 - t) / 0.75) ** 0.8
    x = a - sway
    m = half - abs(x)
    if m <= 0:
        return 0.0, 0.0
    core = math.exp(-(x / (0.35 * half + 0.02)) ** 2) * (1 - t)
    return 0.7 + 0.3 * core, clamp01(smooth(0.0, 0.12, m) * (1 - t ** 3) * 1.1)


def paint_swirl(a, b):
    """Two-turn spiral stroke (the 달빛 고치 swirl, the spiral-jump ribbons)."""
    r = math.hypot(a, b)
    if r > 0.97 or r < 0.04:
        return 0.0, 0.0
    th = math.atan2(b, a) % (2 * math.pi)
    best = 9.0
    for k in range(3):
        rr = 0.06 + 0.14 * (th + 2 * math.pi * k) / (2 * math.pi) * 2.2
        best = min(best, abs(r - rr))
    w = 0.035 + 0.035 * r
    if best > w:
        return 0.0, 0.0
    return 0.75 + 0.25 * (1 - best / w), clamp01((1 - (best / w) ** 2) * 1.2)


# kind -> plane, texture size (w, h), card extent in blocks at scale 1 (a0, a1, b0, b1), painter box, painter, doc
KINDS = {
    'star':     ('face', (64, 64),   (-0.5, 0.5, -0.5, 0.5),     (-1, 1, -1, 1), paint_star, 'four-point star glint'),
    'burst':    ('face', (128, 128), (-0.5, 0.5, -0.5, 0.5),     (-1, 1, -1, 1), paint_burst, 'radial starburst flash'),
    'ring':     ('face', (128, 128), (-0.5, 0.5, -0.5, 0.5),     (-1, 1, -1, 1), paint_ring, 'thin ring / shock ring'),
    'glow':     ('face', (64, 64),   (-0.5, 0.5, -0.5, 0.5),     (-1, 1, -1, 1), paint_glow, 'soft glow disc'),
    'orb':      ('face', (64, 64),   (-0.5, 0.5, -0.5, 0.5),     (-1, 1, -1, 1), paint_orb, 'translucent sphere with swirl bands'),
    'slash':    ('face', (256, 32),  (-0.5, 0.5, -0.0625, 0.0625), (-1, 1, -1, 1), paint_slash, 'long thin streak'),
    'crescent': ('flat', (256, 128), (-0.5, 0.5, 0.0, 0.5),      (-1, 1, 0, 1), paint_crescent, 'swing-plane crescent ribbon'),
    'moon':     ('face', (128, 128), (-0.5, 0.5, -0.5, 0.5),     (-1, 1, -1, 1), paint_moon, 'crescent moon'),
    'shard':    ('face', (32, 128),  (-0.125, 0.125, 0.0, 1.0),  (-1, 1, 0, 1), paint_shard, 'crystal shard (pivot at its root)'),
    'leaf':     ('face', (32, 64),   (-0.25, 0.25, -0.5, 0.5),   (-1, 1, -1, 1), paint_leaf, 'leaf'),
    'flame':    ('face', (64, 128),  (-0.25, 0.25, 0.0, 1.0),    (-1, 1, 0, 1), paint_flame, 'flame tongue (pivot at its base)'),
    'swirl':    ('face', (128, 128), (-0.5, 0.5, -0.5, 0.5),     (-1, 1, -1, 1), paint_swirl, 'two-turn spiral stroke'),
}


def render(kind, ss=3):
    plane, (w, h), _ext, (a0, a1, b0, b1), fn, _ = KINDS[kind]
    px = bytearray()
    for j in range(h):
        px.append(0)
        for i in range(w):
            al = lu = 0.0
            for sj in range(ss):
                v = (j + (sj + 0.5) / ss) / h
                bb = b1 - v * (b1 - b0)
                for si in range(ss):
                    u = (i + (si + 0.5) / ss) / w
                    l, a = fn(a0 + u * (a1 - a0), bb)
                    lu += l * a
                    al += a
            alpha = al / (ss * ss)
            if alpha < 0.1:
                px += bytes((0, 0, 0, 0))
                continue
            g = round(255 * clamp01(lu / al))
            px += bytes((g, g, g, round(255 * clamp01(alpha))))
    return w, h, bytes(px)


def png_bytes(w, h, raw):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


def model_json(kind):
    """A zero-thickness double-sided card (Navia's frame: display-local p at model (8 - 16 px, 8 + 16 py, 8 - 16 pz)),
    every face tinted (tintindex 0 = the item definition's custom_model_data colour)."""
    plane, _size, (a0, a1, b0, b1), _box, _fn, _ = KINDS[kind]
    x0, x1 = 8 + 16 * a0, 8 + 16 * a1
    if plane == 'face':
        y0, y1 = 8 + 16 * b0, 8 + 16 * b1
        frm, to = [x0, y0, 8], [x1, y1, 8]
        faces = {'south': {'uv': [0, 0, 16, 16], 'texture': '#0', 'tintindex': 0},
                 'north': {'uv': [16, 0, 0, 16], 'texture': '#0', 'tintindex': 0}}
    else:
        z_near, z_far = 8 - 16 * b0, 8 - 16 * b1
        frm, to = [x0, 8, z_far], [x1, 8, z_near]
        faces = {'up': {'uv': [0, 0, 16, 16], 'texture': '#0', 'tintindex': 0},
                 'down': {'uv': [0, 16, 16, 0], 'texture': '#0', 'tintindex': 0}}
    for v in frm + to:
        assert -16 <= v <= 32, (kind, frm, to)
    tex = NS_TEX + kind
    return {'ambientocclusion': False, 'textures': {'0': tex, 'particle': tex},
            'elements': [{'from': [round(v, 4) for v in frm], 'to': [round(v, 4) for v in to], 'shade': False, 'faces': faces}]}


def item_json(kind):
    return {'model': {'type': 'minecraft:model', 'model': f'rlk:item/mboss/bf_fx/{kind}',
                      'tints': [{'type': 'minecraft:custom_model_data', 'index': 0, 'default': 16777215}]}}


def build_resourcepack(rp):
    rp = Path(rp)
    root = rp / 'assets/rlk'
    for sub in ('textures/mboss/bf_fx', 'models/item/mboss/bf_fx', 'items/mboss/bf_fx'):
        d = root / sub
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob('*'):
            if old.stem not in KINDS:
                old.unlink()
    px = 0
    for kind in KINDS:
        w, h, raw = render(kind)
        px += w * h
        (root / 'textures/mboss/bf_fx' / f'{kind}.png').write_bytes(png_bytes(w, h, raw))
        (root / 'models/item/mboss/bf_fx' / f'{kind}.json').write_text(json.dumps(model_json(kind), separators=(',', ':')) + '\n', encoding='utf-8')
        (root / 'items/mboss/bf_fx' / f'{kind}.json').write_text(json.dumps(item_json(kind), separators=(',', ':')) + '\n', encoding='utf-8')
    atlaspath = rp / 'assets/minecraft/atlases/items.json'
    atlas = json.loads(atlaspath.read_text(encoding='utf-8')) if atlaspath.exists() else {'sources': []}
    atlas['sources'] = [s for s in atlas['sources']
                        if not str(s.get('resource', '')).startswith(NS_TEX) or s['resource'][len(NS_TEX):] in KINDS]
    have = {s.get('sprite', s.get('resource')) for s in atlas['sources']}
    for kind in KINDS:
        if NS_TEX + kind not in have:
            atlas['sources'].append({'type': 'minecraft:single', 'resource': NS_TEX + kind})
    atlaspath.parent.mkdir(parents=True, exist_ok=True)
    atlaspath.write_text(json.dumps(atlas, indent=2) + '\n', encoding='utf-8')
    return len(KINDS), px


# ---------------------------------------------------------------------------------------------- datapack engine
def num(v):
    return f'{v:.4f}'.rstrip('0').rstrip('.') if isinstance(v, float) else str(v)


def colour_int(c):
    if isinstance(c, str):
        return int(c.lstrip('#'), 16)
    if isinstance(c, int):
        return c
    r, g, b = (max(0, min(255, round(255 * float(x)))) for x in c)
    return (r << 16) | (g << 8) | b


def tcard_call(ns, kind, pos, colour, rot='~ ~', bb='fixed', roll=0, spin=0, s0=0.0, s1=1.0, move=(0.0, 0.0, 0.0),
               life=8, fade=0):
    """One tinted card at the executing position/rotation (see the module doc)."""
    assert kind in KINDS and bb in ('fixed', 'center', 'vertical', 'horizontal'), (kind, bb)
    mv = ','.join(num(float(v)) + 'f' for v in move)
    ax = '0f,1f,0f' if KINDS[kind][0] == 'flat' else '0f,0f,1f'          # spin axis = the card normal
    return (f'execute positioned {pos} rotated {rot} run function {ns}{DIR}/card {{kind:"{kind}",bb:"{bb}",roll:{int(roll)},spin:{int(spin)},'
            f's0:{num(float(s0))},s1:{num(float(s1))},move:"{mv}",life:{int(life)},fade:{int(fade)},col:{colour_int(colour)},ax:"{ax}"}}')


def emit(g, ns):
    """F:mboss/butterfly/tc/** (the engine). Time = the engine's own clock #bfTcNow (+1 per tc/all, which runs every
    module tick while cards live and never while the fight is paused), so cards age with the fight. Per-card times in
    the framework scratch objectives: mbT spawn, mbS end, mbId fade start."""
    fn = f'{ns}{DIR}/'
    w = lambda rel, lines: g.w(f'{DIR}/{rel}', lines)
    w('card', [
        '# One tinted card at the executing position/rotation (tools/mboss_butterfly/cards.py, api.Gen.tcard: the call is',
        '# execute positioned <pos> rotated <rot> run ...): {kind, bb:fixed|center|vertical|horizontal, roll:<deg>, spin:<deg over the life,',
        '#  -170..170>, s0/s1:<start/end size>, move:"dx,dy,dz" (end offset, display frame), life:<t>, fade:<shrink-out t>,',
        f'#  col:<int RGB>, ax:"<spin axis = the card normal>"}}. Kinds: {", ".join(KINDS)}. At most {CAP} live (further spawns',
        '#  are skipped).',
        f'execute if score #bfTcN mb matches {CAP}.. run return 0',
        'scoreboard players add #bfTcN mb 1',
        '$data modify storage rlk:mboss bftc set value {kind:"$(kind)",bb:"$(bb)",s0:$(s0),s1:$(s1),'
        'move:"$(move)",col:$(col),ax:"$(ax)",rr:0f,sr:0f,d:1,f:0}',
        '$scoreboard players set #bfTcR mb $(roll)',
        '$scoreboard players set #bfTcS mb $(spin)',
        '$scoreboard players set #bfTcL mb $(life)',
        '$scoreboard players set #bfTcF mb $(fade)',
        'execute if score #bfTcL mb matches ..1 run scoreboard players set #bfTcL mb 2',
        'execute if score #bfTcF mb matches ..-1 run scoreboard players set #bfTcF mb 0',
        'scoreboard players operation #bfTcD mb = #bfTcL mb',
        'scoreboard players remove #bfTcD mb 2',
        'scoreboard players operation #bfTcF mb < #bfTcD mb',
        'execute if score #bfTcS mb matches 171.. run scoreboard players set #bfTcS mb 170',
        'execute if score #bfTcS mb matches ..-171 run scoreboard players set #bfTcS mb -170',
        'scoreboard players operation #bfTcD mb = #bfTcL mb',
        'scoreboard players operation #bfTcD mb -= #bfTcF mb',
        'scoreboard players remove #bfTcD mb 1',
        'execute store result storage rlk:mboss bftc.rr float 0.017453292 run scoreboard players get #bfTcR mb',
        'execute store result storage rlk:mboss bftc.sr float 0.017453292 run scoreboard players get #bfTcS mb',
        'execute store result storage rlk:mboss bftc.d int 1 run scoreboard players get #bfTcD mb',
        'execute store result storage rlk:mboss bftc.f int 1 run scoreboard players get #bfTcF mb',
        f'function {fn}spawn with storage rlk:mboss bftc',
        'scoreboard players operation #bfTcT mb = #bfTcNow mb',
        f'execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_tcn,limit=1] run function {fn}born',
        'tag @e[type=minecraft:item_display,tag=rlk_mb_bf_tcn] remove rlk_mb_bf_tcn'])
    end_tr = ('translation:[$(move)],left_rotation:{angle:$(rr)f,axis:[0f,0f,1f]},'
              'scale:[$(s1)f,$(s1)f,$(s1)f],right_rotation:{angle:$(sr)f,axis:[$(ax)]}')
    w('spawn', [
        '# Internal: tc/card resolved the arguments into storage rlk:mboss bftc.',
        '$summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_tc","rlk_mb_bf_tcgo","rlk_mb_bf_tcn"],'
        'billboard:"$(bb)",item_display:"none",brightness:{sky:15,block:15},view_range:1.5f,shadow_radius:0f,'
        'teleport_duration:0,interpolation_duration:0,'
        'transformation:{translation:[0f,0f,0f],left_rotation:{angle:$(rr)f,axis:[0f,0f,1f]},scale:[$(s0)f,$(s0)f,$(s0)f],'
        'right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{'
        f'"minecraft:item_model":"{ITEM_NS}$(kind)","minecraft:custom_model_data":{{colors:[$(col)]}},'
        '"minecraft:custom_data":{bftc:{start_interpolation:0,interpolation_duration:$(d),transformation:{' + end_tr + '}},'
        'bftz:{start_interpolation:0,interpolation_duration:$(f),transformation:{scale:[0f,0f,0f]}}}}}}',
        'tp @e[type=minecraft:item_display,tag=rlk_mb_bf_tcn,limit=1] ~ ~ ~ ~ ~'])
    w('born', ['# Internal, as the new card: spawn, end and fade-start time (#bfTcNow).',
               'scoreboard players operation @s mbT = #bfTcT mb',
               'scoreboard players operation #bfTcT mb += #bfTcL mb',
               'scoreboard players operation @s mbS = #bfTcT mb',
               'scoreboard players operation #bfTcT mb -= #bfTcF mb',
               'scoreboard players operation @s mbId = #bfTcT mb',
               'execute if score #bfTcF mb matches 1.. run tag @s add rlk_mb_bf_tcfd'])
    w('all', ['# Module tick / intro_tick / death_tick while #bfTcN >= 1: the engine clock, age every card, recount.',
              'scoreboard players add #bfTcNow mb 1',
              'scoreboard players set #bfTcN mb 0',
              f'execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_tc] run function {fn}tick'])
    w('tick', ['# As one card: expire; start the main interpolation one tick after the spawn; then the fade.',
               'execute unless score @s mbS = @s mbS run return run kill @s',
               'execute if score #bfTcNow mb >= @s mbS run return run kill @s',
               f'execute if entity @s[tag=rlk_mb_bf_tcgo] if score #bfTcNow mb > @s mbT run function {fn}go',
               'scoreboard players add #bfTcN mb 1',
               f'execute if entity @s[tag=rlk_mb_bf_tcfd] if score #bfTcNow mb >= @s mbId run function {fn}fade'])
    w('go', ['data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".bftc',
             'tag @s remove rlk_mb_bf_tcgo'])
    w('fade', ['data modify entity @s {} merge from entity @s item.components."minecraft:custom_data".bftz',
               'tag @s remove rlk_mb_bf_tcfd'])
    w('clear', ['# Every tinted card gone (pause, cleanup).', 'kill @e[type=minecraft:item_display,tag=rlk_mb_bf_tc]',
                'scoreboard players set #bfTcN mb 0'])
