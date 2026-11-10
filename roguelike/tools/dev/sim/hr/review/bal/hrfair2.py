#!/usr/bin/env python3
"""hrfair2.py — hrfair 2.0: the balance probe of the rebuilt 홍련 fight (hr_design §6.4; lane H1). Scratch tool, never shipped.

    python3 hrfair2.py <roguelike> [--out <dir>] [--jobs 4] [--quick] [--only p1,p2,g,kill]
    (run from a copy of tools/dev/sim outside the datapack; results <out>/hrfair2.json + the table on stdout)

World: tests/lib/hrsim.py H1Sim (the REAL player/def judge, mboss framework, bal/**; the F lock and dodge cooldown as ruled
on 11-11, review A-01 / A-12: constants from the loaded pack where they exist). The item-less Lv15 player (268 HP) against
her at L16 (5834 HP); seeds 11 / 22 / 33; 3 600 t per fight phase. The sequences are the core stand-ins until lane H2 lands
(their lengths are the contract's; no cutscene tick is counted as fighting time).

Agents (all but `stand` walk to 2.5 b at 0.216 b/t and hit her every 10 t within 3.5 b with atk x 1.1, a skill hit every
160 t; they know every pattern's hit ticks - the cue / flash gives 7-22 t of notice):
  walker      never presses F or dodges (the old baseline)          stand    never moves or acts
  parrier s   F for every parryable hit, aimed at h - 1 with a normal timing error s (ticks); dodges nothing
  mixed s     parries P hits, perfect-dodges N hits with the same error
  dodger s    a dodge at h - 1 +- s for every hit                   masher   F every 4 t
  sloppy      F at h - 1 +- 6 t (uniform) for every hit
Gauntlet agents stand, or walk 0.22 b/t outward / sideways / inward, and act on every cut.

Targets T1-T13: hr_design §6.4. T1 / T2 divide by 타키's whole-fight melee walker and T3 by the Guardian standing as
RECORDED by hrfair 1.x (review/bal/base_tachy.log: 124.0 and 164.0 %/min): neither boss has a suite in the repository any
more, so "the same tool" cannot be re-run; the old walker also dodged on reaction, this one never does - read T1-T3 as
indicative until both are re-measured with one tool.
"""
import argparse
import json
import math
import random
import sys
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / 'tests' / 'lib'))
sys.path.insert(0, str(HERE.parent.parent / 'tests'))
import hrsim as H  # noqa: E402

TACHY_WALKER, GUARDIAN_STAND = 124.0, 164.0          # %/min, base_tachy.log (hrfair 1.x)
SEEDS = (11, 22, 33)
WALK, REACH, KEEP = 0.216, 3.5, 2.5
ATK_EVERY, SKILL_EVERY = 10, 160
LV_HP = lambda lv: (100 + 30 * (lv - 1) + 5 * (lv - 1) ** 2 // 100) * 400 // 100   # noqa: E731  mob/level_apply %
_API = {}


def api_of(dp):
    if dp not in _API:
        sys.path.insert(0, str(Path(dp).resolve() / 'tools'))
        sys.dont_write_bytecode = True
        from mboss_scarlet import api, s3lib
        _API[dp] = (api, s3lib)
    return _API[dp]


class Agent:
    def __init__(self, s, api, S, kind, sigma, rng, attack=True, move=True):
        self.s, self.api, self.S, self.kind, self.sigma, self.rng = s, api, S, kind, sigma, rng
        self.attack, self.move = attack and kind != 'stand', move and kind != 'stand'
        self.pat, self.t_start, self.q_air = 0, None, False
        self.key_of = {v: k for k, v in S.TID.items()}
        self.hits = {}                # world tick -> 'P' / 'N' of the hits scheduled (the pattern's table)
        self.acted = {}               # world tick of a hit -> ('F' | 'D', the input tick)
        self.gt0 = None

    def err(self):
        if self.kind == 'sloppy':
            return self.rng.randint(-6, 6)
        return int(round(self.rng.gauss(0, self.sigma))) if self.sigma else 0

    def plan(self, h, par):
        """An input for the hit at world tick h."""
        s = self.s
        act = {'walker': None, 'stand': None, 'masher': None, 'parrier': 'F' if par == 'P' else None,
               'mixed': 'F' if par == 'P' else 'D', 'dodger': 'D', 'sloppy': 'F'}[self.kind]
        self.hits[h] = par
        if act is None or h in self.acted:
            return
        t = max(s.t + 1, h - 1 + self.err())
        self.acted[h] = (act, t)
        (s.press if act == 'F' else s.dodge)(at=t)

    def rows(self, key, ph):
        api = self.api
        out = {}
        for i, row in enumerate(api.HITS[key]):
            only = api.HIT_PH.get(key, {}).get(i)
            if only is not None and only != ph:
                continue
            clip = row[0]
            t = api.ev(clip, row[1]) + (api.Q_AIR_T0 if clip == 'q_air' else 0)
            out.setdefault((t, clip == 'q_air'), set()).add(row[6])
        return out

    def watch(self):
        """Before each world tick: a pattern that started -> its hits are planned (a learned pattern: the cue / flash)."""
        s, api = self.s, self.api
        pat, pt = H.hr(s, '#pat') or 0, H.hr(s, '#pt') or 0
        ph = 2 if H.hr(s, '#ph') in (api.PH['p2'],) else 1
        key = self.key_of.get(pat)
        if key in api.GAUNTLETS:
            if self.gt0 != s.t - pt:
                self.gt0 = s.t - pt
                for r in api.SCRIPTS[key]:
                    if r[3]:
                        self.plan(self.gt0 + r[3][2], 'P')
            return
        self.gt0 = None
        if not key or pt < 1:
            self.pat = pat if pt >= 1 else 0
            return
        t_start = s.t - pt
        if pat != self.pat or self.t_start is None or abs(t_start - self.t_start) > 0:
            self.pat, self.t_start, self.q_air = pat, t_start, False
            for (t, air), pars in self.rows(key, ph).items():
                if not air and t > pt:
                    self.plan(t_start + t, 'P' if 'P' in pars else 'N')
        if key == 'q' and not self.q_air and (H.hr(s, '#q_hit') or 0) == 1:
            self.q_air = True
            for (t, air), pars in self.rows(key, ph).items():
                if air:
                    self.plan(t_start + t, 'P' if 'P' in pars else 'N')

    def step(self):
        s = self.s
        self.watch()
        if self.kind == 'masher' and (s.t + 1) % 4 == 0:
            s.press(at=s.t + 1)
        b, pl = H.body_of(s), s.player()
        if b is None:
            return
        dx, dz = b.pos[0] - pl.pos[0], b.pos[2] - pl.pos[2]
        d = math.hypot(dx, dz)
        if self.move and d > KEEP:
            k = min(WALK, d - KEEP) / d
            H.place_player(s, pl.pos[0] + dx * k, pl.pos[2] + dz * k)
        if self.attack and d <= REACH and abs(b.pos[1] - pl.pos[1]) < 2.0 and 'rlk_mb_inv' not in b.tags \
                and (H.mb(s, '#mbSt') or 0) == 1 and not (s.sc('#mbCine', 'mb') or 0):
            atk = s.sc(('e', pl.id), 'atk') or 38
            if s.t % ATK_EVERY == 0:
                H.A.strike(s, b, atk * 11 // 10)
            elif s.t % SKILL_EVERY == 5:
                H.A.strike(s, b, atk * 2, basic=False)


class Meter:
    def __init__(self, s):
        self.s = s
        pl = s.player()
        self.pid = ('e', pl.id)
        self.maxhp = s.sc(self.pid, 'maxHealth')
        self.loss = []
        self.grog, self.grog_on = 0, False
        self.pats, self.last_pat = [], 0

    def tick(self, heal=True):
        s = self.s
        cur = s.sc(self.pid, 'curHealth') or 0
        self.loss.append(max(0, self.maxhp - cur))
        if heal:
            H.heal(s)
        g = (H.bal(s, 'grgT') or 0) > 0
        if g and not self.grog_on:
            self.grog += 1
        self.grog_on = g
        p = H.hr(s, '#pat') or 0
        if p != self.last_pat:
            if p:
                self.pats.append((s.t, p))
            self.last_pat = p

    def intake(self):
        return 100.0 * sum(self.loss) / self.maxhp / (len(self.loss) / 1200.0) if self.loss else 0.0

    def worst(self, n=40):
        best = run = 0
        for i, v in enumerate(self.loss):
            run += v - (self.loss[i - n] if i >= n else 0)
            best = max(best, run)
        return 100.0 * best / self.maxhp


def setup(dp, seed, level=15):
    s, pl = H.setup_h1(dp, seed=seed, lv=level, hp=260 * LV_HP(level + 1) // 100, player_level=level)
    assert H.fight_sc(s)
    return s, pl


def hit_stats(s, ag, t0):
    """Per judged hit after t0: (parryable?, tier, perfect dodge, the agent's input for it)."""
    P = [j for j in s.judged if j['t'] > t0 and not j['np']]
    N = [j for j in s.judged if j['t'] > t0 and j['np']]
    f_ok = {t for t, ok in s.f_log if ok}
    d_ok = {t for t, ok in s.d_log if ok}
    timed_n = [j for j in N if ag.acted.get(j['t'], ('', -1))[0] == 'D' and ag.acted[j['t']][1] in d_ok]
    timed_p = [j for j in P if ag.acted.get(j['t'], ('', -1))[0] == 'F']
    return dict(p=len(P), p_pp=sum(j['parT'] == 3 for j in P), p_t2=sum(j['parT'] == 2 for j in P), p_t1=sum(j['parT'] == 1 for j in P),
                n=len(N), n_pd=sum(j['pdg'] == 1 for j in N), timed_n=len(timed_n), timed_n_pd=sum(j['pdg'] == 1 for j in timed_n),
                timed_p=len(timed_p), timed_p_pp=sum(j['parT'] == 3 for j in timed_p),
                f=len(s.f_log), f_refused=sum(not ok for _t, ok in s.f_log), d=len(s.d_log), d_refused=sum(not ok for _t, ok in s.d_log))


def run_phase(job):
    dp, phase, kind, sigma, seed, ticks = job['dp'], job['phase'], job['kind'], job['sigma'], job['seed'], job['ticks']
    api, S = api_of(dp)
    s, pl = setup(dp, seed)
    if phase == 2:
        H.test_id(s, 33)
    H.facing_setup(s, 3.0)
    b = H.body_of(s)
    bid = ('e', b.id)
    mx = s.sc(bid, 'mhpM')
    lo, back = (mx * 70 // 100, mx) if phase == 1 else (mx * 30 // 100, mx * 55 // 100)
    if phase == 2:
        s.setsc(bid, 'mhpC', back)
    ag = Agent(s, api, S, kind, sigma, random.Random(seed * 7919 + int(sigma * 10)))
    m = Meter(s)
    t0 = s.t
    for _ in range(ticks):
        ag.step()
        H.world_h1(s)
        m.tick()
        if (s.sc(bid, 'mhpC') or 0) < lo:
            s.setsc(bid, 'mhpC', back)
    a6 = [t for t, p in m.pats if p == S.TID['a6']]
    a6max = max([sum(1 for u in a6 if t <= u < t + 400) for t in a6] or [0])
    mins = ticks / 1200.0
    return dict(job, intake=m.intake(), worst=m.worst(), grog=m.grog / mins, ult=sum(1 for t, p in m.pats if p == S.TID['ult']) / mins,
                a6max=a6max, pats=len(m.pats), **hit_stats(s, ag, t0))


def run_gauntlet(job):
    dp, g, kind, sigma, seed, motion = job['dp'], job['g'], job['kind'], job['sigma'], job['seed'], job['motion']
    api, S = api_of(dp)
    s, pl = setup(dp, seed)
    H.facing_setup(s, 6.0)
    H.test_id(s, {'a8': 21, 'a13': 27}[g])
    s.revive = 0
    t0, jt = s.t, api.JUDGE_T[g]
    ag = Agent(s, api, S, kind, sigma, random.Random(seed * 104729 + int(sigma * 10) + len(motion)), attack=False, move=False)
    m = Meter(s)
    f0 = len(s.f_log)
    while s.t < t0 + jt - 1:
        ag.step()
        if motion != 'stand':
            b, p = H.body_of(s), s.player()
            cx, cz = api.CX - p.pos[0], api.CZ - p.pos[2]
            d = math.hypot(cx, cz) or 1.0
            ux, uz = cx / d, cz / d
            vx, vz = {'in': (ux, uz), 'out': (-ux, -uz), 'side': (-uz, ux)}[motion]
            if motion != 'out' or d < api.WALK - 1.0:
                H.place_player(s, p.pos[0] + vx * 0.22, p.pos[2] + vz * 0.22)
        H.world_h1(s)
        m.tick()
    cuts_dmg = 100.0 * sum(m.loss) / m.maxhp
    gau = H.hr(s, '#gau') or 0
    H.world_h1(s)
    cleared = (H.hr(s, '#sqn') or 0) == S.SEQ_ID['repel']
    presses = sum(1 for t, ok in s.f_log[f0:] if ok)
    return dict(job, cleared=cleared, segs=(api.GAUGE['max'] - gau) // api.GAUGE['seg'], presses=presses,
                cuts_dmg=cuts_dmg, **hit_stats(s, ag, t0))


def run_kill(job):
    dp, kind, sigma, seed, level = job['dp'], job['kind'], job['sigma'], job['seed'], job['level']
    api, S = api_of(dp)
    s, pl = setup(dp, seed, level)
    H.facing_setup(s, 3.0)
    rng = random.Random(seed * 31 + level)
    ag = Agent(s, api, S, kind, sigma, rng)
    gag = Agent(s, api, S, 'parrier', 0, rng, attack=False, move=False)     # the gauntlets are parried by every kill agent
    m = Meter(s)
    PH = api.PH
    fight = cut = 0
    per = {}
    for _ in range(job.get('limit', 14000)):
        ph = H.hr(s, '#ph')
        if (H.mb(s, '#mbSt') or 0) == 2 or H.body_of(s) is None:
            break
        (gag if ph in (PH['a8'], PH['a13']) else ag).step()
        H.world_h1(s)
        m.tick()
        ph = H.hr(s, '#ph')
        per[ph] = per.get(ph, 0) + 1
        if ph in (PH['p1'], PH['p2'], PH['a8'], PH['a13'], PH['lead60'], PH['lead']):
            fight += 1
        else:
            cut += 1
    killed = (H.mb(s, '#mbSt') or 0) == 2
    return dict(job, killed=killed, fight_s=fight / 20.0, cut_s=cut / 20.0, intake=m.intake(), grog=m.grog,
                per={str(k): v for k, v in per.items()})


CHAIN_AT = {'a1': 3.0, 'a2': 3.0, 'a3': 3.0, 'a3s': 3.0, 'a4': 9.0, 'd4': 2.6, 'tri': 8.0, 'rings': 2.4, 'mx': 8.0, 'nb': 9.0, 'q': 10.0}


def run_chain(job):
    """T13: one pattern with the player in reach of every hit, F at h - 1 for every parryable hit: every one a perfect
    parry, no press refused (the 12-t / 2-t F lock against the chain's gaps)."""
    dp, key, phase = job['dp'], job['key'], job['phase']
    api, S = api_of(dp)
    s, pl = setup(dp, 11)
    if phase == 2:
        H.test_id(s, 33)
        H.run_h1(s, 2)
    H.facing_setup(s, CHAIN_AT[key])
    ag = Agent(s, api, S, 'parrier', 0, random.Random(1), attack=False, move=False)
    H.start_pattern(s, S.TID[key])
    t0 = s.t
    for _ in range(200):
        if (H.hr(s, '#pat') or 0) == 0:
            break
        ag.step()
        H.heal(s)
        H.world_h1(s)
    st = hit_stats(s, ag, t0)
    want = sum(1 for i, r in enumerate(api.HITS[key]) if r[6] == 'P' and api.HIT_PH.get(key, {}).get(i, phase) == phase)
    return dict(job, want=want, **st)


def run(job):
    try:
        return {'phase': run_phase, 'g': run_gauntlet, 'kill': run_kill, 'chain': run_chain}[job['mode']](job)
    except Exception as e:      # noqa: BLE001
        import traceback
        return dict(job, error=repr(e), tb=traceback.format_exc()[-1500:])


def jobs_of(dp, quick, only):
    J = []
    seeds = SEEDS[:1] if quick else SEEDS
    ticks = 1200 if quick else 3600
    if 'p1' in only or 'p2' in only:
        for phase in (1, 2):
            if f'p{phase}' not in only:
                continue
            for kind, sigma in (('walker', 0), ('stand', 0), ('parrier', 0), ('parrier', 1.5), ('parrier', 3), ('mixed', 0), ('dodger', 1),
                                ('masher', 0)):
                for seed in seeds:
                    J.append(dict(mode='phase', dp=dp, phase=phase, kind=kind, sigma=sigma, seed=seed, ticks=ticks))
    if 'g' in only:
        for g in ('a8', 'a13'):
            J.append(dict(mode='g', dp=dp, g=g, kind='stand', sigma=0, seed=11, motion='stand'))
            for sigma in (0, 1):
                for motion in ('stand', 'out', 'side', 'in'):
                    for seed in seeds:
                        J.append(dict(mode='g', dp=dp, g=g, kind='parrier', sigma=sigma, seed=seed, motion=motion))
            for seed in range(1, 4 if quick else 13):
                J.append(dict(mode='g', dp=dp, g=g, kind='sloppy', sigma=0, seed=seed, motion='stand'))
            for seed in seeds:
                J.append(dict(mode='g', dp=dp, g=g, kind='masher', sigma=0, seed=seed, motion='stand'))
                J.append(dict(mode='g', dp=dp, g=g, kind='dodger', sigma=0, seed=seed, motion='stand'))
    if 'chain' in only:
        for key in CHAIN_AT:
            for phase in ((2,) if key in ('mx', 'nb', 'q') else (1, 2)):
                J.append(dict(mode='chain', dp=dp, key=key, phase=phase))
    if 'kill' in only:
        for level in ((15,) if quick else (5, 10, 15)):
            J.append(dict(mode='kill', dp=dp, kind='walker', sigma=0, seed=11, level=level))
        for seed in seeds[:1 if quick else 2]:
            J.append(dict(mode='kill', dp=dp, kind='parrier', sigma=1.5, seed=seed, level=15))
    return J


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else float('nan')


def table(res):
    ph = lambda phase, kind, sigma=0: [r for r in res if r.get('mode') == 'phase' and r['phase'] == phase and r['kind'] == kind and r['sigma'] == sigma and 'error' not in r]   # noqa: E731
    gz = lambda g, kind, sigma=0: [r for r in res if r.get('mode') == 'g' and r['g'] == g and r['kind'] == kind and r['sigma'] == sigma and 'error' not in r]   # noqa: E731
    kl = lambda kind, level=None: [r for r in res if r.get('mode') == 'kill' and r['kind'] == kind and (level is None or r['level'] == level) and 'error' not in r]   # noqa: E731
    rows = []

    def row(tid, what, val, band, ok):
        rows.append((tid, what, val, band, 'PASS' if ok else 'miss' if ok is not None else '-'))
    I = lambda phase, kind, sigma=0: mean(r['intake'] for r in ph(phase, kind, sigma))   # noqa: E731
    w1, w2 = I(1, 'walker'), I(2, 'walker')
    row('T1', 'P1 walker intake / 타키 whole (recorded 124.0 %/min)', f'{w1:.1f} %/min = {w1 / TACHY_WALKER:.2f} x', '1.00-1.15', 1.0 <= w1 / TACHY_WALKER <= 1.15)
    p3 = I(1, 'parrier', 3)
    row('T1b', 'P1 parrier s3 intake / walker', f'{p3:.1f} %/min = {p3 / w1:.2f} x', '<= 0.60', p3 / w1 <= 0.60)
    m0 = I(1, 'mixed')
    row('T1c', 'P1 mixed s0 intake', f'{m0:.1f} %/min', '<= 5', m0 <= 5)
    row('T2', 'P2 walker intake / 타키 whole', f'{w2:.1f} %/min = {w2 / TACHY_WALKER:.2f} x', '<= 1.25', w2 / TACHY_WALKER <= 1.25)
    st = max(I(1, 'stand'), I(2, 'stand'))
    row('T3', 'standing max(P1, P2) / the Guardian standing (recorded 164.0)', f'{st:.1f} %/min = {st / GUARDIAN_STAND:.2f} x', '<= 1.8', st / GUARDIAN_STAND <= 1.8)
    wr = max([r['worst'] for r in ph(1, 'walker') + ph(2, 'walker')] or [float('nan')])
    row('T4', "walker's worst 40-t window", f'{wr:.1f} % max HP', '<= 40', wr <= 40)
    for tid, g, lim in (('T5', 'a8', 45), ('T5b', 'a13', 55)):
        v = mean(r['cuts_dmg'] for r in gz(g, 'stand'))
        row(tid, f'every cut of {g} on a standing agent', f'{v:.1f} % max HP', f'<= {lim}', v <= lim)
    for sigma, lim in ((0, 95), (1, 90)):
        rs = gz('a8', 'parrier', sigma) + gz('a13', 'parrier', sigma)
        seg = 100.0 * sum(r['timed_p_pp'] for r in rs) / max(1, sum(r['timed_p'] for r in rs))
        clr = 100.0 * mean(r['cleared'] for r in rs)
        row('T6', f'parrier s{sigma} in the gauntlets (stand / walk x3): perfect per timed F; cleared',
            f'{seg:.1f} %; {clr:.0f} % of {len(rs)}', f'>= {lim} / >= {90 if sigma else 95}', seg >= lim and clr >= (90 if sigma else 95))
    sl = gz('a8', 'sloppy') + gz('a13', 'sloppy')
    ma = gz('a8', 'masher') + gz('a13', 'masher')
    do = gz('a8', 'dodger') + gz('a13', 'dodger')
    v = (100 * mean(r['cleared'] for r in sl), 100 * mean(r['cleared'] for r in ma), 100 * mean(r['cleared'] for r in do), mean(r['cuts_dmg'] for r in do))
    row('T7', 'sloppy clears; masher clears; dodger clears (its damage)', f'{v[0]:.0f} %; {v[1]:.0f} %; {v[2]:.0f} % ({v[3]:.1f} % HP)',
        '<= 35; 0; 0 (0)', v[0] <= 35 and v[1] == 0 and v[2] == 0 and v[3] == 0)
    a6 = max([r['a6max'] for r in res if r.get('mode') == 'phase' and 'error' not in r] or [0])
    row('T8', 'A6 starts in any 400 t (all phase runs)', str(a6), '<= 1', a6 <= 1)
    ks = {lv: mean(r['fight_s'] for r in kl('walker', lv) if r['killed']) for lv in (5, 10, 15)}
    row('T9', 'walker kill, fighting time Lv5 / 10 / 15 (cutscenes apart)', ' / '.join(f'{ks[lv]:.0f} s' for lv in (5, 10, 15)), '150-185',
        all(150 <= ks[lv] <= 185 for lv in (5, 10, 15)))
    kp = mean(r['fight_s'] for r in kl('parrier') if r['killed'])
    row('T9b', 'parrier s1.5 kill, fighting time', f'{kp:.0f} s', '125-170', 125 <= kp <= 170)
    gp, gw = mean(r['grog'] for r in ph(1, 'parrier', 1.5) + ph(2, 'parrier', 1.5)), mean(r['grog'] for r in ph(1, 'walker') + ph(2, 'walker'))
    row('T10', 'groggies / min: parrier s1.5; walker', f'{gp:.2f}; {gw:.2f}', '0.8-1.3; <= 0.4', 0.8 <= gp <= 1.3 and gw <= 0.4)
    uw, um = mean(r['ult'] for r in ph(1, 'walker') + ph(2, 'walker')), mean(r['ult'] for r in ph(1, 'mixed') + ph(2, 'mixed'))
    row('T11', 'U / min: walker; mixed s0', f'{uw:.2f}; {um:.2f}', '0.8-1.5; 0.6-1.0', 0.8 <= uw <= 1.5 and 0.6 <= um <= 1.0)
    dd = ph(1, 'dodger', 1) + ph(2, 'dodger', 1)
    v = 100.0 * sum(r['timed_n_pd'] for r in dd) / max(1, sum(r['timed_n'] for r in dd))
    row('T12', 'dodger s1 avoids an N hit it times', f'{v:.1f} % of {sum(r["timed_n"] for r in dd)}', '>= 95', v >= 95)
    ch = [r for r in res if r.get('mode') == 'chain' and 'error' not in r]
    got, want, ref = sum(r['p_pp'] for r in ch), sum(r['want'] for r in ch), sum(r['f_refused'] for r in ch)
    row('T13', 'parrier s0, every chain in reach (F at h - 1): P hits perfect-parried; refused F',
        f'{got} of {want} ({100.0 * got / max(1, want):.1f} %); {ref}', '100; 0', got == want and ref == 0)
    pp = ph(1, 'parrier', 0) + ph(2, 'parrier', 0)
    v = 100.0 * sum(r['timed_p_pp'] for r in pp) / max(1, sum(r['timed_p'] for r in pp))
    row('T13f', '... in the free fight: of the P hits that found it; refused F (presses for hits that missed lock F)',
        f'{v:.1f} % of {sum(r["timed_p"] for r in pp)}; {sum(r["f_refused"] for r in pp)} of {sum(r["f"] for r in pp)}', '(report)', None)
    bad = [(r['key'], r['phase'], r['p_pp'], r['want'], r['f_refused']) for r in ch if r['p_pp'] != r['want'] or r['f_refused']]
    if bad:
        print('T13 chains not fully parried (key, phase, perfect, P hits, refused):', bad)
    w = max(len(r[1]) for r in rows)
    print(f'{"#":4} {"target":{w}}  {"measured":34} {"band":22} result')
    for tid, what, val, band, ok in rows:
        print(f'{tid:4} {what:{w}}  {val:34} {band:22} {ok}')
    print('\nby agent (intake %/min, worst 40 t %, groggy / min, U / min, patterns):')
    for phase in (1, 2):
        for kind, sigma in (('walker', 0), ('stand', 0), ('parrier', 0), ('parrier', 1.5), ('parrier', 3), ('mixed', 0), ('dodger', 1), ('masher', 0)):
            rs = ph(phase, kind, sigma)
            if rs:
                print(f'  P{phase} {kind:8} s{sigma:<3} intake {mean(r["intake"] for r in rs):6.1f}  worst {max(r["worst"] for r in rs):5.1f}  '
                      f'grog {mean(r["grog"] for r in rs):.2f}  U {mean(r["ult"] for r in rs):.2f}  pats/min {mean(r["pats"] / (r["ticks"] / 1200) for r in rs):.1f}  '
                      f'P hits {sum(r["p"] for r in rs)} (pp {sum(r["p_pp"] for r in rs)})  N hits {sum(r["n"] for r in rs)} (pd {sum(r["n_pd"] for r in rs)})')
    for r in kl('walker') + kl('parrier'):
        print(f'  kill {r["kind"]} Lv{r["level"]} seed {r["seed"]}: killed {r["killed"]} fighting {r["fight_s"]:.0f} s, cutscenes {r["cut_s"]:.0f} s, '
              f'intake {r["intake"]:.0f} %/min, groggies {r["grog"]}')
    err = [r for r in res if 'error' in r]
    if err:
        print(f'\n{len(err)} run(s) failed:', err[0]['error'], err[0].get('tb', '')[-600:])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dp')
    ap.add_argument('--out', default=str(HERE / 'out'))
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--quick', action='store_true')
    ap.add_argument('--only', default='p1,p2,g,kill,chain')
    a = ap.parse_args()
    J = jobs_of(str(Path(a.dp).resolve()), a.quick, set(a.only.split(',')))
    print(f'hrfair 2.0: {len(J)} runs, {a.jobs} at a time', flush=True)
    with Pool(a.jobs) as pool:
        res = []
        for i, r in enumerate(pool.imap_unordered(run, J)):
            res.append(r)
            if (i + 1) % 10 == 0:
                print(f'  {i + 1}/{len(J)}', flush=True)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'hrfair2.json').write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
    table(res)


if __name__ == '__main__':
    main()
