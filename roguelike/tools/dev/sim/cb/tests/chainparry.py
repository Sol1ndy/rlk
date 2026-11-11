#!/usr/bin/env python3
"""chainparry.py: every parryable hit of every chained attack can be answered with a perfect parry (round W, lane WP; the user,
11-12: 「연속으로 공격하는 패턴을 이론상 전부 패링할 수 있어야 해」).

    python3 chainparry.py <datapack root> [boss ...] [--json=<file>]      (from a copy of tools/dev/sim outside the datapack)

An ideal parrier presses F (through the REAL player/f_key at the head of the tick, #now = that tick) one tick before every
parryable hit - and on the hit's own tick when the hit before it was only one tick earlier (a press is spent on one tick's
hits; the lock after a parry is #parChain = 1 tick, so the press of tick h + 1 is taken). The hit ticks come from a first run
with the player standing in reach (the scripted patterns are deterministic for a seed); the run is repeated with the presses
until the set of parryable hit ticks is stable (a parried hit can change what follows: balance pips, a shield segment).
Parryable = judged with #hcNP 0 (the boss framework's hazards / projectiles / direct hurts, 홍련's own hits). Unparriable hits of
mixed chains are counted apart (dodge-only by the user's 11-10 ruling) and the parryable hits around them must still be
perfect.

  bosses   hzlog.py's worlds (the real framework and modules): the mid-bosses 파수꾼 / 나비 / 역장, the chapter bosses
           야타용왕 / 아펩, the special 타키, 아를레키노 - every pattern test id of hzlog.BOSSES, one fresh fight per pattern
  scarlet  홍련 in the suites' H1 world (hrsim.world_h1: the REAL f_key, judge and her module): every chain of hrfair2's T13
           list (both phases, the rings, mx, q, nb, tri ...) at its reach, and the gauntlets G1 / G2 (every scripted cut)

Per pattern: parryable hits, the smallest gap between two parryable hit ticks, perfect parries / parryable hits, refused
presses; unparriable hits of the same run. Exit 1 when a parryable hit of any pattern was not a perfect parry.
Not simulated here (no simulator of their AI exists in tools/dev/sim): 나루카미 and the custom mobs - their chains are covered by
the player-side lemma of test_cb `lock` (any parryable hits on distinct ticks: every one a perfect parry for the ideal press,
whatever the tier of the hit before, during a beat, a dodge's cooldown or move).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
OPT = dict(a[2:].split('=', 1) if '=' in a else (a[2:], '1') for a in sys.argv[1:] if a.startswith('--'))
HZ_BOSSES = ['guardian', 'butterfly', 'fieldgen', 'azhdaha', 'apep', 'tachy', 'arlecchino']
NAMES = {'guardian': '파수꾼', 'butterfly': '나비', 'fieldgen': '역장', 'azhdaha': '야타용왕', 'apep': '아펩', 'tachy': '타키',
         'arlecchino': '아를레키노', 'scarlet': '홍련'}


def gaps(ticks):
    t = sorted(set(ticks))
    return min((b - a for a, b in zip(t, t[1:])), default=None)


def presses_for(ticks):
    """the ideal presses: h - 1, or h itself when the hit before was on h - 1 (its press already sits on h - 1)"""
    out, prev = set(), None
    for h in sorted(set(ticks)):
        out.add(h if prev is not None and h - prev == 1 else h - 1)
        prev = h
    return out


# ------------------------------------------------------------------------------------------- worker: one hzlog boss
def worker_hz(dp, bid):
    sys.argv = [sys.argv[0], dp, bid, 'pat']
    sys.path.insert(0, str(HERE))
    import hzlog as HL                                   # noqa: E402  (picks its sim library from the boss id)
    from mcsim import Ctx                                # noqa: E402
    orig = HL.HzLog.call

    def call(self, fid, ctx, macro=None):
        r = orig(self, fid, ctx, macro)
        if fid in ('rlk:cm/hit_pl2', 'rlk:mboss/hz/hurt_pm') and self.hl['hits'] and 'parT' not in self.hl['hits'][-1]:
            self.hl['hits'][-1]['parT'] = self.sc('#parT', 'tmp') or 0
        return r
    HL.HzLog.call = call
    cfg = HL.BOSSES[bid]
    rows = []
    for n in cfg['ids']:
        presses, res = set(), None
        for _it in range(4):
            s, ok, world = HL.make(cfg, bid)
            if not ok:
                rows.append(dict(boss=bid, pat=n, error='the fight did not start'))
                break
            for p in cfg.get('pre', {}).get(n, []):
                HL.test_id(s, p)
                for _ in range(cfg.get('pre_wait', 3)):
                    HL.tick(s, world)
            for k in s.hl:
                s.hl[k] = []
            s.hl_hz = {}
            t0 = s.t
            HL.test_id(s, n)
            refused = 0
            pl = s.player()
            for o in ('parAt', 'parLk', 'parHit', 'dgAt', 'dgRw'):
                if s.sc(('e', pl.id), o) is None:
                    s.setsc(('e', pl.id), o, -1000000)
            for _ in range(int(cfg['ticks'])):
                T = s.t + 1
                if T - t0 in presses:
                    pl = s.player()
                    s.setsc('#now', 'cb', 100000 + T)
                    s.call('rlk:player/f_key', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
                    refused += (s.sc(('e', pl.id), 'parAt') or 0) != 100000 + T
                HL.tick(s, world)
            hits = s.hl['hits']
            P = [h for h in hits if not h['NP'] and h['kind'] != 'pm']
            N = [h for h in hits if h['NP'] or h['kind'] == 'pm']
            want = presses_for([h['t'] - t0 for h in P])
            res = dict(boss=bid, pat=n, p=len(P), p_ticks=sorted({h['t'] - t0 for h in P}), gap=gaps([h['t'] - t0 for h in P]),
                       pp=sum(h.get('parT') == 3 for h in P), tiers=sorted(h.get('parT', 0) for h in P), n=len(N), refused=refused,
                       srcs=sorted({h['src'] for h in P}))
            if want <= presses:
                break
            presses |= want
        if res:
            rows.append(res)
    return rows


# ------------------------------------------------------------------------------------------- worker: 홍련
def worker_scarlet(dp):
    sys.path.insert(0, str(HERE.parents[1] / 'hr/review/bal'))
    sys.path.insert(0, str(HERE.parents[1] / 'hr/tests'))
    sys.path.insert(0, str(HERE.parents[1] / 'hr/tests/lib'))
    import hrfair2 as F                                  # noqa: E402
    import hrsim as H                                    # noqa: E402
    api, S = F.api_of(dp)
    rows = []
    for key in F.CHAIN_AT:
        for phase in (1, 2):
            if key not in S.TID:
                continue
            hits = api.HITS.get(key, [])
            if not any(r[6] == 'P' and api.HIT_PH.get(key, {}).get(i, phase) == phase for i, r in enumerate(hits)):
                continue
            r = F.run_chain(dict(dp=dp, key=key, phase=phase, mode='chain'))
            rows.append(dict(boss='scarlet', pat=f'{key} P{phase}', p=r['p'], pp=r['p_pp'], n=r['n'], refused=r['f_refused'],
                             want=r['want'], gap=r.get('gap')))
    # the gauntlets: F one tick before every scripted cut (test ids 21 / 27 as beatloop_hr)
    for key, tid in (('a8', 21), ('a13', 27)):
        s, pl = H.setup_h1(dp, seed=9, lv=15, hp=5834, player_level=15)
        assert H.fight_sc(s)
        H.facing_setup(s, 6.0)
        H.test_id(s, tid)
        t0 = s.t
        cuts = [c[2] for _t, _s, _cl, c in api.SCRIPTS[key] if c]
        for k in presses_for(cuts):
            s.press(at=t0 + k)
        j0 = len(s.judged)
        for _ in range(api.JUDGE_T[key] + 40):
            H.heal(s)
            H.world_h1(s)
        J = s.judged[j0:]
        P = [j for j in J if not j['np']]
        rows.append(dict(boss='scarlet', pat=f'gauntlet {"G1" if key == "a8" else "G2"} ({key})', p=len(P),
                         p_ticks=sorted(j['t'] - t0 for j in P), gap=gaps([j['t'] - t0 for j in P]), pp=sum(j['parT'] == 3 for j in P),
                         n=len(J) - len(P), refused=sum(not ok for _t, ok in s.f_log), cuts=len(cuts), gau=s.sc('#gau', 'hr')))
    return rows


def main():
    if len(ARGS) >= 2 and ARGS[1].startswith('@'):
        bid = ARGS[1][1:]
        rows = worker_scarlet(ARGS[0]) if bid == 'scarlet' else worker_hz(ARGS[0], bid)
        print('ROWS ' + json.dumps(rows, ensure_ascii=False))
        return 0
    dp = str(Path(ARGS[0]).resolve())
    todo = ARGS[1:] or HZ_BOSSES + ['scarlet']
    procs = {b: subprocess.Popen([sys.executable, __file__, dp, '@' + b], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
             for b in todo}
    rows, bad = [], []
    for b, p in procs.items():
        out, err = p.communicate(timeout=7200)
        got = [l for l in out.splitlines() if l.startswith('ROWS ')]
        if not got:
            bad.append((b, 'worker failed', err.strip().splitlines()[-3:]))
            continue
        rows += json.loads(got[-1][5:])
    print(f'{"boss":10} {"pattern":24} {"P hits":>6} {"min gap":>7} {"perfect":>8} {"refused F":>9} {"N hits":>6}')
    for r in rows:
        if 'error' in r:
            print(f'{NAMES.get(r["boss"], r["boss"]):10} {str(r["pat"]):24} ERROR {r["error"]}')
            bad.append((r['boss'], r['pat'], r['error']))
            continue
        ok = r['pp'] == r['p'] and r['refused'] == 0 and (r.get('want') is None or r['want'] == r['p'])
        print(f'{NAMES.get(r["boss"], r["boss"]):10} {str(r["pat"]):24} {r["p"]:>6} {str(r["gap"]):>7} {r["pp"]:>4}/{r["p"]:<3} '
              f'{r["refused"]:>9} {r["n"]:>6}' + ('' if ok else '   <-- NOT ALL PERFECT ' + str(r.get('tiers', ''))))
        if not ok:
            bad.append((r['boss'], r['pat'], r['pp'], r['p'], r.get('tiers')))
    multi = [r for r in rows if 'error' not in r and r['p'] >= 2]
    tot_p, tot_pp = sum(r['p'] for r in rows if 'error' not in r), sum(r['pp'] for r in rows if 'error' not in r)
    print(f'chainparry: {len(rows)} patterns ({len(multi)} with 2+ parryable hits), parryable hits {tot_pp} / {tot_p} perfect; '
          f'smallest gap {min((r["gap"] for r in rows if r.get("gap")), default=None)}; exceptions {len(bad)}')
    if 'json' in OPT:
        Path(OPT['json']).write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    for b in bad:
        print('EXCEPTION', b)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
