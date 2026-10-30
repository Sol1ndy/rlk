"""Chapter-2 swarm mobs: ns 떠돌이 무사 졸개 · sl/ss 번개 슬라임 · sp 반란군 창병 · dr 오니 북잡이, and the group
spawners g_ns / g_sp / g_sl. Brains are the chapter-1 invisible husks (rlk_cmb, cmId, lure aggro); visuals are
item_display rigs (models from tools/build_ch2_swarm_rigs.mjs, poses from poses.py) owned by cmId.
"""
import math

import poses
import rig

HUSK = ('summon minecraft:husk ~ ~ ~ {{Tags:[{tags}],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Silent:1b,IsBaby:0b,'
        'CanPickUpLoot:0b,active_effects:[{{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}}],'
        'attributes:[{attrs}]}}')

HUMANOID = {
    'ns': {'parts': list(rig.LIMBS) + ['katana'], 'attach': poses.NS_ATTACH, 'poses': poses.NS, 'glow': ('katana',), 'h': 3.6},
    'sp': {'parts': list(rig.LIMBS) + ['yari', 'flag'], 'attach': poses.SP_ATTACH, 'poses': poses.SP, 'glow': ('yari',), 'h': 4.2},
    'dr': {'parts': list(rig.LIMBS) + ['stick_r', 'stick_l', 'taiko'], 'attach': poses.DR_ATTACH, 'poses': poses.DR, 'glow': (), 'h': 3.6},
}
SLIME_SIZE = {'sl': 1.35, 'ss': 0.62}


def part_summon(mob, part, model, root=False, glow=False, bright=False, h=3.6, ns='c2'):
    tags = ['rlk_room', 'rlk_pet', 'rlk_cmlink', f'rlk_{ns}pt', f'rlk_{mob}_pt', f'rlk_{mob}_{part}', f'rlk_{ns}new']
    if root:
        tags.append(f'rlk_{ns}root')
    if glow:
        tags.append(f'rlk_{ns}glow')
    tg = ','.join(f'"{t}"' for t in tags)
    br = 'brightness:{sky:15,block:15},' if bright else ''
    return (f'summon minecraft:item_display ~ ~ ~ {{Tags:[{tg}],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",'
            f'interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:3.6f,height:{h}f,shadow_radius:0f,{br}'
            f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"rlk:{model}",'
            f'"minecraft:custom_model_data":{{colors:[16777215]}}}}}}}}')


def rig_common(w, mob, parts_lines, n, pose_ids, face, pick, extra_tick=(), ns='c2'):
    """create / rebuild / check / tick / pose_m for one mob. parts_lines: summon lines; n = part count.
    ns: shared-code folder / tag family (rlk_<ns>pt · root · this · new · dying, storage rlk:<ns> p)."""
    new, this, root, dying = (f'rlk_{ns}{k}' for k in ('new', 'this', 'root', 'dying'))
    w(f'cm/{mob}/rig/create', '\n'.join([f'# {mob} 리그 {n}부품 (실행 위치 = 발, 모델 중심 [8,8,8]); 새 부품은 {this} 로 남김'] + parts_lines + [
        f'scoreboard players operation @e[tag={new}] cmId = #cid tmp',
        '# 새 부품은 이번 틱 정리(cm/clean)에서 살아남게 표시(분열 · 다시 만들기는 cm/clean 안에서도 일어남)',
        f'tag @e[tag={new}] add rlk_cmsync',
        f'tag @e[tag={new}] add {this}',
        f'tag @e[tag={new}] remove {new}',
        f'function rlk:cm/{mob}/rig/pose/0']))
    w(f'cm/{mob}/rig/check', '\n'.join([
        '# 48틱마다 부품 수 확인(리로드 · 청크 문제로 빠진 부품이 있으면 다시 만듦)',
        'scoreboard players set @s cmAF 0',
        f'execute store result score #c2cnt tmp if entity @e[tag={this}]',
        f'execute if score #c2cnt tmp matches {n} run return 0',
        f'kill @e[tag={this}]',
        f'function rlk:cm/{mob}/rig/create',
        'scoreboard players set @s cmAP -1']))
    w(f'cm/{mob}/rig/pose_m', f'$function rlk:cm/{mob}/rig/pose/$(n)')
    allowed = sorted(pose_ids)
    lines = [f'# {mob} 모습 한 틱 (@s = 두뇌, at @s; #cid = cmId). 내 뿌리 부품을 찾고, 나머지 부품은 뿌리와 같은 자리(모두 함께 옮김)에서만 찾음. 자세는 바뀔 때만 보냄(보간)',
             f'execute as @e[tag={root},tag=rlk_{mob}_pt,tag=!{dying},distance=..6] if score @s cmId = #cid tmp run tag @s add {this}',
             f'execute at @e[tag={this},limit=1] as @e[tag=rlk_{mob}_pt,tag=!{root},tag=!{dying},distance=..0.01] if score @s cmId = #cid tmp run tag @s add {this}',
             'scoreboard players add @s cmAF 1',
             f'execute if score @s cmAF matches 48.. run function rlk:cm/{mob}/rig/check',
             f'tag @e[tag={this}] add rlk_cmsync'] + list(face) + [
             f'execute if score @s cmAH matches 1 as @e[tag={this}] run data modify entity @s item.components."minecraft:custom_model_data" set value {{colors:[16777215]}}'] + list(extra_tick) + [
             f'execute if score @s frzT matches 1.. run return run function rlk:cm/{ns}/rig_frozen',
             f'function rlk:cm/{mob}/rig/pick',
             f'execute unless score @s cmAP = #pose tmp store result storage rlk:{ns} p.n int 1 run scoreboard players get #pose tmp',
             f'execute unless score @s cmAP = #pose tmp run function rlk:cm/{mob}/rig/pose_m with storage rlk:{ns} p',
             'scoreboard players operation @s cmAP = #pose tmp',
             'execute if score @s cmAR matches 1.. run scoreboard players remove @s cmAR 1',
             'execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1',
             f'tag @e[tag={this}] remove {this}']
    w(f'cm/{mob}/rig/tick', '\n'.join(lines))
    w(f'cm/{mob}/rig/pick', '\n'.join(pick))
    return allowed


FACE_AIM = ['execute facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_c2this] run tp @s ~ ~ ~ ~ 0']
FACE_YAW = ['execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw',
            'execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 as @e[tag=rlk_c2this] run tp @s ~ ~ ~ ~ 0']


def humanoid_rig(w, mob, face, pick, H=None, ns='c2', extra_tick=()):
    """H: {'parts', 'attach', 'poses', 'glow', 'h'} (default: this module's HUMANOID[mob]); models rlk:cm/<ns>/<mob>/<part>."""
    H = HUMANOID[mob] if H is None else H
    lines = [part_summon(mob, p, f'cm/{ns}/{mob}/{p}', root=(p == 'body'), glow=(p in H['glow']), bright=(p in H.get('bright', ())), h=H['h'], ns=ns)
             for p in H['parts']]
    for pid, (name, dur, prm) in sorted(H['poses'].items()):
        r = rig.humanoid(prm, H['attach'])
        rig.plant(r)
        w(f'cm/{mob}/rig/pose/{pid}', '\n'.join([f'# {name} ({dur}틱 보간)'] + [
            rig.merge_line(f'@e[tag=rlk_{ns}this,tag=rlk_{mob}_{p},limit=1]', r[p], dur) for p in H['parts']]))
    return rig_common(w, mob, lines, len(H['parts']), H['poses'].keys(), face, pick, extra_tick, ns=ns)


def slime_pose(S, sx, sy, sz, c, lift):
    body = {'t': [0, 0.5 * sy * S, 0], 'q': [0, 0, 0, 1], 's': [sx * S, sy * S, sz * S]}
    cs = c * S
    core = {'t': [0, 0.4375 * sy * S + lift * S + 0.125 * cs, 0], 'q': [0, 0, 0, 1], 's': [cs, cs, cs]}
    return body, core


def slime_rig(w, mob, pick, extra_tick):
    S = SLIME_SIZE[mob]
    lines = [part_summon(mob, 'body', 'cm/c2/slime/body', root=True, bright=True), part_summon(mob, 'core', 'cm/c2/slime/core', bright=True)]
    for pid, (name, dur, (sx, sy, sz, c, lift)) in sorted(poses.SLIME.items()):
        body, core = slime_pose(S, sx, sy, sz, c, lift)
        w(f'cm/{mob}/rig/pose/{pid}', '\n'.join([f'# {name} ({dur}틱 보간)',
                                                rig.merge_line(f'@e[tag=rlk_c2this,tag=rlk_{mob}_body,limit=1]', body, dur),
                                                rig.merge_line(f'@e[tag=rlk_c2this,tag=rlk_{mob}_core,limit=1]', core, dur)]))
    return rig_common(w, mob, lines, 2, poses.SLIME.keys(), FACE_AIM, pick, extra_tick)


def spawn_fn(w, mob, title, tags, attrs, ns='c2', zmob=True):
    base = ['rlk_room'] + (['rlk_zmob'] if zmob else []) + ['rlk_newmob', 'rlk_cmb', f'rlk_cm_{mob}', f'rlk_m_cm{mob}', 'rlk_cmnew', f'rlk_{ns}', f'rlk_{ns}a']
    tg = ','.join(f'"{t}"' for t in base + tags)
    at = ','.join(f'{{id:"minecraft:{k}",base:{v}d}}' for k, v in attrs)
    w(f'cm/spawn/{mob}', f'# {title} 한 마리 (실행 위치 · 방향): 투명 허스크 두뇌 + cmId 로 이은 디스플레이 리그\n'
                         + HUSK.format(tags=tg, attrs=at) + '\nfunction rlk:cm/c2/brain_end')


def group_slot(w, mob, off):
    """One group member at a local offset from the group origin, or at the origin when that spot is not standable."""
    pos = f'^{off[0]} ^ ^{off[1]}'
    return [f'scoreboard players set #c2ok tmp 0',
            f'execute positioned {pos} if function rlk:cm/c2/safe_here run scoreboard players set #c2ok tmp 1',
            f'execute if score #c2ok tmp matches 1 positioned {pos} run function rlk:cm/spawn/{mob}',
            f'execute if score #c2ok tmp matches 0 run function rlk:cm/spawn/{mob}']


def build(w):
    # ================================================================ 떠돌이 무사 졸개 (ns)
    spawn_fn(w, 'ns', '떠돌이 무사 졸개', [], [('movement_speed', 0.25)])
    w('cm/ns/init', '''
# 졸개 준비 (@s): 무리 번호(c2G) · 첫 마리가 무리장(rlk_ns_lead). 무리 소환(g_ns) 밖이면 혼자서 새 무리. 절반은 골드 · 회복 구슬 없음
execute unless score #c2InPack tmp matches 1 run scoreboard players add #c2PackC tmp 1
scoreboard players operation @s c2G = #c2PackC tmp
execute unless score #c2InPack tmp matches 1 run tag @s add rlk_ns_lead
execute if score #c2InPack tmp matches 1 unless score #c2PackLd tmp matches 1 run tag @s add rlk_ns_lead
execute if score #c2InPack tmp matches 1 run scoreboard players set #c2PackLd tmp 1
execute store result score @s cmCd run random value 10..24
execute store result score @s c2T run random value 1..5
execute store result score #c2r tmp run random value 0..1
execute if score #c2r tmp matches 1 run tag @s add rlk_c2lite
function rlk:cm/ns/rig/create
tag @e[tag=rlk_c2this] remove rlk_c2this
''')
    w('cm/ns/tick', '''
# 졸개 (@s = 두뇌, at @s): 무리장 곁(2.5칸)에 붙어 다니고, 한 마리라도 2.5칸 안이면 무리 전체가 함께 칼을 든다(0.6초) → 짧은 베기
execute if score @s cmS matches 1 run return run function rlk:cm/ns/wind
execute if score @s cmAR matches 3.. run scoreboard players set #hold tmp 1
execute if score #free tmp matches 1 if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..2.5] run return run function rlk:cm/ns/pack_go
scoreboard players remove @s c2T 1
execute if score @s c2T matches ..0 run function rlk:cm/ns/cohere
''')
    w('cm/ns/pack_go', '''
# 무리 공격 시작: 같은 무리(c2G)이고 몸에서 7칸 안, 쉬고 있고 경직 · 빙결이 아닌 졸개 모두
scoreboard players operation #g tmp = @s c2G
scoreboard players operation #c2cidS tmp = #cid tmp
execute at @e[tag=rlk_body,limit=1] as @e[tag=rlk_cm_ns,distance=..7] if score @s c2G = #g tmp if score @s cmS matches 0 unless score @s stunT matches 1.. unless score @s frzT matches 1.. at @s run function rlk:cm/ns/start
scoreboard players operation #cid tmp = #c2cidS tmp
''')
    w('cm/ns/start', f'''
scoreboard players set @s cmS 1
scoreboard players set @s cmAR 0
scoreboard players operation @s cmT = #c2W_ns tmp
tag @s add rlk_c2fresh
scoreboard players operation @s cmCd = #c2Cd_ns tmp
scoreboard players operation #cid tmp = @s cmId
execute as @e[tag=rlk_ns_katana,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {{Glowing:1b,glow_color_override:16775885}}
particle minecraft:electric_spark ~ ~2.0 ~ 0.25 0.3 0.25 0.05 6 normal
{w.snd('nsraise', 'minecraft:item.armor.equip_iron', 0.9, 0.6)}
{w.snd('nsglint', 'minecraft:block.amethyst_block.chime', 1.0, 1.7)}
''')
    w('cm/ns/wind', '''
# 칼을 든 채 선딜: 경직 · 빙결이면 취소. 시작한 틱에는 줄지 않음(무리 전체가 같은 틱에 벰). 가속 중이면 한 틱 더
scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/cancel
execute if entity @s[tag=rlk_c2fresh] run return 0
scoreboard players remove @s cmT 1
execute if score #c2X tmp matches 1 run scoreboard players remove @s cmT 1
execute if score @s cmT matches 4..8 run particle minecraft:end_rod ~ ~2.15 ~ 0.12 0.12 0.12 0.01 1 normal
execute if score @s cmT matches ..0 run function rlk:cm/ns/strike
''')
    w('cm/ns/strike', f'''
scoreboard players set @s cmS 0
scoreboard players set @s cmAR 8
execute as @e[tag=rlk_ns_katana,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {{Glowing:0b}}
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^1.1 ^1.1 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1 normal
{w.snd('nsslash', 'minecraft:entity.player.attack.sweep', 0.9, 1.15)}
execute if score #c2NsHit tmp matches 0 if entity @e[tag=rlk_body,distance=..3.0] run function rlk:cm/ns/hit
''')
    w('cm/ns/hit', '''
# 무리 베기는 한 틱에 한 번만 맞힘(여러 마리가 같은 틱에 베도 15 한 번)
scoreboard players set #c2NsHit tmp 1
scoreboard players operation #cmDmg tmp = #c2D_ns tmp
function rlk:cm/hit_me
''')
    w('cm/ns/cohere', '''
# 5틱마다: 무리장을 찾고(없으면 내가 무리장), 2.6칸보다 멀면 무리장 쪽으로 끌림
scoreboard players set @s c2T 5
scoreboard players operation #g tmp = @s c2G
execute as @e[tag=rlk_ns_lead,distance=..24] if score @s c2G = #g tmp run tag @s add rlk_c2ld
execute unless entity @e[tag=rlk_c2ld,limit=1] run tag @s add rlk_ns_lead
execute if entity @s[tag=rlk_ns_lead] run return run tag @e[tag=rlk_c2ld] remove rlk_c2ld
scoreboard players set #c2Fw tmp 230
scoreboard players set #c2Up tmp -1
execute unless entity @e[tag=rlk_c2ld,distance=..2.6] facing entity @e[tag=rlk_c2ld,limit=1,sort=nearest] feet rotated ~ 0 run function rlk:cm/c2/impulse
tag @e[tag=rlk_c2ld] remove rlk_c2ld
''')
    walk8 = ['scoreboard players operation #pose tmp = @s cmAF', 'scoreboard players operation #pose tmp %= #c2c24 tmp',
             'scoreboard players operation #pose tmp /= #c2c3 tmp', 'scoreboard players add #pose tmp 10']
    w('cm/c2/walk8', '\n'.join(walk8))
    idle4 = ['scoreboard players operation #pose tmp = @s cmAF', 'scoreboard players operation #pose tmp /= #c2c12 tmp',
             'execute unless entity @s[tag=rlk_cmhold] unless entity @e[tag=rlk_body,distance=..2.3] run function rlk:cm/c2/walk8']
    humanoid_rig(w, 'ns', FACE_AIM, idle4 + [
        'execute if score @s cmAR matches 7.. run scoreboard players set #pose tmp 24',
        'execute if score @s cmAR matches 4..6 run scoreboard players set #pose tmp 30',
        'execute if score @s cmAR matches 1..3 run scoreboard players set #pose tmp 31',
        'execute if score @s cmS matches 1 if score @s cmT matches 10.. run scoreboard players set #pose tmp 20',
        'execute if score @s cmS matches 1 if score @s cmT matches 3..9 run scoreboard players set #pose tmp 21',
        'execute if score @s cmS matches 1 if score @s cmT matches 2 run scoreboard players set #pose tmp 22',
        'execute if score @s cmS matches 1 if score @s cmT matches ..1 run scoreboard players set #pose tmp 23',
        'execute if score @s cmAH matches 4.. run scoreboard players set #pose tmp 40',
        'execute if score @s cmAH matches 1..3 run scoreboard players set #pose tmp 41'])
    w('cm/ns/rig/die', 'function rlk:cm/ns/rig/pose/50')
    w('cm/ns/rig/fling', 'function rlk:cm/ns/rig/pose/51')

    # ================================================================ 번개 슬라임 (sl) / 작은 번개 슬라임 (ss)
    spawn_fn(w, 'sl', '번개 슬라임', ['rlk_c2slime'], [('scale', 0.8), ('movement_speed', 0.14)])
    spawn_fn(w, 'ss', '작은 번개 슬라임', ['rlk_c2slime', 'rlk_c2lite'], [('scale', 0.5), ('movement_speed', 0.2)])
    for mob, hop0 in (('sl', '6..20'), ('ss', '3..10')):
        w(f'cm/{mob}/init', f'''
execute store result score @s c2T run random value {hop0}
scoreboard players set @s c2T2 0
execute store result score @s cmCd run random value 16..30
function rlk:cm/{mob}/rig/create
tag @e[tag=rlk_c2this] remove rlk_c2this
''')
    w('cm/sl/tick', '''
# 번개 슬라임 (@s, at @s): 몸 쪽으로 깡충 뛰어 옴. 3.2칸 안이면 0.5초 웅크림(예고) → 몸통 박치기(12, 번개)
execute if score @s cmS matches 1 run return run function rlk:cm/sl/crouch
execute if score @s cmS matches 2 run return run function rlk:cm/sl/air
scoreboard players remove @s c2T 1
execute if score #c2X tmp matches 1 run scoreboard players remove @s c2T 1
execute if score #free tmp matches 1 if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..3.2] run return run function rlk:cm/sl/start
execute if score #free tmp matches 1 if score @s c2T matches ..0 run function rlk:cm/sl/hop
''')
    for mob, hop, fw, up, key, snd_id, vol, pitch in (('sl', 'c2Hop_sl', 260, 400, 'sljump', 'minecraft:entity.slime.jump', 0.6, 0.8),
                                                      ('ss', 'c2Hop_ss', 330, 330, 'ssjump', 'minecraft:entity.slime.jump_small', 0.5, 1.2)):
        w(f'cm/{mob}/hop', f'''
# 깡충 (땅에 있을 때만): 몸 쪽으로 {fw / 1000} 칸/틱, 위로 {up / 1000}
scoreboard players operation @s c2T = #{hop} tmp
execute unless data entity @s {{OnGround:1b}} run return 0
scoreboard players set @s c2T2 8
scoreboard players set #c2Fw tmp {fw}
scoreboard players set #c2Up tmp {up}
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:cm/c2/impulse
{w.snd(key, snd_id, vol, pitch)}
''')
    w('cm/sl/start', f'''
scoreboard players set @s cmS 1
scoreboard players operation @s cmT = #c2W_sl tmp
scoreboard players operation @s cmCd = #c2Cd_sl tmp
particle minecraft:electric_spark ~ ~0.6 ~ 0.5 0.3 0.5 0.1 12 normal
{w.snd('slsquish', 'minecraft:entity.slime.squish', 0.9, 0.6)}
{w.snd('slcharge', 'minecraft:block.respawn_anchor.charge', 0.5, 1.6)}
''')
    w('cm/sl/crouch', '''
# 웅크림(예고): 경직 · 빙결이면 취소
scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/cancel
scoreboard players remove @s cmT 1
execute if score #c2X tmp matches 1 run scoreboard players remove @s cmT 1
execute if score @s cmT matches 1.. run particle minecraft:electric_spark ~ ~0.4 ~ 0.45 0.1 0.45 0.05 2 normal
execute if score @s cmT matches ..0 run function rlk:cm/sl/leap
''')
    w('cm/sl/leap', f'''
# 몸이 있던 쪽으로 도약(방향은 이 순간 고정)
scoreboard players set @s cmS 2
scoreboard players set @s cmT 9
scoreboard players set #c2Fw tmp 520
scoreboard players set #c2Up tmp 420
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:cm/c2/impulse
{w.snd('slleap', 'minecraft:entity.slime.jump', 1.0, 0.6)}
''')
    w('cm/sl/air', '''
scoreboard players remove @s cmT 1
execute if score @s cmT matches ..0 run function rlk:cm/sl/land
''')
    w('cm/sl/land', f'''
# 착지: 반경 1.9 안의 몸에 12(번개)
scoreboard players set @s cmS 0
scoreboard players set @s cmAR 6
particle minecraft:electric_spark ~ ~0.2 ~ 1.2 0.1 1.2 0.25 30 normal
particle minecraft:item_slime ~ ~0.3 ~ 0.8 0.2 0.8 0.1 16 normal
{w.snd('slland', 'minecraft:entity.slime.squish', 1.0, 0.5)}
{w.snd('slzap', 'minecraft:entity.lightning_bolt.impact', 0.35, 1.7)}
execute if entity @e[tag=rlk_body,distance=..1.9] run function rlk:cm/sl/hit
''')
    w('cm/sl/hit', 'scoreboard players operation #cmDmg tmp = #c2D_sl tmp\nfunction rlk:cm/c2/hit_el')
    w('cm/ss/tick', '''
# 작은 번개 슬라임 (@s, at @s): 빠르게 뛰어 와 1.7칸 안에서 달라붙음 → 바닥 고리(반경 1.5) 1초 → 작은 감전(6, 번개)
execute if score @s cmS matches 1 run return run function rlk:cm/ss/latch
scoreboard players remove @s c2T 1
execute if score #c2X tmp matches 1 run scoreboard players remove @s c2T 1
execute if score #free tmp matches 1 if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..1.7] if data entity @s {OnGround:1b} run return run function rlk:cm/ss/start
execute if score #free tmp matches 1 if score @s c2T matches ..0 run function rlk:cm/ss/hop
''')
    w('cm/ss/start', f'''
scoreboard players set @s cmS 1
scoreboard players operation @s cmT = #c2W_ss tmp
scoreboard players operation @s cmCd = #c2Cd_ss tmp
summon minecraft:item_display ~ ~0.06 ~ {{Tags:["rlk_room","rlk_pet","rlk_cmlink","rlk_c2ring","rlk_c2new"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",teleport_duration:1,view_range:1.5f,width:3.2f,height:0.3f,shadow_radius:0f,brightness:{{sky:15,block:15}},transformation:{{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,1f,3f],right_rotation:[0f,0f,0f,1f]}},item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"rlk:cm/c2/fx/ring","minecraft:custom_model_data":{{colors:[16777215]}}}}}}}}
scoreboard players operation @e[tag=rlk_c2new] cmId = @s cmId
tag @e[tag=rlk_c2new] add rlk_cmsync
tag @e[tag=rlk_c2new] remove rlk_c2new
{w.snd('sslatch', 'minecraft:entity.slime.squish_small', 1.0, 1.4)}
{w.snd('sshum', 'minecraft:block.amethyst_block.resonate', 0.8, 1.8)}
''')
    w('cm/ss/latch', '''
# 달라붙음(예고 1초, 바닥 고리가 따라옴): 경직 · 빙결이면 취소. 마지막 6틱은 고리가 번쩍
scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/cancel
scoreboard players remove @s cmT 1
execute if score #c2X tmp matches 1 run scoreboard players remove @s cmT 1
execute as @e[tag=rlk_c2ring,distance=..4] if score @s cmId = #cid tmp run function rlk:cm/ss/ring_keep
execute if score @s cmT matches 1.. run particle minecraft:electric_spark ~ ~0.3 ~ 0.3 0.2 0.3 0.05 1 normal
execute if score @s cmT matches 6 as @e[tag=rlk_c2ring,distance=..4] if score @s cmId = #cid tmp run data merge entity @s {Glowing:1b,glow_color_override:13404415}
execute if score @s cmT matches ..0 run function rlk:cm/ss/shock
''')
    w('cm/ss/ring_keep', 'tp @s ~ ~0.06 ~\ntag @s add rlk_cmsync')
    w('cm/ss/shock', f'''
# 감전: 반경 1.5 안의 몸에 6(번개)
scoreboard players set @s cmS 0
scoreboard players set @s cmAR 4
scoreboard players set @s c2T 14
execute as @e[tag=rlk_c2ring,distance=..4] if score @s cmId = #cid tmp run kill @s
particle minecraft:electric_spark ~ ~0.3 ~ 0.9 0.2 0.9 0.3 30 normal
particle minecraft:end_rod ~ ~0.3 ~ 0.6 0.1 0.6 0.05 8 normal
{w.snd('ssshock', 'minecraft:block.amethyst_cluster.break', 0.9, 1.3)}
{w.snd('sszap', 'minecraft:entity.lightning_bolt.impact', 0.25, 2.0)}
execute if entity @e[tag=rlk_body,distance=..1.5] run function rlk:cm/ss/hit
''')
    w('cm/ss/hit', 'scoreboard players operation #cmDmg tmp = #c2D_ss tmp\nfunction rlk:cm/c2/hit_el')
    for mob in ('sl', 'ss'):
        pick = ['scoreboard players operation #pose tmp = @s cmAF', 'scoreboard players operation #pose tmp /= #c2c12 tmp',
                'scoreboard players operation #pose tmp %= #c2c2 tmp',
                'execute if score @s c2T2 matches 7.. run scoreboard players set #pose tmp 7',
                'execute if score @s c2T2 matches 3..6 run scoreboard players set #pose tmp 6',
                'execute if score @s c2T2 matches 1..2 run scoreboard players set #pose tmp 7',
                'execute if score @s cmAR matches 1.. run scoreboard players set #pose tmp 7',
                'execute if score @s cmS matches 1 run scoreboard players set #pose tmp 5',
                'execute if score @s cmS matches 2 run scoreboard players set #pose tmp 6',
                'execute if score @s cmAH matches 3.. run scoreboard players set #pose tmp 40',
                'execute if score @s c2T2 matches 1.. run scoreboard players remove @s c2T2 1']
        keep = [f'execute if score @s c2Age matches 2 as @e[tag=rlk_c2this,tag=rlk_c2root] run scoreboard players operation @s mlv = #clv tmp']
        slime_rig(w, mob, pick, keep)
        w(f'cm/{mob}/rig/fling', f'function rlk:cm/{mob}/rig/pose/51')
    w('cm/sl/rig/die', f'''
# 큰 슬라임 터짐 (@s = 뿌리): 부풀고 → 2칸 안의 다른 슬라임에 방전 → 작은 슬라임 셋으로 분열
function rlk:cm/sl/rig/pose/50
{w.snd('sldeath', 'minecraft:entity.slime.death', 1.0, 0.8)}
function rlk:cm/c2/discharge
function rlk:cm/sl/split
''')
    w('cm/ss/rig/die', f'''
function rlk:cm/ss/rig/pose/50
{w.snd('ssdeath', 'minecraft:entity.slime.death_small', 1.0, 1.2)}
function rlk:cm/c2/discharge
''')
    w('cm/sl/keep_lv', '''
# 죽는 큰 슬라임(@s)의 레벨을 리그 뿌리에 남김(분열한 작은 슬라임이 같은 레벨)
scoreboard players operation #c2kid tmp = @s cmId
scoreboard players operation #c2klv tmp = @s mlv
execute as @e[tag=rlk_sl_body,distance=..6] if score @s cmId = #c2kid tmp run scoreboard players operation @s mlv = #c2klv tmp
''')
    w('cm/sl/split', '''
# 분열 (@s = 뿌리, 몸 쪽을 봄): 0°/120°/240° 방향 0.5칸(설 수 없으면 제자리)에 작은 슬라임, 살짝 바깥으로 튕김(서로 2칸 안 → 연쇄 방전)
scoreboard players set #c2PLv tmp 0
execute if score @s mlv matches 1.. run scoreboard players operation #c2PLv tmp = @s mlv
execute rotated ~ 0 run function rlk:cm/sl/kid
execute rotated ~120 0 run function rlk:cm/sl/kid
execute rotated ~240 0 run function rlk:cm/sl/kid
''')
    w('cm/sl/kid', '\n'.join(group_slot(w, 'ss', (0, 0.5)) + ['execute as @e[tag=rlk_newmob,tag=rlk_cm_ss] run function rlk:cm/sl/kid_go']))
    w('cm/sl/kid_go', '''
function rlk:cm/c2/child_init
scoreboard players set @s cmCd 24
scoreboard players set @s c2T 14
scoreboard players set #c2Fw tmp 120
scoreboard players set #c2Up tmp 300
function rlk:cm/c2/impulse
''')

    # ================================================================ 반란군 창병 (sp)
    spawn_fn(w, 'sp', '반란군 창병', [], [('movement_speed', 0.2)])
    w('cm/sp/init', '''
# 창병 준비 (@s): 대열 번호(c2G) · 자리(c2R 0 왼쪽 1 가운데 2 오른쪽), 바라보는 방향 = 소환 방향
execute unless score #c2InPack tmp matches 1 run scoreboard players add #c2PackC tmp 1
scoreboard players operation @s c2G = #c2PackC tmp
scoreboard players set @s c2R 1
execute if score #c2InPack tmp matches 1 run scoreboard players operation @s c2R = #c2Slot tmp
execute store result score @s cmYaw run data get entity @s Rotation[0] 100
execute store result score @s cmCd run random value 20..40
scoreboard players set @s c2T 4
function rlk:cm/sp/rig/create
tag @e[tag=rlk_c2this] remove rlk_c2this
''')
    w('cm/sp/tick', '''
# 창병 (@s, at @s): 초당 90°로만 돌아섬. 앞(±45°) 4.2칸 안이면 대열 전체가 1초 창끝 빛 → 2칸 찌르며 돌진(16)
execute if score @s cmS matches 1 run return run function rlk:cm/sp/wind
execute if score @s cmS matches 2 run return run function rlk:cm/sp/thrust
function rlk:cm/sp/turn
execute if score @s cmAR matches 1.. run scoreboard players set #hold tmp 1
execute if score #free tmp matches 1 if score @s cmCd matches ..0 if score @s cmAR matches ..0 if score #c2yd tmp matches -4500..4500 if entity @e[tag=rlk_body,distance=..4.2] run return run function rlk:cm/sp/line_go
scoreboard players remove @s c2T 1
execute if score @s c2T matches ..0 run function rlk:cm/sp/form
''')
    w('cm/sp/turn', '''
# cmYaw 를 몸 쪽으로 최대 #c2Turn(0.01°/틱) = 초당 90°. #c2yd = 돌기 전의 차이
execute facing entity @e[tag=rlk_body,limit=1] feet run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0
execute store result score #yd tmp run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100
scoreboard players operation #yd tmp -= @s cmYaw
execute if score #yd tmp matches 18001.. run scoreboard players remove #yd tmp 36000
execute if score #yd tmp matches ..-18001 run scoreboard players add #yd tmp 36000
scoreboard players operation #c2yd tmp = #yd tmp
scoreboard players operation #yd tmp < #c2Turn tmp
scoreboard players operation #yd tmp > #c2TurnN tmp
scoreboard players operation @s cmYaw += #yd tmp
execute if score @s cmYaw matches 18001.. run scoreboard players remove @s cmYaw 36000
execute if score @s cmYaw matches ..-18001 run scoreboard players add @s cmYaw 36000
''')
    w('cm/sp/line_go', '''
# 대열 공격 시작: 같은 대열(c2G)로 8칸 안, 쉬고 있고 경직 · 빙결이 아닌 창병 모두 (각자 지금 바라보는 쪽으로)
scoreboard players operation #g tmp = @s c2G
scoreboard players operation #c2cidS tmp = #cid tmp
execute as @e[tag=rlk_cm_sp,distance=..8] if score @s c2G = #g tmp if score @s cmS matches 0 if score @s cmAR matches ..0 unless score @s stunT matches 1.. unless score @s frzT matches 1.. at @s run function rlk:cm/sp/start
scoreboard players operation #cid tmp = #c2cidS tmp
''')
    w('cm/sp/start', f'''
scoreboard players set @s cmS 1
scoreboard players operation @s cmT = #c2W_sp tmp
tag @s add rlk_c2fresh
scoreboard players operation @s cmCd = #c2Cd_sp tmp
scoreboard players operation #cid tmp = @s cmId
execute as @e[tag=rlk_sp_yari,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {{Glowing:1b,glow_color_override:16772710,brightness:{{sky:15,block:15}}}}
{w.snd('spready', 'minecraft:entity.evoker.prepare_attack', 0.6, 1.4)}
{w.snd('spglint', 'minecraft:block.amethyst_block.chime', 1.0, 1.2)}
''')
    w('cm/sp/wind', '''
# 창끝 빛(1초): 방향 고정, 경직 · 빙결이면 취소
scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/cancel
execute if entity @s[tag=rlk_c2fresh] run return 0
scoreboard players remove @s cmT 1
execute if score #c2X tmp matches 1 run scoreboard players remove @s cmT 1
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^-0.25 ^1.15 ^1.55 run particle minecraft:electric_spark ~ ~ ~ 0.04 0.04 0.04 0.02 1 normal
execute if score @s cmT matches ..0 run function rlk:cm/sp/go
''')
    w('cm/sp/go', f'''
scoreboard players set @s cmS 2
scoreboard players set @s cmT 4
scoreboard players set @s c2T2 0
tag @s add rlk_cmch
{w.snd('spthrust', 'minecraft:item.trident.throw', 1.0, 0.8)}
''')
    w('cm/sp/thrust', '''
# 찌르며 돌진 4틱(0.5칸/틱 = 2칸, 블록은 바닐라 물리로 막힘). 창끝 둘레(1.6칸 앞 r1.3 · 2.6칸 앞 r1.0)에 몸이 있으면 16, 창병 한 마리당 한 번 · 대열 전체로 한 틱 한 번
scoreboard players set #hold tmp 1
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
scoreboard players set #c2Fw tmp 500
scoreboard players set #c2Up tmp -1
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 run function rlk:cm/c2/impulse
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^1.2 ^2.0 run particle minecraft:crit ~ ~ ~ 0.25 0.05 0.25 0.1 3 normal
execute if score @s c2T2 matches 0 if score #c2SpHit tmp matches 0 rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^ ^1.6 if entity @e[tag=rlk_body,distance=..1.3] run function rlk:cm/sp/hit
execute if score @s c2T2 matches 0 if score #c2SpHit tmp matches 0 rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^ ^2.6 if entity @e[tag=rlk_body,distance=..1.0] run function rlk:cm/sp/hit
scoreboard players remove @s cmT 1
execute if score @s cmT matches ..0 run function rlk:cm/sp/end
''')
    w('cm/sp/hit', '''
scoreboard players set @s c2T2 1
scoreboard players set #c2SpHit tmp 1
scoreboard players operation #cmDmg tmp = #c2D_sp tmp
function rlk:cm/hit_me
''')
    w('cm/sp/end', '''
scoreboard players set @s cmS 0
scoreboard players set @s cmAR 12
tag @s remove rlk_cmch
execute as @e[tag=rlk_sp_yari,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:0b,brightness:{sky:0,block:0}}
''')
    w('cm/sp/form', '''
# 4틱마다 대열 유지: 가운데(c2R 1)의 방향 기준 왼쪽(^1.7)/오른쪽(^-1.7) 자리로 끌림. 가운데가 없으면 내가 가운데
scoreboard players set @s c2T 4
execute if score @s c2R matches 1 run return 0
scoreboard players operation #g tmp = @s c2G
execute as @e[tag=rlk_cm_sp,distance=..12] if score @s c2G = #g tmp if score @s c2R matches 1 run tag @s add rlk_c2ld
execute unless entity @e[tag=rlk_c2ld,limit=1] run return run scoreboard players set @s c2R 1
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @e[tag=rlk_c2ld,limit=1] cmYaw
scoreboard players set #c2Fw tmp 180
scoreboard players set #c2Up tmp -1
execute if score @s c2R matches 0 at @e[tag=rlk_c2ld,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^1.7 ^ ^ unless entity @s[distance=..0.8] facing entity @s feet rotated ~180 0 run function rlk:cm/c2/impulse
execute if score @s c2R matches 2 at @e[tag=rlk_c2ld,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^-1.7 ^ ^ unless entity @s[distance=..0.8] facing entity @s feet rotated ~180 0 run function rlk:cm/c2/impulse
tag @e[tag=rlk_c2ld] remove rlk_c2ld
''')
    humanoid_rig(w, 'sp', FACE_YAW, idle4 + [
        'execute if score @s cmAR matches 9.. run scoreboard players set #pose tmp 25',
        'execute if score @s cmAR matches 5..8 run scoreboard players set #pose tmp 30',
        'execute if score @s cmAR matches 1..4 run scoreboard players set #pose tmp 31',
        'execute if score @s cmS matches 1 if score @s cmT matches 15.. run scoreboard players set #pose tmp 20',
        'execute if score @s cmS matches 1 if score @s cmT matches ..14 run scoreboard players set #pose tmp 21',
        'execute if score @s cmS matches 2 if score @s cmT matches 4.. run scoreboard players set #pose tmp 24',
        'execute if score @s cmS matches 2 if score @s cmT matches ..3 run scoreboard players set #pose tmp 25',
        'execute if score @s cmAH matches 4.. run scoreboard players set #pose tmp 40',
        'execute if score @s cmAH matches 1..3 run scoreboard players set #pose tmp 41'])
    w('cm/sp/rig/die', 'function rlk:cm/sp/rig/pose/50')
    w('cm/sp/rig/fling', 'function rlk:cm/sp/rig/pose/51')

    # ================================================================ 오니 북잡이 (dr)
    spawn_fn(w, 'dr', '오니 북잡이', [], [('movement_speed', 0.1)])
    w('cm/dr/init', '''
scoreboard players set @s c2T 10
scoreboard players set @s c2T2 0
function rlk:cm/dr/rig/create
tag @e[tag=rlk_c2this] remove rlk_c2this
''')
    w('cm/dr/tick', '''
# 북잡이 (@s, at @s): 제자리. 북을 치는 동안(rlk_dr_drum) 10칸 안의 커스텀 몹이 빨라짐(cm/c2/world). 맞으면 2초 멈춤
scoreboard players set #hold tmp 1
execute if score @s c2T2 matches 1.. run return run function rlk:cm/dr/stopped
execute if score #free tmp matches 0 run return run tag @s remove rlk_dr_drum
tag @s add rlk_dr_drum
scoreboard players add @s c2T 1
execute if score @s c2T matches 16.. run scoreboard players set @s c2T 0
execute if score @s c2T matches 0 run function rlk:cm/dr/beat
execute if score @s c2T matches 8 run function rlk:cm/dr/beat
''')
    w('cm/dr/beat', f'''
# 북 한 번: 둥 소리 + 노란 파동
{w.snd('drbeat', 'minecraft:block.note_block.basedrum', 1.6, 0.6)}
{w.snd('drbeat2', 'minecraft:block.note_block.bass', 0.8, 0.5)}
execute rotated ~ 0 positioned ^ ^1.0 ^0.9 run particle minecraft:dust{{color:[1.0,0.82,0.18],scale:1.6}} ~ ~ ~ 0.6 0.4 0.6 0 10 normal
execute rotated ~ 0 positioned ^ ^1.0 ^0.9 run particle minecraft:electric_spark ~ ~ ~ 0.4 0.3 0.4 0.15 4 normal
''')
    w('cm/dr/stopped', '''
tag @s remove rlk_dr_drum
scoreboard players remove @s c2T2 1
execute if score @s c2T2 matches 0 run scoreboard players set @s c2T 15
''')
    w('cm/dr/interrupt', f'''
# 맞으면 북 멈춤 #c2DrI 틱(2초). 가속은 다음 c2/world 에서 바로 풀림
scoreboard players operation @s c2T2 = #c2DrI tmp
tag @s remove rlk_dr_drum
{w.snd('drstop', 'minecraft:block.note_block.snare', 1.0, 0.5)}
''')
    humanoid_rig(w, 'dr', FACE_AIM, [
        'scoreboard players operation #pose tmp = @s cmAF', 'scoreboard players operation #pose tmp /= #c2c12 tmp',
        'execute if entity @s[tag=rlk_dr_drum] if score @s c2T matches 0..1 run scoreboard players set #pose tmp 61',
        'execute if entity @s[tag=rlk_dr_drum] if score @s c2T matches 2..7 run scoreboard players set #pose tmp 62',
        'execute if entity @s[tag=rlk_dr_drum] if score @s c2T matches 8..9 run scoreboard players set #pose tmp 63',
        'execute if entity @s[tag=rlk_dr_drum] if score @s c2T matches 10.. run scoreboard players set #pose tmp 60',
        'execute if score @s c2T2 matches 1.. run scoreboard players set #pose tmp 70',
        'execute if score @s cmAH matches 4.. run scoreboard players set #pose tmp 40'])
    w('cm/dr/rig/die', '# 북은 제자리에 남고(rlk_c2still) 북잡이만 날아감\nfunction rlk:cm/dr/rig/pose/50\ntag @e[tag=rlk_c2this,tag=rlk_dr_taiko] add rlk_c2still')
    w('cm/dr/rig/fling', 'function rlk:cm/dr/rig/pose/51')

    # ================================================================ groups
    gns = ['# 졸개 무리 4~6 (실행 위치 = 무리장, 실행 방향 = 앞). 방 배치는 #c2Size, 시험(cm/test)은 무작위',
           'execute unless score #c2SizeSet tmp matches 1 store result score #c2Size tmp run random value 4..6',
           'scoreboard players add #c2PackC tmp 1', 'scoreboard players set #c2InPack tmp 1', 'scoreboard players set #c2PackLd tmp 0',
           'function rlk:cm/spawn/ns']
    for k, off in enumerate([(1.5, 0.5), (-1.5, 0.5), (0.8, -1.3), (-0.8, -1.3), (0, 1.6)]):
        n = k + 2
        body = group_slot(w, 'ns', off)
        if n > 4:
            body = [l.replace('execute ', f'execute if score #c2Size tmp matches {n}.. ', 1) if l.startswith('execute') else
                    l for l in body]
            body = [f'execute if score #c2Size tmp matches {n}.. run ' + l if l.startswith('scoreboard') else l for l in body]
        gns += body
    gns.append('scoreboard players set #c2InPack tmp 0')
    w('cm/spawn/g_ns', '\n'.join(gns))
    gsp = ['# 창병 대열 3 (실행 위치 = 가운데, 실행 방향 = 앞): 왼쪽 ^1.6 · 가운데 · 오른쪽 ^-1.6',
           'scoreboard players add #c2PackC tmp 1', 'scoreboard players set #c2InPack tmp 1',
           'scoreboard players set #c2Slot tmp 1', 'function rlk:cm/spawn/sp', 'scoreboard players set #c2Slot tmp 0']
    gsp += group_slot(w, 'sp', (1.6, 0))
    gsp += ['scoreboard players set #c2Slot tmp 2'] + group_slot(w, 'sp', (-1.6, 0)) + ['scoreboard players set #c2InPack tmp 0']
    w('cm/spawn/g_sp', '\n'.join(gsp))
    gsl = ['# 번개 슬라임 2~3 (실행 위치 · 방향). 방 배치는 #c2Size, 시험은 무작위',
           'execute unless score #c2SizeSet tmp matches 1 store result score #c2Size tmp run random value 2..3',
           'function rlk:cm/spawn/sl'] + group_slot(w, 'sl', (1.8, 0))
    gsl += [('execute if score #c2Size tmp matches 3.. run ' + l) if l.startswith('scoreboard') else l.replace('execute ', 'execute if score #c2Size tmp matches 3.. ', 1)
            for l in group_slot(w, 'sl', (-1.8, -0.4))]
    w('cm/spawn/g_sl', '\n'.join(gsl))
