"""Raiden transformation (P1), Tenma phase (P2), exhausted (P3): the transformation T, patterns 11-20, the armour
shield, the exhausted break and the return to the Shogun. Owner: S2-TENMA (plan rd/plan.md E.0, A.3-A.5, B.2).

Data read by core.build() / raiden_enc.build() (rd/s2_notes.md §3): BAG, REACH (+ REACH_SPOT / REACH_MIN for the
blink-only close-in), CHOOSE_RULES (phase-2 choose lines), TICK_HIDE, TICK_TAIL, IDS, OBJECTIVES, ON_PAUSE, ON_FINISH,
VOICE_LINES.

Conventions of this module
- Timelines run on the pattern clock rdTime (choose = 0, first dispatched frame = 1). A clip is started with
  rig/start/<clip> at rdTime s, which puts clip tick e on rdTime s + e - 1; every pattern starts its clip at 1, so the
  clip events of rd/rig_api (binding, plan §C.5) land on the §B ticks. 17 and 20 open with a short lead (5 / 8 t: the
  voice line and a glint at rdTime 1) before the clip, so their first big or close hit gets the R1 cue time
  (plan_table_src.py rows 17 / 20; S3-F moved both by one tick, review RD-R2 / RD-R3).
- Hazards and FX come from the kit (raiden_kit.hz / fx / snd / decal). Floor decals only where the footage has one:
  the glaive bomb ring (11, 20), the 단절 band (19), the shadow pool (13) and the vajra base rings (14, state decals).
- Every transient entity summoned here carries rlk_room, rlk_raiden_aux, rlk_rd_tmp and rlk_rd_tm; ON_FINISH removes
  rlk_rd_tm, and transform_start / exhausted_start / death/start / pause remove rlk_rd_tmp plus every kit display.
"""
from raiden_kit import decal, fx, hz, hz_group, snd
import re
from .core import (DRAIN, DRAIN_DEFAULT, DRAIN_REACTION, EXHAUST, FLOWER_BREAK, SHIELD_CD, SHIELD_MAX, at, call,
                   center, face, flat, obj, pattern, patterns, sound, target, write)
from .lines import VOICE2

T_LEN = 60                      # transformation length (armor_start); core.TRANSFORM_LEN (also 60) only scales the bar
# The armour beat of the transformation: the clip `transform` turns her into the Tenma (event `form`, clip tick 50 =
# rdTime 50), the burst at 46 announces it. From this tick she carries rlk_rd_armoured and combat/apply ignores hits
# (phase 1); before it the transformation takes damage normally and she can die (user 10-22).
ARMOR_BEAT = 50
TAGS = '"rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_tm"'
SPOT = 'rlk_rd_tm_spot'
AT_SPOT = f'execute at @e[tag={SPOT},limit=1] run '
AT_POOL = 'execute at @e[tag=rlk_rd_hazard,scores={rdHK=8},limit=1] run '
AT_POOL_FLOOR = 'execute at @e[tag=rlk_rd_hazard,scores={rdHK=8},limit=1] positioned ~ 201 ~ run '
AT_CLAP = 'execute at @e[tag=rlk_rd_tm_clapc,limit=1] run '
# 금강괴멸파: three vajras round the centre (side 6, circumradius 3.5), pulses 1,2,3,1,2,3 every 36 t from 60, then all
VAJRAS = [(0, -3.5), (3.03, 1.75), (-3.03, 1.75)]
VAJRA_T = (6, 12, 18)
PULSES = [(60 + 36 * k, v) for k, v in enumerate((1, 2, 3, 1, 2, 3))]
TRIPLE = 276
VAJRA_END = 310
VAJRA_CUE = 12                  # the current runs down the vajra 12 t before its ring (R1; plan: 10)
RING = dict(r0=2, v=0.8, band=1.4, half=180, jump=True, reach=27)
# transformation: one pillar on the player, five more on this fixed layout (polar r, deg) turned by a random yaw
PILLARS = [(8, 30), (12, 150), (12, 270), (18, 90), (18, 210)]
SLAM_POSE = '{translation:[0f,%sf,0f],left_rotation:[0.7071068f,0f,0f,0.7071068f],scale:[%sf,%sf,%sf],right_rotation:[0f,0f,0f,1f]}'
ID_TF = '{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[%sf,%sf,%sf],right_rotation:[0f,0f,0f,1f]}'

BAG = [11, 12, 13, 14, 16, 17, 19]
# Close-in (rd/s2_notes.md §3.2.4): REACH[pid] = (start, stop) as before; REACH_SPOT = the blink lands d b in front of
# the player; REACH_MIN = she also repositions when the player is nearer than lo. 11 blinks if > 8 b, 16 if > 9 b,
# 19 blinks to 10 b in front if the player is outside 6-14 b (plan A.4, B.2).
REACH = {11: (8, 4), 16: (9, 5), 19: (14, 10)}
REACH_SPOT = {11: 3.5, 16: 5, 19: 10}
REACH_MIN = {19: 6}
CHOOSE_RULES = [
    '# Tenma picks (plan A.4), later lines win: 18 when the player is >= 10 b away and the last pick was not 18; 20 when',
    '# the player stood in her rear cone at the end of the last pattern (tm/after) and its 300 t cooldown is over; the 40 %',
    '# chain after 16 (17 or 11); 15 replaces the fourth pick once per transformation.',
    'execute if score @s rdPhase matches 2 unless score @s rdPrev matches 18 at @s unless entity @e[tag=rlk_body,distance=..10] run scoreboard players set @s rdPat 18',
    'execute if score @s rdPhase matches 2 if entity @s[tag=rlk_rd_tm_rear] if score @s rdTmCD matches ..0 run scoreboard players set @s rdPat 20',
    'execute if score @s rdPhase matches 2 if score @s rdTmChain matches 1.. run scoreboard players operation @s rdPat = @s rdTmChain',
    'execute if score @s rdPhase matches 2 if score @s rdUltUsed matches 0 if score #rdTurn rd matches 0 run scoreboard players set @s rdPat 15',
    'scoreboard players set @s rdTmChain 0',
    'tag @s remove rlk_rd_tm_rear']
TICK_HIDE = []
TICK_TAIL = []
IDS = ['11..20']
OBJECTIVES = ['rdTmCD', 'rdTmChain', 'rdTmV']
ON_PAUSE = ['kill @e[tag=rlk_rd_tmp]', call('hazard/clear'),
            'execute as @e[tag=rlk_raiden,scores={rdPhase=2,rdDeath=0}] at @s run ' + call('tm/idle')]
ON_FINISH = ['kill @e[tag=rlk_rd_tm]', 'execute if score @s rdPhase matches 2 run ' + call('tm/after')]
VOICE_LINES = {'foolish': ('어리석군.', 3, VOICE2, 22)}


def ev(p, t, *cmds):
    """Commands at pattern tick t (strings or lists of strings), as the boss at its feet and yaw."""
    for c in cmds:
        for x in ([c] if isinstance(c, str) else c):
            p.append(at(str(t), x))


def span(p, a, b, cmd):
    p.append(f'execute if score @s rdTime matches {a}..{b} at @s rotated as @s run {cmd}')


def clip(name):
    return [call('rig/start/' + name)]


def mk(tag):
    return 'summon minecraft:marker ~ ~ ~ {Tags:[%s,"%s"]}' % (TAGS, tag)


def tagnew(*tags):
    return [f'tag @e[tag=rlk_rd_prop_new] add {t}' for t in ('rlk_rd_tmp', 'rlk_rd_tm') + tags]


def prop(kind, *tags, pre=''):
    return [pre + call('rig/prop/' + kind)] + tagnew(*tags)


def end(p, t):
    ev(p, t, call('finish'))


# ---------------------------------------------------------------------------------------------------------------------
def build():
    lifecycle()
    p11()
    p12()
    p13()
    p14()
    p15()
    p16()
    p17()
    p18()
    p19()
    p20()
    for i in range(11, 21):
        guard(patterns[i])
    write('armor_dispatch', [f'execute if score @s rdPat matches {i} run return run ' + call(f'patterns/{i}') for i in range(11, 21)])


TICK_RE = re.compile(r'^execute if score @s rdTime matches (\d+)')


def guard(lines, every=6):
    """Sort a timeline by its start tick (stable) and insert `return 0` guards, so a tick only runs the lines up to the
    first guard past it: each guard sits between two start ticks and returns for every earlier tick."""
    head = [x for x in lines if not TICK_RE.match(x)]
    body = sorted((x for x in lines if TICK_RE.match(x)), key=lambda x: int(TICK_RE.match(x).group(1)))
    out, n = [], 0
    for k, x in enumerate(body):
        out.append(x)
        n += 1
        if k + 1 < len(body):
            t, nxt = int(TICK_RE.match(x).group(1)), int(TICK_RE.match(body[k + 1]).group(1))
            if n >= every and nxt > t:
                out.append(f'execute if score @s rdTime matches ..{nxt - 1} run return 0')
                n = 0
    lines[:] = head + out


def lifecycle():
    clear = ['kill @e[tag=rlk_rd_tmp]', call('hazard/clear'), call('object/clear'), 'kill @e[tag=rlk_rd_dome]',
             'kill @e[tag=rlk_rd_clap]', 'kill @e[tag=rlk_rd_shadow]']
    write('transform_start', [
        '# Phase 0 -> 1 (rage full while no pattern runs, or a test). Clears every pattern entity and visual, cancels a',
        '# blink, then transform_tick plays the 60 t transformation. Hits land (and can kill her) until the armour',
        f'# beat {ARMOR_BEAT} (tag rlk_rd_armoured: combat/apply returns in phase 1 from then on), as in phase 0.',
        'tag @s remove rlk_rd_armoured',
        'scoreboard players set @s rdGo 0', 'scoreboard players set @s rdNext 0', 'scoreboard players set @s rdWalk 0',
        'scoreboard players set @s rdBlink 0', 'kill @e[tag=rlk_rd_blink_dest]',
        call('illusion/cleanup'), call('movement/cleanup')] + clear + [
        'scoreboard players set @s rdPhase 1', 'scoreboard players set @s rdPat 0', 'scoreboard players set @s rdTime 0',
        'scoreboard players add @s rdCycle 1', 
        'tag @s remove rlk_rd_tm_rear', 'scoreboard players set @s rdTmChain 0', face, flat,
        call('line/eternal'), 'scoreboard players set #rdCapPat rd 0', sound('block.beacon.activate', .8, .6)])
    # T 변신 (B-08): blink to the centre, the travelling floor ring (jump it), the sky crackle locks one pillar on the
    # player and five more round the arena, the burst, the form and the title (clip `transform`: ring 20, pillars 44,
    # form 50).
    t = []
    ev(t, 1, clip('transform'), 'execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..1.5] at @s run ' + call('movement/depart'))
    ev(t, 2, 'execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..1.5] run ' + call('movement/arrive'),
       'execute at @e[tag=rlk_raiden_arena,limit=1] run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet', flat)
    ev(t, 19, hz('sweep', 1, 14, r0=2, v=1.0, band=1.4, half=180, jump=True))
    ev(t, 20, snd('transform_ring'))
    ev(t, 24, target + hz('disk', 20, 16, r=1.5, strike='bolt'),
       'execute store result storage rlk:rd tm.rot int 1 run random value 0..359',
       call('tm/t/pillars') + ' with storage rlk:rd tm', snd('transform_pillars'), 'execute positioned ~ ~9 ~ run ' + fx('star'))
    ev(t, 46, fx('transform_burst'))
    ev(t, ARMOR_BEAT, call('transform_title'), 'function rlk:room/raiden/look_tenma', 'tag @s add rlk_rd_armoured')
    ev(t, T_LEN, call('armor_start'))
    write('transform_tick', ['# Phase 1, as the boss: the transformation timeline on rdTime (plan B.2 row T).'] + t)
    write('tm/t/pillars', ['# The five free pillars of the transformation (r 1.5, hit 20 t later) on a fixed layout turned by {rot}.'] + [
        f'$execute at @e[tag=rlk_raiden_arena,limit=1] rotated $(rot) 0 rotated ~{a} 0 positioned ^ ^ ^{r} run '
        + hz('disk', 20, 16, r=1.5, strike='bolt') for r, a in PILLARS])
    write('transform_title', [
        '# The form name only (R2: no hint subtitle).',
        'title @a[tag=player] times 8 55 16', 'title @a[tag=player] subtitle ""',
        'title @a[tag=player] title {text:"악요의 요고우 텐마",color:"light_purple",bold:true}',
        'scoreboard players set @a[tag=player] vBig 79', 'scoreboard players set @a[tag=player] ttlT 79',
        'scoreboard players set #rdCap rd 1', 'scoreboard players set #rdCapPat rd 0'])
    write('armor_start', [
        '# End of the transformation: the Tenma phase with the full armour (the shield takes over from the phase-1 tag).',
        'attribute @s minecraft:scale base set 2.2', 'scoreboard players set @s rdPhase 2', 'tag @s remove rlk_rd_armoured',
        f'scoreboard players set @s rdShield {SHIELD_MAX}', 'scoreboard players set @s rdUltUsed 0',
        'scoreboard players set @s rdPTime 0', 'scoreboard players set @s rdTurns 0', 'scoreboard players set @s rdHitCD 0',
        'scoreboard players set @s rdTmCD 0', 'scoreboard players set @s rdTmChain 0', call('finish'),
        'scoreboard players set @s rdCool 14'])
    write('armor_tick', '''
scoreboard players add @s rdPTime 1
scoreboard players operation #rdMod rd = @s rdPTime
scoreboard players operation #rdMod rd %= #rd4 rd
execute unless score @s rdPat matches 15 if score #rdMod rd matches 0 run scoreboard players remove @s rdShield 1
scoreboard players operation #rdEnergyTick rd = @s rdPTime
scoreboard players set #rd20 rd 20
scoreboard players operation #rdEnergyTick rd %= #rd20 rd
execute if score #rdEnergyTick rd matches 0 unless score #charN tmp matches 3 run scoreboard players remove @a[tag=player,limit=1] energy 100
execute as @a[tag=player,scores={energy=..-1}] run scoreboard players set @s energy 0
execute if score @s rdTmCD matches 1.. run scoreboard players remove @s rdTmCD 1
execute unless score @s rdPat matches 15 if score @s rdShield matches ..0 run function rlk:boss/raiden/exhausted_start
''')
    write('exhausted_start', [
        '# Armour broken (shield 0): 300 t of collapse, damage x2 (incoming), energy refilled; ends in normal_return.',
        call('illusion/cleanup'), call('movement/cleanup'), 'scoreboard players set @s rdBlink 0',
        'scoreboard players set @s rdWalk 0', 'scoreboard players set @s rdGo 0'] + clear + [
        'attribute @s minecraft:scale base set 1.2', 'scoreboard players set @s rdPhase 3', 'scoreboard players set @s rdPat 0',
        'scoreboard players set @s rdTime 0', 'scoreboard players set @s rdShield 0',
        'scoreboard players operation @a[tag=player,limit=1] energy = #burstCost100 tmp',
        'title @a[tag=player] times 5 45 15',
        'title @a[tag=player] subtitle {text:"갑주 파괴",color:"green",bold:true}',
        'execute as @a[tag=player] run function rlk:view/ttl_blank', 'scoreboard players set @a[tag=player] ttlT 65',
        'scoreboard players set #rdCap rd 1',
        'playsound minecraft:entity.iron_golem.death hostile @a[tag=player] ~ ~ ~ 0.8 0.72 0.3',
        'execute at @s run function rlk:boss/raiden/vfx/armor_break'] + clip('t_collapse'))
    write('exhausted_tick', ['# Phase 3, as the boss: kneel loop after the collapse, stand up, then the Shogun returns.']
          + [at('46', x) for x in clip('exhausted')] + [at(str(EXHAUST - 28), x) for x in clip('recover')]
          + [at(str(EXHAUST), call('normal_return'))])
    write('normal_return', [
        '# Back to the Shogun (end of the break, or test/to_normal). The forced weapon switch comes next: the Shogun',
        '# choose consumes rlk_rd_switch_due (rd/s2_notes.md §3.2.1).',
        'attribute @s minecraft:scale base set 1.2', 'kill @e[tag=rlk_rd_tm]', 'scoreboard players set @s rdPhase 0',
        'scoreboard players set @s rdRage 0', 'tag @s add rlk_rd_switch_due', 'tag @s remove rlk_rd_tm_rear', call('finish'),
        'scoreboard players set @s rdCool 20', 'function rlk:room/raiden/look_shogun',
        'execute if score @s rdRigW matches 1 run ' + call('rig/play/idle_polearm'),
        'execute unless score @s rdRigW matches 1 run ' + call('rig/play/idle_sword')])
    write('shield_hit', '''
# Armor absorbs 80% body damage. Every character can break it; fire and ice work fastest.
execute if score #dmg tmp matches ..0 run return 0
execute if score @s rdHitCD matches ..0 if score #dmg tmp matches 1.. run function rlk:boss/raiden/shield_drain
scoreboard players set #rdDiv rd 5
scoreboard players operation #dmg tmp /= #rdDiv rd
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1
''')
    write('shield_drain', [
        f'# One drain per {SHIELD_CD} ticks however many hits/DoT ticks land. #elem: 0 physical 1 fire 2 water',
        '# 3 thunder 4 ice 5 rock 6 wind 7 grass 8 void; reaction/DoT damage (#tfm) drains least.',
        f'scoreboard players set #rdDrain rd {DRAIN_DEFAULT}'] + [
        f'execute if score #elem tmp matches {e} run scoreboard players set #rdDrain rd {v}' for e, v in DRAIN.items()] + [
        f'execute if score #tfm tmp matches 1 run scoreboard players set #rdDrain rd {DRAIN_REACTION}',
        'scoreboard players operation @s rdShield -= #rdDrain rd',
        f'scoreboard players set @s rdHitCD {SHIELD_CD}'])
    write('tm/idle', ['# @s = the boss in phase 2: the hover idle (also after a pause).', call('rig/play/t_idle')])
    write('tm/after', [
        '# @s = the boss when a phase-2 pattern ends (finish, ON_FINISH): the idle clip, the rear-cone check for 20',
        '# (+-60 deg of her back, <= 9 b: three discs inscribed in the cone) and the 40 % chain after 16 (17 or 11, cool 4).',
        call('tm/idle'), 'tag @s remove rlk_rd_tm_rear',
        'execute at @s rotated as @s rotated ~180 0 positioned ^ ^ ^2 if entity @e[tag=rlk_body,distance=..1.7] run tag @s add rlk_rd_tm_rear',
        'execute at @s rotated as @s rotated ~180 0 positioned ^ ^ ^4.2 if entity @e[tag=rlk_body,distance=..3.6] run tag @s add rlk_rd_tm_rear',
        'execute at @s rotated as @s rotated ~180 0 positioned ^ ^ ^6.5 if entity @e[tag=rlk_body,distance=..5.6] run tag @s add rlk_rd_tm_rear',
        'execute at @s unless entity @e[tag=rlk_body,distance=..9] run tag @s remove rlk_rd_tm_rear',
        'scoreboard players set @s rdTmChain 0',
        'execute unless score @s rdPrev matches 16 run return 0',
        'execute store result score #rdTmR rd run random value 0..99',
        'execute if score #rdTmR rd matches ..19 run scoreboard players set @s rdTmChain 17',
        'execute if score #rdTmR rd matches 20..39 run scoreboard players set @s rdTmChain 11',
        'execute if score @s rdTmChain matches 1.. run scoreboard players set @s rdCool 4'])


# ---------------------------------------------------------------------------------------------------------------------
def throw_bomb(p, lock, bomb_decal):
    """11 / 20: cock-back + aim lock at `lock` (cue), the glaive leaves her hand at lock + 9 (clip release, rd-sync) and
    flies to the spot, landing 12 t after the lock (disk r 3) and staying planted;
    the bomb ring (decal, 12 t) at `bomb_decal`, the bomb (disk r 3.5) 12 t after it."""
    ev(p, lock, f'kill @e[tag={SPOT}]', target + mk(SPOT), face, flat, AT_SPOT + hz('disk', 12, 18, r=3),
       sound('item.trident.riptide_1', .7, 1.3))
    ev(p, lock + 9, call('tm/glaive_fly'))
    ev(p, lock + 10, call('tm/glaive_fly2'))
    ev(p, lock + 12, call('tm/glaive_land'))
    ev(p, bomb_decal, AT_SPOT + hz('disk', 12, 20, r=3.5, decal='ring'), AT_SPOT + snd('bomb_tell'))
    ev(p, bomb_decal + 12, AT_SPOT + fx('bomb'), 'kill @e[tag=rlk_rd_tm_glaive]', f'kill @e[tag={SPOT}]')


def p11():
    # 몽상 • 염원이 깃든 백안지륜 (B-09): two glaive sweeps (annulus 2.5-7.5, +-100 deg), the throw, the planted glaive
    # bursts 50 t after it landed. Clip t_combo3: raise 0, sw1 14, sw2 26, cock 42, throw 54, reform 62.
    p = pattern(11, '몽상 • 염원이 깃든 백안지륜')
    ev(p, 1, clip('t_combo3'), call('line/cleave_all'), face, flat, hz('annulus', 13, 19, r=7.5, rmin=2.5, half=100, sm='rl'))
    ev(p, 14, snd('glaive_sweep'))
    ev(p, 15, face, flat, hz('annulus', 11, 19, r=7.5, rmin=2.5, half=100, sm='lr'))
    ev(p, 26, snd('glaive_sweep'))
    throw_bomb(p, 42, 92)
    end(p, 108)
    write('tm/glaive_fly', [
        '# @s = the boss at the release (lock + 9; t_combo3 51, t_spin_throw 28 hide her glaive): the thrown glaive leaves',
        '# her hand tip first, aimed down at the locked spot (rd-sync: release 3 t before the landing).',
        'kill @e[tag=rlk_rd_tm_flyer]',
        'execute positioned ^-1.0 ^2.4 ^1.8 run summon minecraft:item_display ~ ~ ~ {Tags:[%s,"rlk_rd_tm_flyer"],billboard:"fixed",'
        'item_display:"none",teleport_duration:2,interpolation_duration:0,view_range:3f,width:10f,height:10f,shadow_radius:0f,'
        'brightness:{block:15,sky:15},transformation:{translation:[0f,0f,-4.4f],left_rotation:[0.7071068f,0f,0f,0.7071068f],'
        'scale:[3.6f,3.6f,3.6f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":'
        '"rlk:raiden/glaive"}}}' % TAGS,
        f'execute as @e[tag=rlk_rd_tm_flyer] at @s run tp @s ~ ~ ~ facing entity @e[tag={SPOT},limit=1] feet',
        snd('glaive_sweep')])
    write('tm/glaive_fly2', ['# @s = the boss, lock + 10: the glaive flies onto the spot in 2 t (teleport interpolation).',
                             f'execute as @e[tag=rlk_rd_tm_flyer] at @e[tag={SPOT},limit=1] run tp @s ~ ~0.5 ~'])
    write('tm/glaive_land', [
        '# @s = the boss: the thrown glaive lands on the locked spot (pink beam) and stays planted (prop cut at the floor).',
        'kill @e[tag=rlk_rd_tm_flyer]',
        AT_SPOT + fx('glaive_throw'),
        f'execute at @e[tag={SPOT},limit=1] facing entity @s feet rotated ~180 0 run ' + call('rig/prop/glaive_planted')]
        + tagnew('rlk_rd_tm_glaive'))


def p20():
    # 몽상 • 초월의 악요개안 (B-14), reactive: the line and an eye flare at rdTime 1 lead the clip by 8 t (R1: the spin
    # is a 141 b2 annulus, so 20 t from the first cue; S3-F, review RD-R2: Tenma timelines start at rdTime 1, so the
    # lead is 8, not 7); t_spin_throw: glint 0, spin 13, throw 31 -> pattern 8 / 21 / 39.
    p = pattern(20, '몽상 • 초월의 악요개안')
    ev(p, 1, call('line/foolish'), 'scoreboard players set @s rdTmCD 300', face, flat,
       'execute positioned ~ ~2.6 ~ run ' + fx('star'))
    ev(p, 9, clip('t_spin_throw'), hz('annulus', 12, 18, r=7, rmin=2, half=180, sm='rl'))
    ev(p, 21, snd('glaive_sweep'))
    throw_bomb(p, 27, 77)
    end(p, 93)


def p16():
    # 번개 신의 신속한 발도 (B-10): crouch charge, the orb flash 10, the 360 deg disc slash r 12 at 22 (dash i-frames
    # dodge it). Clip t_iai: crouch 0, flash 10, hit 22.
    p = pattern(16, '번개 신의 신속한 발도')
    ev(p, 1, clip('t_iai'), face, flat, fx('iai_charge'), hz('disk', 21, 30, r=12, sm='rl'))
    ev(p, 10, 'execute positioned ^ ^1.2 ^1.2 run ' + fx('star'))
    ev(p, 22, snd('iai_hit'))
    ev(p, 23, fx('crystal_ring', r=6))
    end(p, 40)


def p19():
    # 몽상 • 단절 (B-12): halo 6, sky column 16, the band to the wall through the player 24 (40 t decal), the slam 64,
    # then a weak field r 4.5 round her for 40 t (detached). Clip t_danjeol: halo 6, raise 10, band 24, slam 64.
    p = pattern(19, '몽상 • 단절')
    ev(p, 1, clip('t_danjeol'), face, flat)
    ev(p, 6, fx('danjeol_halo'), call('line/sever'))
    ev(p, 16, fx('danjeol_column'))
    ev(p, 24, face, flat, hz('to_wall', 40, 34, wid=5, decal='band', sm='chop'), snd('danjeol_band'))
    ev(p, 64, snd('danjeol_slam'), hz('field', 2, 3, r=4.5, every=10, life=43, detached=True))
    end(p, 70)


def p12():
    # 흉장의 수안 · 박수 (B-13): dark sphere, an orb flies to the player, two giant hands flank them and follow at
    # 0.3 b/t, the palms flash (lock) and clap 14 t later; twice. Clip t_summon: sphere 4, throw 16.
    p = pattern(12, '흉장의 수안 · 박수')
    ev(p, 1, clip('t_summon'), face, flat, call('line/prison'), fx('crystal'), snd('clap_summon'))
    ev(p, 4, call('tm/clap/sphere'))
    ev(p, 16, call('tm/clap/orb'))
    ev(p, 17, 'execute as @e[tag=rlk_rd_tm_orb] at @e[tag=rlk_body,limit=1] run tp @s ~ ~1 ~')
    for k, (t0, lock) in enumerate(((24, 50), (80, 104))):
        ev(p, t0, 'kill @e[tag=rlk_rd_tm_orb]', call('tm/clap/spawn'))
        span(p, t0 + 1, lock - 1, call('tm/clap/follow'))
        ev(p, lock, call('tm/clap/lock'))
        ev(p, lock + 11, call('tm/clap/shut'))
        ev(p, lock + 14, AT_CLAP + snd('clap'))
        ev(p, lock + 16, call('tm/clap/fade'))
        ev(p, lock + 22, 'kill @e[tag=rlk_rd_clap]')
    end(p, 130)
    hand = lambda side, d, sub: (f'execute at @e[tag=rlk_rd_tm_clapc,limit=1] facing entity @s feet rotated ~180 0 positioned ^{d} ^1.6 ^ run {sub}')
    write('tm/clap/sphere', ['# @s = the boss: the dark sphere with the eye round her (2.5 b).',
                             'execute positioned ~ ~1.6 ~ run ' + call('rig/prop/seed')] + tagnew('rlk_rd_tm_sphere') + [
        'data merge entity @e[tag=rlk_rd_tm_sphere,limit=1] {transformation:%s}' % (ID_TF % (2.5, 2.5, 2.5))])
    write('tm/clap/orb', ['# @s = the boss: the sphere shrinks into the orb that flies to the player (8 t).',
                          'kill @e[tag=rlk_rd_tm_sphere]', 'execute positioned ~ ~1.6 ~ run ' + call('rig/prop/seed')]
          + tagnew('rlk_rd_tm_orb') + ['data merge entity @e[tag=rlk_rd_tm_orb,limit=1] {teleport_duration:8}'])
    write('tm/clap/spawn', [
        '# @s = the boss: the pair centre on the player, a hand 2.8 b to each side (palms in), its pivot 1.6 b up (the hand',
        '# reaches 0.25 b above the floor, never below it).',
        'kill @e[tag=rlk_rd_clap]',
        'execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run ' + mk('rlk_rd_tm_clapc').replace('"rlk_rd_tm_clapc"', '"rlk_rd_tm_clapc","rlk_rd_clap"'),
        hand('l', 2.8, call('rig/prop/clap_l'))] + tagnew('rlk_rd_clap', 'rlk_rd_tm_hl') + [
        hand('r', -2.8, call('rig/prop/clap_r'))] + tagnew('rlk_rd_clap', 'rlk_rd_tm_hr') + [
        snd('clap_summon')])
    write('tm/clap/follow', [
        '# @s = the boss: the pair centre walks after the player at 0.3 b/t; the hands keep their sides.',
        'execute as @e[tag=rlk_rd_tm_clapc,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.3 unless entity @e[tag=rlk_body,distance=..0.35] run tp @s ~ 201 ~',
        hand('l', 2.8, 'tp @e[tag=rlk_rd_tm_hl,limit=1] ~ ~ ~ ~ 0'),
        hand('r', -2.8, 'tp @e[tag=rlk_rd_tm_hr,limit=1] ~ ~ ~ ~ 0')])
    write('tm/clap/lock', [
        '# @s = the boss: the palms flash (14 t star) and the clap zone locks between them.',
        'execute at @e[tag=rlk_rd_tm_hl,limit=1] run ' + fx('clap_star'),
        'execute at @e[tag=rlk_rd_tm_hr,limit=1] run ' + fx('clap_star'),
        AT_CLAP + hz('disk', 14, 16, r=3)])
    write('tm/clap/shut', [
        '# @s = the boss: the palms slam together over the zone (3 t).',
        'execute as @e[tag=rlk_rd_clap,type=item_display] run data merge entity @s {teleport_duration:3}',
        hand('l', 0.9, 'tp @e[tag=rlk_rd_tm_hl,limit=1] ~ ~ ~ ~ 0'),
        hand('r', -0.9, 'tp @e[tag=rlk_rd_tm_hr,limit=1] ~ ~ ~ ~ 0')])
    write('tm/clap/fade', [
        'execute as @e[tag=rlk_rd_clap,type=item_display] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:%s}' % (ID_TF % (0, 0, 0))])


def p13():
    # 흉장의 수안 · 추적 손바닥 (B-15): the seed, a pool follows the player (DoT every 20 t), stops and grows (dark
    # magenta disc r 4.5), the palm slams from above. Clip t_seed: twirl 0, throw 8.
    p = pattern(13, '흉장의 수안 · 추적 손바닥')
    ev(p, 1, clip('t_seed'), face, flat, fx('twirl', life=8))
    ev(p, 8, call('tm/shadow/seed'))
    ev(p, 9, 'execute as @e[tag=rlk_rd_tm_seed] at @e[tag=rlk_body,limit=1] run tp @s ~ ~0.4 ~')
    ev(p, 12, 'kill @e[tag=rlk_rd_tm_seed]',
       target + hz('follow', 16, 4, r=1.5, v=0.32, every=20, life=57, decal='pool'), target + fx('crystal'))
    for t in (12, 32, 52):
        ev(p, t, AT_POOL + snd('shadow_loop'))
    ev(p, 68, AT_POOL + snd('shadow_grow'))
    ev(p, 69, call('tm/shadow/grow'))
    ev(p, 72, call('tm/shadow/palm'))
    palm = 'execute as @e[tag=rlk_rd_tm_palm,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:%d,transformation:%s}'
    # S3-F (review RD-F1): the palm model reaches 0.416 b below its pivot at scale 3.2 (palm down), so the contact
    # pose sits 0.45 b up (lowest point 0.03 b above the floor) and the rebound 0.85 b; tenma_tests checks the bounds.
    for t, d, y, s in ((73, 4, 7, 3.2), (77, 4, 7.4, 3.2), (81, 3, 0.45, 3.2), (85, 2, 0.85, 3.2), (89, 6, 1.2, 0)):
        ev(p, t, palm % (d, SLAM_POSE % (y, s, s, s)))
    ev(p, 84, AT_SPOT + fx('shadow_palm'))
    ev(p, 95, 'kill @e[tag=rlk_rd_tm_palm]')
    end(p, 96)
    write('tm/shadow/seed', ['# @s = the boss: the seed leaves her hand and reaches the player in 4 t.',
                             'execute positioned ^-0.6 ^1.6 ^0.8 run ' + call('rig/prop/seed')] + tagnew('rlk_rd_tm_seed', 'rlk_rd_shadow') + [
        'data merge entity @e[tag=rlk_rd_tm_seed,limit=1] {teleport_duration:4}', snd('shadow_seed')])
    write('tm/shadow/grow', [
        '# @s = the boss, tick 69: the pool stops; the slam (disk r 4.5, lift) locks where it stopped and its pool decal',
        '# grows from the pool size in 4 t.',
        f'kill @e[tag={SPOT}]', AT_POOL_FLOOR + mk(SPOT),
        f'execute unless entity @e[tag={SPOT}] at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run ' + mk(SPOT),
        AT_SPOT + hz('disk', 15, 24, r=4.5, decal='pool', lift=True),
        'data modify entity @e[tag=rlk_rd_decal_pool,tag=rlk_rd_fxnew,limit=1] transformation.scale set value [1.5f,1f,1.5f]',
        'data modify entity @e[tag=rlk_rd_decal_pool,tag=rlk_rd_fxnew,limit=1] item.components."minecraft:custom_data".d set value 4'])
    write('tm/shadow/palm', [
        '# @s = the boss: the pale palm appears 7 b above the grown pool (palm down; at contact its lowest point is 0.03 b above the floor).',
        AT_SPOT + 'summon minecraft:item_display ~ ~ ~ {Tags:[%s,"rlk_rd_tm_palm","rlk_rd_shadow"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:0,view_range:2.5f,width:16f,height:20f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:%s,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/prop/slam_palm"}}}'
        % (TAGS, SLAM_POSE % (7, 0.01, 0.01, 0.01))])


def p14():
    # 금강괴멸파 (B-18): three vajras, each pulses a floor ring (sweep r0 2, 0.8 b/t, jump it) in the order 1,2,3,1,2,3,
    # then all three. The current runs down the vajra 12 t before its ring, its top flashes 2 t before. Clip t_vajra:
    # hurl 6 / 12 / 18.
    p = pattern(14, '금강괴멸파')
    ev(p, 1, clip('t_vajra'), face, flat, call('line/cheonsu'))
    for k, (t, (x, z)) in enumerate(zip(VAJRA_T, VAJRAS), 1):
        ev(p, t, call('tm/vajra/drive') + f' {{k:{k},x:{x},z:{z},life:{VAJRA_END - t}}}')
    for P, v in PULSES + [(TRIPLE, 0)]:
        sel = f'execute as @e[tag=rlk_rd_tm_vajra{"" if not v else ",scores={rdTmV=%d}" % v}] at @s run '
        ev(p, P - VAJRA_CUE, sel + fx('bolt'), sel + snd('vajra_current'))
        ev(p, P - 2, sel + fx('vajra_pulse'))
        ev(p, P - 1, sel + hz('sweep', 1, 14, **RING))
        ev(p, P, sel + snd('vajra_ring'))
    end(p, VAJRA_END)
    write('tm/vajra/drive', [
        '# @s = the boss: vajra {k} is driven into the floor at the centre + ({x}, {z}), with its base ring (state decal r 2.5).',
        '$execute at @e[tag=rlk_raiden_arena,limit=1] positioned ~$(x) ~ ~$(z) run ' + call('rig/prop/vajra')] + tagnew('rlk_rd_tm_vajra') + [
        '$scoreboard players set @e[tag=rlk_rd_prop_new,limit=1] rdTmV $(k)',
        '$execute at @e[tag=rlk_raiden_arena,limit=1] positioned ~$(x) ~ ~$(z) run ' + fx('vajra_drive'),
        '$execute at @e[tag=rlk_raiden_arena,limit=1] positioned ~$(x) ~ ~$(z) run ' + decal('ring', r=2.5, life=0).replace('life:0', 'life:$(life)')])


# 만겁 sky rift and arm (build_raiden_judgment_rig.mjs: T0 56, key frames to 190, the sweep crosses the dome on 152)
MG_RIFT, MG_RIG_END = 56, 190
MG_BOLTS = [(154, 13, -9), (157, -15, 4), (161, 6, 16), (165, -9, -14)]


def p15():
    # 만겁 (B-17 + the user's reference video S:rd/src/user_refs/mangeop_ref.mp4): she vanishes (immune, hidden, burst
    # energy 0), the arena tints, the flower appears at the centre with the real-game prompt; 1 electro or 4 other hits
    # raise the dome (r 8). The sky tears open on the far side of the flower from the player (56: a slit that gapes into
    # a starry void by 78), a giant armoured arm draws a katana out of it (84..), holds it back to the left (146) and
    # swings it about 210 degrees left -> right with the arm straight (147..160, user 10-22 / 10-22b): on 152 the blade
    # crosses the player's front over the dome (the clash) while the arena-wide slash kills everyone outside it; violet
    # bolts fall round the arena, the dome cracks (160) and shatters (176) as the rift collapses (178..188), she
    # reappears at the centre (184). The camera stays free (the rig faces the player instead; the release's camera lock
    # is not restored). Clips t_vanish (gone 14), t_reform (appear 0).
    p = pattern(15, '만겁')
    ev(p, 1, clip('t_vanish'), call('line/mangeop'), 'scoreboard players set @s rdUltUsed 1', face, flat, fx('iai_charge'))
    ev(p, 14, call('tm/mg/vanish'))
    ev(p, 18, center + fx('mangeop_tint', life=160))
    ev(p, 40, call('tm/mg/flower'))
    ev(p, 42, center + fx('danjeol_column'))
    ev(p, MG_RIFT, 'execute at @e[tag=rlk_raiden_arena,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run '
       + call('judgment_rig/start'), center + snd('mangeop_rift'))
    span(p, MG_RIFT + 1, MG_RIG_END, call('judgment_rig/tick'))
    ev(p, 74, center + snd('mangeop_void'))
    ev(p, 140, center + fx('eye_spawn'))
    ev(p, 151, call('tm/mg/strike'))
    ev(p, 152, call('tm/mg/slash'))
    for t, x, z in MG_BOLTS:
        ev(p, t, center + f'execute positioned ~{x} ~ ~{z} run ' + fx('bolt_big'))
    ev(p, 160, call('tm/mg/crack'))
    ev(p, 176, call('tm/mg/shatter'))
    ev(p, 178, center + snd('mangeop_close'))
    ev(p, 184, call('tm/mg/reform'))
    end(p, 196)
    write('tm/mg/vanish', ['# @s = the boss: the flash and she is gone (rdPat 15 keeps her immune); every burst gauge empties.',
                           fx('mangeop_vanish'), fx('blink_out'), call('rig/state/hidden'),
                           'scoreboard players set @a[tag=player] energy 0'])
    write('tm/mg/flower', [
        '# @s = the boss: the 추모의 꽃다발 at the centre (hit target: 1 electro / 4 other hits, its gauge above it) and the prompt.',
        center + obj(3, 'prop/flower', 4, 1, .05), 'kill @e[tag=rlk_rd_orb_body]',
        center + call('rig/prop/flower')] + tagnew('rlk_rd_tm_flower') + [center + snd('mangeop_flower'), call('judgment_hint')])
    write('judgment_hint', [
        '# The real game\'s prompt for 만겁 (instant kill), R2 allow-list.',
        'title @a[tag=player] times 4 85 16',
        'title @a[tag=player] subtitle {text:"「추모의 꽃다발」에 번개 원소 공격을 가해 보호막을 펼치세요",color:"aqua",bold:true}',
        'execute as @a[tag=player] run function rlk:view/ttl_blank', 'scoreboard players set @a[tag=player] ttlT 105',
        'scoreboard players set #rdCap rd 1', 'scoreboard players set #rdCapPat rd 1'])
    write('tm/mg/strike', [
        '# @s = the boss, tick 151: the slash (hit 152) as a safe dome: inside the raised dome 1 damage, anywhere else fatal;',
        '# without a dome the safe radius is nil.',
        'execute at @e[tag=rlk_rd_dome,limit=1] run ' + hz('safe_dome', 1, 1, r=8, nododge=True),
        'execute unless entity @e[tag=rlk_rd_dome,limit=1] at @e[tag=rlk_raiden_arena,limit=1] run ' + hz('safe_dome', 1, 1, r=0.001, nododge=True)])
    write('tm/mg/slash', [
        '# @s = the boss, tick 152: the screen-wide crescent; the sweeping katana is deflected by a held dome (the clash at',
        '# the blade), which cracks a quarter of the armour. The flower is spent.',
        center + fx('mangeop_slash'),
        'execute if entity @e[tag=rlk_rd_dome,limit=1] run ' + call('judgment_rig/clash'),
        f'execute if entity @e[tag=rlk_rd_dome,limit=1] run scoreboard players remove @s rdShield {FLOWER_BREAK}',
        call('object/clear')])
    write('tm/mg/crack', ['# @s = the boss: the dome cracks under the slash (a short shudder).',
                          'execute at @e[tag=rlk_rd_dome,limit=1] run ' + snd('crystal'),
                          'execute at @e[tag=rlk_rd_dome,limit=1] run ' + snd('mangeop_crack'),
                          'execute as @e[tag=rlk_rd_tm_dome] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:%s}' % (ID_TF % (8.4, 8.4, 8.4)),
                          ])
    write('tm/mg/shatter', ['# @s = the boss: the dome shatters, the flower goes.',
                            'execute at @e[tag=rlk_rd_dome,limit=1] run ' + fx('mangeop_shatter'),
                            'execute at @e[tag=rlk_rd_dome,limit=1] run ' + fx('crystal_ring', r=8),
                            'kill @e[tag=rlk_rd_tm_dome]', 'kill @e[tag=rlk_rd_dome]', 'kill @e[tag=rlk_rd_tm_flower]'])
    write('tm/mg/reform', ['# @s = the boss: she reappears floating at the centre, facing the player.',
                           'execute at @e[tag=rlk_raiden_arena,limit=1] run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet',
                           flat, 'execute at @s run ' + fx('blink_in')] + clip('t_reform'))
    write('dome_create', [
        '# As the broken flower, at it: the safe dome r 8 grows from the flower in 8 t (dome_tick). The bubble is the rig prop',
        '# (rig/prop/dome: 8 displays on fixed yaws, one closed double-sided shell); it starts at a tenth of its size.',
        'kill @e[tag=rlk_rd_dome]', 'kill @e[tag=rlk_rd_tm_dome]',
        'summon minecraft:marker ~ ~ ~ {Tags:[%s,"rlk_rd_dome"]}' % TAGS,
        'scoreboard players set @e[tag=rlk_rd_dome] rdTime 0'] + prop('dome', 'rlk_rd_tm_dome') + [
        'execute as @e[tag=rlk_rd_tm_dome] run data merge entity @s {transformation:%s}' % (ID_TF % (0.8, 0.8, 0.8)),
        fx('mangeop_dome')])
    write('dome_tick', [
        '# As the dome marker (world): grow the dome on its first tick; a stray marker goes after 300 t.',
        'scoreboard players add @s rdTime 1',
        'execute if score @s rdTime matches 1 as @e[tag=rlk_rd_tm_dome] run data merge entity @s {start_interpolation:0,interpolation_duration:8,transformation:%s}' % (ID_TF % (8, 8, 8)),
        'execute if score @s rdTime matches 300.. run kill @s'])


def p17():
    # 몽상 • 궤멸의 검기 (B-11): the line and a glint at rdTime 1 lead the clip by 5 t; t_waves: glint 0, swing1 8, swing2
    # 53 -> pattern 5 / 13 / 58. Swing 1: five tall slabs in a +-30 deg fan (one hit for the set), launched 12 t after the
    # first cue with their near edge 2.2 b out (front d0 3.5, depth 1, tol 0.3), so a player hugging her within 2 b is
    # never hit (plan A.4) and one 2.2-3.8 b out is hit 12 t after the cue (S3-F, review RD-R3: they used to launch 11 t
    # after it with the band at 1.2-2.8 b). Swing 2: one low wide wave (jump it), re-aimed at 46 with its own glint,
    # 12 t before it launches. Both travel on after the end.
    p = pattern(17, '몽상 • 궤멸의 검기')
    ev(p, 1, call('line/goemyeol'), face, flat, 'execute positioned ^ ^2 ^1 run ' + fx('star'))
    ev(p, 6, clip('t_waves'))
    ev(p, 9, face, flat)
    ev(p, 12, hz_group(), *[hz('slab', 1, 15, yawoff=a, d0=3.5, v=0.45, w=0.9, height=4.5, group=True, detached=True)
                             for a in (-30, -15, 0, 15, 30)])
    ev(p, 13, snd('wave_slab'))
    ev(p, 46, face, flat, 'execute positioned ^ ^1 ^1.5 run ' + fx('star'))
    ev(p, 57, hz('sweep', 1, 20, r0=2.5, v=0.28, band=1, half=40, jump=True, detached=True))
    ev(p, 58, snd('wave_low'))
    end(p, 75)


def p18():
    # 번개 신의 강력한 돌진 (B-16): glint, the orb flash locks the player's spot 13, she rushes to 1.5 b short of it
    # in 4 t (23-26), then three undodgeable bursts r 7 round the arrival (28 / 34 / 40). Clip t_rush.
    p = pattern(18, '번개 신의 강력한 돌진')
    ev(p, 1, clip('t_rush'), face, flat, call('line/pierce'), 'execute positioned ^ ^1.4 ^1.5 run ' + fx('star'))
    ev(p, 13, call('tm/rush/lock'))
    span(p, 23, 26, call('tm/rush/step'))
    ev(p, 23, snd('rush'))
    for t in (28, 34, 40):
        ev(p, t, AT_SPOT + snd('barrage'))
    end(p, 52)
    write('tm/rush/lock', [
        '# @s = the boss, tick 13: lock the arrival 1.5 b short of the player (kept 20 b inside the arena), turn to it, the',
        '# flash, the three barrage hazards, and the rush path (start S, delta D in mb) for tm/rush/step.',
        f'kill @e[tag={SPOT}]', 'kill @e[tag=rlk_rd_tm_step]',
        'execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ facing entity @s feet positioned ^ ^ ^1.5 run ' + mk(SPOT),
        f'execute as @e[tag={SPOT},limit=1] at @s unless entity @e[tag=rlk_raiden_arena,distance=..20] at @e[tag=rlk_raiden_arena,limit=1] facing entity @s feet positioned ^ ^ ^20 run tp @s ~ ~ ~',
        f'execute at @s run tp @s ~ ~ ~ facing entity @e[tag={SPOT},limit=1] feet', flat,
        'execute positioned ^ ^1.4 ^1 run ' + fx('star'),
        AT_SPOT + hz('disk', 15, 14, r=7, nododge=True, sm='rl'), AT_SPOT + hz('disk', 21, 14, r=7, nododge=True, sm='lr'),
        AT_SPOT + hz('disk', 27, 14, r=7, nododge=True, sm='chop'),
        'execute store result score #rdTmSX rd run data get entity @s Pos[0] 1000',
        'execute store result score #rdTmSZ rd run data get entity @s Pos[2] 1000',
        f'execute store result score #rdTmDX rd run data get entity @e[tag={SPOT},limit=1] Pos[0] 1000',
        f'execute store result score #rdTmDZ rd run data get entity @e[tag={SPOT},limit=1] Pos[2] 1000',
        'scoreboard players operation #rdTmDX rd -= #rdTmSX rd', 'scoreboard players operation #rdTmDZ rd -= #rdTmSZ rd',
        'execute at @s run ' + mk('rlk_rd_tm_step')])
    write('tm/rush/step', ['# @s = the boss, ticks 23-26: S + D * (rdTime - 22) / 4 (yaw kept).',
                           'scoreboard players operation #rdTmK rd = @s rdTime', 'scoreboard players remove #rdTmK rd 22',
                           'scoreboard players set #rdTm4 rd 4'] + sum(([
        f'scoreboard players operation #rdTm{a} rd = #rdTmD{a} rd', f'scoreboard players operation #rdTm{a} rd *= #rdTmK rd',
        f'scoreboard players operation #rdTm{a} rd /= #rdTm4 rd', f'scoreboard players operation #rdTm{a} rd += #rdTmS{a} rd',
        f'execute store result entity @e[tag=rlk_rd_tm_step,limit=1] Pos[{i}] double 0.001 run scoreboard players get #rdTm{a} rd']
        for a, i in (('X', 0), ('Z', 2))), []) + ['execute at @e[tag=rlk_rd_tm_step,limit=1] run tp @s ~ ~ ~'])
