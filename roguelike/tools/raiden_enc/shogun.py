"""Raiden phase 0 (Shogun form, plan rd/plan.md A.2, A.5, B.2 phase 0): both weapons, the forced weapon switch (27 / 28)
and its after-effects (6 field lightning / 6b blade eyes), the guard stance 9 with its counters, break stun and
카라타케, the single eye 10 then the multi eye 4, 찰나의 포영 5 (build_raiden_illusions.py) then 몽상의 일심 7, the
rear checks 25 / 26, the combos and ranged moves (1, 2, 3, 8, 21-24) and blink-based spacing. Owner: S2-SHOGUN.

Every timeline runs from rdTime 0 (the choose tick) and calls the rig clips at the offsets that put the manifest
events (raiden_rig_api.md) on the plan's ticks. Hazards come from the kit (raiden_kit.hz): quiet unless the footage
shows a floor decal (6 disc_pale, 9 recovery ring, 10 spawn ring, 4 eye rings, 7 orb rings3). New functions live under
F:boss/raiden/sg/; pattern-scoped entities carry rlk_rd_tmp (pause) and rlk_rd_sg (finish).

Data read by core.build(): IDS, OBJECTIVES, ON_PAUSE, ON_FINISH, REACH (empty: the Shogun rows blink inside their
own timelines), TICK_HIDE (찰나의 포영 hides the rig while the clones are out).
"""
from .core import call, center, face, flat, obj, patterns, target, write
from raiden_kit import decal, fx, hz, hz_group, snd

IDS = ['1..10', '21..28']
OBJECTIVES = ['rdSgFx', 'rdSgFxT', 'rdSgGs', 'rdSgGm', 'rdSgGp', 'rdSgCt', 'rdSgCk', 'rdSgCcd', 'rdSgGd', 'rdSgEye',
              'rdSgRearT', 'rdSgRearCD', 'rdSgRearQ', 'rdSgStun', 'rdSgV', 'rdSgDx']
ON_PAUSE = []
ON_FINISH = ['execute if score @s rdPhase matches 0 run function rlk:boss/raiden/sg/finish']
REACH = {}
TICK_HIDE = ['execute if score @s rdPat matches 5 if score #rdIlStep rd matches 1..2 run scoreboard players set #rdHide rd 1']
# Bags per weapon (plan §B.2 weapon columns; plan.md lists no explicit bag): 0 sword, 1 polearm. The reactive (25, 26),
# forced (27, 28, 7 after 5, 4 one pick after 10) and after-effect (6) ids are never drawn.
BAGS = {0: [3, 8, 2, 5, 9, 10], 1: [1, 21, 22, 23, 24, 9, 10]}
BAG = BAGS[0] + [i for i in BAGS[1] if i not in BAGS[0]]
# Range tags at choose (A.2): N <= 7 b, M 6-14 b, F >= 8 b (24: >= 10 b), '*' any. The draw takes a move whose tag
# fits the player's distance; when none fits it takes any move (its own blink closes the gap).
RANGE = {3: 'F', 8: 'N', 2: 'F', 5: '*', 9: 'N', 10: '*', 1: 'N', 21: 'N', 22: 'F', 23: 'M', 24: 'T'}
RFLAG = {'N': '#rdSgRN', 'M': '#rdSgRM', 'F': '#rdSgRF', 'T': '#rdSgRT'}
EYES = [(-10, -6), (10, -6), (0, 11)]           # multi eye spots about the arena centre (unchanged)
GUARD_LEN, GUARD_BREAK, COUNTER_CHANCE, COUNTER_CD = 160, 14, 35, 60
STUN = 100
FX_EVERY = {1: 80, 2: 60}                       # 6 field lightning / 6b blade eyes
# 원류 4단 bolt field: 7 disks r 1.2 in a 10 x 6 zone centred 8 b ahead (local x left, z forward).
FIELD = [(-4.0, 5.6), (-1.6, 9.8), (0.6, 6.2), (3.6, 8.9), (-3.2, 10.4), (1.9, 10.6), (4.2, 5.4)]
SG = 'rlk:boss/raiden/sg/'
TMP = '"rlk_rd_tmp","rlk_raiden_aux","rlk_room"'


def sg(name, **macro):
    if macro:
        return f'function {SG}{name} {{' + ','.join(f'{k}:{v}' for k, v in macro.items()) + '}'
    return f'function {SG}{name}'


def play(clip):
    return 'function rlk:boss/raiden/rig/play/' + clip


def line(key):
    return call('line/' + key)


def prop(kind, *extra):
    """A rig prop at the execution point and yaw, pattern-scoped (finish / pause remove it)."""
    tags = ['rlk_rd_sg', 'rlk_rd_tmp'] + list(extra)
    return [f'function rlk:boss/raiden/rig/prop/{kind}'] + [f'tag @e[tag=rlk_rd_prop_new] add {t}' for t in tags]


def step(d):
    """One dash step of d blocks along her facing, only into free air within radius 20 (never into a block)."""
    return (f'execute positioned ^ ^ ^{d:g} if entity @e[tag=rlk_raiden_arena,distance=..20] if block ~ ~ ~ minecraft:air '
            'if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~')


def fwd(d, cmd):
    return f'execute positioned ^ ^ ^{d:g} run ' + cmd


def up(h, cmd):
    return f'execute positioned ~ ~{h:g} ~ run ' + cmd


def at_point(d, cmd):
    """cmd at the point d blocks ahead (her yaw kept), pulled in to radius 20 about the arena centre."""
    return [fwd(d, 'summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_sgpt",' + TMP + ']}'), sg('clamp_pt'),
            'execute positioned as @e[tag=rlk_rd_sgpt,limit=1] run ' + cmd, 'kill @e[tag=rlk_rd_sgpt]']


def from_player(lr, fw):
    """Execution point relative to the player facing her: lr blocks to the player's left (+) / right (-), fw toward her."""
    return (f'execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^{lr:g} ^ ^{fw:g} '
            'positioned ~ 201 ~ run ')


BLINK_TO = 'function rlk:boss/raiden/movement/blink_to'
FACE = [face, flat]
EYE10 = '@e[tag=rlk_rd_object,scores={rdObjKind=1,rdObjId=10},limit=1]'
EYES3 = '@e[tag=rlk_rd_object,scores={rdObjKind=1,rdObjId=1..3}]'
HUD_EYE = '「마가츠의 뇌안」을 계속 공격해서 제거하세요'
# Tag the hazard hz() just made here (age -1 until the world tick) as an after-effect: `hurt` does not scale it
# (core.BALANCE_PCT, S3-F review RD-B1).
NOBAL = 'tag @e[tag=rlk_rd_hazard,scores={rdHAge=-1},distance=..0.01] add rlk_rd_nobal'


class TL:
    """A pattern timeline: lines run as the boss `at @s rotated as @s` when rdTime matches. Insertion order is the
    order inside a tick; every t0 line is added first, so a finish mid-file (rdTime back to 0) never re-runs them."""

    def __init__(self, pid):
        self.lines = []
        patterns[pid] = self.lines

    def at(self, t, *cmds, cond=''):
        for c in cmds:
            self.lines.append(f'execute if score @s rdTime matches {t} {cond}at @s rotated as @s run {c}')


def build():
    write('normal_dispatch', [f'execute if score @s rdPat matches {i} run ' + call('patterns/' + str(i))
                              for i in list(range(1, 11)) + list(range(21, 29))])
    build_state()
    build_ai()
    build_guard()
    build_effects()
    build_patterns()


# ---------------------------------------------------------------------------------------------------- lifecycle hooks
def build_state():
    write('sg/setup', [
        '# A new fight (setup, before reload): random weapon, no switch after-effect yet, empty bags.',
        'execute store result score @s rdWpn run random value 0..1',
        'scoreboard players set @s rdSgFx 0',
        'scoreboard players set @s rdSgFxT 0',
        'scoreboard players set @s rdSgGd 2',
        'scoreboard players set @s rdSgEye 0'] +
        [f'scoreboard players set #rdSgB{w}_{i} rd 0' for w, moves in BAGS.items() for i in moves])
    write('sg/reload', [
        '# reload (also on a datapack reload mid-fight): the weapon and the after-effect kind stay.',
        'execute unless score @s rdWpn matches 0..1 run scoreboard players set @s rdWpn 0',
        'execute unless score @s rdSgFx matches 0..2 run scoreboard players set @s rdSgFx 0',
        'execute unless score @s rdSgGd matches 0.. run scoreboard players set @s rdSgGd 2',
        'execute unless score @s rdSgEye matches 0.. run scoreboard players set @s rdSgEye 0',
        'scoreboard players set @s rdSgFxT 0', 'scoreboard players set @s rdSgGs 0', 'scoreboard players set @s rdSgGm 0',
        'scoreboard players set @s rdSgGp 0', 'scoreboard players set @s rdSgCt 0', 'scoreboard players set @s rdSgCk 0',
        'scoreboard players set @s rdSgCcd 0', 'scoreboard players set @s rdSgRearT 0', 'scoreboard players set @s rdSgRearCD 0',
        'scoreboard players set @s rdSgRearQ 0', 'scoreboard players set @s rdSgStun 0', 'scoreboard players set @s rdSgV 0',
        'scoreboard players set @s rdSgDx 0'])
    write('sg/pause', [
        '# pause (as every living boss, without a position; runs on every paused tick). The pattern ends with the',
        '# pause (rdPat 0 after this): the rig goes back to idle once, the guard / counter / stun state goes.',
        'execute unless score @s rdPat matches 0 run function rlk:boss/raiden/sg/idle_clip',
        'scoreboard players set @s rdSgGs 0', 'scoreboard players set @s rdSgCt 0', 'scoreboard players set @s rdSgStun 0',
        'scoreboard players set @s rdSgRearQ 0', 'scoreboard players set @s rdSgFxT 0',
        'kill @e[tag=rlk_rd_sgfx]',
        'execute if entity @a[tag=player,scores={hudHold=1..}] run scoreboard players set @a[tag=player] hudHold 0'])
    write('sg/finish', [
        '# finish (ON_FINISH), phase 0, as the boss: back to the weapon idle; queue a rear check when the player',
        '# hit her from behind within 40 t and stands behind her now (she keeps her facing for it).',
        'function rlk:boss/raiden/sg/idle_clip',
        'scoreboard players set @s rdSgV 0', 'scoreboard players set @s rdSgGs 0', 'scoreboard players set @s rdSgCt 0',
        'scoreboard players set @s rdSgRearQ 0',
        'scoreboard players set #rdSgRear rd 0',
        'execute if score @s rdSgRearT matches 1.. if score @s rdSgRearCD matches ..0 at @s run function rlk:boss/raiden/sg/rear_test',
        'execute if score #rdSgRear rd matches 1 run scoreboard players set @s rdSgRearQ 1',
        'execute if score @s rdSgRearQ matches 1 run scoreboard players set @s rdCool 4'])
    write('sg/idle_clip', [
        '# The idle clip of the current form / weapon (play: applied by the next rig/tick).',
        'execute if score @s rdPhase matches 2 run return run function rlk:boss/raiden/rig/play/t_idle',
        'execute if score @s rdWpn matches 1 run return run function rlk:boss/raiden/rig/play/idle_polearm',
        'function rlk:boss/raiden/rig/play/idle_sword'])
    write('sg/look', [
        '# The rig weapon model follows rdWpn (setup, reload, a test that sets rdWpn).',
        'execute if score @s rdWpn matches 1 run return run function rlk:boss/raiden/rig/look/polearm',
        'function rlk:boss/raiden/rig/look/sword'])
    write('sg/rig_hide', [
        '# core tick: the first tick of #rdHide 1 (찰나의 포영 hidden, Tenma patterns that hide). Every part scales to 0',
        '# where it stands (never moved below the floor); the parts keep following her.',
        'function rlk:boss/raiden/rig/state/hidden',
        'scoreboard players set @s rdHidden 1'])
    write('sg/rig_show', [
        '# core tick: the first visible tick after a hide. A clip queued this tick shows the rig; otherwise the idle.',
        'execute unless score @s rdRigT matches -1 run function rlk:boss/raiden/sg/idle_clip',
        'scoreboard players set @s rdHidden 0'])
    write('sg/clamp_pt', [
        '# Pull the point markers (rlk_rd_sgpt) in to radius 20 about the arena centre.',
        'execute as @e[tag=rlk_rd_sgpt] at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..20] facing entity @s feet rotated ~ 0 positioned ^ ^ ^20 run tp @s ~ ~ ~'])
    write('sg/slow_line', [
        '# 「너무 느리군.」 on one blink in three.',
        'execute store result score #rdSgR rd run random value 0..2',
        'execute if score #rdSgR rd matches 0 run ' + line('too_slow')])
    write('sg/stun_begin', [
        '# As the boss: a 100 t stun (rdPat 98; rdSgStun 1 clone found, 2 single eye broken, 3 guard broken). The cut',
        '# pattern\'s pending hazards and props go.',
        'function rlk:boss/raiden/hazard/finish',
        'kill @e[tag=rlk_rd_sg]',
        'scoreboard players set @s rdSgGs 0', 'scoreboard players set @s rdSgCt 0',
        'scoreboard players set @s rdPat 98', 'scoreboard players set @s rdTime 0', 'scoreboard players set @s rdGo 0',
        'execute if entity @a[tag=player,scores={hudHold=1..}] run scoreboard players set @a[tag=player] hudHold 0'])
    write('sg/stun_tick', [
        '# core tick, rdPat 98: stagger (dark stagger disc r 2.5 for the clone / eye stun, A-08; the gold pillar of the',
        '# guard break is fx/guard_shatter), the guard recovery burst at 100 (decal ring r 4.5 from 76), then finish.',
        'execute if score @s rdTime matches 1 run function rlk:boss/raiden/rig/play/stagger',
        'execute if score @s rdTime matches 1 unless score @s rdSgStun matches 3 at @s run ' + decal('stagger', r=2.5, life=99),
        'execute if score @s rdTime matches 72 unless score @s rdSgStun matches 3 run function rlk:boss/raiden/rig/play/recover',
        'execute if score @s rdTime matches 76 if score @s rdSgStun matches 3 at @s run function rlk:boss/raiden/sg/recover_burst',
        f'execute if score @s rdTime matches {STUN}.. run function rlk:boss/raiden/sg/stun_end'])
    write('sg/recover_burst', [
        '# Guard-break recovery (B-07, wiki 카운터 어택): the glowing ring r 4.5 for 24 t, then a nododge burst that pushes.',
        play('stun_recover'), line('absurd'),
        hz('disk', 24, 6, r=4.5, nododge=True, kb=2.5, decal='ring')])
    write('sg/stun_end', [
        'scoreboard players operation #rdSgK rd = @s rdSgStun',
        'scoreboard players set @s rdSgStun 0',
        'function rlk:boss/raiden/finish',
        '# 몽상의 일심 always follows 찰나의 포영, found or not.',
        'execute if score #rdSgK rd matches 1 run scoreboard players set @s rdNext 7'])
    write('sg/eye_break', [
        '# object/break, as a broken eye at itself. A multi eye only loses its disk (the pocket); the single eye (id 10)',
        '# stuns her: 「간파했군.」, 100 t, the multi eye still comes one pick later.',
        'execute unless score @s rdObjId matches 10 run return 0',
        'execute if entity @a[tag=player,scores={hudHold=1..}] run scoreboard players set @a[tag=player] hudHold 0',
        'execute as @e[tag=rlk_raiden,scores={rdPat=10,rdDeath=0},limit=1] at @s run function rlk:boss/raiden/sg/stun_eye'])
    write('sg/stun_eye', [line('ganpa'), 'scoreboard players set @s rdSgStun 2', sg('stun_begin')])
    write('sg/eye_hud', [
        '# The real game\'s HUD message while the single eye lives (A-18), on the actionbar over the regular HUD.',
        'title @a[tag=player] actionbar {text:"' + HUD_EYE + '",color:"#E9D5FF"}',
        'scoreboard players set @a[tag=player] hudHold 24'])
    write('sg/tick', [
        '# core tick, phase 0, as the boss at its feet.',
        'execute if score @s rdSgRearT matches 1.. run scoreboard players remove @s rdSgRearT 1',
        'execute if score @s rdSgRearCD matches 1.. run scoreboard players remove @s rdSgRearCD 1',
        'execute if score @s rdSgCcd matches 1.. run scoreboard players remove @s rdSgCcd 1',
        'execute if score @s rdSgFx matches 1.. run function rlk:boss/raiden/sg/fx_tick'])
    write('sg/incoming', [
        '# core incoming, phase 0, as the boss at its feet (#dmg after the modifiers).',
        'execute if entity @e[tag=rlk_body,distance=..8,limit=1] run function rlk:boss/raiden/sg/rear_hit',
        'execute if score @s rdPat matches 9 if score @s rdSgGs matches 1 run function rlk:boss/raiden/sg/guard_hit',
        '# Guard broken: damage x1.5 during the stun.',
        'execute if score @s rdPat matches 98 if score @s rdSgStun matches 3 run scoreboard players operation #dmg tmp *= #rd3 rd',
        'execute if score @s rdPat matches 98 if score @s rdSgStun matches 3 run scoreboard players operation #dmg tmp /= #rd2 rd'])
    write('sg/rear_hit', [
        '# A hit taken while the player stands behind her (> 120 deg off her facing, <= 8 b): remember it for 40 t.',
        'function rlk:boss/raiden/sg/rear_test',
        'execute if score #rdSgRear rd matches 1 run scoreboard players set @s rdSgRearT 40'])
    write('sg/rear_test', [
        '# As the boss at its feet: #rdSgRear 1 when the player is within 8 b and more than 120 deg off her facing.',
        'scoreboard players set #rdSgRear rd 0',
        'execute unless entity @e[tag=rlk_body,distance=..8,limit=1] run return 0',
        'execute store result score #rdSgY0 rd run data get entity @s Rotation[0] 100',
        'summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_sgface",' + TMP + ']}',
        'execute as @e[tag=rlk_rd_sgface,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0',
        'execute store result score #rdSgY1 rd run data get entity @e[tag=rlk_rd_sgface,limit=1] Rotation[0] 100',
        'kill @e[tag=rlk_rd_sgface]',
        'scoreboard players operation #rdSgY1 rd -= #rdSgY0 rd'] +
        ['execute if score #rdSgY1 rd matches 18000.. run scoreboard players remove #rdSgY1 rd 36000',
         'execute if score #rdSgY1 rd matches ..-18001 run scoreboard players add #rdSgY1 rd 36000'] * 2 +
        ['execute if score #rdSgY1 rd matches 12001.. run scoreboard players set #rdSgRear rd 1',
         'execute if score #rdSgY1 rd matches ..-12001 run scoreboard players set #rdSgRear rd 1'])


# ---------------------------------------------------------------------------------------------------- choose
def build_ai():
    write('sg/choose', [
        '# core choose, phase 0, as the boss at its feet (rdPat 0 on entry).',
        '# 1. The forced first move after normal_return (TENMA tags it): sword -> 28 polearm, polearm -> 27 sword.',
        'execute if entity @s[tag=rlk_rd_switch_due] if score @s rdWpn matches 0 run scoreboard players set @s rdPat 28',
        'execute if entity @s[tag=rlk_rd_switch_due] if score @s rdWpn matches 1 run scoreboard players set @s rdPat 27',
        'tag @s remove rlk_rd_switch_due',
        '# 2. 몽상의 일심 always follows 찰나의 포영 (rdNext 7, set at its end or its stun end).',
        'execute if score @s rdPat matches 0 if score @s rdNext matches 7 run scoreboard players set @s rdPat 7',
        '# 3. The multi eye one pick after the single eye (rdSgEye 2 at the pick of 10).',
        'execute if score @s rdPat matches 0 if score @s rdSgEye matches 1 run scoreboard players set @s rdPat 4',
        'execute if score @s rdPat matches 0 if score @s rdSgEye matches 2.. run scoreboard players remove @s rdSgEye 1',
        '# 4. Rear checks queued at the last pattern end, if the player is still behind her.',
        'scoreboard players set #rdSgRear rd 0',
        'execute if score @s rdPat matches 0 if score @s rdSgRearQ matches 1 at @s run function rlk:boss/raiden/sg/rear_test',
        'execute if score @s rdPat matches 0 if score #rdSgRear rd matches 1 if score @s rdWpn matches 0 run scoreboard players set @s rdPat 25',
        'execute if score @s rdPat matches 0 if score #rdSgRear rd matches 1 if score @s rdWpn matches 1 run scoreboard players set @s rdPat 26',
        'scoreboard players set @s rdSgRearQ 0',
        '# 5. The weapon bag with the range fit.',
        'execute if score @s rdPat matches 0 if score @s rdWpn matches 0 at @s run function rlk:boss/raiden/sg/draw_0',
        'execute if score @s rdPat matches 0 if score @s rdWpn matches 1 at @s run function rlk:boss/raiden/sg/draw_1'])
    picked = ['# core choose after the test hooks (phase 0): the move leaves its weapon bag; guard spacing; eye queue;',
              '# rear-check cooldown; the rig weapon follows rdWpn.']
    for w, moves in BAGS.items():
        picked += [f'execute if score @s rdWpn matches {w} if score @s rdPat matches {i} run scoreboard players set #rdSgB{w}_{i} rd 0'
                   for i in moves]
    picked += ['scoreboard players add @s rdSgGd 1',
               'execute if score @s rdPat matches 9 run scoreboard players set @s rdSgGd 0',
               'execute if score @s rdPat matches 10 run scoreboard players set @s rdSgEye 2',
               'execute if score @s rdPat matches 4 run scoreboard players set @s rdSgEye 0',
               'execute if score @s rdPat matches 25..26 run scoreboard players set @s rdSgRearCD 300',
               'execute if score @s rdPat matches 25..26 run scoreboard players set @s rdSgRearT 0',
               'scoreboard players set @s rdSgV 0',
               'execute unless score @s rdWpn = @s rdRigW run function rlk:boss/raiden/sg/look']
    write('sg/picked', picked)
    for w, moves in BAGS.items():
        elig = ['# Eligible = still in the bag; the guard (9) only after two other picks.']
        elig += [f'scoreboard players operation #rdSgE{i} rd = #rdSgB{w}_{i} rd' for i in moves]
        elig += ['execute if score @s rdSgGd matches ..1 run scoreboard players set #rdSgE9 rd 0',
                 'scoreboard players set #rdSgCnt rd 0']
        elig += [f'execute if score #rdSgE{i} rd matches 1 run scoreboard players add #rdSgCnt rd 1' for i in moves]
        write(f'sg/elig_{w}', elig)
        write(f'sg/fill_{w}', ['# A refilled bag never starts with the move just used.'] +
              [f'scoreboard players set #rdSgB{w}_{i} rd 1' for i in moves] +
              [f'execute if score @s rdPrev matches {i} run scoreboard players set #rdSgB{w}_{i} rd 0' for i in moves])
        draw = ['# As the boss at its feet: draw from the weapon bag, preferring a move whose range tag fits the player.',
                'scoreboard players set #rdSgRN rd 0', 'scoreboard players set #rdSgRM rd 0',
                'scoreboard players set #rdSgRF rd 0', 'scoreboard players set #rdSgRT rd 0',
                'execute if entity @e[tag=rlk_body,distance=..7,limit=1] run scoreboard players set #rdSgRN rd 1',
                'execute if entity @e[tag=rlk_body,distance=6..14,limit=1] run scoreboard players set #rdSgRM rd 1',
                'execute unless entity @e[tag=rlk_body,distance=..8,limit=1] run scoreboard players set #rdSgRF rd 1',
                'execute unless entity @e[tag=rlk_body,distance=..10,limit=1] run scoreboard players set #rdSgRT rd 1',
                sg(f'elig_{w}'),
                f'execute if score #rdSgCnt rd matches 0 run function {SG}fill_{w}',
                f'execute if score #rdSgCnt rd matches 0 run function {SG}elig_{w}',
                'scoreboard players set #rdSgFc rd 0']
        for i in moves:
            draw.append(f'scoreboard players set #rdSgF{i} rd 0')
            cond = '' if RANGE[i] == '*' else f'if score {RFLAG[RANGE[i]]} rd matches 1 '
            draw.append(f'execute if score #rdSgE{i} rd matches 1 {cond}run scoreboard players set #rdSgF{i} rd 1')
            draw.append(f'execute if score #rdSgF{i} rd matches 1 run scoreboard players add #rdSgFc rd 1')
        draw += [f'execute if score #rdSgFc rd matches 1.. run function {SG}pick_f_{w}',
                 f'execute if score #rdSgFc rd matches 0 run function {SG}pick_e_{w}']
        write(f'sg/draw_{w}', draw)
        for kind, cnt in (('f', '#rdSgFc'), ('e', '#rdSgCnt')):
            flag = 'F' if kind == 'f' else 'E'
            write(f'sg/pick_{kind}_{w}', [
                'execute store result score #rdSgR rd run random value 0..9999',
                f'scoreboard players operation #rdSgR rd %= {cnt} rd',
                'scoreboard players add #rdSgR rd 1'] +
                sum(([f'execute if score @s rdPat matches 0 if score #rdSg{flag}{i} rd matches 1 run scoreboard players remove #rdSgR rd 1',
                      f'execute if score @s rdPat matches 0 if score #rdSg{flag}{i} rd matches 1 if score #rdSgR rd matches 0 run scoreboard players set @s rdPat {i}']
                     for i in moves), []))


# ---------------------------------------------------------------------------------------------------- guard
def build_guard():
    write('sg/guard_on', ['scoreboard players set @s rdSgGs 1', 'scoreboard players set @s rdSgGm 0',
                          'scoreboard players set @s rdSgGp 0', 'scoreboard players set @s rdSgCt 0',
                          'scoreboard players set @s rdSgCcd 0'])
    write('sg/guard_off', ['scoreboard players set @s rdSgGs 0', 'scoreboard players set @s rdSgCt 0'])
    write('sg/guard_hit', [
        '# sg/incoming during the guard (B-03..B-07): basic attacks (#icd 1, not a skill, not a reaction) are parried',
        f'# at x0.1 and fill the meter by 1; everything else passes at x0.5 and fills it by 2; {GUARD_BREAK} breaks it.',
        'scoreboard players set #rdSgBasic rd 0',
        'execute if score #icd tmp matches 1 unless score #skillDmg tmp matches 1 unless score #tfm tmp matches 1 run scoreboard players set #rdSgBasic rd 1',
        'execute if score #rdSgBasic rd matches 1 run function rlk:boss/raiden/sg/guard_parry',
        'execute if score #rdSgBasic rd matches 0 run scoreboard players operation #dmg tmp /= #rd2 rd',
        'execute if score #rdSgBasic rd matches 0 run scoreboard players add @s rdSgGm 2',
        f'execute if score @s rdSgGm matches {GUARD_BREAK}.. run function rlk:boss/raiden/sg/guard_break'])
    write('sg/guard_parry', [
        'scoreboard players operation #dmg tmp /= #rd10 rd',
        'scoreboard players add @s rdSgGm 1',
        'scoreboard players add @s rdSgGp 1',
        'execute at @s rotated as @s run ' + fx('parry'),
        'execute unless score @s rdSgCt matches 1.. run ' + play('parry'),
        f'# In-guard counter (B-04/05): {COUNTER_CHANCE} % on a parried hit, cooldown {COUNTER_CD} t, only while it ends',
        f'# before the guard does ({GUARD_LEN}).',
        'execute if score @s rdSgCt matches 1.. run return 0',
        'execute if score @s rdSgCcd matches 1.. run return 0',
        f'execute if score @s rdWpn matches 0 if score @s rdTime matches {GUARD_LEN - 48}.. run return 0',
        f'execute if score @s rdTime matches {GUARD_LEN - 28}.. run return 0',
        'execute store result score #rdSgR rd run random value 0..99',
        f'execute if score #rdSgR rd matches ..{COUNTER_CHANCE - 1} at @s run function rlk:boss/raiden/sg/counter_start'])
    write('sg/counter_start', [
        '# sg/guard_parry (a player hit, outside the boss tick): queue the counter; its c0 runs on the next boss tick',
        '# (sg/counter_tick: c = rdSgCt - 2), so every counter hit counts from the boss clock. rdSgCk = the weapon.',
        'scoreboard players set @s rdSgCt 1',
        f'scoreboard players set @s rdSgCcd {COUNTER_CD}',
        'scoreboard players operation @s rdSgCk = @s rdWpn'])
    write('sg/counter_c0', [
        face, flat,
        'execute if score @s rdSgCk matches 0 at @s rotated as @s run function rlk:boss/raiden/sg/counter_s0',
        'execute if score @s rdSgCk matches 1 at @s rotated as @s run function rlk:boss/raiden/sg/counter_p0'])
    write('sg/counter_s0', [
        '# Sword counter: black line (cue) + shield block, spin 12 (disk r 3), floor bolts 24 (rect 8 x 1.5, aimed 12),',
        '# lunge 40 (rect 8 x 2, re-aimed 28).',
        play('counter_sword'), fx('counter_cue'), 'playsound minecraft:item.shield.block hostile @a[tag=player] ~ ~ ~ 1 1.4 0.2',
        hz('disk', 12, 8, r=3, sm='lr')])
    write('sg/counter_p0', [
        '# Polearm counter: cue, star 8, wide sweep 18 (disk r 4.5).',
        play('counter_spear'), fx('counter_cue'), 'playsound minecraft:item.shield.block hostile @a[tag=player] ~ ~ ~ 1 1.4 0.2',
        hz('disk', 18, 12, r=4.5, sm='rl')])
    write('sg/counter_tick', [
        '# Pattern 9, every guard tick while a counter runs (c = rdSgCt - 2; c0 = the first boss tick after the parry).',
        'scoreboard players add @s rdSgCt 1',
        'execute if score @s rdSgCt matches 2 run function rlk:boss/raiden/sg/counter_c0',
        'execute if score @s rdSgCk matches 0 if score @s rdSgCt matches 14 at @s run function rlk:boss/raiden/sg/counter_s12',
        'execute if score @s rdSgCk matches 0 if score @s rdSgCt matches 30 at @s run function rlk:boss/raiden/sg/counter_s28',
        'execute if score @s rdSgCk matches 0 if score @s rdSgCt matches 48.. run function rlk:boss/raiden/sg/counter_end',
        'execute if score @s rdSgCk matches 1 if score @s rdSgCt matches 10 at @s rotated as @s run ' + up(1.6, fwd(0.8, fx('star'))),
        'execute if score @s rdSgCk matches 1 if score @s rdSgCt matches 28.. run function rlk:boss/raiden/sg/counter_end'])
    write('sg/counter_s12', [face, flat, 'execute at @s rotated as @s run ' + hz('rect', 12, 8, len=8, wid=1.5, sm='chop'),
                             'execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.9 1.2 0.2'])
    write('sg/counter_s28', [face, flat, 'execute at @s rotated as @s run ' + hz('rect', 12, 12, len=8, wid=2, sm='thrust'),
                             'execute at @s run ' + snd('iai_charge')])
    write('sg/counter_end', ['scoreboard players set @s rdSgCt 0', play('guard')])
    write('sg/guard_break', [
        '# The meter is full: the guard shatters (white-violet burst + gold light pillar), stun 100 t at x1.5 damage.',
        sg('guard_off'),
        'execute at @s run ' + fx('guard_shatter'),
        'scoreboard players set @s rdSgStun 3',
        sg('stun_begin')])


# ---------------------------------------------------------------------------------------------------- after-effects
def build_effects():
    write('sg/fx_tick', [
        '# sg/tick: the switch after-effect runs until the next transformation (stuns included), not during 5 or 7.',
        'scoreboard players add @s rdSgFxT 1',
        'execute if score @s rdSgFx matches 2 if score @s rdSgFxT matches 8 as @e[tag=rlk_rd_sgfx] at @s run ' + fx('star'),
        'execute if score @s rdSgFx matches 2 if score @s rdSgFxT matches 14 run kill @e[tag=rlk_rd_sgfx]',
        'execute if score @s rdPat matches 5 run return 0',
        'execute if score @s rdPat matches 7 run return 0',
        f'execute if score @s rdSgFx matches 1 if score @s rdSgFxT matches {FX_EVERY[1]}.. run function {SG}fx6',
        f'execute if score @s rdSgFx matches 2 if score @s rdSgFxT matches {FX_EVERY[2]}.. run function {SG}fx6b'])
    write('sg/fx_off', ['# core tick: not phase 0 any more (transformation): the after-effect ends.',
                        'scoreboard players set @s rdSgFx 0', 'scoreboard players set @s rdSgFxT 0', 'kill @e[tag=rlk_rd_sgfx]'])
    write('sg/fx6', [
        '# 6 field lightning (A-02, sword after-effect): the pale disc under the player (locked), the bolt 20 t later.',
        'scoreboard players set @s rdSgFxT 0',
        target + hz('disk', 20, 8, r=2.5, decal='disc_pale', strike='bolt', detached=True), target + NOBAL,
        'execute at @e[tag=rlk_body,limit=1] run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.6 1.7 0.2'])
    write('sg/fx6b', [
        '# 6b blade eye (A-11, polearm after-effect): an eye sigil 1.5 b beside the player, glint 8, burst 12 (disk r 2).',
        'scoreboard players set @s rdSgFxT 0',
        'kill @e[tag=rlk_rd_sgfx]',
        'execute store result score #rdSgSide rd run random value 0..1',
        'execute if score #rdSgSide rd matches 0 ' + from_player(1.5, 0)[len('execute '):] + f'function {SG}fx6b_at',
        'execute if score #rdSgSide rd matches 1 ' + from_player(-1.5, 0)[len('execute '):] + f'function {SG}fx6b_at'])
    # The sigil (+-0.45 b about its pivot at scale 1.2) floats low beside the player, 0.05-0.95 b up (A-11: about
    # 0.3 b; S3-F, review RD-N3: it was 0.55-1.45 b).
    write('sg/fx6b_at', [up(0.5, 'function rlk:boss/raiden/rig/prop/blade_eye'),
                         'tag @e[tag=rlk_rd_prop_new] add rlk_rd_sgfx', 'tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp',
                         hz('disk', 12, 8, r=2, detached=True), NOBAL,
                         'playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.9 1.6 0.2'])


# ---------------------------------------------------------------------------------------------------- patterns
def build_patterns():
    # ---- 27 무기 변경 – 검 (A-01): forced after the stun, polearm -> sword; starts the field lightning.
    p = TL(27)
    p.at(0, play('switch_sword'), line('command'), fx('switch_hoop'), *prop('hoop'), fwd(1, hz('disk', 20, 16, r=6)))
    p.at(6, *prop('vortex'))
    p.at(18, 'kill @e[tag=rlk_rd_prop_vortex,tag=rlk_rd_sg]')
    p.at(20, fx('switch_burst'), 'kill @e[tag=rlk_rd_prop_hoop,tag=rlk_rd_sg]')
    p.at(22, 'scoreboard players set @s rdWpn 0')
    p.at(34, 'scoreboard players set @s rdSgFx 1', 'scoreboard players set @s rdSgFxT 0', call('finish'))

    # ---- 28 무기 변경 – 창 (A-10): blink to the centre, hoop + vortex 14, burst 34; starts the blade eyes.
    p = TL(28)
    p.at(0, center + BLINK_TO)
    p.at(14, *FACE, play('switch_polearm'), line('musang'), fx('switch_hoop'), *prop('hoop'), *prop('vortex'),
         hz('disk', 20, 16, r=5))
    p.at(30, up(1.6, fx('star')))
    p.at(32, 'kill @e[tag=rlk_rd_prop_vortex,tag=rlk_rd_sg]')
    p.at(34, fx('switch_burst'), 'kill @e[tag=rlk_rd_prop_hoop,tag=rlk_rd_sg]')
    p.at(36, 'scoreboard players set @s rdWpn 1')
    p.at(46, 'scoreboard players set @s rdSgFx 2', 'scoreboard players set @s rdSgFxT 0', call('finish'))

    # ---- 6 field lightning: no bag move any more; test/pattern {id:6} shows one cycle at the player.
    p = TL(6)
    p.at(0, sg('fx6'))
    p.at(24, call('finish'))

    # ---- 10 마가츠의 뇌안 (단일) (A-18, B-01): the eye 6 b to her side, 6 hits; blast 148 unless broken.
    p = TL(10)
    p.at(0, play('cast'), line('gaze'), 'kill @e[tag=rlk_rd_sgeye]',
         'execute store result score #rdSgSide rd run random value 0..1',
         'execute if score #rdSgSide rd matches 0 positioned ^6 ^ ^ run summon minecraft:marker ~ 201 ~ {Tags:["rlk_rd_sgeye","rlk_rd_sgpt","rlk_rd_sg",' + TMP + ']}',
         'execute if score #rdSgSide rd matches 1 positioned ^-6 ^ ^ run summon minecraft:marker ~ 201 ~ {Tags:["rlk_rd_sgeye","rlk_rd_sgpt","rlk_rd_sg",' + TMP + ']}',
         sg('clamp_pt'), 'tag @e[tag=rlk_rd_sgeye] remove rlk_rd_sgpt')
    p.at(4, 'execute at @e[tag=rlk_rd_sgeye,limit=1] run ' + fx('eye_spawn'))
    p.at(8, 'execute at @e[tag=rlk_rd_sgeye,limit=1] run ' + obj(1, 'prop/eye_orb', 6, 10, 1.0),
         'execute at @e[tag=rlk_rd_sgeye,limit=1] run ' + hz('disk', 140, 30, r=5, decal='ring', dlife=20),
         sg('eye_hud'))
    for t in range(28, 148, 20):
        p.at(t, f'execute if entity {EYE10} run ' + sg('eye_hud'))
    p.at(122, f'execute as {EYE10} at @s run ' + fx('eye_glow', r=5, life=26))
    p.at(148, f'execute as {EYE10} at @s run ' + fx('eye_blast'),
         'execute if entity @a[tag=player,scores={hudHold=1..}] run scoreboard players set @a[tag=player] hudHold 0',
         call('object/clear'))
    p.at(150, call('finish'))

    # ---- 4 마가츠의 뇌안 (광역) (B-02): never alone, one pick after 10; 3 eyes, r 12 disks, a broken eye = pocket.
    p = TL(4)
    p.at(0, play('cast'), line('eyes'))
    for x, z in EYES:
        p.at(6, center + f'execute positioned ~{x} ~ ~{z} run ' + fx('eye_spawn'))
    p.at(10, hz_group())
    for k, (x, z) in enumerate(EYES, 1):
        p.at(10, center + f'execute positioned ~{x} ~ ~{z} run ' + obj(1, 'prop/eye_orb', 4, k, 1.7),
             center + f'execute positioned ~{x} ~ ~{z} run ' + hz('disk', 130, 34, r=12, decal='ring', group=True))
    p.at(114, f'execute as {EYES3} at @s run ' + fx('eye_glow', r=12, life=26))
    p.at(140, f'execute as {EYES3} at @s run ' + fx('eye_blast'), call('object/clear'))
    p.at(150, call('finish'))

    # ---- 3 뇌명 돌진 (검) (A-04): far = blink 5.5 b in front, iai dash; near (<= 6 b) = draw in place.
    FAR, NEAR = 'if score @s rdSgV matches 0 ', 'if score @s rdSgV matches 1 '
    p = TL(3)
    p.at(0, 'scoreboard players set @s rdSgV 0',
         'execute if entity @e[tag=rlk_body,distance=..6,limit=1] run scoreboard players set @s rdSgV 1', line('noemyeong'))
    p.at(0, from_player(0, 5.5) + BLINK_TO, cond=FAR)
    p.at(0, play('iai_near'), cond=NEAR)
    p.at(12, *FACE, play('iai_dash'), snd('iai_charge'), cond=FAR)
    # rd-sync: the strikes follow the draw (left to right across her facing) and the end crescent (right to left).
    p.at(18, *FACE, up(1.2, fwd(0.6, fx('star'))), hz('rect', 12, 14, len=10, wid=3, sm='lr'),
         *at_point(9, hz('annulus', 18, 13, r=4, half=70, sm='rl')), cond=FAR)
    for t in range(28, 36):
        p.at(t, step(1.125), cond=FAR)
    p.at(28, snd('rush'), cond=FAR)
    p.at(10, *FACE, up(1.2, fwd(0.6, fx('star'))), hz('rect', 12, 14, len=9, wid=2, sm='lr'),
         hz('rect', 18, 13, len=4, wid=2, sm='rise'), cond=NEAR)
    p.at(40, call('finish'), cond=NEAR)
    p.at(66, call('finish'), cond=FAR)

    # ---- 8 5단 콤보 (A-05): V 12, right cut 22, stab 34, wide cut 50, overhead 64.
    p = TL(8)
    p.at(0, play('combo5'), up(1.1, fwd(0.8, fx('star'))), hz_group(),
         hz('rect', 12, 8, len=6, wid=1.2, yawoff=-25, group=True, sm='chop'),
         hz('rect', 12, 8, len=6, wid=1.2, yawoff=25, group=True, sm='chop'))
    p.at(4, step(0.75))
    p.at(5, step(0.75))
    p.at(12, *FACE, snd('twirl_beat'), hz('rect', 10, 8, len=9, wid=1.5, yawoff=20, sm='lr'))
    p.at(22, *FACE, snd('twirl_beat'), fwd(2, hz('disk', 12, 9, r=2.5)))
    p.at(34, *FACE, snd('twirl_beat'), hz('rect', 16, 12, len=10, wid=2, yawoff=-20, sm='rl'))
    p.at(50, *FACE, snd('twirl_beat'), fwd(2.5, hz('disk', 14, 13, r=3)))
    p.at(74, call('finish'))

    # ---- 2 뇌전이 이끈 번개 (A-06): three discs (re-aimed at launch), then the low wave (jump it).
    # R1: the first disc flies at 1.0 b/t (not 2.0): its hit test reaches r 1.7 + tol 0.3 past the centre, so a player
    # more than 7.5 b away is reached >= 12 t after the star flash; the clip's flick (d1 6) is binding, so the launch
    # tick stays. S3-F (review RD-R1): a ranged move that the bag's no-fit fallback (or a test) can start at melee
    # range, so when the player is within 10 b at its start she first blinks back to 11 b from them (toward the arena
    # centre, so the spot is always inside) and casts 10 t later (variant near_blink); otherwise she casts at once.
    V0, V1 = 'if score @s rdSgV matches 0 ', 'if score @s rdSgV matches 1 '
    p = TL(2)
    p.at(0, 'scoreboard players set @s rdSgV 0',
         'execute if entity @e[tag=rlk_body,distance=..10,limit=1] run scoreboard players set @s rdSgV 1')
    p.at(0, 'execute at @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_raiden_arena,limit=1] feet rotated ~ 0 '
         'positioned ^ ^ ^11 positioned ~ 201 ~ run ' + BLINK_TO, sg('slow_line'), cond=V1)
    for o, cond in ((0, V0), (10, V1)):
        p.at(o, *(FACE if o else []), play('disc_cast'), line('will'), up(1.2, fwd(0.6, fx('star'))), cond=cond)
        for t, v in ((5, 1.0), (9, 2.0), (17, 2.0)):
            p.at(o + t, *FACE, hz('orb', 1, 9, d0=0.5, v=v, r=1.7, y=0.8, reach=24), cond=cond)
        p.at(o + 26, snd('iai_charge'), cond=cond)
        p.at(o + 33, *FACE, hz('sweep', 1, 16, r0=1, v=0.8, band=1, half=22, jump=True, detached=True, reach=25), cond=cond)
        p.at(o + 34, snd('wave_low'), cond=cond)
        p.at(o + 64, call('finish'), cond=cond)

    # ---- 5 찰나의 포영: build_raiden_illusions.py (illusion/tick); rdPat 5 keeps her hidden and immune.
    patterns[5] = [call('illusion/tick')]

    # ---- 7 몽상의 일심 (A-09): blink to the centre (the clip embeds the blink-in), 8 rim orbs, darkening, field slash.
    p = TL(7)
    # rd-sync: the release's scatter where she stood, the reform at the centre (whole at 6 = the clip's appear).
    p.at(0, call('movement/depart'), play('musou'), line('calm'), 'scoreboard players set @s rdBlink 24',
         center + 'tp @s ~ ~ ~', *FACE)
    p.at(1, call('movement/arrive'))
    p.at(10, sg('musou_orbs'))
    p.at(20, up(2.4, fx('star')))
    for k in range(8):
        p.at(30 + 8 * k, f'execute as @e[tag=rlk_rd_sgorb,scores={{rdSgDx={k}}}] at @s run ' + hz('disk', 20, 10, r=4, decal='rings3'),
             f'execute as @e[tag=rlk_rd_sgorb,scores={{rdSgDx={k}}}] at @s run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.2')
        p.at(50 + 8 * k, f'kill @e[tag=rlk_rd_sgorbp,scores={{rdSgDx={k}}}]')
    p.at(110, center + fx('musou_dark', life=50), line('sever_one'), center + 'execute positioned ~ ~1.5 ~ run ' + fx('crystal'),
         center + hz('disk', 20, 30, r=19, sm='lr'))
    p.at(130, center + fx('musou_slash'))
    for t, yaw in ((136, 30), (144, 150), (152, 270)):
        p.at(t, center + f'execute rotated {yaw} 0 positioned ^ ^ ^-9 run ' + fx('crystal_line', len=18))
    p.at(160, up(1.6, fx('star')))
    p.at(166, call('finish'))
    write('sg/musou_orbs', [
        '# 8 orbs at r 21, every 45 deg from a random rotation, delivered by sky bolts.',
        'execute store result storage rlk:rd sg.r int 1 run random value 0..44',
        'execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/sg/musou_ring with storage rlk:rd sg'])
    write('sg/musou_ring', ['$execute rotated $(r) 0 run function rlk:boss/raiden/sg/musou_ring8'])
    write('sg/musou_ring8', [f'execute rotated ~{45 * k} 0 positioned ^ ^ ^21 run function {SG}musou_orb {{k:{k}}}' for k in range(8)])
    write('sg/musou_orb', [
        'summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_sgorb","rlk_rd_sgnew","rlk_rd_sg",' + TMP + ']}',
        '$scoreboard players set @e[tag=rlk_rd_sgnew] rdSgDx $(k)',
        'tag @e[tag=rlk_rd_sgnew] remove rlk_rd_sgnew',
        up(1.5, 'function rlk:boss/raiden/rig/prop/musou_orb')] +
        [f'tag @e[tag=rlk_rd_prop_new] add {t}' for t in ('rlk_rd_sg', 'rlk_rd_tmp', 'rlk_rd_sgorbp')] +
        ['$scoreboard players set @e[tag=rlk_rd_prop_new] rdSgDx $(k)', fx('bolt')])

    # ---- 25 판결의 검 (A-03): reactive, sword; straight behind her (yaw + 180, locked at the cue).
    p = TL(25)
    p.at(0, play('rear_iai'), line('verdict'), snd('iai_charge'), up(1.2, fx('star')),
         hz('rect', 14, 15, len=12, wid=1.6, yawoff=180, sm='thrust'))
    p.at(10, 'execute rotated ~180 0 run ' + up(1.0, fwd(1.5, fx('star'))))
    p.at(14, 'execute rotated ~180 0 run ' + fx('crystal_line', len=12))
    p.at(30, call('finish'))

    # ---- 26 창 뒤 견제 (A-12): reactive, polearm; two rear sweeps; hit 1's band on the floor warns of hit 2.
    p = TL(26)
    # rd-sync: sweep 1 passes behind her from her left to her right (right to left in the rear hazard's frame), 2 back.
    p.at(0, play('p_rear'), fx('twirl', life=16), hz('annulus', 16, 10, r=5.8, rmin=4.2, half=100, yawoff=180, sm='rl'),
         hz('annulus', 26, 12, r=5.8, rmin=4.2, half=100, yawoff=180, sm='lr'))
    p.at(6, snd('twirl_beat'))
    p.at(12, snd('twirl_beat'))
    p.at(36, call('finish'))

    # ---- 1 원류 4단 (A-13, A-14): blink to the player's left, 4 hits, bolt field; 60 % lance follow-up at >= 5 b.
    V0, V1 = 'if score @s rdSgV matches 0 ', 'if score @s rdSgV matches 1 '
    p = TL(1)
    p.at(0, from_player(2.5, 0) + BLINK_TO, sg('slow_line'))
    p.at(6, *FACE, play('p_4hit'))
    p.at(10, *FACE, hz('annulus', 18, 9, r=5.5, half=90, sm='rl'))
    p.at(16, up(2.2, fwd(1.0, fx('star'))))
    p.at(28, *FACE, snd('twirl_beat'), hz('annulus', 10, 9, r=5.5, half=90, sm='lr'))
    p.at(38, *FACE, snd('twirl_beat'), hz('rect', 10, 10, len=6, wid=1.5, sm='chop'))
    p.at(48, *FACE, snd('twirl_beat'), hz('rect', 14, 15, len=3, wid=15, off=2, sm='chop'))
    p.at(62, snd('bomb_tell'), hz_group(), *[f'execute positioned ^{x:g} ^ ^{z:g} run ' + hz('disk', 20, 8, r=1.2, group=True)
                                              for x, z in FIELD])
    p.at(90, 'scoreboard players set @s rdSgV 0',
         'execute unless entity @e[tag=rlk_body,distance=..5,limit=1] store result score #rdSgR rd run random value 0..99',
         'execute unless entity @e[tag=rlk_body,distance=..5,limit=1] if score #rdSgR rd matches ..59 run scoreboard players set @s rdSgV 1')
    p.at(90, *FACE, play('p_lance'), cond=V1)
    p.at(96, call('finish'), cond=V0)
    p.at(96, *FACE, up(2.2, fwd(1.0, fx('star'))), target + hz('disk', 8, 14, r=2, strike='bolt'), cond=V1)
    p.at(112, call('finish'))

    # ---- 21 수천수만의 염원 (A-15): blink to the player's right, a 40 t twirl, then the undodgeable slam.
    p = TL(21)
    p.at(0, from_player(-4.5, 0) + BLINK_TO)
    p.at(10, *FACE, play('p_twirl_slam'), line('return_dust'), fx('twirl', life=36), hz('disk', 40, 22, r=6.5, nododge=True, sm='chop'))
    for t in range(16, 47, 6):
        p.at(t, snd('twirl_beat'))
    p.at(48, up(1.8, fx('star')))
    p.at(62, call('finish'))

    # ---- 22 돌진 3콤보 (A-16): twirl, then three re-aimed dashes through the player (11 b each, 4 t).
    p = TL(22)
    p.at(0, play('p_twirl_dash'), line('shadow_world'), fx('twirl', life=15))
    p.at(6, snd('twirl_beat'))
    p.at(12, *FACE, snd('star'), hz('rect', 8, 12, len=11, wid=2, sm='thrust'))
    for t0, lock, hit in ((19, 22, 32), (31, 34, 44)):
        for t in range(t0, t0 + 4):
            p.at(t, step(2.75))
        p.at(lock, *FACE, snd('star'), hz('rect', hit - lock, 12, len=11, wid=2, sm='thrust'))
    for t in range(43, 47):
        p.at(t, step(2.75))
    p.at(58, call('finish'))

    # ---- 23 번개돌진 콤보 (A-17): zig-zag dash to the player, weak ring, crouch + column, lunge.
    p = TL(23)
    p.at(0, play('p_zigzag'), line('noemyeong'))
    p.at(6, *FACE, hz('rect', 8, 12, len=9, wid=2, sm='thrust'))
    p.at(8, up(1.2, fwd(0.6, fx('star'))))
    for t in range(11, 15):
        p.at(t, 'execute unless entity @e[tag=rlk_body,distance=..2.5,limit=1] run ' + step(2.0))
    p.at(22, up(1.0, fx('star')), hz('disk', 12, 6, r=4.5, sm='lr'))
    p.at(40, *FACE, fx('bolt'), hz('rect', 12, 14, len=5, wid=2, sm='thrust'))
    p.at(64, call('finish'))

    # ---- 24 원거리 창 (A-14): blink to 7 b from the player, raise, tip glow (aim lock), lance.
    p = TL(24)
    p.at(0, from_player(0, 7) + BLINK_TO, sg('slow_line'))
    p.at(10, *FACE, play('p_lance'))
    p.at(16, *FACE, up(2.2, fwd(1.0, fx('star'))), target + hz('disk', 8, 14, r=2, strike='bolt'))
    p.at(34, call('finish'))

    # ---- 9 번개 배리어 (B-03..B-07): 160 t guard; parries, counters, break (stun), 카라타케 on a time-out.
    K = 'if score @s rdSgGp matches 4.. '
    p = TL(9)
    # The stance aura (r 1.8, B.3 `aura`) is the rig's own floor ring, shown by the guard / counter clips.
    p.at(0, play('guard'), line('mock'), sg('guard_on'))
    p.at(f'1..{GUARD_LEN - 1}', 'execute if score @s rdSgCt matches 1.. run ' + sg('counter_tick'))
    p.at(f'1..{GUARD_LEN - 1}', 'execute if score @s rdSgCt matches 0 if score @s rdRigC matches 11 if score @s rdRigT matches 6.. run ' + play('guard'))
    p.at(GUARD_LEN, sg('guard_off'))
    p.at(GUARD_LEN, 'execute if score @s rdSgGp matches ..3 run ' + call('finish'))
    p.at(GUARD_LEN, play('karatake'), line('end_it'), fx('blink_out'), cond=K)
    for t in range(GUARD_LEN, GUARD_LEN + 6):
        p.at(t, step(-1.0), cond=K)
    p.at(GUARD_LEN + 10, *FACE, snd('iai_charge'), hz('rect', 20, 24, len=14, wid=3, sm='chop'), cond=K)
    p.at(GUARD_LEN + 32, call('finish'))
