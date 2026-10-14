"""On-screen dungeon minimap drawn with resource-pack font glyphs (no map item).

    python3 tools/build_minimap.py --resourcepack <unpacked resource pack>

The dungeon is a 6 x 6 grid of 20-block cells (x/z -60..59, see room/data). Each map's
zones occupy cells; doors sit on cell borders. The minimap is the name of an invisible
boss bar (rlk:minimap, colour white, whose bar sprites this pack makes transparent):

- font rlk:minimap: per grid row r (0..5) a set of 20x20 glyphs, all with the same fixed
  advance (a 1/255-alpha pixel pins the width), shifted down 20 px per row via `ascent`:
  cell square, same-zone connectors (right / below), doors (right / below), player dot;
  plus space glyphs to overlay (-21), step one cell (+20), return a row (-120) and binary
  position spaces (all positive): boss bar text is centred and the rows return to their
  start, so a trailing space of 2|x| (x < 0) or a leading one of 2x (x > 0) puts the map's
  left edge at centre + x (#mmX, default top-left; /function rlk:minimap/pos {x:N}).
- Glyphs are white; each text component's colour paints them: unexplored-but-open zones
  dim grey, explored zones light grey (special zones in their map colour), the zone the
  player stands in pale gold; open doors white, closed (unexplored) doors grey.

Datapack (data/rlk/function/minimap/): init (load), build (after room/gen, or once after a
reload: which zone owns each cell, same-zone connectors), tick (from rlk:tick: every 5 ticks, redraws when the
player's cell or any zone/door state changed, at least every 2 s; hidden outside a run,
in the boss arena while Narukami lives, on the map screen, in selection spaces, when dead).
"""
import argparse
import json
import zlib
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FN = ROOT / 'data/rlk/function/minimap'
ap = argparse.ArgumentParser()
ap.add_argument('--resourcepack', required=True)
RP = Path(ap.parse_args().resourcepack)

N = 6                  # grid size
TILE = 20              # glyph tile (GUI px); cells are 18 px with a 2 px gap
ADV = TILE + 1         # bitmap advance = pinned width 20 + 1
DEFAULT_X = -364       # map's left edge relative to the screen centre (GUI px): top-left
                       # (6 px margin) on a ~740 px wide GUI, e.g. a 2220-2304 px window at GUI
                       # scale 3, measured from the user's screenshot.
                       # Change in game: /function rlk:minimap/pos {x:-300}
TOP_ASCENT = 7         # row 0 ascent; each next row TILE px lower
MAX_ZONE = 12
OFFS = [1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1]

TYPES = ['cell', 'conn_r', 'conn_d', 'door_r', 'door_d', 'dot', 'conn_c']
BASE = 0xE300
def glyph(row, t):
    return chr(BASE + row * 8 + TYPES.index(t))
SP_BACK, SP_STEP, SP_ROW = chr(0xE3F0), chr(0xE3F1), chr(0xE3F2)
# Position spaces (positive only, so the text never has a negative width): the rows return
# to their start and boss bar text is centred at centre - width/2, so a trailing 2|x| puts
# the map's left edge at centre + x for x < 0, a leading 2x does it for x > 0.
SP_POS = {w: chr(0xE3A0 + k) for k, w in enumerate(OFFS)}

# Zone colour codes: 0 hidden, 1 open but not entered, 2 explored, 3 player inside, 4.. special
COLORS = {1: '#5A5A5A', 2: '#B4B4B4', 3: '#FFE08A',
          4: '#F0F0F0', 5: '#E0B255', 6: '#6FCF8F', 7: '#5B9BF0', 8: '#D65A5A',
          9: '#B58BE8', 10: '#B08A5A', 11: '#E05050'}
# zkind -> explored colour code (0 start, 1 combat, 2 last, 3 money, 4 shop, 5 sapphire,
# 6 reforge, 7 enchant, 8 root, 9 boss, 10 levelup start)
KIND_CODE = {2: 4, 3: 5, 4: 6, 5: 7, 6: 8, 7: 9, 8: 10, 9: 11}
DOOR_COLORS = {1: '#8C8C8C', 2: '#FFFFFF'}
DOT_COLOR = '#3A2A00'


# ---------------------------------------------------------------- resource pack
def png(w, h, px):
    raw = b''.join(b'\x00' + bytes(sum((px[y * w + x] for x in range(w)), ())) for y in range(h))
    chunk = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


def tile(fill):
    px = [(0, 0, 0, 0)] * (TILE * TILE)
    px[0 * TILE + TILE - 1] = (255, 255, 255, 1)       # pins the glyph width to TILE px
    for (x, y), c in fill.items():
        px[y * TILE + x] = c
    return png(TILE, TILE, px)


W, EDGE = (255, 255, 255, 235), (205, 205, 205, 255)
C = TILE - 2           # cell size; the last 2 px of the tile are the gap to the next cell
OPAQUE = (255, 255, 255, 255)
shapes = {
    'cell': {(x, y): (EDGE if x in (0, C - 1) or y in (0, C - 1) else W) for x in range(C) for y in range(C)},
    'conn_r': {(x, y): W for x in (C - 1, C, C + 1) for y in range(1, C - 1)},
    'conn_d': {(x, y): W for y in (C - 1, C, C + 1) for x in range(1, C - 1)},
    'conn_c': {(x, y): W for x in (C - 1, C, C + 1) for y in (C - 1, C, C + 1)},
    'door_r': {(x, y): OPAQUE for x in (C - 1, C, C + 1) for y in range(C // 2 - 4, C // 2 + 4)},
    'door_d': {(x, y): OPAQUE for y in (C - 1, C, C + 1) for x in range(C // 2 - 4, C // 2 + 4)},
    'dot': {(x, y): OPAQUE for x in range(C // 2 - 3, C // 2 + 3) for y in range(C // 2 - 3, C // 2 + 3)},
}
tex = RP / 'assets/rlk/textures/font/minimap'
tex.mkdir(parents=True, exist_ok=True)
for t, f in shapes.items():
    (tex / f'{t}.png').write_bytes(tile(f))
providers = []
for r in range(N):
    for t in TYPES:
        providers.append({'type': 'bitmap', 'file': f'rlk:font/minimap/{t}.png',
                          'ascent': TOP_ASCENT - TILE * r, 'height': TILE, 'chars': [glyph(r, t)]})
providers.append({'type': 'space', 'advances': {SP_BACK: -ADV, SP_STEP: TILE, SP_ROW: -TILE * N,
                                                **{SP_POS[w]: w for w in OFFS}}})
font = RP / 'assets/rlk/font/minimap.json'
font.parent.mkdir(parents=True, exist_ok=True)
font.write_text(json.dumps({'providers': providers}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
# The white boss bar (only the minimap uses white) is invisible.
bar = RP / 'assets/minecraft/textures/gui/sprites/boss_bar'
bar.mkdir(parents=True, exist_ok=True)
for name in ('white_background', 'white_progress'):
    (bar / f'{name}.png').write_bytes(png(182, 5, [(0, 0, 0, 0)] * (182 * 5)))


# ---------------------------------------------------------------- datapack
def write(name, lines):
    p = FN / (name + '.mcfunction')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def comp(text, color):
    return '{text:"' + text + '",font:"rlk:minimap",color:"' + color + '"}'


CELLS = range(N * N)
write('init', [
    '# Called by load. The minimap is the name of an invisible (white) boss bar.',
    'scoreboard objectives add mm dummy',
    'bossbar add rlk:minimap ""',
    'bossbar set rlk:minimap color white',
    'bossbar set rlk:minimap style progress',
    'bossbar set rlk:minimap value 0',
    'bossbar set rlk:minimap visible false',
    'scoreboard players set #mmSig mm -1',
    '# Rebuild the cell table once after a reload (a map made before it has none).',
    'scoreboard players set #mmBuilt mm 0',
    f'execute unless score #mmX mm matches -1000..1000 run scoreboard players set #mmX mm {DEFAULT_X}',
    '# New default position (version 2): the left edge at the top-left corner.',
    f'execute unless score #mmXv mm matches 2 run scoreboard players set #mmX mm {DEFAULT_X}',
    'scoreboard players set #mmXv mm 2',
])
write('pos', [
    '# /function rlk:minimap/pos {x:N}: the map\'s left edge, GUI px from the screen centre',
    '# (negative = left). Default ' + str(DEFAULT_X) + '.',
    '$scoreboard players set #mmX mm $(x)',
    'execute if score #mmX mm matches ..-1001 run scoreboard players set #mmX mm -1000',
    'execute if score #mmX mm matches 1001.. run scoreboard players set #mmX mm 1000',
    'scoreboard players set #mmSig mm -1',
    'tellraw @s [{text:"[미니맵] ",color:"gold"},{text:"위치 x = ",color:"gray"},{score:{name:"#mmX",objective:"mm"},color:"white"}]',
])
for name, d, word in (('left', -10, '왼쪽'), ('right', 10, '오른쪽')):
    write(name, [f'# /function rlk:minimap/{name}: nudge the minimap 10 GUI px to the {name}.',
                 f'scoreboard players add #mmX mm {d}',
                 'execute if score #mmX mm matches ..-1001 run scoreboard players set #mmX mm -1000',
                 'execute if score #mmX mm matches 1001.. run scoreboard players set #mmX mm 1000',
                 'scoreboard players set #mmSig mm -1',
                 'tellraw @s [{text:"[미니맵] ",color:"gold"},{text:"' + word + '으로 10칸 · 위치 x = ",color:"gray"},{score:{name:"#mmX",objective:"mm"},color:"white"}]'])
write('offset', [
    '# Append position spaces for an advance of 2 x |#mmX| (|#mmX| <= 1000): before the rows',
    '# when #mmX > 0, after them when #mmX < 0 (see draw).',
    'scoreboard players operation #len mm = #mmX mm',
    'scoreboard players operation #len mm += #mmX mm',
    'execute if score #len mm matches ..-1 run scoreboard players operation #len mm *= #neg mm',
] + sum(([f'execute if score #len mm matches {w}.. run data modify storage rlk:mm line append value ' + '{text:"' + SP_POS[w] + '",font:"rlk:minimap"}',
          f'execute if score #len mm matches {w}.. run scoreboard players remove #len mm {w}'] for w in OFFS), []))
# build: which zone owns each cell, and same-zone connectors
write('build', [
    '# After room/gen (zones summoned): cell -> zone id (#g<i>), same-zone connectors.',
] + [f'scoreboard players set #g{i} mm 0' for i in CELLS] + [
    'execute as @e[tag=rlk_zone] run function rlk:minimap/zone_cells',
] + sum(([f'scoreboard players set #hc{i} mm 0', f'scoreboard players set #vc{i} mm 0', f'scoreboard players set #cc{i} mm 0'] for i in CELLS), []) + [
    f'execute if score #g{i} mm matches 1.. if score #g{i} mm = #g{i + 1} mm run scoreboard players set #hc{i} mm 1'
    for i in CELLS if i % N != N - 1] + [
    f'execute if score #g{i} mm matches 1.. if score #g{i} mm = #g{i + N} mm run scoreboard players set #vc{i} mm 1'
    for i in CELLS if i < N * (N - 1)] + [
    f'execute if score #hc{i} mm matches 1 if score #vc{i} mm matches 1 if score #hc{i + N} mm matches 1 if score #vc{i + 1} mm matches 1 run scoreboard players set #cc{i} mm 1'
    for i in CELLS if i % N != N - 1 and i < N * (N - 1)] + [
    'scoreboard players set #mmSig mm -1',
    'scoreboard players set #mmBuilt mm 1',
])
write('zone_cells', [
    '# As a zone marker: mark every cell of its record.',
    'scoreboard players operation #zid mm = @s zid',
    'data modify storage rlk:mm q set from entity @s data.cells',
    'function rlk:minimap/cells_loop',
])
write('cells_loop', [
    'execute unless data storage rlk:mm q[0] run return 0',
    'execute store result score #cx mm run data get storage rlk:mm q[0].x0',
    'execute store result score #cz mm run data get storage rlk:mm q[0].z0',
    'function rlk:minimap/cell_index',
    'function rlk:minimap/set_g',
    'data remove storage rlk:mm q[0]',
    'function rlk:minimap/cells_loop',
])
write('cell_index', [
    '# #cx/#cz block coordinates -> #idx = row * 6 + col (-1 outside the grid).',
    'scoreboard players set #c20 mm 20',
    'scoreboard players set #c6 mm 6',
    'scoreboard players add #cx mm 60',
    'scoreboard players add #cz mm 60',
    'scoreboard players set #idx mm -1',
    'execute unless score #cx mm matches 0..119 run return 0',
    'execute unless score #cz mm matches 0..119 run return 0',
    'scoreboard players operation #cx mm /= #c20 mm',
    'scoreboard players operation #cz mm /= #c20 mm',
    'scoreboard players operation #idx mm = #cz mm',
    'scoreboard players operation #idx mm *= #c6 mm',
    'scoreboard players operation #idx mm += #cx mm',
])
write('set_g', [f'execute if score #idx mm matches {i} run scoreboard players operation #g{i} mm = #zid mm' for i in CELLS])

# tick: visibility, signature, redraw
write('tick', [
    '# From rlk:tick. Every 5 ticks: show/hide, and redraw when something changed.',
    'scoreboard players add #mmT mm 1',
    'execute if score #mmT mm matches 5.. run scoreboard players set #mmT mm 0',
    'execute unless score #mmT mm matches 0 run return 0',
    'scoreboard players set #mmShow mm 1',
    'execute unless score #active room matches 1 run scoreboard players set #mmShow mm 0',
    'execute unless entity @a[tag=player,scores={dead=0},limit=1] run scoreboard players set #mmShow mm 0',
    'execute if entity @a[tag=player,scores={pkMode=1..}] run scoreboard players set #mmShow mm 0',
    'execute if entity @a[tag=player,scores={vMap=1..}] run scoreboard players set #mmShow mm 0',
    'execute if entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] run scoreboard players set #mmShow mm 0',
    'execute if score #mmShow mm matches 0 run return run bossbar set rlk:minimap visible false',
    'execute unless score #mmBuilt mm matches 1 run function rlk:minimap/build',
    'bossbar set rlk:minimap players @a[tag=player]',
    'bossbar set rlk:minimap visible true',
    'function rlk:minimap/signature',
    'scoreboard players add #mmAge mm 1',
    'execute if score #mmAge mm matches 8.. run scoreboard players set #mmSig mm -1',
    'execute unless score #mmNew mm = #mmSig mm run function rlk:minimap/draw',
])
write('signature', [
    '# #mmNew: player cell + zone states + door states folded into one number.',
    'execute store result score #cx mm run data get entity @e[tag=rlk_body,limit=1] Pos[0]',
    'execute store result score #cz mm run data get entity @e[tag=rlk_body,limit=1] Pos[2]',
    'function rlk:minimap/cell_index',
    'scoreboard players operation #pc mm = #idx mm',
    'scoreboard players operation #mmNew mm = #idx mm',
    'scoreboard players set #c31 mm 31',
    'execute as @e[tag=rlk_zone] run function rlk:minimap/sig_zone',
    'execute as @e[tag=rlk_door] run function rlk:minimap/sig_door',
])
write('sig_zone', [
    'scoreboard players operation #mmNew mm *= #c31 mm',
    'scoreboard players operation #mmNew mm += @s zst',
])
write('sig_door', [
    'scoreboard players operation #mmNew mm *= #c31 mm',
    'scoreboard players operation #mmNew mm += @s dst',
])

# draw
draw = ['# Rebuild the minimap text (storage rlk:mm line) and put it on the boss bar.',
        'scoreboard players operation #mmSig mm = #mmNew mm',
        'scoreboard players set #mmAge mm 0',
        '# Zone colour codes (#zc<k>) and door slots (#hd<i> right, #vd<i> below).']
draw += [f'scoreboard players set #zc{k} mm 0' for k in range(1, MAX_ZONE + 1)]
draw += [f'scoreboard players set #pz mm 0',
         'execute if score #pc mm matches 0.. run function rlk:minimap/player_zone',
         'execute as @e[tag=rlk_zone] run function rlk:minimap/zone_color']
draw += sum(([f'scoreboard players set #hd{i} mm 0', f'scoreboard players set #vd{i} mm 0'] for i in CELLS), [])
draw += ['execute as @e[tag=rlk_door] run function rlk:minimap/door_slot',
         'data modify storage rlk:mm line set value []',
         'scoreboard players set #neg mm -1',
         'execute if score #mmX mm matches 1.. run function rlk:minimap/offset']
for r in range(N):
    for c in range(N):
        i = r * N + c
        draw.append(f'scoreboard players set #c mm 0')
        draw += [f'execute if score #g{i} mm matches {k} run scoreboard players operation #c mm = #zc{k} mm'
                 for k in range(1, MAX_ZONE + 1)]
        draw.append(f'execute if score #c mm matches 1.. run function rlk:minimap/c/{i}')
        draw.append(f'execute unless score #c mm matches 1.. if score #hd{i} mm matches 1.. run function rlk:minimap/c/{i}')
        draw.append(f'execute unless score #c mm matches 1.. if score #vd{i} mm matches 1.. run function rlk:minimap/c/{i}')
        draw.append('data modify storage rlk:mm line append value {text:"' + SP_STEP + '",font:"rlk:minimap"}')
    draw.append('data modify storage rlk:mm line append value {text:"' + SP_ROW + '",font:"rlk:minimap"}')
draw.append('execute if score #mmX mm matches ..-1 run function rlk:minimap/offset')
draw.append('bossbar set rlk:minimap name {nbt:"line[]",storage:"rlk:mm",interpret:true,separator:""}')
write('draw', draw)
for r in range(N):
    for c in range(N):
        i = r * N + c
        lines = [f'# Cell row {r} col {c}: the cell, its right/lower joins and doors, the player dot.']
        for code, col in COLORS.items():
            lines.append(f'execute if score #c mm matches {code} run data modify storage rlk:mm line append value '
                         + comp(glyph(r, 'cell') + SP_BACK, col))
            if c < N - 1:
                lines.append(f'execute if score #c mm matches {code} if score #hc{i} mm matches 1 run data modify storage rlk:mm line append value '
                             + comp(glyph(r, 'conn_r') + SP_BACK, col))
            if r < N - 1:
                lines.append(f'execute if score #c mm matches {code} if score #vc{i} mm matches 1 run data modify storage rlk:mm line append value '
                             + comp(glyph(r, 'conn_d') + SP_BACK, col))
            if r < N - 1 and c < N - 1:
                lines.append(f'execute if score #c mm matches {code} if score #cc{i} mm matches 1 run data modify storage rlk:mm line append value '
                             + comp(glyph(r, 'conn_c') + SP_BACK, col))
        for st, col in DOOR_COLORS.items():
            if c < N - 1:
                lines.append(f'execute if score #hd{i} mm matches {st} run data modify storage rlk:mm line append value '
                             + comp(glyph(r, 'door_r') + SP_BACK, col))
            if r < N - 1:
                lines.append(f'execute if score #vd{i} mm matches {st} run data modify storage rlk:mm line append value '
                             + comp(glyph(r, 'door_d') + SP_BACK, col))
        lines.append(f'execute if score #pc mm matches {i} run data modify storage rlk:mm line append value '
                     + comp(glyph(r, 'dot') + SP_BACK, DOT_COLOR))
        write(f'c/{i}', lines)
write('player_zone', [f'execute if score #pc mm matches {i} run scoreboard players operation #pz mm = #g{i} mm' for i in CELLS])
zc = ['# As a zone marker: its colour code into #zc<zid>.',
      'scoreboard players set #z mm 0',
      'execute if score @s zst matches 1 run scoreboard players set #z mm 1',
      'execute if score @s zst matches 2.. run scoreboard players set #z mm 2']
zc += [f'execute if score @s zst matches 2.. if score @s zkind matches {k} run scoreboard players set #z mm {code}'
       for k, code in KIND_CODE.items()]
zc += ['execute if score @s zid = #pz mm run scoreboard players set #z mm 3']
zc += [f'execute if score @s zid matches {k} run scoreboard players operation #zc{k} mm = #z mm' for k in range(1, MAX_ZONE + 1)]
write('zone_color', zc)
write('door_slot', [
    '# As a door marker on a cell border: which border slot, and how to draw it',
    '# (1 closed / unexplored = grey, 2 open = white; hidden doors are not drawn).',
    'execute unless score @s dst matches 1.. run return 0',
    'scoreboard players operation #ds mm = @s dst',
    'execute if score #ds mm matches 3.. run scoreboard players set #ds mm 2',
    'execute store result score #cx mm run data get entity @s Pos[0]',
    'execute store result score #cz mm run data get entity @s Pos[2]',
    'scoreboard players set #c20 mm 20',
    'scoreboard players operation #mx mm = #cx mm',
    'scoreboard players add #mx mm 60',
    'scoreboard players operation #mx mm %= #c20 mm',
    '# On an x border (a wall between two columns): the slot is the left cell\'s right side.',
    'execute if score #mx mm matches 0 run scoreboard players remove #cx mm 1',
    'execute unless score #mx mm matches 0 run scoreboard players remove #cz mm 1',
    'function rlk:minimap/cell_index',
    'execute if score #idx mm matches 0.. if score #mx mm matches 0 run function rlk:minimap/set_hd',
    'execute if score #idx mm matches 0.. unless score #mx mm matches 0 run function rlk:minimap/set_vd',
])
write('set_hd', [f'execute if score #idx mm matches {i} run scoreboard players operation #hd{i} mm = #ds mm' for i in CELLS])
write('set_vd', [f'execute if score #idx mm matches {i} run scoreboard players operation #vd{i} mm = #ds mm' for i in CELLS])
print(f'Minimap: {N}x{N} grid, {len(providers)} font providers, {len(COLORS)} zone colours; '
      f'functions in {FN.relative_to(ROOT)}, glyphs in {tex}.')
