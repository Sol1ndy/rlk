"""The revival stage (plan 7.5-7.7, 3.4; AP-REV): T1 (service 20), the Heart of the Oasis (AP:heart/**), the stage
(AP:rev/**: waves, spawn points, the stage clock, the time-out, the failure strikes, the phase-2 HUD and bar), the failure
strike (service 40) and the CS (service 60). The organisms and the walls are org.py's.

The Heart is the AP-ORG object (fixed UUIDs, om/heart/**; its marker rlk_mb_ap_heart is summoned by om/heart/spawn/<state>):
- E / phase 1: heart/p1_hang (the entrance state: the upright egg in the vine hand 9 b up, the cradle under the floor),
  heart/p1_up (E t70: heart_up, drawn up into the canopy over 30 t, then the heart_hang sway), heart/p1_respawn (the
  canopy state);
- T1: cradle_rise t45, heart_lower t50, heart_drop t100 (land t106, the beam), then heart_idle;
- phase 2: lying in the full cradle (om/heart/spawn/play on a reload / the test jumps), heart_gain / heart_hit on every
  progress change, heart_wither in a failure strike;
- CS: heart_blaze 0-24, heart_lift from t24 (the white-out hides the cradle going), the 「불씨」 ember, egg_green + the
  vine hand's wrap at t76, gone at t92 (the orb fades into the Warden).
The core steps the Heart's clips (and the walls') every module tick while they exist (AP:obj/tick, AP-I2 RREV-1).

Texts: only neutral info, the real game's prompt 「마물을 처치해서 소생 진행도를 올리세요」 (v2 39.6 s, v3) and the instant-kill
warning of the failure strike (the no-tips rule, ap_contract 2.5; no first-time hints).
"""
import math

from .api import Pattern, Gen, BODY, ORGS, K
from . import api as A

L = A.L
n = L.num
R = A.REV
T = A.TXT
NS = A.NS
CX, CY, CZ = A.CENTRE[0], A.CY, A.CENTRE[2]
CEN = f'{n(CX)} {CY} {n(CZ)}'
AT_CEN = f'positioned {CEN}'
FP = A.FOOTPRINT
HANG = FP['hang']
BULB_Y = float(FP['bulb_box']['centre_y'])                 # the lying bulb's centre above the floor (phase 2)
EGG_CS_Y = float(HANG['cs_y']) + 1.2                       # the egg's centre in the CS (its lowest point at cs_y)
AT_BULB = f'positioned {n(CX)} {n(CY + BULB_Y)} {n(CZ)}'
AT_EGG_CS = f'positioned {n(CX)} {n(CY + EGG_CS_Y)} {n(CZ)}'
UU = {d['name']: f'{A.OBJ_BLOCK}{int(d["idx"]):02x}' for d in A.ORG['objects']['heart']['displays']}
BULB = UU['heart_bulb']
HEAD = '# AP-REV (plan 7.5-7.7, 3.4): the revival stage.'
SPECIALS = tuple(A.SPECIAL_BAG)                            # guard nest nurt pred (the shuffle bag of waves 6+)
CAP = R['cap']
P_LEN = {'t1': A.T1_LEN, 'fail': A.FAIL_LEN, 'cs': A.CS_LEN}
PATTERNS = [
    Pattern(20, 't1', '소생 단계 진입', 'service', 'sink_revive', length=A.T1_LEN, max_len=A.T1_LEN + 4, recover=1),
    Pattern(40, 'fail', '소생 실패', 'service', None, length=A.FAIL_LEN, max_len=A.FAIL_LEN + 4, recover=1, hooks=('reload',)),
    Pattern(60, 'cs', '소생', 'service', None, length=A.CS_LEN, max_len=A.CS_LEN + 4, recover=20),
]
STAGE_ZERO = ('#apHt', '#apWave', '#apClk', '#apWT', '#apTo', '#apToT', '#apFail', '#apStage', '#apAlive', '#apSlots',
              '#apOArg', '#apOrgN', '#apHtP', '#apWid', '#apBg0', '#apBg1', '#apBg2', '#apBg3', '#apDNear', '#apPChain',
              '#apClk2', '#apClk8', '#apClk40', '#apq40L')
# T1 (plan 7.5; played ticks of the service clock = the sink_revive clip tick)
T1 = dict(chunks=(20, 30), park=45, cradle=45, lower=50, drop=100, land=100 + A.org_clip('heart', 'heart_drop')['events']['land'],
          goal=108, marks=116, end=A.T1_LEN)
assert T1['land'] == 106 and T1['marks'] + 20 == T1['end'], T1
# the failure strike (plan 3.4) and the CS (plan 7.7)
FAIL = dict(strike=20, end=A.FAIL_LEN)
CS = dict(white=24, cradle_gone=30, revival=32, ember=64, green=76, flash=A.CS_HEAL_T, burst=92, reveal=132, targetable=150,
          end=A.CS_LEN, whiteout_hold=28)
TWIG = A.EMBER_TWIG
EMBER_LEN = math.dist(TWIG[:3], (CX, CY + EGG_CS_Y, CZ))


def sc(name, v):
    return f'scoreboard players set {name} mb {int(v)}'


def emit(g):
    F = g.fn
    fx, snd = K.fx, K.snd
    # ================================================================ the Heart
    g.w('heart/p1_hang', [HEAD, '# E t0 (seq/entrance/setup): the Heart\'s entrance state at the centre: the upright egg (scale 0.7) held by',
                          f'# the vine hand {HANG["entrance_y"]} b up, the cradle under the floor (summons the marker rlk_mb_ap_heart too).',
                          f'execute {AT_CEN} rotated 0 0 run function {NS}om/heart/spawn/entrance'])
    g.w('heart/p1_up', [HEAD, '# E t70 (and seq/entrance/done, idempotent): the Heart drawn up into the canopy (heart_up, 30 t, then the',
                        '# heart_hang sway; the core steps the clips: obj/tick); without a Heart (reload, the test skips) the canopy',
                        '# state at once.',
                        f'execute unless entity {BULB} run return run {F("heart/p1_respawn")}',
                        f'execute as {BULB} if entity @s[tag=rlk_mb_ap_hup] run return 0',
                        f'function {NS}om/heart/play/heart_up', f'tag {BULB} add rlk_mb_ap_hup'])
    g.w('heart/p1_respawn', [HEAD, '# The Heart hanging in the canopy (phase 1; a reload in phase 1, the phase-1 test jumps).',
                             f'execute {AT_CEN} rotated 0 0 run function {NS}om/heart/spawn/canopy', f'tag {BULB} add rlk_mb_ap_hup'])
    g.w('heart/play_state', [HEAD, '# The Heart lying in the full cradle at the centre (phase 2 ready: reload, the test jumps).',
                             f'execute {AT_CEN} rotated 0 0 run function {NS}om/heart/spawn/play'])
    g.w('heart/clear', [HEAD, '# The Heart marker and every Heart display go (idempotent, any executor).', f'function {NS}om/heart/kill'])
    g.w('heart/add', [HEAD, '# Macro {v}: progress + v (clamp 10000; the stage tick starts the CS at 10000): the gain swell, the sparkle and',
                      '# the chime (its pitch rises with the progress: #apHt first, requests/fx.md RFX-2).',
                      '$scoreboard players add #apHt mb $(v)',
                      f'execute if score #apHt mb matches {R["win"] + 1}.. run scoreboard players set #apHt mb {R["win"]}',
                      f'execute {AT_BULB} run {fx("heart_gain")}', f'execute {AT_BULB} run {snd("heart_gain")}',
                      f'execute if score #apStage mb matches 1 if entity {BULB} run function {NS}om/heart/play/heart_gain', sc('#apHudQ', 1)])
    g.w('heart/sub', [HEAD, '# Macro {v}: progress - v (clamp 0; the stage tick starts the failure strike at 0): the flinch, red-gold motes,',
                      '# the hit sound. (The bossui\'s white recent-loss trail shows the loss by itself.)',
                      '$scoreboard players remove #apHt mb $(v)',
                      'execute if score #apHt mb matches ..-1 run scoreboard players set #apHt mb 0',
                      f'execute {AT_BULB} run {fx("heart_hit")}', f'execute {AT_BULB} run {snd("heart_hit")}',
                      f'execute if score #apStage mb matches 1 if entity {BULB} run function {NS}om/heart/play/heart_hit', sc('#apHudQ', 1)])

    # ================================================================ the stage
    g.w('rev/ready', [HEAD, '# Phase 2 ready (the test jumps through ph/ready_2): the Heart in the full cradle, the stage markers, the',
                      '# dressing (the gold swirl, the ley lines), progress 2700 (the stage clocks start in rev/start).',
                      F('heart/play_state'), F('org/marks'),
                      f'execute {AT_CEN} run {K.dress("swirl", r=FP["swirl_r"])}', f'execute {AT_CEN} run {K.dress("ley", n=7)}',
                      sc('#apHt', R['start']), sc('#apHudQ', 1)])
    restart = [sc('#apClk', 0), sc('#apTo', 0), sc('#apToT', 0), sc('#apStage', 1), sc('#apSlots', 0),
               sc('#apBg0', 0), sc('#apBg1', 0), sc('#apBg2', 0), sc('#apBg3', 0), sc('#apHudQ', 1)]
    g.w('rev/start', [HEAD, '# The stage (re)starts from wave 1 (the test jumps, a failure restart): the clocks and the time-out reset; the',
                      '# first wave is due now (its spawn markers, then the organisms 20 t later).',
                      sc('#apWave', 0), sc('#apWT', R['wave_clock']), F('org/consts')] + restart)
    g.w('rev/start_t1', [HEAD, '# T1 t136: the stage starts with wave 1 (marked at T1 t116, emerging now); the stage clock from 0.',
                         sc('#apWave', 1), sc('#apWT', 0), F('org/consts')] + restart)
    g.w('rev/tick', [
        HEAD, '# @s = body (phase 2, the module tick; the core stepped the Heart\'s and the walls\' clips before it). The stage stops',
        '# while a service (fail / CS) runs. Order: the clocks, the walls\' clocks, the pending spawns, the organisms, the',
        '# bolts, the Heart limits (CS / failure strike), the',
        '# waves (every 8 t: due on <= 1 alive or the wave clock; a due wave waits for the cap), the',
        '# time-out, the ambience.',
        'execute if score #apPid mb matches 1.. run return 0',
        'execute unless score #apStage mb matches 1 run return 0',
        'scoreboard players add #apClk mb 1', 'scoreboard players add #apWT mb 1',
        'scoreboard players operation #apClk2 mb = #apClk mb', 'scoreboard players operation #apClk2 mb %= #apK2 mb',
        'scoreboard players operation #apClk8 mb = #apClk mb', 'scoreboard players operation #apClk8 mb %= #apK8 mb',
        'scoreboard players operation #apClk40 mb = #apClk mb', 'scoreboard players operation #apClk40 mb %= #apK40 mb',
        F('wall/tick'), F('org/pend_tick'),
        F('org/tick'),
        F('org/bolts'),
        f'execute if score #apHt mb matches {R["win"]}.. run return run {Gen.svc("req_cs")}',
        f'execute if score #apHt mb matches ..0 run return run {Gen.svc("req_fail")}',
        f'execute if score #apClk8 mb matches 0 run {F("rev/wave_due")}',
        f'execute if score #apWave mb matches 0 unless score #apClk8 mb matches 0 run {F("rev/wave_due")}',
        f'execute if score #apClk mb matches {R["timeout"]}.. run {F("rev/timeout")}',
        f'execute if score #apClk mb matches 1.. if score #apClk40 mb matches 0 {AT_CEN} run {fx("gold_motes")}',
        'scoreboard players operation #apM mb = #apClk mb', 'scoreboard players operation #apM mb %= #apK10 mb',
        f'execute if score #apM mb matches 0 {AT_CEN} run {fx("haze_withered")}'])
    g.w('rev/wave_due', [
        HEAD, f'# Every 8 t: the next wave is due when <= {R["wave_left"]} organisms are alive (pending spawns count) or {R["wave_clock"]} t after the last;',
        f'# it waits while alive + its size > the cap {CAP} (the time-out spawns ignore the cap).',
        'execute store result score #apAlive mb if entity @e[type=minecraft:husk,tag=rlk_mb_ap_org,tag=!rlk_mb_ap_dying]',
        'execute store result score #apX mb if entity @e[type=minecraft:marker,tag=rlk_mb_ap_ospawn]',
        'scoreboard players operation #apAlive mb += #apX mb',
        sc('#apX', 0),
        f'execute if score #apWT mb matches {R["wave_clock"]}.. run scoreboard players set #apX mb 1',
        f'execute if score #apAlive mb matches ..{R["wave_left"]} run scoreboard players set #apX mb 1',
        'execute if score #apX mb matches 0 run return 0',
        sc('#apY', 4),
        'execute if score #apWave mb matches 1.. run scoreboard players set #apY mb 5',
        f'execute if score #apWave mb matches {len(A.WAVES) + 1}.. run scoreboard players set #apY mb 6',
        'scoreboard players operation #apY mb += #apAlive mb',
        f'execute if score #apY mb matches {CAP + 1}.. run return 0',
        F('rev/wave_go')])
    g.w('rev/wave_go', [HEAD, '# A new wave: the index, the wave clock, its spawn markers.', 'scoreboard players add #apWave mb 1', sc('#apWT', 0),
                        sc('#apHudQ', 1), F('rev/wave_marks')])
    g.w('rev/wave_t1', [HEAD, '# T1 t116: wave 1\'s spawn markers (the organisms emerge at t136 with the stage).', sc('#apWave', 1),
                        sc('#apWT', 0), F('rev/wave_marks')])
    marks = [HEAD, '# The spawn markers of wave #apWave (a new wave, or /reload: the current one again; plan 7.6.3): 4 basics on 4',
             '# distinct r 12 points never closer than 4 b to the player (wave 1: 2 melee + 2 ranged, later 50 / 50), then the',
             '# wave\'s specials on their points (수호 nearest 10 b from the player, 둥지 nearest the player, 포식성 farthest, 양육 on',
             '# the r 7 point nearest the new basics); waves 2-5 the table, 6 one from the shuffle bag, 7+ two.',
             F('rev/cands')]
    for j in range(4):
        marks.append(f'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_cand,sort=random,limit=1] at @s run {F(f"rev/mk_basic{j}")}')
    for wv, rec in enumerate(A.WAVES, start=1):
        for k in rec.get('special', []):
            marks.append(f'execute if score #apWave mb matches {wv} run {F("rev/mk_" + k)}')
    marks += [f'execute if score #apWave mb matches {len(A.WAVES) + 1}.. run {F("rev/bag")}',
              f'execute if score #apWave mb matches {len(A.WAVES) + 2}.. run {F("rev/bag")}',
              'kill @e[type=minecraft:marker,tag=rlk_mb_ap_cand]']
    g.w('rev/wave_marks', marks)
    melee = int(A.WAVES[0].get('melee', 2))
    for j in range(4):
        arg = 0 if j < melee else 1
        g.w(f'rev/mk_basic{j}', [f'# @s = a free spawn point: basic {j + 1} of the wave (wave 1: {"melee" if arg == 0 else "ranged"}, else 50 / 50).',
                                 'tag @s remove rlk_mb_ap_cand', 'tag @s add rlk_mb_ap_cused',
                                 f'execute if score #apWave mb matches 1 run return run function {NS}org/mark {{k:{A.KIND_ID["basic"]},a:{arg}}}',
                                 f'function {NS}org/mark {{k:{A.KIND_ID["basic"]},a:-1}}'])
    cand = [HEAD, '# The 8 spawn points on r 12 as candidate markers (rlk_mb_ap_cand), minus those within 4 b of the player.',
            'kill @e[type=minecraft:marker,tag=rlk_mb_ap_cand]', 'kill @e[type=minecraft:marker,tag=rlk_mb_ap_cused]']
    for x, y, z in A.ORG_SPAWN:
        cand.append(f'summon minecraft:marker {n(x, 3)} {CY} {n(z, 3)} {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_cand"]}}')
    cand.append('execute as @e[type=minecraft:marker,tag=rlk_mb_ap_cand] at @s if entity @e[tag=rlk_body,distance=..4] run kill @s')
    g.w('rev/cands', cand)
    pool = ('# the free points first (no basic of this wave there), else the used ones',
            'execute unless entity @e[type=minecraft:marker,tag=rlk_mb_ap_cand] run tag @e[type=minecraft:marker,tag=rlk_mb_ap_cused] add rlk_mb_ap_cand')
    for k in ('guard', 'destr'):
        g.w(f'rev/mk_{k}', [f'# The {A.KIND_KO[k]}: on the point whose distance from the player is nearest 10 b (8-12, else 6-14, else any).', *pool,
                            'tag @e[type=minecraft:marker] remove rlk_mb_ap_cpk',
                            'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_cand] at @s if entity @e[tag=rlk_body,distance=8..12] run tag @s add rlk_mb_ap_cpk',
                            'execute unless entity @e[type=minecraft:marker,tag=rlk_mb_ap_cpk] as @e[type=minecraft:marker,tag=rlk_mb_ap_cand] at @s '
                            'if entity @e[tag=rlk_body,distance=6..14] run tag @s add rlk_mb_ap_cpk',
                            'execute unless entity @e[type=minecraft:marker,tag=rlk_mb_ap_cpk] run tag @e[type=minecraft:marker,tag=rlk_mb_ap_cand] '
                            'add rlk_mb_ap_cpk',
                            f'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_cpk,sort=random,limit=1] at @s run {F(f"rev/put_{k}")}',
                            'tag @e[type=minecraft:marker] remove rlk_mb_ap_cpk'])
    g.w('rev/mk_nest', ['# The 둥지: on the free point nearest the player.', *pool,
                        f'execute at {A.PLAYER} as @e[type=minecraft:marker,tag=rlk_mb_ap_cand,sort=nearest,limit=1] at @s run {F("rev/put_nest")}'])
    g.w('rev/mk_pred', ['# The 포식성: on the free point farthest from the player.', *pool,
                        f'execute at {A.PLAYER} as @e[type=minecraft:marker,tag=rlk_mb_ap_cand,sort=furthest,limit=1] at @s run {F("rev/put_pred")}'])
    nurt = ['# The 양육: on the r 7 point (of the 8 bearings) nearest one of this wave\'s basics, never within 4 b of the player.',
            'kill @e[type=minecraft:marker,tag=rlk_mb_ap_ncand]']
    for x, y, z in A.NURT_SPAWN:
        nurt.append(f'summon minecraft:marker {n(x, 3)} {CY} {n(z, 3)} {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_ncand"]}}')
    nurt += ['execute as @e[type=minecraft:marker,tag=rlk_mb_ap_ncand] at @s if entity @e[tag=rlk_body,distance=..4] run kill @s',
             f'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_ospawn,scores={{apK={A.KIND_ID["basic"]}}},sort=random,limit=1] at @s as '
             f'@e[type=minecraft:marker,tag=rlk_mb_ap_ncand,sort=nearest,limit=1] at @s run function {NS}org/mark {{k:{A.KIND_ID["nurt"]},a:-1}}',
             f'execute unless entity @e[type=minecraft:marker,tag=rlk_mb_ap_ospawn,scores={{apK={A.KIND_ID["nurt"]}}}] as '
             f'@e[type=minecraft:marker,tag=rlk_mb_ap_ncand,sort=random,limit=1] at @s run function {NS}org/mark {{k:{A.KIND_ID["nurt"]},a:-1}}',
             'kill @e[type=minecraft:marker,tag=rlk_mb_ap_ncand]']
    g.w('rev/mk_nurt', nurt)
    for k in ('guard', 'destr', 'nest', 'pred'):
        g.w(f'rev/put_{k}', ['tag @s remove rlk_mb_ap_cand', 'tag @s add rlk_mb_ap_cused',
                             f'function {NS}org/mark {{k:{A.KIND_ID[k]},a:-1}}'])
    bag = [HEAD, f'# One special from the shuffle bag {list(SPECIALS)} (each once before any repeats; #apBg<i> 1 = drawn).',
           f'execute if score #apBg0 mb matches 1 if score #apBg1 mb matches 1 if score #apBg2 mb matches 1 if score #apBg3 mb matches 1 run {F("rev/bag_fill")}',
           'execute store result score #apR mb run random value 0..3']
    for r in range(4):
        for k in range(4):
            i = (r + k) % 4
            bag.append(f'execute if score #apR mb matches {r} if score #apBg{i} mb matches 0 run return run {F(f"rev/bag_{i}")}')
    g.w('rev/bag', bag)
    g.w('rev/bag_fill', [sc(f'#apBg{i}', 0) for i in range(4)])
    for i, k in enumerate(SPECIALS):
        g.w(f'rev/bag_{i}', [sc(f'#apBg{i}', 1), F(f'rev/mk_{k}')])
    g.w('rev/timeout', [HEAD, f'# {R["timeout"]} t into the stage: the warning, a 파괴 at once and then every {R["timeout_every"]} t while fewer than',
                        f'# {R["timeout_alive"] + 1} are alive or coming (time-out spawns ignore the cap).',
                        f'execute if score #apTo mb matches 0 run {F("rev/warn")}',
                        'scoreboard players add #apToT mb 1',
                        f'execute if score #apToT mb matches {R["timeout_every"]}.. run {F("rev/to_spawn")}'])
    g.w('rev/warn', [HEAD, '# The time-out warning (neutral information; plan 7.6.3): the "!" title, the line, the horn.',
                     sc('#apTo', 1), sc('#apToT', R['timeout_every']),
                     K.hud('title', g='warn', t=T['warn_sub'], c=A.WARN_HEX, s='', hold=50),
                     Gen.line(T['warn_line'], A.WARN_HEX, 60), f'execute {AT_CEN} run {snd("timeout_warn")}', sc('#apHudQ', 1)])
    g.w('rev/to_spawn', [sc('#apToT', 0),
                         f'execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_destr,tag=!rlk_mb_ap_dying,limit={R["timeout_alive"]}] run return 0',
                         f'execute if entity @e[type=minecraft:marker,tag=rlk_mb_ap_ospawn,scores={{apK={A.KIND_ID["destr"]}}}] run return 0',
                         F('rev/cands'), F('rev/mk_destr'), 'kill @e[type=minecraft:marker,tag=rlk_mb_ap_cand]',
                         'kill @e[type=minecraft:marker,tag=rlk_mb_ap_cused]'])
    g.w('rev/test_timeout', [HEAD, '# Test 29: the time-out now (the stage clock at its last tick before the warning).',
                             sc('#apClk', R['timeout'] - 1)])
    g.w('rev/reload', [HEAD, '# /reload in phase 2 (every rlk_mb_aux entity is gone): the Heart in the cradle again, the stage markers, the walls',
                       '# cleared (the recorded blocks lost their markers: the safety sweep), the current wave marked again; the progress,',
                       '# the wave index, the clocks and the strikes kept (the core re-made the dressing).',
                       F('heart/play_state'), F('org/marks'), F('wall/clear'), F('org/consts'), sc('#apSlots', 0),
                       f'execute if score #apStage mb matches 1 if score #apWave mb matches 1.. run {F("rev/wave_marks")}',
                       sc('#apHudQ', 1)])
    g.w('rev/pause', [HEAD, '# Pause in phase 2: the walls go (re-cast later); the organisms freeze (the module tick is off).',
                      F('wall/clear'), F('org/freeze')])
    g.w('rev/resume', [HEAD, '# Resume in phase 2: the HUD again (the walls are re-cast by their 둥지).', sc('#apHudQ', 1)])
    g.w('rev/clear', [HEAD, '# The stage gone (cleanup, the phase jumps): the Heart, the stage markers, the pending spawns, the dressing, the',
                      '# stage scores.', F('heart/clear'), F('org/marks_kill'),
                      'kill @e[type=minecraft:marker,tag=rlk_mb_ap_ospawn]', 'kill @e[type=minecraft:marker,tag=rlk_mb_ap_cand]',
                      'kill @e[type=minecraft:marker,tag=rlk_mb_ap_cused]', 'kill @e[type=minecraft:marker,tag=rlk_mb_ap_ncand]',
                      K.dress('clear')] + [sc(k, 0) for k in STAGE_ZERO])
    g.w('rev/bars', [HEAD, '# @s = body (bars hook, phase 2): the gold progress bar (#buHp = #apHt / 10 of 1000, colour 10, no numbers;',
                     '# cm.md 11); the under-bar = the time to the time-out warning (gold), red after it.',
                     'scoreboard players operation #buHp bu = #apHt mb', 'scoreboard players operation #buHp bu /= #c10 mb',
                     'scoreboard players set #buMax bu 1000', 'scoreboard players set #buHpCol bu 10',
                     'scoreboard players set #buNoNum bu 1',
                     f'scoreboard players set #buSub bu {R["timeout"]}', 'scoreboard players operation #buSub bu -= #apClk mb',
                     'execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0',
                     f'scoreboard players set #buSubMax bu {R["timeout"]}',
                     f'scoreboard players set #buSubCol bu {L.ELEM_TO_BU[5]}',
                     f'execute if score #apTo mb matches 1 run scoreboard players set #buSub bu {R["timeout"]}',
                     f'execute if score #apTo mb matches 1 run scoreboard players set #buSubCol bu {L.ELEM_TO_BU[1]}'])
    badges = [f'execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_{k},tag=!rlk_mb_ap_dying,limit=1] run data modify storage rlk:mboss '
              f'extra append value {K.badge(k, True)}' for k in ('guard', 'nest', 'nurt', 'pred', 'destr')]
    g.w('rev/hud', [HEAD, '# @s = body (phase 2, every 4 t or on #apHudQ): line 1 extras (the specials alive as badges, the wave), line 3',
                    '# (소생 진행도 NN%, the failure mark after a strike). Neutral information only.',
                    'data modify storage rlk:mboss extra set value []'] + badges + [
                    'data modify storage rlk:mboss extra append value {text:"  ",color:"#E8E2D0"}',
                    'data modify storage rlk:mboss extra append value {score:{name:"#apWave",objective:"mb"},color:"#E8E2D0"}',
                    'data modify storage rlk:mboss extra append value {text:"웨이브",color:"#E8E2D0"}',
                    'scoreboard players operation #apHtP mb = #apHt mb', 'scoreboard players operation #apHtP mb /= #c100 mb',
                    f'data modify storage rlk:mboss sub set value [{{text:"{T["p2_progress"]} ",color:"{A.HEART_HEX}"}},'
                    f'{{score:{{name:"#apHtP",objective:"mb"}},color:"{A.HEART_HEX}"}},{{text:"%",color:"{A.HEART_HEX}"}}]',
                    'execute if score #apFail mb matches 1.. run data modify storage rlk:mboss sub append value {text:"  "}',
                    f'execute if score #apFail mb matches 1.. run data modify storage rlk:mboss sub append value {K.badge("fail", True)}',
                    sc('#apHudQ', 0)])

    # ================================================================ T1 (service 20, 136 t)
    t1 = TL1 = []
    FLOOR_BODY = f'execute at {BODY} positioned ~ {CY} ~ run'
    TL1 += [Gen.at(T1['chunks'][0], f'{FLOOR_BODY} {fx("root_chunks")}'), Gen.at(T1['chunks'][0], f'{FLOOR_BODY} {snd("p1_dive")}'),
            Gen.at(T1['chunks'][1], f'{FLOOR_BODY} {fx("root_chunks")}'),
            Gen.at(6, Gen.svc('lib_clear')), Gen.at(6, 'scoreboard players set #mbNoLeash mb 1'),
            Gen.at(T1['park'], Gen.svc('park')),
            Gen.at(T1['cradle'], f'function {NS}om/heart/play/cradle_rise'),
            Gen.at(T1['cradle'], f'execute {AT_CEN} run {K.dress("swirl", r=FP["swirl_r"])}'),
            Gen.at(T1['cradle'], f'execute {AT_CEN} run {fx("cradle_dust")}'), Gen.at(T1['cradle'], f'execute {AT_CEN} run {snd("t1_cradle")}'),
            Gen.at(T1['lower'], f'function {NS}om/heart/play/heart_lower'),
            Gen.at(T1['lower'], f'execute positioned {n(CX)} {n(CY + HANG["canopy_y"])} {n(CZ)} run {snd("t1_lower")}'),
            Gen.at(T1['drop'], f'function {NS}om/heart/play/heart_drop'),
            Gen.at(T1['land'], f'execute {AT_CEN} run {fx("heart_beam")}'), Gen.at(T1['land'], f'execute {AT_BULB} run {snd("t1_land")}'),
            Gen.at(T1['land'], F('p/t1/heart_on')),
            Gen.at(T1['goal'], Gen.line(T['p2_goal'], A.HEART_HEX, 100)), Gen.at(T1['goal'], Gen.svc('cine_off')),
            Gen.at(T1['marks'], F('rev/wave_t1')),
            Gen.at((T1['marks'] + 1, T1['end']), F('org/pend_tick')),
            f'execute if score #apPT mb matches {T1["end"]}.. run {F("p/t1/done")}']
    hz10 = ['scoreboard players operation #apM mb = #apPT mb', 'scoreboard players operation #apM mb %= #apK10 mb',
            f'execute if score #apM mb matches 0 {AT_CEN} run {fx("haze_withered")}']
    g.pw('t1', 'start', [HEAD, '# T1 (plan 7.5, 136 t): sink_revive where it stands (the core plays it at 0; its px sets hide the body); t6',
                         '# the libraries cleared; t20 / t30 root chunks; t45 parked, the cradle rises (the gold swirl); t50 the egg lowered;',
                         '# t100 the drop (land t106: the beam, the Heart title, progress 2700, music 2, the ley lines); t108 the goal line,',
                         '# cine off; t116 wave 1\'s spawn markers; t136 phase 2.',
                         Gen.line(T['t1_sink'], '#E8E2D0', 60), Gen.svc('cine_on'), Gen.set_len(A.T1_LEN),
                         f'execute unless entity {BULB} run {F("heart/p1_respawn")}'])
    g.pw('t1', 'tick', [HEAD] + TL1 + hz10)
    g.pw('t1', 'heart_on', [HEAD, '# T1 t106: the Heart objective: its title (FN-6 + the kit title line), the gold progress, music 2, the',
                            '# ley-line dressing, the stage markers.',
                            Gen.svc('title_heart'), K.hud('title', g='heart', t=T['title_heart'], c=A.HEART_HEX, s='', hold=50),
                            f'execute {AT_CEN} run {snd("t1_hud")}', f'execute {AT_CEN} run {K.dress("ley", n=7)}', Gen.svc('music_2'),
                            sc('#apHt', R['start']), F('org/marks'), sc('#apHudQ', 1)])
    g.pw('t1', 'done', [HEAD, Gen.svc('phase_2'), F('rev/start_t1'), Gen.end()])
    g.pw('t1', 'cancel', [HEAD, Gen.svc('cine_off')])

    # ================================================================ the failure strike (service 40, 60 t)
    g.pw('fail', 'start', [
        HEAD, '# 「소생 실패」 (plan 3.4): strike 1 of 2 (the 2nd -> cb/lose: the death path; a Ronova revive restarts the stage at t60);',
        '# every organism bursts with no progress; walls cleared; the Heart withers; the shock ring; the title + the instant-kill',
        f'# warning; t{FAIL["strike"]} the player takes 25 % max HP (non-lethal, no reaction; not after a lose); t{FAIL["end"]} the stage restarts at',
        '# 2700 from wave 1 (no hint line: the no-tips rule).',
        'scoreboard players add #apFail mb 1', sc('#apStage', 0), sc('#apq40L', 0), sc('#apHudQ', 1),
        f'execute if score #apFail mb matches {R["fail_strikes"]}.. run scoreboard players set #apq40L mb 1',
        F('org/burst_all'), F('org/clear'), F('wall/clear'), Gen.svc('lib_clear'),
        f'function {NS}om/heart/play/heart_wither',
        f'execute {AT_CEN} run {fx("shock_ring")}', f'execute {AT_CEN} run {snd("fail_strike")}',
        f'execute if score #apq40L mb matches 0 run {F("p/fail/warn")}',
        f'execute if score #apq40L mb matches 1 run {K.hud("title", g="fail", t=T["fail_title"], c=A.WARN_HEX, s="", hold=50)}',
        Gen.set_len(A.FAIL_LEN),
        f'execute if score #apq40L mb matches 1 run {Gen.svc("lose")}'])
    g.pw('fail', 'warn', [HEAD, '# Strike 1 only: the title with the instant-kill warning and the red line (the lose shows 「소생 실패」 alone;',
                          '# AP-FIX RV-09).',
                          K.hud('title', g='fail', t=T['fail_title'], c=A.WARN_HEX, s=T['fail_line'], hold=50),
                          Gen.line(T['fail_line'], A.WARN_HEX, 80)])
    g.pw('fail', 'strike', [HEAD, '# The wither: 25 % max HP, non-lethal, undodgeable (a DoT), no player-side reaction.',
                            'scoreboard players set #mbNoRx mb 1', *Gen.pl_dot(A.DMG_PM['fail1'], 7, 0)])
    g.pw('fail', 'restart', [HEAD, '# The stage again: 2700, wave 1, the clocks and the time-out reset; the Heart back to its idle look.',
                             sc('#apHt', R['fail_restart']), F('rev/start'),
                             f'execute if entity {BULB} run function {NS}om/heart/look/heart_bulb/idle',
                             f'execute if entity {BULB} run function {NS}om/heart/play/heart_idle', Gen.end()])
    g.pw('fail', 'tick', [HEAD, F('org/burst_q'),
                          Gen.at(FAIL['strike'], f'execute unless score #apq40L mb matches 1 run {F("p/fail/strike")}'),
                          f'execute if score #apPT mb matches {FAIL["end"]}.. run {F("p/fail/restart")}'])
    g.pw('fail', 'reload', [HEAD, '# /reload during the strike: the restart at once (the Heart is re-made by rev/reload).',
                            sc('#apStage', 0), F('p/fail/restart')])
    g.pw('fail', 'cancel', [HEAD, '# Nothing of its own lingers.'])

    # ================================================================ the CS (service 60, 192 t)
    cs = [Gen.at(t, f'execute {AT_BULB} run {fx("gold_drip")}') for t in range(3, CS['white'] + 1, 3)]
    cs += [Gen.at(CS['white'], F('p/cs/white')), Gen.at(CS['white'], f'function {NS}om/heart/play/heart_lift'),
           Gen.at(CS['cradle_gone'], F('p/cs/cradle_gone')),
           Gen.at(CS['revival'], F('p/cs/rise')),
           Gen.at(CS['ember'], f'execute positioned {n(TWIG[0])} {n(TWIG[1])} {n(TWIG[2])} facing {n(CX)} {n(CY + EGG_CS_Y)} {n(CZ)} run '
                  f'{fx("ember_arc", len=round(EMBER_LEN, 1), h=3.0)}'),
           Gen.at(CS['ember'], f'execute positioned {n(TWIG[0])} {n(TWIG[1])} {n(TWIG[2])} run {snd("cs_ember")}'),
           Gen.at(CS['green'], F('p/cs/green'))]
    cs += [Gen.at(t, f'execute {AT_EGG_CS} run {fx("green_lightning")}') for t in range(CS['green'], CS['green'] + 9, 2)]
    cs += [Gen.at(CS['flash'], K.hud('flash_green')), Gen.at(CS['flash'], f'execute {AT_EGG_CS} run {snd("cs_flash")}'),
           Gen.at(CS['flash'], f'execute {AT_EGG_CS} run {snd("cs_heal")}'), Gen.at(CS['flash'], Gen.svc('heal_cs')),
           Gen.at(CS['burst'], F('p/cs/burst')),
           Gen.at(CS['reveal'], Gen.svc('title_p3')), Gen.at(CS['reveal'], Gen.svc('music_3')),
           Gen.at(CS['reveal'], f'execute at {BODY} run {snd("cs_reveal")}'),
           Gen.at(CS['targetable'], Gen.svc('cine_off'))]
    cs += [Gen.at(t, f'execute {AT_CEN} run {fx("haze_lush")}') for t in range(CS['ember'], CS['end'], 10)]
    cs += [f'execute if score #apPT mb matches {CS["end"]}.. run {F("p/cs/done")}']
    g.pw('cs', 'start', [
        HEAD, '# The CS (plan 7.7, 192 t): the progress is full: every organism wilts (the green pulse ring; no progress), walls and',
        '# libraries cleared, cine; the success line; the Heart blazes (0-24, gold dripping), then lifts out of the cradle (heart_lift);',
        f'# t{CS["white"]} the white-out ({CS["whiteout_hold"]} t held): the lush arena, the body unparked (hidden), the phase-3 pool, the p3 look',
        f'# UPRIGHT (the rig stays parked), the push ring; t{CS["cradle_gone"]} the cradle gone; t{CS["revival"]} the body unparked with the rig',
        f'# revival in the same tick (hidden to t92; AP-FIX RV-07); t{CS["ember"]} the 「불씨」 ember;',
        f'# t{CS["green"]} the egg turns green in the wrapping hand; t{CS["flash"]} the green flash + the 25 % heal; t{CS["burst"]} the Warden bursts out',
        f'# (the orb fades into it); t{CS["reveal"]} the phase-3 title + music 3; t{CS["targetable"]} cine off; t{CS["end"]} phase 3.',
        Gen.svc('phase_cs'), sc('#apStage', 0), F('org/burst_all'), F('org/clear'), F('wall/clear'), Gen.svc('lib_clear'),
        Gen.svc('cine_on'), Gen.line(T['cs_done'], A.HEART_HEX, 60),
        K.hud('title', g='success', t=T['cs_done'], c=A.HEART_HEX, s='', hold=14),
        f'execute {AT_CEN} run {fx("wilt_ring")}', f'execute {AT_CEN} run {snd("cs_complete")}',
        f'function {NS}om/heart/play/heart_blaze', Gen.set_len(A.CS_LEN)])
    g.pw('cs', 'white', [HEAD, f'# t{CS["white"]} the white-out: the lush arena + props, the dressing gone, the stage markers gone, the phase-3',
                         f'# pool, the push ring (8 -> 12 b). The body and its rig stay parked until t{CS["revival"]} (p/cs/rise; AP-FIX RV-07: an',
                         '# unparked rig would stand in full view while the white fades in).',
                         K.hud('whiteout', hold=CS['whiteout_hold']), K.dress('clear'), Gen.svc('arena_lush'), F('org/marks_kill'),
                         Gen.svc('repool_p3'), Gen.svc('push_ring_cs')])
    g.pw('cs', 'rise', [HEAD, f'# t{CS["revival"]}: the body unparked at the centre, the p3 look UPRIGHT and the rig revival clip in the same tick',
                        '# (the clip hides every part from its key 0, so the unparked pose is never shown; AP-FIX RV-07).',
                        Gen.svc('unpark'), Gen.svc('look_p3'), f'execute as {BODY} run function {A.rig_fn("stance/upright")}',
                        Gen.play('revival')])
    # AP-FIX RV-10: a pause in the CS drops the title overlay (core pause: hud/flash_end); the resume re-sends the white-out
    # with the ticks left (white held to t{white + 4 + hold}, then the 8-t fade) and the green flash while it runs.
    wo_end = CS['white'] + 4 + CS['whiteout_hold']
    cs_resume = [HEAD, f'# Resume in the CS (AP-FIX RV-10): the white-out again with the ticks left (white to t{wo_end}, fade to t{wo_end + 8}),',
                 f'# the green flash at t{CS["flash"]}..{CS["flash"] + 3}.']
    for t in range(CS['white'], wo_end):
        cs_resume.append(f'execute if score #apPT mb matches {t} run return run {K.hud("whiteout", hold=max(1, wo_end - 4 - t))}')
    cs_resume.append(f'execute if score #apPT mb matches {wo_end}..{wo_end + 7} run return run {K.hud("whiteout", hold=1)}')
    cs_resume.append(f'execute if score #apPT mb matches {CS["flash"]}..{CS["flash"] + 3} run return run {K.hud("flash_green")}')
    g.pw('cs', 'resume', cs_resume)
    g.pw('cs', 'cradle_gone', [HEAD, '# Under the white: the cradle, the arms and the sprouts go (the egg hangs in the vine hand from here).']
         + [f'kill {UU[d]}' for d in ('heart_cradle', 'heart_arms', 'heart_tips')])
    g.pw('cs', 'green', [HEAD, f'# t{CS["green"]}: the vine hand wraps the egg; it turns green.',
                         f'execute if entity {BULB} run function {NS}om/heart/look/heart_bulb/egg_green',
                         f'execute if entity {UU["vine_hand"]} run function {NS}om/heart/look/vine_hand/wrap'])
    g.pw('cs', 'burst', [HEAD, f'# t{CS["burst"]}: the Warden bursts out of the water at the centre in a leaf splash; the egg fades into it.',
                         f'execute {AT_CEN} run {fx("revival_burst")}', f'execute {AT_CEN} run {fx("water_splash")}',
                         f'execute {AT_CEN} run {snd("cs_emerge")}', F('heart/clear')])
    g.pw('cs', 'tick', [HEAD, F('org/burst_q')] + cs)
    g.pw('cs', 'done', [HEAD, Gen.svc('phase_3'), Gen.end()])
    g.pw('cs', 'cancel', [HEAD, Gen.svc('cine_off')])
    assert t1 is TL1
