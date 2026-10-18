"""Butterfly-form patterns: B1 우아한 날개, B2 화염 날개의 습격, B3 날개 휩쓸개, B4 달빛 축복, and the finale B5 달빛 해제
(service pattern 15: the core starts it and owns its mechanics: the caption at clock 0, the flat look, the revert to
human form, the heal orbs vanishing, the groggy after it). Owner: the wing-pattern author (with seq_b.py).

Binding: scratchpad mb2/plan.md (Stage-2 decisions) and mb2/spec/B1..B5_*.md; the effect engine is the fx kit
(bf_fx_api.md: g.fx / snd / kcard / tele_* / kprop); vanilla sounds only. Every damaging hit has a ground decal (kit
tele/*) paired with its framework hazard in the same tick (same tell, #hzQuiet 1, sfx 0) at least 10 t ahead, or is a
projectile that carries its own warning (B2 crescents: a decal at the target from the swing; B4 orbs: the wrap/charge
and the slow glowing orb). Locked ground targets clamp to the walk disc r 20.3 (wx/u/lockw, plan Q8); every point her
body moves to clamps to r 16.5 (wx/u/clamp_b, plan Q9), the release point to r 16; the core tick also leashes the body
at r 16.5 in butterfly form (wx/u/btick).

Clock: #bfPT = the clip tick (the core plays the clip at clock 0). Event ticks come from the rig manifest
(tools/mboss_butterfly_rig_manifest.json) by their Stage-2 names, with the Stage-2 ticks as defaults.
"""
import math

from . import api as A
from .api import Pattern, TL, ev_or, clip_len, DMG, KB, CY, EL_PYRO, EL_DENDRO, L

WX = A.WX
NS = A.NS
K_STRIKE, K_BARRAGE, K_SWEEP, K_COCO, K_RELEASE = 'strike', 'barrage', 'sweep', 'coco', 'release'
L_STRIKE, L_BARRAGE, L_SWEEP, L_COCO, L_RELEASE = (clip_len(c) for c in ('wing_strike', 'wing_barrage', 'flap_dive', 'coco', 'release'))

# ---- B1 우아한 날개 (wing_strike): bank 0, dive 8, hit 15
B1_HIT = ev_or('wing_strike', 'hit', 15)
B1_DIVE = ev_or('wing_strike', 'dive', 8)
B1_TELL = 12
B1_LOCK = B1_HIT - B1_TELL                      # 3: lock L / H, the lane + arc decals
B1_GLIDE = B1_HIT - 7                           # 8: the swoop glide S -> H, 7 t
B1_LANE = (10.0, 3.5)                           # lane from her spot along the aim (her swoop path)
B1_ARC = (4.0, 60)                              # sector r 4, +-60 at L (the plan's front arc)

# ---- B2 화염 날개의 습격 (wing_barrage): four swings, 5 fire crescents each
B2_SWINGS = [ev_or('wing_barrage', f'swing{i}', d) for i, d in enumerate((5, 31, 69, 94), 1)]
B2_WIND = 5                                     # the wind-up 5 t before each swing (the rig: inside the clip)
B2_LEAD = max(0, B2_WIND - B2_SWINGS[0])        # 0 with the rig's swing1 5 (the wind-up is inside the clip)
B2_N = 5
B2_SPAWN, B2_FLIGHT, B2_UP = 2, 12, 5           # crescent i appears at s+2+i, lands 12 t later (s+14+i); 5 t fan-out
B2_FAN = (0, 30, -30, 60, -60)                  # fan yaw of crescent i (her left +)
B2_CROSS = [(0.0, 0.0), (1.8, 0.0), (-1.8, 0.0), (3.6, 0.0), (-3.6, 0.0)]   # odd swings: across the aim (x = her left)
B2_LONG = [(0.0, 0.0), (0.0, 1.8), (0.0, -1.8), (0.0, 3.6), (0.0, -3.6)]    # even swings: along the aim
B2_R = 1.2                                      # splash radius (the decal and the projectile's hit sphere)
B2_SPAWN_R, B2_SPAWN_Y = 2.4, 3.6               # wing-root launch points (body frame)
B2_OUT, B2_PITCH = 3.0, 35.0                    # fan-out: 3 b at 0.6 b/t, rising 35 degrees
B2_ARC = 0.8                                    # the dive curves 0.8 b over its straight line (mv/leap)

# ---- B3 날개 휩쓸개 (flap_dive): rise 0, dive 20, slam 26, fan 28, glide 33 (the rig's events)
B3_DIVE = ev_or('flap_dive', 'dive', 20)
B3_SLAM = ev_or('flap_dive', 'slam', 26)
B3_FAN = ev_or('flap_dive', 'fan', B3_SLAM + 2)
B3_GLIDE = ev_or('flap_dive', 'glide', 33)       # the low glide starts on this event (spec B3 §3: glide 33)
B3_TELL, B3_ACT = 12, 5
B3_LOCK = B3_FAN - B3_TELL                      # 16
B3_TRAIL = [B3_GLIDE + 1 + 2 * i for i in range(4)]  # 34 36 38 40: trail segments (strike +10, act 8)
B3_SIDE = 4.5                                   # the low glide to her right

# ---- B4 달빛 축복 (coco): wrap 5, orb1 19, ball 30, ball_open 42, orb2 46 (the rig's prop/pod at the core anchor 30-41)
B4_WRAP = ev_or('coco', 'wrap', 5)
B4_ORBS = (ev_or('coco', 'orb1', 19), ev_or('coco', 'orb2', 46))
B4_BALL = ev_or('coco', 'ball', 30)
B4_OPEN = ev_or('coco', 'ball_open', 42)
B4_STEER, B4_LIFE = 40, 50                      # homing for 40 t (the pj life), the burst at 50
B4_SPD, B4_HR, B4_BURST = 0.25, 0.8, 2.8
B4_END = max(L_COCO, B4_ORBS[-1] + B4_LIFE + 2)  # 98
B4_SPAWN = ((0.0, 3.0, 1.2), (-1.2, 3.0, 0.8))  # orb 1 at her chest ahead, orb 2 from her right side

# ---- B5 달빛 해제 (release)
B5_SWOOP = 5
B5_CUP = ev_or('release', 'cup', 31)
B5_FLASH = ev_or('release', 'flash', 35)
B5_GLINT = ev_or('release', 'glint', 37)
B5_RINGS = ev_or('release', 'rings', 38)
B5_WRAP = ev_or('release', 'wrap', 44)
B5_SNAP = ev_or('release', 'snap', 52)          # the wings snap open: the pod prop (44-51) goes
B5_DET = ev_or('release', 'detonation', 53)
B5_SHRINK = ev_or('release', 'shrink', 87)
B5_SHATTER = ev_or('release', 'shatter', 91)
B5_LAND = ev_or('release', 'land', 96)
B5_R, B5_OUT = 10.0, 4.0                        # the dome radius; the release point 4 b beyond the player (outward)
assert B5_DET - B5_CUP >= 10 and B3_TELL >= 10 and B1_TELL >= 10

PATTERNS = [
    Pattern(11, K_STRIKE, '우아한 날개', 'b', 'wing_strike', bands=('melee', 'mid'), weight={'melee': 2}, el=EL_DENDRO,
            recover=18, max_len=L_STRIKE + 5, length=L_STRIKE),
    Pattern(12, K_BARRAGE, '화염 날개의 습격', 'b', 'wing_barrage', bands=('mid', 'far'), weight={'far': 2}, el=EL_PYRO,
            lead=B2_LEAD, recover=20, max_len=L_BARRAGE + 5, length=L_BARRAGE),
    Pattern(13, K_SWEEP, '날개 휩쓸개', 'b', 'flap_dive', bands=('melee', 'mid'), weight={'mid': 2}, el=EL_PYRO,
            recover=18, max_len=L_SWEEP + 5, length=L_SWEEP),
    Pattern(14, K_COCO, '달빛 축복', 'b', 'coco', bands=('mid', 'far'), el=EL_DENDRO, recover=20,
            max_len=B4_END + 4, length=B4_END),
    Pattern(15, K_RELEASE, '달빛 해제', 'b', 'release', kind='service', el=EL_DENDRO, recover=0,
            max_len=L_RELEASE + 4, length=L_RELEASE),
]

BODY = 'execute rotated as @s rotated ~ 0 '     # as / at the body: her yaw, pitch 0


def M(tag):
    return f'@e[type=minecraft:marker,tag={tag},limit=1]'


def summon_m(pid, tag, pos='~ ~ ~'):
    return f'summon minecraft:marker {pos} {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p{pid}","{tag}"]}}'


def at_b(pos):
    """run at a body-frame point (as / at the body)."""
    return f'{BODY}positioned {pos} run '


def bf(v):
    return ' '.join('^' + L.num(round(float(c), 3), 3) for c in v)


def hz_tele(g, prefix, shape, size, tell, dmg, el=EL_DENDRO, hold=3, **opts):
    """One framework hazard and its kit decal, created in the same context and tick with the same tell (#hzQuiet 1:
    the decal replaces the framework particles; sfx 0: the pattern composes its own sounds)."""
    lines = list(g.hz_opts(sfx=0, quiet=1, el=el, **opts))
    if shape == 'disc':
        lines += [prefix + g.hz_disc(size, tell, dmg), prefix + g.tele_disc(size, tell, el=el, hold=hold)]
    elif shape == 'sector':
        r, a = size
        lines += [prefix + g.hz_sector(r, a, tell, dmg), prefix + g.tele_sector(r, a, tell, el=el, hold=hold)]
    elif shape == 'line':
        ln, wd = size
        lines += [prefix + g.hz_line(ln, wd, tell, dmg), prefix + g.tele_line(ln, wd, tell, el=el, hold=hold, back=opts.get('back') or 0.0)]
    else:
        raise ValueError(shape)
    return lines


def every(t0, t1, step):
    return list(range(t0, t1 + 1, step))


# =============================================================================================
def emit(g):
    b1(g)
    b2(g)
    b3(g)
    b4(g)
    b5(g)


# ---------------------------------------------------------------------------------------------
def b1(g):
    """B1 우아한 날개 / 날개 치기 (Dendro, spec B1_wing_strike.md): bank 0-8 drifting in, lock at 3 (L under the player,
    H = L + 2 b along the aim and 1.2 b to her right), the lane 10 x 3.5 from her spot + the arc r 4 +-60 at L in one
    volley group (tell 12), the swoop glide to H 8-15, the wing-edge hit at 15, the ground slash band, the trailing
    vertical crescent, the climb and the flutter back to the hover."""
    R, k, pid = g.rig, K_STRIKE, 11
    s_, l_, h_ = 'rlk_mb_bf_p11s', 'rlk_mb_bf_p11l', 'rlk_mb_bf_p11h'
    S_, L_, H_ = M(s_), M(l_), M(h_)
    fw = lambda ev: (A.anchor('wing_strike', ev, 'fwtip_l', A.B_FWTIP_L), A.anchor('wing_strike', ev, 'fwtip_r', A.B_FWTIP_R))
    tl = TL(g, k)
    tl.at(0, R('face/player'))
    tl.span(1, B1_LOCK - 1, R('face/track'))
    tl.span(0, B1_GLIDE - 1, A.bstep('toward', 0.15))
    tl.at(1, g.sound('entity.ender_dragon.flap', 0.5, 1.8))
    # t3: the aim lock: L (walk disc), her yaw S -> L, S (lane origin), H (swoop end, body clamp), the volley group
    lane = hz_tele(g, f'execute at {S_} run ', 'line', B1_LANE, B1_TELL, DMG['b1'], kb=KB['default'], grp=True)
    arc = hz_tele(g, f'execute at {L_} run ', 'sector', B1_ARC, B1_TELL, DMG['b1'], kb=KB['default'], grp=True)
    tl.at(B1_LOCK, '# the aim lock: L on the floor under the player (walk disc), her yaw S -> L, the swoop end H',
          f'kill @e[type=minecraft:marker,tag={l_}]', f'kill @e[type=minecraft:marker,tag={s_}]', f'kill @e[type=minecraft:marker,tag={h_}]',
          R('face/player'), A.lockw(), g.keep(l_, 'rlk_mb_bf_lock'),
          f'execute at @s facing entity {L_} feet run tp @s ~ ~ ~ ~ 0',
          f'execute positioned ~ {CY} ~ run ' + summon_m(pid, s_),
          f'execute as {S_} at @s rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run tp @s ~ ~ ~ ~ 0',
          f'execute as {L_} at @s rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run tp @s ~ ~ ~ ~ 0',
          f'execute at {L_} positioned ^-1.2 ^ ^2.0 run ' + summon_m(pid, h_),
          f'execute as {H_} run {A.clamp_body()}',
          g.GRP_NEW, *lane, *arc,
          '# the Dendro tell cue', g.sound('block.amethyst_block.resonate', 0.35, 1.6))
    for t in every(6, 14, 2):
        a = fw('bank' if t < B1_DIVE else 'dive')
        tl.at(t, at_b(a[0]) + g.dust(A.hexrgb('#E7FDAA'), 0.8, '~ ~ ~', (0.2, 0.2, 0.2), 2),
              at_b(a[1]) + g.dust(A.hexrgb('#E7FDAA'), 0.8, '~ ~ ~', (0.2, 0.2, 0.2), 2))
    tl.at(B1_GLIDE, '# the swoop: glide to H (7 t), the dive whoosh', f'execute positioned as {H_} run function rlk:mboss/mv/glide {{t:7}}',
          g.snd('wing_dive'))
    for t in range(B1_HIT - 5, B1_HIT):
        tl.at(t, BODY + 'run ' + g.kcard('streak', '^ ^0.8 ^-1.0', '~90 0', s0=2.5, s1=3.0, life=3, fade=1, col='#E7FDAA'))
    tl.at(B1_HIT - 3, g.sound('entity.phantom.swoop', 0.5, 1.6))
    leaves = [f'execute at {L_} run ' + g.kcard('leaf', '~ ~1 ~', f'~{a} 70', s0=0.3, s1=0.22, move=(0, 1.5, 0), life=12,
                                                 fade=6, col='#ADDE6D') for a in range(0, 360, 60)]
    tl.at(B1_HIT, '# HIT (the lane + arc strike): the flat wing blade sweeping across (dark teal under bright lime), a burst at L,',
          '# leaves flung out; the wing-strike recipe and a leafy crackle.',
          BODY + 'run ' + g.kcard('cres_lime', '^ ^0.8 ^', '~ 0', spin=-120, s0=7.5, s1=8.2, life=4, fade=2, col='#23717A'),
          BODY + 'run ' + g.kcard('cres_lime', '^ ^0.85 ^', '~ 0', spin=-120, s0=7.2, s1=8.0, life=4, fade=2),
          f'execute at {L_} run ' + g.kcard('burst', '~ ~1 ~', bb='center', s0=0.8, s1=2.6, life=4, fade=2),
          *leaves, g.snd('wing_strike'), g.sound('block.cherry_leaves.break', 0.8, 1.0))
    band = lambda d, col, y, s0, s1: (f'execute at {S_} positioned ^ ^{y} ^{d} run '
                                      + g.kcard('streak', '~ ~ ~', '~90 90', s0=s0, s1=s1, life=8, fade=4, col=col))
    tl.at(B1_HIT + 1, '# the ground slash band along her path (the kit wing_band arc at L + floor slashes from her spot)',
          f'execute at {L_} run ' + g.fx('wing_band'),
          band(2, '#38896B', 0.05, 2.8, 3.2), band(2, '#E7FDAA', 0.07, 2.5, 3.0),
          band(4, '#38896B', 0.05, 2.8, 3.2), band(4, '#E7FDAA', 0.07, 2.5, 3.0),
          g.sound('item.trident.riptide_1', 0.5, 1.6))
    tl.at(B1_HIT + 2, band(6, '#38896B', 0.05, 2.8, 3.2), band(6, '#E7FDAA', 0.07, 2.5, 3.0),
          band(8, '#38896B', 0.05, 2.8, 3.2), band(8, '#E7FDAA', 0.07, 2.5, 3.0))
    tl.at(B1_HIT + 3, *[f'execute at {S_} positioned ^ ^0.2 ^{d} run ' + g.dust(A.hexrgb('#ADDE6D'), 1.0, '~ ~ ~', (0.6, 0.1, 0.6), 3)
                        for d in (2, 4, 6, 8)])
    tl.at(B1_HIT + 4, '# the trailing vertical crescent at the end of the swoop (H), a teal underlay; a second swish',
          f'execute at {H_} positioned ~ ~0.8 ~ run ' + g.fx('wing_flare'),
          f'execute at {H_} positioned ^ ^0.8 ^-0.1 run ' + g.kcard('cres_lime', '~ ~0.2 ~', '~ -90', roll=90, spin=-60, s0=3.7,
                                                                  s1=5.7, life=7, fade=3, col='#23717A'),
          g.sound('entity.player.attack.sweep', 0.5, 1.3), g.sound('block.azalea_leaves.break', 0.5, 1.2))
    tl.span(B1_HIT + 1, B1_HIT + 12, A.bstep('fwd', 0.12))
    for t in (B1_HIT + 6, B1_HIT + 10):
        tl.at(t, BODY + 'run ' + g.kcard('leaf', '^1.2 ^3.5 ^-0.5', bb='center', s0=0.3, s1=0.25, move=(0, -2, 0), life=16, fade=6,
                                          col='#D4FA88'),
              BODY + 'run ' + g.kcard('leaf', '^-1.5 ^3.0 ^0.4', bb='center', s0=0.3, s1=0.25, move=(0, -2, 0), life=16, fade=6,
                                       col='#D4FA88'))
    for t in every(B1_HIT + 6, B1_HIT + 13, 2):
        a = fw('hit')
        tl.at(t, at_b(a[0]) + g.dust(A.LIME_PALE, 0.7, '~ ~ ~', (0.3, 0.3, 0.3), 1),
              at_b(a[1]) + g.dust(A.LIME_PALE, 0.7, '~ ~ ~', (0.3, 0.3, 0.3), 1))
    tl.at(B1_HIT + 7, g.sound('entity.ender_dragon.flap', 0.5, 1.6))
    tl.span(B1_HIT + 7, L_STRIKE - 1, R('face/track'))
    tl.span(B1_HIT + 13, L_STRIKE - 7, f'execute if entity @e[tag=rlk_body,distance=..5,limit=1] run {A.bstep("away", 0.06)}')
    for t in (32, 37, 44):
        tl.at(t, g.sound('entity.phantom.flap', 0.4, 1.4))
    tl.at(50, g.snd('flap_small'))
    tl.at(L_STRIKE, g.end())
    tl.write([f'# B1 우아한 날개 (clip wing_strike: dive {B1_DIVE}, hit {B1_HIT}; lock {B1_LOCK}, swoop {B1_GLIDE}-{B1_HIT}).',
              '# One volley group: the lane 10 x 3.5 from her spot along the aim + the arc r 4 +-60 at L (130 % Dendro, KB 3).'],
             ['# B1 tick.'])
    g.pw(k, 'cancel', ['# Remove what B1 owns (its markers; the hazards go with lib_clear).',
                       f'kill @e[type=minecraft:marker,tag={s_}]', f'kill @e[type=minecraft:marker,tag={l_}]',
                       f'kill @e[type=minecraft:marker,tag={h_}]'])


# ---------------------------------------------------------------------------------------------
def b2_points():
    """Body-frame launch point and fan-out end of crescent i (yaw = fan angle, rising B2_PITCH)."""
    out = []
    for th in B2_FAN:
        s, c = math.sin(math.radians(th)), math.cos(math.radians(th))
        h = B2_OUT * math.cos(math.radians(B2_PITCH))
        out.append(((B2_SPAWN_R * s, B2_SPAWN_Y, B2_SPAWN_R * c),
                    ((B2_SPAWN_R + h) * s, B2_SPAWN_Y + B2_OUT * math.sin(math.radians(B2_PITCH)), (B2_SPAWN_R + h) * c)))
    return out


def b2(g):
    """B2 화염 날개의 습격 / 날개탄 (Pyro, spec B2_wing_barrage.md): four swings; at each swing s the player's spot L is locked
    (walk disc) and 5 targets T_i are set in a row (odd swings across the aim, even swings along it, 1.8 b apart) with
    a Pyro ground marker each (decal r 1.2, its fill reaching the rim on the landing tick s+14+i); crescent i is a REAL
    projectile (framework pj, a fire_claw prop): it leaves her wing root at s+2+i, fans out and rises for 5 t at 0.6 b/t,
    then dives on a curved path onto T_i in 7 t (mv/glide + mv/leap carry it on a fixed timetable, so it lands exactly
    when its marker fills); it is harmless in the air and hits on landing (a sphere r 1.2 under the prop = the splash
    on the floor), 50 % Pyro, KB 2; the 5 crescents of a swing share a volley group: one hit per swing at most."""
    R, k, pid = g.rig, K_BARRAGE, 12
    l_ = 'rlk_mb_bf_p12l'
    t_, c_, n_ = 'rlk_mb_bf_p12t', 'rlk_mb_bf_p12c', 'rlk_mb_bf_p12n'
    L_ = M(l_)
    pts = b2_points()
    fw = lambda ev: (A.anchor('wing_barrage', ev, 'fwtip_l', A.B_FWTIP_L), A.anchor('wing_barrage', ev, 'fwtip_r', A.B_FWTIP_R))
    tl = TL(g, k)
    t0 = -B2_LEAD
    for kk, s in enumerate(B2_SWINGS, 1):
        ev = f'swing{kk}'
        a = fw(ev)
        w0 = max(t0, s - B2_WIND)
        tl.at(w0, f'# swing {kk} wind-up: she turns, one wing swept back; embers at the wing tips', R('face/player'),
              at_b(a[0]) + g.particle('flame', '~ ~ ~', (0.3, 0.3, 0.3), 0.02, 3),
              at_b(a[1]) + g.particle('flame', '~ ~ ~', (0.3, 0.3, 0.3), 0.02, 3),
              g.sound('entity.ender_dragon.flap', 0.6, 1.4), g.sound('entity.player.attack.sweep', 0.4, 0.7))
        tl.span(w0 + 1, s - 1, R('face/track'))
        if s - 1 > w0:
            tl.at(s - 1, g.sound('entity.player.attack.sweep', 0.8, 0.7))
        rows = B2_CROSS if kk % 2 else B2_LONG
        lines = [f'# SWING {kk}: lock L (walk disc), her yaw S -> L, the 5 targets ({"across" if kk % 2 else "along"} the aim) with their',
                 '# Pyro ground markers (fill = landing tick), the volley group of the swing, the flame sheet and the launch roar.',
                 R('face/player'), f'kill @e[type=minecraft:marker,tag={l_}]', f'kill @e[type=minecraft:marker,tag={t_}]',
                 A.lockw(), g.keep(l_, 'rlk_mb_bf_lock'), f'execute at @s facing entity {L_} feet run tp @s ~ ~ ~ ~ 0', g.GRP_NEW]
        for i, (x, z) in enumerate(rows):
            land = B2_SPAWN + B2_FLIGHT + i
            lines += [f'execute at {L_} rotated as @s rotated ~ 0 positioned ^{L.num(x)} ^ ^{L.num(z)} run '
                      + summon_m(pid, f'{t_}{i}', f'~ {CY} ~'),
                      f'tag @e[type=minecraft:marker,tag={t_}{i}] add {t_}',
                      f'execute as {M(t_ + str(i))} run {A.clamp_walk()}',
                      f'execute at {M(t_ + str(i))} run ' + g.tele_disc(B2_R, land, el=EL_PYRO, hold=3)]
        sheet = 'fire_swing_d' if kk % 2 else 'fire_swing'
        lines += [BODY + 'positioned ~ ~3.0 ~ run ' + g.fx(sheet),
                  BODY + 'run ' + g.particle('flame', '^ ^3.0 ^1.5', (2.5, 0.6, 1.0), 0.05, 20)]
        if kk % 2 == 0:
            lines += [BODY + 'run ' + g.kcard('streak', p, '~90 0', s0=3.0, s1=4.5, life=3, fade=1, col='#FBF9F9')
                      for p in ('^2.2 ^3.4 ^0.6', '^-2.2 ^2.6 ^0.6', '^0 ^4.4 ^0.2')]
        lines += [g.snd('fire_cres_launch'), g.sound('entity.ghast.shoot', 0.4, 1.2)]
        tl.at(s, *lines)
        tl.span(s + 1, s + B2_SPAWN + B2_N, R('face/track'))
        for i in range(B2_N):
            tl.at(s + B2_SPAWN + i, g.fn(f'p/{k}/spawn{i}'))
        tl.at(s + 3, g.sound('block.fire.ambient', 0.8, 1.5), g.sound('entity.blaze.burn', 0.3, 1.2))
        tl.at(s + 6, g.sound('item.trident.riptide_1', 0.3, 1.6))
        tl.at(s + B2_SPAWN + B2_UP, g.snd('fire_cres_fly'))
        tl.at(s + 12, g.sound('entity.ender_dragon.flap', 0.4, 1.6))
        tl.span(s + 6, s + 20, f'execute if entity @e[tag=rlk_body,distance=..5,limit=1] run {A.bstep("away", 0.2)}')
        tl.span(s + B2_SPAWN + B2_N + 1, (B2_SWINGS[kk] - B2_WIND - 1) if kk < 4 else L_BARRAGE - 1, R('face/track'))
    tl.at(L_BARRAGE, g.end())
    tl.write([f'# B2 화염 날개의 습격 (clip wing_barrage: swings {B2_SWINGS}; lead {B2_LEAD}). Crescent i of a swing s: spawn s+{B2_SPAWN}+i,',
              f'# fan-out {B2_UP} t, curved dive, lands s+{B2_SPAWN + B2_FLIGHT}+i on its marker (50 % Pyro each, one hit per swing).'],
             ['# B2 tick: the crescents fly first (the module tick runs before mv and pj move them next tick).',
              f'execute if entity @e[type=minecraft:item_display,tag={c_},limit=1] run {g.fn(f"p/{k}/fly")}'], t0=t0)
    g.pw(k, 'fly', [f'execute as @e[type=minecraft:item_display,tag={c_}{i},limit=1] at @s run {g.fn(f"p/{k}/fly{i}")}' for i in range(B2_N)])
    for i, (sp, fo) in enumerate(pts):
        T = M(f'{t_}{i}')
        g.pw(k, f'spawn{i}', [
            f'# @s = body: fire crescent {i} at her wing root ({B2_FAN[i]} degrees), a pj prop (harmless until it lands; the',
            '# swing\'s volley group), then the fan-out glide (5 t, rising); the dive starts in fly at age 5.',
            f'kill @e[type=minecraft:item_display,tag={c_}{i}]',
            at_b(bf(sp)) + f'summon minecraft:item_display ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p12","{c_}","{c_}{i}","{n_}"],'
            'teleport_duration:1,brightness:{block:15,sky:15}}',
            f'execute as @e[type=minecraft:item_display,tag={n_}] run {g.kprop("fire")}',
            f'scoreboard players set @e[type=minecraft:item_display,tag={n_}] mbId {pid}',
            f'scoreboard players set @e[type=minecraft:item_display,tag={n_}] mbT 0',
            *g.pj_opts(el=EL_PYRO, kb=KB['light'], wall=0, grp=True),
            f'execute as @e[type=minecraft:item_display,tag={n_},limit=1] at @s rotated ~ -90 run ' + g.pj_launch(0.25, B2_FLIGHT + 1, 0, B2_R),
            f'{BODY}positioned {bf(fo)} as @e[type=minecraft:item_display,tag={n_},limit=1] run function rlk:mboss/mv/glide {{t:{B2_UP}}}',
            f'execute at @e[type=minecraft:item_display,tag={n_},limit=1] run ' + g.fx('fire_spawn'),
            f'tag @e[type=minecraft:item_display,tag={n_}] remove {n_}'])
        g.pw(k, f'fly{i}', [
            f'# @s = crescent {i}, at it (module tick: before mv and pj move it). Age = mbT; the flame puff trail every 2 t.',
            'scoreboard players add @s mbT 1',
            'scoreboard players operation #bfM mb = @s mbT', 'scoreboard players operation #bfM mb %= #bfK2 mb',
            'execute if score #bfM mb matches 0 run ' + g.fx('fire_trail'),
            f'# age {B2_UP}: the dive onto its marker (curved, {B2_FLIGHT - B2_UP} t; the prop lands 0.65 b up, the pj sub-step lifts it',
            '# 0.25 b, so the hit point 0.9 b under it is on the floor at the marker)',
            f'execute if score @s mbT matches {B2_UP} at {T} positioned ~ ~0.65 ~ run function rlk:mboss/mv/leap {{t:{B2_FLIGHT - B2_UP},h:{int(round(B2_ARC * 10))}}}',
            f'execute if score @s mbT matches {B2_FLIGHT} run {g.fn(f"p/{k}/land{i}")}'])
        g.pw(k, f'land{i}', [
            f'# @s = crescent {i} on its landing tick: armed for this tick\'s pj step (the splash r {L.num(B2_R)} on the floor), the fire',
            '# splash and the landing crack at its marker (gone with it).',
            f'scoreboard players set @s mbPjD {DMG["b2"]}',
            f'execute at {T} run ' + g.fx('fire_land'),
            f'execute at {T} run ' + g.dust(A.hexrgb('#585542'), 1.6, '~ ~0.1 ~', (0.5, 0.02, 0.5), 6),
            f'execute at {T} run ' + g.snd('fire_cres_land'),
            f'kill @e[type=minecraft:marker,tag={t_}{i}]'])
    g.pw(k, 'pj_end', ['# A crescent event (@s = prop): a hit ends it at once; its life end (the tick after landing) removes it.',
                       'execute if score #pjEv mb matches 4 run scoreboard players set #pjKeep mb 0'])
    g.pw(k, 'cancel', ['# Remove what B2 owns: the crescents (pj props; lib_clear may have taken them) and the markers.',
                       f'kill @e[type=minecraft:item_display,tag=rlk_mb_bf_p12]', f'kill @e[type=minecraft:marker,tag={t_}]',
                       f'kill @e[type=minecraft:marker,tag={l_}]'])


# ---------------------------------------------------------------------------------------------
def b3(g):
    """B3 날개 휩쓸개 / 날갯짓 (Pyro, spec B3_flap_dive.md): two big flaps and the rise, the lock at fan-12 (the slam point P
    up to 3 b toward the player and 2.5 b short of them, the aim at the player), the 180 degree flame fan r 4.5 (2.5
    tall, active 5 t, 160 %) telegraphed 12 t, the head-first dive glide to P, the slam, the eruption, then the low
    glide 4.5 b to her right leaving 4 flame-trail segments (r 1, tell 10, act 8, 30 %, two volley groups: at most 2
    touches) whose flares are the hz_vis strike events."""
    R, k, pid = g.rig, K_SWEEP, 13
    p_, gl_ = 'rlk_mb_bf_p13p', 'rlk_mb_bf_p13g'
    P_, G_ = M(p_), M(gl_)
    fw = lambda ev: (A.anchor('flap_dive', ev, 'fwtip_l', A.B_FWTIP_L), A.anchor('flap_dive', ev, 'fwtip_r', A.B_FWTIP_R))
    hw = lambda ev: (A.anchor('flap_dive', ev, 'hwtip_l', A.B_HWTIP_L), A.anchor('flap_dive', ev, 'hwtip_r', A.B_HWTIP_R))
    core = A.anchor('flap_dive', 'rise', 'core', A.B_CORE)
    tl = TL(g, k)
    tl.at(0, '# wings V-up: the Pyro rim glow, the first big flap', R('face/player'),
          at_b(core) + g.kcard('glow', bb='center', s0=1.0, s1=1.6, life=20, fade=6, col='#FAD77C'), g.snd('flap_big'))
    tl.span(1, B3_LOCK - 1, R('face/track'))
    for t in every(0, B3_DIVE - 2, 3):
        a = fw('rise')
        tl.at(t, at_b(a[0]) + g.particle('flame', '~ ~ ~', (0.2, 0.2, 0.2), 0.01, 2),
              at_b(a[1]) + g.particle('flame', '~ ~ ~', (0.2, 0.2, 0.2), 0.01, 2))
    tl.at(6, '# downstroke 1', BODY + 'run ' + g.particle('small_flame', '^ ^2.5 ^', (3.0, 0.3, 0.6), 0.01, 6),
          g.sound('entity.ender_dragon.flap', 0.8, 1.2))
    tl.at(13, g.sound('entity.ender_dragon.flap', 0.6, 1.5))
    fan = hz_tele(g, f'execute at {P_} run ', 'sector', (4.5, 90), B3_TELL, DMG['b3'], el=EL_PYRO, hold=B3_ACT,
                  act=B3_ACT, y1=2.5, kb=KB['default'])
    tl.at(B3_LOCK, '# the lock: the slam point P (dest 3 b, 2.5 b short of the player; body clamp), the aim at the player,',
          '# the flame fan (half disc r 4.5 ahead of P, 2.5 tall, active 5 t) with its Pyro decal',
          f'kill @e[type=minecraft:marker,tag={p_}]', R('face/player'), g.dest(3.0, 2.5), g.keep(p_),
          f'execute as {P_} run {A.clamp_body()}',
          f'execute as {P_} at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ {CY} ~ ~ 0',
          *fan, '# the Pyro tell cue', g.sound('item.firecharge.use', 0.35, 1.6))
    for t in range(B3_DIVE - 2, B3_SLAM):
        a = hw('dive')
        tl.at(t, at_b(a[0]) + g.dust(A.hexrgb('#F88F39'), 1.2, '~ ~ ~', (0.1, 0.1, 0.1), 2),
              at_b(a[1]) + g.dust(A.hexrgb('#F88F39'), 1.2, '~ ~ ~', (0.1, 0.1, 0.1), 2))
    tl.at(B3_DIVE - 1, g.snd('wing_dive'))
    tl.at(B3_DIVE, '# the head-first dive: glide to P', f'execute positioned as {P_} run function rlk:mboss/mv/glide {{t:{B3_SLAM - B3_DIVE}}}',
          g.sound('entity.phantom.swoop', 0.7, 1.2))
    tl.at(B3_SLAM, '# the wing slam: two vertical flame crescents at the wing tips',
          f'execute at {P_} positioned ~ ~2.8 ~ run ' + g.fx('flame_slam'), g.snd('flame_slam'))
    tl.at(B3_SLAM + 1, '# the flame sweeps along the floor toward the player',
          *[f'execute at {P_} positioned ^ ^0.06 ^{d} run ' + g.kcard('streak', '~ ~ ~', '~90 90', s0=2.5, s1=4.0, life=4, fade=2,
                                                                     col='#F7CC9C') for d in (1.5, 3.0)])
    tl.at(B3_FAN, '# the eruption: the 180 degree flame fan (kit flame_fan) with its roar',
          f'execute at {P_} run ' + g.fx('flame_fan'), g.snd('flame_fan'), g.sound('entity.ghast.shoot', 0.5, 1.2))
    tl.at(B3_FAN + 2, g.sound('block.fire.ambient', 0.7, 1.3), g.sound('entity.generic.explode', 0.3, 0.7))
    for t in every(B3_FAN + 4, B3_FAN + 8, 2):
        tl.at(t, f'execute at {P_} positioned ^ ^0.4 ^2.2 run ' + g.dust(A.hexrgb('#EDC30B'), 0.8, '~ ~ ~', (2.2, 0.4, 1.2), 10))
    tl.at(B3_FAN + 4, f'execute at {P_} positioned ^ ^0.1 ^2.2 run ' + g.dust(A.hexrgb('#585542'), 1.8, '~ ~ ~', (2.0, 0.02, 1.2), 16))
    tl.at(B3_FAN + 5, f'execute at {P_} positioned ^ ^0.5 ^2.0 run ' + g.particle('campfire_cosy_smoke', '~ ~ ~', (1.5, 0.2, 1.0), 0.01, 3),
          g.sound('entity.blaze.burn', 0.4, 0.9))
    g0 = B3_GLIDE
    tl.at(g0, '# the low glide to her right (G = P + 4.5 b sideways, body clamp), 10 t from the rig\'s glide event',
          f'kill @e[type=minecraft:marker,tag={gl_}]', f'execute at {P_} positioned ^-{L.num(B3_SIDE)} ^ ^ run ' + summon_m(pid, gl_),
          f'execute as {G_} run {A.clamp_body()}', f'execute positioned as {G_} run function rlk:mboss/mv/glide {{t:10}}',
          g.sound('block.fire.ambient', 0.5, 0.8))
    for i, t in enumerate(B3_TRAIL):
        seg = ([g.GRP_NEW] if i in (0, 2) else [])
        seg += hz_tele(g, f'execute positioned ~ {CY} ~ rotated as @s rotated ~ 0 run ', 'disc', 1.0, 10, DMG['b3t'], el=EL_PYRO,
                       hold=8, act=8, kb=KB['none'], vis=pid * 10 + 1, grp=True)
        tl.at(t, f'# flame-trail segment {i + 1} under her (group {1 if i < 2 else 2}): a dark ember line, the flare 10 t later',
              *seg, BODY + 'positioned ~ ~0.05 ~ run ' + g.kcard('streak', '~ ~ ~', '~ 90', s0=1.6, s1=2.0, life=18, fade=6, col='#E04040'),
              g.dust(A.hexrgb('#8C5436'), 1.2, f'~ ~0.1 ~', (0.4, 0.02, 0.4), 4))
    tl.at(B3_TRAIL[1], g.sound('block.fire.ambient', 0.4, 1.1))
    g.pw(k, 'vis', ['# hz_vis of the flame-trail segments (@s = the hazard marker, at it): the flare on the strike (#hzEv 1).',
                    f'execute if score #hzEv mb matches 1 run {g.fn(f"p/{k}/flare")}'])
    g.pw(k, 'flare', ['# A trail segment flares: flame tongues, a flame line puff, embers; crackle.', g.fx('flame_trail'),
                      g.kcard('flame_tongue', '~0.4 ~ ~', bb='vertical', s0=0.4, s1=1.0, life=8, fade=3, col='#F06A30'),
                      g.kcard('flame_tongue', '~-0.4 ~ ~0.2', bb='vertical', s0=0.4, s1=1.0, life=8, fade=3, col='#F06A30'),
                      g.particle('flame', '~ ~0.3 ~', (0.5, 0.3, 0.5), 0.02, 8),
                      g.sound('block.fire.ambient', 0.5, 1.6), g.sound('entity.generic.burn', 0.3, 1.4)])
    ret = g0 + 10
    tl.span(ret, L_SWEEP - 1, R('face/track'))
    tl.span(ret, L_SWEEP - 1, f'execute if entity @e[tag=rlk_body,distance=..6,limit=1] run {A.bstep("away", 0.25)}')
    tl.at(ret + 2, g.sound('entity.ender_dragon.flap', 0.4, 1.6))
    for t in (50, 54):
        tl.at(t, g.sound('entity.phantom.flap', 0.4, 1.5))
    tl.at(L_SWEEP, g.end())
    tl.write([f'# B3 날개 휩쓸개 (clip flap_dive: dive {B3_DIVE}, slam {B3_SLAM}, fan {B3_FAN}-{B3_FAN + B3_ACT - 1}, glide {B3_GLIDE}; lock {B3_LOCK};',
              f'# trail {B3_TRAIL} strike +10 act 8, two groups).'], ['# B3 tick.'])
    g.pw(k, 'cancel', ['# Remove what B3 owns (its markers; the hazards go with lib_clear).',
                       f'kill @e[type=minecraft:marker,tag={p_}]', f'kill @e[type=minecraft:marker,tag={gl_}]'])


# ---------------------------------------------------------------------------------------------
def b4(g):
    """B4 달빛 축복 / 2단 코코볼 (Dendro, spec B4_coco.md): the wing-wrap charge, orb 1 at orb1 (her chest, ahead) and orb 2
    at orb2 (her right side), the cocoon ball between. Each orb is a framework pj (a kit sphere prop with two spinning
    gyroscope rings, or the rig's orb prop once it exists) flying 0.25 b/t and steering 9 degrees/t toward the player
    for its 40 t life (contact: 150 % Dendro, KB 2, it pops); then it stops, a burst decal r 2.8 fills under it and
    10 t later the radial ground blades burst (150 %, KB 3) in the orb's own volley group: one hit per orb."""
    R, k, pid = g.rig, K_COCO, 14
    o_, r_, n_, v_ = 'rlk_mb_bf_p14o', 'rlk_mb_bf_p14r', 'rlk_mb_bf_p14n', 'rlk_mb_bf_p14v'
    rig_orb, rig_pod = g.prop('orb'), g.prop('pod')
    core = lambda ev: A.anchor('coco', ev, 'core', A.B_CORE)
    tl = TL(g, k)
    tl.at(0, R('face/player'))
    tl.span(1, B4_END - 1, R('face/track'))
    tl.span(0, 4, f'execute unless entity @e[tag=rlk_body,distance=..6.5,limit=1] run {A.bstep("toward", 0.3)}')
    for t0, t1 in ((B4_ORBS[0] - 5, B4_ORBS[0] - 1), (B4_ORBS[1] - 5, B4_ORBS[1] - 1)):
        tl.span(t0, t1, f'execute if entity @e[tag=rlk_body,distance=..5,limit=1] run {A.bstep("away", 0.2)}')
    tl.at(B4_WRAP, '# the wing wrap: the lime core grows at her chest with converging streaks (14 t)',
          at_b(core('wrap')) + g.fx('orb_charge'), g.snd('orb_charge'))
    tl.at(B4_WRAP + 9, g.sound('block.amethyst_block.resonate', 0.5, 1.4))
    tl.at(B4_ORBS[0] - 3, g.sound('entity.ender_dragon.flap', 0.5, 1.6))
    for n, t in enumerate(B4_ORBS):
        tl.at(t, f'# orb {n + 1}', R('face/player'), g.fn(f'p/{k}/orb_new{n}'))
    ball = core('ball')
    tl.at(B4_BALL, '# the cocoon ball (wings wrapped, drifting toward the player): the rig\'s closed pod at the core anchor (rig API',
          '# section 6.1: summoned at ball, cleared at ball_open), lime glow inside, swirling rustle',
          *([f'kill @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod]', at_b(ball) + rig_pod] if rig_pod else []),
          at_b(ball) + g.fx('cocoon_ball'), g.snd('cocoon_ball'), g.sound('entity.breeze.whirl', 0.6, 1.2))
    tl.span(B4_BALL, B4_OPEN - 1, f'execute unless entity @e[tag=rlk_body,distance=..5,limit=1] run {A.bstep("toward", 0.12)}')
    if rig_pod:
        tl.span(B4_BALL + 1, B4_OPEN - 1, f'{BODY}positioned {ball} as @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod] run tp @s ~ ~ ~ ~ ~')
    tl.at(B4_BALL + 2, at_b(core('ball')) + g.fx('orb_charge'), g.snd('orb_charge'))
    tl.at(B4_BALL + 6, g.sound('entity.breeze.whirl', 0.4, 1.0))
    tl.at(B4_OPEN, '# the ball opens (the pod prop goes): a pale lime ring flash',
          *(['kill @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod]'] if rig_pod else []),
          at_b(ball) + g.kcard('ripple', bb='center', s0=2.0, s1=4.0, life=4, fade=2, col='#CCF39C'),
          g.sound('entity.ender_dragon.flap', 0.5, 1.5))
    tl.at(B4_END, g.end())
    tl.write([f'# B4 달빛 축복 (clip coco: wrap {B4_WRAP}, orbs {B4_ORBS}, ball {B4_BALL}-{B4_OPEN}; orb pj {B4_SPD} b/t, steer 9/t for',
              f'# {B4_STEER} t, burst decal r {B4_BURST} at +{B4_STEER}, burst +{B4_LIFE}; end {B4_END} or earlier once both orbs are gone).'],
             ['# B4 tick: the orbs steer (pj props; the module tick runs before pj/all moves them).',
              f'execute if entity @e[type=minecraft:item_display,tag={o_},limit=1] as @e[type=minecraft:item_display,tag={o_}] at @s run {g.fn(f"p/{k}/orb")}',
              f'execute if score #bfPT mb matches {L_COCO + 1}.. unless entity @e[type=minecraft:item_display,tag={o_},limit=1] run return run {g.end()}'])
    for n, sp in enumerate(B4_SPAWN):
        new = [f'# @s = body: orb {n + 1} ({"her chest, ahead" if n == 0 else "her right side"}), a pj prop in its own volley group, aimed at',
               '# the player; its two gyroscope rings follow it (p/coco/orb).',
               f'kill @e[tag={o_}{n}]', f'kill @e[tag={r_}{n}]', f'kill @e[tag={v_}{n}]']
        tags = f'"rlk_room","rlk_mb_aux","rlk_mb_bf_p14","{o_}","{o_}{n}","{n_}"'
        if rig_orb:
            new += [at_b(bf(sp)) + f'summon minecraft:item_display ~ ~ ~ {{Tags:[{tags}],teleport_duration:1}}',
                    at_b(bf(sp)) + rig_orb,
                    f'tag @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_new] add {v_}{n}',
                    f'tag @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_new] add rlk_mb_bf_p14',
                    'tag @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_new] remove rlk_mb_bf_prop_new']
        else:
            new += [at_b(bf(sp)) + f'summon minecraft:item_display ~ ~ ~ {{Tags:[{tags}],teleport_duration:1,brightness:{{block:15,sky:15}}}}',
                    f'execute as @e[type=minecraft:item_display,tag={n_}] run {g.kprop("orb")}']
            for j, pitch in enumerate((0, 55)):
                new += [at_b(bf(sp)) + f'summon minecraft:item_display ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p14","{r_}",'
                        f'"{r_}{n}","{r_}{n}{"ab"[j]}","rlk_mb_bf_p14m"],teleport_duration:1,Rotation:[{30 * j}f,{pitch}f]}}',
                        f'execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_p14m] run {g.kprop("orb_ring")}',
                        'tag @e[type=minecraft:item_display,tag=rlk_mb_bf_p14m] remove rlk_mb_bf_p14m']
        new += [f'scoreboard players set @e[type=minecraft:item_display,tag={n_}] mbId {pid}',
                f'scoreboard players set @e[type=minecraft:item_display,tag={n_}] mbT 0',
                g.GRP_NEW, *g.pj_opts(el=EL_DENDRO, kb=KB['light'], grp=True),
                f'execute as @e[type=minecraft:item_display,tag={n_},limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run '
                + g.pj_launch(B4_SPD, B4_STEER, DMG['b4'], B4_HR),
                f'execute at @e[type=minecraft:item_display,tag={n_},limit=1] run ' + g.fx('orb_launch'),
                f'tag @e[type=minecraft:item_display,tag={n_}] remove {n_}',
                g.snd('orb_launch'), g.sound('entity.allay.item_thrown', 0.5, 0.8)]
        g.pw(k, f'orb_new{n}', new)
        g.pw(k, f'follow{n}', [f'# @s = orb {n + 1}, at it: its ring displays (or the rig orb prop) ride along; the kit rings spin.',
                               '# (to where the pj step puts the orb this tick: 0.25 b along its flight, so they never lag it)',
                               f'execute if score @s mbT matches ..{B4_STEER - 1} positioned ^ ^ ^{L.num(B4_SPD)} as @e[type=minecraft:item_display,tag={r_}{n}a,limit=1] rotated as @s run tp @s ~ ~ ~ ~15 ~',
                               f'execute if score @s mbT matches ..{B4_STEER - 1} positioned ^ ^ ^{L.num(B4_SPD)} as @e[type=minecraft:item_display,tag={r_}{n}b,limit=1] rotated as @s run tp @s ~ ~ ~ ~-12 ~',
                               f'execute if score @s mbT matches ..{B4_STEER - 1} positioned ^ ^ ^{L.num(B4_SPD)} as @e[type=minecraft:item_display,tag={v_}{n}] run tp @s ~ ~ ~',
                               f'execute if score @s mbT matches {B4_STEER}.. as @e[type=minecraft:item_display,tag={r_}{n}a,limit=1] rotated as @s run tp @s ~ ~ ~ ~6 ~',
                               f'execute if score @s mbT matches {B4_STEER}.. as @e[type=minecraft:item_display,tag={r_}{n}b,limit=1] rotated as @s run tp @s ~ ~ ~ ~-5 ~'])
    burst = hz_tele(g, f'execute positioned ~ {CY} ~ run ', 'disc', B4_BURST, B4_LIFE - B4_STEER, DMG['b4'], kb=KB['default'])
    g.pw(k, 'orb', [
        f'# @s = an orb, at it (module tick). Age mbT: homing 1..{B4_STEER - 1} (9 degrees/t), its pj life ends at {B4_STEER}',
        f'# (pj_end keeps it as a still prop), the burst decal + hazard at {B4_STEER} in its group, pulses, the burst at {B4_LIFE}.',
        'scoreboard players add @s mbT 1',
        f'execute if score @s mbT matches 1..{B4_STEER - 1} run ' + g.pj_steer(9),
        *[f'execute if entity @s[tag={o_}{n}] run {g.fn(f"p/{k}/follow{n}")}' for n in range(len(B4_ORBS))],
        'scoreboard players operation #bfM mb = @s mbT', 'scoreboard players operation #bfM mb %= #bfK2 mb',
        f'execute if score @s mbT matches ..{B4_STEER} if score #bfM mb matches 0 run ' + g.dust(A.LIME_PALE, 1.0, '~ ~ ~', (0.4, 0.4, 0.4), 3),
        f'execute if score @s mbT matches ..{B4_STEER} if score #bfM mb matches 0 run ' + g.particle('end_rod', '~ ~ ~', (0.3, 0.3, 0.3), 0.01, 1),
        'scoreboard players operation #bfM mb = @s mbT', 'scoreboard players operation #bfM mb %= #bfK10 mb',
        f'execute if score @s mbT matches ..{B4_STEER - 1} if score #bfM mb matches 0 run {g.fn(f"p/{k}/shadow")}',
        f'execute if score @s mbT matches {B4_STEER} rotated ~ 0 run {g.fn(f"p/{k}/burst_tell")}',
        *[f'execute if score @s mbT matches {t} run data merge entity @s {{start_interpolation:0,interpolation_duration:3,'
          f'transformation:{{scale:[{s}f,{s}f,{s}f]}}}}' for t, s in ((B4_STEER + 1, 1.95), (B4_STEER + 4, 1.7), (B4_STEER + 7, 1.95))],
        f'execute if score @s mbT matches {B4_LIFE} run {g.fn(f"p/{k}/burst")}'])
    g.pw(k, 'shadow', ['# Every 10 t of flight: a lime shadow ring on the floor under the orb (it reads the depth), its hum.',
                       f'execute positioned ~ {CY} ~ run ' + g.dust(A.LIME, 0.8, '~ ~0.1 ~', (0.45, 0.0, 0.45), 10),
                       g.snd('orb_fly')])
    g.pw(k, 'burst_tell', ['# @s = orb at the end of its homing (its pj ends in pj/all this tick: released, harmless): the burst',
                           f'# hazard r {L.num(B4_BURST)} on the floor under it in its own volley group (one hit per orb), the decal.',
                           *g.hz_opts(), 'scoreboard players operation #hzGrp mb = @s mbPjG', *burst,
                           g.sound('block.beacon.power_select', 0.4, 1.9)])
    g.pw(k, 'burst', ['# @s = orb, its burst tick (the hazard strikes now): the radial ground blades, the airy boom; gone.',
                      g.fn(f'p/{k}/pop')])
    g.pw(k, 'pop', ['# @s = orb: burst fx on the floor under it, its rings / rig prop and itself removed.',
                    f'execute positioned ~ {CY} ~ rotated ~ 0 run ' + g.fx('orb_burst'), g.snd('orb_burst'),
                    g.particle('flash{color:[0.92,0.99,0.85,0.9]}', '~ ~0.5 ~', (0, 0, 0), 0, 1),
                    *[f'execute if entity @s[tag={o_}{n}] run kill @e[tag={r_}{n}]' for n in range(len(B4_ORBS))],
                    *[f'execute if entity @s[tag={o_}{n}] run kill @e[tag={v_}{n}]' for n in range(len(B4_ORBS))],
                    'kill @s'])
    g.pw(k, 'pj_end', ['# An orb event (@s = orb, at it): a hit pops it at once (one hit per orb, no burst left behind), a wall pops',
                       f'# it, its life end ({B4_STEER} t) keeps it as a still prop for the burst (p/coco/orb).',
                       f'execute if score #pjEv mb matches 2 run return run scoreboard players set #pjKeep mb 1',
                       'scoreboard players set #pjKeep mb 0',
                       f'execute if score #pjEv mb matches 1 run return run {g.fn(f"p/{k}/pop")}',
                       f'execute if score #pjEv mb matches 4 run return run {g.fn(f"p/{k}/pop")}'])
    g.pw(k, 'cancel', ['# Remove what B4 owns: the orbs (pj or still), their rings / rig props, the pod prop.',
                       'kill @e[type=minecraft:item_display,tag=rlk_mb_bf_p14]',
                       *(['kill @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod]'] if rig_pod else [])])


# ---------------------------------------------------------------------------------------------
def b5(g):
    """B5 달빛 해제 / 강화 해제 (Dendro, service 15; spec B5_release.md): at 0 the release point R = the player's spot + 4 b
    outward from the arena centre (toward her side when the player stands on the centre), clamped to r 16; the swoop
    glide to R (5-14), the whirl with the lime star flare and slash streaks, the cup (the dome decal r 10 and its hazard,
    tell 22: dodge by > 10.3 b from R or a dash at E), the ground flash, the cyan X glint, the gyroscope ring cage, the
    pod, the detonation E (260 % Dendro, KB 4 radial), the tendrils, the embers, the wing shards and shatter, the landing.
    The core: the caption at 0, the flat look, the revert to human form and the groggy."""
    R, k, pid = g.rig, K_RELEASE, 15
    l_, r_ = 'rlk_mb_bf_p15l', 'rlk_mb_bf_p15r'
    L_, R_ = M(l_), M(r_)
    rig_pod = g.prop('pod')
    core = lambda ev, d=A.B_CORE: A.anchor('release', ev, 'core', d)
    fw = lambda ev: (A.anchor('release', ev, 'fwtip_l', A.B_FWTIP_L), A.anchor('release', ev, 'fwtip_r', A.B_FWTIP_R))
    hw = lambda ev: (A.anchor('release', ev, 'hwtip_l', A.B_HWTIP_L), A.anchor('release', ev, 'hwtip_r', A.B_HWTIP_R))
    arena = '@e[tag=rlk_mb_arena,limit=1]'
    body_sel = '@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]'
    tl = TL(g, k)
    tl.at(0, '# the release point R: L0 (the player\'s spot) + 4 b outward from the centre (from her when L0 is on the centre),',
          '# pulled inside r 16; the fold fx (lime butterfly glyphs, a rim glow) and the swoop recipe',
          f'kill @e[type=minecraft:marker,tag={l_}]', f'kill @e[type=minecraft:marker,tag={r_}]', R('face/player'),
          A.lockw(), g.keep(l_, 'rlk_mb_bf_lock'), f'execute at {L_} run ' + summon_m(pid, r_),
          'scoreboard players set #bp15C mb 0',
          f'execute at {arena} positioned ~ {CY} ~ if entity @e[type=minecraft:marker,tag={l_},distance=..1] run scoreboard players set #bp15C mb 1',
          f'execute if score #bp15C mb matches 0 as {R_} at @s facing entity {arena} feet rotated ~180 0 run tp @s ^ ^ ^{L.num(B5_OUT)}',
          f'execute if score #bp15C mb matches 1 as {R_} at @s facing entity {body_sel} feet rotated ~180 0 run tp @s ^ ^ ^{L.num(B5_OUT)}',
          f'execute as {R_} at @s run tp @s ~ {CY} ~', f'execute as {R_} run {A.clamp_release()}',
          at_b(core('swoop')) + g.fx('rel_fold'),
          at_b(core('swoop')) + g.kcard('glow', bb='center', s0=1.0, s1=1.6, life=10, fade=4, col=A.LIME_HEX),
          g.snd('release_swoop'))
    tl.span(1, B5_CUP - 1, R('face/track'))
    tl.at(B5_SWOOP, '# the swoop past the player to R (9 t), the dive whoosh',
          f'execute positioned as {R_} run function rlk:mboss/mv/glide {{t:9}}', g.snd('wing_dive'))
    for t in every(B5_SWOOP, B5_SWOOP + 6, 2):
        tl.at(t, BODY + 'positioned ~ ~0.06 ~ run ' + g.kcard('streak', '~ ~ ~', '~90 90', s0=2.0, s1=3.0, life=4, fade=2, col=A.LIME_HEX),
              g.particle('cherry_leaves', '~ ~0.6 ~', (0.6, 0.2, 0.6), 0, 2))
    tl.at(B5_SWOOP + 4, g.sound('entity.phantom.swoop', 0.5, 1.3),
          *[at_b(a) + g.dust(A.LIME_PALE, 0.8, '~ ~ ~', (0.3, 0.3, 0.3), 3) for a in fw('swoop')])
    tl.at(14, '# settled over R: the core glows', at_b(core('swoop')) + g.kcard('glow', bb='center', s0=0.4, s1=0.9, life=14, fade=4,
                                                                                  col='#D8F2BC'))
    whirl = every(B5_CUP - 13, B5_CUP - 1, 4)   # 18 22 26 30
    for i, t in enumerate(whirl):
        c = core('whirl')
        tl.at(t, f'# whirl: slash streaks round her, the pulsing lime 4-point star flare at her right side',
              at_b(c) + g.fx('rel_slashes'),
              BODY + f'positioned {c} positioned ^-1.2 ^ ^ run ' + g.fx('rel_flare'))
    tl.at(whirl[0], g.sound('entity.breeze.whirl', 0.6, 1.3))
    tl.at(whirl[0] + 2, g.snd('release_charge'))
    tl.at(whirl[0] + 4, g.sound('entity.player.attack.sweep', 0.4, 1.6))
    tl.at(whirl[0] + 6, g.sound('entity.breeze.whirl', 0.5, 1.4))
    tl.at(whirl[0] + 10, g.sound('entity.breeze.whirl', 0.5, 1.5))
    tl.at(whirl[-1], g.sound('entity.player.attack.sweep', 0.4, 1.6))
    dome = hz_tele(g, f'execute at {R_} run ', 'disc', B5_R, B5_DET - B5_CUP, DMG['b5'], kb=KB['heavy'], hold=4)
    tl.at(B5_CUP, f'# the cup: the dome r {L.num(B5_R)} at R, telegraphed {B5_DET - B5_CUP} t (the decal and the hazard), the charge',
          *dome, at_b(core('cup')) + g.kcard('glow', bb='center', s0=1.0, s1=1.8, life=8, fade=3, col='#D8F2BC'),
          g.sound('block.respawn_anchor.charge', 0.7, 1.2), g.sound('block.beacon.activate', 0.6, 1.6))
    tl.at(B5_FLASH, '# the ground flash: a lime mist cone from the floor at R',
          f'execute at {R_} run ' + g.fx('rel_ground_flash'),
          f'execute at {R_} run ' + g.dust(A.hexrgb('#D3F0B8'), 1.4, '~ ~1.5 ~', (0.6, 1.5, 0.6), 20),
          f'execute at {R_} run ' + g.particle('flash{color:[0.93,0.98,0.86,0.8]}', '~ ~0.5 ~', (0, 0, 0), 0, 1),
          g.sound('block.amethyst_block.resonate', 0.7, 1.0))
    tl.at(B5_GLINT, '# the cyan X glint through her chest',
          at_b(core('glint')) + g.fx('rel_xglint'), at_b(core('glint')) + g.particle('end_rod', '~ ~ ~', (0.6, 0.6, 0.6), 0.05, 6),
          g.snd('release_charge'), g.sound('block.amethyst_cluster.hit', 0.8, 1.9))
    tl.at(B5_RINGS, '# the gyroscope ring cage r 4 (refreshed 3 t later)', at_b(core('rings')) + g.fx('rel_cage'),
          g.sound('block.conduit.activate', 0.5, 1.4))
    tl.at(B5_RINGS + 3, at_b(core('rings')) + g.fx('rel_cage'), g.sound('block.respawn_anchor.charge', 0.6, 1.5))
    safe = [f'execute at {R_} run ' + g.particle('end_rod', f'~{L.num(10.5 * math.sin(math.radians(a)), 2)} ~0.3 ~{L.num(10.5 * math.cos(math.radians(a)), 2)}',
                                                  (0, 0, 0), 0, 1) for a in range(0, 360, 15)]
    for t in (B5_RINGS + 3, B5_WRAP + 3):
        tl.at(t, '# the safe line just outside the dome (r 10.5)', *safe)
    tl.at(B5_WRAP, '# the wings wrap into the pod (the rig\'s pod prop at the core anchor until the snap, rig API section 6.1):',
          '# the core glow grows inside it, inward streaks; pressure builds',
          *([f'kill @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod]', at_b(core('wrap')) + rig_pod] if rig_pod else []),
          at_b(core('wrap')) + g.fx('rel_pod'), g.snd('release_wrap'), g.sound('entity.breeze.whirl', 0.5, 0.9))
    if rig_pod:
        tl.span(B5_WRAP + 1, B5_SNAP - 1, f'{BODY}positioned {core("wrap")} as @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod] run tp @s ~ ~ ~ ~ ~')
        tl.at(B5_SNAP, '# the snap: the wings fling open, the pod goes', 'kill @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod]')
    for t in (B5_WRAP + 4, B5_DET - 2):
        tl.at(t, at_b(core('wrap')) + g.kcard('burst', bb='center', s0=1.5, s1=2.5, life=4, fade=2, col='#DFF99C'))
    tl.at(B5_DET - 4, g.sound('entity.warden.sonic_charge', 0.5, 1.8))
    tl.span(B5_DET + 1, B5_LAND - 1, R('face/track'))
    tl.at(B5_DET, '# E: the detonation: white flash, the lime dome r 10 (kit rel_dome) at R, the big boom, a white screen flash',
          f'execute at {R_} run ' + g.fx('rel_dome', r=B5_R), g.snd('release_boom'), g.khud('flash_white'),
          f'execute at {R_} run ' + g.particle('explosion_emitter', '~ ~2 ~', (0, 0, 0), 0, 1))
    tl.at(B5_DET + 2, g.khud('flash_lime'), g.sound('block.azalea_leaves.break', 0.8, 0.9), g.sound('entity.breeze.wind_burst', 0.5, 0.8))
    tl.at(B5_DET + 4, g.sound('block.azalea_leaves.break', 0.6, 1.1))
    tl.at(B5_DET + 5, g.sound('entity.breeze.idle_air', 0.4, 0.6))
    tl.at(B5_DET + 7, '# she re-emerges: lime tendrils stream out', at_b(core('detonation')) + g.fx('rel_tendrils'),
          at_b(core('detonation')) + g.dust(A.hexrgb('#99E358'), 1.2, '~ ~ ~', (1.5, 1.0, 1.5), 20))
    for t in (B5_DET + 10, B5_DET + 22):
        tl.at(t, '# amber ember petals and lime motes drift down', at_b(core('detonation')) + g.fx('embers'))
    tl.at(B5_DET + 10, g.sound('entity.ender_dragon.flap', 0.4, 1.7))
    tl.at(B5_DET + 23, g.sound('entity.ender_dragon.flap', 0.4, 1.7))
    for t in every(B5_DET + 10, B5_SHRINK - 1, 4):
        tl.at(t, at_b(core('detonation')) + g.dust(A.hexrgb('#C4F87E'), 0.8, '~ ~ ~', (1.5, 1.0, 1.5), 2))
    for t in every(B5_SHRINK, B5_SHATTER - 1, 2):
        tl.at(t, *[at_b(a) + g.dust(A.hexrgb('#E7FD7A'), 1.0, '~ ~ ~', (0.2, 0.2, 0.2), 6) for a in fw('flat') + hw('flat')])
    tl.at(B5_SHRINK, g.sound('block.beacon.deactivate', 0.6, 1.8))
    tl.at(B5_SHATTER, '# the shrunken flat lime wings shatter', BODY + 'positioned ^ ^2.8 ^-0.4 run ' + g.fx('wing_shatter'),
          g.snd('wing_shatter'), BODY + 'run ' + g.particle('block{block_state:"minecraft:lime_stained_glass"}', '^ ^3 ^-0.4', (2.0, 1.0, 1.0), 0, 20))
    tl.at(B5_LAND, '# the landing in human form (the core: groggy next)', g.fx('land'), g.snd('land'),
          g.sound('block.moss.fall', 0.8, 1.0), g.particle('poof', '~ ~0.15 ~', (0.6, 0.05, 0.6), 0.03, 8),
          g.particle('block{block_state:"minecraft:moss_block"}', '~ ~0.1 ~', (0.7, 0.05, 0.7), 0, 10))
    tl.at(L_RELEASE, g.end())
    tl.write([f'# B5 달빛 해제 (service; clip release: cup {B5_CUP}, flash {B5_FLASH}, glint {B5_GLINT}, rings {B5_RINGS}, wrap {B5_WRAP},',
              f'# detonation {B5_DET}, shrink {B5_SHRINK}, shatter {B5_SHATTER}, land {B5_LAND}). The dome r {L.num(B5_R)} at R: {DMG["b5"]} % Dendro.'],
             ['# B5 tick.'])
    g.pw(k, 'cancel', ['# Remove what B5 owns (its markers, the pod prop; the dome hazard goes with lib_clear).',
                       f'kill @e[type=minecraft:marker,tag={l_}]', f'kill @e[type=minecraft:marker,tag={r_}]',
                       *(['kill @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod]'] if rig_pod else [])])
