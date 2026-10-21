"""Q2 종말의 여파 (plan 8.3 Q2 / 7.8; ap_contract 0.8 id 32, kind scheduled: forced by the core's Q2 schedule) and the
domes (dome/**).

STUB (AP-CORE): the approach (crouch_p3 + walk_p3 to the centre at 0.4 b/t, <= 50 t, skipped within 2 b), then the
aftermath clip from its tick 0 (pattern sub-clock #apq32, -1 while walking); the release after the blast window; no field,
no domes, no hazards. #apAft1 (core) tells a first, non-lethal cast (0) from a later, lethal one (1). AP-P3 replaces
this file.
"""
from .api import Pattern, Gen, ARENA_M
from . import api as A

AFT = A.clip_len('aftermath')
WALK = A.P3_CENTRE_WALK
PATTERNS = [
    Pattern(32, 'aftermath', '종말의 여파', 'scheduled', None, phase=3, length=8 + WALK['max'] + AFT,
            recover=16, max_len=8 + WALK['max'] + AFT + 30, last_hit=8 + WALK['max'] + A.ev('aftermath', 'window_end')),
]
HEAD = '# STUB (AP-CORE, ap_contract 1.3): 종말의 여파 (aftermath, id 32); the pattern stage AP-P3 replaces this file.'


def emit(g):
    F = g.fn
    near = ARENA_M.replace('limit=1', 'distance=..2,limit=1')
    g.pw('aftermath', 'start', [HEAD, '# #apq32 = the aftermath clock (-1 while the approach runs).',
                                'scoreboard players set #apq32 mb -1', Gen.play('crouch_p3'),
                                f'execute positioned ~ {A.CY} ~ if entity {near} run {F("p/aftermath/go")}'])
    g.pw('aftermath', 'go', [HEAD, '# @s = body: at the centre; the aftermath clip from its tick 0; the expected end on #apPLen.',
                             f'execute at {ARENA_M} run tp @s ~ {A.CY} ~', 'scoreboard players set #apq32 mb 0',
                             'scoreboard players operation #apPLen mb = #apPT mb', f'scoreboard players add #apPLen mb {AFT}',
                             Gen.play('aftermath')])
    g.pw('aftermath', 'tick', [
        HEAD,
        f'execute if score #apq32 mb matches -1 if score #apPT mb matches 8 run {Gen.play("walk_p3")}',
        f'execute if score #apq32 mb matches -1 if score #apPT mb matches 8.. at {ARENA_M} as {A.BODY} at @s run '
        f'{Gen.move_to(ARENA_M, WALK["spd"])}',
        f'execute if score #apq32 mb matches -1 if score #apPT mb matches 8.. positioned ~ {A.CY} ~ if entity '
        f'{ARENA_M.replace("limit=1", "distance=..1,limit=1")} run return run {F("p/aftermath/go")}',
        f'execute if score #apq32 mb matches -1 if score #apPT mb matches {8 + WALK["max"]}.. run return run {F("p/aftermath/go")}',
        'execute if score #apq32 mb matches 0.. run scoreboard players add #apq32 mb 1',
        f'execute if score #apq32 mb matches {A.ev("aftermath", "window_end")} run {Gen.release()}',
        f'execute if score #apq32 mb matches {AFT}.. run {Gen.end()}'])
    g.pw('aftermath', 'cancel', [HEAD, '# the domes and fields go (dome/clear); nothing else lingers.', F('dome/clear'),
                                 'kill @e[tag=rlk_mb_ap_p32]'])
    g.w('dome/clear', [HEAD, '# Every dome (and its displays) and the Q2 safe markers go (idempotent, any executor).',
                       'kill @e[tag=rlk_mb_ap_dome]', 'kill @e[tag=rlk_mb_ap_domed]',
                       'kill @e[type=minecraft:marker,tag=rlk_mb_ap_aft]'])
