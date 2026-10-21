"""Phase-3 patterns Q1, Q3, Q3s, Q4, Q5 (plan 8.3; ap_contract 0.8).

STUB (AP-CORE): working frame stubs with the real clocks, clips, weights, chains and stances, the anchor moves of the
burrows and the Q4 opener walk, and the releases; no hazards, no kit calls. AP-P3 replaces this file.
"""
from .api import Pattern, Gen, stub_pattern, PLAYER, LOCK
from . import api as A

W = lambda n, m, f: dict(near=n, mid=m, far=f)    # noqa: E731
Q4_LEN = 8 + A.clip_len('tail_p3')                 # crouch 8 + the tail; + 30 with the walk opener

PATTERNS = [
    Pattern(31, 'mstrike', '이동 돌진', 'normal', 'move_strike_p3', phase=3, weight=W(1, 2, 3),
            length=92, recover=20, max_len=120, last_hit=69),
    Pattern(33, 'shells', '증폭의 풀', 'normal', 'shells', phase=3, weight=W(1, 3, 3),
            length=113, recover=20, max_len=130, last_hit=96, chain={36: 30}),
    Pattern(34, 'tail3', '생명의 꼬리', 'normal', ['crouch_p3', 'walk_p3', 'tail_p3'], phase=3, weight=W(3, 2, 1),
            length=Q4_LEN, recover=18, max_len=Q4_LEN + 40, last_hit=61),
    Pattern(35, 'spiral', '생명의 나선', 'normal', 'spikes', phase=3, weight=W(2, 2, 2),
            length=72, recover=20, max_len=90, last_hit=64, chain={31: 40}),
    Pattern(36, 'surface', '수면 포격', 'chain', ['sink_p3', 'surface_p3', 'stand_p3'], phase=3,
            length=90, recover=20, max_len=110, last_hit=48),
]
P = {p.key: p for p in PATTERNS}
FACE = f'execute at @s facing entity {PLAYER} feet run tp @s ~ ~ ~ ~ 0'
HEAD = '# STUB (AP-CORE, ap_contract 1.3): {label} ({key}, id {id}); the pattern stage replaces this file.'


def emit(g):
    F = g.fn
    # Q1: lock at t32 (hidden 16-41), the anchor to the burst point (clamp r 16), facing the player at the burst
    g.w('p/mstrike/to_lock', ['# @s = body: the burst point = the predictive lock (lead 6) clamped to r 16.',
                              *Gen.lockv(6), f'execute as {LOCK} run {Gen.clamp("burst3")}', Gen.tp_to(LOCK)])
    stub_pattern(g, P['mstrike'], tick=[(32, F('p/mstrike/to_lock')), (44, FACE), (72, Gen.release())])
    stub_pattern(g, P['shells'], tick=[(97, Gen.release())])
    stub_pattern(g, P['spiral'], tick=[(65, Gen.release())])
    # Q3s: sink 0-20, the surfacing point 9 b before the player on the boss -> player line (clamp r 14) at t30, surface 36
    g.w('p/surface/to_lock', ['# @s = body: the surfacing point (9 b from the player toward the boss, clamp r 14).',
                              Gen.lockb(9.0), Gen.tp_to(LOCK), FACE])
    stub_pattern(g, P['surface'], tick=[(30, F('p/surface/to_lock')), (36, Gen.play('surface_p3')), (49, Gen.release())])
    # Q4: crouch 0-8; the opener walk 8-38 when the player is > 8 b away (#apq34 1); the tail at 8 / 38
    q = P['tail3']
    h = HEAD.format(label=q.label, key=q.key, id=q.id)
    tl = A.clip_len('tail_p3')
    g.pw('tail3', 'start', [h, '# the walk opener when the player is farther than 8 b (#apq34 1); the expected end on #apPLen.',
                            'function rlk:mboss/mv/dist', 'scoreboard players set #apq34 mb 0',
                            f'execute if score #mbDist mb matches {int(A.Q4_FAR * 10) + 1}.. run scoreboard players set #apq34 mb 1',
                            Gen.set_len(8 + tl),
                            'execute if score #apq34 mb matches 1 run ' + Gen.set_len(38 + tl)])
    g.pw('tail3', 'tick', [h, '# keeps time only (the clip of each step at its clock; no hazards)',
                           f'execute if score #apq34 mb matches 1 if score #apPT mb matches 8 run {Gen.play("walk_p3")}',
                           f'execute if score #apq34 mb matches 1 if score #apPT mb matches 9..37 at {PLAYER} unless entity @s[distance=..4] '
                           f'as {A.BODY} at @s run {Gen.move_to(PLAYER, A.P3_WALK["spd"])}',
                           f'execute if score #apq34 mb matches 1 if score #apPT mb matches 9..37 run function rlk:mboss/mv/turn {{max:6}}',
                           f'execute if score #apq34 mb matches 0 if score #apPT mb matches 8 run {Gen.play("tail_p3")}',
                           f'execute if score #apq34 mb matches 1 if score #apPT mb matches 38 run {Gen.play("tail_p3")}',
                           f'execute if score #apq34 mb matches 0 if score #apPT mb matches {8 + 54} run {Gen.release()}',
                           f'execute if score #apq34 mb matches 1 if score #apPT mb matches {38 + 54} run {Gen.release()}',
                           f'execute if score #apPT mb >= #apPLen mb run {Gen.end()}'])
    g.pw('tail3', 'cancel', [h, 'kill @e[tag=rlk_mb_ap_p34]'])
