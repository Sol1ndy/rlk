"""The 야타용왕 AI (plan.md 4.12; s2.md 4.1, 4.3): zones in the anchor frame (mv/local, cm.md 13.2), the FLANK rule with
dwell, the P7 exit test (generated from the api constants), the weighted tables built from the PATTERNS of the pattern
modules, no immediate repeat (except P2 at half weight and P5 up to 2 in a row), cooldowns, the gates (anchor8,
front35, exit, field_area, no_bg in phase 3, no_live), the phase-3 replacements (4 -> 45 / 46, a fore-paw 5 -> 10), the
anti-stall turn180, idle tracking / turn steps / the walk, the module leash to the body disc and the "first" lines.
Called by core.emit (AZ:ai/**).

Decision order (plan 4.12): test request > lock > queued transition > (the B3 frame is a service) > the leg special at
the phase start (the absorb's cast) > anti-stall > FLANK rule > weighted pick > fallbacks.

Zones (#azZone 1 head_near 2 head_mid 3 head_far 4 flank_near 5 flank_far 6 tail_lane 7 tail_off 8 paw), classified
every 4 t by ai/sample and again at every pick: PAW (within 2.8 b of a paw / foot, or under the body: |s| < 3.0 and
-4.8 <= f < 3.6) first, then HEAD (f >= 3.6 and |s| <= 4 + 0.6 (f - 3.6); bands by the anchor distance near <= 9,
mid <= 15, far), TAIL (f < -4.8: lane |s| <= 3.5, else off), FLANK (near |s| <= 9, else far). The FLANK-near test of
the rule (#azFN) is the plan's own (3 <= |s| <= 9, -4.8 <= f < 3.6), independent of the PAW precedence. Deviations
kept for the balance fixer: P5's flank_near 2 (paw <= 2.8) and tail_off 1 (hind <= 2.8) cannot fire (those points are
PAW, weight 5); idle turn steps only for players beyond the near band (the flank and the tail stay the patterns'
business, plan 4.12 FLANK rule / anti-stall).
"""
from . import api as A

WEIGHT_OVERRIDE = {}           # the balance fixer: {pattern id: {phase: {zone: w}}}
REPEAT_HALF = {2}              # may repeat at half weight
REPEAT_MAX = {5: 2}            # at most n in a row
FLANK_PX = (2, 3, 4, 9, 10, 11, 12)     # proxies chest belly hips paw_l paw_r foot_l foot_r (mbPart = layout index + 1)
FLANK_CHANCE = 90
DWELL_N, DWELL_MIN = 6, 4      # FLANK-near for >= 16 of the last 24 t, sampled every 4 t
PROXY_GT = 40
# s2.md 2 gates / plan 4.7: field_area applies to every field-making pick: 32 and 45 always, P1 / P2 / P5 / P5b only
# while their Pyro addons run (Pyro legs, phase >= 2), P8 only in phase 3 (its strip). A pattern declares the gate; these
# conditions are added here.
FIELD_AREA_WHEN = {1: 'if score #azLeg mb matches 1 if score #azPh mb matches 2.. ',
                   2: 'if score #azLeg mb matches 1 if score #azPh mb matches 2.. ',
                   5: 'if score #azLeg mb matches 1 if score #azPh mb matches 2.. ',
                   10: 'if score #azLeg mb matches 1 if score #azPh mb matches 2.. ',
                   8: 'if score #azPh mb matches 3 '}
SKIP_AFTER = (2, 7, 8, 9, 20, 21, 22, 23)
TAIL_PATS = (7, 8)
ANTI_STALL = 3
TURN_IDLE = 3                  # deg/t while |dyaw| <= 45
TURN_LEAD = 4                  # deg/t during a front pattern's pre-turn lead
WALK_SPD = 0.13
WALK_MAX = 40
WALK_CHANCE = 25               # % of the decisions in the far band that walk first
FAR_WALK = A.BAND_MID          # beyond 15 b
LINES = {'p2': '갈라져라! 부서져라!', 'p39': '모락스…!! 빚을 청산할 때가 왔다!', 'p7': '버러지 같은 것들! 교활한 놈!',
         'tail': '가루로… 만들어주마! 흙으로… 돌아가라!',
         'flank1': '옆구리는 위험합니다 — 머리 정면 · 꼬리 끝으로', 'flank1f': '옆구리는 위험합니다 — 머리 정면 · 꼬리 끝으로 · 대시로 바깥쪽으로'}
HINTS = {1: '꼬리를 높이 들면: 머리 정면으로 들어가거나 꼬리 반대편으로 넘어가세요', 2: '옆구리 금지 — 머리 정면 · 꼬리 끝',
         3: '응결 결정 — 주우면 보호막'}

MB = 1000                      # milliblocks
T10 = 10                       # tenths


def mb(v):
    return int(round(v * MB))


def emit(core):
    g, F = core.g, core.F
    w = core.w
    sc = lambda n, v: f'scoreboard players set {n} mb {int(v)}'   # noqa: E731
    BODY, ARENA_M, PLAYER = A.BODY, A.ARENA_M, A.PLAYER
    pats = core.pats
    picks = [p for p in pats if p.kind in ('normal', 'cast', 'bg') and p.replaces is None]

    # ------------------------------------------------------------------ the sampler
    paw = A.P_PAW
    samp = ['# @s = body (every 4 t and at every pick): the player in the anchor frame (#mbLf / #mbLs, mb), the zone, the band,',
            '# the side, the nearest paw, the FLANK-near flag and the dwell ring, the P7 exit test, the P3 front cone, anchor8.',
            A.fw('mv/local'),
            'function rlk:mboss/mv/dist',
            'scoreboard players operation #azDist mb = #mbDist mb',
            'scoreboard players operation #azF mb = #mbLf mb', 'scoreboard players operation #azS mb = #mbLs mb',
            'scoreboard players operation #azAs mb = #azS mb',
            'execute if score #azAs mb matches ..-1 run scoreboard players operation #azAs mb *= #cm1 mb',
            sc('#azSide', 1), 'execute if score #azS mb matches ..-1 run scoreboard players set #azSide mb -1',
            '# band by the anchor distance (tenths)',
            sc('#azBand', 2),
            f'execute if score #azDist mb matches ..{int(A.BAND_NEAR * T10)} run scoreboard players set #azBand mb 1',
            f'execute if score #azDist mb matches {int(A.BAND_MID * T10) + 1}.. run scoreboard players set #azBand mb 3',
            '# tenths for the squares (no int overflow)',
            'scoreboard players operation #azFt mb = #azF mb', 'scoreboard players operation #azFt mb /= #c100 mb',
            'scoreboard players operation #azSt mb = #azS mb', 'scoreboard players operation #azSt mb /= #c100 mb',
            sc('#azPawD2', 999999), sc('#azPaw', 1)]
    for k, (x, _, z) in paw.items():
        samp += [f'scoreboard players operation #azX mb = #azSt mb', f'scoreboard players remove #azX mb {int(round(x * T10))}',
                 'scoreboard players operation #azX mb *= #azX mb',
                 f'scoreboard players operation #azY mb = #azFt mb', f'scoreboard players remove #azY mb {int(round(z * T10))}',
                 'scoreboard players operation #azY mb *= #azY mb', 'scoreboard players operation #azX mb += #azY mb',
                 f'execute if score #azX mb < #azPawD2 mb run scoreboard players set #azPaw mb {k}',
                 'execute if score #azX mb < #azPawD2 mb run scoreboard players operation #azPawD2 mb = #azX mb']
    hf, ts, tf = mb(A.HEAD_F), mb(A.TAIL_S), mb(A.TAIL_F)
    s0, s1 = mb(A.FLANK_S0), mb(A.FLANK_S1)
    c0, c1 = A.HEAD_CONE
    samp += [
        '# the head cone: f >= 3.6 and 10|s| <= 10 x 4 + 6 (f - 3.6) (blocks x 1000)',
        sc('#azHd', 0),
        'scoreboard players operation #azX mb = #azF mb', f'scoreboard players remove #azX mb {hf}',
        f'scoreboard players set #azY mb {int(round(c1 * 10))}', 'scoreboard players operation #azX mb *= #azY mb',
        f'scoreboard players add #azX mb {mb(c0) * 10}',
        'scoreboard players operation #azY mb = #azAs mb', 'scoreboard players operation #azY mb *= #c10 mb',
        f'execute if score #azF mb matches {hf}.. if score #azY mb <= #azX mb run scoreboard players set #azHd mb 1',
        '# the zone: PAW first (2.8 b of a paw / foot, or under the body), HEAD, TAIL, FLANK',
        sc('#azZone', 5),
        f'execute if score #azAs mb matches ..{s1} run scoreboard players set #azZone mb 4',
        f'execute if score #azF mb matches ..{tf - 1} if score #azAs mb matches ..{ts} run scoreboard players set #azZone mb 6',
        f'execute if score #azF mb matches ..{tf - 1} if score #azAs mb matches {ts + 1}.. run scoreboard players set #azZone mb 7',
        'execute if score #azHd mb matches 1 run scoreboard players operation #azZone mb = #azBand mb',
        f'execute if score #azPawD2 mb matches ..{int(round((A.PAW_R * T10) ** 2))} run scoreboard players set #azZone mb 8',
        f'execute if score #azAs mb matches ..{s0 - 1} if score #azF mb matches {tf}..{hf - 1} run scoreboard players set #azZone mb 8',
        '# the FLANK-near test of the rule (plan 4.12, independent of the PAW precedence)',
        sc('#azFN', 0),
        f'execute if score #azAs mb matches {s0}..{s1} if score #azF mb matches {tf}..{hf - 1} run scoreboard players set #azFN mb 1',
        '# within +-45 degrees of the front (idle tracking) and the turn step kind',
        sc('#azF45', 0), 'execute if score #azF mb >= #azAs mb run scoreboard players set #azF45 mb 1',
        '# the P3 cone: within +-35 degrees: f > 0 and 10000 |s| <= 7002 f',
        sc('#azF35', 0),
        'scoreboard players operation #azX mb = #azSt mb',
        'execute if score #azX mb matches ..-1 run scoreboard players operation #azX mb *= #cm1 mb',
        'scoreboard players set #azY mb 10000', 'scoreboard players operation #azX mb *= #azY mb',
        'scoreboard players operation #azY mb = #azFt mb', 'scoreboard players set #azZ mb 7002',
        'scoreboard players operation #azY mb *= #azZ mb',
        'execute if score #azFt mb matches 1.. if score #azX mb <= #azY mb run scoreboard players set #azF35 mb 1',
        F('ai/exit'),
        '# anchor8: the anchor within 8 b of the arena centre',
        sc('#azA8', 0),
        f'execute at @s positioned ~ {A.CY} ~ if entity {ARENA_M.replace("limit=1", f"distance=..{A.L.num(A.BODY_R)},limit=1")} '
        'run scoreboard players set #azA8 mb 1',
    ]
    w('ai/sample', samp)
    # the dwell ring and the flank proxy record (every 4 t)
    ring = ['# @s = body, every 4 t: the FLANK-near dwell ring (6 samples = 24 t) and the proxy record (40 t).',
            F('ai/sample'),
            'scoreboard players add #azFsI mb 1', f'execute if score #azFsI mb matches {DWELL_N}.. run scoreboard players set #azFsI mb 0']
    for i in range(DWELL_N):
        ring.append(f'execute if score #azFsI mb matches {i} run scoreboard players operation #azFs{i} mb = #azFN mb')
    ring += [sc('#azDwell', 0)] + [f'scoreboard players operation #azDwell mb += #azFs{i} mb' for i in range(DWELL_N)]
    ring += ['# a flank proxy hit in the last 40 t from |s| >= 3 (#azPxHit = mbPart of the last hit, #azPxGT its gametime)',
             sc('#azPxF', 0),
             'execute store result score #azX mb run time query gametime', 'scoreboard players operation #azX mb -= #azPxGT mb']
    ring += [f'execute if score #azPxHit mb matches {k} if score #azX mb matches ..{PROXY_GT} if score #azAs mb matches {s0}.. '
             'run scoreboard players set #azPxF mb 1' for k in FLANK_PX]
    w('ai/sample4', ring)

    # ------------------------------------------------------------------ the P7 exit test (generated, plan 5 P7 / 8.3-5)
    R = int(round(A.WHIP_EXIT_R * T10))                    # 72 tenths
    tip = A.WHIP_TIP_R + 0.3                               # 17.05 b: beyond the tip
    import math
    c65, s65 = math.cos(math.radians(A.WHIP_HEAD_LANE)), math.sin(math.radians(A.WHIP_HEAD_LANE))
    tf10 = int(round(A.TAIL_F * T10))
    beyond2 = int(round((tip * T10 - R) ** 2))
    w('ai/exit', [
        f'# The P7 exit test (plan 5 P7; generated from api WHIP_*): one of the three exits lies within {A.WHIP_EXIT_R} b of the',
        f'# player: (1) the unswept half behind the rump (f <= {A.TAIL_F}, the other side), (2) the HEAD lane within',
        f'# {A.L.num(A.WHIP_HEAD_LANE)} degrees of the front axis, (3) beyond the tip (> {A.L.num(tip, 2)} b from the anchor). Tenths.',
        sc('#azExit', 0),
        '# (1) |s| when behind the rump, else hypot(|s|, f - tail_f)',
        'scoreboard players operation #azX mb = #azSt mb', 'execute if score #azX mb matches ..-1 run scoreboard players operation #azX mb *= #cm1 mb',
        'scoreboard players operation #azY mb = #azFt mb', f'scoreboard players remove #azY mb {tf10}',
        'execute if score #azY mb matches ..0 run scoreboard players set #azY mb 0',
        'scoreboard players operation #azZ mb = #azX mb', 'scoreboard players operation #azZ mb *= #azX mb',
        'scoreboard players operation #azY mb *= #azY mb', 'scoreboard players operation #azZ mb += #azY mb',
        f'execute if score #azZ mb matches ..{R * R} run scoreboard players set #azExit mb 1',
        '# (2) the head lane: inside the cone, or within R of its boundary ray (|s| cos65 - f sin65 <= R)',
        f'scoreboard players set #azY mb {int(round(c65 * 10000))}', 'scoreboard players operation #azY mb *= #azX mb',
        f'scoreboard players set #azZ mb {int(round(s65 * 10000))}', 'scoreboard players operation #azZ mb *= #azFt mb',
        'scoreboard players operation #azY mb -= #azZ mb',
        f'execute if score #azY mb matches ..{R * 10000} if score #azFt mb matches 0.. run scoreboard players set #azExit mb 1',
        '# (3) beyond the tip: the anchor distance >= tip - R',
        'scoreboard players operation #azZ mb = #azDist mb', 'scoreboard players operation #azZ mb *= #azDist mb',
        f'execute if score #azZ mb matches {beyond2}.. run scoreboard players set #azExit mb 1'])

    # ------------------------------------------------------------------ idle: tracking, leash, turn steps, the walk
    w('ai/state', [
        '# @s = body, idle (no main-slot pattern): cooldown, idle tracking (<= 3 deg/t within +-45 degrees), the module leash',
        '# to the body disc, the next decision.',
        'execute if score #azCool mb matches 1.. run scoreboard players remove #azCool mb 1',
        f'execute if score #azF45 mb matches 1 unless score #azNoTurn mb matches 1 run function rlk:mboss/mv/turn {{max:{TURN_IDLE}}}',
        f'execute positioned ~ {A.CY} ~ unless entity {ARENA_M.replace("limit=1", f"distance=..{A.L.num(A.BODY_R)},limit=1")} run {F("ai/leash")}',
        f'execute if score #azCool mb matches ..0 run {F("ai/next")}'])
    w('ai/leash', [f'# The anchor is beyond the body disc r {A.L.num(A.BODY_R)}: back toward the centre at {WALK_SPD} b/t.',
                   f'execute facing entity {ARENA_M} feet rotated ~ 0 positioned ^ ^ ^{WALK_SPD} run tp @s ~ ~ ~'])

    # ------------------------------------------------------------------ the decision
    nxt = ['# @s = body: the next action at a decision point (plan 4.12 order).',
           'execute if score #azPat mb matches 1.. run return 0',
           'execute if score #mbSt mb matches 2 run return 0',
           f'execute if score #azReq mb matches 1.. run return run {F("ai/req")}',
           f'execute if score #mbLock mb matches 1.. run return run {F("ai/lock")}',
           f'execute if score #azTr mb matches 1 run return run {F("tr/begin")}',
           F('ai/sample'),
           f'execute if score #azTailN mb matches {ANTI_STALL}.. run return run {F("ai/stall")}',
           f'execute if score #azBand mb matches 3 if score #azA8 mb matches 1 run {F("ai/walk_try")}',
           'execute if score #azPat mb matches 1.. run return 0',
           f'execute if score #azSkipF mb matches 1 run return run {F("ai/skipped")}',
           f'execute if function {A.NS}ai/flank run return 0',
           F('ai/pick')]
    w('ai/next', nxt)
    w('ai/skipped', ['# The FLANK rule is skipped once (after P2, P7, P8 + turn180, P9, the surfacing, the transitions).',
                     sc('#azSkipF', 0), F('ai/pick')])
    w('ai/walk_try', [f'# Far band: {WALK_CHANCE} % walk toward the player first (<= {WALK_MAX} t, {WALK_SPD} b/t, inside the body disc).',
                      'execute store result score #azR mb run random value 0..99',
                      f'execute if score #azR mb matches ..{WALK_CHANCE - 1} run {F("ai/walk_go")}'])
    w('ai/walk_go', [sc('#azPick', 28), F('ai/go')])
    w('ai/stall', ['# Anti-stall: the player stayed on the tail lane for 3 decisions without a tail pattern -> turn180, then a',
                   '# front pattern (#azFront 1: the next pick uses the HEAD near column).',
                   sc('#azTailN', 0), sc('#azFront', 1),
                   sc('#azTurnK', 5), 'execute if score #azS mb matches ..-1 run scoreboard players set #azTurnK mb 6',
                   sc('#azPick', 27), F('ai/go')])

    # FLANK rule
    w('ai/flank', [
        '# The FLANK rule (plan 4.12): dwell >= 4 of 6 samples in FLANK-near, or a flank proxy hit in the last 40 t; then',
        f'# {FLANK_CHANCE} %: not after P6 -> P6; after P6 with the player still in FLANK-near or TAIL-off -> P7 (anchor8 + an',
        '# exit), else P8 (TAIL-off, anchor8) or P2. The other 10 % use the FLANK-near column. Returns 1 when it picked.',
        sc('#azX', 0),
        f'execute if score #azDwell mb matches {DWELL_MIN}.. run scoreboard players set #azX mb 1',
        'execute if score #azPxF mb matches 1 run scoreboard players set #azX mb 1',
        'execute if score #azX mb matches 0 run return fail',
        'execute store result score #azR mb run random value 0..99',
        f'execute if score #azR mb matches {FLANK_CHANCE}.. run return run {F("ai/flank_col")}',
        f'execute unless score #azLast mb matches 6 run return run {F("ai/flank_p6")}',
        sc('#azX', 0),
        'execute if score #azFN mb matches 1 run scoreboard players set #azX mb 1',
        'execute if score #azZone mb matches 7 run scoreboard players set #azX mb 1',
        'execute if score #azX mb matches 0 run return fail',
        f'execute if score #azA8 mb matches 1 if score #azExit mb matches 1 run return run {F("ai/flank_p7")}',
        f'execute if score #azA8 mb matches 1 if score #azZone mb matches 7 run return run {F("ai/flank_p8")}',
        f'return run {F("ai/flank_p2")}'])
    for pid, nm in ((6, 'p6'), (7, 'p7'), (8, 'p8'), (2, 'p2')):
        w(f'ai/flank_{nm}', [f'# The FLANK rule picks P{pid}.', sc('#azPick', pid), F('ai/punish'), F('ai/go'), 'return 1'])
    w('ai/flank_col', ['# 10 %: the FLANK-near column.', sc('#azZone', 4), F('ai/pick_z'), 'return 1'])
    w('ai/punish', [
        '# A flank punishment: the first types the hint (the first feint adds "대시로 바깥쪽으로"); the second within 30 s shows',
        '# "옆구리 금지 — 머리 정면 · 꼬리 끝" on the sub-line for 5 s.',
        f'execute unless score #azFlN mb matches 1.. if score #azPick mb matches 6 run {g.line(LINES["flank1f"])}',
        f'execute unless score #azFlN mb matches 1.. unless score #azPick mb matches 6 run {g.line(LINES["flank1"])}',
        'scoreboard players add #azFlN mb 1',
        'scoreboard players operation #azX mb = #azClk mb', 'scoreboard players operation #azX mb -= #azFlC mb',
        f'execute if score #azFlN mb matches 2.. if score #azX mb matches ..600 run {F("ai/punish_hint")}',
        'scoreboard players operation #azFlC mb = #azClk mb'])
    w('ai/punish_hint', [sc('#azHint', 2), 'scoreboard players operation #azHintT mb = #azClk mb',
                         'scoreboard players add #azHintT mb 100', sc('#azHudQ', 1)])

    # weighted pick
    def wt(p, ph, z):
        o = WEIGHT_OVERRIDE.get(p.id, {}).get(ph, {})
        return int(o.get(z, p.w_in(ph, z)))
    cand = ['# @s = body: candidate weights #azC<id> (x2, so a repeat of P2 counts half) in the current phase and zone, the',
            '# gates, the cooldowns, the element pair, no immediate repeat.']
    for p in picks:
        cand.append(sc(f'#azC{p.id}', 0))
        for ph in (1, 2, 3):
            for z in A.ZONES:
                v = wt(p, ph, z)
                if v:
                    cand.append(f'execute if score #azPh mb matches {ph} if score #azZone mb matches {A.ZONE_ID[z]} run '
                                f'scoreboard players set #azC{p.id} mb {2 * v}')
        if p.id == 1:
            cand.append('# P1 PAW: the fore paws only')
            cand.append('execute if score #azZone mb matches 8 if score #azPaw mb matches 3..4 run scoreboard players set #azC1 mb 0')
        if p.elem:
            side, el = p.elem
            cand.append(f'execute unless score #az{"Leg" if side == "leg" else "Tail"} mb matches {el} run scoreboard players set #azC{p.id} mb 0')
        eff = [p] + [q for q in pats if q.replaces == p.id]
        for q in eff:
            gate_pre = ''
            if q is not p:
                cond = []
                if q.phases != p.phases:
                    cond.append(f'if score #azPh mb matches {min(q.phases)}..{max(q.phases)}')
                if q.elem:
                    cond.append(f'if score #az{"Leg" if q.elem[0] == "leg" else "Tail"} mb matches {q.elem[1]}')
                if q.id == 10:
                    cond.append('if score #azPaw mb matches 1..2')
                gate_pre = ' '.join(cond) + ' '
            for gt in q.gates:
                cond = {'anchor8': 'unless score #azA8 mb matches 1', 'front35': 'unless score #azF35 mb matches 1',
                        'exit': 'unless score #azExit mb matches 1',
                        'field_area': f'if score #azFldA mb matches {A.FIELD_GATE}..',
                        'no_bg': 'if score #azPh mb matches 3 if score #azBgAny mb matches 1'}.get(gt)
                if gt == 'no_live':
                    cand.append(f'execute {gate_pre}if score #azCast mb matches {q.id} run scoreboard players set #azC{p.id} mb 0')
                    cand.append(f'execute {gate_pre}if score #azBgL mb matches {q.id} run scoreboard players set #azC{p.id} mb 0')
                    cand.append(f'execute {gate_pre}if score #azBgT mb matches {q.id} run scoreboard players set #azC{p.id} mb 0')
                elif cond:
                    when = FIELD_AREA_WHEN.get(q.id, '') if gt == 'field_area' else ''
                    cand.append(f'execute {gate_pre}{when}{cond} run scoreboard players set #azC{p.id} mb 0')
            if q.cooldown:
                cand.append(f'execute {gate_pre}if score #azClk mb < #azCdE{q.id} mb run scoreboard players set #azC{p.id} mb 0')
        if p.id in REPEAT_HALF:
            cand.append(f'execute if score #azLast mb matches {p.id} run scoreboard players operation #azC{p.id} mb /= #c2 mb')
        elif p.id in REPEAT_MAX:
            cand.append(f'execute if score #azLast mb matches {p.id} if score #azRepN mb matches {REPEAT_MAX[p.id]}.. run '
                        f'scoreboard players set #azC{p.id} mb 0')
        else:
            cand.append(f'execute if score #azLast mb matches {p.id} run scoreboard players set #azC{p.id} mb 0')
        if p.id == 6:
            cand.append('scoreboard players set #azC6 mb 0')
        if p.id == 5:
            # REQ pa-3: in phase 3 a fore-paw P5 becomes P5b (10) in ai/go, so right after a 10 it would repeat 10
            cand.append('execute if score #azLast mb matches 10 if score #azPh mb matches 3 if score #azPaw mb matches 1..2 run '
                        'scoreboard players set #azC5 mb 0')
    cand += [sc('#azCn', 0)] + [f'scoreboard players operation #azCn mb += #azC{p.id} mb' for p in picks]
    w('ai/cand', cand)
    draw = ['# #azR = 0..#azCn-1 -> the candidate whose weight range holds it.', sc('#azPick', 0)]
    for p in picks:
        draw.append(f'execute if score #azPick mb matches 0 if score #azC{p.id} mb matches 1.. if score #azR mb < #azC{p.id} mb '
                    f'run scoreboard players set #azPick mb {p.id}')
        draw.append(f'scoreboard players operation #azR mb -= #azC{p.id} mb')
    w('ai/draw', draw)
    w('ai/pick', ['# @s = body: the weighted pick in the sampled zone (#azFront 1: the HEAD near column once, after the anti-stall).',
                  'execute if score #azFront mb matches 1 run scoreboard players set #azZone mb 1', sc('#azFront', 0),
                  F('ai/pick_z')])
    w('ai/pick_z', [F('ai/cand'),
                    f'execute if score #azCn mb matches 0 run return run {F("ai/fallback")}',
                    'execute store result score #azR mb run random value 0..9999',
                    'scoreboard players operation #azR mb %= #azCn mb',
                    F('ai/draw'),
                    f'execute if score #azPick mb matches 0 run return run {F("ai/fallback")}',
                    F('ai/go')])
    w('ai/fallback', ['# Nothing allowed here: P2 when it may run (not the last), else idle 10 t.',
                      f'execute unless score #azLast mb matches 2 run return run {F("ai/flank_p2_q")}',
                      sc('#azCool', 10)])
    w('ai/flank_p2_q', [sc('#azPick', 2), F('ai/go')])

    # go: replacements, the slot, the bookkeeping, the "first" lines
    go = ['# Into the main slot (#azPick): the phase-3 replacements, repeat count, anti-stall count, the cast host for a leg',
          '# special, the "first" lines; p/run starts it this tick (pattern clock 0 = clip tick 0 after any lead).']
    for q in pats:
        if q.replaces is not None:
            cond = [f'if score #azPick mb matches {q.replaces}', f'if score #azPh mb matches {min(q.phases)}..{max(q.phases)}']
            if q.elem:
                cond.append(f'if score #az{"Leg" if q.elem[0] == "leg" else "Tail"} mb matches {q.elem[1]}')
            if q.id == 10:
                cond.append('if score #azPaw mb matches 1..2')
            go.append(f'execute {" ".join(cond)} run scoreboard players set #azPick mb {q.id}')
    go += ['# the repeat count (P5 at most 2 in a row) and the anti-stall count (TAIL-lane decisions without a tail pattern)',
           'execute if score #azPick mb = #azLast mb run scoreboard players add #azRepN mb 1',
           'execute unless score #azPick mb = #azLast mb run scoreboard players set #azRepN mb 1',
           'execute if score #azPick mb matches 1..26 run scoreboard players operation #azLast mb = #azPick mb',
           'execute if score #azPick mb matches 31..49 run scoreboard players operation #azLast mb = #azPick mb',
           'execute unless score #azZone mb matches 6 run scoreboard players set #azTailN mb 0',
           f'execute if score #azZone mb matches 6 if score #azPick mb matches 1..26 unless score #azPick mb matches {TAIL_PATS[0]} '
           f'unless score #azPick mb matches {TAIL_PATS[1]} run scoreboard players add #azTailN mb 1',
           f'execute if score #azPick mb matches {TAIL_PATS[0]} run scoreboard players set #azTailN mb 0',
           f'execute if score #azPick mb matches {TAIL_PATS[1]} run scoreboard players set #azTailN mb 0',
           '# a leg special runs in the cast slot behind the core\'s cast host (service 30)',
           'execute if score #azPick mb matches 31..32 run scoreboard players operation #azCastReq mb = #azPick mb',
           'execute if score #azPick mb matches 31..32 run scoreboard players set #azPick mb 30',
           F('ai/lines'),
           'scoreboard players operation #azPat mb = #azPick mb', sc('#azPNew', 1), sc('#azReqT', 0)]
    w('ai/go', go)
    w('ai/lines', ['# The "first" lines of plan 4.13 typed at the pick (the patterns type none of these).',
                   f'execute if score #azPick mb matches 2 unless score #azL2 mb = #azPh mb run {g.line(LINES["p2"])}',
                   'execute if score #azPick mb matches 2 run scoreboard players operation #azL2 mb = #azPh mb',
                   f'execute if score #azPick mb matches 3 unless score #azL39 mb matches 1 run {g.line(LINES["p39"])}',
                   f'execute if score #azPick mb matches 9 unless score #azL39 mb matches 1 run {g.line(LINES["p39"])}',
                   'execute if score #azPick mb matches 3 run scoreboard players set #azL39 mb 1',
                   'execute if score #azPick mb matches 9 run scoreboard players set #azL39 mb 1',
                   f'execute if score #azPick mb matches 7 unless score #azL7 mb = #azPh mb run {g.line(LINES["p7"])}',
                   f'execute if score #azPick mb matches 7 unless score #azL7h mb matches 1 run {F("ai/hint_whip")}',
                   'execute if score #azPick mb matches 7 run scoreboard players operation #azL7 mb = #azPh mb',
                   f'execute if score #azPick mb matches 43..44 unless score #azLT mb matches 1 run {g.line(LINES["tail"])}',
                   'execute if score #azPick mb matches 43..44 run scoreboard players set #azLT mb 1'])
    w('ai/hint_whip', [sc('#azL7h', 1), sc('#azHint', 1), 'scoreboard players operation #azHintT mb = #azClk mb',
                       'scoreboard players add #azHintT mb 100', sc('#azHudQ', 1)])

    # requests and locks
    w('ai/req', ['# A test request (#azReq = pattern / service id; #azReqT = a start clock for services that support it).',
                 'scoreboard players operation #azPick mb = #azReq mb', sc('#azReq', 0),
                 'execute if score #azPick mb matches 31..32 run scoreboard players operation #azCastReq mb = #azPick mb',
                 'execute if score #azPick mb matches 31..32 run scoreboard players set #azPick mb 30',
                 F('ai/lines'),
                 'scoreboard players operation #azPat mb = #azPick mb', sc('#azPNew', 1)])
    lock = ['# #mbLock = N (test/lock): that pattern only (its phase rules ignored; 0 unlocks). Unknown ids idle.']
    known = sorted({p.id for p in pats if p.kind in ('normal', 'cast', 'bg')})
    for pid in known:
        lock.append(f'execute if score #mbLock mb matches {pid} run return run {F("ai/lock_go")}')
    lock.append(sc('#azCool', 20))
    w('ai/lock', lock)
    w('ai/lock_go', [F('ai/sample'), 'scoreboard players operation #azPick mb = #mbLock mb', F('ai/go')])
