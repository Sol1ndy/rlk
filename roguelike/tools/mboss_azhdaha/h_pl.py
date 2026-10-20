"""Helpers of S2-L (leg.py): the binding numbers of plan.md 5 rows 31 / 32 / 33 and 4.6 (the Hydro / Pyro addon bodies),
as plain Python so leg.py and its suite (S:az/tests_pl/pat_leg.py) compute the same ticks and sizes.

Not re-exported by api.py (s2.md 1 allows the line, but api.py is shared: leg.py imports this module directly).
Clocks: 31 / 32 on the cast clock #azCT = the roar_rear clip tick (s2.md 6), 31's orbit on the bg-L clock #azBgLT
(0 = the spawn tick); addon bodies on the host's played clip clock (E = the host event, the body runs at E - 12).
"""
from . import api as _A

__all__ = ['R_EV', 'ORB', 'MET', 'FIRE', 'GEYSER', 'LUMP', 'BLADE', 'POINT_CODE', 'lump_ticks', 'blade_ticks',
           'geyser_ticks', 'clear_points']

# ------------------------------------------------------------------------------------------------- 31 격류 범람
R_EV = _A.ev('roar_rear', 'roar')                        # 20: R of plan 5 row 32
ORB = dict(
    spawn=_A.ev('roar_rear', 'drop') - 2,               # 60 on #azCT (s2.md 6: drop - 2)
    grow=10,                                            # bg clock 0..9: growing from the sides, harmless
    life=600,                                           # bg clock 600: the fade starts (s2.md 6: 600 t + fade 10)
    fade=10,                                            # bg clock 610: bg_end
    refresh=600,                                        # p/orbs/refresh: the fade moves to now + 600 (full life)
    rings={1: (6.5, -3.5), 2: (10.5, 2.4)},             # ring: (radius b, omega deg/t; + = clockwise from above)
    a0=45.0,                                            # orb k at (body yaw + 45 + 90 k): inner k 0 / 2, outer k 1 / 3
    hr=1.3, band=(0.0, 2.2), high=(2.6, 4.6),           # hz disc r, the normal band (not jumpable), the ridden band
    eye_half=30.0, eye_r=11.0,                          # the head-lane eye: front +-30 deg about the facing, < 11 b
    safe_pad=3.2 + 1.3 + 0.3,                           # 42 safe circle r 3.2 + orb r + 0.3: ride high over a circle
    y_lo=1.1, y_hi=3.6,                                 # prop centre heights (2.6 b sphere) for the two bands
    rib=2,                                              # p/orb_ribbon every 2 t
    loop=20,                                            # orb_loop sound every 20 t
)

# ------------------------------------------------------------------------------------------------- 32 운석 낙하
MET = dict(
    seal=R_EV + 7,                                      # 27: seal8 decal + the big hazard under lockp (locked)
    big=R_EV + 35,                                      # 55: the big impact (tell 28)
    big_r=5.2, big_fall=6, big_h=12.0,                  # disc r; the meteor falls in the last 6 t from 12 b
    big_field=(4.5, 200),                               # fire field r / life
    small=[R_EV + 44 + 6 * k for k in range(6)],        # 64 70 76 82 88 94
    small_r=2.8, small_tell=12, small_field=(2.8, 160),
    small_lead=10,                                      # lockv lead (even k); odd k: random 6-14 b from the anchor
    small_rnd=(6, 14),
    halo_h=3.0,                                         # the air halo h over the landing spot
    prop_h=16.0, prop_mid=6.0, prop_fall=4,             # small prop: 16 b up at hit - 12, 6 b at hit - 4, preset fall
)
MET['end'] = MET['small'][-1]                           # 94 = R + 74: g.cast_end() after the last field

# ------------------------------------------------------------------------------------------------- 33 화염 잠식 / fields
FIRE = dict(rule_r=4.5, rule_life=160, extend_r=4.0, amb=10, snd=20)

# ------------------------------------------------------------------------------------------------- addon bodies (4.6)
GEYSER = dict(r=3.0, side=(5.0, 7.0), hit=10, tell=22)  # hit E + 10, decal + hazard from the call (E - 12)
# I2 (perf probe, plan 8.1 <= 3000 commands / tick): lump i lands `stagger` x i ticks after lump 0 (its hazard's tell is
# its own flight), so the three fireballs + fire fields of a volley never run in one tick.
LUMP = dict(r=2.2, flight=26, field=(4.0, 160), lead=8, rnd=(7, 14), apex=5.0, stagger=1,
            launch={'chin/impact': 8, 'jump/wave2': 0, 'stomp/w3': 2, 'stomp3/s3': 2})
BLADE = dict(n=8, r0=2.0, spd=2.0, life=6, hr=1.6, up=0.9, launch=4,
             points=('jump/land', 'stomp/w1', 'stomp3/s1'))
POINT_CODE = {'chin/impact': 'c', 'jump/wave2': 'w', 'stomp/w3': 's', 'stomp3/s3': 't',
              'jump/land': 'j', 'stomp/w1': 'k', 'stomp3/s1': 'u'}


def lump_ticks(point):
    """(call, launch, land) on the host clock for a Pyro lump point."""
    d = _A.ADDON_POINTS[point]
    launch = d['E'] + LUMP['launch'][point]
    return d['call'], launch, launch + LUMP['flight']


def blade_ticks(point):
    """(call, launch, last tick in flight) for a Hydro blade point."""
    d = _A.ADDON_POINTS[point]
    launch = d['E'] + BLADE['launch']
    return d['call'], launch, launch + BLADE['life']


def geyser_ticks():
    d = _A.ADDON_POINTS['chin/impact']
    return d['call'], d['E'] + GEYSER['hit']


def clear_points():
    """The two clear melee points (local s, f of the anchor frame): the head-front point and the tail-lane point."""
    return [(_A.P_HEAD_FRONT[0], _A.P_HEAD_FRONT[2]), (_A.P_TAIL_LANE[0], _A.P_TAIL_LANE[2])]


assert ORB['spawn'] == 60 and MET['seal'] == 27 and MET['big'] == 55 and MET['end'] == 94
assert MET['big'] - MET['seal'] == 28                    # plan 5 32: tell 28
assert geyser_ticks()[1] - geyser_ticks()[0] == GEYSER['tell']
