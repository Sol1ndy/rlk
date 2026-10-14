"""Resource-pack boss bar: level + name line, an HP bar with current/max numbers on it, a
white 'recent damage' trail that drains once damage stops, and a thin bar under it for the
boss's shield (element colour) or another gauge.

    python3 tools/build_bossbar.py --resourcepack <unpacked resource pack>

Vanilla boss bars are kept only for their text: the bars are coloured white, whose bar
sprites this pack makes transparent (the minimap uses the same trick). The bar itself is
drawn with font rlk:bossbar glyphs in the name of the second boss bar:

- HP row: white blocks 9 px tall in power-of-two widths (1..128), tinted per component
  colour; each piece is followed by a -1 space (a bitmap glyph advances width + 1), so runs
  of any length L are drawn from L's binary digits.
- Under row: the same pieces 3 px tall, 2 px under the HP bar (shield / gauge).
- Space glyphs +-1..256 move the cursor (numbers are centred on the bar, then the cursor
  returns to the bar's end so the whole line is exactly BAR px wide and stays centred).
- Every component in the line names its font: the boss bar shows the stored list through an
  nbt component, which appends entries 2.. as children of entry 1 (a bar piece), so an entry
  without a font would inherit rlk:bossbar and its digits would show as missing-glyph boxes.

Datapack: data/rlk/function/bossui/*. A boss calls, as itself, with
  #buHp #buMax (HP), #buSub #buSubMax #buSubCol (under bar; colour code below, 0 = none)
  function rlk:bossui/draw
which updates the boss's trail scores and leaves the line in storage rlk:bu line; then
  bossbar set <id> name {nbt:"line[]",storage:"rlk:bu",interpret:true,separator:""}
"""
import argparse
import json
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FN = ROOT / 'data/rlk/function/bossui'
ap = argparse.ArgumentParser()
ap.add_argument('--resourcepack', required=True)
RP = Path(ap.parse_args().resourcepack)

BAR = 200                       # bar width in GUI px
BITS = [128, 64, 32, 16, 8, 4, 2, 1]
SPACES = [256, 128, 64, 32, 16, 8, 4, 2, 1]
HP_H, HP_ASC = 9, 8             # covers the default font's digits (baseline row)
SUB_H, SUB_ASC = 3, -3          # 2 px under the HP bar
TRAIL_DELAY = 16                # ticks without damage before the white trail drains
DIGIT = 6                       # default-font advance of 0-9 and '/'

HP_COLOR, TRAIL_COLOR, EMPTY_COLOR = '#E0484B', '#FFFFFF', '#2A2A2E'
SUB_EMPTY = '#1E1E22'
# Under-bar colour codes: elements (shield) and gauges.
SUB_COLORS = {1: '#C58BFF',   # electro
              2: '#FF8A3D',   # pyro
              3: '#4FB8FF',   # hydro
              4: '#9FE8F5',   # cryo
              5: '#F2C14E',   # geo
              6: '#6FE3C1',   # anemo
              7: '#A5D94A',   # dendro
              8: '#E8C35A',   # gauge (gold)
              9: '#7BD88F'}   # recovery timer (green)

BASE = 0xE400
def ch(i):
    return chr(BASE + i)
HP_PIECE = {w: ch(k) for k, w in enumerate(BITS)}
SUB_PIECE = {w: ch(16 + k) for k, w in enumerate(BITS)}
SP_POS = {w: ch(32 + k) for k, w in enumerate(SPACES)}
SP_NEG = {w: ch(48 + k) for k, w in enumerate(SPACES)}
SP_BACK1 = SP_NEG[1]


def png(w, h):
    raw = b''.join(b'\x00' + b'\xff\xff\xff\xff' * w for _ in range(h))
    chunk = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


def blank(w, h):
    raw = b''.join(b'\x00' + b'\x00\x00\x00\x00' * w for _ in range(h))
    chunk = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


# ---------------------------------------------------------------- resource pack
tex = RP / 'assets/rlk/textures/font/bossbar'
tex.mkdir(parents=True, exist_ok=True)
providers = []
for w in BITS:
    (tex / f'hp_{w}.png').write_bytes(png(w, HP_H))
    (tex / f'sub_{w}.png').write_bytes(png(w, SUB_H))
    providers.append({'type': 'bitmap', 'file': f'rlk:font/bossbar/hp_{w}.png', 'ascent': HP_ASC, 'height': HP_H, 'chars': [HP_PIECE[w]]})
    providers.append({'type': 'bitmap', 'file': f'rlk:font/bossbar/sub_{w}.png', 'ascent': SUB_ASC, 'height': SUB_H, 'chars': [SUB_PIECE[w]]})
providers.append({'type': 'space', 'advances': {**{SP_POS[w]: w for w in SPACES}, **{SP_NEG[w]: -w for w in SPACES}}})
font = RP / 'assets/rlk/font/bossbar.json'
font.parent.mkdir(parents=True, exist_ok=True)
font.write_text(json.dumps({'providers': providers}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
bar = RP / 'assets/minecraft/textures/gui/sprites/boss_bar'
bar.mkdir(parents=True, exist_ok=True)
for name in ('white_background', 'white_progress'):
    (bar / f'{name}.png').write_bytes(blank(182, 5))


# ---------------------------------------------------------------- datapack
def write(name, lines):
    p = FN / (name + '.mcfunction')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def append(text, color=None):
    c = f',color:"{color}"' if color else ''
    return 'data modify storage rlk:bu line append value {text:"' + text + '",font:"rlk:bossbar"' + c + '}'


write('init', [
    '# Called by load.',
    'scoreboard objectives add bu dummy',
    'scoreboard objectives add buTrail dummy',
    'scoreboard objectives add buLast dummy',
    'scoreboard objectives add buT dummy',
    f'scoreboard players set #bar bu {BAR}',
    'scoreboard players set #2 bu 2',
    f'scoreboard players set #digit bu {DIGIT}',
])
# Runs: #len px of one colour (macro col) on the HP row / under row.
for row, piece in (('hp', HP_PIECE), ('sub', SUB_PIECE)):
    lines = [f'# #len bu px of colour $(col) on the {row} row.']
    for w in BITS:
        lines.append(f'$execute if score #len bu matches {w}.. run data modify storage rlk:bu line append value '
                     '{text:"' + piece[w] + SP_BACK1 + '",font:"rlk:bossbar",color:"$(col)"}')
        lines.append(f'execute if score #len bu matches {w}.. run scoreboard players remove #len bu {w}')
    write(f'run_{row}', lines)
for sign, table in (('pos', SP_POS), ('neg', SP_NEG)):
    lines = [f'# Move the cursor by {"+" if sign == "pos" else "-"}#len bu px.']
    for w in SPACES:
        lines.append(f'execute if score #len bu matches {w}.. run ' + append(table[w]))
        lines.append(f'execute if score #len bu matches {w}.. run scoreboard players remove #len bu {w}')
    write(f'space_{sign}', lines)

write('trail', [
    '# As the boss: the white trail follows HP down only after TRAIL_DELAY ticks without damage.',
    'execute unless score @s buTrail matches 0.. run scoreboard players operation @s buTrail = #buHp bu',
    'execute unless score @s buLast matches 0.. run scoreboard players operation @s buLast = #buHp bu',
    'execute if score #buHp bu < @s buLast run scoreboard players set @s buT 0',
    'scoreboard players add @s buT 1',
    'execute if score @s buTrail < #buHp bu run scoreboard players operation @s buTrail = #buHp bu',
    f'execute if score @s buT matches {TRAIL_DELAY}.. if score @s buTrail > #buHp bu run function rlk:bossui/trail_step',
    'scoreboard players operation @s buLast = #buHp bu',
])
write('trail_step', [
    '# Drain a fifth of the gap (at least 1/150 of max HP) per call.',
    'scoreboard players operation #step bu = @s buTrail',
    'scoreboard players operation #step bu -= #buHp bu',
    'scoreboard players set #c5 bu 5',
    'scoreboard players operation #step bu /= #c5 bu',
    'scoreboard players operation #min bu = #buMax bu',
    'scoreboard players set #c150 bu 150',
    'scoreboard players operation #min bu /= #c150 bu',
    'execute if score #min bu matches ..0 run scoreboard players set #min bu 1',
    'execute if score #step bu < #min bu run scoreboard players operation #step bu = #min bu',
    'scoreboard players operation @s buTrail -= #step bu',
    'execute if score @s buTrail < #buHp bu run scoreboard players operation @s buTrail = #buHp bu',
])


def px(dst, value):
    """#dst = value * BAR / #buMax (value is a score name)."""
    return [f'scoreboard players operation {dst} bu = {value}',
            f'scoreboard players operation {dst} bu *= #bar bu',
            f'scoreboard players operation {dst} bu /= #buMax bu']


draw = ['# As the boss, with #buHp #buMax #buSub #buSubMax #buSubCol set: line -> storage rlk:bu line.',
        'execute if score #buMax bu matches ..0 run scoreboard players set #buMax bu 1',
        'execute if score #buHp bu matches ..-1 run scoreboard players set #buHp bu 0',
        'function rlk:bossui/trail',
        'data modify storage rlk:bu line set value []']
draw += px('#fill', '#buHp bu')
draw += ['execute if score #buHp bu matches 1.. if score #fill bu matches ..0 run scoreboard players set #fill bu 1']
draw += px('#tr', '@s buTrail')
draw += ['execute if score #tr bu < #fill bu run scoreboard players operation #tr bu = #fill bu',
         'scoreboard players operation #white bu = #tr bu',
         'scoreboard players operation #white bu -= #fill bu',
         'scoreboard players operation #empty bu = #bar bu',
         'scoreboard players operation #empty bu -= #tr bu',
         'execute if score #empty bu matches ..-1 run scoreboard players set #empty bu 0',
         'scoreboard players operation #len bu = #fill bu',
         f'function rlk:bossui/run_hp {{col:"{HP_COLOR}"}}',
         'scoreboard players operation #len bu = #white bu',
         f'function rlk:bossui/run_hp {{col:"{TRAIL_COLOR}"}}',
         'scoreboard players operation #len bu = #empty bu',
         f'function rlk:bossui/run_hp {{col:"{EMPTY_COLOR}"}}',
         '# Numbers "hp/max" centred on the bar (default font, 6 px per character).',
         'scoreboard players set #n bu 1']
for lo, d in ((1, 1), (10, 2), (100, 3), (1000, 4), (10000, 5), (100000, 6), (1000000, 7)):
    draw.append(f'execute if score #buHp bu matches {lo}.. run scoreboard players set #nh bu {d}')
    draw.append(f'execute if score #buMax bu matches {lo}.. run scoreboard players set #nm bu {d}')
draw = draw[:-14] + ['scoreboard players set #nh bu 1', 'scoreboard players set #nm bu 1'] + draw[-14:]
draw += ['scoreboard players operation #n bu += #nh bu',
         'scoreboard players operation #n bu += #nm bu',
         'scoreboard players operation #w bu = #n bu',
         'scoreboard players operation #w bu *= #digit bu',
         'scoreboard players operation #half bu = #w bu',
         'scoreboard players operation #half bu /= #2 bu',
         '# back from the bar end to the text start: BAR/2 + w/2',
         f'scoreboard players set #len bu {BAR // 2}',
         'scoreboard players operation #len bu += #half bu',
         'function rlk:bossui/space_neg',
         '# The nbt component joins the list as children of its first entry (a bar piece in font',
         '# rlk:bossbar), so the numbers must name the default font or they inherit the bar font.',
         'data modify storage rlk:bu line append value {score:{name:"#buHp",objective:"bu"},color:"white",font:"minecraft:default"}',
         'data modify storage rlk:bu line append value {text:"/",color:"#D0D0D0",font:"minecraft:default"}',
         'data modify storage rlk:bu line append value {score:{name:"#buMax",objective:"bu"},color:"#D0D0D0",font:"minecraft:default"}',
         '# forward to the bar end again: BAR/2 - w/2',
         f'scoreboard players set #len bu {BAR // 2}',
         'scoreboard players operation #len bu -= #half bu',
         'execute if score #len bu matches 1.. run function rlk:bossui/space_pos',
         '# Under bar (shield in its element colour, or a gauge).',
         'execute if score #buSubCol bu matches 1.. if score #buSubMax bu matches 1.. run function rlk:bossui/sub']
write('draw', draw)
sub = ['# Thin bar under the HP bar: #buSub / #buSubMax in colour #buSubCol.',
       f'scoreboard players set #len bu {BAR}',
       'function rlk:bossui/space_neg',
       'execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0',
       'execute if score #buSub bu > #buSubMax bu run scoreboard players operation #buSub bu = #buSubMax bu',
       'scoreboard players operation #sf bu = #buSub bu',
       'scoreboard players operation #sf bu *= #bar bu',
       'scoreboard players operation #sf bu /= #buSubMax bu',
       'execute if score #buSub bu matches 1.. if score #sf bu matches ..0 run scoreboard players set #sf bu 1',
       'scoreboard players operation #se bu = #bar bu',
       'scoreboard players operation #se bu -= #sf bu',
       'scoreboard players operation #len bu = #sf bu']
for code, col in SUB_COLORS.items():
    sub.append(f'execute if score #buSubCol bu matches {code} run function rlk:bossui/run_sub {{col:"{col}"}}')
sub += ['scoreboard players operation #len bu = #se bu',
        f'function rlk:bossui/run_sub {{col:"{SUB_EMPTY}"}}']
write('sub', sub)
print(f'Boss bar: {BAR} px HP bar + under bar, {len(providers)} font providers, {len(SUB_COLORS)} under-bar colours; '
      f'functions in {FN.relative_to(ROOT)}.')
