"""Phase-1 patterns of 아를레키노 (PLAN §5; OWNER: S3): A 사형장으로의 초대 (a2 / a4 / a5), B 붉은 달의 낫 (b1 / b2),
C 불꽃 도약 (c1 / c2), D 블러드 돌진 (d1 / d2), E 와리가리 베기 (e1), F 붉은 피의 연회 (f1), G 죽음의 칼날 (g1),
H 연옥 그림자 분신 (h1) and the 70 % event E70 재가 된 만상 (footage sheets S:ar/ref/p1_*.jpg).

Every hit tick comes from api.ev (the clip events), every shape / tier / Bond-of-Life flag from api.HITS, dash lengths
from api.DASH_LEN, heights from api.LEAP_H. Hazards are quiet (#hzQuiet 1); the floor markings of PLAN §1.5 (F's flood /
cracks, G's strips / rim tint, E70's pool) are the kit decals (api.K.decal; vanilla dust stand-ins while the kit is
missing). Tells are the pose (the rig clip from tick 0), the flames / crimson glow, the props and the sounds. The user's
lessons are built in: melee strings re-face and step in before every swing (a standing player is hit by each), only the
last hit of a string knocks back (api.KB_CHAIN / KB_FINAL), A runs only when the player is in reach (the AI gate) and
from 4.5-7 b she walks in during the raise, every far gap is closed by a dash / leap / dive to the player, every end point
goes through mv/ok inside api.MOVE_R, airborne parts are the clips' own (no added hovering).

TABLE[key] = the recorded hits (tick, HITS index, tell start, volley group, knockback, bol) for the tests (pat_p1.py).
"""
from . import api
from . import s3lib as S
from .s3lib import PB, sset, fn, num, part, placed

E = api.ev
OBJ = api.OBJ
CY = api.CY
FACE = 'function rlk:mboss/mv/face'
KB0, KB1 = api.KB_CHAIN, api.KB_FINAL
STEP, STOP = 0.3, 2.6           # step-in per tick / stop distance before a swing (her reach 4.2+)
LOCK, LOCK1 = S.LOCK, S.LOCK_FIRST
TABLE = {}
P1 = 1                          # the fight phase of every P1 hit (api.dmg)
BOL_C = api.C_BOL               # kit colour 2 (crimson) of Bond-of-Life hits, 1 (orange-gold) of plain Pyro
PY_C = api.C_PYRO


def look(ch, v):
    return api.rig(f'look/{ch}/{v}')


def snd(name, pos='at @s'):
    return placed(S.snd(name), pos)


def track_to(pb, prev, t, deg=12, lock=LOCK):
    """Re-face: turn toward the player from prev + 1 until `lock` ticks before the hit at t."""
    pb.track(prev + 1, t - lock, deg)


def step_in(pb, prev, t, d=STEP, stop=STOP):
    """Step in on prev + 2 .. t - 2 while the player is farther than stop (mv/step: mv/ok)."""
    pb.advance(prev + 2, t - 2, d, stop)


def at_lock():
    return f'at {S.LOCK_M} rotated as @s rotated ~ 0 positioned ~ {CY} ~'


def lockp():
    return fn('core/lockp')


def ground(pb, key):
    """A cancel of an airborne pattern puts her back on the floor (core/ground: mv/ok, else the arena centre)."""
    pb.cancel_lines.append(f'execute as {S.BODY} at @s run {fn("core/ground")}')


def finish(pb, key, *, clear_kit=False):
    if clear_kit and api.K.fixed('clear'):
        pb.cancel_lines.append(api.K.fixed('clear'))
    pb.write()
    TABLE[key] = pb.hits
    return pb


# ================================================================================================= A 사형장으로의 초대
# (hit index, event, visual, roll) per string: h1 sweep right -> left, h2 backhand, h3 spin ring, h4 overhead slam (+ the
# burst ahead, one group), h5 spin ring (PLAN §5.2 A; ref/p1_A_normal_2hit.jpg, p1_A_normal_5hit.jpg)
A_SPEC = {
    'a2': [((0,), 'h1', 'arc', 0), ((1,), 'h2', 'arc', 180)],
    'a4': [((0,), 'h1', 'arc', 0), ((1,), 'h2', 'arc', 180), ((2,), 'h3', 'spin', 0), ((3, 4), 'h4', 'slam', 90)],
    'a5': [((0,), 'h1', 'arc', 0), ((1,), 'h2', 'arc', 180), ((2,), 'h3', 'spin', 0), ((3, 4), 'h4', 'slam', 90),
           ((5,), 'h5', 'spin', 0)],
}


def build_a(key, W):
    pb = PB(key, W)
    clip = key
    spec = A_SPEC[key]
    end = E(clip, 'end')
    pb.at(0, FACE, api.play(clip), snd('step'))
    prev = 0
    for n, (idxs, ev, kind, roll) in enumerate(spec):
        t = E(clip, ev)
        last = n == len(spec) - 1
        kb = KB1 if last else KB0
        if n == 0:
            # the raise: from 4.5-7 b she walks in at 0.2 b / t (the AI starts A only within 7 b), the aim locks 8 t before
            pb.advance(1, t - 2, 0.2, STOP)
            track_to(pb, 0, t, 12, LOCK1)
        else:
            step_in(pb, prev, t)
            track_to(pb, prev, t, 14)
        g = pb.group(t - 1) if len(idxs) > 1 else 0
        tier = api.HITS[key][idxs[0]][4]
        for i in idxs:
            pb.hit(i, tell_from=0 if n == 0 else prev, grp=g, kb=kb)
        r = api.HITS[key][idxs[0]][3][0]
        if kind == 'arc':
            pb.at(t, S.fx_slash(r, PY_C, roll=roll), snd('swing_light' if tier == 'T1' else 'swing_heavy'))
        elif kind == 'spin':
            pb.at(t, S.fx_spin(r, PY_C), snd('spin'))
        else:
            ahead = api.HITS[key][idxs[1]][3][1]
            pb.at(t, S.fx_slash(r, PY_C, roll=90, pitch=-50, h=2.0),
                  S.fx_impact(2.2, PY_C, pos=f'{S.AT_BODY} positioned ^ ^0.2 ^{num(ahead, 2)}'), snd('slam'))
        prev = t
    pb.end(end)
    return finish(pb, key)


# ================================================================================================= B 붉은 달의 낫
WHEEL_H = 1.2                      # the wheel's centre over the floor (hr 1.1: it covers 0.1-2.3 b)
_ID = 'left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f]'


def wheel_params(key):
    clip, ev_, shape, dims, tier, bol = api.HITS[key][0]
    hr, spd, rng = dims
    eff = pj_eff(spd)
    life = -(-int(round(rng * 100)) // int(round(eff * 100)))
    return hr, spd, life, api.dmg(tier, P1)


def pj_eff(spd):
    """The flown speed of pj/launch (0.25 b sub-steps, rounded up: 1.4 -> 1.5 b / t)."""
    return (-(-int(round(spd * 100)) // 25)) * 0.25


def prop_nbt(key, extra_tags, item, scale):
    """One display per projectile (the user's rule: exactly one card per projectile, facing its travel direction): the kit
    dresses it (fx/prop/<name>); the stand-in is the plain item at that scale."""
    tags = S.tags_nbt(key, *extra_tags)
    if api.K._on():
        return f'{{Tags:{tags},teleport_duration:1}}'
    return (f'{{Tags:{tags},teleport_duration:1,brightness:{{sky:15,block:15}},item:{{id:"{item}",count:1}},'
            f'transformation:{{{_ID},scale:[{scale[0]}f,{scale[1]}f,{scale[2]}f]}}}}')


def write_wheel(key, W):
    """p/<key>/wheel (as the body): one outward wheel from her chest along her yaw; p/<key>/pj_end turns it (event 1 / 2)
    into a returning wheel (a new prop, a new volley group: out and back hit separately) that dies at her hand."""
    hr, spd, life, dmg = wheel_params(key)
    W.w(f'p/{key}/wheel', [
        f'# {key.upper()} one wheel (@s = body): a vertical flaming wheel pj (hr {hr}, {spd} b/t, {life} t out, wall stop),',
        f'# its centre {WHEEL_H} b over the floor, {api.HITS[key][0][4]} plain Pyro; a new volley group per leg.',
        f'execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^0.8 positioned ~ {num(CY + WHEEL_H)} ~ run summon '
        f'minecraft:item_display ~ ~ ~ {prop_nbt(key, ("rlk_kn_wheel", "rlk_kn_new"), "minecraft:fire_charge", (2.2, 2.2, 0.2))}',
        f'execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s rotated as {S.BODY} rotated ~ 0 run {fn(f"p/{key}/launch")}'])
    W.w(f'p/{key}/launch', [f'# @s = the new outward wheel (positioned / rotated as the release).',
                            'tag @s remove rlk_kn_new', 'tag @s add rlk_kn_out', api.K.prop('wheel'), S.L.GRP_NEW]
        + S.L.pj_opts(el=api.PYRO, kb=0, wall=1, grp=True) + [S.L.pj_launch(spd, life, dmg, hr)])
    W.w(f'p/{key}/pj_end', [
        f'# {key.upper()} wheel event (@s = the prop; #pjEv 1 wall, 2 life over, 4 hit the player: it flies on, harmless).',
        'execute unless score #pjEv mb matches 1..2 run return 0',
        f'execute if entity @s[tag=rlk_kn_out] run return run {fn(f"p/{key}/turn")}',
        f'execute at @s run {fn(f"p/{key}/caught")}'])
    W.w(f'p/{key}/turn', [
        '# The outward wheel turns back (@s = it): a new returning wheel here, flying back to her for as many ticks as the',
        '# outward leg flew (she does not move while it flies), a new volley group. summon never takes the execute rotation (the',
        '# new prop faces yaw 0), so the flight direction is aimed at her here: facing her feet, level.',
        f'execute store result storage {api.STORAGE} core.wb.life int 1 run scoreboard players get @s mbPjT',
        f'execute at @s run summon minecraft:item_display ~ ~ ~ '
        f'{prop_nbt(key, ("rlk_kn_wheel", "rlk_kn_new"), "minecraft:fire_charge", (2.2, 2.2, 0.2))}',
        f'execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s facing entity {S.BODY} feet rotated ~ 0 run '
        f'{fn(f"p/{key}/back")} with storage {api.STORAGE} core.wb'])
    W.w(f'p/{key}/back', ['# $(life): the returning wheel (@s = the new prop, rotated toward her).',
                          'tag @s remove rlk_kn_new', 'tag @s add rlk_kn_ret', api.K.prop('wheel'), S.L.GRP_NEW]
        + S.L.pj_opts(el=api.PYRO, kb=0, wall=0, grp=True)
        + [f'$function rlk:mboss/pj/launch {{spd:{S.L.pj_speed_tenths(spd)},life:$(life),dmg:{dmg},'
           f'hr:{int(round(hr * 10))}}}'])
    W.w(f'p/{key}/caught', ['# The returning wheel reached her (@s = the prop, at it): gone, the catch sound.']
        + S.placed(S.snd('wheel_catch'), 'at @s'))
    if api.K.prop('wheel'):
        W.w(f'p/{key}/resume', [f'# {key.upper()} resume: the wheel looks again (pause cleared the kit cards).',
                                f'execute as @e[type=minecraft:item_display,tag={S.tag_p(key)},tag=rlk_kn_wheel] run '
                                f'{api.K.prop("wheel")}'])


def wheel_flight_fx(pb, key, t0, t1):
    """Stand-in flames on the flying wheels (the kit prop carries its own), every 2 t."""
    if api.K.prop('wheel'):
        return
    for t in range(t0, t1 + 1, 2):
        pb.at(t, f'execute as @e[type=minecraft:item_display,tag={S.tag_p(key)},tag=rlk_kn_wheel] at @s run '
                 f'{part("minecraft:flame", 0.5, 0.6, 0.5, 0.02, 6)}')


def build_b(key, W):
    pb = PB(key, W)
    clip = key
    write_wheel(key, W)
    end = E(clip, 'end')
    rel = [E(clip, 'release')] if key == 'b1' else [E(clip, 'rel1'), E(clip, 'rel2')]
    pb.at(0, FACE, api.play(clip))
    pb.at(E(clip, 'spin'), snd('wheel_spin'), S.fx('scythe_form', [part(S.FLAME[1], 0.4, 0.6, 0.4, 0.03, 10)]))
    prev = 0
    hr, spd, life, dmg = wheel_params(key)
    for n, t in enumerate(rel):
        if n == 0:
            track_to(pb, prev, t, 10, LOCK1)
        else:
            # the second wheel leads the player (mv/lockv lead 6), aimed 6 t before the release
            track_to(pb, prev, t - 7, 10, 0)
            pb.at(t - 6, S.L.lockv(6), f'execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0')
            pb.at(E(clip, 'spin2'), snd('wheel_spin'))
        pb.at(t, fn(f'p/{key}/wheel'), look('weapon_r', 'gone'), snd('wheel_throw'),
              S.fx('wheel_trail', [], pos=f'{S.AT_BODY} positioned ~ {CY} ~', len=160))
        pb.at(t + 2 * life + 1, look('weapon_r', 'hand'))
        idx = n
        h = api.HITS[key][idx]
        assert api.ev(h[0], h[1]) == t
        pb.hits.append(dict(t=t, idx=idx, tell=prev, grp=-1, kb=0, bol=h[5], shape=h[2]))
        wheel_flight_fx(pb, key, t + 1, t + 2 * life + 1)
        prev = t
    if key == 'b1':
        pb.at(E(clip, 'catch'), look('weapon_r', 'hand'))
    else:
        reach, lockt, grab = E(clip, 'reach'), E(clip, 'lock'), E(clip, 'grab')
        # the grab (PLAN §5.2 B2): the arm reaches out with a crimson palm (20 t tell), the spot locks at 80, the claw
        # card appears at 92, it closes at 96 (Bond of Life); no floor decal
        track_to(pb, rel[-1], lockt, 10, 0)
        pb.at(reach, look('glow', 'crimson'), api.rig('anchor/palm_r'), snd('claw_reach'),
              S.fx('shock_aura', [part(S.DUST[2], 0.2, 0.2, 0.2, 0, 10)], pos=f'at @e[tag={api.TAGS["anchor"]},limit=1]'))
        pb.at(lockt, lockp())
        for t in range(lockt + 2, grab, 3):
            if not api.K.p('claw', r=22):
                pb.at(t, f'execute at {S.LOCK_M} positioned ~ ~1.2 ~ run {part(S.DUST[2], 0.9, 0.5, 0.9, 0, 6)}')
        pb.at(grab - 4, S.fx('claw', [part(S.DUST[2], 1.0, 0.8, 1.0, 0, 30)], pos=f'at {S.LOCK_M} positioned ~ ~1 ~', r=22))
        pb.hit(2, tell_from=reach, kb=KB1, pos=at_lock())
        pb.at(grab, S.fx_impact(2.2, BOL_C, pos=f'at {S.LOCK_M}'), snd('claw_grab', f'at {S.LOCK_M}'), look('glow', 'normal'))
    pb.end(end)
    pb.cancel_lines.append(f'execute as {S.BODY} at @s run {look("weapon_r", "hand")}')
    return finish(pb, key)


# ================================================================================================= C 불꽃 도약
def build_c(key, W):
    pb = PB(key, W)
    clip = key
    jump, apex, lockt, dive, impact, end = (E(clip, k) for k in ('jump', 'apex', 'lock', 'dive', 'impact', 'end'))
    h = api.LEAP_H[key]
    pb.at(0, FACE, api.play(clip))
    track_to(pb, 0, jump, 10, 1)
    # jump: +9 b in 10 t (the flaming crescent at the take-off), apex: spins with flame and drifts toward the player
    pb.at(jump, f'execute at @s positioned ~ ~{num(h)} ~ run function rlk:mboss/mv/glide {{t:{apex - jump}}}',
          S.fx('leap_flare', [part(S.FLAME[1], 0.6, 0.3, 0.6, 0.05, 20)], pos=f'{S.AT_BODY} positioned ~ ~0.3 ~'),
          snd('leap'))
    pb.at(apex, snd('apex'))
    pb.rng(apex + 1, lockt - 1, fn('core/air/drift'))
    pb.track(apex + 1, lockt, 20)
    for t in range(apex + 2, lockt, 4):
        pb.at(t, f'execute at @s run {part(S.FLAME[1], 0.6, 0.6, 0.6, 0.04, 8)}')
    # lock 44 (the player's spot, inside MOVE_R, mv/ok), dive 48 -> impact 54 at the locked spot
    pb.at(lockt, lockp(), fn('core/lock_short'), f'execute at @s facing entity {S.LOCK_M} feet run tp @s ~ ~ ~ ~ 0',
          snd('dash_tell'))
    pb.at(dive, f'execute positioned as {S.LOCK_M} run function rlk:mboss/mv/glide {{t:{impact - dive}}}',
          S.fx('dive_streak', [], pos=f'{S.AT_BODY} positioned ~ ~1 ~', len=int(h * 10)), snd('dive'))
    g = pb.group(impact - 1)
    kb = KB1 if key == 'c1' else KB0
    pb.hit(0, tell_from=0, grp=g, kb=kb, pos=at_lock())
    pb.hit(1, tell_from=0, grp=g, kb=kb, pos=at_lock())
    pb.at(impact, S.fx_impact(3.6, PY_C, pos=f'at {S.LOCK_M}'), S.fx_slash(4.0, PY_C, roll=90, pitch=-40, h=2.0), snd('impact'))
    if key == 'c2':
        wo, wing = E(clip, 'wing_open'), E(clip, 'wing')
        tell = wing - 12
        # the wing strike (Bond of Life): the wings burst open 12 t before (the crimson tell), she re-faces and steps in
        step_in(pb, impact, wing)
        track_to(pb, impact, wing, 12)
        pb.at(tell, look('wings', 'open'), look('glow', 'crimson'), S.fx('wing_burst', [part(S.DUST[2], 1.2, 1.0, 1.2, 0, 30)]),
              snd('wing_burst'))
        pb.at(wo, snd('wing_burst'))
        pb.hit(2, tell_from=tell, kb=KB1)
        pb.at(wing, S.fx_slash(5.6, BOL_C, roll=10, h=1.8), snd('wing_hit'), look('glow', 'normal'))
        pb.at(130, look('wings', 'off'))
    pb.end(end)
    ground(pb, key)
    return finish(pb, key)


# ================================================================================================= D 블러드 돌진
def dash_lines(pb, key, t_go, ticks, max_b, extra, hit_idx, grp, kb):
    """A straight dash along the locked body yaw: decided at t_go - 1 (length = the player distance + extra, at most
    max_b, probed in 0.5 b steps through mv/ok: the end point is inside the arena's safe disc and never in a block),
    glided over `ticks` from t_go; the api.HITS dash_line hazard is made at t_go - 1 (strikes at t_go, active `ticks`
    ticks while its length grows with the body: core/dash/grow)."""
    dl = f'#{key}_dl'
    clip, event, shape, dims, tier, bol = api.HITS[key][hit_idx]
    assert shape == 'dash_line' and api.ev(clip, event) == t_go
    lines = ['function rlk:mboss/mv/dist',
             f'scoreboard players operation #t {OBJ} = #mbDist mb',
             f'scoreboard players add #t {OBJ} {int(round(extra * 10))}',
             f'scoreboard players operation #t {OBJ} /= #c5 {OBJ}',
             f'execute if score #t {OBJ} matches {int(max_b * 2) + 1}.. run scoreboard players set #t {OBJ} {int(max_b * 2)}',
             fn('core/dash/probe'),
             f'scoreboard players operation {dl} {OBJ} = #t2 {OBJ}',
             f'execute positioned as @e[type=minecraft:marker,tag=rlk_kn_dp,limit=1] run function rlk:mboss/mv/glide {{t:{int(ticks)}}}',
             'kill @e[type=minecraft:marker,tag=rlk_kn_dp]',
             f'data modify storage {api.STORAGE} core.dl set value {{len:0,w:{int(round(dims[0] * 10))},tell:1,'
             f'dmg:{api.dmg(tier, P1)}}}',
             f'execute store result storage {api.STORAGE} core.dl.len int 5 run scoreboard players get {dl} {OBJ}']
    lines += S.L.hz_opts(quiet=1, sfx=0, grp=bool(grp), act=ticks, kb=kb, el=api.PYRO)
    lines += [f'execute {S.AT_BODY} positioned ~ {CY} ~ run function rlk:mboss/hz/line with storage {api.STORAGE} core.dl',
              S.hz_tag(key),
              f'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_kn_dl']
    pb.at(t_go - 1, lines)
    for j in range(ticks):
        pb.at(t_go + j,
              f'scoreboard players operation #hzSzR mb = {dl} {OBJ}',
              f'scoreboard players set #t3 {OBJ} {5 * (j + 1)}',
              f'scoreboard players operation #hzSzR mb *= #t3 {OBJ}',
              f'scoreboard players set #t3 {OBJ} {int(ticks)}',
              f'scoreboard players operation #hzSzR mb /= #t3 {OBJ}',
              f'execute as @e[type=minecraft:marker,tag=rlk_kn_dl,tag={S.tag_p(key)}] run {fn("core/dash/grow")}')
    mx = int(max_b * 2)
    vis = []
    for lo, hi, ln in ((0, mx // 3, mx * 5 // 3), (mx // 3 + 1, 2 * mx // 3, 2 * mx * 5 // 3), (2 * mx // 3 + 1, mx, mx * 5)):
        k = api.K.p('dash_trail', len=ln, c=PY_C)
        if k:
            vis.append(f'execute if score {dl} {OBJ} matches {lo}..{hi} {S.AT_BODY} positioned ~ ~1 ~ run {k}')
    if not vis:
        vis = [f'execute at @s run {part(S.FLAME[1], 0.4, 0.5, 0.4, 0.06, 16)}']
    pb.at(t_go, vis)
    for j in range(1, ticks):
        if not api.K.p('dash_trail', len=10, c=PY_C):
            pb.at(t_go + j, f'execute at @s run {part(S.FLAME[1], 0.3, 0.5, 0.3, 0.04, 10)}')
    if bol:
        for j in range(ticks):
            pb.at(t_go + j, S.bol_mark())
    return dl


def build_d(key, W):
    pb = PB(key, W)
    clip = key
    go, hit, end = E(clip, 'go'), E(clip, 'hit'), E(clip, 'end')
    follow = key == 'd2'
    kb = KB0 if follow else KB1
    # flare (red flare on her body, the scythe drawn back low; v2 7.8): the line locks 6 t before the dash
    pb.at(0, FACE, api.play(clip), S.fx('embers_puff', [part(S.DUST[1], 0.3, 0.6, 0.3, 0, 16)]), snd('dash_tell'))
    track_to(pb, 0, go, 8, 6)
    g = pb.group(go - 1)
    dash_lines(pb, key, go, hit - go, api.DASH_LEN[key], 1.5, 0, g, kb)
    pb.hits.append(dict(t=go, idx=0, tell=0, grp=g, kb=kb, bol=0, shape='dash_line'))
    pb.at(go, snd('dash'))
    pb.hit(1, tell_from=0, grp=g, kb=kb)
    pb.at(hit, S.fx_slash(4.2, PY_C, roll=20), snd('sweep'))
    if follow:
        fhit = E(clip, 'fhit')
        dec = fhit - 12
        # the follow-up (v2 9.9-10.2) only if the dash landed (#hitev on the dash ticks) or the player is within 5 b
        pb.rng(go + 1, hit + 1, f'execute if score #hitev {OBJ} matches 1.. run scoreboard players set #d2_l {OBJ} 1')
        pb.at(0, sset('#d2_l', 0))
        W.w('p/d2/decide', ['# D2 (@s = body, 12 t before the follow-up): it runs if the dash landed or the player is within 5 b;',
                            '# otherwise the cast ends here (the recovery follows).',
                            f'execute if score #d2_l {OBJ} matches 1 run return 0',
                            f'execute at @s if entity {S.PLAYER[:-1]},distance=..5] run return 0',
                            sset('#done', 1)])
        pb.at(dec, fn('p/d2/decide'), snd('follow'))
        step_in(pb, hit, fhit)
        track_to(pb, hit, fhit, 14)
        g2 = pb.group(fhit - 1)
        pb.hit(2, tell_from=hit, grp=g2, kb=KB1)
        pb.hit(3, tell_from=hit, grp=g2, kb=KB1)
        pb.at(fhit, S.fx_impact(3.2, PY_C), S.fx_slash(4.0, PY_C, roll=100, pitch=-30, h=2.0), snd('slam'))
    pb.end(end)
    return finish(pb, key)


# ================================================================================================= E 와리가리 베기
def build_e(W):
    key = clip = 'e1'
    pb = PB(key, W)
    zig = [E(clip, f'zig{i}') for i in range(1, 6)]
    rise, lockt, go, sweep, spin, end = (E(clip, k) for k in ('rise', 'lock', 'go', 'sweep', 'spin', 'end'))
    hy = api.LEAP_H['e1']
    # rise: she hops back to 10-12 b from the player and hovers 2.5 b up (p/e1/spot: mv/ok on the floor below)
    W.w('p/e1/spot', [
        '# E1 hover spot (@s = body): 11 b from the player on the player -> her line (else 30 / 60 deg aside, else 8 b, else',
        f'# here), {hy} b up; the floor spot below must pass mv/ok. Glide there over 12 t.',
        'kill @e[type=minecraft:marker,tag=rlk_kn_dp]']
        + [f'execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at {S.PLAYER} facing entity @s feet rotated ~{a} 0 '
           f'positioned ^ ^ ^{d} positioned ~ {CY} ~ if function rlk:mboss/mv/ok run summon minecraft:marker ~ ~ ~ '
           f'{{Tags:{S.tags_nbt(key, "rlk_kn_dp")}}}'
           for d in (11, 8) for a in (0, 30, -30, 60, -60)]
        + [f'execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at @s positioned ~ {CY} ~ run summon minecraft:marker '
           f'~ ~ ~ {{Tags:{S.tags_nbt(key, "rlk_kn_dp")}}}',
           f'execute positioned as @e[type=minecraft:marker,tag=rlk_kn_dp,limit=1] positioned ~ ~{num(hy)} ~ run '
           'function rlk:mboss/mv/glide {t:12}',
           'kill @e[type=minecraft:marker,tag=rlk_kn_dp]'])
    for side, (a, b) in (('l', (4, -4)), ('r', (-4, 4))):
        W.w(f'p/e1/zig_{side}', [
            f'# One lateral dash (@s = body, facing the player): 4 b to her {"left" if side == "l" else "right"} at the hover',
            '# height over 4 t; the floor spot below must pass mv/ok, else the other side, else none.']
            + [f'execute at @s rotated as @s rotated ~ 0 positioned ^{x} ^ ^ positioned ~ {CY} ~ if function rlk:mboss/mv/ok at @s '
               f'rotated as @s rotated ~ 0 positioned ^{x} ^ ^ run return run function rlk:mboss/mv/glide {{t:4}}' for x in (a, b)])
    pb.at(rise, FACE, api.play(clip), fn('p/e1/spot'), snd('leap'))
    pb.track(1, lockt, 20)
    for i, t in enumerate(zig):
        pb.at(t, fn('p/e1/zig_l') if i % 2 == 0 else fn('p/e1/zig_r'),
              S.fx('zig_streak', [part(S.DUST[1], 0.8, 0.3, 0.8, 0, 14)], pos=f'{S.AT_BODY} positioned ~ ~1.2 ~', len=40),
              snd('zig'))
    # lock 64 (the glint + tell sound), go 70: a 6 t dive to the locked spot, sweep 76 there, spin 92 (re-faced, stepped in)
    pb.at(lockt, lockp(), fn('core/lock_short'), f'execute at @s facing entity {S.LOCK_M} feet run tp @s ~ ~ ~ ~ 0',
          snd('dash_tell'), S.fx('leap_flare', [part('minecraft:end_rod', 0.2, 0.2, 0.2, 0.02, 6)]))
    pb.at(go, f'execute positioned as {S.LOCK_M} run function rlk:mboss/mv/glide {{t:{sweep - go}}}', snd('dive'),
          S.fx('dive_streak', [], pos=f'{S.AT_BODY} positioned ~ ~1 ~', len=60))
    pb.hit(0, tell_from=lockt, kb=KB0, pos=at_lock())
    pb.at(sweep, S.fx_slash(5.2, PY_C, roll=0), snd('sweep'))
    step_in(pb, sweep, spin)
    track_to(pb, sweep, spin, 14)
    pb.hit(1, tell_from=sweep, kb=KB1)
    pb.at(spin, S.fx_spin(4.2, PY_C, h=1.6), S.fx_slash(4.2, PY_C, roll=90, pitch=-60, h=2.0), snd('spin'))
    pb.end(end)
    ground(pb, key)
    return finish(pb, key)


# ================================================================================================= F 붉은 피의 연회
WALK10 = int(api.WALK * 10)


def flood_stand_in(pb, t0, t1):
    """Vanilla stand-in of the flood decal (the kit draws it otherwise): crimson dust over the floor every 4 t."""
    if api.K._on():
        return
    for t in range(t0, t1, 4):
        pb.at(t, f'execute at {S.ARENA_M} positioned ~ {num(CY + 0.1)} ~ run '
                 f'{part(S.DUST[2], api.WALK * 0.45, 0.02, api.WALK * 0.45, 0, 160)}')


def build_f(W):
    key = clip = 'f1'
    pb = PB(key, W)
    raise_, brand, centre, arms, flood, hit1, wings, hit2, end = (
        E(clip, k) for k in ('raise', 'brand', 'centre', 'arms', 'flood', 'hit1', 'wings', 'hit2', 'end'))
    pb.at(raise_, FACE, api.play(clip), look('glow', 'crimson'), snd('brand'))
    # the crimson sigil ring contracts onto the player 6-22 (kit brand_ring; stand-in: a shrinking dust ring)
    pb.at(6, S.fx('brand_ring', [], pos=f'at {S.PLAYER}'))
    if not api.K._on():
        for t in range(6, brand, 2):
            r = 3.0 - (t - 6) * 2.5 / (brand - 6)
            pb.at(t, f'execute at {S.PLAYER} positioned ~ ~0.2 ~ run {part(S.DUST[2], r * 0.6, 0.05, r * 0.6, 0, 12)}')
    pb.at(brand, api.BOND_CALLS['force'])
    # she glides to the arena centre, arms out; the flood spreads from 110 (48 t) and flashes 6 t before each hit
    pb.at(centre, f'execute positioned as {S.ARENA_M} positioned ~ {CY} ~ run function rlk:mboss/mv/glide {{t:16}}')
    pb.track(centre + 17, hit1 - 8, 6)
    k = api.K.decal('flood', r=WALK10, t=hit1 - flood)
    pb.at(flood, placed([k], f'at {S.ARENA_M} positioned ~ {CY} ~') if k else [], snd('flood'))
    flood_stand_in(pb, flood, hit1)
    pb.hit(0, tell_from=flood, kb=KB0, pos=f'at {S.ARENA_M} positioned ~ {CY} ~')
    # combat overhaul (rulings B-01 / B-02): both hits cover the whole arena (unparriable by the framework's rule, dodgeable):
    # the warning glint on her chest when each hit's tell starts (the flood / the wings), >= TELL_BIG t before it
    assert hit1 - flood >= api.TELL_BIG and hit2 - wings >= api.TELL_BIG
    pb.at(flood, S.np_warn())
    pb.at(wings, S.np_warn())
    pb.at(hit1, S.fx('threads', [part(S.DUST[2], 8, 3, 8, 0, 200)], pos=f'at {S.ARENA_M} positioned ~ {num(CY + 0.2)} ~', r=WALK10),
          S.fx('thorns', [], pos=f'at {S.ARENA_M} positioned ~ {CY} ~', r=WALK10), snd('threads'))
    # wings 166: she rises 1 b, wings open; the flood flashes again for hit2
    pb.at(wings, look('wings', 'open'), 'execute at @s positioned ~ ~1 ~ run function rlk:mboss/mv/glide {t:6}',
          S.fx('wing_burst', [part(S.DUST[2], 1.2, 1.0, 1.2, 0, 30)]), snd('wing_burst'))
    k2 = api.K.decal('flood', r=WALK10, t=hit2 - wings)
    if k2:
        pb.at(wings, placed([k2], f'at {S.ARENA_M} positioned ~ {CY} ~'))
    flood_stand_in(pb, wings, hit2)
    pb.hit(1, tell_from=wings, kb=KB1, pos=f'at {S.ARENA_M} positioned ~ {CY} ~')
    kc = api.K.decal('cracks', r=WALK10)
    pb.at(hit2, S.fx('blast', [part('minecraft:explosion', 6, 0.5, 6, 0, 24)], pos=f'at {S.ARENA_M} positioned ~ {CY} ~',
                     r=WALK10), snd('blast'), snd('cracks'), placed([kc], f'at {S.ARENA_M} positioned ~ {CY} ~') if kc else [],
          look('glow', 'normal'))
    pb.at(hit2 + 4, f'execute at @s positioned ~ {CY} ~ run function rlk:mboss/mv/glide {{t:10}}')
    pb.at(end - 10, look('wings', 'off'))
    pb.end(end)
    # resume: the flood decal again with the ticks left to the next hit (the pause cleared the kit cards)
    if api.K._on():
        W.w('p/f1/resume', [
            '# F1 resume (@s = body): the flood decal again with the ticks left to the next hit.',
            f'data modify storage {api.STORAGE} core.dec set value {{r:{WALK10},t:0}}',
            f'execute if score #pt {OBJ} matches {flood}..{hit1 - 1} run scoreboard players set #t {OBJ} {hit1}',
            f'execute if score #pt {OBJ} matches {wings}..{hit2 - 1} run scoreboard players set #t {OBJ} {hit2}',
            f'execute unless score #pt {OBJ} matches {flood}..{hit1 - 1} unless score #pt {OBJ} matches {wings}..{hit2 - 1} run return 0',
            f'scoreboard players operation #t {OBJ} -= #pt {OBJ}',
            f'execute store result storage {api.STORAGE} core.dec.t int 1 run scoreboard players get #t {OBJ}',
            f'execute at {S.ARENA_M} positioned ~ {CY} ~ run {S.kit_with("decal/", "flood", "core.dec")}'])
    ground(pb, key)
    return finish(pb, key, clear_kit=True)


# ================================================================================================= G 죽음의 칼날
# G thorns: sideways offsets across the 3 b line (alternating sides segment by segment) and heights (tenths, foot-anchored)
THORN_X = (-0.55, 0.5, -0.05)
THORN_H = (26, 19, 29, 22, 17, 25, 28, 20, 24, 18, 27, 21)
WALK_M = f'@e[type=minecraft:marker,tag=rlk_mb_arena,distance=..{num(api.WALK + 0.5)}]'
# where a G cross blade may stand: on the walk disc (r 26 + 0.5) with free feet and head (mv/ok's block tests; mv/ok's own
# safe disc, r 23.5, is the body's and would keep the side blades of a cross locked near the rim off the floor)
BLADE_OK = f'if entity {WALK_M} if block ~ ~ ~ #rlk:dash_pass if block ~ ~1 ~ #rlk:dash_pass'
BLADE_D = (14, 10.5, 7, 3.5)            # a cross blade's stand-off from the lock along its arm, outermost that passes


def blade_nbt(key, arm=None):
    tags = ('rlk_kn_blade', 'rlk_kn_new') if arm is None else ('rlk_kn_blade', f'rlk_kn_b{arm}', 'rlk_kn_new')
    return prop_nbt(key, tags, 'minecraft:red_stained_glass_pane', (1.4, 5.0, 1.4))


def write_g(W):
    key = 'g1'
    dress = [f'execute as @e[type=minecraft:item_display,tag=rlk_kn_new] run {api.K.prop("blade")}'] if api.K.prop('blade') else []
    W.w('p/g1/cross', [
        '# G1 (@s = body): the four giant blades at the ends of the cross through the lock (arms 14 b, the lock marker\'s',
        '# yaw = the cross axis; an arm end off the walk disc or in a block pulls its blade in to 10.5 / 7 / 3.5 b, else',
        '# that arm has none), each turned to face the lock (level: they fly in along their arms before the strike;',
        '# summon never takes the execute rotation), the strip decals (t = ticks to the strike in #t kn), the rise burst.',
        f'kill @e[type=minecraft:item_display,tag=rlk_kn_blade,tag={S.tag_p(key)}]']
        + [f'execute {"" if i == 0 else f"unless entity @e[type=minecraft:item_display,tag=rlk_kn_b{a},tag=rlk_kn_new] "}'
           f'at {S.LOCK_M} rotated as {S.LOCK_M} rotated ~{a} 0 positioned ^ ^ ^{num(d)} positioned ~ {CY} ~ {BLADE_OK} run '
           f'summon minecraft:item_display ~ ~ ~ {blade_nbt(key, a)}' for a in (0, 90, 180, 270) for i, d in enumerate(BLADE_D)]
        + dress
        + [f'execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s facing entity {S.LOCK_M} feet run tp @s ~ ~ ~ ~ 0',
           'tag @e[type=minecraft:item_display,tag=rlk_kn_new] remove rlk_kn_new']
        + S.placed(S.snd('blade_rise'), f'at {S.LOCK_M}')
        + [f'execute as @e[type=minecraft:item_display,tag=rlk_kn_blade,tag={S.tag_p(key)}] at @s run {x}'
           for x in S.fx('blade_rise', [part(S.DUST[2], 0.4, 1.5, 0.4, 0, 16)], pos='positioned ~ ~ ~')]
        + ([f'execute store result storage {api.STORAGE} core.st.yaw int 1 run data get entity {S.LOCK_M} Rotation[0]',
            f'execute store result storage {api.STORAGE} core.st.t int 1 run scoreboard players get #t {OBJ}',
            f'execute at {S.LOCK_M} positioned ~ {CY} ~ run {S.kit_with("decal/", "strip", "core.st")}',
            f'execute store result storage {api.STORAGE} core.st.yaw int 1 run scoreboard players get #t2 {OBJ}',
            f'execute at {S.LOCK_M} positioned ~ {CY} ~ run {S.kit_with("decal/", "strip", "core.st")}']
           if api.K._on() else []))
    W.w('p/g1/strips', [
        '# G1 stand-in strips (no kit; @s = body): crimson dust along both cross lines.']
        + [f'execute at {S.LOCK_M} rotated as {S.LOCK_M} rotated ~{a} 0 positioned ^ ^ ^{d} positioned ~ {num(CY + 0.1)} ~ run '
           f'{part(S.DUST[2], 0.6, 0.02, 0.6, 0, 2)}' for a in (0, 90) for d in range(-14, 15, 2)])
    W.w('p/g1/rim', [
        '# G1 rim (@s = body): twelve blades erupt around the rim (r 24, 30 deg apart), the floor tint grows (34 t).',
        f'kill @e[type=minecraft:item_display,tag=rlk_kn_blade,tag={S.tag_p(key)}]']
        + [f'execute at {S.ARENA_M} rotated {a} 0 positioned ^ ^ ^24 positioned ~ {CY} ~ run summon minecraft:item_display ~ ~ ~ '
           f'{blade_nbt(key)}' for a in range(0, 360, 30)]
        + dress + ['tag @e[type=minecraft:item_display,tag=rlk_kn_new] remove rlk_kn_new']
        + S.placed(S.snd('rim'), f'at {S.ARENA_M}')
        + ([placed([api.K.decal('rim_tint', r0=0, r=240, t=34)], f'at {S.ARENA_M} positioned ~ {CY} ~')[0]]
           if api.K._on() else []))


def build_g(W):
    key = clip = 'g1'
    pb = PB(key, W)
    write_g(W)
    plant, blades, cross1, relock, cross2, rim, field, end = (
        E(clip, k) for k in ('plant', 'blades', 'cross1', 'relock', 'cross2', 'rim', 'field', 'end'))
    pb.at(plant, FACE, api.play(clip), look('glow', 'crimson'), snd('brand'))
    pb.track(1, blades - 1, 12)
    # the plus cross centred on the player's spot, along her facing (the lock marker turned to her yaw)
    for t0, t1, a0 in ((blades, cross1, 0), (relock, cross2, 45)):
        pb.at(t0, lockp(), f'execute as {S.LOCK_M} at @s rotated as {S.BODY} run tp @s ~ ~ ~ ~{a0} 0',
              sset('#t', t1 - t0),
              f'execute store result score #t2 {OBJ} run data get entity {S.LOCK_M} Rotation[0]',
              f'scoreboard players add #t2 {OBJ} 90',
              f'data modify storage {api.STORAGE} core.st set value {{len:280,w:30,yaw:0,t:0}}',
              fn('p/g1/cross'))
        if not api.K._on():
            for t in range(t0, t1, 4):
                pb.at(t, fn('p/g1/strips'))
    for idx, t, t0 in ((0, cross1, blades), (1, cross2, relock)):
        g = pb.group(t - 1)
        h = api.HITS[key][idx]
        half = h[3][0] / 2
        for a in (0, 90):
            # one line(28, 3.0) of the cross: centred on the lock (back 14 + forward 14), along the axis a
            pb.at(t - 1, S.hazard(key, h, grp=True, kb=KB0, pos=f'at {S.LOCK_M} rotated as {S.LOCK_M} rotated ~{a} 0 '
                                                                     f'positioned ~ {CY} ~',
                                  dims=(half, h[3][1]), back=half))
            pb.hits.append(dict(t=t, idx=idx, tell=t0, grp=g, kb=KB0, bol=1, shape='line'))
        # the strike (ref/p1_G_cross.jpg 36.2-36.6; v3 36.40-37.25: each blade sweeps its line, crimson thorns erupting
        # behind it): the four blades leave the arm ends 4 t before the hit and close on the cross centre 3.5 b a tick
        # (teleport_duration 1: the client slides each step over the next tick, so they meet there on the hit tick, burst
        # and are gone). The steps are the stand-offs 10.5 / 7 / 3.5 / 0 b, each taken only where a blade may stand
        # (BLADE_OK: a pulled-in blade stays put until its stand-off comes, the lock itself passed mv/ok). The
        # thorns of a 3.5 b segment are called with the step across it: a kit card rises over 2 t from the tick after its
        # call, so they stand up just behind the blade; one thorn per call, 1.15 b apart, each only on the walk disc.
        pb.at(t - 4, snd('blade_fly', f'at {S.LOCK_M}'))
        for k in range(4):
            d = 14 - 3.5 * (k + 1)
            step = f'positioned ^ ^ ^{num(-d)} ' if d else ''
            pb.at(t - 4 + k, f'execute as @e[type=minecraft:item_display,tag=rlk_kn_blade,tag={S.tag_p(key)}] at {S.LOCK_M} '
                             f'rotated as @s {step}positioned ~ {CY} ~ {BLADE_OK} run tp @s ~ ~ ~')
            for arm in (0, 90, 180, 270):
                for j, z in enumerate((0.6, 1.75, 2.9)):
                    x = THORN_X[j] * (1 if k % 2 == 0 else -1)
                    pos = (f'at {S.LOCK_M} rotated as {S.LOCK_M} rotated ~{arm} 0 positioned ^{num(x)} ^ '
                           f'^{num(14 - 3.5 * k - z)} positioned ~ {CY} ~ if entity {WALK_M}')
                    pb.at(t - 4 + k, S.fx('cross_thorns', [part(S.DUST[2], 0.3, 0.6, 0.3, 0, 3)], pos=pos,
                                          h=THORN_H[(3 * k + j + 5 * arm // 90) % len(THORN_H)]))
        pb.at(t, S.bol_mark(), snd('cross_hit', f'at {S.LOCK_M}'),
              [f'execute as @e[type=minecraft:item_display,tag=rlk_kn_blade,tag={S.tag_p(key)}] at @s run {x}'
               for x in S.fx('blade_burst', [part(S.DUST[2], 0.6, 1.0, 0.6, 0, 20)], pos='positioned ~ ~1 ~')],
              f'kill @e[type=minecraft:item_display,tag=rlk_kn_blade,tag={S.tag_p(key)}]')
    pb.at(rim, fn('p/g1/rim'))
    if not api.K._on():
        for t in range(rim, field, 4):
            r = 24.0 * (t - rim + 4) / (field - rim)
            pb.at(t, f'execute at {S.ARENA_M} positioned ~ {num(CY + 0.1)} ~ run {part(S.DUST[2], r * 0.45, 0.02, r * 0.45, 0, 90)}')
    pb.hit(2, tell_from=rim, kb=KB1, pos=f'at {S.ARENA_M} positioned ~ {CY} ~')
    # combat overhaul (rulings B-01 / B-02): the field covers the whole arena (unparriable by the framework's rule,
    # dodgeable; the two crosses are parryable): the warning glint on her chest when the rim starts closing
    assert field - rim >= api.TELL_BIG
    pb.at(rim, S.np_warn())
    pb.at(field, snd('blast'), S.fx('thorns', [part(S.DUST[2], 9, 1.5, 9, 0, 200)], pos=f'at {S.ARENA_M} positioned ~ {CY} ~', r=240),
          [f'execute as @e[type=minecraft:item_display,tag=rlk_kn_blade,tag={S.tag_p(key)}] at @s run {x}'
           for x in S.fx('blade_burst', [part(S.DUST[2], 0.6, 1.0, 0.6, 0, 12)], pos='positioned ~ ~1 ~')],
          look('glow', 'normal'))
    pb.at(field + 8, f'kill @e[type=minecraft:item_display,tag=rlk_kn_blade,tag={S.tag_p(key)}]')
    pb.end(end)
    if api.K.prop('blade'):
        W.w('p/g1/resume', ['# G1 resume: the blade looks again (pause cleared the kit cards).',
                            f'execute as @e[type=minecraft:item_display,tag={S.tag_p(key)},tag=rlk_kn_blade] run {api.K.prop("blade")}'])
    return finish(pb, key, clear_kit=True)


# ================================================================================================= H 연옥 그림자 분신
def build_h(W):
    key = clip = 'h1'
    pb = PB(key, W)
    leap, perch, clones, strike, drop, wing, sweep, end = (
        E(clip, k) for k in ('leap', 'perch', 'clones', 'strike', 'drop', 'wing', 'sweep', 'end'))
    hy = api.LEAP_H['h1']
    clone = {s: prop_nbt(key, ('rlk_kn_clone', f'rlk_kn_clone_{s}', 'rlk_kn_new'), 'minecraft:netherite_hoe', (2.4, 2.4, 2.4))
             for s in ('l', 'r')}
    W.w('p/h1/web', [
        f'# H1 web (@s = body): the web {hy} b above a point 6 b behind her (else 4 / 2 / 0 b; the floor spot passes mv/ok);',
        '# she runs up the crimson thread to it in 10 t.',
        'kill @e[type=minecraft:marker,tag=rlk_kn_dp]']
        + [f'execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at @s rotated as @s rotated ~180 0 positioned ^ ^ ^{d} '
           f'positioned ~ {CY} ~ if function rlk:mboss/mv/ok run summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(key, "rlk_kn_dp")}}}'
           for d in (6, 4, 2, 0)]
        + [f'execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at @s positioned ~ {CY} ~ run summon minecraft:marker '
           f'~ ~ ~ {{Tags:{S.tags_nbt(key, "rlk_kn_dp")}}}',
           f'execute positioned as @e[type=minecraft:marker,tag=rlk_kn_dp,limit=1] positioned ~ ~{num(hy)} ~ run '
           f'function rlk:mboss/mv/glide {{t:{perch - leap}}}',
           'kill @e[type=minecraft:marker,tag=rlk_kn_dp]'])
    dress = [f'execute as @e[type=minecraft:item_display,tag=rlk_kn_new] run {api.K.prop("clone")}'] if api.K.prop('clone') else []
    W.w('p/h1/clones', [
        '# H1 clones (@s = body on the web): two crimson shadow clones left and right of her, each turned toward the lock (yaw',
        f'# only), diving in arcs onto the locked spot over {strike - clones} t.']
        + [f'execute at @s rotated as @s rotated ~ 0 positioned ^{x} ^ ^ run summon minecraft:item_display ~ ~ ~ {clone[s]}'
           for s, x in (('l', 4), ('r', -4))]
        + dress
        + [f'execute as @e[type=minecraft:item_display,tag=rlk_kn_new] at @s facing entity {S.LOCK_M} feet run tp @s ~ ~ ~ ~ 0',
           f'execute as @e[type=minecraft:item_display,tag=rlk_kn_new] positioned as {S.LOCK_M} positioned ~ ~0.5 ~ run '
           f'function rlk:mboss/mv/leap {{t:{strike - clones},h:20}}',
           'tag @e[type=minecraft:item_display,tag=rlk_kn_new] remove rlk_kn_new']
        + S.placed(S.snd('clone_launch'), 'at @s'))
    W.w('p/h1/drop', [
        '# H1 drop (@s = body): she drops to 3 b in front of the player on the player -> web line (else 4.5 / 2 b; mv/ok),',
        '# facing the player, over 8 t.',
        'kill @e[type=minecraft:marker,tag=rlk_kn_dp]']
        + [f'execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at {S.PLAYER} facing entity @s feet rotated ~ 0 '
           f'positioned ^ ^ ^{d} positioned ~ {CY} ~ if function rlk:mboss/mv/ok run summon minecraft:marker ~ ~ ~ '
           f'{{Tags:{S.tags_nbt(key, "rlk_kn_dp")}}}' for d in (3, 4.5, 2)]
        + [f'execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] at @s positioned ~ {CY} ~ if function rlk:mboss/mv/ok '
           f'run summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(key, "rlk_kn_dp")}}}',
           f'execute unless entity @e[type=minecraft:marker,tag=rlk_kn_dp] positioned as {S.ARENA_M} positioned ~ {CY} ~ run '
           f'summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(key, "rlk_kn_dp")}}}',
           f'execute positioned as @e[type=minecraft:marker,tag=rlk_kn_dp,limit=1] run function rlk:mboss/mv/glide '
           f'{{t:{wing - drop}}}',
           'kill @e[type=minecraft:marker,tag=rlk_kn_dp]', FACE])
    pb.at(leap, FACE, api.play(clip), fn('p/h1/web'), snd('leap'),
          S.fx('threads', [part(S.DUST[2], 0.1, 3.0, 0.1, 0, 30)], pos=f'{S.AT_BODY} positioned ~ ~3 ~', r=10))
    pb.at(perch, snd('perch'), S.fx('web', [part('minecraft:white_ash', 1.5, 0.2, 1.5, 0, 30)], pos=f'{S.AT_BODY} positioned ~ ~0.5 ~'))
    pb.track(1, clones, 20)
    pb.at(clones, lockp(), fn('p/h1/clones'))
    if not api.K.prop('clone'):
        for t in range(clones + 1, strike, 2):
            pb.at(t, f'execute as @e[type=minecraft:item_display,tag=rlk_kn_clone,tag={S.tag_p(key)}] at @s run '
                     f'{part(S.DUST[2], 0.3, 0.6, 0.3, 0, 8)}')
    # strike 34: two crossing slashes along the clones' paths through the lock (separate groups: both may hit)
    # the slashes cross at the lock at +-40 deg of her line of sight (a clear X, ref/p1_H_launch.jpg), centred on it
    pb.at(clones, f'execute as {S.LOCK_M} at @s rotated as {S.BODY} run tp @s ~ ~ ~ ~ 0')
    for a in (40, -40):
        g = pb.group(strike - 1)
        pb.at(strike - 1, S.hazard(key, api.HITS[key][0], grp=True, kb=KB0, dims=(5.0, 2.0), back=5.0,
                                   pos=f'at {S.LOCK_M} rotated as {S.LOCK_M} rotated ~{a} 0 positioned ~ {CY} ~'))
        pb.hits.append(dict(t=strike, idx=0, tell=clones, grp=g, kb=KB0, bol=1, shape='line'))
    pb.at(strike, S.bol_mark(), snd('clone_hit', f'at {S.LOCK_M}'), S.fx_impact(2.0, BOL_C, pos=f'at {S.LOCK_M}'))
    pb.at(strike + 2, f'kill @e[type=minecraft:item_display,tag=rlk_kn_clone,tag={S.tag_p(key)}]')
    # perched (hittable) until the wings burst open (the 14 t crimson tell), the drop, the wing (Bond of Life), the sweep;
    # since I1 the clip has them 12 t apart (>= COMBO_GAP): two hits, each re-faced, the sweep stepped in, only the sweep
    # knocks back (S5: the one-group stand-in of R-S3-1 dropped)
    tell = wing - 14
    pb.track(strike + 1, drop, 10)
    pb.at(tell, look('wings', 'open'), look('glow', 'crimson'), S.fx('wing_burst', [part(S.DUST[2], 1.2, 1.0, 1.2, 0, 30)]),
          snd('wing_burst'))
    pb.at(drop, fn('p/h1/drop'), snd('dive'))
    pb.track(drop + 1, wing - 2, 20)
    pb.hit(1, tell_from=tell, grp=pb.group(wing - 1), kb=KB0)
    pb.at(wing, S.fx_slash(6.0, BOL_C, roll=10, h=1.8), snd('wing_hit'), look('glow', 'normal'))
    track_to(pb, wing, sweep, 14, 3)
    pb.advance(wing + 1, sweep - 2, STEP, STOP)
    pb.hit(2, tell_from=wing, grp=pb.group(sweep - 1), kb=KB1)
    pb.at(sweep, S.fx_slash(5.0, PY_C, roll=180), snd('sweep'))
    pb.end(end)                                   # the wings close with the pattern's end (core/pat_end -> looks_rest)
    if api.K.prop('clone'):
        W.w('p/h1/resume', ['# H1 resume: the clone looks again (pause cleared the kit cards).',
                            f'execute as @e[type=minecraft:item_display,tag={S.tag_p(key)},tag=rlk_kn_clone] run {api.K.prop("clone")}'])
    ground(pb, key)
    return finish(pb, key)


# ================================================================================================= E70 재가 된 만상
def build_e70(W):
    key = clip = 'e70'
    pb = PB(key, W)
    glow, rise, pool, brand, wings, land, end = (E(clip, k) for k in ('glow', 'rise', 'pool', 'brand', 'wings', 'land', 'end'))
    pb.at(glow, FACE, api.play(clip), look('glow', 'crimson'), snd('brand'),
          S.fx('embers_puff', [part(S.DUST[2], 0.5, 1.0, 0.5, 0, 24)]))
    pb.at(rise, 'execute at @s positioned ~ ~1 ~ run function rlk:mboss/mv/glide {t:10}')
    k = api.K.decal('pool', r=120, t=brand - pool)
    pb.at(pool, placed([k], f'at @s positioned ~ {CY} ~') if k else [], snd('flood'))
    if not api.K._on():
        for t in range(pool, brand, 4):
            r = 12.0 * (t - pool + 4) / (brand - pool)
            pb.at(t, f'execute at @s positioned ~ {num(CY + 0.1)} ~ run {part(S.DUST[2], r * 0.45, 0.02, r * 0.45, 0, 40)}')
    pb.at(brand, api.BOND_CALLS['force'], fn('core/e70_brand'))
    pb.at(wings, look('wings', 'open'), S.fx('wing_burst', [part(S.DUST[2], 1.4, 1.0, 1.4, 0, 40)]), snd('wing_burst'))
    pb.at(land - 8, f'execute at @s positioned ~ {CY} ~ run function rlk:mboss/mv/glide {{t:8}}')
    pb.at(land, look('wings', 'off'), look('glow', 'normal'))
    pb.end(end)
    if api.K._on():
        W.w('p/e70/resume', [
            '# E70 resume (@s = body): the pool decal again with the ticks left to the brand.',
            f'execute unless score #pt {OBJ} matches {pool}..{brand - 1} run return 0',
            f'scoreboard players set #t {OBJ} {brand}', f'scoreboard players operation #t {OBJ} -= #pt {OBJ}',
            f'data modify storage {api.STORAGE} core.dec set value {{r:120,t:0}}',
            f'execute store result storage {api.STORAGE} core.dec.t int 1 run scoreboard players get #t {OBJ}',
            f'execute at @s positioned ~ {CY} ~ run {S.kit_with("decal/", "pool", "core.dec")}'])
    ground(pb, key)
    return finish(pb, key, clear_kit=True)


def _mk(key, f):
    def build(W):
        f(W)
    return build


PATTERNS = [
    api.Pattern('a2', S.TID['a2'], ('a2',), _mk('a2', lambda W: build_a('a2', W)), notes='A > 70 %: 2 hits, near'),
    api.Pattern('a4', S.TID['a4'], ('a4',), _mk('a4', lambda W: build_a('a4', W)), notes='A <= 70 %: 4 hits'),
    api.Pattern('a5', S.TID['a5'], ('a5',), _mk('a5', lambda W: build_a('a5', W)), notes='A <= 70 %: 5 hits'),
    api.Pattern('b1', S.TID['b1'], ('b1',), _mk('b1', lambda W: build_b('b1', W)), pause=False, notes='one returning wheel'),
    api.Pattern('b2', S.TID['b2'], ('b2',), _mk('b2', lambda W: build_b('b2', W)), notes='two wheels + the grab (BoL)'),
    api.Pattern('c1', S.TID['c1'], ('c1',), _mk('c1', lambda W: build_c('c1', W)), notes='leap slash'),
    api.Pattern('c2', S.TID['c2'], ('c2',), _mk('c2', lambda W: build_c('c2', W)), notes='+ the wing strike (BoL)'),
    api.Pattern('d1', S.TID['d1'], ('d1',), _mk('d1', lambda W: build_d('d1', W)), notes='dash slash'),
    api.Pattern('d2', S.TID['d2'], ('d2',), _mk('d2', lambda W: build_d('d2', W)), notes='+ the follow-up'),
    api.Pattern('e1', S.TID['e1'], ('e1',), _mk('e1', build_e), notes='aerial zig-zag + dive'),
    api.Pattern('f1', S.TID['f1'], ('f1',), _mk('f1', build_f), notes='forced bond, window 22-159, two field hits (BoL)'),
    api.Pattern('g1', S.TID['g1'], ('g1',), _mk('g1', build_g), notes='plus / X crosses + the field (BoL)'),
    api.Pattern('h1', S.TID['h1'], ('h1',), _mk('h1', build_h), notes='web, clones, drop, wing (BoL) + sweep'),
    api.Pattern('e70', S.TID['e70'], ('e70',), _mk('e70', build_e70), notes='the 70 % event: forced bond, no damage'),
]
assert sorted(p.key for p in PATTERNS) == sorted(api.P1)
