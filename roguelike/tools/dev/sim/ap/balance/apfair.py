#!/usr/bin/env python3
"""apfair.py: the Apep fairness agent (plan 9.7 / 12.4; AP-FIX RV-03; scratch tool, never shipped).

The agent is AZ's sim of record (S:az/harness/azfair.py, vendored unchanged as azfair_core.py, md5 in README.md): its
threat reading of every framework hazard kind, escape search, jump planning (#hzY1 bands), dash timing, i-frames,
knockback, the N4 safe circles (kind-6 masks + rlk_mb_hzsafe), moving discs, push capsules and death handling (refill +
record, as azfair). It drives the Apep world of the AP harness (ap/tests/lib/apsim.py on the vendored S1-HARN sims;
azfair's `import azsim` resolves to that vendored copy, so the same engine functions run as in every Apep suite).

Apep parts (ApAgent / ApMod):
- the player: item-less Lv15 (plan 9.1: HP 268, def 38, atk 38) vs L18; characters = azfair's CHARS (= the plan model
  p2sim_rev's: sword [6, 10] t x [1.0, 1.2], bow 8 t x 1.0, catalyst [10, 10, 10, 16] t); `mult` scales atk (items x1.75,
  the strongest bow x2.5); attack element per character (sword 0, bow 1 Pyro, catalyst 8);
- phases 1 / 3: the nearest vulnerable hit proxy (azfair); positional policies melee_front / melee_back use the plan 7.3
  zones (FRONT f >= 3 and |s| <= 4 + 0.6 (f - 3); BACK f < -3) in the anchor frame;
- phase 2 (the revival stage; the body parked): targets are organisms (husks rlk_mb_ap_org, not emerging rlk_mb_inv, not
  spent): agent `plan` = the plan priorities 수호 > buffed basics > 파괴 > basics (nearest within the best class), `nearest` =
  the nearest organism that is not immune (rlk_mb_ap_imm; RV-03), `idle` = no attacks, stands at the arena spawn side;
  melee cleave (every other organism within reach in the front 180 deg, F:combat/find_immediate, as p2sim_rev);
  the 둥지 walls (barrier blocks) are collision for walks and dashes;
- 종말의 여파 (Q2, id 32): q2mode `dome` walks to the nearest footprint at the banner and stays inside until the pop;
  `late` ignores the Q2 masks until dome 1 + 40 t (fix 10-22f: the domes form on the pattern clock, dome 1 at #apPT 34,
  so #apPT 74; was aftermath t94), then walks to the nearest dome; `early` leaves its dome at the blast (t156) and
  ignores the Q2 masks after; `none` = azfair's own escape (masks within 40 t);
- records per run: phase lengths, every player damage event (azsim s.dmg: t, pct, el, HP lost, pattern, phase, nododge,
  src), dodges, dealt, deaths, Heart failures, the Heart curve (P2), Q2 casts (ticks / blast hits per cast), agent stats.

    python3 apfair.py <datapack root> <mode> [policy] [dodge] [agent] [seed] [char] [mult] [n] [q2mode]
    modes: whole (real HP, E .. D) | p1 / p3 (100000 HP, n ticks of the phase) | p2 (real HP, test 20 -> the stage end)
           | q2 (100000 HP, phase 3, casts: test 32 then 37 x (n // 300)) | gd (the Guardian calibration, azfair.fight)
"""
import importlib.util
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = HERE.parent.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(S / 'ap/tests/lib'))
import apsim as P  # noqa: E402
import azsim as AZ  # noqa: E402

_spec = importlib.util.spec_from_file_location('azfair_core', HERE / 'azfair_core.py')
F = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(F)
assert F.Z is AZ, 'azfair_core must run on the vendored azsim of the AP harness'

PLAYER = dict(level=15, hp=268, defence=38, atk=38)
CONTRACT = dict(ph='#apPh', pid='#apPid', tr='#apTr', heart='#apHt', fail='#apFail', wave='#apWave', cine='#mbCine',
                org_tag='rlk_mb_ap_org', inv='rlk_mb_inv', spent='rlk_mb_ap_spent', immune='rlk_mb_ap_imm',
                buff='rlk_mb_ap_buff', kinds={'guard': 'rlk_mb_ap_guard', 'destr': 'rlk_mb_ap_destr', 'nurt': 'rlk_mb_ap_nurt',
                                              'nest': 'rlk_mb_ap_nest', 'pred': 'rlk_mb_ap_pred', 'basic': 'rlk_mb_ap_basic'},
                q2_pid=32, q2_clock='#apq32', q2_fp='rlk_mb_ap_p32f', q2_hz='rlk_mb_ap_p32h', dome='rlk_mb_ap_dome')
PHN = {0: 'e', 1: 'p1', 15: 't1', 2: 'p2', 25: 'cs', 3: 'p3', 9: 'd'}
ARENA = dict(cx=440.0, cy=201.0, cz=8.0, walk=26.0)
Q2T = dict(dome1_pt=34, late_pt=74, ticks_pt=20, blast=156, window_end=176, pop=189, dome_r=4.5)   # fix 10-22f (#apPT / clip)
WALK, SPRINT, SWING = F.WALK, F.SPRINT, F.SWING


class ApMod(F.Mod):
    def is_az(self):
        return False

    def name(self):
        return 'apep'

    def pat(self):
        return self.s.sc(CONTRACT['pid'], 'mb') or 0

    def phase(self):
        s = self.s
        if (s.sc('#mbSt', 'mb') or 0) != 1:
            return 'x'
        ph = s.sc(CONTRACT['ph'], 'mb')
        return PHN.get(ph, 'x%s' % ph)

    def transition(self):
        return (self.s.sc(CONTRACT['cine'], 'mb') or 0) == 1

    def branded(self, pl):
        return False


class ApAgent(F.Agent):
    def __init__(self, s, player, policy='melee', dodge='walk', react=5, char='sword', agent='plan', mult=1.0,
                 q2mode='dome', sprint=False):
        super().__init__(s, player, policy, dodge, react, char, sprint=sprint, level=PLAYER['level'], shards=False)
        self.mod = ApMod(s)
        s.pat_fn = self.mod.pat
        s.ph_fn = self.mod.phase
        self.atk = max(1, int(round(PLAYER['atk'] * mult)))
        self.agent, self.q2mode = agent, q2mode
        self.q2_left = False
        self.stats.update(org_hits=0, org_swings=0, cleave=0, q2_walk=0, wall_blocks=0)

    # -- the Apep world
    def ph(self):
        return self.s.sc(CONTRACT['ph'], 'mb')

    def blocked(self, x, z):
        b = self.s.blocks.get((math.floor(x), 201, math.floor(z)))
        return b is not None and 'barrier' in str(b)

    def zone(self, x, z):
        """plan 7.3 (P1 and the P3 crawl) in the anchor frame (f along the facing, s sideways)."""
        f, sd = self.frame(x, z)
        if f >= 3.0 and abs(sd) <= 4 + 0.6 * (f - 3.0):
            return 'front'
        if f < -3.0:
            return 'back'
        return 'side' if abs(sd) > 3.0 else 'under'

    def hittable(self):
        if self.ph() == 2:
            return True, AZ.body_of(self.s)
        return super().hittable()

    def orgs(self):
        s = self.s
        return [e for e in s.ents if e.alive and e.etype == 'husk' and CONTRACT['org_tag'] in e.tags
                and CONTRACT['inv'] not in e.tags and CONTRACT['spent'] not in e.tags and 'rlk_mb_dying' not in e.tags]

    def targets(self):
        if self.ph() != 2:
            return super().targets()
        if self.agent == 'idle':
            return []
        K = CONTRACT['kinds']
        orgs = self.orgs()
        if self.agent == 'nearest':
            return [(e, 'org', 'org', 0.45) for e in orgs if CONTRACT['immune'] not in e.tags]

        def prio(e):
            if K['guard'] in e.tags:
                return 0
            if CONTRACT['buff'] in e.tags and CONTRACT['immune'] not in e.tags:
                return 1
            if K['destr'] in e.tags:
                return 2
            if CONTRACT['immune'] in e.tags:
                return 9
            return 3
        if not orgs:
            return []
        best = min(prio(e) for e in orgs)
        return [(e, 'org', 'org', 0.45) for e in orgs if prio(e) == best and best < 9]

    def tdist(self, t, x, z, y=None):
        if t[2] == 'org':
            return max(0.0, math.hypot(t[0].pos[0] - x, t[0].pos[2] - z) - t[3])
        return super().tdist(t, x, z, y)

    # -- moves: the 둥지 walls are collision
    def walk_to(self, x, z, v):
        pl = self.player
        x0, z0 = self.pos()
        d = math.hypot(x - x0, z - z0)
        if d < 1e-6:
            return
        st = min(v, d)
        nx, nz = self.clampw(x0 + (x - x0) / d * st, z0 + (z - z0) / d * st)
        if self.blocked(nx, nz):
            self.stats['wall_blocks'] += 1
            return
        pl.pos[0], pl.pos[2] = nx, nz

    def step_toward(self, gx, gz, soon, stop=0.0):
        pl = self.player
        x0, z0 = self.pos()
        d = math.hypot(gx - x0, gz - z0)
        if d <= stop + 1e-6:
            return False
        v = SPRINT if self.atkcd == 0 else SWING
        st = min(v, d - stop)
        caps = self.capsules()
        ux, uz = (gx - x0) / d, (gz - z0) / d
        for a in (0, 30, -30, 60, -60, 90, -90):
            c, sn = math.cos(math.radians(a)), math.sin(math.radians(a))
            nx, nz = self.clampw(x0 + (ux * c - uz * sn) * st, z0 + (ux * sn + uz * c) * st)
            if self.blocked(nx, nz):
                continue
            if self.safe_at(soon, nx, nz, pad=0.3) and not self.in_capsule(nx, nz, caps):
                pl.pos[0], pl.pos[2] = nx, nz
                return True
            if not caps and a == 0 and not self.blocked(nx, nz):
                break
        return False

    def do_dash(self, direction):
        x0, z0 = self.pos()
        ok = super().do_dash(direction)
        if ok and self.blocked(*self.pos()):
            self.player.pos[0], self.player.pos[2] = x0, z0
            self.dash_left = 0
        return ok

    def step(self):
        s = self.s
        # the dash's continuation must not cross a wall either
        if self.dash_left > 0:
            x, z = self.clampw(self.player.pos[0] + self.dash_dir[0], self.player.pos[2] + self.dash_dir[1])
            if self.blocked(x, z):
                self.dash_left = 0
        self._q2goal = self.q2_goal() if self.dodge != 'none' else None
        self._q2moved = False
        ret = super().step()
        if self._q2goal is not None and not self._q2moved and self.dash_left == 0:
            self.q2_walk(self._q2goal)       # no target in reach / no threat at the feet: still walk to the dome
        P.C.moved(s)
        return ret

    # -- 종말의 여파 behaviour
    def q2(self):
        s = self.s
        if self.mod.pat() != CONTRACT['q2_pid']:
            self.q2_left = False
            return None
        fps = [e for e in s.ents if e.alive and CONTRACT['q2_fp'] in e.tags]
        if not fps:
            return None
        return fps, s.sc(CONTRACT['q2_clock'], 'mb'), s.sc('#apPT', 'mb')

    def q2_goal(self):
        """The dome (footprint) the Q2 agent walks to, or None (the mode does not act now)."""
        q = self.q2()
        if q is None or self.q2mode == 'none':
            return None
        fps, clk, pt = q
        clk = clk if clk is not None else -999
        if self.q2mode == 'late' and (pt if pt is not None else -999) < Q2T['late_pt']:
            return None
        if self.q2mode == 'early' and clk >= Q2T['blast']:
            self.q2_left = True
            return None
        x0, z0 = self.pos()
        return min(fps, key=lambda e: math.hypot(e.pos[0] - x0, e.pos[2] - z0))

    def ignore_q2_masks(self):
        q = self.q2()
        if q is None:
            return False
        pt = q[2] if q[2] is not None else -999
        return (self.q2mode == 'late' and pt < Q2T['late_pt']) or (self.q2mode == 'early' and self.q2_left)

    def dodge_step(self, cur, ths, now, y):
        if self.ignore_q2_masks():
            cur = [t for t in cur if not (t.src is not None and CONTRACT['q2_hz'] in t.src.tags)]
            ths = [t for t in ths if not (t.src is not None and CONTRACT['q2_hz'] in t.src.tags)]
            if not cur:
                return False
        goal = getattr(self, '_q2goal', None)
        if goal is not None:
            # inside the chosen dome nothing else matters (the masks spare it); walking there beats the generic search
            return self.q2_walk(goal)
        return super().dodge_step(cur, ths, now, y)

    def q2_walk(self, goal):
        self._q2moved = True
        x0, z0 = self.pos()
        d = math.hypot(goal.pos[0] - x0, goal.pos[2] - z0)
        if d > Q2T['dome_r'] - 1.2:
            v = SPRINT if self.atkcd == 0 else SWING
            self.walk_to(goal.pos[0], goal.pos[2], v)
            self.stats['q2_walk'] += 1
        return True

    def position(self, tg, star, soon, hold, ph):
        goal = getattr(self, '_q2goal', None)
        if goal is not None:
            return self.q2_walk(goal)
        if self.q2_left and self.q2mode == 'early':
            # the early leaver steps out of its dome (away from the dome centre) and stays out
            q = self.q2()
            if q:
                x0, z0 = self.pos()
                fp = min(q[0], key=lambda e: math.hypot(e.pos[0] - x0, e.pos[2] - z0))
                d = math.hypot(x0 - fp.pos[0], z0 - fp.pos[2])
                if d < Q2T['dome_r'] + 1.5:
                    dx, dz = (x0 - fp.pos[0], z0 - fp.pos[2]) if d > 1e-3 else (1.0, 0.0)
                    n = math.hypot(dx, dz)
                    self.walk_to(x0 + dx / n * 3, z0 + dz / n * 3, SPRINT)
                    return True
        if self.ph() == 2:
            return self.position_p2(tg, soon)
        if self.policy in ('melee_front', 'melee_back'):
            # plan 9.7 "FRONT-mid melee walker vs BACK melee walker": FRONT at the mid band (anchor distance >= 7.6 b,
            # hitting the hood proxy from 2.9-3.3 b off its surface; plan 7.3 bands), BACK behind the hips (f < -3)
            want = min(2.5, self.ch['reach'] - 1.0)
            if self.policy == 'melee_front':
                a = self.anchor()
                far = lambda x, z: a is None or math.hypot(x - a.pos[0], z - a.pos[2]) >= 7.6    # noqa: E731
                g = self.goal_mid(soon, far)
                if g is None:
                    g = self.goal_point((), lambda zn: zn == 'front', want, soon)
            else:
                g = self.goal_point((), lambda zn: zn == 'back', want, soon)
                if g is None:
                    g = self.goal_point((), lambda zn: zn == 'back', want + 1.0, soon)
            if g is not None and g[0] > 0.3:
                self.step_toward(g[1], g[2], soon)
            return False
        return super().position(tg, star, soon, hold, ph)

    def goal_mid(self, soon, far):
        x0, z0 = self.pos()
        caps = self.capsules()
        best = None
        for t in self.targets():
            e, n, kind, hw = t
            if kind != 'px':
                continue
            for ri in (2.9, 3.1, 3.3):
                r = hw + ri
                for i in range(36):
                    a = 2 * math.pi * i / 36
                    x, z = self.clampw(e.pos[0] + r * math.cos(a), e.pos[2] + r * math.sin(a))
                    if self.zone(x, z) != 'front' or not far(x, z):
                        continue
                    if self.in_capsule(x, z, caps) or not self.safe_at(soon, x, z, pad=0.3):
                        continue
                    d = math.hypot(x - x0, z - z0)
                    if best is None or d < best[0]:
                        best = (d, x, z)
        return best

    def position_p2(self, tg, soon):
        if not tg or self.policy == 'stand':
            return False
        x0, z0 = self.pos()
        t = min(tg, key=lambda t: self.tdist(t, x0, z0))
        e = t[0]
        d = self.tdist(t, x0, z0)
        if not self.ch['ranged']:
            want = min(2.5, self.ch['reach'] - 1.0)
            if d > want:
                self.step_toward(e.pos[0], e.pos[2], soon, stop=t[3] + want)
            return False
        dd = math.hypot(e.pos[0] - x0, e.pos[2] - z0)
        if dd < 8.0 or dd > 11.0:
            sgn = -1 if dd < 8.0 else 1
            v = SWING if self.atkcd > 0 else WALK
            nx, nz = self.clampw(x0 + (e.pos[0] - x0) / max(dd, 1e-6) * v * sgn, z0 + (e.pos[2] - z0) / max(dd, 1e-6) * v * sgn)
            if math.hypot(nx - x0, nz - z0) < 0.05 and sgn < 0:
                tx, tz = -(e.pos[2] - z0) / max(dd, 1e-6), (e.pos[0] - x0) / max(dd, 1e-6)
                nx, nz = self.clampw(x0 + tx * v, z0 + tz * v)
            if (self.safe_at(soon, nx, nz, pad=0.3) and not self.in_capsule(nx, nz, self.capsules())
                    and not self.blocked(nx, nz)):
                self.player.pos[0], self.player.pos[2] = nx, nz
        return False

    def strike(self, t, coef, ph):
        if t[2] != 'org':
            return super().strike(t, coef, ph)
        s, st = self.s, self.stats
        dmg = max(1, self.atk * coef // 100)
        e = t[0]
        hits = [e]
        if not self.ch['ranged']:
            # melee cleave (F:combat/find_immediate): every other organism within reach in the front 180 deg
            x0, z0 = self.pos()
            fx, fz = e.pos[0] - x0, e.pos[2] - z0
            for o in self.orgs():
                if o is e:
                    continue
                ox, oz = o.pos[0] - x0, o.pos[2] - z0
                if math.hypot(ox, oz) - 0.45 <= self.ch['reach'] and ox * fx + oz * fz >= 0:
                    hits.append(o)
            st['cleave'] += len(hits) - 1
        st['org_swings'] += 1
        for o in hits:
            landed, _, _ = AZ.strike(s, o, dmg, elem=self.ch['el'], ranged=self.ch['ranged'])
            if landed:
                st['org_hits'] += 1
                s.dealt.append([s.t + 1, dmg, ph, s.pat_fn(), 'org'])


# ------------------------------------------------------------------------------------------- one run
def setup(dp, seed, hp):
    s, pl = P.setup(dp, hp=hp, seed=seed, player_level=PLAYER['level'])
    for o, v in (('curHealth', PLAYER['hp']), ('maxHealth', PLAYER['hp']), ('def', PLAYER['defence']), ('atk', PLAYER['atk'])):
        s.setsc(('e', pl.id), o, v)
    s.arena = dict(ARENA)
    s.dealt = []
    return s, pl


def run(dp, mode='whole', policy='melee', dodge='walk', agent='plan', seed=1, char='sword', mult=1.0, n=3600,
        q2mode='dome', react=5, limit=16000):
    dp = Path(dp)
    if mode == 'gd':
        return run_gd(dp, policy, dodge, seed, char, n)
    big = mode in ('p1', 'p3', 'q2')
    s, pl = setup(dp, seed, 100000 if big else 7235)
    P.fight(s)
    P.until(s, lambda s: (s.sc('#mbSt', 'mb') or 0) == 1, 400)
    ag = ApAgent(s, pl, policy, dodge, react, char, agent, mult, q2mode)
    if mode == 'p3' or mode == 'q2':
        P.until(s, lambda s: P.ph(s) == 1 and P.ap(s, '#apPT') is not None, 300)
        P.test_id(s, 30)
        P.until(s, lambda s: P.ph(s) == 3, 600)
    elif mode == 'p2':
        P.until(s, lambda s: P.ph(s) == 1 and P.ap(s, '#apPT') is not None, 300)
        P.test_id(s, 20)
        P.until(s, lambda s: P.ph(s) == 2, 300)
    elif mode == 'p1':
        P.until(s, lambda s: P.ph(s) == 1, 300)
    s.dmg.clear()
    s.dodges.clear()
    t0 = s.t
    phases, heart, casts, fail_t = [], [], [], []
    nfail = P.ap(s, CONTRACT['fail']) or 0
    cast = None
    q2_casts = (n // 300) if mode == 'q2' else 0
    ids = [32] + [37] * max(0, q2_casts - 1)
    end_reason = 'limit'
    steps = n if mode in ('p1', 'p3') else (limit if mode != 'q2' else 300 * max(1, q2_casts) + 200)
    for i in range(steps):
        ph = P.ph(s)
        phn = ag.mod.phase()
        if not phases or phases[-1][0] != phn:
            phases.append((phn, s.t))
        if ph == 2 and s.t % 20 == 0:
            heart.append((s.t, P.ap(s, CONTRACT['heart'])))
        if mode == 'q2':
            pid = P.pid(s)
            if pid != 32 and ids and (cast is None or cast.get('end')) and (P.ap(s, '#apPid') or 0) == 0:
                k = ids.pop(0)
                # each cast from a seeded spot 10-22 b from the centre (the dome walk has to mean something)
                rng = __import__('random').Random(seed * 101 + len(casts))
                a, rr = rng.uniform(0, 2 * math.pi), rng.uniform(10.0, 22.0)
                P.place_player(s, ARENA['cx'] + rr * math.cos(a), ARENA['cz'] + rr * math.sin(a))
                s.setsc(('e', pl.id), 'curHealth', PLAYER['hp'])
                P.test_id(s, k)
                cast = dict(id=k, t0=s.t, ticks=0, blast=0, deaths0=len(ag.stats['deaths']), dmg0=len(s.dmg), hp0=None)
                casts.append(cast)
            if cast is not None and not cast.get('end'):
                if pid == 32 and cast['hp0'] is None:
                    cast['hp0'] = s.sc(('e', pl.id), 'curHealth')
                if pid != 32 and s.t > cast['t0'] + 5:
                    cast['end'] = s.t
            if not ids and cast is not None and cast.get('end'):
                end_reason = 'casts'
                break
        n0 = len(s.dmg)
        clk = P.ap(s, CONTRACT['q2_clock']) if P.pid(s) == 32 else None
        ag.step()
        P.world(s)
        if cast is not None and not cast.get('end') and clk is not None:
            for d in s.dmg[n0:]:
                if d[3] or d[1]:
                    if clk >= Q2T['blast'] - 2:
                        cast['blast'] += 1
                    else:
                        cast['ticks'] += 1
        nf = P.ap(s, CONTRACT['fail']) or 0
        if nf > nfail:
            fail_t.append(s.t - t0)
            nfail = nf
            if mode == 'p2' and (agent == 'idle' or nf >= 2):
                end_reason = 'fail' if nf < 2 else 'lost'
                break
        if mode == 'p2' and phn != 'p2' and len(phases) > 1 and phases[-2][0] == 'p2':
            end_reason = 'stage_end'
            break
        if mode == 'whole' and (P.body(s) is None or (s.sc('#mbSt', 'mb') or 0) in (2, 3)):
            end_reason = 'dead' if P.body(s) is None or (s.sc('#mbSt', 'mb') or 0) == 2 else 'lost'
            break
    phases.append(('end', s.t))
    dur = {}
    for i in range(len(phases) - 1):
        k = str(phases[i][0])
        dur[k] = dur.get(k, 0) + phases[i + 1][1] - phases[i][1]
    for c in casts:
        c['deaths'] = len(ag.stats['deaths']) - c.pop('deaths0')
        c.pop('dmg0', None)
    st = ag.stats
    return dict(mode=mode, policy=policy, dodge=dodge, agent=agent, seed=seed, char=char, mult=mult, q2mode=q2mode,
                ticks=s.t - t0, phases=dur, end=end_reason, dmg=[list(d) for d in s.dmg], dodges=[list(d) for d in s.dodges],
                dealt=[list(d) for d in s.dealt], deaths=list(st['deaths']), fails=P.ap(s, CONTRACT['fail']) or 0, fail_t=fail_t,
                lost=P.ap(s, '#mbLost') or 0, heart=heart, casts=casts, hp=PLAYER['hp'],
                stats={k: st[k] for k in ('ticks', 'hittable', 'attack', 'swings', 'hits', 'dodge_ticks', 'dashes', 'jumps',
                                          'inreach', 'nd_dash', 'hold_ticks', 'org_hits', 'org_swings', 'cleave', 'q2_walk',
                                          'wall_blocks')},
                ph_ticks=st['ph_ticks'], zone_ticks=st['zone_ticks'], pat_ticks=st['pat_ticks'],
                unavoid=len(st['unavoid']), walk_fail=len(st['walk_fail']))


def run_gd(dp, policy, dodge, seed, char, n):
    """The Guardian calibration on this harness (azfair.fight on the vendored azsim with the datapack under test):
    the Lv4 item-less player vs L4, as plan 9.7 states the Guardian reference."""
    s, ag, tr, t0 = F.fight('guardian', policy, dodge, 5, n, seed, 4, char, dp=str(dp))
    hp = s.sc(('e', ag.player.id), 'maxHealth')
    return dict(mode='gd', policy=policy, dodge=dodge, agent='-', seed=seed, char=char, mult=1.0, q2mode='-', ticks=s.t - t0,
                phases={'gd': s.t - t0}, end='limit', dmg=[list(d) for d in s.dmg], dodges=[list(d) for d in s.dodges],
                dealt=[list(d) for d in s.dealt], deaths=list(ag.stats['deaths']), fails=0, lost=0, heart=[], casts=[], hp=hp,
                stats={k: ag.stats[k] for k in ('ticks', 'hittable', 'attack', 'swings', 'hits', 'dodge_ticks', 'dashes',
                                                'jumps', 'inreach', 'nd_dash', 'hold_ticks')},
                ph_ticks=ag.stats['ph_ticks'], zone_ticks=ag.stats['zone_ticks'], pat_ticks=ag.stats['pat_ticks'],
                unavoid=len(ag.stats['unavoid']), walk_fail=len(ag.stats['walk_fail']))


def summary(r):
    hp = r['hp']
    lost = {}
    for d in r['dmg']:
        lost[str(d[5])] = lost.get(str(d[5]), 0) + (d[3] or 0)
    out = {k: v for k, v in r.items() if k not in ('dmg', 'dodges', 'dealt', 'heart')}
    out['lost'] = lost
    out['pct_per_min'] = {k: round(100.0 * v / hp / max(1e-9, r['phases'].get(k, 0) / 1200.0), 1)
                          for k, v in lost.items() if r['phases'].get(k)}
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    dp = a[0] if a else str(P.DEFAULT_DP)
    mode = a[1] if len(a) > 1 else 'p1'
    kw = dict(mode=mode)
    names = ['policy', 'dodge', 'agent', 'seed', 'char', 'mult', 'n', 'q2mode']
    conv = dict(seed=int, mult=float, n=int)
    for nm, v in zip(names, a[2:]):
        kw[nm] = conv.get(nm, str)(v)
    r = run(dp, **kw)
    print(json.dumps(summary(r), ensure_ascii=False)[:3000])
