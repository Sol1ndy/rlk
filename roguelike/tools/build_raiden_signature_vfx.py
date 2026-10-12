"""Display geometry for the flower dome, transformation and final calamity.

Native alpha shells, dimensional cut ribbons and breakable shield meshes.
Generate after the encounter controller; hooks live there.
"""
from pathlib import Path
import argparse
import json
import math

DP = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--resourcepack', required=True)
RP = Path(parser.parse_args().resourcepack)
OUT = DP / 'data/rlk/function/boss/raiden/vfx'
SCALE = 16
TEXTURES = {name: 'rlk:raiden/fx/' + tex for name,tex in
            [('purple','violet_dense'),('blue','blue'),('cyan','cyan'),('white','white'),
             ('glow','glow'),('lavender','lavender'),('violet','violet'),('after','afterglow'),
             ('void','void'),('glass','shield_glass'),('mist','shield_mist')]}
from build_raiden_materials import build_materials
build_materials(RP)


def write(name, lines):
    p = OUT / (name + '.mcfunction')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def box(center, size, color):
    a = [round(8 + (center[i] - size[i]/2)*16/SCALE, 5) for i in range(3)]
    b = [round(8 + (center[i] + size[i]/2)*16/SCALE, 5) for i in range(3)]
    return {'from': a, 'to': b, 'shade': False,
            'faces': {f: {'texture': '#' + color, 'uv': [0, 0, 16, 16]}
                      for f in ['north', 'south', 'east', 'west', 'up', 'down']}}


def stroke(points, width, color, plane='floor', core=False):
    # Overlapping short cuboids make continuous native Minecraft zigzags. The
    # bright stripe protrudes from two faces; it is not hidden inside the shell.
    result = []
    for a, b in zip(points, points[1:]):
        distance = math.dist(a, b)
        count = max(1, math.ceil(distance/.42))
        for j in range(count):
            p = [a[i] + (b[i]-a[i])*j/count for i in range(3)]
            q = [a[i] + (b[i]-a[i])*(j+1)/count for i in range(3)]
            c = [(p[i]+q[i])/2 for i in range(3)]
            size = [abs(q[i]-p[i]) + width for i in range(3)]
            result.append(box(c, size, color))
            if core:
                result.append(box(c,[s+width*.8 for s in size],'glow'))
                exposed = 1 if plane == 'floor' else 2
                bright = [abs(q[i]-p[i])+width*.17 for i in range(3)]
                bright[exposed] = size[exposed] + .014
                result.append(box(c, bright, 'white'))
    return result


def ring(r, y, width, color, core=False):
    count = max(24, math.ceil(2*math.pi*r/.55))
    points = [(r*math.cos(i*2*math.pi/count), y, r*math.sin(i*2*math.pi/count))
              for i in range(count+1)]
    return stroke(points, width, color, core=core)


def column(x, z, height=14, width=.2, phase=0):
    # A bold broken main bolt, plus two thinner forks spreading near the floor.
    flip = -1 if phase % 2 else 1
    points = [(x, height, z), (x-.55*flip, height*.82, z+.2),
              (x+.6*flip, height*.64, z-.3), (x-.18*flip, height*.48, z+.12),
              (x+.5*flip, height*.27, z-.1), (x, .15, z)]
    result = stroke(points, width, 'purple', plane='vertical', core=True)
    for side in [-1, 1]:
        branch = [points[3], (x+side*1.05, height*.32, z+.35),
                  (x+side*.8, height*.16, z+.65), (x+side*1.9, .12, z+.9)]
        result += stroke(branch, width*.48, 'cyan', plane='vertical')
    return result


def model(name, elements):
    root = RP / 'assets/rlk'
    p = root / ('models/item/raiden/fx_signature/' + name + '.json')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({'ambientocclusion': False,
        'textures': {**TEXTURES, 'particle': TEXTURES['purple']}, 'elements': elements},
        separators=(',', ':')) + '\n', encoding='utf-8')
    p = root / ('items/raiden/fx_signature/' + name + '.json')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({'model': {'type': 'minecraft:model',
        'model': 'rlk:item/raiden/fx_signature/' + name}}, separators=(',', ':'))+'\n', encoding='utf-8')


def spawn(name, kind, life, setup=()):
    return [
        'summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_sfx","rlk_rd_sfx_new"],'
        'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_signature/' + name + '"}},'
        'item_display:"none",brightness:{sky:15,block:15},view_range:4f,shadow_radius:0f,'
        'width:0f,height:0f,interpolation_duration:1,start_interpolation:0,'
        'transformation:{translation:[0f,0f,0f],scale:[16f,16f,16f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,1f,0f,0f]}}',
        'scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxAge -1',
        f'scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxLife {life}',
        f'scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxKind {kind}',
        *setup,
        'tag @e[tag=rlk_rd_sfx_new] remove rlk_rd_sfx_new',
    ]



# Radius-four protected hemisphere. Thin alpha panels cover the surface;
# opaque lines are reserved for the rim, contact point and branching cracks.
def dome_panels():
    panels=[]
    for iy in range(16):
        y=(iy+.5)/4
        radius=math.sqrt(max(0,16-y*y))
        for iz in range(-12,12):
            z=(iz+.5)*radius/12
            x=math.sqrt(max(0,radius*radius-z*z))
            for side in [-1,1]:
                panels.append(((side*x,y+.07,z),(.035,.267,radius/12+.025)))
    return panels

PANELS=dome_panels()
dome=[box(c,size,'glass') for c,size in PANELS]
dome+=ring(4,.07,.055,'cyan')+ring(3.94,.09,.12,'glow')
for y in [.85,2.1,3.25]:
    dome+=ring(math.sqrt(16-y*y),y+.07,.024,'mist')
for angle in [0,math.pi/2]:
    points=[(4*math.cos(t)*math.cos(angle),4*math.sin(t)+.07,
             4*math.cos(t)*math.sin(angle)) for t in [i*math.pi/24 for i in range(25)]]
    dome+=stroke(points,.018,'lavender')
model('dome',dome)

def dome_cracks(stage):
    mesh=[]
    # Branches follow the actual hemisphere, not a flat glyph hovering inside.
    for branch in range(3+stage*3):
        theta=branch*2.39996+.23
        points=[]
        for j in range(5+stage):
            polar=.25+j*(.12+stage*.015)
            angle=theta+(0.09 if j%2 else -.07)
            r=4.025*math.sin(polar)
            points.append((r*math.cos(angle),4.025*math.cos(polar)+.07,r*math.sin(angle)))
        mesh+=stroke(points,.075,'cyan',plane='vertical')
        mesh+=stroke(points,.022,'white',plane='vertical')
        if stage>=1:
            a=points[3]; polar=.8+stage*.055
            r=4.04*math.sin(polar)
            b=(r*math.cos(theta+.22),4.04*math.cos(polar)+.07,r*math.sin(theta+.22))
            mesh+=stroke([a,b],.042,'cyan',plane='vertical',core=True)
    return mesh

contact=ring(math.sqrt(16-2.0**2),2.07,.065,'cyan',True)
model('dome_hit',dome+contact+dome_cracks(0))
for stage in range(1,4):
    model('dome_crack_'+str(stage),dome+contact+dome_cracks(stage))

for stage in range(4):
    # Shell tiles open into separated plates; growing gaps and lower alpha
    # reveal the world behind the protective barrier after it absorbed the cut.
    mesh=[]
    for i,(c,size) in enumerate(PANELS):
        if (i*7)%13 < stage+1: continue
        scale=1+stage*.04
        target=(c[0]*scale,c[1]-.035*stage*stage,c[2]*scale)
        mesh.append(box(target,(size[0],size[1]*(.86-stage*.10),size[2]*(.86-stage*.10)),
                        'glass' if i%5 else 'mist'))
    mesh+=ring(4,.07,.055,'cyan')
    mesh+=dome_cracks(3)
    model('dome_fracture_'+str(stage),mesh)

for stage in range(3):
    mesh=[]
    for i,(c,size) in enumerate(PANELS):
        if i%4: continue
        spread=1.16+stage*.14
        target=(c[0]*spread,c[1]-(.20+stage*.45),c[2]*spread)
        mesh.append(box(target,(max(.04,size[0]*2),size[1]*(.55-stage*.10),size[2]*(.55-stage*.10)),
                        'mist' if stage<2 else 'glow'))
        if i%20==0 and stage<2:
            mesh+=stroke([target,(target[0]*1.02,target[1]-.18,target[2]*1.02)],.025,'cyan')
    model('dome_shatter_'+str(stage),mesh)

warning=ring(22.6,.09,.095,'violet')+ring(22.9,.10,.025,'cyan')
for i in range(8):
    a=math.pi*i/4;dx,dz=math.cos(a),math.sin(a)
    for side in [-1,1]:
        warning+=stroke([(dx*22+dz*side*.65,.1,dz*22-dx*side*.65),(dx*20,.1,dz*20)],.07,'purple')
model('judgment_warning',warning)
for stage in range(3):
    # The hand/weapon cinematic owns the spatial rift overhead. Here only
    # the fixed arena boundary intensifies; there is no descending thunderbolt.
    mesh=list(warning)
    mesh+=ring(22.4,.11,.04+.025*stage,'lavender')
    for i in range(12):
        a=math.pi*i/6
        mesh+=stroke([(22.7*math.cos(a),.12,22.7*math.sin(a)),
                      (22.3*math.cos(a+.02),.20+.15*stage,22.3*math.sin(a+.02))],.08,'purple',core=True)
    model('judgment_charge_'+str(stage),mesh)

def cut_ribbon(points,width,color):
    mesh=[]
    for a,b in zip(points,points[1:]):
        # Thin horizontal folded band, rather than a solid vertical wall.
        center=((a[0]+b[0])/2,(a[1]+b[1])/2,(a[2]+b[2])/2)
        mesh.append(box(center,(abs(a[0]-b[0])+.05,.035,abs(a[2]-b[2])+width),color))
    return mesh

for frame in range(3):
    impact=[]
    # A field-wide horizontal sword cut. Frame zero already spans the complete
    # path on the damage tick; later frames are shock-ribbon afterimages.
    path=[(-22+i*.5,2.0+.025*math.sin(i*.7+frame),3+1.35*math.sin((-22+i*.5)*.13)) for i in range(89)]
    impact+=cut_ribbon(path,1.9,'glow')
    impact+=cut_ribbon(path,.65+.15*frame,'violet')
    impact+=stroke(path,.17,'purple',core=True)
    for offset in [-.6,.6]:
        impact+=stroke([(x,y+.10,z+offset) for x,y,z in path],.065,'lavender')
    # Curved energy sheets on either wing give the slash volume and direction.
    for radius in [10,17,22]:
        points=[(radius*math.sin(math.radians(a)),1.85+.13*math.sin(math.radians(a*2)),
                 radius*math.cos(math.radians(a))) for a in range(-160,161,5)]
        impact+=cut_ribbon(points,.85,'glow')
        impact+=stroke(points,.08,'violet')
    def outside_dome(e):
        ax,az,bx,bz=e['from'][0]-8,e['from'][2]-8,e['to'][0]-8,e['to'][2]-8
        dx=max(ax,0,-bx);dz=max(az-3,0,3-bz)
        return dx*dx+dz*dz > 4.1**2
    blocked=[e for e in impact if outside_dome(e)]
    for suffix,mesh in [('',impact),('_blocked',blocked)]:
        model('judgment_strike'+suffix+'_'+str(frame),mesh)
        if frame==0:
            after=json.loads(json.dumps(mesh))
            for element in after:
                for face in element['faces'].values():
                    face['texture']='#after' if face['texture']!='#glow' else '#glow'
            model('judgment_after'+suffix,after)

charge = ring(2.2, 2.7, .055, 'purple') + ring(1.6, 4.3, .07, 'cyan')
for i in range(4):
    a = math.pi*i/2
    charge += stroke([(math.cos(a)*2.2, 2.7, math.sin(a)*2.2),
                      (math.cos(a+.4)*1.5, 3.6, math.sin(a+.4)*1.5),
                      (math.cos(a)*1.6, 4.3, math.sin(a)*1.6), (0, 6, 0)],
                     .08, 'purple', plane='vertical', core=True)
model('transform_charge', charge)

# Arrival/departure rifts: a narrow vertical crack with forked rims, rather
# than a cloud of portal particles. The two instances stay at each endpoint.
blink = []
for side in [-1, 1]:
    blink += stroke([(side*.10, .05, 0), (side*.5, .7, .03), (side*.3, 1.2, -.1),
                     (side*.6, 1.8, .08), (side*.18, 2.6, 0), (0, 3.2, 0)],
                    .075, 'purple', plane='vertical', core=True)
    for y in [.6, 1.4, 2.2]:
        blink += stroke([(side*.2, y, .04), (side*.9, y+.1, -.1),
                         (side*1.15, y+.5, .1)], .045, 'purple', plane='vertical')
blink += ring(.8, .08, .04, 'purple')
model('blink', blink)

# Fast dispersal is made of crisp display fragments. The controller hides the
# body between the departure and arrival; these endpoint meshes carry its
# silhouette into scattered wisps rather than suggesting an instantaneous TP.
for frame in range(4):
    fragments=[]
    spread=[.05,.33,.78,1.35][frame]
    for i in range(42):
        angle=i*2.39996
        base=.17+.025*(i%6)
        y=.15+(i%12)*.185
        r=base+spread*(.52+(i%4)*.20)
        x,z=r*math.cos(angle),r*math.sin(angle)
        # Fragment motion also streaks to the rear, following the body's facing.
        z-=spread*.65
        w=.025+(i%3)*.018
        h=.12+(i%4)*.065
        color='purple' if frame<2 else 'violet' if frame==2 else 'after'
        fragments+=stroke([(x,y,z),(x+math.cos(angle)*(.08+spread*.22),
                                   y+.10+spread*.10,z+math.sin(angle)*(.12+spread*.28))],w,color,plane='vertical',core=frame<2 and i%6==0)
        fragments.append(box((x,y+h/2,z),(w*.65,h,.025),'lavender'))
    if frame<2:
        fragments+=ring(.32+spread,.08,.032,'violet')
    model('blink_scatter_'+str(frame),fragments)

# A hollow shell of angular armor splinters expands and falls away. Separate
# geometry replaces the flash particle and explains the disappearing armor.
shards = []
for i in range(18):
    a = i*2*math.pi/18
    r = 1.0+(i % 3)*.3
    y = .6+(i % 5)*.55
    x, z = r*math.cos(a), r*math.sin(a)
    points = [(x*.8, y-.14, z*.8), (x, y+.2, z), (x*1.12, y+.48, z*1.12)]
    shards += stroke(points, .11 if i % 2 else .17, 'purple', plane='vertical', core=i % 3 == 0)
model('armor_break', shards)

# ---- Painted gradient cards (rlk:raiden/fxg/*) ---------------------------------------
# The calamity cut, its wings and afterglow, the arena warning ring, the transformation
# charge, the blink rifts and the armour shards are rebuilt from flat painted cards
# (tools/build_raiden_fx_textures.py) instead of stair-stepped cubes with flat swatches.
# They keep the same model names, so the functions below are unchanged. The dome shell
# stays a glass shell.
from raiden_obj_cards import Model, save, ensure_textures, fx_names, polar

FX = fx_names()
ensure_textures(RP, FX)


def cm():
    return Model(SCALE, FX)


def cut_path_z(x):
    return 3 + 1.35*math.sin(x*.13)


def outside_dome_card(el):
    ax, az, bx, bz = el['from'][0]-8, el['from'][2]-8, el['to'][0]-8, el['to'][2]-8
    dx = max(ax, 0, -bx)
    dz = max(az-3, 0, 3-bz)
    return dx*dx+dz*dz > 4.1**2


def arc_cards(m, radius, y, start, end, width, tex, step=22.5):
    # Chords of a horizontal arc around the arena centre, one card per 22.5 degrees.
    a = start
    while a <= end+1e-6:
        chord = 2*radius*math.sin(math.radians(step/2))
        m.hcard(polar(radius, a, y), a+90, chord*1.04, width, tex)
        a += step


def calamity(frame, after=False):
    m = cm()
    cores = [['blade_a', 'blade_b', 'blade_c', 'blade_a'], ['blade_b', 'blade_c', 'blade_a', 'blade_b'],
             ['blade_c', 'blade_a', 'blade_b', 'blade_c']][frame]
    bolts = [['bolt_a', 'bolt_b', 'bolt_c', 'bolt_d'], ['bolt_c', 'bolt_d', 'bolt_a', 'bolt_b'], None][frame]
    fade = [1.0, .8, .6][frame]
    # Four long straight cards (11 blocks each) along the cut at z = 3, y = 2: few seams,
    # about 46 texels per block. Alternate cards are mirrored so the sprite never tiles.
    for i in range(4):
        x = -16.5+11*i
        uv = (0, 0, 16, 16) if i % 2 == 0 else (16, 0, 0, 16)
        y, z = 2.0, 3.0
        if after:
            m.vcard((x, y, z), 90, 11.7, .9, 'bolt_after_a' if i % 2 else 'bolt_after_c', uv)
            m.hcard((x, y-.04, z), 90, 11.7, 1.6, 'blade_trail_b', uv)
            continue
        # White-hot cut seen from the locked camera, a violet wake on the cut plane and,
        # on the first frames, a jagged bolt wrapped around it.
        m.vcard((x, y, z-.04), 90, 11.7, 1.9*fade, 'glow_strip', uv)
        m.vcard((x, y, z), 90, 11.7, .55*fade+.25, cores[i], uv)
        m.hcard((x, y-.03, z), 90, 11.7, 2.1*fade, 'blade_trail_a', uv)
        if bolts:
            m.vcard((x, y+.02, z+.04), 90, 11.7, 1.3, bolts[i], uv)
    if not after:
        # Curved energy sheets either side give the cut its sweep across the arena.
        for radius, width in ([(10, 1.1), (17, 1.0), (22, .9)][:3-frame]):
            arc_cards(m, radius, 1.85, -157.5, 157.5, width, 'slash_wave' if frame == 0 else 'blade_trail_b')
    return m


for frame in range(3):
    m = calamity(frame)
    save(RP, 'fx_signature', 'judgment_strike_'+str(frame), m)
    blocked = cm()
    blocked.textures = m.textures
    blocked.elements = [e for e in m.elements if outside_dome_card(e)]
    save(RP, 'fx_signature', 'judgment_strike_blocked_'+str(frame), blocked)
after = calamity(0, after=True)
save(RP, 'fx_signature', 'judgment_after', after)
after_blocked = cm()
after_blocked.textures = after.textures
after_blocked.elements = [e for e in after.elements if outside_dome_card(e)]
save(RP, 'fx_signature', 'judgment_after_blocked', after_blocked)


def boundary(stage=None):
    # The arena edge at radius 22.6: a soft violet band with crackle, plus inward sparks.
    m = cm()
    arc_cards(m, 22.6, .09, 0, 337.5, .7, 'glow_strip')
    arc_cards(m, 22.6, .11, 0, 337.5, .5, 'rim_crackle_a' if not stage else 'rim_crackle_b')
    for k in range(8):
        m.crossed(polar(21.4, k*45, .5), .9, 'charge_spark', planes=2, sv=1.0)
    if stage is not None:
        for k in range(16):
            a = k*22.5
            chord = 2*22.6*math.sin(math.radians(11.25))
            h = .35+.25*stage
            m.vcard(polar(22.7, a, h/2+.05), a+90, chord, h, 'crackle_a' if k % 2 else 'crackle_b')
    return m


save(RP, 'fx_signature', 'judgment_warning', boundary())
for stage in range(3):
    save(RP, 'fx_signature', 'judgment_charge_'+str(stage), boundary(stage))

m = cm()
m.hcard((0, 2.7, 0), 0, 5.4, 5.4, 'chakra_a')
m.hcard((0, 4.3, 0), 45, 3.8, 3.8, 'chakra_b')
m.crossed((0, 3.1, 0), 2.4, 'vbolt_a', planes=4, sv=6.0)
m.crossed((0, 6.0, 0), 2.2, 'flash', planes=2)
m.hcard((0, .06, 0), 0, 5.0, 5.0, 'scorch')
save(RP, 'fx_signature', 'transform_charge', m)

m = cm()
# A tall tear of light where she breaks apart / reforms, forked arcs and a floor scorch.
m.card((0, 1.6, 0), 'z', '+y', '+x', 3.4, .9, 'rift_a')
m.card((0, 1.6, .02), 'x', '+y', '+z', 3.4, .9, 'rift_b')
for y in (.7, 1.5, 2.3):
    for side in (-1, 1):
        m.vcard((side*.55, y, 0), 90, .9, .45, 'arc_a' if side > 0 else 'arc_b')
m.hcard((0, .05, 0), 0, 1.8, 1.8, 'scorch')
save(RP, 'fx_signature', 'blink', m)

m = cm()
for i in range(18):
    a = (i*22.5) % 360
    r = 1.0+(i % 3)*.3
    y = .6+(i % 5)*.55
    p = polar(r, a, y)
    m.crossed(p, .55 if i % 2 else .8, 'glint', planes=2)
    m.vcard(polar(r*1.08, a, y+.25), a, .45, .9, 'obj_shard')
save(RP, 'fx_signature', 'armor_break', m)

write('init', [f'scoreboard objectives add {n} dummy' for n in ['rdSfxAge', 'rdSfxLife', 'rdSfxKind', 'rdSfxStyle']])
write('dome_create', spawn('dome', 1, 260))
write('judgment_warning', spawn('judgment_warning', 2, 125))
write('judgment_strike', spawn('judgment_strike_0', 3, 12, [
    'scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxStyle 0',
    'execute if entity @e[tag=rlk_rd_dome,limit=1] run scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxStyle 1',
    'execute if entity @e[tag=rlk_rd_dome,limit=1] run data modify entity @e[tag=rlk_rd_sfx_new,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/judgment_strike_blocked_0"',
]) + [
    'kill @e[tag=rlk_rd_sfx,scores={rdSfxKind=2}]',
    'execute as @e[tag=rlk_rd_sfx,scores={rdSfxKind=1}] run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/dome_hit"',
    'playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1.4 0.55 0.6',
    'playsound minecraft:entity.iron_golem.attack hostile @a[tag=player] ~ ~ ~ 1.0 0.65 0.5',
    'playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.65 0.70 0.4',
])
write('transform', spawn('transform_charge', 4, 70))
for name, kind, life in [('blink_arrive', 5, 10), ('blink_depart', 6, 7)]:
    write(name, spawn('blink', kind, life, [
        'data modify entity @e[tag=rlk_rd_sfx_new,limit=1] Rotation set from entity @s Rotation',
        'data modify entity @e[tag=rlk_rd_sfx_new,limit=1] Rotation[1] set value 0f',
    ]))
write('armor_break', spawn('armor_break', 7, 15))
write('world', ['execute as @e[tag=rlk_rd_sfx] at @s run function rlk:boss/raiden/vfx/tick'])
tick = [
    'scoreboard players add @s rdSfxAge 1',
    'execute if score @s rdSfxAge >= @s rdSfxLife run return run kill @s',
    'execute if score @s rdSfxKind matches 1 unless entity @e[tag=rlk_rd_dome,limit=1] run return run kill @s',
    'execute if score @s rdSfxKind matches 2 unless entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=..119},limit=1] run return run kill @s',
    'execute if score @s rdSfxKind matches 4 unless entity @e[tag=rlk_raiden,scores={rdPhase=1},limit=1] run return run kill @s',
]
def at_age(kind, age, command):
    return f'execute if score @s rdSfxKind matches {kind} if score @s rdSfxAge matches {age} run {command}'
def modelset(name):
    return 'data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/'+name+'"'
def transform(scale, translation=(0,0,0), duration=2):
    a = lambda v:'['+','.join(str(x)+'f' for x in v)+']'
    return 'data merge entity @s {interpolation_duration:'+str(duration)+',start_interpolation:0,transformation:{scale:'+a(scale)+',translation:'+a(translation)+'}}'
for age, stage in [(35,0),(75,1),(105,2)]:
    tick.append(at_age(2, age, modelset('judgment_charge_'+str(stage))))
for suffix, style in [('',0),('_blocked',1)]:
    for age in [1,2]:
        tick.append(at_age(3, age, f'execute if score @s rdSfxStyle matches {style} run '+modelset('judgment_strike'+suffix+'_'+str(age))))
    tick.append(at_age(3, 4, f'execute if score @s rdSfxStyle matches {style} run '+modelset('judgment_after'+suffix)))

# Dome reaction is synchronized to the sword, independent of when the flower
# was broken. The gameplay marker remains until the protected cinematic ends.
for moment,name in [(120,'dome_hit'),(125,'dome_crack_1'),(134,'dome_crack_2'),(145,'dome_crack_3'),
                    (149,'dome_fracture_0'),(155,'dome_fracture_1'),(161,'dome_fracture_2'),(167,'dome_fracture_3'),
                    (171,'dome_shatter_0'),(173,'dome_shatter_1'),(175,'dome_shatter_2')]:
    tick.append('execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime='+str(moment)+'},limit=1] run '+modelset(name))
for moment,snd,vol,pitch in [(125,'block.respawn_anchor.deplete',.30,1.3),
                            (145,'entity.iron_golem.damage',.35,1.2),
                            (171,'block.beacon.deactivate',.55,1.1)]:
    tick.append('execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime='+str(moment)+'},limit=1] run playsound minecraft:'+snd+' hostile @a[tag=player] ~ ~ ~ '+str(vol)+' '+str(pitch)+' .2')

tick += [
    at_age(5,0,modelset('blink_scatter_3')),at_age(5,2,modelset('blink_scatter_2')),
    at_age(5,4,modelset('blink_scatter_1')),at_age(5,6,modelset('blink_scatter_0')),
    at_age(5,8,transform([.1,16,.1],duration=1)),
    at_age(6,0,modelset('blink_scatter_0')),at_age(6,1,modelset('blink_scatter_1')),
    at_age(6,3,modelset('blink_scatter_2')),at_age(6,5,modelset('blink_scatter_3')),
    at_age(7,1,transform([22,19,22],[0,.15,0])),
    at_age(7,5,transform([27,20,27],[0,-.4,0],duration=4)),
    at_age(7,10,transform([30,16,30],[0,-3,0],duration=4)),
]
write('tick', tick)
print('Generated signature display effects: animated calamity, protected dome, transform, blink rifts and armor shards.')
