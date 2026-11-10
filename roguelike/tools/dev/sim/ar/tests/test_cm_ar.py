#!/usr/bin/env python3
"""test_cm_ar.py: S1 of the 아를레키노 plan (scratchpad ar/PLAN.md §11.3, ar/contract.md §3.1): the chapter-boss framework
needs of the chapter-4 boss, on the tree under test.

    python3 test_cm_ar.py <worktree>/roguelike [section ...]

 1. FN-1 lib + static: mboss_lib.hz_opts(bol=) / pj_opts(bol=) lines and range checks, api.fn1_ready(); the generated
    hit paths against the D0 base (eb0a38a): mboss/hurt +1 command, hz/hurt and pj/hit unchanged, hz/init and pj/launch
    +1, opts_reset unchanged; the new functions (hurt_bol, hz/hurt_pm_bol, hz/init_bol, pj/init_bol)
 2. FN-1 runtime on cproto (cp_test arena, the shipped registry): x #mbBolRe / 100 only on bol hazards (unset = 100,
    250 = x 2.5 of the raw damage), the event #mbHitBol once per landed hit, a dodged / cine-refused hit gives none, the
    volley group, a re-arming hazard (one event per landed hit), a bol projectile, a bol per-mille hazard (the share as
    made: S5, per-mille hits are not multiplied), the one-shot options spent (reset), cleanup_fight (#mbBolRe 100, the rest unset)
 3. FN-1 leaves mid-boss fights alone: a proto fight with strikes and a fieldgen fight hold no FN-1 name, no mbBol score
 4. routing ch1..ch6: the shipped registry (arlecchino disabled: chapter 4 = Raiden) and a variant with arlecchino
    enabled + route:true (ch4 -> arlecchino, ch1 azhdaha, ch3 apep, ch2 / 5 / 6 Raiden); #cbForce 12 under #mbTest
 5. FN-3 the px:false chapter path (variant, arlecchino on; the module is a knsim stub while S3's is absent): creg
    record, entrance -> cprep / forceload / the fl_ruins build job (stamp, sentinel), gate, start (#mbMode 1, #mbAr 4,
    #mbPx 0, no proxies, a plain shielded body), title, pool 64 %, music 1 = crimson forest len 6076, hits through
    cb/inc/arlecchino and the floor, the phase switch (repool 36, title, music 2), pause / resume, /reload, kill (boss
    economy, k_chapter, forceload released), cancel (the gate returns with the same cprep), lose (test/lose), the test
    aliases (boss/test/chapter, boss/test/pattern)
 6. music pool: the crimson forest track table, music_len, the registry len, load_registry's pool rule
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE / 'lib'))
import cmsim as M  # noqa: E402
import knsim as K  # noqa: E402
from mcsim import Ctx, Ent  # noqa: E402

DP = Path(sys.argv[1]).resolve()
ONLY = set(sys.argv[2:])
sys.path.insert(0, str(DP / 'tools'))
import mboss_lib as L  # noqa: E402

C0 = M.C0
check = M.check
BASE = 'eb0a38a'
REG = json.loads((DP / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
F = DP / 'data/rlk/function'
CP = REG['arenas']['cp_test']
AR = REG['arenas']['fl_ruins']
GIT = DP.parent if (DP.parent / '.git').exists() else Path('/home/user/rlk')


def want(n):
    return not ONLY or str(n) in ONLY


def st(s):
    return s.storage.setdefault('rlk:mboss', {})


def cmds_of(text):
    return [x for x in text.split('\n') if x.strip() and not x.lstrip().startswith('#')]


def base_text(rel):
    try:
        return subprocess.run(['git', '-C', str(GIT), 'show', f'{BASE}:roguelike/data/rlk/function/{rel}.mcfunction'],
                              capture_output=True, check=True, text=True).stdout
    except subprocess.CalledProcessError:
        return None


def tree_text(rel, root=DP):
    p = root / f'data/rlk/function/{rel}.mcfunction'
    return p.read_text(encoding='utf-8') if p.exists() else None


def at(x, z, y=201.0):
    return Ctx(None, (x, y, z), (0.0, 0.0))


def opt(s, **kw):
    for k, v in kw.items():
        s.setsc('#' + k, 'mb', v)


def hz(s, hid):
    m = [e for e in s.ents if e.alive and 'rlk_mb_hz' in e.tags and M.esc(s, e, 'mbHzI') == hid]
    return m[0] if m else None


def disc(s, x, z, r=30, tell=20, dmg=50, **kw):
    opt(s, **kw)
    s.call('rlk:mboss/hz/disc', at(x, z), {'r': r, 'tell': tell, 'dmg': dmg})
    return M.mb(s, '#hzLast')


def logged(s):
    """Wrap s.call: [(t, fid, #cmDmg at cm/hit_pl2, #dodged after)], the i-frames (s.ifr) set right before each hit."""
    log = []
    orig = s.call

    def call(fid, ctx, macro=None):
        if fid == 'rlk:cm/hit_pl2' and getattr(s, 'ifr', False) and (s.sc('#mbNoDodge', 'mb') or 0) != 1 and ctx.ex is not None:
            s.setsc(('e', ctx.ex.id), 'dashInvT', 1)
        if fid == 'rlk:mboss/hz/hurt_pm' and getattr(s, 'ifr', False):
            s.setsc(('e', s.player().id), 'dashInvT', 1)
        rec = [s.t, fid, s.sc('#cmDmg', 'tmp') if fid == 'rlk:cm/hit_pl2' else None, None]
        log.append(rec)
        r = orig(fid, ctx, macro)
        rec[3] = s.sc('#dodged', 'tmp')
        return r
    s.call = call
    return log


def cm_dmg(log, i0):
    return [r[2] for r in log[i0:] if r[1] == 'rlk:cm/hit_pl2']


def called(log, i0, fid):
    return sum(1 for r in log[i0:] if r[1] == fid)


def fn1_state(s):
    return {k: M.mb(s, k) for k in K.FN1_NAMES}


def setup_cp():
    s, pl = M.setup(DP)
    s.setsc('#chapter', 'room', 2)
    log = logged(s)
    M.fight(s, 'cproto', 2)
    s.setsc('#cpCool', 'mb', 99999)
    s.setsc('#cpPat', 'mb', 0)
    s.call('rlk:mboss/lib_clear', C0)
    for o, v in (('curHealth', 50000), ('maxHealth', 50000), ('def', 0), ('dashInvT', 0), ('shieldHP', 0), ('gShield', 0)):
        s.setsc(('e', pl.id), o, v)
    pl.pos = [CP['cx'], 201.0, CP['cz']]
    M.moved(s)
    s.ifr = False
    return s, pl, log


def raw_dmg(s, pct):
    """mboss/hurt's raw damage before the clamp: atk x pct x dmgMul / 10000"""
    return M.mb(s, '#mbAtk') * pct * M.mb(s, '#mbDmgMul') // 10000


# ================================================================================================== 1 FN-1 lib + static
if want(1):
    print('== 1. FN-1: mboss_lib options, the generated hit paths against D0')
    check('1a hz_opts(bol=6) = one line #hzBol mb 6 (the option name of api FN1_HZ_SCORE)',
          L.hz_opts(bol=6) == ['scoreboard players set #hzBol mb 6'], L.hz_opts(bol=6))
    check('1b pj_opts(bol=6) = one line #pjBol mb 6', L.pj_opts(bol=6) == ['scoreboard players set #pjBol mb 6'], L.pj_opts(bol=6))
    check('1c the existing options keep their lines and order (bol last)',
          L.hz_opts(quiet=1, pm=450, pm_lethal=0, bol=1) == ['scoreboard players set #hzQuiet mb 1', 'scoreboard players set #hzPm mb 450',
                                                            'scoreboard players set #hzPmL mb 0', 'scoreboard players set #hzBol mb 1']
          and L.pj_opts(el=1, grp=True, bol=6) == ['scoreboard players set #pjEl mb 1', 'scoreboard players set #pjBol mb 6',
                                                    'scoreboard players operation #pjGrp mb = #mbGrp mb'],
          (L.hz_opts(quiet=1, pm=450, pm_lethal=0, bol=1), L.pj_opts(el=1, grp=True, bol=6)))
    bad = []
    for v in (0, 101, -1):
        for fn in (L.hz_opts, L.pj_opts):
            try:
                fn(bol=v)
                bad.append((fn.__name__, v))
            except AssertionError:
                pass
    check('1d bol outside 1..100 is refused by both helpers', not bad, bad)
    try:
        sys.path.insert(0, str(DP / 'tools'))
        import mboss_arlecchino.api as API  # noqa: E402
        check('1e api.fn1_ready() (the frozen names: #hzBol #pjBol #mbBolIn #mbBolRe #mbHitBol)', API.fn1_ready()
              and API.FN1_HZ_SCORE == ('#hzBol', 'mb') and API.FN1_PJ_SCORE == ('#pjBol', 'mb') and API.FN1_IN == ('#mbBolIn', 'mb')
              and API.FN1_RE == ('#mbBolRe', 'mb') and API.FN1_EVENT == ('#mbHitBol', 'mb'))
    except Exception as e:      # noqa: BLE001
        check('1e api.fn1_ready()', False, repr(e))
    delta = {}
    # combat overhaul lane C (11-10) on top of FN-1: mboss/hurt +1 (hurt_ctx + the #mbNoParry reset, the two no-dodge
    # branches -> one), hz/hurt / pj/hit +2 (#mbNoParry set / reset), hz/init +3 (mbHzNP, np_def, np_glint), pj/launch +2
    # (mbPjNP), opts_reset +2 (#hzNoParry / #pjNoParry), hurt_dodge -1 (#mbDodgeOk = perfect dodge / parry), hz/hurt_pm +4
    # (the judge with its context instead of the own dash line)
    LANE_C = {'mboss/hurt': 1, 'mboss/hz/hurt': 2, 'mboss/pj/hit': 2, 'mboss/hz/init': 3, 'mboss/pj/launch': 2,
              'mboss/opts_reset': 2, 'mboss/hurt_dodge': -1, 'mboss/hz/hurt_pm': 4}
    for rel, exp in (('mboss/hurt', 1), ('mboss/hz/hurt', 0), ('mboss/pj/hit', 0), ('mboss/hz/init', 1), ('mboss/pj/launch', 1),
                     ('mboss/opts_reset', 0), ('mboss/hz/make', 0), ('mboss/hurt_ev', 0), ('mboss/hurt_dodge', 0),
                     ('mboss/pl_dot', 0), ('mboss/hz/hurt_pm', 1)):
        exp += LANE_C.get(rel, 0)
        b, t = base_text(rel), tree_text(rel)
        delta[rel] = (len(cmds_of(t)) - len(cmds_of(b)), exp) if b and t else ('missing', exp)
    check('1f commands per call vs D0 (FN-1 + lane C): mboss/hurt +2 (every hit), hz/hurt / pj/hit +2, hurt_ev / pl_dot +0, '
          'hz/init +4 and pj/launch +3 (per creation), hz/hurt_pm +5 (per-mille hits only), opts_reset +2, hz/make +0, hurt_dodge -1',
          all(v[0] == v[1] for v in delta.values()), delta)
    bt, tt = cmds_of(base_text('mboss/hurt')), cmds_of(tree_text('mboss/hurt'))
    lane_c = {'function rlk:mboss/hurt_ctx', 'execute as @a[tag=player,limit=1] run function rlk:cm/hit_pl2',
              'scoreboard players set #mbNoParry mb 0'}
    extra = [x for x in tt if x not in bt and x not in lane_c]
    check('1g the one new mboss/hurt line: the bol branch after the raw damage, before the clamp',
          extra == ['execute if score @s mbBol matches 1.. run return run function rlk:mboss/hurt_bol']
          and tt.index(extra[0]) == tt.index('scoreboard players operation #cmDmg tmp /= #c10000 mb') + 1, extra)
    hb = tree_text('mboss/hurt_bol') or ''
    check('1h hurt_bol: #mbBolIn = mbBol, unset #mbBolRe -> 100, raw x #mbBolRe / 100, the hurt tail, #mbHitBol after a'
          ' landed hit, #mbBolIn reset',
          all(x in hb for x in ('scoreboard players operation #mbBolIn mb = @s mbBol',
                                'execute unless score #mbBolRe mb matches 0.. run scoreboard players set #mbBolRe mb 100',
                                'scoreboard players operation #cmDmg tmp *= #mbBolRe mb', 'scoreboard players operation #cmDmg tmp /= #c100 mb',
                                'function rlk:mboss/hurt_ev',
                                'execute if score #dodged tmp matches 0 run scoreboard players operation #mbHitBol mb = #mbBolIn mb',
                                'scoreboard players reset #mbBolIn mb'))
          and cmds_of(hb)[4:-2] == tt[tt.index(extra[0]) + 1:], hb[:200])
    check('1i the option functions spend their option (reset) and clamp to 100',
          all('scoreboard players reset #%s mb' % k in (tree_text(f) or '') and 'matches 101..' in (tree_text(f) or '')
              for f, k in (('mboss/hz/init_bol', 'hzBol'), ('mboss/pj/init_bol', 'pjBol'))))
    cf = tree_text('mboss/cleanup_fight') or ''
    check('1j cleanup_fight: #mbBolRe 100 only when set, #mbHitBol / #mbBolIn / #hzBol / #pjBol reset',
          'execute if score #mbBolRe mb matches -2147483648.. run scoreboard players set #mbBolRe mb 100' in cf
          and all(f'scoreboard players reset {k} mb' in cf for k in ('#mbHitBol', '#mbBolIn', '#hzBol', '#pjBol')))
    ini = tree_text('mboss/init') or ''
    check('1k init: the objective mbBol, the one-shot names reset, #mbBolRe 100 only when set (no new name at load)',
          'scoreboard objectives add mbBol dummy' in ini and 'scoreboard objectives remove mbBol' in (tree_text('mboss/uninstall') or '')
          and 'execute if score #mbBolRe mb matches -2147483648.. run scoreboard players set #mbBolRe mb 100' in ini
          and not [x for x in cmds_of(ini) if 'Bol' in x and x.startswith('scoreboard players set')])

# ================================================================================================== 2 FN-1 runtime
if want(2):
    print('== 2. FN-1 runtime (cproto, cp_test)')
    X, Z = CP['cx'], CP['cz']
    s, pl, log = setup_cp()
    check('2a a fresh chapter fight holds no FN-1 name', not K.fake_names(s), K.fake_names(s))
    hp0 = s.sc(('e', pl.id), 'curHealth')
    i0 = len(log)
    disc(s, X, Z, dmg=60)
    M.run(s, 24)
    plain = cm_dmg(log, i0)
    lost_plain = hp0 - s.sc(('e', pl.id), 'curHealth')
    check('2b a plain disc (no bol): one hit, raw damage atk x 60 x dmgMul / 10000, no #mbHitBol / #mbBolIn',
          plain == [max(1, raw_dmg(s, 60))] and lost_plain > 0 and M.mb(s, '#mbHitBol') is None and M.mb(s, '#mbBolIn') is None,
          (plain, raw_dmg(s, 60), lost_plain, fn1_state(s)))
    s.setsc(('e', pl.id), 'curHealth', hp0)
    i0 = len(log)
    hid = disc(s, X, Z, dmg=60, hzBol=6)
    m = hz(s, hid)
    check('2c a bol disc: the marker carries mbBol 6; #hzBol is spent (unset) by the call', m is not None and M.esc(s, m, 'mbBol') == 6
          and M.mb(s, '#hzBol') is None, (M.esc(s, m, 'mbBol') if m else None, M.mb(s, '#hzBol')))
    M.run(s, 24)
    got = cm_dmg(log, i0)
    check('2d #mbBolRe unset reads as 100: the same raw damage as the plain disc, the HP loss equal; hurt_bol ran once',
          got == plain and hp0 - s.sc(('e', pl.id), 'curHealth') == lost_plain and called(log, i0, 'rlk:mboss/hurt_bol') == 1,
          (got, plain, hp0 - s.sc(('e', pl.id), 'curHealth'), lost_plain))
    check('2e the landed bol hit: #mbHitBol 6, #mbHitEv 1, #mbBolIn reset afterwards',
          M.mb(s, '#mbHitBol') == 6 and M.mb(s, '#mbHitEv') >= 1 and M.mb(s, '#mbBolIn') is None, fn1_state(s))
    # x 250 %
    s.setsc('#mbHitBol', 'mb', 0)
    s.setsc('#mbBolRe', 'mb', 250)
    s.setsc(('e', pl.id), 'curHealth', hp0)
    i0 = len(log)
    disc(s, X, Z, dmg=60, hzBol=6)
    M.run(s, 24)
    got = cm_dmg(log, i0)
    exp = max(1, raw_dmg(s, 60) * 250 // 100)
    check(f'2f #mbBolRe 250: the raw damage x 2.5 before the clamp ({raw_dmg(s, 60)} -> {exp}), more HP lost; #mbHitBol 6',
          got == [exp] and hp0 - s.sc(('e', pl.id), 'curHealth') > lost_plain and M.mb(s, '#mbHitBol') == 6,
          (got, exp, hp0 - s.sc(('e', pl.id), 'curHealth'), lost_plain))
    s.setsc('#mbHitBol', 'mb', 0)
    s.setsc(('e', pl.id), 'curHealth', hp0)
    i0 = len(log)
    disc(s, X, Z, dmg=60)
    M.run(s, 24)
    check('2g ... a plain disc under #mbBolRe 250 keeps its damage and gives no event (x only on bol hazards)',
          cm_dmg(log, i0) == plain and (M.mb(s, '#mbHitBol') or 0) == 0, (cm_dmg(log, i0), plain, M.mb(s, '#mbHitBol')))
    # dodged
    s.ifr = True
    s.setsc('#mbDodgeEv', 'mb', 0)
    s.setsc(('e', pl.id), 'curHealth', hp0)
    hid = disc(s, X, Z, dmg=60, hzBol=6)
    m = hz(s, hid)
    M.run(s, 24)
    s.ifr = False
    check('2h a dodged bol hit (dash i-frames): no HP lost, a dodge event, no #mbHitBol, the hazard consumed',
          s.sc(('e', pl.id), 'curHealth') == hp0 and M.mb(s, '#mbDodgeEv') == 1 and (M.mb(s, '#mbHitBol') or 0) == 0
          and M.mb(s, '#mbBolIn') is None and (not m.alive or M.esc(s, m, 'mbHzHit') == 1), (s.sc(('e', pl.id), 'curHealth'), fn1_state(s)))
    # cine
    hid = disc(s, X, Z, dmg=60, hzBol=6, hzAct=40)
    m = hz(s, hid)
    s.call('rlk:mboss/cine/start', C0)
    s.setsc('#cpCine', 'mb', 999)                      # cproto ends a cine of its own when its clock is 0
    M.run(s, 24)
    check('2i during the cine a bol disc is refused, not consumed, no event', M.esc(s, m, 'mbHzHit') == 0 and (M.mb(s, '#mbHitBol') or 0) == 0
          and s.sc(('e', pl.id), 'curHealth') == hp0)
    s.setsc('#cpCine', 'mb', 0)
    s.call('rlk:mboss/cine/end', C0)
    M.run(s, 3)
    check('2j after the cine the same hazard lands: #mbHitBol 6', M.mb(s, '#mbHitBol') == 6 and s.sc(('e', pl.id), 'curHealth') < hp0,
          fn1_state(s))
    # volley group: two bol discs, one hit, one event
    s.setsc('#mbHitBol', 'mb', 0)
    s.call('rlk:mboss/grp_new', C0)
    i0 = len(log)
    for k in range(2):
        opt(s, hzBol=6)
        s.setsc('#hzGrp', 'mb', M.mb(s, '#mbGrp'))
        s.call('rlk:mboss/hz/disc', at(X, Z), {'r': 30, 'tell': 20, 'dmg': 60})
    M.run(s, 24)
    check('2k a volley group of two bol discs: one hit, hurt_bol once, the event once (6)',
          len(cm_dmg(log, i0)) == 1 and called(log, i0, 'rlk:mboss/hurt_bol') == 1 and M.mb(s, '#mbHitBol') == 6)
    # re-arming bol hazard: one event per landed hit
    events = []
    s.setsc('#mbHitBol', 'mb', 0)
    hid = disc(s, X, Z, dmg=10, hzBol=6, hzRearm=10, hzAct=45)
    for _ in range(60):
        M.world(s)
        if (M.mb(s, '#mbHitBol') or 0) == 6:
            events.append(s.t)
            s.setsc('#mbHitBol', 'mb', 0)          # the module reads and clears it
    check('2l a re-arming bol hazard (#hzRearm 10, active 45 t): one event per landed hit (3..5), each on a hit tick',
          3 <= len(events) <= 5, events)
    # projectile
    s.call('rlk:mboss/lib_clear', C0)
    s.setsc('#mbHitBol', 'mb', 0)
    s.setsc(('e', pl.id), 'curHealth', hp0)
    e = Ent('block_display', (X, 202.1, Z), (0.0, 0.0), ['rlk_room', 'rlk_mb_aux', 'rlk_mb_knpj'])
    s.ents.append(e)
    opt(s, pjBol=6)
    s.call('rlk:mboss/pj/launch', Ctx(e, tuple(e.pos), (0.0, 0.0)), {'spd': 1, 'life': 80, 'dmg': 60, 'hr': 6})
    check('2m a bol projectile: the prop carries mbBol 6, #pjBol spent', M.esc(s, e, 'mbBol') == 6 and M.mb(s, '#pjBol') is None)
    i0 = len(log)
    s.call('rlk:mboss/pj/hit', Ctx(e, tuple(e.pos), (0.0, 0.0)))
    check('2n its hit: raw x 2.5 (#mbBolRe 250), #mbHitBol 6, #mbBolIn reset',
          cm_dmg(log, i0) == [exp] and M.mb(s, '#mbHitBol') == 6 and M.mb(s, '#mbBolIn') is None, (cm_dmg(log, i0), exp, fn1_state(s)))
    e2 = Ent('block_display', (X, 202.1, Z), (0.0, 0.0), ['rlk_room', 'rlk_mb_aux', 'rlk_mb_knpj'])
    s.ents.append(e2)
    s.call('rlk:mboss/pj/launch', Ctx(e2, tuple(e2.pos), (0.0, 0.0)), {'spd': 1, 'life': 80, 'dmg': 60, 'hr': 6})
    s.setsc('#mbHitBol', 'mb', 0)
    i0 = len(log)
    s.call('rlk:mboss/pj/hit', Ctx(e2, tuple(e2.pos), (0.0, 0.0)))
    check('2o a plain projectile under #mbBolRe 250: no mbBol, its raw damage, no event',
          M.esc(s, e2, 'mbBol') is None and cm_dmg(log, i0) == plain and (M.mb(s, '#mbHitBol') or 0) == 0)
    # per mille
    s.call('rlk:mboss/lib_clear', C0)
    s.setsc('#mbHitBol', 'mb', 0)
    s.setsc(('e', pl.id), 'curHealth', 50000)
    s.setsc(('e', pl.id), 'def', 400)
    disc(s, X, Z, dmg=60, hzBol=6, hzPm=100, hzPmL=0)
    M.run(s, 24)
    # S5 (lead's balance decision, contract §3.1 amended): a per-mille hit keeps its per mille under #mbBolRe
    check('2p a bol per-mille hazard (100 per mille, #mbBolRe 250): still 100 per mille of 50000 = 5000 HP (not multiplied, '
          'defence ignored), #mbHitBol 6', s.sc(('e', pl.id), 'curHealth') == 45000 and M.mb(s, '#mbHitBol') == 6
          and M.mb(s, '#mbBolIn') is None, (s.sc(('e', pl.id), 'curHealth'), fn1_state(s)))
    s.setsc('#mbHitBol', 'mb', 0)
    s.setsc(('e', pl.id), 'curHealth', 50000)
    disc(s, X, Z, dmg=60, hzPm=100, hzPmL=0)
    M.run(s, 24)
    check('2q a plain per-mille hazard under #mbBolRe 250: 100 per mille = 5000 HP, no event',
          s.sc(('e', pl.id), 'curHealth') == 45000 and (M.mb(s, '#mbHitBol') or 0) == 0, s.sc(('e', pl.id), 'curHealth'))
    s.ifr = True
    s.setsc(('e', pl.id), 'curHealth', 50000)
    disc(s, X, Z, dmg=60, hzBol=6, hzPm=100, hzPmL=0)
    M.run(s, 24)
    s.ifr = False
    check('2r a dodged bol per-mille hazard: no HP lost, no event', s.sc(('e', pl.id), 'curHealth') == 50000
          and (M.mb(s, '#mbHitBol') or 0) == 0)
    s.setsc(('e', pl.id), 'def', 0)
    # the options never linger
    opt(s, hzBol=6)
    s.call('rlk:mboss/hz/disc', at(X, Z), {'r': 10, 'tell': 5, 'dmg': 0})
    check('2s every hazard kind consumes #hzBol (a dmg 0 telegraph too)', M.mb(s, '#hzBol') is None)
    # cleanup_fight
    opt(s, hzBol=3, pjBol=3, mbHitBol=6, mbBolIn=6)
    s.setsc('#mbBolRe', 'mb', 250)
    s.call('rlk:mboss/cleanup_fight', C0)
    check('2t cleanup_fight: #mbBolRe 100, #mbHitBol / #mbBolIn / #hzBol / #pjBol unset',
          fn1_state(s) == {'#hzBol': None, '#pjBol': None, '#mbBolIn': None, '#mbBolRe': 100, '#mbHitBol': None}, fn1_state(s))
    s.call('rlk:mboss/init', C0)
    check('2u /reload (mboss/init) keeps #mbBolRe at 100 and makes no other FN-1 name', fn1_state(s) == {'#hzBol': None, '#pjBol': None,
          '#mbBolIn': None, '#mbBolRe': 100, '#mbHitBol': None}, fn1_state(s))

# ================================================================================================== 3 mid-boss fights
if want(3):
    print('== 3. FN-1 leaves mid-boss fights alone')
    for force, label in ((99, 'proto'), (3, 'fieldgen'), (1, 'guardian')):
        s, zone, pl = M.A.setup(force=force, dp=DP, seed=1018)
        for o in ('curHealth', 'maxHealth'):
            s.setsc(('e', pl.id), o, 1000000)
        ok = M.A.to_fight(s, zone)
        hits = [0]
        orig = s.call

        def call(fid, ctx, macro=None, hits=hits, orig=orig):
            if fid == 'rlk:mboss/hurt_bol':
                hits[0] += 1
            return orig(fid, ctx, macro)
        s.call = call
        for i in range(500):
            b = M.A.body_of(s)
            if b is not None and i % 6 == 0 and (s.sc('#mbSt', 'mb') or 0) == 1:
                M.A.strike(s, b, 25, elem=(i // 6) % 8)
            M.A.world(s)
        n_hz = len(s.hz)
        check(f'3a {label}: a 500-t fight ({n_hz} hazards made, {len(s.dmg)} hits on the player) holds no FN-1 fake player, no '
              'mbBol score, never ran hurt_bol', ok and not K.fake_names(s) and not K.ent_scores(s, 'mbBol') and hits[0] == 0,
              (ok, K.fake_names(s), len(K.ent_scores(s, 'mbBol')), hits[0]))

# ================================================================================================== 4 routing
if want(4):
    print('== 4. routing ch1..ch6')

    def route(s, chapter, test=0, force=0):
        s.setsc('#mbTest', 'mb', test)
        s.setsc('#cbForce', 'mb', force)
        s.setsc('#mbForce', 'mb', 0)
        rd0 = s.sc('#RDLAYOUT', 'azs') or 0
        M.boss_map(s, chapter)
        cur = s.storage.get('rlk:room', {}).get('cur') or {}
        ids = sorted({z.get('boss_id') for z in cur.get('zones', []) if z.get('boss_id')})
        return ('raiden' if (s.sc('#RDLAYOUT', 'azs') or 0) - rd0 == 1 and not ids else ','.join(ids) or 'none')

    shipped = {1: 'azhdaha', 2: 'raiden', 3: 'apep', 4: 'arlecchino', 5: 'raiden', 6: 'raiden'}
    s, pl = M.setup(DP)
    got = {c: route(s, c) for c in range(1, 7)}
    check('4a the shipped registry (I1: arlecchino enabled and routed): ch1 azhdaha, ch3 apep, ch4 arlecchino, ch2 / ch5 / ch6 Raiden', got == shipped, got)
    b = K.registry(DP)['boss']
    ar = next(x for x in b if x['id'] == 'arlecchino')
    check('4b the registry entry: n 12, kind chapter, ch [4], px false, shield true, res {"*": 10}, arena fl_ruins; '
          'enabled and routed (I1)', ar['n'] == 12 and ar['kind'] == 'chapter' and ar['ch'] == [4] and ar['px'] is False
          and ar['shield'] is True and ar['res'] == {'*': 10} and ar['arena'] == 'fl_ruins' and ar['enabled'] is True
          and ar['route'] is True, ar)
    V, stubbed = K.variant_ar(DP, route=True, label='route')
    try:
        s, pl = M.setup(V)
        got = {c: route(s, c) for c in range(1, 7)}
        exp = {**shipped, 4: 'arlecchino'}
        check(f'4c variant enabled + route:true{" (stub module)" if stubbed else ""}: ch4 -> arlecchino, ch1 azhdaha, ch3 apep, '
              'ch2 / 5 / 6 Raiden', got == exp, got)
        rl = [x for x in (V / 'data/rlk/function/mboss/cb/route.mcfunction').read_text(encoding='utf-8').split('\n') if 'matches 4 ' in x]
        check('4d cb/route has the chapter-4 line of arlecchino', rl == ['execute if score #chapter room matches 4 run return run '
              'function rlk:mboss/cb/layout {id:"arlecchino"}'], rl)
        check('4e #cbForce 12 under #mbTest 1 lays out the arlecchino entrance in another chapter (2)',
              route(s, 2, test=1, force=12) == 'arlecchino')
        check('4f #cbForce 12 without #mbTest: ignored (chapter 2 Raiden); no routing path sets #mbForce',
              route(s, 2, test=0, force=12) == 'raiden' and (M.mb(s, '#mbForce') or 0) == 0)
    finally:
        M.drop_variant(V)
    V, _ = K.variant_ar(DP, route=False, label='noroute')
    try:
        s, pl = M.setup(V)
        got = {c: route(s, c) for c in range(1, 7)}
        check('4g enabled with route:false: chapter 4 stays Raiden (test/chapter only)', got == {**shipped, 4: 'raiden'}, got)
    finally:
        M.drop_variant(V)

# ================================================================================================== 5 FN-3 px:false path
if want(5):
    print('== 5. FN-3: the px:false chapter path (variant, arlecchino on)')
    V, stubbed = K.variant_ar(DP, route=True, label='fn3')
    try:
        VREG = K.registry(V)
        BX = AR['box']
        CH = {(cx, cz) for cx in range(BX['x0'] >> 4, (BX['x1'] >> 4) + 1) for cz in range(BX['z0'] >> 4, (BX['z1'] >> 4) + 1)}

        def objs(s, oact):
            return [e for e in s.ents if e.alive and 'rlk_obj' in e.tags and s.sc(('e', e.id), 'oact') == oact]

        def fresh(chapter=4):
            s, pl = M.setup(V)
            s.setsc('#chapter', 'room', chapter)
            s.setsc(('e', pl.id), 'gold', 0)
            s.cache.pop('rlk:combat/gold_absorb', None)
            return s, pl

        s, pl = fresh()
        rec = st(s)['cbyid'].get('arlecchino')
        check('5a creg / cbyid hold arlecchino: n 12, ar 4, px 0b, shield 1b, music 1 crimson forest len 6076, music 2 dragon',
              rec is not None and rec['n'] == 12 and rec.get('ar') == 4 and rec.get('px') in (0, False) and rec.get('shield') in (1, True)
              and rec['music']['1'] == {'ev': 'minecraft:music.nether.crimson_forest', 'len': 6076}
              and rec['music']['2']['ev'] == 'minecraft:music.dragon', rec and {k: rec.get(k) for k in ('n', 'ar', 'px', 'shield', 'music')})
        # entrance -> prep -> job
        s.setsc('#mbTest', 'mb', 1)
        s.setsc('#cbForce', 'mb', 12)
        zs = M.boss_map(s, 4)
        z9, gate = M.entrance(s, zs)
        cp = st(s).get('cprep', {}).get('arlecchino', {})
        check('5b the entrance build runs cb/prep: cprep.arlecchino (the prep hook texts), the fl_ruins box forceloaded, a build job',
              bool(cp.get('gate')) and CH <= set(s.fl) and (M.mb(s, '#mbArBuild') or 0) >= 1, (sorted(cp), len(CH & set(s.fl)), M.mb(s, '#mbArBuild')))
        pl.pos = [z9.pos[0], 201.0, z9.pos[2] + 4]
        n = 0
        while (M.mb(s, '#mbArBuild') or 0) > 0 and n < 400:
            M.world(s)
            n += 1
        sx, sy, sz = 760, 196, 8
        check(f'5c the build job finishes ({n} ticks): stamp built_fl_ruins "fl_ruins@1:day", look_fl_ruins day, the sentinel block',
              st(s).get('built_fl_ruins') == 'fl_ruins@1:day' and st(s).get('look_fl_ruins') == 'day'
              and s.blocks.get((sx, sy, sz)) == 'polished_deepslate', (st(s).get('built_fl_ruins'), s.blocks.get((sx, sy, sz))))
        g = M.gate_of(s)
        check('5d the gate object (oact 16) at the zone centre', g is not None and abs(g.pos[0] - z9.pos[0]) < 0.6)
        M.click(s, g)
        ok = M.until(s, lambda s: (M.mb(s, '#mbSt') or 0) == 1, 600)
        b = M.body_of(s)
        check('5e the gate -> cb/start -> the fight: #mbSt 1, #mbMode 1, #mbAr 4, #mbPx 0, #mbKind 1, no proxies',
              ok and M.mb(s, '#mbMode') == 1 and M.mb(s, '#mbAr') == 4 and (M.mb(s, '#mbPx') or 0) == 0 and not M.proxies(s),
              (ok, M.mb(s, '#mbMode'), M.mb(s, '#mbAr'), M.mb(s, '#mbPx'), len(M.proxies(s))))
        check('5f the body: a plain chapter body (rlk_mb_body, boss, no miniboss, no rlk_mb_big / rlk_mb_noshield: it keeps its '
              'click shield), at the arena centre', b is not None and 'miniboss' not in b.tags and 'rlk_mb_big' not in b.tags
              and 'rlk_mb_noshield' not in b.tags and abs(b.pos[0] - 760) < 1.5 and abs(b.pos[2] - 8) < 1.5, b and (sorted(b.tags), b.pos))
        tot = M.mb(s, '#mbTot')
        check('5g pool: mhpM = #mbTot x 64 % (phases[0]); the title from cprep', M.esc(s, b, 'mhpM') == tot * 64 // 100
              and st(s).get('cur', {}).get('title') is not None, (tot, M.esc(s, b, 'mhpM')))
        check('5h music 1 = minecraft:music.nether.crimson_forest, len 6076 (the pool re-pick period)',
              st(s).get('mus', {}).get('ev') == 'minecraft:music.nether.crimson_forest' and st(s).get('mus', {}).get('len') == 6076,
              st(s).get('mus'))
        check('5i the player is in the arena (start point r 22.5 south of the centre)', abs(pl.pos[0] - 760.5) < 1 and abs(pl.pos[2] - 30.5) < 1,
              pl.pos)
        h0 = M.esc(s, b, 'mhpC')
        M.A.strike(s, b, 400)
        M.run(s, 2)
        check('5j a hit on the body lands (combat/apply -> cb/inc/arlecchino -> the module on_hit), HP down',
              M.esc(s, b, 'mhpC') < h0 and (M.mb(s, '#knStubHits') or 0) >= 1 if stubbed else M.esc(s, b, 'mhpC') < h0,
              (h0, M.esc(s, b, 'mhpC')))
        s.setsc(('e', b.id), 'mhpC', 50)
        M.A.strike(s, b, 400)
        M.run(s, 3)
        if stubbed:
            check('5k the floor (#mbFloor 1) holds a lethal hit; the stub phase switch: repool 36 %, music 2, the title swapped, floor 0',
                  M.body_of(s) is not None and M.esc(s, b, 'mhpM') == tot * 36 // 100 and st(s).get('mus', {}).get('ev') == 'minecraft:music.dragon'
                  and (M.mb(s, '#mbFloor') or 0) == 0, (M.esc(s, b, 'mhpM'), tot * 36 // 100, st(s).get('mus'), M.mb(s, '#mbFloor')))
        # pause / resume
        p0 = M.mb(s, '#knStubPause') or 0
        for i in range(60):
            s.setsc(('e', pl.id), 'pkMode', 1 if i < 40 else 0)
            M.world(s)
        check('5l pause (selection screen 40 t) and resume: #mbPause back to 0, the body alive, the module pause hook ran',
              (M.mb(s, '#mbPause') or 0) == 0 and M.body_of(s) is not None and ((M.mb(s, '#knStubPause') or 0) > p0 if stubbed else True))
        # reload
        s.call('rlk:mboss/init', C0)
        M.run(s, 5)
        check('5m /reload mid-fight: the body survives (module reload hook), #mbPx 0, still no proxies, #mbSt 1',
              M.body_of(s) is not None and (M.mb(s, '#mbPx') or 0) == 0 and not M.proxies(s) and M.mb(s, '#mbSt') == 1
              and ((M.mb(s, '#knStubReload') or 0) >= 1 if stubbed else True))
        # kill (the real module holds its P1 floors 70 % / 1: a lethal hit is possible only in P2, test 31 = T skipped)
        if not stubbed:
            s.call('rlk:boss/test/pattern', Ctx(pl, tuple(pl.pos), (0, 0)), {'id': 31})
            M.run(s, 5)
        gold0 = s.sc(('e', pl.id), 'gold') or 0
        sap0 = s.sc('#SAP', 'azs') or 0
        b = M.body_of(s)
        s.setsc(('e', b.id), 'mhpC', 5)
        M.A.strike(s, b, 100000)
        dead = M.until(s, lambda s: M.body_of(s) is None, 300)
        ok = M.until(s, lambda s: bool(objs(s, 8)), 300)
        gmin, gmax, gmul, bsap = (s.sc(k, 'tmp') for k in ('#mobGoldMin', '#mobGoldMax', '#bossGoldMul', '#bossSapphire'))
        got = (s.sc(('e', pl.id), 'gold') or 0) - gold0
        check('5n kill: the next-chapter object (oact 8), gold random x 4 x 15, two sapphires, no boxes, forceload released, '
              '#mbMode 0', dead and ok and gmin * 4 * gmul <= got <= gmax * 4 * gmul and (s.sc('#SAP', 'azs') or 0) - sap0 == bsap
              and not objs(s, 15) and not (CH & set(s.fl)) and (M.mb(s, '#mbMode') or 0) == 0,
              (dead, ok, got, (s.sc('#SAP', 'azs') or 0) - sap0, len(CH & set(s.fl))))
        check('5o the death sequence ran the module death_start', (M.mb(s, '#knStubDeath') or 0) == 1 if stubbed else True)
        # cancel
        s, pl = fresh()
        z9, _ = K.ar_fight(s, 4)
        cp0 = copy.deepcopy(st(s)['cprep']['arlecchino'])
        b = M.body_of(s)
        b.alive = False
        s.ents = [e for e in s.ents if e.alive]
        ok = M.until(s, lambda s: M.gate_of(s) is not None, 200)
        check('5p cancel (the body gone): no reward, the gate returns at the zone with the same cprep, forceload released',
              ok and st(s)['cprep']['arlecchino'] == cp0 and not objs(s, 8) and not (CH & set(s.fl)))
        M.click(s, M.gate_of(s))
        ok = M.until(s, lambda s: (M.mb(s, '#mbSt') or 0) == 1, 600)
        check('5q pressing again fights again', ok and M.body_of(s) is not None)
        # lose
        s.call('rlk:mboss/test/lose', Ctx(pl, tuple(pl.pos), (0, 0)))
        check('5r test/lose -> cb/lose: #mbLost 1, the player at 0 HP', M.mb(s, '#mbLost') == 1 and s.sc(('e', pl.id), 'curHealth') == 0)
        # the test aliases
        s, pl = fresh()
        s.gen_hook = lambda s: M.boss_map(s, s.sc('#chapter', 'room'))
        s.setsc('#active', 'room', 0)                   # outside a run (test/chapter_ch refuses inside one)
        s.call('rlk:boss/test/chapter', Ctx(pl, tuple(pl.pos), (0, 0)), {'id': 'arlecchino'})
        tl = st(s).get('tlast', {})
        check('5s boss/test/chapter {id:"arlecchino"} -> test/chapter_ch in its first chapter (4): the test session and the boss map',
              tl.get('id') == 'arlecchino' and tl.get('ch') == 4 and M.mb(s, '#cbForce') == 12, tl)
        ok = M.until(s, lambda s: (M.mb(s, '#mbSt') or 0) == 1, 1500)
        s.setsc('#mbFloorHit', 'mb', 0)
        s.call('rlk:boss/test/pattern', Ctx(pl, tuple(pl.pos), (0, 0)), {'id': 11})
        check('5t ... the test session reaches the fight (the auto gate press); boss/test/pattern {id:11} reaches the module test '
              'hook' + (' (the stub: the floor-hit flag)' if stubbed else ''), ok and (M.mb(s, '#mbFloorHit') == 1 if stubbed else True),
              (ok, M.mb(s, '#mbFloorHit')))
        r = subprocess.run([sys.executable, 'tools/check_mboss_pack.py'], cwd=V, capture_output=True, text=True)
        check('5u check_mboss_pack.py on the variant (a px:false chapter boss enabled' + (', the stub module' if stubbed else '') + '): '
              '0 problems', r.returncode == 0, (r.stdout + r.stderr)[-400:])
    finally:
        M.drop_variant(V)

# ================================================================================================== 6 music
if want(6):
    print('== 6. music pool')
    tr = L.MUSIC_TRACKS.get('minecraft:music.nether.crimson_forest')
    check('6a MUSIC_TRACKS crimson forest = the five tracks of sounds.json (asset index 34): ballad_of_the_cats 5600, '
          'concrete_halls 5189, chrysopoeia 6068, dead_voxel 6076, warmth 4789', tr == [5600, 5189, 6068, 6076, 4789], tr)
    ar = next(x for x in REG['boss'] if x['id'] == 'arlecchino')
    check('6b music_len = 6076 (the longest track) = the registry music 1 len', L.music_len('minecraft:music.nether.crimson_forest') == 6076
          and ar['music']['1'] == {'ev': 'minecraft:music.nether.crimson_forest', 'len': 6076}, ar['music'])
    bad = copy.deepcopy(json.loads((DP / 'tools/mboss_registry.json').read_text(encoding='utf-8')))
    next(x for x in bad['boss'] if x['id'] == 'arlecchino')['music']['1']['len'] = 6000
    p = HERE / 'tmp' / 'reg_bad.json'
    p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps(bad, ensure_ascii=False), encoding='utf-8')
    old = L.REGISTRY
    try:
        L.REGISTRY = p
        L.load_registry()
        check('6c load_registry rejects a pool len that would cut a track (6000 < 6076)', False)
    except AssertionError as e:
        check('6c load_registry rejects a pool len that would cut a track (6000 < 6076)', 'crimson_forest' in str(e), str(e)[:120])
    finally:
        L.REGISTRY = old
        p.unlink()

M.summary('CM_AR')
