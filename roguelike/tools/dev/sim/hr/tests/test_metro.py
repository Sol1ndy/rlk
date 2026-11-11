#!/usr/bin/env python3
"""test_metro.py: review H-A HA-03 (lead ruling) — no blind F metronome clears a gauntlet.

The rebuilt gauntlets G1 (a8) / G2 (a13) are cleared by 5 perfect parries of their cuts, read off the cue at each lock. A
player who presses F at a fixed period k from some start, without looking, must not get there: for every period
k = 8..30 t and every start (phase and offset: the train starts at any tick from 120 t before the gauntlet to its last
cut, fresh F state), at most 3 perfect parries in G1 (the ruling) and in G2 at most 3 but for at most two periods where a
few starts reach 4 (lane HFA's deviation: with 11 cuts, gaps >= 14 and the moves' spacing no strike set was found that keeps
every period at 3; tools/dev/plan/combat/hfa_progress.md) — never the 5 a clear needs, at any period 2-40. The presses go through the REAL F functions
(player/f_key -> player/def/press | press_re, the judge player/def/judge -> judge2 -> par3 / par2 / par1 -> par_use; the
whiff streak, the lock ladder and the refusal window exactly as shipped), the strikes at the gauntlet's own strike ticks
(read from a real gauntlet run in the H1 world, = api.SCRIPTS). Sections:
  world   one run of each gauntlet in the H1 world (no F): the judged strike ticks = the script's (the train's input)
  train   every period 8..30 and every start: the best train per period (the table), <= 3 perfect parries; mashers (2..7 t)
          and slow beats (31..40 t) never reach the 5 a clear needs
  real    the best train of every period, played in the real gauntlet (F through player/f_key before each world tick):
          the segments it takes = the train's perfect parries, and the gauge is not 0 at the judge (no repel)
    python3 test_metro.py <roguelike> [section ...]      (from a copy of tools/dev/sim outside the datapack; ~4 min)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
import pat_lib as P  # noqa: E402
from pat_lib import ck, H  # noqa: E402
from mcsim import Ctx  # noqa: E402

DP = sys.argv[1]
ONLY = set(sys.argv[2:])
api, S = P.load_api(DP)
SEG, MAXG = api.GAUGE['seg'], api.GAUGE['max']
TEST = {'a8': 21, 'a13': 27}
KS = range(8, 31)
LEAD = 120                   # a train may start this long before the gauntlet (its whiffs build the lock ladder first)
MAX_PP = 3
G2_OVER = {'periods': 2, 'starts': 30}     # G2: periods 8-30 allowed to reach 4 (and their starts in all), never 5
STUB = ('rlk:player/def/guard', 'rlk:items/hook/on_parry_press', 'rlk:items/hook/on_parry', 'rlk:items/hook/on_pdodge',
        'rlk:char/motion/finish', 'rlk:char/cd_cut', 'rlk:player/def/fx/p1', 'rlk:player/def/fx/p2', 'rlk:player/def/fx/p3',
        'rlk:player/def/fx/pd', 'rlk:items/proc/hw_ctr_q', 'rlk:player/def/pd_go', 'rlk:player/def/dg_refund')


def run(name):
    return not ONLY or name in ONLY


def strikes_of(g):
    return [c[2] for _t, _s, _cl, c in api.SCRIPTS[g] if c]


# ================================================================================================== world
STRIKES = {}
for g in api.GAUNTLETS:
    if not run('world') and not run('train') and not run('real'):
        break
    s, pl = H.setup_h1(DP, seed=9)
    assert H.fight_sc(s)
    H.facing_setup(s, 6.0)
    H.test_id(s, TEST[g])
    t0 = s.t
    j0 = len(s.judged)
    while s.t < t0 + api.JUDGE_T[g] - 1:
        H.heal(s)
        H.world_h1(s)
    got = sorted(j['t'] - t0 for j in s.judged[j0:])
    STRIKES[g] = got
    ck(f'world {g}: the judged strikes of a standing player = the script ({len(got)} cuts)', got == strikes_of(g), (got, strikes_of(g)))


# ================================================================================================== the train harness
class Train:
    """The player's F state in a bare H1 world: press(t) runs player/f_key with #now cb = t (the input pre-pass of tick t),
    strike(t) the judge of a parryable boss hit at gametime t (a cut: #hcNP 0, #hcND 0, boss class)."""

    def __init__(self):
        self.s, self.pl = H.setup_h1(DP, seed=9)
        for f in STUB:
            self.s.cache[f] = []
        self.pid = ('e', self.pl.id)
        self.ctx = Ctx(self.pl, tuple(self.pl.pos), tuple(self.pl.rot))

    def reset(self):
        s = self.s
        s.call('rlk:player/def/reset', self.ctx)
        for o in ('vMap', 'pkMode', 'dead', 'buT', 'rnDie', 'rdCam', 'pmMoveLock', 'pmActive', 'dashInvT'):
            s.setsc(self.pid, o, 0)

    def press(self, t):
        s = self.s
        s.t = t
        s.setsc('#now', 'cb', t)
        a0 = s.sc(self.pid, 'parAt')
        s.call('rlk:player/f_key', self.ctx)
        return s.sc(self.pid, 'parAt') == t and a0 != t

    def strike(self, t):
        s = self.s
        s.t = t
        for k, v in (('#hcNP', 0), ('#hcND', 0), ('#hcC', 2), ('#hcK', 3), ('#dodged', 0)):
            s.setsc(k, 'tmp', v)
        s.call('rlk:player/def/judge', self.ctx)
        return s.sc('#parT', 'tmp') or 0

    def train(self, strikes, k, t0):
        """presses at t0, t0 + k, ... up to the last strike (a press before a strike in the same tick); returns
        (perfect parries, the tiers per strike, the accepted presses)"""
        self.reset()
        ev = sorted([(t, 0) for t in range(t0, strikes[-1] + 1, k)] + [(t, 1) for t in strikes])
        tiers, acc = [], []
        for t, kind in ev:
            if kind == 0:
                if self.press(t):
                    acc.append(t)
            else:
                tiers.append(self.strike(t))
        return sum(1 for x in tiers if x == 3), tiers, acc


BEST = {}
N4 = {}
if run('train') or run('real'):
    TR = Train()
    # the harness itself: an F one tick before a strike is a perfect parry, three ticks before a tier 2, a held key is
    # accepted once, a whiff locks the next 12 t
    st = STRIKES.get('a8') or strikes_of('a8')
    TR.reset()
    ok1 = TR.press(st[0] - 1) and TR.strike(st[0]) == 3
    TR.reset()
    ok2 = TR.press(st[0] - 3) and TR.strike(st[0]) == 2
    TR.reset()
    ok3 = TR.press(100) and not TR.press(101) and not TR.press(104) and not TR.press(110) and TR.press(116)
    ck('train: the real F functions (h - 1 perfect, h - 3 tier 2, the 3-t refusal after an ignored press, the 12-t lock)',
       ok1 and ok2 and ok3, (ok1, ok2, ok3))
    for g in api.GAUNTLETS:
        st = STRIKES.get(g) or strikes_of(g)
        table = {}
        N4[g] = {}
        for k in list(range(2, 8)) + list(KS) + list(range(31, 41)):
            best = (-1, None, None)
            n4 = 0
            for t0 in range(-LEAD, st[-1] + 1):
                pp, tiers, acc = TR.train(st, k, t0)
                n4 += pp > MAX_PP
                if pp > best[0]:
                    best = (pp, t0, tiers)
            table[k] = best
            N4[g][k] = n4
        BEST[g] = table
        row = ' '.join(f'{k}:{table[k][0]}' for k in KS)
        print(f'metronome {g} (best perfect parries per period {KS.start}-{KS.stop - 1} t, any start): {row}', flush=True)
        print(f'  mashers 2-7 t: {" ".join(f"{k}:{table[k][0]}" for k in range(2, 8))}; slow 31-40 t: '
              f'{" ".join(f"{k}:{table[k][0]}" for k in range(31, 41))}', flush=True)
        worst = max(table[k][0] for k in KS)
        if g == 'a8':
            ck(f'train {g}: no metronome of period {KS.start}-{KS.stop - 1} t (any start) gets more than {MAX_PP} perfect parries '
               f'(worst {worst})', worst <= MAX_PP, {k: table[k][:2] for k in KS if table[k][0] > MAX_PP})
        else:
            over = {k: N4[g][k] for k in KS if table[k][0] > MAX_PP}
            ck(f'train {g}: no metronome of period {KS.start}-{KS.stop - 1} t (any start) gets more than {MAX_PP + 1} perfect '
               f'parries, more than {MAX_PP} only at {len(over)} period(s) <= {G2_OVER["periods"]} and {sum(over.values())} start(s) '
               f'<= {G2_OVER["starts"]} ({over})', worst <= MAX_PP + 1 and len(over) <= G2_OVER['periods']
               and sum(over.values()) <= G2_OVER['starts'], {k: table[k][:2] for k in KS if table[k][0] > MAX_PP})
        ck(f'train {g}: mashers (2-7 t) and slow beats (31-40 t) never reach the {api.PIPS} a clear needs',
           all(table[k][0] < api.PIPS for k in list(range(2, 8)) + list(range(31, 41))),
           {k: table[k][:2] for k in list(range(2, 8)) + list(range(31, 41)) if table[k][0] >= api.PIPS})
        # the cue-reader still clears: F at h - 1 for every cut
        pp_all = 0
        TR.reset()
        for h in st:
            TR.press(h - 1)
            pp_all += TR.strike(h) == 3
        ck(f'train {g}: F one tick before every cut (the cue-reader) parries all {len(st)} perfectly', pp_all == len(st), pp_all)


# ================================================================================================== real gauntlets
if run('real'):
    for g in api.GAUNTLETS:
        table = BEST[g]
        picks = sorted({k for k in KS if table[k][0] == max(table[kk][0] for kk in KS)} | {14, 15, 16})
        for k in picks:
            pp, t0r, _tiers = table[k]
            s, pl = H.setup_h1(DP, seed=9)
            assert H.fight_sc(s)
            s.revive = 40
            H.facing_setup(s, 6.0)
            pid = ('e', pl.id)
            for o in ('vMap', 'pkMode', 'dead', 'buT', 'rnDie', 'rdCam', 'pmMoveLock', 'pmActive'):
                s.setsc(pid, o, 0)
            for f in STUB[:5]:
                s.cache[f] = []
            ctx = Ctx(pl, tuple(pl.pos), tuple(pl.rot))
            rel = set(range(t0r, api.JUDGE_T[g], k))
            n_pre = max(0, -t0r)
            H.hold(s, True)                          # before the gauntlet: she stands (the train's first presses whiff)
            t0 = s.t + n_pre + 1                 # the first pre-tick's press is at T0 - n_pre

            def tick():
                H.heal(s)
                if s.t + 1 - t0 in rel:              # the input pre-pass of the next tick: #now = its gametime
                    s.setsc('#now', 'cb', s.t + 1)
                    s.call('rlk:player/f_key', ctx)
                H.world_h1(s)
            while s.t < t0:
                tick()
            H.hold(s, False)
            H.test_id(s, TEST[g])
            while s.t < t0 + api.JUDGE_T[g] - 1:
                tick()
            gau_before_judge = H.hr(s, '#gau')
            taken = (MAXG - gau_before_judge) // SEG
            H.heal(s)
            H.world_h1(s)
            ck(f'real {g}: a {k}-t metronome from T{t0r:+d} takes {taken} segment(s) = the train\'s {pp} perfect parries '
               f'(at most {api.PIPS}), {"no repel" if pp < api.PIPS else "the repel"}',
               taken == min(pp, api.PIPS) and (H.hr(s, '#sqn') == S.SEQ_ID['repel']) == (pp >= api.PIPS), (taken, pp, H.hr(s, '#sqn')))
sys.exit(P.summary('test_metro'))
