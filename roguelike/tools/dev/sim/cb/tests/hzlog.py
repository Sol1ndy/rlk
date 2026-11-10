#!/usr/bin/env python3
"""hzlog.py — the hazard / projectile / glint log of one boss in simulated fights (combat overhaul, fix lane FB; the
reviewer's harness of review B rebuilt from the `repro` fields of tools/dev/plan/combat/review/findings_B.json).

    python3 hzlog.py <roguelike dir> <boss> pat   [--ids=1,2,..] [--ticks=N] [--dodge] [--out=<file.json>]
    python3 hzlog.py <roguelike dir> <boss> fight [--ticks=3000] [--seed=N] [--out=<file.json>]

Run it from a copy of tools/dev/sim outside the datapack (sim README 1 B). One boss per process: the vendored sims of
hr/tests/lib (mid-bosses in the plaza, chapter bosses in their arenas, specials through their rift) and ar/s3/lib (아를레키노)
share module names.

What is recorded (the real framework and modules run; every score is read from the marker / prop right after the framework made it):
  hz     every hazard at rlk:mboss/hz/init: K kind (1 disc 2 ring 3 sector 4 line 5 full 6 mask), R / R0 reach (milliblocks), W
         wind-up, A active ticks, D damage %, ND no-dodge, PM per mille, RA re-arm, NP unparriable, G volley group, the
         tick, the position and `src` = the module function that made it; `strike` = the tick of its rlk:mboss/hz/strike
  pj     every prop after rlk:mboss/pj/launch: D ND NP G, speed, life, `src`
  direct every rlk:mboss/hurt a module calls itself (not through hz/hurt or pj/hit): #mbHitPct, #mbNoDodge, #mbNoParry
  glint  every rlk:player/defx/glint-family call (the warning flash): tick, position, the y above the arena floor
  hits   every hit that reached the judge: tick, kind (hz / pj / direct / pm), %, ND, NP, dodged, parT, pdg, HP lost
  cmd    commands per world tick (every command the interpreter runs, sub-commands of execute included)

`pat`: a fresh fight per test id (rlk:mboss/test/pattern {id:N}); with --dodge the player's dodge stamp is refreshed every
tick (a perfect dodge on every tick), which shows what a perfect dodge avoids. `fight`: the AI's own fight against a passive
player who is healed every tick (the fight never pauses), N fight ticks.
"""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.setrecursionlimit(20000)          # deep mcfunction recursion x the python frames of the stacked sim classes
HERE = Path(__file__).resolve().parent
ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
OPT = dict(a[2:].split('=', 1) if '=' in a else (a[2:], '1') for a in sys.argv[1:] if a.startswith('--'))
if __name__ == '__main__' and len(ARGS) < 3:
    print(__doc__)
    sys.exit(2)
DP = Path(ARGS[0]).resolve() if ARGS else None
BID = ARGS[1] if len(ARGS) > 1 else ''
KN = BID == 'arlecchino'
LIB = HERE.parents[1] / ('ar/s3/lib' if KN else 'hr/tests/lib')
sys.path.insert(0, str(LIB))
import azsim  # noqa: E402
import cmsim  # noqa: E402
if KN:
    import knsim  # noqa: E402
else:
    import hrsim  # noqa: E402
from mcsim import Ctx  # noqa: E402

C0 = Ctx(None, (0.0, 0.0, 0.0), (0.0, 0.0))
FW = ('rlk:mboss/hz/', 'rlk:mboss/pj/', 'rlk:mboss/hurt', 'rlk:mboss/grp_', 'rlk:mboss/np_', 'rlk:mboss/d/',
      'rlk:mboss/opts_reset', 'rlk:mboss/main', 'rlk:mboss/fight_tick', 'rlk:mboss/near_all')
GLINTS = ('rlk:player/def/fx/glint',)


class HzLog:
    """Mixin in front of the sim class: the logs above."""

    def __init__(self, root):
        super().__init__(root)
        self.hl = dict(hz=[], pj=[], direct=[], glint=[], hits=[], cmd=[])
        self.hl_hz = {}            # marker id -> its hz record
        self.hl_pj = set()
        self.hl_n = 0
        self.hl_src = None         # (kind, record) of the hit being judged

    def cmd(self, t, ctx):
        self.hl_n += 1
        if t[0] == 'time' and t[1:3] == ['query', 'gametime']:
            return 100000 + self.t
        return super().cmd(t, ctx)

    def hl_caller(self):
        for f in reversed(self.stack):
            if not f.startswith(FW):
                return f.replace('rlk:', '')
        return ''

    def hl_floor(self):
        a = self.select('@e[tag=rlk_mb_arena,limit=1]', C0)
        return a[0].pos[1] if a else 201.0

    def call(self, fid, ctx, macro=None):
        g = lambda o: self.sc(('e', ctx.ex.id), o)  # noqa: E731
        m = lambda k: self.sc(k, 'mb') or 0  # noqa: E731
        if fid in GLINTS:
            b = azsim.body_of(self)
            self.hl['glint'].append(dict(t=self.t, pos=[round(v, 3) for v in ctx.pos], dy=round(ctx.pos[1] - self.hl_floor(), 3),
                                         body=[round(v, 3) for v in b.pos] if b else None, src=self.hl_caller()))
        elif fid == 'rlk:mboss/hz/strike' and ctx.ex is not None and ctx.ex.id in self.hl_hz:
            self.hl_hz[ctx.ex.id].setdefault('strike', self.t)
        elif fid == 'rlk:mboss/hurt':
            top = self.stack[-1] if self.stack else ''
            if top == 'rlk:mboss/hz/hurt':
                self.hl_src = ('hz', self.hl_hz.get(ctx.ex.id) if ctx.ex is not None else None)
            elif top == 'rlk:mboss/pj/hit':
                self.hl_src = ('pj', None)
            else:
                rec = dict(t=self.t, D=m('#mbHitPct'), ND=m('#mbNoDodge'), NP=m('#mbNoParry'), src=self.hl_caller())
                self.hl['direct'].append(rec)
                self.hl_src = ('direct', rec)
        elif fid == 'rlk:mboss/hz/hurt_pm':
            self.hl_src = ('pm', self.hl_hz.get(ctx.ex.id) if ctx.ex is not None else None)
        if fid in ('rlk:cm/hit_pl2', 'rlk:mboss/hz/hurt_pm'):
            pl = self.player()
            hp0 = self.sc(('e', pl.id), 'curHealth') or 0
            kind, rec = self.hl_src or ('?', None)
            pm = fid.endswith('hurt_pm')
            h = dict(t=self.t, kind=kind, D=(g('mbHzPm') if pm else m('#mbHitPct')),
                     ND=(g('mbHzND') if pm else m('#mbNoDodge')) or 0, NP=(g('mbHzNP') if pm else m('#mbNoParry')) or 0,
                     src=(rec or {}).get('src', self.hl_caller()), hz=(rec or {}).get('i'))
            r = super().call(fid, ctx, macro)
            h.update(dodged=self.sc('#dodged', 'tmp') or 0, pdg=self.sc('#pdg', 'tmp') or 0,
                     lost=hp0 - (self.sc(('e', pl.id), 'curHealth') or 0))
            if not pm or h['dodged'] or h['lost']:
                self.hl['hits'].append(h)
            return r
        r = super().call(fid, ctx, macro)
        if fid == 'rlk:mboss/hz/init' and ctx.ex is not None:
            rec = dict(i=len(self.hl['hz']), t=self.t, K=g('mbHzK'), R=g('mbHzR'), R0=g('mbHzR0'), W=g('mbHzW'), A=g('mbHzA'),
                       D=g('mbHzD'), ND=g('mbHzND') or 0, PM=g('mbHzPm') or 0, RA=g('mbHzRA') or 0, NP=g('mbHzNP') or 0,
                       G=g('mbHzG') or 0, Y1=g('mbHzY1'), pos=[round(v, 2) for v in ctx.ex.pos], yaw=round(ctx.ex.rot[0], 1),
                       src=self.hl_caller())
            self.hl['hz'].append(rec)
            self.hl_hz[ctx.ex.id] = rec
        elif fid == 'rlk:mboss/pj/launch':
            for e in self.ents:
                if e.alive and 'rlk_mb_pj' in e.tags and e.id not in self.hl_pj:
                    self.hl_pj.add(e.id)
                    q = lambda o: self.sc(('e', e.id), o)  # noqa: E731
                    self.hl['pj'].append(dict(t=self.t, D=q('mbPjD'), ND=q('mbPjND') or 0, NP=q('mbPjNP') or 0, G=q('mbPjG') or 0,
                                              R=q('mbPjR'), life=q('mbPjL'), spd=(macro or {}).get('spd'), src=self.hl_caller()))
        return r


# ----------------------------------------------------------------------------------------------------- the worlds
BOSSES = {
    # ids: the module's test numbers that start an attack (test/help); pre: test ids sent first (a phase), wait: ticks after
    # them; ticks: how long one pattern is watched; rig: the generated rig / stub prefix (not needed here)
    'guardian': dict(kind='mid', n=1, ids=[1, 2, 3, 4, 5, 11, 12, 13], ticks=260),
    'butterfly': dict(kind='mid', n=2, ids=[1, 2, 3, 4, 11, 12, 13, 14, 15], ticks=320),
    'fieldgen': dict(kind='mid', n=3, ids=[1, 2, 3, 4, 5, 6, 11, 12, 21], ticks=420),
    'azhdaha': dict(kind='chapter', ch=1, ids=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 31, 32, 33, 41, 42, 43, 44, 45, 46], ticks=420),
    'apep': dict(kind='chapter', ch=3, ids=[1, 2, 3, 4, 5, 6, 9, 31, 32, 33, 34, 35, 36, 37], ticks=420),
    'tachy': dict(kind='special', ids=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 21], ticks=320),
    'arlecchino': dict(kind='kn', ids=[1, 2, 13, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 41, 42, 43, 44, 45, 46, 47, 48], ticks=420),
    'scarlet': dict(kind='sc', ids=[], ticks=320),
    'proto': dict(kind='mid', n=99, ids=[], ticks=200),
    'cproto': dict(kind='chapter', ch=1, ids=[], ticks=200),
    'spproto': dict(kind='special', ids=[], ticks=200),
}


def make(cfg, bid, seed=None):
    kw = {} if seed is None else {'seed': seed}
    if cfg['kind'] == 'mid':
        s, zone, pl = azsim.setup(force=cfg['n'], dp=DP, cls=type('LogAz', (HzLog, azsim.AzSim), {}), **kw)
        ok = azsim.to_fight(s, zone)
        return s, ok, azsim.world
    if cfg['kind'] == 'chapter':
        s, zone, pl = azsim.setup(force=0, dp=DP, cls=type('LogCm', (HzLog, cmsim.CmSim), {}), player_pos=(0.5, 201.0, 33.5), **kw)
        cmsim.install(s)
        s.call('rlk:mboss/init', C0)
        zone.alive = False
        s.ents = [e for e in s.ents if e.alive]
        s.setsc('#mapIdx', 'room', 5)
        s.setsc('#mapType', 'room', 8)
        cmsim.fight(s, bid, chapter=cfg.get('ch', 1))
        return s, (s.sc('#mbSt', 'mb') or 0) == 1, azsim.world
    if cfg['kind'] == 'kn':
        if not issubclass(knsim.KnSim, HzLog):
            knsim.KnSim = type('LogKn', (HzLog, knsim.KnSim), {})
        s, pl = knsim.setup(dp=DP, hp=200000, **kw)
        knsim.fight(s)
        return s, (s.sc('#mbSt', 'mb') or 0) == 1, knsim.world
    if cfg['kind'] == 'sc':
        s, pl = hrsim.setup_sc(DP, cls=type('LogSc', (HzLog, hrsim.ScSim), {}), **kw)
        ok = hrsim.fight_sc(s, intro=False)
        return s, ok and (s.sc('#mbSt', 'mb') or 0) == 1, hrsim.world_sc
    s, zone, pl = azsim.setup(force=0, dp=DP, cls=type('LogHr', (HzLog, hrsim.HrSim), {}), player_pos=(0.5, 201.0, 0.5), **kw)
    cmsim.install(s)
    s.call('rlk:mboss/init', C0)
    s.call('rlk:room/rift/init', C0)
    zone.alive = False
    s.ents = [e for e in s.ents if e.alive]
    s.setsc('#mapIdx', 'room', 2)
    s.setsc('#mapType', 'room', 1)
    z, a, ok = hrsim.special_fight(s, bid)
    return s, ok, azsim.world


def heal(s):
    pl = s.player()
    s.setsc(('e', pl.id), 'curHealth', s.sc(('e', pl.id), 'maxHealth'))
    s.setsc(('e', pl.id), 'dead', 0)


def tick(s, world, dodge=False):
    heal(s)
    if dodge:
        pl = s.player()
        for o in ('parAt', 'parLk', 'parHit', 'dgRw'):
            if s.sc(('e', pl.id), o) is None:
                s.setsc(('e', pl.id), o, -1000000)
        s.setsc(('e', pl.id), 'dgAt', 100000 + s.t + 1)        # the tick about to run
    n0 = s.hl_n
    world(s)
    s.hl['cmd'].append(s.hl_n - n0)


def test_id(s, n):
    pl = s.player()
    s.call('rlk:mboss/test/pattern', Ctx(pl, tuple(pl.pos), tuple(pl.rot)), {'id': n})


def out_of(s, extra=None):
    d = {k: v for k, v in s.hl.items()}
    d.update(extra or {})
    return d


def run_pat(cfg, bid):
    res = {}
    ids = [int(x) for x in OPT['ids'].split(',')] if 'ids' in OPT else cfg['ids']
    for n in ids:
        s, ok, world = make(cfg, bid)
        if not ok:
            raise SystemExit(f'{bid}: the fight did not start')
        for p in cfg.get('pre', {}).get(n, []):
            test_id(s, p)
            for _ in range(cfg.get('pre_wait', 3)):
                tick(s, world)
        for k in s.hl:
            s.hl[k] = []
        s.hl_hz = {}
        t0 = s.t
        test_id(s, n)
        for _ in range(int(OPT.get('ticks', cfg['ticks']))):
            tick(s, world, dodge='dodge' in OPT)
        res[str(n)] = out_of(s, dict(t0=t0))
    return res


def run_fight(cfg, bid):
    s, ok, world = make(cfg, bid, seed=int(OPT['seed']) if 'seed' in OPT else None)
    if not ok:
        raise SystemExit(f'{bid}: the fight did not start')
    for k in s.hl:
        s.hl[k] = []
    t0 = s.t
    for _ in range(int(OPT.get('ticks', 3000))):
        tick(s, world)
        if (s.sc('#mbLive', 'mb') or 0) == 0:
            break
    return out_of(s, dict(t0=t0, ticks=s.t - t0))


if __name__ == '__main__':
    cfg = BOSSES[BID]
    mode = ARGS[2]
    res = run_pat(cfg, BID) if mode == 'pat' else run_fight(cfg, BID)
    txt = json.dumps(res, ensure_ascii=False)
    if 'out' in OPT:
        Path(OPT['out']).write_text(txt, encoding='utf-8')
        print(f'{BID} {mode}: wrote {OPT["out"]}')
    else:
        print(txt)
