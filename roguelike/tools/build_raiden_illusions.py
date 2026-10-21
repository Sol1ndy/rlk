r"""찰나의 포영 (pattern 5, plan rd/plan.md B.2 row 5, footage A-07; sword only): four clones round the arena centre, one
of them real. rd-sync rework (user requests): the clones stand on a ring about the arena centre, they are animated
copies of Raiden built from the rig's part models (build_raiden_clones.mjs: joined arms, the katana in hand), the three
fakes each cut one diagonal and throw one crescent wave, the real one cuts a quick X and throws two crossing crescents
(the second 4 t after the first); the waves are clean crescent blades of light (the kit's slab `wave` look).

Run from anywhere:  python3 tools/build_raiden_illusions.py [--resourcepack <RP>]   (the pack is not written)

Writes data/rlk/function/boss/raiden/illusion/*.mcfunction. The encounter dispatches to illusion/tick (patterns/5),
calls illusion/on_break from object/break and illusion/cleanup from pause / transform / exhausted / cleanup / reload /
death. Each clone is an object husk (kind 2, 1 hit reveals; plan A8) carrying 14 clone part displays.

Timeline (boss rdTime; rdPat 5 keeps her immune the whole time, the rig is hidden while #rdIlStep is 1..2):
  0      she scatters where she stands (the release blink art) 「찰나의... 포영!」
  4      hidden (#rdIlStep 1)
  8      four sky pillars on a ring of radius 13 about the arena centre, 90 deg apart, 45 deg off the player's bearing
         from the centre (so the player is never in line with a clone)
  12     the clones appear there facing the player, hittable; one at random is real
  V-14   every clone turns to the player (aim lock) and raises its sword: the glint (cue)        V = 40 / 96 / 152
  V-4    wound up high on her right
  V      the diagonal cut (her upper right -> lower left) crosses her facing: its crescent wave (\ as the player
         sees it) leaves the blade; the real one, from V+1, winds up on her left and cuts back at V+4 (/): the X.
         Waves: slab w 2.6 (5.2 b wide), depth 1, 0.8 b/t from 0.5 b; one hit max per volley for the whole set
  V+12   back to rest
  174    not found: the fakes scatter, the real clone glows
  176    she reforms on the real clone's spot                                                     (#rdIlStep 3)
  182    end; 몽상의 일심 (7) follows (rdNext 7)
  hit    the real clone (any time after 12): pending waves vanish, the fakes scatter, she reforms there, 「간파했군.」,
         stun 100 t (rdPat 98, sg/stun_begin with rdSgStun 1), then 7. A fake shatters alone.
No body is ever moved below the floor: a removed clone is killed where it stands.
"""
from pathlib import Path
import argparse
import sys

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from raiden_kit import fx, hz, hz_group  # noqa: E402

ROOT = TOOLS.parent
OUT = ROOT / 'data/rlk/function/boss/raiden/illusion'
parser = argparse.ArgumentParser()
parser.add_argument('--resourcepack', help='accepted for build_raiden_all.py; unused')
parser.parse_args()

HIDE_T, PILLAR_T, APPEAR_T = 4, 8, 12
VOLLEYS = (40, 96, 152)
RAISE, WIND, XGAP = 14, 4, 4                    # the cue V-14; wound up V-4; the real one's second cut V+4
RING = 13                                        # clone ring radius about the arena centre (walkable r 23)
FAIL_T, REFORM_T, END_T = 174, 176, 182
DAMAGE = 10
WAVE = dict(w=2.6, depth=1, v=0.8, height=5, d0=0.5, reach=24)
LIFT = 1.375

written = set()


def write(name, lines):
    p = OUT / (name + '.mcfunction')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    written.add(p)


def call(name):
    return 'function rlk:boss/raiden/' + name


def sound(event, vol=1, pitch=1, at='~ ~1 ~'):
    return f'playsound minecraft:{event} hostile @a[tag=player] {at} {vol} {pitch} 0.2'


def pose(sel, p, d, look='dark'):
    """Every clone part matching sel eases to pose p over d ticks (build_raiden_clones.mjs)."""
    return call('clone/pose') + f' {{sel:"{sel}",p:"{p}",d:{d},look:"{look}"}}'


ILL = '@e[tag=rlk_rd_illusion]'
VIS = '@e[type=minecraft:item_display,tag=rlk_rd_ilvis]'
CENTER = '@e[tag=rlk_raiden_arena,limit=1]'
BOSS = '@e[tag=rlk_raiden,limit=1]'
BODY = '@e[tag=rlk_body,limit=1]'
TMP = '"rlk_rd_tmp","rlk_rd_sg","rlk_raiden_aux","rlk_room"'
ALL, FAKE, REAL = 'tag=rlk_rd_ilvis', 'tag=rlk_rd_clfake', 'tag=rlk_rd_clreal'
WAVE_HZ = lambda tell, tilt: hz('slab', tell, DAMAGE, group=True, wave=tilt, **WAVE)
ON = 'if score #rdIlStep rd matches 1 '

tick = ['# patterns/5: as the boss at its feet every tick of rdPat 5 (rdTime 0 = the choose tick).',
        '# #rdIlStep: 1 clones out (hidden), 2 dissolving (hidden), 3 reformed, 4 found.',
        'execute if score @s rdTime matches 0 run ' + call('illusion/start'),
        f'execute if score @s rdTime matches {HIDE_T} run scoreboard players set #rdIlStep rd 1',
        f'execute if score @s rdTime matches {PILLAR_T} {ON}run ' + call('illusion/pillars'),
        f'execute if score @s rdTime matches {APPEAR_T} {ON}run ' + call('illusion/appear')]
for v in VOLLEYS:
    tick += [f'execute if score @s rdTime matches {v - RAISE} {ON}run ' + call('illusion/raise'),
             f'execute if score @s rdTime matches {v - WIND} {ON}run ' + pose(ALL, 'high_r', 3),
             f'execute if score @s rdTime matches {v - 1} {ON}run ' + call('illusion/volley'),
             f'execute if score @s rdTime matches {v} {ON}run ' + pose(ALL, 'low_l', 2),
             f'execute if score @s rdTime matches {v} {ON}as {ILL} at @s run ' + sound('entity.player.attack.sweep', .8, .8),
             f'execute if score @s rdTime matches {v} {ON}as {ILL} at @s run ' + call('fx/snd/wave_slab'),
             f'execute if score @s rdTime matches {v + 1} {ON}run ' + pose(REAL, 'high_l', 2),
             f'execute if score @s rdTime matches {v + XGAP - 1} {ON}run ' + pose(REAL, 'cross_x', 1),
             f'execute if score @s rdTime matches {v + XGAP} {ON}run ' + pose(REAL, 'low_r', 2),
             f'execute if score @s rdTime matches {v + XGAP} {ON}as @e[tag=rlk_rd_illusion,scores={{rdReal=1}}] at @s run ' +
             sound('entity.player.attack.sweep', .9, 1.1),
             f'execute if score @s rdTime matches {v + 12} {ON}run ' + pose(ALL, 'rest', 6)]
tick += [f'execute if score @s rdTime matches {FAIL_T} {ON}run ' + call('illusion/fail'),
         f'execute if score @s rdTime matches {REFORM_T} if score #rdIlStep rd matches 2 run ' + call('illusion/reform'),
         '# Lost state (e.g. a reload mid-pattern): end visibly instead of hiding her forever.',
         f'execute if score @s rdTime matches {HIDE_T + 1}.. unless score #rdIlStep rd matches 1..3 run return run ' + call('illusion/lost'),
         f'execute if score @s rdTime matches {END_T}.. run ' + call('illusion/end')]
write('tick', tick)
write('start', [
    '# rdTime 0, as the boss where the previous move left her. Leftovers go silently. She scatters where she stands',
    '# (the release blink art) and stays hidden.',
    call('illusion/reset'),
    call('object/clear'),
    'scoreboard players set @s rdBlink 0',
    'kill @e[tag=rlk_rd_blink_dest]',
    call('rig/state/hidden'),
    'execute at @s run ' + call('movement/depart'),
    call('line/pohyeong'),
])
write('pillars', [
    f'# As the boss: four spots on a ring of radius {RING} about the arena centre, 90 deg apart, 45 deg off the bearing of',
    '# the player from the centre; sky pillars there.',
    'kill @e[tag=rlk_rd_ilspot]',
    f'execute at {CENTER} facing entity {BODY} feet rotated ~45 0 run ' + call('illusion/spots'),
    'execute as @e[tag=rlk_rd_ilspot] at @s run ' + call('fx/bolt'),
])
spots = []
for k in range(4):
    spots += [f'execute rotated ~{90 * k} 0 positioned ^ ^ ^{RING} run summon minecraft:marker ~ ~ ~ '
              '{Tags:["rlk_rd_ilspot","rlk_rd_ilnew",' + TMP + ']}',
              f'scoreboard players set @e[tag=rlk_rd_ilnew] rdObjId {k + 1}',
              'tag @e[tag=rlk_rd_ilnew] remove rlk_rd_ilnew']
write('spots', spots)
write('appear', [
    '# As the boss: the four clones (object kind 2, 1 hit) on the spots, facing the player; one is real (its parts are',
    '# tagged rlk_rd_clreal, the others rlk_rd_clfake: the real one alone cuts the X).'] +
    [f'execute as @e[tag=rlk_rd_ilspot,scores={{rdObjId={k}}},limit=1] at @s run ' + call('object/create') +
     f' {{kind:2,model:"prop/clone_ready_dark",hp:1,id:{k},y:{LIFT}}}' for k in range(1, 5)] + [
    'execute as @e[tag=rlk_rd_object,scores={rdObjKind=2},tag=!rlk_rd_illusion] at @s run ' + call('illusion/adopt'),
    'execute as @e[tag=rlk_rd_illusion,sort=random,limit=1] run scoreboard players set @s rdReal 1',
    'execute as @e[tag=rlk_rd_illusion,scores={rdReal=1},limit=1] run scoreboard players operation #rdIlId rd = @s rdObjId',
    'execute as @e[type=minecraft:item_display,tag=rlk_rd_clp] if score @s rdObjId = #rdIlId rd run tag @s add rlk_rd_clreal',
    'tag @e[type=minecraft:item_display,tag=rlk_rd_clp,tag=!rlk_rd_clreal] add rlk_rd_clfake',
    sound('entity.illusioner.mirror_move', 1, 1.15),
])
write('adopt', [
    '# As a new clone husk at its feet: face the player, hittable at once; its object display gives way to the clone',
    '# figure (14 parts, build_raiden_clones.mjs).',
    'tag @s add rlk_rd_illusion',
    f'tp @s ~ ~ ~ facing entity {BODY} feet',
    'execute rotated as @s run tp @s ~ ~ ~ ~ 0',
    'scoreboard players set @s rdHitCD 0',
    'scoreboard players operation #rdIlId rd = @s rdObjId',
    'execute as @e[type=minecraft:item_display,tag=rlk_rd_objvisual,tag=!rlk_rd_clp] if score @s rdObjId = #rdIlId rd run kill @s',
    'execute store result storage rlk:rd il.id int 1 run scoreboard players get @s rdObjId',
    'execute rotated as @s run ' + call('clone/summon') + ' with storage rlk:rd il',
])
write('raise', [f'execute as {ILL} at @s run ' + call('illusion/raise_one'),
                pose(ALL, 'ready', 6),
                sound('item.trident.return', .6, 1.25, '~ ~ ~')])
write('raise_one', [
    '# As a clone husk at its feet: aim lock on the player (the figure turns with it), the glint on the raised blade.',
    f'tp @s ~ ~ ~ facing entity {BODY} feet',
    'execute rotated as @s run tp @s ~ ~ ~ ~ 0',
    'scoreboard players operation #rdIlId rd = @s rdObjId',
    f'execute rotated as @s as {VIS} if score @s rdObjId = #rdIlId rd run tp @s ~ ~ ~ ~ 0',
    'execute rotated as @s positioned ^ ^3.2 ^0.3 run ' + fx('star'),
])
write('volley', ['# One tick before the cut: the crescent waves (they launch next tick, as the blade crosses her facing);',
                 '# one hit max for the whole volley.',
                 hz_group(),
                 f'execute as {ILL} at @s rotated as @s run ' + call('illusion/fire'),
                 pose(ALL, 'cross_d', 1)])
write('fire', [
    '# As a clone at its feet, its yaw: every clone cuts the diagonal (\\ wave); the real one also cuts back 4 t later',
    '# (/ wave): the X.',
    WAVE_HZ(1, '\\'),
    'execute if score @s rdReal matches 1 run ' + WAVE_HZ(1 + XGAP, '/'),
    'tag @e[tag=rlk_rd_hazard,tag=!rlk_rd_ilhaz,distance=..0.1] add rlk_rd_ilhaz',
])
write('fail', [
    '# As the boss: not found. The fakes scatter, the real clone glows; she reforms there 2 t later.',
    'scoreboard players set #rdIlStep rd 2',
    'execute as @e[tag=rlk_rd_illusion,scores={rdReal=0}] at @s run ' + call('illusion/dissolve'),
    pose(REAL, 'rest', 4, 'glow'),
])
write('reform', [
    '# As the boss: on the real clone\'s spot (or where she is without one), facing the player; the rig shows again.',
    f'execute as @e[tag=rlk_rd_illusion,scores={{rdReal=1}},limit=1] at @s run tp {BOSS} ~ ~ ~',
    f'execute at @s run tp @s ~ ~ ~ facing entity {BODY} feet',
    'execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0',
    f'execute as {ILL} at @s run ' + call('illusion/vanish'),
    call('rig/play/blink_in'),
    'execute at @s run ' + call('movement/arrive'),
    'scoreboard players set #rdIlStep rd 3',
])
write('end', [
    '# Not broken: 몽상의 일심 (7) comes next.',
    call('illusion/reset'),
    call('finish'),
    'scoreboard players set @s rdNext 7',
])
write('won', [
    '# As the shattered REAL clone at its spot (object/break, before it is removed).',
    'scoreboard players set #rdIlStep rd 4',
    '# Waves that have not launched yet go with their displays.',
    'execute as @e[tag=rlk_rd_ilhaz] if score @s rdHAge < @s rdWind run ' + call('hazard/expire'),
    'execute as @e[tag=rlk_rd_illusion,scores={rdReal=0}] at @s run ' + call('illusion/dissolve'),
    f'tp {BOSS} ~ ~ ~',
    f'execute as {BOSS} at @s run ' + call('illusion/found'),
])
write('found', [
    '# As the boss on the real clone\'s spot: she reforms, 「간파했군.」, stun 100 t (then 7).',
    f'tp @s ~ ~ ~ facing entity {BODY} feet',
    'execute rotated as @s run tp @s ~ ~ ~ ~ 0',
    call('rig/play/blink_in'),
    call('movement/arrive'),
    call('line/ganpa'),
    sound('block.glass.break', .8, .9),
    'scoreboard players remove @s rdRage 120',
    'execute if score @s rdRage matches ..-1 run scoreboard players set @s rdRage 0',
    call('illusion/reset'),
    'scoreboard players set @s rdSgStun 1',
    call('sg/stun_begin'),
])
write('lost', [
    '# rdPat 5 without clone state: reform where she is and move on.',
    call('illusion/reset'),
    call('rig/play/blink_in'),
    'execute at @s run ' + call('movement/arrive'),
    call('finish'),
])
write('dissolve', [
    '# As a clone husk at its feet: it scatters (the blink art) and goes.',
    call('movement/depart'),
    call('illusion/vanish'),
])
write('vanish', [
    '# As a clone husk: remove it and its figure where they stand (never moved below the floor).',
    'scoreboard players operation #rdIlId rd = @s rdObjId',
    f'execute as {VIS} if score @s rdObjId = #rdIlId rd run kill @s',
    'tag @s remove rlk_rd_illusion',
    'kill @s',
])
write('on_break', [
    '# object/break, as the shattered clone at itself (its figure already removed).',
    'execute unless score #rdIlStep rd matches 1 run return 0',
    'execute if score @s rdReal matches 1 run return run ' + call('illusion/won'),
    '# A shattered fake loses its pending wave.',
    'tag @s remove rlk_rd_illusion',
    'execute as @e[tag=rlk_rd_ilhaz,distance=..0.2] if score @s rdHAge < @s rdWind run ' + call('hazard/expire'),
    sound('block.glass.break', .7, 1.25),
])
write('cleanup', [
    '# Idempotent; any executor. pause / transform / exhausted / cleanup / reload / death call it.',
    '# A cut-short challenge still shows the reform when the boss lives, and the clones scatter.',
    'execute if score #rdIlStep rd matches 1..2 as @e[tag=rlk_raiden,scores={rdPat=5,rdDeath=0},limit=1] at @s run ' + call('movement/arrive'),
    f'execute as {ILL} at @s run ' + call('movement/depart'),
    call('illusion/reset'),
])
write('reset', [
    f'execute as {ILL} at @s run ' + call('illusion/vanish'),
    f'kill {VIS}',
    'kill @e[tag=rlk_rd_ilspot]',
    'execute as @e[tag=rlk_rd_ilhaz] if score @s rdHAge < @s rdWind run ' + call('hazard/expire'),
    'tag @e[tag=rlk_rd_ilhaz] remove rlk_rd_ilhaz',
    'scoreboard players set #rdIlStep rd 0',
])

for stale in OUT.glob('*.mcfunction'):
    if stale not in written:
        stale.unlink()
print(f'Generated 찰나의 포영: {len(written)} functions (volleys {VOLLEYS}, ring r {RING}, end {END_T}).')
