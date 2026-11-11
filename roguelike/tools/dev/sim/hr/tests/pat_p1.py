#!/usr/bin/env python3
"""pat_p1.py: the P1 kit of the rebuilt 홍련 fight (hr_design §2.1-2.2, §6.1; lane H1): a1 a2 a3 a3s a4 a6 a9 a10 d4 tri
rings ult hcut blue kcut, in P1 and in P2 (rings: four rings in P1, five in P2). The checks are pat_lib.check_key's; plus:
a6 has no hazard and says line 12; ult spends the gauge at its second cut; rings chains into ult only at a full gauge.
    python3 pat_p1.py <roguelike>      (from a copy of tools/dev/sim outside the datapack)
"""
import sys

import pat_lib as P
from pat_lib import ck, H

DP = sys.argv[1]
api, S = P.load_api(DP)
NEW = set(api.NEW_FIGHT_CLIPS)
DIST = {'a1': 3.0, 'a2': 3.0, 'a3': 3.0, 'a3s': 3.0, 'a4': 9.0, 'a9': 4.0, 'a10': 6.0, 'd4': 2.6, 'tri': 8.0, 'rings': 2.4,
        'ult': 2.4, 'hcut': 14.0, 'blue': 5.0, 'kcut': 5.0}
for ph in (1, 2):
    for key in api.P1:
        if key == 'a6':
            continue
        end = None
        if key == 'rings':
            end = api.RINGS_END[ph]
        P.check_key(DP, api, S, key, ph, DIST[key], end=end, new=key in NEW)

# a6: no hazard, the line, the end
r = P.run_key(DP, api, S, 'a6', 1, 3.0)
ck('a6: no hazard', not r['hz'], r['hz'])
ck('a6: line 12 at its tick', [(t, a.get('id')) for t, c, a in r['kit'] if c == 'hud/line'] == [(api.A6_TRIGGER['line_t'], 12)],
   [(t, c) for t, c, a in r['kit'] if c == 'hud/line'])
ck('a6: ends at its `next` tick', r['end'] == api.A6_TRIGGER['next'], r['end'])

# ult: only after rings at a full gauge; the gauge is spent at the second cut; both cuts hit a standing player
s, pl = H.setup_h1(DP, seed=3)
H.fight_sc(s)
H.facing_setup(s, 2.4)
H.test_id(s, 12)
H.hold(s)
ck('test 12: the gauge is full and rings runs with ult to follow', (H.hr(s, '#gau'), H.hr(s, '#pat'), H.hr(s, '#ultq')) ==
   (api.GAUGE['max'], S.TID['rings'], 1), (H.hr(s, '#gau'), H.hr(s, '#pat'), H.hr(s, '#ultq')))
t0 = s.t
H.until_h1(s, lambda s: H.hr(s, '#pat') == S.TID['ult'], 100, each=lambda s: H.heal(s))
ck(f'rings -> ult {api.ULT_AFTER} t after the last ring (P1: tick {api.ev("rings", "r4") + api.ULT_AFTER})',
   s.t - t0 == api.ev('rings', 'r4') + api.ULT_AFTER, s.t - t0)
tu = s.t
g = []
H.until_h1(s, lambda s: H.hr(s, '#pat') != S.TID['ult'], 100, each=lambda s: (H.heal(s), g.append(H.hr(s, '#gau'))))
c2 = api.ev('ult', 'cut2')
ck('ult: the gauge is full until the second cut and 0 from it on', g[c2 - 1] == api.GAUGE['max'] and g[c2] == 0, g[c2 - 2:c2 + 2])
ju = [j['t'] - tu for j in s.judged if j['t'] > tu]
ck('ult: both whole-arena cuts hit a standing player', ju == [api.ev('ult', 'cut1'), c2], ju)
ck('ult: both hits were unparriable (the judge saw #hcNP 1)', all(j['np'] == 1 for j in s.judged if j['t'] > tu))
# rings without a full gauge does not chain
s, pl = H.setup_h1(DP, seed=3)
H.fight_sc(s)
H.facing_setup(s, 2.4)
H.start_pattern(s, S.TID['rings'])
seen = set()
H.until_h1(s, lambda s: (H.hr(s, '#pat') or 0) == 0, 120, each=lambda s: (H.heal(s), seen.add(H.hr(s, '#pat'))))
ck('rings below a full gauge: no ult follows', S.TID['ult'] not in seen and (H.hr(s, '#ultq') or 0) == 0, seen)
sys.exit(P.summary('pat_p1'))
