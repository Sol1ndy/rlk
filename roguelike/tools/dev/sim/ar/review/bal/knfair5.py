#!/usr/bin/env python3
"""knfair5.py (S5: knfair2 + KN_ORB=1, an agent that walks to her heal orbs while bonded, and the real
combat/healorb_tick on every orb each tick; knfair2.py is the S4 copy of S3's knfair.py + mode p2: test 31 = straight to P2, then n ticks of P2 with Q0 first) - (S3, scratch): the 아를레키노 fairness probe on the sim of record's agent (S:ap/balance/azfair_core.py,
unchanged) driving the S3 knsim world (S:ar/s3/lib, the same vendored azsim / cmsim md5s), so the numbers sit next to
S:ap/balance/analysis.txt (Apep P1 melee walk 127.7 %max/min; item-less Lv15 player vs L18) and Tachy's review runs.

  python3 knfair.py <dp> <mode> <policy> <dodge> <char> <seed> [n] [lv] [plv] [out.json]
  modes: p1a | p1b (100000 HP, n ticks in that phase; FN-1 stand-in: x2.5 waits for I1), whole (real HP until death)
The human reads the pose: a quiet hazard made 1 t before its hit is perceived LEAD t earlier (as tkfair, KN_LEAD 12).
"""
import importlib.util
import json
import math
import os
import re
import sys
from pathlib import Path

S = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad')
sys.dont_write_bytecode = True
sys.path.insert(0, str(S / 'ar/s3/lib'))
import knsim as T  # noqa: E402
import azsim as AZ  # noqa: E402
_spec = importlib.util.spec_from_file_location('azfair_core', S / 'ap/balance/azfair_core.py')
F = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(F)
assert F.Z is AZ
LEAD = int(os.environ.get('KN_LEAD', '12'))
_call = T.KnSim.call


def _lead_call(self, fid, ctx, macro=None):
    if fid == 'rlk:mboss/hz/make' and LEAD and 1 <= (self.sc('#pat', 'kn') or 0) <= 49 and (self.sc('#hzW', 'mb') or 0) <= 2:
        self.setsc('#hzW', 'mb', (self.sc('#hzW', 'mb') or 0) + LEAD)
    return _call(self, fid, ctx, macro)


T.KnSim.call = _lead_call
PHN = {0: 'e', 1: 'p1a', 2: 'e70', 3: 'p1b', 4: 't', 5: 'p2', 6: 'd'}


class KnMod(F.Mod):
    def pat(self):
        return self.s.sc('#pat', 'kn') or 0

    def phase(self):
        if (self.s.sc('#mbSt', 'mb') or 0) != 1:
            return 'x'
        return PHN.get(self.s.sc('#ph', 'kn') or 0, '?')

    def transition(self):
        return (self.s.sc('#mbCine', 'mb') or 0) == 1 or (self.s.sc('#ph', 'kn') or 0) in (4,)


def api_whatif(s, patch):
    """What-if probe (sim only, nothing written): patch api tables in memory ({"WEIGHTS": {"Q1": {"p2": [n, m, f]}},
    "COOLDOWN": {"Q1": 200}, "DMG": {...}}), rebuild every module function text with capture writers and put the changed
    ones into the sim's function cache."""
    import types
    from mboss_arlecchino import api, core, ai, bond, p1, p2, seq
    for tab, upd in patch.items():
        if tab == 'Q5B_PM':                    # S5: the Q5B final's per mille (api.HITS q5b 'final' dims[1])
            api.HITS['q5b'] = [h if h[1] != 'final' else h[:3] + ((h[3][0], int(upd)),) + h[4:] for h in api.HITS['q5b']]
            continue
        if not isinstance(upd, dict):          # S5: a scalar (BOL_REHIT_PCT, P2_MUL, ...)
            setattr(api, tab, upd)
            continue
        d = getattr(api, tab)
        for k, v in upd.items():
            if isinstance(v, dict):
                d[k] = dict(d.get(k, {}), **{c: tuple(x) for c, x in v.items()})
            else:
                d[k] = v

    class CapW:
        def __init__(self):
            self.files = {}
            self.out = types.SimpleNamespace(written=set())

        def w(self, rel, body):
            self.files[rel] = body
            self.out.written.add((api.L.FN / f'{api.ROOT}/{rel}.mcfunction').resolve())
    W3, W4, W2 = CapW(), CapW(), CapW()
    pats = []
    for mod, Wr in ((p1, W3), (p2, W4)):
        for p in mod.PATTERNS:
            p.build(Wr)
            pats.append(p)
    for sv in seq.SERVICES:
        sv.build(W2)
    ctx = core.Ctx(pats, W4, seq.SERVICES)
    ai.build(W3, ctx)
    bond.build(W3, ctx)
    core.build(W3, ctx)
    n = 0
    for Wr in (W3, W4, W2):
        for rel, body in Wr.files.items():
            lines = [ln for ln in body if ln and not ln.startswith('#')]
            s.cache[f'rlk:boss/arlecchino/{rel}'] = lines
            n += 1
    return n


ORB = os.environ.get('KN_ORB') == '1'
_strike = AZ.strike


def _strike_na(s, target, dmg, elem=0, ranged=False, basic=True, crit=0):
    """azsim.strike with the real normal-attack flag: combat/find_immediate (melee) and char/bow/na_shot set #icd 1 for
    every normal attack, physical ones too (azsim sets it only for elemental hits); 선혈의 충격 reads it (on_hit)."""
    pl = s.player()
    real = s.setsc

    def setsc(who, obj, v):
        if who == '#icd' and obj == 'tmp' and basic:
            v = 1
        return real(who, obj, v)
    s.setsc = setsc
    try:
        return _strike(s, target, dmg, elem, ranged, basic, crit)
    finally:
        s.setsc = real


AZ.strike = _strike_na


class OrbAgent(F.Agent):
    """KN_ORB=1: while the player carries a bond (the HUD's 생명의 계약), walk to the nearest heal orb (dodging first, as
    the base agent: dodge_step runs before position)."""
    def position(self, tg, star, soon, hold, ph):
        if ORB and (self.s.sc(('e', self.player.id), 'bol') or 0) > 0:
            orbs = [e for e in self.s.ents if e.alive and 'rlk_healorb' in e.tags]
            if orbs:
                x0, z0 = self.pos()
                o = min(orbs, key=lambda e: math.hypot(e.pos[0] - x0, e.pos[2] - z0))
                self.stats['orb_walk'] = self.stats.get('orb_walk', 0) + 1
                return self.step_toward(o.pos[0], o.pos[2], soon) or True
        return super().position(tg, star, soon, hold, ph)


def orb_tick(s):
    """rlk:tick:61 for the heal orbs (the sim's world() runs only the fight parts): landed on the floor, absorbed within 1.6 b."""
    for e in [e for e in s.ents if e.alive and 'rlk_healorb' in e.tags]:
        e.pos[1] = 201.0
        s.call('rlk:combat/healorb_tick', T.Ctx(e, tuple(e.pos), tuple(e.rot)))
        if not e.alive:
            s.orbs_taken = getattr(s, 'orbs_taken', 0) + 1
    s.ents = [e for e in s.ents if e.alive]


def run(dp, mode='p1a', policy='melee', dodge='walk', char='sword', seed=1, n=3600, lv=18, plv=15):
    big = mode != 'whole'
    reg = json.loads((Path(dp) / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
    b = next(x for x in reg['boss'] if x['id'] == 'arlecchino')
    hp = 100000 if big else b['hp'] * AZ.LV_HP(lv) // 100
    s, pl = T.setup(dp=dp, hp=hp, lv=lv, seed=seed, player_level=plv)
    s.arena = dict(cx=760.0, cy=201.0, cz=8.0, walk=26.0)
    s.dealt = []
    T.fight(s)
    T.until(s, lambda s: (s.sc('#mbSt', 'mb') or 0) == 1, 400)
    if os.environ.get('KN_API'):
        api_whatif(s, json.loads(os.environ['KN_API']))
    if os.environ.get('KN_PMX') == '1':
        # what-if (S5): per-mille Bond-of-Life hazards ignore #mbBolRe (the event / bond stay)
        lines = s.load('rlk:mboss/hz/hurt_pm_bol')
        s.cache['rlk:mboss/hz/hurt_pm_bol'] = [ln for ln in lines if '#mbDotPct mb *= #mbBolRe' not in ln
                                               and '#mbDotPct mb /= #c100' not in ln]
    for kv in filter(None, os.environ.get('KN_PATCH', '').split(',')):
        # what-if probe (sim only, never shipped): a group's cooldown, e.g. Q1=240 -> core/start/q1 adds 240 to #cd_Q1
        g, v = kv.split('=')
        for key in [k for k, gg in (('q1', 'Q1'), ('q2', 'Q2'), ('q4', 'Q4'), ('q6', 'Q6'), ('q3', 'Q3')) if gg == g]:
            fid = f'rlk:boss/arlecchino/core/start/{key}'
            f = Path(dp) / f'data/rlk/function/boss/arlecchino/core/start/{key}.mcfunction'
            lines = [ln for ln in f.read_text(encoding='utf-8').split('\n') if ln and not ln.startswith('#')]
            s.cache[fid] = [re.sub(rf'(add #cd_{g} kn )\d+', rf'\g<1>{v}', ln) for ln in lines]
    if os.environ.get('KN_DMGMUL'):
        # what-if probe: every hit's dmgMul (the registry's 150) scaled, as a uniform tier change would
        s.setsc('#mbDmgMul', 'mb', int(os.environ['KN_DMGMUL']))
    ag = OrbAgent(s, pl, policy, dodge, 5, char, level=plv)
    ag.mod = KnMod(s)
    s.pat_fn = ag.mod.pat
    s.ph_fn = ag.mod.phase
    if mode == 'p1b':
        T.test_id(s, 30)
    if mode == 'p2':
        T.test_id(s, 31)
    s.dmg.clear()
    s.dodges.clear()
    t0 = s.t
    phases = []
    end = 'limit'
    steps = n if big else 20000
    for _ in range(steps):
        phn = ag.mod.phase()
        if not phases or phases[-1][0] != phn:
            phases.append((phn, s.t))
        st0 = s.sc('#stun', 'kn') or 0
        ag.step()
        T.world(s)
        orb_tick(s)
        if not st0 and (s.sc('#stun', 'kn') or 0):
            s.breaks = getattr(s, 'breaks', 0) + 1
        if not big and (T.body(s) is None or (s.sc('#mbSt', 'mb') or 0) in (2, 3)):
            end = 'dead'
            break
    phases.append(('end', s.t))
    dur = {}
    for i in range(len(phases) - 1):
        dur[phases[i][0]] = dur.get(phases[i][0], 0) + phases[i + 1][1] - phases[i][1]
    hpmax = s.sc(('e', pl.id), 'maxHealth')
    st = ag.stats
    return dict(mode=mode, policy=policy, dodge=dodge, char=char, seed=seed, lv=lv, plv=plv, ticks=s.t - t0, end=end,
                phases=dur, hp=hpmax, dmg=[list(d) for d in s.dmg], deaths=list(st['deaths']),
                dealt=sum(d[1] for d in s.dealt), pat_ticks=st['pat_ticks'], unavoid=len(st['unavoid']),
                orbs=getattr(s, 'orbs_taken', 0), orb_walk=st.get('orb_walk', 0), brk=getattr(s, 'breaks', 0))


if __name__ == '__main__':
    a = sys.argv[1:]
    dp, mode, policy, dodge, char, seed = a[0], a[1], a[2], a[3], a[4], int(a[5])
    n = int(a[6]) if len(a) > 6 else 3600
    lv = int(a[7]) if len(a) > 7 else 18
    plv = int(a[8]) if len(a) > 8 else 15
    out = a[9] if len(a) > 9 else None
    r = run(dp, mode, policy, dodge, char, seed, n, lv, plv)
    if out:
        Path(out).write_text(json.dumps(r, ensure_ascii=False))
    lost = sum(d[3] or 0 for d in r['dmg'])
    bypat = {}
    for d in r['dmg']:
        bypat[d[4]] = bypat.get(d[4], 0) + (d[3] or 0)
    print(mode, policy, dodge, char, seed, 'ticks', r['ticks'], 'end', r['end'], 'lost %max/min',
          round(100.0 * lost / r['hp'] / max(1e-9, r['ticks'] / 1200), 1), 'deaths', len(r['deaths']),
          'by pat', {k: round(100.0 * v / r['hp'], 1) for k, v in sorted(bypat.items(), key=lambda x: -x[1])})
