"""Chapter-3 (Sumeru) mob framework (owner: swarm side, part A). Writes data/rlk/function/cm/c3/** and the narrow,
repeatable hook lines into the shared cm / combat / room / load files.

Built on the chapter-2 framework (tools/ch2mob): the Writer / Patcher classes and the namespace-parametrised swarm
blocks (swarm_hurt · swarm_cancel · rig_frozen · swarm_death · kill_cue · true_hit) are imported and called with
ns='c3'; at run time the chapter-3 code calls the chapter-2 helpers that are not chapter-specific (cm/c2/impulse · vec ·
knock · safe_here · brain_end · first, the #c2* constants and kill clock from cm/c2/load).

Every chapter-3 brain carries `rlk_c3` (B's elite ids get it in cm/c3/stats_chk at mob_init); A's mobs also carry
`rlk_c3a`. What the framework gives them:
  * cm/c3/world (once a tick, before the brains): per-tick hit limits, fresh / pod-hit tag reset.
  * cm/c3/tick (per brain, not while the player is down): age, first-tick knockback 0, then `cm/<id>/tick`.
  * swarm hit feel (cm/c3/hurt: 0.25 s stun, knockback 0.42 b/t, red flash), death fling + pop (cm/c3/die · death_tick),
    multi-kill cue (cm/c3/kill_note from combat/apply). Pods (fp) tick from cm/c3/clean, the head of cm/clean.
  * combat/apply guards: a spore pod (`rlk_c3pod`) only marks itself to burst (no reward, no number); a burrowed
    hatchling (`rlk_c3bur`) takes nothing. Burrowed brains also drop `rlk_mob`, so player attacks never select them.
  * chapter-3 room routing: room/mob_wave asks cm/c3/plan for groups by map order and the zone biome (data.sd, 1 =
    desert), room/mob_summon spawns one group per placement through `$function rlk:cm/spawn/$(id)`.
"""
import re  # noqa: F401  (kept for callers that lint)

import help_lib
from ch2mob import common as c2

A_IDS = ('fu', 'em', 'sb', 'cw')          # brains with a rig (fp is an object, owned by fu)
OWN_IDS = A_IDS + ('fp',)
B_IDS = ('cs', 'rv', 'pc')
GROUPS = ('g_fu', 'g_em', 'g_sb')
# rlk:cm/test {t:"help"} rows of chapter 3 (cm/c3/test_help, tools/help_lib.py): every spawn id with its Korean name
TEST_ROWS = [('fu', '둥실 버섯'), ('em', '에르미타 단검 용병'), ('sb', '모래 전갈 새끼'), ('cw', '에르미타 맑은물 술사'),
             ('cs', '성수 전갈'), ('rv', '성수 붉은 독수리'), ('pc', '원시 정령 기계·재구성자'),
             ('g_fu', '둥실 버섯 무리 5~7'), ('g_em', '단검 용병 무리 3~4'), ('g_sb', '모래 전갈 새끼 무리 6~8')]

TUNE = {
    # damage (raw)
    'c3D_fu': 10, 'c3D_em': 14, 'c3D_sb': 8,
    # tells (ticks): fungus swell, mercenary crouch, sand mound
    'c3W_fu': 10, 'c3W_em': 12, 'c3W_sb': 16,
    # intervals (ticks): per mob; em pair gap (whole group waits this long between pairs)
    'c3Cd_fu': 44, 'c3Cd_em': 80, 'c3Gap_em': 34,
    # hatchling cycle: up (exposed) / burrowed (ticks)
    'c3Up_sb': 40, 'c3Dn_sb': 60,
    # healer: % of max HP per pulse, pulse interval, interrupt after a hit (ticks)
    'c3Hp_cw': 10, 'c3Hi_cw': 40, 'c3Int_cw': 60,
    # spore pod: life (ticks), burst flat damage, % of max HP to non-fungus mobs (fungus: 100 %)
    'c3PodL': 60, 'c3PodD': 12, 'c3PodPct': 30,
    # orbit: 1.5 deg/tick (0.01 deg units), one turn = 240 ticks
    'c3Orb': 150, 'c3c240': 240, 'c3c36000': 36000, 'c3c7919': 7919, 'c3c3': 3, 'c3c10': 10, 'c3c6': 6, 'c3c4': 4,
}
# 1st-level HP and kill xp (B's rows follow the shared contract; B's module may set its own on the first tick)
STATS = {'fu': (6, 2), 'em': (10, 3), 'sb': (4, 1), 'cw': (22, 6), 'cs': (80, 14), 'rv': (55, 11), 'pc': (75, 13)}
OBJ = ('c3N', 'c3B', 'c3H', 'c3I', 'c3L')


class Writer(c2.Writer):
    def __init__(self, dp):
        super().__init__(dp, ns='c3', groups=GROUPS)


def cond(lines, n):
    """Guard a group_slot block so it only runs when #c3Size >= n."""
    out = []
    for l in lines:
        if l.startswith('execute '):
            out.append(l.replace('execute ', f'execute if score #c3Size tmp matches {n}.. ', 1))
        else:
            out.append(f'execute if score #c3Size tmp matches {n}.. run ' + l)
    return out


# ---------------------------------------------------------------- framework functions
def build(w):
    T = TUNE
    w('cm/c3/load', '\n'.join(
        ['# 3챕터 몹 점수(tools/build_ch3_mobs.py): 무리 크기 · 모래 단계 · 치유 · 끊김 · 포자 수명. 무리 번호 · 자리 · 타이머 · 나이는 2챕터 것(c2G c2R c2T c2T2 c2Age)'] +
        [f'scoreboard objectives add {o} dummy' for o in OBJ] +
        ['# 피해(원피해) · 예고(틱) · 간격(틱) · 모래 순환 · 치유 · 포자 · 맴돌기 상수'] +
        [f'scoreboard players set #{k} tmp {v}' for k, v in T.items()]))
    w('cm/c3/uninstall', '\n'.join(f'scoreboard objectives remove {o}' for o in OBJ))

    w('cm/c3/world', '''
# 3챕터 몹 공용, 매 틱 두뇌보다 먼저 (cm/world). 한 틱 피격 제한 · 같은 틱 시작 표시 · 포자 피해 표시
scoreboard players set #c3FuHit tmp 0
scoreboard players set #c3EmHit tmp 0
scoreboard players set #c3SbHit tmp 0
execute if entity @e[tag=rlk_c3fresh,limit=1] run tag @e[tag=rlk_c3fresh] remove rlk_c3fresh
execute if entity @e[tag=rlk_c3pz,limit=1] run tag @e[tag=rlk_c3pz] remove rlk_c3pz
execute unless entity @e[tag=rlk_c2vec,limit=1] at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2vec","rlk_cmglob"]}
''')

    # ---- swarm hit feel (chapter-2 blocks, ns c3)
    c2.swarm_hurt(w, 'c3', extra=['execute if entity @s[tag=rlk_cm_cw] run function rlk:cm/cw/interrupt'])
    c2.swarm_cancel(w, 'c3', extra=['execute if entity @s[tag=rlk_cm_cw] run function rlk:cm/cw/stop'])
    c2.rig_frozen(w, 'c3')
    c2.swarm_death(w, 'c3', ids=A_IDS, label='3챕터',
                   pop_fx=['particle minecraft:poof ~ ~0.7 ~ 0.3 0.35 0.3 0.05 12 normal',
                           'particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.5 ~ 0.35 0.3 0.35 0.1 14 normal',
                           'particle minecraft:composter ~ ~0.8 ~ 0.35 0.4 0.35 0.1 10 normal',
                           'particle minecraft:crit ~ ~0.9 ~ 0.3 0.4 0.3 0.4 8 normal'],
                   pop_title='# 터짐: 연기 · 모래 · 풀빛 포자 · 소리, 부품 제거',
                   pop_snd=('pop', 'minecraft:entity.firework_rocket.blast', 0.6, 1.3),
                   clean_pre=['# 포자 주머니(fp)는 두뇌가 아니라서 여기서 한 틱씩 돈다(마지막 몹이 죽은 뒤에도 사라질 때까지)',
                              'execute as @e[tag=rlk_c3pod] at @s run function rlk:cm/fp/tick'])
    c2.kill_cue(w, 'c3', label='3챕터', pre=[],
                fx=['execute at @e[tag=rlk_body,limit=1] run particle minecraft:composter ~ ~1 ~ 0.9 0.5 0.9 0.2 24 normal',
                    'execute at @e[tag=rlk_body,limit=1] run particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.4 ~ 0.9 0.2 0.9 0.2 20 normal'],
                note_title='# 3챕터 몹 처치 기록 (@s = 죽는 두뇌, combat/apply 에서). 10틱 안에 3마리(2챕터와 같은 시계) → 다중 처치 신호')
    c2.true_hit(w, 'c3', elem=7)

    # ---- spawning helpers / stats
    st = ['# 3챕터 몹 1레벨 체력 · 처치 경험치 (@s = 새 두뇌, room/mob_init 에서). 정예 id 도 여기서 rlk_c3 를 받음']
    for i in B_IDS:
        st.append(f'execute if entity @s[tag=rlk_cm_{i}] run tag @s add rlk_c3')
    st.append('execute if entity @s[tag=rlk_c3] run function rlk:cm/c3/stats')
    w('cm/c3/stats_chk', '\n'.join(st))
    st = ['scoreboard players set #mad tmp 0']
    for i, (hp, xp) in STATS.items():
        st.append(f'execute if entity @s[tag=rlk_cm_{i}] run scoreboard players set #mhp tmp {hp}')
        st.append(f'execute if entity @s[tag=rlk_cm_{i}] run scoreboard players set @s xpDrop {xp}')
    w('cm/c3/stats', '\n'.join(st))
    w('cm/c3/turn', '''
# 무리 공통 각도 (0.01°, @s = 무리원): (게임 시간 % 240) × 1.5° + 자리 × 360° / 무리 크기 + 무리 번호마다 다른 시작각 → #c3a
execute store result score #c3a tmp run time query gametime
scoreboard players operation #c3a tmp %= #c3c240 tmp
scoreboard players operation #c3a tmp *= #c3Orb tmp
scoreboard players operation #c3s tmp = @s c2R
scoreboard players operation #c3s tmp *= #c3c36000 tmp
execute if score @s c3N matches 1.. run scoreboard players operation #c3s tmp /= @s c3N
scoreboard players operation #c3a tmp += #c3s tmp
scoreboard players operation #c3s tmp = @s c2G
scoreboard players operation #c3s tmp *= #c3c7919 tmp
scoreboard players operation #c3a tmp += #c3s tmp
scoreboard players operation #c3a tmp %= #c3c36000 tmp
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get #c3a tmp
''')
    w('cm/c3/col_ok', '''
# 한 칸 기둥이 지나갈 수 있는가 (실행 위치 = 발 높이의 그 칸): 몸 · 머리 칸이 비고(벽 · 문 · 철창 · 물 아님) 발밑 1~2칸 안에 바닥. 한 칸 오르막도 됨
execute if block ~ ~0.4 ~ #rlk:dash_pass if block ~ ~1.4 ~ #rlk:dash_pass unless block ~ ~-0.6 ~ #rlk:cm_pass run return 1
execute if block ~ ~0.4 ~ #rlk:dash_pass if block ~ ~1.4 ~ #rlk:dash_pass unless block ~ ~-1.6 ~ #rlk:cm_pass run return 1
execute unless block ~ ~0.4 ~ #rlk:cm_pass if block ~ ~1.4 ~ #rlk:dash_pass if block ~ ~2.4 ~ #rlk:dash_pass run return 1
return 0
''')

    # ---- room plan + slot spawner
    w('cm/c3/plan', '''
# 3챕터 방 구성 (@s = 구역 표식, room/mob_wave 에서). #mobN(방 크기 규칙의 수) → 무리 목록 rlk:c3 plan, #mobN = 무리 수.
# 구역 data.sd 1 = 사막(모래 전갈 새끼 · 성수 전갈), 0 = 우림(둥실 버섯 · 재구성자). 정예 id 는 실행 시점에 부름
data modify storage rlk:c3 plan set value []
scoreboard players operation #c3N tmp = #mobN tmp
execute store result score #c3sd tmp run data get entity @s data.sd
execute if score #c3N tmp matches ..2 run function rlk:cm/c3/plan_small
execute if score #c3N tmp matches 3.. if score #mapIdx room matches ..1 run function rlk:cm/c3/plan_a
execute if score #c3N tmp matches 3.. if score #mapIdx room matches 2.. run function rlk:cm/c3/plan_b
execute if score #c3N tmp matches 3.. if score #mapIdx room matches 4.. run function rlk:cm/c3/plan_c
execute store result score #mobN tmp run data get storage rlk:c3 plan
''')
    w('cm/c3/plan_add', '''
$data modify storage rlk:c3 plan append value {id:"$(id)",n:0}
execute store result storage rlk:c3 plan[-1].n int 1 run scoreboard players get #c3n tmp
''')
    w('cm/c3/plan_small', '''
# 아주 작은 방: 무리 하나. 우림 = 버섯 무리, 사막 = 전갈 새끼(5~6번째 맵은 용병 무리)
scoreboard players set #c3n tmp 5
execute if score #c3sd tmp matches 0 run return run function rlk:cm/c3/plan_add {id:"g_fu"}
scoreboard players set #c3n tmp 6
execute if score #mapIdx room matches ..3 run return run function rlk:cm/c3/plan_add {id:"g_sb"}
scoreboard players set #c3n tmp 3
function rlk:cm/c3/plan_add {id:"g_em"}
''')
    w('cm/c3/plan_a', '''
# 1~2번째 맵: 우림 = 버섯 무리 둘, 사막 = 전갈 새끼 무리 + 용병 무리 (방이 클수록 무리가 커짐)
execute if score #c3sd tmp matches 1 run return run function rlk:cm/c3/plan_a_d
scoreboard players set #c3n tmp 5
execute if score #c3N tmp matches 6.. run scoreboard players set #c3n tmp 6
execute if score #c3N tmp matches 8.. run scoreboard players set #c3n tmp 7
function rlk:cm/c3/plan_add {id:"g_fu"}
scoreboard players set #c3n tmp 5
execute if score #c3N tmp matches 7.. run scoreboard players set #c3n tmp 6
function rlk:cm/c3/plan_add {id:"g_fu"}
''')
    w('cm/c3/plan_a_d', '''
scoreboard players set #c3n tmp 6
execute if score #c3N tmp matches 6.. run scoreboard players set #c3n tmp 7
execute if score #c3N tmp matches 8.. run scoreboard players set #c3n tmp 8
function rlk:cm/c3/plan_add {id:"g_sb"}
scoreboard players set #c3n tmp 3
execute if score #c3N tmp matches 7.. run scoreboard players set #c3n tmp 4
function rlk:cm/c3/plan_add {id:"g_em"}
''')
    w('cm/c3/plan_b', '''
# 3~6번째 맵의 바탕: 무리 둘(우림 = 버섯 + 용병, 사막 = 전갈 새끼 + 용병) + 3~4번째 맵은 정예 하나(우림 = 재구성자, 사막 = 성수 전갈 · 독수리 반반)
scoreboard players set #c3n tmp 5
execute if score #c3N tmp matches 7.. run scoreboard players set #c3n tmp 6
execute if score #c3sd tmp matches 0 run function rlk:cm/c3/plan_add {id:"g_fu"}
scoreboard players set #c3n tmp 6
execute if score #c3N tmp matches 7.. run scoreboard players set #c3n tmp 7
execute if score #c3sd tmp matches 1 run function rlk:cm/c3/plan_add {id:"g_sb"}
scoreboard players set #c3n tmp 3
execute if score #c3N tmp matches 6.. run scoreboard players set #c3n tmp 4
function rlk:cm/c3/plan_add {id:"g_em"}
execute if score #mapIdx room matches 4.. run return 0
scoreboard players set #c3n tmp 1
execute if score #c3sd tmp matches 0 run return run function rlk:cm/c3/plan_add {id:"pc"}
execute store result score #c3r tmp run random value 1..2
execute if score #c3r tmp matches 1 run function rlk:cm/c3/plan_add {id:"cs"}
execute if score #c3r tmp matches 2 run function rlk:cm/c3/plan_add {id:"rv"}
''')
    w('cm/c3/plan_c', '''
# 5~6번째 맵: plan_b 의 무리 둘 + 정예 둘(우림 = 재구성자 + 독수리, 사막 = 성수 전갈 + 독수리) + 맑은물 술사
scoreboard players set #c3n tmp 1
execute if score #c3sd tmp matches 0 run function rlk:cm/c3/plan_add {id:"pc"}
execute if score #c3sd tmp matches 1 run function rlk:cm/c3/plan_add {id:"cs"}
function rlk:cm/c3/plan_add {id:"rv"}
function rlk:cm/c3/plan_add {id:"cw"}
''')
    w('cm/c3/room_slot', f'''
# 3챕터 방 몹: 계획(rlk:c3 plan)의 맨 앞 무리를 실행 위치에 (room/mob_summon 에서). 몸 쪽을 보고 선다
execute unless data storage rlk:c3 plan[0] run data modify storage rlk:c3 plan append value {{id:"g_em",n:3}}
data modify storage rlk:c3 cur set from storage rlk:c3 plan[0]
data remove storage rlk:c3 plan[0]
execute store result score #c3Size tmp run data get storage rlk:c3 cur.n
scoreboard players set #c3SizeSet tmp 1
execute if entity @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:cm/c3/spawn_id with storage rlk:c3 cur
execute unless entity @e[tag=rlk_body,limit=1] run function rlk:cm/c3/spawn_id with storage rlk:c3 cur
scoreboard players set #c3SizeSet tmp 0
execute as @e[tag=rlk_newmob] run function rlk:room/mob_init
particle minecraft:poof ~ ~1 ~ 0.6 0.6 0.6 0.02 16
{w.snd('arrive', 'minecraft:block.azalea_leaves.break', 0.7, 0.8)}
''')
    w('cm/c3/spawn_id', '''
# 소환 id 를 실행 시점에 풀어 부름 (정예 id 는 다른 쪽 파일이라 직접 참조하지 않음)
$function rlk:cm/spawn/$(id)
''')


# ---------------------------------------------------------------- dispatch + shared-file hooks
def finish(w):
    tick = ['# 3챕터 두뇌 한 틱 (@s, at @s; cm/tick 에서, 플레이어가 쓰러져 있지 않을 때). 정예(B)는 자기 연결 줄로 돈다',
            'scoreboard players add @s c2Age 1',
            'execute if score @s c2Age matches 1 if entity @s[tag=rlk_c3a] run function rlk:cm/c2/first']
    init = ['# 3챕터 두뇌 준비 (@s = 새 두뇌, at @s; cm/init 끝에서, #cid = cmId)',
            'scoreboard players set @s c2Age 0',
            'execute unless entity @s[tag=rlk_c3a] run return 0',
            'scoreboard players set @s cmAH 0',
            'scoreboard players set @s cmAR 0',
            'scoreboard players set @s cmAP -1',
            'execute store result score @s cmAF run random value 0..47']
    vis = []
    for i in A_IDS:
        tick.append(f'execute if entity @s[tag=rlk_cm_{i}] run return run function rlk:cm/{i}/tick')
        init.append(f'execute if entity @s[tag=rlk_cm_{i}] run return run function rlk:cm/{i}/init')
        vis.append(f'execute if entity @s[tag=rlk_cm_{i}] run return run function rlk:cm/{i}/rig/tick')
    w('cm/c3/tick', '\n'.join(tick))
    w('cm/c3/init', '\n'.join(init))
    w('cm/c3/vis', '# 3챕터 몹 모습 (@s = 두뇌, at @s; cm/vis 맨 앞)\n' + '\n'.join(vis))
    # {t:"help"} of rlk:cm/test: this chapter's section (patch_shared rebuilds cm/test_help from the sections on disk)
    assert [i for i, _ in TEST_ROWS] == list(A_IDS + B_IDS + GROUPS), 'TEST_ROWS must list every chapter-3 spawn id'
    w(help_lib.CM_SECTION.format(n=3), help_lib.cm_test_section(3, TEST_ROWS))


def patch_shared(fn_root):
    """Idempotent hook lines; anchors are chapter-1 lines (or the chapter-2 load line), so either generator can run
    first and running both again changes nothing."""
    P = c2.Patcher(fn_root)
    P.before('cm/tick', '# 이동 멈춤(사거리 안 · 차지 중): 넉백은 그대로 받는다',
             'execute if score #cmDown tmp matches 0 if entity @s[tag=rlk_c3] run function rlk:cm/c3/tick')
    P.prefix('cm/vis', 'execute if entity @s[tag=rlk_c3a] run return run function rlk:cm/c3/vis')
    P.prefix('cm/flash', 'execute if entity @s[tag=rlk_c3a] run return run function rlk:cm/c3/hurt')
    P.after('cm/init', 'execute if entity @s[tag=rlk_cm_sh] run function rlk:cm/sh/rig/rebuild',
            'execute if entity @s[tag=rlk_c3] run function rlk:cm/c3/init')
    P.after('cm/cancel', 'function rlk:cm/pose_s', 'execute if entity @s[tag=rlk_c3a] run function rlk:cm/c3/cancel')
    P.prefix('cm/clean', 'function rlk:cm/c3/clean')
    P.before('cm/world', 'execute as @e[tag=rlk_cmb] at @s run function rlk:cm/tick',
             'execute if entity @e[tag=rlk_c3,limit=1] run function rlk:cm/c3/world')
    # combat: pods only mark themselves; burrowed hatchlings take nothing; multi-kill note
    P.after('combat/apply', 'execute if entity @s[tag=rlk_rd_object] run return run function rlk:boss/raiden/object/on_hit',
            'execute if entity @s[tag=rlk_c3pod] run return run function rlk:cm/fp/hit')
    P.after('combat/apply', 'execute if entity @s[tag=rlk_c3pod] run return run function rlk:cm/fp/hit',
            'execute if entity @s[tag=rlk_c3bur] run return 0')
    P.before('combat/apply', 'execute if score #mobHP tmp matches ..0 run function rlk:combat/heal_orb_roll',
             'execute if score #mobHP tmp matches ..0 if entity @s[tag=rlk_c3] run function rlk:cm/c3/kill_note')
    # room: chapter-3 roster (chapters 1, 2 and 4+ unchanged; #mobTmp 1 still means the old temporary mobs)
    P.before('room/mob_summon', 'execute unless score #mobTmp room matches 1 run return run function rlk:cm/summon_c1',
             'execute if score #chapter room matches 3 unless score #mobTmp room matches 1 run return run function rlk:cm/c3/room_slot')
    P.before('room/mob_wave', 'function rlk:room/mob_loop',
             'execute if score #chapter room matches 3 unless score #mobTmp room matches 1 run function rlk:cm/c3/plan')
    P.before('room/mob_init', '# 레벨 = (챕터 - 1) × 6 + 이번 맵의 순서(1~6). 체력은 레벨에 따라 늘어남(mob/level_apply), 공격력은 맞을 때 레벨로 보정',
             'execute if entity @s[tag=rlk_cmb] run function rlk:cm/c3/stats_chk')
    P.after('load', 'function rlk:cm/c2/load', 'function rlk:cm/c3/load')
    P.after('uninstall', 'function rlk:cm/c2/uninstall', 'function rlk:cm/c3/uninstall')
    # cm/test {t:"help"}: chapter-1 list + every cm/c<N>/test_help on disk (order-independent; any chapter generator rewrites it)
    if help_lib.cm_test_help(P.root):
        P.changed.append('cm/test_help')
    return P.changed
