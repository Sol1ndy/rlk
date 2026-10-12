"""Narukami illusion challenge (pattern 5): four running sword illusions, one real body.

Run from anywhere:  python3 tools/build_raiden_illusions.py --resourcepack <RP>

Writes data/rlk/function/boss/raiden/illusion/*.mcfunction and the skin-based pose
models rlk:raiden/illusion_{ready,run_0..3,wind,slash}. The encounter controller only
dispatches to illusion/tick (patterns/5), calls illusion/on_break from object/break and
illusion/cleanup from pause/transform/exhausted/cleanup/reload/death.

Timeline (boss rdTime / volley clock):
  1      the boss scatters where she stands (movement/depart); the hidden body crosses
         to the arena centre in the same frame.
  3      the body reforms at the centre (movement/arrive) ...
  7      ... and splits: four identical illusions appear there, one secretly real.
  8-21   they run out in four directions (1 block/tick, 4-frame stride, forward lean).
  22     they hold their spots 14 blocks out and turn to face the centre (hittable now).
  23+    four volleys, about 1.7 s apart. In each, all four wind up together with
         identical tells (a ground line toward the centre, 14 ticks) and slash toward the
         centre at once: a fake cuts once, the real one cuts an X - two quick diagonal
         strokes, the second line landing 3 ticks after the first.
  end    after the fourth volley without finding her the others dissolve and the boss
         reforms on the real illusion's spot, then finish; like the original, 몽상의 일심
         (pattern 7) always follows an illusion round that was not broken.
  hit    shattering the real illusion at any time once they hold their spots: pending
         slashes vanish, the others dissolve, the boss reforms there and is stunned for
         10 s (rdPat 98: collapse, kneel, recover); a fake just shatters.
Every relocation of the boss is hidden behind depart/arrive art; nothing snaps in view.
"""
from pathlib import Path
import argparse
import json
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'data/rlk/function/boss/raiden/illusion'
parser = argparse.ArgumentParser()
parser.add_argument('--resourcepack', required=True)
RP = Path(parser.parse_args().resourcepack)

# ---- Encounter tuning -----------------------------------------------------------
RUN_FROM, RUN_TICKS, RUN_STEP = 8, 14, 1.0       # 14 x 1.0 = 14 blocks from the centre
SPAWN_T, ARRIVE_T = 7, 3
HOLD_T = RUN_FROM+RUN_TICKS                      # 22: take positions, hittable from here
VOLLEYS = 4                                      # simultaneous volleys before it ends
TELL = 14                                        # shared wind-up of every volley (0.7 s)
STRIKE = 1+TELL                                  # volley clock 15: everyone cuts
XGAP = 3                                         # the real one's second X stroke: clock 18
X_YAW = 15                                       # its second line, turned off the first
VOLLEY_END = STRIKE+XGAP+16                      # 34 ticks per volley
STUN = 200                                       # 10 s stun after the real one is found
DAMAGE = 10
SHAPE = 13                                       # hazard: 22-long, 2.4-wide sword wave
REFORM = 5                                       # arrive art needs 5 ticks to finish forming

written = set()


def write(name, lines):
    p = OUT/(name+'.mcfunction')
    p.parent.mkdir(parents=True, exist_ok=True)
    text = lines.strip() if isinstance(lines, str) else '\n'.join(lines)
    p.write_text(text+'\n', encoding='utf-8')
    written.add(p)


def call(name):
    return 'function rlk:boss/raiden/'+name


def sound(event, vol=1, pitch=1, at='~ ~1 ~'):
    return f'playsound minecraft:{event} hostile @a[tag=player] {at} {vol} {pitch} 0.2'


ILL = '@e[tag=rlk_rd_illusion]'
VIS = '@e[type=minecraft:item_display,tag=rlk_rd_ilvis]'
ACT = '@e[tag=rlk_rd_ilact,limit=1]'
CENTER = '@e[tag=rlk_raiden_arena,limit=1]'
BOSS = '@e[tag=rlk_raiden,limit=1]'
BODY = '@e[tag=rlk_body,limit=1]'


def model_set(name):
    return 'data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/'+name+'"'


def transform(lean):
    # Lean the whole figure forward about its waist (entity-local +X axis, forward +Z)
    # and slide it so the feet stay planted on the floor.
    a = math.radians(lean)
    q = [math.sin(a/2), 0, 0, math.cos(a/2)]
    t = [0, LIFT*math.cos(a), LIFT*math.sin(a)]
    f = lambda v: f'{v:.6f}f'
    return ('{translation:['+','.join(f(v) for v in t)+'],left_rotation:['+','.join(f(v) for v in q)+'],'
            f'scale:[{f(DISPLAY)},{f(DISPLAY)},{f(DISPLAY)}],right_rotation:[0f,0f,0f,1f]}}')


# ---- Pose models ------------------------------------------------------------------
# Authored in figure pixels: feet at the origin, front -Z (the skin's north face),
# character right +X. ItemDisplayRenderer's 180 degree turn puts the front on the
# entity's facing direction (identity right_rotation, like the boss rig parts).
# Element rotations stay single-axis in 22.5 degree steps (valid in every version).
FIG = 1.2                # same size as the real body (attribute scale 1.2)
DISPLAY = 2.4            # display scale; models use half-size pixels for headroom
LIFT = 1.2               # display translation: model centre at waist height
TINT = 0xE0D0FF          # faint lavender over the skin: still Raiden, visibly an illusion
assert abs(FIG/16*16/DISPLAY-.5) < 1e-9


def mp(p):
    return [round(8+p[0]*.5, 4), round(8+(p[1]*FIG/16-LIFT)*16/DISPLAY, 4), round(8+p[2]*.5, 4)]


def rot(p, pivot, axis, angle):
    a = math.radians(angle)
    c, s = math.cos(a), math.sin(a)
    x, y, z = (p[i]-pivot[i] for i in range(3))
    if axis == 'x':
        y, z = y*c-z*s, y*s+z*c
    elif axis == 'y':
        z, x = z*c-x*s, z*s+x*c
    else:
        x, y = x*c-y*s, x*s+y*c
    return (x+pivot[0], y+pivot[1], z+pivot[2])


def skin_faces(u, v, w, h, d, start=0, end=None):
    end = h if end is None else end
    face = lambda a, b, c, e: {'uv': [a/4, b/4, c/4, e/4], 'texture': '#skin', 'tintindex': 0}
    return {'east': face(u, v+d+start, u+d, v+d+end), 'north': face(u+d, v+d+start, u+d+w, v+d+end),
            'west': face(u+d+w, v+d+start, u+2*d+w, v+d+end), 'south': face(u+2*d+w, v+d+start, u+2*d+2*w, v+d+end),
            'up': face(u+d, v, u+d+w, v+d), 'down': face(u+d+w, v+d, u+d+2*w, v)}


def flat_faces(tex):
    return {f: {'uv': [0, 0, 16, 16], 'texture': '#'+tex} for f in ('north', 'south', 'east', 'west', 'up', 'down')}


# Standard 64x64 player-skin boxes (u, v, w, h, d) and their second-layer boxes.
HEAD = ((0, 0, 8, 8, 8), (32, 0, 8, 8, 8))
TORSO = ((16, 16, 8, 12, 4), (16, 32, 8, 12, 4))
ARM = {'r': ((40, 16, 4, 12, 4), (40, 32, 4, 12, 4)), 'l': ((32, 48, 4, 12, 4), (48, 48, 4, 12, 4))}
LEG = {'r': ((0, 16, 4, 12, 4), (0, 32, 4, 12, 4)), 'l': ((16, 48, 4, 12, 4), (0, 48, 4, 12, 4))}


class Figure:
    def __init__(self):
        self.raw = []            # (lo, hi, faces, pivot, axis, angle) in figure pixels
        self.feet = []

    def seg(self, pivot, lo, hi, uvs, rows, r, overlay=.25, aura=.75):
        axis, angle = r
        base, over = uvs
        for inflate, faces in ((0, skin_faces(*base, *rows)), (overlay, skin_faces(*over, *rows)),
                               (aura, flat_faces('glow'))):
            a = tuple(pivot[i]+lo[i]-inflate for i in range(3))
            b = tuple(pivot[i]+hi[i]+inflate for i in range(3))
            self.raw.append((a, b, faces, pivot, axis, angle))

    def box(self, lo, hi, tex, pivot, axis, angle):
        self.raw.append((lo, hi, flat_faces(tex), pivot, axis, angle))

    def elements(self):
        # Plant the lowest foot corner on the floor.
        drop = -min(p[1] for p in self.feet)
        out = []
        for lo, hi, faces, pivot, axis, angle in self.raw:
            sh = lambda p: (p[0], p[1]+drop, p[2])
            e = {'from': mp(sh(lo)), 'to': mp(sh(hi)), 'faces': faces}
            if angle:
                e['rotation'] = {'origin': mp(sh(pivot)), 'axis': axis, 'angle': angle}
            for v in e['from']+e['to']:
                assert -16 <= v <= 32, (v, lo, hi)
            out.append(e)
        return out


def katana(fig, hand, along, edge, side, r):
    """Pale violet katana, grip at the hand, blade toward `along`, cutting edge toward `edge`."""
    axis, angle = r

    def piece(a0, a1, e0, e1, s0, s1, tex):
        corners = [tuple(hand[i]+a*along[i]+e*edge[i]+s*side[i] for i in range(3))
                   for a in (a0, a1) for e in (e0, e1) for s in (s0, s1)]
        lo = tuple(min(c[i] for c in corners) for i in range(3))
        hi = tuple(max(c[i] for c in corners) for i in range(3))
        fig.box(lo, hi, tex, hand, axis, angle)

    piece(-4.3, -3.6, -.8, .8, -.8, .8, 'gold')                  # kashira
    piece(-3.6, .9, -.6, .6, -.55, .55, 'grip')                 # wrapped grip
    for a in (-2.9, -1.7, -.5):
        piece(a, a+.3, -.66, .66, -.6, .6, 'gold')               # menuki bands
    piece(.9, 1.5, -1.7, 1.7, -1.7, 1.7, 'gold')                # tsuba
    piece(1.5, 2.1, -.75, .8, -.42, .42, 'gold')                # habaki
    start, length, n = 2.1, 17.4, 8
    for i in range(n):
        a0, a1 = start+length*i/n, start+length*(i+1)/n
        mid = (a0+a1)/2-start
        c = -1.05*(mid/length)**2                                # tip curves toward the spine
        w = 1.5-.06*i
        piece(a0, a1, c-.55, c+w-.55, -.22, .22, 'blade')
        piece(a0, a1, c+w-.8, c+w-.42, -.27, .27, 'edge')         # bright cutting edge
        piece(a0, a1, c-.25, c+.08, -.26, .26, 'core')            # shinogi groove
        piece(a0, a1, c-.85, c+w-.25, -.5, .5, 'violet')          # electro sheen (translucent)
    c = -1.05
    piece(start+length, start+length+1.1, c-.25, c+.55, -.18, .18, 'edge')  # kissaki


def figure(pose):
    fig = Figure()
    hip = (0, 12, 0)
    torso = pose.get('torso', ('x', 0))
    fig.seg(hip, (-4, 0, -2), (4, 12, 2), TORSO, (0, 12), torso)
    neck = rot((0, 24, 0), hip, *torso)
    fig.seg(neck, (-4, 0, -4), (4, 8, 4), HEAD, (0, 8), pose.get('head', torso), .5, .9)
    hand = None
    for side, sx in (('r', 1), ('l', -1)):
        shoulder = rot((6*sx, 22, 0), hip, *torso)
        upper, fore = pose[side+'_arm'], pose[side+'_fore']
        fig.seg(shoulder, (-2, -4, -2), (2, 2, 2), ARM[side], (0, 6), upper)
        elbow = rot((shoulder[0], shoulder[1]-4, shoulder[2]), shoulder, *upper)
        fig.seg(elbow, (-2, -6, -2), (2, 0, 2), ARM[side], (6, 12), fore)
        if side == 'r':
            hand = rot((elbow[0], elbow[1]-5, elbow[2]), elbow, *fore)
        pelvis = (2*sx, 12, 0)
        thigh, shin = pose[side+'_thigh'], pose[side+'_shin']
        fig.seg(pelvis, (-2, -6, -2), (2, 0, 2), LEG[side], (0, 6), thigh)
        knee = rot((pelvis[0], 6, 0), pelvis, *thigh)
        fig.seg(knee, (-2, -6, -2), (2, 0, 2), LEG[side], (6, 12), shin)
        fig.feet += [rot((knee[0]+dx, knee[1]-6, knee[2]+dz), knee, *shin) for dx in (-2, 2) for dz in (-2, 2)]
    katana(fig, hand, *pose['katana'])
    return fig.elements()


X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
NX, NY, NZ = (-1, 0, 0), (0, -1, 0), (0, 0, -1)
# The sword arm trails the blade low behind while running (edge down, tip lifted).
RUN_SWORD = dict(r_arm=('x', -22.5), r_fore=('x', -45), katana=(Z, NY, X, ('x', 0)))
POSES = {
    # Guard at the spot: blade forward and up toward the centre, front knee bent.
    'illusion_ready': dict(r_arm=('x', 22.5), r_fore=('x', 45), l_arm=('z', -22.5), l_fore=('x', 22.5),
                           r_thigh=('x', 22.5), r_shin=('x', 0), l_thigh=('x', -22.5), l_shin=('x', -22.5),
                           katana=(Y, NZ, X, ('x', -45))),
    # Four-frame sprint stride: contact R, passing (left knee up), contact L, passing.
    'illusion_run_0': dict(RUN_SWORD, l_arm=('x', 22.5), l_fore=('x', 45),
                           r_thigh=('x', 45), r_shin=('x', 22.5), l_thigh=('x', -22.5), l_shin=('x', -45)),
    'illusion_run_1': dict(RUN_SWORD, l_arm=('x', 0), l_fore=('x', 22.5),
                           r_thigh=('x', 0), r_shin=('x', 0), l_thigh=('x', 45), l_shin=('x', 0)),
    'illusion_run_2': dict(RUN_SWORD, l_arm=('x', -45), l_fore=('x', -22.5),
                           l_thigh=('x', 45), l_shin=('x', 22.5), r_thigh=('x', -22.5), r_shin=('x', -45)),
    'illusion_run_3': dict(RUN_SWORD, l_arm=('x', -22.5), l_fore=('x', 0),
                           l_thigh=('x', 0), l_shin=('x', 0), r_thigh=('x', 45), r_shin=('x', 0)),
    # Wind-up for a horizontal cut: chest cocked right, blade drawn back flat at the
    # right hip, cutting edge outward; head keeps facing the centre; wide stance.
    'illusion_wind': dict(torso=('y', -22.5), head=('y', 0), r_arm=('z', 45), r_fore=('x', -45),
                          l_arm=('z', -22.5), l_fore=('x', 45),
                          r_thigh=('z', 22.5), r_shin=('x', 0), l_thigh=('z', -22.5), l_shin=('x', 0),
                          katana=(Z, X, Y, ('y', 22.5))),
    # Follow-through after cutting right-to-left: chest turned left, sword arm reaching
    # forward, blade flat across the front pointing left (edge trailing the sweep).
    'illusion_slash': dict(torso=('y', 22.5), head=('y', 0), r_arm=('x', 45), r_fore=('x', 45),
                           l_arm=('x', -45), l_fore=('x', -22.5),
                           r_thigh=('z', 22.5), r_shin=('x', 0), l_thigh=('z', -22.5), l_shin=('x', 0),
                           katana=(NX, Z, Y, ('y', -22.5))),
}
TEXTURES = {'skin': 'rlk:raiden/skin', 'glow': 'rlk:raiden/fx/glow', 'violet': 'rlk:raiden/fx/violet',
            'blade': 'rlk:raiden/fx/blade_pale', 'edge': 'rlk:raiden/fx/blade_edge',
            'core': 'rlk:raiden/fx/blade_core', 'grip': 'rlk:raiden/fx/grip_dark',
            'gold': 'rlk:raiden/fx/gold_dull', 'particle': 'rlk:raiden/fx/blade_pale'}
for name, pose in POSES.items():
    p = RP/f'assets/rlk/models/item/raiden/{name}.json'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({'ambientocclusion': False, 'textures': TEXTURES, 'elements': figure(pose)},
                            separators=(',', ':'))+'\n', encoding='utf-8')
    p = RP/f'assets/rlk/items/raiden/{name}.json'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({'model': {'type': 'minecraft:model', 'model': f'rlk:item/raiden/{name}',
                                       'tints': [{'type': 'minecraft:constant', 'value': TINT}]}},
                            separators=(',', ':'))+'\n', encoding='utf-8')


# ---- Controller ---------------------------------------------------------------------
write('tick', [
    '# patterns/5: as the boss at its feet every tick of rdPat 5; rdTime 1 is the first frame.',
    '# Global state lives on #rdIl* fake players (one encounter at a time):',
    '#   #rdIlStep 1 intro/run-out, 2 turns, 3 failed (reforming), 4 found (reforming).',
    'execute if score @s rdTime matches 1 run '+call('illusion/start'),
    'execute if score #rdIlStep rd matches 4 run return run '+call('illusion/won_tick'),
    'execute if score #rdIlStep rd matches 3 run return run '+call('illusion/fail_tick'),
    '# Lost state (should not happen): end visibly instead of hiding the boss forever.',
    'execute unless score #rdIlStep rd matches 1..2 run return run '+call('illusion/lost'),
    'execute if score #rdIlStep rd matches 1 run '+call('illusion/intro'),
    'execute if score #rdIlStep rd matches 2 run '+call('illusion/volleys'),
    'execute if score #rdIlStep rd matches 1..2 if score @s rdTime matches 400.. run '+call('illusion/fail'),
    f'execute if score #rdIlStep rd matches 1..2 as {ILL} at @s run '+call('illusion/sync'),
])
write('start', [
    '# rdTime 1, as the boss where the previous move left it. Leftovers go silently.',
    f'execute as {ILL} at @s run '+call('illusion/vanish'),
    f'kill {VIS}',
    call('object/clear'),
    'scoreboard players set @s rdWalk 0',
    'scoreboard players set @s rdBlink 0',
    'kill @e[tag=rlk_rd_blink_dest]',
    'scoreboard players set #rdIlStep rd 1',
    'scoreboard players set #rdIlClock rd 0',
    'scoreboard players set #rdIlTurn rd 0',
    'scoreboard players set #rdIlSlash rd 0',
    'scoreboard players set #rdIlShots rd 0',
    '# She scatters where she stands; the hidden body crosses to the centre this frame.',
    call('movement/depart'),
    sound('entity.illusioner.mirror_move', .9, .75),
    f'execute at {CENTER} run tp @s ~ ~ ~ facing entity {BODY} feet',
    'execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0',
    call('line/pohyeong'),
])
intro = [
    '# As the boss (hidden at the centre). Reform there, split in four, run out.',
    f'execute if score @s rdTime matches {ARRIVE_T} at @s run '+call('movement/arrive'),
    f'execute if score @s rdTime matches {SPAWN_T} run '+call('illusion/spawn_all'),
    f'execute if score @s rdTime matches {RUN_FROM} run '+call('illusion/lean'),
    f'execute if score @s rdTime matches {RUN_FROM}..{HOLD_T-1} as {ILL} at @s run tp @s ^ ^ ^{RUN_STEP}',
]
for i, t in enumerate(range(RUN_FROM, HOLD_T, 2)):
    intro.append(f'execute if score @s rdTime matches {t} run '+call('illusion/frame')+f' {{model:"illusion_run_{i%4}"}}')
intro.append(f'execute if score @s rdTime matches {HOLD_T} run '+call('illusion/hold'))
write('intro', intro)
write('spawn_all', [
    '# Base direction: diagonal to the player\'s bearing, so nobody runs straight at them.',
    f'execute if entity {BODY} at {CENTER} facing entity {BODY} feet rotated ~45 0 run '+call('illusion/spawn_ring'),
    f'execute unless entity {BODY} at {CENTER} rotated 45 0 run '+call('illusion/spawn_ring'),
])
write('spawn_ring', [
    '# As the boss at the arena centre; each illusion faces its own running direction.',
    call('illusion/spawn')+' {id:1}',
    'execute rotated ~90 0 run '+call('illusion/spawn')+' {id:2}',
    'execute rotated ~180 0 run '+call('illusion/spawn')+' {id:3}',
    'execute rotated ~270 0 run '+call('illusion/spawn')+' {id:4}',
    '# One random illusion is the real body.',
    f'execute as @e[tag=rlk_rd_illusion,sort=random,limit=1] run scoreboard players set @s rdReal 1',
    sound('entity.illusioner.mirror_move', 1, 1.15),
    sound('entity.breeze.charge', .7, 1.4),
])
write('spawn', [
    '$function rlk:boss/raiden/object/create {kind:2,model:"illusion_ready",hp:1,id:$(id),y:0}',
    '$execute as @e[tag=rlk_rd_object,scores={rdObjKind=2,rdObjId=$(id)},tag=!rlk_rd_illusion,limit=1] run '+call('illusion/adopt'),
])
write('adopt', [
    '# As the new hitbox husk; execution rotation = its running direction.',
    'tag @s add rlk_rd_illusion',
    'tp @s ~ ~ ~ ~ 0',
    'scoreboard players set @s rdTurns 0',
    '# Untouchable while the four overlap and run; hittable once they hold their spots.',
    'scoreboard players set @s rdHitCD 100',
    'scoreboard players operation #rdIlId rd = @s rdObjId',
    'execute as @e[type=minecraft:item_display,tag=rlk_rd_objvisual] if score @s rdObjId = #rdIlId rd run '+call('illusion/adopt_visual'),
])
write('adopt_visual', [
    '# object/create\'s display becomes the posed illusion: feet on the floor, boss-sized.',
    'tag @s add rlk_rd_ilvis',
    'tp @s ~ ~ ~ ~ 0',
    'data merge entity @s {teleport_duration:1,interpolation_duration:0,view_range:3f,transformation:'+transform(0)+'}',
])
write('frame', [f'$execute as {VIS} run '+model_set('$(model)')])
write('lean', [f'execute as {VIS} run data merge entity @s {{interpolation_duration:3,start_interpolation:0,transformation:{transform(14)}}}'])
write('hold', [
    'title @a[tag=player] times 3 36 10',
    'title @a[tag=player] subtitle {text:"X자로 베는 분신이 진짜 · 찾아서 공격하세요",color:"light_purple"}',
    'execute as @a[tag=player] run function rlk:view/ttl_blank',
    'scoreboard players set @a[tag=player] ttlT 49',
    'scoreboard players set #rdCap rd 1',
    'scoreboard players set #rdCapPat rd 1',
    '# Positions taken: everyone turns to the centre, settles into the guard, can be hit.',
    f'execute as {ILL} at @s facing entity {CENTER} feet run tp @s ~ ~ ~ ~ 0',
    f'scoreboard players set {ILL} rdHitCD 0',
    f'execute as {VIS} run data merge entity @s {{interpolation_duration:3,start_interpolation:0,transformation:{transform(0)}}}',
    call('illusion/frame')+' {model:"illusion_ready"}',
    sound('entity.breeze.land', .8, 1.3, '~ ~ ~'),
    'scoreboard players set #rdIlStep rd 2',
    '# Turns start next tick (clock 1).',
    'scoreboard players set #rdIlClock rd -1',
])
write('sync', [
    '# As an illusion husk at itself: its display follows (teleport_duration smooths it).',
    'scoreboard players operation #rdIlId rd = @s rdObjId',
    f'execute as {VIS} if score @s rdObjId = #rdIlId rd run tp @s ~ ~ ~ ~ ~',
])
write('pose', [
    '# As an illusion husk: swap its display to the pose model.',
    'scoreboard players operation #rdIlId rd = @s rdObjId',
    f'$execute as {VIS} if score @s rdObjId = #rdIlId rd run '+model_set('$(model)'),
])
write('volleys', [
    f'# As the boss. {VOLLEYS} volleys: everyone winds up together and cuts toward the centre;',
    f'# fakes once, the real one an X (second diagonal stroke {XGAP} ticks later).',
    'scoreboard players add #rdIlClock rd 1',
    '# hold() hands over with clock -1: nothing happens on the tick the spots are taken.',
    'execute if score #rdIlClock rd matches ..0 run return 0',
    f'execute if score #rdIlClock rd matches 1 as {ILL} at @s run '+call('illusion/wind')+f' {{tell:{TELL},life:{TELL+10}}}',
    f'execute if score #rdIlClock rd matches {STRIKE} as {ILL} at @s run '+call('illusion/strike'),
    f'execute if score #rdIlClock rd matches {STRIKE+XGAP} as @e[tag=rlk_rd_illusion,scores={{rdReal=1}},limit=1] at @s run '+call('illusion/strike_x2'),
    f'execute if score #rdIlClock rd matches {VOLLEY_END}.. run '+call('illusion/volley_end'),
])
write('volley_end', [
    f'execute as {ILL} run '+call('illusion/pose')+' {model:"illusion_ready"}',
    'scoreboard players add #rdIlTurn rd 1',
    'scoreboard players set #rdIlClock rd 0',
    f'# {VOLLEYS} volleys without finding her: over.',
    f'execute if score #rdIlTurn rd matches {VOLLEYS}.. run '+call('illusion/fail'),
])
write('wind', [
    '# As an illusion at its feet: face the centre, wind up, lay the slash line (all alike).',
    f'execute facing entity {CENTER} feet run tp @s ~ ~ ~ ~ 0',
    f'$function rlk:boss/raiden/hazard/create {{shape:{SHAPE},tell:$(tell),damage:{DAMAGE},life:$(life)}}',
    'tag @e[type=minecraft:marker,tag=rlk_rd_hazard,tag=!rlk_rd_ilhaz,distance=..0.1] add rlk_rd_ilhaz',
    '$function rlk:boss/raiden/object_vfx/illusion_cue {life:$(tell)}',
    call('illusion/pose')+' {model:"illusion_wind"}',
    sound('item.trident.return', .45, 1.25),
])
write('strike', [
    '# Same tick as its hazard strike. A fake cuts once (flat arc + wave); the real one',
    '# opens its X with a diagonal stroke and lays the second, crossing line right away.',
    call('illusion/pose')+' {model:"illusion_slash"}',
    'execute if score @s rdReal matches 0 run '+call('object_vfx/slash'),
    'execute if score @s rdReal matches 1 run '+call('object_vfx/slash_xa'),
    f'execute if score @s rdReal matches 1 run tp @s ~ ~ ~ ~{X_YAW} 0',
    f'execute if score @s rdReal matches 1 run function rlk:boss/raiden/hazard/create {{shape:{SHAPE},tell:{XGAP},damage:{DAMAGE},life:{XGAP+10}}}',
    'execute if score @s rdReal matches 1 run tag @e[type=minecraft:marker,tag=rlk_rd_hazard,tag=!rlk_rd_ilhaz,distance=..0.1] add rlk_rd_ilhaz',
    'execute if score @s rdReal matches 1 run tp @s ~ ~ ~ ~ 0',
    'scoreboard players add #rdIlSlash rd 1',
    sound('entity.player.attack.sweep', .6, .8),
])
write('strike_x2', [
    '# As the REAL illusion: the second diagonal stroke of its X.',
    call('illusion/pose')+' {model:"illusion_wind"}',
    call('object_vfx/slash_xb'),
    'scoreboard players add #rdIlSlash rd 1',
    sound('entity.player.attack.sweep', .9, 1.15),
])
write('fail', [
    '# As the boss. Not found in time: no punishment strike, she simply reforms.',
    'scoreboard players set #rdIlStep rd 3',
    'scoreboard players set #rdIlClock rd 0',
    'tag @e[tag=rlk_rd_ilact] remove rlk_rd_ilact',
    'execute as @e[tag=rlk_rd_illusion,scores={rdReal=0}] at @s run '+call('illusion/dissolve'),
    '# The body reforms on the real illusion\'s spot (or stays at the centre without one).',
    f'execute as @e[tag=rlk_rd_illusion,scores={{rdReal=1}},limit=1] at @s run tp {BOSS} ~ ~ ~',
    'execute as @e[tag=rlk_rd_illusion,scores={rdReal=1}] at @s run '+call('illusion/vanish'),
    'execute at @s run '+call('illusion/reform'),
    sound('entity.illusioner.mirror_move', .8, .7, '~ ~ ~'),
])
write('fail_tick', [
    'scoreboard players add #rdIlClock rd 1',
    f'execute if score #rdIlClock rd matches {REFORM}.. run '+call('illusion/fail_end'),
])
write('fail_end', [
    '# The arrive art is fully formed now: the rig reappears this same tick. Not broken:',
    '# 몽상의 일심 (pattern 7) comes next, as in the original.',
    call('illusion/reset'),
    call('finish'),
    'scoreboard players set @s rdNext 7',
])
write('won', [
    '# As the shattered REAL illusion at its spot (object/break, before it is removed).',
    'scoreboard players set #rdIlStep rd 4',
    'scoreboard players set #rdIlClock rd 0',
    'tag @e[tag=rlk_rd_ilact] remove rlk_rd_ilact',
    '# Slashes that have not landed yet are cancelled together with their displays.',
    'execute as @e[tag=rlk_rd_ilhaz] if score @s rdHAge < @s rdWind run '+call('hazard/expire'),
    'execute as @e[tag=rlk_rd_illusion,scores={rdReal=0}] at @s run '+call('illusion/dissolve'),
    f'tp {BOSS} ~ ~ ~',
    f'execute as {BOSS} at @s run '+call('illusion/reform'),
    call('line/ganpa'),
    sound('block.glass.break', .8, .9),
    sound('entity.illusioner.mirror_move', 1, 1.3),
])
write('won_tick', [
    'scoreboard players add #rdIlClock rd 1',
    f'execute if score #rdIlClock rd matches {REFORM+1}.. run '+call('illusion/stagger'),
])
write('stagger', [
    "# As the boss, reformed on the real illusion's spot: a 10 s stun (rdPat 98).",
    call('illusion/reset'),
    call('object/clear'),
    'scoreboard players set @s rdPat 98',
    'scoreboard players set @s rdTime 0',
    'scoreboard players set @s rdAnim 23',
    'scoreboard players remove @s rdRage 120',
    'execute if score @s rdRage matches ..0 run scoreboard players set @s rdRage 0',
    sound('block.beacon.deactivate', .8, .65, '~ ~ ~'),
])
write('stun_tick', [
    '# boss/raiden/tick, as the stunned boss (rdPat 98): collapse, kneel, rise, move on.',
    'execute if score @s rdTime matches 46 run scoreboard players set @s rdAnim 22',
    f'execute if score @s rdTime matches {STUN-28} run scoreboard players set @s rdAnim 24',
    f'execute if score @s rdTime matches {STUN}.. run '+call('finish'),
])
write('reform', [
    '# As the boss at its (new) feet: face the player and play the arrival art. The rig',
    '# stays hidden (rdPat 5) until the art has formed, then finish/stagger shows it.',
    f'tp @s ~ ~ ~ facing entity {BODY} feet',
    'execute rotated as @s run tp @s ~ ~ ~ ~ 0',
    call('movement/arrive'),
])
write('lost', [
    '# rdPat 5 without illusion state (e.g. state reset mid-pattern): reform and move on.',
    call('illusion/reset'),
    'execute at @s run '+call('illusion/reform'),
    call('finish'),
])
write('dissolve', [
    '# As an illusion husk at its feet: it scatters like the boss does (boss = art owner).',
    f'execute rotated as @s as {BOSS} run rotate @s ~ 0',
    f'execute as {BOSS} run '+call('movement/depart'),
    call('illusion/vanish'),
])
write('vanish', [
    '# As an illusion husk at its feet: remove it and its display without a death puff.',
    'scoreboard players operation #rdIlId rd = @s rdObjId',
    f'execute as {VIS} if score @s rdObjId = #rdIlId rd run kill @s',
    'tag @s remove rlk_rd_illusion',
    'tp @s ~ ~-100 ~',
    'kill @s',
])
write('on_break', [
    '# object/break, as the shattered illusion at itself (display already removed).',
    'execute unless score #rdIlStep rd matches 1..2 run return 0',
    'execute if score @s rdReal matches 1 run return run '+call('illusion/won'),
    '# A shattered fake loses its pending slash and its turn.',
    'tag @s remove rlk_rd_illusion',
    'execute as @e[tag=rlk_rd_ilhaz,distance=..0.2] if score @s rdHAge < @s rdWind run '+call('hazard/expire'),
    sound('block.glass.break', .7, 1.25),
])
write('cleanup', [
    '# Idempotent; any executor. pause/transform/exhausted/cleanup/reload/death call it.',
    '# A cut-short challenge still shows the scatter/reform art when the boss is alive.',
    'execute if score #rdIlStep rd matches 1..2 as @e[tag=rlk_raiden,scores={rdPat=5,rdDeath=0},limit=1] at @s run '+call('movement/arrive'),
    f'execute if entity @e[tag=rlk_raiden,scores={{rdDeath=0}},limit=1] as {ILL} at @s run '+call('illusion/dissolve'),
    call('illusion/reset'),
])
write('reset', [
    f'execute as {ILL} at @s run '+call('illusion/vanish'),
    f'kill {VIS}',
    'execute as @e[tag=rlk_rd_ilhaz] if score @s rdHAge < @s rdWind run '+call('hazard/expire'),
    'tag @e[tag=rlk_rd_ilhaz] remove rlk_rd_ilhaz',
    'tag @e[tag=rlk_rd_ilact] remove rlk_rd_ilact',
    'scoreboard players set #rdIlStep rd 0',
    'scoreboard players set #rdIlClock rd 0',
    'scoreboard players set #rdIlTurn rd 0',
    'scoreboard players set #rdIlSlash rd 0',
    'scoreboard players set #rdIlShots rd 0',
])

for stale in OUT.glob('*.mcfunction'):
    if stale not in written:
        stale.unlink()
print(f'Generated the illusion challenge: {len(written)} functions, {len(POSES)} skin pose models '
      f'(run-out {RUN_TICKS} ticks to {RUN_TICKS*RUN_STEP:g} blocks, {VOLLEYS} volleys of {VOLLEY_END} ticks, stun {STUN} ticks, hazard shape {SHAPE}).')
