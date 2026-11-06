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
           event scores 0); the seat point written exactly in every command that places or finds it (I1b round 2: the
           game block-centres a whole x / z, the sim does not); the empty hooks (aux_hit / incoming / hz_vis / pj_end) have
           no command; on_hit (skill flag, counter feed); test/help rows; uninstall (objective, storage, rlk_hr_*); the
           decor props (kit build)
  phases   the order of §4.6 with deflects (P1 -> CS1 -> SQ1 -> A8 -> CS2 -> down -> kipup -> P2 -> lead_stand -> A13 -> CS3
           -> death) and both fail branches (A8 fail -> P2 at T + 214 without a down window; A13 fail -> the instant death
           -> the revive stance -> A13 again); the floors 60 % / 5 % (never below by normal damage); the invulnerable windows
           tick by tick; the CS2 / CS3 HP steps (15 / 15 / 15 per mille, 15 / 15 / the kill) at flash 24 / land 75 / kick
           102; the down window's both exits (the timer -> kipup -> P2; the 5 % floor -> lead_down 40 t later); durations;
           the arena ambience (I1b round 1: ambient_p1 every 10 t in P1, ambient_p2 every 6 t in A8 / the down window / P2 /
           A13, none in a sequence)
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
           the final look is the last one requested; each job re-looks the decor props (I1b round 1: the halo p1 / p2 / off,
           the 8 lotus bud / bloom / bloom for moon / crimson / dark); V2 (HR-51): no job when the arena's stamp already
           reads the requested look (the decor re-looked, the request served all the same)
  pause    pause -> resume and /reload in every phase and sequence (PLAN §3.8)
  cs4      (I1, s3-8) the real seq/ending through the full core path: her distance to an unmoving player over ending
           ticks 300-1042 stays 3.5-6 b
  cleanup  won / cancel / defeat leave no rlk_hr_* entity, the core scores and storage core gone, the event scores kept;
           F-I (f3_requests r5, HR-05): objective hr holds nothing but the event scores (api.EV_FP), storage rlk:hr no seq
  cost     commands per fight tick (P1 + P2 + the gauntlets + the fight-state sequences) with the kit running for real
           (I1b verification round 1): average <= Apep's 830 (target <= 600), every tick <= 3000 but the arena look job's
           slice ticks (<= 5000, contract §5 gate 5); V2 (HR-50): also the down window (by its timer; a 5 % floor hit in
           it -> lead_down), the A8 fail -> P2, the A13 instant death -> the revive -> lead_stand -> A13, a 20-t pause and
           a /reload (its chain counted as a tick) right after A8's judge / in P2 / in the down window (Z5: all reached);
           Z4 (HR-51) no look job on an arena already in that look; Z6 (HR-52) the kit's prop chain idle through CS0
  f1       F1 (the 11-05 review fixes, the lead's decisions): HR-01 the judged A8 fail + a pause / reload / leave -> P2 at
           once; HR-07 A13 past its last counting cut with pips left + a pause / reload / leave -> the instant death at once
           (then the revive path), a reload while away keeps it pending, before that cut the restart stays; HR-06 tests 30 /
           35 refused outside P1 / P2, test 23's forced fail ends with its judge; HR-04 no counter / A6 between the floor hit
           and the reserved step (P1 / P2, basic / skill); HR-13 a passive near player never sees two empty picks in a row,
           a forced empty band -> the backstep (>= 5 b) -> the mid pick; HR-25 the move clip after a flinch (F1 round 1:
           the far fallback's approach glide too, P1 / P2); HR-26 no
           counter from 10 b, the counter from 3 b, no rear A1 at 10 b; HR-38 A6's P2 cooldown 400; F1 round 1: the pause /
           resume hook headers name #grs 4 / 5
"""
import math
import re
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
                        'pause', 'cleanup', 'cost', 'f1']
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


def world(seed=5, name='base', intro=False, kit=False):
    """kit: the kit runs for real (H.kit_on; I1b verification round 1, the cost section), else its calls are logged only."""
    s, pl = H.setup_sc(var(name), seed=seed)
    if kit:
        H.kit_on(s)
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
                rigc=s.sc(('e', b.id), 'hrRigC') if b else None, rvw=hr(s, '#rvw'),
                hold=(s.sc(('e', pl.id), 'hudHold') or 0) if pl else None)     # F2 (HR-29): the player's HUD hold after the tick


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


# I1b verification round 2 (m1): the game block-centres an absolute x / z written without a decimal point in summon / tp /
# execute positioned / facing (+0.5; never y), while mcsim reads every coordinate as written. A position the sim checks
# (K3's seat) holds in game only if the commands write its x / z with a decimal point (api.xyz).
ABS_POINT = re.compile(r'(summon \S+|tp \S+|teleport \S+|positioned|facing) (-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?) '
                       r'(-?\d+(?:\.\d+)?)(?=\s|$)')


def abs_points(root=None):
    """[(function, line no, (x, y, z) as written)] of every absolute point in the commands of F:boss/scarlet."""
    base = (root or DP) / 'data/rlk/function/boss/scarlet'
    out = []
    for p in sorted(base.rglob('*.mcfunction')):
        for i, ln in enumerate(p.read_text(encoding='utf-8').split('\n'), 1):
            if not ln.lstrip().startswith('#'):
                out += [(p.relative_to(base).with_suffix('').as_posix(), i, m.group(2, 3, 4)) for m in ABS_POINT.finditer(ln)]
    return out


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
    pts = abs_points()
    seat = [(f, i, t) for f, i, t in pts if all(abs(float(v) - c) < 1e-9 for v, c in zip(t, API.SEAT_POS))]
    need = {'spawn', 'core/deco', 'core/deco_seat', 'core/replay/start', 'seq/intro/skip'}
    bad = [(f, i, ' '.join(t)) for f, i, t in seat if '.' not in t[0] or '.' not in t[2]]
    check(f'K3b the seat point written exactly wherever a command places or finds it ({len(seat)} lines: x / z with a decimal '
          'point, so the game does not block-centre them; I1b round 2)', bool(seat) and need <= {f for f, _, _ in seat} and not bad,
          (bad, sorted(need - {f for f, _, _ in seat})))
    whole = {}
    for f, i, t in pts:
        if '.' not in t[0] or '.' not in t[2]:
            whole[' '.join(t)] = whole.get(' '.join(t), 0) + 1
    print('  K3b other absolute points with a whole x / z (block-centred in game, not checked here): '
          + (', '.join(f'{k} x{n}' for k, n in sorted(whole.items())) or 'none'))
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


AMB = {'ambient_p1': (10, (PH['p1'],)), 'ambient_p2': (6, (PH['a8'], PH['down'], PH['p2'], PH['a13']))}


def amb_cadence(s, R, need):
    """I1b verification round 1 (m4): the arena ambience in a run (core/amb -> amb1 / amb2; PLAN §6.3 / §6.4, request s1k-2),
    from the kit log (#ph read at each call): each preset only in its phases and once per beat (one player); within every span
    of those phases (records R) at least 2 beats long, a call every `step` t, span // step - 1 .. + 1 of them (a beat on a span's
    first tick can belong to the phase before); no other caller of the ambient presets but S2b's intro start (its E0 staging).
    need: the presets that must have run. Returns (ok, the faults)."""
    bad = {}
    amb = (H.ROOT_SC + 'core/amb1', H.ROOT_SC + 'core/amb2')
    for k, (step, phs) in AMB.items():
        allc = H.kit_ex(s, f'p/{k}')
        calls = [c for c in allc if c['caller'] in amb]
        other = [(c['t'], c['caller']) for c in allc if c['caller'] not in amb + (H.ROOT_SC + 'seq/intro/start',)]
        ts = [c['t'] for c in calls]
        wrong = [(c['t'], c['ph']) for c in calls if c['ph'] not in phs]
        short = []
        for ph, a, b in spans(R):
            if ph in phs and b - a + 1 >= 2 * step:
                inside = [t for t in ts if a <= t <= b]
                gaps = sorted({y - x for x, y in zip(inside, inside[1:])})
                if gaps != [step] or not ((b - a + 1) // step - 1 <= len(inside) <= (b - a + 1) // step + 1):
                    short.append((ph, a, b, len(inside), gaps))
        if wrong or len(ts) != len(set(ts)) or short or other or (k in need and not calls):
            bad[k] = (wrong[:4], len(ts) - len(set(ts)), short[:4], other[:4], len(calls))
    return not bad, bad


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
    # I1b verification round 1 (m4): the arena ambience through the whole chain, then a P1 stretch
    amb = {ph: n for ph, a, b in spans(R) for n in [b - a + 1] if ph in AMB['ambient_p2'][1]}
    ok_a, why = amb_cadence(s, R, need=('ambient_p2',))
    check(f'P14 the ambience (core/amb): ambient_p2 at the player every 6 t in A8, the down window, P2 and A13 ({amb} ticks), '
          f'none in the sequences (CS1, SQ1, CS2, the lead-in, CS3, the death), ambient_p1 only in P1', ok_a, why)
    s1, _pl = world(16)
    H.place_player(s1, API.CX + 0.5, API.CZ + 6.0)
    R1 = run(s1, 300)
    ok_a, why = amb_cadence(s1, R1, need=('ambient_p1',))
    n1 = len([c for c in H.kit_ex(s1, 'p/ambient_p1') if c['caller'] == H.ROOT_SC + 'core/amb1'])
    check(f'P15 the ambience in P1: ambient_p1 at the player every 10 t ({n1} calls in {len(R1)} ticks), no ambient_p2',
          ok_a and all(r['ph'] == PH['p1'] for r in R1) and not H.kit_ex(s1, 'p/ambient_p2'), why)
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
def intro_world(seed, name='kit', kit=False):
    s, pl = H.setup_sc(var(name), seed=seed)
    if kit:
        H.kit_on(s)
    ok = H.fight_sc(s, intro=True)
    assert ok
    return s, pl


# The intro's end distance (lead decision 1, I1b): the walk keeps its 0.15 b/t legs and the seat rock sits 5 b nearer the
# start (api.SEAT_POS (884.0, 201, 5.0), 26.7 b from `start`; written exactly since I1b round 2, K3b, so the game puts her
# there too; the legs walk while she is more than 7 b away), so a player who stays at `start` meets her <= 7 b away when the
# walk stops, as the skip stands her (PLAN §3.1, E10's pose). I2 compares every key of the end state again, `near` included
# (I1a had left it out while the decision was open: i1_notes §10, §11 m3).
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
def hud_tick(s):
    """F2 (HR-29): the player's actionbar HUD tick before the module's (F:player/hud/tick: while hudHold >= 1 it rests and
    counts it down; the sim does not run it): a sequence that holds the HUD sets it back to 2 each tick."""
    pl = s.player()
    if pl and (s.sc(('e', pl.id), 'hudHold') or 0) >= 1:
        s.setsc(('e', pl.id), 'hudHold', s.sc(('e', pl.id), 'hudHold') - 1)


# F2 round 1 (VF2-1-02): the HUD-off sequences blank the actionbar once at their start (the game keeps the last one ~60 t)
HUD_OFF_SEQ = ('intro', 'cs1', 'ending', 'event')
BLANK = '@a[tag=player] actionbar ""'


def watch_starts(s, names=HUD_OFF_SEQ):
    for n in names:
        s.watch[f'rlk:boss/scarlet/seq/{n}/start'] = []


def blank_at_start(s, name):
    """(ok, detail): seq/<name>/start ran and the same tick sent the empty actionbar"""
    ts = [t for t, *_ in s.watch.get(f'rlk:boss/scarlet/seq/{name}/start', [])]
    blank = {t for t, x in s.titles if x.strip() == BLANK}
    return bool(ts) and all(t in blank for t in ts), (name, ts, sorted(blank)[:4])


# F2 round 1 (V2R-02): the framework shows the bars in mboss/start_go after her spawn hook; F-I guards that show with
# #mbBarOff (f2_requests f2-8, start_go is pack-wide). Until the guard is in the tree the test emulates it, so the module's part
# (her spawn turns the bars off) is still proven end to end; with the guard present the real file runs.
START_GO_GUARD = 'execute unless score #mbBarOff mb matches 1 run function rlk:mboss/bars_show'


def bar_log(s, log):
    log.append((s.t, s.bars.get('rlk:mboss'), mb(s, '#mbBarOff')))


def bars_intro_world(seed):
    """world(seed, intro=True) with logs from the rift on: [(t, rlk:mboss visible, #mbBarOff)] after every tick, the
    start_go tick and the HUD-off sequence starts; returns (s, pl, log, start_go tick, guard in the tree)"""
    s, pl = H.setup_sc(var('base'), seed=seed)
    lines = s.load('rlk:mboss/start_go')
    guarded = any(START_GO_GUARD in x for x in lines)
    if not guarded:
        s.cache['rlk:mboss/start_go'] = [START_GO_GUARD if x.strip() == 'function rlk:mboss/bars_show' else x for x in lines]
    s.watch['rlk:mboss/start_go'] = []
    watch_starts(s)
    log = []
    z, a = H.rift_zone(s, 'scarlet')
    s.player().pos = list(a.pos)
    r = H.enter(s, a)

    def cond(ss):
        bar_log(ss, log)
        return (body(ss) is not None and mb(ss, '#mbSt') == 0 and hr(ss, '#ph') == 0 and hr(ss, '#sq') >= 1)
    ok = bool(r) and H.until_sc(s, cond, 900)
    assert ok, 'the fight did not start'
    s.zone_sc = z
    sg = [t for t, *_ in s.watch['rlk:mboss/start_go']]
    return s, pl, log, (sg[0] if sg else None), guarded


def sec_bars():
    s, pl = world(81)
    n0 = len(s.bar_draws)
    watch_starts(s)
    test(s, 20)
    t0 = s.t
    ok, R = until(s, lambda s: hr(s, '#ph') == PH['sq1'], 400, each=hud_tick)
    t1 = s.t
    draws_cs1 = [t for t in s.bar_draws[n0:] if t0 < t < t1]
    check('B1 CS1: bars_off (#mbBarOff 1), no bar drawn for its 213 t', ok and not draws_cs1 and all(r['baroff'] == 1 for r in R[:-1]),
          (ok, draws_cs1[:3]))
    # F2 (HR-29): the player's actionbar HUD held (hudHold >= 1 after every tick: player/hud/tick rests) through CS1
    ok6, why6 = blank_at_start(s, 'cs1')
    check('B6 CS1: the player HUD held every tick (hudHold >= 1), the actionbar blanked at its start',
          ok and ok6 and all(r['hold'] >= 1 for r in R[:-1]), ([(r['t'], r['hold']) for r in R[:-1] if r['hold'] < 1][:4], why6))
    R2 = run(s, 3, each=hud_tick)
    check('B2 SQ1 tick 0: bars_on (#mbBarOff 0), drawn again, the shield under bar (#buSub 5)',
          [t for t in s.bar_draws if t > t1] and mb(s, '#mbBarOff') == 0 and s.sc('#buSub', 'bu') == API.PIPS,
          (s.bar_draws[-3:], mb(s, '#mbBarOff'), s.sc('#buSub', 'bu')))
    check('B7 SQ1: the HUD is back (no hold)', R2[-1]['hold'] == 0, R2[-1]['hold'])
    # F2 (HR-29): CS0 shows no boss bar (bars off at the intro's start; the original's bar grows at control, f498) and holds the
    # player HUD; at control the bars come back, the HP bar filling over its first 30 t (mboss/bars_ramp)
    s, pl, blog, tsg, guarded = bars_intro_world(83)
    n0 = len(s.bar_draws)
    t0 = s.t
    ok, R = until(s, lambda s: (bar_log(s, blog), hr(s, '#ph') == PH['p1'])[1], API.SEQ_LEN['intro'] + 200, each=hud_tick)
    t1 = s.t
    intro = [r for r in R if r['ph'] == PH['intro']]
    draws = [t for t in s.bar_draws[n0:] if t0 <= t < t1]
    check('B3 CS0: no boss bar drawn (#mbBarOff 1) until control', ok and len(intro) > 500 and not draws
          and all(r['baroff'] == 1 for r in intro), (ok, len(intro), draws[:3], sorted({r['baroff'] for r in intro})))
    # V2R-02: from the start_go tick on (her spawn: bars off) the boss bar is never on screen until control (t1: P1)
    at_sg = [(t, v, off) for t, v, off in blog if t == tsg]
    shown = [t for t, v, _off in blog if tsg is not None and tsg <= t < t1 and v]
    check('B3a her spawn hook turns the bars off before the framework\'s show (#mbBarOff 1 at the end of the start_go tick)',
          tsg is not None and at_sg and at_sg[0][2] == 1, (tsg, at_sg))
    check(f'B3b the boss bar never visible from start_go to control (start_go\'s show {"guarded" if guarded else "guard EMULATED"})',
          tsg is not None and not shown, (tsg, shown[:4]))
    if not guarded:
        print('B3b: PENDING F-I (f2_requests f2-8): rlk:mboss/start_go still shows the bars unguarded; B3b ran with the guard '
              'emulated in the sim')
    ok4, why4 = blank_at_start(s, 'intro')
    check('B4 CS0: the player HUD held every tick, the actionbar blanked at its start', ok and ok4
          and all(r['hold'] >= 1 for r in intro), ([(r['t'], r['hold']) for r in intro if r['hold'] < 1][:4], why4))
    ramp = []
    R3 = run(s, 32, each=lambda ss: ramp.append(ss.sc('#buHp', 'bu')))
    hpv = [v for v in ramp[1:] if v is not None]
    check('B5 control: the bars back (#mbBarOff 0, drawn), the HP bar filling over 30 t (mboss/bars_ramp), then full',
          mb(s, '#mbBarOff') == 0 and [t for t in s.bar_draws if t > t1] and hpv and hpv[0] < hpv[-1]
          and all(a <= b for a, b in zip(hpv, hpv[1:])), (mb(s, '#mbBarOff'), hpv[:4], hpv[-2:]))
    # LF-01: the moon halo's point written exactly (x / z with a decimal point: the game block-centres a whole x / z)
    halo = [l for f in ('core/deco', 'core/deco_re') for l in (FN / f'{f}.mcfunction').read_text(encoding='utf-8').split('\n')
            if 'summon minecraft:item_display' in l and 'rlk_hr_deco_moon_halo' in l]
    loose = [l for l in halo if not re.search(r'summon minecraft:item_display -?\d+\.\d+ -?[\d.]+ -?\d+\.\d+ ', l)]
    check('LF-01: the halo summons (core/deco, core/deco_re) keep x / z exact', len(halo) == 3 and not loose, (len(halo), loose[:1]))


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


def look_stamp(look):
    """The arena's stamp once a job of that look is done (framework arena/<aid>/done: built_<aid> = "<aid>@<ver>:<look>")."""
    return f'{API.AID}@{API.ARENA["ver"]}:{look}'


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
    # I1b verification round 1 (m4): core/look/go re-looks S3's decor props with each job (PLAN §6.3-§6.5 "kit props"): the one
    # halo and the 8 lotus, in the tick the job starts, from look/go itself (a /reload's core/deco_re re-spawns them apart)
    deco = {'moon': ('p1', 'bud'), 'crimson': ('p2', 'bloom'), 'dark': ('off', 'bloom')}
    go = H.ROOT_SC + 'core/look/go'
    halo = [c for c in H.kit_ex(s, 'prop/moon_halo') if c['caller'] == go]
    lotus = [c for c in H.kit_ex(s, 'prop/lotus') if c['caller'] == go]
    bad = []
    for t, look in lr2:
        h = [c['a'].get('look') for c in halo if c['t'] == t and API.TAGS['deco_moon_halo'] in c['tags']]
        lo = [c['a'].get('look') for c in lotus if c['t'] == t and API.TAGS['deco_lotus'] in c['tags']]
        if h != [deco[look][0]] or lo != [deco[look][1]] * 8:
            bad.append((t, look, h, lo))
    orphan = sorted({c['t'] for c in halo + lotus} - {t for t, _ in lr2})
    # the moon row: no fight request asks for moon (the arena starts in it), so a moon request is served here directly
    s.setsc('#mbArBuild', 'mb', 0)
    s.storage.get('rlk:mboss', {}).pop('arjob', None)
    # (V2, HR-51: the stub jobs leave the fight's first stamp, moon; the real crimson job of the A8 judge stamped crimson)
    s.storage.setdefault('rlk:mboss', {})[f'built_{API.AID}'] = look_stamp('crimson')
    s.setsc('#hrLook', 'hr', API.LOOK_ID['moon'])
    n0 = len(s.kitl)
    H.call_sc(s, 'core/look')
    moon = [(c, a.get('look'), x) for (t, c, a), (x, f, ph) in list(zip(s.kitl, s.kitx))[n0:] if f == go]
    moon_ok = (sorted(lk for c, lk, x in moon if c == 'prop/moon_halo' and API.TAGS['deco_moon_halo'] in x) == [deco['moon'][0]]
               and [lk for c, lk, x in moon if c == 'prop/lotus' and API.TAGS['deco_lotus'] in x] == [deco['moon'][1]] * 8
               and looks_run(s)[-1][1] == 'moon')
    check(f'L5 each look job re-looks the decor props in its tick (core/look/go): moon -> halo p1 / lotus bud, crimson -> p2 / '
          f'bloom, dark -> off / bloom; the halo and all 8 lotus ({len(lr2)} jobs in the fight: {[l for _, l in lr2]}, + moon)',
          {l for _, l in lr2} >= {'crimson', 'dark'} and not bad and not orphan and moon_ok,
          (bad[:3], orphan[:3], moon_ok, [(c, lk) for c, lk, _x in moon][:3]))
    # V2 (HR-51, D6-02): a request for the look the arena already stands in (its stamp built_hr_field = "hr_field@<ver>:<look>",
    # written by the job's last slice, dropped when a job starts) starts no job; the decor props are re-looked all the same and
    # the request is served (#hrLook 0, #lk); another look's stamp or none (a job cut by a reload) -> the job runs
    rows = []
    for have, want in (('crimson', 'crimson'), ('dark', 'dark'), ('moon', 'moon'), ('moon', 'crimson'), (None, 'crimson'),
                       ('crimson', 'dark'), ('dark', 'crimson')):
        st = s.storage.setdefault('rlk:mboss', {})
        s.setsc('#mbArBuild', 'mb', 0)
        st.pop('arjob', None)
        st.pop(f'built_{API.AID}', None)
        if have:
            st[f'built_{API.AID}'] = look_stamp(have)
        s.setsc('#hrLook', 'hr', API.LOOK_ID[want])
        n0, k0 = len(looks_run(s)), len(s.kitl)
        H.call_sc(s, 'core/look')
        halo = [a.get('look') for (t, c, a), (x, f, ph) in list(zip(s.kitl, s.kitx))[k0:] if f == go and c == 'prop/moon_halo']
        rows.append((have, want, len(looks_run(s)) - n0, halo, hr(s, '#hrLook'), hr(s, '#lk')))
    check('L6 V2 (HR-51): no look job when the arena already stands in the requested look (the stamp), the decor re-looked and '
          'the request served all the same; another look\'s stamp or none -> the job',
          all((n == 0) == (have == want) and n <= 1 and halo == [deco[want][0]] and lk0 == 0 and lk == API.LOOK_ID[want]
              for have, want, n, halo, lk0, lk in rows), rows)


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
    watch_starts(s)
    test(s, 28)
    ok, R = until(s, lambda s: hr(s, '#sqn') == SEQ['ending'], 900, each=hud_tick)
    p0 = list(s.player().pos)
    dist = {}

    def pin(ss):
        ss.player().pos = list(p0)
        hud_tick(ss)
        if hr(ss, '#sqn') == SEQ['ending']:
            b = body(ss)
            dist[hr(ss, '#sq')] = math.hypot(b.pos[0] - p0[0], b.pos[2] - p0[2])

    ok2, R2 = until(s, lambda s: hr(s, '#sqn') == SEQ['event'], API.SEQ_LEN['ending'] + 20, each=pin)
    # F2 (HR-29): CS4 and the event coda hold the player HUD every tick; CS3 (repel) keeps it
    ok3, R3 = until(s, lambda s: hr(s, '#sqn') != SEQ['event'], API.SEQ_LEN['event'] + 20, each=pin)
    held = [r for r in R2 + R3 if r['sqn'] in (SEQ['ending'], SEQ['event'])]
    rep = [r for r in R if r['sqn'] == SEQ['repel']]
    oke, whye = blank_at_start(s, 'ending')
    okv, whyv = blank_at_start(s, 'event')
    check('C42 CS4 + the coda: the player HUD held every tick (hudHold >= 1), the actionbar blanked at each start; CS3 keeps '
          'the HUD', len(held) > API.SEQ_LEN['ending'] and all(r['hold'] >= 1 for r in held) and rep and any(r['hold'] == 0 for r in rep)
          and oke and okv, (len(held), [(r['t'], r['sqn'], r['hold']) for r in held if r['hold'] < 1][:4], len(rep), whye, whyv))
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
        # F-I (f3_requests r5, F3's HR-05: save the event scores, `scoreboard players reset * hr`, restore): no other owner's
        # fake player (patterns, ghost helpers, sequences) nor any entity score is left in objective hr, nor storage seq
        held = sorted(str(k[0]) for k, v in s.scores.items() if k[1] == 'hr' and v is not None and k[0] not in API.EV_FP)
        check(f'C3 {how}: objective hr holds only the event scores (api.EV_FP), storage rlk:hr has no seq',
              ok and not held and 'seq' not in s.storage.get('rlk:hr', {}), (held[:6], sorted(s.storage.get('rlk:hr', {}))))


# ================================================================================================= cost
JOB_FN = 'rlk:mboss/arena/hr_field/tick'      # one slice of the arena's running job (S1K's theme, I1b)
TICK_MAX, SLICE_MAX = 3000, 5000               # every fight tick (S3); a look job's slice tick (contract §5 gate 5)
FIGHT_SEQ = ('cs1', 'sq1', 'repel', 'lead_down', 'lead_stand')
# V2 (HR-50, D6-01): the fight-state rows of the table — the sequences, the down window (phase, no sequence), the A8 / A13 fail
# branches, the pause / resume and the /reload samples
FIGHT_ROWS = ('A8 fail', 'A13 fail') + FIGHT_SEQ[:3] + ('down',) + FIGHT_SEQ[3:] + ('pause', 'reload')
LOOK_FN = f'rlk:mboss/arena/{API.AID}/look/'   # the start of an arena look job (V2, HR-51)
ANIM_FN = 'rlk:boss/scarlet/fx/e/anim'         # the kit's per-tick prop chain (V2, HR-52)
KIPUP = 20                                     # the down window's kipup after its 200 t (sec_phases P3)


def watch_jobs(s):
    """I1b: log the ticks that run a slice of the arena job (a look job: 2.2-2.5 k commands; contract §5 gate 5 allows
    look-job spikes up to 5 k), so the per-tick limit of the fight is checked without them and they are checked apart."""
    s.watch.setdefault(JOB_FN, [])
    return s.t


def log_looks(s, log):
    """V2 (HR-51): log every start of an arena look job (look/<look>) as (t, look, the arena's stamp at that moment)."""
    orig = s.call

    def call(fid, ctx, macro=None):
        if fid.startswith(LOOK_FN):
            log.append((s.t, fid[len(LOOK_FN):], (s.storage.get('rlk:mboss') or {}).get(f'built_{API.AID}')))
        return orig(fid, ctx, macro)
    s.call = call
    return s


def cost_run(s, n, each=None):
    """n world ticks of s (run()) as [(commands, the kit's own commands, slice tick?, record)]: a tick that runs a slice of
    the arena job is marked (I1b); the kit's share = the commands run inside rlk:boss/scarlet/fx/** (I1b round 1)."""
    t0, n0 = watch_jobs(s), len(s.cmd_hist)
    R = run(s, n, each=each)
    jt = {t for t, *_ in s.watch[JOB_FN]}
    return [(c, k, t0 + 1 + i in jt, r) for i, (c, k, r) in enumerate(zip(s.cmd_hist[n0:], s.kit_hist[n0:], R))]


def where(r, part):
    """A tick's place for the report: the sequence and its clock, else the phase / pattern and its clock."""
    name_of = {v: k for k, v in SEQ.items()}
    if r is None:
        return part
    if r['sqn']:
        return f'{name_of.get(r["sqn"], r["sqn"])} #sq {r["sq"]}'
    return f'{part} #pat {S3.KEY_OF.get(r["pat"], r["pat"])} #pt {r["pt"]}'


def sec_cost():
    """Commands per world tick, strict count (an `execute ... run X` counts X too), in fights on the real rig, sequences,
    gauntlets, the theme's look jobs and, since I1b verification round 1, the kit running for real (H.kit_on: the presets'
    cards, the card ager they schedule, the cull, the HUD tickers; each module kit call costs what it costs in the kit's own
    harness). The kit's share of each tick is reported apart. V2 (HR-50, D6-01): also the down window (by its timer and with
    the 5 % floor hit -> lead_down), the A8 / A13 fail branches (the revive path), a pause and a /reload at three points."""
    looks = []

    def cworld(seed):
        s, pl = world(seed, kit=True)
        log_looks(s, looks)
        return s, pl
    # P1 then P2 (test 33), the player circling C at 3-10 b
    s, pl = cworld(131)

    def mover(s, ang=[0.0]):
        ang[0] += 0.013
        r = 3.0 + 7.0 * (0.5 + 0.5 * math.sin(s.t / 83.0))
        pl = s.player()
        pl.pos = [API.CX + r * math.cos(ang[0]), 201.0, API.CZ + r * math.sin(ang[0])]
        H.C.moved(s)
    parts = {}
    parts['P1'] = cost_run(s, 1500, mover)
    test(s, 33)
    parts['P2'] = cost_run(s, 1500, mover)
    # the gauntlets with the first five cuts dashed (A8 from test 21, A13 from test 27)
    for seed, tid, g in ((132, 21, 'a8'), (133, 27, 'a13')):
        sg, plg = cworld(seed)
        H.place_player(sg, API.CX + 0.5, API.CZ + 6.0)
        test(sg, tid)
        parts[g.upper()] = cost_run(sg, API.JUDGE_T[g], dasher(CUTS[g][:5]))
    # V2 (HR-50): the fail branches, nothing dashed — A8 (test 21): the fail hit and P2 at T + FAIL60_P2_T; A13 (test 27): the
    # instant death, Ronova's revive (40 t), the stance, lead_stand and A13 again from T0
    sg, plg = cworld(140)
    H.place_player(sg, API.CX + 0.5, API.CZ + 6.0)
    test(sg, 21)
    parts['A8 fail'] = cost_run(sg, API.FAIL60_P2_T + 10)
    sg, plg = cworld(141)
    sg.revive = 40
    H.place_player(sg, API.CX + 0.5, API.CZ + 6.0)
    test(sg, 27)
    parts['A13 fail'] = cost_run(sg, API.JUDGE_T['a13'] + sg.revive + API.REVIVE['wait'] + API.SEQ_LEN['lead_stand'] + 30)
    deaths13 = len(sg.deaths)
    # the sequences: CS1 -> SQ1 (test 20), repel and (V2) the down window after it by its timer, the kipup included (24),
    # lead_stand (26), A13 deflect -> CS3 -> the kill -> CS4 -> the event (28)
    name_of = {v: k for k, v in SEQ.items()}
    seqc = {}
    down24 = 0
    for seed, tid, limit in ((134, 20, 290), (135, 24, API.SEQ_LEN['repel'] + API.DOWN_T + KIPUP + 10), (136, 26, 90),
                             (137, 28, 1750)):
        sx, plx = cworld(seed)
        H.place_player(sx, API.CX + 0.5, API.CZ + 6.0)
        sx.storage.setdefault('rlk:pinv', {}).setdefault('order', [])    # a run's inventory record (the coda's grant reads it)
        sx.setsc(('e', plx.id), 'invCap', 9)
        test(sx, tid)
        for x in cost_run(sx, limit):
            if x[3]['sqn']:
                seqc.setdefault(name_of.get(x[3]['sqn'], x[3]['sqn']), []).append(x)
            elif x[3]['ph'] == PH['down']:
                seqc.setdefault('down', []).append(x)
                down24 += tid == 24
    # V2 (HR-50): a hit reaching the 5 % floor 30 t into the down window (test 25) -> lead_down 40 t later -> A13
    sx, plx = cworld(139)
    H.place_player(sx, API.CX + 0.5, API.CZ + 6.0)
    test(sx, 25)
    hit = []

    def floor_hit(s):
        if not hit and hr(s, '#ph') == PH['down'] and hr(s, '#down') <= API.DOWN_T - 30:
            hit.append(s.t)
            to_floor(s)
    for x in cost_run(sx, 30 + API.DOWN_FLOOR_WAIT + API.SEQ_LEN['lead_down'] + 10, floor_hit):
        k = name_of.get(x[3]['sqn'], x[3]['sqn']) if x[3]['sqn'] else 'down' if x[3]['ph'] == PH['down'] else None
        if k:
            seqc.setdefault(k, []).append(x)
    # V2 (HR-50): a 20-t pause (pkMode; then 120 t) and a /reload (its own chain, rlk:mboss/init, counted as one tick; then
    # 120 t) right after A8's deflect judge (from CS1, test 20: the A8 in the dark look, the judge's crimson job running), in P2
    # with a pattern running and in the down window
    d8 = dasher(CUTS['a8'][:5])
    points = (('the A8 judge', 20, lambda s: hr(s, '#ph') == PH['a8'] and hr(s, '#pt') >= API.JUDGE_T['a8'] + 1),
              ('P2', 33, lambda s: hr(s, '#ph') == PH['p2'] and hr(s, '#pat') != 0 and hr(s, '#pt') >= 5),
              ('the down window', 25, lambda s: hr(s, '#ph') == PH['down'] and hr(s, '#down') <= API.DOWN_T - 50))
    reached, after = [], {}
    for i, (at, tid, cond) in enumerate(points):
        for how in ('pause', 'reload'):
            sp, plp = cworld(150 + 2 * i + (how == 'reload'))
            H.place_player(sp, API.CX + 0.5, API.CZ + 6.0)
            test(sp, tid)
            ok, _R = until(sp, cond, 900, each=d8)
            reached.append((at, how, ok))
            n_look = len(looks)
            if how == 'pause':
                sp.setsc(('e', plp.id), 'pkMode', 1)
                rows_ = cost_run(sp, 20)
                sp.setsc(('e', plp.id), 'pkMode', 0)
            else:
                n0, k0 = sp.ncmd, sp.nkit
                reload(sp)
                rows_ = [(sp.ncmd - n0, sp.nkit - k0, False, rec(sp))]
            rows_ += cost_run(sp, 120, d8)
            parts.setdefault(how, []).extend(rows_)
            after[(at, how)] = (looks[n_look:], max(x[0] for x in rows_), [x[0] for x in rows_ if x[2]])
    # the intro (CS0); V2 (HR-52): the kit's per-tick prop chain watched through it
    si, pli = intro_world(138, name='base', kit=True)
    si.watch[ANIM_FN] = []
    ni = len(si.cmd_hist)
    run_intro(si)
    seqc['intro'] = [(c, k, False, None) for c, k in zip(si.cmd_hist[ni:], si.kit_hist[ni:])]
    anim_cs0 = sorted({t for t, *_ in si.watch[ANIM_FN]})
    seat_left = [tg for _e, tg in H.ents_tagged(si, 'rlk_hr_') if 'rlk_hr_deco_seat_rock' in tg or 'rlk_hr_fxfs' in tg]
    # the table
    rows = [(k, parts[k]) for k in ('P1', 'P2', 'A8', 'A13', 'A8 fail', 'A13 fail')] + \
           [(k, seqc[k]) for k in ('intro',) + FIGHT_SEQ[:3] + ('down',) + FIGHT_SEQ[3:] + ('ending', 'event') if k in seqc] + \
           [(k, parts[k]) for k in ('pause', 'reload')]
    print('  cost (the kit running for real)  ticks    avg   max | no slice: max | kit share: avg   max')
    for k, v in rows:
        ns = [x[0] for x in v if not x[2]]
        print(f'  cost {k:10s} {len(v):27d} {statistics.mean(x[0] for x in v):6.0f} {max(x[0] for x in v):5d} | '
              f'{max(ns or [0]):13d} | {statistics.mean(x[1] for x in v):14.0f} {max(x[1] for x in v):5d}')
    p3 = parts['P1'] + parts['P2'] + parts['A8']
    fight = p3 + parts['A13'] + [x for k, v in rows if k in FIGHT_ROWS for x in v]
    loc = {id(x): where(x[3], k) for k, v in rows for x in v}
    avg1, avg2 = statistics.mean(x[0] for x in p3), statistics.mean(x[0] for x in fight)
    nojob1, nojob2 = [x for x in p3 if not x[2]], [x for x in fight if not x[2]]
    jobs1, jobs2 = [x[0] for x in p3 if x[2]], [x[0] for x in fight if x[2]]
    top = sorted(nojob2, key=lambda x: -x[0])[:5]
    topj = sorted([x for x in fight if x[2]], key=lambda x: -x[0])[:3]
    print(f'  cost fight state (P1 + P2 + A8 + A13 + {" / ".join(FIGHT_ROWS)}): {len(fight)} ticks, avg {avg2:.0f} '
          f'(the kit {statistics.mean(x[1] for x in fight):.0f}), max {max(x[0] for x in fight)}; the intro / ending / event are the '
          f'intro and death states')
    print(f'  cost fight state without the arena job\'s slice ticks: {len(nojob2)} ticks, max {max(x[0] for x in nojob2)}; the '
          f'{len(jobs2)} slice ticks avg {statistics.mean(jobs2 or [0]):.0f} max {max(jobs2 or [0])}')
    print('  cost the highest ticks without a slice: ' + '; '.join(f'{x[0]} (kit {x[1]}) at {loc[id(x)]}' for x in top))
    print('  cost the highest slice ticks: ' + '; '.join(f'{x[0]} (kit {x[1]}) at {loc[id(x)]}' for x in topj))
    print('  cost after a pause / a /reload (max tick incl. the reload chain; look jobs started; slice ticks): '
          + '; '.join(f'{how} at {at}: {mx}, {[lk for _t, lk, _st in lj]}, {sl}' for (at, how), (lj, mx, sl) in after.items()))
    print(f'  cost CS0: the kit\'s prop chain ran on {len(anim_cs0)} of {len(seqc["intro"])} intro ticks')
    check(f'Z1 commands per fight tick (P1 + P2 + A8, the kit running): the average <= 830 (Apep) and <= 600 (target); every '
          f'tick <= {TICK_MAX} but the arena job\'s slice ticks, those <= {SLICE_MAX} (contract §5 gate 5)',
          avg1 <= 600 and max(x[0] for x in nojob1) <= TICK_MAX and max(jobs1 or [0]) <= SLICE_MAX,
          (avg1, max(x[0] for x in nojob1), max(jobs1 or [0])))
    check(f'Z2 I1 / V2 (HR-50): every fight-state tick incl. A13, the fail branches, the fight-state sequences, the down window, '
          f'the pauses and the reloads (the kit running): the average <= 600 (target; Apep ~830 hard), every tick (and each '
          f'/reload chain) <= {TICK_MAX} but the arena job\'s slice ticks (I1b), those <= {SLICE_MAX}',
          avg2 <= 600 and max(x[0] for x in nojob2) <= TICK_MAX and max(jobs2 or [0]) <= SLICE_MAX,
          (avg2, [(x[0], loc[id(x)]) for x in top[:3]], max(jobs2 or [0])))
    # the kit really ran: P1's ambience (core/amb, every 10 t) puts kit commands in every 10-tick window of P1, and the card
    # ager it schedules runs between the calls (kit commands on most P1 ticks, not only on the call ticks)
    p1k = [x[1] for x in parts['P1']]
    win = [sum(p1k[i:i + 10]) for i in range(0, len(p1k) - 9, 10)]
    check('Z3 I1b round 1: the kit is counted (it runs for real in these worlds): kit commands in every 10-tick window of P1 '
          '(the ambience every 10 t) and on most P1 ticks (the card ager between the calls)',
          win and min(win) > 0 and sum(1 for k in p1k if k) >= len(p1k) * 0.8, (min(win or [0]), sum(1 for k in p1k if k), len(p1k)))
    # V2 (HR-51, D6-02): no arena look job starts on an arena that already stands in that look (the stamp) in any of these
    # worlds — after a pause / a /reload right after A8's judge (the judge's own crimson job runs on through them and stamps)
    # and a /reload in P2 / the down window, crimson was asked for again on the crimson arena and rewrote it (4 slices; at the
    # resume after the judge the fight's heaviest tick)
    dup = [x for x in looks if x[2] == look_stamp(x[1])]
    check(f'Z4 V2 (HR-51): no look job on an arena already in that look ({len(looks)} jobs started in the cost worlds; none '
          f'after the pauses / reloads, the arena crimson)', looks and not dup and not any(v[0] for v in after.values()),
          (dup[:4], {k: [lk for _t, lk, _s in v[0]] for k, v in after.items()}))
    # V2 (HR-50): the gate reaches every fight state it now lists
    a8f = phase_list([x[3] for x in parts['A8 fail']])
    a13f = phase_list([x[3] for x in parts['A13 fail']])
    rev = any(a13f[j:j + 3] == [PH['a13'], PH['lead'], PH['a13']] for j in range(len(a13f)))
    cov = dict(down_by_timer=down24, lead_down=len(seqc.get('lead_down', [])), floor_hit=bool(hit),
               a8_fail=a8f, a13_fail=a13f, deaths=deaths13, reached=[r for r in reached if not r[2]])
    check(f'Z5 V2 (HR-50): the cost runs reach every fight state they list — the down window by its timer with the kipup '
          f'({API.DOWN_T} + {KIPUP} t), a 5 % floor hit in it -> lead_down ({API.SEQ_LEN["lead_down"]} t), the A8 fail -> P2 '
          f'(no CS2), the A13 instant death -> the revive -> lead_stand -> A13 again, a pause and a /reload right after A8\'s '
          f'judge / in P2 / in the down window',
          down24 >= API.DOWN_T + KIPUP and abs(len(seqc.get('lead_down', [])) - API.SEQ_LEN['lead_down']) <= 1 and hit
          and any(a8f[j:j + 2] == [PH['a8'], PH['p2']] for j in range(len(a8f))) and PH['cs2'] not in a8f and deaths13 >= 1
          and rev and all(r[2] for r in reached),
          cov)
    # V2 (HR-52, D6-03): through CS0 the kit's per-tick prop chain no longer runs for the seat stone's motionless bottle / cup
    # (e/anim ~39 commands on every CS0 tick before); the stone and its items are gone at the intro's end
    check(f'Z6 V2 (HR-52): the kit\'s per-tick prop chain (fx/e/anim) runs on no CS0 tick ({len(anim_cs0)} of '
          f'{len(seqc["intro"])}); the seat stone and its items gone at the intro\'s end', not anim_cs0 and not seat_left,
          (anim_cs0[:5], seat_left))
    VARS['cost_rows'] = [(k, len(v), statistics.mean(x[0] for x in v), max(x[0] for x in v)) for k, v in rows]


# ================================================================================================= F1 (11-05 review fixes)
J8, J13 = API.JUDGE_T['a8'], API.JUDGE_T['a13']


def leave(s, n):
    """The player leaves for n ticks (no tagged player: the framework pause, as a disconnect), then comes back."""
    pl = s.player()
    pl.tags.discard('player')
    s.setsc('#riftOn', 'room', 0)                 # sim only: the rift's own tick needs a tagged player
    out = run(s, n, heal=False)
    pl.tags.add('player')
    s.setsc('#riftOn', 'room', 1)
    return out


def interrupt(s, how, n=10):
    if how == 'pause':
        return pause_for(s, n)
    if how == 'leave':
        return leave(s, n)
    reload(s)
    return [rec(s)]


def watch(s, *fns):
    s.watch.update({f'rlk:boss/scarlet/{f}': [] for f in fns})


def watched(s, f):
    return [t for t, *_r in s.watch.get(f'rlk:boss/scarlet/{f}', [])]


def sec_f1():
    """F1 (the 11-05 review fixes, the lead's decisions in HR/review/findings.md): HR-01 the judged A8 fail survives a pause /
    reload (P2 at once); HR-07 a lethal gauntlet past its last counting cut with pips left: the fail is pending and lands at
    the resume / reload (the revive path), before it the restart stays; HR-06 test 30 / 35 only in P1 / P2, a test's forced
    fail ends with its judge; HR-04 no counter / A6 between the floor hit and the reserved step; HR-13 never two empty picks in
    a row (the backstep + the mid pick); HR-25 the move clip after a flinch; HR-26 the counter / rear rules only in the near
    band; HR-38 A6's P2 cooldown 400."""
    # HR-01: the A8 fail (test 21, no dash: 5 pips -> #gres 2 at the judge), interrupted between the judge and T + 214
    for how, at in (('pause', J8 + 1), ('pause', J8 + 12), ('reload', J8 + 6), ('leave', J8 + 18)):
        s, pl = world(300 + at)
        H.place_player(s, API.CX + 0.5, API.CZ + 6.0)
        test(s, 21)
        ok, R = until(s, lambda s: hr(s, '#ph') == PH['a8'] and hr(s, '#pt') >= at, 400)
        g0 = hr(s, '#gres')
        R1 = interrupt(s, how)
        R2 = run(s, 160)
        a8s = [r for r in R2 if r['pat'] == TID['a8']]
        check(f'F1 HR-01 the judged A8 fail (#gres {g0}), a {how} at T+{at}: P2 at once (no lead_stand, no second A8)',
              ok and g0 == 2 and R2[0]['ph'] == PH['p2'] and PH['lead'] not in [r['ph'] for r in R2] and not a8s,
              (g0, phase_list(R1 + R2)[:6]))
    # HR-07: A13 (test 27, no dash: 5 pips) after U10's pip window (strike + 1): the fatal at the resume / reload; Ronova's
    # revive -> the stance -> lead_stand -> A13 again with 5/5
    last13 = max(CUTS['a13'])
    for how, at in (('pause', last13 + 6), ('reload', last13 + 12), ('leave', J13 - 1)):
        s, pl = world(320 + at)
        s.revive = 40
        H.place_player(s, API.CX + 0.5, API.CZ + 6.0)
        test(s, 27)
        ok, R = until(s, lambda s: hr(s, '#ph') == PH['a13'] and hr(s, '#pt') >= at, 500)
        pips, d0 = hr(s, '#pips'), len(s.deaths)
        R1 = interrupt(s, how)
        R2 = run(s, 2, heal=False)
        died = len(s.deaths) > d0
        check(f'F2 HR-07 A13 with {pips} pips past its last counting cut (strike {last13}), a {how} at T+{at}: the instant death lands '
              'at once (no restart of A13)', ok and pips >= 1 and died and not any(r['ph'] == PH['lead'] and r['rvw'] == 0 for r in R2),
              (pips, s.deaths[d0:], phase_list(R1 + R2)))
        ok2, R3 = until(s, lambda s: hr(s, '#ph') == PH['a13'] and hr(s, '#pat') == TID['a13'] and 1 <= hr(s, '#pt') <= 2, 700)
        stance = any(r['rvw'] >= 1 for r in R3)
        check(f'F3 HR-07 ... ({how}) then Ronova\'s revive: the stance, lead_stand, A13 from T0 with 5/5', ok2 and stance
              and hr(s, '#pips') == API.PIPS, (ok2, stance, hr(s, '#pips')))
    # ... a /reload while the player is away keeps the fail pending; it lands when they come back
    s, pl = world(330)
    s.revive = 40
    H.place_player(s, API.CX + 0.5, API.CZ + 6.0)
    test(s, 27)
    ok, R = until(s, lambda s: hr(s, '#ph') == PH['a13'] and hr(s, '#pt') >= last13 + 4, 500)
    d0 = len(s.deaths)
    pl.tags.discard('player')
    s.setsc('#riftOn', 'room', 0)
    run(s, 3, heal=False)
    reload(s)
    R1 = run(s, 10, heal=False)
    away = len(s.deaths) == d0 and hr(s, '#grs') == 5
    pl.tags.add('player')
    s.setsc('#riftOn', 'room', 1)
    run(s, 2, heal=False)
    check('F4 HR-07 a /reload while the player is away: the fail stays pending (#grs 5, no death), it lands when they are back',
          ok and away and len(s.deaths) > d0, (away, s.deaths[d0:], hr(s, '#grs')))
    # before the last counting cut the restart rule (PLAN §3.8 / §5.6) stays
    s, pl = world(331)
    H.place_player(s, API.CX + 0.5, API.CZ + 6.0)
    test(s, 27)
    ok, R = until(s, lambda s: hr(s, '#ph') == PH['a13'] and hr(s, '#pt') >= last13 - 8, 500)
    d0 = len(s.deaths)
    pause_for(s, 10)
    R2 = run(s, 3)
    check(f'F5 HR-07 a pause before the last counting cut (T+{last13 - 8}): no death, lead_stand {{g:"a13"}} -> A13 from T0 (the restart)',
          ok and len(s.deaths) == d0 and R2[-1]['ph'] == PH['lead'] and hr(s, '#sqn') == SEQ['lead_stand'], phase_list(R2))
    # HR-06: test 30 / 35 refuse outside P1 / P2
    for tid in (30, 35):
        s, pl = at_phase(340 + tid, 20, lambda s: hr(s, '#ph') == PH['cs1'] and hr(s, '#sq') >= 40)
        sq0 = hr(s, '#sq')
        test(s, tid)
        run(s, 5)
        check(f'F6 HR-06 test {tid} in CS1: refused (CS1 goes on, no replay)', hr(s, '#rp') == 0 and hr(s, '#ph') == PH['cs1']
              and hr(s, '#sqn') == SEQ['cs1'] and hr(s, '#sq') == sq0 + 5, (hr(s, '#rp'), hr(s, '#ph'), hr(s, '#sq'), sq0))
    s, pl = at_phase(350, 21, lambda s: hr(s, '#ph') == PH['a8'] and hr(s, '#pt') >= 30)
    pt0 = hr(s, '#pt')
    test(s, 30)
    run(s, 5)
    check('F7 HR-06 test 30 in A8: refused (the gauntlet goes on)', hr(s, '#pat') == TID['a8'] and hr(s, '#pt') == pt0 + 5
          and hr(s, '#rp') == 0, (hr(s, '#pat'), hr(s, '#pt'), pt0))
    s, pl = world(351)
    test(s, 30)
    run(s, 3)
    check('F8 HR-06 test 30 in P1: the intro replay runs (#rp 1)', hr(s, '#rp') == 1 and hr(s, '#ph') == PH['p1'], hr(s, '#rp'))
    s, pl = at_phase(352, 23, lambda s: hr(s, '#ph') == PH['a8'] and hr(s, '#pt') >= 60)
    pause_for(s, 10)
    ok, R = until(s, lambda s: hr(s, '#ph') == PH['a8'] and hr(s, '#pt') >= 1, 200)
    ok2, R2 = until(s, lambda s: hr(s, '#gres') != 0 or hr(s, '#ph') != PH['a8'], 260, each=dasher(CUTS['a8']))
    check('F9 HR-06 test 23 (a forced fail) + a pause: the restarted A8 counts timed dashes again (0 pips -> the deflect)',
          ok and ok2 and hr(s, '#gres') == 1, (ok, ok2, hr(s, '#gres'), hr(s, '#pips'), hr(s, '#pipoff')))
    # HR-04: 3 small hits, then the hit reaching the floor (a basic / a skill hit), all within 40 t while she recovers in front of
    # the player: no counter / A6 before the reserved step (CS1 in P1, the A13 lead-in in P2)
    for phase, skill in (('p1', False), ('p1', True), ('p2', False), ('p2', True)):
        moves = []
        for i in range(8):
            s, pl = world(360 + i + (20 if phase == 'p2' else 0) + (40 if skill else 0))
            H.hold(s, True)
            if phase == 'p2':
                test(s, 33)
                H.hold(s, True)
            run(s, 3)
            H.hold(s, False)
            H.place_body(s, API.CX, API.CZ, yaw=0.0)
            H.place_player(s, API.CX, API.CZ + 2.8)
            b = body(s)
            s.setsc(('e', b.id), 'mhpC', (FL60 if phase == 'p1' else FL5) + 40)
            s.setsc('#pat', 'hr', 0)
            s.setsc('#rec', 'hr', 30)
            s.setsc('#ai_pht', 'hr', 400)
            for _ in range(3):
                strike(s, 5)
                run(s, 2)
            strike(s, skill=skill)
            ok, R = until(s, lambda s: hr(s, '#ph') in (PH['cs1'], PH['lead']), 120)
            moves.append([S3.KEY_OF.get(p) for p in sorted({r['pat'] for r in R if r['pat']})] if ok else ['no step'])
        bad = [m for m in moves if m]
        check(f'F10 HR-04 {phase.upper()}: a 4-hit flurry ending on the floor hit ({"a skill" if skill else "a basic"} hit), 8 seeds: '
              f'{"CS1" if phase == "p1" else "the A13 lead-in"} at the next decision, no counter / A6 before it', not bad, moves)
    # HR-13: never two empty picks in a row - a passive player near her for 1600 t (no hits): no two ai/none extensions without a
    # pattern or a backstep between
    s, pl = world(370)
    H.place_player(s, API.CX + 0.5, API.CZ + 3.0)
    watch(s, 'ai/none', 'ai/backstep', *[f'core/start/{k}' for k in API.P1])
    run(s, 1600, each=lambda s: H.place_player(s, API.CX + 0.5, API.CZ + 3.0))
    ev = sorted([(t, 'N') for t in watched(s, 'ai/none')] + [(t, 'B') for t in watched(s, 'ai/backstep')]
                + [(t, 'S') for k in API.P1 for t in watched(s, f'core/start/{k}')])
    ext = [e for i, e in enumerate(ev) if e[1] == 'N' and not (i + 1 < len(ev) and ev[i + 1] == (e[0], 'B'))]
    seq_ = [k for t, k in ev if not (k == 'N' and (t, 'B') in ev)]
    twice = [i for i, (a, b) in enumerate(zip(seq_, seq_[1:])) if a == b == 'N']
    starts = sum(1 for _t, k in ev if k == 'S')
    check(f'F11 HR-13 a passive player near her, 1600 t: never two empty picks in a row ({len(ext)} ai/none extensions, {starts} '
          'pattern starts)', not twice and starts >= 15, (len(twice), seq_[:30]))
    # ... forced: every near candidate cooling down -> ai/none (8 t), then the backstep (she steps away to >= 5 b), then the
    # mid pick (A4, the one ready)
    s, pl = world(371)
    H.hold(s, False)
    H.place_body(s, API.CX, API.CZ, yaw=0.0)
    H.place_player(s, API.CX, API.CZ + 3.0)
    clk = hr(s, '#clk')
    for k in API.COOLDOWN:
        s.setsc(f'#cd_{k}', 'hr', clk + (-10 if k == 'a4' else 900))
    s.setsc('#last', 'hr', 0)
    s.setsc('#pat', 'hr', 0)
    s.setsc('#rec', 'hr', 1)
    s.setsc('#ai_nn', 'hr', 0)
    watch(s, 'ai/none', 'ai/backstep', *[f'core/start/{k}' for k in API.P1])
    t0 = s.t
    ok, R = until(s, lambda s: hr(s, '#pat') != 0, 80, each=lambda s: H.place_player(s, API.CX, API.CZ + 3.0))
    bk = watched(s, 'ai/backstep')
    d = math.hypot(body(s).pos[0] - API.CX, body(s).pos[2] - (API.CZ + 3.0))
    played = [c for t, c in s.rigl if t > t0 and c == 'play/backstep']
    check('F12 HR-13 the near band empty twice in a row: the backstep clip (she steps to >= 5 b), then the mid pick (A4)',
          ok and S3.KEY_OF.get(hr(s, '#pat')) == 'a4' and len(bk) == 1 and played and d >= 4.9,
          (S3.KEY_OF.get(hr(s, '#pat')), watched(s, 'ai/none'), bk, played[:1], round(d, 2)))
    # HR-25: after a flinch the recovery's move clip plays again
    s, pl = world(372)
    H.hold(s, False)
    H.place_body(s, API.CX, API.CZ, yaw=0.0)
    H.place_player(s, API.CX, API.CZ + 3.0)
    s.setsc('#pat', 'hr', 0)
    H.call_sc(s, 'ai/rec_start')
    s.setsc('#rec', 'hr', 40)
    s.setsc('#flq', 'hr', 1)
    n0 = len(s.rigl)
    run(s, 12, each=lambda s: H.place_player(s, API.CX, API.CZ + 3.0))
    plays = [(t, c) for t, c in s.rigl[n0:] if c.startswith('play/')]
    fl = [t for t, c in plays if c == 'play/flinch']
    after = [c for t, c in plays if fl and t > fl[0]]
    check('F13 HR-25 a flinch in the recovery: the move clip (walk / strafe) plays again when it ends', fl and after
          and after[0] in ('play/walk', 'play/strafe_l', 'play/strafe_r', 'play/glide'), plays)
    # ... and (F1 round 1, VF1-01 / VF1R-02) during the far fallback's approach glide (ai/approach, #ai_mv 4: the player
    # 14 b away, A3 forced next), P1 and P2: the glide clip plays again when the flinch ends and she glides on toward them
    for ph in (PH['p1'], PH['p2']):
        s, pl = world(373 + ph)
        H.hold(s, False)
        s.setsc('#ph', 'hr', ph)
        H.place_body(s, API.CX, API.CZ, yaw=0.0)
        H.place_player(s, API.CX, API.CZ + 14.0)
        s.setsc('#pat', 'hr', 0)
        s.setsc('#ai_nx', 'hr', TID['a3'])
        H.call_sc(s, 'ai/rec_start')
        mv = hr(s, '#ai_mv')
        s.setsc('#flq', 'hr', 1)
        n0 = len(s.rigl)
        zs = []
        def keep(s):
            H.place_player(s, API.CX, API.CZ + 14.0)
        for _ in range(14):
            run(s, 1, each=keep)
            zs.append(body(s).pos[2] - API.CZ)
        plays = [(t, c) for t, c in s.rigl[n0:] if c.startswith('play/')]
        fl = [t for t, c in plays if c == 'play/flinch']
        after = [c for t, c in plays if fl and t > fl[0]]
        check(f'F13b HR-25 a flinch during the far fallback\'s approach glide (#ai_mv 4, {"P1" if ph == PH["p1"] else "P2"}): the glide '
              'clip plays again when it ends and she glides on (>= 1 b over the last 5 t)',
              mv == 4 and fl and after[:1] == ['play/glide'] and zs[-1] - zs[-6] >= 1.0,
              (mv, plays, [round(z, 2) for z in zs]))
    # HR-26: the counter / rear rules only inside the near band
    def ctr(dist):
        def f(s):
            H.hold(s, False)
            H.place_body(s, API.CX, API.CZ, yaw=0.0)
            H.place_player(s, API.CX, API.CZ + dist)
            s.setsc('#rec', 'hr', 40)
            s.setsc('#pat', 'hr', 0)
            for _ in range(API.COUNTER_TRIGGER['hits']):
                strike(s, 5)
        return f
    far = [ai_trial(380 + i, ctr(10.0), ticks=2)[1] for i in range(30)]
    near = [ai_trial(420 + i, ctr(3.0), ticks=2)[1] for i in range(30)]
    check('F14 HR-26 4 hits in 40 t from 10 b (ranged): never A1 / A2', not [k for k in far if k in ('a1', 'a2')], far)
    check('F15 HR-26 ... from 3 b: the counter as before (seeded share)', 0.5 <= sum(k in ('a1', 'a2') for k in near) / 30 <= 0.9, near)

    def rear10(s):
        H.hold(s, False)
        H.place_body(s, API.CX, API.CZ, yaw=0.0)
        H.place_player(s, API.CX, API.CZ - 10.0)
        s.setsc('#rear', 'hr', 0b111111)
        s.setsc('#rec', 'hr', 1)
        s.setsc('#last', 'hr', 0)
        s.setsc('#ai_rcd', 'hr', hr(s, '#clk') - API.REAR_RULE['cd_ignore_every'])
    ks = [ai_trial(460 + i, rear10, ticks=3)[1] for i in range(10)]
    check('F16 HR-26 the rear rule with the player 10 b behind her: no A1 (the band pick decides)', not [k for k in ks if k == 'a1'], ks)
    # HR-38: A6's P2 cooldown 400 (PLAN §4.8: at most one back-blink per 20 s)
    st = cmds('core/start/a6')
    cd2 = [ln for ln in st if f'#ph hr matches {PH["p2"]}' in ln and '#a6cd hr' in ln and 'add' in ln]
    check('F17 HR-38 A6 in P2 sets its cooldown to 400 t (core/start/a6)', len(cd2) == 1 and cd2[0].endswith(' 400'), cd2)
    blinks = []
    for i in range(20):
        s, pl = world(480 + i)
        test(s, 33)
        H.hold(s, True)
        run(s, 2)
        H.place_body(s, API.CX, API.CZ, yaw=0.0)
        H.place_player(s, API.CX, API.CZ + 3.0)
        H.call_sc(s, 'core/start/a6')
        ok, R = until(s, lambda s: hr(s, '#pat') == 0, 40)
        s.setsc('#clk', 'hr', hr(s, '#clk') + 360)      # 19 s later: a skill hit within 4.5 b while she recovers
        s.setsc('#ai_pht', 'hr', 1000)
        s.setsc('#pat', 'hr', 0)
        s.setsc('#rec', 'hr', 40)
        b = body(s)
        H.place_player(s, b.pos[0], b.pos[2] + 3.0)
        H.hold(s, False)
        strike(s, 5, skill=True)
        run(s, 2)
        blinks.append(hr(s, '#pat') == TID['a6'])
    check('F18 HR-38 P2: a skill hit 19 s after a back-blink never starts another (20 seeds)', not any(blinks), blinks)
    # F1 round 1, VF1-05 (HR-01 / HR-07's comments): the pause / resume hook headers name what a paused gauntlet leaves besides
    # the restart: the judged A8 fail -> P2 at once (#grs 4) and a lethal gauntlet's pending fail (#grs 5, core/g/fail_now)
    hd = {n: ' '.join(ln for ln in (fn_lines(n) or []) if ln.startswith('#')) for n in ('pause', 'resume')}
    miss = [(n, w) for n in hd for w in ('judged A8 fail', 'core/g/fail_now') if w not in hd[n]]
    miss += [(n, w) for n, w in (('pause', '#grs 4'), ('pause', '#grs 5'), ('resume', '(4)'), ('resume', '(5,')) if w not in hd[n]]
    check('F19 HR-01 / HR-07 (VF1-05): the pause / resume hook headers name #grs 4 (the judged A8 fail -> P2 at once) and #grs 5 '
          '(the pending lethal fail, core/g/fail_now)', not miss, miss)


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
