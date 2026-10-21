"""The revival stage (plan 7.5-7.7, 3.4): T1 (service 20), the Heart of the Oasis (heart/**), the stage (rev/**: waves,
the stage clock, the time-out, the failure strikes, the phase-2 HUD and bar), the failure strike (service 40) and the CS
(service 60).

STUB (AP-CORE): working frame with the real clocks (T1 136 t, the fail strike 60 t, the CS 192 t), the real economy table
(api.REV: start 2700, win 10000, kills +325 / +1400, drains, the destr blast, cap 6, wave clock 600, time-out 2000 then a
destr every 600), the waves of api.WAVES (+ the shuffle-bag specials from wave 6, two from wave 7), the strikes (the 2nd
-> cb/lose), the Heart as a marker + a stand-in display, the progress bar (#buHpCol 10, #buNoNum 1) and a plain HUD.
Missing (AP-REV): the org displays and clips of the cradle / Heart (heart_lower, heart_drop, heart_blaze, heart_lift),
the kit HUD, the hints, the spawn-point rules (distance to the player), Ronova's revive restart. AP-REV replaces this file.
"""
from .api import Pattern, Gen, BODY, HEART_M, ORGS
from . import api as A

R = A.REV
T = A.TXT
PATTERNS = [
    Pattern(20, 't1', '소생 단계 진입', 'service', 'sink_revive', length=A.T1_LEN, max_len=A.T1_LEN + 4, recover=1),
    Pattern(40, 'fail', '소생 실패', 'service', None, length=A.FAIL_LEN, max_len=A.FAIL_LEN + 4, recover=1, hooks=('reload',)),
    Pattern(60, 'cs', '소생', 'service', None, length=A.CS_LEN, max_len=A.CS_LEN + 4, recover=20),
]
HEAD = '# STUB (AP-CORE, ap_contract 1.6): the revival stage; AP-REV replaces this file.'
SPECIALS = ('guard', 'nest', 'nurt', 'pred')
CAP = R['cap']
STAGE_ZERO = ('#apHt', '#apWave', '#apClk', '#apWT', '#apTo', '#apToT', '#apFail', '#apStage', '#apAlive', '#apSlots',
              '#apOArg', '#apOrgN', '#apHtP')


def sc(n, v):
    return f'scoreboard players set {n} mb {int(v)}'


def emit(g):
    F = g.fn
    n = A.L.num
    cx, cz = A.CENTRE[0], A.CENTRE[2]
    egg = ('{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_heartd"],billboard:"fixed",brightness:{block:15,sky:15},'
           'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],'
           'scale:[2f,2f,2f]},item:{id:"minecraft:sniffer_egg",count:1}}')
    # ---------------------------------------------------------------- the Heart
    g.w('heart/p1_hang', [HEAD, '# E: the Heart (egg look) hangs 9 b above the centre in the vine hand (a display; rlk_mb_aux).',
                          'kill @e[tag=rlk_mb_ap_heartd]',
                          f'summon minecraft:item_display {n(cx)} {n(A.CY + 9)} {n(cz)} {egg}'])
    g.w('heart/p1_up', [HEAD, '# E t70: the Heart is drawn up out of sight (+20 b; idempotent).',
                        f'execute unless entity @e[tag=rlk_mb_ap_heartd] run summon minecraft:item_display {n(cx)} {n(A.CY + 20)} {n(cz)} {egg}',
                        f'tp @e[type=minecraft:item_display,tag=rlk_mb_ap_heartd] {n(cx)} {n(A.CY + 20)} {n(cz)}'])
    g.w('heart/p1_respawn', [HEAD, '# /reload in phase 1: the drawn-up Heart prop again.', F('heart/p1_up')])
    g.w('heart/clear', [HEAD, '# The Heart marker and its displays go (idempotent, any executor).',
                        'kill @e[type=minecraft:marker,tag=rlk_mb_ap_heart]', 'kill @e[tag=rlk_mb_ap_heartd]'])
    g.w('heart/make', [HEAD, '# The Heart in the cradle at the centre: marker rlk_mb_ap_heart (not rlk_mob) + the egg display.',
                       F('heart/clear'),
                       f'summon minecraft:marker {n(cx)} {A.CY} {n(cz)} {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_heart"]}}',
                       f'summon minecraft:item_display {n(cx)} {n(A.CY + 1.2)} {n(cz)} {egg}'])
    g.w('heart/add', [HEAD, '# Macro {v}: progress + v (clamp 10000; the stage tick starts the CS at 10000).',
                      '$scoreboard players add #apHt mb $(v)',
                      'execute if score #apHt mb matches 10001.. run scoreboard players set #apHt mb 10000',
                      f'execute at {HEART_M} run ' + Gen.sound('block.amethyst_block.chime', 1.0, 1.2), sc('#apHudQ', 1)])
    g.w('heart/sub', [HEAD, '# Macro {v}: progress - v (clamp 0; the stage tick starts the failure strike at 0).',
                      '$scoreboard players remove #apHt mb $(v)',
                      'execute if score #apHt mb matches ..-1 run scoreboard players set #apHt mb 0',
                      f'execute at {HEART_M} run ' + Gen.sound('block.amethyst_block.hit', 0.4, 0.6), sc('#apHudQ', 1)])

    # ---------------------------------------------------------------- the stage
    g.w('rev/ready', [HEAD, '# Phase 2 ready: the Heart in the cradle, progress 2700 (the stage clocks start in rev/start).',
                      F('heart/make'), sc('#apHt', R['start']), sc('#apHudQ', 1)])
    g.w('rev/start', [HEAD, '# The stage (re)starts from wave 1: clocks and the time-out reset; the first wave is due now.',
                      sc('#apWave', 0), sc('#apClk', 0), sc('#apWT', R['wave_clock']), sc('#apTo', 0), sc('#apToT', 0),
                      sc('#apStage', 1), sc('#apHudQ', 1)])
    g.w('rev/tick', [
        HEAD, '# @s = body (phase 2, module tick): the stage stops while a service (fail / CS) runs; the organisms; the Heart',
        '# limits (CS / failure strike); the waves (due on <= 1 alive or the wave clock; a due wave waits for the cap); the',
        '# time-out.',
        'execute unless score #apStage mb matches 1 run return 0',
        'execute if score #apPid mb matches 1.. run return 0',
        'scoreboard players add #apClk mb 1', 'scoreboard players add #apWT mb 1', sc('#apSlots', 0),
        f'execute as {ORGS} at @s run {F("org/tick")}',
        f'execute if score #apHt mb matches {R["win"]}.. run return run {Gen.svc("req_cs")}',
        f'execute if score #apHt mb matches ..0 run return run {Gen.svc("req_fail")}',
        f'execute store result score #apAlive mb if entity {ORGS}',
        F('rev/wave_due'),
        f'execute if score #apClk mb matches {R["timeout"]}.. run {F("rev/timeout")}'])
    g.w('rev/wave_due', [HEAD, f'# The next wave: due when <= {R["wave_left"]} alive or {R["wave_clock"]} t after the last; it waits',
                         f'# while alive + its size > the cap {CAP}.',
                         sc('#apX', 0),
                         f'execute if score #apWT mb matches {R["wave_clock"]}.. run scoreboard players set #apX mb 1',
                         f'execute if score #apAlive mb matches ..{R["wave_left"]} run scoreboard players set #apX mb 1',
                         'execute if score #apX mb matches 0 run return 0',
                         sc('#apY', 4),
                         'execute if score #apWave mb matches 1.. run scoreboard players set #apY mb 5',
                         'execute if score #apWave mb matches 6.. run scoreboard players set #apY mb 6',
                         'scoreboard players operation #apY mb += #apAlive mb',
                         f'execute if score #apY mb matches {CAP + 1}.. run return 0',
                         'scoreboard players add #apWave mb 1', sc('#apWT', 0), sc('#apHudQ', 1),
                         F('rev/wave_spawn')])
    pts = A.ORG_SPAWN
    spawn = [HEAD, '# The current wave #apWave (also /reload: the wave again): 4 basics on 4 of the 8 r 12 points (odd / even by',
             '# the wave; wave 1: 2 melee + 2 ranged, later 50 / 50), then its specials (waves 2-5 the table, 6 one from the bag,',
             '# 7+ two).']
    for par, idx in ((1, (0, 2, 4, 6)), (0, (1, 3, 5, 7))):
        for j, i in enumerate(idx):
            x, y, z = pts[i]
            spawn.append(f'scoreboard players set #apOArg mb {-1}')
            spawn.append(f'execute if score #apWave mb matches 1 run scoreboard players set #apOArg mb {j % 2}')
            spawn.append(f'scoreboard players operation #apM mb = #apWave mb')
            spawn.append(f'scoreboard players operation #apM mb %= #apK2 mb')
            spawn.append(f'execute if score #apM mb matches {par} positioned {n(x)} {n(y)} {n(z)} run {F("org/spawn_basic")}')
    for wv, rec in enumerate(A.WAVES, start=1):
        for k in rec.get('special', []):
            spawn.append(f'execute if score #apWave mb matches {wv} run {F("rev/sp_" + k)}')
    spawn += [f'execute if score #apWave mb matches {len(A.WAVES) + 1}.. run {F("rev/sp_bag")}',
              f'execute if score #apWave mb matches {len(A.WAVES) + 2}.. run {F("rev/sp_bag")}']
    g.w('rev/wave_spawn', spawn)
    sp_at = {'guard': pts[1], 'nest': pts[5], 'pred': pts[3], 'destr': pts[7], 'nurt': A.NURT_SPAWN[0]}
    for k, (x, y, z) in sp_at.items():
        g.w(f'rev/sp_{k}', [f'execute positioned {n(x)} {n(y)} {n(z)} run {F("org/spawn_" + k)}'])
    g.w('rev/sp_bag', ['# A special from the bag {수호, 둥지, 양육, 포식성} (the stub draws at random).',
                       'execute store result score #apR mb run random value 0..3']
        + [f'execute if score #apR mb matches {i} run return run {F("rev/sp_" + k)}' for i, k in enumerate(SPECIALS)])
    g.w('rev/timeout', [HEAD, f'# {R["timeout"]} t into the stage: the warning, a 파괴 at once and then every {R["timeout_every"]} t while',
                        f'# fewer than {R["timeout_alive"] + 1} are alive (time-out spawns ignore the cap).',
                        f'execute if score #apTo mb matches 0 run {F("rev/warn")}',
                        'scoreboard players add #apToT mb 1',
                        f'execute if score #apToT mb matches {R["timeout_every"]}.. run {F("rev/to_spawn")}'])
    g.w('rev/warn', [sc('#apTo', 1), sc('#apToT', R['timeout_every']),
                     f'title @a[tag=player] title {{text:"{T["warn_title"]}",color:"{A.HEART_HEX}"}}',
                     f'title @a[tag=player] subtitle {{text:"{T["warn_sub"]}",color:"{A.WARN_HEX}"}}',
                     Gen.line(T['warn_line'], A.WARN_HEX, 60),
                     Gen.sound('event.raid.horn', 0.3, 1.0), sc('#apHudQ', 1)])
    g.w('rev/to_spawn', [sc('#apToT', 0),
                         f'execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_destr,limit={R["timeout_alive"]}] run return 0',
                         F('rev/sp_destr')])
    g.w('rev/test_timeout', [HEAD, '# Test 29: the time-out now (the stage clock at its last tick before the warning).',
                             sc('#apClk', R['timeout'] - 1)])
    g.w('rev/reload', [HEAD, '# /reload in phase 2 (the module entities are gone): the Heart again, the walls cleared, the current wave',
                       '# again; progress, wave index, clocks and strikes kept.',
                       F('heart/make'), F('wall/clear'),
                       f'execute if score #apStage mb matches 1 if score #apWave mb matches 1.. run {F("rev/wave_spawn")}', sc('#apHudQ', 1)])
    g.w('rev/pause', [HEAD, '# Pause in phase 2: the walls go (re-cast later); the organisms freeze (NoAI, the module tick is off).',
                      F('wall/clear'), F('org/freeze')])
    g.w('rev/resume', [HEAD, '# Resume in phase 2: nothing to restore (the walls are re-cast by their 둥지).', sc('#apHudQ', 1)])
    g.w('rev/clear', [HEAD, '# The stage gone (cleanup, the phase jumps): the Heart, the stage scores.', F('heart/clear')]
        + [sc(k, 0) for k in STAGE_ZERO])
    g.w('rev/bars', [HEAD, '# @s = body (bars hook, phase 2): the gold progress bar (#buHp = #apHt / 10 of 1000, colour 10, no',
                     '# numbers; cm.md 11); the under-bar = the time to the warning (gold), red after it.',
                     'scoreboard players operation #buHp bu = #apHt mb', 'scoreboard players operation #buHp bu /= #c10 mb',
                     'scoreboard players set #buMax bu 1000', 'scoreboard players set #buHpCol bu 10',
                     'scoreboard players set #buNoNum bu 1',
                     f'scoreboard players set #buSub bu {R["timeout"]}', 'scoreboard players operation #buSub bu -= #apClk mb',
                     'execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0',
                     f'scoreboard players set #buSubMax bu {R["timeout"]}',
                     f'scoreboard players set #buSubCol bu {A.L.ELEM_TO_BU[5]}',
                     f'execute if score #apTo mb matches 1 run scoreboard players set #buSub bu {R["timeout"]}',
                     f'execute if score #apTo mb matches 1 run scoreboard players set #buSubCol bu {A.L.ELEM_TO_BU[1]}'])
    badges = []
    for k in ('guard', 'nest', 'nurt', 'pred', 'destr'):
        badges.append(f'execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_{k},limit=1] run data modify storage rlk:mboss extra '
                      f'append value {A.K.badge(k, True)}' if not A.KIT else f'# kit badge {k}')
    g.w('rev/hud', [HEAD, '# @s = body (phase 2, every 4 t): line 1 extras (the specials alive, the wave), line 3 (the progress, ⚠).',
                    'data modify storage rlk:mboss extra set value []'] + badges + [
                    'data modify storage rlk:mboss extra append value {text:"  ",color:"#E8E2D0"}',
                    'data modify storage rlk:mboss extra append value {score:{name:"#apWave",objective:"mb"},color:"#E8E2D0"}',
                    'data modify storage rlk:mboss extra append value {text:"웨이브",color:"#E8E2D0"}',
                    'scoreboard players operation #apHtP mb = #apHt mb', 'scoreboard players operation #apHtP mb /= #c100 mb',
                    f'data modify storage rlk:mboss sub set value [{{text:"{T["p2_progress"]} ",color:"{A.HEART_HEX}"}},'
                    f'{{score:{{name:"#apHtP",objective:"mb"}},color:"{A.HEART_HEX}"}},{{text:"%",color:"{A.HEART_HEX}"}}]',
                    f'execute if score #apFail mb matches 1.. run data modify storage rlk:mboss sub append value {{text:"  ⚠",color:"{A.WARN_HEX}"}}',
                    sc('#apHudQ', 0)])

    # ---------------------------------------------------------------- T1 (service 20, 136 t)
    t1 = ['# T1 (plan 7.5): sink_revive where it stands (the core plays it at 0); t6 libraries cleared; t45 parked; t100 the',
          '# Heart in the cradle (progress 2700); t106 the Heart title + music 2; t108 the goal line, cine off; t136 phase 2.']
    g.pw('t1', 'start', [HEAD] + t1 + [Gen.line(T['t1_sink'], '#E8E2D0', 60), Gen.svc('cine_on'), Gen.set_len(A.T1_LEN)])
    g.pw('t1', 'tick', [HEAD,
                        Gen.at(6, Gen.svc('lib_clear')), Gen.at(6, 'scoreboard players set #mbNoLeash mb 1'),
                        Gen.at(45, Gen.svc('park')), Gen.at(50, F('heart/clear')), Gen.at(100, F('rev/ready')),
                        Gen.at(106, Gen.svc('title_heart')), Gen.at(106, Gen.svc('music_2')),
                        Gen.at(108, Gen.line(T['p2_goal'], A.HEART_HEX, 100)), Gen.at(108, Gen.svc('cine_off')),
                        f'execute if score #apPT mb matches {A.T1_LEN}.. run {F("p/t1/done")}'])
    g.pw('t1', 'done', [HEAD, Gen.svc('phase_2'), F('rev/start'), Gen.end()])
    g.pw('t1', 'cancel', [HEAD, Gen.svc('cine_off')])

    # ---------------------------------------------------------------- the failure strike (service 40, 60 t)
    g.pw('fail', 'start', [HEAD, '# 「소생 실패」 (plan 3.4): strike 1 of 2 (the 2nd -> cb/lose); every organism bursts with no progress;',
                           '# walls cleared; the title; t20 the player takes 25 % max HP (non-lethal, no reaction); t60 the stage',
                           '# restarts at 2700 from wave 1.',
                           'scoreboard players add #apFail mb 1', sc('#apStage', 0),
                           f'execute if score #apFail mb matches {R["fail_strikes"]}.. run return run {Gen.svc("lose")}',
                           F('org/clear'), F('wall/clear'),
                           f'title @a[tag=player] title {{text:"{T["fail_title"]}",color:"{A.WARN_HEX}"}}',
                           f'title @a[tag=player] subtitle {{text:"{T["fail_line"]}",color:"{A.WARN_HEX}"}}',
                           Gen.set_len(A.FAIL_LEN)])
    g.pw('fail', 'strike', [HEAD, 'scoreboard players set #mbNoRx mb 1', *Gen.pl_dot(A.DMG_PM['fail1'], 7, 0)])
    g.pw('fail', 'restart', [HEAD, sc('#apHt', R['fail_restart']), F('rev/start'), Gen.line(T['fail_hint'], A.HEART_HEX, 100),
                             Gen.end()])
    g.pw('fail', 'tick', [HEAD, Gen.at(20, F('p/fail/strike')),
                          f'execute if score #apPT mb matches {A.FAIL_LEN}.. run {F("p/fail/restart")}'])
    g.pw('fail', 'reload', [HEAD, '# /reload during the strike: the restart at once.', F('p/fail/restart')])
    g.pw('fail', 'cancel', [HEAD])

    # ---------------------------------------------------------------- the CS (service 60, 192 t)
    g.pw('cs', 'start', [HEAD, '# The CS (plan 7.7): every organism bursts, walls cleared, libraries cleared, cine; the success line.',
                         Gen.svc('phase_cs'), sc('#apStage', 0), F('org/clear'), F('wall/clear'), Gen.svc('lib_clear'),
                         Gen.svc('cine_on'), Gen.line(T['cs_done'], A.HEART_HEX, 60), Gen.set_len(A.CS_LEN)])
    g.pw('cs', 'white', [HEAD, '# t24 the white-out: the lush arena + props, the cradle gone, the body unparked at the centre (hidden),',
                         '# the phase-3 pool, the p3 look UPRIGHT, the push ring.',
                         Gen.svc('arena_lush'), F('heart/clear'), Gen.svc('unpark'), Gen.svc('repool_p3'), Gen.svc('look_p3'),
                         f'execute as {BODY} run function {A.rig_fn("stance/upright")}', Gen.svc('push_ring_cs')])
    g.pw('cs', 'tick', [HEAD, Gen.at(24, F('p/cs/white')), Gen.at(32, Gen.play('revival')),
                        Gen.at(80, Gen.svc('heal_cs')),
                        Gen.at(132, Gen.svc('title_p3')), Gen.at(132, Gen.svc('music_3')),
                        Gen.at(150, Gen.svc('cine_off')),
                        f'execute if score #apPT mb matches {A.CS_LEN}.. run {F("p/cs/done")}'])
    g.pw('cs', 'done', [HEAD, Gen.svc('phase_3'), Gen.end()])
    g.pw('cs', 'cancel', [HEAD, Gen.svc('cine_off')])
