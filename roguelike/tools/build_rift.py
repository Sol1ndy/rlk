#!/usr/bin/env python3
"""The room rift (균열) that leads to a special boss (Tachy S1; scratchpad tk/PLAN.md §7, tk/contract.md §3.1).

    python3 tools/build_rift.py [--resourcepack <unpacked RP>] [--datapack <dp root>]

Writes (and owns: stale files there are deleted on every run)
  datapack       F:room/rift/**            roll, arm, show, spot search, open / reopen / close, tick, enter, click, init,
                                           forget, uninstall
                 F:room/obj/k_rift         the hover object of an open rift (oact 17: label 균열, hint ▶ 좌클릭)
                 the shared hook lines of PLAN §7.8 in hand-written engine files, each one preceded by the marker
                 comment `# rift (build_rift.py)`: every run first removes every marked line, then inserts them again at
                 their anchors (the anchors are base-file lines, never lines of another generator), so running it twice,
                 or in any order with tools/build_ch2_mobs.py / build_ch3_mobs.py, gives identical files.
  resource pack  assets/rlk/textures/rift/{void,rim,crack,arc_0..3}.png (stdlib painter, fixed seeds), the item models
  (optional)     assets/rlk/models/item/rift/*.json, the item definitions assets/rlk/items/rift/*.json (item model ids
                 rlk:rift/<kind>) and their entries in assets/minecraft/atlases/items.json (sprites rlk:rift/<kind>).

The rift's special-boss side (sp/roll, sp/prep, sp/gate, the fight, the reward) is the core's F:mboss/sp/**
(tools/build_mboss_core.py). Runtime state: fake players #rift* in objective room (#riftPm per mille, set in load's
조절 지점; #riftUsed once per run; #riftForce the test's forced rift; #riftOn while a rift or a queued show exists), the
zone tags rlk_riftz (holds a rift) / rlk_riftdone (its special was killed) / rlk_riftq (show queued for the next tick),
zone data.rift {id}; the anchor marker rlk_rift (scores zid, riftS state, riftT clock, riftCd cooldown, riftDw dwell,
riftPk boxes after the collapse, riftX/Y/Z position x100) and its parts rlk_rift_part (void, rim, crack, 3 arcs: riftA,
the hover object group rlk_rift_obj), every one rlk_room, so a map change, room/wipe, run end and uninstall remove them.
"""
import argparse
import json
import math
import random
import struct
import sys
import zlib
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import mboss_lib as L  # noqa: E402

GEN = 'tools/build_rift.py'
MARK = '# rift (build_rift.py)'
NS = 'rlk:room/rift/'

# ---------------------------------------------------------------------------------------------------------- tuning
RIFT_PM = 30                 # load's 조절 지점: per mille per eligible combat room built
TRIES = 24                   # spot search tries (PLAN §7.4)
DOOR_R, OBJ_R, PLAYER_R, WALL_IN = 4.5, 3.5, 5.0, 3.0
NODE_R = {4: 9.0}            # node zones whose centre holds a wide object group: keep this far from the centre
NODE_R_DEFAULT = 4.5         # other non-combat kinds (objects at the centre)
DWELL = 10                   # walk-in: consecutive ticks within 1 b horizontal, |dy| < 1.5
REFUSE_CD = 40               # a refused entry holds the rift this long
REOPEN_CD = 60               # after a cancelled fight the rift reopens with this cooldown
GROW_T, CLOSE_T = 20, 30
BLIND_T = 20                 # entering: blindness at this tick (the arena jump is at #spawnT 30)
CENTRE = 1.45                # void centre above the anchor (open); dormant = half size at the same bottom
VOID_H = 2.6                 # void card height (blocks) = item display scale of a 16-unit model
RIM_K = 1.16                 # rim card relative to the void (its glow band shows around the tear)
CRACK_S = 3.2
ARC_S = 1.5
# arcs in the billboard plane (x screen-right, y up, blocks at full size): around the rim
ARC_POS = [(-0.80, 1.90), (0.85, 1.10), (0.10, 2.70)]
ARC_ROLLS = [-0.9, -0.55, -0.25, 0.0, 0.3, 0.6, 0.95, 3.14]
# rim points for the open particles (billboard plane, x, y over the anchor)
RIM_PTS = [(0.85 * math.sin(a), CENTRE + 1.3 * math.cos(a)) for a in [k * math.pi / 4 for k in range(8)]]

# ---------------------------------------------------------------------------------------------------------- textures
TEX = {'void': (64, 96), 'rim': (64, 96), 'crack': (64, 64), 'arc_0': (32, 64), 'arc_1': (32, 64), 'arc_2': (32, 64),
       'arc_3': (32, 64)}
ATLAS_BUDGET = 30_000
TEX_NS = 'rlk:rift/'


def atlas_px():
    return sum(w * h for w, h in TEX.values())


def png_bytes(w, h, px):
    raw = b''.join(b'\x00' + bytes(v for p in px[y * w:(y + 1) * w] for v in p) for y in range(h))

    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)) +
            chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


BLOB = (32.0, 50.0, 26.0, 41.0)          # centre x, y, radii (px) of the tear on the 64 x 96 cards


def _blob_r(theta, rng_ph):
    a, b, c = rng_ph
    return 1.0 + 0.07 * math.sin(3 * theta + a) + 0.045 * math.sin(5 * theta + b) + 0.03 * math.sin(11 * theta + c)


def _blob_rho(x, y, ph, jag):
    cx, cy, rx, ry = BLOB
    dx, dy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
    th = math.atan2(dy, dx)
    k = int((th + math.pi) / (2 * math.pi) * len(jag)) % len(jag)
    return math.hypot(dx, dy) / (_blob_r(th, ph) * (1.0 + jag[k]))


def paint_void():
    w, h = TEX['void']
    rng = random.Random(7101)
    ph = (rng.uniform(0, 6.28), rng.uniform(0, 6.28), rng.uniform(0, 6.28))
    jag = [rng.uniform(-0.035, 0.035) for _ in range(72)]
    px = []
    for y in range(h):
        for x in range(w):
            r = _blob_rho(x, y, ph, jag)
            if r <= 1.0:
                # pure black, a few near-black violet flecks deep inside (depth, not light)
                v = (6, 2, 12, 255) if (r < 0.7 and rng.random() < 0.03) else (0, 0, 0, 255)
            elif r <= 1.0 + 2.0 / BLOB[2] and rng.random() < 0.6:
                v = (14, 8, 26, rng.choice((150, 190, 230)))          # 1-2 px ragged edge
            else:
                v = (0, 0, 0, 0)
            px.append(v)
    return w, h, px


def _mix(c0, c1, t):
    return tuple(int(round(c0[i] + (c1[i] - c0[i]) * t)) for i in range(3))


def paint_rim():
    # The same tear, drawn RIM_K x behind the void: in these texture coordinates the void edge is at rho 1 / RIM_K. Hollow inside
    # (no coplanar overlap with the void), a white-cyan core band at the edge, then a cyan glow with jagged spikes outward.
    w, h = TEX['rim']
    rng = random.Random(7101)
    ph = (rng.uniform(0, 6.28), rng.uniform(0, 6.28), rng.uniform(0, 6.28))
    jag = [rng.uniform(-0.035, 0.035) for _ in range(72)]
    rng = random.Random(7202)
    spikes = [rng.uniform(0.0, 0.09) if rng.random() < 0.3 else 0.0 for _ in range(48)]
    edge = 1.0 / RIM_K
    core, glow = (0xE8, 0xFB, 0xFF), (0x7F, 0xD8, 0xFF)
    px = []
    for y in range(h):
        for x in range(w):
            r = _blob_rho(x, y, ph, jag)
            cx, cy, rx, ry = BLOB
            th = math.atan2((y + 0.5 - cy) / ry, (x + 0.5 - cx) / rx)
            k = int((th + math.pi) / (2 * math.pi) * len(spikes)) % len(spikes)
            outer = 1.0 + spikes[k]
            if r < edge - 0.04:
                v = (0, 0, 0, 0)
            elif r < edge + 0.05:
                v = core + (255,)
            elif r < outer:
                t = (r - edge - 0.05) / max(0.01, outer - edge - 0.05)
                a = int(round(235 - 175 * t))
                v = _mix(core, glow, min(1.0, t * 1.4)) + (a if rng.random() < 0.92 else a // 2,)
            else:
                v = (0, 0, 0, 0)
            px.append(v)
    return w, h, px


def _line(px, w, h, x0, y0, x1, y1, col, width=1):
    n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
    for i in range(n + 1):
        t = i / n
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        for ox in range(-(width // 2), width - width // 2):
            xi, yi = int(x) + ox, int(y)
            if 0 <= xi < w and 0 <= yi < h:
                px[yi * w + xi] = col


def _blend_px(px, w, h, x, y, col, a):
    if 0 <= x < w and 0 <= y < h:
        o = px[y * w + x]
        if o[3] >= a:
            return
        px[y * w + x] = col + (a,)


def paint_crack():
    w, h = TEX['crack']
    rng = random.Random(7303)
    px = [(0, 0, 0, 0)] * (w * h)
    cx = cy = 31.5
    # faint lit floor: a cyan radial glow
    for y in range(h):
        for x in range(w):
            d = math.hypot(x - cx, y - cy)
            if d < 30:
                a = int(120 * (1 - d / 30) ** 1.4)
                if a > 4:
                    px[y * w + x] = (0x6F, 0xD0, 0xF5, a)
    cracks = []
    for i in range(8):
        ang = i * math.pi / 4 + rng.uniform(-0.3, 0.3)
        x, y, pts = cx, cy, [(cx, cy)]
        ln = rng.uniform(20, 30)
        for s in range(int(ln / 3)):
            ang += rng.uniform(-0.55, 0.55)
            x += 3 * math.cos(ang)
            y += 3 * math.sin(ang)
            pts.append((x, y))
            if rng.random() < 0.18:
                b = ang + rng.choice((-1, 1)) * rng.uniform(0.6, 1.1)
                cracks.append([(x, y), (x + 5 * math.cos(b), y + 5 * math.sin(b))])
        cracks.append(pts)
    glow = (0x5F, 0xC8, 0xF0)
    for pts in cracks:
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
            for i in range(n + 1):
                t = i / n
                x, y = int(x0 + (x1 - x0) * t), int(y0 + (y1 - y0) * t)
                for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    _blend_px(px, w, h, x + ox, y + oy, glow, 110)
    for pts in cracks:
        wd = 2 if len(pts) > 4 else 1
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            _line(px, w, h, x0, y0, x1, y1, (4, 3, 10, 255), wd)
    for y in range(h):
        for x in range(w):
            if math.hypot(x - cx, y - cy) < 4.5:
                px[y * w + x] = (2, 1, 6, 255)
    return w, h, px


def paint_arc(k):
    w, h = TEX[f'arc_{k}']
    rng = random.Random(7400 + k)
    px = [(0, 0, 0, 0)] * (w * h)
    pts = [(16.0 + rng.uniform(-3, 3), 62.0)]
    y = 62.0
    while y > 3:
        y -= rng.uniform(5, 9)
        pts.append((min(27.0, max(4.0, pts[-1][0] + rng.uniform(-7, 7))), max(2.0, y)))
    branches = []
    for i in range(1, len(pts) - 1):
        if rng.random() < 0.35:
            x0, y0 = pts[i]
            x1 = min(30.0, max(1.0, x0 + rng.choice((-1, 1)) * rng.uniform(5, 10)))
            branches.append([(x0, y0), (x1, y0 - rng.uniform(3, 8))])
    glow, mid, core = (0x7F, 0xD8, 0xFF), (0xBF, 0xF0, 0xFF), (0xFF, 0xFF, 0xFF)
    for seg_pts, wd in [(pts, 2)] + [(b, 1) for b in branches]:
        for (x0, y0), (x1, y1) in zip(seg_pts, seg_pts[1:]):
            n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
            for i in range(n + 1):
                t = i / n
                x, yy = int(x0 + (x1 - x0) * t), int(y0 + (y1 - y0) * t)
                for ox in range(-2, 3):
                    for oy in range(-1, 2):
                        _blend_px(px, w, h, x + ox, yy + oy, glow, 90 if abs(ox) == 2 else 150)
            _line(px, w, h, x0, y0, x1, y1, mid + (255,), wd + 1)
            _line(px, w, h, x0, y0, x1, y1, core + (255,), wd)
    return w, h, px


PAINT = {'void': paint_void, 'rim': paint_rim, 'crack': paint_crack, **{f'arc_{k}': (lambda k=k: paint_arc(k)) for k in range(4)}}


def model_json(kind):
    tex = TEX_NS + kind
    w, h = TEX[kind]
    if kind == 'crack':                       # flat floor card (up / down faces)
        el = {'from': [0, 8, 0], 'to': [16, 8, 16], 'shade': False,
              'faces': {'up': {'uv': [0, 0, 16, 16], 'texture': '#0'}, 'down': {'uv': [0, 16, 16, 0], 'texture': '#0'}}}
    else:
        # vertical cards (billboard): the void at model z 7.6, the rim behind it at 8.4, the arcs in front at 7.2 (a
        # billboarded item_display turns model -z toward the camera: ItemDisplayRenderer's Ry180)
        z = {'void': 7.6, 'rim': 8.4}.get(kind, 7.2)
        half = 8.0 * w / h
        el = {'from': [round(8 - half, 4), 0, z], 'to': [round(8 + half, 4), 16, z], 'shade': False,
              'faces': {'north': {'uv': [0, 0, 16, 16], 'texture': '#0'}, 'south': {'uv': [16, 0, 0, 16], 'texture': '#0'}}}
    return {'ambientocclusion': False, 'textures': {'0': tex, 'particle': tex}, 'elements': [el]}


def build_resourcepack(rp):
    rp = Path(rp)
    px_total = atlas_px()
    assert px_total <= ATLAS_BUDGET, f'rift atlas budget: {px_total} > {ATLAS_BUDGET}'
    root = rp / 'assets/rlk'
    dirs = {'textures/rift': '.png', 'models/item/rift': '.json', 'items/rift': '.json'}
    for sub in dirs:
        d = root / sub
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob('*'):
            if old.stem not in TEX or old.suffix != dirs[sub]:
                old.unlink()
    for kind in TEX:
        w, h, px = PAINT[kind]()
        assert (w, h) == TEX[kind] and len(px) == w * h, kind
        (root / 'textures/rift' / f'{kind}.png').write_bytes(png_bytes(w, h, px))
        (root / 'models/item/rift' / f'{kind}.json').write_text(json.dumps(model_json(kind), separators=(',', ':')) + '\n',
                                                                encoding='utf-8')
        (root / 'items/rift' / f'{kind}.json').write_text(
            json.dumps({'model': {'type': 'minecraft:model', 'model': f'rlk:item/rift/{kind}'}}, separators=(',', ':')) + '\n',
            encoding='utf-8')
    ap = rp / 'assets/minecraft/atlases/items.json'
    atlas = json.loads(ap.read_text(encoding='utf-8')) if ap.exists() else {'sources': []}
    atlas['sources'] = [s for s in atlas['sources'] if not str(s.get('resource', '')).startswith(TEX_NS)
                        or s['resource'][len(TEX_NS):] in TEX]
    have = {s.get('sprite', s.get('resource')) for s in atlas['sources']}
    for kind in TEX:
        if TEX_NS + kind not in have:
            atlas['sources'].append({'type': 'minecraft:single', 'resource': TEX_NS + kind})
    ap.parent.mkdir(parents=True, exist_ok=True)
    ap.write_text(json.dumps(atlas, indent=2) + '\n', encoding='utf-8')
    return len(TEX), px_total


# ---------------------------------------------------------------------------------------------------------- datapack
def f(v):
    return L.num(round(v, 4)) + 'f'


def tr(x, y, z, s, sy=None, roll=None):
    sy = s if sy is None else sy
    lr = '[0f,0f,0f,1f]' if roll is None else f'{{angle:{f(roll)},axis:[0f,0f,1f]}}'
    return (f'transformation:{{translation:[{f(x)},{f(y)},{f(z)}],left_rotation:{lr},'
            f'scale:[{f(s)},{f(sy)},{f(s)}],right_rotation:[0f,0f,0f,1f]}}')


def item(kind):
    return f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{TEX_NS}{kind}"}}}}'


def ccall(name, args=None):
    return f'function {NS}{name}' + (f' {args}' if args else '')


SIZE = {1: 0.5, 2: 1.0}          # riftS 1 dormant (half size), 2 open


def look(sz):
    """{part tag: transformation text} of the rift at size factor sz (bottom kept: the centre moves with the size)."""
    c = 0.15 + (CENTRE - 0.15) * sz
    out = {
        'void': tr(0, c, 0, VOID_H * sz),
        'rim': tr(0, c, 0, VOID_H * RIM_K * sz),
        'crack': tr(0, 0.02, 0, CRACK_S * sz),
    }
    for i, (ax, ay) in enumerate(ARC_POS):
        out[f'arc{i}'] = tr(ax * sz, 0.15 + (ay - 0.15) * sz, 0.05, ARC_S * sz)
    return out


class Out:
    def __init__(self, root):
        self.fn = Path(root) / 'data/rlk/function'
        self.written = set()

    def w(self, name, text):
        p = self.fn / (name + '.mcfunction')
        p.parent.mkdir(parents=True, exist_ok=True)
        text = (text if isinstance(text, str) else '\n'.join(text)).strip('\n')
        for i, line in enumerate(text.split('\n'), 1):
            s = line.lstrip()
            if s.startswith('$'):
                assert '$(' in s, f'{name}:{i} macro line without $(var)'
            elif '$(' in s and not s.startswith('#'):
                raise AssertionError(f'{name}:{i} $(var) in a non-macro line')
        p.write_text(text + '\n', encoding='utf-8')
        self.written.add(p.resolve())

    def clean(self, owned_dirs, owned_files):
        n = 0
        for d in owned_dirs:
            d = self.fn / d
            if d.exists():
                for p in sorted(d.rglob('*.mcfunction')):
                    if p.resolve() not in self.written:
                        p.unlink()
                        n += 1
                for p in sorted(d.rglob('*'), reverse=True):
                    if p.is_dir() and not any(p.iterdir()):
                        p.rmdir()
        for fpath in owned_files:
            p = self.fn / (fpath + '.mcfunction')
            if p.exists() and p.resolve() not in self.written:
                p.unlink()
                n += 1
        return n


def zsel(tag, extra=''):
    """Entities of this rift (#riftZid room = the anchor's zid)."""
    return f'@e[tag={tag}{extra}] if score @s zid = #riftZid room'


def build_datapack(o):
    W = o.w
    # ------------------------------------------------------------------ init / forget / uninstall
    objs = ['riftS', 'riftT', 'riftCd', 'riftDw', 'riftPk', 'riftA', 'riftX', 'riftY', 'riftZ']
    W('room/rift/init', ['# From rlk:load (after mboss/init): the rift objectives, the run defaults, #riftOn re-derived from the world',
                         '# (/reload keeps every rift entity); a rift caught collapsing finishes now (its boxes fall), one caught',
                         '# growing is open, a queued show stays queued.']
      + [f'scoreboard objectives add {o_} dummy' for o_ in objs]
      + ['execute unless score #riftUsed room matches 0.. run scoreboard players set #riftUsed room 0',
         'execute unless score #riftForce room matches 0.. run scoreboard players set #riftForce room 0',
         'scoreboard players set #riftC2 room 2', 'scoreboard players set #riftC4 room 4', 'scoreboard players set #riftC8 room 8',
         'scoreboard players set #riftC40 room 40', 'scoreboard players set #riftC10 room 10',
         'execute as @e[type=minecraft:marker,tag=rlk_rift,scores={riftS=4}] at @s run ' + ccall('close_end'),
         'execute as @e[type=minecraft:marker,tag=rlk_rift,scores={riftS=5}] at @s run ' + ccall('open_now'),
         'scoreboard players set #riftOn room 0',
         'execute if entity @e[type=minecraft:marker,tag=rlk_rift,limit=1] run scoreboard players set #riftOn room 1',
         'execute if entity @e[type=minecraft:marker,tag=rlk_riftq,limit=1] run scoreboard players set #riftOn room 1'])
    W('room/rift/forget', ['# From room/clear (map change, run end, death, room/wipe): the rift entities went with rlk_room, so the tick',
                           '# stops. (#riftUsed stays: once per run; #riftForce stays armed until a zone takes it.)',
                           'scoreboard players set #riftOn room 0'])
    W('room/rift/uninstall', ['# From rlk:uninstall: every rift entity and the rift objectives (the #rift* fake players go with room).',
                              'kill @e[tag=rlk_rift_part]', 'kill @e[tag=rlk_rift]', 'tag @e[tag=rlk_riftz] remove rlk_riftz',
                              'tag @e[tag=rlk_riftq] remove rlk_riftq']
      + [f'scoreboard objectives remove {o_}' for o_ in objs]
      + ['scoreboard players reset #riftOn room', 'scoreboard players reset #riftForce room', 'scoreboard players reset #riftUsed room'])

    # ------------------------------------------------------------------ roll / arm (zone build)
    W('room/rift/roll', [
        '# From room/zone_build (@s = the zone marker, after zst 1): the rift roll of PLAN §7.1. A forced rift (test/rift,',
        '# rift_id, special) takes the next zone built of any kind but 9 (boss) / 15 (mid-boss), regardless of chance,',
        '# #riftUsed, map type, chapter or test state. Naturally: a run, no boss test, no rift yet this run, a combat room',
        '# (zkind 1), not the boss map, not chapter 1\'s first map, a special with w >= 1 enabled, not peaceful, then',
        '# #riftPm per mille.',
        'execute if score #riftForce room matches 1 unless score @s zkind matches 9 unless score @s zkind matches 15 run return run ' + ccall('arm'),
        'execute unless score #active room matches 1 run return 0',
        'execute if score #riftUsed room matches 1.. run return 0',
        'execute unless score @s zkind matches 1 run return 0',
        'execute if score #mapType room matches 8 run return 0',
        'execute if score #chapter room matches 1 if score #mapIdx room matches 0 run return 0',
        'execute if score #mbTest mb matches 1 run return 0',
        'execute if score #rdTest rd matches 1 run return 0',
        'execute unless score #spRoll mb matches 1.. run return 0',
        'execute store result score #riftDiff room run difficulty',
        'execute if score #riftDiff room matches 0 run return 0',
        'execute store result score #riftR room run random value 0..999',
        'execute if score #riftR room < #riftPm room run ' + ccall('arm')])
    W('room/rift/arm', [
        '# @s = the zone marker (rift/roll): the special of this rift (mboss/sp/roll: the test\'s fixed id first), zone tag',
        '# rlk_riftz + data.rift {id}, at most once per run (#riftUsed 1: it counts even if never entered), the force spent,',
        '# and mboss/sp/prep {id} (the special\'s arena forceloaded, its build job started now). No special: no rift.',
        'scoreboard players set #riftForce room 0',
        'execute unless function rlk:mboss/sp/roll run return 0',
        'tag @s add rlk_riftz',
        'scoreboard players set #riftUsed room 1',
        'data modify entity @s data.rift set value {}',
        'data modify entity @s data.rift.id set from storage rlk:mboss spid',
        'function rlk:mboss/sp/prep with entity @s data.rift'])

    # ------------------------------------------------------------------ show (zone enter / first zone)
    W('room/rift/show', [
        '# From room/zone_enter (after zst 2, before the combat return) and room/zone_first (last) on a rlk_riftz zone (@s =',
        '# the zone marker, at it). A combat room whose fight is still to come (zkind 1, zst <= 2) shows the rift at once,',
        '# dormant; any other zone queues the show for the next rift tick (rlk_riftq), when the zone\'s own objects exist and',
        '# the player stands where the map put them (the spot keeps its distances to both). Shown once per zone.',
        'scoreboard players operation #riftZid room = @s zid',
        'execute as @e[type=minecraft:marker,tag=rlk_rift] if score @s zid = #riftZid room run return 0',
        'execute if score @s zkind matches 1 if score @s zst matches ..2 run return run ' + ccall('show_now'),
        'tag @s add rlk_riftq',
        'scoreboard players set #riftOn room 1'])
    W('room/rift/show_now', [
        '# @s = the zone marker, at it: the spot (spot/pick: a marker rlk_riftc), then the anchor and its parts, dormant in a',
        '# combat room whose fight is still to come, else open.',
        'tag @s remove rlk_riftq',
        'scoreboard players operation #riftZid room = @s zid',
        'execute as @e[type=minecraft:marker,tag=rlk_rift] if score @s zid = #riftZid room run return 0',
        'scoreboard players set #riftSt room 2',
        'execute if score @s zkind matches 1 if score @s zst matches ..2 run scoreboard players set #riftSt room 1',
        'kill @e[type=minecraft:marker,tag=rlk_riftc]',
        ccall('spot/pick'),
        'execute as @e[type=minecraft:marker,tag=rlk_riftc,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_zone,tag=rlk_riftcz,limit=1] feet run tp @s ~ ~ ~ ~ 0',
        'tag @s remove rlk_riftcz',
        'execute as @e[type=minecraft:marker,tag=rlk_riftc,limit=1] at @s rotated as @s run ' + ccall('build'),
        'scoreboard players set #riftOn room 1'])
    lk1, lk2 = look(SIZE[1]), look(SIZE[2])
    parts = [
        ('void', 'vertical', '{sky:0,block:0}', 'void', lk1['void']),
        ('rim', 'vertical', '{sky:6,block:6}', 'rim', lk1['rim']),
        ('crack', 'fixed', '{sky:10,block:10}', 'crack', lk1['crack']),
    ] + [(f'arc{i}', 'center', '{sky:15,block:15}', f'arc_{i % 4}', lk1[f'arc{i}'] if i == 0 else tr(0, CENTRE, 0, 0))
         for i in range(3)]
    build = ['# @s = the new anchor (the rlk_riftc marker), at it, rotated toward the zone centre; #riftSt room = 1 dormant / 2',
             '# open; #riftZid room = its zone. The anchor becomes rlk_rift; the parts (rlk_rift_part, zid) are summoned dormant',
             '# and an open rift is opened at once (open_now: full size, the hover object) without the grow animation.',
             'tag @s remove rlk_riftc',
             'tag @s add rlk_rift',
             'scoreboard players operation @s zid = #riftZid room',
             'scoreboard players operation @s riftS = #riftSt room',
             'scoreboard players set @s riftT 0', 'scoreboard players set @s riftCd 0', 'scoreboard players set @s riftDw 0',
             'scoreboard players set @s riftPk 0',
             'execute store result score @s riftX run data get entity @s Pos[0] 100',
             'execute store result score @s riftY run data get entity @s Pos[1] 100',
             'execute store result score @s riftZ run data get entity @s Pos[2] 100']
    for tag, bb, br, kind, t in parts:
        extra = ',Rotation:[0f,0f]' if bb == 'fixed' else ''
        build.append(f'summon minecraft:item_display ~ ~ ~ {{Tags:["rlk_room","rlk_rift_part","rlk_rift_{tag}","rlk_rift_new"],'
                     f'billboard:"{bb}",brightness:{br},view_range:1.5f,shadow_radius:0f,interpolation_duration:0,{item(kind)},{t}{extra}}}')
    build += ['execute as @e[type=minecraft:item_display,tag=rlk_rift_new,tag=rlk_rift_crack] at @s run tp @s ~ ~ ~ ~ 0',
              'scoreboard players operation @e[tag=rlk_rift_new] zid = #riftZid room',
              'scoreboard players set @e[tag=rlk_rift_new,tag=rlk_rift_arc0] riftA 0',
              'scoreboard players set @e[tag=rlk_rift_new,tag=rlk_rift_arc1] riftA 1',
              'scoreboard players set @e[tag=rlk_rift_new,tag=rlk_rift_arc2] riftA 2',
              'tag @e[tag=rlk_rift_arc0,tag=rlk_rift_new] add rlk_rift_arc',
              'tag @e[tag=rlk_rift_arc1,tag=rlk_rift_new] add rlk_rift_arc',
              'tag @e[tag=rlk_rift_arc2,tag=rlk_rift_new] add rlk_rift_arc',
              'tag @e[tag=rlk_rift_new] remove rlk_rift_new',
              'execute if score @s riftS matches 2 run ' + ccall('open_now'),
              'execute if score @s riftS matches 1 run ' + ccall('snd/dormant')]
    W('room/rift/build', build)

    # ------------------------------------------------------------------ looks (data merge on the parts of this rift)
    def look_fn(name, lk, dur, br_rim, comment, hide_arcs=False):
        lines = [f'# @s = the anchor: {comment}', 'scoreboard players operation #riftZid room = @s zid']
        for tag in ('void', 'rim', 'crack'):
            extra = f',brightness:{br_rim}' if tag == 'rim' else ''
            lines.append(f'execute as {zsel("rlk_rift_" + tag)} run data merge entity @s '
                         f'{{start_interpolation:0,interpolation_duration:{dur}{extra},{lk[tag]}}}')
        for i in range(3):
            t = tr(0, CENTRE, 0, 0) if (hide_arcs and i) else lk[f'arc{i}']
            lines.append(f'execute as {zsel("rlk_rift_arc" + str(i))} run data merge entity @s '
                         f'{{start_interpolation:0,interpolation_duration:{min(dur, 4)},{t}}}')
        return lines
    W('room/rift/look/dormant', look_fn('dormant', lk1, 0, '{sky:6,block:6}', 'dormant (half size, dim rim, one arc).', True))
    W('room/rift/look/grow', look_fn('grow', lk2, GROW_T, '{sky:15,block:15}', f'grow to the open size over {GROW_T} t.'))
    W('room/rift/look/open', look_fn('open', lk2, 0, '{sky:15,block:15}', 'open at once (show of a quiet room, reopen, reload).'))
    lkc = look(0.02)
    W('room/rift/look/close', look_fn('close', lkc, CLOSE_T, '{sky:15,block:15}', f'collapse over {CLOSE_T} t (arcs snap in faster).'))
    pulse = look(1.0)
    pulse['rim'] = tr(0, 0.15 + (CENTRE - 0.15), 0, VOID_H * RIM_K * 1.18)
    W('room/rift/look/pulse', look_fn('pulse', pulse, 6, '{sky:15,block:15}', 'entering: the rim flares (6 t).'))
    W('room/rift/look/breathe', [
        '# @s = the anchor (open, every 20 t): the rim breathes between 0.97 and 1.03 of its size (#riftB room 0 / 1).',
        'scoreboard players operation #riftZid room = @s zid',
        'execute if score #riftB room matches 0 run execute as ' + zsel('rlk_rift_rim') + ' run data merge entity @s '
        f'{{start_interpolation:0,interpolation_duration:20,{tr(0, CENTRE, 0, VOID_H * RIM_K * 0.97)}}}',
        'execute if score #riftB room matches 1 run execute as ' + zsel('rlk_rift_rim') + ' run data merge entity @s '
        f'{{start_interpolation:0,interpolation_duration:20,{tr(0, CENTRE, 0, VOID_H * RIM_K * 1.03)}}}'])

    # ------------------------------------------------------------------ open / reopen / close / go (state changes)
    W('room/rift/open', [
        '# From room/combat_clear on a rlk_riftz zone (@s = the zone marker, at it; the room\'s own fight is over): its dormant',
        '# rift grows open (state 5 for 20 t, then 2).',
        'scoreboard players operation #riftZid room = @s zid',
        'execute as @e[type=minecraft:marker,tag=rlk_rift,scores={riftS=1}] if score @s zid = #riftZid room at @s run ' + ccall('grow')])
    W('room/rift/grow', [
        '# @s = a dormant anchor, at it: grow (20 t), burst, sounds.',
        'scoreboard players set @s riftS 5',
        'scoreboard players set @s riftT 0',
        ccall('look/grow'),
        f'particle minecraft:electric_spark ~ ~{L.num(CENTRE)} ~ 0.6 0.9 0.6 0.4 40',
        f'particle minecraft:end_rod ~ ~{L.num(CENTRE)} ~ 0.3 0.6 0.3 0.12 16',
        f'particle minecraft:flash{{color:[0.875f,0.965f,1f,1f]}} ~ ~{L.num(CENTRE)} ~ 0 0 0 0 1',
        L.sound('entity.lightning_bolt.thunder', 0.4, 1.6, source='block'),
        L.sound('block.end_portal.spawn', 0.5, 1.3, source='block')])
    W('room/rift/open_now', [
        '# @s = an anchor, at it: open now (the grow finished; /reload during the grow; a reopen): state 2, the hover object.',
        'scoreboard players set @s riftS 2',
        'scoreboard players set @s riftT 0',
        'scoreboard players set @s riftDw 0',
        ccall('look/open'),
        'scoreboard players operation #riftZid room = @s zid',
        'scoreboard players set #riftHas room 0',
        'execute as ' + zsel('rlk_rift_obj', ',type=minecraft:marker') + ' run scoreboard players set #riftHas room 1',
        'execute if score #riftHas room matches 0 run function rlk:room/obj/k_rift'])
    W('room/rift/reopen', [
        '# From mboss/sp/won_cancel (@s = the anchor, at it): the fight was cancelled, the rift is open again; the returning',
        f'# player (1.2 - 2 b in front of it) gets {REOPEN_CD} t before a walk-in counts.',
        ccall('open_now'),
        f'scoreboard players set @s riftCd {REOPEN_CD}',
        L.sound('block.end_portal.spawn', 0.4, 1.5, source='block')])
    W('room/rift/go', [
        '# From mboss/sp/g/<id> (@s = the anchor, at it): the fight starts. The hover object goes, the rift flares (state 3,',
        f'# entering), the player is pulled onto the anchor (the spot is a checked 3 x 3 floor with 3 b of headroom) with',
        f'# blindness at {BLIND_T} t; mboss/start_go moves the player into the arena at #spawnT 30.',
        'scoreboard players set @s riftS 3',
        'scoreboard players set @s riftT 0',
        'scoreboard players set @s riftDw 0',
        'scoreboard players operation #riftZid room = @s zid',
        'execute as ' + zsel('rlk_rift_obj') + ' run kill @s',
        ccall('look/pulse'),
        'tp @a[tag=player,limit=1] ~ ~ ~',
        'tp @e[tag=rlk_safe,limit=1] ~ ~ ~',
        'execute as @a[tag=player,limit=1] run function rlk:view/sync',
        L.sound('block.portal.trigger', 0.5, 1.0, source='block'),
        L.sound('entity.enderman.teleport', 0.8, 0.6, source='block'),
        f'particle minecraft:reverse_portal ~ ~{L.num(CENTRE)} ~ 0.8 1.0 0.8 0.05 40'])
    W('room/rift/close', [
        f'# From mboss/sp/reward (@s = the anchor, at it; #spPk mb = the boxes): the collapse ({CLOSE_T} t: the rim shrinks, the arcs',
        '# snap inward, an implosion), then room/rift/close_end drops the boxes on the spot and removes the rift.',
        'scoreboard players set @s riftS 4',
        'scoreboard players set @s riftT 0',
        'scoreboard players operation @s riftPk = #spPk mb',
        'scoreboard players operation #riftZid room = @s zid',
        'execute as ' + zsel('rlk_rift_obj') + ' run kill @s',
        ccall('look/close'),
        L.sound('block.respawn_anchor.deplete', 0.8, 1.0, source='block'),
        L.sound('block.beacon.deactivate', 0.6, 1.0, source='block')])
    W('room/rift/close_end', [
        '# @s = a collapsing anchor, at it (tick 30, or /reload during the collapse): the implosion, the reward boxes',
        '# (mboss/box/drop_all with #mbPk = riftPk, as the anchor at the spot), then every entity of this rift goes. The zone',
        '# keeps rlk_riftdone.',
        f'particle minecraft:reverse_portal ~ ~{L.num(CENTRE)} ~ 0.3 0.5 0.3 0.6 60',
        f'particle minecraft:flash{{color:[0.875f,0.965f,1f,1f]}} ~ ~{L.num(CENTRE)} ~ 0 0 0 0 1',
        'scoreboard players operation #mbPk mb = @s riftPk',
        'execute if score #mbPk mb matches 1.. run function rlk:mboss/box/drop_all',
        'scoreboard players operation #riftZid room = @s zid',
        'execute as ' + zsel('rlk_rift_part') + ' run kill @s',
        'kill @s'])

    # ------------------------------------------------------------------ the hover object (room/obj/k_rift, oact 17)
    W('room/obj/k_rift', [
        '# 균열 오브젝트 (위치 = 균열 표식 = 바닥, @s = 그 표식): 조준 표시용 표식(oact 17) + 이름표 "균열" + 안내 줄("▶ 좌클릭",',
        '# room/obj/hover). 좌클릭 → room/obj/click → room/rift/click → room/rift/enter. 균열의 모습(rlk_rift_part)은 이 묶음이',
        '# 아니라서 kill_group 이 지우지 않는다. 열린 균열에만 있다(room/rift/open_now 가 만들고 go · close 가 지움). tools/build_rift.py 가 만듦',
        'scoreboard players operation #riftZid room = @s zid',
        f'summon minecraft:marker ~ ~{L.num(CENTRE)} ~ {{Tags:["rlk_room","rlk_obj","rlk_rift_part","rlk_rift_obj","rlk_rift_onew"]}}',
        f'summon minecraft:text_display ~ ~{L.num(CENTRE + 1.75)} ~ {{Tags:["rlk_room","rlk_olbl","rlk_rift_part","rlk_rift_obj","rlk_rift_onew"],'
        'billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:{text:"균열",color:"white",bold:true},'
        'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}',
        f'summon minecraft:text_display ~ ~{L.num(CENTRE + 1.45)} ~ {{Tags:["rlk_room","rlk_ohint","rlk_rift_part","rlk_rift_obj","rlk_rift_onew"],'
        'billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:{text:""},'
        'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}',
        'execute store result score #ogid room run scoreboard players add #ogid room 1',
        'scoreboard players operation @e[tag=rlk_rift_onew] ogid = #ogid room',
        'scoreboard players operation @e[tag=rlk_rift_onew] zid = #riftZid room',
        'scoreboard players set @e[tag=rlk_rift_onew,type=minecraft:marker] oact 17',
        'scoreboard players set @e[tag=rlk_rift_onew,type=minecraft:marker] oarg 0',
        'tag @e[tag=rlk_rift_onew] remove rlk_rift_onew'])
    W('room/rift/click', [
        '# From room/obj/click (oact 17; @s = the rift\'s hover object, at it; clicks during combat are refused there): the',
        '# rift of this zone is entered.',
        'scoreboard players operation #riftZid room = @s zid',
        'execute as @e[type=minecraft:marker,tag=rlk_rift] if score @s zid = #riftZid room at @s run ' + ccall('enter')])
    W('room/rift/enter', [
        '# @s = the anchor, at it (walk-in dwell, click, the test\'s auto-enter): an open rift, no cooldown, no combat, a',
        f'# living player outside the selection space -> mboss/sp/gate. Refused there: the rift holds for {REFUSE_CD} t.',
        'execute unless score @s riftS matches 2 run return 0',
        'execute if score @s riftCd matches 1.. run return 0',
        'execute if score #combat room matches 1.. run return 0',
        'execute if entity @a[tag=player,scores={dead=1}] run return 0',
        'execute if entity @a[tag=player,scores={pkMode=1..}] run return 0',
        'scoreboard players set @s riftDw 0',
        'execute store result score #riftG room run function rlk:mboss/sp/gate',
        f'execute unless score #riftG room matches 1 run scoreboard players set @s riftCd {REFUSE_CD}'])

    # ------------------------------------------------------------------ tick
    W('room/rift/tick', [
        '# From room/tick while #riftOn room is 1 (the run is active): every rift of the map, and the queued shows.',
        'scoreboard players set #riftOn room 0',
        'execute as @e[type=minecraft:marker,tag=rlk_rift] at @s run ' + ccall('t/one'),
        'execute as @e[type=minecraft:marker,tag=rlk_riftq] at @s run ' + ccall('show_now')])
    W('room/rift/t/one', [
        '# @s = an anchor, at it: the clock and the state (1 dormant, 2 open, 3 entering, 4 collapsing, 5 growing).',
        'scoreboard players set #riftOn room 1',
        'scoreboard players add @s riftT 1',
        'execute if score @s riftCd matches 1.. run scoreboard players remove @s riftCd 1',
        'scoreboard players operation #riftZid room = @s zid',
        'scoreboard players operation #riftQ room = @s riftT',
        'scoreboard players operation #riftQ room %= #riftC2 room',
        'execute if score @s riftS matches 1 run return run ' + ccall('t/dormant'),
        'execute if score @s riftS matches 2 run return run ' + ccall('t/open'),
        'execute if score @s riftS matches 3 run return run ' + ccall('t/enter'),
        'execute if score @s riftS matches 4 run return run ' + ccall('t/close'),
        'execute if score @s riftS matches 5 run return run ' + ccall('t/grow')])
    W('room/rift/t/dormant', [
        '# Dormant (the room\'s fight runs): one slow arc, a third of the open particles (every 6 t), not enterable.',
        'scoreboard players operation #riftQ room = @s riftT',
        'scoreboard players set #riftK room 6',
        'scoreboard players operation #riftQ room %= #riftK room',
        'execute if score #riftQ room matches 0 run ' + ccall('fx/arcs'),
        'execute if score #riftQ room matches 0 run ' + ccall('fx/dust')])
    W('room/rift/t/open', [
        '# Open: arcs every 2 t (frame) / 4 t (roll), particles every 2 t, the rim breathing every 20 t, ambient sound every',
        f'# 40 t; the walk-in dwell ({DWELL} t within 1 b horizontal and 1.5 b vertical).',
        'execute if score #riftQ room matches 0 run ' + ccall('fx/arcs'),
        'execute if score #riftQ room matches 0 run ' + ccall('fx/open'),
        'scoreboard players operation #riftQ room = @s riftT',
        'scoreboard players operation #riftQ room %= #riftC40 room',
        'execute if score #riftQ room matches 0 run ' + ccall('fx/ambient'),
        'execute if score #riftQ room matches 0 run scoreboard players set #riftB room 0',
        'execute if score #riftQ room matches 20 run scoreboard players set #riftB room 1',
        'execute if score #riftQ room matches 0 run ' + ccall('look/breathe'),
        'execute if score #riftQ room matches 20 run ' + ccall('look/breathe'),
        ccall('dwell')])
    W('room/rift/dwell', [
        '# @s = an open anchor, at it: the player body within 1.0 b horizontal and |dy| < 1.5 b for 10 consecutive ticks while',
        '# no combat, alive, outside the selection space and the map screen -> room/rift/enter.',
        'execute unless score #combat room matches 0 run return run scoreboard players set @s riftDw 0',
        'execute if score @s riftCd matches 1.. run return run scoreboard players set @s riftDw 0',
        'execute unless entity @e[tag=rlk_body,distance=..1.81,limit=1] run return run scoreboard players set @s riftDw 0',
        'execute if entity @a[tag=player,scores={dead=1}] run return run scoreboard players set @s riftDw 0',
        'execute if entity @a[tag=player,scores={pkMode=1..}] run return run scoreboard players set @s riftDw 0',
        'execute if entity @a[tag=player,scores={vMap=1}] run return run scoreboard players set @s riftDw 0',
        'execute unless function rlk:room/rift/near run return run scoreboard players set @s riftDw 0',
        'scoreboard players add @s riftDw 1',
        'execute at @e[tag=rlk_body,limit=1] run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.5 0.3 0.4 4',
        'execute if score @s riftDw matches 1 run ' + L.sound('block.portal.ambient', 0.3, 1.8, source='block'),
        f'execute if score @s riftDw matches {DWELL}.. run ' + ccall('enter')])
    W('room/rift/near', [
        '# @s = the anchor: 1 when the player body is within 1.0 b horizontal and |dy| < 1.5 b of it (positions x100), else fail.',
        'execute store result score #riftBx room run data get entity @e[tag=rlk_body,limit=1] Pos[0] 100',
        'execute store result score #riftBy room run data get entity @e[tag=rlk_body,limit=1] Pos[1] 100',
        'execute store result score #riftBz room run data get entity @e[tag=rlk_body,limit=1] Pos[2] 100',
        'scoreboard players operation #riftBx room -= @s riftX',
        'scoreboard players operation #riftBy room -= @s riftY',
        'scoreboard players operation #riftBz room -= @s riftZ',
        'execute unless score #riftBy room matches -149..149 run return fail',
        'execute unless score #riftBx room matches -100..100 run return fail',
        'execute unless score #riftBz room matches -100..100 run return fail',
        'scoreboard players operation #riftBx room *= #riftBx room',
        'scoreboard players operation #riftBz room *= #riftBz room',
        'scoreboard players operation #riftBx room += #riftBz room',
        'execute if score #riftBx room matches 10001.. run return fail',
        'return 1'])
    W('room/rift/t/grow', [
        f'# Growing ({GROW_T} t): sparks pour out, the arcs flicker; then open.',
        'execute if score #riftQ room matches 0 run ' + ccall('fx/arcs'),
        'execute if score #riftQ room matches 0 run ' + ccall('fx/open'),
        f'execute if score @s riftT matches {GROW_T}.. run ' + ccall('open_now')])
    W('room/rift/t/enter', [
        f'# Entering (the fight starts; the rift stays lit until the fight ends): the flare settles at 6 t, blindness at {BLIND_T} t.',
        'execute if score #riftQ room matches 0 run ' + ccall('fx/arcs'),
        'execute if score #riftQ room matches 0 run ' + ccall('fx/open'),
        'execute if score @s riftT matches 6 run ' + ccall('look/open'),
        f'execute if score @s riftT matches {BLIND_T} run effect give @a[tag=player] minecraft:blindness 2 0 true',
        f'execute if score @s riftT matches ..{BLIND_T} at @e[tag=rlk_body,limit=1] run particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.6 0.4 0.6 6'])
    W('room/rift/t/close', [
        f'# Collapsing ({CLOSE_T} t): sparks pulled in, the implosion at the end (close_end).',
        f'execute if score #riftQ room matches 0 run particle minecraft:reverse_portal ~ ~{L.num(CENTRE)} ~ 0.7 1.0 0.7 0.3 8',
        f'execute if score #riftQ room matches 0 run particle minecraft:electric_spark ~ ~{L.num(CENTRE)} ~ 0.3 0.5 0.3 0.05 3',
        f'execute if score @s riftT matches {CLOSE_T}.. run ' + ccall('close_end')])
    # arcs: frame every 2 t, roll every 4 t (dormant: arc 0 only)
    W('room/rift/fx/arcs', [
        '# @s = the anchor (every 2 t open / growing / entering, every 6 t dormant): the arc frames and their roll.',
        'scoreboard players operation #riftF room = @s riftT',
        'scoreboard players operation #riftF room /= #riftC2 room',
        'scoreboard players operation #riftRl room = #riftF room',
        'scoreboard players operation #riftRl room %= #riftC2 room',
        'scoreboard players operation #riftSt room = @s riftS',
        'execute as ' + zsel('rlk_rift_arc', ',type=minecraft:item_display') + ' run ' + ccall('fx/arc')])
    arc = ['# @s = an arc card: frame (#riftF + riftA) mod 4; every second call a new roll angle. Dormant: arcs 1 and 2 rest.',
           'execute if score #riftSt room matches 1 unless score @s riftA matches 0 run return 0',
           'scoreboard players operation #riftAf room = #riftF room',
           'scoreboard players operation #riftAf room += @s riftA',
           'scoreboard players operation #riftAf room %= #riftC4 room']
    for k in range(4):
        arc.append(f'execute if score #riftAf room matches {k} run data modify entity @s item.components."minecraft:item_model" set value "{TEX_NS}arc_{k}"')
    arc += ['execute if score #riftRl room matches 1 run return 0',
            'execute store result score #riftAr room run random value 0..7']
    for k, a in enumerate(ARC_ROLLS):
        arc.append(f'execute if score #riftAr room matches {k} run data merge entity @s {{transformation:{{left_rotation:{{angle:{f(a)},axis:[0f,0f,1f]}}}}}}')
    W('room/rift/fx/arc', arc)
    fo = ['# @s = the anchor (every 2 t): electric sparks on two rim points, an end rod drifting, ink at the edge, reverse portal',
          '# pulled in. The rim points are in the plane facing the player (rotated toward them, pitch 0).',
          'scoreboard players operation #riftP room = @s riftT',
          'scoreboard players operation #riftP room /= #riftC2 room',
          'scoreboard players operation #riftP room %= #riftC4 room',
          'execute facing entity @a[tag=player,limit=1] feet rotated ~ 0 run ' + ccall('fx/rim')]
    W('room/rift/fx/open', fo + [
        f'particle minecraft:end_rod ~ ~{L.num(CENTRE)} ~ 0.5 0.8 0.5 0.01 1',
        f'particle minecraft:reverse_portal ~ ~{L.num(CENTRE)} ~ 0.7 1.0 0.7 0.2 2'])
    rim = ['# Rotated toward the player: the rim points k and k + 4 (k = #riftP room) get a spark each, k gets an ink puff.']
    for k in range(4):
        for j in (k, k + 4):
            x, y = RIM_PTS[j]
            rim.append(f'execute if score #riftP room matches {k} positioned ^{L.num(round(x, 3))} ^{L.num(round(y, 3))} ^ run '
                       'particle minecraft:electric_spark ~ ~ ~ 0.05 0.05 0.05 0.03 1')
        x, y = RIM_PTS[k]
        rim.append(f'execute if score #riftP room matches {k} positioned ^{L.num(round(x * 0.92, 3))} ^{L.num(round(y, 3))} ^ run '
                   'particle minecraft:squid_ink ~ ~ ~ 0.02 0.02 0.02 0.005 1')
    W('room/rift/fx/rim', rim)
    W('room/rift/fx/dust', [
        '# Dormant (every 6 t): the open particle set at half size.',
        f'particle minecraft:electric_spark ~ ~{L.num(0.15 + (CENTRE - 0.15) * 0.5)} ~ 0.3 0.45 0.3 0.03 2',
        f'particle minecraft:end_rod ~ ~{L.num(0.15 + (CENTRE - 0.15) * 0.5)} ~ 0.25 0.4 0.25 0.01 1',
        f'particle minecraft:reverse_portal ~ ~{L.num(0.15 + (CENTRE - 0.15) * 0.5)} ~ 0.35 0.5 0.35 0.1 2'])
    W('room/rift/fx/ambient', [
        '# Open (every 40 t): the hum, and half the time a crackle.',
        L.sound('block.respawn_anchor.ambient', 0.6, 1.0, source='block'),
        'execute store result score #riftR room run random value 0..1',
        'execute if score #riftR room matches 1 run ' + L.sound('entity.lightning_bolt.impact', 0.15, 1.9, source='block')])
    W('room/rift/snd/dormant', [
        '# A dormant rift appears (the room\'s fight is about to start): a low crackle.',
        L.sound('entity.lightning_bolt.impact', 0.2, 1.4, source='block'),
        L.sound('block.respawn_anchor.ambient', 0.5, 0.8, source='block')])

    # ------------------------------------------------------------------ spot (PLAN §7.4)
    W('room/rift/spot/pick', [
        f'# @s = the zone marker, at it: up to {TRIES} random cell points of the zone (as room/mob_try), the ground found as',
        '# room/mob_up; accepted when spot/check passes. Fallback: the zone centre ground, then 2 b in front of the player\'s',
        '# rlk_safe spot. Result: one marker rlk_riftc at the spot, #riftWay room = 1 random / 2 centre / 3 safe / 0 none;',
        '# the zone is tagged rlk_riftcz (the anchor turns toward it).',
        'tag @s add rlk_riftcz',
        'scoreboard players set #riftTry room 0',
        'scoreboard players set #riftWay room 0',
        # node zones keep their central object group clear
        'scoreboard players set #riftCr room 0']
      + [f'execute if score @s zkind matches {k} run scoreboard players set #riftCr room {int(round((r * 10) ** 2))}' for k, r in NODE_R.items()]
      + [f'execute if score #riftCr room matches 0 unless score @s zkind matches 0..1 run scoreboard players set #riftCr room '
         f'{int(round((NODE_R_DEFAULT * 10) ** 2))}']
      + ['execute store result score #riftCx room run data get entity @s Pos[0] 10',
         'execute store result score #riftCz room run data get entity @s Pos[2] 10',
         ccall('spot/try'),
         'execute if score #riftWay room matches 0 positioned ~0.5 ~ ~0.5 run ' + ccall('spot/centre'),
         'execute if score #riftWay room matches 0 run ' + ccall('spot/safe')])
    W('room/rift/spot/try', [
        '# One try (recursive): a random cell, a random point inside its walls (>= 3 b from a wall face), the ground, the check.',
        'scoreboard players add #riftTry room 1',
        f'execute if score #riftTry room matches {TRIES + 1}.. run return 0',
        'function rlk:room/mob_cell with entity @s data',
        'function rlk:room/mob_cell2 with storage rlk:room a',
        ccall('spot/range'),
        'execute if score #riftRg room matches 1 run ' + ccall('spot/at', 'with storage rlk:room rsp'),
        'execute if score #riftWay room matches 1 run return 1',
        ccall('spot/try')])
    rng_lines = ['# The cell rlk:room sc: x / z ranges of block centres >= 3 b inside its wall faces (a side whose sx equals ix is an',
                 '# open join to the next cell: its whole spawn range counts). #riftRg room 0 when the cell is too small.',
                 'scoreboard players set #riftRg room 0']
    for ax in ('x', 'z'):
        rng_lines += [
            f'execute store result score #riftS0 room run data get storage rlk:room sc.s{ax}0',
            f'execute store result score #riftS1 room run data get storage rlk:room sc.s{ax}1',
            f'execute store result score #riftI0 room run data get storage rlk:room sc.i{ax}0',
            f'execute store result score #riftI1 room run data get storage rlk:room sc.i{ax}1',
            f'scoreboard players operation #riftLo room = #riftS0 room',
            f'execute if score #riftS0 room > #riftI0 room run scoreboard players operation #riftLo room = #riftI0 room',
            f'execute if score #riftS0 room > #riftI0 room run scoreboard players add #riftLo room {int(math.ceil(WALL_IN - 0.5))}',
            f'scoreboard players operation #riftHi room = #riftS1 room',
            f'execute if score #riftS1 room < #riftI1 room run scoreboard players operation #riftHi room = #riftI1 room',
            f'execute if score #riftS1 room < #riftI1 room run scoreboard players remove #riftHi room {int(math.ceil(WALL_IN - 0.5))}',
            'execute if score #riftLo room > #riftHi room run return 0',
            f'execute store result storage rlk:room rsr.{ax}0 int 1 run scoreboard players get #riftLo room',
            f'execute store result storage rlk:room rsr.{ax}1 int 1 run scoreboard players get #riftHi room']
    rng_lines += [ccall('spot/rand', 'with storage rlk:room rsr'),
                  'data modify storage rlk:room rsp.y set from entity @s data.cy',
                  'scoreboard players set #riftRg room 1']
    W('room/rift/spot/range', rng_lines)
    W('room/rift/spot/rand', ['$execute store result storage rlk:room rsp.x int 1 run random value $(x0)..$(x1)',
                              '$execute store result storage rlk:room rsp.z int 1 run random value $(z0)..$(z1)'])
    W('room/rift/spot/at', [
        '# {x,y,z} (@s = the zone marker): the block centre of the candidate, the ground found upward (<= 5 b, as room/mob_up).',
        'scoreboard players set #riftU room 0',
        '$execute positioned $(x) $(y) $(z) positioned ~0.5 ~ ~0.5 run ' + ccall('spot/up')])
    W('room/rift/spot/up', [
        'scoreboard players add #riftU room 1',
        'execute if score #riftU room matches 7.. run return 0',
        'execute unless block ~ ~ ~ #rlk:dash_pass positioned ~ ~1 ~ run return run ' + ccall('spot/up'),
        'execute if function rlk:room/rift/spot/check run ' + ccall('spot/accept', '{way:1}')])
    chk = ['# At a candidate (block centre, feet = the ground found): 1 when the rift may stand here, else fail. A 3 x 3 footprint',
           '# of solid floor (not #rlk:no_spawn, leaves, logs; theme 4 house floors excluded as room/mob_up) at the same y with 3 b',
           '# of #rlk:dash_pass above all nine and no water / lava; not over a pit (zone data.pits, its warning box); >= 4.5 b',
           '# from every door, >= 3.5 b from every room object (rlk_obj, rlk_odisp, the fountain of XP), >= 5 b from the player',
           '# (horizontal); a node zone keeps its centre clear.']
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            p = f'~{dx if dx else ""} ~{{}} ~{dz if dz else ""}'
            chk += [f'execute if block {p.format("-1")} #rlk:dash_pass run return fail',
                    f'execute unless block {p.format("")} #rlk:dash_pass run return fail',
                    f'execute unless block {p.format("1")} #rlk:dash_pass run return fail',
                    f'execute unless block {p.format("2")} #rlk:dash_pass run return fail',
                    f'execute if block {p.format("")} minecraft:water run return fail',
                    f'execute if block {p.format("")} minecraft:lava run return fail',
                    f'execute if block {p.format("-1")} #rlk:no_spawn run return fail',
                    f'execute if block {p.format("-1")} #minecraft:leaves run return fail',
                    f'execute if block {p.format("-1")} #minecraft:logs run return fail',
                    f'execute if score #th room matches 4 if block {p.format("-1")} minecraft:spruce_planks run return fail']
    chk += [
        'execute store result score #riftPx room run data get storage rlk:room rsp.x',
        'execute store result score #riftPz room run data get storage rlk:room rsp.z',
        'execute unless function rlk:room/rift/spot/pits run return fail',
        '# distances (tenths, horizontal): the candidate centre',
        'scoreboard players operation #riftQx room = #riftPx room',
        'scoreboard players operation #riftQx room *= #riftC10 room',
        'scoreboard players add #riftQx room 5',
        'scoreboard players operation #riftQz room = #riftPz room',
        'scoreboard players operation #riftQz room *= #riftC10 room',
        'scoreboard players add #riftQz room 5',
        'scoreboard players set #riftBad room 0',
        f'scoreboard players set #riftRr room {int(round((DOOR_R * 10) ** 2))}',
        'execute as @e[tag=rlk_door] run ' + ccall('spot/far'),
        f'scoreboard players set #riftRr room {int(round((OBJ_R * 10) ** 2))}',
        'execute as @e[tag=rlk_obj] run ' + ccall('spot/far'),
        'execute as @e[tag=rlk_odisp] run ' + ccall('spot/far'),
        'execute as @e[tag=rlk_xpspot] run ' + ccall('spot/far'),
        'execute as @e[tag=rlk_xpsrc] run ' + ccall('spot/far'),
        f'scoreboard players set #riftRr room {int(round((PLAYER_R * 10) ** 2))}',
        'execute as @e[tag=rlk_body] run ' + ccall('spot/far'),
        'execute if score #riftBad room matches 1 run return fail',
        'execute if score #riftCr room matches 1.. run ' + ccall('spot/node'),
        'execute if score #riftBad room matches 1 run return fail',
        'return 1']
    W('room/rift/spot/check', chk)
    W('room/rift/spot/far', [
        '# @s = a door / object / the player: #riftBad room 1 when it is closer (horizontal) than sqrt(#riftRr) tenths.',
        'execute store result score #riftEx room run data get entity @s Pos[0] 10',
        'execute store result score #riftEz room run data get entity @s Pos[2] 10',
        'scoreboard players operation #riftEx room -= #riftQx room',
        'scoreboard players operation #riftEz room -= #riftQz room',
        'scoreboard players operation #riftEx room *= #riftEx room',
        'scoreboard players operation #riftEz room *= #riftEz room',
        'scoreboard players operation #riftEx room += #riftEz room',
        'execute if score #riftEx room < #riftRr room run scoreboard players set #riftBad room 1'])
    W('room/rift/spot/node', [
        '# A node zone: the candidate must keep sqrt(#riftCr) tenths from the zone centre (#riftCx / #riftCz).',
        'scoreboard players operation #riftEx room = #riftCx room',
        'scoreboard players operation #riftEz room = #riftCz room',
        'scoreboard players operation #riftEx room -= #riftQx room',
        'scoreboard players operation #riftEz room -= #riftQz room',
        'scoreboard players operation #riftEx room *= #riftEx room',
        'scoreboard players operation #riftEz room *= #riftEz room',
        'scoreboard players operation #riftEx room += #riftEz room',
        'execute if score #riftEx room < #riftCr room run scoreboard players set #riftBad room 1'])
    W('room/rift/spot/pits', [
        '# @s = the zone marker: 1 when the 3 x 3 footprint (#riftPx / #riftPz +- 1) stays off every pit warning box, else fail.',
        'data modify storage rlk:room rpq set value []',
        'data modify storage rlk:room rpq set from entity @s data.pits',
        'scoreboard players operation #riftA0 room = #riftPx room',
        'scoreboard players add #riftA0 room 1',
        'scoreboard players operation #riftA1 room = #riftPx room',
        'scoreboard players remove #riftA1 room 1',
        'scoreboard players operation #riftA2 room = #riftPz room',
        'scoreboard players add #riftA2 room 1',
        'scoreboard players operation #riftA3 room = #riftPz room',
        'scoreboard players remove #riftA3 room 1',
        'return run ' + ccall('spot/pit_loop')])
    W('room/rift/spot/pit_loop', [
        'execute unless data storage rlk:room rpq[0] run return 1',
        'execute store result score #riftW0 room run data get storage rlk:room rpq[0].wx0',
        'execute store result score #riftW1 room run data get storage rlk:room rpq[0].wz0',
        'execute store result score #riftW2 room run data get storage rlk:room rpq[0].wx1',
        'execute store result score #riftW3 room run data get storage rlk:room rpq[0].wz1',
        'execute if score #riftA0 room >= #riftW0 room if score #riftA1 room <= #riftW2 room if score #riftA2 room >= #riftW1 room '
        'if score #riftA3 room <= #riftW3 room run return fail',
        'data remove storage rlk:room rpq[0]',
        'return run ' + ccall('spot/pit_loop')])
    W('room/rift/spot/accept', [
        '# {way} at the accepted spot: the marker rlk_riftc (the anchor to be), #riftWay room = way.',
        'summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_riftc"]}',
        '$scoreboard players set #riftWay room $(way)'])
    W('room/rift/spot/centre', [
        '# Fallback 1 (at the zone centre block): the ground found upward as room/mob_up (free feet and head, a floor).',
        'scoreboard players set #riftU room 0',
        ccall('spot/cup')])
    W('room/rift/spot/cup', [
        'scoreboard players add #riftU room 1',
        'execute if score #riftU room matches 7.. run return 0',
        'execute unless block ~ ~ ~ #rlk:dash_pass positioned ~ ~1 ~ run return run ' + ccall('spot/cup'),
        'execute unless block ~ ~1 ~ #rlk:dash_pass run return 0',
        'execute if block ~ ~-1 ~ #rlk:dash_pass run return 0',
        ccall('spot/accept', '{way:2}')])
    W('room/rift/spot/safe', [
        '# Fallback 2: 2 b in front of the player\'s last safe footing (rlk_safe), facing as the player.',
        'execute at @e[tag=rlk_safe,limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ^ ^ ^2 run '
        + ccall('spot/accept', '{way:3}')])
    return None


# ---------------------------------------------------------------------------------------------------------- hooks
# (file, mode, anchor, line): the anchor is a line of the hand-written base file (never another generator's line).
HOOKS = [
    ('room/zone_build', 'after', 'scoreboard players set @s zst 1', 'function rlk:room/rift/roll'),
    ('room/zone_enter', 'after', 'scoreboard players set @s zst 2',
     'execute if entity @s[tag=rlk_riftz] at @s run function rlk:room/rift/show'),
    ('room/zone_first', 'end', None, 'execute if entity @s[tag=rlk_riftz] at @s run function rlk:room/rift/show'),
    ('room/combat_clear', 'before', '# 챕터 보스 구역: 경기장 정리 → 귀환 → 처치했으면 다음 챕터 오브젝트, 취소면 문이 다시 나타남(mboss/cb/clear)',
     'execute if entity @s[tag=rlk_riftz] if score #spOn mb matches 1 run return run function rlk:mboss/sp/clear'),
    ('room/combat_clear', 'before', '# 챕터 보스 구역: 경기장 정리 → 귀환 → 처치했으면 다음 챕터 오브젝트, 취소면 문이 다시 나타남(mboss/cb/clear)',
     'execute if entity @s[tag=rlk_riftz] run function rlk:room/rift/open'),
    ('room/mob_wave', 'after', '# 적 소환 (@s = 구역 표식, at @s). 수 = 구역 크기별 범위 + (챕터 - 1)',
     'execute if entity @s[tag=rlk_riftz] if score #spOn mb matches 1 run return run function rlk:mboss/sp/start_zone'),
    ('room/obj/click', 'after', 'execute if score @s oact matches 16 run return run function rlk:mboss/cb/gate',
     'execute if score @s oact matches 17 run return run function rlk:room/rift/click'),
    ('room/tick', 'after', 'execute if score #mbBoxOn mb matches 1 run function rlk:mboss/box/all',
     'execute if score #riftOn room matches 1 run function rlk:room/rift/tick'),
    ('room/clear', 'after', 'function rlk:mboss/cleanup', 'function rlk:room/rift/forget'),
    ('run/start', 'after', 'scoreboard players set #mirUsed room 0', 'scoreboard players set #riftUsed room 0'),
    ('load', 'after', '# ===== 조절 지점 =====', f'scoreboard players set #riftPm room {RIFT_PM}'),
    ('load', 'after', 'function rlk:mboss/init', 'function rlk:room/rift/init'),
    ('uninstall', 'after', 'function rlk:mboss/uninstall', 'function rlk:room/rift/uninstall'),
]


def install_hooks(fn_root):
    """Remove every marked line (the marker comment and the line after it), then insert HOOKS again. Returns the files
    that changed."""
    fn_root = Path(fn_root)
    changed = []
    by_file = {}
    for h in HOOKS:
        by_file.setdefault(h[0], []).append(h)
    for rel, hooks in by_file.items():
        p = fn_root / (rel + '.mcfunction')
        s0 = p.read_text(encoding='utf-8').replace('\r\n', '\n')
        trail = s0.endswith('\n')
        lines = s0.rstrip('\n').split('\n')
        out, skip = [], False
        for ln in lines:
            if skip:
                skip = False
                continue
            if ln == MARK:
                skip = True
                continue
            out.append(ln)
        lines = out
        for _, mode, anchor, line in hooks:
            assert line not in lines, f'{rel}: unmarked copy of the hook line {line}'
            if mode == 'end':
                lines += [MARK, line]
                continue
            if anchor not in lines:
                raise RuntimeError(f'missing hook anchor in {rel}: {anchor}')
            i = lines.index(anchor)
            if mode == 'after':
                j = i + 1
                while j < len(lines) and lines[j] == MARK:      # after earlier hooks at the same anchor
                    j += 2
                lines[j:j] = [MARK, line]
            else:
                lines[i:i] = [MARK, line]
        s1 = '\n'.join(lines) + ('\n' if trail else '')
        if s1 != s0:
            p.write_text(s1, encoding='utf-8')
            changed.append(rel)
    return changed


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--resourcepack', help='unpacked resource pack root to write the rift sprites / models / atlas entries into')
    ap.add_argument('--datapack', help='datapack root (default: this tools/ folder\'s parent)')
    a = ap.parse_args()
    root = Path(a.datapack).resolve() if a.datapack else TOOLS.parent
    o = Out(root)
    build_datapack(o)
    removed = o.clean(['room/rift'], ['room/obj/k_rift'])
    changed = install_hooks(o.fn)
    msg = (f'rift: {len(o.written)} functions, {removed} stale removed, {len(HOOKS)} hook lines '
           f'({len(changed)} files changed{": " + ", ".join(changed) if changed else ""})')
    if a.resourcepack:
        n, px = build_resourcepack(a.resourcepack)
        msg += f', {n} sprites ({px} px of atlas) in {a.resourcepack}'
    print(msg)


if __name__ == '__main__':
    main()
