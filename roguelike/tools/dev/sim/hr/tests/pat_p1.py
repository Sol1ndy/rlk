#!/usr/bin/env python3
"""pat_p1.py: the phase-1 patterns of 홍련 (Scarlet), stage S3 (scratchpad hr/PLAN.md §4.3, §9.3; contract §3.5):
A1, A2, A3, A4 + A5, A6, A9, A10 (tools/mboss_scarlet/p1.py) in the sim on a variant with her enabled.

    python3 pat_p1.py <datapack root> [section ...]

Run it from HR/tests: the tree is only read; the variant (her registry entry forced enabled, the core regenerated, a real
copy of F:boss/scarlet) lives in ./tmp and is removed at the end.

  table   p1.TABLE (a dry build of p1.py) = api.HITS: every hit tick = its clip event (api.ev), the HITS order, shapes,
          tiers, kb; the tell from the first visible motion >= TELL_MIN 12 (T3 / yellow >= TELL_BIG 20); successive hits of
          a chain >= COMBO_GAP 10 apart; no turn command inside the LOCK_LEAD 7 ticks before a hit (static, p/<k>/tick)
  hits    the sim (several player spots): each hazard is made at pattern tick event - 1 with tell 1 (so it strikes on the
          event tick), the player is hit only on event ticks, one landing per strike group; shapes / sizes / tiers / kb /
          Electro of every hazard as api.HITS; the aim (yaw, the locked spot) unchanged over the 7 ticks before each hit
  quiet   every hazard #hzQuiet 1 + #hzSfx 0; no outline / flash particle of the framework's hazards, no display entity
          or block placed by a pattern (no floor decal); hz_vis does nothing
  ends    from 9 player spots x 3 seeds (and a column of stone where her moves would end): every tick of every pattern the
          body is <= MOVE_R from C, every end point (landing, dash end, blink, the pattern end) passes mv/ok (free feet /
          head, never in a block), she is on the floor at the end, no glide left
  cancel  a cancel (core/cancel_pat, the reload / test path) at every pattern tick 0..end: no rlk_hr_* entity of the
          pattern (hazards, lock, probe, A9 start marker), no glide, on the floor, #pat 0, no later hit on the player
  f1      F1 (11-05 review fixes, the lead's decisions): HR-14 every P1-kit pattern ends 8-12 t after its last hit (A1 24,
          A2 22, A3 79, A4 46, A9 40, A10 32) and she turns to the player on every tick of the tail kept (static + sim)
          and moves as the recovery does from 4 t after the last hit (A4: the landing), the recovery keeping that move
          (F1 round 1; static + sim); HR-22 A2's lilac blade glow 6-11, off at the hit and in its cancel (static + sim);
          HR-28 A4's leap and A10's spring / dive leave the afterimage trail along the motion in both phases (+ A10's dive
          line toward the lock), A3 / A6 / A9's afterimage stays P2-only (static + a P1 sim); HR-13 / HR-14 / HR-18 the
          package's numbers in the generated AI (recovery P1 12-20 / P2 10-16 t, A9 / A10 cooldowns, the P1 near pick with
          A1 / A2 / A10)
"""
import math
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
import hrsim as H  # noqa: E402

ARGS = sys.argv[1:]
DP = Path(ARGS[0]).resolve()
SECTIONS = ARGS[1:] or ['table', 'hits', 'quiet', 'ends', 'cancel', 'f1']
sys.path.insert(0, str(DP / 'tools'))
import mboss_scarlet.api as API  # noqa: E402
import mboss_scarlet.p1 as P1  # noqa: E402
import mboss_scarlet.s3lib as S3  # noqa: E402
check = H.ck
FN = DP / 'data/rlk/function/boss/scarlet'
C = (API.CX, API.CY, API.CZ)
KIND = {'disc': 1, 'pdisc': 1, 'sector': 3, 'line': 4, 'dash_line': 4}
KEYS = [k for k in API.P1]
# F1 (HR-14): a P1-kit pattern ends at api.PAT_END (8-12 t after its last hit), no longer at its clip's end
END = {k: getattr(API, 'PAT_END', {}).get(k, API.ev(k, 'end')) if k != 'a6' else API.A6_TRIGGER['next'] for k in KEYS}


class Dry:
    """A Writer stand-in for a dry build of p1.py (fills p1.TABLE / MOVES, writes nothing)."""

    def __init__(self):
        self.files = {}

    def w(self, rel, body):
        self.files[rel] = list(body)


DRY = Dry()
for _k in KEYS:
    P1.BUILD[_k](DRY)


def big(h):
    return h['tier'] in ('T3', 'T4')


def fn_lines(rel):
    p = FN / (rel + '.mcfunction')
    return p.read_text(encoding='utf-8').split('\n') if p.exists() else []


# ================================================================================================= table (static)
def sec_table():
    for k in KEYS:
        hs = P1.TABLE[k]
        exp = [(API.ev(c, e), shape, dims, tier, kb) for c, e, shape, dims, tier, kb in API.HITS[k]]
        got = [(h['t'], h['shape'], tuple(h['dims']), h['tier'], h['kb']) for h in sorted(hs, key=lambda h: (h['t'], h['idx']))]
        check(f'T1 {k}: the recorded hits = api.HITS (tick = clip event, shape, dims, tier, kb)', got == [(a, b, tuple(c), d, e) for a, b, c, d, e in exp],
              (got, exp))
        bad = [(h['t'], h['tell']) for h in hs if h['t'] - h['tell'] < (API.TELL_BIG if big(h) else API.TELL_MIN)]
        check(f'T2 {k}: every tell >= {API.TELL_MIN} t ({API.TELL_BIG} for T3 / T4)', not bad, bad)
        ts = sorted({h['t'] for h in hs})
        gaps = [b - a for a, b in zip(ts, ts[1:])]
        check(f'T3 {k}: successive hits >= {API.COMBO_GAP} t apart', all(g >= API.COMBO_GAP for g in gaps), gaps)
        # no turn / face / tp-rotation command on the LOCK_LEAD ticks before each hit (p/<k>/tick + k/<t> + start)
        turns = set()
        for ln in fn_lines(f'p/{k}/tick'):
            if 'mv/turn' in ln or 'mv/face' in ln:
                rr = ln.split('matches ')[1].split(' ')[0]
                a, _, b = rr.partition('..')
                turns.update(range(int(a), int(b or a) + 1))
        for t in range(1, END[k] + 1):
            body = '\n'.join(fn_lines(f'p/{k}/k/{t}'))
            if 'mv/turn' in body or 'mv/face' in body or ('facing entity' in body and 'run tp @s ~ ~ ~ ~ 0' in body):
                turns.add(t)
        lock_bad = [(h['t'], sorted(turns & set(range(h['t'] - API.LOCK_LEAD + 1, h['t'] + 1)))) for h in hs
                    if turns & set(range(h['t'] - API.LOCK_LEAD + 1, h['t'] + 1))]
        check(f'T4 {k}: no turn in the {API.LOCK_LEAD} ticks before a hit (the aim locks at hit - {API.LOCK_LEAD} or earlier)', not lock_bad,
              lock_bad)
        check(f'T5 {k}: p/{k}/{{start,tick,cancel}} exist; #done at its end tick {END[k]}',
              all((FN / f'p/{k}/{f}.mcfunction').exists() for f in ('start', 'tick', 'cancel'))
              and any(f'matches {END[k]} run scoreboard players set #done hr 1' in ln for ln in fn_lines(f'p/{k}/tick')))
    check('T6 A6 has no hit (a blink + line 12)', P1.TABLE['a6'] == [] and API.HITS['a6'] == [])
    check('T7 A9: one strike group (dash line + the disc at the locked spot, the same tick)',
          len({h['grp'] for h in P1.TABLE['a9']}) == 1 and len({h['t'] for h in P1.TABLE['a9']}) == 1)


# ================================================================================================= the sim runs
VAR = {}


def var():
    if 'v' not in VAR:
        VAR['v'] = H.variant_hr(DP, H.enable_scarlet, label='pat_p1')
    return VAR['v']


def world(seed=5):
    s, pl = H.setup_sc(var(), seed=seed)
    ok = H.fight_sc(s, intro=False)
    H.run_sc(s, 2)
    assert ok
    return s, pl


SPOTS = [(880.5, 14.0), (883.5, 12.0), (876.0, 10.0), (880.0, 2.0), (889.0, 8.0), (880.0, 9.5), (898.0, 8.0),
         (880.0, 28.0), (866.0, -6.0)]
BODY_AT = {(898.0, 8.0): (893.0, 8.0), (880.0, 28.0): (880.0, 22.0), (866.0, -6.0): (870.0, -2.0)}


def run_pattern(s, key, ppos, bpos=None, byaw=None, cancel_at=None, extra=0, stone=None):
    """Start key at the body (bpos, facing the player unless byaw), the player at ppos (kept there); run until #pat 0
    (+ extra ticks) or cancel at pattern tick cancel_at. Returns a record."""
    if stone:
        for (x, y, z) in stone:
            s.setb(x, y, z, 'minecraft:stone')
    H.place_player(s, *ppos)
    H.place_body(s, *(bpos or (C[0], C[2])), yaw=byaw)
    n0, p0 = len(s.hzr), len(s.phits)
    H.start_pattern(s, S3.TID[key])
    t0 = s.t
    snaps = [H.snap(s)]
    cancelled = False
    for _ in range(END[key] + 40):
        H.heal(s)
        pl = s.player()
        pl.pos = [float(ppos[0]), 201.0, float(ppos[1])]
        if cancel_at is not None and not cancelled and (H.hr(s, '#pt') or 0) >= cancel_at:
            H.call_sc(s, 'core/cancel_pat')
            H.hold(s, True)
            cancelled = True
            snaps.append(H.snap(s))
            break
        H.world_sc(s)
        snaps.append(H.snap(s))
        if (H.hr(s, '#pat') or 0) == 0:
            break
    for _ in range(extra):
        H.heal(s)
        H.world_sc(s)
    return dict(t0=t0, snaps=snaps, hz=s.hzr[n0:], ph=s.phits[p0:], cancelled=cancelled)


def expected(key):
    return sorted((API.ev(c, e), shape) for c, e, shape, *_ in API.HITS[key])


def hz_match(h, hit):
    c, e, shape, dims, tier, kb = hit
    ok = h['kind'] == KIND[shape] and h['dmg'] == API.DMG[tier] and h['kb'] == kb and h['el'] == API.ELEC and h['tell'] == 1
    if shape in ('disc', 'pdisc'):
        ok = ok and h['r'] == round(dims[0] * 10)
    elif shape == 'sector':
        ok = ok and h['r'] == round(dims[0] * 10) and h['a'] == dims[1]
    elif shape == 'line':
        ok = ok and h['r'] == round(dims[0] * 10) and h['hw'] == round(dims[1] * 10)
    elif shape == 'dash_line':
        ok = ok and h['hw'] == round(dims[0] * 10) and h['r'] >= 5
    return ok


def sec_hits():
    for k in KEYS:
        for seed, spot in ((5, SPOTS[0]), (6, SPOTS[1]), (7, SPOTS[3])):
            s, pl = world(seed)
            r = run_pattern(s, k, spot, extra=6)
            made = sorted((h['pt'] + 1, h['kind']) for h in r['hz'])
            exp = sorted((t, KIND[sh]) for t, sh in expected(k))
            check(f'H1 {k} @ {spot}: every hazard made at pattern tick event - 1 with tell 1 (strike = the clip event)',
                  made == exp and all(h['tell'] == 1 for h in r['hz']), (made, exp))
            hits = sorted(t - r['t0'] for t, *_ in r['ph'])
            evs = {t for t, _ in expected(k)}
            check(f'H2 {k} @ {spot}: the player is hit only on event ticks, at most once per strike',
                  set(hits) <= evs and len(hits) == len(set(hits)), (hits, sorted(evs)))
            order = sorted(r['hz'], key=lambda h: (h['pt'], h['kind'] != 4))
            hits_def = sorted(API.HITS[k], key=lambda x: (API.ev(x[0], x[1]), KIND[x[2]] != 4))
            check(f'H3 {k} @ {spot}: shapes / sizes / tiers / kb / Electro as api.HITS',
                  len(order) == len(hits_def) and all(hz_match(h, d) for h, d in zip(order, hits_def)),
                  [(h['kind'], h['r'], h['a'], h['hw'], h['dmg'], h['kb'], h['el']) for h in order])
            # the aim: yaw unchanged over the LOCK_LEAD ticks before each hit; a locked spot fixed over them
            sn = {x['pt']: x for x in r['snaps'] if x['pat'] == S3.TID[k]}
            bad = []
            for h in r['hz']:
                t = h['pt'] + 1
                a = sn.get(t - API.LOCK_LEAD)
                b = sn.get(t - 1)
                if a and b and h['kind'] in (3, 4) and abs(((a['yaw'] - b['yaw']) + 180) % 360 - 180) > 0.01:
                    bad.append(('yaw', t, a['yaw'], b['yaw']))
                if a and b and h['kind'] == 1 and k in ('a4', 'a10', 'a9') and t == API.ev(k, 'hit' if k != 'a9' else 'cut') \
                        and (a['lock'] is None or a['lock'] != b['lock']):
                    bad.append(('lock', t, a['lock'], b['lock']))
            check(f'H4 {k} @ {spot}: the aim (yaw / locked spot) fixed over the {API.LOCK_LEAD} ticks before each hit', not bad, bad)
    # one landing per group: A9's line + disc (same group) hit a player standing in both once
    s, pl = world(9)
    r = run_pattern(s, 'a9', (880.5, 14.0), extra=4)
    check('H5 A9: the dash line and the disc (one group) land once on a player inside both', len(r['ph']) == 1, r['ph'])


def sec_quiet():
    allhz = []
    for k in KEYS:
        s, pl = world(11)
        n_part = len(s.particles)
        r = run_pattern(s, k, SPOTS[0], extra=8)
        allhz += r['hz']
        check(f'Q1 {k}: every hazard quiet (#hzQuiet 1) and silent (#hzSfx 0)',
              all(h['quiet'] == 1 and h['sfx'] == 0 for h in r['hz']), [(h['quiet'], h['sfx']) for h in r['hz']])
        # I1: exactly the pattern tags rlk_hr_p / rlk_hr_p_<key> (the real rig's parts carry rlk_hr_part)
        ents = [e for e in s.ents if e.alive and e.etype in ('block_display', 'text_display', 'item_display')
                and any(t == 'rlk_hr_p' or t.startswith('rlk_hr_p_') for t in e.tags)]
        check(f'Q2 {k}: no display entity of the pattern (no decal), no particle of the framework hazard functions (no outline / flash)',
              not ents and not s.hz_particles, (ents, s.hz_particles[:4]))
    text = '\n'.join((FN / f).read_text(encoding='utf-8') for f in [p.relative_to(FN) for p in (FN / 'p').rglob('*.mcfunction')])
    check('Q3 no setblock / fill / block_display / text_display in any P1 pattern file (no floor decal)',
          not any(w in text for w in ('setblock ', 'fill ', 'block_display', 'text_display')))
    hv = [ln for ln in fn_lines('hz_vis') if ln.strip() and not ln.startswith('#')]
    check('Q4 hz_vis: no command (the framework draws nothing for her quiet hazards)', hv == [], hv)


def mv_ok(s, pos):
    return s.call('rlk:mboss/mv/ok', H.Ctx(None, (pos[0], pos[1], pos[2]), (0.0, 0.0))) == 1


def sec_ends():
    worst = 0.0
    n = 0
    for k in KEYS:
        for seed in (21, 22, 23):
            for spot in SPOTS:
                s, pl = world(seed)
                bpos = BODY_AT.get(spot)
                r = run_pattern(s, k, spot, bpos=bpos, extra=0)
                n += 1
                d = max(math.hypot(x['pos'][0] - C[0], x['pos'][2] - C[2]) for x in r['snaps'])
                worst = max(worst, d)
                last = r['snaps'][-1]
                b = H.body_of(s)
                check(f'E1 {k} seed {seed} @ {spot}: inside MOVE_R every tick; ends on the floor, mv/ok there, no glide',
                      d <= API.MOVE_R + 1e-6 and abs(b.pos[1] - C[1]) < 1e-6 and mv_ok(s, b.pos) and 'rlk_mb_mv' not in b.tags
                      and last['pat'] == 0, (round(d, 2), b.pos, sorted(b.tags)))
    # a stone column where the moves would end: never inside a block (mv/ok refuses the spot)
    stone = [(x, y, z) for x in range(876, 886) for z in range(14, 20) for y in (201, 202)]
    for k in KEYS:
        s, pl = world(31)
        r = run_pattern(s, k, (880.5, 13.0), bpos=(880.0, 6.0), stone=stone)
        inside = [x['pos'] for x in r['snaps'] if (math.floor(x['pos'][0]), 201, math.floor(x['pos'][2])) in set(stone)]
        b = H.body_of(s)
        check(f'E2 {k}: a stone wall behind the player: she never stands in a block; the end spot passes mv/ok',
              not inside and mv_ok(s, b.pos), (inside[:3], b.pos))
    print(f'  ends: {n} runs, the farthest body point {worst:.2f} b from C (MOVE_R {API.MOVE_R})')


NOT_PATTERN = {'rlk_hr_anchor', 'rlk_hr_deco', 'rlk_hr_part', 'rlk_hr_shadow', 'rlk_hr_stage'}


def sec_cancel():
    for k in KEYS:
        bad = []
        for t in range(0, END[k] + 1):
            s, pl = world(41 + t % 3)
            r = run_pattern(s, k, SPOTS[0], cancel_at=t, extra=0)
            pre = len(s.phits)
            # I1: the real rig's own entities (parts, shadow, anchor) and a finished sequence's staging marker (S2b: kept
            # until the next sequence / cleanup) are not the pattern's
            left = [tg for _, tg in H.ents_tagged(s, 'rlk_hr_') if not set(tg) & NOT_PATTERN]
            hz = [e for e in s.ents if e.alive and 'rlk_mb_hz' in e.tags]
            b = H.body_of(s)
            H.run_sc(s, 30, each=H.heal)
            later = [x for x in s.phits[pre:] if x[3] == S3.TID[k]]
            if left or hz or 'rlk_mb_mv' in b.tags or abs(b.pos[1] - C[1]) > 1e-6 or H.hr(s, '#pat') not in (0, None) or later:
                bad.append((t, left[:2], len(hz), b.pos[1], sorted(b.tags & {'rlk_mb_mv'}), H.hr(s, '#pat'), later[:1]))
        check(f'C1 {k}: a cancel at every tick 0..{END[k]} leaves no pattern entity / hazard / glide, her on the floor, no later hit',
              not bad, bad[:4])


# ================================================================================================= F1 (11-05 review fixes)
# The lead's decisions (HR/review/findings.md, 11-05): every P1-kit pattern ends 8-12 t after its last hit at these ticks
# (D5-01's ends) and she turns to the player in the tail kept (HR-14); A2's lilac blade glow 6-11 (HR-22); A4's leap and
# A10's spring / dive leave a trail along the motion in both phases, A3 / A6 / A9's afterimage stays P2-only (HR-28).
# Written so that they fail on the 4c81817 tree (no new api names needed).
F1_END = {'a1': 24, 'a2': 22, 'a3': 79, 'a4': 46, 'a9': 40, 'a10': 32}
# F1 round 1 (HR-14, VF1R-01: "during any tail kept ... she walks / strafes facing and tracking the player"): her tail move
# starts 4 t after the last hit (A4: at its landing 38), one step each later tick to the end
F1_TAIL = {'a1': 18, 'a2': 16, 'a3': 73, 'a4': 38, 'a9': 32, 'a10': 26}
MOVE_CLIPS = ('play/walk', 'play/glide', 'play/strafe_l', 'play/strafe_r')
F1_TRAIL = {'a4': [2, 4, 6], 'a10': [2, 5, 8, 20, 21]}
F1_P2ONLY = {'a3': 1, 'a6': 0, 'a9': API.ev('a9', 'go')}


def done_tick(k):
    for ln in fn_lines(f'p/{k}/tick'):
        m = re.search(r'matches (\d+) run scoreboard players set #done hr 1', ln)
        if m:
            return int(m.group(1))
    return None


def turn_ticks(k):
    """The pattern ticks with a turn of the body (mv/turn, mv/face, a facing tp) in p/<k>/tick or its k/<t>."""
    out = set()
    for ln in fn_lines(f'p/{k}/tick'):
        if 'mv/turn' in ln or 'mv/face' in ln:
            rr = ln.split('matches ')[1].split(' ')[0]
            a, _, b = rr.partition('..')
            out.update(range(int(a), int(b or a) + 1))
    for t in range(1, 120):
        body = '\n'.join(fn_lines(f'p/{k}/k/{t}'))
        if 'mv/turn' in body or 'mv/face' in body:
            out.add(t)
    return out


def calls_at(k, t, needle):
    """The command lines of pattern tick t of p/<k> (inline in p/<k>/tick or in k/<t>; t 0 = start) containing needle."""
    lines = fn_lines(f'p/{k}/start') if t == 0 else (
        [ln for ln in fn_lines(f'p/{k}/tick') if re.search(rf'#pt hr matches {t}(?=\s)', ln)] + fn_lines(f'p/{k}/k/{t}'))
    return [ln for ln in lines if needle in ln and not ln.startswith('#')]


def call_ticks(k, name):
    """The pattern ticks whose p/<k>/tick lines (single ticks or ranges) or k/<t> files call function boss/scarlet/<name>
    (exactly that function)."""
    out, pat = set(), re.compile(rf'function rlk:boss/scarlet/{re.escape(name)}$')
    for ln in fn_lines(f'p/{k}/tick'):
        m = re.match(r'execute if score #pt hr matches (\d+)(?:\.\.(\d+))? run (.*)$', ln)
        if m and pat.search(m.group(3)):
            out.update(range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1))
    for t in range(1, 120):
        if any(pat.search(ln) for ln in fn_lines(f'p/{k}/k/{t}') if not ln.startswith('#')):
            out.add(t)
    return out


def p2_gated(ln):
    return '#ph hr matches 7' in ln.split(' run ')[0]


def yaw_err(snap, ppos):
    b = snap['pos']
    want = math.degrees(math.atan2(-(ppos[0] - b[0]), ppos[1] - b[2])) % 360
    return abs((snap['yaw'] - want + 180) % 360 - 180)


def sec_f1():
    # HR-14: the ends and the tail (static)
    for k, want in F1_END.items():
        last = max(h['t'] for h in P1.TABLE[k])
        end = done_tick(k)
        check(f'F1 HR-14 {k}: the pattern ends 8-12 t after its last hit, at {want} ({last} -> {end})',
              end == want and 8 <= end - last <= 12, (last, end))
        tr = turn_ticks(k)
        miss = [t for t in range(last + 1, end) if t not in tr] if end else ['no #done']
        check(f'F2 HR-14 {k}: she turns to the player on every tick of the tail kept ({last + 1}..{(end or 1) - 1})',
              end is not None and not miss, miss)
    # HR-14 in the sim: the pattern is over at its end tick, and in the tail she tracks a player who circles her at 0.2 b/t from
    # her last hit on: her aim error shrinks by >= 5 deg / t until it is <= 12 deg and stays there (mv/turn 10 deg / t)
    for k, want in F1_END.items():
        s, pl = world(61)
        H.place_player(s, C[0] + 3.0, C[2] + 2.5)
        H.place_body(s, C[0], C[2] - 1.0)
        H.start_pattern(s, S3.TID[k])
        last = max(h['t'] for h in P1.TABLE[k])
        errs, ended = [], None
        for _ in range(140):
            H.heal(s)
            pt = H.hr(s, '#pt') or 0
            p, b = s.player(), H.body_of(s)
            if pt >= last:
                d = max(2.0, math.hypot(p.pos[0] - b.pos[0], p.pos[2] - b.pos[2]))
                a = math.atan2(p.pos[2] - b.pos[2], p.pos[0] - b.pos[0]) + 0.2 / d
                p.pos = [b.pos[0] + d * math.cos(a), 201.0, b.pos[2] + d * math.sin(a)]
                H.C.moved(s)
            H.world_sc(s)
            if (H.hr(s, '#pat') or 0) != S3.TID[k]:
                ended = pt + 1
                break
            if pt + 1 > last:
                errs.append(yaw_err(H.snap(s), (s.player().pos[0], s.player().pos[2])))
        ok = ended == want and errs and all(y <= max(x - 5.0, 12.0) for x, y in zip(errs, errs[1:]))
        check(f'F3 HR-14 {k} (sim): over at pattern tick {want}; in the tail she tracks a player circling her (aim error shrinks '
              f'to <= 12 deg and stays)', ok, (ended, [round(e, 1) for e in errs]))
    # HR-14 (F1 round 1, VF1R-01): in the tail she also moves as the recovery does - the recovery's move and clip at
    # last hit + 4 (A4: the landing), one step on every later tick to the end - and the recovery keeps that move
    for k, t0 in F1_TAIL.items():
        end = done_tick(k)
        st, sp = call_ticks(k, 'ai/tail'), call_ticks(k, 'ai/tail_step')
        want = set(range(t0 + 1, end or 0))
        check(f'F12 HR-14 {k}: the tail move: ai/tail at {t0} (the recovery\'s move + clip), ai/tail_step on {t0 + 1}..{(end or 1) - 1}',
              end is not None and st == {t0} and sp == want, (sorted(st), sorted(sp - want), sorted(want - sp)))
    for k, t0 in F1_TAIL.items():
        s, pl = world(65)
        n0 = len(s.rigl)
        ppos = (C[0] + 3.0, C[2] + 2.5)
        r = run_pattern(s, k, ppos, bpos=(C[0], C[2] - 1.0))
        end = F1_END[k]
        sn = {x['pt']: x for x in r['snaps'] if x['pat'] == S3.TID[k]}
        plays = [(t - r['t0'], c) for t, c in s.rigl[n0:] if c.startswith('play/') and t - r['t0'] > t0 - 4]
        mv0 = H.hr(s, '#ai_mv')
        # the recovery after the end, the AI free: she keeps the move (no new clip) and goes on moving
        H.hold(s, False)
        p_end = H.body_of(s).pos[:]
        for _ in range(3):
            H.heal(s)
            s.player().pos = [float(ppos[0]), 201.0, float(ppos[1])]
            H.world_sc(s)
        later = [(t - r['t0'], c) for t, c in s.rigl[n0:] if c.startswith('play/') and t - r['t0'] >= end]
        moved = math.hypot(sn[end - 1]['pos'][0] - sn[t0]['pos'][0], sn[end - 1]['pos'][2] - sn[t0]['pos'][2]) \
            if t0 in sn and end - 1 in sn else 0.0
        on = math.hypot(H.body_of(s).pos[0] - p_end[0], H.body_of(s).pos[2] - p_end[2])
        ok = (plays[:1] and plays[0][0] == t0 and plays[0][1] in MOVE_CLIPS and moved >= 0.08 * (end - 1 - t0)
              and not later and H.hr(s, '#ai_mv') == mv0 and on >= 0.2)
        check(f'F13 HR-14 {k} (sim): from {t0} a move clip and she moves in the tail (>= 0.08 b / t); the recovery keeps the move '
              '(no new clip, still moving)', ok, (plays[:2], round(moved, 2), later[:2], mv0, H.hr(s, '#ai_mv'), round(on, 2)))
    # HR-22: A2's lilac blade glow from its 'glow' event to the hit, and off in its cancel (A6 may cancel the windup)
    glow, hit = API.ev('a2', 'glow'), API.ev('a2', 'hit')
    on = calls_at('a2', glow, 'rig/look/blade/lilac')
    off = calls_at('a2', hit, 'rig/look/blade/off')
    can = [ln for ln in fn_lines('p/a2/cancel') if 'rig/look/blade/off' in ln and 'rlk_mb_body' in ln]
    check(f'F4 HR-22 A2: rig look/blade/lilac at {glow} (the clip\'s glow event), off at the hit {hit}, off in p/a2/cancel (as the body)',
          len(on) == 1 and len(off) == 1 and len(can) == 1, (on, off, can))
    s, pl = world(62)
    n0 = len(s.rigl)
    r = run_pattern(s, 'a2', SPOTS[0], extra=0)
    got = [(t - r['t0'], c) for t, c in s.rigl[n0:] if c.startswith('look/blade/')]
    check('F5 HR-22 A2 (sim): the blade glows lilac from tick 6 to the hit 12', got == [(glow, 'look/blade/lilac'), (hit, 'look/blade/off')],
          got)
    s, pl = world(63)
    n0 = len(s.rigl)
    r = run_pattern(s, 'a2', SPOTS[0], cancel_at=glow + 2)
    got = [c for t, c in s.rigl[n0:] if c.startswith('look/blade/')]
    check('F6 HR-22 A2 cancelled while it glows (tick 8): the blade glow is turned off', got[-1:] == ['look/blade/off'] and
          'look/blade/lilac' in got, got)
    # HR-28: the trails (static: ungated afterimage calls at the move ticks; A10's dive line toward the lock; P2-only kept)
    for k, ticks in F1_TRAIL.items():
        bad = [t for t in ticks if not [ln for ln in calls_at(k, t, 'fx/p/afterimage') if not p2_gated(ln)]]
        check(f'F7 HR-28 {k}: the afterimage trail at pattern ticks {ticks} in both phases (not gated on #ph 7)', not bad, bad)
    dl = calls_at('a10', API.ev('a10', 'dive'), 'fx/p/qi_line')
    check('F8 HR-28 A10: the dive trail line at its dive tick, from her toward the locked spot (facing the lock marker)',
          len(dl) == 1 and 'facing entity @e[type=minecraft:marker,tag=rlk_hr_lock' in dl[0], dl)
    bad = [(k, t) for k, t in F1_P2ONLY.items() if not calls_at(k, t, 'fx/p/afterimage')
           or any(not p2_gated(ln) for ln in calls_at(k, t, 'fx/p/afterimage'))]
    check('F9 HR-28 the afterimage of A3 (glide) / A6 (blink) / A9 (dash) stays P2-only (PLAN §4.4)', not bad, bad)
    # HR-28 in the sim (P1): the trail calls at those ticks while her body rises (A4 leap, A10 spring) / falls (A10 dive)
    for k, ticks in F1_TRAIL.items():
        s, pl = world(64)
        k0 = len(s.kitl)
        r = run_pattern(s, k, (C[0] + 0.5, C[2] + 8.0), bpos=(C[0], C[2] - 1.0), extra=0)
        sn = {x['pt']: x for x in r['snaps'] if x['pat'] == S3.TID[k]}
        got = sorted({t - r['t0'] for t, sub, _a in s.kitl[k0:] if sub == 'p/afterimage'})
        ys = [sn[t]['pos'][1] for t in ticks if t in sn]
        rise = ys[:3]
        ok = got == ticks and all(b > a for a, b in zip(rise, rise[1:])) and (k != 'a10' or ys[4] < ys[3])
        check(f'F10 HR-28 {k} in P1 (sim): the afterimage at pattern ticks {ticks} along her motion (rising{", then diving" if k == "a10" else ""})',
              ok, (got, [round(y, 2) for y in ys]))
    # HR-13 / HR-14 / HR-18 (the package's numbers, lead decision 11-05) in the generated AI: the recovery P1 12-20 t / P2 10-16 t,
    # A9 / A10 cooldowns 160 / 140 and 180 / 150, the P1 near pick with A1 10, A2 10 and A10 20
    p1, p2 = API.PH['p1'], API.PH['p2']
    want = {'ai/rec_start': [f'execute if score #ph hr matches {p1} store result score #rec hr run random value 12..20',
                             f'execute if score #ph hr matches {p2} store result score #rec hr run random value 10..16'],
            'core/start/a9': [f'execute if score #ph hr matches {p1} run scoreboard players add #cd_a9 hr 160',
                              f'execute if score #ph hr matches {p2} run scoreboard players add #cd_a9 hr 140'],
            'core/start/a10': [f'execute if score #ph hr matches {p1} run scoreboard players add #cd_a10 hr 180',
                               f'execute if score #ph hr matches {p2} run scoreboard players add #cd_a10 hr 150'],
            'ai/pick/p1_near': ['scoreboard players set #ai_wa1 hr 10', 'scoreboard players set #ai_wa2 hr 10',
                                'scoreboard players set #ai_wa10 hr 20']}
    miss = [(rel, ln) for rel, lns in want.items() for ln in lns if ln not in fn_lines(rel)]
    check('F11 HR-13 / HR-14 / HR-18 the package in the AI: recovery P1 12-20 / P2 10-16 t, A9 160 / 140, A10 180 / 150 t, '
          'the P1 near pick A1 10 / A2 10 / A10 20', not miss, miss[:4])


def main():
    try:
        for sec in SECTIONS:
            {'table': sec_table, 'hits': sec_hits, 'quiet': sec_quiet, 'ends': sec_ends, 'cancel': sec_cancel, 'f1': sec_f1}[sec]()
    finally:
        if 'v' in VAR:
            H.drop_variant(VAR.pop('v'))
    return H.summary('pat_p1')


if __name__ == '__main__':
    sys.exit(main())
