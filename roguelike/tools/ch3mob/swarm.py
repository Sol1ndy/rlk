"""Chapter-3 swarm mobs + healer (part A): fu 둥실 버섯 (+ fp 포자 주머니), em 에르미타 단검 용병, sb 모래 전갈 새끼,
cw 에르미타 맑은물 술사, and the group spawners g_fu / g_em / g_sb.

Brains are the chapter-1 invisible husks (rlk_cmb, cmId, lure aggro); visuals are item_display rigs owned by cmId,
built with the chapter-2 rig helpers (ch2mob/swarm.py, ns 'c3': parts rlk_c3pt, root rlk_c3root). Models / skins:
tools/build_ch3_swarm_rigs.mjs (rlk:cm/c3/*). Keyframes: tools/ch3mob/poses.py.
"""
import rig  # ch2mob/rig.py (quaternions, humanoid joints, merge lines)

from ch2mob import swarm as s2
from ch3mob import poses

NS = 'c3'
HUMANOID = {
    'em': {'parts': list(rig.LIMBS) + ['dagger_r', 'dagger_l', 'cloak'], 'attach': poses.EM_ATTACH, 'poses': poses.EM,
           'glow': ('dagger_r', 'dagger_l'), 'h': 3.6},
    'cw': {'parts': list(rig.LIMBS) + ['robe', 'orb'], 'attach': poses.CW_ATTACH, 'poses': poses.CW, 'glow': ('orb',), 'bright': ('orb',), 'h': 3.6},
}
PROP = {  # prop rigs: parts (first = root), bright parts, glow (outline-capable) parts, poses
    'fu': (('stem', 'cap', 'glow'), ('glow',), ('glow',), poses.FU),
    'sb': (('body', 'tail', 'mound'), (), (), poses.SB),
}
PARTS = {m: len(HUMANOID[m]['parts']) for m in HUMANOID}
PARTS.update({m: len(PROP[m][0]) for m in PROP})
FACE_AIM = [l.replace('rlk_c2this', f'rlk_{NS}this') for l in s2.FACE_AIM]   # displays face the body's chest
POD_PARTS = ('pod', 'glow')


def _tqs(spec):
    t, e, s = spec
    return {'t': list(t), 'q': rig.q(e) if len(e) == 3 else list(e), 's': list(s)}


def prop_rig(w, mob, pick, extra_tick=()):
    parts, bright, glow, P = PROP[mob]
    lines = [s2.part_summon(mob, p, f'cm/{NS}/{mob}/{p}', root=(k == 0), glow=(p in glow), bright=(p in bright), h=2.0, ns=NS)
             for k, p in enumerate(parts)]
    for pid, (name, dur, spec) in sorted(P.items()):
        w(f'cm/{mob}/rig/pose/{pid}', '\n'.join([f'# {name} ({dur}틱 보간)'] + [
            rig.merge_line(f'@e[tag=rlk_{NS}this,tag=rlk_{mob}_{p},limit=1]', _tqs(spec[p]), dur) for p in parts]))
    return s2.rig_common(w, mob, lines, len(parts), P.keys(), FACE_AIM, pick, extra_tick, ns=NS)


def group_slot(mob, off):
    return s2.group_slot(None, mob, off)


def common_init(mob, lines=()):
    """Group bookkeeping shared by the pack mobs: group id c2G (the chapter-2 counter, so ids never clash), slot c2R,
    group size c3N; outside a group spawner the mob is a group of one."""
    return '\n'.join([
        'execute unless score #c3InPack tmp matches 1 run scoreboard players add #c2PackC tmp 1',
        'scoreboard players operation @s c2G = #c2PackC tmp',
        'scoreboard players set @s c2R 0',
        'scoreboard players set @s c3N 1',
        'execute if score #c3InPack tmp matches 1 run scoreboard players operation @s c2R = #c3Slot tmp',
        'execute if score #c3InPack tmp matches 1 run scoreboard players operation @s c3N = #c3Size tmp',
        'execute if score #c3InPack tmp matches 1 run scoreboard players add #c3Slot tmp 1'] + list(lines) + [
        f'function rlk:cm/{mob}/rig/create',
        f'tag @e[tag=rlk_{NS}this] remove rlk_{NS}this'])


def build(w):
    fungus(w)
    pod(w)
    mercenary(w)
    hatchling(w)
    healer(w)
    groups(w)


# ==================================================================== 둥실 버섯 (fu)
def fungus(w):
    s2.spawn_fn(w, 'fu', '둥실 버섯', [], [('scale', 0.75), ('movement_speed', 0.2)], ns=NS)
    w('cm/fu/init', common_init('fu', [
        '# 첫 마리가 무리장(rlk_fu_lead). 절반은 골드 · 회복 구슬 없음',
        'execute unless score #c3InPack tmp matches 1 run tag @s add rlk_fu_lead',
        'execute if score #c3InPack tmp matches 1 unless score #c3PackLd tmp matches 1 run tag @s add rlk_fu_lead',
        'execute if score #c3InPack tmp matches 1 run scoreboard players set #c3PackLd tmp 1',
        'execute store result score @s cmCd run random value 12..36',
        'execute store result score @s c2T run random value 1..4',
        'execute store result score #c3r tmp run random value 0..1',
        'execute if score #c3r tmp matches 1 run tag @s add rlk_c2lite']))
    w('cm/fu/tick', '''
# 둥실 버섯 (@s = 두뇌, at @s): 무리장 곁(1.8칸)에 뭉쳐 떠다니며 다가옴. 2.4칸 안이면 0.5초 부풀기(예고) → 몸통 박치기(10)
execute if score @s cmS matches 1 run return run function rlk:cm/fu/swell
execute if score @s cmS matches 2 run return run function rlk:cm/fu/bump
execute if score @s cmAR matches 1.. run scoreboard players set #hold tmp 1
execute if score #free tmp matches 1 if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..2.4] run return run function rlk:cm/fu/start
scoreboard players remove @s c2T 1
execute if score @s c2T matches ..0 run function rlk:cm/fu/cohere
''')
    w('cm/fu/start', f'''
scoreboard players set @s cmS 1
scoreboard players operation @s cmT = #c3W_fu tmp
scoreboard players operation @s cmCd = #c3Cd_fu tmp
scoreboard players operation #cid tmp = @s cmId
execute as @e[tag=rlk_fu_glow,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {{Glowing:1b,glow_color_override:9502608}}
particle minecraft:composter ~ ~1.2 ~ 0.3 0.25 0.3 0.05 8 normal
{w.snd('fuswell', 'minecraft:entity.puffer_fish.blow_up', 1.0, 1.2)}
{w.snd('fuhum', 'minecraft:block.big_dripleaf.tilt_down', 0.7, 1.6)}
''')
    w('cm/fu/swell', '''
# 부풀기(예고 0.5초, 갓이 커지고 반점이 빛남): 경직 · 빙결이면 취소
scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/cancel
scoreboard players remove @s cmT 1
execute if score @s cmT matches 1.. run particle minecraft:spore_blossom_air ~ ~1.3 ~ 0.35 0.2 0.35 0 2 normal
execute if score @s cmT matches ..0 run function rlk:cm/fu/go
''')
    w('cm/fu/go', f'''
# 몸이 있던 쪽으로 툭 박치기(4틱, 방향은 이 순간 고정)
scoreboard players set @s cmS 2
scoreboard players set @s cmT 4
scoreboard players set @s c2T2 0
scoreboard players set #c2Fw tmp 420
scoreboard players set #c2Up tmp 120
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:cm/c2/impulse
{w.snd('fubump', 'minecraft:entity.puffer_fish.blow_out', 1.0, 0.8)}
''')
    w('cm/fu/bump', '''
# 박치기 중: 반경 1.5 안의 몸에 10, 버섯 한 마리당 한 번 · 버섯 전체로 한 틱 한 번
scoreboard players set #hold tmp 1
execute if score @s c2T2 matches 0 if score #c3FuHit tmp matches 0 if entity @e[tag=rlk_body,distance=..1.5] run function rlk:cm/fu/hit
scoreboard players remove @s cmT 1
execute if score @s cmT matches ..0 run function rlk:cm/fu/end
''')
    w('cm/fu/hit', '''
scoreboard players set @s c2T2 1
scoreboard players set #c3FuHit tmp 1
particle minecraft:composter ~ ~0.9 ~ 0.4 0.3 0.4 0.1 10 normal
scoreboard players operation #cmDmg tmp = #c3D_fu tmp
function rlk:cm/hit_me
''')
    w('cm/fu/end', '''
scoreboard players set @s cmS 0
scoreboard players set @s cmAR 8
execute as @e[tag=rlk_fu_glow,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:0b}
''')
    w('cm/fu/cohere', '''
# 4틱마다: 무리장을 찾고(없으면 내가 무리장), 1.8칸보다 멀면 무리장 쪽으로 끌림 → 무리가 한 덩어리로 뭉침
scoreboard players set @s c2T 4
scoreboard players operation #g tmp = @s c2G
execute as @e[tag=rlk_fu_lead,distance=..24] if score @s c2G = #g tmp run tag @s add rlk_c2ld
execute unless entity @e[tag=rlk_c2ld,limit=1] run tag @s add rlk_fu_lead
execute if entity @s[tag=rlk_fu_lead] run return run tag @e[tag=rlk_c2ld] remove rlk_c2ld
scoreboard players set #c2Fw tmp 240
scoreboard players set #c2Up tmp -1
execute unless entity @e[tag=rlk_c2ld,distance=..1.8] facing entity @e[tag=rlk_c2ld,limit=1,sort=nearest] feet rotated ~ 0 run function rlk:cm/c2/impulse
tag @e[tag=rlk_c2ld] remove rlk_c2ld
''')
    prop_rig(w, 'fu', [
        'scoreboard players operation #pose tmp = @s cmAF', 'scoreboard players operation #pose tmp /= #c2c12 tmp',
        'execute if score @s cmAR matches 5.. run scoreboard players set #pose tmp 30',
        'execute if score @s cmAR matches 1..4 run scoreboard players set #pose tmp 31',
        'execute if score @s cmS matches 1 if score @s cmT matches 6.. run scoreboard players set #pose tmp 20',
        'execute if score @s cmS matches 1 if score @s cmT matches ..5 run scoreboard players set #pose tmp 21',
        'execute if score @s cmS matches 2 run scoreboard players set #pose tmp 24',
        'execute if score @s cmAH matches 3.. run scoreboard players set #pose tmp 40'])
    w('cm/fu/rig/die', f'''
# 버섯이 죽음 (@s = 뿌리 = 두뇌가 있던 바닥): 부풀어 터지고, 그 자리에 포자 주머니(3초). 포자 폭발로 죽은 버섯은 주머니를 남기지 않음
function rlk:cm/fu/rig/pose/50
particle minecraft:spore_blossom_air ~ ~1 ~ 0.4 0.3 0.4 0 12 normal
{w.snd('fudie', 'minecraft:entity.puffer_fish.death', 0.9, 1.3)}
execute unless entity @s[tag=rlk_c3nopod] run function rlk:cm/fp/spawn
''')
    w('cm/fu/rig/fling', 'function rlk:cm/fu/rig/pose/51')


# ==================================================================== 포자 주머니 (fp)
def pod(w):
    tags = '"rlk_room","rlk_mob","rlk_cmlink","rlk_c3pod","rlk_c3pnew"'
    parts = []
    for p in POD_PARTS:
        tg = f'"rlk_room","rlk_pet","rlk_cmlink","rlk_fp_pt","rlk_fp_{p}","rlk_c3pnew"'
        parts.append(f'summon minecraft:item_display ~ ~ ~ {{Tags:[{tg}],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",'
                     f'interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:1.6f,height:1.6f,shadow_radius:0f,brightness:{{sky:15,block:15}},'
                     f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"rlk:cm/{NS}/fp/{p}","minecraft:custom_model_data":{{colors:[16777215]}}}}}}}}')
    w('cm/fp/spawn', '\n'.join([
        '# 포자 주머니 (실행 위치 = 버섯이 죽은 바닥). 맞힐 수 있는 물체: 투명 NoAI 허스크(rlk_mob 을 미리 달아 체력바 · 방 몹 아님, rlk_zmob 없음) + 모습 2부품',
        f'summon minecraft:husk ~ ~ ~ {{Tags:[{tags}],NoAI:1b,Silent:1b,PersistenceRequired:1b,DeathLootTable:"minecraft:empty",IsBaby:0b,CanPickUpLoot:0b,'
        'active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}],'
        'attributes:[{id:"minecraft:scale",base:0.55d},{id:"minecraft:max_health",base:1024d},{id:"minecraft:knockback_resistance",base:1d}],Health:1024f}',
        'scoreboard players operation @e[tag=rlk_c3pnew,type=minecraft:husk] c3L = #c3PodL tmp',
        'scoreboard players set @e[tag=rlk_c3pnew,type=minecraft:husk] mlv 1',
        'scoreboard players set @e[tag=rlk_c3pnew,type=minecraft:husk] mhp0 1',
        'scoreboard players set @e[tag=rlk_c3pnew,type=minecraft:husk] mhpM 1',
        'scoreboard players set @e[tag=rlk_c3pnew,type=minecraft:husk] mhpC 1'] + parts + [
        '# 주머니와 부품은 cmId 로 묶임. 주머니도 rlk_cmlink(매 틱 cm/c3/clean 에서 rlk_cmsync) → 모습이 없어져도 cm/clean 이 돌아 제때 사라짐',
        'scoreboard players add #cmIdC tmp 1',
        'scoreboard players operation @e[tag=rlk_c3pnew] cmId = #cmIdC tmp',
        'tag @e[tag=rlk_c3pnew] add rlk_cmsync',
        'execute as @e[tag=rlk_c3pnew,tag=rlk_fp_pt] run function rlk:cm/fp/pose/0',
        'tag @e[tag=rlk_c3pnew] remove rlk_c3pnew',
        w.snd('fpgrow', 'minecraft:block.big_dripleaf.place', 0.8, 1.4)]))
    w('cm/fp/hit', '''
# 플레이어의 공격이 주머니에 닿음 (@s = 주머니, combat/apply 맨 앞에서): 이번 틱 cm/clean 에서 터짐. 보상 · 숫자 · 원소 반응 없음
tag @s add rlk_c3pop
''')
    w('cm/fp/tick', '''
# 주머니 한 틱 (@s = 주머니 허스크, at @s; cm/c3/clean 에서): 모습 유지 · 맥박 · 터짐 / 시듦
scoreboard players operation #pid tmp = @s cmId
execute as @e[tag=rlk_fp_pt,distance=..2] if score @s cmId = #pid tmp run tag @s add rlk_c3this
tag @e[tag=rlk_c3this] add rlk_cmsync
tag @s add rlk_cmsync
execute if entity @s[tag=rlk_c3pop] run return run function rlk:cm/fp/burst
scoreboard players remove @s c3L 1
execute if score @s c3L matches ..0 run return run function rlk:cm/fp/wither
scoreboard players operation #c3m tmp = @s c3L
scoreboard players operation #c3m tmp %= #c3c10 tmp
execute if score @s c3L matches 21.. if score #c3m tmp matches 0 as @e[tag=rlk_c3this] run function rlk:cm/fp/pose/1
execute if score @s c3L matches 21.. if score #c3m tmp matches 5 as @e[tag=rlk_c3this] run function rlk:cm/fp/pose/2
scoreboard players operation #c3m tmp = @s c3L
scoreboard players operation #c3m tmp %= #c3c6 tmp
execute if score @s c3L matches ..20 if score #c3m tmp matches 0 as @e[tag=rlk_c3this] run function rlk:cm/fp/pose/3
execute if score @s c3L matches ..20 if score #c3m tmp matches 3 as @e[tag=rlk_c3this] run function rlk:cm/fp/pose/4
execute if score #c3m tmp matches 1 run particle minecraft:spore_blossom_air ~ ~0.6 ~ 0.25 0.25 0.25 0 2 normal
execute if score @s c3L matches ..20 if score #c3m tmp matches 0 run particle minecraft:happy_villager ~ ~0.5 ~ 0.25 0.2 0.25 0 2 normal
tag @e[tag=rlk_c3this] remove rlk_c3this
''')
    for pid, (name, dur, spec) in sorted(poses.FP.items()):
        lines = [f'# {name} ({dur}틱 보간) @s = 주머니 부품']
        for p in POD_PARTS:
            lines.append(f'execute if entity @s[tag=rlk_fp_{p}] run ' + rig.merge_line('@s', _tqs(spec[p]), dur))
        w(f'cm/fp/pose/{pid}', '\n'.join(lines))
    w('cm/fp/burst', f'''
# 터짐 (@s = 주머니, at @s): 반경 3 안의 맞힐 수 있는 커스텀 몹 두뇌에만(rlk_mob: 플레이어 · 땅속에 있는 전갈 새끼 · 성수 전갈 제외). 버섯 = 최대 체력 100 %(한 방에 무리째), 다른 몹 = 12 + 최대 체력 30 %. 한 몹은 한 틱에 주머니 하나만
execute as @e[tag=rlk_c3this] run function rlk:cm/fp/pose/50
particle minecraft:explosion ~ ~0.6 ~ 0 0 0 0 1 normal
particle minecraft:composter ~ ~0.6 ~ 1.4 0.5 1.4 0.3 40 normal
particle minecraft:spore_blossom_air ~ ~1 ~ 1.5 0.6 1.5 0 30 normal
particle minecraft:dust{{color:[0.55,0.95,0.6],scale:2.0}} ~ ~0.6 ~ 1.3 0.4 1.3 0 24 normal
{w.snd('fpburst', 'minecraft:entity.puffer_fish.blow_out', 1.2, 0.6)}
{w.snd('fpboom', 'minecraft:entity.generic.explode', 0.5, 1.7)}
execute as @e[tag=rlk_cmb,tag=rlk_mob,distance=..3] at @s run function rlk:cm/fp/blast_one
kill @e[tag=rlk_c3this]
kill @s
''')
    w('cm/fp/blast_one', '''
# 포자 폭발 한 대 (@s = 맞는 두뇌). 진짜 피해(보정 · 반응 없음, 면역 없음), 숫자는 풀 색
execute if entity @s[tag=rlk_c3pz] run return 0
tag @s add rlk_c3pz
scoreboard players operation #c2zd tmp = @s mhpM
execute if entity @s[tag=rlk_cm_fu] run function rlk:cm/fp/fu_mark
execute unless entity @s[tag=rlk_cm_fu] run function rlk:cm/fp/pct
particle minecraft:composter ~ ~0.8 ~ 0.25 0.3 0.25 0.1 8 normal
function rlk:cm/c3/true_hit
''')
    w('cm/fp/pct', '''
scoreboard players operation #c2zd tmp *= #c3PodPct tmp
scoreboard players operation #c2zd tmp /= #c2c100 tmp
scoreboard players operation #c2zd tmp += #c3PodD tmp
''')
    w('cm/fp/fu_mark', '''
# 포자로 터진 버섯은 새 주머니를 남기지 않음(뿌리 부품에 표시)
scoreboard players operation #c3k tmp = @s cmId
execute as @e[tag=rlk_fu_stem,distance=..4] if score @s cmId = #c3k tmp run tag @s add rlk_c3nopod
''')
    w('cm/fp/wither', f'''
# 3초 동안 아무도 안 건드림: 쪼그라들며 사라짐(피해 없음)
particle minecraft:poof ~ ~0.4 ~ 0.2 0.2 0.2 0.02 6 normal
{w.snd('fpwither', 'minecraft:block.azalea_leaves.break', 0.7, 0.6)}
kill @e[tag=rlk_c3this]
kill @s
''')


# ==================================================================== 에르미타 단검 용병 (em)
def mercenary(w):
    s2.spawn_fn(w, 'em', '에르미타 단검 용병', [], [('movement_speed', 0.27)], ns=NS)
    w('cm/em/init', common_init('em', [
        'execute store result score @s cmCd run random value 30..60',
        'execute store result score @s c2T run random value 1..3']))
    w('cm/em/tick', '''
# 단검 용병 (@s, at @s): 9칸 밖이면 걸어 옴. 안이면 무리가 몸 둘레 4칸을 함께 돎(자리 = 무리 각도). 둘씩 0.6초 웅크림 → 몸 쪽으로 돌진 찌르기(14), 가운데서 뭉친 채 0.8초 멈춤
execute if score @s cmS matches 1 run return run function rlk:cm/em/crouch
execute if score @s cmS matches 2 run return run function rlk:cm/em/dash
execute if score @s cmAR matches 1.. run return run scoreboard players set #hold tmp 1
execute unless entity @e[tag=rlk_body,distance=..9] run return 0
scoreboard players set #hold tmp 1
execute if score #free tmp matches 1 if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..6.5] run return run function rlk:cm/em/pair_go
execute if score #free tmp matches 0 run return 0
scoreboard players remove @s c2T 1
execute if score @s c2T matches ..0 run function rlk:cm/em/orbit
''')
    w('cm/em/orbit', '''
# 3틱마다 내 자리(몸에서 4칸, 무리 각도)로 끌림
scoreboard players set @s c2T 3
function rlk:cm/c3/turn
scoreboard players set #c2Fw tmp 210
scoreboard players set #c2Up tmp -1
execute at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^ ^4 unless entity @s[distance=..0.7] facing entity @s feet rotated ~180 0 run function rlk:cm/c2/impulse
''')
    w('cm/em/pair_go', '''
# 둘씩 공격: 나 + 같은 무리에서 쉬는 한 마리(무작위). 무리 전체는 다음 쌍까지 #c3Gap_em 틱 기다림. 몸까지 길이 막혔거나 낭떠러지면 안 감
execute unless function rlk:cm/em/dash_ok run return run scoreboard players set @s cmCd 10
scoreboard players operation #g tmp = @s c2G
scoreboard players operation #c3cidS tmp = #cid tmp
tag @s add rlk_c3pick
execute at @e[tag=rlk_body,limit=1] as @e[tag=rlk_cm_em,tag=!rlk_c3pick,distance=..9] if score @s c2G = #g tmp if score @s cmS matches 0 if score @s cmAR matches ..0 unless score @s stunT matches 1.. unless score @s frzT matches 1.. at @s if function rlk:cm/em/dash_ok run tag @s add rlk_c3cand
execute at @e[tag=rlk_body,limit=1] as @e[tag=rlk_cm_em,distance=..16] if score @s c2G = #g tmp if score @s cmCd < #c3Gap_em tmp run scoreboard players operation @s cmCd = #c3Gap_em tmp
execute as @e[tag=rlk_c3cand,limit=1,sort=random] at @s run function rlk:cm/em/start
function rlk:cm/em/start
tag @e[tag=rlk_c3cand] remove rlk_c3cand
tag @s remove rlk_c3pick
scoreboard players operation #cid tmp = #c3cidS tmp
''')
    w('cm/em/dash_ok', '''
# 몸까지 돌진할 수 있는가 (@s, at @s): 6.5칸 안 · 1 / 2 / 3칸 앞 기둥이 지나갈 수 있음(벽 · 문 · 낭떠러지 아님)
execute unless entity @e[tag=rlk_body,distance=..6.5] run return 0
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^1 unless function rlk:cm/c3/col_ok run return 0
execute if entity @e[tag=rlk_body,distance=2.2..] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^2 unless function rlk:cm/c3/col_ok run return 0
execute if entity @e[tag=rlk_body,distance=3.2..] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^3 unless function rlk:cm/c3/col_ok run return 0
return 1
''')
    w('cm/em/start', f'''
scoreboard players set @s cmS 1
scoreboard players operation @s cmT = #c3W_em tmp
tag @s add rlk_c3fresh
scoreboard players operation @s cmCd = #c3Cd_em tmp
scoreboard players operation #cid tmp = @s cmId
execute as @e[tag=rlk_c3glow,tag=rlk_em_pt,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {{Glowing:1b,glow_color_override:16757606}}
particle minecraft:block{{block_state:"minecraft:sand"}} ~ ~0.2 ~ 0.3 0.05 0.3 0.1 8 normal
{w.snd('emcrouch', 'minecraft:item.armor.equip_leather', 1.0, 0.7)}
{w.snd('emglint', 'minecraft:block.amethyst_block.chime', 1.0, 1.9)}
''')
    w('cm/em/crouch', '''
# 웅크림(예고 0.6초, 두 단검이 빛남): 경직 · 빙결이면 그 용병만 취소. 시작한 틱에는 줄지 않음(둘이 같은 틱에 돌진)
scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/cancel
execute if entity @s[tag=rlk_c3fresh] run return 0
scoreboard players remove @s cmT 1
execute if score @s cmT matches 3..7 run particle minecraft:end_rod ~ ~0.9 ~ 0.3 0.1 0.3 0.01 1 normal
execute if score @s cmT matches ..0 run function rlk:cm/em/go
''')
    w('cm/em/go', f'''
# 돌진: 이 순간 몸이 있는 쪽으로 방향 고정, 거리만큼(4 / 6 / 8틱 × 0.6칸) → 둘이 가운데로 모임. 돌진 중에는 경직 면역
execute facing entity @e[tag=rlk_body,limit=1] feet run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0
execute store result score @s cmYaw run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100
scoreboard players set @s cmS 2
scoreboard players set @s cmT 8
execute if entity @e[tag=rlk_body,distance=..4.5] run scoreboard players set @s cmT 6
execute if entity @e[tag=rlk_body,distance=..3] run scoreboard players set @s cmT 4
scoreboard players set @s c2T2 0
tag @s add rlk_cmch
{w.snd('emdash', 'minecraft:item.trident.throw', 1.0, 1.4)}
''')
    w('cm/em/dash', '''
# 돌진 찌르기 (0.6칸/틱, 블록은 바닐라 물리로 막힘). 단검 끝(0.8칸 앞 r1.3)에 몸이 있으면 14, 용병 한 마리당 한 번 · 무리 전체로 한 틱 한 번
scoreboard players set #hold tmp 1
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
scoreboard players set #c2Fw tmp 600
scoreboard players set #c2Up tmp -1
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 run function rlk:cm/c2/impulse
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^0.9 ^0.8 run particle minecraft:crit ~ ~ ~ 0.2 0.1 0.2 0.1 2 normal
execute if score @s c2T2 matches 0 if score #c3EmHit tmp matches 0 rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^ ^0.8 if entity @e[tag=rlk_body,distance=..1.3] run function rlk:cm/em/hit
scoreboard players remove @s cmT 1
execute if score @s cmT matches ..0 run function rlk:cm/em/end
''')
    w('cm/em/hit', f'''
scoreboard players set @s c2T2 1
scoreboard players set #c3EmHit tmp 1
{w.snd('emstab', 'minecraft:entity.player.attack.sweep', 0.9, 1.5)}
scoreboard players operation #cmDmg tmp = #c3D_em tmp
function rlk:cm/hit_me
''')
    w('cm/em/end', '''
scoreboard players set @s cmS 0
scoreboard players set @s cmAR 16
tag @s remove rlk_cmch
execute as @e[tag=rlk_c3glow,tag=rlk_em_pt,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:0b}
''')
    walk = ['scoreboard players operation #pose tmp = @s cmAF', 'scoreboard players operation #pose tmp /= #c2c12 tmp',
            'execute unless entity @e[tag=rlk_body,distance=..2.3] if score @s c2Age matches 1.. if data entity @s {OnGround:1b} unless entity @s[tag=rlk_cmhold] run function rlk:cm/c2/walk8',
            'execute if entity @s[tag=rlk_cmhold] if score @s c2T matches 1..3 unless entity @e[tag=rlk_body,distance=..3] run function rlk:cm/c2/walk8']
    s2.humanoid_rig(w, 'em', FACE_AIM, walk + [
        'execute if score @s cmAR matches 12.. run scoreboard players set #pose tmp 30',
        'execute if score @s cmAR matches 1..11 run scoreboard players set #pose tmp 31',
        'execute if score @s cmS matches 1 if score @s cmT matches 8.. run scoreboard players set #pose tmp 20',
        'execute if score @s cmS matches 1 if score @s cmT matches ..7 run scoreboard players set #pose tmp 21',
        'execute if score @s cmS matches 2 if score @s cmT matches 3.. run scoreboard players set #pose tmp 24',
        'execute if score @s cmS matches 2 if score @s cmT matches ..2 run scoreboard players set #pose tmp 25',
        'execute if score @s cmAH matches 4.. run scoreboard players set #pose tmp 40',
        'execute if score @s cmAH matches 1..3 run scoreboard players set #pose tmp 41'], H=HUMANOID['em'], ns=NS)
    w('cm/em/rig/die', 'function rlk:cm/em/rig/pose/50')
    w('cm/em/rig/fling', 'function rlk:cm/em/rig/pose/51')


# ==================================================================== 모래 전갈 새끼 (sb)
def hatchling(w):
    s2.spawn_fn(w, 'sb', '모래 전갈 새끼', [], [('scale', 0.6), ('movement_speed', 0.3)], ns=NS)
    w('cm/sb/init', common_init('sb', [
        '# 땅속에서 시작(맞힐 수 없음). 무리는 같은 타이머(#c3SbT)로 함께 솟음. 넷 중 셋은 골드 · 회복 구슬 없음',
        'function rlk:cm/sb/hide',
        'execute store result score @s c2T run random value 20..50',
        'execute if score #c3InPack tmp matches 1 run scoreboard players operation @s c2T = #c3SbT tmp',
        'scoreboard players set @s c2T2 -1',
        'execute store result score #c3r tmp run random value 0..3',
        'execute unless score #c3r tmp matches 0 run tag @s add rlk_c2lite']))
    w('cm/sb/hide', '''
# 땅속으로 (@s = 두뇌): rlk_mob 을 떼고 rlk_pet(몹 준비 대상 아님) → 플레이어 공격 · 자동 조준이 고르지 않음, 체력바 · 클릭 실드도 정리됨. 무적, 다중 처치 대상 아님
tag @s add rlk_c3bur
tag @s add rlk_pet
tag @s remove rlk_mob
data merge entity @s {Invulnerable:1b}
scoreboard players set @s c3B 0
''')
    w('cm/sb/unhide', '''
# 땅 위로: 다음 틱 몹 준비(mob/setup)가 rlk_mob · 체력바 · 클릭 실드를 다시 붙임
tag @s remove rlk_c3bur
tag @s remove rlk_pet
data merge entity @s {Invulnerable:0b}
''')
    w('cm/sb/tick', '''
# 모래 전갈 새끼 (@s, at @s). 순환: 땅속(#c3Dn_sb) → 몸 둘레 고리 자리에 모래 둔덕(예고 0.8초) → 솟구쳐 물기(8) → 땅 위 2초(반격 시간) → 다시 파고듦.
# 걷지 않음(자리 이동은 솟을 때 한 번). 빙결 중에는 순환이 멈춤(땅 위에서만 얼 수 있음)
scoreboard players set #hold tmp 1
execute if score @s frzT matches 1.. run return 0
scoreboard players remove @s c2T 1
execute if score @s c3B matches 0 run return run function rlk:cm/sb/under
execute if score @s c3B matches 1 run return run function rlk:cm/sb/mound
execute if score @s c3B matches 2 run return run function rlk:cm/sb/up
execute if score @s c3B matches 3 run return run function rlk:cm/sb/sink
''')
    w('cm/sb/under', '''
execute if score @s c2T matches 1.. run return 0
function rlk:cm/sb/emerge
''')
    w('cm/sb/emerge', f'''
# 솟을 자리 정하기: 몸에서 2.6칸, 각도 = 무리 각도(자리 × 360° / 무리 크기 + 회전). 몸에서 그 자리까지 벽이 없고 설 수 있는 자리여야 함(한 칸 위 · 아래도 봄). 안 되면 지금 자리에서
scoreboard players set @s c3B 1
scoreboard players operation @s c2T = #c3W_sb tmp
scoreboard players set #c3ok tmp 0
execute if entity @e[tag=rlk_body,limit=1] run function rlk:cm/c3/turn
execute if entity @e[tag=rlk_body,limit=1] at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 if function rlk:cm/sb/ray_ok positioned ^ ^ ^2.6 if function rlk:cm/c2/safe_here run function rlk:cm/sb/move
execute if score #c3ok tmp matches 0 if entity @e[tag=rlk_body,limit=1] at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 if function rlk:cm/sb/ray_ok positioned ^ ^1 ^2.6 if function rlk:cm/c2/safe_here run function rlk:cm/sb/move
execute if score #c3ok tmp matches 0 if entity @e[tag=rlk_body,limit=1] at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 if function rlk:cm/sb/ray_ok positioned ^ ^-1 ^2.6 if function rlk:cm/c2/safe_here run function rlk:cm/sb/move
# 솟구칠 방향 = 지금 몸 쪽(둔덕이 나온 순간 고정: 둔덕 고리 밖으로 나가면 피함)
execute if entity @e[tag=rlk_body,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0
execute if entity @e[tag=rlk_body,limit=1] store result score @s cmYaw run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100
execute at @s run particle minecraft:block{{block_state:"minecraft:sand"}} ~ ~0.1 ~ 0.3 0.05 0.3 0.1 10 normal
execute at @s run {w.snd('sbmound', 'minecraft:block.sand.break', 0.9, 0.7)}
''')
    w('cm/sb/ray_ok', '''
# 몸(실행 위치)에서 고리 자리 쪽 0.9 · 1.8칸이 몸 높이로 비었는가(벽 · 문 너머로는 안 솟음)
execute unless block ^ ^0.5 ^0.9 #rlk:dash_pass run return 0
execute unless block ^ ^1.2 ^0.9 #rlk:dash_pass run return 0
execute unless block ^ ^0.5 ^1.8 #rlk:dash_pass run return 0
execute unless block ^ ^1.2 ^1.8 #rlk:dash_pass run return 0
return 1
''')
    w('cm/sb/move', '''
# 땅속에서 자리 옮김(실행 위치 = 확인한 발 자리). 이번 틱의 cm/tick 은 옛 자리에서 돌므로, 리그 부품은 이번 틱 모습 처리
# (sb/rig/tick, 옛 자리에서 부품을 찾은 뒤)가 rlk_c3moved 를 보고 새 자리로 옮김 → 멀리 솟아도 리그를 잃지 않음
tp @s ~ ~ ~
tag @s add rlk_c3moved
scoreboard players set #c3ok tmp 1
''')
    w('cm/sb/mound', '''
# 모래 둔덕(예고 0.8초): 둔덕이 부풀며 떨림 · 모래가 튐. 아직 맞힐 수 없음
execute if score @s c2T matches 1.. if score @s c2T matches 2..15 run particle minecraft:falling_dust{block_state:"minecraft:sand"} ~ ~0.3 ~ 0.25 0.1 0.25 0 1 normal
execute if score @s c2T matches 1..6 run particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.15 ~ 0.25 0.05 0.25 0.05 3 normal
execute if score @s c2T matches ..0 run function rlk:cm/sb/erupt
''')
    w('cm/sb/erupt', f'''
# 솟구침: 맞힐 수 있게 되고, 둔덕이 나올 때 정한 쪽(고리 가운데)으로 짧게 튀어 오름. 물기는 자리 번호에 따라 3~5틱 뒤(무리가 한 번에 다 물지 않게)
function rlk:cm/sb/unhide
scoreboard players set @s c3B 2
scoreboard players operation @s c2T = #c3Up_sb tmp
scoreboard players operation @s c2T2 = @s c2R
scoreboard players operation @s c2T2 %= #c3c3 tmp
scoreboard players add @s c2T2 3
particle minecraft:block{{block_state:"minecraft:sand"}} ~ ~0.3 ~ 0.35 0.25 0.35 0.2 20 normal
{w.snd('sberupt', 'minecraft:block.suspicious_sand.break', 1.0, 0.8)}
{w.snd('sbhiss', 'minecraft:entity.silverfish.ambient', 0.8, 1.6)}
scoreboard players set #c2Fw tmp 260
scoreboard players set #c2Up tmp 280
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 run function rlk:cm/c2/impulse
''')
    w('cm/sb/up', '''
# 땅 위 2초: 물기 한 번(c2T2 가 0 이 되는 틱), 두 틱 뒤 넉백 저항 0(몹 준비가 0.5 로 되돌려 놓으므로)
execute if score @s c2T2 matches 1.. run scoreboard players remove @s c2T2 1
execute if score @s c2T2 matches 0 run function rlk:cm/sb/bite
execute if score @s c2T2 matches 1 run function rlk:cm/c2/first
execute if score @s c2T matches ..0 run function rlk:cm/sb/sink_go
''')
    w('cm/sb/bite', f'''
# 물기: 반경 1.9 안의 몸에 8. 전갈 새끼 전체로 한 틱 한 번. 경직 · 빙결이면 못 묾
scoreboard players set @s c2T2 -1
execute unless score #free tmp matches 1 run return 0
scoreboard players set @s cmAR 6
{w.snd('sbbite', 'minecraft:entity.fox.bite', 0.9, 1.5)}
execute if score #c3SbHit tmp matches 0 if entity @e[tag=rlk_body,distance=..1.9] run function rlk:cm/sb/hit
''')
    w('cm/sb/hit', '''
scoreboard players set #c3SbHit tmp 1
scoreboard players operation #cmDmg tmp = #c3D_sb tmp
function rlk:cm/hit_me
''')
    w('cm/sb/sink_go', f'''
scoreboard players set @s c3B 3
scoreboard players set @s c2T 6
scoreboard players set @s c2T2 -1
particle minecraft:block{{block_state:"minecraft:sand"}} ~ ~0.2 ~ 0.3 0.1 0.3 0.1 12 normal
{w.snd('sbsink', 'minecraft:block.sand.place', 0.8, 0.8)}
''')
    w('cm/sb/sink', '''
# 파고듦(0.3초, 아직 맞힐 수 있음) → 땅속
execute if score @s c2T matches 1.. run return 0
function rlk:cm/sb/hide
scoreboard players operation @s c2T = #c3Dn_sb tmp
''')
    prop_rig(w, 'sb', [
        'scoreboard players set #pose tmp 90',
        'execute if score @s c3B matches 1 run scoreboard players operation #pose tmp = @s c2T',
        'execute if score @s c3B matches 1 run scoreboard players operation #pose tmp %= #c3c4 tmp',
        'execute if score @s c3B matches 1 if score #pose tmp matches 0..1 run scoreboard players set #pose tmp 80',
        'execute if score @s c3B matches 1 if score #pose tmp matches 2..3 run scoreboard players set #pose tmp 81',
        'execute if score @s c3B matches 2 run function rlk:cm/sb/rig/pick_up',
        'execute if score @s c3B matches 3 run scoreboard players set #pose tmp 85'], extra_tick=[
        'execute if entity @s[tag=rlk_c3moved] at @s run tp @e[tag=rlk_c3this] ~ ~ ~',
        'tag @s remove rlk_c3moved'])
    w('cm/sb/rig/pick_up', '''
scoreboard players operation #pose tmp = @s cmAF
scoreboard players operation #pose tmp /= #c3c3 tmp
scoreboard players operation #pose tmp %= #c3c4 tmp
execute if score @s c2T matches 37.. run scoreboard players set #pose tmp 82
execute if score @s cmAR matches 4.. run scoreboard players set #pose tmp 24
execute if score @s cmAR matches 1..3 run scoreboard players set #pose tmp 30
execute if score @s cmAH matches 3.. run scoreboard players set #pose tmp 40
''')
    w('cm/sb/rig/die', f'function rlk:cm/sb/rig/pose/50\n{w.snd("sbdie", "minecraft:entity.silverfish.death", 0.9, 1.4)}')
    w('cm/sb/rig/fling', 'function rlk:cm/sb/rig/pose/51')


# ==================================================================== 에르미타 맑은물 술사 (cw)
def healer(w):
    s2.spawn_fn(w, 'cw', '에르미타 맑은물 술사', [], [('movement_speed', 0.22)], ns=NS)
    w('cm/cw/init', '''
scoreboard players set @s c3H 0
scoreboard players set @s c3I 0
scoreboard players set @s c2T 0
function rlk:cm/cw/rig/create
tag @e[tag=rlk_c3this] remove rlk_c3this
''')
    w('cm/cw/tick', '''
# 맑은물 술사 (@s, at @s): 몸과 7~10칸을 둠(7칸 안이면 물러남). 8칸 안에 다친 커스텀 몹(어느 챕터든, 나 말고)이 있으면 제자리에서 영창:
# 2초마다 그 몹들의 체력을 최대 체력의 10 %씩(최대 체력을 넘지 않음), 술사에서 각 몹까지 물줄기. 맞으면 3초 동안 끊김. 직접 공격은 없음
execute if score @s c3I matches 1.. run scoreboard players remove @s c3I 1
function rlk:cm/cw/keep
execute if score #free tmp matches 0 run return run function rlk:cm/cw/stop
execute if score @s c3I matches 1.. run return 0
scoreboard players set #c3w tmp 0
execute as @e[tag=rlk_cmb,distance=..8] unless score @s cmId = #cid tmp if score @s mhpC < @s mhpM run scoreboard players set #c3w tmp 1
execute if score #c3w tmp matches 0 run return run function rlk:cm/cw/stop
execute if score @s cmS matches 0 run function rlk:cm/cw/begin
scoreboard players set #hold tmp 1
scoreboard players remove @s c3H 1
execute if score @s c3H matches ..0 run function rlk:cm/cw/pulse
''')
    w('cm/cw/keep', '''
# 거리 두기: 10칸 안이면 더 다가오지 않고, 7칸 안이면 3틱마다 몸 반대쪽으로(뒤 1.2칸이 지나갈 수 있을 때만)
execute unless entity @e[tag=rlk_body,limit=1] run return 0
execute if entity @e[tag=rlk_body,distance=..10] run scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return 0
execute if score @s c2T matches 1.. run scoreboard players remove @s c2T 1
execute unless entity @e[tag=rlk_body,distance=..7] run return 0
execute if score @s c2T matches 1.. run return 0
scoreboard players set @s c2T 3
scoreboard players set #c2Fw tmp 230
scoreboard players set #c2Up tmp -1
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^1.2 if function rlk:cm/c3/col_ok positioned ^ ^ ^-1.2 run function rlk:cm/c2/impulse
''')
    w('cm/cw/begin', f'''
# 영창 시작: 물 구슬이 머리 위로, 빛남
scoreboard players set @s cmS 1
scoreboard players operation @s c3H = #c3Hi_cw tmp
execute as @e[tag=rlk_cw_orb,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {{Glowing:1b,glow_color_override:6737151}}
{w.snd('cwcast', 'minecraft:block.conduit.activate', 0.7, 1.6)}
{w.snd('cwsplash', 'minecraft:entity.player.splash', 0.5, 1.4)}
''')
    w('cm/cw/pulse', f'''
# 치유 한 번 (2초마다): 8칸 안의 다친 커스텀 몹 두뇌(나 말고) 모두 +최대 체력 10 %, 최대 체력에서 멈춤. 물줄기를 그림
scoreboard players operation @s c3H = #c3Hi_cw tmp
tag @s add rlk_c3heal
execute as @e[tag=rlk_cmb,distance=..8] unless score @s cmId = #cid tmp if score @s mhpC < @s mhpM at @s run function rlk:cm/cw/heal_one
tag @s remove rlk_c3heal
particle minecraft:splash ~ ~2.4 ~ 0.3 0.3 0.3 0.2 20 normal
{w.snd('cwheal', 'minecraft:item.bucket.empty', 0.8, 1.3)}
{w.snd('cwchime', 'minecraft:block.amethyst_block.resonate', 0.6, 1.8)}
''')
    w('cm/cw/heal_one', '''
# @s = 치유받는 두뇌, at @s
scoreboard players operation #c3hv tmp = @s mhpM
scoreboard players operation #c3hv tmp *= #c3Hp_cw tmp
scoreboard players operation #c3hv tmp /= #c2c100 tmp
execute if score #c3hv tmp matches ..0 run scoreboard players set #c3hv tmp 1
scoreboard players operation @s mhpC += #c3hv tmp
scoreboard players operation @s mhpC < @s mhpM
particle minecraft:splash ~ ~1 ~ 0.3 0.4 0.3 0.1 12 normal
particle minecraft:dust{color:[0.45,0.8,1.0],scale:1.2} ~ ~1.1 ~ 0.3 0.4 0.3 0 6 normal
scoreboard players set #c3rs tmp 16
execute positioned ~ ~1.1 ~ facing entity @e[tag=rlk_c3heal,limit=1] feet positioned ^ ^ ^0.5 run function rlk:cm/cw/ribbon
''')
    w('cm/cw/ribbon', '''
# 물줄기 한 칸(0.5칸씩 술사 쪽으로, 최대 16칸 = 8칸 거리): 물빛 입자 + 물방울. 술사 1칸 안에서 멈춤
particle minecraft:dust{color:[0.3,0.7,1.0],scale:1.0} ~ ~ ~ 0.03 0.03 0.03 0 2 normal
particle minecraft:falling_water ~ ~ ~ 0.05 0.05 0.05 0 1 normal
scoreboard players remove #c3rs tmp 1
execute if score #c3rs tmp matches ..0 run return 0
execute if entity @e[tag=rlk_c3heal,distance=..1.6] run return 0
execute positioned ^ ^ ^0.5 run function rlk:cm/cw/ribbon
''')
    w('cm/cw/stop', f'''
# 영창 끝(치유할 몹이 없음 · 경직 · 빙결 · 끊김)
execute unless score @s cmS matches 1 run return 0
scoreboard players set @s cmS 0
execute as @e[tag=rlk_cw_orb,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {{Glowing:0b}}
''')
    w('cm/cw/interrupt', f'''
# 맞음: 3초 동안 영창 못 함(구슬이 터지는 소리 · 물보라)
scoreboard players operation @s c3I = #c3Int_cw tmp
execute if score @s cmS matches 1 run particle minecraft:splash ~ ~2.3 ~ 0.4 0.3 0.4 0.3 30 normal
execute if score @s cmS matches 1 run {w.snd('cwbreak', 'minecraft:block.fire.extinguish', 0.7, 1.4)}
scoreboard players operation #cid tmp = @s cmId
function rlk:cm/cw/stop
''')
    walk = ['scoreboard players operation #pose tmp = @s cmAF', 'scoreboard players operation #pose tmp /= #c2c12 tmp',
            'execute unless entity @s[tag=rlk_cmhold] run function rlk:cm/c2/walk8',
            'execute if score @s c2T matches 1..3 if entity @e[tag=rlk_body,distance=..7] run function rlk:cm/c2/walk8']
    s2.humanoid_rig(w, 'cw', FACE_AIM, walk + [
        'execute if score @s cmS matches 1 run function rlk:cm/cw/rig/chan',
        'execute if score @s c3I matches 45.. run scoreboard players set #pose tmp 70',
        'execute if score @s cmAH matches 4.. run scoreboard players set #pose tmp 40',
        'execute if score @s cmAH matches 1..3 run scoreboard players set #pose tmp 41'], H=HUMANOID['cw'], ns=NS, extra_tick=[
        'execute if score @s cmS matches 1 if score @s c3H matches 2..40 at @e[tag=rlk_cw_orb,tag=rlk_c3this,limit=1] run particle minecraft:dripping_water ~ ~2.35 ~ 0.2 0.1 0.2 0 1 normal'])
    w('cm/cw/rig/chan', '''
scoreboard players operation #pose tmp = @s cmAF
scoreboard players operation #pose tmp /= #c3c6 tmp
scoreboard players operation #pose tmp %= #c3c4 tmp
scoreboard players add #pose tmp 60
''')
    w('cm/cw/rig/die', f'function rlk:cm/cw/rig/pose/50\nparticle minecraft:splash ~ ~1.5 ~ 0.4 0.4 0.4 0.3 20 normal\n{w.snd("cwdie", "minecraft:entity.player.splash.high_speed", 0.7, 1.2)}')
    w('cm/cw/rig/fling', 'function rlk:cm/cw/rig/pose/51')


# ==================================================================== groups
def groups(w):
    from ch3mob.common import cond

    def head(title, rng, mob, extra=()):
        return [title, f'execute unless score #c3SizeSet tmp matches 1 store result score #c3Size tmp run random value {rng}',
                'scoreboard players add #c2PackC tmp 1', 'scoreboard players set #c3InPack tmp 1', 'scoreboard players set #c3PackLd tmp 0',
                'scoreboard players set #c3Slot tmp 0'] + list(extra) + [f'function rlk:cm/spawn/{mob}']

    g = head('# 둥실 버섯 무리 5~7 (실행 위치 = 무리장, 실행 방향 = 앞). 방 배치는 #c3Size, 시험(cm/test)은 무작위. 서로 1칸 남짓 붙어서 나옴', '5..7', 'fu')
    for k, off in enumerate([(1.1, 0.4), (-1.1, 0.4), (0.6, -1.0), (-0.6, -1.0), (0, 1.2), (1.3, -0.5)]):
        body = group_slot('fu', off)
        g += cond(body, k + 2) if k + 2 > 5 else body
    w('cm/spawn/g_fu', '\n'.join(g + ['scoreboard players set #c3InPack tmp 0']))
    g = head('# 에르미타 단검 용병 3~4 (실행 위치 · 방향). 자리 번호 = 몸 둘레를 도는 순서', '3..4', 'em')
    for k, off in enumerate([(1.6, 0), (-1.6, 0), (0, -1.6)]):
        body = group_slot('em', off)
        g += cond(body, k + 2) if k + 2 > 3 else body
    w('cm/spawn/g_em', '\n'.join(g + ['scoreboard players set #c3InPack tmp 0']))
    g = head('# 모래 전갈 새끼 6~8 (실행 위치 · 방향): 땅속에서 시작, 무리가 같은 타이머(#c3SbT)로 함께 솟음', '6..8', 'sb',
             ['execute store result score #c3SbT tmp run random value 20..40'])
    for k, off in enumerate([(1.0, 0), (-1.0, 0), (0, 1.0), (0, -1.0), (0.8, 0.8), (-0.8, -0.8), (0.8, -0.8)]):
        body = group_slot('sb', off)
        g += cond(body, k + 2) if k + 2 > 6 else body
    w('cm/spawn/g_sb', '\n'.join(g + ['scoreboard players set #c3InPack tmp 0']))
