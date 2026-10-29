"""Original keyframes of the chapter-3 (Sumeru) regular mobs, 20 ticks/s. Humanoids (em, cw) are authored like
tools/ch2mob/poses.py (-Z forward, right hand on -X, degrees; built by ch2mob/rig.humanoid). The fungus, spore pod and
sand hatchling are small prop rigs posed directly in the display frame (+Z = the way the mob faces, y up, metres):
each pose is {part: (t, euler, scale)}; quaternions come from rig.q.

Pose ids keep the chapter-2 meaning: 0-3 idle, 10-17 walk, 20-23 tell, 24-25 strike, 30-32 recovery, 40-41 hit,
50-51 death; mob-specific: cw 60-63 channel / 70 interrupted; sb 80-81 mound, 82 erupt, 85 sink, 90 burrowed.
No reference motions copied.
"""
import math

from rig import GUARD

# ---------------------------------------------------------------- 에르미타 단검 용병: low stance, a dagger in each hand
EM_ATTACH = [('dagger_r', 'rhand', 0.0, [180, 0, 0], 1.0), ('dagger_l', 'lhand', 0.0, [180, 0, 0], 1.0),
             ('cloak', 'back', [0, 0, 0], [6, 0, 0], 1.0)]
EM_BASE = {'torso': [14, -6, 0], 'head': [-10, 6, 0], 'right_arm': [38, -10, -14], 'left_arm': [34, 10, 16],
           'right_leg': [-14, 0, -6], 'left_leg': [16, 0, 6], 'dagger_r': [180, 0, 0], 'dagger_l': [180, 0, 0],
           'cloak': [6, 0, 0], 'size': 0.96, 'ropen': 10, 'shift': [0, -0.05, 0]}


def _em():
    P = {}
    for i in range(4):
        a = i * math.pi / 2
        P[i] = ('ready_%d' % i, 12, {'shift': [0, -0.05 + math.sin(a) * .012, 0], 'torso': [14 + math.sin(a) * 1.5, -6, math.cos(a)],
                                     'head': [-10 - math.sin(a), 6, 0], 'cloak': [6 + math.sin(a) * 2, 0, 0]})
    for i in range(8):
        a = i * math.pi / 4
        s = math.sin(a)
        P[10 + i] = ('stalk_%d' % i, 3, {'shift': [0, -0.06 + abs(math.cos(a)) * .03, 0], 'torso': [18, -6 + s * 5, -s * 2], 'head': [-14, 6 - s * 5, 0],
                                         'right_arm': [40 + s * 14, -10, -14], 'left_arm': [36 - s * 14, 10, 16],
                                         'right_leg': [s * 34, 0, -3], 'left_leg': [-s * 34, 0, 3], 'cloak': [14 + abs(s) * 8, 0, s * 3]})
    # tell 0.6 s: sink into a crouch, both blades drawn back low, then coiled (blades glint)
    P[20] = ('crouch', 4, {'shift': [0, -0.14, 0.04], 'torso': [30, -4, 0], 'head': [-26, 4, 0], 'right_arm': [-20, -6, -26], 'left_arm': [-20, 6, 26],
                           'right_leg': [-38, 0, -8], 'left_leg': [30, 0, 8], 'dagger_r': [200, 0, 0], 'dagger_l': [200, 0, 0], 'cloak': [20, 0, 0]})
    P[21] = ('coiled', 6, {'shift': [0, -0.18, 0.06], 'torso': [36, -2, 0], 'head': [-32, 2, 0], 'right_arm': [-34, -8, -30], 'left_arm': [-34, 8, 30],
                           'right_leg': [-46, 0, -9], 'left_leg': [36, 0, 9], 'dagger_r': [210, 0, 0], 'dagger_l': [210, 0, 0], 'cloak': [26, 0, 0]})
    # dash + stab: lunge flat out, both daggers driven forward
    P[24] = ('lunge', 1, {'shift': [0, -0.1, -0.12], 'torso': [40, 0, 0], 'head': [-36, 0, 0], 'right_arm': [50, -14, -6], 'left_arm': [46, 14, 6],
                          'right_leg': [-50, 0, -4], 'left_leg': [44, 0, 4], 'dagger_r': [180, 0, 0], 'dagger_l': [180, 0, 0], 'cloak': [40, 0, 0]})
    P[25] = ('stab', 1, {'shift': [0, -0.12, -0.16], 'torso': [34, 0, 0], 'head': [-30, 0, 0], 'right_arm': [62, -20, -2], 'left_arm': [58, 20, 2],
                         'right_leg': [-40, 0, -4], 'left_leg': [40, 0, 4], 'dagger_r': [176, 0, 0], 'dagger_l': [176, 0, 0], 'cloak': [34, 0, 0]})
    P[30] = ('skid', 3, {'shift': [0, -0.13, -0.06], 'torso': [24, 10, 4], 'head': [-20, -10, -2], 'right_arm': [56, -24, -20], 'left_arm': [70, 18, 22],
                         'right_leg': [-28, 0, -10], 'left_leg': [30, 0, 10], 'dagger_r': [170, 0, 0], 'dagger_l': [190, 0, 0], 'cloak': [24, 0, 6]})
    P[31] = ('rise', 5, {'shift': [0, -0.08, -0.02], 'torso': [18, 4, 2], 'head': [-14, -4, 0]})
    P[40] = ('hit_recoil', 2, {'shift': [0, -0.08, 0.07], 'torso': [-12, 10, -8], 'head': [14, -10, 6], 'right_arm': [20, 6, -34], 'left_arm': [16, -6, 34],
                               'right_leg': [-10, 0, -6], 'left_leg': [14, 0, 6], 'cloak': [-6, 0, -4]})
    P[41] = ('hit_recover', 3, {'shift': [0, -0.06, 0.02], 'torso': [6, 2, -2], 'head': [-2, -2, 2]})
    P[50] = ('death_buckle', 2, {'shift': [0, -0.15, 0.05], 'torso': [-24, 12, -16], 'head': [24, -10, -10], 'right_arm': [70, 10, -60], 'left_arm': [70, 10, 60],
                                 'right_leg': [-26, 0, -14], 'left_leg': [30, 0, 14], 'dagger_r': [-30, 30, -30], 'dagger_l': [-30, -30, 30], 'cloak': [-20, 0, 0]})
    P[51] = ('death_fling', 3, {'root': [-38, 0, 16], 'rootShift': [0, 0.25, 0.1], 'torso': [-10, 0, 8], 'head': [16, -3, -6], 'right_arm': [100, 0, -70],
                                'left_arm': [100, 5, 70], 'right_leg': [-30, 0, -12], 'left_leg': [24, 0, 12], 'dagger_r': [20, 40, -60], 'dagger_l': [20, -40, 60],
                                'cloak': [-40, 0, 0]})
    return P


# ---------------------------------------------------------------- 에르미타 맑은물 술사: upright robed mage, water orb over the left palm
CW_ATTACH = [('robe', 'back', [0, -0.75, 0], [0, 0, 0], 1.0), ('orb', 'lhand', 0.42, [180, 0, 0], 1.0)]
CW_BASE = {'torso': [2, 8, 0], 'head': [-2, -8, 0], 'right_arm': [10, 0, -10], 'left_arm': [62, 20, 14],
           'right_leg': [-4, 0, -3], 'left_leg': [4, 0, 3], 'robe': [0, 0, 0], 'orb': [180, 0, 0], 'size': 1.0, 'ropen': 4}


def _cw():
    P = {}
    for i in range(4):
        a = i * math.pi / 2
        P[i] = ('poise_%d' % i, 12, {'shift': [0, math.sin(a) * .012, 0], 'torso': [2 + math.sin(a), 8, math.cos(a) * .6],
                                     'left_arm': [62 + math.sin(a) * 3, 20, 14], 'robe': [math.sin(a) * 1.5, 0, 0]})
    for i in range(8):
        a = i * math.pi / 4
        s = math.sin(a)
        P[10 + i] = ('glide_%d' % i, 3, {'shift': [0, abs(math.cos(a)) * .02, 0], 'torso': [5, 8 + s * 2, -s], 'head': [-4, -8 - s * 2, 0],
                                         'right_arm': [10 - s * 16, 0, -10], 'right_leg': [s * 24, 0, -2], 'left_leg': [-s * 24, 0, 2],
                                         'robe': [6 + abs(s) * 4, 0, s * 2]})
    # channel: orb raised high over the head, the free hand open toward the allies; sways while the water flows
    for i in range(4):
        a = i * math.pi / 2
        P[60 + i] = ('channel_%d' % i, 6, {'shift': [0, 0.02 + math.sin(a) * .015, 0], 'torso': [-6 + math.sin(a) * 2, 6, math.cos(a) * 2],
                                           'head': [-10, -6, 0], 'left_arm': [168 + math.sin(a) * 4, 10, 16], 'right_arm': [70, -30 + math.cos(a) * 8, -34],
                                           'robe': [-4 + math.sin(a) * 3, 0, math.cos(a) * 2], 'orb': [180 + math.cos(a) * 6, 0, 0]})
    P[70] = ('broken_channel', 3, {'shift': [0, -0.08, 0.08], 'torso': [-16, 18, -10], 'head': [18, -12, 8], 'right_arm': [40, 10, -50], 'left_arm': [120, -10, 40],
                                   'right_leg': [-14, 0, -8], 'left_leg': [12, 0, 8], 'robe': [-10, 0, -6]})
    P[40] = ('hit_recoil', 2, {'shift': [0, -0.06, 0.06], 'torso': [-14, 10, -8], 'head': [14, -10, 5], 'right_arm': [30, 6, -30], 'left_arm': [80, -10, 30],
                               'robe': [-8, 0, -4]})
    P[41] = ('hit_recover', 3, {'shift': [0, -0.03, 0.02], 'torso': [-2, 8, -2]})
    P[50] = ('death_buckle', 2, {'shift': [0, -0.15, 0.06], 'torso': [-26, 10, -18], 'head': [26, -8, -10], 'right_arm': [70, 10, -60], 'left_arm': [70, 10, 60],
                                 'right_leg': [-20, 0, -10], 'left_leg': [22, 0, 10], 'robe': [-20, 0, -10]})
    P[51] = ('death_fling', 3, {'root': [-40, 0, -14], 'rootShift': [0, 0.25, 0.1], 'torso': [-10, 0, -8], 'head': [16, 3, 6], 'right_arm': [110, 0, -70],
                                'left_arm': [110, 5, 70], 'right_leg': [-24, 0, -10], 'left_leg': [20, 0, 10], 'robe': [-30, 0, 0]})
    return P


def humanoid_set(base, table):
    out = {}
    for pid, (name, dur, over) in table.items():
        p = dict(GUARD)
        p.update(base)
        p.update(over)
        out[pid] = (name, dur, p)
    return out


EM = humanoid_set(EM_BASE, _em())
CW = humanoid_set(CW_BASE, _cw())


# ---------------------------------------------------------------- prop rigs (display frame)
# 둥실 버섯: stem (root), cap, glow (bright spots + gills). All three share one origin; FU_H = float height of the stem foot.
FU_S = 1.1
FU_H = 0.82


def _fu_part(lift, tilt=0.0, fwd=0.0, cap=1.0, squash=1.0):
    """Stem foot (model y 0) at height lift; the cap and glow (model y 6..12.5) scale by cap about the cap base, which
    stays on the stem top. tilt (deg) leans the whole fungus forward (+) about the stem pivot."""
    import rig
    S = FU_S
    ty = lift + 0.5 * S
    q = [tilt, 0, 0]
    stem = ([0, ty, fwd], q, [S, S * squash, S])
    dy = (6 / 16 - 0.5) * S * squash * (1 - cap)
    off = rig.rot(rig.q(q), [0, dy, 0])
    capt = ([off[0], ty + off[1], fwd + off[2]], q, [S * cap, S * cap * squash, S * cap])
    return {'stem': stem, 'cap': capt, 'glow': capt}


def _fu():
    P = {}
    for i in range(4):
        a = i * math.pi / 2
        P[i] = ('bob_%d' % i, 12, _fu_part(FU_H + math.sin(a) * 0.07, tilt=math.cos(a) * 3))
    P[20] = ('swell_a', 5, _fu_part(FU_H + 0.05, tilt=-8, cap=1.22, squash=0.94))
    P[21] = ('swell_b', 4, _fu_part(FU_H + 0.08, tilt=-10, cap=1.4, squash=0.9))
    P[24] = ('bump', 2, _fu_part(FU_H - 0.08, tilt=24, fwd=0.32, cap=1.05, squash=1.1))
    P[30] = ('wobble', 4, _fu_part(FU_H, tilt=-6, cap=0.94))
    P[31] = ('settle', 4, _fu_part(FU_H + 0.03, tilt=2))
    P[40] = ('hit', 2, _fu_part(FU_H + 0.04, tilt=-18, fwd=-0.08, cap=0.88, squash=1.08))
    P[50] = ('burst', 2, _fu_part(FU_H + 0.1, tilt=-12, cap=1.5, squash=0.85))
    P[51] = ('puff', 4, _fu_part(FU_H + 0.2, tilt=-30, cap=0.2, squash=0.3))
    return P


FU = _fu()

# 포자 주머니: pod + glow, both pivot on the ground (model y 8 = floor), so a scale never reaches below it.
FP_S = 0.9


def _fp_part(k, glow, squash=1.0):
    S = FP_S
    return {'pod': ([0, 0.01, 0], [0, 0, 0], [S * k, S * k * squash, S * k]), 'glow': ([0, 0.01, 0], [0, 0, 0], [S * glow, S * glow * squash, S * glow])}


FP = {0: ('grow', 4, _fp_part(0.75, 0.6)), 1: ('pulse_in', 5, _fp_part(0.95, 0.8, 0.95)), 2: ('pulse_out', 5, _fp_part(1.08, 1.0, 1.04)),
      3: ('quick_in', 3, _fp_part(1.0, 0.95, 0.92)), 4: ('quick_out', 3, _fp_part(1.16, 1.12, 1.06)),
      50: ('burst', 2, _fp_part(1.45, 1.5, 0.9)), 51: ('wither', 6, _fp_part(0.3, 0.1, 0.6))}

# 모래 전갈 새끼: body (root), tail (pivot at the tail base), mound (pivot on the floor). Burrowed / mound poses shrink the
# scorpion to a speck at floor level instead of sinking it (nothing below the floor).
SB_S = 0.62
SB_TAIL_BASE = (8, 3.0, 14.2)  # body-model pixel where the tail joins (the rear: +Z in the model = behind)


def sb_parts(lift=0.0, pitch=0.0, k=1.0, curl=0.0, strike=0.0, mound=0.0, shake=0.0, yaw=0.0):
    """Display-frame transforms (t, q, s) for the three parts. k = scorpion scale factor, mound = mound scale."""
    import rig
    S = SB_S * k
    qb = rig.q([pitch, yaw, 0])
    # body model y 0 (belly) sits at lift; pivot [8,8,8] -> centre offset (8/16 - .5) = 0 ... belly is model y 0
    tb = [0, lift + 0.5 * S, 0]
    x, y, z = SB_TAIL_BASE
    v = [-(x / 16 - .5) * S, (y / 16 - .5) * S, -(z / 16 - .5) * S]
    tt = rig.add(tb, rig.rot(qb, v))
    qt = rig.mul(qb, rig.q([curl + strike, 0, 0]))
    m = max(mound, 0.001)
    out = {'body': (tb, qb, [S, S, S]), 'tail': (tt, qt, [S, S, S]),
           'mound': ([0, 0.01, 0], rig.q([0, shake, 0]), [m, m * (0.8 + 0.2 * mound), m])}
    return out


def _sb():
    P = {}
    for i in range(4):
        a = i * math.pi / 2
        P[i] = ('skitter_%d' % i, 3, sb_parts(lift=0.02 + abs(math.sin(a)) * 0.03, pitch=math.sin(a) * 3, curl=math.cos(a) * 6, yaw=math.sin(a) * 6))
    P[24] = ('bite', 1, sb_parts(lift=0.06, pitch=12, curl=-10, strike=30))
    P[30] = ('bite_back', 3, sb_parts(lift=0.02, pitch=-4, curl=6))
    P[40] = ('hit', 2, sb_parts(lift=0.05, pitch=-14, curl=14))
    P[80] = ('mound_a', 4, sb_parts(k=0.02, mound=0.75, shake=-8))
    P[81] = ('mound_b', 4, sb_parts(k=0.02, mound=0.95, shake=8))
    P[82] = ('erupt', 1, sb_parts(lift=0.18, pitch=-24, curl=-6, mound=0.6))
    P[85] = ('sink', 4, sb_parts(k=0.15, mound=0.55))
    P[90] = ('burrowed', 2, sb_parts(k=0.02, mound=0.0))
    P[50] = ('death_curl', 2, sb_parts(lift=0.04, pitch=-30, curl=40, k=1.05))
    P[51] = ('death_fling', 3, sb_parts(lift=0.2, pitch=-150, curl=50, k=0.9))
    return P


SB = _sb()
