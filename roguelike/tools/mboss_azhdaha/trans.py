"""S2-S: the transition services 20 파멸의 산사태 (landslide), 21 absorb 1, 22 absorb 2 and 23 the B3 frame (plan.md
4.3, 4.4, 4.8, 5 T1-T3, B3; s2.md 7, 11). WORKING STUB by S1-MOD (ownership passes to S2-S at I1): the real clocks
and every core-relevant action (cine, proxy states, looks, the arena recolour, phases and floors, music, the cast of
the leg special at the absorb-1 roar, the B3 frame with the special start / tick / stop calls, the tail window, the
surfacing and "마지막 일격!"), the six landslide fronts (N10, plan 5 T1 sizes and ticks) and the B3 emergence burst,
with stand-in kit calls. S2-S replaces the visuals and sounds, keeps the clocks, and adds h_ps.py.

The core sequences them (core tr/*): transition 1 = message -> 20 -> 21 -> phase 2; transition 2 = message -> the
leg special first (core service 30) -> 20 -> 22 -> 23 -> phase 3. #azTrN = 1 / 2 tells the services which one runs
(0 = a test request outside a transition). Every service declares `reload` (plan 4.3: a cut landslide resumes at its
next wave, a cut absorb finishes at once with its looks, a cut B3 resumes at its frame tick); the core also uses the
reload of 23 to start the frame at a later tick (tests 25 and 61).
"""
from . import api as A
from .api import TL, L

NS = A.NS
BODY = A.BODY
ARENA_M = A.ARENA_M
SLIDE_LEAD = 40                                       # the walk to the centre; the landslide clip starts here
SLIDE = A.clip_len('landslide')
SLIDE_EV = {k: SLIDE_LEAD + v for k, v in A.CLIPS['landslide']['events'].items()}
SLIDE_END = SLIDE_LEAD + SLIDE                        # 243
WAVES = [SLIDE_EV[f'w{k}'] for k in range(1, 6)]
WAVE6 = SLIDE_EV['w6']
ABS1 = A.clip_len('absorb')                           # 94
ABS1_BURST = A.ev('absorb', 'burst')                  # 47
ROAR = A.clip_len('roar_rear')                        # 82
ROAR_R = A.ev('roar_rear', 'roar')                    # 20
ABS1_END = ABS1 + ROAR                                # 176
ABS2 = A.clip_len('absorb_p3')                        # 52
ABS2_BURST = A.ev('absorb_p3', 'burst')               # 42
ABS2_END = ABS2 + ROAR                                # 134
B3 = A

LINES_T1 = {'w1': '천 년의 원한을 어찌 갚을까!', 'rear': '대지의 진노는 잠재울 수 없다!'}
LINES_T2 = {'w1': '오늘이야말로 묵은 원한을 전부 청산하지!', 'w3': '천 년의 원한을 어찌 갚을까!', 'rear': '대지의 진노는 잠재울 수 없다!'}
LINE_ABS1 = '으윽…! 넌 이번에도 날 배신할 셈인가!'
LINE_ABS2_BURST = '모락스! 너 정말 날 파멸시킬 작정이냐!'
LINE_ABS2_ROAR = '이 곳이 네놈들이 묻힐 곳이다! 받거라… 천 년의 분노를…!'

PATTERNS = [
    A.Pattern(20, 'slide', '파멸의 산사태', 'service', None, recover=20, max_len=SLIDE_END + 6, length=SLIDE_END,
              hooks=('reload',)),
    A.Pattern(21, 'absorb1', '원소 흡수', 'service', 'absorb', recover=10, max_len=ABS1_END + 6, length=ABS1_END,
              hooks=('reload',)),
    A.Pattern(22, 'absorb2', '원소 흡수', 'service', 'absorb_p3', recover=0, max_len=ABS2_END + 6, length=ABS2_END,
              hooks=('reload',)),
    A.Pattern(23, 'burrow3', '잠복', 'service', 'p3_sink', recover=16, max_len=A.B3_LEN + 6, length=A.B3_LEN,
              hooks=('reload',)),
]
assert WAVES == [97, 117, 138, 158, 179] and WAVE6 == 219 and SLIDE_END == 243


def _tr(n):
    return f'execute if score #azTrN mb matches {n} run '


def slide(g):
    key = 'slide'
    tl = TL(g, key)
    walk = f'execute as {BODY} at @s positioned ~ {A.CY} ~ unless entity {ARENA_M.replace("limit=1", "distance=..2,limit=1")} run '
    tl.at(0, 'scoreboard players set #aq20W mb 0',
          f'{walk}scoreboard players set #aq20W mb 1',
          f'execute if score #aq20W mb matches 1 at {ARENA_M} run function rlk:mboss/mv/glide {{t:30}}',
          f'execute if score #aq20W mb matches 1 run {g.play("walk")}',
          f'execute unless score #aq20W mb matches 1 run {g.play("idle")}',
          'scoreboard players set #mbNoLeash mb 1',
          # no rim rings (plan Change note 1: T1 is a *none* row; the banner, the typed lines, the cue and the lift
          # poses are the tell)
          A.K.snd('slide_lift'))
    tl.at(30, f'execute if score #aq20W mb matches 1 run {g.play("walk_stop")}')
    tl.span(0, SLIDE_LEAD + 45, 'scoreboard players set #azNoPush mb 1', g.face('track'))
    tl.at(SLIDE_LEAD, g.play('landslide'))
    for k, strike in enumerate(WAVES, 1):
        g.wave(tl, strike, 4.0, 18.0, 3.0, 3.5, 20, A.DMG['t1_wave'], nd=1, el='ground', grp='new', low=0.7, wid=k - 1,
               tag=f'rlk_mb_az_p20w{k}')
        tl.at(strike - 8, f'execute at {BODY} if entity @a[tag=player,distance=..18] run function {NS}p/{key}/cue')
        tl.at(strike, A.K.snd('slide_wave'))
    g.wave(tl, WAVE6, 4.0, 30.0, 4.0, 4.5, 20, A.DMG['t1_wave6'], nd=1, el='ground', grp='new', low=0.7, wid=5,
           tag='rlk_mb_az_p20w6')
    tl.at(WAVE6 - 10, f'function {NS}p/{key}/cue')
    tl.at(WAVE6, A.K.snd('slide_wave6'))
    tl.at(SLIDE_EV['w1'], _tr('..1') + g.line(LINES_T1['w1']), _tr(2) + g.line(LINES_T2['w1']))
    tl.at(SLIDE_EV['w3'], _tr(2) + g.line(LINES_T2['w3']))
    tl.at(SLIDE_EV['rear'], g.line(LINES_T1['rear']))
    tl.at(SLIDE_END, 'scoreboard players set #mbNoLeash mb 0', g.end())
    tl.write(['# 20 파멸의 산사태 (WORKING STUB, S1-MOD): t0 the walk to <= 2 b of the centre (30 t), the clip at '
              f'{SLIDE_LEAD}; fronts at {WAVES} and wave 6 at {WAVE6} (nododge, low 0.7, internal tell 20, no pre-strike decal: Change note 1); end {SLIDE_END}.'],
             [f'# {key} tick (#azPT).'])
    g.pw(key, 'cue', ['# The jump cue: "점프!" on the sub-line 12 t + a bell (plan 5 T1 tells).',
                      'scoreboard players set #azCue mb 12', A.K.hud('cue_jump'), A.K.snd('jump_cue'),
                      f'execute as @a[tag=player] at @s run {L.sound("block.note_block.bell", 0.9, 1.2, target="@s")}'])
    g.pw(key, 'cancel', ['# Fronts and the walk go (selectors only).', 'kill @e[type=minecraft:marker,tag=rlk_mb_az_p20]',
                         'scoreboard players set #mbNoLeash mb 0']
         + [f'kill @e[type=minecraft:marker,tag=rlk_mb_az_p20w{k}]' for k in range(1, 7)])
    g.pw(key, 'reload', ['# /reload inside the landslide: the hazards are gone; the clock goes on (the next wave comes).',
                         'scoreboard players set #mbNoLeash mb 1'])


def absorb1(g):
    key = 'absorb1'
    tl = TL(g, key)
    tl.at(0, g.cine(True), g.px('inv'), g.glow(True),
          *_leg_dispatch(lambda e: A.K.fxe('vortex', e, t=ABS1_BURST)), *_leg_dispatch(lambda e: A.K.snde('absorb_vortex', e)))
    tl.at(ABS1_BURST, g.look_legs(), g.arena_look('leg'), A.fw('push/ring', '{r:80,to:85,kb:4}'), g.banner('ab'),
          *_leg_dispatch(lambda e: A.K.snde('absorb_burst', e)))
    tl.at(A.ev('absorb', 'gold_off'), g.glow(False))
    tl.at(ABS1, g.phase(2), g.play('roar_rear'), g.cast_leg())
    tl.at(ABS1 + ROAR_R, g.line(LINE_ABS1), A.K.fx('shock_dome', r=80), A.K.snd('absorb_roar'), g.cine(False), g.px('normal'))
    tl.at(ABS1_END, g.end())
    tl.write([f'# 21 absorb 1 (WORKING STUB, S1-MOD): cine + untargetable; burst {ABS1_BURST}: the legs look, the arena, the push ring;',
              f'# {ABS1}: phase 2 (floor F2, music 2, the brand banner), roar_rear + the leg special; roar {ABS1 + ROAR_R}: cine ends.'],
             [f'# {key} tick.'])
    g.pw(key, 'cancel', ['# Immediate cleanup: the cine and the gold glow end.', g.cine(False), g.glow(False)])
    g.pw(key, 'reload', ['# /reload inside absorb 1: it finishes at once (plan 4.3): the looks, phase 2, targetable again.',
                         f'execute if score #azPT mb matches ..{ABS1 - 1} run {g.phase(2)}',
                         g.look_legs(), g.arena_look('leg'), g.cine(False), g.glow(False), g.px('normal'), g.end()])


def absorb2(g):
    key = 'absorb2'
    tl = TL(g, key)
    tl.at(0, g.cine(True), g.px('inv'), g.glow(True), *_tail_dispatch(lambda e: A.K.snde('absorb_vortex', e)))
    tl.at(ABS2_BURST, g.look_tail(), g.arena_look('tail'), g.banner('ab2'), g.line(LINE_ABS2_BURST), g.phase(3),
          A.fw('push/ring', '{r:80,to:85,kb:4}'), *_tail_dispatch(lambda e: A.K.fxe('shard_rain', e, r=120, t=48)),
          *_tail_dispatch(lambda e: A.K.snde('absorb_burst', e)))
    tl.at(A.ev('absorb_p3', 'gold_off'), g.glow(False))
    tl.at(ABS2, g.play('roar_rear'))
    tl.at(ABS2 + ROAR_R, g.line(LINE_ABS2_ROAR), A.K.snd('absorb_roar'), g.cine(False), g.px('normal'))
    tl.at(ABS2_END, g.end())
    tl.write([f'# 22 absorb 2 (WORKING STUB, S1-MOD): burst {ABS2_BURST}: the tail look, phase 3, #mbFloor 1; {ABS2}: roar_rear',
              f'# (no cast); roar {ABS2 + ROAR_R}: cine ends; then the B3 frame.'], [f'# {key} tick.'])
    g.pw(key, 'cancel', ['# Immediate cleanup.', g.cine(False), g.glow(False)])
    g.pw(key, 'reload', ['# /reload inside absorb 2: it finishes at once (the tail look, phase 3, floor 1), then the B3.',
                         f'execute if score #azPT mb matches ..{ABS2_BURST - 1} run {g.phase(3)}',
                         g.look_tail(), g.arena_look('tail'), g.cine(False), g.glow(False), g.px('normal'), g.end()])


def burrow3(g):
    key = 'burrow3'
    tl = TL(g, key)
    B = A
    centre = f'execute at {ARENA_M} run '
    tl.at(0, f'{centre}{A.K.tele_crater(7.5, B.B3_GLIDE[0], hold=3)}', g.fxe('dig', 'ground'), A.K.snd('b3_sink'),
          'scoreboard players set #mbNoLeash mb 1', 'scoreboard players set #azB3Sp mb 0')
    tl.at(B.B3_INV, g.px('inv'))
    tl.at(B.B3_GLIDE[0], f'execute at {ARENA_M} run function rlk:mboss/mv/glide {{t:{B.B3_GLIDE[1] - B.B3_GLIDE[0]}}}')
    tl.at(B.B3_TAILUP, g.px('tail_only'), 'scoreboard players set #azBur mb 1', g.b3_special('start'), A.K.snd('b3_rise'))
    tl.at(B.B3_TAILSINK, g.play('tail_pillar_sink'), g.px('inv'))
    tl.at(B.B3_EMERGE_HZ, f'execute at {ARENA_M} run function {NS}p/{key}/emerge')
    tl.at(B.B3_EMERGE, g.play('burrow_emerge'))
    tl.at(B.B3_BURST, g.b3_special('stop'), f'{centre}{A.K.fx("emerge_spikes", r=52)}', A.K.snd('b3_emerge'))
    # the surfacing ends the transition (tr/done: #azTr 0, the FLANK skip, the cooldown): the fight is on again for the
    # last 15 t of the frame ("마지막 일격!")
    tl.at(B.B3_OUT, g.px('normal'), g.floor(0), 'scoreboard players set #azBur mb 0', f'function {NS}tr/done',
          f'execute as {BODY} if score @s mhpC matches ..1 run function {NS}p/{key}/last')
    tl.at(B.B3_END, 'scoreboard players set #mbNoLeash mb 0', g.end())
    tl.write([f'# 23 the B3 frame (WORKING STUB, S1-MOD; s2.md 7): #azB3T = #azPT; dig, inv {B.B3_INV}, the hidden glide to the',
              f'# centre {B.B3_GLIDE}, tail-up {B.B3_TAILUP} (tail_only, #azBur 1, the special starts), sink {B.B3_TAILSINK}, emergence',
              f'# hazard {B.B3_EMERGE_HZ} (no decal), burst {B.B3_BURST} (the special stops), out {B.B3_OUT} (normal, floor 0), end {B.B3_END}.'],
             [f'# {key} tick: the B3 clock, the special\'s tick in the tail window.',
              'scoreboard players operation #azB3T mb = #azPT mb',
              'scoreboard players set #azNoPush mb 1',
              f'execute if score #azPT mb matches {B.B3_TAILUP + 1}..{B.B3_BURST - 1} run {g.b3_special("tick")}'],
             extra_tick=())
    g.pw(key, 'emerge', [f'# The emergence burst at the centre: disc r 5.2, internal tell {B.B3_BURST - B.B3_EMERGE_HZ}, no decal',
                         '# (plan Change note 1: the dust mound of B3_MOUND is the tell),',
                         '# the leg element + brand, dodgeable (step away from the surfacing spot).',
                         g.GRP_NEW] + g.hz_opts(grp=True, kb=A.KB['heavy']) + g.el_ground()
         + [L.hz_disc(5.2, B.B3_BURST - B.B3_EMERGE_HZ, A.DMG['b3_emerge']), g.tag_last_hz('rlk_mb_az_p23e')])
    g.pw(key, 'last', ['# HP 1 at the surfacing: "마지막 일격!" (the next hit kills through the normal path).',
                       'scoreboard players set #azLastHit mb 1', 'scoreboard players set #azHudQ mb 1', g.glow(True)])
    g.pw(key, 'cancel', ['# The special is cancelled, the burrow state ends (selectors only).', g.b3_special('cancel'),
                         'scoreboard players set #azBur mb 0', 'scoreboard players set #mbNoLeash mb 0',
                         'kill @e[type=minecraft:marker,tag=rlk_mb_az_p23e]'])
    # resume at the frame tick (/reload, tests 25 / 61): the state of #azPT
    r = ['# The B3 resumes at its frame tick #azPT (plan 4.3; tests 25 / 61 start here): the proxy state, the rig clip, the',
         '# anchor at the centre after the glide, #azBur, the special (re-made from the current B3 tick, or started).',
         'scoreboard players operation #azB3T mb = #azPT mb', 'scoreboard players set #mbNoLeash mb 1',
         f'execute if score #azPT mb matches {B.B3_GLIDE[1]}..{B.B3_EMERGE + 37} as {BODY} at {ARENA_M} run tp @s ~ ~ ~',
         f'execute if score #azPT mb matches ..{B.B3_INV - 1} run {g.px("normal")}',
         f'execute if score #azPT mb matches {B.B3_INV}..{B.B3_TAILUP - 1} run {g.px("inv")}',
         f'execute if score #azPT mb matches {B.B3_TAILUP}..{B.B3_TAILSINK - 1} run {g.px("tail_only")}',
         f'execute if score #azPT mb matches {B.B3_TAILSINK}..{B.B3_OUT - 1} run {g.px("inv")}',
         f'execute if score #azPT mb matches {B.B3_OUT}.. run {g.px("normal")}',
         f'execute if score #azPT mb matches ..{B.B3_PILLAR - 1} run {g.play("p3_sink")}',
         f'execute if score #azPT mb matches {B.B3_PILLAR}..{B.B3_TAILSINK - 1} run {g.play("tail_pillar")}',
         f'execute if score #azPT mb matches {B.B3_TAILSINK}..{B.B3_EMERGE - 1} run {g.play("tail_pillar_sink")}',
         f'execute if score #azPT mb matches {B.B3_EMERGE}.. run {g.play("burrow_emerge")}',
         'scoreboard players set #azBur mb 0',
         f'execute if score #azPT mb matches {B.B3_TAILUP}..{B.B3_OUT - 1} run scoreboard players set #azBur mb 1',
         f'execute if score #azPT mb matches {B.B3_TAILUP}..{B.B3_BURST - 1} if score #azB3Sp mb matches 1.. run {g.b3_special("reload")}',
         f'execute if score #azPT mb matches {B.B3_TAILUP}..{B.B3_BURST - 1} unless score #azB3Sp mb matches 1.. run {g.b3_special("start")}',
         f'execute if score #azPT mb matches {B.B3_EMERGE_HZ}..{B.B3_BURST - 1} at {ARENA_M} run function {NS}p/{key}/emerge']
    g.pw(key, 'reload', r)


def _leg_dispatch(fn):
    return [f'execute if score #azLeg mb matches {e} run {fn(e)}' for e in A.LEG_ELS]


def _tail_dispatch(fn):
    return [f'execute if score #azTail mb matches {e} run {fn(e)}' for e in A.TAIL_ELS]


def emit(g):
    slide(g)
    absorb1(g)
    absorb2(g)
    burrow3(g)
