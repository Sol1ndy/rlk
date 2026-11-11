#!/usr/bin/env python3
"""test_input_hr.py: the player's inputs in the H1 world (lib/hrsim.py world_h1; lane HB, review H-A) against the rules of
README 3 「패링 · 닷지」 / 2 「닷지」 written out here as a reference model, on press and dodge sequences. hrsim drives the REAL
player/f_key (player/def/press / press_re, the judge's par_use) and the REAL dashCool; the reference reads every constant
from the loaded pack (load.mcfunction):
  F  accepted unless now < parLk or now < #parMl; accepted: parLk = now + #parGap (round W: the whiff ladder is gone, the
     user's ruling). Refused: #parMl = now + #parRe. A parry (the judge, any tier): parHit = parLk - #parChain = now.
  dodge  accepted when dashCool is 0: dashCool = #dashCoolT; a dodge that avoided a hit gets #dashCoolT - #dashCoolHitT
     back once; - 1 per tick. Round W: a press inside the cooldown 1..#dgChW t after the set's first dodge is the double
     dodge's second move (dashCool + #dashCoolT), once per set.
    python3 test_input_hr.py <roguelike>      (from a copy of tools/dev/sim outside the datapack)
"""
import sys

import pat_lib as P
from pat_lib import ck, H

DP = sys.argv[1]
api, S = P.load_api(DP)


class Ref:
    """The rules as README 3 states them (no Minecraft code)."""

    def __init__(self, s):
        g = lambda k: s.sc(k, 'tmp')    # noqa: E731
        self.gap, self.re, self.chain = g('#parGap'), g('#parRe'), g('#parChain')
        self.cd, self.cd_hit, self.chw = g('#dashCoolT'), g('#dashCoolHitT'), g('#dgChW')
        self.par_at = self.par_lk = self.par_hit = self.ml = -10 ** 6
        self.ws = 0
        self.d_ready = -10 ** 6
        self.d_set = None

    def press(self, t):
        if t < self.par_lk or t < self.ml:
            self.ml = t + self.re
            return False
        self.par_at, self.par_lk = t, t + self.gap
        return True

    def parry(self, t, tier):
        self.par_hit, self.par_lk = t, t + self.chain

    def dodge(self, t):
        if t < self.d_ready:
            if self.d_set is not None and 1 <= t - self.d_set <= self.chw:
                self.d_ready += self.cd          # the double dodge
                self.d_set = None
                return True
            return False
        self.d_ready = t + self.cd
        self.d_set = t
        return True

    def avoided(self):
        self.d_ready -= self.cd - self.cd_hit


def fresh():
    s, pl = H.setup_h1(DP, seed=5)
    assert H.fight_sc(s)
    H.hold(s, True)
    H.facing_setup(s, 30.0)
    return s


def presses(rel, key=None, dist=3.0, n=None):
    """F at t0 + each of rel (ticks, >= 1: t0 is the tick already run); with key, that pattern runs in reach first (the hold keeps it the only one). Returns
    (sim accepted list, reference accepted list, the judged parries, s)."""
    s = fresh()
    if key:
        H.facing_setup(s, dist)
        H.start_pattern(s, S.TID[key])
    t0 = s.t
    for r in rel:
        s.press(at=t0 + r)
    ref = Ref(s)
    H.run_h1(s, (n or max(rel) + 3), each=lambda s: H.heal(s))
    par = sorted((j['t'], j['parT']) for j in s.judged if j['t'] > t0 and j['parT'])
    want, pi = [], 0
    for r in rel:
        t = t0 + r
        while pi < len(par) and par[pi][0] < t:          # parries of earlier ticks
            ref.parry(*par[pi])
            pi += 1
        want.append(ref.press(t))
        while pi < len(par) and par[pi][0] == t:         # a parry in the press's own tick comes after the input pre-pass
            ref.parry(*par[pi])
            pi += 1
    got = [ok for _t, ok in s.f_log]
    return got, want, par, s


def same(name, rel, **kw):
    got, want, par, s = presses(rel, **kw)
    ck(f'{name}: accepted presses = the rules ({sum(want)} of {len(want)})', got == want, (got, want, par))
    return got, par, s


# whiffs only (no attack in reach)
got, _p, s = same('whiffs 20 t apart (the streak: 12 -> 24 -> 36 -> 48 t)', [1 + 20 * i for i in range(8)])
ck('... and the streak reaches the cap: refused presses 3, 5, 7, 8', got == [True, True, False, True, False, True, False, False], got)
same('whiffs 70 t apart (no ladder: 12 t each)', [1, 71, 141, 211, 281])
same('whiffs 13 t apart (no ladder: every one taken)', [1, 14, 27, 40, 53])
same('a held key (every 4 t)', list(range(1, 81, 4)))
same('mashing every 2 t', list(range(1, 61, 2)))
same('every 3 t', list(range(1, 61, 3)))
same('every 13 t', list(range(1, 131, 13)))
same('irregular', [1, 6, 12, 15, 31, 32, 34, 51, 65, 66, 91, 131, 132, 201])
# parries: a3's five hits (14 / 30 / 45 / 57 / 69 on its clock), the player in reach
hs = [api.ev('a3', e) for e in ('h1', 'h2', 'h3', 'h4', 'h5')]
got, par, s = same('a3, F at h - 1 for every hit (perfect, the chain lock)', [h - 1 for h in hs], key='a3', n=hs[-1] + 12)
ck('... five perfect parries', [p[1] for p in par] == [3] * 5, par)
got, par, s = same('a3, F at h - 7 (tier 1: the streak stays)', [h - 7 for h in hs], key='a3', n=hs[-1] + 12)
ck('... tier-1 parries', all(p[1] == 1 for p in par) and par, par)
same('a3, mixed timings and extra presses', [hs[0] - 3, hs[0] + 2, hs[1] - 1, hs[1] + 1, hs[2] - 12, hs[3] - 2, hs[3], hs[4] - 5],
     key='a3', n=hs[-1] + 12)
same('a3, a whiff before the chain, then h - 1', [1, hs[0] - 1, hs[1] - 1, hs[2] - 1], key='a3', n=hs[-1] + 12)
# the dodge: no hit (18 t), a perfect dodge of a10 (12 t)
s = fresh()
ref = Ref(s)
t0 = s.t
for r in range(1, 101, 5):
    s.dodge(at=t0 + r)
H.run_h1(s, 102)
want = [ref.dodge(t0 + r) for r in range(1, 101, 5)]
ck(f'dodges every 5 t, nothing to avoid: a set (the step + the double dodge 5 t later) per 2 x #dashCoolT ({ref.cd} t)',
   [ok for _t, ok in s.d_log] == want and want[:3] == [True, True, False], (s.d_log, want))
s = fresh()
H.facing_setup(s, 6.0)
H.start_pattern(s, S.TID['a10'])
t0 = s.t
h = api.ev('a10', 'hit')
rel = [h - 1, h - 1 + 4, h - 1 + 8, h - 1 + 12, h - 1 + 16, h - 1 + 20]
for r in rel:
    s.dodge(at=t0 + r)
H.run_h1(s, h + 30, each=lambda s: H.heal(s))
ref = Ref(s)
want = []
for r in rel:
    want.append(ref.dodge(t0 + r))
    if r == h - 1:
        ref.avoided()
pd = [j for j in s.judged if j['t'] > t0 and j['pdg']]
ck(f'a10 perfect-dodged (h - 1), then dodges every 4 t: the next one {ref.cd_hit} t later', len(pd) == 1 and [ok for _t, ok in s.d_log] == want,
   (pd, s.d_log, want))
sys.exit(P.summary('test_input_hr'))
