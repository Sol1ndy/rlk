"""E (the entrance) and D (the death) sequences (plan 8.4; ap_contract 0.8 ids 50 / 51; kind seq: run by the core's intro
and death hooks, no main slot).

STUB (AP-CORE): the clocks (#apPT = #mbT - 1), the title at E t30, the Heart prop's hang / draw-up hand-offs to the
revival module (heart/p1_hang at E t0, heart/p1_up at E t70), the seed prop of D. AP-P1 replaces this file.
"""
from .api import Pattern, Gen
from . import api as A

PATTERNS = [
    Pattern(50, 'entrance', '등장', 'seq', 'entrance_p1', length=A.E_LEN, max_len=A.E_LEN),
    Pattern(51, 'death', '퇴장', 'seq', 'death', length=A.D_LEN, max_len=A.D_LEN),
]
HEAD = '# STUB (AP-CORE, ap_contract 1.6): the pattern stage AP-P1 replaces this file.'


def emit(g):
    F = g.fn
    g.w('seq/entrance/setup', [HEAD, '# @s = the new body, at it (intro/setup): the Heart hangs 9 b above the centre in the vine hand.',
                               F('heart/p1_hang')])
    g.w('seq/entrance/tick', [HEAD, '# @s = body, #apPT = 0.. (entrance_p1 110 t): the title fades in at t30; the Heart is drawn up at',
                              '# t70 (heart_up); the roar at t100.',
                              Gen.at(30, Gen.svc('title_p1')),
                              Gen.at(A.ev('entrance_p1', 'heart_up'), F('heart/p1_up')),
                              Gen.at(A.ev('entrance_p1', 'roar'), Gen.sound('entity.warden.roar', 1.0, 1.3))])
    g.w('seq/entrance/done', [HEAD, '# E is over (or skipped): the Heart prop drawn up (idempotent).', F('heart/p1_up')])
    g.w('seq/death/start', [HEAD, '# @s = body (death_start): the death clip runs (core); the seed prop at the centre.',
                            'kill @e[tag=rlk_mb_ap_seed]',
                            f'execute positioned {A.L.num(A.CENTRE[0])} {A.L.num(A.CY + 0.4)} {A.L.num(A.CENTRE[2])} run summon '
                            'minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_seed"],billboard:"center",'
                            'brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],'
                            'right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]},item:{id:"minecraft:torchflower_seeds",count:1}}'])
    g.w('seq/death/tick', [HEAD, '# @s = body, #apPT = 0..: the seed shows at the sink (t100).',
                           Gen.at(A.ev('death', 'sink'), 'data merge entity @e[type=minecraft:item_display,tag=rlk_mb_ap_seed,limit=1] '
                                  '{start_interpolation:0,interpolation_duration:10,transformation:{translation:[0f,0f,0f],'
                                  'left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f]}}')])
