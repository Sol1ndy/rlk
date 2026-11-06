"""Original keyframes of the chapter-2 swarm rigs (20 ticks/s). Authored like tools/build_swordsman.mjs: -Z forward,
right hand on -X, angles in degrees (x = pitch forward, y = yaw, z = roll). Hand props (katana, yari, sticks) use
rig.humanoid's arm-sense grip angles: [0,0,0] = blade / tip / stick head straight on out of the fist along the
forearm, +x swings it forward like the arm (10-29 grip fix: the raw-model-axis angles held every prop reversed;
the raised-blade / raised-stick tells that had been tuned against that were re-expressed, same look). Read by swarm.py; previewed by the
scratchpad renders. No reference motions copied.

Pose ids (shared meaning across the humanoids so the AI code reads the same):
  0-3 idle breath, 10-17 walk, 20-23 tell, 24-25 strike, 30-32 recovery, 40-41 hit recoil, 50-51 death,
  60-64 / 70 drummer beats / interrupted. Slimes: 0-1 idle wobble, 5 crouch, 6 stretch, 7 squash, 40 hit, 50 burst.
"""
import math

from rig import GUARD

# ---------------------------------------------------------------- 떠돌이 무사 졸개: hunched ronin, katana held low
NS_ATTACH = [('katana', 'rhand', 0.0, [6, 4, -6], 1.0)]
NS_BASE = {'torso': [10, -10, 0], 'head': [-8, 10, 0], 'right_arm': [44, -14, -8], 'left_arm': [18, 0, 14],
           'right_leg': [-9, 0, -4], 'left_leg': [12, 0, 4], 'katana': [6, 4, -6], 'size': 0.95, 'ropen': 22,
           'shift': [0, -0.03, 0]}


def _ns():
    P = {}
    for i in range(4):
        a = i * math.pi / 2
        P[i] = ('breath_%d' % i, 12, {'shift': [0, -0.03 + math.sin(a) * .012, 0], 'torso': [10 + math.sin(a) * 1.5, -10, math.cos(a) * .6],
                                      'head': [-8 - math.sin(a), 10, 0], 'right_arm': [44 + math.sin(a) * 2, -14, -8]})
    for i in range(8):
        a = i * math.pi / 4
        s = math.sin(a)
        P[10 + i] = ('prowl_%d' % i, 3, {'shift': [0, -0.04 + abs(math.cos(a)) * .03, 0], 'torso': [14, -10 + s * 4, -s * 2], 'head': [-12, 10 - s * 4, 0],
                                         'right_arm': [40 - s * 6, -14, -8], 'left_arm': [16 - s * 26, 0, 12], 'right_leg': [s * 32, 0, -2], 'left_leg': [-s * 32, 0, 2]})
    # tell: the whole pack raises blades together (two-stage lift, held high with the glint, then a dip before the cut)
    P[20] = ('draw_back', 3, {'shift': [0, -0.06, 0.02], 'torso': [4, 18, -5], 'head': [-2, -18, 2], 'right_arm': [100, 8, -24], 'left_arm': [36, 6, 18],
                              'right_leg': [-12, 0, -7], 'left_leg': [18, 0, 7], 'katana': [60, 0, -8]})
    P[21] = ('blade_high', 4, {'shift': [0, -0.07, 0.025], 'torso': [-6, 28, -9], 'head': [8, -28, 4], 'right_arm': [150, 14, -30], 'left_arm': [46, -12, 26],
                               'right_leg': [-13, 0, -8], 'left_leg': [21, 0, 8], 'katana': [0, 0, -8]})
    P[22] = ('blade_loaded', 2, {'shift': [0, -0.05, 0.03], 'torso': [-9, 32, -9], 'head': [9, -32, 4], 'right_arm': [160, 12, -30], 'left_arm': [48, -14, 26],
                                 'right_leg': [-13, 0, -7], 'left_leg': [19, 0, 7], 'katana': [-25, 0, -6]})
    P[23] = ('release', 1, {'shift': [0, -0.03, -0.01], 'torso': [-1, 24, -5], 'head': [2, -24, 1], 'right_arm': [146, -2, -23], 'left_arm': [38, -8, 24],
                            'right_leg': [-17, 0, -4], 'left_leg': [19, 0, 4], 'katana': [24, 0, -6]})
    P[24] = ('cut', 2, {'shift': [0, -0.07, -0.06], 'torso': [18, -20, 7], 'head': [-14, 20, -4], 'right_arm': [14, -36, 32], 'left_arm': [14, 15, 23],
                        'right_leg': [22, 0, -5], 'left_leg': [-15, 0, 5], 'katana': [54, 24, -8]})
    P[30] = ('follow_through', 2, {'shift': [0, -0.08, -0.07], 'torso': [21, -30, 10], 'head': [-17, 30, -5], 'right_arm': [-20, -44, 40], 'left_arm': [8, 13, 20],
                                   'right_leg': [22, 0, -5], 'left_leg': [-15, 0, 5], 'katana': [38, 44, -12]})
    P[31] = ('finish_low', 3, {'shift': [0, -0.075, -0.05], 'torso': [15, -22, 7], 'head': [-11, 22, -3], 'right_arm': [-12, -36, 30], 'left_arm': [10, 10, 17],
                               'right_leg': [17, 0, -4], 'left_leg': [-11, 0, 4], 'katana': [36, 40, -10]})
    P[32] = ('recover', 3, {})
    P[40] = ('hit_recoil', 2, {'shift': [0, -0.07, 0.06], 'torso': [-16, 8, -9], 'head': [16, -8, 6], 'right_arm': [30, 6, -28], 'left_arm': [44, -14, 30],
                               'right_leg': [-12, 0, -5], 'left_leg': [16, 0, 5], 'katana': [-10, 4, -6]})
    P[41] = ('hit_recover', 3, {'shift': [0, -0.04, 0.02], 'torso': [-2, -2, -3], 'head': [4, 2, 2], 'right_arm': [40, -8, -16], 'left_arm': [26, -6, 18], 'katana': [4, 4, -6]})
    P[50] = ('death_buckle', 2, {'shift': [0, -0.15, 0.05], 'torso': [-24, 10, -18], 'head': [24, -8, -10], 'right_arm': [70, 10, -60], 'left_arm': [70, 10, 60],
                                 'right_leg': [-26, 0, -14], 'left_leg': [30, 0, 14], 'katana': [-60, 30, -30]})
    P[51] = ('death_fling', 3, {'root': [-38, 0, -18], 'rootShift': [0, 0.25, 0.1], 'torso': [-10, 0, -8], 'head': [16, 3, 6], 'right_arm': [100, 0, -70],
                                'left_arm': [100, 5, 70], 'right_leg': [-30, 0, -12], 'left_leg': [24, 0, 12], 'katana': [-40, 40, -60]})
    return P


# ---------------------------------------------------------------- 반란군 창병: yari levelled forward, sashimono on the back
SP_ATTACH = [('yari', 'rhand', 0.42, [64, 0, 0], 1.0), ('flag', 'back', [0, .30, .3], [-16, 0, 0], 0.82)]
SP_BASE = {'torso': [6, -24, 0], 'head': [-4, 24, 0], 'right_arm': [26, 0, -6], 'left_arm': [62, -30, 16],
           'right_leg': [-8, 0, -4], 'left_leg': [12, 0, 4], 'yari': [64, 0, 0], 'size': 1.0, 'ropen': 6}


def _sp():
    P = {}
    for i in range(4):
        a = i * math.pi / 2
        P[i] = ('kamae_%d' % i, 12, {'shift': [0, math.sin(a) * .012, 0], 'torso': [6 + math.sin(a), -24, math.cos(a) * .5], 'head': [-4 - math.sin(a), 24, 0]})
    for i in range(8):
        a = i * math.pi / 4
        s = math.sin(a)
        P[10 + i] = ('advance_%d' % i, 3, {'shift': [0, abs(math.cos(a)) * .025, 0], 'torso': [9, -24 + s * 2, -s * 1.2], 'head': [-6, 24 - s * 2, 0],
                                            'right_leg': [s * 28, 0, -2], 'left_leg': [-s * 28, 0, 2]})
    # tell 1 s: draw the spear back, crouch, tip forward and glowing
    P[20] = ('draw_spear', 4, {'shift': [0, -0.08, 0.06], 'torso': [14, -40, 0], 'head': [-10, 40, 0], 'right_arm': [10, 10, -10], 'left_arm': [56, -42, 14],
                               'right_leg': [-22, 0, -6], 'left_leg': [26, 0, 6], 'yari': [80, 0, 0]})
    P[21] = ('coiled', 6, {'shift': [0, -0.11, 0.1], 'torso': [18, -46, 0], 'head': [-14, 46, 0], 'right_arm': [2, 14, -10], 'left_arm': [52, -46, 14],
                           'right_leg': [-26, 0, -6], 'left_leg': [30, 0, 6], 'yari': [88, 0, 0]})
    P[24] = ('thrust', 1, {'shift': [0, -0.06, -0.14], 'torso': [22, -8, 0], 'head': [-18, 8, 0], 'right_arm': [80, -6, -4], 'left_arm': [84, -18, 8],
                           'right_leg': [-30, 0, -4], 'left_leg': [38, 0, 4], 'yari': [-10, 0, 0]})
    P[25] = ('lunge_hold', 2, {'shift': [0, -0.08, -0.16], 'torso': [26, -6, 0], 'head': [-22, 6, 0], 'right_arm': [86, -4, -4], 'left_arm': [88, -16, 8],
                               'right_leg': [-34, 0, -4], 'left_leg': [42, 0, 4], 'yari': [-22, 0, 0]})
    P[30] = ('withdraw', 4, {'shift': [0, -0.05, -0.06], 'torso': [14, -18, 0], 'head': [-10, 18, 0], 'right_arm': [44, -2, -6], 'left_arm': [70, -26, 14],
                             'right_leg': [-16, 0, -4], 'left_leg': [20, 0, 4], 'yari': [46, 0, 0]})
    P[31] = ('settle', 4, {})
    P[40] = ('hit_recoil', 2, {'shift': [0, -0.06, 0.07], 'torso': [-14, -16, -6], 'head': [12, 16, 4], 'right_arm': [16, 4, -14], 'left_arm': [50, -20, 24],
                               'right_leg': [-12, 0, -5], 'left_leg': [16, 0, 5], 'yari': [70, 0, 0]})
    P[41] = ('hit_recover', 3, {'shift': [0, -0.03, 0.03], 'torso': [0, -22, -2], 'head': [2, 22, 1]})
    P[50] = ('death_buckle', 2, {'shift': [0, -0.15, 0.05], 'torso': [-22, -10, -16], 'head': [22, 8, -8], 'right_arm': [60, 10, -50], 'left_arm': [70, 10, 50],
                                 'right_leg': [-24, 0, -14], 'left_leg': [30, 0, 14], 'yari': [40, 30, 30]})
    P[51] = ('death_fling', 3, {'root': [-36, 0, 16], 'rootShift': [0, 0.25, 0.1], 'torso': [-10, 0, 8], 'head': [16, -3, -6], 'right_arm': [100, 0, -70],
                                'left_arm': [100, 5, 70], 'right_leg': [-30, 0, -12], 'left_leg': [24, 0, 12], 'yari': [30, 40, 60]})
    return P


# ---------------------------------------------------------------- 오니 북잡이: masked drummer behind a big taiko
DR_ATTACH = [('stick_r', 'rhand', 0.26, [20, 0, 0], 1.0), ('stick_l', 'lhand', 0.26, [20, 0, 0], 1.0), ('taiko', 'root', [0, .86, -.78], [0, 0, 0], 0.9)]
DR_BASE = {'torso': [8, 0, 0], 'head': [-6, 0, 0], 'right_arm': [70, 0, -10], 'left_arm': [70, 0, 10], 'right_leg': [-4, 0, -8], 'left_leg': [4, 0, 8],
           'stick_r': [20, 0, 0], 'stick_l': [20, 0, 0], 'size': 1.08, 'ropen': 0, 'shift': [0, -0.04, 0]}


def _dr():
    P = {}
    up = {'right_arm': [168, 6, -18], 'stick_r': [-8, 0, 0]}
    upl = {'left_arm': [168, -6, 18], 'stick_l': [-8, 0, 0]}
    downr = {'right_arm': [62, 0, -8], 'stick_r': [38, 0, 0]}
    downl = {'left_arm': [62, 0, 8], 'stick_l': [38, 0, 0]}
    for i in range(4):
        a = i * math.pi / 2
        P[i] = ('ready_%d' % i, 12, {'shift': [0, -0.04 + math.sin(a) * .012, 0], 'torso': [8 + math.sin(a), 0, 0], 'right_arm': [96, 0, -12], 'left_arm': [96, 0, 12], 'stick_r': [-36, 0, 0], 'stick_l': [-36, 0, 0]})
    P[60] = ('raise_right', 5, dict(up, torso=[2, -14, 0], head=[-4, 14, 0], left_arm=[84, 0, 12], stick_l=[-24, 0, 0], shift=[0, -0.02, 0]))
    P[61] = ('strike_right', 1, dict(downr, torso=[16, 10, 0], head=[-12, -10, 0], left_arm=[118, 0, 14], stick_l=[-58, 0, 0], shift=[0, -0.08, -0.02]))
    P[62] = ('raise_left', 5, dict(upl, torso=[2, 14, 0], head=[-4, -14, 0], right_arm=[84, 0, -12], stick_r=[-24, 0, 0], shift=[0, -0.02, 0]))
    P[63] = ('strike_left', 1, dict(downl, torso=[16, -10, 0], head=[-12, 10, 0], right_arm=[118, 0, -14], stick_r=[-58, 0, 0], shift=[0, -0.08, -0.02]))
    P[70] = ('stunned', 3, {'shift': [0, -0.1, 0.08], 'torso': [-12, 18, -10], 'head': [18, -12, 8], 'right_arm': [30, 10, -40], 'left_arm': [140, -20, 30],
                            'stick_r': [60, 0, 0], 'stick_l': [-10, 0, 0], 'right_leg': [-14, 0, -10], 'left_leg': [12, 0, 10]})
    P[40] = ('hit_recoil', 2, {'shift': [0, -0.07, 0.06], 'torso': [-14, 8, -8], 'head': [14, -8, 5], 'right_arm': [40, 6, -30], 'left_arm': [50, -10, 30]})
    P[50] = ('death_buckle', 2, {'shift': [0, -0.15, 0.06], 'torso': [-26, 10, -18], 'head': [26, -8, -10], 'right_arm': [70, 10, -60], 'left_arm': [70, 10, 60],
                                 'right_leg': [-26, 0, -14], 'left_leg': [30, 0, 14], 'stick_r': [40, 40, 30], 'stick_l': [40, -40, -30]})
    P[51] = ('death_fling', 3, {'root': [-40, 0, -14], 'rootShift': [0, 0.25, 0.1], 'torso': [-10, 0, -8], 'head': [16, 3, 6], 'right_arm': [110, 0, -70],
                                'left_arm': [110, 5, 70], 'right_leg': [-30, 0, -12], 'left_leg': [24, 0, 12]})
    return P


def humanoid_set(base, table):
    """Complete pose parameters: every pose starts from the mob's base stance."""
    out = {}
    for pid, (name, dur, over) in table.items():
        p = dict(GUARD)
        p.update(base)
        p.update(over)
        out[pid] = (name, dur, p)
    return out


NS = humanoid_set(NS_BASE, _ns())
SP = humanoid_set(SP_BASE, _sp())
DR = humanoid_set(DR_BASE, _dr())


# ---------------------------------------------------------------- slimes: (sx, sy, sz, core scale, core lift) per pose
SLIME = {0: ('wobble_a', 10, (1.0, 1.0, 1.0, 1.0, 0.0)), 1: ('wobble_b', 10, (1.04, 0.95, 1.04, 0.92, -0.02)),
         5: ('crouch', 6, (1.28, 0.62, 1.28, 1.25, -0.04)), 6: ('stretch', 2, (0.84, 1.28, 0.84, 0.9, 0.06)),
         7: ('squash', 2, (1.22, 0.74, 1.22, 1.05, -0.03)), 40: ('hit', 2, (1.14, 0.86, 1.14, 1.2, 0.0)),
         50: ('burst', 2, (1.35, 1.25, 1.35, 1.5, 0.05)), 51: ('pop', 5, (0.05, 0.05, 0.05, 0.05, 0.0))}
