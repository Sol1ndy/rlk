"""찰나의 포영 (pattern 5, plan rd/plan.md B.2 row 5, footage A-07; sword only): four clones, one of them real.

Run from anywhere:  python3 tools/build_raiden_illusions.py [--resourcepack <RP>]   (the pack is not written any more)

Writes data/rlk/function/boss/raiden/illusion/*.mcfunction. The encounter dispatches to illusion/tick (patterns/5),
calls illusion/on_break from object/break and illusion/cleanup from pause / transform / exhausted / cleanup / reload /
death. The clones are the rig props clone_ready / clone_slash (dark; _glow for the revealed one) at boss scale, shown
by the object displays (kind 2, 1 hit reveals; plan A8).

Timeline (boss rdTime; rdPat 5 keeps her immune the whole time, the rig is hidden while #rdIlStep is 1..2):
  0      blink out where she stands (clip blink_out, fx/blink_out) 「찰나의... 포영!」
  4      hidden (#rdIlStep 1)
  8      four sky pillars 13 b from the player, 90 deg apart (diagonal to her bearing), pulled in to radius 20
  12     the clones appear there facing the player, hittable; one at random is real
  V-14   every clone raises its sword and turns to the player (aim lock; glint card on the blade)   V = 40 / 96 / 152
  V      the volley: a fake cuts one slab 12 b wide (w 6, depth 1, chest height, 0.8 b/t); the real one cuts an X
         (two slabs crossing at +-15 deg). One hit max per volley for the whole set (a group).
  174    not found: the fakes dissolve, the real clone glows
  176    she reappears on the real clone's spot (blink_in)                                       (#rdIlStep 3)
  182    end; 몽상의 일심 (7) follows (rdNext 7)
  hit    the real clone (any time after 12): pending slabs vanish, the fakes dissolve, she reappears there,
         「간파했군.」, stun 100 t (rdPat 98, sg/stun_begin with rdSgStun 1), then 7. A fake shatters alone.
No body is ever moved below the floor: a removed clone husk is killed where it stands.
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
RAISE = 14
DIST, CLAMP = 13, 20
FAIL_T, REFORM_T, END_T = 174, 176, 182
DAMAGE, SLAB = 10, dict(w=6, depth=1, v=0.8, height=2.5, d0=0.5, reach=24)
X_YAW = 15
LIFT = 1.375                        # clone props: pivot 1.375 b above the feet

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


ILL = '@e[tag=rlk_rd_illusion]'
VIS = '@e[type=minecraft:item_display,tag=rlk_rd_ilvis]'
CENTER = '@e[tag=rlk_raiden_arena,limit=1]'
BOSS = '@e[tag=rlk_raiden,limit=1]'
BODY = '@e[tag=rlk_body,limit=1]'
TMP = '"rlk_rd_tmp","rlk_rd_sg","rlk_raiden_aux","rlk_room"'
SLAB_HZ = lambda yaw=0: hz('slab', 1, DAMAGE, group=True, yawoff=yaw, **SLAB)

tick = ['# patterns/5: as the boss at its feet every tick of rdPat 5 (rdTime 0 = the choose tick).',
        '# #rdIlStep: 1 clones out (hidden), 2 dissolving (hidden), 3 reformed, 4 found.',
        'execute if score @s rdTime matches 0 run ' + call('illusion/start'),
        f'execute if score @s rdTime matches {HIDE_T} run scoreboard players set #rdIlStep rd 1',
        f'execute if score @s rdTime matches {PILLAR_T} if score #rdIlStep rd matches 1 run ' + call('illusion/pillars'),
        f'execute if score @s rdTime matches {APPEAR_T} if score #rdIlStep rd matches 1 run ' + call('illusion/appear')]
for v in VOLLEYS:
    tick += [f'execute if score @s rdTime matches {v - RAISE} if score #rdIlStep rd matches 1 run ' + call('illusion/raise'),
             f'execute if score @s rdTime matches {v - 1} if score #rdIlStep rd matches 1 run ' + call('illusion/volley'),
             f'execute if score @s rdTime matches {v} if score #rdIlStep rd matches 1 run ' + call('illusion/slash')]
tick += [f'execute if score @s rdTime matches {FAIL_T} if score #rdIlStep rd matches 1 run ' + call('illusion/fail'),
         f'execute if score @s rdTime matches {REFORM_T} if score #rdIlStep rd matches 2 run ' + call('illusion/reform'),
         '# Lost state (e.g. a reload mid-pattern): end visibly instead of hiding her forever.',
         f'execute if score @s rdTime matches {HIDE_T + 1}.. unless score #rdIlStep rd matches 1..3 run return run ' + call('illusion/lost'),
         f'execute if score @s rdTime matches {END_T}.. run ' + call('illusion/end')]
write('tick', tick)
write('start', [
    '# rdTime 0, as the boss where the previous move left her. Leftovers go silently.',
    call('illusion/reset'),
    call('object/clear'),
    'scoreboard players set @s rdBlink 0',
    'kill @e[tag=rlk_rd_blink_dest]',
    call('rig/play/blink_out'),
    'execute at @s run ' + call('fx/blink_out'),
    call('line/pohyeong'),
])
write('pillars', [
    f'# As the boss: four spots {DIST} b from the player, 90 deg apart, diagonal to her bearing; sky pillars there.',
    'kill @e[tag=rlk_rd_ilspot]',
    f'execute at {BODY} facing entity @s feet rotated ~45 0 positioned ~ 201 ~ run ' + call('illusion/spots'),
    f'execute as @e[tag=rlk_rd_ilspot] at {CENTER} unless entity @s[distance=..{CLAMP}] facing entity @s feet rotated ~ 0 '
    f'positioned ^ ^ ^{CLAMP} run tp @s ~ ~ ~',
    'execute as @e[tag=rlk_rd_ilspot] at @s run ' + call('fx/bolt'),
])
spots = []
for k in range(4):
    spots += [f'execute rotated ~{90 * k} 0 positioned ^ ^ ^{DIST} run summon minecraft:marker ~ ~ ~ '
              '{Tags:["rlk_rd_ilspot","rlk_rd_ilnew",' + TMP + ']}',
              f'scoreboard players set @e[tag=rlk_rd_ilnew] rdObjId {k + 1}',
              'tag @e[tag=rlk_rd_ilnew] remove rlk_rd_ilnew']
write('spots', spots)
write('appear', [
    '# As the boss: the four clones (object kind 2, 1 hit) on the spots, facing the player; one is real.'] +
    [f'execute as @e[tag=rlk_rd_ilspot,scores={{rdObjId={k}}},limit=1] at @s run ' + call('object/create') +
     f' {{kind:2,model:"prop/clone_slash_dark",hp:1,id:{k},y:{LIFT}}}' for k in range(1, 5)] + [
    'execute as @e[tag=rlk_rd_object,scores={rdObjKind=2},tag=!rlk_rd_illusion] at @s run ' + call('illusion/adopt'),
    f'execute as @e[tag=rlk_rd_illusion,sort=random,limit=1] run scoreboard players set @s rdReal 1',
    sound('entity.illusioner.mirror_move', 1, 1.15),
])
write('adopt', [
    '# As a new clone husk at its feet: face the player, hittable at once; its display becomes the posed clone.',
    'tag @s add rlk_rd_illusion',
    f'tp @s ~ ~ ~ facing entity {BODY} feet',
    'execute rotated as @s run tp @s ~ ~ ~ ~ 0',
    'scoreboard players set @s rdHitCD 0',
    'scoreboard players operation #rdIlId rd = @s rdObjId',
    'execute rotated as @s as @e[type=minecraft:item_display,tag=rlk_rd_objvisual] if score @s rdObjId = #rdIlId rd '
    'positioned as @s run ' + call('illusion/adopt_visual'),
])
write('adopt_visual', ['tag @s add rlk_rd_ilvis', 'tp @s ~ ~ ~ ~ 0',
                       'data merge entity @s {teleport_duration:1,interpolation_duration:0,view_range:3f}'])
write('pose', [
    '# As a clone husk: its display takes the pose model and the husk\'s yaw.',
    'scoreboard players operation #rdIlId rd = @s rdObjId',
    f'$execute as {VIS} if score @s rdObjId = #rdIlId rd run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/$(model)"',
    f'execute rotated as @s as {VIS} if score @s rdObjId = #rdIlId rd positioned as @s run tp @s ~ ~ ~ ~ 0',
])
write('raise', [f'execute as {ILL} at @s run ' + call('illusion/raise_one'),
                sound('item.trident.return', .6, 1.25, '~ ~ ~')])
write('raise_one', [
    '# As a clone at its feet: aim lock on the player, sword raised, glint card on the blade.',
    f'tp @s ~ ~ ~ facing entity {BODY} feet',
    'execute rotated as @s run tp @s ~ ~ ~ ~ 0',
    call('illusion/pose') + ' {model:"prop/clone_ready_dark"}',
    'execute rotated as @s positioned ^ ^2.6 ^0.3 run ' + fx('star'),
])
write('volley', ['# One tick before the volley: the slabs (they launch next tick); one hit max for the set.',
                 hz_group(),
                 f'execute as {ILL} at @s rotated as @s run ' + call('illusion/fire')])
write('fire', [
    '# As a clone at its feet, its yaw: a fake cuts one slab, the real one an X.',
    'execute if score @s rdReal matches 0 run ' + SLAB_HZ(),
    'execute if score @s rdReal matches 1 run ' + SLAB_HZ(-X_YAW),
    'execute if score @s rdReal matches 1 run ' + SLAB_HZ(X_YAW),
    'tag @e[tag=rlk_rd_hazard,tag=!rlk_rd_ilhaz,distance=..0.1] add rlk_rd_ilhaz',
])
write('slash', [f'execute as {ILL} run ' + call('illusion/pose') + ' {model:"prop/clone_slash_dark"}',
                f'execute as {ILL} at @s run ' + sound('entity.player.attack.sweep', .8, .8),
                f'execute as {ILL} at @s run ' + call('fx/snd/wave_slab')])
write('fail', [
    '# As the boss: not found. The fakes dissolve, the real clone glows; she reappears there 2 t later.',
    'scoreboard players set #rdIlStep rd 2',
    'execute as @e[tag=rlk_rd_illusion,scores={rdReal=0}] at @s run ' + call('illusion/dissolve'),
    'execute as @e[tag=rlk_rd_illusion,scores={rdReal=1}] run ' + call('illusion/pose') + ' {model:"prop/clone_ready_glow"}',
])
write('reform', [
    '# As the boss: on the real clone\'s spot (or where she is without one), facing the player; the rig shows again.',
    f'execute as @e[tag=rlk_rd_illusion,scores={{rdReal=1}},limit=1] at @s run tp {BOSS} ~ ~ ~',
    f'execute at @s run tp @s ~ ~ ~ facing entity {BODY} feet',
    'execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0',
    f'execute as {ILL} at @s run ' + call('illusion/vanish'),
    call('rig/play/blink_in'),
    'execute at @s run ' + call('fx/blink_in'),
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
    '# Slashes that have not launched yet go with their displays.',
    'execute as @e[tag=rlk_rd_ilhaz] if score @s rdHAge < @s rdWind run ' + call('hazard/expire'),
    'execute as @e[tag=rlk_rd_illusion,scores={rdReal=0}] at @s run ' + call('illusion/dissolve'),
    f'tp {BOSS} ~ ~ ~',
    f'execute as {BOSS} at @s run ' + call('illusion/found'),
])
write('found', [
    '# As the boss on the real clone\'s spot: she reappears, 「간파했군.」, stun 100 t (then 7).',
    f'tp @s ~ ~ ~ facing entity {BODY} feet',
    'execute rotated as @s run tp @s ~ ~ ~ ~ 0',
    call('rig/play/blink_in'),
    call('fx/blink_in'),
    call('line/ganpa'),
    sound('block.glass.break', .8, .9),
    'scoreboard players remove @s rdRage 120',
    'execute if score @s rdRage matches ..-1 run scoreboard players set @s rdRage 0',
    call('illusion/reset'),
    'scoreboard players set @s rdSgStun 1',
    call('sg/stun_begin'),
])
write('lost', [
    '# rdPat 5 without clone state: reappear where she is and move on.',
    call('illusion/reset'),
    call('rig/play/blink_in'),
    'execute at @s run ' + call('fx/blink_in'),
    call('finish'),
])
write('dissolve', [
    '# As a clone husk at its feet: it scatters (the blink cue) and goes.',
    call('fx/blink_out'),
    call('illusion/vanish'),
])
write('vanish', [
    '# As a clone husk: remove it and its display where they stand (never moved below the floor).',
    'scoreboard players operation #rdIlId rd = @s rdObjId',
    f'execute as {VIS} if score @s rdObjId = #rdIlId rd run kill @s',
    'tag @s remove rlk_rd_illusion',
    'kill @s',
])
write('on_break', [
    '# object/break, as the shattered clone at itself (display already removed).',
    'execute unless score #rdIlStep rd matches 1 run return 0',
    'execute if score @s rdReal matches 1 run return run ' + call('illusion/won'),
    '# A shattered fake loses its pending slab.',
    'tag @s remove rlk_rd_illusion',
    'execute as @e[tag=rlk_rd_ilhaz,distance=..0.2] if score @s rdHAge < @s rdWind run ' + call('hazard/expire'),
    sound('block.glass.break', .7, 1.25),
])
write('cleanup', [
    '# Idempotent; any executor. pause / transform / exhausted / cleanup / reload / death call it.',
    '# A cut-short challenge still shows the reappearance when the boss lives.',
    'execute if score #rdIlStep rd matches 1..2 as @e[tag=rlk_raiden,scores={rdPat=5,rdDeath=0},limit=1] at @s run ' + call('fx/blink_in'),
    f'execute as {ILL} at @s run ' + call('fx/blink_out'),
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
print(f'Generated 찰나의 포영: {len(written)} functions (volleys {VOLLEYS}, end {END_T}).')
