"""Phase-1 patterns P1-P6 and R (plan 8.1; ap_contract 0.8) + the move sounds (p/move/fx).

STUB (AP-CORE): working frame stubs with the real clocks, clips, weights, cooldowns and leads, the anchor moves of the
burrows (lock -> hidden tp) and the releases; no hazards, no kit calls. AP-P1 replaces this file (ownership: OWN['p1']).
"""
from .api import Pattern, Gen, stub_pattern, R_FAR, CLAMPS, PLAYER, LOCK, ARENA_M
from . import api as A

W = lambda fn, fm, ff, su, bk: dict(front_near=fn, front_mid=fm, front_far=ff, side_under=su, back=bk)   # noqa: E731

PATTERNS = [
    Pattern(1, 'burrow', '잠복 돌진', 'normal', 'burrow_strike', phase=1, weight=W(1, 3, 4, 2, 2), cooldown=400,
            length=82, recover=40, max_len=100, last_hit=71),
    Pattern(2, 'hands', '생명의 손', 'normal', 'hands', phase=1, weight=W(1, 3, 3, 2, 2), lead=10,
            length=140, recover=20, max_len=170, last_hit=82),
    Pattern(3, 'glow', '발광하는 파수꾼', 'normal', ['burrow_in_p1', 'emerge_crown_p1', 'glow_slams'], phase=1,
            weight=W(2, 2, 2, 2, 2), cooldown=700, first_after=3, length=225, recover=20, max_len=260, last_hit=195),
    Pattern(4, 'wither', '초목이 시든 풍경', 'normal', 'rotation', phase=1, weight=W(4, 2, 2, 4, 2),
            length=130, recover=10, max_len=150, last_hit=71, opener=(7, R_FAR)),
    Pattern(5, 'tail', '생명의 꼬리', 'normal', 'tail_p1x2', phase=1, weight=W(0, 0, 0, 1, 0), cooldown=200,
            length=127, recover=15, max_len=150, last_hit=59, gates=('side_rear',)),
    Pattern(6, 'combo', '근접 콤보', 'normal', 'combo_a', phase=1, weight=W(4, 1, 0, 1, 0), lead=10,
            length=170, recover=20, max_len=200, last_hit=120),
    Pattern(7, 'reloc', '잠복 이동', 'opener', ['sink_p1', 'emerge_on_p1'], length=42, recover=0, max_len=60),
]
P = {p.key: p for p in PATTERNS}
FACE = f'execute at @s facing entity {PLAYER} feet run tp @s ~ ~ ~ ~ 0'


def emit(g):
    F = g.fn
    # P1: lock at t32 (hidden 22-43), the anchor to the burst point (clamp r 18), facing the player at the burst
    g.w('p/burrow/to_lock', ['# @s = body: the burst point = the predictive lock (lead 6) clamped to r 18; the anchor jumps there.',
                             *Gen.lockv(6), f'execute as {LOCK} run {Gen.clamp("burst1")}', Gen.tp_to(LOCK)])
    stub_pattern(g, P['burrow'], tick=[(32, F('p/burrow/to_lock')), (44, FACE), (77, Gen.release())])
    stub_pattern(g, P['hands'], tick=[(100, Gen.release())])
    # P3: glide hidden to the centre 23-39, emerge 44, turn 84-94, slams from 94
    stub_pattern(g, P['glow'], tick=[(39, f'execute at {ARENA_M} run tp @s ~ {A.CY} ~'),
                                     (44, Gen.play('emerge_crown_p1')),
                                     ((84, 93), 'function rlk:mboss/mv/turn {max:6}'),
                                     (94, Gen.play('glow_slams')), (200, Gen.release())])
    stub_pattern(g, P['wither'], tick=[(72, Gen.release())])
    stub_pattern(g, P['tail'], tick=[(60, Gen.release())])
    # P6: #apq6 = hits (2 / 3 / 4; #apArg 2..4 from tests, else rolled 3 / 4 / 3)
    c = P['combo']
    g.pw('combo', 'roll', ['# The hit count: #apArg (tests) or the 3 / 4 / 3 roll; the expected end on #apPLen.',
                           'scoreboard players operation #apq6 mb = #apArg mb',
                           'execute unless score #apq6 mb matches 2..4 store result score #apR mb run random value 0..9',
                           'execute unless score #apq6 mb matches 2..4 if score #apR mb matches 0..2 run scoreboard players set #apq6 mb 2',
                           'execute unless score #apq6 mb matches 2..4 if score #apR mb matches 3..6 run scoreboard players set #apq6 mb 3',
                           'execute unless score #apq6 mb matches 2..4 run scoreboard players set #apq6 mb 4',
                           'execute if score #apq6 mb matches 2 run ' + Gen.set_len(93),
                           'execute if score #apq6 mb matches 3 run ' + Gen.set_len(113),
                           'execute if score #apq6 mb matches 4 run ' + Gen.set_len(170)])
    head = f'# STUB (AP-CORE, ap_contract 1.3): {c.label} ({c.key}, id {c.id}); the pattern stage replaces this file.'
    g.pw('combo', 'start', [head, F('p/combo/roll')])
    g.pw('combo', 'tick', [head, '# a 0-29, b 29-73, then c 73-93 + end 93-113 (3 hits) / end 73-93 (2) / d 93-170 (4)',
                           Gen.at(29, Gen.play('combo_b')),
                           f'execute if score #apq6 mb matches 2 if score #apPT mb matches 73 run {Gen.play("combo_end")}',
                           f'execute if score #apq6 mb matches 3.. if score #apPT mb matches 73 run {Gen.play("combo_c")}',
                           f'execute if score #apq6 mb matches 3 if score #apPT mb matches 93 run {Gen.play("combo_end")}',
                           f'execute if score #apq6 mb matches 4 if score #apPT mb matches 93 run {Gen.play("combo_d")}',
                           f'execute if score #apPT mb >= #apPLen mb run {Gen.end()}'])
    g.pw('combo', 'cancel', [head, 'kill @e[tag=rlk_mb_ap_p6]'])
    # R: sink 0-17, the lock 2 b in front of the player (clamp r 14) at t17, emerge 18-42
    g.w('p/reloc/to_lock', ['# @s = body: R\'s re-emerge point (2 b before the player on the boss -> player line, clamp r 14).',
                            Gen.lockb(2.0), Gen.tp_to(LOCK), FACE])
    stub_pattern(g, P['reloc'], tick=[(17, F('p/reloc/to_lock')), (18, Gen.play('emerge_on_p1'))])
    # the move sounds (core service 10 calls p/move/fx every move tick)
    g.w('p/move/fx', ['# STUB (AP-CORE): the step sounds of the moves (plan 8.1 M); #apMvK 1 crawl, 2 walk, 3-4 steps.',
                      *Gen.every(8, 'execute if score #apMvK mb matches 1 run ' + Gen.sound('entity.camel.step', 0.8, 0.6), clock='#apMvT'),
                      *Gen.every(8, 'execute if score #apMvK mb matches 2 run ' + Gen.sound('entity.warden.step', 0.7, 0.8), clock='#apMvT'),
                      *Gen.every(5, 'execute if score #apMvK mb matches 3.. run ' + Gen.sound('block.moss_carpet.step', 0.8, 0.7), clock='#apMvT')])
    assert CLAMPS
