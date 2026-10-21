"""The organism runtime (plan 7.6.4-7.6.7; org/**) and the nesting walls (wall/**).

STUB (AP-CORE): organisms as framework aux husks (aux/spawn: HP = #apTot x the per-mille of api.ORG_PM, RES Dendro 20 /
others 10 through #auxRes / #auxResEl / #auxResElV, the click shield of the org manifest's kind) tagged rlk_mb_ap_org +
rlk_mb_ap_<kind>, apK = the kind id, one stand-in display each (rlk_mb_ap_om, linked by apOI, following by tp). A
minimal behaviour keeps the stage's economy running: basics walk to the Heart (0.12 b/t, melee r 3.4 / ranged r 8) and
drain it every 40 / 50 t while holding one of the 3 attack slots (buffed: -120); the 파괴 rolls in (0.10 b/t) and blasts
after its 56 t fuse; the 양육 links up to 3 basics within r 10 and is immune while it holds one (NURTURE_MODE 'A'; 'B':
the buffed basics); a kill adds +325 (basic) / +1400 (others). No hazards on the player, no shields, no walls, no
swallow, no models (AP-REV / AP-ORG replace this file).
"""
from .api import Gen, HEART_M, ORGS
from . import api as A

R = A.REV
HEAD = '# STUB (AP-CORE, ap_contract 1.6): the organism runtime; AP-REV replaces this file.'
STAND = {'basic': 'minecraft:big_dripleaf', 'nurt': 'minecraft:flowering_azalea', 'guard': 'minecraft:bamboo',
         'nest': 'minecraft:spore_blossom', 'destr': 'minecraft:pitcher_pod', 'pred': 'minecraft:tropical_fish'}
SPEED = {'basic': R['basic_spd'], 'destr': R['destr_spd']}


def sc(n, v):
    return f'scoreboard players set {n} mb {int(v)}'


def heart_near(r):
    return HEART_M.replace('limit=1', f'distance=..{A.L.num(r)},limit=1')


def emit(g):
    F = g.fn
    kinds = A.KINDS
    for k, rec in kinds.items():
        pm = A.ORG_PM[k]
        sh = rec.get('shield') or {}
        g.w(f'org/spawn_{k}', [
            HEAD, f'# A {rec["name"]} ({k}, apK {rec["id"]}) at the execution position: HP {pm} per mille of #apTot, RES Dendro '
            f'{A.ORG_RES["dendro"]} / others {A.ORG_RES["other"]}.',
            'scoreboard players operation #auxHp mb = #apTot mb', sc('#apX', pm),
            'scoreboard players operation #auxHp mb *= #apX mb', 'scoreboard players operation #auxHp mb /= #c1000 mb',
            'execute if score #auxHp mb matches ..0 run scoreboard players set #auxHp mb 1',
            sc('#auxRes', A.ORG_RES['other']), sc('#auxResEl', 7), sc('#auxResElV', A.ORG_RES['dendro']),
            *A.L.aux_opts(shield_w=float(sh.get('w', 1.2)), shield_h=float(sh.get('h', 2.2))),
            'function rlk:mboss/aux/spawn',
            f'execute as @e[type=minecraft:husk,tag=rlk_mb_auxlast,limit=1] at @s run {F("org/init_" + k)}'])
        init = [HEAD, f'# @s = the new {k} aux husk, at it: tags, kind, state, the stand-in display (apOI link).',
                'tag @s add rlk_mb_ap_org', f'tag @s add rlk_mb_ap_{k}', f'scoreboard players set @s apK {rec["id"]}',
                'scoreboard players set @s apS 0', 'scoreboard players set @s apT 0',
                'scoreboard players add #apOrgN mb 1', 'scoreboard players operation @s apOI = #apOrgN mb',
                f'summon minecraft:item_display ~ ~{A.L.num(0.8 + float(rec.get("hover_y", 0.0)))} ~ '
                '{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_omnew"],billboard:"vertical",teleport_duration:2,'
                'brightness:{block:14,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],'
                f'right_rotation:[0f,0f,0f,1f],scale:[1.6f,1.6f,1.6f]}},item:{{id:"{STAND[k]}",count:1}}}}',
                'scoreboard players operation @e[type=minecraft:item_display,tag=rlk_mb_ap_omnew] apOI = #apOrgN mb',
                'tag @e[type=minecraft:item_display,tag=rlk_mb_ap_omnew] remove rlk_mb_ap_omnew']
        if k == 'basic':
            init += ['# melee / ranged: #apOArg 0 / 1, else 50 / 50',
                     'scoreboard players operation #apX mb = #apOArg mb',
                     'execute unless score #apX mb matches 0..1 store result score #apX mb run random value 0..1',
                     'execute if score #apX mb matches 1 run tag @s add rlk_mb_ap_rng']
        g.w(f'org/init_{k}', init)

    hover = {k: float(rec.get('hover_y', 0.0)) for k, rec in kinds.items()}
    tick = [HEAD, '# @s = an organism husk, at it (rev/tick, phase 2): a kill pays the progress and removes it; else its clock, the',
            '# display follows, the kind\'s behaviour (apK).',
            f'execute if entity @s[tag=rlk_mb_broken] run return run {F("org/broke")}',
            'scoreboard players add @s apT 1',
            'scoreboard players operation #apO mb = @s apOI',
            'execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_om] if score @s apOI = #apO mb run tp @s ~ ~0.8 ~']
    for k, rec in kinds.items():
        if g.has(f'org/k_{k}') or k in ('basic', 'destr', 'nurt'):
            tick.append(f'execute if score @s apK matches {rec["id"]} run return run {F("org/k_" + k)}')
    g.w('org/tick', tick)
    assert hover is not None
    # basics
    g.w('org/k_basic', [HEAD, '# 0 emerging (30 t), 1 walking to the Heart, 2 at its range: an attack every 40 t (ranged 50 t) while',
                        f'# holding one of the {R["slots"]} slots.',
                        'execute if score @s apS matches 0 if score @s apT matches 30.. run scoreboard players set @s apS 1',
                        'execute if score @s apS matches 0 run return 0',
                        f'execute if score @s apS matches 1 run return run {F("org/b_walk")}',
                        F('org/b_attack')])
    g.w('org/b_walk', [f'execute if entity @s[tag=!rlk_mb_ap_rng] if entity {heart_near(3.4)} run return run {F("org/b_arrive")}',
                       f'execute if entity @s[tag=rlk_mb_ap_rng] if entity {heart_near(8.0)} run return run {F("org/b_arrive")}',
                       f'execute facing entity {HEART_M} feet rotated ~ 0 run {A.L.step_flat(SPEED["basic"])}'])
    g.w('org/b_arrive', ['scoreboard players set @s apS 2', 'scoreboard players set @s apT 0'])
    g.w('org/b_attack', [f'execute if score #apSlots mb matches {R["slots"]}.. run return 0', 'scoreboard players add #apSlots mb 1',
                         f'execute if entity @s[tag=!rlk_mb_ap_rng] if score @s apT matches ..{R["melee_every"] - 1} run return 0',
                         f'execute if entity @s[tag=rlk_mb_ap_rng] if score @s apT matches ..{R["ranged_every"] - 1} run return 0',
                         'scoreboard players set @s apT 0',
                         f'execute if entity @s[tag=rlk_mb_ap_buff] run return run function {A.NS}heart/sub {{v:{R["buffed_hit"]}}}',
                         f'function {A.NS}heart/sub {{v:{R["basic_hit"]}}}'])
    # 파괴
    g.w('org/k_destr', [HEAD, f'# 0 emerging (30 t), 1 rolling to the Heart ({R["destr_spd"]} b/t) until r 2.6, 2 the fuse ({R["destr_fuse"]} t) ->',
                        f'# the blast (-{R["destr_blast"]}, no progress).',
                        'execute if score @s apS matches 0 if score @s apT matches 30.. run scoreboard players set @s apS 1',
                        f'execute if score @s apS matches 1 if entity {heart_near(2.6)} run return run {F("org/b_arrive")}',
                        f'execute if score @s apS matches 1 facing entity {HEART_M} feet rotated ~ 0 run {A.L.step_flat(SPEED["destr"])}',
                        f'execute if score @s apS matches 2 if score @s apT matches {R["destr_fuse"]}.. run return run {F("org/d_blast")}'])
    g.w('org/d_blast', [f'function {A.NS}heart/sub {{v:{R["destr_blast"]}}}', Gen.sound('entity.generic.explode', 1.0, 1.2),
                        Gen.particle('explosion', n=1), F('org/remove')])
    # 양육
    imm_self = A.NURTURE_MODE == 'A'
    g.w('org/k_nurt', [HEAD, f'# Stationary; after its 20 t tell it links up to {R["nurt_links"]} basics within r 10 (tag rlk_mb_ap_buff);',
                       f'# NURTURE_MODE {A.NURTURE_MODE}: ' + ('itself immune (rlk_mb_ap_imm) while it holds a link.' if imm_self
                                                               else 'the buffed basics immune (rlk_mb_ap_imm).'),
                       'execute if score @s apT matches ..19 run return 0',
                       f'tag @e[type=minecraft:husk,tag=rlk_mb_ap_basic,distance=..10,limit={R["nurt_links"]},sort=nearest] add rlk_mb_ap_buff',
                       'tag @s remove rlk_mb_ap_imm' if imm_self else 'tag @e[type=minecraft:husk,tag=rlk_mb_ap_buff] add rlk_mb_ap_imm',
                       ('execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_buff,distance=..10,limit=1] run tag @s add rlk_mb_ap_imm'
                        if imm_self else '# (mode B: the 양육 itself is not immune)')])
    # kills and removal
    g.w('org/broke', [HEAD, '# @s = a broken organism (rlk_mb_broken from aux/take): the progress (+325 basic / +1400 others), the',
                      '# energy particles, removed.',
                      f'execute if score @s apK matches 1 run function {A.NS}heart/add {{v:{R["basic_kill"]}}}',
                      f'execute unless score @s apK matches 1 run function {A.NS}heart/add {{v:{R["kill"]}}}',
                      Gen.particle('happy_villager', '~ ~1 ~', (0.4, 0.4, 0.4), 0, 12), F('org/remove')])
    g.w('org/remove', ['# @s = an organism: its display, a 양육\'s links, itself (no rewards: aux kills pay none).',
                       'scoreboard players operation #apO mb = @s apOI',
                       'execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_om] if score @s apOI = #apO mb run kill @s',
                       f'execute if score @s apK matches {A.KIND_ID["nurt"]} run tag @e[type=minecraft:husk,tag=rlk_mb_ap_basic] remove rlk_mb_ap_buff',
                       f'execute if score @s apK matches {A.KIND_ID["nurt"]} run tag @e[type=minecraft:husk,tag=rlk_mb_ap_basic] remove rlk_mb_ap_imm',
                       'kill @s'])
    g.w('org/clear', [HEAD, '# Every organism and its displays (no progress; cleanup, CS, failure, death, phase jumps).',
                      'kill @e[tag=rlk_mb_ap_om]', f'kill {ORGS}', sc('#apSlots', 0)])
    g.w('org/freeze', [HEAD, '# Pause: the organisms are NoAI husks moved only by the module tick, which is off; nothing to do.',
                       sc('#apSlots', 0)])
    g.w('org/aux_hit', [HEAD, '# @s = an organism inside combat/apply (#dmg after RES): the shield pools (AP-REV) go here.',
                        'execute unless entity @s[tag=rlk_mb_ap_org] run return 0'])
    g.w('wall/clear', [HEAD, '# The nesting walls: the recorded blocks (AP-REV) and the safety sweep of the barrier band (FN-26).',
                       'kill @e[type=minecraft:marker,tag=rlk_mb_ap_wall]', 'kill @e[tag=rlk_mb_ap_wall_blade]',
                       f'function rlk:mboss/arena/{A.AID}/sweep {{y0:{A.ARENA["sweep"]["y0"]},y1:{A.ARENA["sweep"]["y1"]}}}'])
