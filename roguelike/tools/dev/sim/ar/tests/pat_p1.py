#!/usr/bin/env python3
"""pat_p1.py (S3): the phase-1 patterns of 아를레키노 in the knsim world (S:ar/s3/lib/knsim.py; PLAN §5, §11.3).

    python3 pat_p1.py [<roguelike dir>] [key ...]

Per pattern (a2 a4 a5 b1 b2 c1 c2 d1 d2 e1 f1 g1 h1 e70), started by core/start/<key> with the AI held, for several
player placements (near / mid / far / at the arena edge behind her):
 1 every hazard strikes on the tick of its api.HITS clip event (creation #pt + tell), and every HITS entry strikes
   (the dash line at 'go'); shapes (kind, radius / length / width / back / half angle), tiers (api.dmg), Pyro, quiet
 2 Bond of Life: every bol hazard carries the FN-1 option #hzBol = BOL_HIT, a plain one none (I1: FN-1 live)
 3 knockback: only the last hit of a cast pushes (KB_FINAL), the rest KB_CHAIN
 4 tells: first visible motion -> hit >= TELL_MIN (>= TELL_BIG for big hits), combo follow-ups >= COMBO_GAP apart
   (except inside one volley group: one landing)
 5 end points / heights: the body inside MOVE_R of the axis every tick, between the floor and AIR_MAX, on the floor at
   the end; mv/ok for every landing (the sim's arena is open floor: the in-block half is the game's mv/ok)
 6 projectiles (b1 / b2): speed, radius, height, out + back legs (separate volley groups), the back leg ends at her
 7 a standing player (no dash) is hit by every swing of the A strings (re-face + step in), from 3 b and from 6 b
 8 decals only for the PLAN §1.5 keys (a kit-on dry build: api.K forced on, every fx/decal call per pattern)
 9 cancel at every tick leaves nothing (markers, props, hazards, glide, window, airborne body)
Renders: AR/renders/s3_<key>.png (top-down hit shapes over time, from the recorded hazards).
"""
import copy
import math
import re
import sys
from pathlib import Path

SCR = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad')
sys.path.insert(0, str(SCR / 'ar/s3/lib'))
import knsim as T  # noqa: E402
from mcsim import Ctx  # noqa: E402

check, summary = T.check, T.summary
DP = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].isalpha() and '/' in sys.argv[1] else T.DEFAULT_DP
ONLY = [a for a in sys.argv[1:] if '/' not in a]
KIND = {'disc': 1, 'disc_ahead': 1, 'ring': 2, 'sector': 3, 'line': 4, 'dash_line': 4, 'full': 5}
RENDER = SCR / 'ar/renders'
EN = {'a2': 'normal string 2', 'a4': 'normal string 4', 'a5': 'normal string 5', 'b1': 'scythe throw', 'b2': 'throw x2 + grab',
      'c1': 'leap slash', 'c2': 'leap + wing', 'd1': 'blood dash', 'd2': 'dash + follow', 'e1': 'aerial zig-zag',
      'f1': 'banquet (break 22-159)', 'g1': 'blades of death', 'h1': 'shadow clones', 'e70': '70 % event'}


def bctx(s):
    b = T.body(s)
    return Ctx(b, tuple(b.pos), tuple(b.rot))


def fresh():
    s, pl = T.setup(dp=DP, hp=200000)
    T.fight(s)
    T.test_id(s, 99)                      # hold the AI
    T.run(s, 30, T.heal_player)           # the recovery in progress finishes into the hold
    return s


def place(s, d, side=0.0):
    """The player d b from her along her facing (side = lateral offset)."""
    b = T.body(s)
    yaw = math.radians(b.rot[0])
    fx, fz = -math.sin(yaw), math.cos(yaw)
    x = b.pos[0] + fx * d - fz * side
    z = b.pos[2] + fz * d + fx * side
    T.place_player(s, x, z)


PLACE = {'near': 3.0, 'near6': 6.0, 'mid': 9.0, 'far': 16.0}


def run_pattern(s, key, limit=400, each=None, snap=False):
    """Start key (core/start/<key> as the body), run until the pattern ended. Returns the per-tick log."""
    api = s.api
    tid = T.S_TID[key]
    s.hzr.clear()
    s.pjs.clear()
    s.phits.clear()
    s.rigl.clear()
    s.call(f'rlk:boss/arlecchino/core/start/{key}', bctx(s))
    log = []
    snaps = []
    for _ in range(limit):
        pt = T.kn(s, '#pt')
        if snap:
            a = s.api
            s.api = None
            snaps.append((pt, copy.deepcopy(s)))
            s.api = a
        if each:
            each(s)
        T.world(s)
        b = T.body(s)
        log.append(dict(t=s.t, pt=T.kn(s, '#pt'), pat=T.kn(s, '#pat'), pos=tuple(b.pos), yaw=b.rot[0],
                        bolw=T.kn(s, '#bolw'), win=T.kn(s, '#win'), mv='rlk_mb_mv' in b.tags))
        if T.kn(s, '#pat') != tid:
            break
    return log, snaps


def hazards_of(s, tid):
    return [h for h in s.hzr if h['pat'] == tid]


def static_dims(hit, tier_dmg):
    clip, ev, shape, dims, tier, bol = hit
    return shape, dims


def big(shape, dims):
    if shape == 'full':
        return True
    if shape in ('disc', 'disc_ahead'):
        return math.pi * dims[0] ** 2 >= 100 or dims[0] >= 8
    if shape == 'sector':
        return math.pi * dims[0] ** 2 * dims[1] / 180 >= 100 or dims[0] >= 8
    if shape == 'ring':
        return math.pi * (dims[1] ** 2 - dims[0] ** 2) >= 100 or dims[1] >= 8
    if shape == 'line':
        return dims[0] * dims[1] >= 100
    return False


# --------------------------------------------------------------------------------------------------- checks per pattern
def check_pattern(api, P1, key, s, log, where):
    tid = T.S_TID[key]
    hits = api.HITS[key]
    hz = hazards_of(s, tid)
    strikes = sorted(((h['pt'] + h['tell'], h) for h in hz), key=lambda x: x[0])
    want = {}
    for i, (clip, ev, shape, dims, tier, bol) in enumerate(hits):
        if shape.startswith('pj_'):
            continue
        t = api.ev(clip, ev)
        n = 2 if (key == 'g1' and ev in ('cross1', 'cross2')) or (key == 'h1' and ev == 'strike') else 1
        want.setdefault(t, []).extend([(i, shape, dims, tier, bol)] * n)
    got = {}
    for t, h in strikes:
        got.setdefault(t, []).append(h)
    ok_ticks = sorted(got) == sorted(want) and all(len(got[t]) == len(want[t]) for t in want)
    if key == 'd2' and not ok_ticks:
        # the follow-up runs only when the dash landed or the player is within 5 b
        w2 = {t: v for t, v in want.items() if t != api.ev('d2', 'fhit')}
        ok_ticks = sorted(got) == sorted(w2) and all(len(got[t]) == len(w2[t]) for t in w2)
    check(f'{key} [{where}]: every hazard strikes on its clip event (HITS ticks)', ok_ticks,
          (sorted((t, len(v)) for t, v in got.items()), sorted((t, len(v)) for t, v in want.items())))
    bad = []
    for t, hs in got.items():
        if t not in want:
            continue
        exp = sorted(want[t], key=lambda x: (KIND[x[1]], x[2]))
        hs2 = sorted(hs, key=lambda h: (h['kind'], h['r']))
        for (i, shape, dims, tier, bol), h in zip(exp, hs2):
            dmg = api.dmg(tier, 1)
            if h['kind'] != KIND[shape] or h['dmg'] != dmg or h['quiet'] != 1 or h['el'] != api.PYRO:
                bad.append((t, shape, h['kind'], h['dmg'], dmg, h['quiet'], h['el']))
                continue
            if shape in ('disc', 'disc_ahead', 'sector') and h['r'] != round(dims[0] * 10):
                bad.append((t, shape, 'r', h['r'], dims[0]))
            if shape == 'sector' and h['a'] != round(dims[1]):
                bad.append((t, shape, 'a', h['a'], dims[1]))
            if shape == 'line':
                tot = (h['r'] or 0) + (h['back'] or 0)
                if tot != round(dims[0] * 10) or h['hw'] != round(dims[1] * 10):
                    bad.append((t, shape, 'len/w', tot, h['hw'], dims))
            if shape == 'dash_line' and h['hw'] != round(dims[0] * 10):
                bad.append((t, shape, 'w', h['hw'], dims))
            if shape == 'full' and h['r'] != int(api.WALK * 10):
                bad.append((t, shape, 'r', h['r']))
            # 2 Bond of Life (FN-1 live since I1): a bol hazard carries the option #hzBol = BOL_HIT, a plain one none
            if (h.get('bol') or 0) != (api.BOL_HIT if bol else 0):
                bad.append((t, shape, 'hzBol', h.get('bol'), bol))
    check(f'{key} [{where}]: shapes / tiers / Pyro / quiet / Bond-of-Life marks match api.HITS', not bad, bad[:4])
    # 5 end points / heights
    cx, cz = api.CX, api.CZ
    out = [(r['pt'], round(math.hypot(r['pos'][0] - cx, r['pos'][2] - cz), 2)) for r in log
           if math.hypot(r['pos'][0] - cx, r['pos'][2] - cz) > api.MOVE_R + 0.01]
    hy = [(r['pt'], round(r['pos'][1] - api.CY, 2)) for r in log
          if r['pos'][1] < api.CY - 0.001 or r['pos'][1] > api.CY + api.AIR_MAX + 0.01]
    check(f'{key} [{where}]: the body stays inside MOVE_R and between the floor and AIR_MAX', not out and not hy, (out[:3], hy[:3]))
    end = log[-1]
    check(f'{key} [{where}]: on the floor, not gliding, window closed at the end',
          abs(end['pos'][1] - api.CY) < 0.01 and not end['mv'] and (end['win'] or 0) == 0, end)


def tells(api, P1):
    for key in api.P1:
        tab = P1.TABLE.get(key, [])
        ticks = sorted({h['t'] for h in tab})
        bad = []
        for h in tab:
            hit = api.HITS[key][h['idx']]
            gap = h['t'] - h['tell']
            follow = h['tell'] in ticks and h['tell'] < h['t']
            same_grp = follow and any(o['t'] == h['tell'] and o['grp'] == h['grp'] and h['grp'] not in (0, -1) for o in tab)
            if follow:
                if gap < api.COMBO_GAP and not same_grp:
                    bad.append((h['t'], 'gap', gap))
            else:
                need = api.TELL_BIG if big(hit[2], hit[3]) else api.TELL_MIN
                if gap < need:
                    bad.append((h['t'], 'tell', gap, need))
        check(f'{key}: tells >= {api.TELL_MIN} / {api.TELL_BIG} (big) t, combo follow-ups >= {api.COMBO_GAP} t (or one group)',
              not bad, bad)
        kb = [(h['t'], h['kb']) for h in tab]
        last = max(ticks) if ticks else None
        badkb = [(t, k) for t, k in kb if (t == last and k != api.KB_FINAL) or (t != last and k != api.KB_CHAIN)]
        if key in ('b1', 'b2'):
            badkb = [(t, k) for t, k in badkb if k not in (0,)] if key == 'b1' else [(t, k) for t, k in badkb if t == last and k != api.KB_FINAL]
        check(f'{key}: knockback only on the last hit (KB_FINAL), the chain hits KB_CHAIN', not badkb, badkb)


def decal_dry(api, P1):
    """Build every P1 pattern with the kit forced on into a dummy writer: the fx/decal calls per pattern."""
    import types
    out = {}
    real = api.K._on

    class DW:
        def __init__(self):
            self.files = {}
            self.out = types.SimpleNamespace(written=set())

        def w(self, rel, body):
            self.files[rel] = body
    api.K._on = lambda: True
    try:
        for p in P1.PATTERNS:
            W = DW()
            p.build(W)
            txt = '\n'.join(ln for body in W.files.values() for ln in (body if isinstance(body, list) else [body]))
            out[p.key] = sorted(set(re.findall(r'fx/decal/([a-z_]+)', txt)))
    finally:
        api.K._on = real
    bad = {k: v for k, v in out.items() if v and (k not in api.DECALS or not set(v) <= set(api.DECALS[k]))}
    check('decals: only the PLAN §1.5 keys draw floor decals (kit-on dry build)', not bad, (bad, out))
    need = {k: sorted(v) for k, v in api.DECALS.items() if k in api.P1}
    miss = {k: v for k, v in need.items() if out.get(k) != v}
    check('decals: f1 flood / cracks, g1 strip / rim_tint, e70 pool are all drawn with the kit', not miss, (miss, out))


def wheels(api, s, key, log):
    pjs = [p for p in s.pjs]
    spd = api.L.pj_speed_tenths(api.HITS[key][0][3][1])
    hr = round(api.HITS[key][0][3][0] * 10)
    nrel = 1 if key == 'b1' else 2
    outs = [p for p in pjs if p[1].get('life') is not None]
    check(f'{key}: {nrel} wheel(s), each an outward + a returning leg (pj speed {spd}, hr {hr}, Pyro dmg)',
          len(outs) == 2 * nrel and all(p[1]['spd'] == spd and p[1]['hr'] == hr and p[1]['dmg'] == api.dmg('T2', 1) for p in outs),
          [(p[0], p[1]) for p in outs])
    grps = [p[3] for p in outs]
    check(f'{key}: out and back legs are separate volley groups', len(set(grps)) == len(grps), grps)


def standing(api, P1, key, d):
    s = fresh()
    place(s, d)
    log, _ = run_pattern(s, key, each=T.heal_player)
    n_hits = len({h['t'] for h in P1.TABLE[key]})
    landed = sorted({t for t, *_ in s.phits})
    check(f'{key}: a standing player at {d} b is hit by every swing ({n_hits})', len(landed) == n_hits, (landed, n_hits))


def cancel_every_tick(api, key):
    s = fresh()
    place(s, 7.0)
    log, snaps = run_pattern(s, key, snap=True, each=T.heal_player)
    bad = []
    for pt, snap in snaps[1:]:
        snap.api = s.api
        b = T.body(snap)
        snap.call('rlk:boss/arlecchino/core/cancel_pat', Ctx(b, tuple(b.pos), tuple(b.rot)))
        T.run(snap, 2, T.heal_player)
        b = T.body(snap)
        # pattern markers / props (rlk_kn_p, rlk_kn_p_<key>); the real rig's parts (rlk_kn_part) and the wisps (rlk_kn_prop) stay
        left = [e.tags for e in snap.ents if e.alive and any(t == 'rlk_kn_p' or t.startswith('rlk_kn_p_')
                                                              or t in ('rlk_kn_lock', 'rlk_kn_dp', 'rlk_kn_win') for t in e.tags)]
        hz = [e for e in snap.ents if e.alive and 'rlk_mb_hz' in e.tags]
        pj = [e for e in snap.ents if e.alive and 'rlk_mb_pj' in e.tags]
        if left or hz or pj or abs(b.pos[1] - api.CY) > 0.01 or (T.kn(snap, '#win') or 0) or (T.kn(snap, '#pat') or 0) != 0:
            bad.append((pt, len(left), len(hz), len(pj), round(b.pos[1] - api.CY, 2), T.kn(snap, '#win'), T.kn(snap, '#pat')))
    check(f'{key}: a cancel at every tick ({len(snaps) - 1}) leaves no marker / prop / hazard / projectile, the body on the floor',
          not bad, bad[:4])


# --------------------------------------------------------------------------------------------------- renders
def render(api, key, s, log, path):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    tid = T.S_TID[key]
    hz = hazards_of(s, tid)
    if not hz and key != 'b1' and key != 'b2':
        hz = []
    W_, H_ = 640, 400
    img = Image.new('RGB', (W_, H_), (24, 24, 30))
    d = ImageDraw.Draw(img)
    sc = 7.0
    cx, cz = 230, 200
    ox, oz = api.CX, api.CZ

    def P(x, z):
        return (cx + (x - ox) * sc, cz + (z - oz) * sc)
    d.ellipse([P(ox - api.WALK, oz - api.WALK), P(ox + api.WALK, oz + api.WALK)], outline=(90, 90, 100))
    d.ellipse([P(ox - api.MOVE_R, oz - api.MOVE_R), P(ox + api.MOVE_R, oz + api.MOVE_R)], outline=(60, 60, 70))
    path_pts = [P(r['pos'][0], r['pos'][2]) for r in log]
    if len(path_pts) > 1:
        d.line(path_pts, fill=(200, 200, 200), width=1)
    tmax = max([h['pt'] + h['tell'] for h in hz] + [1])
    pal = [(255, 140, 40), (255, 200, 60), (230, 60, 70), (160, 30, 60), (255, 110, 160), (120, 200, 255)]
    rows = []
    for n, h in enumerate(sorted(hz, key=lambda h: h['pt'])):
        t = h['pt'] + h['tell']
        bol = any(api.ev(c, e) == t and b for c, e, sh, dm, ti, b in api.HITS[key])
        h['bol'] = bol
        col = pal[n % len(pal)] if not bol else (220, 30, 50)
        x, z = h['pos'][0], h['pos'][2]
        yaw = math.radians(h['yaw'])
        fx, fz = -math.sin(yaw), math.cos(yaw)
        r = (h['r'] or 0) / 10
        if h['kind'] == 1:
            d.ellipse([P(x - r, z - r), P(x + r, z + r)], outline=col, width=2)
        elif h['kind'] == 3:
            a = h['a']
            pts = [P(x, z)]
            for k in range(-a, a + 1, 5):
                q = yaw + math.radians(k)
                pts.append(P(x - math.sin(q) * r, z + math.cos(q) * r))
            pts.append(P(x, z))
            d.line(pts, fill=col, width=2)
        elif h['kind'] == 4:
            back = (h['back'] or 0) / 10
            hw = (h['hw'] or 0) / 20
            ln = r
            if ln <= 0:
                ln = 6
            ax, az = x - fx * back, z - fz * back
            bx, bz = x + fx * ln, z + fz * ln
            sx, sz = -fz * hw, fx * hw
            d.polygon([P(ax + sx, az + sz), P(bx + sx, bz + sz), P(bx - sx, bz - sz), P(ax - sx, az - sz)], outline=col)
        elif h['kind'] == 5:
            d.ellipse([P(ox - api.WALK + 0.4, oz - api.WALK + 0.4), P(ox + api.WALK - 0.4, oz + api.WALK - 0.4)], outline=col, width=3)
        rows.append((t, h, col))
    pl = T.place_player
    d.text((470, 10), f'{key} {EN.get(key, "")}', fill=(255, 255, 255))
    d.text((470, 26), f'clip {api.CLIPS[key][0]} t' if key in api.CLIPS else '', fill=(200, 200, 200))
    y = 46
    for t, h, col in rows[:20]:
        kind = {1: 'disc', 2: 'ring', 3: 'sector', 4: 'line', 5: 'full'}.get(h['kind'], '?')
        d.text((470, y), f't{t:>4} {kind:<6} r{(h["r"] or 0) / 10:.1f} {"BoL" if h["bol"] else ""}', fill=col)
        y += 14
    for p in s.pjs:
        d.text((470, y), f'pj t+{p[0] - log[0]["t"] + 1} spd {p[1].get("spd")} life {p[1].get("life")}', fill=(255, 160, 60))
        y += 14
    img.save(path)


# --------------------------------------------------------------------------------------------------- main
def main():
    s0 = fresh()
    api = s0.api
    from mboss_arlecchino import p1 as P1
    T.S_TID = {n.split(' ')[0]: v for v, n in api.TEST_IDS.items() if n.split(' ')[0] in api.P1 + api.P2}
    keys = [k for k in api.P1 if not ONLY or k in ONLY]
    check('static: LEAP_H <= AIR_MAX, MOVE_R = walk - 1.5', max(api.LEAP_H.values()) <= api.AIR_MAX and api.MOVE_R == api.WALK - 1.5)
    tells(api, P1)
    decal_dry(api, P1)
    RENDER.mkdir(parents=True, exist_ok=True)
    for key in keys:
        for where, d, side in (('near', 3.0, 0.0), ('mid', 9.0, 2.0), ('far', 16.0, -3.0), ('edge', 0.0, 0.0)):
            s = fresh()
            if where == 'edge':
                # her near the arena rim, the player across from the axis: the clamps / mv/ok fallbacks
                b = T.body(s)
                b.pos = [api.CX + 0.0, api.CY, api.CZ + 21.0]
                b.rot = [180.0, 0.0]
                T.place_player(s, api.CX + 2.0, api.CZ - 14.0)
            else:
                place(s, d, side)
            log, _ = run_pattern(s, key, each=T.heal_player)
            check_pattern(api, P1, key, s, log, where)
            if key in ('b1', 'b2') and where == 'mid':
                wheels(api, s, key, log)
            if where == 'mid':
                render(api, key, s, log, RENDER / f's3_{key}.png')
    for key in ('a2', 'a4', 'a5'):
        if key in keys:
            standing(api, P1, key, 3.0)
            standing(api, P1, key, 6.0)
    for key in keys:
        cancel_every_tick(api, key)
    summary('pat_p1')


main()
