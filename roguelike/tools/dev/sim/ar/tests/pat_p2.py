#!/usr/bin/env python3
"""pat_p2.py (S4): the phase-2 patterns of 아를레키노 in the knsim world (S:ar/s3/lib/knsim.py; PLAN §6, §11.3).

    python3 pat_p2.py [<roguelike dir>] [section ...]      sections: hits tells geo q5b beam pj q6 q0 ends cancel pause
                                                            stand decals static render (default: all)

Every case starts from P2 (test 31: T skipped) with the AI held, then core/start/<key> as the body.
 hits    every hazard strikes on the tick of its api.HITS clip event in its stage (stage clock == clip tick; Q6 feathers
         where they land, event + FEATHER_T); every HITS entry of the branch taken strikes; shapes, tiers (api.dmg(t, 2)),
         Pyro, quiet; the FN-1 option #hzBol on every bol hazard (I1), none on a plain one; only the last hit knocks back; the body
         inside MOVE_R, between the floor and AIR_MAX every tick, on the floor and not gliding at the end
 tells   first visible motion -> hit >= TELL_MIN (>= TELL_BIG big), follow-ups >= COMBO_GAP or one volley group (Q5B: groups
         of 2 rapid slashes, landings >= 6 t apart)
 geo     Q5A disc / donut / wide disc and Q0 disc + blade ring: safe bands exist and are walkable in time
 q5b     the per-mille final (api.HITS; x #mbBolRe with FN-1 while bonded) is non-lethal (1 HP stays), Bond of Life, dash-dodgeable; at most 5 slash landings
 beam    Q4: the aim tracks the player until the lock, the beam goes along the locked line (a player who leaves it after the
         lock is missed, a standing one is hit), 1 / 2 (missed) / 3 (<= 50 % pool, test 45) shots
 pj      Q1 / Q3 crescents (speed, half width, range, the return in the same group, wall stop), Q2 wheel (speed, burst on
         arrival at the lock, in the wheel's group, strikes <= 32)
 q6      the 8 rim orbs (r 22, 45 deg apart, inside walk) and the safe band between them and the dive; feathers visible >= 14 t
 q0      the trigger (a 1.5 b move / 80 t, a jump in place is no move), the landing 1.5 b in front, once per fight (AI)
 ends    end points (hover, dive landing, dash, lunge, rise) over 500 seeded player / boss positions incl. the rim, with
         random 2-block pillars: inside MOVE_R, mv/ok, never in a block, <= AIR_MAX
 cancel  a cancel at every tick leaves no marker / prop / hazard / projectile, the body on the floor, the window closed
 pause   a 25 t pause in the middle changes no hit tick (pattern clock frozen), nothing duplicated
 stand   a standing player takes the whole Q1 string (3 b, 6 b), Q3 near; landings per cast of a standing player
 decals  only q5a draws floor decals and only ring_o / donut_o (kit-on dry build); resume redraws them
 static  no rlk_mb_inv, no negative add / remove literals, lowercase ids in p/q*/**
Renders: AR/renders/s4_<key>.png (top-down hit shapes over time + her height over time).
"""
import copy
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SCR = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad')
sys.path.insert(0, str(SCR / 'ar/s3/lib'))
import knsim as T  # noqa: E402
from mcsim import Ctx  # noqa: E402

check, summary = T.check, T.summary
ARGS = sys.argv[1:]
DP = Path(ARGS[0]) if ARGS and '/' in ARGS[0] else SCR / 'ar/wt_i1/roguelike'
ONLY = [a for a in ARGS if '/' not in a]
RENDER = SCR / 'ar/renders'
KIND = {'disc': 1, 'pj_bolt': 1, 'pm_disc': 1, 'orb_discs': 1, 'ring': 2, 'sector': 3, 'line': 4}
EN = {'q0': 'opening fall', 'q1': 'twin string', 'q2': 'wheel + dash', 'q3': 'rear whip-spin', 'q4': 'beams',
      'q5a': 'penalty rings (break 22-121)', 'q5b': 'execution (break 22-96)', 'q6': 'blood feast'}

api = T.load_api(DP)
from mboss_arlecchino import p2 as P2  # noqa: E402
from mboss_arlecchino import s3lib as SL  # noqa: E402
TID = {k: SL.TID[k] for k in api.P2}
KEY_OF = {v: k for k, v in TID.items()}
CX, CY, CZ = api.CX, api.CY, api.CZ
_FPM = next(h[3][1] for h in api.HITS['q5b'] if h[1] == 'final')
FIN_PM = (_FPM, max(1, _FPM * api.BOL_REHIT_PCT // 100))           # the final's pl_dot: plain / bonded (FN-1 x #mbBolRe)

# ------------------------------------------------------------------------------------------------- recording hooks
_call = T.KnSim.call


def _rec_call(self, fid, ctx, macro=None):
    if fid == 'rlk:mboss/pj/launch' and ctx.ex is not None:
        g = lambda k: self.sc(k, 'mb')  # noqa: E731
        self.pjx.append(dict(t=self.t, tags=list(ctx.ex.tags), pos=tuple(ctx.pos), rot=tuple(ctx.rot), macro=dict(macro or {}),
                             kb=g('#pjKB'), grp=g('#pjGrp'), shape=g('#pjShape'), wall=g('#pjWall'), pat=self.sc('#pat', 'kn')))
    if fid == 'rlk:mboss/pl_dot':
        self.dots.append((self.t, self.sc('#mbDotPct', 'mb'), self.sc('#mbDotLethal', 'mb'), self.sc('#pat', 'kn')))
    n0 = len(self.hzr)
    if fid == 'rlk:mboss/pj/all':
        self.inpj = True
    if fid == 'rlk:mboss/hz/hurt_pm' and self.player() is not None:
        # the sim sets the dash i-frames only inside cm/hit_pl2; the per-mille path reads them before pl_dot
        self.setsc(('e', self.player().id), 'dashInvT', 1 if self.t <= getattr(self, 'iframe_end', -1) else 0)
    r = _call(self, fid, ctx, macro)
    if fid == 'rlk:mboss/pj/all':
        self.inpj = False
    if fid == 'rlk:mboss/hz/make' and len(self.hzr) > n0:
        h = self.hzr[n0]
        key = KEY_OF.get(h['pat'])
        h['st'] = self.sc(f'#{key}_s', 'kn') if key else None
        h['sc'] = self.sc(f'#{key}_c', 'kn') if key else None
        h['gt'] = self.t
        h['pj'] = getattr(self, 'inpj', False)
        h['st_gt'] = h['gt'] + h['tell'] + (1 if h['pj'] else 0)      # the world tick it strikes
    return r


T.KnSim.call = _rec_call
_orig_init = T.KnSim.__init__


def _init(self, root):
    _orig_init(self, root)
    self.pjx = []
    self.dots = []


T.KnSim.__init__ = _init

# pm / nododge of a hazard are read from its marker right after hz/init (hz/make -> init)
_PM = {}


def hz_markers(s, key):
    return [e for e in s.ents if e.alive and 'rlk_mb_hz' in e.tags and f'rlk_kn_p_{key}' in e.tags]


# ------------------------------------------------------------------------------------------------- world helpers
def bctx(s):
    b = T.body(s)
    return Ctx(b, tuple(b.pos), tuple(b.rot))


def fresh(hold=True):
    s, pl = T.setup(dp=DP, hp=200000)
    T.fight(s)
    T.test_id(s, 99)
    T.run(s, 30, T.heal_player)
    T.test_id(s, 31)
    T.run(s, 5, T.heal_player)
    if not hold:
        T.test_id(s, 99)
    return s


def place(s, d, side=0.0):
    b = T.body(s)
    yaw = math.radians(b.rot[0])
    fx, fz = -math.sin(yaw), math.cos(yaw)
    T.place_player(s, b.pos[0] + fx * d - fz * side, b.pos[2] + fz * d + fx * side)


def stage_names(key):
    return P2_SM[key]


def run_pattern(s, key, limit=600, each=None, snap=False, extra=()):
    tid = TID[key]
    for lst in (s.hzr, s.pjs, s.phits, s.rigl, s.pjx, s.dots):
        lst.clear()
    s.call(f'rlk:boss/arlecchino/core/start/{key}', bctx(s))
    log, snaps = [], []
    for _ in range(limit):
        if snap:
            a = s.api
            s.api = None
            snaps.append((T.kn(s, '#pt'), copy.deepcopy(s)))
            s.api = a
        if each:
            each(s)
        T.world(s)
        b = T.body(s)
        row = dict(t=s.t, pt=T.kn(s, '#pt'), pat=T.kn(s, '#pat'), st=T.kn(s, f'#{key}_s'), c=T.kn(s, f'#{key}_c'),
                   pos=tuple(b.pos), yaw=b.rot[0], bolw=T.kn(s, '#bolw'), win=T.kn(s, '#win'), mv='rlk_mb_mv' in b.tags)
        for x in extra:
            row[x] = T.kn(s, x)
        log.append(row)
        if T.kn(s, '#pat') != tid:
            break
    return log, snaps


P2_SM = {}


def build_tables():
    """Stage order per pattern (the SM stage index = order + 1) from a dry build of p2.PATTERNS."""
    import types

    class DW:
        def __init__(self):
            self.files = {}
            self.out = types.SimpleNamespace(written=set())

        def w(self, rel, body):
            self.files[rel] = body
    out = {}
    for p in P2.PATTERNS:
        W = DW()
        p.build(W)
        sts = []
        for rel, body in W.files.items():
            m = re.match(rf'p/{p.key}/s/([a-z0-9_]+)/go$', rel)
            if m:
                idx = next(int(x.split()[-1]) for x in body if x.startswith(f'scoreboard players set #{p.key}_s '))
                sts.append((idx, m.group(1)))
        out[p.key] = [n for _, n in sorted(sts)]
    return out


P2_SM.update(build_tables())


def visits(log, key):
    """[(stage name, the #pt of its tick 0, max clock)] in order."""
    names = P2_SM[key]
    out = []
    prev = None
    for r in log:
        st = r['st']
        if not st:
            continue
        nm = names[st - 1]
        if prev is None or nm != prev[0] or r['c'] < prev[2]:
            out.append([nm, r['pt'] - r['c'], r['c']])
        else:
            out[-1][2] = r['c']
        prev = out[-1]
    return out


def big(shape, dims):
    if shape in ('disc', 'pm_disc', 'pj_bolt'):
        return math.pi * dims[0] ** 2 >= 100 or dims[0] >= 8
    if shape == 'orb_discs':
        return True
    if shape == 'sector':
        return math.pi * dims[0] ** 2 * dims[1] / 180 >= 100 or dims[0] >= 8
    if shape == 'ring':
        return math.pi * (dims[1] ** 2 - dims[0] ** 2) >= 100 or dims[1] >= 8
    if shape == 'line':
        return dims[0] * dims[1] >= 100
    return False


def hitdims(h):
    hk_hit = api.HITS[h['hk']][h['idx']]
    return hk_hit


# ------------------------------------------------------------------------------------------------- 1 hits
def check_run(key, s, log, where, branch=None):
    tid = TID[key]
    tab = P2.TABLE[key]
    vis = visits(log, key)
    hz = [h for h in s.hzr if h['pat'] == tid]
    if key == 'q2':
        bursts = [h for h in hz if h['kind'] == 1]
        hz = [h for h in hz if h['kind'] != 1]
    got = Counter()
    rows = defaultdict(list)
    for h in hz:
        if h['st'] is None or h['st'] == 0:
            rows[('?', -1)].append(h)
            continue
        nm = P2_SM[key][h['st'] - 1]
        t = h['sc'] + h['tell']
        got[(nm, t)] += 1
        rows[(nm, t)].append(h)
    want = Counter()
    for nm, t0, cmax in vis:
        for e in tab:
            if e['stage'] != nm or e['t'] > cmax + (1 if e['shape'] == 'pj_bolt' else 0):
                continue
            if e['shape'] in ('pj_cres', 'pj_burst'):
                continue
            if key == 'q2' and e['idx'] == 1 and not branch.get('slash'):
                continue
            want[(nm, e['t'])] += 8 if e['shape'] == 'orb_discs' else 1
    check(f'{key} [{where}]: every hazard strikes on its clip event in its stage (visits {[(v[0], v[2]) for v in vis]})',
          got == want, (sorted(got.items()), sorted(want.items())))
    bad = []
    for (nm, t), hs in rows.items():
        ents = [e for e in tab if e['stage'] == nm and e['t'] == t and e['shape'] not in ('pj_cres', 'pj_burst')]
        if not ents:
            bad.append((nm, t, 'no entry'))
            continue
        exp = []
        for e in ents:
            hh = api.HITS[e['hk']][e['idx']]
            shape, dims, tier = e['shape'], hh[3], hh[4]
            if shape == 'orb_discs':
                exp += [('disc', dims[0], tier, e['bol'])] * 8
            elif shape == 'burst':
                exp.append(('disc', hh[3][2], tier, 0))
            elif shape == 'pm_disc':
                exp.append(('pm', dims[0], 'PM', e['bol']))
            elif shape == 'pj_bolt':
                exp.append(('disc', dims[0], tier, e['bol']))
            else:
                exp.append((shape, dims, tier, e['bol']))
        for (shape, dims, tier, bol), h in zip(sorted(exp, key=lambda x: str(x[1])), sorted(hs, key=lambda h: (h['kind'], h['r']))):
            if h['quiet'] != 1 or h['el'] != api.PYRO:
                bad.append((nm, t, 'quiet/el', h['quiet'], h['el']))
            if (h.get('bol') or 0) != (api.BOL_HIT if bol else 0):           # FN-1 live (I1): the hazard's own option
                bad.append((nm, t, 'hzBol', h.get('bol'), bol))
            if shape == 'pm':
                if h['kind'] != 1 or h['r'] != round(dims * 10) or h['dmg'] != 1:
                    bad.append((nm, t, 'pm', h['kind'], h['r'], h['dmg']))
                continue
            dmg = api.dmg(tier, 2)
            if h['dmg'] != dmg:
                bad.append((nm, t, shape, 'dmg', h['dmg'], dmg))
            if shape == 'disc' and (h['kind'] != 1 or h['r'] != round((dims if isinstance(dims, float) else dims[0]) * 10)):
                bad.append((nm, t, shape, h['kind'], h['r'], dims))
            if shape == 'sector' and (h['kind'] != 3 or h['r'] != round(dims[0] * 10) or h['a'] != round(dims[1])):
                bad.append((nm, t, shape, h['kind'], h['r'], h['a']))
            if shape == 'ring' and (h['kind'] != 2 or h['r'] != round(dims[1] * 10)):
                bad.append((nm, t, shape, h['kind'], h['r']))
            if shape == 'line' and (h['kind'] != 4 or (h['r'] or 0) + (h['back'] or 0) != round(dims[0] * 10) or h['hw'] != round(dims[1] * 10)):
                bad.append((nm, t, shape, h['kind'], h['r'], h['hw']))
    check(f'{key} [{where}]: shapes / tiers (P2) / Pyro / quiet / Bond-of-Life marks match api.HITS', not bad, bad[:5])
    # no plain hit strikes on the game tick of a bol strike (the FN-1 stand-in is exact)
    gt = defaultdict(set)
    for (nm, t), hs in rows.items():
        ents = [e for e in tab if e['stage'] == nm and e['t'] == t]
        for h in hs:
            gt[h['st_gt']].add(max((e['bol'] for e in ents), default=0))
    mixed = [t for t, v in gt.items() if v == {0, 1}]
    check(f'{key} [{where}]: no plain hit on a Bond-of-Life strike tick', not mixed, mixed)
    # knockback: every hit but the last of the cast KB_CHAIN (a non-last KB_FINAL hit that did not land is allowed)
    evs = [(h['st_gt'], h['kb'], 'hz') for h in hz + (bursts if key == 'q2' else [])] + [(p['t'], p['kb'], 'pj') for p in s.pjx if p['pat'] == tid
                                                                and 'rlk_kn_out' in p['tags'] or (p['pat'] == tid and 'rlk_kn_wheel' in p['tags'])]
    evs.sort()
    landed = {t for t, *_ in s.phits}
    badkb = []
    if evs:
        last_t = evs[-1][0]
        for t, kb, kind in evs:
            if t == last_t:
                if kb != api.KB_FINAL and not (key == 'q2' and not branch.get('slash')):
                    badkb.append((t, kb, kind, 'last'))
            elif kb != api.KB_CHAIN and (t in landed or t + 1 in landed):
                badkb.append((t, kb, kind))
    check(f'{key} [{where}]: only the last hit knocks back', not badkb, (badkb, evs[-4:]))
    out = [(r['pt'], round(math.hypot(r['pos'][0] - CX, r['pos'][2] - CZ), 2)) for r in log
           if math.hypot(r['pos'][0] - CX, r['pos'][2] - CZ) > api.MOVE_R + 0.01]
    hy = [(r['pt'], round(r['pos'][1] - CY, 2)) for r in log if r['pos'][1] < CY - 0.001 or r['pos'][1] > CY + api.AIR_MAX + 0.01]
    check(f'{key} [{where}]: the body inside MOVE_R, between the floor and AIR_MAX every tick', not out and not hy, (out[:3], hy[:3]))
    end = log[-1]
    check(f'{key} [{where}]: on the floor, not gliding, window closed, nothing of the pattern left at the end',
          abs(end['pos'][1] - CY) < 0.01 and not end['mv'] and (end['win'] or 0) == 0 and not T.ents(s, f'rlk_kn_p_{key}')
          and not T.ents(s, 'rlk_kn_dp'), (end, [e.tags for e in T.ents(s, f'rlk_kn_p_{key}')]))
    return vis


def branch_of(key, s, log):
    return {'slash': any(h['pat'] == TID['q2'] and h['kind'] == 3 for h in s.hzr)} if key == 'q2' else {}


def sec_hits():
    for key in api.P2:
        for where, d, side in (('near', 3.0, 0.0), ('mid', 9.0, 2.0), ('far', 16.0, -3.0), ('edge', 0.0, 0.0)):
            s = fresh()
            if where == 'edge':
                b = T.body(s)
                b.pos = [CX, CY, CZ + 21.0]
                b.rot = [180.0, 0.0]
                T.place_player(s, CX + 2.0, CZ - 14.0)
            else:
                place(s, d, side)
            log, _ = run_pattern(s, key, each=T.heal_player, extra=('#q2_sl', '#q1_k', '#q3_k', '#q4_n'))
            br = branch_of(key, s, log)
            check_run(key, s, log, where, br)
            if where == 'mid':
                RUNS[key] = (s, log)


RUNS = {}


# ------------------------------------------------------------------------------------------------- 2 tells
def sec_tells():
    for key in api.P2:
        tab = P2.TABLE[key]
        bad = []
        for h in tab:
            hit = api.HITS[h['hk']][h['idx']]
            shape = h['shape']
            gap = h['t'] - h['tell']
            prev = [o for o in tab if o['stage'] == h['stage'] and o['t'] == h['tell'] and o is not h]
            if prev:
                same = any(o['grp'] == h['grp'] and h['grp'] not in (0, -1) for o in prev)
                if key == 'q5b' and shape == 'disc':
                    if gap < 3:
                        bad.append((h['t'], 'rapid gap', gap))
                elif gap < api.COMBO_GAP and not same:
                    bad.append((h['stage'], h['t'], 'follow-up', gap))
            else:
                need = api.TELL_BIG if big(shape if shape != 'pj_burst' else 'disc', hit[3] if shape != 'pj_burst' else (hit[3][2],)) else api.TELL_MIN
                if gap < need:
                    bad.append((h['stage'], h['t'], 'tell', gap, need))
        check(f'{key}: tells >= {api.TELL_MIN} / {api.TELL_BIG} (big) t from the first visible motion, follow-ups >= {api.COMBO_GAP} t',
              not bad, bad)
    # Q5B: groups of 2 rapid slashes -> landings >= 6 t apart, <= 5 landings
    sl = [h for h in P2.TABLE['q5b'] if h['shape'] == 'disc']
    grps = Counter(h['grp'] for h in sl)
    firsts = sorted(min(h['t'] for h in sl if h['grp'] == g) for g in grps)
    check('q5b: the 9 rapid slashes in 5 volley groups of <= 2 (landings >= 6 t apart)',
          len(sl) == 9 and len(grps) == 5 and max(grps.values()) <= api.Q5B_SLASH_GROUP
          and all(b - a >= 6 for a, b in zip(firsts, firsts[1:])), (grps, firsts))


# ------------------------------------------------------------------------------------------------- 3 geometry
def sec_geo():
    M = 0.3
    walk = api.WALK
    # Q5A: hit1 disc 6, hit2 ring 6-15, hit3 disc 11, centred on her (at the axis and at the rim)
    r1 = api.HITS['q5a'][0][3][0]
    r20, r2 = api.HITS['q5a'][1][3]
    r3 = api.HITS['q5a'][2][3][0]
    for cx, cz, lab in ((0.0, 0.0, 'axis'), (0.0, 23.0, 'rim')):
        pts = [(x, z) for x in range(-26, 27) for z in range(-26, 27) if math.hypot(x, z) <= walk - 0.5]
        d = [math.hypot(x - cx, z - cz) for x, z in pts]
        s1 = [v for v in d if v > r1 + M]
        s2 = [v for v in d if v < r20 - M or v > r2 + M]
        s3 = [v for v in d if v > r3 + M]
        check(f'q5a geometry ({lab}): a safe band exists for each burst (outside {r1}, inside {r20} / outside {r2}, outside {r3})',
              s1 and s2 and s3 and any(v < r20 - M for v in s2), (len(s1), len(s2), len(s3)))
    walkv = 0.216
    t12 = api.ev('q5a', 'hit2') - api.ev('q5a', 'hit1')
    t23 = api.ev('q5a', 'hit3') - api.ev('q5a', 'hit2')
    check('q5a: the outs are walkable in time (outside 6 -> inside 6 between hit1 and hit2; inside 6 -> outside 11 after hit2)',
          (2 * M) / t12 <= walkv and (r3 + M - (r20 - M)) / t23 <= walkv, (t12, t23))
    # Q0: impact disc 3 + blade ring 3-7: the ring leaves the landing disc safe; outside 7 safe from both
    r0 = api.HITS['q0'][0][3][0]
    a, b = api.HITS['q0'][1][3]
    check('q0 geometry: disc(3) then ring(3,7): the centre is safe from the ring, outside 7.3 safe from both',
          a >= r0 and b > a, (r0, a, b))


# ------------------------------------------------------------------------------------------------- 4 Q5B final
def sec_q5b():
    s = fresh()
    place(s, 3.0)
    pl = s.player()
    st = {'low': False}

    def low(s):
        pt = T.kn(s, '#pt') or 0
        if pt < api.ev('q5b', 'final') - 3:
            T.heal_player(s)
        elif not st['low']:
            s.setsc(('e', pl.id), 'curHealth', 6)
            st['low'] = True
    log, _ = run_pattern(s, 'q5b', each=low)
    fin = [d for d in s.dots if d[3] == TID['q5b'] and d[1] in FIN_PM]
    check(f'q5b: the final is a {FIN_PM[0]} per-mille pl_dot (x #mbBolRe while bonded), non-lethal (#mbDotLethal 0)',
          fin and all(d[2] == 0 for d in fin), (fin, s.dots[-3:]))
    check('q5b: a player at 6 HP survives the final with >= 1 HP', T.esc(s, pl, 'curHealth') >= 1 and (T.esc(s, pl, 'dead') or 0) == 0,
          (T.esc(s, pl, 'curHealth'), T.esc(s, pl, 'dead')))
    mk = [h for h in s.hzr if h['pat'] == TID['q5b'] and h['r'] == 75]
    check('q5b: the final is a Bond-of-Life strike (FN-1 #hzBol on its hazard)', mk and mk[0].get('bol') == api.BOL_HIT, mk[:1])
    landings = sorted({t for t, *_ in s.phits})
    check('q5b: a standing player at 3 b takes <= 5 rapid-slash landings', len(landings) <= 5, landings)
    # dash-dodgeable: dash i-frames at the final tick
    s = fresh()
    place(s, 3.0)
    pl = s.player()

    def dash(s):
        T.heal_player(s)
        if (T.kn(s, '#pt') or 0) == api.ev('q5b', 'final') - 1:
            s.iframe_end = s.t + 3
    log, _ = run_pattern(s, 'q5b', each=dash)
    fin = [d for d in s.dots if d[3] == TID['q5b'] and d[1] in FIN_PM]
    check('q5b: the final is dodged by the dash i-frames (no pl_dot)', not fin, fin)
    mk = [h for h in s.hzr if h['pat'] == TID['q5b'] and h['r'] == 75]
    check('q5b: the final hazard is quiet, not nododge (dash-dodgeable)', mk and mk[0]['quiet'] == 1, mk[:1])


# ------------------------------------------------------------------------------------------------- 5 Q4 beam
def sec_beam():
    lockt, fire = api.ev('q4_shot', 'lock'), api.ev('q4_shot', 'fire')
    top = api.ev('q4_up', 'top')
    # a player who walks sideways during the aim, then stops: the beam goes along the line locked at 20
    s = fresh()
    place(s, 9.0)
    yaws = []

    def side(s):
        T.heal_player(s)
        pt = T.kn(s, '#pt') or 0
        pl = s.player()
        b = T.body(s)
        if top < pt < top + lockt:
            yaw = math.radians(b.rot[0])
            pl.pos[0] += math.cos(yaw) * 0.2
            pl.pos[2] += math.sin(yaw) * 0.2
            T.C.moved(s)
        if pt in (top + lockt - 6, top + lockt - 1):
            yaws.append(b.rot[0])
    log, _ = run_pattern(s, 'q4', each=side)
    beams = [h for h in s.hzr if h['pat'] == TID['q4'] and h['kind'] == 4]
    lock = [r for r in log if r['pt'] == top + lockt]
    check('q4 beam: the aim tracks the moving player during the aim (her yaw changes)', len(yaws) == 2 and abs(yaws[0] - yaws[1]) > 1,
          yaws)
    check('q4 beam: the beam is aimed along her yaw at the lock (line 30 x 2.2 from her floor spot)',
          beams and lock and abs(((beams[0]['yaw'] - lock[0]['yaw']) + 180) % 360 - 180) < 0.5 and beams[0]['r'] == 300
          and beams[0]['hw'] == 22, (beams[:1], lock[:1]))
    check('q4 beam: a standing player (after the walk) on the locked line is hit', len(s.phits) >= 1, s.phits)
    # a player who leaves the locked line after the lock (3 b sideways) is missed
    s = fresh()
    place(s, 9.0)

    def leave(s):
        T.heal_player(s)
        pt = T.kn(s, '#pt') or 0
        if pt == top + lockt + 1:
            pl = s.player()
            b = T.body(s)
            yaw = math.radians(b.rot[0])
            pl.pos[0] += math.cos(yaw) * 3.0
            pl.pos[2] += math.sin(yaw) * 3.0
            T.C.moved(s)
    log, _ = run_pattern(s, 'q4', each=leave)
    shots1 = [h for h in s.hzr if h['pat'] == TID['q4'] and h['kind'] == 4]
    check('q4 beam: a player who leaves the line after the lock is missed by shot 1, so a 2nd shot follows (missed -> 2)',
          not [p for p in s.phits if p[0] <= shots1[0]['gt'] + 2] and len(shots1) == api.Q4_SHOTS['missed'],
          (s.phits, len(shots1)))
    # a standing player: hit by shot 1 -> 1 shot
    s = fresh()
    place(s, 9.0)
    log, _ = run_pattern(s, 'q4', each=T.heal_player)
    n = len([h for h in s.hzr if h['pat'] == TID['q4'] and h['kind'] == 4])
    check('q4: a standing player is hit by the first beam -> 1 shot', n == api.Q4_SHOTS['base'] and len(s.phits) == 1, (n, s.phits))
    # <= 50 % of the P2 pool -> 3 shots
    s = fresh()
    place(s, 9.0)
    b = T.body(s)
    s.setsc(('e', b.id), 'mhpC', T.esc(s, b, 'mhpM') // 2)
    log, _ = run_pattern(s, 'q4', each=T.heal_player)
    n = len([h for h in s.hzr if h['pat'] == TID['q4'] and h['kind'] == 4])
    vis = visits(log, 'q4')
    check('q4: at <= 50 % of the pool 3 shots, 50 t apart, then the landing (stages up, shot x3, land)',
          n == api.Q4_SHOTS['low_pct'][1] and [v[0] for v in vis] == ['up', 'shot', 'shot', 'shot', 'land']
          and [v[1] for v in vis][1:4] == [top, top + 50, top + 100], (n, vis))
    # test 45 -> 3 shots (and the test id is consumed: the next AI-picked q4 is normal)
    s = fresh()
    place(s, 9.0)
    for lst in (s.hzr,):
        lst.clear()
    T.test_id(s, 45)
    T.run(s, 300, T.heal_player)
    n = len([h for h in s.hzr if h['pat'] == TID['q4'] and h['kind'] == 4])
    check('q4: test 45 fires 3 shots and its flag is consumed (#q4_t3, R-S4-2)', n == 3 and (T.kn(s, '#q4_t3') or 0) == 0,
          (n, T.kn(s, '#q4_t3')))


# ------------------------------------------------------------------------------------------------- 6 projectiles
def sec_pj():
    hr, spd, rng = api.HITS['q1'][2][3]
    v = api.L.pj_speed_tenths(spd)
    s, log = RUNS.get('q1') or (None, None)
    s = fresh()
    place(s, 3.0)
    log, _ = run_pattern(s, 'q1', each=T.heal_player)
    pj = [p for p in s.pjx if p['pat'] == TID['q1']]
    outs = [p for p in pj if 'rlk_kn_out' in p['tags']]
    rets = [p for p in pj if 'rlk_kn_ret' in p['tags']]
    check(f'q1 crescents: 3 thrown (h3 + the h6 pair), blade shape, {v / 10} b/t, half width {hr}, range {rng} b, wall stop',
          len(outs) == 3 and all(p['macro']['spd'] == v and p['macro']['hr'] == round(hr * 10) and p['shape'] == 1 and p['wall'] == 1
                                 and p['macro']['life'] * (math.ceil(spd / 0.25) * 0.25) >= rng - 0.01 for p in outs), outs)
    check('q1 crescents: each returns in the same volley group (one landing per throw), no wall stop on the way back',
          len(rets) == 3 and sorted(p['grp'] for p in rets) == sorted(p['grp'] for p in outs) and all(p['wall'] == 0 for p in rets)
          and len({p['grp'] for p in outs}) == 2, ([p['grp'] for p in outs], [p['grp'] for p in rets]))
    h6 = [p for p in outs if p['t'] == max(q['t'] for q in outs)]
    yaws = sorted(p['rot'][0] for p in h6)
    check('q1 h6: the pair is thrown at her yaw +-15 deg', len(h6) == 2 and abs(((yaws[1] - yaws[0]) % 360) - 30) < 0.6, yaws)
    # wall stop: a wall 4 b in front of her at chest height -> the outward leg ends early and returns
    s = fresh()
    place(s, 3.0)
    b = T.body(s)
    yaw = math.radians(b.rot[0])
    fx, fz = -math.sin(yaw), math.cos(yaw)
    wall = [(math.floor(b.pos[0] + fx * 6 - fz * k), y, math.floor(b.pos[2] + fz * 6 + fx * k)) for k in range(-4, 5)
            for y in range(CY, CY + 4)]

    def walled(s):
        # I1: the real fl_ruins look job (crimson, from test 31) rewrites the arena slices for a while after the fight
        # starts and would clear a wall set once: the wall is set again every tick
        T.heal_player(s)
        for x, y, z in wall:
            s.setb(x, y, z, 'stone')
    log, _ = run_pattern(s, 'q1', each=walled)
    pj = [p for p in s.pjx if p['pat'] == TID['q1']]
    o = [p for p in pj if 'rlk_kn_out' in p['tags']]
    r = [p for p in pj if 'rlk_kn_ret' in p['tags']]
    check('q1 crescent: a wall stops the outward leg early (it returns after < its range)', o and r and r[0]['t'] - o[0]['t'] < 10
          and r[0]['macro']['life'] < 10, ([(p['t'], p['macro']) for p in o[:1]], [(p['t'], p['macro']) for p in r[:1]]))
    # Q2 wheel: speed, the burst at the lock in the wheel's group, strikes <= 32
    for d in (6.0, 12.0, 22.0):
        s = fresh()
        place(s, d)
        log, _ = run_pattern(s, 'q2', each=T.heal_player, extra=('#q2_sl',))
        wh = [p for p in s.pjx if p['pat'] == TID['q2']]
        bs = [h for h in s.hzr if h['pat'] == TID['q2'] and h['kind'] == 1]
        hr2, spd2, r2 = api.HITS['q2'][0][3]
        st0 = log[0]['t'] - 1
        ok = (len(wh) == 1 and wh[0]['macro']['spd'] == api.L.pj_speed_tenths(spd2) and wh[0]['macro']['hr'] == round(hr2 * 10)
              and wh[0]['macro']['life'] <= P2.WHEEL_LIFE and len(bs) == 1 and bs[0]['r'] == round(r2 * 10)
              and bs[0]['grp'] == wh[0]['grp'] and bs[0]['st_gt'] - st0 <= api.ev('q2', 'slash') - api.COMBO_GAP)
        check(f'q2 [{d} b]: one wheel ({spd2} b/t, {hr2} b, <= {P2.WHEEL_LIFE} t), one burst disc({r2}) in its group, the burst '
              f'>= {api.COMBO_GAP} t before the slash', ok, ([(p['t'] - st0, p['macro'], p['grp']) for p in wh],
                                                            [(h['st_gt'] - st0, h['grp'], h['pos']) for h in bs]))
        sl = [h for h in s.hzr if h['pat'] == TID['q2'] and h['kind'] == 3]
        dist = math.hypot(*(a - b for a, b in zip(T.body(s).pos[::2], s.player().pos[::2])))
        check(f'q2 [{d} b]: the dash ends within reach and the slash comes (no whiff); far beyond reach it is skipped',
              # I1 accepted DASH_LEN['q2'] 20 (R-S4-6): a player within the dash + the slash reach is reached
              (len(sl) == 1 and dist <= P2.SLASH_REACH) if d <= api.DASH_LEN['q2'] + P2.SLASH_REACH
              else (not sl and dist > P2.SLASH_REACH), (len(sl), round(dist, 2)))


# ------------------------------------------------------------------------------------------------- 7 Q6
def sec_q6():
    s = fresh()
    place(s, 9.0)
    log, _ = run_pattern(s, 'q6', each=T.heal_player)
    imp = api.ev('q6', 'impact')
    orbs = [h for h in s.hzr if h['pat'] == TID['q6'] and h['r'] == 50]
    rr = [math.hypot(h['pos'][0] - CX, h['pos'][2] - CZ) for h in orbs]
    ang = sorted(math.degrees(math.atan2(h['pos'][2] - CZ, h['pos'][0] - CX)) % 360 for h in orbs)
    gaps = [(b - a) for a, b in zip(ang, ang[1:] + [ang[0] + 360])]
    check('q6: 8 orb bursts on the rim, r 22 from the axis (inside walk), 45 deg apart',
          len(orbs) == 8 and all(abs(r - 22.0) < 0.15 for r in rr) and all(abs(g - 45) < 0.6 for g in gaps) and max(rr) + 0 <= api.WALK,
          (rr, gaps))
    dive = [h for h in s.hzr if h['pat'] == TID['q6'] and h['r'] == 40]
    # the safe band: points inside walk outside every orb disc (+0.3) and the dive disc (+0.3); between neighbouring orbs too
    pts = [(CX + x * 0.5, CZ + z * 0.5) for x in range(-52, 53) for z in range(-52, 53) if math.hypot(x * 0.5, z * 0.5) <= api.WALK - 0.5]
    hit = lambda x, z: any(math.hypot(x - h['pos'][0], z - h['pos'][2]) <= h['r'] / 10 + 0.3 for h in orbs + dive)  # noqa: E731
    safe = [p for p in pts if not hit(*p)]
    rim_gap = [p for p in safe if math.hypot(p[0] - CX, p[1] - CZ) > 18]
    check('q6: a safe band exists between the rim orbs and the dive (inner area and the gaps between orbs)',
          len(safe) > 0.3 * len(pts) and rim_gap, (len(safe), len(pts), len(rim_gap)))
    fe = [e for e in P2.TABLE['q6'] if e['shape'] == 'pj_bolt']
    check(f'q6: six feathers, each visible {P2.FEATHER_T} t (>= 14) before it lands, 10 t apart',
          len(fe) == 6 and all(e['t'] - e['tell'] >= 14 for e in fe), [(e['t'], e['tell']) for e in fe])
    hmax = max(r['pos'][1] for r in log) - CY
    check('q6: she hovers at <= AIR_MAX (12 b) over the north half', hmax <= api.AIR_MAX + 0.01 and hmax > 11.0, hmax)


# ------------------------------------------------------------------------------------------------- 8 Q0
def sec_q0():
    wait = api.Q0_TRIGGER[1]
    # move 2 b at hover tick 10 -> the dive starts at once
    s = fresh()
    place(s, 6.0)

    def mv(s):
        T.heal_player(s)
        if (T.kn(s, '#q0_c') or 0) == 10 and T.kn(s, '#q0_s') == 1:
            pl = s.player()
            pl.pos[0] += 2.0
            T.C.moved(s)
    log, _ = run_pattern(s, 'q0', each=mv)
    vis = visits(log, 'q0')
    check('q0: a 2 b move at hover tick 10 starts the dive on the next tick', [v[0] for v in vis] == ['hover', 'dive'] and vis[0][2] <= 12,
          vis)
    # no move -> the dive at 80 t; the hover spot 14 b from the player, 10 b up
    s = fresh()
    place(s, 6.0)
    p0 = tuple(s.player().pos)
    log, _ = run_pattern(s, 'q0', each=T.heal_player)
    vis = visits(log, 'q0')
    hrow = next(r for r in log if r['st'] == 1 and r['c'] == 2)
    dh = math.hypot(hrow['pos'][0] - p0[0], hrow['pos'][2] - p0[2])
    check(f'q0: without a move the dive starts at {wait} t; the hover {api.LEAP_H["q0"]} b up, 14 b from the player',
          [v[0] for v in vis] == ['hover', 'dive'] and vis[1][1] == wait and abs(hrow['pos'][1] - CY - api.LEAP_H['q0']) < 0.01
          and abs(dh - 14.0) < 0.2, (vis, hrow['pos'], round(dh, 2)))
    land = log[-1]['pos']
    dl = math.hypot(land[0] - p0[0], land[2] - p0[2])
    check('q0: she lands about 1.5 b in front of the player (not on them)', 1.3 <= dl <= 1.7, round(dl, 2))
    # a jump in place is no move
    s = fresh()
    place(s, 6.0)

    def jump(s):
        T.heal_player(s)
        c = T.kn(s, '#q0_c') or 0
        pl = s.player()
        pl.pos[1] = CY + (1.2 if 10 <= c <= 18 and T.kn(s, '#q0_s') == 1 else 0.0)
        T.C.moved(s)
    log, _ = run_pattern(s, 'q0', each=jump)
    vis = visits(log, 'q0')
    check('q0: a jump in place does not trigger the dive', len(vis) == 2 and vis[1][1] == wait, vis)
    # once per fight: with the AI running after Q0, it is never picked again
    s = fresh()
    place(s, 6.0)
    s.setsc('#lock', 'kn', 0)          # release the hold (the sim's store-success of a failed `unless` keeps 1)
    pats = []

    def mv2(s):
        T.heal_player(s)
        pats.append(T.kn(s, '#pat'))
    T.run(s, 1500, mv2)
    n0 = sum(1 for a, b in zip(pats, pats[1:]) if b == TID['q0'] and a != TID['q0'])
    check('q0: runs once as the P2 opener, then #q0_ok 1 and never again (1500 t of AI)', n0 == 1 and T.kn(s, '#q0_ok') == 1,
          (n0, T.kn(s, '#q0_ok'), Counter(pats).most_common(6)))


# ------------------------------------------------------------------------------------------------- 9 end points
def sec_ends():
    rnd = random.Random(1102)
    stats = {}
    s0 = fresh()
    a = s0.api
    s0.api = None
    base = copy.deepcopy(s0)
    s0.api = a

    def rpt(rmax, rim=False):
        r = rnd.uniform(api.WALK - 1.4, api.WALK - 0.1) if rim else rmax * math.sqrt(rnd.random())
        q = rnd.uniform(0, 2 * math.pi)
        return CX + r * math.cos(q), CZ + r * math.sin(q)

    def okp(s, x, y, z):
        b = T.body(s)
        return s.call('rlk:mboss/mv/ok', Ctx(b, (x, CY, z), (0, 0)))

    def free(s, x, y, z):
        return all(s.block_test((x, yy, z), '#rlk:dash_pass') for yy in (CY, CY + 1))
    cases = ['q0 hover', 'q4 rise', 'q1 lunge', 'q2 dash', 'dive landing']
    for case in cases:
        res = []
        bad = []
        for i in range(500):
            s = copy.deepcopy(base)
            s.api = a
            # random 2-block pillars (the end points must avoid them)
            rim = i % 5 == 0
            pxz = rpt(api.WALK - 0.1, rim)
            bxz = rpt(api.SAFE - 0.6)
            n_p = 0
            while n_p < 25:
                px, pz = rpt(api.SAFE - 1)
                if min(math.hypot(px - q[0], pz - q[1]) for q in (pxz, bxz)) < 1.5:
                    continue                 # her start / the player's spot are never inside a block in the game
                n_p += 1
                for y in (CY, CY + 1):
                    s.setb(math.floor(px), y, math.floor(pz), 'stone')
            b = T.body(s)
            b.pos = [bxz[0], CY, bxz[1]]
            T.place_player(s, *pxz)
            b.rot = [math.degrees(math.atan2(-(pxz[0] - bxz[0]), pxz[1] - bxz[1])), 0.0]
            ctx = Ctx(b, tuple(b.pos), tuple(b.rot))
            sc = lambda k: s.sc(('e', b.id), k)  # noqa: E731
            if case == 'q0 hover':
                s.call('rlk:boss/arlecchino/p/q0/f/spot', ctx)
                end = tuple(T.body(s).pos)
            elif case == 'q4 rise':
                s.call('rlk:boss/arlecchino/p/q4/f/spot', ctx)
                end = (sc('mbMvX1') / 1000, sc('mbMvY1') / 1000, sc('mbMvZ1') / 1000) if 'rlk_mb_mv' in b.tags else tuple(b.pos)
            elif case == 'q1 lunge':
                s.call('rlk:boss/arlecchino/p/q1/f/lunge', ctx)
                end = (sc('mbMvX1') / 1000, sc('mbMvY1') / 1000, sc('mbMvZ1') / 1000) if 'rlk_mb_mv' in b.tags else tuple(b.pos)
            elif case == 'q2 dash':
                s.call('rlk:boss/arlecchino/p/q2/dash', ctx)
                end = (sc('mbMvX1') / 1000, sc('mbMvY1') / 1000, sc('mbMvZ1') / 1000) if 'rlk_mb_mv' in b.tags else tuple(b.pos)
            else:
                s.call('rlk:boss/arlecchino/core/lockp', ctx)
                s.call('rlk:boss/arlecchino/core/lock_short', ctx)
                lk = [e for e in s.ents if e.alive and 'rlk_kn_lock' in e.tags]
                end = tuple(lk[0].pos) if lk else None
            if end is None:
                bad.append((i, 'none'))
                continue
            r = math.hypot(end[0] - CX, end[2] - CZ)
            h = end[1] - CY
            dpl = math.hypot(end[0] - pxz[0], end[2] - pxz[1])
            ok = okp(s, end[0], CY, end[2]) and free(s, end[0], CY, end[2])
            res.append((r, h, dpl))
            if r > api.MOVE_R + 1e-6 or not ok or h > api.AIR_MAX + 1e-6 or h < -1e-6:
                bad.append((i, round(r, 2), round(h, 2), ok, rim))
        stats[case] = dict(n=len(res), r_max=round(max(x[0] for x in res), 2), h_max=round(max(x[1] for x in res), 2),
                           d_player_mean=round(sum(x[2] for x in res) / len(res), 2),
                           d_player_min=round(min(x[2] for x in res), 2), d_player_max=round(max(x[2] for x in res), 2))
        check(f'end points [{case}]: 500 seeded player / boss positions (1 in 5 at the rim, 25 random pillars): inside MOVE_R, '
              f'mv/ok, free feet / head, <= AIR_MAX', not bad, (bad[:4], stats[case]))
    (SCR / 'ar/s4').mkdir(exist_ok=True)
    (SCR / 'ar/s4/endpoints.json').write_text(json.dumps(stats, indent=1))
    print('end-point stats', json.dumps(stats))


# ------------------------------------------------------------------------------------------------- 10 cancel
def sec_cancel():
    for key in api.P2:
        s = fresh()
        place(s, 7.0)
        log, snaps = run_pattern(s, key, snap=True, each=T.heal_player)
        bad = []
        for pt, snap in snaps[1:]:
            snap.api = s.api
            b = T.body(snap)
            snap.call('rlk:boss/arlecchino/core/cancel_pat', Ctx(b, tuple(b.pos), tuple(b.rot)))
            snap.call('rlk:boss/arlecchino/core/cancel_pat', Ctx(b, tuple(b.pos), tuple(b.rot)))   # idempotent
            T.run(snap, 2, T.heal_player)
            b = T.body(snap)
            left = [e.tags for e in snap.ents if e.alive and any(t == 'rlk_kn_p' or t.startswith('rlk_kn_p_') or t in ('rlk_kn_lock', 'rlk_kn_dp', 'rlk_kn_win')
                                                                  for t in e.tags)]
            hz = [e for e in snap.ents if e.alive and 'rlk_mb_hz' in e.tags]
            pj = [e for e in snap.ents if e.alive and 'rlk_mb_pj' in e.tags]
            if left or hz or pj or abs(b.pos[1] - CY) > 0.01 or (T.kn(snap, '#win') or 0) or (T.kn(snap, '#pat') or 0) != 0:
                bad.append((pt, len(left), len(hz), len(pj), round(b.pos[1] - CY, 2), T.kn(snap, '#win'), T.kn(snap, '#pat')))
        check(f'{key}: a cancel (twice) at every tick ({len(snaps) - 1}) leaves no marker / prop / hazard / projectile, the body on '
              f'the floor, the window closed', not bad, bad[:4])


# ------------------------------------------------------------------------------------------------- 11 pause
def sec_pause():
    for key in api.P2:
        ref = fresh()
        place(ref, 7.0)
        log0, _ = run_pattern(ref, key, each=T.heal_player)
        n = len(log0)
        s = fresh()
        place(s, 7.0)
        pl = s.player()
        st = {'n': 0}

        def pz(s):
            st['n'] += 1
            if st['n'] == n // 2:
                s.setsc(('e', pl.id), 'dead', 1)
            if st['n'] == n // 2 + 25:
                s.setsc(('e', pl.id), 'dead', 0)
            if not (n // 2 <= st['n'] < n // 2 + 25):
                T.heal_player(s)
        log1, _ = run_pattern(s, key, each=pz, limit=800)
        a = sorted((h['pt'] + h['tell'], h['kind'], h['r']) for h in ref.hzr if h['pat'] == TID[key])
        b = sorted((h['pt'] + h['tell'], h['kind'], h['r']) for h in s.hzr if h['pat'] == TID[key])
        pjs_a = len([p for p in ref.pjx if p['pat'] == TID[key]])
        pjs_b = len([p for p in s.pjx if p['pat'] == TID[key]])
        check(f'{key}: a 25 t pause in the middle: same hit ticks on the pattern clock, same projectiles, nothing left over',
              a == b and pjs_a == pjs_b and not T.ents(s, f'rlk_kn_p_{key}') and len(log1) >= n + 20,
              (len(a), len(b), pjs_a, pjs_b, len(log0), len(log1)))


# ------------------------------------------------------------------------------------------------- 12 standing players
LAND = {}


def sec_stand():
    cases = (('q1', 3.0, 6), ('q1', 6.0, 6), ('q3', 4.0, 4), ('q3', 9.0, 1), ('q2', 9.0, 2), ('q2', 14.0, 2), ('q0', 6.0, 1),
             ('q4', 9.0, 1), ('q5a', 3.0, 2), ('q5b', 3.0, 6), ('q6', 9.0, 7))
    for key, d, want in cases:
        s = fresh()
        place(s, d)
        pl = s.player()
        hp0 = T.pmax(s)
        lost = [0]

        def keep(s):
            c = T.esc(s, pl, 'curHealth')
            m = T.esc(s, pl, 'maxHealth')
            if c < m:
                lost[0] += m - c
            T.heal_player(s)
        log, _ = run_pattern(s, key, each=keep)
        landed = sorted({t for t, *_ in s.phits} | {d[0] for d in s.dots if d[3] == TID[key] and d[1] in FIN_PM})
        LAND[(key, d)] = (len(landed), round(100.0 * lost[0] / hp0, 1))
        check(f'{key}: a standing player at {d} b takes {want} landing(s) ({round(100.0 * lost[0] / hp0, 1)} % max HP, Lv20 vs L20)',
              len(landed) == want, landed)
    print('standing landings', {f'{k} {d}': v for (k, d), v in LAND.items()})


# ------------------------------------------------------------------------------------------------- 13 decals (kit-on dry build)
def sec_decals():
    import types

    class DW:
        def __init__(self):
            self.files = {}
            self.out = types.SimpleNamespace(written=set())

        def w(self, rel, body):
            self.files[rel] = body
    real = api.K._on
    api.K._on = lambda: True
    out = {}
    files = {}
    try:
        for p in P2.PATTERNS:
            W = DW()
            p.build(W)
            txt = '\n'.join(ln for body in W.files.values() for ln in body)
            out[p.key] = sorted(set(re.findall(r'fx/decal/([a-z_]+)', txt)))
            files[p.key] = W.files
    finally:
        api.K._on = real
    bad = {k: v for k, v in out.items() if v and (k not in api.DECALS or not set(v) <= set(api.DECALS[k]))}
    check('decals: only q5a draws floor decals, only ring_o / donut_o (kit-on dry build)', not bad and out['q5a'] == ['donut_o', 'ring_o'],
          out)
    res = files['q5a'].get('p/q5a/resume', [])
    check('decals: q5a/resume redraws the outline with the ticks left (#pt windows of the three outlines)',
          sum('matches 60..94' in x or 'matches 100..120' in x or 'matches 130..157' in x for x in res) == 3, res)
    for k, tags in (('q1', ('crescent',)), ('q2', ('wheel',)), ('q3', ('crescent',)), ('q6', ('feather', 'orb'))):
        r = files[k].get(f'p/{k}/resume', [])
        check(f'decals: {k}/resume re-dresses its kit props {tags}', all(any(f'fx/prop/{t}' in x for x in r) for t in tags), r)
    # one display per projectile (kit on: the summon carries no item; one prop call per projectile)
    sm = [ln for k in files for body in files[k].values() for ln in body if 'summon minecraft:item_display' in ln]
    check('props: every projectile / prop is one item display (no second card)', all(ln.count('summon') == 1 for ln in sm), len(sm))


# ------------------------------------------------------------------------------------------------- 14 static
def sec_static():
    root = DP / 'data/rlk/function/boss/arlecchino/p'
    files = [f for k in api.P2 for f in (root / k).rglob('*.mcfunction')]
    txt = {f: f.read_text(encoding='utf-8') for f in files}
    check('static: no P2 file sets rlk_mb_inv', not [f for f, t in txt.items() if 'rlk_mb_inv' in t])
    neg = [(f.name, ln) for f, t in txt.items() for ln in t.split('\n') if re.search(r'scoreboard players (add|remove) \S+ \S+ -\d', ln)]
    check('static: no negative scoreboard add / remove literals', not neg, neg[:3])
    ids = [(f.name, m) for f, t in txt.items() for m in re.findall(r'(?:function|playsound) ([a-z0-9_.:/-]*[A-Z][^\s{]*)', t)]
    check('static: lowercase resource ids', not ids, ids[:3])
    snds = sorted({m for t in txt.values() for m in re.findall(r'playsound minecraft:([a-z0-9_.]+)', t)})
    check('static: vanilla sounds only (minecraft: namespace)', all(re.fullmatch(r'[a-z0-9_.]+', x) for x in snds), snds)
    texts = [(f.name, ln) for f, t in txt.items() for ln in t.split('\n') if ('tellraw' in ln or 'title @' in ln or '"text"' in ln)]
    check('static: no text (no tellraw / title / text components) in P2 files', not texts, texts[:3])
    check('static: S4 function count', True, len(files))
    print('S4 functions', len(files))


# ------------------------------------------------------------------------------------------------- renders
def render(key, s, log, path):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    tid = TID[key]
    hz = [h for h in s.hzr if h['pat'] == tid]
    W_, H_ = 640, 420
    img = Image.new('RGB', (W_, H_), (24, 24, 30))
    mp = Image.new('RGB', (430, 400), (24, 24, 30))      # the map panel (clipped), pasted at the left
    d = ImageDraw.Draw(mp)
    # whole arena (7 px / b) unless everything (hazards, her path, projectile legs) fits 11 b around its centre: then 15 px / b
    pts = [(h['pos'][0], h['pos'][2], (h['r'] or 0) / 10) for h in hz] + [(r['pos'][0], r['pos'][2], 0) for r in log]
    pts += [(p['pos'][0], p['pos'][2], p['macro']['life'] * p['macro']['spd'] / 10) for p in s.pjx if p['pat'] == tid]
    mx = sum(p[0] for p in pts) / len(pts)
    mz = sum(p[1] for p in pts) / len(pts)
    ext = max(math.hypot(p[0] - mx, p[1] - mz) + p[2] for p in pts)
    if ext <= 11:
        sc, ox, oz = 15.0, mx, mz
    else:
        sc, ox, oz = 7.0, CX, CZ
    cx, cz = 210, 210

    def P(x, z):
        return (cx + (x - ox) * sc, cz + (z - oz) * sc)
    d.ellipse([P(CX - api.WALK, CZ - api.WALK), P(CX + api.WALK, CZ + api.WALK)], outline=(90, 90, 100))
    d.ellipse([P(CX - api.MOVE_R, CZ - api.MOVE_R), P(CX + api.MOVE_R, CZ + api.MOVE_R)], outline=(60, 60, 70))
    pts = [P(r['pos'][0], r['pos'][2]) for r in log]
    if len(pts) > 1:
        d.line(pts, fill=(200, 200, 200), width=1)
    pl = s.player()
    d.ellipse([P(pl.pos[0] - 0.4, pl.pos[2] - 0.4), P(pl.pos[0] + 0.4, pl.pos[2] + 0.4)], fill=(90, 160, 255))
    t0 = log[0]['t'] - 1
    tmax = max([h['gt'] + h['tell'] - t0 for h in hz] + [1])
    rows = []
    for h in sorted(hz, key=lambda h: h['gt'] + h['tell']):
        t = h['gt'] + h['tell'] - t0
        k = t / max(1, tmax)
        bol = any(e['bol'] for e in P2.TABLE[key] if e['t'] == (h['sc'] or 0) + h['tell'])
        col = (int(200 + 55 * k), int(60 + 120 * (1 - k)), 40) if not bol else (int(150 + 100 * k), 20, int(40 + 40 * k))
        x, z = h['pos'][0], h['pos'][2]
        yaw = math.radians(h['yaw'])
        fx, fz = -math.sin(yaw), math.cos(yaw)
        r = (h['r'] or 0) / 10
        if h['kind'] == 1:
            d.ellipse([P(x - r, z - r), P(x + r, z + r)], outline=col, width=2)
        elif h['kind'] == 2:
            d.ellipse([P(x - r, z - r), P(x + r, z + r)], outline=col, width=2)
        elif h['kind'] == 3:
            a = h['a']
            pp = [P(x, z)] + [P(x - math.sin(yaw + math.radians(k2)) * r, z + math.cos(yaw + math.radians(k2)) * r)
                              for k2 in range(-a, a + 1, 5)] + [P(x, z)]
            d.line(pp, fill=col, width=2)
        elif h['kind'] == 4:
            hw = (h['hw'] or 0) / 20
            ax, az, bx, bz = x, z, x + fx * r, z + fz * r
            sx, sz = -fz * hw, fx * hw
            d.polygon([P(ax + sx, az + sz), P(bx + sx, bz + sz), P(bx - sx, bz - sz), P(ax - sx, az - sz)], outline=col)
        rows.append((t, h, col, bol))
    for p in s.pjx:
        if p['pat'] != tid:
            continue
        yaw = math.radians(p['rot'][0])
        ln = p['macro']['life'] * p['macro']['spd'] / 10 * 1.04
        x, z = p['pos'][0], p['pos'][2]
        d.line([P(x, z), P(x - math.sin(yaw) * ln, z + math.cos(yaw) * ln)], fill=(255, 170, 60) if 'rlk_kn_out' in p['tags'] or
               'rlk_kn_wheel' in p['tags'] else (160, 120, 60), width=1)
    img.paste(mp, (0, 0))
    d = ImageDraw.Draw(img)
    d.text((440, 8), f'{key} {EN[key]}', fill=(255, 255, 255))
    d.text((8, 404), f'{"zoom 15 px/b" if sc > 7 else "arena 7 px/b"}; grey: her path; blue: the player; crimson: Bond of Life',
           fill=(150, 150, 150))
    y = 26
    for t, h, col, bol in rows[:14]:
        kind = {1: 'disc', 2: 'ring', 3: 'sector', 4: 'line'}.get(h['kind'], '?')
        d.text((440, y), f't{t:>4} {kind:<6} r{(h["r"] or 0) / 10:.1f} {"BoL" if bol else ""}', fill=col)
        y += 13
    if len(rows) > 14:
        d.text((440, y), f'... {len(rows) - 14} more', fill=(160, 160, 160))
        y += 13
    npj = len([p for p in s.pjx if p['pat'] == tid])
    if npj:
        d.text((440, y), f'{npj} projectile legs (orange)', fill=(255, 170, 60))
    # side view: her height over time
    gx0, gy0, gw, gh = 440, 300, 190, 100
    d.rectangle([gx0, gy0, gx0 + gw, gy0 + gh], outline=(70, 70, 80))
    n = len(log)
    hp = [(gx0 + gw * i / max(1, n - 1), gy0 + gh - gh * (r['pos'][1] - CY) / api.AIR_MAX) for i, r in enumerate(log)]
    d.line(hp, fill=(220, 220, 220), width=1)
    d.text((gx0, gy0 - 14), f'height 0-{int(api.AIR_MAX)} b over {n} t', fill=(180, 180, 180))
    img.save(path)


def sec_render():
    RENDER.mkdir(parents=True, exist_ok=True)
    for key in api.P2:
        s = fresh()
        place(s, 9.0, 2.0) if key not in ('q1', 'q3', 'q5b') else place(s, 3.5)
        log, _ = run_pattern(s, key, each=T.heal_player)
        render(key, s, log, RENDER / f's4_{key}.png')


SECTIONS = {'hits': sec_hits, 'tells': sec_tells, 'geo': sec_geo, 'q5b': sec_q5b, 'beam': sec_beam, 'pj': sec_pj, 'q6': sec_q6,
            'q0': sec_q0, 'ends': sec_ends, 'cancel': sec_cancel, 'pause': sec_pause, 'stand': sec_stand, 'decals': sec_decals,
            'static': sec_static, 'render': sec_render}


def main():
    check('static: MOVE_R = walk - 1.5, LEAP_H of P2 <= AIR_MAX', api.MOVE_R == api.WALK - 1.5
          and max(api.LEAP_H[k] for k in ('q0', 'q4', 'q6')) <= api.AIR_MAX)
    for name, f in SECTIONS.items():
        if not ONLY or name in ONLY:
            f()
    summary('pat_p2')


main()
