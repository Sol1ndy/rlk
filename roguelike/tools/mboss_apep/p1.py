"""Phase-1 patterns of 아펩의 오아시스 파수꾼 (AP-P1; plan 8.1, 8.0, 7.10-7.11, 9.3, the 10-20 telegraph rule of plan 14;
ap_contract 0.8 / 1.3 / 1.4 / 0.13): P1 잠복 돌진 (1 burrow), P2 생명의 손 (2 hands), P3 발광하는 파수꾼 (3 glow),
P4 초목이 시든 풍경 (4 wither), P5 생명의 꼬리 (5 tail), P6 근접 콤보 (6 combo), R 잠복 이동 (7 reloc, the opener of P4) and
the move sounds of the core's service 10 (p/move/fx). Writes AP:p/{burrow,hands,glow,wither,tail,combo,reloc}/** and
AP:p/move/fx only (api.OWN['p1']).

Clocks: #apPT = the first clip's tick (the core plays p.clip at clock 0; P2 / P6 start at -10 = the pre-turn lead).
Every event tick below is read from the rig manifest (api.ev / api.anchor / api.track / api.wedges); the module never
types a part position. Hazards: the framework hz/* with the module defaults (Dendro, quiet, no framework sound,
player-side reactions kept), DMG of api.py, sizes x1.2 of the footage (plan 8.0).

Telegraph rule (plan 14, 10-20; the user: a floor telegraph only where the footage shows one). keep rows: P1's burst
(the shadow_glide preset is the marker, no ring), P2's crack strips (tele/crack, same tick / size / tell as each strip),
P4's disc (tele/disc el 23 with its 23-t fill). Every other hazard is quiet and draws nothing on the floor before its hit;
the readable tell is the clip pose + sound named in the TABLE of S:ap/tests/pat_p1.py (tell_src), >= 10 t (>= 20 t for
the big ones), and each hit shows its impact preset on the hit tick. No-tips rule: no line, title or banner here.

Decisions inside the plan's latitude (documented for AP-I2 / the review):
- P1: the shadow (the hidden anchor) re-aims at the predictive lock (lead 10) at t23 / 26 / 29 and glides so that it is
  there at t32 (plan 8.1 says <= 0.7 b/t; the 10-20 rule needs the marker at the lock by t32, which a far player cannot
  get at 0.7 b/t, so the glide is as fast as the distance needs). The anchor stops with the burst anchor (the rig's
  burst/impact point, 3.13 b ahead) on the lock; the burst disc is centred there (= the lock unless the anchor clamp
  r 18 moved it).
- P2: the plunge disc is centred on the rig's plunge/impact anchor (4.22 b ahead, where the hands go in); the four
  stalks stand 6.6 b from the lock at +-60 deg (near, the boss side) and +-140 deg (far) of the lock -> boss direction,
  slams R-L-L-R = near right, far left, near left, far right (v1 H); a root beyond r 25.3 steps toward the lock.
  Strips 3-4 (and their crack decals) are made one tick after 1-2 (tells 34 / 41): the command budget.
- P3: the slams land on the rig's slam/impact anchor (4.22 b ahead of the anchor parked at the arena centre), the
  carpet and the homing wheels start there. The two homing wheels leave the front at +-12 deg of the player's bearing
  and steer (8 deg/t) from their 2nd tick while they ride the front at 0.75 b/t for 6 t, then 0.5 b/t (plan 8.1 says
  "then homing": steering only after the ride left every player 6-11 b from the slam point out of their reach, the
  wheels' 3.6-b turn radius being larger than the gap; v1 G shows them curving back onto the player).
- P5: the swings are the rig's (swing 1 sweeps the start frame's front -61..+89 deg, swing 2 its back -94..-227 deg);
  the pre-swing turn (1-8, <= 5 deg/t, <= 40 deg) puts the tail root toward the player (a BACK player meets swing 2).
  The swept wedges are api.wedges widened for the root's own motion (swept(), RP1-3); a second tip flash + cue at
  cock 2 (t48) marks swing 2.
Open requests: S:ap/requests/ap-p1.md (RP1-1 the yaw rebase, RP1-2 the org object tick, RP1-3 the wedges).
- P6: hit 4's disc is 7.2 b ahead of where the lunge glide (2.5 b, inside r 16) ends.
"""
import math

from .api import Pattern, Gen, TL, K, R_FAR, PLAYER, BODY, LOCK, ARENA_M
from . import api as A

L = A.L
n = L.num
CY = A.CY
DMG = A.DMG
KB = A.KB


def W(fn, fm, ff, su, bk):
    return dict(front_near=fn, front_mid=fm, front_far=ff, side_under=su, back=bk)


ev, rt, anchor = A.ev, A.rt, A.anchor
# ------------------------------------------------------------------------------------------------ the timelines
P1 = dict(dive=ev('burrow_strike', 'dive'), sink=ev('burrow_strike', 'sink'), hide=ev('burrow_strike', 'hide'),
          travel=ev('burrow_strike', 'travel'), lock=ev('burrow_strike', 'lock'), burst=ev('burrow_strike', 'burst'),
          loom=ev('burrow_strike', 'loom'), yawlock=ev('burrow_strike', 'yawlock'), sweep=ev('burrow_strike', 'sweep'),
          sweep_end=ev('burrow_strike', 'sweep_end'), land=ev('burrow_strike', 'land'), end=A.clip_len('burrow_strike'),
          head=anchor('burrow_strike', 'burst', 'impact')[2], burst_r=4.2, len=10.8, w=3.6, glide=7.0, lead_v=10,
          retarget=(23, 26, 29))
P1['burst_tell'] = P1['burst'] - P1['lock']                                  # 12: the shadow on the lock
P1['sweep_tell'] = P1['sweep'] - P1['yawlock']                               # 12: loom + yaw lock
assert (P1['lock'], P1['burst'], P1['sweep'], P1['end']) == (32, 44, 64, 82), P1
assert P1['retarget'][0] == P1['travel'] and P1['retarget'][-1] < P1['lock']

RL = dict(sink=ev('sink_p1', 'sink'), len1=A.clip_len('sink_p1'), emerge=A.clip_len('sink_p1') + 1,
          len2=A.clip_len('emerge_on_p1'), d=2.0)
RL['end'] = RL['emerge'] + RL['len2']                                        # 18 + 24 = 42
assert (RL['sink'], RL['emerge'], RL['end']) == (4, 18, 42), RL

P2 = dict(lead=10, swirl=ev('hands', 'swirl'), raise_=ev('hands', 'raise'), plunge=ev('hands', 'plunge'),
          lock=ev('hands', 'lock'), legs=ev('hands', 'legs'), lines=ev('hands', 'lines'),
          slams=tuple(ev('hands', f'slam{k}') for k in (1, 2, 3, 4)), sink=ev('hands', 'sink'), stand=ev('hands', 'stand'),
          flower=ev('hands', 'flower'), fold=ev('hands', 'fold'), end=A.clip_len('hands'),
          plunge_f=anchor('hands', 'plunge', 'impact')[2], plunge_r=4.2, strip=8.4, strip_w=3.0, strip_y1=2.5,
          ring=6.6, lead_v=6, slam_lead=4, stalk_kill=100)
# stalk k: (bearing from the lock -> boss direction, + = the right of a player facing the boss), slam order R-L-L-R
STALKS = ((60, 'near right'), (-140, 'far left'), (-60, 'near left'), (140, 'far right'))
# the crack strips: slams 1-2 drawn at t40 (lines), slams 3-4 one tick later (perf: four crack decals and four strips in
# one tick passed the 3000-command budget next to the rising stalks)
P2['made'] = (P2['lines'], P2['lines'], P2['lines'] + 1, P2['lines'] + 1)
P2['tells'] = tuple(t - m for t, m in zip(P2['slams'], P2['made']))          # 22 / 29 / 34 / 41
assert P2['plunge'] == 30 and P2['slams'] == (62, 69, 75, 82) and P2['tells'] == (22, 29, 34, 41), P2
assert A.org_clip('stalk', 'leg_slam')['events']['hit'] == P2['slam_lead'], 'the stalk slam lands on leg_slam hit'
assert P2['legs'] + A.org_clip('stalk', 'leg_rise')['len'] <= P2['lines'] + 6

P3 = dict(dive=5, travel=A.clip_len('burrow_in_p1'), glow_at=39, emerge=44, turn=(84, 93), slams_at=94,
          impact_f=anchor('glow_slams', 'slam1', 'impact')[2], slam_r=5.4, slam_y1=4.0, blade_r=7.2,
          car_r0=3.0, car_r1=14.4, car_dur=14, car_band=1.0, car_y1=0.7, wheel_r0=3.0, wheel_y=1.05, wheel_ang=12,
          wheel_spd=0.75, wheel_ride=6, wheel_steer_from=2, wheel_home=0.5, wheel_steer=8, wheel_life=22, wheel_hr=1.0)
P3['slams'] = tuple(P3['slams_at'] + ev('glow_slams', f'slam{k}') for k in (1, 2, 3))          # 141 / 164 / 195
P3['made'] = (P3['slams'][0] - 30, P3['slams'][0], P3['slams'][1])                            # 111 / 141 / 164
P3['tells'] = tuple(s - m for s, m in zip(P3['slams'], P3['made']))                           # 30 / 23 / 31
P3['end'] = P3['slams_at'] + A.clip_len('glow_slams')                                         # 225
P3['windup'] = (P3['slams_at'], P3['slams_at'] + ev('glow_slams', 'column'))                  # 94-130
P3['rear2'] = P3['slams_at'] + 52                     # the re-rear straight out of slam 1 (rig glow_slams keys 52-65)
assert P3['slams'] == (141, 164, 195) and P3['tells'] == (30, 23, 31) and P3['end'] == 225, P3
assert all(P3['impact_f'] == anchor('glow_slams', f'slam{k}', 'impact')[2] for k in (1, 2, 3))
assert P3['travel'] == 23 and ev('burrow_in_p1', 'dive') == P3['dive'] and P3['emerge'] + ev('emerge_crown_p1', 'targetable') == 55
CAR_RADII = [P3['car_r0'] + (P3['car_r1'] - P3['car_r0']) * k / P3['car_dur'] for k in range(1, P3['car_dur'] + 1)]
assert all(b - a <= P3['car_band'] + 1e-9 for a, b in zip([P3['car_r0']] + CAR_RADII, CAR_RADII))   # plan 7.11 rule 5
assert L.pj_speed_tenths(P3['wheel_spd']) == 7 and L.pj_speed_tenths(P3['wheel_home']) == 5        # quantized (rule 6)

P4 = dict(rear=ev('rotation', 'rear'), disc=ev('rotation', 'disc'), crash=ev('rotation', 'crash'), spin=ev('rotation', 'spin'),
          flash=ev('rotation', 'flash'), spin_end=ev('rotation', 'spin_end'), end=A.clip_len('rotation'), r=9.0, y1=3.0)
P4['tell'] = P4['crash'] - P4['disc']                                        # 24 (the fill reaches the rim at t39 / t40)
P4['act'] = P4['spin_end'] - P4['crash']                                     # 31: active over the crash and the spin
assert (P4['disc'], P4['crash'], P4['act']) == (16, 40, 31), P4

P5 = dict(turn=(0, 8), turn_max=5, raise_=ev('tail_p1x2', 'raise'), cock=ev('tail_p1x2', 'cock'),
          sw1=(ev('tail_p1x2', 'swing1'), ev('tail_p1x2', 'end1') - 2), cock2=ev('tail_p1x2', 'cock2'),
          sw2=(ev('tail_p1x2', 'swing2'), ev('tail_p1x2', 'end2')), made=(14, 39), reach=11.4, y1=3.0,
          end=A.clip_len('tail_p1x2'))
P5['sw1'] = (P5['sw1'][0], P5['sw1'][0] + 7)                                 # 8 swept ticks each (28-35, 52-59)
P5['sw2'] = (P5['sw2'][0], P5['sw2'][0] + 7)
API_WEDGES1 = A.wedges('tail_p1x2', P5['sw1'][0], P5['sw1'][1], P5['reach'])
API_WEDGES2 = A.wedges('tail_p1x2', P5['sw2'][0], P5['sw2'][1], P5['reach'])


def _tail_pts(t):
    """The tail root (s, f) and the tail-line yaw of tail_p1x2 at tick t in the start frame."""
    root, tip = A.track('tail_p1x2', 'tail_root')[t], A.track('tail_p1x2', 'tail_tip')[t]
    d = A.yaw_at('tail_p1x2', t)
    rs, rf = A.rot_local(root[0], root[2], d)
    ts, tf = A.rot_local(tip[0], tip[2], d)
    return (rs, rf), A.dir_yaw(ts - rs, tf - rf)


def swept(ws, reach):
    """api.wedges widened for the root's own motion (TODO(I2) requests/ap-p1.md RP1-3): the root swings ~1.2 b per tick,
    so the bare wedge about this tick's root misses slivers of the lane the tail line swept between the ticks (a standing
    player 4-6 b out could slip between two wedges). Each wedge keeps its root and grows to every point of the previous
    tick's tail line seen from that root from 3 b out (nearer, the hips and the 0.3-b pad cover), the radius to the
    farthest of them (<= reach + the root step); the overlap with the previous wedge is in the same volley group."""
    out = []
    for w in ws:
        (ps, pf), pa = _tail_pts(w['t'] - 1)
        rs, rf = w['root']
        lo, hi, r1 = w['a0'], w['a1'], reach
        for i in range(1, 23):
            u = reach * i / 22.0
            qs, qf = ps + u * -math.sin(math.radians(pa)), pf + u * math.cos(math.radians(pa))
            dd = math.hypot(qs - rs, qf - rf)
            if dd < 3.0:
                continue
            a = A.dir_yaw(qs - rs, qf - rf)
            mid = (w['a0'] + w['a1']) / 2.0
            while a - mid > 180:
                a -= 360
            while a - mid < -180:
                a += 360
            lo, hi, r1 = min(lo, a), max(hi, a), max(r1, dd)
        out.append(dict(w, a0=lo, a1=hi, r1=round(min(r1, reach + 1.5), 2)))
    return out


WEDGES1 = swept(API_WEDGES1, P5['reach'])
WEDGES2 = swept(API_WEDGES2, P5['reach'])
assert P5['sw1'] == (28, 35) and P5['sw2'] == (52, 59) and P5['turn'][1] * P5['turn_max'] <= 40, P5
assert A.yaw_at('tail_p1x2', P5['made'][0]) == 0 and A.yaw_at('tail_p1x2', P5['sw1'][0] - 1) == 0


def tail_line(t):
    """The tail-line yaw of tail_p1x2 at played tick t (start frame, Minecraft sense; api.wedges' construction)."""
    root, tip = A.track('tail_p1x2', 'tail_root')[t], A.track('tail_p1x2', 'tail_tip')[t]
    d = A.yaw_at('tail_p1x2', t)
    rs, rf = A.rot_local(root[0], root[2], d)
    ts, tf = A.rot_local(tip[0], tip[2], d)
    return A.dir_yaw(ts - rs, tf - rf)


def arc(t0, t1, d):
    """(start, end) of a swing's tail line from tick t0 - 1 to t1, unwrapped in the sweep direction d (+1 clockwise)."""
    a, b = tail_line(t0 - 1), tail_line(t1)
    while d * (b - a) < 0:
        b += 360 * d
    return a, b


ARC1 = arc(P5['sw1'][0], P5['sw1'][1], 1)                                    # -61 .. +88.6 (clockwise)
ARC2 = arc(P5['sw2'][0], P5['sw2'][1], -1)                                   # -94 .. -227 (counter-clockwise)
assert -70 < ARC1[0] < -50 and 80 < ARC1[1] < 95 and -100 < ARC2[0] < -85 and -235 < ARC2[1] < -220, (ARC1, ARC2)

P6 = dict(lead=10, track=(0, 3), lock1=4, hit1=ev('combo_a', 'hit'), b_at=A.clip_len('combo_a'),
          r1=7.2, a1=78, y1_1=1.8, r2=6.6, f2=anchor('combo_b', 'slam', 'impact')[2], r3=7.2, y1_3=0.7,
          r4=6.6, f4=anchor('combo_d', 'slam', 'impact')[2], lunge=2.5)
P6['hit2'] = P6['b_at'] + ev('combo_b', 'slam')                              # 29 + 17 = 46
P6['c_at'] = P6['b_at'] + A.clip_len('combo_b')                              # 73
P6['hit3'] = P6['c_at'] + ev('combo_c', 'hit')                               # 83
P6['d_at'] = P6['c_at'] + A.clip_len('combo_c')                              # 93
P6['hit4'] = P6['d_at'] + ev('combo_d', 'slam')                              # 120
P6['lunge_at'] = P6['d_at'] + ev('combo_d', 'lunge')                         # 115
P6['tells'] = (P6['hit1'] - P6['lock1'], 14, 10, 22)
P6['made'] = tuple(h - t for h, t in zip((P6['hit1'], P6['hit2'], P6['hit3'], P6['hit4']), P6['tells']))   # 4 / 32 / 73 / 98
P6['ends'] = {2: P6['c_at'] + A.clip_len('combo_end'), 3: P6['d_at'] + A.clip_len('combo_end'),
              4: P6['d_at'] + A.clip_len('combo_d')}                         # 93 / 113 / 170
assert (P6['hit1'], P6['hit2'], P6['hit3'], P6['hit4']) == (14, 46, 83, 120), P6
assert P6['made'] == (4, 32, 73, 98) and P6['ends'] == {2: 93, 3: 113, 4: 170}, P6
assert (P6['f2'], P6['f4']) == (4.8, 7.2), P6

PATTERNS = [
    Pattern(1, 'burrow', '잠복 돌진', 'normal', 'burrow_strike', phase=1, weight=W(1, 3, 4, 2, 2), cooldown=400,
            length=P1['end'], recover=40, max_len=100, last_hit=P1['sweep']),
    Pattern(2, 'hands', '생명의 손', 'normal', 'hands', phase=1, weight=W(1, 3, 3, 2, 2), lead=P2['lead'],
            length=P2['end'], recover=20, max_len=170, last_hit=P2['slams'][-1], hooks=('resume',)),
    Pattern(3, 'glow', '발광하는 파수꾼', 'normal', ['burrow_in_p1', 'emerge_crown_p1', 'glow_slams'], phase=1,
            weight=W(2, 2, 2, 2, 2), cooldown=700, first_after=3, length=P3['end'], recover=20, max_len=260,
            last_hit=P3['slams'][-1], hooks=('pj_end',)),
    Pattern(4, 'wither', '초목이 시든 풍경', 'normal', 'rotation', phase=1, weight=W(4, 2, 2, 4, 2),
            length=P4['end'], recover=10, max_len=150, last_hit=P4['spin_end'], opener=(7, R_FAR), hooks=('resume',)),
    Pattern(5, 'tail', '생명의 꼬리', 'normal', 'tail_p1x2', phase=1, weight=W(0, 0, 0, 1, 0), cooldown=200,
            length=P5['end'], recover=15, max_len=150, last_hit=P5['sw2'][1], gates=('side_rear',)),
    Pattern(6, 'combo', '근접 콤보', 'normal', 'combo_a', phase=1, weight=W(4, 1, 0, 1, 0), lead=P6['lead'],
            length=P6['ends'][4], recover=20, max_len=200, last_hit=P6['hit4']),
    Pattern(7, 'reloc', '잠복 이동', 'opener', ['sink_p1', 'emerge_on_p1'], length=RL['end'], recover=0, max_len=60),
]
P = {p.key: p for p in PATTERNS}

# ------------------------------------------------------------------------------------------------ helpers
AT_BODY = 'at @s rotated as @s rotated ~ 0'                  # the body's floor point, rotated as its facing


def msel(tag):
    return f'@e[type=minecraft:marker,tag={tag},limit=1]'


def at_m(tag):
    return f'at {msel(tag)} rotated as {msel(tag)}'


def marker(ctx, pid, tag):
    """A pattern marker at the execution context `ctx` (an execute chain), y on the floor, rotated as the context."""
    tags = ','.join(f'"{t}"' for t in ('rlk_room', 'rlk_mb_aux', 'rlk_mb_ap_pat', f'rlk_mb_ap_p{pid}', tag))
    return [f'kill @e[type=minecraft:marker,tag={tag}]',
            f'execute {ctx} positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:[{tags}]}}',
            f'execute {ctx} positioned ~ {CY} ~ run tp {msel(tag)} ~ ~ ~ ~ 0']


def hz(ctx, pid, opts, shape, *extra_tags):
    """A quiet framework hazard (module defaults + opts) made at the execution context `ctx`, tagged with its pattern
    (cancel / end remove it) and any extra tags."""
    return (Gen.hz_opts(**opts) + [f'execute {ctx} run {shape}' if ctx else shape]
            + [Gen.tag_last_hz(t) for t in (f'rlk_mb_ap_p{pid}',) + extra_tags])


def x(ctx, *cmds):
    return [f'execute {ctx} run {c}' for c in cmds]


def end_lines(pid):
    return [f'kill @e[tag=rlk_mb_ap_p{pid}]', Gen.end()]


def cancel(g, key, pid, extra=()):
    g.pw(key, 'cancel', [f'# {P[key].label} cut (any executor; idempotent): its markers, hazards and props go.',
                         f'kill @e[tag=rlk_mb_ap_p{pid}]', *extra])


STOP_MV = 'function rlk:mboss/mv/stop'
TURN = 'function rlk:mboss/mv/turn {{max:{}}}'


# ================================================================================================ P1 잠복 돌진
def emit_burrow(g):
    p, pid, key = P['burrow'], 1, 'burrow'
    head, F = P1['head'], g.fn
    tl = TL(g, key)
    floor = f'at @s positioned ~ {CY} ~'
    tl.at(P1['dive'], *x(floor, K.fx('burrow_pool', r=3.5), K.snd('p1_dive')))
    tl.at(P1['sink'], *x(floor, K.fx('leaf_flakes')))
    # the shadow: the hidden anchor glides at the predictive lock and stops with its head (the burst anchor) on it
    for t, tt in zip(P1['retarget'], (9, 6, 3)):
        tl.at(t, F(f'p/{key}/aim') + f' {{t:{P1["lock"] - t}}}')
    for t in range(P1['travel'], P1['burst'], 2):
        tl.at(t, *x(f'{AT_BODY} positioned ^ ^ ^{n(head)}', K.fx('shadow_glide')),
              *x(AT_BODY, K.fx('shadow_glide')), *x(f'{AT_BODY} positioned ^ ^ ^-2.5', K.fx('shadow_glide')))
    for t in range(P1['travel'], P1['burst'], 7):
        tl.at(t, *x(f'{AT_BODY} positioned ^ ^ ^{n(head)}', K.snd('p1_travel')))
    tl.at(P1['lock'], F(f'p/{key}/lock'))
    tl.at(P1['burst'], *x(at_m('rlk_mb_ap_p1b'), K.fx('gold_burst'), K.fx('leaf_debris'), K.snd('p1_burst')))
    # erupt / loom: the head tracks the player until the yaw lock (52), then the lane
    tl.span(P1['burst'] + 1, P1['yawlock'], TURN.format(6))
    tl.at(P1['yawlock'], F(f'p/{key}/lane'))
    tl.at(P1['sweep'], *x(at_m('rlk_mb_ap_p1l'), K.fx('slash_band', len=P1['len']), K.fx('spine_afterimage', len=P1['len']),
                          K.snd('p1_sweep')),
          f'execute at {msel("rlk_mb_ap_p1e")} run function rlk:mboss/mv/glide {{t:{P1["sweep_end"] - P1["sweep"]}}}')
    tl.at(P1['sweep_end'] + 1, Gen.release())
    tl.at(P1['land'], *x(floor, K.fx('leaf_splash'), K.snd('p1_land')))
    tl.at(P1['end'], *end_lines(pid))
    g.pw(key, 'aim', [
        f'# @s = body (hidden, t{P1["retarget"]}): the shadow\'s next goal: the predictive lock (lead {P1["lead_v"]}), its head ({n(head)} b',
        '# ahead, the rig\'s burst anchor) on it, the anchor inside r 18; it faces the lock and glides there over $(t) t.',
        *Gen.lockv(P1['lead_v']),
        *marker(f'at {LOCK} facing entity @s feet rotated ~ 0 positioned ^ ^ ^{n(head)}', pid, 'rlk_mb_ap_p1g'),
        f'execute as {msel("rlk_mb_ap_p1g")} run {Gen.clamp("burst1")}',
        f'execute at @s facing entity {LOCK} feet run tp @s ~ ~ ~ ~ 0',
        f'$execute at {msel("rlk_mb_ap_p1g")} run function rlk:mboss/mv/glide {{t:$(t)}}'])
    g.pw(key, 'lock', [
        f'# @s = body (t{P1["lock"]}, hidden): the lock is fixed: the anchor under it (head on the lock, clamp r 18), facing',
        f'# it; the burst disc r {P1["burst_r"]} on the head point, tell {P1["burst_tell"]} (keep row: the shadow is the marker, no ring),',
        f'# KB {KB["default"]} outward, height 0-4, {DMG["p1_burst"]} %.',
        *Gen.lockv(P1['lead_v']),
        *marker(f'at {LOCK} facing entity @s feet rotated ~ 0 positioned ^ ^ ^{n(head)}', pid, 'rlk_mb_ap_p1g'),
        f'execute as {msel("rlk_mb_ap_p1g")} run {Gen.clamp("burst1")}',
        STOP_MV,
        f'execute at {msel("rlk_mb_ap_p1g")} facing entity {LOCK} feet run tp @s ~ {CY} ~ ~ 0',
        *marker(f'{AT_BODY} positioned ^ ^ ^{n(head)}', pid, 'rlk_mb_ap_p1b'),
        *hz(at_m('rlk_mb_ap_p1b'), pid, dict(kb=KB['default'], kbdir=0, y1=4.0),
           Gen.hz_disc(P1['burst_r'], P1['burst_tell'], DMG['p1_burst'])),
        *x(at_m('rlk_mb_ap_p1b'), K.snd('p1_ring')),
        f'kill @e[type=minecraft:marker,tag=rlk_mb_ap_p1g]'])
    g.pw(key, 'lane', [
        f'# @s = body (t{P1["yawlock"]}): the yaw is locked; the sweep lane from the anchor along the facing, len {P1["len"]} w',
        f'# {P1["w"]}, height 0-3, tell {P1["sweep_tell"]} (none row: the loom + the lock are the tell), {DMG["p1_sweep"]} %; the glide goal',
        f'# {P1["glide"]} b along it (inside r 16).',
        *marker(AT_BODY, pid, 'rlk_mb_ap_p1l'),
        *hz(at_m('rlk_mb_ap_p1l'), pid, dict(y1=3.0), Gen.hz_line(P1['len'], P1['w'], P1['sweep_tell'], DMG['p1_sweep'])),
        *marker(f'{at_m("rlk_mb_ap_p1l")} positioned ^ ^ ^{n(P1["glide"])}', pid, 'rlk_mb_ap_p1e'),
        f'execute as {msel("rlk_mb_ap_p1e")} run {Gen.clamp("glide")}'])
    tl.write([f'# P1 잠복 돌진 (plan 8.1): dive {P1["dive"]}, hidden 22-43 (px burrowed 6-43: the clip), the shadow 23-43, lock',
              f'# {P1["lock"]}, burst {P1["burst"]}, yaw lock {P1["yawlock"]}, sweep {P1["sweep"]} + the glide to {P1["sweep_end"]}, land {P1["land"]}, end {P1["end"]}.',
              f'kill @e[tag=rlk_mb_ap_p{pid}]'], [f'# P1 tick (#apPT = the burrow_strike clip tick)'])
    cancel(g, key, pid, [f'execute as {BODY} run {STOP_MV}'])


# ================================================================================================ R 잠복 이동
def emit_reloc(g):
    p, pid, key = P['reloc'], 7, 'reloc'
    tl = TL(g, key)
    tl.at(RL['sink'], *x(f'at @s positioned ~ {CY} ~', K.fx('root_chunks'), K.snd('r_sink')))
    tl.at(RL['emerge'] - 1, Gen.lockb(RL['d']), Gen.tp_to(LOCK),
          f'execute at @s facing entity {PLAYER} feet run tp @s ~ ~ ~ ~ 0')
    tl.at(RL['emerge'], Gen.play('emerge_on_p1'), *x(f'at @s positioned ~ {CY} ~', K.fx('emerge_motes'), K.snd('r_emerge')))
    tl.at(RL['end'], *end_lines(pid))
    tl.write([f'# R 잠복 이동 (plan 8.1 R, the opener of P4 when the player is > {n(R_FAR)} b away): sink_p1 0-{RL["len1"]} (px burrowed',
              f'# from {RL["sink"]}), hidden, the anchor {n(RL["d"])} b before the player (lockb, inside r 14) facing them at t{RL["emerge"] - 1},',
              f'# emerge_on_p1 {RL["emerge"]}-{RL["end"]}; no damage. The core hands over to P4 at the end.',
              f'kill @e[tag=rlk_mb_ap_p{pid}]'], ['# R tick (#apPT: sink_p1 0-17, emerge_on_p1 from 18)'])
    cancel(g, key, pid)


# ================================================================================================ P2 생명의 손
def emit_hands(g):
    p, pid, key = P['hands'], 2, 'hands'
    F = g.fn
    tl = TL(g, key)
    tl.at(0, *marker(f'{AT_BODY} positioned ^ ^ ^{n(P2["plunge_f"])}', pid, 'rlk_mb_ap_p2p'),
          *hz(at_m('rlk_mb_ap_p2p'), pid, {}, Gen.hz_disc(P2['plunge_r'], P2['plunge'], DMG['p2_plunge'])))
    tl.at(P2['swirl'], *x('at @s', K.snd('p2_swirl')))
    for t in range(P2['swirl'], P2['raise_'] + 1, 4):
        tl.at(t, *x(AT_BODY, K.fx('swirl_wisps')))
    for t in range(P2['swirl'] + 3, P2['raise_'] + 1, 3):
        tl.at(t, *x('at @s', K.snd('p2_swirl_tick')))
    tl.at(P2['plunge'], *x(at_m('rlk_mb_ap_p2p'), K.fx('plunge_flash'), K.fx('splinter_splash'), K.snd('p2_plunge')))
    tl.at(P2['lock'], F(f'p/{key}/lock'))
    tl.at(P2['legs'], *[f'execute {at_m(f"rlk_mb_ap_p2s{k}")} run function {A.NS}om/stalk/spawn {{i:{k}}}' for k in range(4)],
          *[f'function {A.NS}om/stalk/play {{i:{k},clip:"leg_rise"}}' for k in range(4)],
          *x(at_m('rlk_mb_ap_p2k'), K.snd('p2_stalks')))
    tl.at(P2['made'][0], F(f'p/{key}/strips0'))
    tl.at(P2['made'][2], F(f'p/{key}/strips1'))
    for k, t in enumerate(P2['slams']):
        tl.at(t - P2['slam_lead'], f'function {A.NS}om/stalk/play {{i:{k},clip:"leg_slam"}}')
        tl.at(t, *x(at_m(f'rlk_mb_ap_p2s{k}'), K.fx('slam_arc'), K.snd('p2_slam')))
    tl.at(P2['sink'], *[f'function {A.NS}om/stalk/play {{i:{k},clip:"leg_sink"}}' for k in range(4)])
    # TODO(I2) requests/ap-p1.md RP1-2: the org objects tick (om/objects_tick, RORG-3) is not run by the core yet; P2
    # steps its own stalks while they live (drop this span when the core ticks the objects).
    tl.span(P2['legs'], P2['stalk_kill'] - 1, f'function {A.NS}om/stalk/tick')
    tl.at(P2['stalk_kill'], f'function {A.NS}om/stalk/kill_all', Gen.release())
    tl.at(P2['flower'], *x('at @s', K.snd('p2_flower')))
    tl.at(P2['fold'], *x('at @s', K.snd('p2_fold')))
    tl.at(P2['end'], f'function {A.NS}om/stalk/kill_all', *end_lines(pid))
    stalk_lines = []
    for k, (ang, name) in enumerate(STALKS):
        tag = f'rlk_mb_ap_p2s{k}'
        stalk_lines += [f'# stalk {k} ({name}, slam {k + 1} at t{P2["slams"][k]}): {P2["ring"]} b from the lock at {ang:+d} deg of the lock -> boss',
                        '# direction, facing the lock; a root beyond the walk disc steps toward the lock (0.5 b, at least 2.5 b off it).',
                        *marker(f'at {msel("rlk_mb_ap_p2k")} facing entity @s feet rotated ~{ang} 0 positioned ^ ^ ^{n(P2["ring"])}', pid, tag),
                        f'execute as {msel(tag)} at @s facing entity {msel("rlk_mb_ap_p2k")} feet run tp @s ~ ~ ~ ~ 0',
                        'scoreboard players set #apq2N mb 0',
                        f'execute as {msel(tag)} at @s run {F(f"p/{key}/root")}']
    g.pw(key, 'lock', [f'# @s = body (t{P2["lock"]}): the lock (lead {P2["lead_v"]}) kept as rlk_mb_ap_p2k; the four stalk roots.',
                       *Gen.lockv(P2['lead_v']), *Gen.keep('rlk_mb_ap_p2k')] + stalk_lines)
    g.pw(key, 'root', ['# @s = a stalk root marker, facing the lock: step 0.5 b toward it while beyond r 25.3 (<= 8 steps).',
                       f'execute positioned ~ {CY} ~ if entity {ARENA_M.replace("limit=1", f"distance=..{n(A.WALK_R)},limit=1")} run return 0',
                       'scoreboard players add #apq2N mb 1', 'execute if score #apq2N mb matches 9.. run return 0',
                       'tp @s ^ ^ ^0.5', F(f'p/{key}/root')])
    for half, ks in enumerate(((0, 1), (2, 3))):
        made = P2['made'][ks[0]]
        strips = [f'# @s = body (t{made}): crack strips {ks[0] + 1}-{ks[1] + 1} (keep rows: tele/crack, same tick / size / tell as each strip)',
                  f'# from the root toward the lock: len {P2["strip"]} w {P2["strip_w"]}, height 0-{P2["strip_y1"]}, tells',
                  f'# {tuple(P2["tells"][k] for k in ks)}, {DMG["p2_strip"]} % each, one volley group (<= 1 hit of the two).', Gen.GRP_NEW]
        for k in ks:
            tell = P2['tells'][k]
            strips += x(at_m(f'rlk_mb_ap_p2s{k}'), *Gen.decal('keep', K.tele_crack(P2['strip'], P2['strip_w'], tell)))
            strips += hz(at_m(f'rlk_mb_ap_p2s{k}'), pid, dict(grp=True, y1=P2['strip_y1']),
                         Gen.hz_line(P2['strip'], P2['strip_w'], tell, DMG['p2_strip']))
        if half == 0:
            strips += x(at_m('rlk_mb_ap_p2k'), K.snd('p2_lines'))
        g.pw(key, f'strips{half}', strips)
    # resume (after a pause cleared the kit telegraphs): the strips not yet slammed are drawn again with the ticks left
    res = ['# Resume (the pause cleared the kit telegraphs): each crack strip still to slam is drawn again with the ticks left.']
    for k, t in enumerate(P2['slams']):
        m = P2['made'][k]
        res += [f'execute if score #apPT mb matches {m}..{t - 1} run scoreboard players set #apq2R mb {t}',
                f'execute if score #apPT mb matches {m}..{t - 1} run scoreboard players operation #apq2R mb -= #apPT mb',
                f'execute if score #apPT mb matches {m}..{t - 1} store result storage rlk:mboss ap.p2.t int 1 run '
                'scoreboard players get #apq2R mb',
                f'execute if score #apPT mb matches {m}..{t - 1} {at_m(f"rlk_mb_ap_p2s{k}")} run '
                f'{F(f"p/{key}/crack")} with storage rlk:mboss ap.p2']
    g.pw(key, 'resume', res)
    g.pw(key, 'crack', ['# Macro {t}: one crack strip drawn again (keep row) with t ticks to its slam.',
                        f'$function {K.FN}tele/crack {{len:{int(round(P2["strip"] * 10))},w:{int(round(P2["strip_w"] * 10))},'
                        'back:0,tell:$(t),nd:0,hold:3}'])
    tl.write([f'# P2 생명의 손 (plan 8.1): pre-turn {P2["lead"]} t (the core), the plunge disc (0 -> {P2["plunge"]}), swirl {P2["swirl"]}-{P2["raise_"]}, lock',
              f'# {P2["lock"]}, stalks {P2["legs"]}, strips {P2["lines"]}, slams {P2["slams"]}, stalks sink {P2["sink"]}, end {P2["end"]}.',
              f'kill @e[tag=rlk_mb_ap_p{pid}]', f'function {A.NS}om/stalk/kill_all'],
             ['# P2 tick (#apPT = the hands clip tick; -9..0 the pre-turn)'], t0=-P2['lead'])
    cancel(g, key, pid, [f'function {A.NS}om/stalk/kill_all'])


# ================================================================================================ P3 발광하는 파수꾼
WHEEL_TAG = 'rlk_mb_ap_p3w'


def emit_glow(g):
    p, pid, key = P['glow'], 3, 'glow'
    F = g.fn
    tl = TL(g, key)
    floor = f'at @s positioned ~ {CY} ~'
    tl.at(P3['dive'], *x(floor, K.fx('burrow_pool', r=3.5), K.snd('p1_dive')))
    # hidden: the shadow glides to the arena centre (23-39), the gold glow, the emergence facing the player
    tl.at(P3['travel'], f'execute at @s facing entity {ARENA_M} feet run tp @s ~ ~ ~ ~ 0',
          f'execute at {ARENA_M} positioned ~ {CY} ~ run function rlk:mboss/mv/glide {{t:{P3["glow_at"] - P3["travel"]}}}')
    for t in range(P3['travel'], P3['glow_at'], 2):
        tl.at(t, *x(AT_BODY, K.fx('shadow_glide')), *x(f'{AT_BODY} positioned ^ ^ ^3', K.fx('shadow_glide')))
    tl.at(P3['glow_at'], STOP_MV, f'execute at {ARENA_M} run tp @s ~ {CY} ~', 'function rlk:mboss/mv/face',
          *x(f'at {ARENA_M} positioned ~ {CY} ~', K.fx('gold_glow', r=3.0), K.snd('p3_glow')))
    tl.at(P3['emerge'] - 1, 'function rlk:mboss/mv/face')
    tl.at(P3['emerge'], Gen.play('emerge_crown_p1'), *x(f'at @s positioned ~ {CY} ~', K.fx('crown_debris'), K.snd('p3_emerge')))
    tl.span(P3['turn'][0], P3['turn'][1], TURN.format(6))
    # the slams: the slam point (the rig's slam anchor, 4.22 b ahead), the wind-up, the hazards made per plan 8.1
    tl.at(P3['slams_at'], Gen.play('glow_slams'), *marker(f'{AT_BODY} positioned ^ ^ ^{n(P3["impact_f"])}', pid, 'rlk_mb_ap_p3c'),
          *x('at @s', K.snd('p3_windup')))
    for t in range(P3['windup'][0], P3['windup'][1] + 1, 4):
        tl.at(t, *x(AT_BODY, K.fx('spiral_wisps')))
    for k, (made, slam, tell) in enumerate(zip(P3['made'], P3['slams'], P3['tells'])):
        tl.at(made, F(f'p/{key}/hz{k}'))
        tl.at(slam - 1, *x(at_m('rlk_mb_ap_p3c'), K.fx('wheel_carpet', r0=P3['car_r0'], r1=P3['car_r1'], dur=P3['car_dur'])))
        tl.at(slam, *x(at_m('rlk_mb_ap_p3c'), K.fx('gold_burst'), K.snd('p3_slam'), K.snd('p3_wheels')), F(f'p/{key}/wheels{k}'))
        # the airborne blade rays follow one tick later (perf: the slam tick also makes the next slam's hazards)
        tl.at(slam + 1, *x(at_m('rlk_mb_ap_p3c'), K.fx('blade_burst', r=P3['blade_r'])))
        for i, r in enumerate(CAR_RADII, 1):
            tl.at(slam + i, f'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p3c{k}] run '
                            f'{Gen.hz_resize(r, max(0.0, r - P3["car_band"]))}')
        for t in range(slam + 4, slam + P3['car_dur'] + 1, 4):
            tl.at(t, *x(at_m('rlk_mb_ap_p3c'), K.snd('p3_wheel_roll')))
        g.pw(key, f'hz{k}', [
            f'# @s = body (t{made}): slam {k + 1} at t{slam} (none row: the coil / re-rear / leap is the tell; tell {tell}): the disc r',
            f'# {P3["slam_r"]} at the slam point, height 0-{n(P3["slam_y1"])}, {DMG[f"p3_slam{k + 1}"]} %; the thorn-wheel carpet: a ring front',
            f'# {P3["car_r0"]} -> {P3["car_r1"]} b in {P3["car_dur"]} t ({n((P3["car_r1"] - P3["car_r0"]) / P3["car_dur"], 3)} b/t), band {P3["car_band"]} b,',
            f'# jumpable (#hzY1 {int(P3["car_y1"] * 10)}), {DMG["p3_carpet"]} %, in a new volley group with homing wheel 1 (#apq3G).',
            *hz(at_m('rlk_mb_ap_p3c'), pid, dict(y1=P3['slam_y1']), Gen.hz_disc(P3['slam_r'], tell, DMG[f'p3_slam{k + 1}'])),
            Gen.GRP_NEW, 'scoreboard players operation #apq3G mb = #mbGrp mb',
            *hz(at_m('rlk_mb_ap_p3c'), pid, dict(grp=True, act=P3['car_dur'] + 1, y1=P3['car_y1']),
                Gen.hz_ring(P3['car_r0'] - P3['car_band'], P3['car_r0'], tell, DMG['p3_carpet']), f'rlk_mb_ap_p3c{k}')])
        wl = [f'# @s = body (slam {k + 1}, t{slam}): two homing thorn wheels (#pjNoDodge 1, sphere hr {P3["wheel_hr"]}, {DMG["p3_wheel"]} % each)',
              f'# on the carpet front (r {P3["wheel_r0"]}) at +-{P3["wheel_ang"]} deg of the player\'s bearing: {P3["wheel_spd"]} b/t for {P3["wheel_ride"]} t, then',
              f'# {P3["wheel_home"]} b/t, steering from {P3["wheel_steer_from"]} t (pj/steer {{max:{P3["wheel_steer"]}}}), life {P3["wheel_life"]} t; wheel 1 shares the carpet\'s group.']
        for i, ang in enumerate((-P3['wheel_ang'], P3['wheel_ang'])):
            tags = ','.join(f'"{t}"' for t in ('rlk_room', 'rlk_mb_aux', 'rlk_mb_ap_pat', f'rlk_mb_ap_p{pid}', WHEEL_TAG, 'rlk_mb_ap_p3wn'))
            wl += [f'execute {at_m("rlk_mb_ap_p3c")} facing entity {PLAYER} feet rotated ~{ang} 0 positioned ^ ^{n(P3["wheel_y"])} '
                   f'^{n(P3["wheel_r0"])} run summon minecraft:item_display ~ ~ ~ {{Tags:[{tags}],teleport_duration:1}}',
                   f'execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p3wn] run {K.prop("thorn_wheel_homing")}',
                   *Gen.pj_opts(nododge=1)]
            if i == 0:
                wl.append('scoreboard players operation #pjGrp mb = #apq3G mb')
            wl += [f'execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_p3wn] at @s facing entity {msel("rlk_mb_ap_p3c")} feet rotated ~180 0 '
                   f'run {Gen.pj_launch(P3["wheel_spd"], P3["wheel_life"], DMG["p3_wheel"], P3["wheel_hr"])}',
                   'tag @e[type=minecraft:item_display,tag=rlk_mb_ap_p3wn] remove rlk_mb_ap_p3wn']
        g.pw(key, f'wheels{k}', wl)
    tl.at(P3['slams'][-1] + 1, Gen.release())
    tl.at(P3['end'], *end_lines(pid))
    g.pw(key, 'wheel', [
        f'# @s = a homing wheel (module tick, before pj/all moves it; mbPjT = ticks flown): it peels off the carpet front toward the',
        f'# player from {P3["wheel_steer_from"]} t (<= {P3["wheel_steer"]} deg/t, level flight: the pitch stays 0) and slows to {P3["wheel_home"]} b/t after {P3["wheel_ride"]} t on the',
        '# front; the trail every 2 t (run as the wheel: it also spins the prop), the loop sound every 10 t.',
        f'execute if score @s mbPjT matches {P3["wheel_ride"]} run scoreboard players set @s mbPjV {L.pj_speed_tenths(P3["wheel_home"])}',
        f'execute if score @s mbPjT matches {P3["wheel_steer_from"]}.. run {Gen.pj_steer(P3["wheel_steer"])}',
        'execute at @s run tp @s ~ ~ ~ ~ 0',
        'scoreboard players operation #apq3M mb = @s mbPjT', 'scoreboard players operation #apq3M mb %= #apK2 mb',
        f'execute if score #apq3M mb matches 0 run {K.fx("homing_trail")}',
        'scoreboard players operation #apq3M mb = @s mbPjT', 'scoreboard players operation #apq3M mb %= #apK10 mb',
        f'execute if score #apq3M mb matches 1 run {K.snd("p3_homing_loop")}'])
    g.pw(key, 'pj_end', [
        '# Hook pj_end (@s = a P3 prop, #pjEv 1 wall / 2 life over / 4 hit): the wheel pops where it is (a hit: the thorn sound).',
        f'execute if score #pjEv mb matches 4 at @s run {K.snd("p3_wheel_hit")}',
        f'execute at @s run {K.fx("wheel_pop")}',
        'scoreboard players set #pjKeep mb 0'])
    tl.write([f'# P3 발광하는 파수꾼 (plan 8.1): dive {P3["dive"]}, hidden glide to the centre {P3["travel"]}-{P3["glow_at"]}, gold glow {P3["glow_at"]},',
              f'# emerge_crown_p1 {P3["emerge"]} (targetable 55), turn {P3["turn"]}, glow_slams {P3["slams_at"]}: slams {P3["slams"]} (+ carpets and',
              f'# homing wheels), end {P3["end"]}.', f'kill @e[tag=rlk_mb_ap_p{pid}]'],
             ['# P3 tick (#apPT: burrow_in_p1 0-22, hidden, emerge_crown_p1 44-83, glow_slams 94-224); the live wheels first.'],
             extra_tick=[f'execute as @e[type=minecraft:item_display,tag={WHEEL_TAG}] at @s run {F(f"p/{key}/wheel")}'])
    cancel(g, key, pid, [f'execute as {BODY} run {STOP_MV}'])


# ================================================================================================ P4 초목이 시든 풍경
def emit_wither(g):
    p, pid, key = P['wither'], 4, 'wither'
    F = g.fn
    tl = TL(g, key)
    disc = [K.tele_disc(P4['r'], P4['tell'], el=23, hold=P4['act'])]
    tl.at(P4['rear'] - 10, *x('at @s', K.snd('p4_rear')))
    tl.at(P4['disc'], *marker('at @s', pid, 'rlk_mb_ap_p4d'),
          *x(f'at @s positioned ~ {CY} ~', *Gen.decal('keep', *disc)),
          *hz(f'at @s positioned ~ {CY} ~', pid, dict(act=P4['act'], kb=KB['heavy'], kbdir=0, y1=P4['y1']),
              Gen.hz_disc(P4['r'], P4['tell'], DMG['p4'])),
          *x('at @s', K.snd('p4_hum')))
    tl.at(P4['crash'], *x(f'at @s positioned ~ {CY} ~', K.fx('leaf_splash'), K.snd('p4_spin')))
    for t in range(P4['spin'], P4['spin_end'] + 1, 3):
        tl.at(t, *x(AT_BODY, K.fx('spin_trails')))
    tl.at(P4['flash'], *x(AT_BODY, K.fx('spin_flash')))
    tl.at(P4['spin_end'] + 1, Gen.release())
    tl.at(P4['end'], *end_lines(pid))
    g.pw(key, 'resume', [
        '# Resume (the pause cleared the kit telegraphs): the disc again with the ticks left to the strike (fill) or of the',
        '# active window (hold).',
        f'execute if score #apPT mb matches {P4["disc"]}..{P4["crash"] - 1} run scoreboard players set #apq4R mb {P4["crash"]}',
        f'execute if score #apPT mb matches {P4["disc"]}..{P4["crash"] - 1} run scoreboard players operation #apq4R mb -= #apPT mb',
        f'execute if score #apPT mb matches {P4["disc"]}..{P4["crash"] - 1} store result storage rlk:mboss ap.p4.t int 1 run '
        'scoreboard players get #apq4R mb',
        f'execute if score #apPT mb matches {P4["disc"]}..{P4["crash"] - 1} run data modify storage rlk:mboss ap.p4.h set value {P4["act"]}',
        f'execute if score #apPT mb matches {P4["crash"]}..{P4["spin_end"] - 1} run data modify storage rlk:mboss ap.p4.t set value 1',
        f'execute if score #apPT mb matches {P4["crash"]}..{P4["spin_end"] - 1} run scoreboard players set #apq4R mb {P4["spin_end"]}',
        f'execute if score #apPT mb matches {P4["crash"]}..{P4["spin_end"] - 1} run scoreboard players operation #apq4R mb -= #apPT mb',
        f'execute if score #apPT mb matches {P4["crash"]}..{P4["spin_end"] - 1} store result storage rlk:mboss ap.p4.h int 1 run '
        'scoreboard players get #apq4R mb',
        f'execute if score #apPT mb matches {P4["disc"]}..{P4["spin_end"] - 1} {at_m("rlk_mb_ap_p4d")} run {F(f"p/{key}/disc")} with storage rlk:mboss ap.p4'])
    g.pw(key, 'disc', ['# Macro {t, h}: the P4 disc drawn again (keep row): fill to the rim in t, then hold h.',
                       f'$function {K.FN}tele/disc {{r:{int(round(P4["r"] * 10))},tell:$(t),el:23,nd:0,hold:$(h)}}'])
    tl.write([f'# P4 초목이 시든 풍경 (plan 8.1): arms / rear 0-{P4["disc"]}, the disc decal + hazard at t{P4["disc"]} (r {P4["r"]}, tell',
              f'# {P4["tell"]}: the 23-t fill, never shorter), strike {P4["crash"]} active {P4["act"]} t over the crash and spin, KB',
              f'# {KB["heavy"]} outward, height 0-3, {DMG["p4"]} %; spin {P4["spin"]}-{P4["spin_end"]}, stand, end {P4["end"]}.',
              f'kill @e[tag=rlk_mb_ap_p{pid}]'], ['# P4 tick (#apPT = the rotation clip tick)'])
    cancel(g, key, pid)


# ================================================================================================ P5 생명의 꼬리
def emit_tail(g):
    p, pid, key = P['tail'], 5, 'tail'
    F = g.fn
    tl = TL(g, key)
    tl.span(P5['turn'][0] + 1, P5['turn'][1], F(f'p/{key}/turn'))
    tl.at(P5['turn'][1] + 1, *marker('at @s rotated as @s rotated ~ 0', pid, 'rlk_mb_ap_p5f'))
    tl.at(P5['raise_'], *x('at @s', K.snd('p5_raise')))
    tip1 = anchor('tail_p1x2', 'cock', 'tail_tip')
    tip2 = A.track('tail_p1x2', 'tail_tip')[P5['cock2']]
    tl.at(P5['cock'], *x(f'{AT_BODY} positioned {A.loc(tip1[0], tip1[2], tip1[1])}', K.fx('tail_tip_flash'), K.snd('p5_cock')))
    tl.at(P5['cock2'], *x(f'{AT_BODY} positioned {A.loc(tip2[0], tip2[2], tip2[1])}', K.fx('tail_tip_flash'), K.snd('p5_cock')))
    for k, (ws, made, dmg, ac, d) in enumerate(((WEDGES1, P5['made'][0], 'p5_1', ARC1, 1), (WEDGES2, P5['made'][1], 'p5_2', ARC2, -1))):
        lines = [Gen.GRP_NEW]
        for w in ws:
            half = (w['a1'] - w['a0']) / 2.0
            mid = (w['a1'] + w['a0']) / 2.0
            lines += hz(f'{at_m("rlk_mb_ap_p5f")} positioned {A.loc(w["root"][0], w["root"][1])} rotated ~{n(mid, 2)} 0', pid,
                        dict(grp=True, kb=KB['heavy'], y1=P5['y1']),
                        Gen.hz_sector(w['r1'], max(1, math.ceil(half)), w['t'] - made, DMG[dmg]))
        g.pw(key, f'swing{k + 1}', [
            f'# @s = body (t{made}): swing {k + 1}\'s {len(ws)} swept wedges (plan 7.11 rule 3; api.wedges of the manifest\'s tail track x',
            f'# the yaw schedule, in the start frame rlk_mb_ap_p5f): hz/sector r {P5["reach"]} about each tick\'s tail root, the',
            f'# angle swept that tick, ticks {ws[0]["t"]}-{ws[-1]["t"]}, one volley group, KB {KB["heavy"]}, height 0-3, {DMG[dmg]} %. None row (no',
            '# lane decal): the S-raise / cock cue / tip flash / recoil are the tell.'] + lines)
        tl.at(made, F(f'p/{key}/swing{k + 1}'))
        s0, s1 = (P5['sw1'], P5['sw2'])[k]
        mid_arc = (ac[0] + ac[1]) / 2.0
        tl.at(s0, *x(f'{at_m("rlk_mb_ap_p5f")} rotated ~{n(mid_arc, 1)} 0',
                     K.fx('arc_trail', r=P5['reach'], a=int(round(abs(ac[1] - ac[0]) / 2.0)), dir=d)),
              *x('at @s', K.snd('p5_swing')))
        tl.at(s0 - 1, 'scoreboard players set #mbHitEv mb 0')
        tl.span(s0 + 1, s1 + 2, F(f'p/{key}/hit'))
    tl.at(P5['sw2'][1] + 1, Gen.release())
    tl.at(P5['end'], *end_lines(pid))
    g.pw(key, 'hit', ['# A tail hit landed this tick (the framework hit event): the knockback crack at the player, the edge flash.',
                      'execute unless score #mbHitEv mb matches 1.. run return 0', 'scoreboard players set #mbHitEv mb 0',
                      f'execute at {PLAYER} run {K.snd("p5_hit")}', K.hud('flash_hit')])
    g.pw(key, 'turn', [
        f'# @s = body (t1-{P5["turn"][1]}): turn the tail root toward the player (the back to it) by <= {P5["turn_max"]} deg/t.',
        'execute store result score #apq5Y mb run data get entity @s Rotation[0] 100',
        *marker(f'at @s facing entity {PLAYER} feet rotated ~180 0', pid, 'rlk_mb_ap_p5t'),
        f'execute store result score #apq5D mb run data get entity {msel("rlk_mb_ap_p5t")} Rotation[0] 100',
        'kill @e[type=minecraft:marker,tag=rlk_mb_ap_p5t]',
        'scoreboard players operation #apq5D mb -= #apq5Y mb', 'scoreboard players add #apq5D mb 90000',
        'scoreboard players operation #apq5D mb %= #c36000 mb', 'scoreboard players remove #apq5D mb 18000',
        f'scoreboard players set #apq5M mb {P5["turn_max"] * 100}', 'scoreboard players operation #apq5D mb < #apq5M mb',
        f'scoreboard players set #apq5M mb -{P5["turn_max"] * 100}', 'scoreboard players operation #apq5D mb > #apq5M mb',
        'scoreboard players operation #apq5Y mb += #apq5D mb',
        'execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #apq5Y mb',
        '# TODO(I2) requests/ap-p1.md RP1-1: the clip\'s yaw schedule pins Rotation to #apYaw0 every tick (core yaw/tick);',
        '# the pre-swing turn moves that start with it (an api helper would own this line).',
        'scoreboard players operation #apYaw0 mb = #apq5Y mb'])
    tl.write([f'# P5 생명의 꼬리 x2 (plan 8.1): turn the back to the player 1-{P5["turn"][1]} (<= {P5["turn_max"]} deg/t), S-raise {P5["raise_"]},',
              f'# cock cue {P5["cock"]} (tip flash), swing 1 wedges {P5["sw1"]}, recoil / cock 2 {P5["cock2"]}, swing 2 wedges {P5["sw2"]}, rise, end {P5["end"]}.',
              f'kill @e[tag=rlk_mb_ap_p{pid}]'], ['# P5 tick (#apPT = the tail_p1x2 clip tick)'])
    cancel(g, key, pid)


# ================================================================================================ P6 근접 콤보
def emit_combo(g):
    p, pid, key = P['combo'], 6, 'combo'
    F = g.fn
    tl = TL(g, key)
    g.pw(key, 'roll', ['# The hit count: #apArg (tests) or the 3 / 4 / 3 roll; the expected end on #apPLen.',
                       'scoreboard players operation #apq6 mb = #apArg mb',
                       'execute unless score #apq6 mb matches 2..4 store result score #apR mb run random value 0..9',
                       'execute unless score #apq6 mb matches 2..4 if score #apR mb matches 0..2 run scoreboard players set #apq6 mb 2',
                       'execute unless score #apq6 mb matches 2..4 if score #apR mb matches 3..6 run scoreboard players set #apq6 mb 3',
                       'execute unless score #apq6 mb matches 2..4 run scoreboard players set #apq6 mb 4']
         + [f'execute if score #apq6 mb matches {h} run {Gen.set_len(t)}' for h, t in sorted(P6['ends'].items())])
    IF = lambda cond, cmd: f'execute if score #apq6 mb matches {cond} run {cmd}'   # noqa: E731
    tl.span(P6['track'][0] + 1, P6['track'][1], TURN.format(3))
    # hit 1: the low arm sweep (sector), locked at t4
    tl.at(P6['made'][0], *hz(AT_BODY, pid, dict(y1=P6['y1_1']), Gen.hz_sector(P6['r1'], P6['a1'], P6['tells'][0], DMG['p6_1'])))
    tl.at(P6['hit1'], *x(AT_BODY, K.fx('arm_sweep', r=P6['r1'], a=P6['a1']), K.snd('p6_sweep')))
    tl.span(P6['hit1'] + 1, P6['made'][1] - 1, TURN.format(4))
    tl.at(P6['b_at'], Gen.play('combo_b'))
    # hit 2: the double slam 4.8 b ahead
    tl.at(P6['made'][1], *marker(f'{AT_BODY} positioned ^ ^ ^{n(P6["f2"])}', pid, 'rlk_mb_ap_p6b'),
          *hz(at_m('rlk_mb_ap_p6b'), pid, {}, Gen.hz_disc(P6['r2'], P6['tells'][1], DMG['p6_2'])))
    tl.at(P6['hit2'], *x(at_m('rlk_mb_ap_p6b'), K.fx('slam_burst'), K.snd('p6_slam')))
    tl.at(P6['hit2'] + 1, IF(2, Gen.release()))
    tl.span(P6['hit2'] + 1, P6['c_at'] - 1, IF('3..', TURN.format(4)))
    tl.at(P6['c_at'], IF(2, Gen.play('combo_end')), IF('3..', Gen.play('combo_c')), IF('3..', F(f'p/{key}/hit3')))
    tl.at(P6['hit3'], IF('3..', F(f'p/{key}/fx3')))
    tl.at(P6['hit3'] + 1, IF(3, Gen.release()))
    tl.at(P6['d_at'], IF(2, Gen.end()), IF(3, Gen.play('combo_end')), IF(4, Gen.play('combo_d')))
    tl.span(P6['d_at'] + 1, P6['made'][3] - 1, IF(4, TURN.format(4)))
    tl.at(P6['made'][3], IF(4, F(f'p/{key}/hit4')))
    tl.at(P6['lunge_at'], IF(4, f'execute at {msel("rlk_mb_ap_p6d")} run function rlk:mboss/mv/glide {{t:{P6["hit4"] - P6["lunge_at"]}}}'))
    tl.at(P6['hit4'], IF(4, F(f'p/{key}/fx4')))
    tl.at(P6['hit4'] + 1, IF(4, Gen.release()))
    tl.at(P6['ends'][3], IF(3, Gen.end()))
    tl.at(P6['ends'][4], IF(4, Gen.end()))
    g.pw(key, 'hit3', [f'# @s = body (t{P6["made"][2]}): hit 3, the low spin: a disc r {P6["r3"]} about the body, jumpable (#hzY1 {int(P6["y1_3"] * 10)}),',
                       f'# tell {P6["tells"][2]} (none row: the twist from t{P6["c_at"]}), {DMG["p6_3"]} %.',
                       *hz(f'at @s positioned ~ {CY} ~', pid, dict(y1=P6['y1_3']), Gen.hz_disc(P6['r3'], P6['tells'][2], DMG['p6_3']))])
    g.pw(key, 'fx3', [*x(AT_BODY, K.fx('spin_ring', r=P6['r3']), K.snd('p6_spin'))])
    g.pw(key, 'hit4', [f'# @s = body (t{P6["made"][3]}): hit 4, the leaping slam: the lunge goal {P6["lunge"]} b ahead (inside r 16); the disc',
                       f'# r {P6["r4"]} {P6["f4"]} b ahead of it (the rig\'s slam anchor after the lunge), tell {P6["tells"][3]} (none row: the',
                       f'# tallest rear from t{P6["d_at"]}), {DMG["p6_4"]} %.',
                       *marker(f'{AT_BODY} positioned ^ ^ ^{n(P6["lunge"])}', pid, 'rlk_mb_ap_p6d'),
                       f'execute as {msel("rlk_mb_ap_p6d")} run {Gen.clamp("glide")}',
                       *marker(f'at {msel("rlk_mb_ap_p6d")} rotated as @s rotated ~ 0 positioned ^ ^ ^{n(P6["f4"])}', pid, 'rlk_mb_ap_p6e'),
                       *hz(at_m('rlk_mb_ap_p6e'), pid, {}, Gen.hz_disc(P6['r4'], P6['tells'][3], DMG['p6_4']))])
    g.pw(key, 'fx4', [*x(at_m('rlk_mb_ap_p6e'), K.fx('leap_slam'), K.snd('p6_slam'))])
    tl.write([f'# P6 근접 콤보 (plan 8.1): pre-turn {P6["lead"]} t (the core), 2 / 3 / 4 hits (#apq6: #apArg or the 3 / 4 / 3 roll): a',
              f'# {P6["hit1"]}, b {P6["hit2"]}, c {P6["hit3"]}, d {P6["hit4"]} (lunge {P6["lunge_at"]}); ends {P6["ends"]}.',
              f'kill @e[tag=rlk_mb_ap_p{pid}]', F(f'p/{key}/roll')],
             ['# P6 tick (#apPT: combo_a 0-28, combo_b 29-72, combo_c / combo_end 73-92, combo_d / combo_end 93-)'], t0=-P6['lead'])
    cancel(g, key, pid, [f'execute as {BODY} run {STOP_MV}'])


# ================================================================================================ M (the core's service 10)
def emit_move_fx(g):
    crawl = A.CRAWL['max']
    stop_plant = crawl + 1 + ev('crawl_stop_p1', 'plant')
    walk_steps = [t for t in range(9, A.WALK['max'] + 1, 9)]
    lines = ['# Service 10 (core) step sounds (plan 8.1 M; @s = body, #apMvT = 1.. the move clock, #apMvK 1 crawl 2 walk 3-4',
             f'# crab-turn steps): crawl_p1 steps every 8 t to t{crawl}, the plant of crawl_stop_p1 at t{stop_plant}; walk_p1 steps every',
             '# 9 t; turn_p1_step steps every 5 t.',
             *Gen.every(8, f'execute if score #apMvK mb matches 1 if score #apMvT mb matches ..{crawl} run {K.snd("m_crawl")}',
                        clock='#apMvT'),
             f'execute if score #apMvK mb matches 1 if score #apMvT mb matches {stop_plant} run {K.snd("p1_land")}']
    lines += [f'execute if score #apMvK mb matches 2 if score #apMvT mb matches {t} run {K.snd("m_walk")}' for t in walk_steps]
    lines += Gen.every(5, f'execute if score #apMvK mb matches 3.. run {K.snd("m_walk")}', clock='#apMvT')
    g.w('p/move/fx', lines)


def emit(g):
    emit_burrow(g)
    emit_reloc(g)
    emit_hands(g)
    emit_glow(g)
    emit_wither(g)
    emit_tail(g)
    emit_combo(g)
    emit_move_fx(g)
