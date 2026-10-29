"""AI of 타키 (Tachy) (PLAN §4.3; OWNER: S3): distance bands, the rear / far dwell rules, api.WEIGHTS / api.COOLDOWN /
api.K_RULES, no immediate repeat, the recovery prowl and the phase step at the next decision after a floor.

Runtime (@s = the body): ai/sample every 5 fight ticks (mv/local: the squared distance #ai_d2 in cm^2, a 6-bit rear history
#rear = the last 30 t, the far dwell #far); ai/recover each idle tick (prowl: turn <= 8 deg/t, walk 0.12 b/t when farther
than 6 b, else strafe 0.08 b/t; the clip set by ai/rec_start); ai/decide at the end of the recovery. Only patterns present
in p_melee / p_air / p_mantle PATTERNS are ever picked. Cooldowns are ready times on the module clock #clk (no per-tick
countdown): #cd_<key> = #clk + cooldown (x 0.8 in P3; L 560).
"""
from . import api
from . import s3lib as S

OBJ = api.OBJ
fn, sset = S.fn, S.sset
NEAR2, MID2, FAR2 = int((api.BANDS[0] * 100) ** 2), int((api.BANDS[1] * 100) ** 2), int((api.FAR_B * 100) ** 2)
WALK2 = 600 ** 2                     # prowl: walk in beyond 6 b
BANDS = ('near', 'mid', 'far')
REAR_SAMPLES = api.REAR_DWELL[0] // 5          # 20 of 30 t = 4 of the last 6 samples (5 t apart)
SAMPLE_EVERY = 5
FP_OF_PH = {api.PH['p1']: 1, api.PH['p2']: 2, api.PH['p3']: 3}
C_TIDS = sorted(S.TID[k] for k in api.K_RULES['not_after'])


def cooldown(key, fp):
    if key == 'l' and fp == 3:
        return api.L_P3_COOLDOWN
    cd = api.COOLDOWN[key]
    return cd * api.P3_COOLDOWN_PCT // 100 if fp == 3 else cd


def allowed_lines(key, fp, var, check_cd=True):
    """Lines zeroing `var` when key may not run now (cooldown, no repeat, K rules, L's first use in P2)."""
    tid = S.TID[key]
    out = []
    if check_cd:
        out.append(f'execute if score #cd_{key} {OBJ} > #clk {OBJ} run scoreboard players set {var} {OBJ} 0')
    out.append(f'execute if score #last {OBJ} matches {tid} run scoreboard players set {var} {OBJ} 0')
    if key == 'k':
        out.append(f'execute if score #kgap {OBJ} matches ..{api.K_RULES["gap"] - 1} run scoreboard players set {var} {OBJ} 0')
        out.append(f'execute if score #last {OBJ} matches {C_TIDS[0]}..{C_TIDS[-1]} run scoreboard players set {var} {OBJ} 0')
    if key == 'l' and fp == 2:
        out.append(f'execute if score #ai_pht {OBJ} matches ..{api.L_FIRST_P2 - 1} run scoreboard players set {var} {OBJ} 0')
    return out


def build(W, ctx):
    w = W.w
    present = ctx.present                      # keys with a Pattern (melee + S4's)
    w('ai/sample', [
        f'# AI sample (@s = body, every {SAMPLE_EVERY} fight ticks and at each decision): the player in the body frame (mv/local, mm).',
        '# #ai_d2 = squared distance in cm^2; #rear = 6-bit history of "behind her" (rear +-60 deg, the last 30 t); #far = ticks',
        f'# farther than {api.FAR_B} b (0 when nearer).',
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
    w('ai/phase', [
        '# A fight phase starts (P1 after the intro, P2 after T1, P3 after T2; @s any): weights column, forced-swap limit,',
        '# the phase clock (L first use), the cooldowns reset to ready.',
        f'execute if score #ph {OBJ} matches {api.PH["p1"]} run {sset("#ai_fp", 1)}',
        f'execute if score #ph {OBJ} matches {api.PH["p2"]} run {sset("#ai_fp", 2)}',
        f'execute if score #ph {OBJ} matches {api.PH["p3"]} run {sset("#ai_fp", 3)}']
      + [f'execute if score #ai_fp {OBJ} matches {fp} run {sset("#ai_swl", api.G1_FORCE_SWAP[fp])}' for fp in (1, 2, 3)]
      + [sset('#ai_pht', 0)] + [f'scoreboard players operation #cd_{k} {OBJ} = #clk {OBJ}' for k in sorted(present)])
    # recovery
    rs = ['# Recovery start (@s = body, after a pattern / swap / stagger / transition): idle 18-26 t (P3 12-18) of slow prowl',
          '# facing the player: walk in when farther than 6 b, else strafe (random side) - the punish window.']
    for fp in (1, 2, 3):
        lo, hi = api.RECOVER[fp]
        rs.append(f'execute if score #ai_fp {OBJ} matches {fp} store result score #rec {OBJ} run random value {lo}..{hi}')
    rs += [f'execute if score #ai_d2 {OBJ} matches {WALK2 + 1}.. run {sset("#ai_mv", 1)}',
           f'execute if score #ai_d2 {OBJ} matches {WALK2 + 1}.. run return run {api.play("walk")}',
           f'execute store result score #ai_mv {OBJ} run random value 2..3',
           f'execute if score #ai_mv {OBJ} matches 2 run {api.play("strafe_l")}',
           f'execute if score #ai_mv {OBJ} matches 3 run {api.play("strafe_r")}']
    w('ai/rec_start', rs)
    w('ai/recover', [
        '# One idle tick (@s = body, #pat 0): prowl, then the decision when the recovery ran out.',
        f'execute if score #rec {OBJ} matches 1.. run scoreboard players remove #rec {OBJ} 1',
        'function rlk:mboss/mv/turn {max:8}',
        f'execute if score #ai_mv {OBJ} matches 1 at @s unless entity @e[tag=rlk_body,distance=..2.5,limit=1] run function rlk:mboss/mv/toward {{d:0.12}}',
        f'execute if score #ai_mv {OBJ} matches 2 at @s rotated as @s rotated ~-90 0 positioned ^ ^ ^0.08 if function rlk:mboss/mv/ok run tp @s ~ ~ ~',
        f'execute if score #ai_mv {OBJ} matches 3 at @s rotated as @s rotated ~90 0 positioned ^ ^ ^0.08 if function rlk:mboss/mv/ok run tp @s ~ ~ ~',
        f'execute if score #rec {OBJ} matches ..0 run {fn("ai/decide")}'])
    # decision
    dec = ['# The decision (@s = body, end of the recovery). Order: test freeze, the reserved phase step (a floor was reached:',
           '# the mantle), the forced G1 swap, the test lock (#mbLock), the rear rule, the far rule, the weighted pick of the',
           '# phase / band (cooldowns, no immediate repeat, K rules).',
           f'execute if score #lock {OBJ} matches 1 run return run {sset("#rec", 10)}',
           f'execute if score #flnext {OBJ} matches 1.. run return run {fn("mantle/start")}',
           f'execute if score #swt {OBJ} >= #ai_swl {OBJ} run return run {fn("el/swap_start")}',
           fn('ai/sample')]
    for k in sorted(present, key=lambda k: S.TID[k]):
        dec.append(f'execute if score #mbLock mb matches {S.TID[k]} run return run {fn(f"core/start/{k}")}')
    dec += [fn('ai/rear_count'),
            f'execute if score #ai_rc {OBJ} matches {REAR_SAMPLES}.. if function {api.NS}ai/rear run return 1',
            f'execute if score #far {OBJ} matches {api.FAR_DWELL}.. if function {api.NS}ai/far run return 1']
    for fp in (1, 2, 3):
        dec.append(f'execute if score #ai_fp {OBJ} matches {fp} if score #ai_d2 {OBJ} matches ..{NEAR2} run return run {fn(f"ai/pick/p{fp}_near")}')
        dec.append(f'execute if score #ai_fp {OBJ} matches {fp} if score #ai_d2 {OBJ} matches ..{MID2} run return run {fn(f"ai/pick/p{fp}_mid")}')
        dec.append(f'execute if score #ai_fp {OBJ} matches {fp} run return run {fn(f"ai/pick/p{fp}_far")}')
    w('ai/decide', dec)
    w('ai/none', ['# Nothing may run now (every candidate cooling down): prowl a little longer.', sset('#rec', 8)])
    # rear rule: B2 70 % (the hop turns her) or K 30 %
    rear = [f'# The player stayed behind her ({api.REAR_DWELL[0]} of {api.REAR_DWELL[1]} t): B2 70 % or K 30 % (no repeat, K rules; '
            'cooldowns ignored). Fails when neither may run.',
            f'execute store result score #t {OBJ} run random value 1..100']
    have_k = 'k' in present
    if have_k:
        rear += [sset('#ai_wk', 1)] + allowed_lines('k', 0, '#ai_wk', check_cd=False)
    rear += [sset('#ai_wb', 1)] + allowed_lines('b2', 0, '#ai_wb', check_cd=False)
    if have_k:
        rear.append(f'execute if score #t {OBJ} matches 71.. if score #ai_wk {OBJ} matches 1 run return run {fn("ai/go_k")}')
    rear.append(f'execute if score #ai_wb {OBJ} matches 1 run return run {fn("ai/go_b2")}')
    if have_k:
        rear.append(f'execute if score #ai_wk {OBJ} matches 1 run return run {fn("ai/go_k")}')
    rear.append('return fail')
    w('ai/rear', rear)
    for k in ('a1', 'b2', 'k', 'w1'):
        if k in present:
            w(f'ai/go_{k}', [fn(f'core/start/{k}'), 'return 1'])
    far = [f'# The player stayed farther than {api.FAR_B} b for {api.FAR_DWELL} t: A1 or W1 (50 %, no repeat; cooldowns ignored).',
           f'execute store result score #t {OBJ} run random value 1..100']
    cand = [k for k in ('a1', 'w1') if k in present]
    for k in cand:
        far += [sset(f'#ai_w{k}', 1)] + allowed_lines(k, 0, f'#ai_w{k}', check_cd=False)
    if len(cand) == 2:
        far.append(f'execute if score #t {OBJ} matches 51.. if score #ai_ww1 {OBJ} matches 1 run return run {fn("ai/go_w1")}')
    for k in cand:
        far.append(f'execute if score #ai_w{k} {OBJ} matches 1 run return run {fn(f"ai/go_{k}")}')
    far.append('return fail')
    w('ai/far', far)
    # weighted picks
    for fp in (1, 2, 3):
        for bi, band in enumerate(BANDS):
            cands = [(k, api.WEIGHTS[k][fp][bi]) for k in sorted(present, key=lambda k: S.TID[k]) if api.WEIGHTS[k][fp][bi] > 0]
            lines = [f'# Weighted pick, phase {fp}, {band} (api.WEIGHTS; zeroed when cooling down / repeating / K rules).',
                     sset('#ai_sum', 0)]
            for k, wt in cands:
                var = f'#ai_w_{k}'
                lines.append(sset(var, wt))
                lines += allowed_lines(k, fp, var)
                lines.append(f'scoreboard players operation #ai_sum {OBJ} += {var} {OBJ}')
            lines += [f'execute if score #ai_sum {OBJ} matches ..0 run return run {fn("ai/none")}',
                      f'execute store result score #ai_r {OBJ} run random value 0..999',
                      f'scoreboard players operation #ai_r {OBJ} *= #ai_sum {OBJ}',
                      f'scoreboard players operation #ai_r {OBJ} /= #c1000 {OBJ}']
            for k, wt in cands:
                var = f'#ai_w_{k}'
                lines.append(f'execute if score #ai_r {OBJ} < {var} {OBJ} run return run {fn(f"core/start/{k}")}')
                lines.append(f'scoreboard players operation #ai_r {OBJ} -= {var} {OBJ}')
            lines.append(fn('ai/none'))
            w(f'ai/pick/p{fp}_{band}', lines)
