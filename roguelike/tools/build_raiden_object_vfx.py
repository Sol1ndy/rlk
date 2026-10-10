"""Display-only lightning for Narukami eyes, stakes and the illusion challenge.

Generate independently of the encounter controller. Object IDs may be reused
by later patterns, so persistent effects follow a separate unique owner serial.
Illusion cues are identical for the real and the fake illusions (only the number
of slashes tells them apart); each slash adds a swing arc and a flying sword wave.
"""
from pathlib import Path
import argparse
import json
import math

DP = Path(__file__).resolve().parents[1]
args = argparse.ArgumentParser()
args.add_argument('--resourcepack', required=True)
RP = Path(args.parse_args().resourcepack)
OUT = DP / 'data/rlk/function/boss/raiden/object_vfx'
SCALE = 4
COLORS = {name:'rlk:raiden/fx/'+tex for name,tex in
          [('purple','violet_dense'),('blue','blue'),('cyan','cyan'),('white','white'),
           ('glow','glow'),('after','afterglow'),('lavender','lavender'),('pearl','pearl')]}


def write(name, lines):
    p = OUT / (name + '.mcfunction')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def box(center, extent, color):
    return {
        'from': [round(8 + (center[i] - extent[i]/2)*16/SCALE, 5) for i in range(3)],
        'to': [round(8 + (center[i] + extent[i]/2)*16/SCALE, 5) for i in range(3)],
        'shade': False,
        'faces': {face: {'texture': '#' + color, 'uv': [0, 0, 16, 16]}
                  for face in ['north', 'south', 'east', 'west', 'up', 'down']},
    }


def stroke(points, width=.055, color='purple', core=True):
    mesh = []
    for a, b in zip(points, points[1:]):
        count = max(1, math.ceil(math.dist(a, b)/.20))
        for j in range(count):
            p = [a[i] + (b[i]-a[i])*j/count for i in range(3)]
            q = [a[i] + (b[i]-a[i])*(j+1)/count for i in range(3)]
            center = [(p[i]+q[i])/2 for i in range(3)]
            extent = [abs(q[i]-p[i]) + width for i in range(3)]
            mesh.append(box(center, extent, color))
            if core:
                mesh.append(box(center,[s+width*.8 for s in extent],'glow'))
                bright = [abs(q[i]-p[i]) + width*.17 for i in range(3)]
                # Project the luminous seam from both front/back faces.
                bright[2] = extent[2] + .012
                mesh.append(box(center, bright, 'white'))
    return mesh


def model(name, mesh, fade=False):
    colors=dict(COLORS)
    if fade:
        colors.update(purple=COLORS['after'],cyan=COLORS['lavender'],white=COLORS['lavender'],blue=COLORS['after'],pearl=COLORS['lavender'])
    p = RP / ('assets/rlk/models/item/raiden/fx_object/' + name + '.json')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({'ambientocclusion': False,
        'textures': {**colors, 'particle': colors['purple']}, 'elements': mesh},
        separators=(',', ':'))+'\n', encoding='utf-8')
    p = RP / ('assets/rlk/items/raiden/fx_object/' + name + '.json')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({'model': {'type': 'minecraft:model',
        'model': 'rlk:item/raiden/fx_object/' + name}}, separators=(',', ':'))+'\n', encoding='utf-8')


for variant in [0, 1]:
    eye = []
    # Charged orbit around the orb, never a floor marker implying danger.
    for elevation in [.77, 1.14]:
        path = []
        for i in range(19):
            angle = i*2*math.pi/18 + variant*.14
            radius = .64 + (.10 if i%2 == variant else -.04)
            path.append((math.cos(angle)*radius, elevation + (.08 if i%2 else -.08),
                         math.sin(angle)*radius))
        eye += stroke(path, .06, core=False)
    for side in [-1, 1]:
        path = [(side*.35, .95, 0), (side*.78, 1.12, .14),
                (side*.59, 1.40, -.1), (side*1.04, 1.74 + variant*.12, .05)]
        eye += stroke(path, .085)
        eye += stroke([path[1], (side*1.14, .93, .28), (side*1.3, 1.14, .18)], .04)
    model(f'eye_{variant}', eye)

    stake = []
    # A bolt climbing the physical stake, with outward forks above the floor.
    for side in [-1, 1]:
        path = [(side*.23, .1, 0), (side*.37, .46, .18),
                (side*.19, .77, -.1), (side*.40, 1.13, .12),
                (side*.20, 1.46, -.07), (side*.56, 1.91 + variant*.12, .14)]
        stake += stroke(path, .07)
        stake += stroke([path[3], (side*.88, 1.29, .3),
                         (side*1.17, .94 + variant*.15, .2)], .052)
    model(f'stake_{variant}', stake)


# Illusion wind-up glint: the same single jagged line for every illusion; its last
# three ticks switch to the charged (thicker, cored) version right before the cut.
for contact in [False, True]:
    path = [(-1.13, .83, .38), (-.50, 1.09, .38), (-.18, 1.35, .38), (.24, 1.46, .38),
            (.54, 1.75, .38), (1.13, 1.93, .38)]
    model('strike_slash' if contact else 'warn_slash',
          stroke(path, .13 if contact else .072, 'purple' if contact else 'blue', core=contact))


def ribbon(points, inner, width=.09, color='purple'):
    # Sword-light smear: bright cored outer edge plus a translucent inner trail.
    mesh = stroke(points, width, color)
    mesh += stroke(inner, width*.8, 'lavender', core=False)
    return mesh


# Swing arc: mesh +Z is the illusion's front, -X its right. The cut sweeps from the
# right side round the front to the left, dropping slightly (a level horizontal cut).
for fade in [False, True]:
    arc, trail = [], []
    for i in range(15):
        a = math.radians(-105 + 210*i/14)
        y = 1.62 - .42*i/14
        arc.append((1.85*math.sin(a), y, 1.85*math.cos(a)))
        trail.append((1.45*math.sin(a), y - .05, 1.45*math.cos(a)))
    mesh = ribbon(arc, trail, .10)
    tip = arc[-1]
    # A short spark where the blade leaves the arc.
    mesh += stroke([tip, (tip[0]+.35, tip[1]+.22, tip[2]-.28), (tip[0]+.52, tip[1]+.05, tip[2]-.55)], .05)
    model('swing_fade' if fade else 'swing', mesh, fade)

# Flying sword wave: a horizontal crescent bulging forward (+Z) at chest height,
# with two short lightning tails. It travels to the far end of the slash line.
for fade in [False, True]:
    outer, inner = [], []
    for i in range(13):
        u = -1 + 2*i/12
        outer.append((1.55*u, 1.18 + .05*math.sin(i*1.9), .62*(1 - u*u)))
        inner.append((1.25*u, 1.16, .30*(1 - u*u) - .06))
    mesh = ribbon(outer, inner, .12, 'pearl')
    mesh += stroke(outer[2:11], .05, 'purple')
    for side in [-1, 1]:
        mesh += stroke([(side*.55, 1.2, .35), (side*.75, 1.42, -.25), (side*.48, 1.25, -.85),
                        (side*.70, 1.38, -1.35)], .045)
    model('wave_fade' if fade else 'wave', mesh, fade)


for flower in [False, True]:
    mesh = []
    for i in range(8):
        a = i*2*math.pi/8
        x, z = math.cos(a), math.sin(a)
        path = [(x*.15, .9, z*.15), (x*.55-z*.12, 1.12, z*.55+x*.12),
                (x*.82+z*.15, .76, z*.82-x*.15), (x*1.35, .99, z*1.35)]
        mesh += stroke(path, .09, 'cyan' if flower else 'purple')
    for side in [-1, 1]:
        mesh += stroke([(0,.9,0),(side*.25,1.35,.1),(-side*.12,1.72,.03),
                        (side*.37,2.05,.08)], .075, 'cyan' if flower else 'purple')
    model('flower_break' if flower else 'object_break', mesh)
    model(('flower_break' if flower else 'object_break')+'_fade',mesh,True)


def spawn(name, kind, owned=True, life=0):
    lines = [
        'summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_object_fx","rlk_rd_ofnew"],'
        'NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",teleport_duration:0,'
        'brightness:{sky:15,block:15},view_range:3f,width:6f,height:6f,shadow_radius:0f,'
        'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_object/' + name + '"}},'
        'transformation:{translation:[0f,0f,0f],scale:[4f,4f,4f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,1f,0f,0f]}}',
        'data modify entity @e[tag=rlk_rd_ofnew,limit=1] Rotation set from entity @s Rotation',
        'data modify entity @e[tag=rlk_rd_ofnew,limit=1] Rotation[1] set value 0f',
        f'scoreboard players set @e[tag=rlk_rd_ofnew] rdOvKind {kind}',
        'scoreboard players set @e[tag=rlk_rd_ofnew] rdOvAge -1',
        f'scoreboard players set @e[tag=rlk_rd_ofnew] rdOvLife {life}',
    ]
    if owned:
        lines += ['scoreboard players operation @e[tag=rlk_rd_ofnew,limit=1] rdOvId = @s rdOvId',
                  'scoreboard players operation @e[tag=rlk_rd_ofnew,limit=1] rdObjId = @s rdObjId']
    lines += ['tag @e[tag=rlk_rd_ofnew] remove rlk_rd_ofnew']
    return lines


(OUT / 'cross.mcfunction').unlink(missing_ok=True)  # retired real-illusion X cue
write('init', [f'scoreboard objectives add {name} dummy' for name in
               ['rdOvId', 'rdOvKind', 'rdOvAge', 'rdOvLife']])
write('create', [
    '# Call once as every newly created gameplay object, including flower/illusion.',
    'scoreboard players add #rdObjectSerial rd 1',
    'scoreboard players operation @s rdOvId = #rdObjectSerial rd',
    'execute if score @s rdObjKind matches 1 run function rlk:boss/raiden/object_vfx/eye',
    'execute if score @s rdObjKind matches 4 run function rlk:boss/raiden/object_vfx/stake',
])
write('eye', spawn('eye_0', 1))
write('stake', spawn('stake_0', 2))
cue = ['$scoreboard players set @e[tag=rlk_rd_ofnew] rdOvLife $(life)' if line.endswith(' rdOvLife 0') else line
       for line in spawn('warn_slash', 5)]
assert any(line.startswith('$') for line in cue)
write('illusion_cue', [
    '# As an illusion facing the arena centre, {life:<ticks until its slash>}. Identical',
    '# for the real and the fake illusions; it disappears with its owner.',
] + cue)
swing = spawn('swing', 6, owned=False, life=4)
wave = spawn('wave', 7, owned=False, life=5)
wave.insert(-1, 'data merge entity @e[tag=rlk_rd_ofnew,limit=1] {teleport_duration:1}')
write('slash', [
    '# As the slashing illusion at its feet, facing the centre: swing arc + flying wave.',
] + swing + wave)
write('break', [
    '# Detached burst survives its destroyed owner for nine ticks, then disappears.',
    'execute if score @s rdObjKind matches 3 run function rlk:boss/raiden/object_vfx/flower_break',
    'execute unless score @s rdObjKind matches 3 run function rlk:boss/raiden/object_vfx/object_break',
])
write('flower_break', spawn('flower_break', 4, owned=False, life=9))
write('object_break', spawn('object_break', 3, owned=False, life=9))
hit = spawn('object_break', 3, owned=False, life=5)
hit.insert(-1, 'data merge entity @e[tag=rlk_rd_ofnew,limit=1] {transformation:{translation:[0f,.5f,0f],scale:[1.8f,1.8f,1.8f]}}')
write('hit', hit)
write('clear', ['kill @e[tag=rlk_rd_object_fx]'])
write('world', ['execute as @e[tag=rlk_rd_object_fx] at @s run function rlk:boss/raiden/object_vfx/tick'])
write('owner', [
    'scoreboard players operation #rdOvOwner rd = @s rdOvId',
    'scoreboard players set #rdOvExists rd 0',
    'execute as @e[tag=rlk_rd_object] if score @s rdOvId = #rdOvOwner rd run scoreboard players set #rdOvExists rd 1',
])
setmodel = lambda name: 'data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_object/' + name + '"'
write('cue_tick', [
    'scoreboard players operation #rdOvLeft rd = @s rdOvLife',
    'scoreboard players operation #rdOvLeft rd -= @s rdOvAge',
    'execute if score #rdOvLeft rd matches 3 run ' + setmodel('strike_slash'),
])
write('tick', [
    'execute if score @s rdOvKind matches 1..2 run function rlk:boss/raiden/object_vfx/owner',
    'execute if score @s rdOvKind matches 5 run function rlk:boss/raiden/object_vfx/owner',
    'execute if score @s rdOvKind matches 1..2 if score #rdOvExists rd matches 0 run return run kill @s',
    'execute if score @s rdOvKind matches 5 if score #rdOvExists rd matches 0 run return run kill @s',
    'scoreboard players add @s rdOvAge 1',
    'execute if score @s rdOvLife matches 1.. if score @s rdOvAge >= @s rdOvLife run return run kill @s',
    'scoreboard players operation #rdOvFrame rd = @s rdOvAge',
    'scoreboard players set #rdOvEight rd 8',
    'scoreboard players operation #rdOvFrame rd %= #rdOvEight rd',
    'execute if score @s rdOvKind matches 1 if score #rdOvFrame rd matches 0 run ' + setmodel('eye_0'),
    'execute if score @s rdOvKind matches 1 if score #rdOvFrame rd matches 4 run ' + setmodel('eye_1'),
    'execute if score @s rdOvKind matches 2 if score #rdOvFrame rd matches 0 run ' + setmodel('stake_0'),
    'execute if score @s rdOvKind matches 2 if score #rdOvFrame rd matches 4 run ' + setmodel('stake_1'),
    # Illusion cue (5) charges for its last three ticks; it dies on the slash tick.
    'execute if score @s rdOvKind matches 5 run function rlk:boss/raiden/object_vfx/cue_tick',
    # Swing arc (6) fades; the sword wave (7) flies 5.5 blocks a tick to the line's end.
    'execute if score @s rdOvKind matches 6 if score @s rdOvAge matches 2 run ' + setmodel('swing_fade'),
    'execute if score @s rdOvKind matches 7 if score @s rdOvAge matches 1.. run tp @s ^ ^ ^5.5',
    'execute if score @s rdOvKind matches 7 if score @s rdOvAge matches 3 run ' + setmodel('wave_fade'),
    'execute if score @s rdOvKind matches 3 if score @s rdOvAge matches 3 run ' + setmodel('object_break_fade'),
    'execute if score @s rdOvKind matches 4 if score @s rdOvAge matches 3 run ' + setmodel('flower_break_fade'),
])
print('Generated 14 layered-alpha object lightning models: eyes, stakes, illusion cue/swing/wave and fading break flashes.')
