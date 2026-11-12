#!/usr/bin/env python3
"""hrfair2.py — hrfair 2.0: the balance probe of the rebuilt 홍련 fight (hr_design §6.4; lane H1). Scratch tool, never shipped.

    python3 hrfair2.py <roguelike> [--out <dir>] [--jobs 4] [--quick] [--only p1,p2,g,kill]
    (run from a copy of tools/dev/sim outside the datapack; results <out>/hrfair2.json + the table on stdout)

World: tests/lib/hrsim.py H1Sim (the REAL player/def judge, mboss framework, bal/**; the F lock and dodge cooldown as ruled
on 11-11, review A-01 / A-12: constants from the loaded pack where they exist). The item-less Lv15 player (268 HP) against
her at L16 (registry hp x LV_HP(16) / 100: 5049 at hp 225); seeds 11 / 22 / 33; 3 600 t per fight phase. The sequences are the core stand-ins until lane H2 lands
(their lengths are the contract's; no cutscene tick is counted as fighting time).

Agents (all but `stand` walk to 2.5 b at 0.216 b/t and hit her every 10 t within 3.5 b with atk x 1.1, a skill hit every
160 t; they know every pattern's hit ticks - the cue / flash gives 7-22 t of notice):
  walker      never presses F or dodges (the old baseline)          stand    never moves or acts
  parrier s   F for every parryable hit, aimed at h - 1 with a normal timing error s (ticks); dodges nothing
  mixed s     parries P hits, perfect-dodges N hits with the same error
  dodger s    a dodge at h - 1 +- s for every hit                   masher   F every 4 t
  (HB: an input whose cue never showed - its pattern ended or was cancelled first - is withdrawn)
  sloppy      F at h - 1 +- 6 t (uniform) for every hit
  metro p/k   (gauntlets, HB) F every p ticks from the gauntlet's tick k (0 <= k < p), reading no cue: every p 8..30, every k
Gauntlet agents stand, or walk 0.22 b/t outward / sideways / inward, and act on every cut.

Targets T1-T13: hr_design §6.4. H1 divided T1 / T2 by 타키's whole-fight melee walker and T3 by the Guardian standing as
RECORDED by hrfair 1.x (review/bal/base_tachy.log: 124.0 and 164.0 %/min; the old walker dodged on reaction, this one never
does); HB measures both references with this tool (below) and falls back to the recorded numbers only without `base` runs.

HB (balance lane, 11-11): (1) the player's inputs as the game takes them: hrsim.world_h1 now drives the REAL player/f_key
(player/def/press / press_re / par_use: every lock constant of load.mcfunction) and the REAL dashCool (#dashCoolT, the
refund of player/def/dg_refund) instead of its own model (review H-A; tests/test_input_hr.py checks it). (2) 타키 and the Guardian are
re-measured by THIS tool (`base` runs: 타키's whole fight with the same walker, real HP at L16, its rift and intro as
hrsim.special_fight; the Guardian standing in azsim's plaza, Lv15 vs L15): T1 / T2 / T3 divide by those (T1-T3 as hr_design
§6.4 restated 11-11). (3) Every target per seed (11 / 22 / 33) and pooled; the kill runs on all three seeds; T6 sigma 1 and
T12 as a fraction of the 3-tick window's ceiling at the agent's timing error.
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
        self.m0, self.period, self.phase = s.t, 1, 0      # the metronome: F at m0 + phase + n x period
        self.cur = []                 # (hit tick, input, input tick) planned for the running pattern

    def err(self):
        if self.kind == 'sloppy':
            return self.rng.randint(-6, 6)
        return int(round(self.rng.gauss(0, self.sigma))) if self.sigma else 0

    def plan(self, h, par):
        """An input for the hit at world tick h."""
        s = self.s
        act = {'walker': None, 'stand': None, 'masher': None, 'metro': None, 'parrier': 'F' if par == 'P' else None,
               'mixed': 'F' if par == 'P' else 'D', 'dodger': 'D', 'sloppy': 'F'}[self.kind]
        self.hits[h] = par
        if act is None or h in self.acted:
            return
        t = max(s.t + 1, h - 1 + self.err())
        self.acted[h] = (act, t)
        self.cur.append((h, act, t))
        (s.press if act == 'F' else s.dodge)(at=t)

    def withdraw(self):
        """HB (11-11): the running pattern ended or was cancelled (a groggy, A6, a floor, a perfect-parry flinch): the inputs
        planned for its hits whose cue never showed (cue at h - CUE_LEAD) are not pressed. Before, they were: a press for a hit
        that never came is a whiff, and the whiff streak then refused the presses for the next pattern's real cues."""
        now = self.s.t
        for h, act, ti in self.cur:
            if h - self.api.CUE_LEAD > now and self.acted.get(h) == (act, ti):
                (self.s.f_at if act == 'F' else self.s.d_at).discard(ti)
                del self.acted[h]
        self.cur = []

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
            if self.cur:
                self.withdraw()
            self.pat = pat if pt >= 1 else 0
            return
        t_start = s.t - pt
        if pat != self.pat or self.t_start is None or abs(t_start - self.t_start) > 0:
            self.withdraw()
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
        if self.kind == 'metro' and (s.t + 1 - self.m0) % self.period == self.phase:
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
                skill_strike(s, b, atk * 2)


def skill_strike(s, b, dmg):
    """A skill hit through the REAL combat/apply with #skillDmg tmp 1 (what on_hit's A6 trigger reads)."""
    pl = s.player()
    s.call('rlk:combat/clear_atkflags', H.Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
    for k, v in (('#dmg', dmg), ('#elem', 0), ('#elU', 0), ('#icd', 0), ('#crit', 0), ('#stunHit', 0), ('#hitLanded', 0), ('#bowHit', 0),
                 ('#lunar', 0), ('#tfm', 0), ('#trueDmg', 0), ('#skillDmg', 1)):
        s.setsc(k, 'tmp', v)
    s.stack.append('rlk:azsim/strike')
    try:
        s.call('rlk:combat/apply', H.Ctx(b, tuple(b.pos), tuple(b.rot)))
    finally:
        s.stack.pop()
    s.setsc('#skillDmg', 'tmp', 0)


class Meter:
    def __init__(self, s):
        self.s = s
        pl = s.player()
        self.pid = ('e', pl.id)
        self.maxhp = s.sc(self.pid, 'maxHealth')
        self.loss = []
        self.grog, self.grog_on = 0, False
        self.pats, self.last_pat = [], 0
        self.loss_by, self.prev_pat = {}, 0          # HP lost per pattern id (the running one, else the one before)

    def tick(self, heal=True):
        s = self.s
        cur = s.sc(self.pid, 'curHealth') or 0
        self.loss.append(max(0, self.maxhp - cur))
        if self.loss[-1]:
            k = (H.hr(s, '#pat') or 0) or self.prev_pat
            self.loss_by[k] = self.loss_by.get(k, 0) + self.loss[-1]
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
                self.prev_pat = p
            self.last_pat = p

    def intake(self):
        return 100.0 * sum(self.loss) / self.maxhp / (len(self.loss) / 1200.0) if self.loss else 0.0

    def worst(self, n=40):
        best = run = 0
        for i, v in enumerate(self.loss):
            run += v - (self.loss[i - n] if i >= n else 0)
            best = max(best, run)
        return 100.0 * best / self.maxhp


def hp_of(dp):
    """Her registry hp (the knob of hr_design §6.4; 260 at H1)."""
    api, _S = api_of(dp)
    return api.BOSS['hp']


def setup(dp, seed, level=15):
    s, pl = H.setup_h1(dp, seed=seed, lv=level, hp=hp_of(dp) * LV_HP(level + 1) // 100, player_level=level)
    assert H.fight_sc(s)
    return s, pl


world = H.world_h1      # the inputs through the REAL player/f_key and dashCool (hrsim, HB 11-11)


def hit_stats(s, ag, t0):
    """Per judged hit after t0: (parryable?, tier, perfect dodge, the agent's input for it)."""
    P = [j for j in s.judged if j['t'] > t0 and not j['np']]
    N = [j for j in s.judged if j['t'] > t0 and j['np']]
    f_ok = {t for t, ok in s.f_log if ok}
    d_ok = {t for t, ok in s.d_log if ok}
    timed_n = [j for j in N if ag.acted.get(j['t'], ('', -1))[0] == 'D' and ag.acted[j['t']][1] in d_ok]
    timed_p = [j for j in P if ag.acted.get(j['t'], ('', -1))[0] == 'F']
    win = lambda j: abs(ag.acted[j['t']][1] - (j['t'] - 1)) <= 1     # noqa: E731  the input's realized error inside the 3-t window
    timed_n_w = [j for j in timed_n if win(j)]
    timed_p_w = [j for j in timed_p if win(j)]
    return dict(p=len(P), p_pp=sum(j['parT'] == 3 for j in P), p_t2=sum(j['parT'] == 2 for j in P), p_t1=sum(j['parT'] == 1 for j in P),
                n=len(N), n_pd=sum(j['pdg'] == 1 for j in N), timed_n=len(timed_n), timed_n_pd=sum(j['pdg'] == 1 for j in timed_n),
                timed_p=len(timed_p), timed_p_pp=sum(j['parT'] == 3 for j in timed_p),
                timed_n_w=len(timed_n_w), timed_n_w_pd=sum(j['pdg'] == 1 for j in timed_n_w),
                timed_p_w=len(timed_p_w), timed_p_w_pp=sum(j['parT'] == 3 for j in timed_p_w),
                f=len(s.f_log), f_refused=sum(not ok for _t, ok in s.f_log), d=len(s.d_log), d_refused=sum(not ok for _t, ok in s.d_log))


def pmix(S, pats):
    """How many times each pattern key started."""
    key_of = {v: k for k, v in S.TID.items()}
    out = {}
    for _t, p in pats:
        k = key_of.get(p, str(p))
        out[k] = out.get(k, 0) + 1
    return out


def pstat(S, m, s, t0):
    """Per pattern key: [% max HP lost, P hits judged, of them perfect-parried, N hits judged, of them perfect-dodged]."""
    key_of = {v: k for k, v in S.TID.items()}
    out = {}
    for pid, v in m.loss_by.items():
        out.setdefault(key_of.get(pid, str(pid)), [0.0, 0, 0, 0, 0])[0] += 100.0 * v / m.maxhp
    for j in s.judged:
        if j['t'] > t0:
            r = out.setdefault(key_of.get(j['pat'], str(j['pat'])), [0.0, 0, 0, 0, 0])
            if j['np']:
                r[3] += 1
                r[4] += j['pdg'] == 1
            else:
                r[1] += 1
                r[2] += j['parT'] == 3
    return out


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
        world(s)
        m.tick()
        if (s.sc(bid, 'mhpC') or 0) < lo:
            s.setsc(bid, 'mhpC', back)
    a6 = [t for t, p in m.pats if p == S.TID['a6']]
    a6max = max([sum(1 for u in a6 if t <= u < t + 400) for t in a6] or [0])
    mins = ticks / 1200.0
    return dict(job, intake=m.intake(), worst=m.worst(), grog=m.grog / mins, ult=sum(1 for t, p in m.pats if p == S.TID['ult']) / mins,
                a6max=a6max, pats=len(m.pats), pmix=pmix(S, m.pats), pstat=pstat(S, m, s, t0), **hit_stats(s, ag, t0))


def run_gauntlet(job):
    dp, g, kind, sigma, seed, motion = job['dp'], job['g'], job['kind'], job['sigma'], job['seed'], job['motion']
    api, S = api_of(dp)
    s, pl = setup(dp, seed)
    H.facing_setup(s, 6.0)
    H.test_id(s, {'a8': 21, 'a13': 27}[g])
    s.revive = 0
    t0, jt = s.t, api.JUDGE_T[g]
    ag = Agent(s, api, S, kind, sigma, random.Random(seed * 104729 + int(sigma * 10) + len(motion)), attack=False, move=False)
    if kind == 'metro':
        ag.m0, ag.period, ag.phase = t0, job['period'], job['k']
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
        world(s)
        m.tick()
    cuts_dmg = 100.0 * sum(m.loss) / m.maxhp
    gau = H.hr(s, '#gau') or 0
    world(s)
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
        world(s)
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
        world(s)
    st = hit_stats(s, ag, t0)
    want = sum(1 for i, r in enumerate(api.HITS[key]) if r[6] == 'P' and api.HIT_PH.get(key, {}).get(i, phase) == phase)
    return dict(job, want=want, **st)


def run_base(job):
    """The references of T1-T3 measured by this tool (HB, 11-11): 타키's whole fight against the same walker (real HP at L16 =
    its registry hp x LV_HP(16), its rift entered and its intro played as hrsim.special_fight, until it dies), or the
    Guardian against the standing agent in azsim's plaza (Lv15 vs L15, 100000 HP, `ticks`). Intake over every tick from
    the fight start (타키: its transitions included, as the README figure T1 / T2 were written against)."""
    dp, boss, kind, seed = job['dp'], job['boss'], job['kind'], job['seed']
    api, S = api_of(dp)
    if boss == 'tachy':
        hp = next(b for b in api.REG['boss'] if b['id'] == 'tachy')['hp']
        s, pl = H.setup(dp, seed=seed, lv=15, hp=hp * LV_HP(16) // 100, player_level=15)
        z, a, ok = H.special_fight(s, 'tachy')
        step = H.world
    else:
        s, zone, pl = H.A.setup(force=1, lv=15, hp=100000, seed=seed, player_level=15, dp=dp)
        ok = H.A.to_fight(s, zone)
        step = H.A.world
    assert ok, f'{boss}: the fight did not start'
    ag = Agent(s, api, S, kind, 0, random.Random(seed * 7919))
    m = Meter(s)
    for _ in range(job['ticks']):
        if (H.mb(s, '#mbSt') or 0) == 2 or H.body_of(s) is None:
            break
        ag.step()
        step(s)
        m.tick()
    killed = (H.mb(s, '#mbSt') or 0) == 2 or H.body_of(s) is None
    return dict(job, intake=m.intake(), worst=m.worst(), ticks_run=len(m.loss), killed=killed)


def run(job):
    try:
        return {'phase': run_phase, 'g': run_gauntlet, 'kill': run_kill, 'chain': run_chain, 'base': run_base}[job['mode']](job)
    except Exception as e:      # noqa: BLE001
        import traceback
        return dict(job, error=repr(e), tb=traceback.format_exc()[-1500:])


AGENTS = (('walker', 0), ('stand', 0), ('parrier', 0), ('parrier', 1.5), ('parrier', 3), ('mixed', 0), ('dodger', 1), ('masher', 0))


def jobs_of(dp, quick, only, seeds=None, agents=None):
    J = []
    seeds = seeds or (SEEDS[:1] if quick else SEEDS)
    ticks = 1200 if quick else 3600
    for phase in (1, 2):
        if f'p{phase}' not in only:
            continue
        for kind, sigma in agents or AGENTS:
            for seed in seeds:
                J.append(dict(mode='phase', dp=dp, phase=phase, kind=kind, sigma=sigma, seed=seed, ticks=ticks))
    if 'g' in only:
        for g in ('a8', 'a13'):
            for seed in seeds:
                J.append(dict(mode='g', dp=dp, g=g, kind='stand', sigma=0, seed=seed, motion='stand'))
                for sigma in (0, 1):
                    for motion in ('stand', 'out', 'side', 'in'):
                        J.append(dict(mode='g', dp=dp, g=g, kind='parrier', sigma=sigma, seed=seed, motion=motion))
                for k in range(1 if quick else 4):        # sloppy: 4 runs per seed and gauntlet (grp = the seed)
                    J.append(dict(mode='g', dp=dp, g=g, kind='sloppy', sigma=0, seed=seed * 100 + k, grp=seed, motion='stand'))
                J.append(dict(mode='g', dp=dp, g=g, kind='masher', sigma=0, seed=seed, motion='stand'))
                J.append(dict(mode='g', dp=dp, g=g, kind='dodger', sigma=0, seed=seed, motion='stand'))
    if 'metro' in only:       # review H-A: a metronome F, every period 8..30 and every phase; no seed (nothing random in it)
        for g in ('a8', 'a13'):
            for per in range(8, 31):
                for k in range(per):
                    J.append(dict(mode='g', dp=dp, g=g, kind='metro', sigma=0, seed=0, period=per, k=k, motion='stand'))
    if 'chain' in only:
        for key in CHAIN_AT:
            for phase in ((2,) if key in ('mx', 'nb', 'q') else (1, 2)):
                J.append(dict(mode='chain', dp=dp, key=key, phase=phase))
    if 'kill' in only:
        for seed in seeds:
            for level in ((15,) if quick else (5, 10, 15)):
                J.append(dict(mode='kill', dp=dp, kind='walker', sigma=0, seed=seed, level=level))
            J.append(dict(mode='kill', dp=dp, kind='parrier', sigma=1.5, seed=seed, level=15))
    if 'base' in only:
        for seed in seeds:
            J.append(dict(mode='base', dp=dp, boss='tachy', kind='walker', sigma=0, seed=seed, ticks=12000))
            J.append(dict(mode='base', dp=dp, boss='guardian', kind='stand', sigma=0, seed=seed, ticks=ticks))
    return J


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else float('nan')


def ceiling(sigma, w=3):
    """The share of presses aimed at h - 1 with a normal error sigma (rounded to ticks) that land in the w-tick perfect window
    (p 0..w-1 = an error of -1..w-2 ticks): P(-1.5 < x < w - 1.5)."""
    if not sigma:
        return 1.0
    cdf = lambda x: 0.5 * (1 + math.erf(x / (sigma * math.sqrt(2))))   # noqa: E731
    return cdf(w - 1.5) - cdf(-1.5)


# hr_design §6.4 as restated by HB (11-11): T6 sigma 1 and T12 as a share of the window's ceiling (pooled; per seed, with
# ~90 judged inputs each, a looser floor for the sampling error); T1-T3 against references this tool measures (run_base).
FRAC_POOLED, FRAC_SEED = 0.95, 0.90


def rows_of(res, seed, base):
    """The T1-T13 rows for the runs of one seed (None = all seeds pooled): [(id, what, value, band, ok | None)]."""
    pooled = seed is None
    ok_seed = lambda r: 'error' not in r and (pooled or r.get('grp', r.get('seed')) == seed)   # noqa: E731
    R = [r for r in res if ok_seed(r)]
    ph = lambda phase, kind, sigma=0: [r for r in R if r['mode'] == 'phase' and r['phase'] == phase and r['kind'] == kind and r['sigma'] == sigma]   # noqa: E731
    gz = lambda g, kind, sigma=0: [r for r in R if r['mode'] == 'g' and r['g'] == g and r['kind'] == kind and r['sigma'] == sigma]   # noqa: E731
    kl = lambda kind, level=None: [r for r in R if r['mode'] == 'kill' and r['kind'] == kind and (level is None or r['level'] == level)]   # noqa: E731
    I = lambda phase, kind, sigma=0: mean(r['intake'] for r in ph(phase, kind, sigma))   # noqa: E731
    rows = []

    def row(tid, what, val, band, ok):
        rows.append((tid, what, val, band, ok))
    tk, gd = base
    w1, w2 = I(1, 'walker'), I(2, 'walker')
    row('T1', f'P1 walker intake / 타키 whole walker ({tk[1]} {tk[0]:.1f} %/min)', f'{w1:.1f} = {w1 / tk[0]:.2f} x', '1.00-1.15', 1.0 <= w1 / tk[0] <= 1.15)
    p3 = I(1, 'parrier', 3)
    row('T1b', 'P1 parrier s3 intake / walker', f'{p3 / w1:.2f}', '<= 0.60', p3 / w1 <= 0.60)
    m0 = I(1, 'mixed')
    row('T1c', 'P1 mixed s0 intake %/min', f'{m0:.1f}', '<= 5', m0 <= 5)
    row('T2', 'P2 walker intake / 타키 whole walker', f'{w2:.1f} = {w2 / tk[0]:.2f} x', '<= 1.25', w2 / tk[0] <= 1.25)
    st = max(I(1, 'stand'), I(2, 'stand'))
    row('T3', f'standing max(P1, P2) / the Guardian standing ({gd[1]} {gd[0]:.1f})', f'{st:.1f} = {st / gd[0]:.2f} x', '<= 1.8', st / gd[0] <= 1.8)
    wr = max([r['worst'] for r in ph(1, 'walker') + ph(2, 'walker')] or [float('nan')])
    row('T4', "walker's worst 40-t window % max HP", f'{wr:.1f}', '<= 40', wr <= 40)
    for tid, g, lim in (('T5', 'a8', 45), ('T5b', 'a13', 55)):
        v = mean(r['cuts_dmg'] for r in gz(g, 'stand'))
        row(tid, f'every cut of {g} on a standing agent % max HP', f'{v:.1f}', f'<= {lim}', v <= lim)
    for sigma in (0, 1):
        rs = gz('a8', 'parrier', sigma) + gz('a13', 'parrier', sigma)
        seg = 100.0 * sum(r['timed_p_pp'] for r in rs) / max(1, sum(r['timed_p'] for r in rs))
        segw = 100.0 * sum(r.get('timed_p_w_pp', 0) for r in rs) / max(1, sum(r.get('timed_p_w', 0) for r in rs))
        clr = 100.0 * mean(r['cleared'] for r in rs)
        cl = 100.0 * ceiling(sigma)
        row(f'T6s{sigma}', f'parrier s{sigma} gauntlets (stand / walk x3): perfect per timed F (ceiling {cl:.1f}) / per F inside the window; cleared',
            f'{seg:.1f} ({seg / cl:.0%}) / {segw:.1f}; {clr:.0f} % of {len(rs)}', f'- / >= 95; >= {90 if sigma else 95}', segw >= 95 and clr >= (90 if sigma else 95))
    sl = gz('a8', 'sloppy') + gz('a13', 'sloppy')
    ma = gz('a8', 'masher') + gz('a13', 'masher')
    do = gz('a8', 'dodger') + gz('a13', 'dodger')
    v = (100 * mean(r['cleared'] for r in sl), 100 * mean(r['cleared'] for r in ma), 100 * mean(r['cleared'] for r in do), mean(r['cuts_dmg'] for r in do))
    row('T7', 'sloppy clears; masher clears; dodger clears (its damage)', f'{v[0]:.0f}; {v[1]:.0f}; {v[2]:.0f} ({v[3]:.1f})',
        '<= 35; 0; 0 (0)', v[0] <= 35 and v[1] == 0 and v[2] == 0 and v[3] == 0)
    mt = [r for r in res if r.get('mode') == 'g' and r['kind'] == 'metro' and 'error' not in r]
    if mt or any(r.get('kind') == 'metro' for r in res):
        cl = {g: sorted({r['period'] for r in mt if r['g'] == g and r['cleared']}) for g in ('a8', 'a13')}
        n = {g: (sum(r['cleared'] for r in mt if r['g'] == g), sum(1 for r in mt if r['g'] == g)) for g in ('a8', 'a13')}
        mx = {g: max([r['segs'] for r in mt if r['g'] == g] or [0]) for g in ('a8', 'a13')}
        row('T7m', 'metronome F (p 8-30, every phase) clears G1; G2 (periods that clear; most segments taken)',
            f'{n["a8"][0]}/{n["a8"][1]} {cl["a8"]} ({mx["a8"]}); {n["a13"][0]}/{n["a13"][1]} {cl["a13"]} ({mx["a13"]})', '0; 0',
            n['a8'][0] == 0 and n['a13'][0] == 0)
    a6 = max([r['a6max'] for r in R if r['mode'] == 'phase'] or [0])
    row('T8', 'A6 starts in any 400 t (all phase runs)', str(a6), '<= 1', a6 <= 1)
    ks = {lv: mean(r['fight_s'] for r in kl('walker', lv) if r['killed']) for lv in (5, 10, 15)}
    row('T9', 'walker kill, fighting s, Lv5 / 10 / 15', ' / '.join(f'{ks[lv]:.0f}' for lv in (5, 10, 15)), '150-185',
        all(150 <= ks[lv] <= 185 for lv in (5, 10, 15)))
    kp = mean(r['fight_s'] for r in kl('parrier') if r['killed'])
    row('T9b', 'parrier s1.5 kill, fighting s', f'{kp:.0f}', '125-170', 125 <= kp <= 170)
    gp, gw = mean(r['grog'] for r in ph(1, 'parrier', 1.5) + ph(2, 'parrier', 1.5)), mean(r['grog'] for r in ph(1, 'walker') + ph(2, 'walker'))
    row('T10', 'groggies / min: parrier s1.5; walker (band relaxed by the lead 11-11: was 0.8-1.3)', f'{gp:.2f}; {gw:.2f}', '0.8-1.6; <= 0.4',
        0.8 <= gp <= 1.6 and gw <= 0.4)
    uw, um = mean(r['ult'] for r in ph(1, 'walker') + ph(2, 'walker')), mean(r['ult'] for r in ph(1, 'mixed') + ph(2, 'mixed'))
    row('T11', 'U / min: walker; mixed s0', f'{uw:.2f}; {um:.2f}', '0.8-1.5; 0.6-1.0', 0.8 <= uw <= 1.5 and 0.6 <= um <= 1.0)
    dd = ph(1, 'dodger', 1) + ph(2, 'dodger', 1)
    v = 100.0 * sum(r['timed_n_pd'] for r in dd) / max(1, sum(r['timed_n'] for r in dd))
    vw = 100.0 * sum(r.get('timed_n_w_pd', 0) for r in dd) / max(1, sum(r.get('timed_n_w', 0) for r in dd))
    cl = 100.0 * ceiling(1)
    row('T12', f'dodger s1 avoids an N hit it times (ceiling {cl:.1f}) / of those inside the window',
        f'{v:.1f} ({v / cl:.0%}) of {sum(r["timed_n"] for r in dd)} / {vw:.1f}', '- / >= 95', vw >= 95)
    ch = [r for r in res if r.get('mode') == 'chain' and 'error' not in r]
    got, want, ref = sum(r['p_pp'] for r in ch), sum(r['want'] for r in ch), sum(r['f_refused'] for r in ch)
    row('T13', 'parrier s0, every chain in reach (F at h - 1): perfect; refused F (one run, no seed)',
        f'{got} / {want}; {ref}', '100 %; 0', got == want and ref == 0)
    dp_ = next((r['dp'] for r in res if r.get('dp')), None)
    if dp_ and (Path(dp_) / 'tools/mboss_scarlet/api.py').exists():
        api, _S = api_of(dp_)
        if hasattr(api, 'NP_SHARE'):
            sh = []
            for fp in (1, 2):
                for b in range(3):
                    w = {k: v[fp][b] for k, v in api.WEIGHTS.items() if fp in v}
                    sh.append(sum(x * api.NP_SHARE.get(k, 0) for k, x in w.items()) / max(1, sum(w.values())))
                w = api.FAR_RULE[fp]
                sh.append(sum(x * api.NP_SHARE.get(k, 0) for k, x in w.items()) / max(1, sum(w.values())))
            row('W35', 'unparriable share of the pick weight, P1 / P2 near-mid-far-far rule (the lead 11-11)',
                ' '.join(f'{100 * x:.0f}' for x in sh), '<= 35 % each', max(sh) <= api.NP_SHARE_MAX + 1e-9)
    pp = ph(1, 'parrier', 0) + ph(2, 'parrier', 0)
    v = 100.0 * sum(r['timed_p_pp'] for r in pp) / max(1, sum(r['timed_p'] for r in pp))
    row('T13f', '... free fight: perfect of the P hits that found it; refused F of presses',
        f'{v:.1f} of {sum(r["timed_p"] for r in pp)}; {sum(r["f_refused"] for r in pp)} / {sum(r["f"] for r in pp)}', '(report)', None)
    return rows


def base_of(res):
    """(타키 whole walker %/min, label), (the Guardian standing %/min, label): measured here when the base runs are present,
    else hrfair 1.x's recorded numbers."""
    tk = [r['intake'] for r in res if r.get('mode') == 'base' and r['boss'] == 'tachy' and r.get('killed') and 'error' not in r]
    gd = [r['intake'] for r in res if r.get('mode') == 'base' and r['boss'] == 'guardian' and 'error' not in r]
    return ((mean(tk), 'measured') if tk else (TACHY_WALKER, 'recorded 1.x'), (mean(gd), 'measured') if gd else (GUARDIAN_STAND, 'recorded 1.x'))


def table(res):
    base = base_of(res)
    seeds = sorted({r.get('grp', r.get('seed')) for r in res if r.get('mode') in ('phase', 'g', 'kill') and r.get('kind') != 'metro' and 'error' not in r})
    cols = [rows_of(res, sd, base) for sd in seeds] + [rows_of(res, None, base)]
    w = max(len(r[1]) for r in cols[-1])
    print(f'{"#":5} {"target":{w}}  {"band":20} ' + ' '.join(f'{"s" + str(sd):24}' for sd in seeds) + f' {"pooled":30} result')
    out = []
    for i, (tid, what, val, band, ok) in enumerate(cols[-1]):
        per = [c[i] for c in cols[:-1]]
        oks = [p[4] for p in per] + [ok]
        res_ = '-' if ok is None else 'PASS' if all(oks) else 'miss'
        print(f'{tid:5} {what:{w}}  {band:20} ' + ' '.join(f'{(p[2] + (" *" if p[4] is False else "")):24}' for p in per) + f' {val:30} {res_}')
        out.append(dict(id=tid, what=what, band=band, seeds={str(sd): [p[2], p[4]] for sd, p in zip(seeds, per)}, pooled=[val, ok], result=res_))
    print('(* = this seed misses the band)')
    tkr = [r for r in res if r.get('mode') == 'base' and 'error' not in r]
    for r in tkr:
        print(f'  base {r["boss"]} {r["kind"]} seed {r["seed"]}: intake {r["intake"]:.1f} %/min over {r["ticks_run"]} t, worst {r["worst"]:.1f} %, '
              f'killed {r["killed"]}')
    ph = lambda phase, kind, sigma=0: [r for r in res if r.get('mode') == 'phase' and r['phase'] == phase and r['kind'] == kind and r['sigma'] == sigma and 'error' not in r]   # noqa: E731
    print('\nby agent, pooled (intake %/min, worst 40 t %, groggy / min, U / min, patterns / min, P hits (perfect), N hits (perfect dodge)):')
    for phase in (1, 2):
        for kind, sigma in AGENTS:
            rs = ph(phase, kind, sigma)
            if rs:
                print(f'  P{phase} {kind:8} s{sigma:<3} intake {mean(r["intake"] for r in rs):6.1f}  worst {max(r["worst"] for r in rs):5.1f}  '
                      f'grog {mean(r["grog"] for r in rs):.2f}  U {mean(r["ult"] for r in rs):.2f}  pats/min {mean(r["pats"] / (r["ticks"] / 1200) for r in rs):.1f}  '
                      f'P hits {sum(r["p"] for r in rs)} (pp {sum(r["p_pp"] for r in rs)})  N hits {sum(r["n"] for r in rs)} (pd {sum(r["n_pd"] for r in rs)})  '
                      f'F {sum(r["f"] for r in rs)} (refused {sum(r["f_refused"] for r in rs)})')
    for phase in (1, 2):
        for kind, sigma in (('walker', 0), ('parrier', 1.5)):
            rs = [r for r in ph(phase, kind, sigma) if 'pmix' in r]
            if rs:
                tot = {}
                for r in rs:
                    for k, v in r['pmix'].items():
                        tot[k] = tot.get(k, 0) + v
                mins = sum(r['ticks'] for r in rs) / 1200.0
                print(f'  P{phase} {kind} s{sigma} patterns / min: ' + ' '.join(f'{k} {v / mins:.2f}' for k, v in sorted(tot.items(), key=lambda kv: -kv[1])))
    for r in sorted((r for r in res if r.get('mode') == 'kill' and 'error' not in r), key=lambda r: (r['kind'], r['level'], r['seed'])):
        print(f'  kill {r["kind"]} Lv{r["level"]} seed {r["seed"]}: killed {r["killed"]} fighting {r["fight_s"]:.0f} s, cutscenes {r["cut_s"]:.0f} s, '
              f'intake {r["intake"]:.0f} %/min, groggies {r["grog"]}')
    ch = [r for r in res if r.get('mode') == 'chain' and 'error' not in r]
    bad = [(r['key'], r['phase'], r['p_pp'], r['want'], r['f_refused']) for r in ch if r['p_pp'] != r['want'] or r['f_refused']]
    if bad:
        print('T13 chains not fully parried (key, phase, perfect, P hits, refused):', bad)
    err = [r for r in res if 'error' in r]
    if err:
        print(f'\n{len(err)} run(s) failed:', err[0]['error'], err[0].get('tb', '')[-600:])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dp')
    ap.add_argument('--out', default=str(HERE / 'out'))
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--quick', action='store_true')
    ap.add_argument('--only', default='p1,p2,g,kill,chain,base')
    ap.add_argument('--seeds', default='')
    ap.add_argument('--agents', default='', help='phase agents kind:sigma,... (default: all eight)')
    ap.add_argument('--base', default='', help='a hrfair2.json whose base runs (타키 / the Guardian) are reused')
    ap.add_argument('--table', default='', help='only print the table of an existing hrfair2.json (+ --base)')
    a = ap.parse_args()
    extra = []
    if a.base:
        extra = [r for r in json.loads(Path(a.base).read_text(encoding='utf-8')) if r.get('mode') == 'base']
    if a.table:
        res = json.loads(Path(a.table).read_text(encoding='utf-8'))
        if extra and not any(r.get('mode') == 'base' for r in res):
            res += extra
        table(res)
        return
    seeds = tuple(int(x) for x in a.seeds.split(',')) if a.seeds else None
    agents = tuple((k, float(v) if '.' in v else int(v)) for k, v in (x.split(':') for x in a.agents.split(','))) if a.agents else None
    J = jobs_of(str(Path(a.dp).resolve()), a.quick, set(a.only.split(',')), seeds, agents)
    J.sort(key=lambda j: -(j.get('ticks', 0) + (12000 if j['mode'] in ('kill', 'base') else 0)))   # the long runs first
    print(f'hrfair 2.0 (HB): {len(J)} runs, {a.jobs} at a time', flush=True)
    with Pool(a.jobs) as pool:
        res = []
        for i, r in enumerate(pool.imap_unordered(run, J)):
            res.append(r)
            if (i + 1) % 10 == 0:
                print(f'  {i + 1}/{len(J)}', flush=True)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'hrfair2.json').write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
    table(res + [r for r in extra if not any(x.get('mode') == 'base' for x in res)])


if __name__ == '__main__':
    main()
