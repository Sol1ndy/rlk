"""Raiden transformation (P1), Tenma phase (P2), exhausted (P3): patterns 11-18, clap/shadow/stakes/judgment, the
armour shield. Owner: S2-TENMA (plan rd/plan.md E.0).

Data read by core.build(): BAG, REACH, CHOOSE_RULES (phase-2 choose lines), TICK_HIDE and TICK_TAIL (tick hooks).
"""
from .core import (DRAIN, DRAIN_DEFAULT, DRAIN_REACTION, EXHAUST, FLOWER_BREAK, SHIELD_CD, SHIELD_MAX,
                   TRANSFORM_FX, TRANSFORM_LEN, at, anim, call, caption, center, end, event, face, flat, gated,
                   haz, obj, pattern, sound, target, tell, write)

# Final calamity entry (pattern 15): she gathers lightning, rises inside a lightning
# pillar while bolts rake the arena, and dissolves at the top (rig hidden from then on).
ASCEND_END, ASCEND_STEP = 26, 0.32
CLAP_LOCK, CLAP_TELL = 17, 14   # pattern 12: hands follow until 17, clap lands 14 later
SHADOW_LOCK = 37                 # pattern 13: the shadow chases for 36 ticks
# 금강괴멸파 (pattern 14): three stakes spread around the centre; each pulse is a ring that
# travels from radius 2 to the far wall (RING_END over RING_FRAMES ticks, jump it).
from build_raiden_fx_textures import RING_END, RING_FRAMES
STAKES = [(0, -9), (7.8, 4.5), (-7.8, 4.5)]
STAKE_TELL = 12

BAG = [11, 12, 13, 14, 16, 17, 18]
REACH = {11: (10, 8), 16: (11, 9), 17: (14, 12), 18: (20, 17)}
CHOOSE_RULES = [
    '# At most one ultimate in each transformation, guaranteed by the fourth move.',
    'execute if score @s rdPhase matches 2 if score @s rdUltUsed matches 1 if score @s rdPat matches 15 run scoreboard players set @s rdPat 18',
    'execute if score @s rdPhase matches 2 if score @s rdUltUsed matches 0 if score #rdTurn rd matches 0 run scoreboard players set @s rdPat 15']
TICK_HIDE = [f'execute if score @s rdPat matches 15 if score @s rdTime matches {ASCEND_END}.. run scoreboard players set #rdHide rd 1']
# M1 seams read by core.build() and raiden_enc.build() (rd/s2_notes.md §3): pattern id ranges, extra objectives,
# pause / finish additions, and voice lines (new keys, or a replacement of a Tenma-owned key of lines.LINES).
IDS = ['11..18']
OBJECTIVES = []
ON_PAUSE = []
ON_FINISH = []
VOICE_LINES = {}
TICK_TAIL = [
    'execute if score @s rdPat matches 15 run function rlk:boss/raiden/judgment_rig/tick',
    'execute if score @s rdPat matches 15 if score @s rdTime matches 80..173 run function rlk:boss/raiden/camera/try_start',
    'execute if score @s rdPat matches 15 if score @s rdTime matches 174 run function rlk:boss/raiden/camera/release_all']

# Following clap hands (pattern 12). Display-only hands owned by the boss; the hazard is
# created on lock at the hands' midpoint, facing along the boss -> player line.
HAND='{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/support_hand_%s"}}'
def hand_tf(side,gap):
    # Fingers up, palm facing the other hand (half turns about the (1,0,+-1) diagonals of
    # the support-hand model: fingers -Y, palm -Z), hand centred gap blocks to the side.
    x=gap if side=='l' else -gap
    q='[0.7071068f,0f,0.7071068f,0f]' if side=='l' else '[0.7071068f,0f,-0.7071068f,0f]'
    return '{translation:[%.3ff,1.6f,0f],left_rotation:%s,scale:[3.6f,3.6f,3.6f],right_rotation:[0f,0f,0f,1f]}'%(x,q)


def build():
    write('transform_start','''
function rlk:boss/raiden/camera/release_all
scoreboard players set @s rdGo 0
scoreboard players set @s rdNext 0
function rlk:boss/raiden/judgment_rig/cleanup
function rlk:boss/raiden/illusion/cleanup
scoreboard players set @s rdWalk 0
kill @e[tag=rlk_rd_hazard]
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
scoreboard players set @s rdPhase 1
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players add @s rdCycle 1
# Transforms where it stands (normally only after its pattern ended). A test/forced
# start can land mid-blink: let that blink finish in place without a destination.
kill @e[tag=rlk_rd_blink_dest]
scoreboard players set @s rdAnim 9
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
function rlk:boss/raiden/line/eternal
scoreboard players set #rdCapPat rd 0
playsound minecraft:entity.wither.spawn hostile @a[tag=player] ~ ~ ~ 0.8 0.5 0.4
''')
    # The burst and its danger circle start at the boss on TRANSFORM_FX; the transform
    # clip (46) ends before armor_start at TRANSFORM_LEN.
    write('transform_title',['# After her line: the form name and the armour hint.']+'''title @a[tag=player] times 8 55 16
title @a[tag=player] subtitle {text:"번개 갑주를 파괴하면 잠시 무력화됩니다",color:"white"}
title @a[tag=player] title {text:"악요의 요고우 텐마",color:"light_purple",bold:true}
scoreboard players set @a[tag=player] vBig 79
scoreboard players set @a[tag=player] ttlT 79
scoreboard players set #rdCap rd 1
# Not a pattern caption: an interrupted illusion caption must not let armor_start\'s
# finish (rdTime 56) cut this one short.
'''.strip().split('\n')+['scoreboard players set #rdCapPat rd 0'])
    write('transform_tick',[caption('악요의 요고우 텐마 · 변신'),at('30',call('transform_title')),
        at(str(TRANSFORM_FX),call('vfx/transform')),at(str(TRANSFORM_FX),haz(8,30,18,42)),
        at(str(TRANSFORM_FX+14),sound('entity.lightning_bolt.thunder',.6,.7)),
        at(str(TRANSFORM_LEN),call('armor_start'))])
    write('armor_start',f'''
attribute @s minecraft:scale base set 2.2
scoreboard players set @s rdPhase 2
scoreboard players set @s rdShield {SHIELD_MAX}
scoreboard players set @s rdUltUsed 0
scoreboard players set @s rdPTime 0
scoreboard players set @s rdTurns 0
scoreboard players set @s rdHitCD 0
function rlk:boss/raiden/finish
scoreboard players set @s rdCool 14
''')
    write('armor_tick','''
scoreboard players add @s rdPTime 1
scoreboard players operation #rdMod rd = @s rdPTime
scoreboard players operation #rdMod rd %= #rd4 rd
execute unless score @s rdPat matches 15 if score #rdMod rd matches 0 run scoreboard players remove @s rdShield 1
scoreboard players operation #rdEnergyTick rd = @s rdPTime
scoreboard players set #rd20 rd 20
scoreboard players operation #rdEnergyTick rd %= #rd20 rd
execute if score #rdEnergyTick rd matches 0 unless score #charN tmp matches 3 run scoreboard players remove @a[tag=player,limit=1] energy 100
execute as @a[tag=player,scores={energy=..-1}] run scoreboard players set @s energy 0
execute unless score @s rdPat matches 15 if score @s rdShield matches ..0 run function rlk:boss/raiden/exhausted_start
''')
    write('exhausted_start','''
function rlk:boss/raiden/camera/release_all
kill @e[tag=rlk_rd_clap]
kill @e[tag=rlk_rd_shadow]
function rlk:boss/raiden/judgment_rig/cleanup
function rlk:boss/raiden/illusion/cleanup
function rlk:boss/raiden/movement/cleanup
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
attribute @s minecraft:scale base set 1.2
kill @e[tag=rlk_rd_hazard]
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
scoreboard players set @s rdPhase 3
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdAnim 23
scoreboard players set @s rdShield 0
scoreboard players operation @a[tag=player,limit=1] energy = #burstCost100 tmp
title @a[tag=player] times 5 45 15
title @a[tag=player] subtitle {text:"갑주 파괴 · 지금 공격하세요!",color:"green",bold:true}
execute as @a[tag=player] run function rlk:view/ttl_blank
scoreboard players set @a[tag=player] ttlT 65
scoreboard players set #rdCap rd 1
playsound minecraft:entity.iron_golem.death hostile @a[tag=player] ~ ~ ~ 0.8 0.72 0.3
execute at @s run function rlk:boss/raiden/vfx/armor_break
''')
    write('exhausted_tick',[at('46',anim(22)),at(str(EXHAUST-28),anim(24)),at(str(EXHAUST),call('normal_return'))])
    write('normal_return','''
attribute @s minecraft:scale base set 1.2
scoreboard players set @s rdPhase 0
scoreboard players set @s rdRage 0
function rlk:boss/raiden/finish
scoreboard players set @s rdCool 20
''')
    write('shield_hit','''
# Armor absorbs 80% body damage. Every character can break it; fire and ice work fastest.
execute if score #dmg tmp matches ..0 run return 0
execute if score @s rdHitCD matches ..0 if score #dmg tmp matches 1.. run function rlk:boss/raiden/shield_drain
scoreboard players set #rdDiv rd 5
scoreboard players operation #dmg tmp /= #rdDiv rd
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1
''')
    write('shield_drain',[
        f'# One drain per {SHIELD_CD} ticks however many hits/DoT ticks land. #elem: 0 physical 1 fire 2 water',
        '# 3 thunder 4 ice 5 rock 6 wind 7 grass 8 void; reaction/DoT damage (#tfm) drains least.',
        f'scoreboard players set #rdDrain rd {DRAIN_DEFAULT}']+[
        f'execute if score #elem tmp matches {e} run scoreboard players set #rdDrain rd {v}' for e,v in DRAIN.items()]+[
        f'execute if score #tfm tmp matches 1 run scoreboard players set #rdDrain rd {DRAIN_REACTION}',
        'scoreboard players operation @s rdShield -= #rdDrain rd',
        f'scoreboard players set @s rdHitCD {SHIELD_CD}'])
    write('armor_dispatch',[f'execute if score @s rdPat matches {i} run '+call('patterns/'+str(i)) for i in range(11,19)])
    p=pattern(11,'거대 팔 연격 · 검의 궤적과 투척 낙뢰에 주의')
    event(p,1,call('line/cleave_all'))
    for t in [1,6+tell(11)]:
        event(p,t,face,flat,anim(10),haz(4,tell(11),19));event(p,t+tell(11),anim(11),sound('entity.player.attack.sweep',1.2,.62))
    t+=tell(11)+5
    event(p,t,anim(7),target+haz(3,tell(10),22));event(p,t+tell(10),anim(8));end(p,t+tell(10)+7)
    p=pattern(12,'인공팔 협격 · 따라오는 두 손이 박수치기 전에 빠져나오세요')
    # Two hands appear at the player's sides and follow them, then lock and clap shut.
    event(p,1,face,flat,anim(12),call('clap/spawn'),call('line/prison'))
    p.append('execute if score @s rdTime matches 1..'+str(CLAP_LOCK-1)+' run '+call('clap/follow'))
    event(p,CLAP_LOCK,call('clap/lock'))
    event(p,CLAP_LOCK+CLAP_TELL-3,call('clap/shut'))
    event(p,CLAP_LOCK+CLAP_TELL,anim(13),sound('entity.iron_golem.attack',1,.65),sound('entity.zombie.attack_iron_door',.7,.6))
    event(p,CLAP_LOCK+CLAP_TELL+3,call('clap/fade'))
    event(p,CLAP_LOCK+CLAP_TELL+9,call('clap/clear'))
    end(p,CLAP_LOCK+CLAP_TELL+10)
    p=pattern(13,'그림자 손 · 따라오는 그림자에서 계속 달아나세요')
    # A shadow chases the player (repeated small damage while it covers them), then a hand
    # slams down where it stops. Contract with build_raiden_rig.mjs: the floating hand lands
    # at hazard age 12 (SLAM_CONTACT); the finish 12 ticks after landing lets it fade.
    event(p,1,anim(14),call('shadow/spawn'),sound('entity.warden.dig',.6,1.4),call('line/prison'))
    p.append('execute if score @s rdTime matches 1..'+str(SHADOW_LOCK-1)+' run '+call('shadow/follow'))
    event(p,SHADOW_LOCK,call('shadow/lock'))
    event(p,SHADOW_LOCK+12,anim(15),sound('entity.generic.explode',.65,.72))
    end(p,SHADOW_LOCK+24)
    p=pattern(14,'금강괴멸파 · 퍼지는 번개 고리를 점프로 회피')
    event(p,1,anim(7),call('stakes_start'),call('line/cheonsu'));event(p,15,anim(8))
    # As in the original: each stake fires once in turn, twice round, then all three at once.
    # Rings overlap in time (each travels RING_FRAMES ticks to the far wall).
    for k,i in enumerate([1,2,3,1,2,3]):
        event(p,20+28*k,call('stakes_pulse_'+str(i)))
    LAST=20+28*6+4
    event(p,LAST,call('stakes_pulse'))
    end(p,LAST+STAKE_TELL+RING_FRAMES+4)
    p=pattern(15,'최종 재앙 · 추억의 꽃을 공격한 뒤 보호막 안으로!')
    event(p,1,call('judgment_start'),anim(16));
    p.append(f'execute if score @s rdTime matches 2..{ASCEND_END-1} at @s run tp @s ~ ~{ASCEND_STEP} ~')
    for t,(bx,bz) in zip([3,7,11,15,19,23],[(9,-6),(-11,4),(5,12),(-7,-12),(13,6),(-14,-3)]):
        event(p,t,center+f'execute positioned ~{bx} ~ ~{bz} run '+call('vfx/judgment_bolt'),center+f'execute positioned ~{bx} ~ ~{bz} run playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 1.2 0.7 0.4')
    event(p,ASCEND_END,call('movement/depart'),sound('entity.lightning_bolt.thunder',1,.6),center+'execute positioned ~ ~ ~-8 run tp @s ~ ~ ~ 0 0')
    # The gameplay hint follows once the line has been spoken (line ends ~tick 46).
    event(p,ASCEND_END+21,call('judgment_hint'));event(p,30,sound('block.beacon.ambient',.6,.5));event(p,70,sound('block.portal.ambient',.45,.55))
    # The flower retains the full six-second response window despite quicker recovery.
    # The hidden body already waits at centre-8; it reforms there facing the player.
    event(p,120,call('judgment_strike'));event(p,170,face,flat,call('movement/arrive'));end(p,176)
    p=pattern(16,'신속한 발도 / 몽상 · 단절')
    # Two moves of the original, picked at random:
    #  0 신속한 발도: a charged horizontal iai around her; a white flash marks the dodge.
    #  1 몽상·단절: the giant sword rises while a straight line lights up on the floor, she
    #    calls "단절!" and brings it straight down along the line; a weak field rings her.
    p.append('execute if score @s rdTime matches 1 store result score #rdVar rd run random value 0..1')
    IAI='if score #rdVar rd matches 0'
    hit=1+tell(14)
    gated(p,1,IAI,face,flat,anim(10),haz(4,tell(14),30),haz(10,tell(14),26))
    gated(p,hit-4,IAI,'execute positioned ^ ^2.4 ^1.2 run '+call('object_vfx/object_break'),sound('block.amethyst_block.resonate',1,1.9))
    gated(p,hit,IAI,anim(11),sound('entity.lightning_bolt.thunder',.8,.68))
    gated(p,hit+11,IAI,call('finish'))
    CUT='if score #rdVar rd matches 1'
    hit=1+tell(16)
    gated(p,1,CUT,face,flat,anim(16),haz(5,tell(16),34),haz(8,12,5),sound('block.beacon.power_select',.7,.6))
    gated(p,hit-5,CUT,call('line/sever'))
    gated(p,hit,CUT,anim(17),sound('entity.lightning_bolt.thunder',.9,.6),sound('entity.generic.explode',.6,.8))
    gated(p,hit+12,CUT,call('finish'))
    p=pattern(17,'검파 연사 · 다섯 갈래 뒤 넓은 가로 검파')
    event(p,1,call('line/goemyeol'))
    t=1+tell(10)
    event(p,1,face,flat,anim(7),haz(9,tell(10),17));event(p,t,anim(8),sound('entity.breeze.shoot',.8,.72))
    event(p,t+5,face,flat,anim(10),haz(10,tell(10),21));event(p,t+5+tell(10),anim(11));end(p,t+12+tell(10))
    p=pattern(18,'발도 돌진 · 고정된 직선 경로를 피하세요')
    event(p,1,call('line/pierce'))
    t=1+tell(10)
    event(p,1,face,flat,anim(2),haz(5,tell(10),22));event(p,t,anim(21),sound('item.trident.riptide_3',.7,.8))
    p.append(f'execute if score @s rdTime matches {t}..{t+11} at @s rotated as @s positioned ^ ^ ^0.75 if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless entity @e[tag=rlk_raiden_arena,distance=20.5..] run tp @s ~ ~ ~')
    # After the dash she keeps cutting: two wide sweeps in a row.
    t+=14
    event(p,t,face,flat,anim(10),haz(4,tell(9),19));event(p,t+tell(9),anim(11),sound('entity.player.attack.sweep',1.2,.62))
    t+=tell(9)+4
    event(p,t,face,flat,anim(10),haz(4,tell(8),19));event(p,t+tell(8),anim(11),sound('entity.player.attack.sweep',1.2,.7));end(p,t+tell(8)+7)
    write('clap/spawn',[
        '# As the boss. Two hands appear beside the player, facing along the boss -> player line.',
        'kill @e[tag=rlk_rd_clap]',
        'execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ facing entity @s feet rotated ~180 0 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_clap","rlk_rd_clap_l"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",teleport_duration:2,interpolation_duration:4,view_range:3f,width:12f,height:8f,shadow_radius:0f,brightness:{sky:15,block:15},transformation:'+hand_tf('l',4.2).replace('3.6f,3.6f,3.6f','0.2f,0.2f,0.2f')+',item:'+HAND%'l'+'}',
        'execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ facing entity @s feet rotated ~180 0 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_clap","rlk_rd_clap_r"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",teleport_duration:2,interpolation_duration:4,view_range:3f,width:12f,height:8f,shadow_radius:0f,brightness:{sky:15,block:15},transformation:'+hand_tf('r',4.2).replace('3.6f,3.6f,3.6f','0.2f,0.2f,0.2f')+',item:'+HAND%'r'+'}',
        'execute as @e[tag=rlk_rd_clap] at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_raiden,limit=1] feet',
        'execute as @e[tag=rlk_rd_clap] at @s rotated ~180 0 run tp @s ~ ~ ~ ~ 0',
        'data merge entity @e[tag=rlk_rd_clap_l,limit=1] {start_interpolation:0,transformation:'+hand_tf('l',4.2)+'}',
        'data merge entity @e[tag=rlk_rd_clap_r,limit=1] {start_interpolation:0,transformation:'+hand_tf('r',4.2)+'}',
    ])
    write('clap/follow',[
        '# As the boss: the hands drift after the player (slower than a sprint).',
        'execute as @e[tag=rlk_rd_clap] at @s facing entity @e[tag=rlk_body,limit=1] feet positioned ^ ^ ^0.3 unless entity @e[tag=rlk_body,distance=..0.4] run tp @s ~ 201 ~',
        'execute as @e[tag=rlk_rd_clap] at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_raiden,limit=1] feet',
        'execute as @e[tag=rlk_rd_clap] at @s rotated ~180 0 run tp @s ~ ~ ~ ~ 0',
    ])
    write('clap/lock',[
        '# As the boss: the hands stop; the clap zone (8 x 8) is centred between them.',
        'execute as @e[tag=rlk_rd_clap_l,limit=1] at @s rotated as @s positioned ^ ^ ^-4 run '+haz(7,CLAP_TELL,25),
        'execute as @e[tag=rlk_rd_clap] run data merge entity @s {teleport_duration:0}',
    ])
    write('clap/shut',[
        '# Three ticks before the hit: the palms slam together over the zone.',
        'data merge entity @e[tag=rlk_rd_clap_l,limit=1] {interpolation_duration:3,start_interpolation:0,transformation:'+hand_tf('l',.7)+'}',
        'data merge entity @e[tag=rlk_rd_clap_r,limit=1] {interpolation_duration:3,start_interpolation:0,transformation:'+hand_tf('r',.7)+'}',
    ])
    write('clap/fade',[
        'execute as @e[tag=rlk_rd_clap] run data merge entity @s {interpolation_duration:5,start_interpolation:0,transformation:{translation:[0f,2.4f,0f],left_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]}}',
    ])
    write('clap/clear',['kill @e[tag=rlk_rd_clap]'])

    # Chasing shadow (pattern 13): a dark decal follows the player more slowly than a sprint,
    # nibbling them while it covers them, then the floating hand slams where it stopped.
    write('shadow/spawn',[
        'kill @e[tag=rlk_rd_shadow]',
        'execute at @e[tag=rlk_body,limit=1] positioned ~ 201.03 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_shadow"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:5,view_range:3f,width:6f,height:2f,shadow_radius:0f,brightness:{sky:15,block:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2f,2f,2f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_hazard/after_3"}}}',
        'data merge entity @e[tag=rlk_rd_shadow,limit=1] {start_interpolation:0,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[19f,19f,19f],right_rotation:[0f,1f,0f,0f]}}',
        'scoreboard players set #rdShadowT rd 0',
    ])
    write('shadow/follow',[
        '# As the boss. 0.26 block/tick: walking cannot outrun it, sprinting/dashing can.',
        f'execute as @e[tag=rlk_rd_shadow,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet positioned ^ ^ ^0.26 unless entity @e[tag=rlk_body,distance=..0.3] run tp @s ~ 201.03 ~',
        'scoreboard players add #rdShadowT rd 1',
        'execute if score #rdShadowT rd matches 8.. run '+call('shadow/bite'),
    ])
    write('shadow/bite',[
        'scoreboard players set #rdShadowT rd 0',
        'execute as @e[tag=rlk_rd_shadow,limit=1] at @s if entity @e[tag=rlk_body,distance=..1.8] run '+call('shadow/hurt'),
    ])
    write('shadow/hurt',[
        '# As the shadow (knockback source).',
        'scoreboard players set #cmDmg tmp 6',
        'scoreboard players operation #cmLv tmp = @e[tag=rlk_raiden,limit=1] mlv',
        'scoreboard players set #cmEl tmp 3',
        call('hurt'),
    ])
    write('shadow/lock',[
        '# As the boss: the shadow becomes the slam target (hand + 12-tick disk, radius 5).',
        'execute at @e[tag=rlk_rd_shadow,limit=1] positioned ~ 201 ~ run '+haz(6,12,24),
        'execute at @e[tag=rlk_rd_shadow,limit=1] positioned ~ 201 ~ run '+call('rig/target_slam_spawn'),
        'kill @e[tag=rlk_rd_shadow]',
    ])
    write('stakes_start',[call('object/clear')]+[
        center+f'execute positioned ~{x} ~ ~{z} run '+obj(4,'lightning_stake',1,i,0)
        for i,(x,z) in enumerate(STAKES,1)])
    RING=haz(11,STAKE_TELL,14,STAKE_TELL+RING_FRAMES+5)
    write('stakes_pulse',['execute as @e[tag=rlk_rd_object,scores={rdObjKind=4}] at @s run '+RING,sound('block.beacon.power_select',.55,.7)])
    for i in [1,2,3]:
        write('stakes_pulse_'+str(i),[f'execute as @e[tag=rlk_rd_object,scores={{rdObjKind=4,rdObjId={i}}}] at @s run '+RING,
            f'execute as @e[tag=rlk_rd_object,scores={{rdObjKind=4,rdObjId={i}}}] at @s run playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.9 0.7 0.3'])
    write('judgment_start',[call('object/clear'),'scoreboard players set @s rdUltUsed 1','scoreboard players set @s rdWalk 0',
        center+call('judgment_rig/start'),
        center+call('vfx/judgment_warning'),
        center+'execute positioned ~ ~ ~3 run '+obj(3,'remembrance_flower',4,1,.05),
        '# She stays in view: lightning gathers around her and she rises (patterns/15 lifts her).',
        call('vfx/judgment_ascend'),
        call('line/mangeop'),
        sound('entity.wither.ambient',.7,.5),sound('block.beacon.activate',.9,.5)])
    write('judgment_hint',[
        'title @a[tag=player] times 4 85 16',
        'title @a[tag=player] subtitle {text:"꽃을 공격 → 보호막 안으로! 번개 1타 / 다른 공격 4타",color:"aqua",bold:true}',
        'execute as @a[tag=player] run function rlk:view/ttl_blank',
        'scoreboard players set @a[tag=player] ttlT 105',
        'scoreboard players set #rdCap rd 1',
        'scoreboard players set #rdCapPat rd 1',
    ])
    write('dome_create','''
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_dome"]}
scoreboard players set @e[tag=rlk_rd_dome] rdTime 0
function rlk:boss/raiden/vfx/dome_create
playsound minecraft:block.beacon.activate player @a[tag=player] ~ ~ ~ .85 1.25 .4
''')
    # A persistent wire dome marks the exact safe radius. Keep the old entry point
    # harmless for callers retained across reloads; no particle-only replacement.
    write('dome_draw',['# Safe dome is rendered by vfx/dome_create.'])
    write('dome_tick','''
scoreboard players add @s rdTime 1
execute if score @s rdTime matches 180.. run kill @s
''')
    write('judgment_strike',f'''
scoreboard players set #rdSafe rd 0
execute as @e[tag=rlk_rd_dome,limit=1] at @s run function rlk:boss/raiden/dome_contains
execute if score #rdSafe rd matches 0 as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:boss/raiden/judgment_fatal
execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/vfx/judgment_strike
# A successful defence cracks a quarter of the armor.
execute if score #rdSafe rd matches 1 run scoreboard players remove @s rdShield {FLOWER_BREAK}
''')
    write('judgment_fatal','''
# This announced encounter mechanic requires the flower dome, not a timed dash.
# Setting custom HP to zero preserves the existing death / Ronova revival flow.
execute if score @s dead matches 1 run return 0
execute if score @s rnDie matches 1.. run return 0
scoreboard players operation #hurtDmg tmp = @s curHealth
scoreboard players set #elem tmp 3
function rlk:player/hurt_do
scoreboard players set @s curHealth 0
function rlk:player/die
''')
    write('dome_contains','''
# The entire marked ground circle is safe, including a player jumping inside it.
execute unless entity @e[tag=rlk_body,distance=..7,limit=1] run return 0
execute store result score #rdSafeX rd run data get entity @e[tag=rlk_body,limit=1] Pos[0] 100
execute store result score #rdSafeZ rd run data get entity @e[tag=rlk_body,limit=1] Pos[2] 100
execute store result score #rdDomeX rd run data get entity @s Pos[0] 100
execute store result score #rdDomeZ rd run data get entity @s Pos[2] 100
scoreboard players operation #rdSafeX rd -= #rdDomeX rd
scoreboard players operation #rdSafeZ rd -= #rdDomeZ rd
scoreboard players operation #rdSafeX rd *= #rdSafeX rd
scoreboard players operation #rdSafeZ rd *= #rdSafeZ rd
scoreboard players operation #rdSafeX rd += #rdSafeZ rd
execute if score #rdSafeX rd matches ..160000 run scoreboard players set #rdSafe rd 1
''')
