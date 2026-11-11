#!/usr/bin/env python3
"""pat_p2.py: P2's three entries of the rebuilt 홍련 fight (hr_design §2.2, §8.2, §6.1; lane H1): mx (the retreat first when
the player is near), nb, q (the grab is unparriable; landed -> q_air; missed / perfect-dodged -> the reform).
    python3 pat_p2.py <roguelike>      (from a copy of tools/dev/sim outside the datapack)
"""
import sys

import pat_lib as P
from pat_lib import ck, H

DP = sys.argv[1]
api, S = P.load_api(DP)
P.check_key(DP, api, S, 'mx', 2, 8.0, new=True)
P.check_key(DP, api, S, 'nb', 2, 9.0, new=True)
r = P.check_key(DP, api, S, 'q', 2, 10.0, new=True, end=api.Q_AIR_T0 + 90)

# mx: the player nearer than 6 b -> the 12-t retreat first, then the same pattern (the clock is held)
near, far, pre = api.MX_RETREAT
r = P.run_key(DP, api, S, 'mx', 2, 3.0)
ck(f'mx near: the pattern takes {pre} t longer (the retreat)', r['end'] == api.PAT_END['mx'] + pre, r['end'])
ck('mx near: the same hit ticks on the held clock', sorted(h['h'] for h in r['hz']) == [api.ev('mx', 'x'), api.ev('mx', 'dome')],
   sorted(h['h'] for h in r['hz']))
ck('mx near: no flash and no cue during the retreat', not [t for t, c, a in r['kit'] if t <= pre and c in ('snd/a9_star', 'snd/parry_cue')])
ck('mx near: the backstep clip plays', any(c == 'play/backstep' for t, c in r['s'].rigl if t > r['t0'] - 1))

# q: the miss branches
T0 = api.Q_AIR_T0


def q_run(act):
    s, pl = H.setup_h1(DP, seed=5)
    H.fight_sc(s)
    H.test_id(s, 33)
    H.run_h1(s, 2)
    H.facing_setup(s, 10.0)
    n0 = len(s.hzr)
    H.start_pattern(s, S.TID['q'])
    t0 = s.t
    act(s, t0)
    H.until_h1(s, lambda s: (H.hr(s, '#pat') or 0) == 0, 200, each=lambda s: H.heal(s))
    return s, t0, [h['pt'] + h['tell'] for h in s.hzr[n0:]]


s, t0, hz = q_run(lambda s, t0: s.dodge(at=t0 + api.ev('q_grab', 'grab') - 1))
ck('q: a perfect dodge of the grab -> no q_air (one hazard, the end at Q_MISS_END)', (hz, s.t - t0) == ([20], api.Q_MISS_END), (hz, s.t - t0))
ck('q: the perfect dodge was judged (pdg)', [j['pdg'] for j in s.judged if j['t'] == t0 + 20] == [1])
s, t0, hz = q_run(lambda s, t0: s.press(at=t0 + api.ev('q_grab', 'grab') - 1))
ck('q: F does nothing against the grab (unparriable): it lands, q_air follows', len(hz) == 4 and
   [(j['dodged'], j['parT']) for j in s.judged if j['t'] == t0 + 20] == [(0, 0)], (hz, [j for j in s.judged if j['t'] == t0 + 20]))


def walk_out(s, t0):
    s.walk_from = t0 + api.ev('q_grab', 'lock')


s, pl = H.setup_h1(DP, seed=5)
H.fight_sc(s)
H.test_id(s, 33)
H.run_h1(s, 2)
H.facing_setup(s, 10.0)
n0 = len(s.hzr)
H.start_pattern(s, S.TID['q'])
t0 = s.t


ghost = {}


def each(s):
    H.heal(s)
    ghost[s.t - t0] = 'rlk_hr_ghost' in H.body_of(s).tags
    if s.t >= t0 + api.ev('q_grab', 'lock'):
        p = s.player()
        H.place_player(s, p.pos[0] + 0.5, p.pos[2])


H.until_h1(s, lambda s: (H.hr(s, '#pat') or 0) == 0, 200, each=each)
ck('q: she is a ghost (invulnerable) only from the ghost event to the grab',
   [t for t, g in sorted(ghost.items()) if g] == list(range(api.ev('q_grab', 'ghost'), api.ev('q_grab', 'grab'))),
   [t for t, g in sorted(ghost.items()) if g])
ck('q: leaving the disc after the lock -> the grab misses, the reform, the end at Q_MISS_END',
   (len(s.hzr) - n0, s.t - t0) == (1, api.Q_MISS_END), (len(s.hzr) - n0, s.t - t0))
# the landed run: the beam and the dive can be perfect-parried, the pillar not
s, t0, hz = q_run(lambda s, t0: [s.press(at=t0 + T0 + api.ev('q_air', e) - 1) for e in ('beam', 'hit', 'pillar')])
res = {j['t'] - t0 - T0: (j['dodged'], j['parT']) for j in s.judged if j['t'] > t0 + 20}
ck('q_air: F at h - 1 -> the beam and the dive are perfect parries, the pillar lands',
   res == {api.ev('q_air', 'beam'): (1, 3), api.ev('q_air', 'hit'): (1, 3), api.ev('q_air', 'pillar'): (0, 0)}, res)
sys.exit(P.summary('pat_p2'))
