"""S2-S: the transition services 20 파멸의 산사태 (landslide), 21 absorb 1, 22 absorb 2 and 23 the B3 frame (plan.md
4.3, 4.4, 4.8, 5 T1-T3, B3, Change notes 1 / 3; s2.md 7, 11, 17, 18). Built on S1-MOD's working stub: the clocks, the
core calls (cine, proxy states, looks, the arena recolour, phases and floors, music, the leg special's cast at the
absorb-1 roar, the B3 special start / tick / stop, the tail window, the surfacing and "마지막 일격!") and the service
interfaces of s2.md 7 / 11 / 18 are unchanged; this file adds the real choreography (h_ps.py holds the schedules).

The core sequences them (core tr/*): transition 1 = message -> 20 -> 21 -> phase 2; transition 2 = message -> the leg
special first (core service 30) -> 20 -> 22 -> 23 -> phase 3. #azTrN = 1 / 2 tells the services which one runs (0 = a
test request outside a transition: the transition-1 lines). Every service declares `reload` (plan 4.3: a cut landslide
goes on to its next wave, a cut absorb finishes at once with its looks, a cut B3 resumes at its frame tick); the core
also starts the B3 at a later tick through its reload (tests 25 and 61).

Telegraphs (Change note 1): T1's fronts and the B3 surfacing are *none* rows: no ground decal; the landslide is read from
the lift poses of the clip (each wave's fore lifts from the previous slam, the wave-6 rear-up hangs 20 t), the lift and
growl sounds, the transition banner / typed lines (no jump prompt on the HUD, user 10-21); the surfacing from the dust
mound over the centre (B3_MOUND) and its rumble. Every hit shows its impact visual at the strike (the travelling front
p/front, the slam impact / dust ring; the earth-spike burst). The B3 crater is decor (footage), not a hit.

T1 facing (R3a note, rig API 12): the landslide clip has no yaw schedule and its feet stay planted, so the module turns
the anchor only in the lead before the clip, while the walk clip steps (walking to the centre, or stepping in place when
the boss already stands there and must turn more than 20 degrees); from the clip start the yaw is fixed (#azNoTurn).
"""
from . import api as A
from . import h_ps as H
from .api import TL, L

K = A.K
NS = A.NS
BODY = A.BODY
ARENA_M = A.ARENA_M
CY = A.CY
SLIDE_LEAD = H.SLIDE_LEAD
SLIDE = A.clip_len('landslide')
SLIDE_EV = {k: SLIDE_LEAD + v for k, v in A.CLIPS['landslide']['events'].items()}
SLIDE_END = SLIDE_LEAD + SLIDE                        # 243
WAVES_SPEC = H.slide_waves()
WAVES = [w['strike'] for w in WAVES_SPEC[:5]]
WAVE6 = WAVES_SPEC[5]['strike']
ABS1 = A.clip_len('absorb')                           # 94
ABS1_EV = A.CLIPS['absorb']['events']
ABS1_BURST = ABS1_EV['burst']                         # 47
ROAR = A.clip_len('roar_rear')                        # 82
ROAR_EV = A.CLIPS['roar_rear']['events']
ROAR_R = ROAR_EV['roar']                              # 20
ABS1_END = ABS1 + ROAR                                # 176
ABS2 = A.clip_len('absorb_p3')                        # 52
ABS2_EV = A.CLIPS['absorb_p3']['events']
ABS2_BURST = ABS2_EV['burst']                         # 42
ABS2_END = ABS2 + ROAR                                # 134
BACK = A.CLIPS['absorb']['anchors']['burst']['back']  # the orb / discharge point over the back (local x, y, z)
CRATER_UUID = '[I;1380731725,1096434688,-2147483648,129]'    # 524c4b4d-415a-4400-8000-000000000081 (Rig decision change 3)
CRATER_TAG = 'rlk_mb_az_p23c'
PUSH_RING = '{r:80,to:85,kb:4}'                       # the absorb bursts' push-only ring r 8 (plan 4.4, cm.md 13.5)

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
              hooks=('reload', 'resume')),
]
assert WAVES == [97, 117, 138, 158, 179] and WAVE6 == 219 and SLIDE_END == 243
assert ABS1_BURST == 47 and ABS2_BURST == 42 and ROAR_R == 20


def _tr(n):
    return f'execute if score #azTrN mb matches {n} run '


def _flat(x):
    return list(H.flat([x]))


def _leg(fn):
    """One line per rolled leg element (#azLeg 1 Pyro / 2 Hydro)."""
    return [f'execute if score #azLeg mb matches {e} run {fn(e)}' for e in A.LEG_ELS]


def _tail(fn):
    return [f'execute if score #azTail mb matches {e} run {fn(e)}' for e in A.TAIL_ELS]


def _pt(p):
    """The local (x, z) of a rest anchor."""
    x, _y, z = A.REST[p]
    return x, z


def _centre(lines):
    return [f'execute at {ARENA_M} run {ln}' for ln in _flat(lines)]


# ============================================================================================ 20 파멸의 산사태
def slide(g):
    key = 'slide'
    tl = TL(g, key)
    F = lambda rel: f'function {NS}p/{key}/{rel}'               # noqa: E731
    G = H.GLIDE_MAX
    # ---- the lead (0 .. SLIDE_LEAD - 1): walk to the centre / step-turn in place, the only turning of the service
    near = ARENA_M.replace('limit=1', 'distance=..{d},limit=1')
    lead = ['# T1 lead (@s = body): walk to <= 2 b of the arena centre (the glide length from the distance, GLIDE_SPD',
            f'# {H.GLIDE_SPD} b/t, {H.GLIDE_MIN}-{H.GLIDE_MAX} t, then walk_stop) or, already there, step-turn in place when',
            '# the player is more than 20 degrees off the facing; the turn runs only until the clip starts (the landslide',
            '# clip keeps its feet planted: no yaw schedule, R3a note).',
            'scoreboard players set #aq20W mb 0', 'scoreboard players set #aq20S mb 0', 'scoreboard players set #aq20M mb 0',
            f'scoreboard players set #aq20G mb {G}',
            f'execute positioned ~ {CY} ~ unless entity {near.format(d=2)} run scoreboard players set #aq20W mb 1']
    for d, t in ((6.0, 20), (4.8, 16), (3.6, 12), (2.4, 8)):
        assert t >= H.glide_ticks(d) - 1, (d, t)
        lead.append(f'execute positioned ~ {CY} ~ if entity {near.format(d=d)} run scoreboard players set #aq20G mb {t}')
    lead += ['execute store result storage rlk:mboss az.p20.t int 1 run scoreboard players get #aq20G mb',
             f'execute if score #aq20W mb matches 1 at {ARENA_M} run function rlk:mboss/mv/glide with storage rlk:mboss az.p20',
             f'execute if score #aq20W mb matches 0 run {F("yerr")}',
             'execute if score #aq20W mb matches 0 if score #aq20Y mb matches 2001.. run scoreboard players set #aq20S mb 1',
             'execute if score #aq20S mb matches 1 run scoreboard players set #aq20G mb 8',
             'execute if score #aq20S mb matches 1 if score #aq20Y mb matches 3201.. run scoreboard players set #aq20G mb 16',
             'execute if score #aq20S mb matches 1 if score #aq20Y mb matches 6401.. run scoreboard players set #aq20G mb 24',
             'execute if score #aq20W mb matches 1 run scoreboard players set #aq20M mb 1',
             'execute if score #aq20S mb matches 1 run scoreboard players set #aq20M mb 1',
             f'execute if score #aq20M mb matches 1 run {g.play("walk")}',
             f'execute if score #aq20M mb matches 0 run {g.play("idle")}']
    g.pw(key, 'lead', lead)
    g.pw(key, 'yerr', [
        '# #aq20Y = |yaw to the player - the facing| x 100 (0 .. 18000), as rlk:mboss/mv/turn measures it.',
        'execute store result score #aq20Y mb run data get entity @s Rotation[0] 100',
        'execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_help"]}',
        'execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @e[tag=rlk_mb_help,limit=1] ~ ~ ~ ~ 0',
        'execute store result score #t mb run data get entity @e[tag=rlk_mb_help,limit=1] Rotation[0] 100',
        'kill @e[type=minecraft:marker,tag=rlk_mb_help]',
        'scoreboard players operation #t mb -= #aq20Y mb', 'scoreboard players add #t mb 90000',
        'scoreboard players operation #t mb %= #c36000 mb', 'scoreboard players remove #t mb 18000',
        'execute if score #t mb matches ..-1 run scoreboard players operation #t mb *= #cm1 mb',
        'scoreboard players operation #aq20Y mb = #t mb'])
    tl.at(0, 'scoreboard players set #mbNoLeash mb 1', F('lead'))
    # ---- the clip and its tell
    c = lambda t: SLIDE_LEAD + t                                # noqa: E731  service tick of clip tick t
    tl.at(c(0), g.play('landslide'), g.sound('entity.ender_dragon.growl', 0.7, 0.55), g.sound('entity.ravager.ambient', 0.8, 0.5))
    lifts = H.slide_lifts()
    for t in lifts:
        tl.at(c(t), K.snd('slide_lift'))
    # the two tell lifts plant again (right fore 40, right hind 56 authored)
    for auth, paw in ((40, 'paw_fr'), (56, 'foot_hr')):
        x, z = _pt(paw)
        tl.at(c(A.rt('landslide', auth)), *H.at_local(x, z, g.fxe('footfall', 'ground')), g.snde('footfall', 'ground'))
    # ---- the six fronts (N10, plan 5 T1 sizes and ticks; nododge, low 0.7; *none* row: no pre-strike decal)
    for w in WAVES_SPEC:
        k, s = w['k'], w['strike']
        g.wave(tl, s, w['r0'], w['r1'], w['spd'], w['band'], 20, A.DMG[w['dmg']], nd=1, el='ground', grp='new', low=0.7,
               wid=k - 1, tag=f'rlk_mb_az_p20w{k}')
        # the impact at the slam: between the fores (w1), the slamming fore (w2-w5), the chest (w6); dust; rocks after
        if k == 1:
            ix, iz = 0.0, _pt('paw_fl')[1]
        else:
            ix, iz = _pt(w['paws'][0])
        hits = [*H.at_local(ix, iz, g.fxe('impact', 'ground'))]
        if k == 6:
            # (FIX STATE-2) wave 6's dust ring and first rock rain 1 t after the chest impact (one tick of the fronts' start,
            # the impact and both presets went over 3000 commands)
            hits += [K.snd('slide_wave6')]
            tl.at(s + 1, *g.fxe('dust_ring', 'ground', r=6.0), K.fx('rock_rain', r=12.0))
        else:
            hits += [K.snd('slide_wave')]
        tl.at(s, *hits)
        tl.at(s + 4, K.fx('rock_rain', r=8.0 if k < 6 else 14.0))
    # the rear-up before wave 6 (the visual wave-6 cue): a roar at the top, held 20 t
    tl.at(SLIDE_EV['rear'], g.sound('entity.ravager.roar', 1.0, 0.5), g.sound('entity.ender_dragon.growl', 0.8, 0.6))
    tl.at(SLIDE_EV['w1'], _tr('..1') + g.line(LINES_T1['w1']), _tr(2) + g.line(LINES_T2['w1']))
    tl.at(SLIDE_EV['w3'], _tr(2) + g.line(LINES_T2['w3']))
    tl.at(SLIDE_EV['rear'], g.line(LINES_T1['rear']))
    tl.at(SLIDE_END, 'scoreboard players set #mbNoLeash mb 0', g.end())
    extra = [f'execute if score #azPT mb matches ..{SLIDE_LEAD - 1} run scoreboard players set #azNoPush mb 1',
             f'execute if score #azPT mb matches ..{SLIDE_LEAD - 1} if score #aq20M mb matches 1 run function rlk:mboss/mv/turn {{max:4}}',
             f'execute if score #azPT mb matches ..{SLIDE_LEAD - 1} if score #aq20M mb matches 0 run function rlk:mboss/mv/turn {{max:1}}',
             f'execute if score #azPT mb matches ..{SLIDE_LEAD - 1} if score #aq20M mb matches 1 if score #azPT mb = #aq20G mb run {g.play("walk_stop")}',
             f'execute if score #azPT mb matches {SLIDE_LEAD}.. run scoreboard players set #azNoTurn mb 1']
    tl.write([f'# 20 파멸의 산사태 (S2-S; plan 5 T1): lead 0-{SLIDE_LEAD - 1} (walk / step-turn to the centre, the only turn),',
              f'# the clip at {SLIDE_LEAD} (anchor fixed); fronts {WAVES} r 4 -> 18 at 3 b/t, wave 6 {WAVE6} r 4 -> 30 at 4 b/t',
              '# (nododge, low 0.7, internal tell 20, Geo at transition 1 / the leg element + brand at transition 2; no',
              f'# pre-strike decal: Change note 1; no jump prompt: the lift poses and sounds are the tell); end {SLIDE_END}.'],
             [f'# {key} tick (#azPT; the clip tick = #azPT - {SLIDE_LEAD}).'], extra_tick=extra)
    g.pw(key, 'cancel', ['# Fronts and the walk go (selectors only).',
                         f'execute as {BODY} run function rlk:mboss/mv/stop',
                         'scoreboard players set #mbNoLeash mb 0']
         + [f'kill @e[type=minecraft:marker,tag=rlk_mb_az_p20w{k}]' for k in range(1, 7)])
    g.pw(key, 'reload', [
        '# /reload inside the landslide: the hazards are gone, the clock goes on and the next wave comes (plan 4.3). A cut',
        '# walk ends at the centre at once. (The rig respawns in idle: it cannot resume a clip mid-way, so the remaining',
        '# waves keep their sounds but not the lift poses.)',
        'scoreboard players set #mbNoLeash mb 1',
        f'execute if score #azPT mb matches ..{SLIDE_LEAD - 1} as {BODY} at {ARENA_M} run tp @s ~ ~ ~',
        f'execute if score #azPT mb matches ..{SLIDE_LEAD - 1} run scoreboard players set #aq20M mb 0'])


# ============================================================================================ 21 absorb 1
def absorb1(g):
    key = 'absorb1'
    tl = TL(g, key)
    R = ABS1 + ROAR_R
    fl, fr = _pt('paw_fl'), _pt('paw_fr')
    tl.at(0, g.cine(True), g.px('inv'), g.glow(True),
          *_leg(lambda e: K.fxe('vortex', e, t=ABS1_BURST)), *_leg(lambda e: K.fxe('sigils', e)),
          *_leg(lambda e: K.snde('absorb_vortex', e)))
    tl.at(24, *_leg(lambda e: K.snde('absorb_vortex', e)), *_leg(lambda e: K.fxe('sigils', e)))
    # burst: the legs look, the arena recolour wave, the push-only ring r 8 with its dome, the banner
    # (FIX STATE-2) the dust ring 1 t and the recolour wave 2 t after the burst tick (as absorb 2's burst)
    tl.at(ABS1_BURST, g.look_legs(), g.arena_look('leg'), A.fw('push/ring', PUSH_RING), g.banner('ab'),
          *_leg(lambda e: K.snde('absorb_burst', e)), K.fx('shock_dome', r=8.0),
          *H.at_local(0, fl[1], _leg(lambda e: K.fxe('impact', e))))
    tl.at(ABS1_BURST + 1, *_leg(lambda e: K.fxe('dust_ring', e, r=8.0)))
    tl.at(ABS1_BURST + 2, *_leg(lambda e: K.fxe('recolour', e, r=28.0, t=20)))
    tl.at(ABS1_EV['gold_off'], g.glow(False))
    # pawing the ground (the stamps: left fore, then right)
    for ev_, (x, z) in (('stamp1', fl), ('stamp2', fr)):
        tl.at(ABS1_EV[ev_], *H.at_local(x, z, _leg(lambda e: K.fxe('footfall', e))), *_leg(lambda e: K.snde('footfall', e)))
    # t94: phase 2 (floor F2, music 2), roar_rear + the leg special (its cast clock 0)
    tl.at(ABS1, g.phase(2), g.play('roar_rear'), g.cast_leg())
    # the roar: cine ends, gameplay resumes, so the brand banner (once per fight; REQ ps-3) replaces the absorb banner here
    tl.at(R, g.line(LINE_ABS1), K.snd('absorb_roar'), g.cine(False), g.px('normal'), g.banner('brand'))
    for dt in H.roar_rings(1):
        tl.at(R + dt, K.fx('shock_dome', r=8.0 + dt / 4), K.snd('roar_ring'))
    tl.at(ABS1 + ROAR_EV['land'], *H.at_local(*fl, _leg(lambda e: K.fxe('footfall', e))),
          *H.at_local(*fr, _leg(lambda e: K.fxe('footfall', e))), *_leg(lambda e: K.snde('footfall', e)))
    tl.at(ABS1_END, g.end())
    tl.write([f'# 21 absorb 1 (S2-S; plan 5 T2, 4.4): cine + untargetable; the vortex and sigils of the leg element; burst',
              f'# {ABS1_BURST}: the legs look, the arena, the push ring r 8; {ABS1}: phase 2 (floor F2, music 2), roar_rear + the',
              f'# leg special; roar {R}: the line, the brand banner, the dome rings, cine ends.'],
             [f'# {key} tick.'])
    g.pw(key, 'cancel', ['# Immediate cleanup: the cine and the gold glow end.', g.cine(False), g.glow(False)])
    g.pw(key, 'reload', ['# /reload inside absorb 1: it finishes at once (plan 4.3): the looks, phase 2, targetable again.',
                         f'execute if score #azPT mb matches ..{ABS1 - 1} run {g.phase(2)}',
                         '# (FIX STATE-6) the leg special that opens phase 2 (plan 5 T2) was not cast yet, or its cast part is cut by',
                         '# the core reload (orbs not out yet): the first phase-2 decision runs it (service 30 with its own roar)',
                         f'execute if score #azPT mb matches ..{ABS1 - 1} unless score #azBgL mb matches 31 run function {NS}p/{key}/requeue',
                         f'execute if score #azPT mb matches {ABS1}.. if score #azCast mb matches 31..32 unless score #azBgL mb matches 31 '
                         f'run function {NS}p/{key}/requeue',
                         g.look_legs(), g.arena_look('leg'), g.cine(False), g.glow(False), g.px('normal'), g.banner('brand'),
                         g.end()])
    g.pw(key, 'requeue', ['# The leg special as the next pick (#azReq 30 = the cast host; #azCastReq = the rolled leg element\'s).',
                          'execute if score #azLeg mb matches 2 run scoreboard players set #azCastReq mb 31',
                          'execute if score #azLeg mb matches 1 run scoreboard players set #azCastReq mb 32',
                          'scoreboard players set #azReq mb 30'])


# ============================================================================================ 22 absorb 2
def absorb2(g):
    key = 'absorb2'
    tl = TL(g, key)
    R = ABS2 + ROAR_R
    fl, fr = _pt('paw_fl'), _pt('paw_fr')
    bx, by, bz = BACK
    back = lambda lines: H.at_local(bx, bz, lines, y=by)          # noqa: E731
    tl.at(0, g.cine(True), g.px('inv'), g.glow(True),
          *_tail(lambda e: K.fxe('vortex', e, t=ABS2_BURST)), *_tail(lambda e: K.fxe('sigils', e)),
          *_tail(lambda e: K.snde('absorb_vortex', e)))
    # the gather over the back: Electro bolts strike onto it ([v5] E, [v6] A), Cryo ice gathers ([v7] C)
    for t in (12, 24, 34):
        tl.at(t, f'execute if score #azTail mb matches 3 run {back(K.fx("bolt"))[0]}',
              f'execute if score #azTail mb matches 4 run {back(K.fx("hail", r=3.0))[0]}')
    tl.at(21, *_tail(lambda e: K.snde('absorb_vortex', e)))
    # burst: the tail look, phase 3 (floor 1), the arena, the push ring, the shard rain / bolts, the flash
    # (FIX STATE-2) the burst's visuals over four ticks (one tick of ~36 new cards + the push ring went over 3000
    # commands): the burst tick keeps the state, the push ring, the impact, the dome, the flash and the Electro bolt;
    # the Cryo frost burst +1, the shard rain +2 (it runs to +48 anyway), the recolour wave +3
    tl.at(ABS2_BURST, g.look_tail(), g.arena_look('tail'), g.banner('ab2'), g.line(LINE_ABS2_BURST), g.phase(3),
          A.fw('push/ring', PUSH_RING), *_tail(lambda e: K.snde('absorb_burst', e)),
          *H.at_local(0, fl[1], _tail(lambda e: K.fxe('impact', e))), K.fx('shock_dome', r=8.0),
          f'execute if score #azTail mb matches 3 run {back(K.fx("bolt"))[0]}',
          f'execute if score #azTail mb matches 3 run {K.hud("flash_violet")}',
          f'execute if score #azTail mb matches 4 run {K.hud("flash_white")}')
    tl.at(ABS2_BURST + 1, f'execute if score #azTail mb matches 4 run {K.fx("frost_burst", r=6.0)}')
    tl.at(ABS2_BURST + 2, *_centre(_tail(lambda e: K.fxe('shard_rain', e, r=20.0, t=46))))
    tl.at(ABS2_BURST + 3, *_tail(lambda e: K.fxe('recolour', e, r=28.0, t=20)))
    tl.at(ABS2_EV['gold_off'], g.glow(False))
    tl.at(ABS2, g.play('roar_rear'))
    tl.at(R, g.line(LINE_ABS2_ROAR), K.snd('absorb_roar'), g.cine(False), g.px('normal'))
    rings = {}
    for e in A.TAIL_ELS:
        for dt in H.roar_rings(e):
            rings.setdefault(dt, []).append(e)
    for dt, els in sorted(rings.items()):
        lines = [K.fx('shock_dome', r=8.0 + dt / 4), K.snd('roar_ring')]
        if len(els) == len(A.TAIL_ELS):
            tl.at(R + dt, *lines)
        else:
            for e in els:
                tl.at(R + dt, *[f'execute if score #azTail mb matches {e} run {ln}' for ln in lines])
    tl.at(ABS2 + ROAR_EV['land'], *H.at_local(*fl, g.fxe('footfall', 'ground')), *H.at_local(*fr, g.fxe('footfall', 'ground')),
          g.snde('footfall', 'ground'))
    tl.at(ABS2_END, g.end())
    tl.write([f'# 22 absorb 2 (S2-S; plan 5 T3, 4.4): cine + untargetable; the element gathers over the back; burst {ABS2_BURST}:',
              f'# the tail look, phase 3, #mbFloor 1, the shard rain, the push ring; {ABS2}: roar_rear (no cast); roar {R}: the',
              '# line, the dome rings, cine ends; then the B3 frame.'], [f'# {key} tick.'])
    g.pw(key, 'cancel', ['# Immediate cleanup.', g.cine(False), g.glow(False)])
    g.pw(key, 'reload', ['# /reload inside absorb 2: it finishes at once (the tail look, phase 3, floor 1), then the B3.',
                         f'execute if score #azPT mb matches ..{ABS2_BURST - 1} run {g.phase(3)}',
                         g.look_tail(), g.arena_look('tail'), g.cine(False), g.glow(False), g.px('normal'), g.end()])


# ============================================================================================ 23 the B3 frame
def burrow3(g):
    key = 'burrow3'
    tl = TL(g, key)
    B = A
    F = lambda rel: f'function {NS}p/{key}/{rel}'               # noqa: E731
    centre = f'execute at {ARENA_M} run '
    fl, fr = _pt('paw_fl'), _pt('paw_fr')
    # t0: the dig in place (the tail element's mounds / ice puffs / violet slabs), the crater outline growing at the
    # centre (decor from the footage), the sink rumble
    tl.at(0, f'{centre}{K.tele_crater(7.5, B.B3_GLIDE[0], hold=3)}', *g.fxe('dig', 'tail'), K.snd('b3_sink'),
          'scoreboard players set #mbNoLeash mb 1', 'scoreboard players set #azB3Sp mb 0')
    tl.at(B.B3_INV, g.px('inv'), *H.at_local(*fl, K.fx('mound')), *H.at_local(*fr, K.fx('mound')))
    for t, (x, z) in ((16, (4.0, -2.0)), (24, (-4.0, -2.0)), (32, (0.0, -5.0))):
        tl.at(t, *H.at_local(x, z, K.fx('mound')), K.snd('burrow_loop'))
    tl.at(20, *g.fxe('dig', 'tail'))
    # t40: under (the body hidden by the clip); the hidden glide to the centre; the crater at the floor cut
    tl.at(B.B3_GLIDE[0], f'execute at {ARENA_M} run function rlk:mboss/mv/glide {{t:{B.B3_GLIDE[1] - B.B3_GLIDE[0]}}}',
          F('crater'))
    # t58: the tail rises out of the centre (tail_only, #azBur 1; no sub-line hint), the special starts
    tl.at(B.B3_TAILUP, g.px('tail_only'), 'scoreboard players set #azBur mb 1', g.b3_special('start'), K.snd('b3_rise'),
          *_centre([K.fx('mound')] + g.fxe('dust_ring', 'tail', r=3.0)))
    for t in H.b3_pulses():
        tl.at(t, *_centre(g.fxe('footfall', 'tail')))           # frost / sparks at the pillar foot (2-3 cards)
    # t335: the tail drops into the floor (an olive dust burst replaces it); the mound over the hole is the tell of the
    # surfacing (Change note 1: B3_MOUND + the rumble; the emergence hazard is made at B3_EMERGE_HZ without a decal)
    tl.at(B.B3_TAILSINK, g.play('tail_pillar_sink'), g.px('inv'), *_centre([K.fx('dust'), K.fx('mound')]), K.snd('b3_sink'))
    for t in H.b3_mounds():
        tl.at(t, *_centre([K.fx('mound'), K.snd('burrow_loop'),
                           L.sound('entity.ravager.step', 0.8, 0.5), L.sound('block.gravel.break', 0.7, 0.5)]))
    tl.at(B.B3_EMERGE_HZ, f'execute at {ARENA_M} run {F("emerge")}')
    tl.at(B.B3_EMERGE, g.play('burrow_emerge'))
    # t388: the emergence burst (the special stops): the earth-spike cluster, boulders, the impact
    tl.at(B.B3_BURST, g.b3_special('stop'), *_centre([K.fx('emerge_spikes', r=5.2), K.fx('rock_rain', r=6.0),
                                                       K.snd('b3_emerge')] + g.fxe('impact', 'ground')))
    tl.at(B.B3_EMERGE + 31, *H.at_local(*fl, g.fxe('footfall', 'ground')), *H.at_local(*fr, g.fxe('footfall', 'ground')),
          g.snde('footfall', 'ground'))
    # the surfacing ends the transition (tr/done: #azTr 0, the FLANK skip, the cooldown): the fight is on again for the
    # last 15 t of the frame ("마지막 일격!")
    tl.at(B.B3_OUT, g.px('normal'), g.floor(0), 'scoreboard players set #azBur mb 0', f'function {NS}tr/done',
          f'execute as {BODY} if score @s mhpC matches ..1 run {F("last")}',
          f'kill @e[type=minecraft:item_display,tag={CRATER_TAG}]', *_centre(K.fx('dust')))
    tl.at(B.B3_END, 'scoreboard players set #mbNoLeash mb 0', g.end())
    tl.write([f'# 23 the B3 frame (S2-S; plan 5 B3, s2.md 7): #azB3T = #azPT; dig, inv {B.B3_INV}, the hidden glide to the',
              f'# centre {B.B3_GLIDE} and the crater, tail-up {B.B3_TAILUP} (tail_only, #azBur 1, the special starts), sink',
              f'# {B.B3_TAILSINK}, dust mound {B.B3_MOUND}, emergence hazard {B.B3_EMERGE_HZ} (no decal), burst {B.B3_BURST} (the',
              f'# special stops), out {B.B3_OUT} (normal, floor 0), end {B.B3_END}.'],
             [f'# {key} tick: the B3 clock, the special\'s tick in the tail window.',
              'scoreboard players operation #azB3T mb = #azPT mb',
              'scoreboard players set #azNoPush mb 1',
              f'execute if score #azPT mb matches {B.B3_TAILUP + 1}..{B.B3_BURST - 1} run {g.b3_special("tick")}'],
             extra_tick=())
    g.pw(key, 'crater', ['# The B3 crater (decor, footage v6 10.55-11.15 s): the kit crater prop at the floor cut of the arena',
                         '# centre, fixed UUID 0x81 (Rig decision change 3); re-made by reload / resume; gone at the surfacing.',
                         f'kill @e[type=minecraft:item_display,tag={CRATER_TAG}]',
                         f'execute at {ARENA_M} positioned ~ {L.num(CY + 0.03, 2)} ~ run summon minecraft:item_display ~ ~ ~ '
                         f'{{UUID:{CRATER_UUID},Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","{CRATER_TAG}"],'
                         'Rotation:[0f,0f],billboard:"fixed"}',
                         f'execute as @e[type=minecraft:item_display,tag={CRATER_TAG}] run {K.prop("crater")}'])
    g.pw(key, 'emerge', [f'# The emergence burst at the centre: disc r 5.2, internal tell {B.B3_BURST - B.B3_EMERGE_HZ}, no decal',
                         '# (plan Change note 1: the dust mound of B3_MOUND is the tell),',
                         '# the leg element + brand, dodgeable (step away from the surfacing spot).',
                         g.GRP_NEW] + g.hz_opts(grp=True, kb=A.KB['heavy']) + g.el_ground()
         + [L.hz_disc(5.2, B.B3_BURST - B.B3_EMERGE_HZ, A.DMG['b3_emerge']), g.tag_last_hz('rlk_mb_az_p23e')])
    # (FIX STATE-16) /reload inside the emergence window: the hazard again with the ticks left to the burst (it strikes
    # with the visible burst at B3_BURST, not a full tell after the reload)
    rem = L.hz_disc(5.2, 1, A.DMG['b3_emerge']).replace('tell:1,', 'tell:$(tell),')
    assert '$(tell)' in rem, rem
    g.pw(key, 'emerge_r', ['# Reload re-make of the emergence: the remaining tell (B3_BURST - 1 - #azPT, at least 1).',
                           # the reload hook runs before this tick's #azPT step, so the hazard made now strikes on (#azPT + 1) + tell
                           f'scoreboard players set #aq23T mb {B.B3_BURST - 1}', 'scoreboard players operation #aq23T mb -= #azPT mb',
                           'execute if score #aq23T mb matches ..0 run scoreboard players set #aq23T mb 1',
                           'execute store result storage rlk:mboss az.p23.tell int 1 run scoreboard players get #aq23T mb',
                           f'function {NS}p/{key}/emerge_m with storage rlk:mboss az.p23'])
    g.pw(key, 'emerge_m', ['# Macro {tell}: the emergence burst at the centre with the given tell.', g.GRP_NEW]
         + g.hz_opts(grp=True, kb=A.KB['heavy']) + g.el_ground()
         + ['$' + rem if not rem.startswith('$') else rem, g.tag_last_hz('rlk_mb_az_p23e')])
    g.pw(key, 'last', ['# HP 1 at the surfacing: "마지막 일격!" (the next hit kills through the normal path); a gold glow on the',
                       '# body (the gold parts lit) and gold motes at every hit proxy.',
                       'scoreboard players set #azLastHit mb 1', 'scoreboard players set #azHudQ mb 1', g.glow(True),
                       'execute as @e[tag=rlk_mb_px] at @s run particle minecraft:wax_on ~ ~1 ~ 0.4 0.8 0.4 0 6 force @a[tag=player]',
                       K.snd('hint')])
    g.pw(key, 'cancel', ['# The special is cancelled, the burrow state ends (selectors only).', g.b3_special('cancel'),
                         'scoreboard players set #azBur mb 0', 'scoreboard players set #mbNoLeash mb 0',
                         'kill @e[type=minecraft:marker,tag=rlk_mb_az_p23e]',
                         f'kill @e[type=minecraft:item_display,tag={CRATER_TAG}]'])
    g.pw(key, 'resume', ['# Resume after a pause: the kit cleared the growing crater outline; the crater prop now instead.',
                         f'execute if score #azPT mb matches ..{B.B3_GLIDE[0] - 1} run {F("crater")}'])
    # resume at the frame tick (/reload, tests 25 / 61): the state of #azPT
    r = ['# The B3 resumes at its frame tick #azPT (plan 4.3; tests 25 / 61 start here): the proxy state, the rig clip, the',
         '# anchor at the centre after the glide, #azBur, the special (re-made from the current B3 tick, or started), the crater.',
         'scoreboard players operation #azB3T mb = #azPT mb', 'scoreboard players set #mbNoLeash mb 1',
         f'execute if score #azPT mb matches {B.B3_GLIDE[0]}..{B.B3_EMERGE + 37} as {BODY} at {ARENA_M} run tp @s ~ ~ ~',
         '# (FIX STATE-4: from the glide\'s start: the body is hidden from t40, the stopped glide would leave it off-centre)',
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
         f'execute if score #azPT mb matches {B.B3_EMERGE_HZ}..{B.B3_BURST - 1} at {ARENA_M} run {F("emerge_r")}',
         f'execute if score #azPT mb matches ..{B.B3_OUT - 1} run {F("crater")}']
    g.pw(key, 'reload', r)


def emit(g):
    slide(g)
    absorb1(g)
    absorb2(g)
    burrow3(g)
