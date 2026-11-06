"""AI of 아를레키노 (PLAN §7.2; OWNER: S3): distance bands, the rear / far dwell rules, api.WEIGHTS / COOLDOWN / SCHEDULE,
no immediate repeat, the recovery walk / strafe facing the player, the phase step at the next decision after a floor.

Runtime (@s = the body): ai/sample every SAMPLE_EVERY fight ticks (mv/local: the squared distance #ai_d2 in cm^2, a 6-bit
rear history #rear = the last 30 t, the far dwell #far); ai/recover each idle tick; ai/decide when the recovery ran out.
Only patterns present in p1.PATTERNS + p2.PATTERNS are ever picked (S4's may be missing: skipped). Cooldowns are ready
times on the module clock #clk: #cd_<group> = #clk + cooldown. The schedules (F in P1b, Q5 in P2) are due times on #clk
(#sch_f / #sch_q5) plus the count of other patterns since (#ai_nf / #ai_nq); the clock stops while the fight is paused and
reload keeps the scores, so pause / reload keep the schedule. A (the melee string) starts only within A_GATE b (the
user's rule: melee only when the player is in reach; from 4.5 b she walks in during the raise).
"""
from . import api
from . import s3lib as S

OBJ = api.OBJ
fn, sset = S.fn, S.sset
NEAR2, MID2 = int((api.BANDS[0] * 100) ** 2), int((api.BANDS[1] * 100) ** 2)
FAR2 = int((api.FAR_DWELL[0] * 100) ** 2)
A_GATE = 7.0
A_GATE2 = int((A_GATE * 100) ** 2)
WALK2 = 600 ** 2                     # recovery: walk in beyond 6 b, else strafe
SAMPLE_EVERY = 5
REAR_SAMPLES = api.REAR_DWELL[0] // SAMPLE_EVERY        # 20 of 30 t = 4 of the last 6 samples
BANDS = ('near', 'mid', 'far')
COLS = ('p1a', 'p1b', 'p2')
GROUP_ID = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'G': 6, 'H': 7, 'F': 8, 'E70': 9,
            'Q0': 10, 'Q1': 11, 'Q2': 12, 'Q3': 13, 'Q4': 14, 'Q5': 15, 'Q6': 16}
COL_PH = {'p1a': api.PH['p1a'], 'p1b': api.PH['p1b'], 'p2': api.PH['p2']}


class Groups:
    """The AI groups whose variant patterns exist in this build."""

    def __init__(self, present):
        self.present = set(present)

    def variants(self, g, col):
        return [k for k in api.GROUPS[g].get(col, ()) if k in self.present]

    def has(self, g, col):
        return bool(self.variants(g, col))


def go_lines(groups, g, col):
    """Start group g in column col: its variant (A p1b: a4 / a5 50 %; Q5: q5a / q5b, never the same twice)."""
    vs = groups.variants(g, col)
    if len(vs) == 1:
        return [fn(f'core/start/{vs[0]}')]
    if g == 'A':
        a4, a5 = 'a4', 'a5'
        return [f'execute store result score #t {OBJ} run random value 1..100',
                f'execute if score #t {OBJ} matches ..{api.A_FIVE_PCT} run return run {fn(f"core/start/{a5}")}',
                fn(f'core/start/{a4}')]
    if g == 'Q5':
        qa, qb = S.TID['q5a'], S.TID['q5b']
        return [f'execute if score #ai_q5 {OBJ} matches {qa} run return run {fn("core/start/q5b")}',
                f'execute if score #ai_q5 {OBJ} matches {qb} run return run {fn("core/start/q5a")}',
                f'execute store result score #t {OBJ} run random value 0..1',
                f'execute if score #t {OBJ} matches 1 run return run {fn("core/start/q5b")}',
                fn('core/start/q5a')]
    raise AssertionError((g, vs))


def allowed(g, var, check_cd=True):
    """Lines zeroing var when group g may not run now (cooldown, no immediate repeat, Q6's first use, A's reach gate)."""
    out = []
    if check_cd and g in api.COOLDOWN:
        out.append(f'execute if score #cd_{g} {OBJ} > #clk {OBJ} run scoreboard players set {var} {OBJ} 0')
    out.append(f'execute if score #last {OBJ} matches {GROUP_ID[g]} run scoreboard players set {var} {OBJ} 0')
    if g == 'Q6':
        out.append(f'execute if score #ai_pht {OBJ} matches ..{api.Q6_FIRST - 1} run scoreboard players set {var} {OBJ} 0')
    if g == 'A':
        out.append(f'execute if score #ai_d2 {OBJ} matches {A_GATE2 + 1}.. run scoreboard players set {var} {OBJ} 0')
    return out


def build(W, ctx):
    w = W.w
    groups = Groups(ctx.present)
    ctx.groups = groups
    w('ai/sample', [
        f'# AI sample (@s = body, every {SAMPLE_EVERY} fight ticks and at each decision): the player in the body frame (mv/local, mm).',
        f'# #ai_d2 = squared distance in cm^2; #rear = 6-bit history of "behind her" (+-{api.REAR_DEG} deg, the last 30 t); #far =',
        f'# ticks farther than {L_num(api.FAR_DWELL[0])} b (0 when nearer).',
        'execute unless function rlk:mboss/mv/local run return 0',
        f'scoreboard players operation #t {OBJ} = #mbLf mb', f'scoreboard players operation #t {OBJ} /= #c10 {OBJ}',
        f'scoreboard players operation #t2 {OBJ} = #mbLs mb', f'scoreboard players operation #t2 {OBJ} /= #c10 {OBJ}',
        f'scoreboard players operation #ai_d2 {OBJ} = #t {OBJ}', f'scoreboard players operation #ai_d2 {OBJ} *= #t {OBJ}',
        f'scoreboard players operation #t3 {OBJ} = #t2 {OBJ}', f'scoreboard players operation #t3 {OBJ} *= #t2 {OBJ}',
        f'scoreboard players operation #ai_d2 {OBJ} += #t3 {OBJ}',
        f'scoreboard players operation #rear {OBJ} *= #c2 {OBJ}', f'scoreboard players operation #rear {OBJ} %= #c64 {OBJ}',
        f'execute if score #t {OBJ} matches ..-1 run {fn("ai/rear_bit")}',
        f'execute if score #ai_d2 {OBJ} matches {FAR2 + 1}.. run scoreboard players add #far {OBJ} {SAMPLE_EVERY}',
        f'execute unless score #ai_d2 {OBJ} matches {FAR2 + 1}.. run scoreboard players set #far {OBJ} 0'])
    w('ai/rear_bit', [
        f'# Behind her (#t = forward cm < 0): inside +-{api.REAR_DEG} deg of her back when -f x 1000 >= |s| x 577 (cot 60 deg).',
        f'scoreboard players operation #t3 {OBJ} = #t {OBJ}', f'scoreboard players operation #t3 {OBJ} *= #cn1000 {OBJ}',
        f'scoreboard players operation #t4 {OBJ} = #t2 {OBJ}',
        f'execute if score #t4 {OBJ} matches ..-1 run scoreboard players operation #t4 {OBJ} *= #cn1 {OBJ}',
        f'scoreboard players operation #t4 {OBJ} *= #c577 {OBJ}',
        f'execute if score #t3 {OBJ} >= #t4 {OBJ} run scoreboard players add #rear {OBJ} 1'])
    w('ai/rear_count', ['# #ai_rc = rear samples among the last 6 (bits of #rear).',
                        sset('#ai_rc', 0), f'scoreboard players operation #t {OBJ} = #rear {OBJ}']
      + [ln for _ in range(6) for ln in (f'scoreboard players operation #t2 {OBJ} = #t {OBJ}',
                                          f'scoreboard players operation #t2 {OBJ} %= #c2 {OBJ}',
                                          f'scoreboard players operation #ai_rc {OBJ} += #t2 {OBJ}',
                                          f'scoreboard players operation #t {OBJ} /= #c2 {OBJ}')])
    groups_all = sorted({g for g in api.GROUPS if any(groups.has(g, c) for c in COLS)}, key=lambda g: GROUP_ID[g])
    ctx.groups_all = groups_all
    w('ai/phase', ['# A fight phase starts (P1a after the intro, P1b after E70, P2 after T; @s any): the phase clock (Q6 first use),',
                   '# the cooldowns of every group ready now.', sset('#ai_pht', 0)]
      + [f'scoreboard players operation #cd_{g} {OBJ} = #clk {OBJ}' for g in groups_all if g in api.COOLDOWN])
    # schedules (PLAN §7.2: F first >= 240 t after E70, Q5 first >= 300 t after Q0; then every 900 t and >= 3 others)
    sf, sq = api.SCHEDULE['F'], api.SCHEDULE['Q5']
    w('ai/sched_f', [f'# F scheduled (@s any): first {sf["first_after"][1]} t after E70 (no count needed).',
                     f'scoreboard players operation #sch_f {OBJ} = #clk {OBJ}',
                     f'scoreboard players add #sch_f {OBJ} {sf["first_after"][1]}', sset('#ai_nf', 99)])
    w('ai/resched_f', [f'# F ran (or its break stun ended; @s any): the next one {sf["every"]} t from now and after >= {sf["min_others"]} others.',
                       f'scoreboard players operation #sch_f {OBJ} = #clk {OBJ}', f'scoreboard players add #sch_f {OBJ} {sf["every"]}',
                       sset('#ai_nf', 0)])
    w('ai/sched_q5', [f'# Q5 scheduled (@s any): first {sq["first_after"][1]} t after Q0.',
                      f'scoreboard players operation #sch_q5 {OBJ} = #clk {OBJ}',
                      f'scoreboard players add #sch_q5 {OBJ} {sq["first_after"][1]}', sset('#ai_nq', 99)])
    w('ai/resched_q5', [f'# Q5 ran (or its break stun ended): the next one {sq["every"]} t from now and after >= {sq["min_others"]} others.',
                        f'scoreboard players operation #sch_q5 {OBJ} = #clk {OBJ}', f'scoreboard players add #sch_q5 {OBJ} {sq["every"]}',
                        sset('#ai_nq', 0)])
    # recovery
    rs = ['# Recovery start (@s = body, after a pattern / stun / transition): idle 16-24 t (P2 12-18) facing the player - the',
          '# punish window, the scythe low: walk in (0.12 b/t) when farther than 6 b, else strafe (random side).']
    for col, fp in (('p1a', 1), ('p1b', 1), ('p2', 2)):
        lo, hi = api.RECOVER[fp]
        rs.append(f'execute if score #ph {OBJ} matches {COL_PH[col]} store result score #rec {OBJ} run random value {lo}..{hi}')
    rs += [f'execute if score #ai_d2 {OBJ} matches {WALK2 + 1}.. run {sset("#ai_mv", 1)}',
           f'execute if score #ai_d2 {OBJ} matches {WALK2 + 1}.. run return run {fn("ai/play_walk")}',
           f'execute store result score #ai_mv {OBJ} run random value 2..3',
           fn('ai/play_strafe')]
    w('ai/rec_start', rs)
    w('ai/play_walk', [f'execute if score #ph {OBJ} matches {api.PH["p2"]} run return run {api.play("walk2")}', api.play('walk')])
    w('ai/play_strafe', [f'execute if score #ai_mv {OBJ} matches 2 if score #ph {OBJ} matches {api.PH["p2"]} run return run {api.play("strafe2_l")}',
                         f'execute if score #ai_mv {OBJ} matches 3 if score #ph {OBJ} matches {api.PH["p2"]} run return run {api.play("strafe2_r")}',
                         f'execute if score #ai_mv {OBJ} matches 2 run return run {api.play("strafe_l")}',
                         api.play('strafe_r')])
    w('ai/recover', [
        '# One idle tick (@s = body, #pat 0): face the player, walk / strafe, then the decision when the recovery ran out.',
        f'execute if score #rec {OBJ} matches 1.. run scoreboard players remove #rec {OBJ} 1',
        'function rlk:mboss/mv/turn {max:10}',
        f'execute if score #ai_mv {OBJ} matches 1 at @s unless entity {S.PLAYER[:-1]},distance=..3] run function rlk:mboss/mv/toward {{d:{api.WALK_SPEED}}}',
        f'execute if score #ai_mv {OBJ} matches 2 at @s rotated as @s rotated ~-90 0 positioned ^ ^ ^0.08 if function rlk:mboss/mv/ok run tp @s ~ ~ ~',
        f'execute if score #ai_mv {OBJ} matches 3 at @s rotated as @s rotated ~90 0 positioned ^ ^ ^0.08 if function rlk:mboss/mv/ok run tp @s ~ ~ ~',
        f'execute if score #rec {OBJ} matches ..0 run {fn("ai/decide")}'])
    # decision
    dec = ['# The decision (@s = body, end of the recovery). Order: test hold, the reserved phase step (a floor was reached:',
           '# E70 / T), the test lock (#mbLock), Q0 (P2 opener), the schedules (F / Q5), the rear rule (P2: Q3), the far rule,',
           '# the weighted pick of the phase column / band (cooldowns, no immediate repeat, A within reach, Q6 first use).',
           f'execute if score #lock {OBJ} matches 1 run return run {sset("#rec", 10)}',
           f'execute if score #fl {OBJ} matches 1 run return run {fn("core/e70_go")}',
           f'execute if score #fl {OBJ} matches 2 run return run {fn("core/tr/start")}',
           fn('ai/sample')]
    for k in sorted(ctx.present, key=lambda k: S.TID[k]):
        if S.TID[k] in api.LOCK_IDS:
            dec.append(f'execute if score #mbLock mb matches {S.TID[k]} run return run {fn(f"core/start/{k}")}')
    if 'q0' in ctx.present:
        dec.append(f'execute if score #ph {OBJ} matches {api.PH["p2"]} if score #q0_ok {OBJ} matches 0 run return run {fn("core/start/q0")}')
    if groups.has('F', 'p1b'):
        dec.append(f'execute if score #ph {OBJ} matches {api.PH["p1b"]} if score #clk {OBJ} >= #sch_f {OBJ} if score #ai_nf {OBJ} '
                   f'matches {sf["min_others"]}.. run return run {fn("ai/go_f_p1b")}')
    if groups.has('Q5', 'p2'):
        dec.append(f'execute if score #ph {OBJ} matches {api.PH["p2"]} if score #q0_ok {OBJ} matches 1.. if score #clk {OBJ} >= '
                   f'#sch_q5 {OBJ} if score #ai_nq {OBJ} matches {sq["min_others"]}.. run return run {fn("ai/go_q5_p2")}')
    if groups.has('Q3', 'p2'):
        dec += [fn('ai/rear_count'),
                f'execute if score #ph {OBJ} matches {api.PH["p2"]} if score #ai_rc {OBJ} matches {REAR_SAMPLES}.. if function '
                f'{api.NS}ai/rear run return 1']
    dec.append(f'execute if score #far {OBJ} matches {api.FAR_DWELL[1]}.. if function {api.NS}ai/far run return 1')
    for col in COLS:
        if not any(api.WEIGHTS.get(g, {}).get(col) and groups.has(g, col) for g in api.WEIGHTS):
            continue
        dec.append(f'execute if score #ph {OBJ} matches {COL_PH[col]} if score #ai_d2 {OBJ} matches ..{NEAR2} run return run {fn(f"ai/pick/{col}_near")}')
        dec.append(f'execute if score #ph {OBJ} matches {COL_PH[col]} if score #ai_d2 {OBJ} matches ..{MID2} run return run {fn(f"ai/pick/{col}_mid")}')
        dec.append(f'execute if score #ph {OBJ} matches {COL_PH[col]} run return run {fn(f"ai/pick/{col}_far")}')
    dec.append(fn('ai/none'))
    w('ai/decide', dec)
    w('ai/none', ['# Nothing may run now (every candidate cooling down, or no pattern of this phase built yet): idle a little longer.',
                  sset('#rec', 8)])
    for col in COLS:
        for g in groups_all:
            if groups.has(g, col):
                w(f'ai/go_{g.lower()}_{col}', [f'# Start group {g} in {col} (@s = body).'] + go_lines(groups, g, col) + ['return 1'])
    # rear rule (P2): Q3 Q3_CHANCE %
    if groups.has('Q3', 'p2'):
        w('ai/rear', [f'# The player stayed behind her ({api.REAR_DWELL[0]} of {api.REAR_DWELL[1]} t, P2): Q3 {api.Q3_CHANCE} % (its cooldown',
                      '# and the no-repeat rule kept). Fails when not taken.',
                      f'execute store result score #t {OBJ} run random value 1..100',
                      f'execute if score #t {OBJ} matches {api.Q3_CHANCE + 1}.. run return fail',
                      sset('#ai_wq3', 1)] + allowed('Q3', '#ai_wq3')
          + [f'execute if score #ai_wq3 {OBJ} matches 1 run return run {fn("ai/go_q3_p2")}', 'return fail'])
    # far rule: D (P1) / Q2 (P2) 60 %, else C / Q4
    far = [f'# The player stayed farther than {L_num(api.FAR_DWELL[0])} b for {api.FAR_DWELL[1]} t: the gap closer - D (P1) / Q2 (P2) 60 %,',
           '# else C / Q4 (cooldowns ignored, no immediate repeat). Fails when neither may run.',
           f'execute store result score #t {OBJ} run random value 1..100']
    for col, (g1, g2) in (('p1a', ('D', 'C')), ('p1b', ('D', 'C')), ('p2', ('Q2', 'Q4'))):
        cands = [g for g in (g1, g2) if groups.has(g, col)]
        for g in cands:
            far += [sset(f'#ai_f{g}', 1)] + allowed(g, f'#ai_f{g}', check_cd=False)
        ph = f'if score #ph {OBJ} matches {COL_PH[col]}'
        if len(cands) == 2:
            far.append(f'execute {ph} if score #t {OBJ} matches ..60 if score #ai_f{g1} {OBJ} matches 1 run return run {fn(f"ai/go_{g1.lower()}_{col}")}')
            far.append(f'execute {ph} if score #ai_f{g2} {OBJ} matches 1 run return run {fn(f"ai/go_{g2.lower()}_{col}")}')
        for g in cands:
            far.append(f'execute {ph} if score #ai_f{g} {OBJ} matches 1 run return run {fn(f"ai/go_{g.lower()}_{col}")}')
    far.append('return fail')
    w('ai/far', far)
    # weighted picks
    for col in COLS:
        for bi, band in enumerate(BANDS):
            cands = [(g, api.WEIGHTS[g][col][bi]) for g in groups_all
                     if col in api.WEIGHTS.get(g, {}) and api.WEIGHTS[g][col][bi] > 0 and groups.has(g, col)]
            lines = [f'# Weighted pick, {col}, {band} (api.WEIGHTS; zeroed when cooling down / repeating / A out of reach).',
                     sset('#ai_sum', 0)]
            for g, wt in cands:
                var = f'#ai_w{g}'
                lines.append(sset(var, wt))
                lines += allowed(g, var)
                lines.append(f'scoreboard players operation #ai_sum {OBJ} += {var} {OBJ}')
            lines += [f'execute if score #ai_sum {OBJ} matches ..0 run return run {fn("ai/none")}',
                      f'execute store result score #ai_r {OBJ} run random value 0..999',
                      f'scoreboard players operation #ai_r {OBJ} *= #ai_sum {OBJ}',
                      f'scoreboard players operation #ai_r {OBJ} /= #c1000 {OBJ}']
            for g, wt in cands:
                var = f'#ai_w{g}'
                lines.append(f'execute if score #ai_r {OBJ} < {var} {OBJ} run return run {fn(f"ai/go_{g.lower()}_{col}")}')
                lines.append(f'scoreboard players operation #ai_r {OBJ} -= {var} {OBJ}')
            lines.append(fn('ai/none'))
            if any(api.WEIGHTS.get(g, {}).get(col) and groups.has(g, col) for g in api.WEIGHTS):
                w(f'ai/pick/{col}_{band}', lines)


def L_num(v):
    return api.L.num(v)
