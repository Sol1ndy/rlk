#!/usr/bin/env python3
"""test_wi.py: round W, the three lanes TOGETHER (the integration WI, 11-12; tools/dev/plan/combat/wi_progress.md).

    python3 test_wi.py <roguelike> [section ...]        (run from a copy of tools/dev/sim outside the datapack)

Lane WP's dodge set (the dash is gone: twist / lunge-step / back-step after an avoided hit / the double dodge's cartwheel,
the faster perfect dodge), lane WB's fight (the blade's trail, the stop rule that keeps her out of the player's F5 camera
line: core/cam_ok / core/cam_clear) and lane WC's cutscenes (the actor, the kill of the fight's blade cards at every
sequence start). Each lane's own suite proves its part alone; this one proves the seams. test_vi.py (round V) keeps the
beat's seams (beatpat on the trail, follow, swap, beatseq, skip) and is run beside it.

  dodgecam  every 홍련 pattern (api.P1 + api.P2, both gauntlets) in the H1 world (the real core, judge and hazards) with the
            player using the REAL dodge set: the right click is the real player/dash (-> dash_go / dodge/again), the body
            moves by player/tick's own move line (dash_move_tick), an avoided hit turns the move into the back-step away from
            her (the judge's dg_refund -> dodge/away), a second press 3 t later is the cartwheel. The player dodges one tick
            before every hit (a perfect dodge) and, in a second run, also presses again for the cartwheel; the view either
            follows her (the user steering the camera at her), stays where it was, or follows her 60 degrees off. At the end of every tick the vanilla F5
            camera (4 b behind the eyes along the view) is measured against her body: never inside her (her body cylinder
            r 0.6, 2.1 high), she never moves onto the player (closer than 0.6 b: the player's own forward twist / cartwheel
            into her is counted apart), and her stop rule (core/cam_clear's step out of the camera line) answers a player's
            move at most once per move. A standing player with the same
            perfect dodges (no travel: hrsim's stamp model) is the reference.
  trailcut  lane WB's trail (band, pieces, ribbon, wave, the ride / origin markers) against lane WC's sequence starts: the kill
            list every sequence start runs (seq.KILL_FIGHT_FX -> the sequences' first tick) takes every tag blade.py gives a
            trail entity; in the fight world a sequence that starts while a pattern's trail is alive leaves no trail entity
            one tick later, with the beat (a perfect parry freeze / a perfect dodge slow motion) running or not.
  dodgelock a dodge move in flight when a locked sequence starts (lane VC / WC's actor, the real char/cine/**): the twist, the
            lunge-step, the back-step and the cartwheel (the stand-in rig of the four mannequin characters, the rig
            characters' clip), with the lock starting at every tick of the move: one body at the end of every tick, the
            hidden avatar does not travel during the lock, and after the hand-back nothing of the dodge is left (no crouch,
            no stand-in rig, no move, the avatar visible as it was). Without a lock the cartwheel's stand-in rig plays its 9
            ticks and goes (rlk:tick runs it when no beat runs).
Prints one line per check; exit 1 on any failure.
"""
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / 'lib'))
import test_vi as V  # noqa: E402  (the round V seams' worlds: SwapWorld, the beat's lines, the stubs)
from test_vi import H, api, S3, B, DP, FN, C0, fn_lines, bt, beat_reset  # noqa: E402
from mcsim import Ctx, split  # noqa: E402

SECT = V.SECT
FAILS, NCK = [], [0]


def ck(name, ok, info=''):
    NCK[0] += 1
    print(('ok   ' if ok else 'FAIL ') + name + ('' if ok or info == '' else f'  -- {str(info)[:900]}'), flush=True)
    if not ok:
        FAILS.append(name)
    return ok


def want(name):
    return not SECT or name in SECT


PTICK = fn_lines('player/tick')
MOVE = next(l for l in PTICK if 'dash_move_tick' in l)
COOL = next(l for l in PTICK if 'remove @s dashCool 1' in l)
PHEAD = [l for l in PTICK[:12] if 'rdCam' in l or 'rlk_mb_camh' in l]     # player/tick's head: the cameras' holds end a dodge
TICK = fn_lines('tick')
# rlk:tick's post lines: the beat's post while a beat runs, and the stand-in rig's own tick when none runs (the integration)
POSTS = [l for l in TICK if 'player/def/beat/post' in l or ('lite/tick' in l and 'plActive' in l)]

# ============================================================================================================ dodgecam
CAM_D = 4.0                     # the vanilla F5 camera distance behind the eyes (the seat's camera_distance, client_facts §1)
EYE = 1.62
IN_R, IN_H = 0.6, 2.1           # her body as the camera sees it: the near plane inside this cylinder fills the picture
LINE_R = 1.3                    # lane WB's camera-line clearance (core/cam_ok)
SEP_MIN = 0.6                   # her body and the player's never closer (feet to feet, horizontal)
DC_STUB = tuple(f for f in V.STUB_FX if f != 'rlk:player/dash_dir') + V.STUB_AV + (
    'rlk:char/motion/dash_b', 'rlk:char/motion/dash2', 'rlk:char/motion/dash_l', 'rlk:items/hook/on_dash_move',
    'rlk:player/dodge/snd_step', 'rlk:player/dodge/snd_flip', 'rlk:player/dash_fail', 'rlk:player/dodge/crouch',
    'rlk:player/dodge/stand')
CAM_CLEAR = 'rlk:boss/scarlet/core/cam_clear'


class DcSim(H.H1Sim):
    """The H1 world + a count of her steps out of the camera line (core/cam_clear's glides)."""

    def __init__(self, root):
        super().__init__(root)
        self.clears = []             # world ticks of a cam_clear glide

    def call(self, fid, ctx, macro=None):
        if fid == 'rlk:mboss/mv/glide' and CAM_CLEAR in self.stack:
            self.clears.append(self.t)
        return super().call(fid, ctx, macro)


def look(yaw, pitch):
    y, p = math.radians(yaw), math.radians(pitch)
    return (-math.sin(y) * math.cos(p), -math.sin(p), math.cos(y) * math.cos(p))


def aim_at(pl, b):
    """The player's view on her chest (the user steering the F5 camera at her)."""
    dx, dy, dz = b.pos[0] - pl.pos[0], (b.pos[1] + 1.2) - (pl.pos[1] + EYE), b.pos[2] - pl.pos[2]
    yaw = math.degrees(math.atan2(-dx, dz))
    pitch = math.degrees(-math.atan2(dy, math.hypot(dx, dz)))
    return [yaw, max(-30.0, min(45.0, pitch))]


def cam_geom(pl, b):
    lx, ly, lz = look(*pl.rot)
    ex, ey, ez = pl.pos[0], pl.pos[1] + EYE, pl.pos[2]
    cx, cy, cz = ex - CAM_D * lx, ey - CAM_D * ly, ez - CAM_D * lz
    hz = math.hypot(cx - b.pos[0], cz - b.pos[2])
    inside = hz < IN_R and b.pos[1] - 0.1 <= cy <= b.pos[1] + IN_H
    bx, by, bz = b.pos[0], b.pos[1] + 1.0, b.pos[2]
    line = min(math.dist((ex - k * lx, ey - k * ly, ez - k * lz), (bx, by, bz)) for k in [i * 0.25 for i in range(17)])
    sep = math.hypot(pl.pos[0] - b.pos[0], pl.pos[2] - b.pos[2])
    return inside, line, sep, hz


def dc_world(key, ph, dist):
    s, pl = H.setup_sc(DP, seed=9, lv=15, hp=5834, player_level=15, cls=DcSim)
    s.cache['rlk:mob/setup'] = ['tag @s add rlk_mob', 'function rlk:bal/init']
    s.call('rlk:bal/load', C0)
    beat_reset(s, 0, DC_STUB)
    assert H.fight_sc(s)
    if ph == 2 and key not in api.GAUNTLETS:
        H.test_id(s, 33)
        H.run_h1(s, 2)
    H.heal(s)
    H.facing_setup(s, dist)
    pl.tags.add('rlk_body')                                 # the player is the body (dash / dash_go / the move run at it)
    pid = ('e', pl.id)
    for o in ('rdCam', 'pmMoveLock', 'pmActive', 'skDash', 'dashMoveT', 'dashCool', 'dashUpN'):
        s.setsc(pid, o, 0)
    s.setsc(pid, 'dashPX', round(pl.pos[0] * 100))
    s.setsc(pid, 'dashPZ', round(pl.pos[2] * 100))
    s.setsc('#charN', 'tmp', 5)
    s.setsc('#inAct', 'view', 0)
    return s, pl


def dc_tick(s, pl, press):
    """One game tick in rlk:tick's order for the player: the input pre-pass (the right click -> the REAL player/dash at the
    body, gametime = this tick), player/tick's cooldown and move lines, her balance clock, the fight (world_sc), the
    previous position for the next tick's direction (rlk:tick's last lines)."""
    pid = ('e', pl.id)
    if press:
        s.gt_off = 1
        try:
            s.call('rlk:player/dash', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
        finally:
            s.gt_off = 0
    pc = Ctx(pl, tuple(pl.pos), tuple(pl.rot))
    s.cmd(split(COOL), pc)
    s.cmd(split(MOVE), Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
    b = H.body_of(s)
    if b is not None and b.alive and (s.sc(('e', b.id), 'balT') or 0) >= 1 and 'rlk_mb_dying' not in b.tags:
        s.call('rlk:bal/tick', Ctx(b, tuple(b.pos), tuple(b.rot)))
    H.world_sc(s)
    s.setsc(pid, 'dashPX', round(pl.pos[0] * 100))
    s.setsc(pid, 'dashPZ', round(pl.pos[2] * 100))


def dc_run(key, ph, policy, view, dist=3.0):
    """policy: 'still' (hrsim's stamp: perfect dodges with no travel), 'none' (no input), 'step' (the real dodge one tick before every hit),
    'double' (and the second press 3 t later: the cartwheel). view: 'track' (aimed at her chest every tick) or 'fixed'."""
    s, pl = dc_world(key, ph, dist)
    pid = ('e', pl.id)
    b0 = H.body_of(s)
    pl.rot = aim_at(pl, b0)
    tid = S3.TID[key]
    if key in api.GAUNTLETS:
        H.test_id(s, tid)
    else:
        H.start_pattern(s, tid)
    t0 = s.t
    limit = (api.JUDGE_T[key] + 40) if key in api.GAUNTLETS else 300
    st = dict(inside=[], line=0, sep=99.0, ticks=0, moved=0.0, back=0, cart=0, presses=0, her_on=[], own_on=0, kb_on=[])
    presses = set()
    seen = False
    travel = 0.0
    prev = tuple(pl.pos)
    while s.t - t0 < limit:
        pat = H.hr(s, '#pat') or 0
        if key not in api.GAUNTLETS:
            want_tid = S3.TID['ult'] if key == 'ult' else tid
            if pat == want_tid or (key == 'ult' and pat == S3.TID['rings']):
                seen = True
            elif seen and pat == 0:
                break
        for h in s.select('@e[type=minecraft:marker,tag=rlk_mb_hz]', C0):
            g = lambda o, h=h: s.sc(('e', h.id), o) or 0  # noqa: E731
            if g('mbHzD') >= 1 and g('mbHzHit') == 0 and g('mbHzW') - g('mbHzT') == 1:
                if policy == 'still':
                    s.dodge(at=s.t + 1)
                elif policy == 'none':
                    pass
                else:
                    presses.add(s.t + 1)
                    if policy == 'double':
                        presses.add(s.t + 4)
        b = H.body_of(s)
        if view != 'fixed' and b is not None:
            pl.rot = aim_at(pl, b)
            if view == 'side':
                pl.rot[0] += 60.0
        hb0 = tuple(b.pos) if b is not None else None
        H.heal(s)
        t = s.t + 1
        p0 = tuple(pl.pos)
        dodging = (s.sc(pid, 'dashMoveT') or 0) >= 1 or t in presses
        if policy in ('still', 'none'):
            H.world_h1(s)
        else:
            mv0 = s.sc('#dgMv', 'cb')
            dc_tick(s, pl, t in presses)
            if t in presses:
                st['presses'] += 1
            mv1 = s.sc('#dgMv', 'cb')
            if mv1 == 4 and mv0 != 4:
                st['back'] += 1
            if mv1 == 2 and mv0 != 2:
                st['cart'] += 1
        b = H.body_of(s)
        if b is None:
            continue
        inside, line, sep, hz = cam_geom(pl, b)
        st['ticks'] += 1
        if inside:
            st['inside'].append((s.t - t0, round(hz, 2), tuple(round(v, 2) for v in pl.pos), tuple(round(v, 2) for v in b.pos)))
        if line < LINE_R:
            st['line'] += 1
        st['sep'] = min(st['sep'], sep)
        if sep < SEP_MIN:
            if math.dist(p0, pl.pos) > 0.01 and not dodging:
                st['kb_on'].append((s.t - t0, round(sep, 2)))      # the player knocked back by her hit across her way
            elif hb0 is not None and math.dist(hb0, b.pos) > 0.01:
                st['her_on'].append((s.t - t0, round(sep, 2)))     # she moved onto the player this tick
            else:
                st['own_on'] += 1                                   # the player's own move (a forward twist / cartwheel)
        travel += math.dist(prev, pl.pos)
        prev = tuple(pl.pos)
    st['moved'] = round(travel, 2)
    st['clears'] = len(s.clears)
    st['clear_ticks'] = sorted(set(t - t0 for t in s.clears))
    st['judged'] = len(s.judged)
    st['dodged'] = len([j for j in s.judged if j['dodged']])
    return st


def dodgecam():
    keys = [(k, 1) for k in api.P1] + [(k, 2) for k in api.P2]
    only = [a[7:].split(',') for a in sys.argv[1:] if a.startswith('--keys=')]
    if only:
        keys = [k for k in keys if k[0] in only[0]]
    tot = dict(runs=0, back=0, cart=0, inside=0, ticks=0, moved=0.0, line=0, line_ref=0, clears=0, clears_ref=0, own_on=0, kb_on=0, kb_runs=[])
    rows = []
    for key, ph in keys:
        dist = 6.0 if key in api.GAUNTLETS else 3.0
        refs = {view: dc_run(key, ph, 'still', view, dist) for view in ('track', 'fixed', 'side')}
        for ref in refs.values():
            tot['line_ref'] += 2 * ref['line']
            tot['clears_ref'] += 2 * ref['clears']
        for pol in ('step', 'double'):
            for view in ('track', 'fixed', 'side'):
                ref = refs[view]                                # the standing player with the same view
                r = dc_run(key, ph, pol, view, dist)
                tot['runs'] += 1
                for k in ('back', 'cart', 'ticks', 'line', 'clears'):
                    tot[k] += r[k]
                tot['inside'] += len(r['inside'])
                tot['moved'] += r['moved']
                rows.append((key, pol, view, r))
                lab = f'dodgecam {key} P{ph} ({pol}, view {view})'
                # her step out of the line may come once per move; with the player moving it must not come more often than a
                # standing player's + one per back-step / cartwheel the player made (the player moved the line: one answer)
                tot['own_on'] += r['own_on']
                tot['kb_on'] += len(r['kb_on'])
                if r['kb_on']:
                    tot['kb_runs'].append(f'{key} {pol} {view} {r["kb_on"][:2]}')
                ck(f'{lab}: {r["presses"]} presses, {r["back"]} back-steps, {r["cart"]} cartwheels, the player travelled {r["moved"]} b; '
                   f'the F5 camera never inside her ({len(r["inside"])} of {r["ticks"]} ticks), she never moves onto the player '
                   f'(closest {r["sep"]:.2f} b; closer than {SEP_MIN} b: {r["own_on"]} ticks by the player\'s own move, {len(r["kb_on"])} by her '
                   f'hit\'s knockback); in the camera '
                   f'line {r["line"]} ticks (standing: {ref["line"]}); her steps out of it {r["clears"]} (standing: {ref["clears"]})',
                   not r['inside'] and not r['her_on'] and r['clears'] <= ref['clears'] + r['back'] + r['cart'] + 1,
                   dict(inside=r['inside'][:4], her_on=r['her_on'][:4], clears=r['clear_ticks'][:8], ref=ref['clear_ticks'][:8]))
    if only:
        return
    ck(f'dodgecam: {tot["runs"]} runs with the real dodge set: {tot["back"]} back-steps after an avoided hit and {tot["cart"]} '
       f'cartwheels seen, the player travelled {tot["moved"]:.0f} b in all; the camera inside her on {tot["inside"]} of '
       f'{tot["ticks"]} ticks; her body in the camera line {tot["line"]} ticks (the standing player with the same views: {tot["line_ref"]}); '
       f'her steps out of the line {tot["clears"]} (standing: {tot["clears_ref"]}); the player\'s own move closer than '
       f'{SEP_MIN} b to her on {tot["own_on"]} ticks (a direction-less double dodge goes along the view: into her), knocked back by '
       f'her hit across her way on {tot["kb_on"]} ({tot["kb_runs"][:4]})',
       tot['back'] >= 20 and tot['cart'] >= 10 and tot['inside'] == 0, tot)


# ============================================================================================================ trailcut
def trail_tags():
    """Every tag blade.py gives an entity of the trail (its TAG* constants)."""
    return sorted({v for k, v in vars(B).items() if k.startswith('TAG') and isinstance(v, str) and v.startswith('rlk_')})


def trail_alive(s):
    """Live entities of the trail (any tag blade.py gives one: the band, the pieces, the ribbon, the wave, the round V cards, the
    ride / origin markers)."""
    tags = set(trail_tags()) | {getattr(B, n) for n in ('TR', 'TR_RIDE', 'TR_BAND', 'TR_GROW', 'TR_TGT', 'TR_NEW') if hasattr(B, n)}
    return [e for e in s.ents if e.alive and tags & set(e.tags)]


def tc_world(key, ph):
    s, pl = H.setup_sc(DP, seed=9, lv=15, hp=5834, player_level=15, cls=V.PatSim)
    s.cache['rlk:mob/setup'] = ['tag @s add rlk_mob', 'function rlk:bal/init']
    s.call('rlk:bal/load', C0)
    beat_reset(s, 1, V.STUB_FX + V.STUB_AV)
    assert H.fight_sc(s)
    if ph == 2:
        H.test_id(s, 33)
        H.run_h1(s, 2)
    H.heal(s)
    H.facing_setup(s, 3.0)
    return s, pl


def trailcut():
    """Lane WC kills the fight's blade cards at every sequence start (seq.KILL_FIGHT_FX: round V's rlk_hr_sw cards); lane WB's
    trail carries rlk_hr_tr (+ rlk_hr_p of the pattern that made it). Whatever path starts a sequence in the fight (CS1 from the
    60 % floor, the ending from her death, the repel from a gauntlet's judge), no trail entity may be left one tick later, with a
    beat (a perfect parry freeze / a perfect dodge slow motion) running or not."""
    starts = (('cs1', 1, 'core/cs1/start'), ('ending', 2, 'death_start'))
    seen, bad = 0, []
    for key, ph in [(k, 1) for k in ('a1', 'a3', 'a9', 'tri', 'hcut', 'kcut')] + [(k, 2) for k in ('mx', 'nb', 'q')]:
        for beat in (None, 'p', 'd'):
            seq = 'cs1' if ph == 1 else 'ending'
            fn = dict((a, c) for a, _p, c in starts)[seq]
            s, pl = tc_world(key, ph)
            H.start_pattern(s, S3.TID[key])
            n = 0
            for _ in range(200):                              # until her trail is alive (the wind-up's band, a cut's pieces)
                H.world_h1(s)
                if len(trail_alive(s)) >= 3:
                    n = len(trail_alive(s))
                    break
            if not n:
                bad.append((key, beat, 'no trail seen'))
                continue
            seen += n
            if beat:
                s.call('rlk:player/def/beat/start_p' if beat == 'p' else 'rlk:player/def/beat/start_d', Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
            H.call_sc(s, fn)
            s.pre = 1
            s.cmd(split(V.CLOCK), C0)
            s.pre = 0
            H.world_h1(s)
            s.cmd(split(V.POST), C0)
            left = trail_alive(s)
            if left:
                bad.append((key, beat, seq, n, sorted({t for e in left for t in e.tags if t.startswith('rlk_hr_')})[:6]))
    ck(f'trailcut: a sequence started while her trail is alive (CS1 in P1: a1 a3 a9 tri hcut kcut; the ending in P2: mx nb q; each '
       f'with no beat, a perfect parry\'s freeze and a perfect dodge\'s slow motion running): no trail entity one tick later '
       f'({seen} trail entities alive at the starts)', not bad and seen > 0, bad[:6])
    # the repel: a cleared gauntlet's judge (G1, the ideal parrier) -> no trail entity on the tick the repel starts
    for key in api.GAUNTLETS:
        s, pl = tc_world(key, 1)                            # (test_vi's gauntlet runs: no phase-2 setup)
        H.facing_setup(s, 6.0)
        H.test_id(s, S3.TID[key])
        t0, at, left, most = s.t, None, None, 0
        while s.t - t0 < api.JUDGE_T[key] + 60:
            for h in s.select('@e[type=minecraft:marker,tag=rlk_mb_hz]', C0):
                g = lambda o, h=h: s.sc(('e', h.id), o) or 0  # noqa: E731
                if g('mbHzD') >= 1 and g('mbHzHit') == 0 and g('mbHzW') - g('mbHzT') == 1 and g('mbHzNP') == 0:
                    s.press(at=s.t + 1)
            H.heal(s)
            H.world_h1(s)
            most = max(most, len(trail_alive(s)))
            if (H.hr(s, '#ph') or 0) in (api.PH['cs2'], api.PH['cs3']) and at is None:     # the repel {at:60} / {at:5}
                at, left = s.t - t0, trail_alive(s)
                break
        ck(f'trailcut: {key} cleared by the ideal parrier -> the repel starts at {at} (judge {api.JUDGE_T[key]}) with no trail entity '
           f'left (the gauntlet\'s trail: up to {most} alive)', at is not None and not left and most > 0,
           (at, sorted({t for e in (left or []) for t in e.tags if t.startswith('rlk_hr_')})[:6], most))


# ============================================================================================================ dodgelock
DL_REAL = ('rlk:player/dash', 'rlk:player/dash_go', 'rlk:player/dash_dir', 'rlk:player/dash_lookvec', 'rlk:player/dash_norm',
           'rlk:player/dodge/', 'rlk:player/dash_move_tick', 'rlk:player/dash_sub', 'rlk:player/def/dodge_stamp',
           'rlk:player/def/dg_refund', 'rlk:char/motion/dash', 'rlk:char/motion/dash2', 'rlk:char/motion/dash_l',
           'rlk:char/motion/dash_b', 'rlk:player/def/beat/act', 'rlk:view/dash_dir')
DL_STUB = ('rlk:player/dodge/snd_', 'rlk:player/def/reset', 'rlk:player/dash_fail')


class DlWorld(V.SwapWorld):
    """test_vi's SwapWorld + the real dodge set (player/dash -> dash_go -> dodge/again, the moves, the back-step, the avatar's
    crouch / stand-in rig / clip calls). The rig characters' clip engine (char/motion/start) stays an empty call: their own
    rig is hidden / shown by char/cine like any other part; the move itself is real."""

    def load(self, fid):
        if fid.startswith(DL_REAL) and not fid.startswith(DL_STUB):
            return super(V.SwapWorld, self).load(fid)
        return super().load(fid)

    def cmd(self, t, ctx):
        if t[:3] == ['time', 'query', 'gametime']:
            return self.now
        if t[0] == 'tp' and len(t) == 9 and t[5] == 'facing':      # tp <sel> <x y z> facing <x y z> (char/motion/lite/face)
            pos, tgt = self.coords(t[2:5], ctx), self.coords(t[6:9], ctx)
            es = self._es(t[1], ctx)
            for e in es:
                e.pos = list(pos)
                dx, dy, dz = (tgt[k] - pos[k] for k in range(3))
                e.rot = [math.degrees(math.atan2(-dx, dz)), math.degrees(-math.atan2(dy, math.hypot(dx, dz)))]
            return 1 if es else 0
        return super().cmd(t, ctx)


def dl_setup(ch):
    """V.swap_world's avatar for character ch in a DlWorld (the load's constants set first)."""
    real = V.SwapWorld
    try:
        V.SwapWorld = DlWorld
        w = V.swap_world(ch)
    finally:
        V.SwapWorld = real
    for l in fn_lines('load'):
        p = l.split()
        if l.startswith('scoreboard players set #') and len(p) == 6 and p[4] in ('tmp', 'cb', 'view'):
            if w.sc(p[3], p[4]) is None:
                w.cmd(p, C0)
    pid = ('e', w.player.id)
    for o in ('rdCam', 'skDash', 'dashMoveT', 'dashCool', 'dashUpN', 'dgAt', 'parHit', 'parAt', 'dashDX', 'dashDZ', 'dashUX',
              'dashUZ', 'stepT', 'buT', 'energy'):
        w.setsc(pid, o, 0)
    w.setsc(pid, 'parHit', -1000000)
    w.setsc(pid, 'dgAt', -1000000)
    w.setsc('#btAdj', 'cb', 0)
    w.setsc('#dgTry', 'cb', -1000)
    w.setsc('#dgMv', 'cb', 0)
    w.setsc('#dgN', 'cb', 0)
    w.setsc('#dgCr', 'cb', 0)
    w.setsc('#inAct', 'view', 0)
    w.setsc('#rcRep', 'tmp', 0)
    w.av.data['pose'] = 'standing'
    w.setsc(pid, 'dashPX', round(w.av.pos[0] * 100))
    w.setsc(pid, 'dashPZ', round(w.av.pos[2] * 100))
    return w


MOVES = ('twist', 'lunge', 'back', 'cartwheel')


def dl_tick(w, t, start, move, lock):
    """One game tick in rlk:tick's order: the input pre-pass (the move's presses), player/tick's cooldown + move lines, the
    fight (the back-step: an attack avoided on the first move's 2nd tick -> dg_refund), the lock's start / tick / end, the
    post lines, the previous position."""
    w.now = t
    pid = ('e', w.player.id)
    w.cmd(split(V.CLOCK), C0)
    at = lambda: V.pctx(w, (w.av.pos, w.player.rot))  # noqa: E731
    if move == 'lunge':                                     # a direction held (+x) in the view's input (view/dash_dir)
        w.setsc('#inAct', 'view', 1 if t == start else 0)
        w.setsc('#inx', 'view', 100)
        w.setsc('#inz', 'view', 0)
    if t == start or (move == 'cartwheel' and t == start + 3):
        w.call('rlk:player/dash', at())
    for l in PHEAD:
        w.cmd(split(l), V.pctx(w))
    w.cmd(split(COOL), V.pctx(w))
    w.cmd(split(MOVE), V.pctx(w))
    if move == 'back' and t == start + 1:
        w.call('rlk:player/def/dg_refund', V.pctx(w))
    if lock and lock[0] <= t < lock[1]:
        if t == lock[0]:
            w.call('rlk:char/cine/spawn', V.pctx(w, V.STAGE_AT))
            w.call('rlk:char/cine/play', V.pctx(w), {'clip': 'cs1'})
        w.setsc('#mbCam', 'mb', 1)
        w.setsc('#cavT', 'cine', t - lock[0])
        w.call('rlk:char/cine/tick', V.pctx(w))
        w.player.tags.add('rlk_mb_camh')
    elif lock and t == lock[1]:
        w.setsc('#mbCam', 'mb', 0)
        w.player.tags.discard('rlk_mb_camh')
        w.call('rlk:char/cine/stop', V.pctx(w))
    for l in POSTS:
        w.cmd(split(l), C0)
    w.setsc(pid, 'dashPX', round(w.av.pos[0] * 100))
    w.setsc(pid, 'dashPZ', round(w.av.pos[2] * 100))


def dodgelock():
    L_LEN, END = 40, 90
    tot = 0
    for ch, name in sorted((V.MAN_CH | V.RIG_CH).items()):
        own = 'rig' if ch in V.RIG_CH else 'avatar'
        for move in MOVES:
            bad, after, travel, alone = [], [], [], []
            for age in [None] + list(range(0, 10)):
                w = dl_setup(ch)
                prof0, hand0 = dict(w.av.data['profile']), dict(w.av.data['hand'])
                start = 20
                lock = (start + age, start + age + L_LEN) if age is not None else None
                seen_pl = False
                pos_lock = None
                for t in range(1, END + 1):
                    dl_tick(w, t, start, move, lock)
                    b = V.bodies(w)
                    locked = lock is not None and lock[0] <= t < lock[1]
                    if 'stand-in' in b:
                        seen_pl = True
                    if locked:
                        blank = w.av.data.get('profile', {}).get('texture') == 'rlk:skin/blank' and w.av.data.get('invis', 0) > w.now
                        if b != ['actor'] or not blank:
                            bad.append((age, t - lock[0], b, 'blank' if blank else 'NOT blank'))
                        if t == lock[0]:
                            pos_lock = tuple(round(v, 3) for v in w.av.pos)
                        elif tuple(round(v, 3) for v in w.av.pos) != pos_lock:
                            travel.append((age, t - lock[0], pos_lock, tuple(round(v, 3) for v in w.av.pos)))
                            pos_lock = tuple(round(v, 3) for v in w.av.pos)
                    elif len(b) != 1 or b == ['actor']:
                        bad.append((age, t, b))
                    tot += 1
                pid = ('e', w.player.id)
                back = (V.bodies(w) == [own] and w.av.data.get('profile') == prof0 and w.av.data['hand'] == hand0
                        and w.av.data.get('pose', 'standing') == 'standing'
                        and not any(e.alive and ('rlk_pl' in e.tags or 'rlk_cine_part' in e.tags or 'rlk_cine_hid' in e.tags
                                                 or 'rlk_pl_basis' in e.tags) for e in w.ents)
                        and (w.sc(pid, 'plActive') or 0) == 0 and (w.sc(pid, 'dashMoveT') or 0) == 0
                        and (w.sc('#dgCr', 'cb') or 0) == 0)
                if not back:
                    after.append((age, V.bodies(w), w.av.data.get('pose'), w.sc(pid, 'plActive'), w.sc(pid, 'dashMoveT'),
                                  w.sc('#dgCr', 'cb')))
                if age is None and move == 'cartwheel' and ch in V.MAN_CH:
                    alone.append(seen_pl)
            ck(f'dodgelock {name} ({"rig" if ch in V.RIG_CH else "mannequin"} character), the {move}: alone and with a lock starting at each '
               f'tick 0-9 of it: exactly one body at the end of every tick (the actor alone inside the lock, the avatar invisible and '
               f'blank)', not bad, bad[:6])
            ck(f'dodgelock {name}, the {move}: the hidden avatar does not travel during the lock', not travel, travel[:4])
            ck(f'dodgelock {name}, the {move}: after the hand-back (and without a lock) nothing of the dodge is left (standing pose, no '
               f'stand-in rig, no move, the {own} back as it was)', not after, after[:4])
            if alone:
                ck(f'dodgelock {name}, the cartwheel without a lock: the stand-in rig shows and plays its 9 ticks (rlk:tick runs it '
                   f'when no beat runs), then goes', all(alone) and not after, (alone, after[:2]))
    ck(f'dodgelock: {tot} ticks looked at (7 characters x 4 moves x every lock age)', tot > 2000, tot)


# ============================================================================================================ dmgnum
PX_PER_B = 540.0                # 1080p, FOV 90 (vertical): pixels per block at 1 b = 540 / tan(45 deg)
GLYPH = 0.025                   # b per font pixel of a text display at scale 1 (the name-tag scale)


def text_w_px(e, cam_d):
    """The on-screen width (px) of a damage number at the fight camera's distance: the font's advance widths (digits and
    spaces 6 / 4 px, the stars 8, bold + 1 each) x 0.025 b x the display's scale."""
    m = __import__('re').search(r'scale:\[([\d.]+)f', e.data.get('nbt', ''))
    sc = float(m.group(1)) if m else 1.0
    txt = e.data.get('txt', '')
    bold = 'bold:true' in e.data.get('nbt', '')
    w = sum(8 if ch in '✦✧' else 4 if ch == ' ' else 6 for ch in txt) + (len(txt) if bold else 0)
    return w * GLYPH * sc * PX_PER_B / cam_d, sc


class DnSim(H.H1Sim):
    def cmd(self, t, ctx):
        r = super().cmd(t, ctx)
        if t[0] == 'summon' and 'text_display' in t[1]:
            e = self.ents[-1]
            nbt = ' '.join(t[5:]) if len(t) > 5 else ''
            e.data['nbt'] = nbt
            import re as _re
            e.data['txt'] = ''.join(_re.findall(r'text:"([^"]*)"', nbt))
        return r


def dmgnum():
    s, pl = H.setup_sc(DP, seed=9, lv=15, hp=5834, player_level=15, cls=DnSim)
    s.cache['rlk:mob/setup'] = ['tag @s add rlk_mob', 'function rlk:bal/init']
    s.call('rlk:bal/load', C0)
    beat_reset(s, 0, V.STUB_FX + V.STUB_AV)
    assert H.fight_sc(s)
    H.facing_setup(s, 4.0)
    b = H.body_of(s)
    # the number functions are leaves of the suites' worlds (azsim LEAF_PREFIX rlk:combat/text_normal / text_crit, element/color):
    # here hers run for real, with a colour set as element/color would
    for fid in ('rlk:combat/text_normal_side', 'rlk:combat/text_normal_side_n', 'rlk:combat/text_crit_side'):
        s.cache[fid] = [l for l in (FN / (fid[4:] + '.mcfunction')).read_text(encoding='utf-8').split('\n') if l.strip() and not l.startswith('#')]
    s.storage.setdefault('rlk:combat', {}).update(col='#FF6633', sc1='#FFE08A', sc2='#FFC14A')
    cam_d = 4.0 + 4.0                                       # the player 4 b in front of her, the F5 camera 4 b behind the eyes
    rows = []
    for crit in (0, 1, 0, 1, 0, 1, 0, 1):
        s.call('rlk:combat/clear_atkflags', H.Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
        for k, v in (('#dmg', 259), ('#elem', 1), ('#elU', 0), ('#icd', 0), ('#crit', crit), ('#stunHit', 0), ('#hitLanded', 0),
                     ('#bowHit', 0), ('#lunar', 0), ('#tfm', 0), ('#trueDmg', 0), ('#skillDmg', 1)):
            s.setsc(k, 'tmp', v)
        n0 = {e.id for e in s.ents}
        s.stack.append('rlk:azsim/strike')
        try:
            s.call('rlk:combat/apply', H.Ctx(b, tuple(b.pos), tuple(b.rot)))
        finally:
            s.stack.pop()
        new = [e for e in s.ents if e.alive and e.id not in n0 and 'dmgText' in e.tags]
        for e in new:
            dx, dz = e.pos[0] - b.pos[0], e.pos[2] - b.pos[2]
            ax, az = pl.pos[0] - b.pos[0], pl.pos[2] - b.pos[2]
            n = math.hypot(ax, az)
            lat = abs(dx * az / n - dz * ax / n)              # off her -> player line
            px, sc = text_w_px(e, cam_d)
            rows.append(dict(crit=crit, n=len(new), lat=round(lat, 2), h=round(e.pos[1] - b.pos[1], 2), sc=sc, px=round(px)))
        for e in new:
            e.alive = False
    ok = all(r['n'] == 1 and 1.0 <= r['lat'] <= 1.6 and 1.8 <= r['h'] <= 2.5 and r['sc'] == (1.2 if r['crit'] else 0.9) for r in rows)
    ck(f'dmgnum: a hit on her body shows one number, 2/3 size (scale 0.9 / crit 1.2), beside her as seen from the player (off the '
       f'line to the player {min(r["lat"] for r in rows)}-{max(r["lat"] for r in rows)} b), at shoulder-head height '
       f'({min(r["h"] for r in rows)}-{max(r["h"] for r in rows)} b); at the fight camera ({cam_d:.0f} b, FOV 90, 1080p) "259" '
       f'{max(r["px"] for r in rows if not r["crit"])} px wide, a crit {max(r["px"] for r in rows if r["crit"])} px',
       ok and len(rows) == 8, rows[:4])
    # the old numbers for everything else (and the size her numbers had): the same macros as before, unchanged
    apply = fn_lines('combat/apply')
    ck('dmgnum: every other target keeps the old numbers (combat/text_normal_macro 1.35 / text_crit_macro 1.9 at +-0.8 b, 1.6-2.6 b): '
       'the two lines skip only rlk_mb_scarlet',
       sum(1 for l in apply if 'unless entity @s[tag=rlk_mb_scarlet]' in l and '_macro with storage rlk:combat' in l) == 2
       and any('if entity @s[tag=rlk_mb_scarlet] run function rlk:combat/text_normal_side' in l for l in apply)
       and 'scale:[1.35f' in (FN / 'combat/text_normal_macro.mcfunction').read_text(encoding='utf-8')
       and 'scale:[1.9f' in (FN / 'combat/text_crit_macro.mcfunction').read_text(encoding='utf-8'))
    old_n = 3 * 6 * GLYPH * 1.35 * PX_PER_B / cam_d
    old_c = (8 + 8 + 4 + 18 + 4 + 8 + 8 + 9) * GLYPH * 1.9 * PX_PER_B / cam_d
    print(f'   before (the same distance): "259" {old_n:.0f} px wide, a crit {old_c:.0f} px, both on her chest / head')


SECTIONS = [('trailcut', trailcut), ('dodgelock', dodgelock), ('dmgnum', dmgnum), ('dodgecam', dodgecam)]


def main():
    for name, f in SECTIONS:
        if want(name):
            print(f'== {name}', flush=True)
            f()
    print(f'test_wi: {NCK[0] - len(FAILS)}/{NCK[0]} passed' + (f'; FAILED: {FAILS}' if FAILS else ''))
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
