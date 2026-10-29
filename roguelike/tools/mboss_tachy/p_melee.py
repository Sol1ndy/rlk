"""Melee patterns of 타키 (Tachy): A1 돌진 베기, B1 날개 가리기 2연격, B2 옆걸음 4연격, B3 충전 6연격, C1-C3 연속기 · 블링크
(PLAN §4.2, footage sheets S:tk/ref/t_A1_v8.jpg, t_B1_v5.jpg, t_B2*_v5.jpg, t_B3*_v5.jpg, t_C*.jpg). OWNER: S3.

Every hit tick comes from api.ev (the clip events), every shape / tier / element from api.HITS, dash lengths from
api.DASH_LEN. All hazards are quiet (#hzQuiet 1, no ground telegraph: the footage shows none); the tells are the pose (the
rig clip from tick 0), the chest / visor flare, the blade glint and the sounds; the hit shows the slash itself (kit). The
body tracks the player between hits and stops turning s3lib.LOCK ticks before each hit (aim lock). G3 core windows are
the core's (api.G3_WINDOWS on #pt); the flare looks here match them.
"""
from . import api
from . import s3lib as S
from .s3lib import PB, sset

E = api.ev
OBJ = api.OBJ


def look(ch, v):
    return api.rig(f'look/{ch}/{v}')


EDGE_BACK = S.fn('el/edge')            # the blade edge back to the current element (core el/edge)
FACE = 'function rlk:mboss/mv/face'


def snd_tier(tier):
    return S.snd('slash_light' if tier == 'T1' else 'slash_heavy')


def strike(pb, idx, t, kind='arc', roll=0, pitch=0, yaw=0, r=None, grp=False, impact=False):
    """Visual + sound of hit idx at tick t (the hazard itself is pb.hit)."""
    clip, event, shape, dims, tier, el = api.HITS[pb.key][idx]
    r = r if r is not None else dims[0]
    if kind == 'arc':
        pb.at(t, S.fx_slash(r, el, roll=roll, pitch=pitch, yaw=yaw))
    elif kind == 'spin':
        pb.at(t, S.fx_spin(r, el))
    pb.at(t, snd_tier(tier))
    if impact:
        pb.at(t, S.fx_impact(el, fwd=min(r * 0.6, 2.4)))


def lock_track(pb, prev, t, deg=6):
    """Track the player from prev + 1 until LOCK ticks before the hit at t."""
    pb.track(prev + 1, t - S.LOCK, deg)


# ------------------------------------------------------------------------------------------------- A1 돌진 베기
def build_a1(W):
    pb = PB('a1', W)
    c = 'a1_dash'
    go, hit, end = E(c, 'go'), E(c, 'hit'), E(c, 'end')
    w0, w1 = api.G3_WINDOWS['a1']
    pb.at(0, FACE, api.play(c), look('chest', 'red'), S.fx_flare(2), S.snd('flare_tell'))
    pb.track(1, go - 6, 8)                                  # the line locks 6 t before the dash
    pb.at(w1, look('chest', 'off'))
    pb.dash(go, hit - go, api.DASH_LEN['a1'], stop_before=2.0, hit_idx=0, grp=True)
    pb.at(go, S.snd('dash'))
    pb.at(hit - 1, S.hazard('a1', api.HITS['a1'][1], grp=True))      # same volley group as the dash line
    pb.hit_ticks.append((hit, 1))
    strike(pb, 1, hit, roll=-20, impact=True)
    pb.end(end)
    pb.cancel_lines.append(f'execute as {S.BODY} at @s run {look("chest", "off")}')
    pb.write()
    return pb


# ------------------------------------------------------------------------------------------------- B1 날개 가리기 2연격
def build_b1(W):
    pb = PB('b1', W)
    c = 'b1_wrap2'
    op, h1, h2, end = E(c, 'open'), E(c, 'hit1'), E(c, 'hit2'), E(c, 'end')
    pb.at(0, FACE, api.play(c), S.snd('step'))
    # from mid range she walks in during the wrap (0.12 b/t) until 3 b
    pb.rng(1, op - 2, 'execute at @s unless entity @e[tag=rlk_body,distance=..3,limit=1] run function rlk:mboss/mv/toward {d:0.12}')
    lock_track(pb, 0, h1)
    pb.at(op, S.fx_plain('wing_flare', [], pos='~ ~1.4 ~'))
    pb.hit(0)
    strike(pb, 0, h1, roll=0)
    pb.advance(h1 + 2, h1 + 7, 0.17, 2.0)                    # 1 b in
    lock_track(pb, h1, h2)
    pb.group(h2 - 1)
    pb.hit(1, grp=True)
    pb.hit(2, grp=True)
    strike(pb, 1, h2, roll=-40, pitch=-20, impact=True)
    pb.end(end)
    pb.write()
    return pb


# ------------------------------------------------------------------------------------------------- B2 옆걸음 4연격
def build_b2(W):
    pb = PB('b2', W)
    c = 'b2_side4'
    land, h1, raise_, h2, h3, h4, end = (E(c, k) for k in ('land', 'hit1', 'raise', 'hit2', 'hit3', 'hit4', 'end'))
    # the hop: 3 b to her left or right (random; the other side when blocked; none when both are)
    pb.at(0, api.play(c), S.snd('step'), S.fn('p/b2/hop'))
    W.w('p/b2/hop', [
        '# B2 hop (@s = body): 3 b sideways over 12 t (mv/leap, apex 0.6 b), a random side first; the spot must pass mv/ok.',
        f'execute store result score #b2_s {OBJ} run random value 0..1',
        f'execute if score #b2_s {OBJ} matches 0 at @s rotated as @s rotated ~ 0 positioned ^3 ^ ^ if function rlk:mboss/mv/ok '
        'run return run function rlk:mboss/mv/leap {t:12,h:6}',
        'execute at @s rotated as @s rotated ~ 0 positioned ^-3 ^ ^ if function rlk:mboss/mv/ok '
        'run return run function rlk:mboss/mv/leap {t:12,h:6}',
        'execute at @s rotated as @s rotated ~ 0 positioned ^3 ^ ^ if function rlk:mboss/mv/ok '
        'run return run function rlk:mboss/mv/leap {t:12,h:6}'])
    pb.at(land - 2, FACE)                                    # she lands facing the player (the turn of B2)
    pb.advance(h1 - 4, h1 - 1, 0.375, 2.2)                   # the lunge (1.5 b)
    pb.hit(0)
    strike(pb, 0, h1, roll=25)
    lock_track(pb, h1, h2)
    pb.at(raise_, look('edge', 'glint'), S.snd('flare_tell'))
    pb.hit(1)
    strike(pb, 1, h2, roll=90, impact=True)
    pb.at(h2, EDGE_BACK)
    lock_track(pb, h2, h3, 8)
    pb.hit(2)
    strike(pb, 2, h3, roll=5)
    lock_track(pb, h3, h4, 8)
    pb.hit(3)
    strike(pb, 3, h4, roll=175)
    pb.end(end)
    pb.cancel_lines.append(f'execute as {S.BODY} at @s run {EDGE_BACK}')
    pb.write()
    return pb


# ------------------------------------------------------------------------------------------------- B3 충전 6연격
def build_b3(W):
    pb = PB('b3', W)
    c = 'b3_six'
    dash, h1, h2, h3, raise_, end = (E(c, k) for k in ('dash', 'hit1', 'hit2', 'hit3', 'raise', 'end'))
    bangs = [E(c, k) for k in ('bang1', 'bang2', 'bang3')]
    w0, w1 = api.G3_WINDOWS['b3']
    pb.at(0, FACE, api.play(c), look('chest', 'red'), S.fx_flare(2), S.snd('charge_core'))
    pb.track(1, dash - 4, 6)
    pb.at(w1, look('chest', 'off'))
    pb.at(dash - 1, FACE)
    pb.dash(dash, h1 - dash, 12.0, stop_before=2.5)          # dash-in to 2.5 b (no hit while dashing)
    pb.at(dash, S.snd('dash'))
    pb.hit(0)
    strike(pb, 0, h1, roll=-10, r=5.0)
    lock_track(pb, h1, h2)
    pb.hit(1)
    strike(pb, 1, h2, roll=170)
    lock_track(pb, h2, h3)
    pb.hit(2)
    strike(pb, 2, h3, roll=10)
    pb.at(raise_, look('edge', 'glint'))
    for i, b in enumerate(bangs):
        # re-aimed at each raise (<= 30 degrees, once, 10 t before the chop), then locked
        pb.at(b - 10, 'function rlk:mboss/mv/turn {max:30}')
        pb.group(b - 1)
        pb.hit(3 + 2 * i, grp=True, kb=2)
        pb.hit(4 + 2 * i, grp=True, kb=2)
        pb.at(b, S.fx_slash(3.2, api.PYRO, pitch=80), S.fx_impact(api.PYRO, fwd=2.0), S.snd('chop'),
              S.fx_plain('dust_ring', [], pos='^ ^0.1 ^2', r=14))
    pb.at(bangs[-1], EDGE_BACK)
    pb.end(end)
    pb.cancel_lines += [f'execute as {S.BODY} at @s run {x}' for x in (look('chest', 'off'), EDGE_BACK) if x]
    pb.write()
    return pb


# ------------------------------------------------------------------------------------------------- C1-C3 연속기 · 블링크
# (hit index, event, visual kind, roll, pitch, step-in) per combo; the thrust follows the glint by 18 t.
C_SPEC = {
    'c1': ('c1_combo', [(0, 'h1', 'arc', 35, 0, False), (1, 'h2', 'spin', 0, 0, True), (2, 'h3', 'arc', -35, 0, False),
                        (3, 'h4', 'arc', 45, 0, True)], 4),
    'c2': ('c2_combo', [(0, 'h1', 'arc', 30, 0, False), (1, 'h2', 'arc', -30, 0, False), (2, 'h3', 'arc', -20, -25, True)], 3),
    'c3': ('c3_combo', [(0, 'h1', 'arc', 30, 0, False), (1, 'h2', 'arc', -30, 0, False), (2, 'h3', 'arc', 20, 0, False),
                        (3, 'h4', 'arc', -45, 0, True), (4, 'h5', 'arc', 45, -15, True)], 5),
}


def build_c(key, W):
    clip, hits, thrust_idx = C_SPEC[key]
    pb = PB(key, W)
    glint, thrust, end = E(clip, 'glint'), E(clip, 'thrust'), E(clip, 'end')
    head = [FACE, api.play(clip)]
    if key in api.G3_WINDOWS:                                 # C3: the red core flare tell (G3 window)
        w0, w1 = api.G3_WINDOWS[key]
        head += [look('chest', 'red'), *S.fx_flare(2), *S.snd('flare_tell')]
        pb.at(w1, look('chest', 'off'))
    pb.at(0, head)
    prev = 0
    for idx, ev, kind, roll, pitch, step in hits:
        t = E(clip, ev)
        lock_track(pb, prev, t)
        if step:
            pb.advance(prev + 2, t - S.LOCK, 0.15, 3.0)
        pb.hit(idx)
        strike(pb, idx, t, kind=kind, roll=roll, pitch=pitch, impact=(kind == 'spin'))
        prev = t
    # glint: the point is locked (face the player once), the blade flashes gold; thrust 18 t later
    pb.at(glint, FACE, look('edge', 'glint'), S.fx_glint(), S.snd('glint'))
    pb.dash(thrust, 4, api.DASH_LEN[key], hit_idx=thrust_idx, trail='thrust_trail')
    pb.at(thrust, S.snd('thrust'), EDGE_BACK)
    pb.end(end)
    pb.cancel_lines += [f'execute as {S.BODY} at @s run {x}' for x in (look('chest', 'off'), EDGE_BACK) if x]
    pb.write()
    return pb


BUILT = {}


def _mk(key, f):
    def build(W):
        BUILT[key] = f(W)
    return build


PATTERNS = [
    api.Pattern('a1', S.TID['a1'], ('a1_dash',), _mk('a1', build_a1), notes='gap-close dash (far / mid), G3 window'),
    api.Pattern('b1', S.TID['b1'], ('b1_wrap2',), _mk('b1', build_b1), notes='P2+, near'),
    api.Pattern('b2', S.TID['b2'], ('b2_side4',), _mk('b2', build_b2), notes='near / mid, the rear-zone turn'),
    api.Pattern('b3', S.TID['b3'], ('b3_six',), _mk('b3', build_b3), notes='P3, G3 window'),
    api.Pattern('c1', S.TID['c1'], ('c1_combo',), _mk('c1', lambda W: build_c('c1', W))),
    api.Pattern('c2', S.TID['c2'], ('c2_combo',), _mk('c2', lambda W: build_c('c2', W))),
    api.Pattern('c3', S.TID['c3'], ('c3_combo',), _mk('c3', lambda W: build_c('c3', W)), notes='P3, G3 window'),
]
assert [p.key for p in PATTERNS] == list(api.MELEE)
