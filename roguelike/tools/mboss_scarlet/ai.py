"""AI of 홍련 (PLAN §4.7; OWNER: S3): the distance bands, api.WEIGHTS / COOLDOWN / MID_MAX per fight phase (P1 / P2), no
immediate repeat, the counter trigger (A1 / A2 + the flinch), the skill trigger (A6), the far rule (after A6 too) and the
rear rule, the recovery walk / strafe / P2 glide facing the player; every random draw is `random value` (the seeded
stream of the sims).

Runtime (@s = the body): ai/sample every SAMPLE_EVERY fight ticks and at each decision (mv/local: the player in her
frame, #ai_lf / #ai_ls cm, #ai_d2 cm^2; a 6-bit rear history #rear = the last 30 t; the far dwell #far = ticks farther
than FAR_RULE dist); ai/recover each idle tick; ai/decide when the recovery ran out. Cooldowns are ready times on the
module clock #clk (#cd_<key> = #clk + cooldown at the start; A6 #a6cd); the clock stops while the fight is paused and a
reload keeps the scores. Only patterns present in p1.PATTERNS + p_ghost.PATTERNS are ever picked (S4's may be missing).
The decision order: the test hold (99), the reserved phase step (#fl: CS1 in P1, the A13 lead-in in P2), the test lock
(#mbLock mb), a forced next entry (#ai_nx: A3 after the far fallback's approach), the rear rule, the far rule (also right
after A6), the weighted pick of the band.
"""
from . import api
from . import s3lib as S
from .s3lib import sset, fn

OBJ = api.OBJ
PH = api.PH
SAMPLE_EVERY = 5
FPS = {1: PH['p1'], 2: PH['p2']}                         # fight phase -> #ph
BANDS = ('near', 'mid', 'far')
CM2 = lambda b: int((b * 100) ** 2)                      # noqa: E731  blocks -> cm^2
NEAR2, MID2 = CM2(api.BANDS[0]), CM2(api.BANDS[1])
FAR2 = CM2(api.FAR_RULE['dist'])
WALK2 = CM2(6.0)                                          # recovery: walk / glide in beyond 6 b, else strafe
REAR_N = api.REAR_RULE['dwell'][0] // SAMPLE_EVERY        # 20 of 30 t = 4 of the last 6 samples
CT = api.COUNTER_TRIGGER
A6 = A = api.A6_TRIGGER


def cooldown(key, fp):
    return api.COOLDOWN.get(key, {}).get(fp)


def allowed(key, var, fp, check_cd=True, mid_max=False):
    """Lines zeroing var when entry `key` may not start now: cooldown, no immediate repeat, MID_MAX (mid band)."""
    out = []
    if check_cd and cooldown(key, fp) is not None:
        out.append(f'execute if score #cd_{key} {OBJ} > #clk {OBJ} run {sset(var, 0)}')
    if api.NO_REPEAT:
        out.append(f'execute if score #last {OBJ} matches {S.TID[key]} run {sset(var, 0)}')
    if mid_max and key in api.MID_MAX:
        out.append(f'execute if score #ai_d2 {OBJ} matches {CM2(api.MID_MAX[key]) + 1}.. run {sset(var, 0)}')
    return out


def weighted(cands, var_of, fp, mid_band=False, none_fn='ai/none'):
    """A weighted pick among (key, weight) (zeroed by allowed()), renormalised over what is left; none -> none_fn."""
    lines = [sset('#ai_sum', 0)]
    for k, wt in cands:
        v = var_of(k)
        lines.append(sset(v, wt))
        lines += allowed(k, v, fp, mid_max=mid_band)
        lines.append(f'scoreboard players operation #ai_sum {OBJ} += {v} {OBJ}')
    lines += [f'execute if score #ai_sum {OBJ} matches ..0 run return run {fn(none_fn)}',
              f'execute store result score #ai_r {OBJ} run random value 0..999',
              f'scoreboard players operation #ai_r {OBJ} *= #ai_sum {OBJ}',
              f'scoreboard players operation #ai_r {OBJ} /= #c1000 {OBJ}']
    for k, _wt in cands:
        v = var_of(k)
        lines.append(f'execute if score #ai_r {OBJ} < {v} {OBJ} run return run {fn(f"core/start/{k}")}')
        lines.append(f'scoreboard players operation #ai_r {OBJ} -= {v} {OBJ}')
    lines.append(fn(none_fn))
    return lines


def build(W, ctx):
    w = W.w
    present = set(ctx.present)
    var = lambda k: f'#ai_w{k}'  # noqa: E731
    # ------------------------------------------------------------------------------------------- samples
    w('ai/sample', [
        f'# AI sample (@s = body, every {SAMPLE_EVERY} fight ticks and at each decision): the player in her frame (mv/local, mm ->',
        f'# cm): #ai_lf forward, #ai_ls left, #ai_d2 = squared distance (cm^2); #rear = 6-bit history of "behind her" (+-',
        f'# {api.REAR_RULE["deg"]} deg of her back); #far = ticks farther than {api.L.num(api.FAR_RULE["dist"])} b (0 when nearer).',
        'execute unless function rlk:mboss/mv/local run return 0',
        f'scoreboard players operation #ai_lf {OBJ} = #mbLf mb', f'scoreboard players operation #ai_lf {OBJ} /= #c10 {OBJ}',
        f'scoreboard players operation #ai_ls {OBJ} = #mbLs mb', f'scoreboard players operation #ai_ls {OBJ} /= #c10 {OBJ}',
        f'scoreboard players operation #ai_d2 {OBJ} = #ai_lf {OBJ}', f'scoreboard players operation #ai_d2 {OBJ} *= #ai_lf {OBJ}',
        f'scoreboard players operation #t3 {OBJ} = #ai_ls {OBJ}', f'scoreboard players operation #t3 {OBJ} *= #ai_ls {OBJ}',
        f'scoreboard players operation #ai_d2 {OBJ} += #t3 {OBJ}',
        f'scoreboard players operation #rear {OBJ} *= #c2 {OBJ}', f'scoreboard players operation #rear {OBJ} %= #c64 {OBJ}',
        f'execute if score #ai_lf {OBJ} matches ..-1 run {fn("ai/rear_bit")}',
        f'execute if score #ai_d2 {OBJ} matches {FAR2 + 1}.. run scoreboard players add #far {OBJ} {SAMPLE_EVERY}',
        f'execute unless score #ai_d2 {OBJ} matches {FAR2 + 1}.. run {sset("#far", 0)}'])
    w('ai/rear_bit', [
        f'# Behind her (#ai_lf < 0): inside +-{api.REAR_RULE["deg"]} deg of her back when -f x 1000 >= |s| x 577 (cot 60 deg).',
        f'scoreboard players operation #t3 {OBJ} = #ai_lf {OBJ}', f'scoreboard players operation #t3 {OBJ} *= #cn1000 {OBJ}',
        f'scoreboard players operation #t4 {OBJ} = #ai_ls {OBJ}',
        f'execute if score #t4 {OBJ} matches ..-1 run scoreboard players operation #t4 {OBJ} *= #cn1 {OBJ}',
        f'scoreboard players operation #t4 {OBJ} *= #c577 {OBJ}',
        f'execute if score #t3 {OBJ} >= #t4 {OBJ} run scoreboard players add #rear {OBJ} 1'])
    w('ai/rear_count', ['# #ai_rc = rear samples among the last 6 (the bits of #rear).', sset('#ai_rc', 0),
                        f'scoreboard players operation #t {OBJ} = #rear {OBJ}']
      + [ln for _ in range(6) for ln in (f'scoreboard players operation #t2 {OBJ} = #t {OBJ}',
                                          f'scoreboard players operation #t2 {OBJ} %= #c2 {OBJ}',
                                          f'scoreboard players operation #ai_rc {OBJ} += #t2 {OBJ}',
                                          f'scoreboard players operation #t {OBJ} /= #c2 {OBJ}')])
    w('ai/front', [f'# 1 when the player is in front of her (|bearing| <= {CT["front_deg"]} deg: f >= |s|, f > 0), else fail.',
                   f'execute if score #ai_lf {OBJ} matches ..0 run return fail',
                   f'scoreboard players operation #t4 {OBJ} = #ai_ls {OBJ}',
                   f'execute if score #t4 {OBJ} matches ..-1 run scoreboard players operation #t4 {OBJ} *= #cn1 {OBJ}',
                   f'execute if score #ai_lf {OBJ} >= #t4 {OBJ} run return 1',
                   'return fail'])
    keys_cd = sorted(k for k in api.COOLDOWN if k in present)
    w('ai/phase', ['# A fight phase starts (P1 after the intro, P2 after the down / the A8 fail; @s any): the phase clock (A6',
                   f'# grace {A6["phase_grace"]} t), every cooldown ready now, the dwell counters cleared.',
                   sset('#ai_pht', 0), sset('#far', 0), sset('#rear', 0), sset('#ai_ff', 0), sset('#ai_nx', 0),
                   f'scoreboard players operation #a6cd {OBJ} = #clk {OBJ}', f'scoreboard players operation #ai_rcd {OBJ} = #clk {OBJ}',
                   f'scoreboard players remove #ai_rcd {OBJ} {api.REAR_RULE["cd_ignore_every"]}']
      + [f'scoreboard players operation #cd_{k} {OBJ} = #clk {OBJ}' for k in keys_cd])
    # ------------------------------------------------------------------------------------------- recovery
    rs = ['# Recovery start (@s = body, after a pattern / a transition): idle P1 16-24 t, P2 12-18 t (api.RECOVER) facing the',
          '# player - the punish window: farther than 6 b she walks in (P1 0.12 b/t) / glides in (P2 0.18 b/t), else strafes.',
          sset('#ai_fl', 0)]
    for fp, ph in FPS.items():
        lo, hi = api.RECOVER[fp]
        rs.append(f'execute if score #ph {OBJ} matches {ph} store result score #rec {OBJ} run random value {lo}..{hi}')
    rs += [f'execute unless score #ph {OBJ} matches {FPS[1]} unless score #ph {OBJ} matches {FPS[2]} run {sset("#rec", api.RECOVER[2][0])}',
           fn('ai/sample'),
           f'execute if score #ai_nx {OBJ} matches {S.TID["a3"]} run return run {fn("ai/approach")}',
           f'execute if score #ai_d2 {OBJ} matches {WALK2 + 1}.. if score #ph {OBJ} matches {FPS[2]} run {sset("#ai_mv", 5)}',
           f'execute if score #ai_d2 {OBJ} matches {WALK2 + 1}.. unless score #ph {OBJ} matches {FPS[2]} run {sset("#ai_mv", 1)}',
           f'execute if score #ai_d2 {OBJ} matches {WALK2 + 1}.. run return run {fn("ai/play_move")}',
           f'execute store result score #ai_mv {OBJ} run random value 2..3',
           fn('ai/play_move')]
    w('ai/rec_start', rs)
    w('ai/approach', ['# The far fallback (FAR_RULE glide + A3): glide in (A3_GLIDE b/t) until within 8 b, then A3 (#ai_nx).',
                      sset('#ai_mv', 4), sset('#rec', 40), api.play('glide')])
    w('ai/play_move', ['# The recovery clip (@s = body): walk / P2 glide in, strafe left / right (P2 the idle2 stance between).',
                       f'execute if score #ai_mv {OBJ} matches 1 run return run {api.play("walk")}',
                       f'execute if score #ai_mv {OBJ} matches 5 run return run {api.play("glide")}',
                       f'execute if score #ai_mv {OBJ} matches 2 run return run {api.play("strafe_l")}',
                       f'execute if score #ai_mv {OBJ} matches 3 run return run {api.play("strafe_r")}',
                       f'execute if score #ph {OBJ} matches {FPS[2]} run return run {api.play("idle2")}',
                       api.play('idle')])
    sp = api.L.num(api.WALK_SPEED, 3)
    w('ai/recover', [
        '# One idle tick (@s = body, #pat 0): face the player, walk / glide / strafe (mv/ok-checked), the flinch (6 t, no step),',
        '# then the decision when the recovery ran out.',
        f'execute if score #rec {OBJ} matches 1.. run scoreboard players remove #rec {OBJ} 1',
        f'function rlk:mboss/mv/turn {{max:{api.TRACK["deg"]}}}',
        f'execute if score #ai_fl {OBJ} matches 1.. run scoreboard players remove #ai_fl {OBJ} 1',
        f'execute if score #ai_fl {OBJ} matches 1.. run return 0',
        f'execute if score #ai_mv {OBJ} matches 1 at @s unless entity {S.PLAYER[:-1]},distance=..3] run function rlk:mboss/mv/toward {{d:{sp}}}',
        f'execute if score #ai_mv {OBJ} matches 5 at @s unless entity {S.PLAYER[:-1]},distance=..3] run function rlk:mboss/mv/toward {{d:{api.L.num(api.GLIDE_SPEED, 3)}}}',
        f'execute if score #ai_mv {OBJ} matches 4 at @s unless entity {S.PLAYER[:-1]},distance=..{api.L.num(api.A3_GLIDE[0], 1)}] run function rlk:mboss/mv/toward {{d:{api.L.num(api.A3_GLIDE[1], 3)}}}',
        f'execute if score #ai_mv {OBJ} matches 4 at @s if entity {S.PLAYER[:-1]},distance=..{api.L.num(api.A3_GLIDE[0], 1)}] run {sset("#rec", 0)}',
        f'execute if score #ai_mv {OBJ} matches 2 at @s rotated as @s rotated ~-90 0 positioned ^ ^ ^{sp} if function rlk:mboss/mv/ok run tp @s ~ ~ ~',
        f'execute if score #ai_mv {OBJ} matches 3 at @s rotated as @s rotated ~90 0 positioned ^ ^ ^{sp} if function rlk:mboss/mv/ok run tp @s ~ ~ ~',
        f'execute if score #rec {OBJ} matches ..0 run {fn("ai/decide")}'])
    # ------------------------------------------------------------------------------------------- the decision
    dec = ['# The decision (@s = body, the end of the recovery): the test hold, the reserved phase step (a floor was reached),',
           '# the test lock, a forced next entry, the rear rule, the far rule, the weighted pick of the band (cooldowns, no',
           '# immediate repeat, MID_MAX).',
           f'execute if score #lock {OBJ} matches 1 run return run {sset("#rec", 10)}',
           f'execute if score #fl {OBJ} matches 1 if score #ph {OBJ} matches {PH["p1"]} run return run {fn("core/cs1/start")}',
           f'execute if score #fl {OBJ} matches 2 if score #ph {OBJ} matches {PH["p2"]} run return run {fn("core/lead/a13")}',
           fn('ai/sample')]
    for k in sorted(present, key=lambda k: S.TID[k]):
        if S.TID[k] in api.LOCK_IDS:
            dec.append(f'execute if score #mbLock mb matches {S.TID[k]} run return run {fn(f"core/start/{k}")}')
    dec += [f'execute if score #ai_nx {OBJ} matches {S.TID["a3"]} run return run {fn("ai/next_a3")}',
            fn('ai/rear_count'),
            f'execute if score #ai_rc {OBJ} matches {REAR_N}.. if function {api.NS}ai/rear run return 1',
            f'execute if score #ai_ff {OBJ} matches 1 if function {api.NS}ai/after_a6 run return 1',
            f'execute if score #far {OBJ} matches {api.FAR_RULE["dwell"]}.. run return run {fn("ai/far")}']
    for fp, ph in FPS.items():
        for bi, band in enumerate(BANDS):
            lim = (f'..{NEAR2}', f'..{MID2}', None)[bi]
            cond = f'if score #ph {OBJ} matches {ph}' + (f' if score #ai_d2 {OBJ} matches {lim}' if lim else '')
            dec.append(f'execute {cond} run return run {fn(f"ai/pick/p{fp}_{band}")}')
    dec.append(fn('ai/none'))
    w('ai/decide', dec)
    w('ai/next_a3', ['# The far fallback\'s approach ended: A3 (its cooldown and the no-repeat rule kept; else the normal pick).',
                     sset('#ai_nx', 0), sset('#ai_wa3', 1)] + allowed('a3', '#ai_wa3', 1)
      + [f'execute if score #ai_wa3 {OBJ} matches 1 run return run {fn("core/start/a3")}', fn('ai/decide')])
    w('ai/none', ['# Nothing may run now (every candidate cooling down): the recovery goes on a little longer.', sset('#rec', 8)])
    w('ai/after_a6', [f'# The decision {A6["next"]} t after A6: the far rule when the player is farther than {api.L.num(api.FAR_RULE["dist"])} b (no dwell',
                      '# needed), else the normal pick (fails).', sset('#ai_ff', 0),
                      f'execute unless score #ai_d2 {OBJ} matches {FAR2 + 1}.. run return fail',
                      fn('ai/far'), 'return 1'])
    # the rear rule: A1 (its cooldown ignored once per cd_ignore_every t); fails when it does not run
    rr = api.REAR_RULE
    rk = rr['key']
    w('ai/rear', [f'# The player stayed behind her ({rr["dwell"][0]} of {rr["dwell"][1]} t): {rk.upper()} (no immediate repeat); its cooldown is',
                  f'# ignored once per {rr["cd_ignore_every"]} t. Fails when it may not run.',
                  f'execute if score #last {OBJ} matches {S.TID[rk]} run return fail',
                  f'execute if score #cd_{rk} {OBJ} <= #clk {OBJ} run return run {fn("ai/rear_go")}',
                  f'scoreboard players operation #t {OBJ} = #clk {OBJ}', f'scoreboard players operation #t {OBJ} -= #ai_rcd {OBJ}',
                  f'execute if score #t {OBJ} matches ..{rr["cd_ignore_every"] - 1} run return fail',
                  f'scoreboard players operation #ai_rcd {OBJ} = #clk {OBJ}', f'return run {fn("ai/rear_go")}'])
    w('ai/rear_go', [f'# The rear rule starts {rk.upper()}.', fn(f'core/start/{rk}'), 'return 1'])
    # the far rule: per fight phase, weighted, cooldowns respected; fallback glide in + A3
    far = [f'# The player stayed farther than {api.L.num(api.FAR_RULE["dist"])} b for {api.FAR_RULE["dwell"]} t (or right after A6): the gap',
           '# closer of the fight phase (FAR_RULE weights; cooldowns and no-repeat kept); none may run -> glide in + A3.']
    for fp, ph in FPS.items():
        cands = [(k, wt) for k, wt in api.FAR_RULE[fp].items() if k in present]
        far.append(f'execute if score #ph {OBJ} matches {ph} run return run {fn(f"ai/far_p{fp}")}')
        w(f'ai/far_p{fp}', [f'# The far rule, P{fp}.'] + weighted(cands, var, fp, none_fn='ai/far_none'))
    far.append(fn('ai/far_none'))
    w('ai/far', far)
    w('ai/far_none', ['# The far fallback (FAR_RULE fallback glide + A3).', sset('#far', 0), sset('#ai_nx', S.TID['a3']), fn('ai/approach')])
    # weighted picks per fight phase and band
    for fp in FPS:
        for bi, band in enumerate(BANDS):
            cands = [(k, api.WEIGHTS[k][fp][bi]) for k in api.WEIGHTS if fp in api.WEIGHTS[k] and k in present
                     and api.WEIGHTS[k][fp][bi] > 0]
            w(f'ai/pick/p{fp}_{band}', [f'# Weighted pick, P{fp}, {band} (api.WEIGHTS; zeroed while cooling down / repeating / beyond MID_MAX).']
              + weighted(cands, var, fp, mid_band=(band == 'mid')))
    # ------------------------------------------------------------------------------------------- the triggers
    w('ai/counter', [
        f'# The counter trigger (core/fp: {CT["hits"]} player hits in {CT["window"]} t while she recovers / idles): {CT["chance"]} %: A1 when the',
        f'# player is beside / behind her (|bearing| > {CT["front_deg"]} deg), A2 in front; their cooldowns and no-repeat kept.',
        sset('#ctr', 0),
        f'execute store result score #t {OBJ} run random value 1..100',
        f'execute if score #t {OBJ} matches {CT["chance"] + 1}.. run return fail',
        fn('ai/sample'), sset('#t', 0),
        f'execute if function {api.NS}ai/front run {sset("#t", 1)}',
        f'execute if score #t {OBJ} matches 1 if function {api.NS}ai/counter_a2 run return 1',
        f'execute if score #t {OBJ} matches 0 if function {api.NS}ai/counter_a1 run return 1',
        'return fail'])
    for k in ('a1', 'a2'):
        fp_lines = [sset(f'#ai_w{k}', 1)]
        for fp, ph in FPS.items():
            fp_lines += [S.gate(f'if score #ph {OBJ} matches {ph}', x) for x in allowed(k, f'#ai_w{k}', fp)]
        w(f'ai/counter_{k}', [f'# The counter: {k.upper()} now (when it may run).'] + fp_lines
          + [f'execute unless score #ai_w{k} {OBJ} matches 1 run return fail', fn(f'core/start/{k}'), 'return 1'])
    w('ai/a6', [
        f'# The skill trigger (core/fp, on_hit flagged #a6q): A6 when the player is within {api.L.num(A["near"])} b, the phase is older',
        f'# than {A["phase_grace"]} t, it is off cooldown, she is between patterns or in the first {A["windup_t"]} t of a windup, {A["chance"]} %.',
        sset('#a6q', 0),
        f'execute if score #ai_pht {OBJ} matches ..{A["phase_grace"] - 1} run return fail',
        f'execute if score #a6cd {OBJ} > #clk {OBJ} run return fail',
        f'execute if score #pat {OBJ} matches {S.TID["a6"]} run return fail',
        f'execute if score #pat {OBJ} matches 1.. if score #pt {OBJ} matches {A["windup_t"] + 1}.. run return fail',
        f'execute if score #pat {OBJ} matches {min(S.TID[g] for g in api.GAUNTLETS)}.. run return fail',
        f'execute at @s unless entity {S.PLAYER[:-1]},distance=..{api.L.num(A["near"])}] run return fail',
        f'execute store result score #t {OBJ} run random value 1..100',
        f'execute if score #t {OBJ} matches {A["chance"] + 1}.. run return fail',
        f'execute if score #pat {OBJ} matches 1.. run {fn("core/cancel_pat0")}',
        fn('core/start/a6'), 'return 1'])
