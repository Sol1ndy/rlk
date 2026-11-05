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
"""
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
import hrsim as H  # noqa: E402

ARGS = sys.argv[1:]
DP = Path(ARGS[0]).resolve()
SECTIONS = ARGS[1:] or ['table', 'hits', 'quiet', 'ends', 'cancel']
sys.path.insert(0, str(DP / 'tools'))
import mboss_scarlet.api as API  # noqa: E402
import mboss_scarlet.p1 as P1  # noqa: E402
import mboss_scarlet.s3lib as S3  # noqa: E402
check = H.ck
FN = DP / 'data/rlk/function/boss/scarlet'
C = (API.CX, API.CY, API.CZ)
KIND = {'disc': 1, 'pdisc': 1, 'sector': 3, 'line': 4, 'dash_line': 4}
KEYS = [k for k in API.P1]
END = {k: API.ev(k, 'end') if k != 'a6' else API.A6_TRIGGER['next'] for k in KEYS}


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


def main():
    try:
        for sec in SECTIONS:
            {'table': sec_table, 'hits': sec_hits, 'quiet': sec_quiet, 'ends': sec_ends, 'cancel': sec_cancel}[sec]()
    finally:
        if 'v' in VAR:
            H.drop_variant(VAR.pop('v'))
    return H.summary('pat_p1')


if __name__ == '__main__':
    sys.exit(main())
