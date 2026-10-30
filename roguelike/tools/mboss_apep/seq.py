"""E (the entrance) and D (the death) of 아펩의 오아시스 파수꾼 (AP-P1; plan 8.1 E, 8.4 D, 7.9; ap_contract 0.8 ids 50 /
51, 1.6 REQ_FILES seq). Kind seq: the core's intro / death hooks run them (no main slot) with #apPT = #mbT - 1, then the
rig and the px-set drivers. Writes AP:seq/** only (api.OWN['seq']).

E (entrance_p1, 110 t, untargetable: the clip's px set inv): the boss rises at the centre out of the dark leaf pool,
the Heart (egg look) hangs 9 b above the centre in the vine hand (heart/p1_hang, the revival module's), the right A arm
reaches up and touches it (touch 47), the bulb flash (60), golden leaf embers (63-80), the vine draws the Heart up into
the canopy (heart_up 70: heart/p1_up), crouch and roar (91-107). The title fades in at t30 (the core's svc/title_p1:
the boss's name, neutral info). No hazards; no line of advice (no-tips rule).

D (death, 120 t): the rig's death clip (hood snap, flicker, droop 30, kneel 55, topple 70-82 onto the water, wither 85,
sink 100, gone 118); the module adds the sounds of plan 8.4 (no creature vocals), the splash at the topple, the white
leaflet bursts while it sinks, and the small glowing golden seed (the org manifest's seed object, om/seed) at the
death spot when the body is gone; cleanup removes it (tag rlk_mb_ap_seed).
"""
from .api import Pattern, Gen, K, BODY
from . import api as A

L = A.L
n = L.num
CY = A.CY
ev = A.ev

PATTERNS = [
    Pattern(50, 'entrance', '등장', 'seq', 'entrance_p1', length=A.E_LEN, max_len=A.E_LEN),
    Pattern(51, 'death', '퇴장', 'seq', 'death', length=A.D_LEN, max_len=A.D_LEN),
]
E = dict(pool=ev('entrance_p1', 'pool'), title=30, touch=ev('entrance_p1', 'touch'), flash=ev('entrance_p1', 'flash'),
         embers=(ev('entrance_p1', 'embers'), 80), heart_up=ev('entrance_p1', 'heart_up'), roar=ev('entrance_p1', 'roar'),
         end=A.E_LEN, bulb=A.anchor('entrance_p1', 'touch', 'hand_a_r'))
assert (E['pool'], E['touch'], E['flash'], E['heart_up'], E['roar']) == (0, 47, 60, 70, 100), E
D = dict(droop=ev('death', 'droop'), land=ev('death', 'land'), wither=ev('death', 'wither'), sink=ev('death', 'sink'),
         gone=ev('death', 'gone'), end=ev('death', 'end'), leaves=(ev('death', 'wither'), ev('death', 'sink'), 110))
assert (D['droop'], D['land'], D['wither'], D['sink'], D['gone'], D['end']) == (30, 82, 85, 100, 118, 120), D

AT_BODY = 'at @s rotated as @s rotated ~ 0'
FLOOR = f'at @s positioned ~ {CY} ~'
# the bulb: where the raised right A hand touches the hanging egg (the rig's touch anchor, x = s left, z = f forward)
BULB = f'{AT_BODY} positioned {A.loc(E["bulb"][0], E["bulb"][2], E["bulb"][1])}'


def x(ctx, *cmds):
    return [f'execute {ctx} run {c}' for c in cmds]


def emit(g):
    F = g.fn
    head = '# AP-P1 (plan 8.1 E): '
    g.w('seq/entrance/setup', [head + '@s = the new body, at it (intro/setup): the Heart hangs 9 b above the centre in the vine hand',
                               '# (the revival module\'s heart/p1_hang).', F('heart/p1_hang')])
    tick = [head + f'@s = body, #apPT = 0..{E["end"] - 1} (entrance_p1). The pool and the rise 0-31, the touch {E["touch"]}, the',
            f'# bulb flash {E["flash"]}, the embers {E["embers"][0]}-{E["embers"][1]}, the Heart drawn up {E["heart_up"]}, the roar {E["roar"]};',
            f'# the title at t{E["title"]}.',
            Gen.at(E['pool'], f'execute {FLOOR} run {K.fx("burrow_pool", r=3.5)}'),
            Gen.at(E['pool'], f'execute {FLOOR} run {K.fx("leaf_flakes")}'),
            Gen.at(E['pool'], f'execute {FLOOR} run {K.snd("e_emerge")}'),
            Gen.at(16, f'execute {FLOOR} run {K.fx("leaf_flakes")}'),
            Gen.at(E['title'], Gen.svc('title_p1')),
            Gen.at(E['flash'], f'execute {BULB} run {K.fx("bulb_flash")}'),
            Gen.at(E['flash'], f'execute {BULB} run {K.snd("e_flash")}'),
            *[Gen.at(t, f'execute {BULB} run {K.fx("gold_embers")}') for t in range(E['embers'][0], E['embers'][1] + 1, 4)],
            Gen.at(E['heart_up'], F('heart/p1_up')),
            Gen.at(E['heart_up'], f'execute {BULB} run {K.snd("e_heart_up")}'),
            Gen.at(E['roar'], f'execute at @s run {K.snd("e_roar")}')]
    g.w('seq/entrance/tick', tick)
    g.w('seq/entrance/done', [head + 'E is over (or skipped: /reload, the tests): the Heart prop drawn up (idempotent).',
                              F('heart/p1_up')])
    dh = '# AP-P1 (plan 8.4 D, 7.9): '
    g.w('seq/death/start', [dh + '@s = body (death_start; the core plays the death clip): no seed yet (it appears when the body',
                            '# is gone).', f'function {A.NS}om/seed/kill'])
    seed_at = D['gone']
    g.w('seq/death/tick', [
        dh + f'@s = body, #apPT = 0..: droop {D["droop"]} (+ the face fades), the topple lands {D["land"]} (splash), wither',
        f'# {D["wither"]}, sink {D["sink"]}-{D["gone"]} (white leaflets every 6 t), gone {D["gone"]}: the golden seed at the death spot, its chime',
        f'# at {D["end"]}. No creature vocals.',
        Gen.at(D['droop'], f'execute at @s run {K.snd("d_droop")}'),
        Gen.at(D['droop'], f'execute at @s run {K.snd("d_face_fade")}'),
        Gen.at(D['land'], f'execute {FLOOR} run {K.fx("water_splash")}'),
        Gen.at(D['land'], f'execute at @s run {K.snd("d_splash")}'),
        *[Gen.at(t, f'execute at @s run {K.snd("d_leaves")}') for t in D['leaves']],
        *[Gen.at(t, f'execute {AT_BODY} run {K.fx("leaf_dissolve")}') for t in range(D['sink'], D['gone'] + 1, 6)],
        Gen.at(D['sink'], f'execute at @s run {K.snd("d_sink")}'),
        Gen.at(seed_at, f'execute {FLOOR} rotated as @s rotated ~ 0 run function {A.NS}om/seed/spawn'),
        Gen.at(D['end'], f'execute {FLOOR} run {K.snd("d_seed")}')])
    assert BODY
