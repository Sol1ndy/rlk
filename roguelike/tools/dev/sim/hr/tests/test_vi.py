#!/usr/bin/env python3
"""test_vi.py: round V, the three lanes TOGETHER (the integration, 11-12; tools/dev/plan/combat/vi_progress.md).

    python3 test_vi.py <roguelike> [section ...]        (run from a copy of tools/dev/sim outside the datapack)

Lane VP's beat (the perfect parry freeze / the perfect dodge slow motion) meets lane VB's fight (the wind-ups, the drawn blade
path, the slash from the blade track, the cue / flashes of the kit) and lane VC's locked sequences (the display camera, the
skip on Space, the actor). Each lane's own suite proves its part alone; this one proves the seams.

  beatpat   every 홍련 pattern type (P1 and P2 lists: singles, chains, leaps, dashes, the ultimate, the grab + its air part)
            and both gauntlets in the H1 world (the real core, F path and judge; tests/lib/hrsim.py) with the REAL effect kit,
            answered perfectly (F one tick before each parryable hit; a second run also perfect-dodges the unparriable ones),
            once with the beat's world hold off (#btOn tmp 0) and once on. The beat-on run must be the beat-off run, world tick
            by world tick: the pattern clock, her body, the rig calls (her clip), the sweep cards (the drawn path, its head, the
            slash pieces: rlk_hr_sw), the kit's calls and its live cards with their remaining life (the cue star, the flashes:
            on the beat's clock since the integration), the hazards and the judged hits. On a held tick nothing of hers moves
            or ages. Every path head disappears on a tick a hit of the pattern lands (in world ticks, beat on). The gauntlets'
            judge counts as before (#gau, #gres and the judged strikes).
  follow    her MODEL stands at her body after every instant move of the fight (the gauntlets' reappearances, a cancelled
            leap, the revive's placing): the rig's follow as seqsim models it, run in the fight.
  beatseq   the whole chain with the real core, the real sequences and their lock (test_flow's world) and the beat ON: a
            perfect parry / a perfect dodge beat that is running when a locked sequence starts (the 60 % floor -> CS1, the
            cleared gauntlet -> the repel, the 5 % floor -> lead5) and a sequence that starts inside the dodge's slow motion:
            one real tick later nothing is held (#btK / #btHold / #btInv 0, no NoAI left by the beat, no beat tag), the lock
            holds the player from the sequence's first tick with the client on the live camera, the sequence runs its full
            length and hands back clean.
  swap      the avatar, lane VP's stand-in rig and lane VC's actor (the real char/cine/**, char/motion/beat/**, char/motion/
            lite/** and player/def/beat/{post,end}) for the four mannequin characters (루미네, 클로린드, 로노바, 네페르) and
            the three rig characters, a lock starting at every age of a parry and of a dodge beat, in rlk:tick's order: at the
            end of every tick exactly one body is visible (the avatar or its stand-in rig or its own rig before the lock; the
            actor alone during it; the avatar / its rig after it), the hidden avatar is blank, and after the hand-back the
            avatar is back as it was (skin, hand, no glow left, no stand-in part left).
  skip      the Space skip of CS0 and CS1 while a beat runs and while other inputs are held (F, Shift, a movement key, Space
            held since before the window): the skip fires on the same sequence tick and lands in the same state as the plain
            skip (test_seq's K1 state), the beat is over one tick after it started, the client stays on the live camera.
Prints one line per check; exit 1 on any failure.
"""
import math
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / 'lib'))
sys.path.insert(0, str(HERE.parent / 'h2'))
import pat_lib as P  # noqa: E402
from pat_lib import H  # noqa: E402
import camsim as CS  # noqa: E402
import seqsim as Q  # noqa: E402
import mcsim  # noqa: E402
from mcsim import Ctx, split  # noqa: E402

ARGS = [a for a in sys.argv[1:] if not a.startswith('-')]
DP = Path(ARGS[0]).resolve()
SECT = ARGS[1:]
FN = DP / 'data/rlk/function'
C0 = H.C0
api, S3 = P.load_api(DP)
from mboss_scarlet import blade as B  # noqa: E402
OBJ = api.OBJ
FAILS, NCK = [], [0]


def ck(name, ok, info=''):
    NCK[0] += 1
    print(('ok   ' if ok else 'FAIL ') + name + ('' if ok or info == '' else f'  -- {str(info)[:900]}'), flush=True)
    if not ok:
        FAILS.append(name)
    return ok


def want(name):
    return not SECT or name in SECT


def fn_lines(rel):
    p = FN / (rel + '.mcfunction')
    return [l for l in p.read_text(encoding='utf-8').split('\n') if l.strip() and not l.startswith('#')] if p.exists() else []


TICK = fn_lines('tick')
CLOCK = next(l for l in TICK if 'player/def/beat/clock' in l)
POST = next(l for l in TICK if 'player/def/beat/post' in l)
MAINL = next(l for l in TICK if 'function rlk:mboss/main' in l)
# presentation the simulator has no use for (particles, glyph titles, the avatar's clips): the beat's ENGINE stays real
STUB_FX = ('rlk:player/def/guard', 'rlk:items/hook/on_parry_press', 'rlk:items/hook/on_parry', 'rlk:items/hook/on_pdodge',
           'rlk:items/hook/on_dash', 'rlk:char/motion/dash', 'rlk:char/motion/finish', 'rlk:player/dash_dir',
           'rlk:player/def/fx/p1', 'rlk:player/def/fx/p2', 'rlk:player/def/fx/p3_at', 'rlk:player/def/fx/p3_star',
           'rlk:player/def/fx/p3_shatter', 'rlk:player/def/fx/p3_bolt', 'rlk:player/def/fx/pd_at', 'rlk:player/def/fx/pd_body',
           'rlk:player/def/fx/pd_ember', 'rlk:player/def/fx/pd_chime', 'rlk:player/def/fx/ovl', 'rlk:player/def/beat/act',
           'rlk:player/def/beat/rock_on', 'rlk:player/def/beat/rock_off', 'rlk:player/def/beat/st/pass',
           'rlk:player/def/beat/st/off', 'rlk:player/def/beat/st/tp_on', 'rlk:player/def/beat/st/tp_off')
STUB_AV = ('rlk:char/motion/beat/parry', 'rlk:char/motion/beat/dodge0', 'rlk:char/motion/beat/dodge', 'rlk:char/motion/beat/off',
           'rlk:char/motion/beat/wglow_off', 'rlk:char/motion/beat/tint_off', 'rlk:char/motion/lite/tick')
SKIP_SC = {'#plG', '#pxG', '#mbPlG'}      # raw game-time caches of the framework (same-tick tests only)
BEAT_TAGS = ('rlk_bt_noai', 'rlk_bt_tp', 'rlk_bt_st', 'rlk_bt_rk', 'rlk_bt_atk', 'rlk_bt_pt')


class BeatClock:
    """The game time of a world whose s.t is the WORLD tick (= the beat's clock): the real tick = s.t + the ticks the beat has
    held (+ 1 in the scheduled phase, + 1 while rlk:tick's head runs before the tick is counted). Scheduled functions are
    kept in real time, so the effect kit's ager runs on held ticks too, as in the game."""
    held = 0
    pre = 0

    def real(self):
        return self.t + self.gt_off + self.held + self.pre

    def cmd(self, t, ctx):
        if t[:3] == ['time', 'query', 'gametime']:
            return self.real()
        if t[0] == 'schedule' and len(t) > 3 and t[1] == 'function':
            self.sched[t[2]] = self.real() + int(t[3].rstrip('t'))
            return 1
        return super().cmd(t, ctx)

    def run_sched_at(self, now):
        super().run_sched_at(now + self.held)


def beat_reset(s, on, stubs):
    for f in stubs:
        s.cache[f] = []
    pl = s.player()
    for o in ('dead', 'rnDie', 'pkMode', 'vMap', 'rdCam', 'devMode', 'plActive'):
        if s.sc(('e', pl.id), o) is None:
            s.setsc(('e', pl.id), o, 0)
    s.setsc('#3', 'tmp', 3)
    s.call('rlk:player/def/beat/reset', C0)
    s.setsc('#btOn', 'tmp', on)


def bt(s, k):
    return s.sc(k, 'cb') or 0


def beat_left(s):
    """What a beat may leave behind: {} when nothing is held."""
    out = {k: bt(s, k) for k in ('#btK', '#btHold', '#btInv', '#btHeld', '#btRk', '#btSt', '#btTp') if bt(s, k)}
    tg = sorted({t for e in s.ents if e.alive for t in e.tags if t in BEAT_TAGS})
    if tg:
        out['tags'] = tg
    if bt(s, '#btAdj') != bt(s, '#btLag'):
        out['adj'] = (bt(s, '#btAdj'), bt(s, '#btLag'))
    return out


# ============================================================================================================ beatpat
class PatSim(BeatClock, H.H1Sim):
    pass


def cards(s, tag):
    return [e for e in s.ents if e.alive and tag in e.tags]


def sw_state(s):
    """The sweep cards of blade.py as the world holds them: (own tags, place, yaw) of each."""
    return tuple(sorted((tuple(sorted(t for t in e.tags if t.startswith('rlk_hr_sw'))), tuple(round(v, 3) for v in e.pos),
                         round(e.rot[0] % 360, 2)) for e in cards(s, B.TAG)))


def kit_state(s):
    """The kit's live cards with the life each has left on the kit's own clock (#now hrFx of the last ager pass)."""
    now = s.sc('#now', 'hrFx') or 0
    return tuple(sorted((tuple(sorted(e.tags)), tuple(round(v, 2) for v in e.pos), (s.sc(('e', e.id), 'hrFxD') or 0) - now)
                        for e in cards(s, 'rlk_hr_fx')))


def pat_world(key, on, policy, ph):
    s, pl = H.setup_sc(DP, seed=9, lv=15, hp=5834, player_level=15, cls=PatSim)
    s.cache['rlk:mob/setup'] = ['tag @s add rlk_mob', 'function rlk:bal/init']
    s.call('rlk:bal/load', C0)
    H.kit_on(s)
    beat_reset(s, on, STUB_FX + STUB_AV)
    assert H.fight_sc(s)
    if ph == 2 and key not in api.GAUNTLETS:
        H.test_id(s, 33)
        H.run_h1(s, 2)
    H.heal(s)
    H.facing_setup(s, 3.0 if key not in api.GAUNTLETS else 6.0)
    tid = S3.TID[key]
    if key in api.GAUNTLETS:
        H.test_id(s, tid)
    else:
        H.start_pattern(s, tid)
    t0 = s.t
    rows, st = {}, dict(real=0, held=0, froze=[], heads={}, hits=set())
    j0, h0, k0, r0 = len(s.judged), len(s.hzr), len(s.kitl), len(s.rigl)
    lag0 = bt(s, '#btLag')
    seen = False
    limit = (api.JUDGE_T[key] + 40) if key in api.GAUNTLETS else 300
    if key in api.GAUNTLETS:
        st['hits'].add(api.JUDGE_T[key])                   # the dive's judge (the core's own tick, no hazard marker)
    pid = ('e', pl.id)
    while s.t - t0 < limit and st['real'] < 4000:
        pat = H.hr(s, '#pat') or 0
        if key not in api.GAUNTLETS:
            want_tid = S3.TID['ult'] if key == 'ult' else tid          # test 12 = rings, the ult follows
            if pat == want_tid or (key == 'ult' and pat == S3.TID['rings']):
                seen = True
            elif seen and pat == 0:
                break
        # the perfect answer: one tick before a hit (the hazard's tell ends on the next world tick)
        for h in s.select('@e[type=minecraft:marker,tag=rlk_mb_hz]', C0):
            g = lambda o, h=h: s.sc(('e', h.id), o) or 0  # noqa: E731
            if g('mbHzD') >= 1 and g('mbHzHit') == 0 and g('mbHzW') - g('mbHzT') == 1:
                st['hits'].add(s.t + 1 - t0)
                if g('mbHzNP') == 0:
                    s.press(at=s.t + 1)
                elif policy == 'mix' and g('mbHzND') == 0:
                    s.dodge(at=s.t + 1)
        H.heal(s)
        s.pre = 1
        s.cmd(split(CLOCK), C0)
        s.pre = 0
        st['real'] += 1
        if bt(s, '#btHold') == 1:
            before = (sw_state(s), kit_state(s), tuple(H.body_of(s).pos), H.hr(s, '#pt'), len(s.rigl), len(s.kitl))
            st['held'] += 1
            s.held += 1
            s.cmd(split(MAINL), C0)
            s.gt_off = 1
            try:
                s.run_sched_at(s.t + 1)
            finally:
                s.gt_off = 0
            after = (sw_state(s), kit_state(s), tuple(H.body_of(s).pos), H.hr(s, '#pt'), len(s.rigl), len(s.kitl))
            if before != after:
                st['froze'].append((s.t - t0, [i for i, (x, y) in enumerate(zip(before, after)) if x != y]))
        else:
            heads0 = {e.id for e in cards(s, B.TAG_HEAD)} | {e.id for e in cards(s, B.TAG_LHEAD)}
            H.world_h1(s)
            b = H.body_of(s)
            wt = s.t - t0
            heads1 = {e.id for e in cards(s, B.TAG_HEAD)} | {e.id for e in cards(s, B.TAG_LHEAD)}
            for i in heads0 - heads1:
                st['heads'][i] = wt
            sc = tuple(sorted((k[0], v) for k, v in s.scores.items() if k[1] in ('mb', OBJ) and isinstance(k[0], str)
                              and k[0] not in SKIP_SC))
            rows[wt] = dict(sc=sc, body=(tuple(round(v, 3) for v in b.pos), round(b.rot[0], 2)) if b else None,
                            sw=sw_state(s), kit=kit_state(s), hp=(s.sc(pid, 'curHealth'), s.sc(('e', b.id), 'mhpC') if b else None))
        s.cmd(split(POST), C0)
    st['judged'] = [(j['t'] - t0, j['dodged'], j['parT'], j['pdg'], j['pat'], j['np']) for j in s.judged[j0:]]
    st['hz'] = [(h['t'] - t0, h['tell'], h['dmg'], h['kind'], h['pt'], tuple(round(v, 2) for v in h['pos'])) for h in s.hzr[h0:]]
    st['kitl'] = [(t - t0, c, tuple(sorted(a.items()))) for t, c, a in s.kitl[k0:]]
    st['rigl'] = [(t - t0, c) for t, c in s.rigl[r0:]]
    st['lag'] = bt(s, '#btLag') - lag0
    st['gau'], st['gres'] = H.hr(s, '#gau'), H.hr(s, '#gres')
    st['left'] = beat_left(s) if bt(s, '#btK') == 0 else {}
    st['nsw'] = max((len(r['sw']) for r in rows.values()), default=0)
    st['nkit'] = max((len(r['kit']) for r in rows.values()), default=0)
    return rows, st


def first_diff(a, b):
    for k in sorted(set(a) | set(b)):
        if a.get(k) != b.get(k):
            if k not in a or k not in b:
                return k, 'missing', k in a, k in b
            for f in ('sc', 'body', 'sw', 'kit', 'hp'):
                if a[k][f] != b[k][f]:
                    x, y = a[k][f], b[k][f]
                    if f in ('sc', 'sw', 'kit'):
                        return k, f, sorted(set(x) ^ set(y))[:4]
                    return k, f, x, y
    return None


def beatpat():
    keys = [(k, 1) for k in api.P1] + [(k, 2) for k in api.P2]
    only = [a[7:].split(',') for a in sys.argv[1:] if a.startswith('--keys=')]          # a development filter
    if only:
        keys = [k for k in keys if k[0] in only[0]]
    tot = dict(par=0, pd=0, held=0, runs=0)
    for key, ph in keys:
        pols = ('parry',) if key in api.GAUNTLETS else ('parry', 'mix')
        for pol in pols:
            if pol == 'mix' and all(r[6] == 'P' for r in api.HITS[key]):
                continue                                    # no unparriable hit: the mixed run is the parry run
            r0, s0 = pat_world(key, 0, pol, ph)
            r1, s1 = pat_world(key, 1, pol, ph)
            par = len([j for j in s1['judged'] if j[2] == 3])
            pd = len([j for j in s1['judged'] if j[3] == 1])
            tot['par'] += par
            tot['pd'] += pd
            tot['held'] += s1['held']
            tot['runs'] += 1
            lab = f'beatpat {key} P{ph} ({pol})'
            d = first_diff(r0, r1)
            ck(f'{lab}: beat on = beat off, world tick by world tick ({len(r1)} world ticks; the pattern clock and every `# hr` / '
               f'`# mb` score, her body, <= {s1["nsw"]} sweep cards, <= {s1["nkit"]} kit cards with their remaining life, both '
               f'health pools)', d is None and len(r0) == len(r1) and len(r1) >= 10, d)
            ck(f'{lab}: the same judged hits, hazards, kit calls and rig calls on the same world ticks '
               f'({len(s1["judged"])} judged: {par} perfect parries, {pd} perfect dodges; {len(s1["hz"])} hazards, '
               f'{len(s1["kitl"])} kit calls, {len(s1["rigl"])} rig calls)',
               all(s0[k] == s1[k] for k in ('judged', 'hz', 'kitl', 'rigl')),
               [k for k in ('judged', 'hz', 'kitl', 'rigl') if s0[k] != s1[k]])
            ck(f'{lab}: held {s1["held"]} real ticks = 5 x {par} + 7 x {pd} = #btLag (+{s1["lag"]}); on a held tick no sweep card, '
               f'no kit card, no rig call, no kit call, not her body, not #pt changes; nothing held at the end',
               s1['held'] == 5 * par + 7 * pd == s1['lag'] and s0['held'] == 0 and not s1['froze'] and not s1['left']
               and s1['real'] == len(r1) + s1['held'], (s1['held'], par, pd, s1['lag'], s1['froze'][:3], s1['left']))
            if s1['heads']:
                bad = {i: t for i, t in s1['heads'].items() if t not in s1['hits'] and t - 1 not in s1['hits']}
                ck(f'{lab}: each of the {len(s1["heads"])} path heads is gone on a world tick a hit lands (beat on), having '
                   f'run there on the pattern clock', not bad, (sorted(bad.values()), sorted(s1['hits'])))
            if key in api.GAUNTLETS:
                cuts = [c[2] for _t, _s, _cl, c in api.SCRIPTS[key] if c]
                ck(f'{lab}: the gauntlet judge counts as before: every one of the {len(cuts)} cuts a perfect parry, the shield '
                   f'gauge {s1["gau"]} and the result {s1["gres"]} as with the beat off',
                   par == len(cuts) and (s0['gau'], s0['gres']) == (s1['gau'], s1['gres']), (par, s0['gau'], s1['gau'], s0['gres'], s1['gres']))
    if only:
        return
    ck(f'beatpat: {tot["runs"]} pattern runs with the beat on held the world {tot["held"]} real ticks for {tot["par"]} perfect '
       f'parries and {tot["pd"]} perfect dodges (both kinds seen)', tot['par'] >= 20 and tot['pd'] >= 5, tot)
    # the kit really is on the beat's clock (the other six kits' form), the HUD mirrors of client title timers are not
    w = fn_lines('boss/scarlet/fx/e/world')
    mk = fn_lines('boss/scarlet/fx/e/make')
    lag = 'scoreboard players operation #now hrFx -= #btLag cb'
    ck('beatpat: fx/e/world holds on a held tick (its second command) and reads its clock minus #btLag; fx/e/make stamps on it',
       w[1] == 'execute if score #btHold cb matches 1 run return run schedule function rlk:boss/scarlet/fx/e/world 1t replace'
       and any(a.endswith('run time query gametime') and b == lag for a, b in zip(w, w[1:]))
       and any(a.endswith('run time query gametime') and b == lag for a, b in zip(mk, mk[1:])), w[:3])
    sw = [l for p in (FN / 'boss/scarlet/p').rglob('*.mcfunction') for l in p.read_text(encoding='utf-8').split('\n') if '"rlk_hr_sw"' in l and 'summon ' in l]
    ck(f'beatpat: every sweep card ({len(sw)} summon lines) is an item_display with teleport_duration 0 or 1 and no shadow: the '
       f'slow motion\'s stretch pass (beat/st/tp_on) takes the moving ones',
       len(sw) > 200 and all('minecraft:item_display' in l and 'shadow_radius:0f' in l and re.search(r'teleport_duration:[01],', l) for l in sw)
       and any('tag=rlk_hr_sw,' in l and 'beat/st/tp1' in l for l in fn_lines('player/def/beat/st/tp_on')))


# ============================================================================================================ follow
ROOT = 'rlk:boss/scarlet/'


class FollowSim(H.H1Sim):
    """H1Sim + where her model stands (seqsim.SeqSim.rig_follow's model of rig/follow: the parts go to the EXECUTION position of
    rig/tick when the body's place or yaw differs from the cached one; rig/follow_now always)."""
    rig_pos = None
    rig_cache = None

    def call(self, fid, ctx, macro=None):
        if fid in (ROOT + 'rig/tick', ROOT + 'rig/follow_now'):
            b = H.body_of(self)
            if b is not None:
                cur = (tuple(math.floor(v * 100) for v in b.pos), math.floor(b.rot[0] * 100))
                if fid.endswith('/follow_now') or cur != self.rig_cache:
                    self.rig_pos, self.rig_cache = tuple(ctx.pos), cur
        return super().call(fid, ctx, macro)


def follow():
    for kind, tid, n in (('G1 (a8), failed', 21, None), ('G2 (a13), failed + the revive\'s placing', 27, None),
                         ('the free P1 fight', None, 900), ('the free P2 fight', 33, 900)):
        s, pl = H.setup_sc(DP, seed=9, lv=15, hp=5834, player_level=15, cls=FollowSim)
        s.revive = 40
        assert H.fight_sc(s)
        H.facing_setup(s, 6.0)
        if tid:
            H.test_id(s, tid)
        t0 = s.t
        key = {S3.TID[g]: g for g in api.GAUNTLETS}.get(tid)
        end = t0 + (api.JUDGE_T[key] + 120 if key in api.JUDGE_T else n)
        worst, jumps, prev, off = 0.0, 0, None, []
        while s.t < end:
            if not (s.sc(('e', pl.id), 'rnDie') or 0):
                H.heal(s)
            H.world_h1(s)
            b = H.body_of(s)
            if b is None or s.rig_pos is None:
                continue
            d = math.dist(b.pos, s.rig_pos)
            if prev is not None and math.dist(b.pos, prev) > 1.5:
                jumps += 1
            prev = tuple(b.pos)
            worst = max(worst, d)
            if d > 0.5:
                off.append((s.t - t0, round(d, 2)))
        ck(f'follow {kind}: at the end of every tick her model stands within 0.5 b of her body ({jumps} moves of more '
           f'than 1.5 b in one tick; the farthest {worst:.2f} b = one tick of her own walk)', not off and (jumps >= 3 or not tid or tid == 33), off[:8])
    g = fn_lines('boss/scarlet/core/ground_to')
    ck('follow: core/ground_to (a cancelled leap, g/ground), core/place8 (the revive) and the replay\'s seat end with rig/follow_now',
       g[-1].endswith('rig/follow_now') and fn_lines('boss/scarlet/core/place8')[-1].endswith('rig/follow_now')
       and any(l.endswith('rig/follow_now') for l in fn_lines('boss/scarlet/core/replay/start'))
       and all('core/ground_to' in l for l in fn_lines('boss/scarlet/g/ground')[-2:]))
    bad = [str(p.relative_to(FN)) for p in (FN / 'boss/scarlet').rglob('*.mcfunction')
           if 'in_sneak' in p.read_text(encoding='utf-8').split('\n', 1)[-1] or any('in_sneak' in l for l in fn_lines(str(p.relative_to(FN))[:-11]))]
    ck('follow: no function of her module reads rlk:in_sneak (the parked core skip reads the jump key as the sequences do)',
       not bad and any('predicate rlk:in_jump' in l for l in fn_lines('boss/scarlet/core/skip')), bad[:5])


# ============================================================================================================ swap
RIG_CH = {3: 'skirk', 5: 'arle', 6: 'navia'}
MAN_CH = {1: 'lumine', 4: 'clorinde', 7: 'ronova', 8: 'nefer'}
CAT = {7: 'rlk_rncat', 8: 'rlk_nfcat'}
REAL_PRE = ('rlk:char/cine/', 'rlk:char/motion/beat/', 'rlk:char/motion/lite/', 'rlk:player/def/beat/')
SWAP_STUB = ('rlk:player/def/beat/rock_on', 'rlk:player/def/beat/rock_off', 'rlk:player/def/beat/act', 'rlk:player/def/beat/st/')
STAGE_AT = ((104.25, 64.0, 203.75), (55.0, 0.0))
UUID_RE = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')


class SwapWorld(mcsim.Sim):
    """mcsim + what the avatar's three bodies use (the model of tests/test_actor.py's World, widened to lane VP's stand-in rig
    and glow): display NBT (view_range, the item model, Glowing), the avatar's invisibility, hand and profile, fixed UUIDs.
    Real: char/cine/**, char/motion/beat/**, char/motion/lite/**, player/def/beat/** (but its rock / stretch passes: no enemy
    here); every other function is an empty call."""

    def __init__(self):
        super().__init__(FN)
        self.now = 0
        self.objectives = set()

    def load(self, fid):
        if fid.startswith(REAL_PRE) and not fid.startswith(SWAP_STUB):
            return super().load(fid)
        return []

    def select(self, sel, ctx):
        if UUID_RE.fullmatch(sel):
            return [e for e in self.ents if e.alive and e.data.get('_uuid') == sel]
        return super().select(sel, ctx)

    def _es(self, sel, ctx):
        return [ctx.ex] if sel == '@s' else self.select(sel, ctx)

    def execute(self, t, ctx):
        # `if|unless data entity <sel> {item:{components:{"minecraft:item_model":"X"}}}` (the weapon's glow variants)
        for i in range(1, len(t) - 4):
            if t[i] in ('if', 'unless') and t[i + 1] == 'data' and t[i + 2] == 'entity':
                es = self._es(t[i + 3], ctx)
                m = re.search(r'"minecraft:item_model":"([^"]+)"', t[i + 4])
                ok = bool(es) and (es[0].data.get('model') == m.group(1) if m else True)
                if ok != (t[i] == 'if'):
                    return 0
                return self.execute(t[:i] + t[i + 5:], ctx)
        return super().execute(t, ctx)

    def cmd(self, t, ctx):
        c = t[0]
        if c == 'scoreboard' and t[1] == 'objectives':
            if t[2] == 'add':
                self.objectives.add(t[3])
            elif t[2] == 'remove':
                self.objectives.discard(t[3])
                for k in [k for k in self.scores if k[1] == t[3]]:
                    del self.scores[k]
            return 1
        if c == 'scoreboard' and t[1] == 'players' and 'cine' in (t[4:5] + t[7:8]) and 'cine' not in self.objectives:
            return 0                                    # the game: unknown objective, the command fails
        if c == 'summon':
            nbt = t[5] if len(t) > 5 else '{}'
            r = super().cmd(t, ctx)
            e = self.ents[-1]
            m = re.search(r'UUID:\[I;(-?\d+),(-?\d+),(-?\d+),(-?\d+)\]', nbt)
            if m:
                h = ''.join(f'{int(x) & 0xffffffff:08x}' for x in m.groups())
                e.data['_uuid'] = f'{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}'
            m = re.search(r'"minecraft:item_model":"([^"]+)"', nbt)
            e.data['model'] = m.group(1) if m else None
            m = re.search(r'view_range:([\d.]+)f', nbt)
            e.data['view_range'] = float(m.group(1)) if m else 1.0
            return r
        if c == 'data' and t[1] == 'merge' and t[2] == 'entity':
            es = self._es(t[3], ctx)
            for e in es:
                m = re.search(r'view_range:([\d.]+)f', t[4])
                if m:
                    e.data['view_range'] = float(m.group(1))
                m = re.search(r'"minecraft:item_model":"([^"]+)"', t[4])
                if m:
                    e.data['model'] = m.group(1)
                m = re.search(r'Glowing:(\d)b', t[4])
                if m:
                    e.data['glow'] = m.group(1) == '1'
            return 1 if es else 0
        if c == 'data' and t[1] == 'modify' and t[2] == 'entity' and t[4].startswith('profile'):
            for e in self._es(t[3], ctx):
                if t[4] == 'profile.texture':
                    e.data['profile'] = dict(e.data.get('profile') or {}, texture=t[7].strip('"'))
                elif t[5:7] == ['set', 'from']:
                    e.data['profile'] = dict(self.storage.get(t[8], {}).get(t[9]) or {})
            return 1
        if c == 'data' and t[1] == 'modify' and t[2] == 'storage' and t[5:8] == ['set', 'from', 'entity'] and t[9] == 'profile':
            es = self._es(t[8], ctx)
            if not es or not es[0].data.get('profile'):
                return 0                                # no such path: the command fails, the value written before stays
            self.storage.setdefault(t[3], {})[t[4]] = dict(es[0].data['profile'])
            return 1
        if c == 'data' and t[1] == 'remove' and t[2] == 'entity':
            for e in self._es(t[3], ctx):
                if t[4] == 'item':
                    e.data['model'] = None
            return 1
        if c == 'data' and t[1] == 'remove' and t[2] == 'storage':
            self.storage.get(t[3], {}).pop(t[4], None)
            return 1
        if c == 'effect':
            for e in self._es(t[2], ctx):
                if t[1] == 'give':
                    e.data['invis'] = max(e.data.get('invis', 0), self.now + (10 ** 9 if t[4] == 'infinite' else int(t[4]) * 20))
                else:
                    e.data.pop('invis', None)
            return 1
        if c == 'item' and t[1] == 'replace':
            for e in self._es(t[3], ctx):
                if t[4] == 'contents':
                    src = self._es(t[7], ctx)
                    e.data['model'] = 'minecraft:iron_sword' if src and src[0].data.get('hand', {}).get('weapon.mainhand') == 'item' else None
                else:
                    e.data.setdefault('hand', {})[t[4]] = 'air' if t[5] == 'with' and 'air' in t[6] else 'item'
            return 1
        if c in ('attribute', 'playsound', 'particle', 'title'):
            return 1
        return super().cmd(t, ctx)


def swap_world(ch):
    w = SwapWorld()
    w.setsc('#charN', 'tmp', ch)
    w.setsc('#3', 'tmp', 3)
    pl = mcsim.Ent('player', (100.5, 64.0, 200.5), (30.0, 10.0), ['player'])
    av = mcsim.Ent('mannequin', (100.5, 64.0, 200.5), (30.0, 0.0), ['rlk_view', 'rlk_av', 'rlk_body'])
    av.data['hand'] = {'weapon.mainhand': 'air' if ch in CAT else 'item', 'weapon.offhand': 'air'}
    av.data['profile'] = {'texture': f'rlk:skin/{(MAN_CH | RIG_CH)[ch]}'} if ch != 1 else {'name': 'lumine_profile'}
    w.ents += [pl, av]
    w.player, w.av = pl, av
    pid = ('e', pl.id)
    for o in ('dead', 'rnDie', 'pkMode', 'vMap', 'rdCam', 'devMode', 'plActive', 'pmActive', 'pmVisible', 'pmMoveLock', 'pbGlow', 'pbTint'):
        w.setsc(pid, o, 0)
    if ch in RIG_CH:
        for i in range(11):
            e = mcsim.Ent('item_display', av.pos, (30.0, 0.0), ['rlk_view', 'rlk_pm'] + (['rlk_pm_weapon'] if i == 10 else []))
            e.data.update(view_range=1.5, model='rlk:player_motion/weapons/sword' if i == 10 else f'rlk:player_motion/x/{i}')
            w.ents.append(e)
        for o, v in (('pmVisible', 1), ('pmActive', 0), ('pmWModel', 3), ('pmRigChar', ch)):
            w.setsc(pid, o, v)
        av.data['invis'] = 10 ** 9
        av.data['hand'] = {'weapon.mainhand': 'air', 'weapon.offhand': 'air'}
    if ch in CAT:
        for i in range(5):
            e = mcsim.Ent('block_display', av.pos, (0.0, 0.0), [CAT[ch]])
            e.data['view_range'] = 1.0
            w.ents.append(e)
    w.setsc('#btLag', 'cb', 0)                              # (the game reads an unset score as 0; mcsim refuses)
    w.call('rlk:player/def/beat/reset', C0)
    w.setsc('#btOn', 'tmp', 1)
    w.setsc('#mbCam', 'mb', 0)
    w.setsc('#mbCine', 'mb', 0)
    return w


def pctx(w, at=None):
    pos, rot = at or (w.player.pos, w.player.rot)
    return Ctx(w.player, tuple(pos), tuple(rot))


def bodies(w):
    """Which of the avatar's bodies would be drawn now: the avatar (a mannequin that is not invisible), its stand-in rig
    (rlk_pl), its own rig (rlk_pm), the actor (rlk_cine_part)."""
    vis = lambda tag, no=None: any(e.alive and tag in e.tags and (no is None or no not in e.tags) and e.data.get('view_range', 1.0) > 0  # noqa: E731
                                   for e in w.ents)
    out = []
    if w.av.data.get('invis', 0) <= w.now:
        out.append('avatar')
    if vis('rlk_pl', 'rlk_pl_weapon'):
        out.append('stand-in')
    if vis('rlk_pm', 'rlk_pm_weapon'):
        out.append('rig')
    if vis('rlk_cine_part'):
        out.append('actor')
    return out


def swap_tick(w, t, beat_at, kind, lock):
    """One game tick in rlk:tick's order: the beat's clock, the fight tick (the judged answer that starts the beat on tick
    beat_at; the locked sequence's start / tick while t is in `lock`), the camera hold, the beat's post."""
    w.now = t
    w.cmd(split(CLOCK), C0)
    if t == beat_at:
        w.call('rlk:player/def/beat/start_p' if kind == 'parry' else 'rlk:player/def/beat/start_d', pctx(w))
    if lock and lock[0] <= t < lock[1]:
        if t == lock[0]:
            w.call('rlk:char/cine/spawn', pctx(w, STAGE_AT))
            w.call('rlk:char/cine/play', pctx(w), {'clip': 'cs1'})
        w.setsc('#mbCam', 'mb', 1)
        w.setsc('#cavT', 'cine', t - lock[0])
        w.call('rlk:char/cine/tick', pctx(w))
        w.player.tags.add('rlk_mb_camh')                   # rlk:tick's hold line (after mboss/main)
    elif lock and t == lock[1]:
        w.setsc('#mbCam', 'mb', 0)
        w.player.tags.discard('rlk_mb_camh')
        w.call('rlk:char/cine/stop', pctx(w))              # mboss/cam/release
    w.cmd(split(POST), C0)


def swap():
    cine_hide = fn_lines('char/cine/hide')
    ck('swap: char/cine/hide also takes the stand-in rig out of view (rlk_pl -> hide_one), as it does the rig characters\' displays',
       any('tag=rlk_pl,' in l and 'hide_one' in l for l in cine_hide), [l for l in cine_hide if 'hide_one' in l])
    L0, L1, END = 40, 75, 110
    tot = 0
    for ch, name in sorted((MAN_CH | RIG_CH).items()):
        own = 'rig' if ch in RIG_CH else 'avatar'
        for kind, last in (('parry', 17), ('dodge', 27)):
            bad, after, glows = [], [], []
            # no lock: the beat alone
            for age in [None] + list(range(0, last + 1)):
                w = swap_world(ch)
                prof0, hand0 = dict(w.av.data['profile']), dict(w.av.data['hand'])
                b0 = L0 - age if age is not None else 20
                lock = (L0, L1) if age is not None else None
                for t in range(1, END + 1):
                    swap_tick(w, t, b0, kind, lock)
                    b = bodies(w)
                    locked = lock is not None and L0 <= t < L1
                    want = ['actor'] if locked else None
                    if locked:
                        blank = w.av.data.get('profile', {}).get('texture') == 'rlk:skin/blank' and w.av.data.get('invis', 0) > w.now
                        if b != want or not blank:
                            bad.append((age, t - L0, b, 'blank' if blank else 'NOT blank'))
                    elif len(b) != 1 or (b == ['stand-in'] and ch in RIG_CH) or b == ['actor']:
                        bad.append((age, t, b))
                    tot += 1
                    if locked and t == L0 + 1:
                        left = {k: bt(w, k) for k in ('#btK', '#btHold', '#btInv') if bt(w, k)}
                        if left or any(e.alive and ('rlk_pl' in e.tags or 'rlk_pl_basis' in e.tags) for e in w.ents):
                            bad.append((age, 'one tick into the lock', left, 'stand-in parts left'))
                pid = ('e', w.player.id)
                back = (bodies(w) == [own] and w.av.data.get('profile') == prof0 and w.av.data['hand'] == hand0
                        and not any(e.alive and ('rlk_pl' in e.tags or 'rlk_cine_part' in e.tags or 'rlk_cine_hid' in e.tags) for e in w.ents)
                        and (w.sc(pid, 'plActive') or 0) == 0 and 'cine' not in w.objectives)
                if not back:
                    after.append((age, bodies(w), w.av.data.get('profile'), w.av.data['hand']))
                gl = [(sorted(e.tags)[0], e.data.get('model')) for e in w.ents if e.alive and (e.data.get('glow') or '_glow' in str(e.data.get('model')) or '/wg/' in str(e.data.get('model')))]
                if gl or (w.sc(pid, 'pbGlow') or 0) or (w.sc(pid, 'pbTint') or 0) or bt(w, '#btK'):
                    glows.append((age, gl[:3]))
            ck(f'swap {name} ({"rig" if ch in RIG_CH else "mannequin"} character), a perfect {kind}: alone and with a lock starting at each beat age 0-{last}: '
               f'exactly one body at the end of every tick (the {own}{"" if ch in RIG_CH else " or its stand-in rig"} outside the lock; the actor alone inside it, the avatar '
               f'invisible and blank), nothing of the beat left one tick into the lock', not bad, bad[:6])
            ck(f'swap {name}, a perfect {kind}: after the hand-back (and without a lock) the {own} is back as it was (skin, hand), no stand-in part, no '
               f'actor part, no glow, no tint, no beat left', not after and not glows, (after[:3], glows[:3]))
    ck(f'swap: {tot} ticks looked at (7 characters x 2 beats x every lock age)', tot > 30000, tot)


# ============================================================================================================ beatseq
import copy  # noqa: E402
PH, SEQL = api.PH, api.SEQ_LEN
PHN = {v: k for k, v in PH.items()}
A_ = H.A


class FlowBeatSim(BeatClock, Q.SeqSim, H.H1Sim):
    """test_flow's world (camsim's view and lock, seqsim's actor model, H1Sim's inputs and judge; the real core starts and
    ticks the sequences) on the beat's clock: rlk:tick's beat lines run as written around the fight tick."""
    parry_on = True
    inject = None               # (world tick, 'p' | 'd'): a beat started by the judge inside that fight tick
    log = None                  # per real tick: (world tick, held by the beat, held by the camera, client on the live camera)

    def __init__(self, root):
        super().__init__(root)
        self.log = []


def vworld(s):
    """One REAL tick in rlk:tick's order: the beat's clock, view/tick, the fight tick (or, on a tick the beat holds, only
    rlk:tick's own mboss/main line and the scheduled functions), FN-cam's lines, the beat's post, the player's server tick."""
    k0 = len(s.kitl)
    s.pre = 1
    s.cmd(split(CLOCK), C0)
    s.pre = 0
    hold = bt(s, '#btHold') == 1
    CS.view_tick(s)
    s._cam_done = False
    if hold:
        s.held += 1
        s.cmd(split(MAINL), C0)
        s.gt_off = 1
        try:
            s.run_sched_at(s.t + 1)
        finally:
            s.gt_off = 0
    else:
        H.world_h1(s)
        if s.inject and s.inject[0] == s.t:
            pl = s.player()
            s.call('rlk:player/def/beat/start_' + s.inject[1], Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
            s.inject = None
    if not s._cam_done:
        s.run_cam_lines()
    s.cmd(split(POST), C0)
    pl = s.player()
    if pl is not None:
        s.net_tick(pl)
    live = s.sc('#mbCamId', 'mb')
    on = CS.client_on(s)
    s.log.append((s.t, hold, CS.held(s), on is not None and f'rlk_mb_cam{live}' in on, bt(s, '#btK')))
    for t, c, a in s.kitl[k0:]:                      # the parrier: F one tick before every cued hit
        if c == 'snd/' + api.CUE_SND and s.parry_on:
            s.press(at=t + api.CUE_LEAD - 1)


def vrun(s, cond, limit, each=None):
    for _ in range(limit):
        if cond(s):
            return True
        if each:
            each(s)
        vworld(s)
    return cond(s)


def vheal(s):
    if s.player() is not None and not (s.sc(('e', s.player().id), 'rnDie') or 0):
        H.heal(s)


def vstate(s):
    b = H.body_of(s)
    return dict(ph=PHN.get(H.hr(s, '#ph')), sqn=H.hr(s, '#sqn'), hp=s.sc(('e', b.id), 'mhpC') if b else None,
                body=[round(v, 2) for v in b.pos] if b else None, yaw=round(b.rot[0] % 360, 1) if b else None,
                gau=H.hr(s, '#gau'), bal=H.bal(s), php=s.sc(('e', s.player().id), 'curHealth'))


def seq_variants(snap, name, started, ended, cases):
    """From the snapshot `snap` (taken before sequence `name` starts): the reference run, then one run per (kind, k): a beat
    started by the judge k world ticks before the sequence's first tick."""
    ref = copy.deepcopy(snap)
    ok = vrun(ref, started, 600, each=vheal)
    w0 = ref.t
    held0 = CS.held(ref)
    ok = ok and vrun(ref, ended, SEQL[name] + 60, each=vheal)
    w1 = ref.t
    for _ in range(3):
        vheal(ref)
        vworld(ref)
    st_ref = vstate(ref)
    clean = [k for k, v in CS.clean(ref).items() if not v] if held0 else []
    ck(f'beatseq {name}: the reference run (no beat near it): starts on world tick {w0}, {"locks the player" if held0 else "does not lock the player"}, '
       f'ends {w1 - w0} world ticks later, hands back clean', ok and not clean and not any(e.alive and 'rlk_cine_root' in e.tags for e in ref.ents),
       (ok, clean))
    for kind, k in cases:
        s = copy.deepcopy(snap)
        s.log = []
        s.inject = (w0 - k, kind)
        lag0 = bt(s, '#btLag')
        vrun(s, started, 700, each=vheal)
        i0 = len(s.log) - 1                                  # the real tick the sequence started on
        age = bt(s, '#btA') if bt(s, '#btK') else None
        same = s.t == w0
        vheal(s)
        vworld(s)
        left = beat_left(s)
        done = vrun(s, ended, SEQL[name] + 80, each=vheal)
        w1b = s.t
        for _ in range(3):
            vheal(s)
            vworld(s)
        lg = s.log[i0:]
        held_after = [r[0] for r in lg[1:] if r[1]]
        lock = [r for r in lg if r[0] < w1b]
        cam_ok = (not held0) or all(r[2] and r[3] for r in lock[1:]) and lock[0][2]
        st = vstate(s)
        clean = [x for x, v in CS.clean(s).items() if not v] if held0 else []
        what = {'p': 'a perfect parry', 'd': 'a perfect dodge'}[kind]
        slow = ' (inside the slow motion)' if kind == 'd' and age in (8, 11) else ''
        if not held0:
            # a lead-in of the fight (no camera lock, no #mbCine): the beat is not cut: it runs its own length, and the
            # lead-in still ends on the same world tick in the same state
            n = 5 if kind == 'p' else 7
            ck(f'beatseq {name} (not a locked sequence): {what} judged {k} world tick(s) before it: the beat runs its course (the world '
               f'held {s.held - snap.held} real ticks), the lead-in starts and ends on the same world ticks and the fight goes on from '
               f'the same state; nothing held at the end', same and done and w1b == w1 and st == st_ref and s.held - snap.held == n
               and bt(s, '#btLag') - lag0 == n and not beat_left(s) and bt(s, '#btK') == 0,
               dict(same=same, end=(w1b, w1), held=s.held - snap.held, left=beat_left(s), st=[(x, st[x], st_ref[x]) for x in st if st[x] != st_ref[x]]))
            continue
        ck(f'beatseq {name}: {what} judged {k} world tick(s) before it: the sequence starts on the same world tick with the beat at age '
           f'{age}{slow}; one real tick later nothing is held ({left or "nothing left"}), no tick is held after that; '
           f'{"the camera holds the player from the first tick and the client is on the live camera on every tick of it; " if held0 else ""}'
           f'it ends on the same world tick, hands back clean, and the fight goes on from the same state',
           same and age is not None and not left and not held_after and done and w1b == w1 and cam_ok and not clean and st == st_ref
           and bt(s, '#btLag') - lag0 == s.held - snap.held,
           dict(same=same, age=age, left=left, held_after=held_after[:4], end=(w1b, w1), cam=cam_ok, clean=clean,
                st=[(x, st[x], st_ref[x]) for x in st if st[x] != st_ref[x]], lag=(bt(s, '#btLag') - lag0, s.held - snap.held)))
    return ref


def beatseq():
    s, pl = CS.setup(DP, cls=FlowBeatSim, seed=11, lv=15, hp=5834, player_level=15)
    s.cache['rlk:mob/setup'] = ['tag @s add rlk_mob', 'function rlk:bal/init']
    s.call('rlk:bal/load', C0)
    s.storage.setdefault('rlk:pinv', {}).setdefault('order', [])
    beat_reset(s, 1, STUB_FX + STUB_AV)
    z, a = H.rift_zone(s, 'scarlet')
    s.player().pos = list(a.pos)
    ok = bool(H.enter(s, a))
    s.zone_sc = z
    ok = ok and vrun(s, lambda s: H.body_of(s) is not None and s.avatar() is not None and (s.sc('#sq', 'hr') or 0) >= 1, 1200)
    ok = ok and vrun(s, lambda s: (H.mb(s, '#mbSt') or 0) == 1, SEQL['intro'] + 40, each=vheal)
    vworld(s)
    ck('beatseq: the rift, CS0 locked to its end and the hand-back, on the beat\'s clock (beat on, nothing to hold yet)',
       ok and H.hr(s, '#ph') == PH['p1'] and s.held == 0 and not [k for k, v in CS.clean(s).items() if not v])

    def p_each(s):
        vheal(s)
        b, p = H.body_of(s), s.player()
        if s.t % 8 == 0 and math.dist(b.pos[::2], p.pos[::2]) <= 4.0 and 'rlk_mb_inv' not in b.tags:
            A_.strike(s, b, 30)

    H.facing_setup(s, 3.0)
    j0, h0 = len(s.judged), s.held
    vrun(s, lambda s: False, 400, each=p_each)
    par = len([j for j in s.judged[j0:] if j['parT'] == 3])
    ck(f'beatseq P1, 400 real ticks with the perfect parrier: {par} perfect parries held the world {s.held - h0} real ticks (5 each)',
       par >= 3 and s.held - h0 in (5 * par, 5 * par - 5 + max(0, min(5, bt(s, "#btA")))) or s.held - h0 == 5 * par, (par, s.held - h0))
    vrun(s, lambda s: bt(s, '#btK') == 0, 40, each=vheal)
    P_CASES = (('p', 0), ('p', 1), ('p', 4), ('d', 0), ('d', 1), ('d', 3), ('d', 5), ('d', 6), ('d', 7))
    # ---- the 60 % floor -> CS1
    s.parry_on = False
    H.test_id(s, 80)
    vrun(s, lambda s: (H.hr(s, '#pat') or 0) == 0 and (s.sc(('e', H.body_of(s).id), 'grgT') or 0) == 0, 200, each=vheal)
    A_.strike(s, H.body_of(s), 99999)
    s.parry_on = True
    s = seq_variants(s, 'cs1', lambda s: H.hr(s, '#ph') == PH['cs1'], lambda s: H.hr(s, '#ph') == PH['lead60'], P_CASES)
    # ---- lead60 -> G1 cleared -> the repel
    ok = vrun(s, lambda s: H.hr(s, '#ph') == PH['a8'], SEQL['lead60'] + 10, each=vheal)
    t1, h1, j1 = s.t, s.held, len(s.judged)
    vrun(s, lambda s: s.t - t1 >= api.JUDGE_T['a8'] - 12, 600, each=vheal)
    pp = len([j for j in s.judged[j1:] if j['parT'] == 3])
    ck(f'beatseq G1 with the beat on: {pp} perfect parries (every cut), the world held {s.held - h1} real ticks = 5 x {pp}; the judge '
       f'is still {api.JUDGE_T["a8"]} world ticks after the start', ok and pp == len([c for *_x, c in api.SCRIPTS['a8'] if c]) and s.held - h1 == 5 * pp, (pp, s.held - h1))
    s = seq_variants(s, 'repel', lambda s: H.hr(s, '#ph') == PH['cs2'], lambda s: H.hr(s, '#ph') == PH['p2'], P_CASES)
    ck(f'beatseq: the repel started at G1\'s judge (world tick T + {api.JUDGE_T["a8"]})', s.log and True)
    # ---- P2 -> the 5 % floor -> lead5
    H.facing_setup(s, 5.0)
    vrun(s, lambda s: False, 200, each=p_each)
    vrun(s, lambda s: bt(s, '#btK') == 0, 40, each=vheal)
    s.parry_on = False
    H.test_id(s, 34)
    vrun(s, lambda s: (H.hr(s, '#pat') or 0) == 0 and (s.sc(('e', H.body_of(s).id), 'grgT') or 0) == 0, 200, each=vheal)
    A_.strike(s, H.body_of(s), 99999)
    s.parry_on = True
    seq_variants(s, 'lead5', lambda s: H.hr(s, '#ph') == PH['lead'], lambda s: H.hr(s, '#ph') == PH['a13'], P_CASES)


# ============================================================================================================ skip
class SkipSim(BeatClock, Q.SeqSim):
    """seqsim's driven world (the parked core, the real sequence files, the lock, the client model) on the beat's clock."""


def sworld(s, inject=None):
    """One real tick in rlk:tick's order (camsim.world + the beat's lines); inject 'p' | 'd': the judge starts a beat in it."""
    s.pre = 1
    s.cmd(split(CLOCK), C0)
    s.pre = 0
    hold = bt(s, '#btHold') == 1
    CS.view_tick(s)
    s._cam_done = False
    if hold:
        s.held += 1
        s.cmd(split(MAINL), C0)
        s.gt_off = 1
        try:
            s.run_sched_at(s.t + 1)
        finally:
            s.gt_off = 0
    else:
        H.world_sc(s)
        if inject:
            pl = s.player()
            s.call('rlk:player/def/beat/start_' + inject, Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
    if not s._cam_done:
        s.run_cam_lines()
    s.cmd(split(POST), C0)
    pl = s.player()
    if pl is not None:
        s.net_tick(pl)
    s.client_tick()
    return hold


def sq_state(s):
    """test_seq.state: what a skip must reproduce."""
    b = H.body_of(s)
    live = s.sc('#mbCamId', 'mb')
    v = CS.client_view(s)
    cam = next((e for e in s.ents if e.alive and f'rlk_mb_cam{live}' in e.tags), None)
    tx = [next((x.data.get('text') for x in s.ents if x.alive and t in x.tags and cam is not None and x.data.get('riding') == cam.id), None)
          for t in (CS.LINE_TAG, CS.HINT_TAG)]
    return dict(body=[round(v_, 2) for v_ in b.pos], yaw=round(b.rot[0] % 360, 1), live=live,
                rig=None if s.rig_pos is None else [round(v_, 2) for v_ in s.rig_pos],
                view=None if v is None else ([round(x, 2) for x in v[0]], [round(x, 2) for x in v[1]]),
                on=CS.client_on(s) is not None and f'rlk_mb_cam{live}' in CS.client_on(s),
                text=tx[0], hint=tx[1], cav=s.sc('#cavT', 'cine'), sq=s.sc('#sq', 'hr'),
                stage=[(sorted(e.tags)[0], [round(x, 2) for x in e.pos], round(e.rot[0], 1)) for e in s.ents
                       if e.alive and e.etype == 'marker' and ('rlk_hr_stage' in e.tags or 'rlk_hr_stage2' in e.tags)],
                props=sorted(sorted(e.tags) for e in s.ents if e.alive and ('rlk_hr_sqp' in e.tags or 'rlk_hr_deco_seat_rock' in e.tags)),
                held=CS.held(s))


def skip_world(name):
    import sheets
    s, pl = CS.setup(DP, cls=SkipSim)
    s.storage.setdefault('rlk:pinv', {}).setdefault('order', [])
    assert Q.fight(s), 'the fight did not start'
    if name == 'intro':
        b = H.body_of(s)
        b.pos = list(api.SEAT_POS)
        mp = api.MOON_POS
        b.rot = [math.degrees(math.atan2(-(mp[0] - b.pos[0]), mp[2] - b.pos[2])), 0.0]
        st = api.ARENA['start']
        s.avatar().pos = [st['x'], st['y'], st['z']]
    else:
        Q.place(s, *sheets.STAGES['c'])
    beat_reset(s, 1, STUB_FX + STUB_AV)
    s.drive = dict(name=name, args=None, t=-1, then=None)
    return s, pl


def skip_run(name, at, keys=('jump',), sneak=False, beat=None, beat_dt=0, early=0):
    """The sequence to tick `at` (`early`: Space already held that many ticks before), then the keys held until the skip; a
    beat started by the judge beat_dt ticks after `at`. Returns what happened."""
    to = api.SKIP[name]['to']
    s, pl = skip_world(name)
    sq = lambda: s.sc('#sq', 'hr') or 0  # noqa: E731
    n = 0
    while sq() < at - early and n < 3000:
        sworld(s)
        n += 1
    out = dict(held=0, on=True, fired=None, left=None, beat_held=0)
    pl.data['keys'] = set(keys)
    pl.data['sneak'] = sneak
    k = 0
    for k in range(api.SKIP_HOLD + early + 40):
        inj = beat if (beat and sq() == at + beat_dt - 1) else None
        t_before = sq()
        h = sworld(s, inject=inj)
        out['beat_held'] += h
        out['held'] += 1
        if beat and out['left'] is None and bt(s, '#btK') == 0 and k > 0:
            out['left'] = beat_left(s)
        live = s.sc('#mbCamId', 'mb')
        on = CS.client_on(s)
        out['on'] = out['on'] and on is not None and f'rlk_mb_cam{live}' in on
        if sq() == to - 1:
            out['fired'] = t_before + 1
            break
    pl.data['keys'] = set()
    pl.data['sneak'] = False
    while s.drive is not None and sq() < to + 4:
        sworld(s)
        live = s.sc('#mbCamId', 'mb')
        on = CS.client_on(s)
        out['on'] = out['on'] and on is not None and f'rlk_mb_cam{live}' in on
    out['state'] = sq_state(s)
    out['end_left'] = beat_left(s)
    out['K'] = bt(s, '#btK')
    return out


def skip():
    for name in ('intro', 'cs1'):
        lo, hi = api.SKIP[name]['window']
        to = api.SKIP[name]['to']
        at = lo + 37
        ref = skip_run(name, at)
        ck(f'skip {name}: the plain skip on the beat\'s clock: Space held from tick {at} fires after {api.SKIP_HOLD} ticks (at {ref["fired"]}), the '
           f'client on the live camera throughout, her model at her body at {to + 4}',
           ref['fired'] == at + api.SKIP_HOLD and ref['held'] == api.SKIP_HOLD and ref['on'] and ref['state']['rig'] == ref['state']['body']
           and ref['state']['held'], (ref['fired'], ref['held'], ref['on']))
        cases = [('a perfect parry beat started the tick Space goes down', dict(beat='p')),
                 ('a perfect dodge beat started the tick Space goes down', dict(beat='d')),
                 ('a perfect parry beat started 10 ticks into the hold', dict(beat='p', beat_dt=10)),
                 ('a perfect dodge beat started 10 ticks into the hold', dict(beat='d', beat_dt=10)),
                 ('a perfect dodge beat started on the tick of the skip itself', dict(beat='d', beat_dt=api.SKIP_HOLD)),
                 ('W, A and sprint held with Space', dict(keys=('jump', 'f', 'l', 'sprint'))),
                 ('S and D held with Space', dict(keys=('jump', 'b', 'r'))),
                 ('Shift held with Space', dict(sneak=True)),
                 ('Shift, W and a dodge beat with Space', dict(sneak=True, keys=('jump', 'f'), beat='d', beat_dt=3))]
        for what, kw in cases:
            r = skip_run(name, at, **kw)
            diff = [(k, r['state'][k], ref['state'][k]) for k in ref['state'] if r['state'][k] != ref['state'][k]]
            ck(f'skip {name}: {what}: the skip fires on the same tick ({r["fired"]}), lands in the plain skip\'s state at {to + 4}, the client is '
               f'on the live camera on every tick' + ('; the beat is over one tick after it started and never holds a tick' if kw.get('beat') else ''),
               r['fired'] == ref['fired'] and not diff and r['on'] and r['beat_held'] == 0 and not r['end_left'] and r['K'] == 0
               and (not kw.get('beat') or r['left'] == {} or kw.get('beat_dt') == api.SKIP_HOLD),
               dict(fired=(r['fired'], ref['fired']), diff=diff[:4], on=r['on'], beat_held=r['beat_held'], left=r['left'], end=r['end_left']))
        r = skip_run(name, lo, early=min(lo - 2, 15))
        diff = [(k, r['state'][k], ref['state'][k]) for k in ref['state'] if r['state'][k] != ref['state'][k]]
        ck(f'skip {name}: Space already held before the window opens ({min(lo - 2, 15)} ticks early): nothing is counted before tick {lo}; the '
           f'skip fires on the window\'s {api.SKIP_HOLD}th tick (at {r["fired"]}) and lands in the same state',
           r['fired'] == lo + api.SKIP_HOLD - 1 and not diff and r['on'], (r['fired'], lo + api.SKIP_HOLD - 1, diff[:3]))


SECTIONS = [('beatpat', beatpat), ('follow', follow), ('swap', swap), ('beatseq', beatseq), ('skip', skip)]


def main():
    for name, f in SECTIONS:
        if want(name):
            print(f'== {name}', flush=True)
            f()
    print(f'test_vi: {NCK[0] - len(FAILS)}/{NCK[0]} passed' + (f'; FAILED: {FAILS}' if FAILS else ''))
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
