#!/usr/bin/env python3
"""test_gauge.py: the 5-segment gauge of the rebuilt 홍련 fight outside the gauntlets (hr_design §1.2, §6.1; lane H1):
+3 when a pattern ends (not A6, not U), +5 per hit of hers that lands (a tier 1 / 2 parry lands; a perfect parry and a
perfect dodge do not), the cap 50, no charge while groggy / in a lead-in / gauntlet / cutscene, a full gauge forces rings
-> ult in the near band (HA-09: from the mid band she glides in first, then the rings reach; not from far), 0 after ult's
second cut, full at lead60's tick 0 and at the refill beats of lead5 / lead_re, the under bar = #gau / 10 of 5; HA-01: a
floor reached during the forced rings ends the chain (no ult), the step (CS1 / lead5) starts at the next decision.
    python3 test_gauge.py <roguelike>      (from a copy of tools/dev/sim outside the datapack)
"""
import sys

import pat_lib as P
from pat_lib import ck, H

DP = sys.argv[1]
api, S = P.load_api(DP)
G = api.GAUGE
g = lambda s: H.hr(s, '#gau') or 0     # noqa: E731


def fresh(seed=4, p2=False):
    s, pl = H.setup_h1(DP, seed=seed)
    assert H.fight_sc(s)
    if p2:
        H.test_id(s, 33)
        H.run_h1(s, 2)
    return s


def one(key, dist, act=None, p2=False):
    """Pattern key once (the hold on) against a player healed every tick; returns (s, the gauge before / after, t0)."""
    s = fresh(p2=p2)
    H.facing_setup(s, dist)
    H.start_pattern(s, S.TID[key])
    t0, g0 = s.t, g(s)
    if act:
        act(s, t0)
    H.until_h1(s, lambda s: (H.hr(s, '#pat') or 0) == 0, 200, each=lambda s: H.heal(s))
    H.run_h1(s, 2)
    return s, g0, g(s), t0


s, g0, g1, t0 = one('a1', 30.0)
ck(f'a pattern that hits nothing: + {G["pat"]} at its end', g1 - g0 == G['pat'], (g0, g1))
s, g0, g1, t0 = one('a1', 3.0)
ck(f'a landed hit: + {G["hit"]} (and + {G["pat"]} at the end)', g1 - g0 == G['pat'] + G['hit'], (g0, g1))
h = api.ev('a1', 'hit')
s, g0, g1, t0 = one('a1', 3.0, lambda s, t0: s.press(at=t0 + h - 4))
ck('a tier-2 parry is a landed hit: + 5', g1 - g0 == G['pat'] + G['hit'] and [j['parT'] for j in s.judged if j['t'] > t0] == [2],
   (g0, g1, [j['parT'] for j in s.judged if j['t'] > t0]))
s, g0, g1, t0 = one('a1', 3.0, lambda s, t0: s.press(at=t0 + h - 1))
ck('a perfect parry is not a landed hit: only the pattern\'s + 3', g1 - g0 == G['pat'], (g0, g1))
s, g0, g1, t0 = one('a10', 6.0, lambda s, t0: s.dodge(at=t0 + api.ev('a10', 'hit') - 1))
ck('a perfect dodge is not a landed hit: only the pattern\'s + 3', g1 - g0 == G['pat'] and [j['pdg'] for j in s.judged if j['t'] > t0] == [1],
   (g0, g1))
s, g0, g1, t0 = one('a3', 3.0)
ck('a3 against a standing player: 5 hits + the pattern', g1 - g0 == G['pat'] + 5 * G['hit'], (g0, g1))
s, g0, g1, t0 = one('a6', 3.0)
ck('A6 gives nothing', g1 == g0, (g0, g1))
# the cap
s = fresh()
s.setsc('#gau', 'hr', G['max'] - 2)
H.facing_setup(s, 3.0)
H.start_pattern(s, S.TID['a3'])
H.until_h1(s, lambda s: (H.hr(s, '#pat') or 0) == 0, 200, each=lambda s: H.heal(s))
ck(f'the cap is {G["max"]}', g(s) == G['max'], g(s))
ck('the under bar = #gau / 10 of 5 (electro)', (s.sc('#buSub', 'bu'), s.sc('#buSubMax', 'bu'), s.sc('#buSubCol', 'bu')) == (5, 5, api.BU_SHIELD),
   (s.sc('#buSub', 'bu'), s.sc('#buSubMax', 'bu'), s.sc('#buSubCol', 'bu')))
# a full gauge forces rings -> ult at the next near / mid decision
H.hold(s, False)
seen = []
H.until_h1(s, lambda s: len(seen) >= 2 and (H.hr(s, '#pat') or 0) == 0, 400,
           each=lambda s: (H.heal(s), seen.append(H.hr(s, '#pat')) if (H.hr(s, '#pat') or 0) and (not seen or seen[-1] != H.hr(s, '#pat')) else None))
ck('a full gauge: the next near decision is rings, then ult', seen[:2] == [S.TID['rings'], S.TID['ult']], seen)
ck('the gauge is 0 after ult (its + 3 is not given either)', g(s) == 0, g(s))
# from far she closes first: no forced rings while the player is beyond the mid band
s = fresh()
s.setsc('#gau', 'hr', G['max'])
H.facing_setup(s, 16.0)
first = []
H.until_h1(s, lambda s: bool(first), 200, each=lambda s: (H.heal(s), first.append(H.hr(s, '#pat')) if (H.hr(s, '#pat') or 0) else None))
ck('a full gauge with the player far: the first move is not rings (she closes first)', first and first[0] != S.TID['rings'], first)
ck('... and the gauge is still full for the next near / mid decision', g(s) == G['max'], g(s))
# HA-09 (review H-A): a full gauge forces the rings only in the near band; from the mid band she glides in first (ai/ult_close)
# and the rings start near enough to reach a standing player (every ring lands); a player who keeps away does not make it a
# chase (the close ends after its time, the rings start)
NEAR = api.BANDS[0]
for dist in (3.0, 6.0, 8.0, 10.5):
    s = fresh(seed=5)
    s.setsc('#gau', 'hr', G['max'])
    H.facing_setup(s, dist)
    n0, j0 = len(s.hzr), len(s.judged)
    st = {}

    def each(s):
        H.heal(s)
        if H.hr(s, '#pat') == S.TID['rings'] and 'd' not in st:
            b, p = H.body_of(s), s.player()
            st['d'] = ((b.pos[0] - p.pos[0]) ** 2 + (b.pos[2] - p.pos[2]) ** 2) ** 0.5
            st['t'] = s.t
        if 'glide' not in st and H.hr(s, '#ai_mv') == 7:
            st['glide'] = s.t
    H.until_h1(s, lambda s: 't' in st and s.t >= st['t'] + api.RINGS_END[1], 400, each=each)
    rings = sorted({h['pt'] + h['tell'] for h in s.hzr[n0:] if h['pat'] == S.TID['rings']})
    hit = sorted({j['t'] - st['t'] for j in s.judged[j0:] if 't' in st and j['t'] - st['t'] in rings})
    # (from 6 b her recovery walk may already bring her into the near band; from 10.5 b only the glide can)
    ck(f'full gauge, the player {dist} b away: the rings start within the near band ({st.get("d", 0):.1f} b <= {NEAR} b)'
       + ('' if dist <= NEAR else ', after a glide in' if dist > 10 else ''),
       'd' in st and st['d'] <= NEAR + 0.05 and (dist > NEAR or 'glide' not in st) and (dist <= 10 or 'glide' in st), (st, dist))
    ck(f'full gauge, the player {dist} b away: every ring reaches a standing player ({len(hit)} of {len(rings)})',
       len(rings) == 4 and hit == rings, (rings, hit))
s = fresh(seed=5)
s.setsc('#gau', 'hr', G['max'])
H.facing_setup(s, 8.0)
st = {}


def away(s):
    H.heal(s)
    if H.hr(s, '#ai_mv') == 7:
        st.setdefault('glide', s.t)
        b, p = H.body_of(s), s.player()
        dx, dz = p.pos[0] - b.pos[0], p.pos[2] - b.pos[2]
        n = (dx * dx + dz * dz) ** 0.5 or 1
        H.place_player(s, p.pos[0] + 0.32 * dx / n, p.pos[2] + 0.32 * dz / n)   # walks away faster than she glides
    if H.hr(s, '#pat') == S.TID['rings']:
        st.setdefault('rings', s.t)


H.until_h1(s, lambda s: 'rings' in st, 300, each=away)
ck('full gauge, a player who keeps away: the close ends after its time and the rings start (no chase)',
   'glide' in st and 'rings' in st and st['rings'] - st['glide'] <= 42, st)

# HA-01 (review H-A, lead ruling): a floor reached during the forced rings: no ult, the step (CS1 at 60 %, lead5 at 5 %)
for ph, tid, step in ((1, 80, 'cs1'), (2, 34, 'lead')):
    s = fresh(seed=11, p2=(ph == 2))
    H.facing_setup(s, 3.0)
    H.hold(s)
    H.test_id(s, tid)                                  # HP = the floor + 1
    H.test_id(s, 12)                                   # the gauge full: rings now, ult to follow
    H.hold(s, False)
    pats, hit = [], [False]

    def each(s):
        H.heal(s)
        if not hit[0] and H.hr(s, '#pat') == S.TID['rings'] and H.hr(s, '#pt') == 3:
            H.A.strike(s, H.body_of(s), 5000)
            hit[0] = True
        p = H.hr(s, '#pat') or 0
        if p and (not pats or pats[-1] != p):
            pats.append(p)
    ok = H.until_h1(s, lambda s: H.hr(s, '#ph') == api.PH[step], 200, each=each)
    ck(f'P{ph}: the floor reached during the forced rings: the rings end, no ult, then {step} '
       f'({"CS1" if ph == 1 else "lead5"})', hit[0] and ok and pats == [S.TID['rings']] and H.hr(s, '#fl') == 0,
       (hit[0], ok, pats, H.hr(s, '#ph')))

# no charge while groggy
s = fresh()
H.facing_setup(s, 3.0)
H.hold(s)
H.run_h1(s, 3)
g0 = g(s)
H.test_id(s, 19)
H.run_h1(s, 100, each=lambda s: H.heal(s))
ck('no charge while groggy', g(s) == g0 and (H.bal(s, 'grgT') or 0) <= 1, (g0, g(s), H.bal(s, 'grgT')))
# lead60 tick 0 / the refill beats / no charge in cutscenes and gauntlets
s = fresh()
s.setsc('#gau', 'hr', 23)
H.test_id(s, 20)                                    # CS1 -> lead60 -> G1
ck('CS1: the module HUD is off, the gauge is kept', (H.hr(s, '#hud'), g(s)) == (0, 23), (H.hr(s, '#hud'), g(s)))
H.until_h1(s, lambda s: H.hr(s, '#ph') == api.PH['lead60'], api.SEQ_LEN['cs1'] + 5)
ck('lead60 tick 0: the gauge is 5/5, the bars are back', (g(s), H.hr(s, '#hud'), H.hr(s, '#sq') or 0) == (G['max'], 1, 0),
   (g(s), H.hr(s, '#hud'), H.hr(s, '#sq')))
H.until_h1(s, lambda s: H.hr(s, '#ph') == api.PH['a8'], api.SEQ_LEN['lead60'] + 5)
ck(f'G1 starts {api.SEQ_LEN["lead60"]} t later with 5/5', g(s) == G['max'] and H.hr(s, '#pat') == S.TID['a8'], (g(s), H.hr(s, '#pat')))
s = fresh(p2=True)
s.setsc('#gau', 'hr', 17)
H.test_id(s, 26)                                    # lead5 -> G2
rb = api.ev('lead5', 'refill')
H.run_h1(s, rb - 1)
ck('lead5: the gauge keeps its P2 value until the refill beat', g(s) == 17, g(s))
H.run_h1(s, 2)
ck(f'lead5: 5/5 at the refill beat ({rb})', g(s) == G['max'], g(s))
ck('lead5: the warning banner is on from the refill beat (the lethal gauntlet)', [a.get('on') for t, c, a in s.kitl if c == 'hud/warn'][-1:] == [1],
   [a for t, c, a in s.kitl if c == 'hud/warn'][-2:])
s = fresh(p2=True)
H.test_id(s, 27)
H.run_h1(s, 110, each=lambda s: H.heal(s))
pid = ('e', s.player().id)
s.setsc(pid, 'pkMode', 1)
H.run_h1(s, 3)
s.setsc(pid, 'pkMode', 0)
H.run_h1(s, 2)
ck('a paused G2 restarts through lead_re with the gauge empty until its refill beat', (H.hr(s, '#sqn'), g(s)) == (S.SEQ_ID['lead_re'], 0),
   (H.hr(s, '#sqn'), g(s)))
H.run_h1(s, api.ev('lead_re', 'refill') + 1)
ck('lead_re: 5/5 at its refill beat', g(s) == G['max'], g(s))
sys.exit(P.summary('test_gauge'))
