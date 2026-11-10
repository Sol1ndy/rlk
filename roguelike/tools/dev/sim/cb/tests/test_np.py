#!/usr/bin/env python3
"""test_np.py — the enemy side of the combat overhaul after review B (fix lane FB; tools/dev/plan/combat/review/findings_B.json,
rulings_B.md): the unparriable rule and its warning glint, one volley = one answer, the two mob fixes, the two boss groggy fixes.

    python3 test_np.py <roguelike dir> [fw] [b08] [b09] [mobs] [table] [--logs=<dir> --tag=<tag>] [--jobs=N]

Run it from a copy of tools/dev/sim outside the datapack (sim README 1 B). Sections (default: all):
  fw     the framework in a real mid-boss world (hr/tests/lib): B-01 the default rule hz/np_def (no size thresholds) and the
         options noparry 0 / 1 / glint=False; B-02 / B-04 hz/np_auto (a glint only for an unparriable hazard that hits, can be
         dodged, is not re-arming and is made >= 12 t before its strike); the gate (spacing, cutscene, #mbNpOwn); B-03 the glint
         point (registry "glint" / mboss_lib.glint_of: above the floor for every boss, never the husk's eyes); B-10 + A-04
         one volley = one answer (a landed hit, a tier-2 parry, a perfect parry and a perfect dodge consume the group;
         burst i-frames do not; the per-mille path too)
  b08    타키: a balance groggy in the side-step hop puts her on the floor
  b09    아펩: no pips while the body is parked (untargetable); pips again when it is back
  mobs   (child process, bal/tests/lib) B-06 the archer's arrow carries its owner: the hit context names the archer; B-07 the
         conjurer's cicins: no new ram while she is groggy, a ram is judged as hers
  table  hzlog.py `pat` and `pat --dodge` of the seven bosses (child processes; --logs / --tag reuse existing logs): the
         unparriable patterns per boss are exactly the ruled list; every unparriable hazard that can be dodged has its glint
         >= 12 t before the strike (the module list >= 20 t), no glint belongs to a parryable / no-dodge / lingering hazard,
         every glint is >= 1 b above the floor; no volley group and no strike mixes parryable and unparriable hazards; with a
         perfect dodge on every tick every such hit is avoided and no no-dodge hit is; unparriable strikes a perfect dodge
         has to answer are never closer than the dodge cooldown allows.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
OPT = dict(a[2:].split('=', 1) if '=' in a else (a[2:], '1') for a in sys.argv[1:] if a.startswith('--'))
DP = Path(ARGS[0]).resolve() if ARGS and '/' in ARGS[0] else HERE.parents[4]
SECT = [a for a in ARGS if '/' not in a] or ['fw', 'b08', 'b09', 'mobs', 'table']
FN = DP / 'data/rlk/function'
R = []


def ck(name, ok, info=''):
    R.append((name, bool(ok)))
    print(('PASS ' if ok else 'FAIL ') + name + ('' if ok else f'   [{info}]'), flush=True)
    return ok


def text(rel):
    p = FN / (rel + '.mcfunction')
    return p.read_text(encoding='utf-8') if p.exists() else ''


def cmds(rel):
    return [l for l in text(rel).split('\n') if l and not l.startswith('#')]


# ruled list (rulings_B.md B-01): the pattern groups (np_table.group_of) that hold an unparriable hazard that can be dodged
# (= with the glint), and the ones unparriable by nature (no-dodge / lingering: no glint)
RULED = {
    'guardian': ({'p/flyslam', 'p/fail'}, set()),
    'butterfly': ({'p/release'}, set()),
    'fieldgen': ({'p/burst'}, {'p/laser', 'p/waves'}),
    'azhdaha': ({'p/frost', 'p/burrow3', 'p/meteor'}, {'p/feint', 'p/whip', 'p/slide', 'p/bolt', 'orb', 'fld'}),
    'apep': ({'p/tail', 'p/glow', 'p/wither'}, {'p/aftermath', 'p/glow'}),
    'tachy': ({'p/l', 'p/mantle'}, set()),
    'arlecchino': ({'p/f1', 'p/g1', 'p/q4', 'p/q5a', 'p/q5b', 'p/q6'}, set()),
}
# the framework-rule hits among them (full arena / per mille: a glint >= 20 t too) are in the same list; lead floors
LEAD, LEAD_BIG = 12, 20
# apep's swing 2 follows swing 1 by 17 t: its tell cannot start earlier than the recoil (16 t before its first wedge)
LEAD_EXC = {('apep', 'p/tail'): 16}
DODGE_GAP = 10          # two perfect dodges: press 2 at >= press 1 + 12 (cooldown after a dodge that avoided), windows of 3 t


# ============================================================================================ fw / b08 / b09 (hr/tests/lib)
def boss_world(kind, bid=None, n=None):
    sys.path.insert(0, str(HERE.parents[1] / 'hr/tests/lib'))
    import azsim
    import cmsim
    import hrsim
    from mcsim import Ctx
    C0 = Ctx(None, (0.0, 0.0, 0.0), (0.0, 0.0))

    class Log:
        def __init__(self, root):
            super().__init__(root)
            self.glints = []

        def cmd(self, t, ctx):
            if t[0] == 'time' and t[1:3] == ['query', 'gametime']:
                return 100000 + self.t
            return super().cmd(t, ctx)

        def call(self, fid, ctx, macro=None):
            if fid == 'rlk:player/def/fx/glint':
                self.glints.append((self.t, tuple(ctx.pos)))
            return super().call(fid, ctx, macro)

    if kind == 'mid':
        s, zone, pl = azsim.setup(force=n, dp=DP, cls=type('W', (Log, azsim.AzSim), {}))
        ok = azsim.to_fight(s, zone)
    elif kind == 'chapter':
        s, zone, pl = azsim.setup(force=0, dp=DP, cls=type('W', (Log, cmsim.CmSim), {}), player_pos=(0.5, 201.0, 33.5))
        cmsim.install(s)
        s.call('rlk:mboss/init', C0)
        zone.alive = False
        s.ents = [e for e in s.ents if e.alive]
        s.setsc('#mapIdx', 'room', 5)
        s.setsc('#mapType', 'room', 8)
        s.cache['rlk:mob/setup'] = ['tag @s add rlk_mob', 'function rlk:bal/init']
        s.call('rlk:bal/load', C0)
        cmsim.fight(s, bid, chapter=n)
        ok = (s.sc('#mbSt', 'mb') or 0) == 1
    else:
        s, zone, pl = azsim.setup(force=0, dp=DP, cls=type('W', (Log, hrsim.HrSim), {}), player_pos=(0.5, 201.0, 0.5))
        cmsim.install(s)
        s.call('rlk:mboss/init', C0)
        s.call('rlk:room/rift/init', C0)
        zone.alive = False
        s.ents = [e for e in s.ents if e.alive]
        s.setsc('#mapIdx', 'room', 2)
        s.setsc('#mapType', 'room', 1)
        s.cache['rlk:mob/setup'] = ['tag @s add rlk_mob', 'function rlk:bal/init']
        s.call('rlk:bal/load', C0)
        z, a, ok = hrsim.special_fight(s, bid)
    return s, ok, azsim, Ctx, C0


def t_fw():
    s, ok, azsim, Ctx, C0 = boss_world('mid', n=1)
    if not ck('fw 0 a Guardian fight for the framework checks', ok):
        return
    b = azsim.body_of(s)
    pl = s.player()
    bc = lambda: Ctx(b, tuple(b.pos), (b.rot[0], 0.0))  # noqa: E731
    e = lambda x, o: s.sc(('e', x.id), o)  # noqa: E731

    def make(kind, opts=None, **macro):
        """One framework hazard at the body with the one-shot options `opts`; returns (marker, glints made)."""
        s.call('rlk:mboss/opts_reset', C0)
        for k, v in (opts or {}).items():
            s.setsc(k, 'mb', v)
        s.t += 40                                # outside the glint gap of the last one
        g0 = len(s.glints)
        ids = {x.id for x in s.ents}
        s.call(f'rlk:mboss/hz/{kind}', bc(), macro)
        m = [x for x in s.ents if x.alive and 'rlk_mb_hz' in x.tags and x.id not in ids]
        return (m[0] if m else None), len(s.glints) - g0

    def kill_hz():
        for x in s.ents:
            if 'rlk_mb_hz' in x.tags:
                x.alive = False

    # ---- B-01: the default rule
    rows = [('disc r 12 (tell 20)', 'disc', {}, dict(r=120, tell=20, dmg=100), 0),
            ('disc r 4.5', 'disc', {}, dict(r=45, tell=20, dmg=100), 0),
            ('sector r 12', 'sector', {}, dict(r=120, a=60, tell=20, dmg=100), 0),
            ('line 28 b', 'line', {}, dict(len=280, w=30, tell=20, dmg=100), 0),
            ('ring 3-7', 'ring', {}, dict(r0=30, r=70, tell=20, dmg=100), 0),
            ('no-dodge disc r 2', 'disc', {'#hzNoDodge': 1}, dict(r=20, tell=20, dmg=100), 1),
            ('per-mille disc', 'disc', {'#hzPm': 300}, dict(r=20, tell=20, dmg=1), 1),
            ('re-arming line', 'line', {'#hzRearm': 10}, dict(len=28, w=10, tell=20, dmg=75), 1),
            ('full arena', 'full', {}, dict(tell=20, dmg=100), 1)]
    got = []
    for name, kind, opts, macro, exp in rows:
        m, g = make(kind, opts, **macro)
        got.append((name, e(m, 'mbHzNP') if m else None, exp))
    kill_hz()
    ck('fw B-01 the default rule: a disc / sector / line / ring of any size is parryable; no-dodge, per-mille, re-arming and '
       'full-arena hazards are not', all(g == x for _, g, x in got), [r for r in got if r[1] != r[2]])
    npd = cmds('mboss/hz/np_def')
    ck('fw B-01 static: hz/np_def has no size threshold (no mbHzR test) and names ND / Pm / RA / kinds 5-6',
       not any('mbHzR ' in l for l in npd) and all(any(k in l for l in npd) for k in ('mbHzND', 'mbHzPm', 'mbHzRA', 'mbHzK matches 5..6')), npd)
    # the mask kind (6) through its own entry
    s.call('rlk:mboss/opts_reset', C0)
    ids = {x.id for x in s.ents}
    s.call('rlk:mboss/hz/mask', bc(), {'r0': 30, 'tell': 20, 'dmg': 100})
    mk = [x for x in s.ents if x.alive and 'rlk_mb_hz' in x.tags and x.id not in ids]
    ck('fw B-01 a mask hazard is unparriable by the rule', bool(mk) and e(mk[0], 'mbHzNP') == 1, mk and e(mk[0], 'mbHzNP'))
    kill_hz()
    m1, g1 = make('disc', {'#hzNoParry': 1}, r=30, tell=20, dmg=100)
    m0, g0 = make('disc', {'#hzNoParry': 0, '#hzNoDodge': 1}, r=30, tell=20, dmg=100)
    m2, g2 = make('disc', {'#hzNoParry': 2}, r=30, tell=20, dmg=100)
    ck('fw B-01 the module options: noparry 1 -> unparriable, 0 -> parryable even when no-dodge, 2 (glint=False) -> stored as 1',
       (e(m1, 'mbHzNP'), e(m0, 'mbHzNP'), e(m2, 'mbHzNP')) == (1, 0, 1), (e(m1, 'mbHzNP'), e(m0, 'mbHzNP'), e(m2, 'mbHzNP')))
    kill_hz()
    sys.path.insert(0, str(DP / 'tools'))
    import mboss_lib as L
    o1, o2 = L.hz_opts(noparry=1), L.hz_opts(noparry=1, glint=False)
    bad = False
    try:
        L.hz_opts(glint=False)
    except AssertionError:
        bad = True
    ck('fw B-01 mboss_lib.hz_opts: noparry=1 -> #hzNoParry 1, + glint=False -> 2, glint=False alone is refused',
       'scoreboard players set #hzNoParry mb 1' in o1 and 'scoreboard players set #hzNoParry mb 2' in o2 and bad, (o1, o2, bad))
    # ---- B-02 / B-04: hz/np_auto
    cases = [('unparriable, dodgeable, tell 20', {'#hzNoParry': 1}, dict(r=60, tell=20, dmg=100), 1),
             ('... tell 12', {'#hzNoParry': 1}, dict(r=60, tell=12, dmg=100), 1),
             ('... tell 11 (made too late: the module warns)', {'#hzNoParry': 1}, dict(r=60, tell=11, dmg=100), 0),
             ('... tell 1 (a strike-frame hazard)', {'#hzNoParry': 1}, dict(r=60, tell=1, dmg=100), 0),
             ('... glint=False', {'#hzNoParry': 2}, dict(r=60, tell=20, dmg=100), 0),
             ('... telegraph only (dmg 0)', {'#hzNoParry': 1}, dict(r=60, tell=20, dmg=0), 0),
             ('no-dodge (position only)', {'#hzNoDodge': 1}, dict(r=60, tell=20, dmg=100), 0),
             ('re-arming (a lingering field)', {'#hzRearm': 10}, dict(r=60, tell=20, dmg=100), 0),
             ('per mille, dodgeable, tell 44', {'#hzPm': 250}, dict(r=60, tell=44, dmg=1), 1),
             ('parryable', {}, dict(r=60, tell=20, dmg=100), 0)]
    got = [(n, make('disc', o, **m)[1], x) for n, o, m, x in cases]
    kill_hz()
    ck('fw B-02 / B-04 hz/np_auto: the glint only for an unparriable hazard that hits, can be dodged, is not re-arming and is '
       'made >= 12 t before its strike', all(g == x for _, g, x in got), [r for r in got if r[1] != r[2]])
    # ---- the gate
    s.t += 40
    n0 = len(s.glints)
    s.call('rlk:mboss/np_glint', bc())
    s.call('rlk:mboss/np_glint', bc())
    s.call('rlk:mboss/np_glint_here', bc())
    n1 = len(s.glints) - n0
    s.t += int(s.sc('#npGap', 'tmp') or 10)
    s.call('rlk:mboss/np_glint_here', Ctx(b, (b.pos[0], b.pos[1] + 5.0, b.pos[2]), (0.0, 0.0)))
    n2 = len(s.glints) - n0
    here = s.glints[-1][1]
    s.t += 40
    s.setsc('#mbNpOwn', 'mb', 1)
    s.call('rlk:mboss/np_glint', bc())
    s.setsc('#mbNpOwn', 'mb', 0)
    s.setsc('#mbCine', 'mb', 1)
    s.call('rlk:mboss/np_glint', bc())
    s.call('rlk:mboss/np_glint_here', bc())
    s.setsc('#mbCine', 'mb', 0)
    n3 = len(s.glints) - n0
    ck('fw gate: once per #npGap for np_glint and np_glint_here together, again after it, never with #mbNpOwn 1 or in a cutscene',
       (n1, n2, n3) == (1, 2, 2), (n1, n2, n3))
    ck('fw np_glint_here draws at the execution position', abs(here[1] - (b.pos[1] + 5.0)) < 1e-6, here)
    # ---- B-03: the glint point
    reg = json.loads((DP / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
    pts = {x['id']: L.glint_of(x) for x in reg['boss'] if x.get('enabled', True)}
    ck('fw B-03 every boss\'s glint point is >= 1 b above the body anchor (never at or under the floor)',
       all(v[0] >= 1.0 for v in pts.values()), pts)
    ck('fw B-03 the proxy bosses (a 0.2-b husk under a big rig) have their own registry point',
       all('glint' in x for x in reg['boss'] if x.get('px') and x['id'] in ('azhdaha', 'apep')),
       [x['id'] for x in reg['boss'] if x.get('px') and 'glint' not in x])
    s.t += 40
    s.call('rlk:mboss/np_glint', Ctx(None, (0.0, 0.0, 0.0), (0.0, 0.0)))
    at = s.glints[-1][1]
    up, fwd = pts['guardian']
    import math
    yaw = math.radians(b.rot[0])
    exp = (b.pos[0] - math.sin(yaw) * fwd, b.pos[1] + up, b.pos[2] + math.cos(yaw) * fwd)
    ck('fw B-03 np_glint (any executor) draws at the body anchor + the registry point', all(abs(a - x) < 0.01 for a, x in zip(at, exp)),
       (at, exp))
    ck('fw B-03 static: no glint function reads the husk\'s eyes (np_glint, np_glint_here, d/np_at, hz/np_auto)',
       not any('anchored eyes' in text(f) for f in ('mboss/np_glint', 'mboss/np_glint_here', 'mboss/d/np_at', 'mboss/hz/np_auto'))
       and 'mboss/hz/np_auto' in text('mboss/hz/init') and 'np_glint' not in '\n'.join(cmds('mboss/hz/init')))
    # ---- B-10 + A-04: one volley = one answer
    def volley(answer, pm=False):
        """Two hazards of one group on the player; `answer` to the first; returns (dodged1, group consumed, HP lost by the second)."""
        kill_hz()
        s.setsc('#mbCine', 'mb', 0)
        s.t += 60
        pl.pos = [b.pos[0], b.pos[1], b.pos[2] + 2.0]
        hp = e(pl, 'maxHealth')
        for o, v in (('curHealth', hp), ('dead', 0), ('dashInvT', 0), ('parAt', -1000000), ('parLk', -1000000),
                     ('parHit', -1000000), ('dgAt', -1000000), ('dgRw', -1000000), ('shieldHP', 0), ('gShield', 0)):
            s.setsc(('e', pl.id), o, v)
        s.call('rlk:mboss/grp_new', C0)
        ms = []
        for k in range(2):
            opts = {'#hzGrp': s.sc('#mbGrp', 'mb'), '#hzKB': 0}
            if pm:
                opts['#hzPm'] = 100
            s.call('rlk:mboss/opts_reset', C0)
            for o, v in opts.items():
                s.setsc(o, 'mb', v)
            ids = {x.id for x in s.ents}
            s.call('rlk:mboss/hz/disc', bc(), {'r': 80, 'tell': 1, 'dmg': 100})
            ms.append([x for x in s.ents if x.alive and 'rlk_mb_hz' in x.tags and x.id not in ids][0])
        now = 100000 + s.t
        if answer == 'pdodge':
            s.setsc(('e', pl.id), 'dgAt', now)
        elif answer == 'parry3':
            s.setsc(('e', pl.id), 'parAt', now)
        elif answer == 'parry2':
            s.setsc(('e', pl.id), 'parAt', now - 4)
        elif answer == 'iframes':
            s.setsc(('e', pl.id), 'dashInvT', 5)
        s.call('rlk:mboss/hz/hurt', Ctx(ms[0], tuple(ms[0].pos), (0.0, 0.0)))
        d1 = s.sc('#dodged', 'tmp')
        consumed = e(ms[1], 'mbHzHit') == 1
        s.setsc(('e', pl.id), 'dashInvT', 0)
        s.t += 1                                    # the next wedge, one tick later: the press is spent
        hp1 = e(pl, 'curHealth')
        if not consumed:
            s.call('rlk:mboss/hz/hurt', Ctx(ms[1], tuple(ms[1].pos), (0.0, 0.0)))
        return d1, consumed, hp1 - e(pl, 'curHealth')

    res = {a: volley(a) for a in ('none', 'parry2', 'parry3', 'pdodge', 'iframes')}
    ck('fw B-10 + A-04 a landed hit and a tier-2 parry consume the volley group (as before)',
       res['none'][1] and res['parry2'][1], res)
    ck('fw A-04 a perfect parry consumes the volley group: the next member does not hit', res['parry3'] == (1, True, 0), res['parry3'])
    ck('fw B-10 a perfect dodge consumes the volley group: the wedge one tick later does not hit', res['pdodge'] == (1, True, 0),
       res['pdodge'])
    ck('fw B-10 burst / revive i-frames avoid the hit but do not consume the group (the next member hits)',
       res['iframes'][0] == 1 and not res['iframes'][1] and res['iframes'][2] > 0, res['iframes'])
    rp = volley('pdodge', pm=True)
    ck('fw B-10 the per-mille path: a perfect dodge of one member consumes the group too', rp == (1, True, 0), rp)
    ck('fw static: hz/hurt, pj/hit and the per-mille dodge path decide through mboss/grp_hit',
       all('rlk:mboss/grp_hit' in text(f) for f in ('mboss/hz/hurt', 'mboss/pj/hit', 'mboss/hz/hurt_pm_dodge'))
       and all(k in text('mboss/grp_hit') for k in ('#dodged tmp matches 0', '#parT tmp matches 3', '#pdg tmp matches 1')))
    kill_hz()


def t_b08():
    s, ok, azsim, Ctx, C0 = boss_world('special', bid='tachy')
    if not ck('b08 0 a 타키 fight', ok):
        return
    b = azsim.body_of(s)
    pl = s.player()

    def W():
        for x in [x for x in s.ents if x.alive and 'rlk_mob' in x.tags and x.etype != 'player']:
            if (s.sc(('e', x.id), 'balT') or 0) >= 1 and 'rlk_mb_dying' not in x.tags:
                s.call('rlk:bal/tick', Ctx(x, tuple(x.pos), tuple(x.rot)))
        s.setsc(('e', pl.id), 'curHealth', s.sc(('e', pl.id), 'maxHealth'))
        azsim.world(s)
    found = None
    for attempt in range(6):
        s.call('rlk:mboss/test/pattern', Ctx(pl, tuple(pl.pos), tuple(pl.rot)), {'id': 3})
        for _ in range(260):
            W()
            if s.sc('#pat', 'tk') == 3 and b.pos[1] > 201.3 and s.call('rlk:mboss/d/bal_ok', Ctx(b, tuple(b.pos), tuple(b.rot))):
                found = b.pos[1]
                break
        if found:
            break
    if not ck('b08 1 pattern 3 (옆걸음 4연격) lifts the body off the floor in its hop (> 0.3 b) in an allowed state', found, b.pos):
        return
    s.call('rlk:bal/hit', Ctx(b, tuple(b.pos), tuple(b.rot)), {'n': 12})
    y0 = b.pos[1]
    ys = []
    for _ in range(100):
        W()
        ys.append(b.pos[1])
    ck(f'b08 2 the balance groggy from y {found:.2f} puts her on the floor at once and she stays there for its 100 t',
       abs(y0 - 201.0) < 0.05 and max(abs(y - 201.0) for y in ys) < 0.05 and s.sc(('e', b.id), 'grgT') == 0,
       (y0, min(ys), max(ys), s.sc(('e', b.id), 'grgT')))
    ck('b08 static: bal_on calls core/ground after the move stop', 'boss/tachy/core/ground' in text('boss/tachy/bal_on')
       and 'mboss/mv/ok' in text('boss/tachy/core/ground'))


def t_b09():
    s, ok, azsim, Ctx, C0 = boss_world('chapter', bid='apep', n=3)
    if not ck('b09 0 an 아펩 fight', ok):
        return
    b = azsim.body_of(s)
    bc = lambda: Ctx(b, tuple(b.pos), tuple(b.rot))  # noqa: E731
    e = lambda o: s.sc(('e', b.id), o)  # noqa: E731
    ck('b09 1 the body has its 12 pips and takes one in play', e('bal') == 12 and s.call('rlk:bal/hit', bc(), {'n': 1}) and e('bal') == 11,
       e('bal'))
    s.call('rlk:boss/apep/svc/park', C0)
    inv = 'rlk_mb_inv' in b.tags
    r = [s.call('rlk:bal/hit', bc(), {'n': 1}) for _ in range(12)]
    ck('b09 2 parked for the revival phase (untargetable): 12 perfect-parry pips are refused, the gauge and the pending flag stay',
       inv and not any(r) and e('bal') == 11 and 'rlk_bal_pend' not in b.tags and (e('grgT') or 0) == 0,
       (inv, r, e('bal'), b.tags & {'rlk_bal_pend'}))
    s.call('rlk:boss/apep/svc/unpark', C0)
    s.call('rlk:boss/apep/svc/targetable', C0)
    for x in list(b.tags):
        if x in ('rlk_mb_inv', 'rlk_mb_pxinv'):
            b.tags.discard(x)
    ck('b09 3 back in play: a pip is taken again', bool(s.call('rlk:bal/hit', bc(), {'n': 1})) and e('bal') == 10, e('bal'))
    ck('b09 static: bal/boss/may refuses an untargetable registry body',
       any('tag=rlk_mb_body,tag=rlk_mb_inv' in l and 'return fail' in l for l in cmds('bal/boss/may')))


# ============================================================================================ mobs (bal/tests/lib, a child)
def t_mobs():
    sys.path.insert(0, str(HERE.parents[1] / 'bal/tests/lib'))
    from balsim import BalSim
    real = ('rlk:cm/ar/', 'rlk:player/def/ctx_cm', 'rlk:player/def/ctx_owner', 'rlk:cm/hit_pl', 'rlk:cm/ci/r_hit',
            'rlk:cm/cc/flock', 'rlk:cm/cc/lib/pre')

    def sim():
        s = BalSim(DP, extra_real=real)
        s.is_real = lambda fid, f=s.is_real: (fid in ('rlk:cm/hit_pl', 'rlk:cm/ci/r_hit', 'rlk:cm/ci/r_hit_own', 'rlk:cm/cc/flock',
                                                       'rlk:cm/cc/flock_one', 'rlk:cm/cc/flock_ram', 'rlk:player/def/ctx_cm',
                                                       'rlk:player/def/ctx_owner')
                                              or fid.startswith('rlk:cm/ar/') and not fid.startswith('rlk:cm/ar/rig')
                                              or (f(fid) and fid != 'rlk:cm/hit_pl2'))
        s.run('bal/load')
        s.hc = []
        s.stub_fns['rlk:cm/hit_pl2'] = lambda sm, ctx, macro: sm.hc.append(
            sorted((x.etype, tuple(sorted(t for t in x.tags if t.startswith('rlk_cm_')))) for x in sm.ents if x.alive and 'rlk_hc_atk' in x.tags)) or 1
        return s

    def brain(s, m, extra=(), **scores):
        tags = ['rlk_room', 'rlk_zmob', 'rlk_cmb', f'rlk_cm_{m}'] + list(extra)
        base = dict(cmId=7, cmS=0, cmCd=0, cmCd2=0, stunT=-1, frzT=0, mlv=3)
        base.update(scores)
        e = s.spawn('husk', tags=tags, **base)
        e.tags.add('rlk_mob')
        s.run('bal/init', e)
        return e

    # ---- B-06 the archer's arrow
    s = sim()
    s.spawn('player', pos=(6.5, 201.0, 0.5), tags=('rlk_body', 'player'))
    s.spawn('marker', pos=(6.5, 201.0, 0.5), tags=('rlk_cmaim',))
    ar = brain(s, 'ar')
    s.setsc('#cid', 'tmp', 7)
    for k, v in (('#cmW_ar', 20), ('#cmW_arL', 6), ('#cmD_ar', 10), ('#clv', 3), ('#cmCd_ar', 60)):
        s.setsc(k, 'tmp', v)
    s.run('cm/ar/start', ar)
    s.run('cm/ar/fire', ar)
    arrows = [x for x in s.ents if x.alive and 'rlk_cmp_ar' in x.tags]
    ck('mobs B-06 the archer\'s arrow carries its owner\'s cmId', len(arrows) == 1 and s.s(arrows[0], 'cmId') == 7,
       [(sorted(x.tags), s.s(x, 'cmId')) for x in arrows])
    if arrows:
        s.setsc('#hcK', 'tmp', 0)
        s.run('player/def/ctx_cm', arrows[0])
        ck('mobs B-06 the arrow\'s hit context names the archer (the perfect parry\'s pip goes to its 4-pip gauge)',
           'rlk_hc_atk' in ar.tags and s.s(ar, 'balMax') == 4, sorted(ar.tags))
        s.run('bal/hit', ar, {'n': 1})
        ck('mobs B-06 ... and rlk:bal/hit on that attacker takes one of the 4 pips', s.s(ar, 'bal') == 3, s.s(ar, 'bal'))
    # ---- B-07 the conjurer's cicins
    s = sim()
    s.spawn('player', pos=(6.5, 201.0, 0.5), tags=('rlk_body', 'player'))
    cc = brain(s, 'cc', extra=('rlk_c2e',), cmD=0, c2eF=1, c2eQ=1)
    cis = []
    for k in range(4):
        c = s.spawn('husk', pos=(2.5 + k, 201.0, 2.5), tags=('rlk_room', 'rlk_cm_ci', 'rlk_cmlink', 'rlk_cmsync', 'rlk_mob'),
                    cmId=20 + k, c2eOw=7, cmS=0, frzT=0, mlv=3, cmCd=0)
        cis.append(c)
    s.setsc('#cid', 'tmp', 7)
    s.setsc('#eStep', 'tmp', 1)
    s.stub_fns['rlk:cm/ci/r_start'] = lambda sm, ctx, macro: sm.set(ctx.ex, 'cmS', 0) or 1
    s.stubbed.clear()
    s.run('cm/cc/flock', cc)
    free = len(s.stub_calls(r'cm/ci/r_start$'))
    s.run('bal/hit', cc, {'n': 7})
    grg = s.s(cc, 'grgT')
    s.stubbed.clear()
    for _ in range((grg or 1) - 1):
        s.run('bal/tick', cc)
        s.set(cc, 'cmD', 0)
        s.run('cm/cc/flock', cc)
    during = len(s.stub_calls(r'cm/ci/r_start$'))
    s.run('bal/tick', cc)
    s.stubbed.clear()
    s.set(cc, 'cmD', 0)
    s.run('cm/cc/flock', cc)
    after = len(s.stub_calls(r'cm/ci/r_start$'))
    ck('mobs B-07 the conjurer sends a cicin when free, none during her 80-t groggy, one again right after it',
       (free, grg, during, after) == (1, 80, 0, 1), (free, grg, during, after))
    s.hc.clear()
    s.setsc('#hcK', 'tmp', 0)
    s.run('cm/ci/r_hit', cis[0])
    ck('mobs B-07 an owned cicin\'s ram is judged with its caster as the attacker (her 7-pip gauge), its own id put back',
       s.hc == [[('husk', ('rlk_cm_cc',))]] and s.s(cis[0], 'cmId') == 20, (s.hc, s.s(cis[0], 'cmId')))
    wild = s.spawn('husk', pos=(3.5, 201.0, 4.5), tags=('rlk_room', 'rlk_cm_ci', 'rlk_cmb', 'rlk_mob'), cmId=31, c2eOw=0, mlv=3)
    s.hc.clear()
    s.setsc('#hcK', 'tmp', 0)
    s.run('cm/ci/r_hit', wild)
    ck('mobs B-07 a wild cicin (its own brain) still hits as itself', s.hc == [[('husk', ('rlk_cm_ci',))]], s.hc)


# ============================================================================================ table (hzlog logs)
def t_table():
    sys.path.insert(0, str(HERE))
    import np_table as T
    bosses = list(RULED)
    if 'logs' in OPT:
        logs, tag = Path(OPT['logs']), OPT.get('tag', 'new')
    else:
        logs, tag = Path(tempfile.mkdtemp(prefix='np_')), 't'
        jobs = [(b, m) for m in ('pat', 'dodge') for b in bosses]
        running = []
        maxj = int(OPT.get('jobs', 3))
        while jobs or running:
            while jobs and len(running) < maxj:
                b, m = jobs.pop(0)
                cmd = [sys.executable, str(HERE / 'hzlog.py'), str(DP), b, 'pat', f'--out={logs}/{tag}_{b}_{m}.json']
                if m == 'dodge':
                    cmd.append('--dodge')
                running.append((b, m, subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)))
            b, m, p = running.pop(0)
            err = p.communicate()[1]
            if p.returncode:
                ck(f'table hzlog {b} {m} ran', False, err[-600:])
    for b in bosses:
        pat, dodge = T.load(logs, tag, b, 'pat'), T.load(logs, tag, b, 'dodge')
        if not ck(f'table {b} 0 the logs exist', pat is not None and dodge is not None, (logs, tag)):
            continue
        rows = T.rows_of(pat, dodge)
        u = {g for g, r in rows.items() if 'U' in r['st']}
        nat = {g for g, r in rows.items() if 'U-ND' in r['st'] or 'U-field' in r['st']}
        ck(f'table {b} 1 unparriable-and-dodgeable patterns are exactly the ruled list {sorted(RULED[b][0])} of {len(rows)} groups',
           u == RULED[b][0], sorted(u ^ RULED[b][0]))
        ck(f'table {b} 2 the patterns unparriable by nature (no-dodge / lingering, no glint) are {sorted(RULED[b][1])}', nat == RULED[b][1],
           sorted(nat ^ RULED[b][1]))
        bad_lead, no_glint, glint_on_other, low, mixed_grp, mixed_strike, undodged, nd_dodged = [], [], [], [], [], [], [], []
        for tid, v in pat.items():
            gl = v['glint']
            hz = [h for h in v['hz'] if h['D'] or h['PM']]
            u_spans = []
            for h in hz:
                st = T.state_of(h)
                g = T.group_of(h['src'])
                if st == 'U':
                    ld = T.glint_lead(h, gl)
                    floor = LEAD_EXC.get((b, g), LEAD_BIG)
                    if ld is None and h.get('strike') is not None:
                        no_glint.append((tid, h['src'], h['t']))
                    elif ld is not None and ld < floor:
                        bad_lead.append((tid, h['src'], ld))
                    if h.get('strike') is not None:
                        u_spans.append((h['strike'] - T.GLINT_BACK, h['strike']))
            end = v['t0'] + len(v['cmd'])            # the last tick watched: a glint in its last GLINT_BACK ticks may
            for x in gl:                             # announce a strike after the window
                if x['dy'] < 1.0:
                    low.append((tid, x['src'], x['dy']))
                if x['t'] <= end - T.GLINT_BACK and not any(a <= x['t'] <= z - LEAD for a, z in u_spans):
                    glint_on_other.append((tid, x['src'], x['t']))
            # one answer per volley / strike: never a parryable hazard (answer: F) beside an unparriable one whose answer is
            # the dodge. (A no-dodge part - the side lanes of Azhdaha's 성동격서, her whip - is a place to leave, whatever
            # else the strike holds: those keep their own tells and are not counted here.)
            grp = {}
            for h in hz:
                st = T.state_of(h)
                if st not in ('P', 'U'):
                    continue
                if h['G']:
                    grp.setdefault(h['G'], set()).add(st)
                if h.get('strike') is not None:
                    key = (h['src'].rsplit('/', 1)[0] if '/k/' in h['src'] else h['src'], h['strike'], h['G'])
                    grp.setdefault(('s',) + key, set()).add(st)
            mixed_grp += [(tid, k) for k, x in grp.items() if len(x) > 1 and not isinstance(k, tuple)]
            mixed_strike += [(tid, k) for k, x in grp.items() if len(x) > 1 and isinstance(k, tuple)]
        ck(f'table {b} 3 every unparriable hazard that can be dodged has its warning glint (B-02)', not no_glint, no_glint[:6])
        ck(f'table {b} 4 ... at least {LEAD_BIG} t before the strike (apep\'s second tail swing: 16 t, right after the first)', not bad_lead, bad_lead[:6])
        ck(f'table {b} 5 no glint without such a hazard >= {LEAD} t after it (B-04: none for no-dodge / lingering / parryable)',
           not glint_on_other, glint_on_other[:6])
        ck(f'table {b} 6 every glint is >= 1 b above the arena floor (B-03)', not low, low[:6])
        ck(f'table {b} 7 no volley group mixes parryable hazards with unparriable ones to dodge (one answer per volley)', not mixed_grp, mixed_grp[:6])
        ck(f'table {b} 8 no strike (same pattern function, strike tick and group) mixes them', not mixed_strike, mixed_strike[:6])
        seq = []
        for tid, v in dodge.items():
            last = {}
            for h in v['hits']:
                if h['kind'] not in ('hz', 'pm') or h['hz'] is None:
                    continue
                rec = v['hz'][h['hz']]
                st = T.state_of(rec)
                if st == 'U' and not h['dodged']:
                    undodged.append((tid, h['src'], h['t']))
                if st == 'U-ND' and h['dodged']:
                    nd_dodged.append((tid, h['src'], h['t']))
                if st == 'U' and h['dodged']:
                    g = rec['G'] or ('h', rec['i'])
                    if g not in last:
                        last[g] = h['t']
            ts = sorted(last.values())
            seq += [(tid, a, z) for a, z in zip(ts, ts[1:]) if z - a < DODGE_GAP]
        ck(f'table {b} 9 a perfect dodge avoids every unparriable-and-dodgeable hit', not undodged, undodged[:6])
        ck(f'table {b} 10 ... and no no-dodge hit (those keep their own tells, no glint)', not nd_dodged, nd_dodged[:6])
        ck(f'table {b} 11 two unparriable strikes a dodge must answer are never closer than {DODGE_GAP} t (the dodge cooldown)',
           not seq, seq[:6])


if __name__ == '__main__':
    if '--child-mobs' in sys.argv:
        t_mobs()
    else:
        for sec in SECT:
            print(f'--- {sec}', flush=True)
            try:
                if sec == 'mobs':
                    r = subprocess.run([sys.executable, str(Path(__file__)), str(DP), '--child-mobs'], capture_output=True, text=True)
                    out = [l for l in r.stdout.splitlines() if l.startswith(('PASS', 'FAIL'))]
                    print('\n'.join(out) + ('' if out and not r.returncode else '\n' + r.stdout[-1500:] + r.stderr[-3000:]), flush=True)
                    R.extend((l[5:], l.startswith('PASS')) for l in out)
                    if not out or r.returncode:
                        ck('mobs (child) ran', False, r.returncode)
                else:
                    {'fw': t_fw, 'b08': t_b08, 'b09': t_b09, 'table': t_table}[sec]()
            except Exception as ex:  # noqa: BLE001
                import traceback
                traceback.print_exc()
                ck(f'{sec} crashed', False, repr(ex))
    bad = [r for r in R if not r[1]]
    if '--child-mobs' not in sys.argv:
        print(f'\ntest_np: {len(R) - len(bad)}/{len(R)} passed' + (f', {len(bad)} FAILED' if bad else ''))
    sys.exit(1 if bad else 0)
