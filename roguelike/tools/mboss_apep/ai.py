"""The Apep AI (plan 7.3 / 7.4; ap_contract 1.7): zones in the anchor frame (mv/local, cm.md 13.2), bands, idle facing
(tracking, the crab-turn step), the module leash to the idle disc, crawl / walk decisions, the BACK dwell rule with the
rim rule and the first-time hint, the weighted tables built from the PATTERNS of the pattern modules, cooldowns,
first_after, no immediate repeat, the gates, the R opener of P4, chains, the Q2 schedule, the anti-stall 180-degree
crab-turn, test requests and test/lock. Called by core.emit (AP:ai/**).

Decision order (plan 7.4): test request > lock > queued transition (#apTr 1, phase 1) > chain pending (phase 3) >
Q2 due (phase 3) > anti-stall / rim / BACK rule (phase 1) > a move (phase 1: crawl when far, side walk when mid) >
weighted pick by zone and band > fallback.

Zones (#apZone 1 FRONT 2 SIDE 3 UNDER 4 BACK; milliblocks, f forward / s left of the anchor): FRONT f >= 3 and
|s| <= 4 + 0.6 (f - 3); BACK f < -3; UNDER |s| <= 3 and -3 <= f < 3; SIDE otherwise (incl. the forward diagonals outside
the cone). Bands by the anchor distance (#apBand 1 near 2 mid 3 far; P1 7.5 / 14, P3 6 / 14). The weight column #apCol:
phase 1 1 front_near 2 front_mid 3 front_far 4 side_under 5 back; phase 3 1 near 2 mid 3 far.

Deviations kept for the balance fixer (documented in ap_contract 1.7): the crab-turn step only for players outside BACK
(the BACK zone is the BACK rule's / anti-stall's business; idle tracking stops beyond 60 degrees so a BACK player stays
BACK); a move decision is never followed by another move; the rim rule picks P1 when it is off cooldown, else the turn.
"""
from . import api as A

WEIGHT_OVERRIDE = {}           # the balance fixer: {pattern id: {column: w}}
CRAWL_PCT = 40                 # phase 1, far band: % of the decisions that crawl first (plan 7.3 locomotion)
WALK_PCT = 15                  # phase 1, mid band: % that side-walk first
RIM_P1_PCT = 50                # the rim rule: % P1 (when off cooldown), else the 180-degree crab-turn
STEP_COOL = 5                  # a crab-turn step at idle only while the cooldown has >= this many ticks left
MB = 1000


def mb(v):
    return int(round(v * MB))


def local_line():
    """The anchor-frame sample of the framework (#mbLf / #mbLs, milliblocks)."""
    return A.L.local()


def emit(core):
    g, F = core.g, core.F
    w = core.w
    sc = lambda n, v: f'scoreboard players set {n} mb {int(v)}'   # noqa: E731
    BODY, ARENA_M, PLAYER = A.BODY, A.ARENA_M, A.PLAYER
    pats = core.pats
    picks = [p for p in pats if p.kind == 'normal']
    by_id = {p.id: p for p in pats}
    num = A.L.num

    # ------------------------------------------------------------------ the sampler
    f3, s3 = mb(A.FRONT_F), mb(A.SIDE_S)
    c0, c1 = A.FRONT_CONE
    tan60 = 577                   # |dyaw| > 60 deg  <=>  1000 f < 577 |s|
    samp = ['# @s = body: the player in the anchor frame (#apF / #apS mb, #apAs = |s|), the distance (#apDist tenths), the',
            '# zone, the band, the weight column, the side, the wide flag (|dyaw| > 60), the rim and centre flags.',
            local_line(), 'function rlk:mboss/mv/dist',
            'scoreboard players operation #apDist mb = #mbDist mb',
            'scoreboard players operation #apF mb = #mbLf mb', 'scoreboard players operation #apS mb = #mbLs mb',
            'scoreboard players operation #apAs mb = #apS mb',
            'execute if score #apAs mb matches ..-1 run scoreboard players operation #apAs mb *= #cm1 mb',
            sc('#apSide', 1), 'execute if score #apS mb matches ..-1 run scoreboard players set #apSide mb -1',
            f'# FRONT cone: f >= {A.FRONT_F} and 10 |s| <= 10 x {c0} + {int(c1 * 10)} (f - {A.FRONT_F}) (mb)',
            sc('#apZone', 2),
            'scoreboard players operation #apX mb = #apF mb', f'scoreboard players remove #apX mb {f3}',
            f'scoreboard players set #apY mb {int(round(c1 * 10))}', 'scoreboard players operation #apX mb *= #apY mb',
            f'scoreboard players add #apX mb {mb(c0) * 10}',
            'scoreboard players operation #apY mb = #apAs mb', 'scoreboard players operation #apY mb *= #c10 mb',
            f'execute if score #apF mb matches {f3}.. if score #apY mb <= #apX mb run scoreboard players set #apZone mb 1',
            f'execute if score #apF mb matches {-f3}..{f3 - 1} if score #apAs mb matches ..{s3} run scoreboard players set #apZone mb 3',
            f'execute if score #apF mb matches ..{-f3 - 1} run scoreboard players set #apZone mb 4',
            '# the band (tenths of the anchor distance; P1 / P3 bounds)',
            sc('#apBand', 2)]
    for ph, (near, mid) in ((1, A.BAND_P1), (3, A.BAND_P3)):
        samp += [f'execute if score #apPh mb matches {ph} if score #apDist mb matches ..{int(round(near * 10))} run scoreboard players set #apBand mb 1',
                 f'execute if score #apPh mb matches {ph} if score #apDist mb matches {int(round(mid * 10)) + 1}.. run scoreboard players set #apBand mb 3']
    samp += ['# the weight column (phase 1: FRONT x band, SIDE / UNDER, BACK; phase 3: the band)',
             'scoreboard players operation #apCol mb = #apBand mb',
             'execute if score #apPh mb matches 1 if score #apZone mb matches 2..3 run scoreboard players set #apCol mb 4',
             'execute if score #apPh mb matches 1 if score #apZone mb matches 4 run scoreboard players set #apCol mb 5',
             '# wide: |dyaw| > 60 degrees (1000 f < 577 |s|)',
             sc('#apWide', 0),
             'scoreboard players operation #apX mb = #apF mb', 'scoreboard players operation #apX mb *= #c1000 mb',
             f'scoreboard players set #apY mb {tan60}', 'scoreboard players operation #apY mb *= #apAs mb',
             'execute if score #apX mb < #apY mb run scoreboard players set #apWide mb 1',
             f'# rim: the anchor beyond r {num(A.RIM_R)} of the centre; cfree: the player beyond 5 b of the centre',
             sc('#apRim', 0),
             f'execute positioned ~ {A.CY} ~ unless entity {ARENA_M.replace("limit=1", f"distance=..{num(A.RIM_R)},limit=1")} '
             'run scoreboard players set #apRim mb 1',
             sc('#apCFree', 1),
             f'execute at {PLAYER} positioned ~ {A.CY} ~ if entity {ARENA_M.replace("limit=1", "distance=..5,limit=1")} '
             'run scoreboard players set #apCFree mb 0']
    w('ai/sample', samp)
    n, k, need = A.BACK_DWELL
    ring = [f'# @s = body (module tick, phase 1): every {n} t a sample and the BACK dwell ring ({k} samples; the rule needs >= {need}).',
            'scoreboard players operation #apM mb = #apFc mb', f'scoreboard players operation #apM mb %= #apK{n} mb',
            'execute unless score #apM mb matches 0 run return 0',
            F('ai/sample'),
            'scoreboard players add #apBkI mb 1', f'execute if score #apBkI mb matches {k}.. run scoreboard players set #apBkI mb 0']
    for i in range(k):
        ring += [f'execute if score #apBkI mb matches {i} run scoreboard players set #apBk{i} mb 0',
                 f'execute if score #apBkI mb matches {i} if score #apZone mb matches 4 run scoreboard players set #apBk{i} mb 1']
    ring += [sc('#apBackT', 0)] + [f'scoreboard players operation #apBackT mb += #apBk{i} mb' for i in range(k)]
    w('ai/ring', ring)

    # ------------------------------------------------------------------ idle: tracking, the step, the leash
    w('ai/state', [
        '# @s = body, idle (no main-slot pattern, not in a cine; phases 1 and 3): cooldown, idle tracking (phase 1 <= 3 deg/t',
        '# within 60 degrees, else a crab-turn step for a player outside BACK; phase 3 <= 3 deg/t always), the module leash',
        f'# to the idle disc r {num(A.IDLE_R)} at {A.LEASH_SPD} b/t, the next decision.',
        'execute if score #apCool mb matches 1.. run scoreboard players remove #apCool mb 1',
        f'execute if score #apPh mb matches 3 run function rlk:mboss/mv/turn {{max:{A.TURN_IDLE[3]}}}',
        f'execute if score #apPh mb matches 1 unless score #apWide mb matches 1 run function rlk:mboss/mv/turn {{max:{A.TURN_IDLE[1]}}}',
        f'execute if score #apPh mb matches 1 if score #apWide mb matches 1 unless score #apZone mb matches 4 if score #apCool mb matches '
        f'{STEP_COOL}.. unless score #apLastMv mb matches 1 run return run {F("ai/step_go")}',
        f'execute positioned ~ {A.CY} ~ unless entity {ARENA_M.replace("limit=1", f"distance=..{num(A.IDLE_R)},limit=1")} run {F("ai/leash")}',
        f'execute if score #apCool mb matches ..0 run {F("ai/next")}'])
    w('ai/leash', [f'# The anchor is beyond the idle disc: back toward the centre at {A.LEASH_SPD} b/t (yaw kept).',
                   f'execute facing entity {ARENA_M} feet rotated ~ 0 positioned ^ ^ ^{num(A.LEASH_SPD)} run tp @s ~ {A.CY} ~'])

    # ------------------------------------------------------------------ the decision
    nxt = ['# @s = body: the next action at a decision point (plan 7.4 order).',
           'execute if score #apPid mb matches 1.. run return 0',
           f'execute if score #apReq mb matches 1.. run return run {F("ai/req")}',
           f'execute if score #mbLock mb matches 1.. run return run {F("ai/lock")}',
           f'execute if score #apPh mb matches 1 if score #apTr mb matches 1 run return run {F("tr/begin")}',
           F('ai/sample'),
           f'execute if score #apPh mb matches 3 if score #apChP mb matches 1.. run return run {F("ai/chain_go")}',
           f'execute if score #apPh mb matches 3 if function {A.NS}ai/q2_due run return run {F("ai/q2_go")}',
           f'execute if score #apPh mb matches 1 if function {A.NS}ai/back run return 0',
           f'execute if score #apPh mb matches 1 unless score #apLastMv mb matches 1 if function {A.NS}ai/move run return 0',
           F('ai/pick')]
    w('ai/next', nxt)
    w('ai/chain_go', ['# A chain is pending (plan 7.4: Q5 -> Q1 40 %, Q3 -> Q3s 30 %): it runs now (#apChainRun 1: no chain after it).',
                      'scoreboard players operation #apPick mb = #apChP mb', sc('#apChP', 0), sc('#apChainRun', 1),
                      sc('#apArg', 0), F('ai/go_raw')])
    q2 = by_id.get(32)
    w('ai/q2_due', [
        f'# Q2 (plan 7.4): first after {A.Q2_FIRST_AFTER} phase-3 pattern(s); then >= {A.Q2_EVERY} t after the last and >= {A.Q2_OTHERS}',
        f'# other patterns; never before #apAftCd (a cancel: +{A.Q2_CANCEL_CD} t). Returns 1 when due.',
        'execute if score #apFc mb < #apAftCd mb run return fail',
        f'execute if score #apAft1 mb matches 0 if score #apP3N mb matches {A.Q2_FIRST_AFTER}.. run return 1',
        f'execute if score #apAft1 mb matches 1 if score #apAftN mb matches {A.Q2_OTHERS}.. run return 1',
        'return fail'])
    w('ai/q2_go', [sc('#apPick', 32 if q2 else 0), sc('#apArg', 0), F('ai/go_raw')])

    # BACK rule, rim rule, anti-stall (phase 1)
    assert by_id[5].cooldown and by_id[1].cooldown, 'P1 / P5 cooldowns (plan 7.4) drive the BACK and rim rules'
    w('ai/back', [
        '# Phase 1 (plan 7.3 / 7.4). Returns 1 when it picked. Anti-stall: BACK for >= 3 decisions while P5 cools down -> a',
        f'# 180-degree crab-turn. Rim: the anchor beyond r {num(A.RIM_R)} with the player BACK -> P1 ({RIM_P1_PCT} %, off cooldown) or',
        f'# the turn. BACK rule: BACK for >= {need} of the last {k} samples -> {A.BACK_RULE_PCT} % P5 (off its cooldown).',
        'execute unless score #apZone mb matches 4 run scoreboard players set #apBackN mb 0',
        'execute unless score #apZone mb matches 4 run return fail',
        'execute if score #apFc mb < #apCdE5 mb run scoreboard players add #apBackN mb 1',
        f'execute if score #apBackN mb matches {A.ANTI_STALL}.. run return run {F("ai/turn180")}',
        f'execute if score #apRim mb matches 1 run return run {F("ai/rim")}',
        f'execute if score #apBackT mb matches ..{need - 1} run return fail',
        'execute store result score #apR mb run random value 0..99',
        f'execute if score #apR mb matches {A.BACK_RULE_PCT}.. run return fail',
        'execute if score #apFc mb < #apCdE5 mb run return fail',
        f'return run {F("ai/back_p5")}'])
    w('ai/back_p5', ['# The BACK rule picks P5 (the first time of the fight: the hint line).',
                     f'execute unless score #apBackH mb matches 1 run {g.line(A.TXT["back_hint"], A.WARN_HEX, 70)}',
                     sc('#apBackH', 1), sc('#apBackN', 0), sc('#apPick', 5), sc('#apArg', 0), F('ai/go'), 'return 1'])
    w('ai/rim', ['# The rim rule: P1 (off cooldown, not the last) or the 180-degree crab-turn.',
                 'execute store result score #apR mb run random value 0..99',
                 f'execute if score #apR mb matches ..{RIM_P1_PCT - 1} if score #apFc mb >= #apCdE1 mb unless score #apLast mb matches 1 run return run {F("ai/rim_p1")}',
                 f'return run {F("ai/turn180")}'])
    w('ai/rim_p1', [sc('#apBackN', 0), sc('#apPick', 1), sc('#apArg', 0), F('ai/go'), 'return 1'])
    w('ai/turn180', ['# A 180-degree crab-turn (service 10, kind 4: two steps toward the player\'s side).',
                     sc('#apBackN', 0), sc('#apMvK', 4), sc('#apPick', 10), F('ai/go_raw'), 'return 1'])
    w('ai/step_go', ['# A crab-turn step toward the player (service 10, kind 3).', sc('#apMvK', 3), sc('#apPick', 10), F('ai/go_raw')])
    w('ai/move', [
        f'# Phase 1 locomotion (plan 7.3): far band {CRAWL_PCT} % a crab crawl toward the player; mid band {WALK_PCT} % a side walk.',
        '# Returns 1 when it moved.',
        'execute store result score #apR mb run random value 0..99',
        f'execute if score #apBand mb matches 3 if score #apR mb matches ..{CRAWL_PCT - 1} run return run {F("ai/move_crawl")}',
        f'execute if score #apBand mb matches 2 if score #apR mb matches ..{WALK_PCT - 1} run return run {F("ai/move_walk")}',
        'return fail'])
    w('ai/move_crawl', [sc('#apMvK', 1), sc('#apPick', 10), F('ai/go_raw'), 'return 1'])
    w('ai/move_walk', [sc('#apMvK', 2), sc('#apMvD', 1),
                       'execute store result score #apR mb run random value 0..1',
                       'execute if score #apR mb matches 0 run scoreboard players set #apMvD mb -1',
                       sc('#apPick', 10), F('ai/go_raw'), 'return 1'])

    # ------------------------------------------------------------------ weighted pick
    def wt(p, col):
        return int(WEIGHT_OVERRIDE.get(p.id, {}).get(col, p.w(col)))
    gate_cond = {'side_rear': 'unless score #apZone mb matches 2 run scoreboard players set #apC{id} mb 0',
                 'centre_free': 'unless score #apCFree mb matches 1 run scoreboard players set #apC{id} mb 0'}
    cand = ['# @s = body: candidate weights #apC<id> in the current phase and column; gates, cooldowns, first_after, no',
            '# immediate repeat.']
    for p in picks:
        cols = A.COLS_P1 if p.phase == 1 else A.COLS_P3
        cand.append(sc(f'#apC{p.id}', 0))
        for i, col in enumerate(cols):
            v = wt(p, col)
            if v:
                cand.append(f'execute if score #apPh mb matches {p.phase} if score #apCol mb matches {i + 1} run '
                            f'scoreboard players set #apC{p.id} mb {v}')
        for gt in p.gates:
            cand.append('execute ' + gate_cond[gt].format(id=p.id))
            if gt == 'side_rear':
                cand.append(f'execute if score #apF mb matches 0.. run scoreboard players set #apC{p.id} mb 0')
        if p.cooldown:
            cand.append(f'execute if score #apFc mb < #apCdE{p.id} mb run scoreboard players set #apC{p.id} mb 0')
        if p.first_after:
            cand.append(f'execute if score #apPatN mb matches ..{p.first_after - 1} run scoreboard players set #apC{p.id} mb 0')
        cand.append(f'execute if score #apLast mb matches {p.id} run scoreboard players set #apC{p.id} mb 0')
    cand += [sc('#apCn', 0)] + [f'scoreboard players operation #apCn mb += #apC{p.id} mb' for p in picks]
    w('ai/cand', cand)
    draw = ['# #apR = 0..#apCn-1 -> the candidate whose weight range holds it.', sc('#apPick', 0)]
    for p in picks:
        draw.append(f'execute if score #apPick mb matches 0 if score #apC{p.id} mb matches 1.. if score #apR mb < #apC{p.id} mb '
                    f'run scoreboard players set #apPick mb {p.id}')
        draw.append(f'scoreboard players operation #apR mb -= #apC{p.id} mb')
    w('ai/draw', draw)
    w('ai/pick', ['# @s = body: the weighted pick in the sampled column.',
                  F('ai/cand'),
                  f'execute if score #apCn mb matches 0 run return run {F("ai/fallback")}',
                  'execute store result score #apR mb run random value 0..9999',
                  'scoreboard players operation #apR mb %= #apCn mb',
                  F('ai/draw'),
                  f'execute if score #apPick mb matches 0 run return run {F("ai/fallback")}',
                  sc('#apArg', 0), F('ai/go')])
    w('ai/fallback', ['# Nothing allowed here: phase 1 a crab-turn step (not after a move), else idle 10 t.',
                      f'execute if score #apPh mb matches 1 unless score #apLastMv mb matches 1 run return run {F("ai/step_go")}',
                      sc('#apCool', 10)])

    # ------------------------------------------------------------------ go
    go = ['# Into the main slot (#apPick): the opener of a pattern that names one (R before P4 when the player is far: #apNext',
          '# hands P4 over at the opener\'s end), then go_raw.']
    for p in pats:
        if p.opener:
            oid, dist = p.opener
            go.append(f'execute if score #apPick mb matches {p.id} if score #apDist mb matches {int(round(dist * 10)) + 1}.. run '
                      f'scoreboard players set #apNext mb {p.id}')
            go.append(f'execute if score #apPick mb matches {p.id} if score #apNext mb matches {p.id} run scoreboard players set #apPick mb {oid}')
    go.append(F('ai/go_raw'))
    w('ai/go', go)
    last = [p.id for p in pats if p.kind in ('normal', 'scheduled', 'chain')]
    raw = ['# #apPick -> the main slot (p/run starts it this tick); #apLast for the attack patterns; #apLastMv for moves.']
    raw += [f'execute if score #apPick mb matches {i} run scoreboard players operation #apLast mb = #apPick mb' for i in last]
    raw += [sc('#apLastMv', 0), 'execute if score #apPick mb matches 10 run scoreboard players set #apLastMv mb 1',
            'scoreboard players operation #apPid mb = #apPick mb', sc('#apPNew', 1), sc('#apReqT', 0)]
    w('ai/go_raw', raw)
    w('ai/next_go', ['# The opener ended: its host (#apNext) starts now (no opener check, no recover).',
                     'scoreboard players operation #apPick mb = #apNext mb', sc('#apNext', 0), F('ai/go_raw')])

    # ------------------------------------------------------------------ requests and locks
    w('ai/req', ['# A test request (#apReq = a pattern / service id; #apArg / #apNext kept as the test set them).',
                 'scoreboard players operation #apPick mb = #apReq mb', sc('#apReq', 0),
                 f'execute if score #apPick mb matches 20 run return run {F("tr/begin")}',
                 F('ai/sample'), F('ai/go_raw')])
    lock = ['# #mbLock = N (test/lock): that pattern only, in its own phase (another phase\'s id idles); 0 unlocks.']
    for p in pats:
        if p.kind in ('normal', 'scheduled', 'chain'):
            lock.append(f'execute if score #mbLock mb matches {p.id} if score #apPh mb matches {p.phase} run return run {F("ai/lock_go")}')
    lock.append(sc('#apCool', 20))
    w('ai/lock', lock)
    w('ai/lock_go', [F('ai/sample'), 'scoreboard players operation #apPick mb = #mbLock mb', sc('#apArg', 0), F('ai/go')])
    assert BODY
