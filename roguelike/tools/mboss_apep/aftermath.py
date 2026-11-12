"""Q2 종말의 여파 (AP-P3; plan 8.3 Q2, 7.4, 7.8, 9.3, Q3 / Q25; cm.md 13.6 / 13.11; ap_contract 0.8 id 32, kind
scheduled: forced by the core's Q2 schedule) and the 소생의 찬가 domes (AP:dome/**). Writes AP:p/aftermath/** and
AP:dome/** only (api.OWN['aftermath']).

Two clocks: #apPT = the pattern clock from B0 (the pattern start, before anything moves) and #apq32 = the aftermath clip
tick (#apPT - #apq32S, negative during the approach; #apq32S = 8 + n, the crouch and the walk of n <= 50 t).

B0: the real game's banner (kit hud/banner_aftermath, "소생의 찬가 보호막 안으로 들어가서 종말의 여파를 막아내세요" with the
red phrase: footage v5 18.2 s, w1; the allowed instant-kill warning), the three dome footprints (pale rims, dim until
their dome forms) and - fix 10-22f (user 10-22: "the field must be down before you are in a shield and chip you a
little; the shields at random spots, not an equilateral triangle, and further apart") - the field itself: the kit
mask wash and the field ring spread from the arena centre to r 26 over SPREAD t and the field-tick mask (FN-14 /
FN-15, Dendro, #hzNoDodge, no reaction, never lethal) ticks q2_tick per mille of max HP every TICK_EVERY t from
#apPT SPREAD to the last tick before the blast, on everyone outside a formed dome. The domes form on the pattern clock
(light pillars #apPT 24 / 28 / 32, formed 34 / 38 / 42), so there is a stretch where nobody can be inside a dome yet
(the chip the user asked for) and the player's own dome forms first. Then crouch_p3 and, unless the boss is within
2 b of the centre, the crawl to it (walk_p3, 0.4 b/t, <= 50 t); the aftermath clip from its tick 0.

Footprints (fix 10-22f, LAYOUT below): a random layout per cast out of a precomputed table, in the frame at the arena
centre facing the player at B0 (^z toward the player), chosen by the player's distance band (3 b bands) and a random
index (`random value`). Every layout of the table: centres in the annulus R_IN..R_OUT about the centre (the boss stands
at the centre for the cast; the dome edge <= 21.9 b, inside the walk radius 26 and clear of every arena prop: the
innermost, a lily pad corner, at 21.99 b; no walls in phase 3), pairwise S_MIN..S_MAX b apart, never near-equilateral
(the three distances not within EQ of each other, the angles not all within ANG_EQ of 60 deg), and the nearest dome
<= REACH b from any player position of the band inside the walk radius (<= REACH_BARRIER at the barrier, 26.6 b).
Dome 0 (the one nearest the band's player) forms first.

Clip (#apq32): t40 the boss lands at the centre: a field ring pulse (visual) and the blast mask (800 per mille, t156-175,
one hit; the first cast of a fight is never lethal, #apAft1 0, and is followed by the instant-kill warning
TXT['q2_lethal']). Inside a formed dome: no hit, +1 % max HP every 20 t (t54-174). The domes pop at t189. No cine (the
player must act). No-tips rule (user 10-21): the plan's sub-line "보호막이 사라질 때까지 기다리세요" (blast -> pop) is
advice the footage does not show: dropped.
"""
import itertools
import math
import random

from .api import Pattern, Gen, TL, PLAYER, ARENA_M, K, L
from . import api as A
from .p3 import mdist_lines, marker, m1, mall

NS = A.NS
CY = A.CY
num = L.num
AFT = 'aftermath'
ev = A.ev
WALK = A.P3_CENTRE_WALK
QA = dict(crouch=A.clip_len('crouch_p3'), field=ev(AFT, 'field'), rain=ev(AFT, 'rain'), blast=ev(AFT, 'blast'),
          window_end=ev(AFT, 'window_end'), pop=ev(AFT, 'pop'), burst=ev(AFT, 'burst'), end=A.clip_len(AFT),
          whirl=ev(AFT, 'whirl'), dome_r=4.5, field_r=26.0, heal_every=20, near=2.0, turn=12, pop_clip=6,
          # fix 10-22f, on the pattern clock #apPT (B0 = 0): the field spreads 0 -> SPREAD (>= 20 t of readable cue: the
          # banner, the footprints and the spreading field) and ticks from there; the light pillars and the domes after
          # it (10 t pillar tells, 4 t apart; dome 0 = the player's), so the ticks at 20 and 30 find nobody inside a dome
          spread=20, tick_every=10, pillars=(24, 28, 32), domes=(34, 38, 42))
assert (QA['field'], QA['blast'], QA['window_end'], QA['pop'], QA['end']) == (40, 156, 176, 189, 224), QA
S_MIN_, S_MAX_ = QA['crouch'], QA['crouch'] + WALK['max']                  # #apq32S = 8 + n, n 0..50
QA['tick_act'] = QA['blast'] - QA['spread']               # #hzAct = #apq32S + 136: the last tick at #apPT S + 155 (< the blast)
TICKS_MIN = len(range(QA['spread'], S_MIN_ + QA['blast'], QA['tick_every']))     # 15 (no walk: #apPT 20 .. 160)
TICKS_MAX = len(range(QA['spread'], S_MAX_ + QA['blast'], QA['tick_every']))     # 20 (the longest walk: 20 .. 210)
PRE_DOME = len(range(QA['spread'], QA['domes'][0], QA['tick_every']))            # 2: ticks before the first dome stands
assert QA['spread'] < QA['domes'][0], 'the field ticks before any dome stands (user 10-22)'
assert all(d - p == 10 for p, d in zip(QA['pillars'], QA['domes']))
assert S_MIN_ + QA['blast'] - QA['domes'][-1] >= 85       # every dome stands >= 85 t before the blast (U4): >= 122 t now
assert PRE_DOME == 2 and QA['domes'][0] % QA['tick_every'] != 0          # the first dome never forms on a tick
assert (TICKS_MIN, TICKS_MAX) == (15, 20) and TICKS_MAX * A.DMG_PM['q2_tick'] <= 400, (TICKS_MIN, TICKS_MAX)   # <= 40 % alone
HEAL_TICKS = list(range(54, QA['pop'], QA['heal_every']))   # 54 .. 174 (clip clock; every dome stands by then)
LEN = QA['crouch'] + WALK['max'] + QA['end']
PATTERNS = [
    Pattern(32, 'aftermath', '종말의 여파', 'scheduled', None, phase=3, length=LEN, recover=16, max_len=LEN + 30,
            last_hit=QA['crouch'] + WALK['max'] + QA['window_end']),
]
T_ = 'rlk_mb_ap_p32'
FP = [f'{T_}f{k}' for k in range(3)]                          # the footprints (planned dome centres)
HZ = f'{T_}h'                                                 # the two mask hazards
DOME = 'rlk_mb_ap_dome'
CX, CZ = num(A.CENTRE[0]), num(A.CENTRE[2])
CENTRE = f'positioned {CX} {CY} {CZ}'
HEAD = '# 종말의 여파 (aftermath, id 32; plan 8.3 Q2 / 7.8; fix 10-22f).'

# ------------------------------------------------------------------------------------------- the dome layouts (10-22f)
# The region and the rules (old, plan 7.8: A on the bearing at 7 b, B / C 120 deg round at 14 b or B near a far player:
# centres >= 9 b apart, 9.0-30.5 b in practice, the near case always the same isosceles 18.5 / 18.5 / 24.2).
LAYOUT = dict(r_in=7.0, r_out=17.4, s_min=14.0, s_max=30.0, eq=0.15, ang_eq=10.0, reach=9.0, reach_barrier=9.3,
              walk=float(A.ARENA['walk']), barrier=26.6, band=3.0, bands=9, per_band=12, seed=1022, prop_edge=21.99)
assert LAYOUT['r_out'] + QA['dome_r'] < LAYOUT['prop_edge'] and LAYOUT['walk'] == 26.0


def _angles(p):
    out = []
    for a, b, c in ((p[0], p[1], p[2]), (p[1], p[2], p[0]), (p[2], p[0], p[1])):
        v1, v2 = (b[0] - a[0], b[1] - a[1]), (c[0] - a[0], c[1] - a[1])
        cs = (v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2))
        out.append(math.degrees(math.acos(max(-1.0, min(1.0, cs)))))
    return out


def band_range(b):
    lo = b * LAYOUT['band']
    return lo, (LAYOUT['barrier'] if b == LAYOUT['bands'] - 1 else lo + LAYOUT['band'])


def layout_ok(p, b):
    """The rules of one layout p = 3 x (x left, z toward the player) for distance band b (see the docstring); p[0] = the
    player's dome (it forms first) is the one within reach."""
    lo, hi = band_range(b)
    rr = [math.hypot(*q) for q in p]
    dd = [math.dist(a, c) for a, c in itertools.combinations(p, 2)]
    if min(rr) < LAYOUT['r_in'] - 1e-9 or max(rr) > LAYOUT['r_out'] + 1e-9:
        return False
    if min(dd) < LAYOUT['s_min'] - 1e-9 or max(dd) > LAYOUT['s_max'] + 1e-9:
        return False
    if (max(dd) - min(dd)) / min(dd) < LAYOUT['eq'] or all(abs(a - 60.0) <= LAYOUT['ang_eq'] for a in _angles(p)):
        return False
    near = lambda d: math.dist((0.0, d), p[0])                  # noqa: E731  (convex in d: the band ends suffice)
    if any(near(d) > LAYOUT['reach'] + 1e-9 for d in (max(0.0, lo - 0.3), min(LAYOUT['walk'], hi + 0.3))):
        return False
    return hi <= LAYOUT['walk'] or near(LAYOUT['barrier']) <= LAYOUT['reach_barrier'] + 1e-9


def _layouts():
    rng = random.Random(LAYOUT['seed'])
    r_in, r_out = LAYOUT['r_in'], LAYOUT['r_out']

    def anywhere():
        rho, th = math.sqrt(rng.uniform(r_in ** 2, r_out ** 2)), rng.uniform(-math.pi, math.pi)
        return rho * math.sin(th), rho * math.cos(th)
    out = []
    for b in range(LAYOUT['bands']):
        lo, hi = band_range(b)
        got = []
        while len(got) < LAYOUT['per_band']:
            # the player's dome near the bearing at a reachable radius, the other two anywhere in the annulus
            rho0 = rng.uniform(max(r_in, min(r_out, hi - 9.5)), min(r_out, max(r_in, lo + 9.0)))
            a0 = math.radians(rng.uniform(-45.0, 45.0))
            p = [(rho0 * math.sin(a0), rho0 * math.cos(a0)), anywhere(), anywhere()]
            mid = (lo + min(hi, LAYOUT['walk'])) / 2
            p = sorted([(round(x, 2), round(z, 2)) for x, z in p], key=lambda q: math.dist((0.0, mid), q))   # dome 0 first
            if not layout_ok(p, b) or any(sum(min(math.dist(a, q) for q in g) for a in p) < 6.0 for g in got):
                continue
            got.append(p)
        out.append(got)
    return out


LAYOUTS = _layouts()
assert all(len(g) == LAYOUT['per_band'] and all(layout_ok(p, b) for p in g) for b, g in enumerate(LAYOUTS))
_DD = [math.dist(a, c) for g in LAYOUTS for p in g for a, c in itertools.combinations(p, 2)]
SPACING = (round(min(_DD), 2), round(max(_DD), 2))          # the table's actual pairwise range (>= 14, <= 30)


def mask(pm, tell, act, lethal, rearm=None, act_lines=()):
    """A mask hazard here (the cast's safe group #apq32G): pm per mille of max HP, tell, active window (act_lines: a
    runtime #hzAct instead)."""
    opts = dict(nododge=1, norx=1, pm=pm, act=act)
    if not lethal:
        opts['pm_lethal'] = 0
    if rearm:
        opts['rearm'] = rearm
    return [*Gen.hz_opts(**opts), *act_lines, 'scoreboard players operation #hzSafeG mb = #apq32G mb',
            *L.hz_mask(QA['dome_r'], tell, 1), Gen.tag_last_hz(HZ)]


def emit(g):
    p = PATTERNS[0]
    key = p.key
    F = g.fn
    tl = TL(g, key, clock='#apq32')
    tb = TL(g, key, clock='#apPT', sub='b')                   # the B0 clock (fix 10-22f): the field, the domes
    d0 = QA['domes']
    # ---------------------------------------------------------------- B0 + approach
    start = [HEAD, '# B0: the banner, the footprints (a random layout), the safe group; the approach length n (0 within 2 b of the',
             f'# centre, else ceil(d / 0.4 b) <= {WALK["max"]}); the clip starts at #apPT = 8 + n (#apq32S); then the field (the',
             f'# wash and the ring from the centre, r {QA["field_r"]} at t{QA["spread"]}) and its tick mask from t{QA["spread"]} (fix 10-22f).',
             f'kill @e[tag={T_}]', F('dome/clear'),
             L.hz_safe_new(), 'scoreboard players operation #apq32G mb = #mbSafeG mb',
             f'execute at @s run {K.hud("banner_aftermath")}', f'execute at @s run {K.snd("q2_banner")}',
             F(f'p/{key}/place'),
             f'execute at @s run {F(f"p/{key}/dist")}',
             'scoreboard players set #apq32N mb 0',
             f'execute if score #apq32D mb matches {int(QA["near"] * 10) + 1}.. run scoreboard players operation #apq32N mb = #apq32D mb',
             f'execute if score #apq32D mb matches {int(QA["near"] * 10) + 1}.. run scoreboard players add #apq32N mb 3',
             f'execute if score #apq32D mb matches {int(QA["near"] * 10) + 1}.. run scoreboard players operation #apq32N mb /= #apK4 mb',
             f'execute if score #apq32N mb matches {WALK["max"] + 1}.. run scoreboard players set #apq32N mb {WALK["max"]}',
             'scoreboard players operation #apq32S mb = #apq32N mb', f'scoreboard players add #apq32S mb {QA["crouch"]}',
             'scoreboard players operation #apPLen mb = #apq32S mb', f'scoreboard players add #apPLen mb {QA["end"]}',
             'scoreboard players operation #apq32 mb = #apPT mb', 'scoreboard players operation #apq32 mb -= #apq32S mb',
             'scoreboard players operation #apq32H mb = #mbHitEv mb',
             Gen.play('crouch_p3')]
    for k in range(3):
        start += [f'data modify storage rlk:mboss ap.p32.r{k} set value {{id:{k},r:{int(QA["dome_r"] * 10)},tell:{d0[k]},hold:1}}',
                  'scoreboard players operation #apq32X mb = #apq32S mb', f'scoreboard players add #apq32X mb {QA["pop"] - d0[k]}',
                  f'execute store result storage rlk:mboss ap.p32.r{k}.hold int 1 run scoreboard players get #apq32X mb',
                  f'execute at {m1(FP[k])} run function {K.FN}tele/safe_rim with storage rlk:mboss ap.p32.r{k}']
    start += [f'data modify storage rlk:mboss ap.p32.w set value {{r:{int(QA["field_r"] * 10)},tell:{QA["spread"]},hold:1}}',
              'scoreboard players operation #apq32X mb = #apq32S mb',
              f'scoreboard players add #apq32X mb {QA["window_end"] - QA["spread"]}',
              'execute store result storage rlk:mboss ap.p32.w.hold int 1 run scoreboard players get #apq32X mb',
              f'execute {CENTRE} run function {K.FN}tele/mask_wash with storage rlk:mboss ap.p32.w',
              f'execute {CENTRE} run {K.fx("field_ring", r0=3.0, r1=QA["field_r"], dur=QA["spread"])}',
              f'execute {CENTRE} run {K.snd("q2_release")}',
              f'execute {CENTRE} run {F(f"p/{key}/hz_ticks")}']
    g.pw(key, 'dist', ['# @s = body: #apq32D = the horizontal distance to the arena centre in tenths.']
         + mdist_lines(ARENA_M, '#apq32D', '#apq32'))
    g.pw(key, 'pdist', ['# @s = the player: #apq32P = the horizontal distance to the arena centre in tenths.']
         + mdist_lines(ARENA_M, '#apq32P', '#apq32'))
    nb = LAYOUT['bands']
    step = int(LAYOUT['band'] * 10)
    g.pw(key, 'place', [
        '# @s = body (B0): the three footprints (fix 10-22f): the player\'s distance band (3 b; #apq32P tenths) and a random',
        f'# layout of the band ({LAYOUT["per_band"]} each, aftermath.LAYOUTS: centres {num(LAYOUT["r_in"])}-{num(LAYOUT["r_out"])} b from the centre, '
        f'{num(LAYOUT["s_min"])}-{num(LAYOUT["s_max"])} b apart,',
        f'# never near-equilateral, the nearest <= {num(LAYOUT["reach"])} b from the band\'s player), in the frame at the centre facing the player.',
        f'kill @e[tag={T_}f]', 'scoreboard players set #apq32P mb 0',
        f'execute as {PLAYER} run {F(f"p/{key}/pdist")}',
        f'execute store result score #apq32L mb run random value 0..{LAYOUT["per_band"] - 1}']
        + [f'execute if score #apq32P mb matches {"" if b == 0 else b * step}..{"" if b == nb - 1 else (b + 1) * step - 1} {CENTRE} '
           f'facing entity {PLAYER} feet rotated ~ 0 run {F(f"p/{key}/lay/b{b}")}' for b in range(nb)])
    for b, grp in enumerate(LAYOUTS):
        lo, hi = band_range(b)
        lines = [f'# Band {b}: the player {num(lo)}-{num(hi)} b from the centre. At the centre (floor), ^z toward the player; #apq32L picks one.']
        for i, lay in enumerate(grp):
            for k, (x, z) in enumerate(lay):
                lines.append(f'execute if score #apq32L mb matches {i} positioned ^{num(x)} ^ ^{num(z)} run {marker(32, f"{T_}f", FP[k])}')
        g.pw(key, f'lay/b{b}', lines)
    # ---------------------------------------------------------------- the B0 clock (#apPT): domes, field look / sound
    for k in range(3):
        tb.at(QA['pillars'][k], f'execute at {m1(FP[k])} run {K.fx("light_pillar")}')
        tb.at(d0[k], f'execute at {m1(FP[k])} run {F(f"p/{key}/form")} {{i:{k}}}')
    last = S_MAX_ + QA['blast']
    for t in range(QA['spread'], last, 10):
        tb.at(t, f'execute if score #apq32 mb matches ..{QA["blast"] - 1} {CENTRE} run {K.fx("floor_glitter")}')
    for t in range(20, last, 20):
        tb.at(t, f'execute if score #apq32 mb matches ..{QA["blast"] - 1} {CENTRE} run {K.snd("q2_field_loop")}')
    for t, lines in sorted(tb.ev.items()):
        g.pw(key, tb.tname(t), [f'# {key} #apPT {t}'] + lines)
    g.pw(key, 'btick', ['# the B0 clock (#apPT; fix 10-22f): the light pillars and the domes, the field\'s glitter and loop until the blast.']
         + tb._node(sorted(tb.ev)))
    # ---------------------------------------------------------------- the clip timeline (#apq32 = the aftermath tick)
    tl.at(0, F(f'p/{key}/go'))
    tl.at(0, f'execute at @s run {K.fx("crouch_splash")}', f'execute at @s run {K.snd("q2_charge")}')
    tl.at(QA['whirl'], f'execute at @s run {K.snd("q2_whirl")}')
    for t in range(QA['whirl'], QA['whirl'] + 19, 3):
        tl.at(t, f'execute at @s run {K.fx("whirl_leaves")}')
    tl.at(QA['field'], F(f'p/{key}/field'))
    for t in HEAL_TICKS:
        tl.at(t, F(f'p/{key}/heal'))
    tl.at(QA['rain'], f'execute {CENTRE} run {K.snd("q2_rain")}')
    for t in range(QA['rain'], QA['blast'] + 1, 4):
        tl.at(t, f'execute {CENTRE} run {K.fx("beam_rain")}')
    # the flood sliced over three ticks (AP-I2 RP3-3: the whole flood in the blast tick passed the 3000-commands budget)
    tl.at(QA['blast'], K.hud('flash_white'), f'execute {CENTRE} run {K.fx("flood_part", life=24, part=0)}',
          f'execute {CENTRE} run {K.snd("q2_blast")}', K.hud('banner_end'))
    tl.at(QA['blast'] + 1, f'execute {CENTRE} run {K.fx("flood_part", life=23, part=1)}')
    tl.at(QA['blast'] + 2, f'execute {CENTRE} run {K.fx("flood_part", life=22, part=2)}')
    tl.at(QA['window_end'], Gen.release(),
          f'execute if score #apAft1 mb matches 0 run {Gen.line(A.TXT["q2_lethal"], A.WARN_HEX, 60)}')
    tl.at(QA['pop'], F(f'p/{key}/pop'))
    for k in range(3):
        tl.at(QA['pop'] + k, f'execute at {m1(FP[k])} run {K.fx("dome_pop")}')
    tl.at(QA['burst'], f'execute at @s run {K.fx("green_burst")}')
    tl.at(QA['pop'] + QA['pop_clip'] + 1, f'function {NS}om/dome/kill_all')
    extra = ['scoreboard players operation #apq32 mb = #apPT mb', 'scoreboard players operation #apq32 mb -= #apq32S mb',
             f'execute if score #apq32 mb matches ..-1 if score #apPT mb matches {QA["crouch"]} run {Gen.play("walk_p3")}',
             f'execute if score #apq32 mb matches ..-1 if score #apPT mb matches {QA["crouch"]}.. run {F(f"p/{key}/walk")}',
             f'execute if score #apq32 mb matches {QA["end"]}.. run return run {F(f"p/{key}/done")}',
             # a landed field tick (any tick up to the blast; the mask re-arms every TICK_EVERY t): its sound at the player
             f'execute if score #apq32 mb matches ..{QA["blast"] - 1} if score #mbHitEv mb > #apq32H mb at {PLAYER} run {K.snd("q2_tick")}',
             'scoreboard players operation #apq32H mb = #mbHitEv mb',
             F(f'p/{key}/btick')]
    tl.write(start, [HEAD, '# tick: the approach (#apq32 < 0), then the clip timeline (the core steps the dome models\' clips: obj/tick);',
                     '# the B0 clock first (btick: the domes and the field look).'], t0=-1000, extra_tick=extra)
    g.pw(key, 'walk', ['# @s = body (the approach): one 0.4 b step toward the centre and a turn toward it (<= 12 deg/t).',
                       f'execute at @s unless entity {ARENA_M.replace("limit=1", "distance=..0.25,limit=1")} run '
                       f'{Gen.move_to(ARENA_M, WALK["spd"])}',
                       F(f'p/{key}/turn_c')])
    g.pw(key, 'turn_c', [
        '# @s = body: turn toward the arena centre by <= 12 degrees (mboss/mv/turn with the centre as the target).',
        'execute store result score #apq32Y0 mb run data get entity @s Rotation[0] 100',
        f'execute at @s run summon minecraft:marker ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","{T_}","{T_}y"]}}',
        f'execute at @s facing entity {ARENA_M} feet run tp {m1(T_ + "y")} ~ ~ ~ ~ 0',
        f'execute store result score #apq32Y1 mb run data get entity {m1(T_ + "y")} Rotation[0] 100',
        f'kill {mall(T_ + "y")}',
        'scoreboard players operation #apq32Y1 mb -= #apq32Y0 mb', 'scoreboard players add #apq32Y1 mb 90000',
        'scoreboard players operation #apq32Y1 mb %= #c36000 mb', 'scoreboard players remove #apq32Y1 mb 18000',
        f'execute if score #apq32Y1 mb matches {QA["turn"] * 100 + 1}.. run scoreboard players set #apq32Y1 mb {QA["turn"] * 100}',
        f'execute if score #apq32Y1 mb matches ..{-QA["turn"] * 100 - 1} run scoreboard players set #apq32Y1 mb {-QA["turn"] * 100}',
        'scoreboard players operation #apq32Y0 mb += #apq32Y1 mb',
        'execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #apq32Y0 mb'])
    g.pw(key, 'go', [f'# @s = body (#apq32 0): at the centre on the floor (yaw kept), the aftermath clip ({QA["end"]} t) from its tick 0.',
                     f'execute at {ARENA_M} run tp @s ~ {CY} ~', Gen.play(AFT)])
    g.pw(key, 'field', [
        f'# At t{QA["field"]}: the boss lands at the centre: a field ring pulse r 3 -> {QA["field_r"]} (the field itself lies since B0) and the',
        f'# blast mask of the cast\'s safe group ({A.DMG_PM["q2_blast"]} per mille, t{QA["blast"]}-{QA["window_end"] - 1}, lethal unless this is the',
        '# first cast: #apAft1 0).',
        f'execute {CENTRE} run {K.fx("field_ring", r0=3.0, r1=QA["field_r"], dur=18)}',
        f'execute {CENTRE} run {K.snd("q2_release")}',
        f'execute if score #apAft1 mb matches 0 {CENTRE} run {F(f"p/{key}/hz_blast0")}',
        f'execute unless score #apAft1 mb matches 0 {CENTRE} run {F(f"p/{key}/hz_blast1")}'])
    g.pw(key, 'hz_ticks', [
        f'# B0 (fix 10-22f): the field ticks, {A.DMG_PM["q2_tick"]} per mille of max HP, never lethal, re-armed every {QA["tick_every"]} t from',
        f'# #apPT {QA["spread"]} (the field at r {QA["field_r"]}) to the last tick before the blast (#apPT #apq32S + {QA["blast"] - 1}):',
        f'# #hzAct = #apq32S + {QA["tick_act"]}; {TICKS_MIN}-{TICKS_MAX} ticks for a player outside every dome the whole time.']
        + mask(A.DMG_PM['q2_tick'], QA['spread'], None, False, rearm=QA['tick_every'],
               act_lines=['scoreboard players operation #hzAct mb = #apq32S mb', f'scoreboard players add #hzAct mb {QA["tick_act"]}']))
    g.pw(key, 'hz_blast0', ['# the first cast of the fight: the blast never kills (plan Q3).']
         + mask(A.DMG_PM['q2_blast'], QA['blast'] - QA['field'], QA['window_end'] - QA['blast'], False))
    g.pw(key, 'hz_blast1', ['# a later cast: the blast is lethal.']
         + mask(A.DMG_PM['q2_blast'], QA['blast'] - QA['field'], QA['window_end'] - QA['blast'], True))
    g.pw(key, 'form', [
        '# Macro {i}, at footprint i: the dome forms: the safe marker (rlk_mb_ap_dome + rlk_mb_hzsafe, mbHzSG = the cast\'s group;',
        '# at the floor point, RFX-3 / RORG-2), the dome models (org om/dome, rising), the rise sparkle and its sound.',
        f'summon minecraft:marker ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","{T_}","{DOME}","rlk_mb_hzsafe","{T_}n"]}}',
        f'scoreboard players operation @e[type=minecraft:marker,tag={T_}n] mbHzSG = #apq32G mb',
        f'$scoreboard players set @e[type=minecraft:marker,tag={T_}n] apL $(i)',
        f'tag @e[type=minecraft:marker,tag={T_}n] remove {T_}n',
        f'$execute rotated 0 0 run function {NS}om/dome/spawn {{i:$(i)}}',
        f'$function {NS}om/dome/play {{i:$(i),clip:"dome_rise"}}',
        K.fx('dome_rise'), K.snd('q2_dome')])
    g.pw(key, 'heal', [
        f'# Every {QA["heal_every"]} t while the domes stand: a player inside a formed dome (feet within its radius) heals 1 % max HP',
        '# (plan Q25 "소생의 찬가"; player/heal, so the item heal hooks see it).',
        f'execute at {PLAYER} positioned ~ {CY} ~ if entity @e[type=minecraft:marker,tag={DOME},distance=..{num(QA["dome_r"] + 0.3)}] '
        f'as @a[tag=player,scores={{dead=0}}] run {F(f"p/{key}/heal1")}'])
    g.pw(key, 'heal1', ['scoreboard players operation #heal tmp = @s maxHealth', 'scoreboard players operation #heal tmp /= #c100 mb',
                        'execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1', 'function rlk:player/heal',
                        f'execute at {PLAYER} run {K.fx("spark")}'])
    g.pw(key, 'pop', [f'# t{QA["pop"]}: every dome pops (the models\' pop clip, the rims end, the pop sound); the safe markers go. The kit\'s',
                      '# flash + shards per dome at t189 / 190 / 191 (one dome a tick: the per-tick command budget).']
         + [f'function {NS}om/dome/play {{i:{k},clip:"dome_pop"}}' for k in range(3)]
         + [f'execute as @e[type=minecraft:marker,tag={DOME},limit=1] at @s run {K.snd("q2_pop")}']
         + [K.tele_safe_end(k) for k in range(3)] + [f'kill @e[type=minecraft:marker,tag={DOME}]'])
    g.pw(key, 'done', [HEAD, '# The clip is over: the domes (popped at t189) and the pattern\'s markers go, then p/end.', F('dome/clear'),
                       f'kill @e[tag={T_}]', Gen.end()])
    g.pw(key, 'cancel', [HEAD, '# Cut / cancelled (pause -> resume, reload, death, tests; any executor): the domes, the masks, the',
                         '# footprints, the field wash and the banner go.', F('dome/clear'), f'kill @e[tag={T_}]', K.hud('banner_end')])
    g.w('dome/clear', ['# Every dome (safe markers + org models), the Q2 mask hazards and the footprint rims (idempotent, any executor;',
                       '# the core calls it from cleanup, the phase jumps, death and a cancelled Q2).',
                       f'execute as @e[type=minecraft:marker,tag={HZ}] at @s run function rlk:mboss/hz/expire',
                       f'kill @e[type=minecraft:marker,tag={DOME}]', f'function {NS}om/dome/kill_all',
                       'kill @e[tag=rlk_mb_ap_domed]', 'kill @e[type=minecraft:marker,tag=rlk_mb_ap_aft]']
        + [K.tele_safe_end(k) for k in range(3)])
