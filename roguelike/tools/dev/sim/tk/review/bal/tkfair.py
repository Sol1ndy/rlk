#!/usr/bin/env python3
"""tkfair.py (review R-S5, scratch): the Tachy fairness / balance runs on the sim of record's agent (S:ap/balance/
azfair_core.py, unchanged) driving the S3 TkSim world (S:tk/s3/lib, the same vendored azsim / cmsim md5s), so the numbers
sit next to S:az/vfy/logs/analyze_v.txt (Guardian / Azhdaha, item-less Lv5 player, boss L6 / mid-boss L4 there).

  python3 tkfair.py <dp> <mode> <policy> <dodge> <char> <seed> [n] [lv]
  modes: whole (real HP, intro skipped, until death / n) | p1 | p2 | p3 (100000 HP, n ticks in that phase)
"""
import importlib.util
import json
import sys
from pathlib import Path

S = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad')
sys.dont_write_bytecode = True
sys.path.insert(0, str(S / 'tk/s3/lib'))
import tksim as T  # noqa: E402
import azsim as AZ  # noqa: E402
_spec = importlib.util.spec_from_file_location('azfair_core', S / 'ap/balance/azfair_core.py')
F = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(F)
assert F.Z is AZ
LEAD = int(__import__('os').environ.get('TK_LEAD', '12'))
_call = T.TkSim.call


def _lead_call(self, fid, ctx, macro=None):
    # the human reads the pose: a Tachy melee hazard (made 1 t before its hit, #hzQuiet 1) is perceived LEAD t earlier;
    # modelled by making it LEAD t sooner with LEAD more tell ticks (the area is the one aimed at the lock)
    if fid == 'rlk:mboss/hz/make' and LEAD and (self.sc('#pat', 'tk') or 0) in range(1, 12) and (self.sc('#hzW', 'mb') or 0) <= 2:
        self.setsc('#hzW', 'mb', (self.sc('#hzW', 'mb') or 0) + LEAD)
    return _call(self, fid, ctx, macro)


T.TkSim.call = _lead_call
PHN = {0: 'e', 1: 'p1', 2: 'm1', 3: 't1', 4: 'p2', 5: 'm2', 6: 't2', 7: 'p3', 8: 'd'}


class TkMod(F.Mod):
    def pat(self):
        return self.s.sc('#pat', 'tk') or 0

    def phase(self):
        if (self.s.sc('#mbSt', 'mb') or 0) != 1:
            return 'x'
        return PHN.get(self.s.sc('#ph', 'tk') or 0, '?')

    def transition(self):
        return (self.s.sc('#mbCine', 'mb') or 0) == 1 or (self.s.sc('#ph', 'tk') or 0) in (3, 6)


def run(dp, mode='whole', policy='melee', dodge='walk', char='sword', seed=1, n=3600, lv=6, plv=5):
    big = mode != 'whole'
    reg = json.loads((Path(dp) / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
    b = next(x for x in reg['boss'] if x['id'] == 'tachy')
    hp = 100000 if big else b['hp'] * AZ.LV_HP(lv) // 100
    s, pl = T.setup(dp=dp, hp=hp, lv=lv, seed=seed, player_level=plv)
    s.arena = dict(cx=640.0, cy=201.0, cz=8.0, walk=24.0)
    s.dealt = []
    T.fight(s)
    T.until(s, lambda s: (s.sc('#mbSt', 'mb') or 0) == 1, 400)
    ag = F.Agent(s, pl, policy, dodge, 5, char, level=plv)
    ag.mod = TkMod(s)
    s.pat_fn = ag.mod.pat
    s.ph_fn = ag.mod.phase
    if mode == 'p2':
        T.test_id(s, 30)
        T.until(s, lambda s: T.tk(s, '#ph') == 4, 600)
    elif mode == 'p3':
        T.test_id(s, 31)
        T.until(s, lambda s: T.tk(s, '#ph') == 7, 600)
    s.dmg.clear()
    s.dodges.clear()
    t0 = s.t
    phases = []
    end = 'limit'
    steps = n if big else 12000
    for _ in range(steps):
        phn = ag.mod.phase()
        if not phases or phases[-1][0] != phn:
            phases.append((phn, s.t))
        ag.step()
        T.world(s)
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
                dealt=sum(d[1] for d in s.dealt),
                stats={k: st[k] for k in ('ticks', 'hittable', 'attack', 'swings', 'hits', 'dodge_ticks', 'dashes', 'jumps')},
                pat_ticks=st['pat_ticks'], unavoid=len(st['unavoid']))


if __name__ == '__main__':
    a = sys.argv[1:]
    dp, mode, policy, dodge, char, seed = a[0], a[1], a[2], a[3], a[4], int(a[5])
    n = int(a[6]) if len(a) > 6 else 3600
    lv = int(a[7]) if len(a) > 7 else 6
    out = a[8] if len(a) > 8 else None
    r = run(dp, mode, policy, dodge, char, seed, n, lv)
    txt = json.dumps(r, ensure_ascii=False)
    if out:
        Path(out).write_text(txt)
    lost = sum(d[3] or 0 for d in r['dmg'])
    print(mode, policy, dodge, char, seed, 'ticks', r['ticks'], 'end', r['end'], 'lost %max/min',
          round(100.0 * lost / r['hp'] / max(1e-9, r['ticks'] / 1200), 1), 'deaths', len(r['deaths']), 'phases', r['phases'])
