#!/usr/bin/env python3
"""test_scarlet.py: the 홍련 (Scarlet) module core, stage S3 (scratchpad hr/PLAN.md §3, §4.6-4.8, §5, §6.6, §9.3; contract
§3): hooks, the phase machine, the shield / judge / fail hits, the banner, the intro skip, the AI triggers, the bars, the
look requests, pause / reload in every phase, cleanup, the tick cost.

    python3 test_scarlet.py <datapack root> [section ...]

Run it from HR/tests; the tree is only read. Variants (her registry entry forced enabled, the core regenerated, a real
copy of F:boss/scarlet; for the kit / theme / switch sections a dry rebuild of F:boss/scarlet inside the variant with
api.K / the theme forced on and the switch patched) live in ./tmp and are removed at the end. On the merged tree (I1)
S2b's sequences, S4's gauntlets and S2a's rig are the real ones (the stand-ins core/sq/**, core/gs/**, rig_stub/** are gone).

  hooks    the 17 hooks + test/help + init + reward exist; spawn (seat, yaw to the moon, rlk_mb_inv, objective + constants,
           event scores 0); the empty hooks (aux_hit / incoming / hz_vis / pj_end) have no command; on_hit (skill flag,
           counter feed); test/help rows; uninstall (objective, storage, rlk_hr_*); the decor props (kit build)
  phases   the order of §4.6 with deflects (P1 -> CS1 -> SQ1 -> A8 -> CS2 -> down -> kipup -> P2 -> lead_stand -> A13 -> CS3
           -> death) and both fail branches (A8 fail -> P2 at T + 214 without a down window; A13 fail -> the instant death
           -> the revive stance -> A13 again); the floors 60 % / 5 % (never below by normal damage); the invulnerable windows
           tick by tick; the CS2 / CS3 HP steps (15 / 15 / 15 per mille, 15 / 15 / the kill) at flash 24 / land 75 / kick
           102; the down window's both exits (the timer -> kipup -> P2; the 5 % floor -> lead_down 40 t later); durations
  pips     a timed dash at a counting cut's strike (dashInvT 1..6 at s, 1..5 at s + 1) removes one pip whatever its
           direction; outside the strike ticks / beyond 6.2 b / a dash started after s: nothing; one per cut; never < 0
  judge    0 pips -> #gres 1 + the deflect staging (g_deflect, the sound); >= 1 -> #gres 2
  fail60   the A8 fail: 500 per mille of max HP (pl_dot, Electro), never kills at 1 HP, the push ring (3 b away), P2 at
           T + 214 with her HP unchanged
  fatal    ult/fatal kills through dash i-frames and shields, does nothing while rnDie; a revive -> the stance (60 t) ->
           lead_stand -> A13 from T0 with 5/5
  banner   (kit build) the warning banner (fx/hud/warn) never on during A8 with ULT60_LETHAL false nor during A13 with
           ULT5_LETHAL false (incl. the restarts after a pause and after a revive); on during A13 with the default switch
  skip     (kit build) sneak held 20 t from any start 20..521 -> the black, the jump (next tick = intro 554: line 11), the
           same end state as the full intro (her distance apart while I2_NEAR_OPEN: lead decision 1); released at 19 t ->
           no skip; outside 20-540 -> no skip
  ai       the counter trigger (4 hits / 40 t, 70 %, A1 beside / behind, A2 in front), the skill trigger (60 %, 4.5 b,
           phase grace, windup <= 6 t, cooldown), the far rule (8 b / 30 t: A4 / A10, fallback glide + A3), the rear rule
           (20 of 30 t: A1, its cooldown ignored once per 200 t), the band weights (seeded), cooldowns + no repeat in a
           long fight
  bars     FN-f: no bar draw during CS1 (bars_off), the bars back at SQ1 tick 0 with the shield under bar
  look     (theme build) a look request waits while an arena job runs and survives a pause / a reload inside the job;
           the final look is the last one requested
  pause    pause -> resume and /reload in every phase and sequence (PLAN §3.8)
  cs4      (I1, s3-8) the real seq/ending through the full core path: her distance to an unmoving player over ending
           ticks 300-1042 stays 3.5-6 b
  cleanup  won / cancel / defeat leave no rlk_hr_* entity, the core scores and storage core gone, the event scores kept
  cost     commands per fight tick (P1 + P2 + the gauntlets): average <= Apep's 830 (target <= 600)
"""
import math
import statistics
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
import hrsim as H  # noqa: E402
import azsim as AZ  # noqa: E402

ARGS = [a for a in sys.argv[1:] if a != '-v']
VERBOSE = '-v' in sys.argv[1:]
DP = Path(ARGS[0]).resolve()
SECTIONS = ARGS[1:] or ['hooks', 'phases', 'pips', 'judge', 'fail60', 'fatal', 'banner', 'skip', 'ai', 'bars', 'look', 'cs4',
                        'pause', 'cleanup', 'cost']
sys.path.insert(0, str(DP / 'tools'))
import mboss_scarlet.api as API  # noqa: E402
import mboss_scarlet.s3lib as S3  # noqa: E402
check = H.check if VERBOSE else H.ck
FN = DP / 'data/rlk/function/boss/scarlet'
PH = API.PH
TID = S3.TID
SEQ = S3.SEQ_ID
HP = 100000
FL60, FL5 = HP * API.FLOOR_P1 // 1000, HP * API.FLOOR_ULT // 1000
CUTS = {g: [c[2] for _t, _s, _cl, c in API.SCRIPTS[g] if c] for g in API.GAUNTLETS}
LOCKS = {g: [c[1] for _t, _s, _cl, c in API.SCRIPTS[g] if c] for g in API.GAUNTLETS}

# ------------------------------------------------------------------------------------------------- variants
VARS = {}


def var(name='base'):
    """base: her enabled (the tree's own F:boss/scarlet); kit: + a dry rebuild with the kit and the theme on; kit5: kit
    with ULT5_LETHAL false; kit60: kit with ULT60_LETHAL true. One variant tree, rebuilt when the wanted build changes."""
    if 'root' not in VARS:
        VARS['root'] = H.variant_hr(DP, H.enable_scarlet, label='scarlet')
        VARS['build'] = 'base'
    root = VARS['root']
    if VARS['build'] != name:
        patch = {'base': None, 'kit': '', 'kit5': 'api.ULT5_LETHAL = False', 'kit60': 'api.ULT60_LETHAL = True'}[name]
        if patch is None:
            import shutil
            d = root / 'data/rlk/function/boss/scarlet'
            shutil.rmtree(d)
            shutil.copytree(DP / 'data/rlk/function/boss/scarlet', d)
        else:
            H.dry_build(root, kit=True, theme=True, patch=patch)
        VARS['build'] = name
    return root


def world(seed=5, name='base', intro=False):
    s, pl = H.setup_sc(var(name), seed=seed)
    ok = H.fight_sc(s, intro=intro)
    assert ok, 'the fight did not start'
    if not intro:
        H.run_sc(s, 2)
    return s, pl


# ------------------------------------------------------------------------------------------------- helpers
def hr(s, k):
    return H.hr(s, k) or 0


def mb(s, k):
    return H.mb(s, k) or 0


def body(s):
    return H.body_of(s)


def hp(s):
    b = body(s)
    return s.sc(('e', b.id), 'mhpC') if b else None


def rec(s):
    b = body(s)
    pl = s.player()
    return dict(t=s.t, ph=hr(s, '#ph'), sqn=hr(s, '#sqn'), sq=hr(s, '#sq'), pat=hr(s, '#pat'), pt=hr(s, '#pt'),
                inv=bool(b and 'rlk_mb_inv' in b.tags), hp=hp(s), pips=hr(s, '#pips'), gres=hr(s, '#gres'),
                cine=mb(s, '#mbCine'), baroff=mb(s, '#mbBarOff'), st=mb(s, '#mbSt'), shb=hr(s, '#shb'),
                php=s.sc(('e', pl.id), 'curHealth') if pl else None, alive=b is not None,
                # I1: the ghost form (S4) and the shown clip tick of the real rig (S2a: hrRigT / hrRigC on the body)
                ghost=bool(b and 'rlk_hr_ghost' in b.tags), rigt=s.sc(('e', b.id), 'hrRigT') if b else None,
                rigc=s.sc(('e', b.id), 'hrRigC') if b else None)


def run(s, n, each=None, heal=True):
    out = []
    for _ in range(n):
        if heal:
            H.heal(s)
        if each:
            each(s)
        H.world_sc(s)
        out.append(rec(s))
    return out


def until(s, cond, limit=3000, each=None, heal=True):
    out = []
    for _ in range(limit):
        if cond(s):
            return True, out
        if heal:
            H.heal(s)
        if each:
            each(s)
        H.world_sc(s)
        out.append(rec(s))
    return cond(s), out


def strike(s, dmg=10 ** 7, skill=False):
    """One player hit on her body (the REAL combat path, azsim.strike); skill: a skill / burst hit (#skillDmg tmp 1 after
    combat/clear_atkflags, as the skill paths set it, no basic-attack flag)."""
    b = body(s)
    if not skill:
        return AZ.strike(s, b, dmg)
    orig = s.call

    def call(fid, ctx, macro=None):
        r = orig(fid, ctx, macro)
        if fid == 'rlk:combat/clear_atkflags':
            s.setsc('#skillDmg', 'tmp', 1)
        return r
    s.call = call
    try:
        return AZ.strike(s, b, dmg, basic=False)
    finally:
        del s.call
        s.setsc('#skillDmg', 'tmp', 0)


def dasher(cuts, off=0, v0=6, phases=(PH['a8'], PH['a13'])):
    """An agent dashing so that the world tick with #pt = s + off sees dashInvT v0, for every s in cuts."""
    cuts = set(cuts)

    def each(s):
        if hr(s, '#ph') in phases and hr(s, '#pt') + 1 - off in cuts:
            s.dash(v0)
    return each


def test(s, n):
    return H.test_id(s, n)


def phase_list(recs):
    out = []
    for r in recs:
        if not out or out[-1] != r['ph']:
            out.append(r['ph'])
    return out


def spans(recs, key='ph'):
    """[(value, first t, last t)] of consecutive runs of recs[key]."""
    out = []
    for r in recs:
        if out and out[-1][0] == r[key]:
            out[-1][2] = r['t']
        else:
            out.append([r[key], r['t'], r['t']])
    return [tuple(x) for x in out]


def pause_for(s, n, how='pkMode'):
    """The framework pause for n ticks (a selection screen: pkMode 1), then back (the resume edge on the next tick)."""
    pl = s.player()
    s.setsc(('e', pl.id), how, 1)
    out = run(s, n)
    s.setsc(('e', pl.id), how, 0)
    return out


def reload(s):
    """/reload: rlk:mboss/init (aux entities die, the module reload hook runs as the body)."""
    s.call('rlk:mboss/init', H.C0)


def fn_lines(rel, root=None):
    p = (root or DP) / 'data/rlk/function/boss/scarlet' / (rel + '.mcfunction')
    return p.read_text(encoding='utf-8').split('\n') if p.exists() else None


def cmds(rel, root=None):
    return [ln for ln in (fn_lines(rel, root) or []) if ln.strip() and not ln.lstrip().startswith('#')]


# ================================================================================================= hooks
def sec_hooks():
    names = API.L.HOOKS + API.L.HELP_HOOKS + ['init', API.REWARD_HOOK]
    miss = [n for n in names if fn_lines(n) is None]
    check('K1 the 17 hooks + test/help + init + reward exist', not miss, miss)
    for h in ('aux_hit', 'incoming', 'hz_vis', 'pj_end'):
        check(f'K2 {h}: no command (her framework default)', cmds(h) == [], cmds(h))
    s, pl = H.setup_sc(var(), seed=3)
    z, a = H.rift_zone(s, 'scarlet')
    s.player().pos = list(a.pos)
    H.enter(s, a)
    ok, _ = until(s, lambda s: body(s) is not None, 300)
    b = body(s)
    yaw = math.degrees(math.atan2(-(API.MOON_POS[0] - API.SEAT_POS[0]), API.MOON_POS[2] - API.SEAT_POS[2])) % 360
    check('K3 spawn: the body on her seat facing the moon, rlk_mb_inv in the intro, objective hr + constants, #ph intro',
          ok and abs(b.pos[0] - API.SEAT_POS[0]) < 1e-6 and abs(b.pos[2] - API.SEAT_POS[2]) < 1e-6
          and abs((b.rot[0] % 360) - yaw) < 0.05 and 'rlk_mb_inv' in b.tags and hr(s, '#c1000') == 1000
          and hr(s, '#cn1') == -1 and hr(s, '#ph') == PH['intro'],
          (b and b.pos, b and b.rot, yaw, b and sorted(b.tags)))
    check('K4 spawn: the event scores 0 (api.EV_FP)', all(s.sc(k, 'hr') == 0 for k in API.EV_FP),
          [s.sc(k, 'hr') for k in API.EV_FP])
    run(s, 5)
    check('K5 the intro state: #mbSt 0, #sqn intro, #inv 1, the floors from mhpM (60 % / 5 %)',
          mb(s, '#mbSt') == 0 and hr(s, '#sqn') == SEQ['intro'] and hr(s, '#inv') == 1 and hr(s, '#fl60') == FL60
          and hr(s, '#fl5') == FL5, (mb(s, '#mbSt'), hr(s, '#sqn'), hr(s, '#fl60'), hr(s, '#fl5')))
    # on_hit
    s, pl = world(4)
    H.hold(s)
    s.setsc('#a6q', 'hr', 0)
    h0 = hr(s, '#hits')
    strike(s, 10, skill=True)
    check('K6 on_hit: a skill hit flags the A6 trigger (#a6q 1); a hit while she idles feeds the counter (#hits + 1)',
          hr(s, '#a6q') == 1 and hr(s, '#hits') == h0 + 1, (hr(s, '#a6q'), h0, hr(s, '#hits')))
    test(s, TID['a3'])
    h1 = hr(s, '#hits')
    strike(s, 10)
    check('K7 on_hit: no counter feed while a pattern runs', hr(s, '#hits') == h1, (h1, hr(s, '#hits')))
    # test/help rows
    rows = '\n'.join(fn_lines('test/help'))
    present = [k for k in API.P1]
    want = [i for i in API.TEST_IDS if API.TEST_IDS[i] not in API.P1 + API.P2 or API.TEST_IDS[i] in present]
    missing = [i for i in want if f'{{id:{i}}}' not in rows]
    absent_listed = [i for i in API.TEST_IDS if API.TEST_IDS[i] in API.P2 and API.TEST_IDS[i] not in API.GAUNTLETS
                     and f'{{id:{i}}} ' in rows]
    check('K8 test/help: a row per available test id (P1 keys, 20-35, 80, 90-92, 99), none for S4\'s absent keys',
          not missing and not absent_listed, (missing, absent_listed))
    # uninstall
    s.call('rlk:boss/scarlet/uninstall', H.C0)
    left = H.ents_tagged(s)
    check('K9 uninstall: objective hr removed (no hr score left, the event scores too), storage rlk:hr keys gone, no rlk_hr_* entity',
          not any(k[1] == 'hr' for k in s.scores) and not left and not s.storage.get('rlk:hr'),
          ([k for k in s.scores if k[1] == 'hr'][:4], left[:3], s.storage.get('rlk:hr')))
    # the decor props (kit build): the halo, 8 lotus buds, the seat rock; the rock goes with the intro
    s, pl = H.setup_sc(var('kit'), seed=3)
    H.fight_sc(s, intro=True)
    deco = [tg for _, tg in H.ents_tagged(s, 'rlk_hr_deco')]
    names_d = sorted(t for tg in deco for t in tg if t.startswith('rlk_hr_deco_'))
    check('K10 the decor props at spawn (kit build): moon halo, 8 lotus, the seat rock (rlk_hr_deco + rlk_hr_deco_<name>)',
          names_d.count('rlk_hr_deco_lotus') == 8 and names_d.count('rlk_hr_deco_moon_halo') == 1
          and names_d.count('rlk_hr_deco_seat_rock') == 1, names_d)
    H.call_sc(s, 'core/intro/done')
    check('K11 the seat rock goes with the intro; the halo and the lotus stay',
          not [1 for _, tg in H.ents_tagged(s, 'rlk_hr_deco_seat') if tg] and len(H.ents_tagged(s, 'rlk_hr_deco')) == 9,
          H.ents_tagged(s, 'rlk_hr_deco'))
    reload(s)
    check('K12 /reload: the props come back (core/deco_re: halo + lotus, no rock)', len(H.ents_tagged(s, 'rlk_hr_deco')) == 9,
          len(H.ents_tagged(s, 'rlk_hr_deco')))


# ================================================================================================= phases
def to_floor(s):
    """A huge hit: the framework floor keeps her at #mbFloor exactly (#mbFloorHit)."""
    return strike(s)


def chain(seed=11, a8='deflect', a13='deflect', revive=0, limit=6000):
    """One whole fight from P1: the 60 % floor hit, the A8 chain, P2, the 5 % floor hit, the A13 chain; dashes timed at
    the first 5 counting cuts of a gauntlet when its branch is 'deflect'. Returns (sim, recs)."""
    s, pl = world(seed)
    s.revive = revive
    recs = [rec(s)]
    H.place_player(s, API.CX + 0.5, API.CZ + 6.0)
    to_floor(s)
    d8, d13 = dasher(CUTS['a8'][:5]), dasher(CUTS['a13'][:5])

    def each(s):
        ph = hr(s, '#ph')
        if ph == PH['a8'] and a8 == 'deflect':
            d8(s)
        if ph == PH['a13'] and a13 == 'deflect':
            d13(s)
        if ph == PH['p2'] and hr(s, '#fl') == 0 and hp(s) is not None and hp(s) > FL5 and s.t % 7 == 0 \
                and each.p2_t is not None and s.t - each.p2_t >= 60:
            to_floor(s)
        if ph == PH['p2'] and each.p2_t is None:
            each.p2_t = s.t
        pl = s.player()
        pl.pos = [API.CX + 0.5, 201.0, API.CZ + 6.0]
    each.p2_t = None
    ok, r = until(s, lambda s: mb(s, '#mbSt') == 2 or (a13 == 'fail' and len(s.deaths) >= 2), limit, each=each)
    recs += r
    return s, recs, ok


def sec_phases():
    s, R, ok = chain(11)
    order = phase_list(R)
    want = [PH[k] for k in ('p1', 'cs1', 'sq1', 'a8', 'cs2', 'down', 'p2', 'lead', 'a13', 'cs3', 'death')]
    check('P1 the order with both deflects: P1 CS1 SQ1 A8 CS2 down P2 lead A13 CS3 death', ok and order == want, order)
    sp = {v: (a, b) for v, a, b in spans(R)}
    dur = {k: sp[PH[k]][1] - sp[PH[k]][0] + 1 for k in ('cs1', 'sq1', 'a8', 'cs2', 'lead', 'a13') if PH[k] in sp}
    check('P2 durations: CS1 213 (+1 the decision tick), SQ1 60, A8 to REPEL_T 206, CS2 104, the lead-in 70, A13 to 270',
          dur.get('cs1') in (213, 214) and dur.get('sq1') in (60, 61) and dur.get('a8') == API.REPEL_T['a8']
          and dur.get('cs2') in (104, 105) and dur.get('lead') in (70, 71) and dur.get('a13') == API.REPEL_T['a13'], dur)
    down = [r for r in R if r['ph'] == PH['down']]
    check('P3 the down window by its timer: 200 t down + the 20-t kipup, then P2', len(down) in (220, 221), len(down))
    # floors / HP
    p1 = [r for r in R if r['ph'] == PH['cs1']]
    check('P4 the 60 % floor: the huge P1 hit leaves exactly 60 % (normal damage never below the floor)',
          p1 and p1[0]['hp'] == FL60, p1 and p1[0]['hp'])
    cs2 = [r for r in R if r['ph'] == PH['cs2']]
    steps = [(r['t'] - cs2[0]['t'], r['hp']) for i, r in enumerate(cs2) if i and r['hp'] != cs2[i - 1]['hp']]
    pm = HP * 15 // 1000
    check('P5 CS2 HP steps: -15 per mille of max HP at repel ticks 24 / 75 / 102 (true damage)',
          [h for _, h in steps] == [FL60 - pm, FL60 - 2 * pm, FL60 - 3 * pm]
          and [t for t, _ in steps] == [API.ev('repel', e) for e in API.COUNTER_EV], steps)
    lead = [r for r in R if r['ph'] == PH['lead']]
    check('P6 the 5 % floor: the P2 hit leaves exactly 5 % before the lead-in', lead and lead[0]['hp'] == FL5,
          lead and lead[0]['hp'])
    cs3 = [r for r in R if r['ph'] == PH['cs3']]
    steps3 = [(r['t'] - cs3[0]['t'], r['hp']) for i, r in enumerate(cs3) if i and r['hp'] != cs3[i - 1]['hp']]
    check('P7 CS3: -15 / -15 per mille, then the kill at the kick (death state)',
          [h for _, h in steps3] == [FL5 - pm, FL5 - 2 * pm] and R[-1]['st'] == 2, (steps3, R[-1]))
    # invulnerability per phase
    inv_on = {PH[k] for k in ('cs1', 'sq1', 'a8', 'cs2', 'lead', 'a13', 'cs3')}
    # I1 (request s4-1): the ghost windows of R1 / R3 (the body tagged rlk_hr_ghost, PLAN §4.1 / §4.6) are invulnerable too
    bad = [(r['t'], r['ph'], r['inv']) for r in R if r['st'] == 1 and r['pat'] != TID['a6'] and not r['ghost']
           and ((r['ph'] in inv_on) != r['inv']) and not (r['ph'] == PH['down'])]
    dn = [r for r in R if r['ph'] == PH['down']]
    kip_ok = all(r['inv'] == (i >= 200) for i, r in enumerate(dn))
    check('P8 rlk_mb_inv tick by tick: on from CS1 to the end of CS2, in the kipup, the lead-in to CS3; off in P1, P2 and the down '
          '(the A6 blink and the ghost windows apart)', not bad and kip_ok, (bad[:5], [r['inv'] for r in dn][195:205]))
    gh = [r for r in R if r['st'] == 1 and r['ghost'] and r['ph'] == PH['p2']]
    check(f'P8b the ghost form in P2 (R1 / R3, {len(gh)} ticks in this chain) is invulnerable on every tick',
          all(r['inv'] for r in gh), [(r['t'], r['pat'], r['pt']) for r in gh if not r['inv']][:5])
    # A8 fail branch
    s, R, ok = chain(12, a8='fail')
    order = phase_list(R)
    check('P9 the A8 fail: A8 -> P2 (no CS2, no down window)', ok and order[:5] == [PH['p1'], PH['cs1'], PH['sq1'], PH['a8'], PH['p2']],
          order)
    sp = spans(R)
    a8 = [x for x in sp if x[0] == PH['a8']][0]
    check(f'P10 the A8 fail: P2 at T + {API.FAIL60_P2_T} (her HP unchanged by the fail)', a8[2] - a8[1] + 1 == API.FAIL60_P2_T
          and [r for r in R if r['ph'] == PH['p2']][0]['hp'] == FL60, (a8, [r for r in R if r['ph'] == PH['p2']][0]['hp']))
    # A13 fail -> instant death -> revive -> A13 again
    s, R, ok = chain(13, a13='fail', revive=40)
    order = phase_list(R)
    i = order.index(PH['a13'])
    check('P11 the A13 fail (a revive): the instant death, then the stance, lead_stand and A13 again',
          ok and len(s.deaths) >= 2 and order[i:i + 3] == [PH['a13'], PH['lead'], PH['a13']] and mb(s, '#mbSt') == 1,
          (order, s.deaths))
    # the down window's 5 % exit
    s, pl = world(14)
    test(s, 25)
    run(s, 30)
    to_floor(s)
    t0 = s.t
    ok, R = until(s, lambda s: hr(s, '#ph') == PH['lead'], 400)
    check(f'P12 the down window: a hit reaching 5 % -> lead_down {API.DOWN_FLOOR_WAIT} t later (HP = 5 %)',
          ok and abs((s.t - t0) - API.DOWN_FLOOR_WAIT) <= 2 and hr(s, '#sqn') == SEQ['lead_down'] and hp(s) == FL5,
          (ok, s.t - t0, hr(s, '#sqn'), hp(s)))
    ok, R = until(s, lambda s: hr(s, '#ph') == PH['a13'], 200)
    check('P13 lead_down (82 t) -> A13 with the shield 5/5', ok and hr(s, '#pips') == API.PIPS and len(R) in (82, 83), (ok, len(R)))


# ================================================================================================= pips
def a8_run(seed, each=None, n=API.JUDGE_T['a8'] - 1, pips=None, tid=21):
    s, pl = world(seed)
    H.place_player(s, API.CX + 0.5, API.CZ + 6.0)
    test(s, tid)
    if pips is not None:
        s.setsc('#pips', 'hr', pips)
    R = run(s, n, each=each)
    return s, R


def sec_pips():
    # stand + a timed dash at the strike of the first cut (dashInvT 6 at s)
    for off, v0, want, what in ((0, 6, 1, 'dashInvT 6 at s'), (0, 1, 1, 'dashInvT 1 at s'), (1, 5, 1, 'dashInvT 5 at s + 1'),
                                (1, 6, 0, 'dashInvT 6 at s + 1 (a dash after s)'), (-1, 1, 0, 'dashInvT 0 at s (ended at s - 1)'),
                                (2, 4, 0, 'dashInvT 4 at s + 2 (window closed)'), (-8, 6, 0, 'a dash 8 t early')):
        s, R = a8_run(21, each=dasher(CUTS['a8'][:1], off=off, v0=v0), n=CUTS['a8'][0] + 4)
        lost = API.PIPS - hr(s, '#pips')
        check(f'S1 A8 cut 1 (strike {CUTS["a8"][0]}): {what} -> {want} pip', lost == want, lost)
    # whatever the direction: the player moves 0.6 b / t (forward, back, sideways) during the dash, within 6.2 b
    for name, (dx, dz) in (('forward', (0, -0.6)), ('back', (0, 0.6)), ('left', (0.6, 0)), ('right', (-0.6, 0))):
        def each(s, dx=dx, dz=dz, d=dasher(CUTS['a8'][:1])):
            d(s)
            if s.dash_t0 is not None and 0 <= s.t + 1 - s.dash_t0 < 6:
                pl = s.player()
                pl.pos = [pl.pos[0] + dx, pl.pos[1], pl.pos[2] + dz]
                H.C.moved(s)
        s, R = a8_run(22, each=each, n=CUTS['a8'][0] + 3)
        check(f'S2 a timed dash moving {name} counts (any direction)', API.PIPS - hr(s, '#pips') == 1, hr(s, '#pips'))
    # beyond PIP_R from the lock point: the player walks 7 b away before the strike
    def away(s, d=dasher(CUTS['a8'][:1])):
        d(s)
        if hr(s, '#ph') == PH['a8'] and hr(s, '#pt') == LOCKS['a8'][0] + 1:
            H.place_player(s, API.CX + 0.5, API.CZ + 6.0 + 7.0)
    s, R = a8_run(23, each=away, n=CUTS['a8'][0] + 3)
    check(f'S3 a timed dash {API.PIP_R + 0.8:.1f} b from the lock point: no pip', hr(s, '#pips') == API.PIPS, hr(s, '#pips'))
    # one per cut: a dash whose window covers s and s + 1 removes one pip; five cuts -> 0
    s, R = a8_run(24, each=dasher(CUTS['a8'][:1], off=0, v0=6), n=CUTS['a8'][0] + 3)
    check('S4 one pip per cut (dashInvT 6 at s and 5 at s + 1: one pip)', API.PIPS - hr(s, '#pips') == 1, hr(s, '#pips'))
    s, R = a8_run(25, each=dasher(CUTS['a8']))
    pips = [r['pips'] for r in R]
    check('S5 a timed dash at every cut: 5 -> 0 at the 5th, never below 0 for the 4 extra cuts',
          min(pips) == 0 and hr(s, '#pips') == 0 and all(p >= 0 for p in pips)
          and [R[i]['pips'] for i in range(len(R)) if R[i]['pt'] in CUTS['a8'][:5]] == [4, 3, 2, 1, 0], pips[::10])
    s, R = a8_run(26, each=dasher(CUTS['a8']), pips=0, tid=22)
    check('S6 test 22 (0 pips): timed dashes keep 0', all(r['pips'] == 0 for r in R), set(r['pips'] for r in R))
    # disc dodges / other dashes ignored: dashes at every non-strike tick of A8 -> no pip
    other = [t for t in range(1, API.JUDGE_T['a8']) if all(abs(t - c) > 7 for c in CUTS['a8'])]
    s, R = a8_run(27, each=dasher(other[::7]))
    check('S7 dashes away from every strike (dodging anything else) never take a pip', hr(s, '#pips') == API.PIPS, hr(s, '#pips'))
    # A13 too (its own cut ticks)
    s, pl = world(28)
    H.place_player(s, API.CX + 0.5, API.CZ + 6.0)
    test(s, 27)
    R = run(s, API.JUDGE_T['a13'] - 1, each=dasher(CUTS['a13'][:5]))
    check('S8 A13: timed dashes at its first 5 cuts -> 0 pips before the judge', hr(s, '#pips') == 0,
          [r['pips'] for r in R if r['pt'] in CUTS['a13']])


# ================================================================================================= judge
def sec_judge():
    s, R = a8_run(31, each=dasher(CUTS['a8'][:5]), n=API.JUDGE_T['a8'] + 2)
    g = [r for r in R if r['pt'] >= API.JUDGE_T['a8']]
    played = [c for t, c in s.rigl if c == 'play/g_deflect']
    check('J1 0 pips at the judge -> #gres 1 (deflect), the under bar gone, g_deflect played',
          g and g[0]['gres'] == 1 and g[0]['shb'] == 0 and played, (g[:1], played))
    s, R = a8_run(32, each=dasher(CUTS['a8'][:4]), n=API.JUDGE_T['a8'] + 2)
    g = [r for r in R if r['pt'] >= API.JUDGE_T['a8']]
    check('J2 1 pip left at the judge -> #gres 2 (fail)', g and g[0]['gres'] == 2 and g[0]['pips'] == 1, g[:1])
    ok, R2 = until(s, lambda s: hr(s, '#ph') == PH['p2'], 100)
    check('J3 after the A8 deflect... (fail here) -> P2; after a deflect -> CS2 (P1 of the phases section)', ok)


# ================================================================================================= fail60
def sec_fail60():
    s, R = a8_run(41, n=API.JUDGE_T['a8'] - 1)
    pl = s.player()
    mx = s.sc(('e', pl.id), 'maxHealth')
    s.setsc(('e', pl.id), 'curHealth', mx)
    p0 = tuple(pl.pos)
    R = run(s, 1, heal=False)
    lost = mx - s.sc(('e', pl.id), 'curHealth')
    check('F1 the A8 fail: 500 per mille of max HP (pl_dot, through the element shield rules)', lost == mx * API.FAIL60_PM // 1000,
          (lost, mx))
    R = run(s, 6, heal=False)
    d = math.hypot(pl.pos[0] - p0[0], pl.pos[2] - p0[2])
    check(f'F2 the push ring at the impact (the player): moved ~{API.FAIL60_PUSH[1]} b away', 2.0 <= d <= 3.6, (p0, pl.pos, d))
    s, R = a8_run(42, n=API.JUDGE_T['a8'] - 1)
    pl = s.player()
    s.setsc(('e', pl.id), 'curHealth', 1)
    R = run(s, 3, heal=False)
    check('F3 never kills: at 1 HP the fail leaves 1 HP, no death', s.sc(('e', pl.id), 'curHealth') == 1 and not s.deaths,
          (s.sc(('e', pl.id), 'curHealth'), s.deaths))
    hp0 = hp(s)
    ok, R = until(s, lambda s: hr(s, '#ph') == PH['p2'], 60)
    check(f'F4 P2 at T + {API.FAIL60_P2_T}, her HP unchanged', ok and hp(s) == hp0, (ok, hp0, hp(s)))


# ================================================================================================= fatal
def sec_fatal():
    for what, prep in (('dash i-frames (dashInvT 6)', lambda s, pl: s.setsc(('e', pl.id), 'dashInvT', 6)),
                       ('a guard + an element shield', lambda s, pl: (s.setsc(('e', pl.id), 'shieldHP', 10 ** 6),
                                                                      s.setsc(('e', pl.id), 'gShield', 10 ** 6))),
                       ('nothing', lambda s, pl: None)):
        s, pl = world(51)
        prep(s, pl)
        s.call('rlk:boss/scarlet/ult/fatal', H.Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
        check(f'X1 ult/fatal kills through {what}', s.deaths and s.sc(('e', pl.id), 'curHealth') in (0, 1), (s.deaths,))
    s, pl = world(52)
    s.setsc(('e', pl.id), 'rnDie', 5)
    hp0 = s.sc(('e', pl.id), 'curHealth')
    s.call('rlk:boss/scarlet/ult/fatal', H.Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
    check('X2 ult/fatal does nothing while the player revives (rnDie >= 1)', not s.deaths and s.sc(('e', pl.id), 'curHealth') == hp0,
          (s.deaths, hp0))
    # A13 fail with Ronova's revive: the stance, lead_stand, A13 from T0 with 5/5
    s, pl = world(53)
    s.revive = 40
    H.place_player(s, API.CX + 0.5, API.CZ + 6.0)
    test(s, 27)
    ok, R = until(s, lambda s: len(s.deaths) >= 1, 400)
    t_d = s.t
    ok1, R1 = until(s, lambda s: hr(s, '#ph') == PH['lead'] and hr(s, '#rvw') >= 1, 200)
    b, pl = body(s), s.player()
    d = math.hypot(b.pos[0] - pl.pos[0], b.pos[2] - pl.pos[2]) if b else None
    check(f'X3 a revive: the fight pauses while rnDie, then the stance {API.REVIVE["dist"]} b from the player (#rvw {API.REVIVE["wait"]})',
          ok and ok1 and d is not None and abs(d - API.REVIVE['dist']) <= 0.6 and hr(s, '#pat') == 0, (ok, ok1, d, s.t - t_d))
    ok2, R2 = until(s, lambda s: hr(s, '#ph') == PH['a13'] and hr(s, '#pat') == TID['a13'] and hr(s, '#pt') >= 1, 400)
    lead = [r for r in R1 + R2 if r['ph'] == PH['lead']]
    check('X4 ... -> lead_stand {g:"a13"} (70 t) after the 60-t stance -> A13 from T0 with 5/5',
          ok2 and hr(s, '#pips') == API.PIPS and hr(s, '#pt') == 1
          and len(lead) in range(API.REVIVE['wait'] + API.SEQ_LEN['lead_stand'] - 1, API.REVIVE['wait'] + API.SEQ_LEN['lead_stand'] + 3),
          (ok2, len(lead), hr(s, '#pips'), hr(s, '#pt')))


# ================================================================================================= banner (kit builds)
def banner_states(s):
    """[(t, on)] from the kit calls fx/hud/warn {on}."""
    return [(t, int(a.get('on', 0))) for t, c, a in s.kitl if c == 'hud/warn']


def banner_on_at(s, t):
    st = 0
    for tt, on in banner_states(s):
        if tt <= t:
            st = on
    return st


def gauntlet_ticks(R, g):
    return [r['t'] for r in R if r['ph'] == PH[g]]


def sec_banner():
    for name, g, want_on in (('kit', 'a8', False), ('kit', 'a13', True), ('kit5', 'a13', False), ('kit60', 'a8', True)):
        lethal = {'kit': (API.ULT60_LETHAL, API.ULT5_LETHAL), 'kit5': (API.ULT60_LETHAL, False), 'kit60': (True, API.ULT5_LETHAL)}[name]
        # the chain through the lead-in (A13) / SQ1 (A8), a pause inside the gauntlet (restart via lead_stand), a revive
        s, pl = world(61, name=name)
        H.place_player(s, API.CX + 0.5, API.CZ + 6.0)
        s.revive = 30
        if g == 'a8':
            test(s, 20)                      # CS1 -> SQ1 -> A8
        else:
            test(s, 26)                      # lead_stand {g:"a13"} -> A13
        ok, R = until(s, lambda s: hr(s, '#ph') == PH[g] and hr(s, '#pt') >= 60, 800)
        R += pause_for(s, 20)
        ok2, R2 = until(s, lambda s: hr(s, '#ph') == PH[g] and hr(s, '#pt') >= 60, 400)
        R += R2
        if g == 'a13' and lethal[1]:
            ok3, R3 = until(s, lambda s: len(s.deaths) >= 1, 400)
            R += R3
        elif g == 'a13':
            # I1 (request s4-1): ULT5_LETHAL false = the 500 per-mille hit (no death), then the revive stance -> lead_stand
            ok3, R3 = until(s, lambda s: (hr(s, '#rvw') or 0) >= 1 or hr(s, '#ph') == PH['lead'], 400)
            R += R3
            ok4, R4 = until(s, lambda s: hr(s, '#ph') == PH['a13'] and hr(s, '#pt') >= 30, 400)
            R += R4
        else:
            ok3 = ok4 = True
        ticks = gauntlet_ticks(R, g)
        ons = [t for t in ticks if banner_on_at(s, t)]
        if want_on:
            # the banner from the lead-in's brim beat until the judge, on every run of the gauntlet (incl. the restarts)
            check(f'B1 {name}: the banner on during {g.upper()} (ULT{60 if g == "a8" else 5}_LETHAL {lethal[0 if g == "a8" else 1]})'
                  f' incl. after a pause and a revive', ok and ok2 and ok3 and ok4 and ticks and len(ons) >= len(ticks) * 0.6, (len(ons), len(ticks)))
        else:
            check(f'B1 {name}: the banner never on during {g.upper()} (ULT{60 if g == "a8" else 5}_LETHAL false), incl. the restart'
                  f'{"s after a pause and a revive" if g == "a13" else " after a pause"}',
                  ok and ok2 and ok3 and ok4 and not ons and ticks, (ons[:5], len(ticks), banner_states(s)[:6]))
        offs = [t for t, on in banner_states(s) if on == 0]
        check(f'B2 {name} {g}: every banner on is matched by an off (judge / pause / revive / death)',
              not banner_states(s) or banner_states(s)[-1][1] == 0 or hr(s, '#ph') == PH[g], banner_states(s)[-4:])


# ================================================================================================= skip (kit build)
def intro_world(seed, name='kit'):
    s, pl = H.setup_sc(var(name), seed=seed)
    ok = H.fight_sc(s, intro=True)
    assert ok
    return s, pl


# The intro's end distance (lead decision 1, I1b): the walk keeps its 0.15 b/t legs and the seat rock sits 5 b nearer the
# start (api.SEAT_POS 884 201 5, 26.7 b from `start`; the legs walk while she is more than 7 b away), so a player who stays at
# `start` meets her <= 7 b away when the walk stops, as the skip stands her (PLAN §3.1, E10's pose). I2 compares every key of
# the end state again, `near` included (I1a had left it out while the decision was open: i1_notes §10, §11 m3).
I2_NEAR_OPEN = False


def her_dist(s):
    b = body(s)
    pl = s.player()
    return math.hypot(b.pos[0] - pl.pos[0], b.pos[2] - pl.pos[2])


def end_state(s):
    b = body(s)
    return dict(st=mb(s, '#mbSt'), ph=hr(s, '#ph'), inv=hr(s, '#inv'), inv_tag='rlk_mb_inv' in b.tags, floor=mb(s, '#mbFloor'),
                mus=mb(s, '#mbMusPh'), skip=hr(s, '#skip'), sqn=hr(s, '#sqn'), rock=bool(H.ents_tagged(s, 'rlk_hr_deco_seat')),
                near=her_dist(s) <= 7.05,
                title=any('홍련' in str(x) for _, x in s.titles))


def run_intro(s, hold_from=None, hold_n=0, limit=800):
    """The intro with the player standing at the start; sneak held from intro tick hold_from for hold_n ticks."""
    R = []
    jump = None
    for _ in range(limit):
        sq = hr(s, '#sq')
        pl = s.player()
        pl.data['sneak'] = hold_from is not None and hold_from <= sq + 1 < hold_from + hold_n and mb(s, '#mbSt') == 0
        before = sq
        H.heal(s)
        H.world_sc(s)
        if mb(s, '#mbSt') == 0 and hr(s, '#sq') - before > 1 and jump is None:
            jump = (before, hr(s, '#sq'), s.t)
        R.append(rec(s))
        if mb(s, '#mbSt') == 1:
            break
    pl.data['sneak'] = False
    return R, jump


def sec_skip():
    s, pl = intro_world(70)
    R, jump = run_intro(s)
    full = end_state(s)
    d_full, d_skip = her_dist(s), []
    line11 = [t for t, c, a in s.kitl if c == 'hud/line' and a.get('id') == 11]
    check('I1 the full intro: 640 t, line 11 at intro 554, the fight state (P1, 60 % floor, music 1, the title, no rock)',
          jump is None and full['st'] == 1 and full['ph'] == PH['p1'] and full['floor'] == FL60 and full['mus'] == 1
          and not full['rock'] and full['title'] and len(line11) == 1, (full, line11, len(R)))
    for start in (20, 21, 100, 333, 521):
        s, pl = intro_world(71)
        R, jump = run_intro(s, hold_from=start, hold_n=API.SKIP_HOLD)
        st = end_state(s)
        d_skip.append(her_dist(s))
        black = [(t, a) for t, c, a in s.kitl if c == 'hud/ovl' and a.get('g') == 'black']
        l11 = [t for t, c, a in s.kitl if c == 'hud/line' and a.get('id') == 11]
        # I1: while I2_NEAR_OPEN (lead decision 1, above) her distance is left out of the shared end state and the skip's
        # <= 7 b (PLAN §3.1, E10's pose) is checked apart (near)
        same = {k: v for k, v in st.items() if not (I2_NEAR_OPEN and k == 'near') and full[k] != v}
        check(f'I2 sneak held {API.SKIP_HOLD} t from intro tick {start}: the black, the jump (next tick 554), line 11 right after,'
              f' the same end state as the full intro{" (her distance apart: OPEN, lead decision 1)" if I2_NEAR_OPEN else ""},'
              f' her <= 7 b from the player (PLAN §3.1)',
              jump is not None and jump[0] + 1 == start + API.SKIP_HOLD - 1 and jump[1] == API.SKIP_T - 1 and black and black[0][0] == jump[2]
              and l11 and l11[0] == jump[2] + 1 and not same and st['near'], (jump, black[:1], l11, same, st['near']))
    print(f'  I2 her distance at the intro\'s end (lead decision 1): the full intro {d_full:.2f} b from the player who stays at'
          f' the start, the skip {min(d_skip):.2f}-{max(d_skip):.2f} b')
    for start, n, what in ((100, API.SKIP_HOLD - 1, f'released after {API.SKIP_HOLD - 1} t'), (5, 14, 'held before 20 only'),
                           (522, API.SKIP_HOLD, 'completing after tick 540'), (560, 40, 'after the window')):
        s, pl = intro_world(72)
        R, jump = run_intro(s, hold_from=start, hold_n=n)
        black = [t for t, c, a in s.kitl if c == 'hud/ovl' and a.get('g') == 'black']
        check(f'I3 {what}: no skip (the intro runs its 640 t)', jump is None and not black and mb(s, '#mbSt') == 1, (jump, black))
    # the prompt: shown from 20 to 540 (kit hud/skip {s}), cleared after
    s, pl = intro_world(73)
    R, jump = run_intro(s)
    sk = [(t, a.get('s')) for t, c, a in s.kitl if c == 'hud/skip']
    check('I4 the skip prompt (kit hud/skip) from intro tick 20 to 540, then cleared (s 5)', sk and sk[-1][1] == 5, sk[-3:])


# ================================================================================================= ai
def ai_trial(seed, setup, ticks=3):
    s, pl = world(seed)
    setup(s)
    started = None
    for _ in range(ticks):
        H.heal(s)
        H.world_sc(s)
        if hr(s, '#pat') and started is None:
            started = S3.KEY_OF.get(hr(s, '#pat'))
    return s, started


def sec_ai():
    import random
    # the counter trigger: 4 hits in 40 t while she idles
    def counter_setup(front):
        def f(s):
            H.hold(s, False)
            H.place_body(s, API.CX, API.CZ, yaw=0.0 if front else 180.0)    # yaw 0 faces +z
            H.place_player(s, API.CX, API.CZ + 2.5)
            s.setsc('#rec', 'hr', 40)
            s.setsc('#pat', 'hr', 0)
            for _ in range(API.COUNTER_TRIGGER['hits']):
                strike(s, 5)
        return f
    res = {True: [], False: []}
    for i in range(160):
        front = i % 2 == 0
        s, k = ai_trial(1000 + i, counter_setup(front), ticks=2)
        res[front].append(k)
    rate = sum(1 for v in res[True] + res[False] if v in ('a1', 'a2')) / 160
    check(f'A1 the counter trigger: 4 hits / 40 t while she idles -> {API.COUNTER_TRIGGER["chance"]} % a counter (seeded)',
          0.55 <= rate <= 0.85, rate)
    check('A2 in front -> A2, beside / behind -> A1', all(v in (None, 'a2') for v in res[True]) and all(v in (None, 'a1') for v in res[False])
          and 'a2' in res[True] and 'a1' in res[False], (set(res[True]), set(res[False])))
    # 3 hits only -> never
    def three(s):
        H.hold(s, False)
        H.place_body(s, API.CX, API.CZ, yaw=0.0)
        H.place_player(s, API.CX, API.CZ + 2.5)
        s.setsc('#rec', 'hr', 40)
        for _ in range(API.COUNTER_TRIGGER['hits'] - 1):
            strike(s, 5)
    ks = [ai_trial(1200 + i, three, ticks=2)[1] for i in range(30)]
    check('A3 3 hits only: no counter', all(k is None for k in ks), ks)
    # the skill trigger
    def skill_setup(age, dist, cd=False):
        def f(s):
            H.hold(s, False)
            H.place_body(s, API.CX, API.CZ, yaw=0.0)
            H.place_player(s, API.CX, API.CZ + dist)
            s.setsc('#ai_pht', 'hr', age)
            s.setsc('#rec', 'hr', 40)
            if cd:
                s.setsc('#a6cd', 'hr', hr(s, '#clk') + 100)
            strike(s, 5, skill=True)
        return f
    ks = [ai_trial(1300 + i, skill_setup(400, 3.0), ticks=2)[1] for i in range(120)]
    rate = ks.count('a6') / 120
    check(f'A4 the skill trigger: a skill hit within {API.A6_TRIGGER["near"]} b -> A6 at {API.A6_TRIGGER["chance"]} % (seeded)',
          0.45 <= rate <= 0.75, rate)
    for what, f in (('the phase younger than 200 t', skill_setup(100, 3.0)), ('farther than 4.5 b', skill_setup(400, 6.0)),
                    ('A6 cooling down', skill_setup(400, 3.0, cd=True))):
        ks = [ai_trial(1400 + i, f, ticks=2)[1] for i in range(30)]
        check(f'A5 no A6 with {what}', 'a6' not in ks, ks)
    # in a windup: <= 6 t -> A6 cancels it; later -> no
    def windup(t):
        def f(s):
            H.place_body(s, API.CX, API.CZ, yaw=0.0)
            H.place_player(s, API.CX, API.CZ + 3.0)
            s.setsc('#ai_pht', 'hr', 400)
            test(s, TID['a3'])
            H.hold(s, False)
            for _ in range(t):
                H.heal(s)
                H.world_sc(s)
            strike(s, 5, skill=True)
        return f
    early = [ai_trial(1500 + i, windup(3), ticks=2)[0] for i in range(40)]
    late = [ai_trial(1600 + i, windup(12), ticks=2)[0] for i in range(30)]
    check('A6 a skill hit in the first 6 t of a windup -> A6 replaces it (seeded share); after 6 t -> never',
          any(hr(s, '#pat') == TID['a6'] for s in early) and all(hr(s, '#pat') == TID['a3'] for s in late),
          (sum(hr(s, '#pat') == TID['a6'] for s in early), [hr(s, '#pat') for s in late][:5]))
    # the far rule: the player 12 b away for 30 t -> A4 / A10 at the decision
    def far_setup(s):
        H.hold(s, False)
        H.place_body(s, API.CX, API.CZ, yaw=0.0)
        H.place_player(s, API.CX, API.CZ + 12.0)
        s.setsc('#far', 'hr', API.FAR_RULE['dwell'])
        s.setsc('#rec', 'hr', 1)
        s.setsc('#last', 'hr', 0)
    ks = [ai_trial(1700 + i, far_setup, ticks=3)[1] for i in range(150)]
    share = ks.count('a4') / max(1, ks.count('a4') + ks.count('a10'))
    check('A7 the far rule (P1): A4 60 / A10 40 (seeded)', set(ks) <= {'a4', 'a10'} and 0.48 <= share <= 0.72, (share, set(ks)))
    def far_cd(s):
        far_setup(s)
        for k in ('a4', 'a10'):
            s.setsc(f'#cd_{k}', 'hr', hr(s, '#clk') + 500)
    s, k = ai_trial(1900, far_cd, ticks=3)
    check('A8 the far rule with A4 and A10 cooling down: the glide in, then A3 (#ai_nx)', k is None and hr(s, '#ai_nx') == TID['a3']
          and hr(s, '#ai_mv') == 4, (k, hr(s, '#ai_nx'), hr(s, '#ai_mv')))
    ok, R = until(s, lambda s: hr(s, '#pat') != 0, 200)
    check('A9 ... and A3 when she is within 8 b', ok and hr(s, '#pat') == TID['a3'], hr(s, '#pat'))
    # the rear rule: the player behind her for >= 4 of the last 6 samples -> A1 (its cooldown ignored once per 200 t)
    def rear_setup(cd):
        def f(s):
            H.hold(s, False)
            H.place_body(s, API.CX, API.CZ, yaw=0.0)
            H.place_player(s, API.CX, API.CZ - 3.0)
            s.setsc('#rear', 'hr', 0b111100)
            s.setsc('#rec', 'hr', 1)
            s.setsc('#last', 'hr', 0)
            s.setsc('#ai_rcd', 'hr', hr(s, '#clk') - API.REAR_RULE['cd_ignore_every'])
            if cd:
                s.setsc('#cd_a1', 'hr', hr(s, '#clk') + 500)
        return f
    s, k = ai_trial(2000, rear_setup(False), ticks=2)
    check('A10 the rear rule: behind her 20 of 30 t -> A1', k == 'a1', k)
    s, k = ai_trial(2001, rear_setup(True), ticks=2)
    check('A11 the rear rule ignores A1\'s cooldown once per 200 t', k == 'a1', k)
    def rear_twice(s):
        rear_setup(True)(s)
        s.setsc('#ai_rcd', 'hr', hr(s, '#clk') - 50)
    s, k = ai_trial(2002, rear_twice, ticks=2)
    check('A12 ... but not twice within 200 t (normal pick instead)', k != 'a1', k)
    # band weights (seeded, the pick functions directly; cooldowns ready, no repeat cleared)
    s, pl = world(2100)
    H.hold(s)
    random.seed(77)
    b = body(s)
    bc = H.Ctx(b, tuple(b.pos), tuple(b.rot))
    for band, d2, w in (('near', 300 ** 2, {k: API.WEIGHTS[k][1][0] for k in API.WEIGHTS if 1 in API.WEIGHTS[k]}),
                        ('mid', 600 ** 2, {k: API.WEIGHTS[k][1][1] for k in API.WEIGHTS if 1 in API.WEIGHTS[k]}),
                        ('far', 1300 ** 2, {k: API.WEIGHTS[k][1][2] for k in API.WEIGHTS if 1 in API.WEIGHTS[k]})):
        w = {k: v for k, v in w.items() if v > 0 and k in API.P1}
        cnt = {}
        n = 1500
        for _ in range(n):
            for k in API.COOLDOWN:
                s.setsc(f'#cd_{k}', 'hr', -10)
            s.setsc('#clk', 'hr', 1000)
            s.setsc('#last', 'hr', 0)
            s.setsc('#ai_d2', 'hr', d2)
            s.call(f'rlk:boss/scarlet/ai/pick/p1_{band}', bc)
            k = S3.KEY_OF.get(hr(s, '#pat'))
            cnt[k] = cnt.get(k, 0) + 1
            s.call('rlk:boss/scarlet/core/cancel_pat0', bc)
        tot = sum(w.values())
        dev = {k: round(cnt.get(k, 0) / n - v / tot, 3) for k, v in w.items()}
        check(f'A13 P1 {band} band weights {w} (seeded, n {n}): every share within 4 points', all(abs(x) <= 0.04 for x in dev.values())
              and set(cnt) <= set(w), (cnt, dev))
    # a long fight: cooldowns kept, no immediate repeat
    s, pl = world(2200)
    starts = []
    def mover(s, ang=[0.0]):
        ang[0] += 0.01
        r = 4.0 + 6.0 * (0.5 + 0.5 * math.sin(s.t / 97.0))
        pl = s.player()
        pl.pos = [API.CX + r * math.cos(ang[0]), 201.0, API.CZ + r * math.sin(ang[0])]
        H.C.moved(s)
        p = hr(s, '#pat')
        if p and (not starts or starts[-1][1] != p or mover.prev == 0):
            if mover.prev == 0:
                starts.append((hr(s, '#clk'), p))
        mover.prev = p
    mover.prev = 0
    run(s, 4000, each=mover)
    rep = [(a, b) for a, b in zip(starts, starts[1:]) if a[1] == b[1]]
    bad = []
    last = {}
    for clk, p in starts:
        k = S3.KEY_OF[p]
        cd = API.COOLDOWN.get(k, {}).get(1)
        if k in last and cd and clk - last[k] < cd and k != 'a1':
            bad.append((k, clk - last[k], cd))
        last[k] = clk
    check(f'A14 a long P1 fight ({len(starts)} patterns): no immediate repeat, no start inside its cooldown',
          len(starts) >= 15 and not rep and not bad, (len(starts), rep[:3], bad[:3]))


# ================================================================================================= bars
def sec_bars():
    s, pl = world(81)
    n0 = len(s.bar_draws)
    test(s, 20)
    t0 = s.t
    ok, R = until(s, lambda s: hr(s, '#ph') == PH['sq1'], 400)
    t1 = s.t
    draws_cs1 = [t for t in s.bar_draws[n0:] if t0 < t < t1]
    check('B1 CS1: bars_off (#mbBarOff 1), no bar drawn for its 213 t', ok and not draws_cs1 and all(r['baroff'] == 1 for r in R[:-1]),
          (ok, draws_cs1[:3]))
    R2 = run(s, 3)
    check('B2 SQ1 tick 0: bars_on (#mbBarOff 0), drawn again, the shield under bar (#buSub 5)',
          [t for t in s.bar_draws if t > t1] and mb(s, '#mbBarOff') == 0 and s.sc('#buSub', 'bu') == API.PIPS,
          (s.bar_draws[-3:], mb(s, '#mbBarOff'), s.sc('#buSub', 'bu')))


# ================================================================================================= look (theme build)
def look_stubs(s, job_t=60):
    """The arena look jobs as stubs: each one is a job of job_t ticks (#mbArBuild; job_tick counts it down); a call while
    another job runs is counted (#LOOKOVL azs: the core must never start one then). The plaza counts as built (a /reload
    finds it, as in game)."""
    for look, i in API.LOOK_ID.items():
        s.cache[f'rlk:mboss/arena/hr_field/look/{look}'] = ['execute if score #mbArBuild mb matches 1.. run scoreboard players add #LOOKOVL azs 1',
                                                            f'scoreboard players set #mbArBuild mb {job_t}',
                                                            'data modify storage rlk:mboss arjob set value {aid:"hr_field"}']
        s.watch[f'rlk:mboss/arena/hr_field/look/{look}'] = []
    # I1b: with S1K's theme merged the real arena/job_tick dispatches to the real hr_field/tick (a /reload re-arms job_tick
    # through mboss/init); the stub job is driven by job_tick() below, so the theme's slice runner is a no-op here
    s.cache['rlk:mboss/arena/hr_field/tick'] = ['# stub (test_scarlet look_stubs): the test drives the job']
    s.storage.setdefault('rlk:mboss', {})['built'] = 'plaza@2'
    s.setb(200, 200, 8, 'minecraft:pink_wool')


def job_tick(s):
    """One slice of the stub job per tick (the arena job of S1K's theme: rlk:mboss arjob + #mbArBuild)."""
    if mb(s, '#mbArBuild') >= 1:
        s.setsc('#mbArBuild', 'mb', mb(s, '#mbArBuild') - 1)
        if mb(s, '#mbArBuild') == 0:
            s.storage.get('rlk:mboss', {}).pop('arjob', None)


def looks_run(s):
    out = []
    for look in API.LOOK_ID:
        out += [(t, look) for t, *_ in s.watch[f'rlk:mboss/arena/hr_field/look/{look}']]
    return sorted(out)


def sec_look():
    s, pl = world(91, name='kit')
    look_stubs(s, job_t=120)
    H.place_player(s, API.CX + 0.5, API.CZ + 6.0)
    test(s, 20)                                           # CS1: crimson at 'recolour'
    ok, R = until(s, lambda s: hr(s, '#ph') == PH['sq1'] and hr(s, '#sq') >= API.ev('sq1', 'dark') + 2, 600, each=job_tick)
    lr = looks_run(s)
    check('L1 the crimson job runs at CS1 recolour; the SQ1 dark request waits while it runs (#mbArBuild >= 1)',
          lr and lr[0][1] == 'crimson' and all(l != 'dark' for _, l in lr) and hr(s, '#hrLook') == API.LOOK_ID['dark']
          and mb(s, '#mbArBuild') >= 1, (lr, hr(s, '#hrLook'), mb(s, '#mbArBuild')))
    pause_for(s, 15)
    ok, R = until(s, lambda s: hr(s, '#hrLook') == 0, 300, each=job_tick)
    lr = looks_run(s)
    check('L2 a pause inside the running job: the pending dark request is kept and runs when the job is over',
          ok and lr[-1][1] == 'dark' and mb(s, '#mbArBuild') >= 1, (lr, mb(s, '#mbArBuild')))
    # a /reload inside the dark job (A8): crimson requested again (core/re/look), A8 restarts through lead_stand (dark again),
    # its judge lifts the darkness (crimson); the jobs never overlap and the last one is the look the state needs
    n0 = len(lr)
    reload(s)
    ok, R = until(s, lambda s: hr(s, '#ph') == PH['p2'] and hr(s, '#hrLook') == 0 and mb(s, '#mbArBuild') == 0, 1500,
                  each=job_tick)
    lr2 = looks_run(s)
    check('L3 a /reload inside the job: no job started while another runs, nothing left pending, the requests served in order',
          ok and (s.sc('#LOOKOVL', 'azs') or 0) == 0 and hr(s, '#hrLook') == 0 and len(lr2) > n0, (lr2, s.sc('#LOOKOVL', 'azs')))
    check('L4 the final look = the last one requested = crimson after the A8 judge (#lk)', lr2[-1][1] == 'crimson'
          and API.LOOK_ID[lr2[-1][1]] == hr(s, '#lk'), (lr2[-1], hr(s, '#lk')))


# ================================================================================================= pause / reload (§3.8)
def at_phase(seed, tid, cond, limit=900, name='base', dash=None):
    s, pl = world(seed, name=name)
    H.place_player(s, API.CX + 0.5, API.CZ + 6.0)
    if tid:
        test(s, tid)
    ok, R = until(s, cond, limit, each=dash)
    assert ok, (tid, rec(s))
    return s, pl


def frozen(s, n=20):
    a = rec(s)
    R = pause_for(s, n)
    b = R[-1]
    same = all(a[k] == b[k] for k in ('ph', 'sqn', 'sq', 'pat', 'pt', 'hp', 'pips'))
    R2 = run(s, 5)
    moved = R2[-1]['sq'] != a['sq'] or R2[-1]['pt'] != a['pt'] or R2[-1]['ph'] != a['ph']
    return same, moved, a, b


def sec_pause():
    # CS0 (the intro)
    s, pl = intro_world(101, name='base')
    run(s, 100)
    same, moved, a, b = frozen(s)
    check('R1 CS0 pause: freezes (#sq), then continues', same and moved, (a['sq'], b['sq']))
    reload(s)
    run(s, 1)
    check('R2 CS0 /reload: the end of the intro (fight state P1, the 60 % floor, music 1, no rock)',
          mb(s, '#mbSt') == 1 and hr(s, '#ph') == PH['p1'] and mb(s, '#mbFloor') == FL60 and mb(s, '#mbMusPh') == 1
          and not H.ents_tagged(s, 'rlk_hr_deco_seat'), (mb(s, '#mbSt'), hr(s, '#ph')))
    # a P1 pattern
    s, pl = at_phase(102, TID['a3'], lambda s: hr(s, '#pt') >= 20)
    same, moved, a, b = frozen(s)
    check('R3 P1 pattern pause: freezes, then continues', same and moved, (a['pt'], b['pt']))
    reload(s)
    check('R4 P1 pattern /reload: cancelled (no pattern entity), the recovery', hr(s, '#pat') == 0 and hr(s, '#rec') >= 1
          and not [1 for _, tg in H.ents_tagged(s, 'rlk_hr_p') if 'rlk_hr_p' in tg], (hr(s, '#pat'), H.ents_tagged(s, 'rlk_hr_p')))
    # CS1
    s, pl = at_phase(103, 20, lambda s: hr(s, '#ph') == PH['cs1'] and hr(s, '#sq') >= 50)
    same, moved, a, b = frozen(s)
    check('R5 CS1 pause: freezes, then continues', same and moved, (a['sq'], b['sq']))
    reload(s)
    check('R6 CS1 /reload: SQ1 tick 0 (phase sq1, cine off, the bars back, music 2, the shield 5/5; its clock held one tick)',
          hr(s, '#ph') == PH['sq1'] and hr(s, '#sqn') == SEQ['sq1'] and hr(s, '#sq') == -1 and mb(s, '#mbCine') == 0
          and mb(s, '#mbBarOff') == 0 and mb(s, '#mbMusPh') == 2 and hr(s, '#pips') == API.PIPS,
          (hr(s, '#ph'), hr(s, '#sqn'), hr(s, '#sq'), mb(s, '#mbCine'), mb(s, '#mbMusPh')))
    # SQ1
    s, pl = at_phase(104, 20, lambda s: hr(s, '#ph') == PH['sq1'] and hr(s, '#sq') >= 30, 600)
    same, moved, a, b = frozen(s)
    check('R7 SQ1 pause: freezes, then continues', same and moved, (a['sq'], b['sq']))
    reload(s)
    check('R8 SQ1 /reload: SQ1 again from 0 (its clock held one tick)', hr(s, '#ph') == PH['sq1'] and hr(s, '#sq') == -1
          and hr(s, '#sqn') == SEQ['sq1'], (hr(s, '#ph'), hr(s, '#sq')))
    ok, R = until(s, lambda s: hr(s, '#ph') != PH['sq1'], 80)
    sq1 = [r for r in R if r['ph'] == PH['sq1']]
    check('R8b I1 (s3-10): the restarted SQ1 shows clip tick #sq on every tick (#sq = hrRigT, from 0), 60 t',
          ok and sq1 and sq1[0]['sq'] == 0 and all(r['sq'] == r['rigt'] for r in sq1) and len(sq1) in (60, 61),
          (ok, [(r['sq'], r['rigt']) for r in sq1 if r['sq'] != r['rigt']][:4], len(sq1)))
    # A8 / A13: pause -> cancelled, resume -> lead_stand {g} -> the gauntlet from T0 with 5/5; reload as pause
    for g, tid in (('a8', 21), ('a13', 27)):
        s, pl = at_phase(105, tid, lambda s: hr(s, '#ph') == PH[g] and hr(s, '#pt') >= 60, dash=dasher(CUTS[g][:2]))
        R = pause_for(s, 10)
        cut_left = [tg for _, tg in H.ents_tagged(s, 'rlk_hr_') if 'rlk_hr_pip' in tg or 'rlk_hr_cut' in tg]
        check(f'R9 {g.upper()} pause: cancelled at once (no cut / pip window, #pat 0, the shield off)',
              hr(s, '#pat') == 0 and not cut_left and hr(s, '#pips') == 0 and hr(s, '#grs') == 1, (hr(s, '#pat'), cut_left, hr(s, '#grs')))
        ok0, R0 = until(s, lambda s: hr(s, '#ph') == PH['lead'], 5)
        ok, R = until(s, lambda s: hr(s, '#ph') == PH[g], 200)
        ok = ok and ok0
        lead = [r for r in R0 + R if r['ph'] == PH['lead']]
        check(f'R10 {g.upper()} resume: lead_stand {{g:"{g}"}} ({API.SEQ_LEN["lead_stand"]} t), then {g.upper()} from T0 with 5/5',
              ok and len(lead) in range(API.SEQ_LEN['lead_stand'] - 1, API.SEQ_LEN['lead_stand'] + 2) and hr(s, '#pips') == API.PIPS
              and hr(s, '#pt') <= 1, (ok, len(lead), hr(s, '#pips'), hr(s, '#pt')))
        check(f'R10b {g.upper()} I1 (s3-10): the lead-in restarted by the resume shows clip tick #sq on every tick (#sq = hrRigT, '
              f'from 0; {API.SEQ_LEN["lead_stand"]} t)', lead and lead[0]['sq'] == 0 and all(r['sq'] == r['rigt'] for r in lead)
              and len(lead) == API.SEQ_LEN['lead_stand'], ([(r['sq'], r['rigt']) for r in lead if r['sq'] != r['rigt']][:4], len(lead)))
        s, pl = at_phase(106, tid, lambda s: hr(s, '#ph') == PH[g] and hr(s, '#pt') >= 60)
        reload(s)
        check(f'R11 {g.upper()} /reload: as pause -> lead_stand {{g:"{g}"}} at once', hr(s, '#ph') == PH['lead']
              and hr(s, '#sqn') == SEQ['lead_stand'] and hr(s, '#gk') == S3.GK[g] and hr(s, '#pat') == 0,
              (hr(s, '#ph'), hr(s, '#sqn'), hr(s, '#gk')))
        ok, R = until(s, lambda s: hr(s, '#ph') != PH['lead'], 100)
        lead = [r for r in R if r['ph'] == PH['lead']]
        check(f'R11b {g.upper()} I1 (s3-10): the lead-in restarted by /reload shows clip tick #sq on every tick (#sq = hrRigT, '
              f'from 0)', ok and lead and lead[0]['sq'] == 0 and all(r['sq'] == r['rigt'] for r in lead),
              ([(r['sq'], r['rigt']) for r in lead if r['sq'] != r['rigt']][:4], len(lead)))
    # CS2 / CS3
    for g, tid, ph in (('a8', 24, 'cs2'), ('a13', None, 'cs3')):
        if tid:
            s, pl = at_phase(107, tid, lambda s: hr(s, '#ph') == PH[ph] and hr(s, '#sq') >= 30)
        else:
            s, pl = at_phase(107, 28, lambda s: hr(s, '#ph') == PH[ph] and hr(s, '#sq') >= 30, dash=dasher(CUTS['a13']))
        same, moved, a, b = frozen(s)
        check(f'R12 {ph.upper()} pause: freezes, then continues', same and moved, (a['sq'], b['sq']))
        hp0 = hp(s)
        reload(s)
        if ph == 'cs2':
            check('R13 CS2 /reload: its end - the HP steps not applied yet, then the down window',
                  hr(s, '#ph') == PH['down'] and hp(s) == hp0 - 2 * HP * 15 // 1000, (hr(s, '#ph'), hp0, hp(s)))
        else:
            check('R13 CS3 /reload: its end - the lethal hit -> CS4 (death state)', mb(s, '#mbSt') == 2 or body(s) is None
                  or 'rlk_mb_dying' in body(s).tags, (mb(s, '#mbSt'),))
    # down
    s, pl = at_phase(108, 25, lambda s: hr(s, '#ph') == PH['down'] and hr(s, '#down') <= 150)
    d0 = hr(s, '#down')
    pause_for(s, 20)
    check('R14 down pause: the timer pauses', hr(s, '#down') == d0, (d0, hr(s, '#down')))
    s, pl = at_phase(109, 25, lambda s: hr(s, '#ph') == PH['down'] and hr(s, '#down') >= 150)
    reload(s)
    check('R15 down /reload: it goes on with <= 100 t left', hr(s, '#ph') == PH['down'] and hr(s, '#down') == 100, hr(s, '#down'))
    # the lead-ins
    s, pl = at_phase(110, 26, lambda s: hr(s, '#ph') == PH['lead'] and hr(s, '#sq') >= 30)
    same, moved, a, b = frozen(s)
    check('R16 lead_stand pause: freezes, then continues', same and moved, (a['sq'], b['sq']))
    reload(s)
    check('R17 lead_stand /reload: again from 0 (crimson first; its clock held one tick, I1 s3-10)', hr(s, '#ph') == PH['lead']
          and hr(s, '#sq') == -1 and hr(s, '#sqn') == SEQ['lead_stand'], (hr(s, '#ph'), hr(s, '#sq')))
    # P2 pattern
    s, pl = at_phase(111, 33, lambda s: hr(s, '#ph') == PH['p2'] and hr(s, '#pat') >= 1 and hr(s, '#pt') >= 8, 400)
    reload(s)
    check('R18 P2 pattern /reload: cancelled + the recovery', hr(s, '#pat') == 0 and hr(s, '#ph') == PH['p2'], hr(s, '#pat'))
    # CS4: pause freezes (the death state), reload finishes the death (test_reward covers the reward)
    s, pl = world(112)
    H.kill(s, pl)
    run(s, 50)
    sq0 = hr(s, '#sq')
    pause_for(s, 10)
    check('R19 CS4 pause: the ending freezes', hr(s, '#sq') == sq0, (sq0, hr(s, '#sq')))


# ================================================================================================= cleanup
def sec_cs4():
    """I1 (request s3-8): the real seq/ending in the full core path (test 28: A13 with 0 pips -> deflect -> CS3 -> the kill
    at the kick -> death_start -> CS4): her distance to an unmoving player (pinned: no input, nothing moves them) over the
    ending ticks 300-1042 stays 3.5-6 b (PLAN §9.3; S2b's ev_dry.py checks the same in a dry run of seq/ending alone)."""
    s, pl = world(71)
    H.place_player(s, API.CX + 0.5, API.CZ + 6.0)
    test(s, 28)
    ok, R = until(s, lambda s: hr(s, '#sqn') == SEQ['ending'], 900)
    p0 = list(s.player().pos)
    dist = {}

    def pin(ss):
        ss.player().pos = list(p0)
        if hr(ss, '#sqn') == SEQ['ending']:
            b = body(ss)
            dist[hr(ss, '#sq')] = math.hypot(b.pos[0] - p0[0], b.pos[2] - p0[2])

    ok2, R2 = until(s, lambda s: hr(s, '#sqn') == SEQ['event'], API.SEQ_LEN['ending'] + 20, each=pin)
    late = [dist[k] for k in range(300, API.SEQ_LEN['ending']) if k in dist]
    check(f'C41 CS4 (the full core path): her distance to an unmoving player over ending ticks 300-{API.SEQ_LEN["ending"] - 1} '
          f'stays 3.5-6 b ({min(late or [0]):.2f}-{max(late or [0]):.2f}, {len(late)} ticks)',
          ok and ok2 and len(late) >= API.SEQ_LEN['ending'] - 300 - 1 and 3.5 <= min(late) and max(late) <= 6.0,
          (ok, ok2, len(late)))


def sec_cleanup():
    for how in ('won', 'abort', 'cleanup'):
        s, pl = world(121)
        s.setsc('#mbTest', 'mb', 1)
        s.storage['rlk:mboss']['tlast'] = {'id': 'scarlet', 'ch': 1, 'sp': 1}
        H.place_player(s, API.CX + 0.5, API.CZ + 6.0)
        test(s, 21)
        run(s, 50)
        s.setsc('#hrEv', 'hr', 2)
        if how == 'won':
            H.kill(s, pl)
            ok = H.until_sc(s, lambda s: mb(s, '#mbLive') == 0 and (s.sc('#combat', 'room') or 0) == 0, 2500, each=H.heal)
        elif how == 'abort':
            s.call('rlk:mboss/test/abort', H.ctx(pl))
            ok = H.until_sc(s, lambda s: mb(s, '#mbLive') == 0, 200, each=H.heal)
        else:
            # a defeat / a map change: the framework's mboss/cleanup (every module's cleanup hook), the body gone
            s.call('rlk:mboss/cleanup', H.C0)
            ok = H.until_sc(s, lambda s: mb(s, '#mbLive') == 0, 200)
        left = H.ents_tagged(s, 'rlk_hr_')
        fp = [k for k in S3.FP if s.sc(k, 'hr') is not None and k not in [f'#c{c}' for c in S3.CONSTS] + ['#cn1', '#cn1000']]
        check(f'C1 {how}: no rlk_hr_* entity, the core scores reset, storage core gone',
              ok and not left and not fp and 'core' not in s.storage.get('rlk:hr', {}), (ok, left[:3], fp[:5], s.storage.get('rlk:hr')))
        if how != 'won':
            check(f'C2 {how}: the event scores untouched by the cleanup (#hrEv kept)', s.sc('#hrEv', 'hr') == 2, s.sc('#hrEv', 'hr'))


# ================================================================================================= cost
JOB_FN = 'rlk:mboss/arena/hr_field/tick'      # one slice of the arena's running job (S1K's theme, I1b)


def watch_jobs(s):
    """I1b: log the ticks that run a slice of the arena job (a look job: 2.2-2.5 k commands; contract §5 gate 5 allows
    look-job spikes up to 5 k), so the per-tick limit of the fight is checked without them and they are checked apart."""
    s.watch.setdefault(JOB_FN, [])
    return s.t


def split_jobs(s, t0, hist):
    """(fight ticks, job-slice ticks) of a cmd_hist slice that started after tick t0 (world_sc: s.t += 1 first)."""
    jt = {t for t, *_ in s.watch.get(JOB_FN, [])}
    fight, job = [], []
    for k, c in enumerate(hist):
        (job if t0 + 1 + k in jt else fight).append(c)
    return fight, job


def sec_cost():
    s, pl = world(131)
    t_s = watch_jobs(s)
    def mover(s, ang=[0.0]):
        ang[0] += 0.013
        r = 3.0 + 7.0 * (0.5 + 0.5 * math.sin(s.t / 83.0))
        pl = s.player()
        pl.pos = [API.CX + r * math.cos(ang[0]), 201.0, API.CZ + r * math.sin(ang[0])]
        H.C.moved(s)
    n0 = len(s.cmd_hist)
    run(s, 1500, each=mover)
    p1 = s.cmd_hist[n0:]
    test(s, 33)
    n1 = len(s.cmd_hist)
    run(s, 1500, each=mover)
    p2 = s.cmd_hist[n1:]
    fs, js = split_jobs(s, t_s, s.cmd_hist[n0:])
    s2, pl2 = world(132)
    H.place_player(s2, API.CX + 0.5, API.CZ + 6.0)
    test(s2, 21)
    t_2 = watch_jobs(s2)
    n2 = len(s2.cmd_hist)
    run(s2, API.JUDGE_T['a8'], each=dasher(CUTS['a8'][:5]))
    g = s2.cmd_hist[n2:]
    f2, j2 = split_jobs(s2, t_2, g)
    allf = p1 + p2 + g
    avg = statistics.mean(allf)
    nojob, jobs = fs + f2, js + j2
    print(f'  cost: P1 avg {statistics.mean(p1):.0f} max {max(p1)}; P2 avg {statistics.mean(p2):.0f} max {max(p2)}; '
          f'A8 avg {statistics.mean(g):.0f} max {max(g)}; all {avg:.0f} (Apep ~830, target <= 600); without the arena job\'s '
          f'{len(jobs)} slice ticks max {max(nojob)}, those ticks max {max(jobs or [0])}')
    # I1b: the arena job's slice ticks (S1K's look jobs: CS1 crimson, the gauntlets' dark / crimson) are checked apart against
    # the contract's look-job spike limit (§5 gate 5: <= 5 k); every other tick stays <= 3000
    check('Z1 commands per fight tick: the average <= 830 (Apep) and <= 600 (target); every tick <= 3000 but the arena job\'s '
          'slice ticks, those <= 5000 (contract §5 gate 5)',
          avg <= 600 and max(nojob) <= 3000 and max(jobs or [0]) <= 5000, (avg, max(nojob), max(jobs or [0])))
    VARS['cost'] = (statistics.mean(p1), max(p1), statistics.mean(p2), max(p2), statistics.mean(g), max(g), avg)
    # I1: A13 and the sequence ticks with the real gauntlets / sequences / rig (the kit and the theme still missing: I1b)
    s3, pl3 = world(133)
    H.place_player(s3, API.CX + 0.5, API.CZ + 6.0)
    test(s3, 27)
    t_3 = watch_jobs(s3)
    n3 = len(s3.cmd_hist)
    run(s3, API.JUDGE_T['a13'], each=dasher(CUTS['a13'][:5]))
    a13 = s3.cmd_hist[n3:]
    f3, j3 = split_jobs(s3, t_3, a13)
    nojob, jobs = nojob + f3, jobs + j3
    name_of = {v: k for k, v in SEQ.items()}
    seqc = {}
    for seed, tid, limit in ((134, 20, 290), (135, 24, 120), (136, 26, 90), (137, 28, 1750)):
        sx, plx = world(seed)
        H.place_player(sx, API.CX + 0.5, API.CZ + 6.0)
        sx.storage.setdefault('rlk:pinv', {}).setdefault('order', [])    # a run's inventory record (the coda's grant reads it)
        sx.setsc(('e', plx.id), 'invCap', 9)
        test(sx, tid)
        t_x = watch_jobs(sx)
        nx = len(sx.cmd_hist)
        Rx = run(sx, limit)
        jt = {t for t, *_ in sx.watch.get(JOB_FN, [])}
        for k, (r, c) in enumerate(zip(Rx, sx.cmd_hist[nx:])):
            if r['sqn']:
                seqc.setdefault(name_of.get(r['sqn'], r['sqn']), []).append(c)
                if name_of.get(r['sqn']) in ('cs1', 'sq1', 'repel', 'lead_down', 'lead_stand'):
                    (jobs if t_x + 1 + k in jt else nojob).append(c)
    si, pli = intro_world(138, name='base')
    ni = len(si.cmd_hist)
    run_intro(si)
    seqc['intro'] = si.cmd_hist[ni:]
    fight_seq = [c for k in ('cs1', 'sq1', 'repel', 'lead_down', 'lead_stand') for c in seqc.get(k, [])]
    fight_all = allf + a13 + fight_seq
    avg2 = statistics.mean(fight_all)
    rows = [('P1', p1), ('P2', p2), ('A8', g), ('A13', a13)] + [(k, seqc[k]) for k in
                                                                ('intro', 'cs1', 'sq1', 'repel', 'lead_stand', 'ending', 'event') if k in seqc]
    for k, v in rows:
        print(f'  cost {k:10s} ticks {len(v):5d} avg {statistics.mean(v):6.0f} max {max(v):5d}')
    print(f'  cost fight state (P1 + P2 + A8 + A13 + cs1 / sq1 / repel / lead-ins): avg {avg2:.0f} max {max(fight_all)}; '
          f'the intro / ending / event are the intro and death states')
    print(f'  cost fight state without the arena job\'s slice ticks: {len(nojob)} ticks, max {max(nojob)}; the {len(jobs)} slice '
          f'ticks avg {statistics.mean(jobs or [0]):.0f} max {max(jobs or [0])}')
    check('Z2 I1: every fight-state tick incl. A13 and the fight-state sequences: the average <= 600 (target; Apep ~830 hard), '
          'every tick <= 3000 but the arena job\'s slice ticks (I1b), those <= 5000',
          avg2 <= 600 and max(nojob) <= 3000 and max(jobs or [0]) <= 5000, (avg2, max(nojob), max(jobs or [0])))
    VARS['cost_rows'] = [(k, len(v), statistics.mean(v), max(v)) for k, v in rows] + [('fight', len(fight_all), avg2, max(fight_all)),
                                                                                       ('fight, no job slice', len(nojob), statistics.mean(nojob), max(nojob)),
                                                                                       ('job slice ticks', len(jobs), statistics.mean(jobs or [0]), max(jobs or [0]))]


def main():
    try:
        for sec in SECTIONS:
            globals()[f'sec_{sec}']()
    finally:
        if 'root' in VARS:
            H.drop_variant(VARS.pop('root'))
    return H.summary('test_scarlet')


if __name__ == '__main__':
    sys.exit(main())
