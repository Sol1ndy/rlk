#!/usr/bin/env python3
"""test_bal_boss.py — the balance groggy of the registry bosses in a real fight (combat overhaul lane B).

    python3 test_bal_boss.py [<roguelike dir>] [boss ...]      (default: every boss with the registry flag "bal")

The engines are the vendored sims of tools/dev/sim/hr/tests/lib (read only): azsim (mid-boss plaza world), cmsim (chapter
mode, real arenas), hrsim.HrSim (specials through their rift). Two changes are made here, in subclasses: mob/setup also
runs the REAL rlk:bal/init (the stub only tagged rlk_mob), and `time query gametime` answers the world clock.
Per boss (registry flag "bal"):
  1 the body gets 12 pips;               2 a burst hit through the REAL combat/apply takes 2 pips (regen delay 300);
  3 at 0 (bal/hit {n:12}) in an allowed state: grgT 100, the module's groggy state, the pattern's hazards / projectiles
    gone, nothing new started for the whole groggy (no hz/make, no pj/launch, no pattern);
  4 a pause (the player dead) stops the groggy clock;   5 groggy end: full gauge, the AI picks a pattern again;
  6 (bosses with protected test states) bal_ok refuses -> pending; her own groggy refills the gauge and drops it;
    back to an allowed state -> the pending groggy starts;
  7 killed while groggy: the fight ends and cleans up, no bal tag or row left.
"""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
KN = '--kn' in sys.argv          # Arlecchino: her own world (knsim of tools/dev/sim/ar/s3/lib), run in a child process
LIB = HERE.parents[1] / ('ar/s3/lib' if KN else 'hr/tests/lib')
sys.path.insert(0, str(LIB))
import azsim  # noqa: E402
import cmsim  # noqa: E402
if KN:
    import knsim  # noqa: E402
else:
    import hrsim  # noqa: E402
from mcsim import Ctx  # noqa: E402

DP = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 and '/' in sys.argv[1] else HERE.parents[4]
ONLY = [a for a in sys.argv[1:] if '/' not in a and not a.startswith('--')]
C0 = Ctx(None, (0.0, 0.0, 0.0), (0.0, 0.0))
R = []


def ck(name, ok, info=''):
    R.append((name, bool(ok)))
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else f'   [{info}]'), flush=True)
    return ok


class GameTime:
    def cmd(self, t, ctx):
        if t[0] == 'time' and t[1:3] == ['query', 'gametime']:
            return 100000 + self.t
        return super().cmd(t, ctx)


class BalAz(GameTime, azsim.AzSim):
    pass


class BalCm(GameTime, cmsim.CmSim):
    pass


if not KN:
    class BalHr(GameTime, hrsim.HrSim):
        pass

    class BalSc(GameTime, hrsim.ScSim):
        pass
else:
    knsim.KnSim = type('BalKn', (GameTime, knsim.KnSim), {})


def bal_setup(s):
    s.cache['rlk:mob/setup'] = ['tag @s add rlk_mob', 'function rlk:bal/init']
    s.call('rlk:bal/load', C0)


def start_mid(cfg):
    s, zone, pl = azsim.setup(force=cfg['n'], dp=DP, cls=BalAz)
    bal_setup(s)
    return s, azsim.to_fight(s, zone)


def start_chapter(cfg, bid):
    s, zone, pl = azsim.setup(force=0, dp=DP, cls=BalCm, player_pos=(0.5, 201.0, 33.5))
    cmsim.install(s)
    s.call('rlk:mboss/init', C0)
    zone.alive = False
    s.ents = [e for e in s.ents if e.alive]
    s.setsc('#mapIdx', 'room', 5)
    s.setsc('#mapType', 'room', 8)
    bal_setup(s)
    cmsim.fight(s, bid, chapter=cfg.get('ch', 1))
    return s, (s.sc('#mbSt', 'mb') or 0) == 1


def start_kn(cfg, bid):
    s, pl = knsim.setup(dp=DP, hp=200000)
    bal_setup(s)
    knsim.fight(s)
    return s, (s.sc('#mbSt', 'mb') or 0) == 1


def start_sc(cfg, bid):
    s, pl = hrsim.setup_sc(DP, cls=BalSc)
    bal_setup(s)
    ok = hrsim.fight_sc(s, intro=False)
    for _ in range(5):
        hrsim.world_sc(s)
    return s, ok and (s.sc('#mbSt', 'mb') or 0) == 1


def start_special(cfg, bid):
    s, zone, pl = azsim.setup(force=0, dp=DP, cls=BalHr, player_pos=(0.5, 201.0, 0.5))
    cmsim.install(s)
    s.call('rlk:mboss/init', C0)
    s.call('rlk:room/rift/init', C0)
    zone.alive = False
    s.ents = [e for e in s.ents if e.alive]
    s.setsc('#mapIdx', 'room', 2)
    s.setsc('#mapType', 'room', 1)
    bal_setup(s)
    z, a, ok = hrsim.special_fight(s, bid)
    return s, ok


def sc(s, e, o):
    return s.sc(('e', e.id), o)


def live(s, tag):
    return [e for e in s.ents if e.alive and tag in e.tags]


def bctx(b):
    return Ctx(b, tuple(b.pos), tuple(b.rot))


def burst_hit(s, b, dmg=1):
    """A burst hit the way the bursts do it: clear_atkflags, the skill flags, items/hook/burst_dmg (REAL: the flag),
    combat/apply as the target, char/after_hit (REAL: the flag goes)."""
    pl = s.player()
    pc = Ctx(pl, tuple(pl.pos), tuple(pl.rot))
    s.call('rlk:combat/clear_atkflags', pc)
    for k, v in (('#dmg', dmg), ('#crit', 0), ('#stunHit', 1), ('#skillDmg', 1), ('#hitLanded', 0), ('#bowHit', 0)):
        s.setsc(k, 'tmp', v)
    s.setsc('#basic', 'itv', 0)
    s.call('rlk:items/hook/burst_dmg', pc)
    s.call('rlk:combat/apply', bctx(b))
    s.call('rlk:char/after_hit', pc)


def test_id(s, n):
    pl = s.player()
    s.call('rlk:mboss/test/pattern', Ctx(pl, tuple(pl.pos), tuple(pl.rot)), {'id': n})


# kind: mid / chapter / special; pat: the module's pattern score (objective po, default mb); grog: the module's groggy
# state after bal_on (default: pattern 0); prot / free / refill: module test ids (a protected state, back to idle, her
# own groggy); free_wait: ticks the way back may take.
BOSSES = {
    'proto': dict(kind='mid', n=99, pat='#prPat'),
    'guardian': dict(kind='mid', n=1, pat='#gdPat', prot=20, free=99, refill=40),
    'butterfly': dict(kind='mid', n=2, pat='#bfPat', prot=20, free=99, refill=40),
    'fieldgen': dict(kind='mid', n=3, pat='#fgPat', prot=20, free=23, free_wait=400, refill=40),
    'cproto': dict(kind='chapter', pat='#cpPat'),
    'azhdaha': dict(kind='chapter', ch=1, pat='#azPat', prot=23, free=99, free_wait=40),
    'apep': dict(kind='chapter', ch=3, pat='#apPid'),
    'arlecchino': dict(kind='kn', pat='#pat', po='kn', grog=('#pat', 'kn', 50), prot=10, refill=29, free=None, free_wait=500),
    'spproto': dict(kind='special', pat='#spPat'),
    'tachy': dict(kind='special', pat='#pat', po='tk', grog=('#stag', 'tk', 100), prot=20, refill='strike'),
    'scarlet': dict(kind='sc', pat='#pat', po='hr', prot=21, refill=25),
}


def run_boss(bid, cfg):
    po = cfg.get('po', 'mb')
    pat = lambda s: s.sc(cfg['pat'], po) or 0  # noqa: E731
    if cfg['kind'] == 'mid':
        s, ok = start_mid(cfg)
    elif cfg['kind'] == 'kn':
        s, ok = start_kn(cfg, bid)
    elif cfg['kind'] == 'sc':
        s, ok = start_sc(cfg, bid)
    elif cfg['kind'] == 'chapter':
        s, ok = start_chapter(cfg, bid)
    else:
        s, ok = start_special(cfg, bid)
    if not ck(f'{bid} 0 the fight starts', ok):
        return
    W0 = knsim.world if KN else hrsim.world_sc if cfg['kind'] == 'sc' else azsim.world

    def W(s):
        # mob/tick's balance line (the vendored worlds run only mob/tick's element line): every enemy but Raiden, balT >= 1
        for e in [e for e in s.ents if e.alive and 'rlk_mob' in e.tags and e.etype != 'player' and 'rlk_raiden' not in e.tags]:
            if (s.sc(('e', e.id), 'balT') or 0) >= 1 and 'rlk_mb_dying' not in e.tags:
                s.call('rlk:bal/tick', Ctx(e, tuple(e.pos), tuple(e.rot)))
        W0(s)
    b = knsim.body(s) if KN else azsim.body_of(s)
    ck(f'{bid} 1 the body has 12 pips', (sc(s, b, 'balMax'), sc(s, b, 'bal')) == (12, 12), (sc(s, b, 'balMax'), sc(s, b, 'bal')))
    burst_hit(s, b)
    ck(f'{bid} 2 a burst hit (REAL combat/apply) takes 2 pips, regen delay 300', (sc(s, b, 'bal'), sc(s, b, 'balT')) == (10, 300),
       (sc(s, b, 'bal'), sc(s, b, 'balT')))
    # wait for a running pattern the module allows, then break the balance in the middle of it
    okn = False
    for _ in range(900):
        W(s)
        if pat(s) >= 1 and s.call('rlk:mboss/d/bal_ok', bctx(b)):
            okn = True
            break
    p0 = pat(s)
    s.call('rlk:bal/hit', bctx(b), {'n': 12})
    g = cfg.get('grog')
    gstate = (s.sc(g[0], g[1]) == g[2]) if g else pat(s) == 0
    ck(f'{bid} 3a groggy from inside pattern {p0} (found {okn}): grgT 100, the groggy state, no live hazard / projectile',
       sc(s, b, 'grgT') == 100 and gstate and not live(s, 'rlk_mb_hz') and not live(s, 'rlk_mb_pj'),
       (p0, sc(s, b, 'grgT'), pat(s), g and s.sc(g[0], g[1]), len(live(s, 'rlk_mb_hz')), len(live(s, 'rlk_mb_pj'))))
    ck(f'{bid} 3b the boss row is the groggy row', s.storage['rlk:bal']['brow']['extra'][0]['text'] == chr(0xED22) + (chr(0xED13) + chr(0xED20)) * 12 + chr(0xED21))
    nhz, npj = len(s.hz), len(s.pjs)
    for _ in range(50):
        W(s)
    pl = s.player()
    s.setsc(('e', pl.id), 'dead', 1)
    g50 = sc(s, b, 'grgT')
    for _ in range(40):
        W(s)
    # (the clock runs in mob/tick, before mboss/main notices the pause: the first paused tick still counts, the resume
    # tick does not, so the module's bal_tick still gets exactly the 100 groggy ticks)
    ck(f'{bid} 4 a pause (player down) stops the groggy clock (the pause edge tick aside)', g50 == 50 and sc(s, b, 'grgT') == 49,
       (g50, sc(s, b, 'grgT')))
    s.setsc(('e', pl.id), 'dead', 0)
    for _ in range(49):
        W(s)
    gstate = (s.sc(g[0], g[1]) >= 1) if g else pat(s) == 0
    ck(f'{bid} 3c nothing started during the groggy (no hz/make, no pj/launch, still in the groggy state)',
       len(s.hz) == nhz and len(s.pjs) == npj and gstate and sc(s, b, 'grgT') == 1,
       (len(s.hz) - nhz, len(s.pjs) - npj, pat(s), sc(s, b, 'grgT')))
    W(s)
    ck(f'{bid} 5a groggy over after 100 fight ticks: full gauge, no regen clock, no bal tags',
       (sc(s, b, 'grgT'), sc(s, b, 'bal'), sc(s, b, 'balT')) == (0, 12, 0) and not ({'rlk_bal_grog', 'rlk_bal_pend'} & b.tags)
       and (not g or s.sc(g[0], g[1]) != g[2]), (sc(s, b, 'grgT'), sc(s, b, 'bal'), g and s.sc(g[0], g[1])))
    started = None
    for k in range(400):
        W(s)
        if 1 <= pat(s) <= 49:
            started = k
            break
    ck(f'{bid} 5b the AI picks a pattern again ({started} t after)', started is not None)
    if 'prot' in cfg:
        test_id(s, cfg['prot'])
        for _ in range(3):
            W(s)
        okp = s.call('rlk:mboss/d/bal_ok', bctx(b))
        s.call('rlk:bal/hit', bctx(b), {'n': 12})
        W(s)
        ck(f'{bid} 6a a protected state (test {cfg["prot"]}): bal_ok refuses, the gauge at 0 waits (pending)',
           not okp and 'rlk_bal_pend' in b.tags and sc(s, b, 'grgT') == 0 and sc(s, b, 'bal') == 0,
           (okp, b.tags & {'rlk_bal_pend'}, sc(s, b, 'grgT'), sc(s, b, 'bal')))
        if 'refill' in cfg:
            if cfg['refill'] == 'strike':
                azsim.strike(s, b, 1)
            else:
                test_id(s, cfg['refill'])
            for _ in range(3):
                W(s)
            ck(f'{bid} 6c her own groggy (test {cfg["refill"]}) refills the gauge and drops the pending balance groggy',
               'rlk_bal_pend' not in b.tags and sc(s, b, 'bal') == 12 and sc(s, b, 'grgT') == 0, (b.tags & {'rlk_bal_pend'}, sc(s, b, 'bal')))
            if 'free' not in cfg:
                cfg = dict(cfg, done=True)
            else:
                for _ in range(800):
                    if s.call('rlk:mboss/d/bal_ok', bctx(b)):
                        break
                    W(s)
                test_id(s, cfg['prot'])
                for _ in range(3):
                    W(s)
                s.call('rlk:bal/hit', bctx(b), {'n': 12})
                W(s)
    if 'prot' in cfg and 'free' in cfg:
        if cfg['free'] is not None:
            test_id(s, cfg['free'])
        waited = 0
        for _ in range(2 + cfg.get('free_wait', 0)):
            W(s)
            waited += 1
            if waited >= 2 and (sc(s, b, 'grgT') or 0) >= 1:
                break
        ck(f'{bid} 6b back to an allowed state (test {cfg["free"]}, {waited} t): the pending groggy starts',
           (sc(s, b, 'grgT') or 0) >= 90 and 'rlk_bal_pend' not in b.tags, (sc(s, b, 'grgT'), b.tags & {'rlk_bal_pend'}))
        for _ in range(110):
            W(s)
    # death while groggy
    s.call('rlk:bal/hit', bctx(b), {'n': 12})
    pl = s.player()
    s.call('rlk:mboss/test/kill', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
    for _ in range(1500):
        W(s)
        if (s.sc('#mbLive', 'mb') or 0) == 0:
            break
    ck(f'{bid} 7 killed while groggy / pending: the fight ends and cleans up, no bal tag or row left',
       (s.sc('#mbLive', 'mb') or 0) == 0 and not [e for e in s.ents if e.alive and ({'rlk_bal_grog', 'rlk_bal_pend', 'rlk_hb_bal'} & e.tags)])


reg = json.loads((DP / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
flag = {b['id'] for b in reg['boss'] if b.get('bal') and b.get('enabled', True)}
for bid, cfg in BOSSES.items():
    if ONLY and bid not in ONLY:
        continue
    if (cfg['kind'] == 'kn') != KN:
        if cfg['kind'] == 'kn':
            import subprocess
            r = subprocess.run([sys.executable, str(Path(__file__)), str(DP), bid, '--kn'], capture_output=True, text=True)
            out = [l for l in r.stdout.splitlines() if l.startswith(('PASS', 'FAIL', '---'))]
            print('\n'.join(out) + ('' if out else r.stdout[-2000:] + r.stderr[-2000:]), flush=True)
            R.extend((l[5:], l.startswith('PASS')) for l in out if not l.startswith('---'))
            if not out:
                ck(f'{bid} (knsim child) ran', False, r.returncode)
        continue
    print(f'--- {bid}', flush=True)
    if bid not in flag:
        ck(f'{bid} has the registry flag "bal"', False)
        continue
    try:
        run_boss(bid, cfg)
    except Exception as ex:  # noqa: BLE001
        import traceback
        traceback.print_exc()
        ck(f'{bid} crashed', False, repr(ex))
if not ONLY:
    missing = sorted(flag - set(BOSSES))
    ck('every flagged boss has a case here', not missing, missing)
bad = [r for r in R if not r[1]]
print(f'\n{len(R) - len(bad)}/{len(R)} passed' + (f', {len(bad)} FAILED' if bad else ''))
sys.exit(1 if bad else 0)
