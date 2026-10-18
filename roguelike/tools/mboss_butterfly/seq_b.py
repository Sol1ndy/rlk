"""Wing-author sequences and helpers of the butterfly module (owner: the wing-pattern author, next to wing.py).

Writes F:mboss/butterfly/wx/** only (through the core's Gen, so the core's stale-file cleaner keeps it):

    wx/u/*       runtime helpers the wing patterns share: lockw (lock under the player inside the WALK disc r 20.3,
                 plan Q8), clamp_w / clamp_b / clamp_r (pull a marker inside r 20.3 / 16.5 / 16), okb + toward / away /
                 fwd (butterfly body steps inside r 16.5), btick (every butterfly-form tick: the body leash at r 16.5,
                 plan Q9, and the persistent Pyro rim embers of S6 section 3)
    wx/tf/<t>    S2 the transformation fx on the transform clip ticks (the core's p/transform calls them)
    wx/coc/fx    S2 section 5: the fx and sounds on the player as 달빛 고치 lands (the core's coc/apply_pl calls it)
    wx/cure/*    S5 the 20 t cure timeline at the player (gold beam, burst + ring, emblem, sparkle rain, chimes) on
                 its own clock #bpS5T (the core's coc/cure starts it, the core tick runs it, coc/clear stops it)
    wx/sw/*      S6 the wing element switch fx (the core's look/switch calls wx/sw/fx) and the Pyro rim embers

Specs: scratchpad mb2/spec/S2_transform_debuff.md, S5_cure_fx.md, S6_element_switch.md; the fx kit (bf_fx_api.md) is
the effect engine; vanilla sounds only. Every function is visual / audio only (no gameplay state of the core is set).
"""
import math

from . import api as A
from .api import L, CY, ev_or, clip_len

WX = A.WX
NS = A.NS
S5_T = '#bpS5T'               # S5 cure fx clock (1 on the cure tick, 0 = idle)

TR_LEN = clip_len('transform')
TR_OPEN = ev_or('transform', 'open', 4)
TR_SPHERE = ev_or('transform', 'sphere', 6)
TR_RINGS = ev_or('transform', 'rings', 9)
TR_SPREAD = ev_or('transform', 'spread', 12)


def fn(rel):
    return f'function {NS}{WX}/{rel}'


def ring_pts(g, rgb, r, n, y=0.15, scale=1.0, plane='h', yaw=0.0, cnt=1):
    """Dust points on a circle of radius r around the execution position: plane 'h' horizontal at height y,
    'v' vertical (in the plane turned `yaw` degrees about the vertical axis, centred at height y)."""
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        if plane == 'h':
            x, yy, z = r * math.sin(a), y, r * math.cos(a)
        else:
            u, v = r * math.cos(a), r * math.sin(a)
            x, yy, z = u * math.cos(math.radians(yaw)), y + v, u * math.sin(math.radians(yaw))
        out.append(g.dust(rgb, scale, f'~{L.num(x, 2)} ~{L.num(yy, 2)} ~{L.num(z, 2)}', (0, 0, 0), cnt))
    return out


# =============================================================================================
def utils(g):
    w = lambda rel, lines: g.w(f'{WX}/u/{rel}', lines)
    arena = '@e[tag=rlk_mb_arena,limit=1]'
    for name, r, doc in (('w', A.WALK_R, 'the WALK disc (locked ground-hazard targets, plan Q8)'),
                         ('b', A.BODY_R_B, 'the butterfly body disc (plan Q9)'),
                         ('r', A.REL_R, 'the 달빛 해제 release disc (plan Q9)')):
        rr = L.num(r)
        w(f'clamp_{name}', [f'# @s = a marker: pulled toward the arena axis (0.5 b steps) until inside r {rr}, {doc}.',
                            'scoreboard players set #bpCl mb 0', fn(f'u/clamp_{name}_s')])
        w(f'clamp_{name}_s', [f'execute at @s positioned ~ {CY} ~ if entity @e[tag=rlk_mb_arena,distance=..{rr},limit=1] run return 0',
                              'scoreboard players add #bpCl mb 1',
                              'execute if score #bpCl mb matches 90.. run return 0',
                              f'execute at @s facing entity {arena} feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~',
                              fn(f'u/clamp_{name}_s')])
    w('lockw', ['# Marker rlk_mb_bf_lock on the floor under the player\'s body, pulled inside the walk disc r '
                f'{L.num(A.WALK_R)} (not the safe disc: a player hugging the wall is still covered). Any executor.',
                'kill @e[type=minecraft:marker,tag=rlk_mb_bf_lock]',
                f'execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ {CY} ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_lock"]}}',
                f'execute as @e[type=minecraft:marker,tag=rlk_mb_bf_lock,limit=1] run {fn("u/clamp_w")}'])
    w('okb', [f'# At a proposed body position: inside r {L.num(A.BODY_R_B)} (butterfly form) with free feet and head.',
              f'execute positioned ~ {CY} ~ unless entity @e[tag=rlk_mb_arena,distance=..{L.num(A.BODY_R_B)},limit=1] run return fail',
              'execute unless block ~ ~ ~ #rlk:dash_pass run return fail',
              'execute unless block ~ ~1 ~ #rlk:dash_pass run return fail',
              'return 1'])
    w('toward', ['# @s = body: {d} blocks toward the player (no turn), only inside the butterfly disc (wx/u/okb).',
                 f'$execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^$(d) if function {NS}{WX}/u/okb run tp @s ~ ~ ~'])
    w('away', ['# @s = body: {d} blocks away from the player (no turn), only inside the butterfly disc.',
               f'$execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^$(d) if function {NS}{WX}/u/okb run tp @s ~ ~ ~'])
    w('fwd', ['# @s = body: {d} blocks along her yaw, only inside the butterfly disc.',
              f'$execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^$(d) if function {NS}{WX}/u/okb run tp @s ~ ~ ~'])
    fw = A.rest_anchor('butterfly', 'fwtip_l', A.B_FWTIP_L), A.rest_anchor('butterfly', 'fwtip_r', A.B_FWTIP_R)
    w('btick', [
        '# @s = body, at it, every module tick in butterfly form (the core tick): the body leash at r '
        f'{L.num(A.BODY_R_B)} (plan Q9: 0.3 b/t back toward the axis; her own glides stay inside), then S6 section 3:',
        '# while the wings are Pyro, every 6 t a small flame and a magenta-pink spark at each forewing tip.',
        f'execute positioned ~ {CY} ~ unless entity @e[tag=rlk_mb_arena,distance=..{L.num(A.BODY_R_B)},limit=1] '
        f'facing entity {arena} feet rotated ~ 0 positioned ^ ^ ^0.3 run tp @s ~ ~ ~',
        f'execute unless score #bfLook mb matches {A.EL_PYRO} run return 0',
        'scoreboard players operation #bfM mb = #bfClk mb', 'scoreboard players operation #bfM mb %= #bfK6 mb',
        f'execute if score #bfM mb matches 0 run {fn("sw/embers")}'])


# =============================================================================================
def switch(g):
    """S6: the 1 t wing look swap (the rig) with a short glow and <= 12 particles, <= 3 cards."""
    w = lambda rel, lines: g.w(f'{WX}/sw/{rel}', lines)
    fl, fr = A.rest_anchor('butterfly', 'fwtip_l', A.B_FWTIP_L), A.rest_anchor('butterfly', 'fwtip_r', A.B_FWTIP_R)
    body = 'execute rotated as @s rotated ~ 0 '
    w('fx', ['# @s = body, at it (look/switch, #bfLook = the new look): S6 section 2 tick 0.',
             f'execute if score #bfLook mb matches {A.EL_PYRO} run return run {fn("sw/pyro")}',
             fn('sw/dendro')])
    w('pyro', ['# -> Pyro: the kit\'s magenta-pink rim pulse (2 cards, 10 small flames), a gold wing-span glow (#FAD77C),',
               '# a magenta spark at each forewing tip; the soft whump + shimmer recipe (S6: about one real tick).',
               body + 'positioned ~ ~2.8 ~ run ' + g.fx('pyro_switch'),
               body + 'positioned ~ ~3.0 ~ run ' + g.kcard('glow', bb='center', s0=1.5, s1=4.5, life=6, fade=3, col='#FAD77C'),
               body + f'positioned {fl} run ' + g.dust(A.hexrgb('#E26E50'), 1.2, '~ ~ ~', (0.1, 0.1, 0.1), 1),
               body + f'positioned {fr} run ' + g.dust(A.hexrgb('#E26E50'), 1.2, '~ ~ ~', (0.1, 0.1, 0.1), 1),
               g.snd('pyro_switch')])
    w('dendro', ['# -> Dendro: the kit\'s lime pulse (1 card, 10 dust), pale glows at the forewing tips, two leaf puffs.',
                 body + 'positioned ~ ~2.8 ~ run ' + g.fx('dendro_switch'),
                 body + f'positioned {fl} run ' + g.kcard('glow', bb='center', s0=1.0, s1=2.5, life=5, fade=2, col='#E5FBC8'),
                 body + f'positioned {fr} run ' + g.kcard('glow', bb='center', s0=1.0, s1=2.5, life=5, fade=2, col='#E5FBC8'),
                 body + f'positioned {fl} run ' + g.particle('composter', '~ ~ ~', (0.2, 0.2, 0.2), 0, 1),
                 body + f'positioned {fr} run ' + g.particle('composter', '~ ~ ~', (0.2, 0.2, 0.2), 0, 1),
                 g.snd('dendro_switch')])
    w('embers', ['# S6 section 3 (every 6 t while the wings are Pyro): rim embers at the forewing tips (idle-b rest anchors).',
                 body + f'positioned {fl} run ' + g.particle('small_flame', '~ ~ ~', (0.15, 0.15, 0.15), 0.005, 1),
                 body + f'positioned {fr} run ' + g.particle('small_flame', '~ ~ ~', (0.15, 0.15, 0.15), 0.005, 1),
                 body + f'positioned {fl} run ' + g.dust(A.hexrgb('#E26E50'), 0.6, '~ ~ ~', (0.1, 0.1, 0.1), 1),
                 body + f'positioned {fr} run ' + g.dust(A.hexrgb('#E26E50'), 0.6, '~ ~ ~', (0.1, 0.1, 0.1), 1)])


# =============================================================================================
def transform(g):
    """S2 section 3: the fx of the transformation clip (30 t), one file per busy tick (wx/tf/<t>, @s = body, at it).
    The core keeps the mechanics (look/dendro, face/player, 달빛 고치 at the sphere, the end)."""
    body = 'execute rotated as @s rotated ~ 0 '
    chest = body + 'positioned ~ ~1.6 ~ run '
    core_at = A.anchor('transform', 'sphere', 'core', (0.0, 2.2, 0.0))
    fl, fr = A.rest_anchor('butterfly', 'fwtip_l', A.B_FWTIP_L), A.rest_anchor('butterfly', 'fwtip_r', A.B_FWTIP_R)
    ev = {}
    add = lambda t, *lines: ev.setdefault(t, []).extend(lines)
    add(0, '# t0 the green vertical glow sheath wraps her lower body (kit tf_sheath), the cocoon glow recipe.',
        chest + g.fx('tf_sheath'), g.snd('transform_glow'),
        g.dust(A.hexrgb('#B5F089'), 1.3, '~ ~1.0 ~', (0.3, 0.7, 0.3), 10),
        g.dust(A.hexrgb('#508B90'), 0.8, '~ ~1.0 ~', (0.35, 0.7, 0.35), 4))
    for t in range(1, TR_OPEN):
        add(t, g.dust(A.hexrgb('#C2FA72'), 1.2, '~ ~1.0 ~', (0.25, 0.6, 0.25), 6))
    add(TR_OPEN, f'# t{TR_OPEN} the folded wings open partially: white sparks, a rim glint on each folded wing.',
        g.particle('end_rod', '~ ~2.3 ~', (0.3, 0.3, 0.3), 0.05, 6),
        body + 'positioned ^0.6 ^2.6 ^-0.3 run ' + g.kcard('glint', bb='center', s0=0.3, s1=0.9, life=3, fade=1, col='#EFFDA2'),
        body + 'positioned ^-0.6 ^2.6 ^-0.3 run ' + g.kcard('glint', bb='center', s0=0.3, s1=0.9, life=3, fade=1, col='#EFFDA2'),
        g.sound('entity.ender_dragon.flap', 0.6, 1.5))
    add(TR_SPHERE - 1, f'# t{TR_SPHERE - 1} the core flash: a yellow-white flare at her chest.',
        body + f'positioned {core_at} run ' + g.kcard('glint', bb='center', s0=0.4, s1=2.0, life=3, fade=1, col='#FAFCD4'),
        g.dust(A.hexrgb('#FAFCD4'), 1.6, '~ ~2.2 ~', (0.15, 0.15, 0.15), 12))
    sph = [f'# t{TR_SPHERE} the light sphere r 2.5 (kit tf_sphere; 달빛 고치 lands now, the core\'s form/sphere), three vertical',
           '# particle rings and a horizontal one r 2.5, a bloom; the swell recipe and a curse-like chime.',
           chest + g.fx('tf_sphere'), g.snd('transform_swell'), g.sound('entity.elder_guardian.curse', 0.4, 1.6),
           g.particle('flash{color:[0.97,0.99,0.73,1.0]}', '~ ~1.6 ~', (0, 0, 0), 0, 1)]
    sph += ring_pts(g, A.hexrgb('#F8FDBB'), 2.5, 12, y=1.6, scale=1.3)
    for yaw in (0, 60, 120):
        sph += ring_pts(g, A.hexrgb('#FAFCD4'), 2.5, 10, y=1.6, scale=1.0, plane='v', yaw=yaw)
    add(TR_SPHERE, *sph)
    add(TR_RINGS, f'# t{TR_RINGS} the sphere bursts into ripple rings (kit tf_ripples: a floor ring, two vertical arcs, radial',
        '# speed lines) and a floor dust ring r 3.', chest + g.fx('tf_ripples'),
        g.sound('entity.breeze.wind_burst', 0.8, 0.8), g.sound('block.amethyst_block.resonate', 0.7, 1.0),
        *ring_pts(g, A.hexrgb('#BDE592'), 3.0, 16, y=0.15, scale=1.2))
    add(TR_RINGS + 1, '# ripple 2: floor ring r 4.', *ring_pts(g, A.hexrgb('#BDE592'), 4.0, 20, y=0.15, scale=1.2))
    add(TR_RINGS + 2, '# ripple 3: floor ring r 5 (dark mint), the swell flap.', *ring_pts(g, A.hexrgb('#428B71'), 5.0, 24, y=0.15, scale=1.2),
        g.sound('entity.ender_dragon.flap', 0.6, 1.5))
    add(max(TR_SPREAD, TR_RINGS + 3), '# the wings fully spread: a sparkle at each forewing tip.',
        body + f'positioned {fl} run ' + g.kcard('glint', bb='center', s0=0.2, s1=0.8, life=4, fade=2, col='#E5FBC8'),
        body + f'positioned {fr} run ' + g.kcard('glint', bb='center', s0=0.2, s1=0.8, life=4, fade=2, col='#E5FBC8'))
    add(max(TR_SPREAD, TR_RINGS + 3) + 1, g.sound('entity.ender_dragon.flap', 0.5, 1.5))
    for t in range(16, TR_LEN, 4):
        add(t, body + f'positioned {fl} run ' + g.dust(A.LIME_PALE, 0.8, '~ ~ ~', (0.3, 0.2, 0.3), 2),
            body + f'positioned {fr} run ' + g.dust(A.LIME_PALE, 0.8, '~ ~ ~', (0.3, 0.2, 0.3), 2))
    for t in (18, 24):
        add(t, g.snd('flap_small'))
    for t, lines in ev.items():
        g.w(f'{WX}/tf/{t}', [f'# S2 transformation fx, clock {t} (@s = body, at it; the core\'s p/transform calls it).'] + lines)
    return sorted(ev)


TF_TICKS = None               # filled by emit(): the transformation clock ticks that have a wx/tf/<t> file


# =============================================================================================
def debuff(g):
    """S2 section 5: 달빛 고치 lands on the player (run at the player's body, rotated ~ 0)."""
    pts = []
    for i in range(16):
        a = 2 * math.pi * i * 1.5 / 16
        r = 0.35 + 0.75 * i / 15
        y = 0.3 + 1.9 * i / 15
        col = A.COC if i % 2 == 0 else A.COC_SWIRL
        pts.append(g.dust(col, 1.1, f'~{L.num(r * math.sin(a), 2)} ~{L.num(y, 2)} ~{L.num(r * math.cos(a), 2)}', (0, 0, 0), 1))
    g.w(f'{WX}/coc/fx', ['# At the player\'s feet (the core\'s coc/apply_pl): the kit\'s maroon swirl ring, salmon glow and badge glyph',
                         '# (coc_apply), a maroon / salmon dust spiral rising 0.3 -> 2.2 b around the body, the badge pop glow over',
                         '# the head; the debuff recipe and a curse chime.',
                         g.fx('coc_apply'), *pts,
                         g.kcard('glow', '~ ~2.4 ~', bb='center', s0=0.4, s1=1.2, life=8, fade=4, col=A.COC_HEX),
                         g.snd('debuff'), g.sound('entity.elder_guardian.curse', 0.35, 1.7),
                         g.sound('block.amethyst_block.resonate', 0.6, 0.7)])


# =============================================================================================
def cure(g):
    """S5: 20 t at the player's body on the clock #bpS5T (t = #bpS5T - 1): the kit's cure (beam, burst + ring, emblem)
    plus the descending beam dust, the gold particle rings, the sparkle rain and the chime layers."""
    ev = {}
    add = lambda t, *lines: ev.setdefault(t, []).extend(lines)
    add(0, '# t0 (the cure tick): the kit\'s cure (gold beam 0-8, burst + ring from 6, emblem from 11) and its chime recipe.',
        g.fx('cure'), g.snd('cure_chime'))
    add(1, g.sound('block.amethyst_block.chime', 0.6, 2.0))
    for t in range(1, 7):
        y = 6.5 - (t - 1)
        add(t, g.dust(A.GOLD, 1.3, f'~ ~{L.num(y)} ~', (0.05, 0.5, 0.05), 6),
            g.dust(A.WHITE, 0.8, f'~ ~{L.num(y - 0.6)} ~', (0.05, 0.2, 0.05), 2))
    add(3, g.sound('block.beacon.ambient', 0.4, 2.0))
    add(7, g.sound('entity.firework_rocket.twinkle', 0.6, 1.2), g.sound('block.amethyst_block.resonate', 0.6, 1.4))
    for t in range(7, 12):
        add(t, *ring_pts(g, A.GOLD_RING, 1.5 + 0.25 * (t - 7), 14, y=1.0, scale=0.9))
    add(9, g.sound('block.amethyst_block.chime', 0.8, 1.7))
    add(12, g.sound('entity.player.levelup', 0.35, 1.8), g.sound('block.amethyst_block.chime', 0.7, 1.7))
    for t in range(12, 21):
        add(t, g.particle('wax_on', '~ ~3.0 ~', (0.8, 0.4, 0.8), 0, 2), g.particle('end_rod', '~ ~3.0 ~', (0.6, 0.3, 0.6), 0.01, 1))
    add(14, g.sound('block.amethyst_block.chime', 0.7, 2.0))
    for t, lines in ev.items():
        if t:
            g.w(f'{WX}/cure/k/{t}', [f'# S5 cure fx, t {t} (at the player\'s body).'] + lines)
    g.w(f'{WX}/cure/start', ['# 달빛 고치 cured (the core\'s coc/cure, at the player\'s body): S5 tick 0, then the clock.',
                             f'scoreboard players set {S5_T} mb 1'] + ev[0])
    last = max(ev)
    g.w(f'{WX}/cure/tick', [f'# Every module tick while {S5_T} >= 1 (the core tick, at the player\'s body): S5 ticks 1..{last}.',
                            f'scoreboard players add {S5_T} mb 1',
                            f'scoreboard players operation #bfM mb = {S5_T} mb', 'scoreboard players remove #bfM mb 1']
           + [f'execute if score #bfM mb matches {t} run {fn(f"cure/k/{t}")}' for t in sorted(ev) if t]
           + [f'execute if score #bfM mb matches {last}.. run scoreboard players set {S5_T} mb 0'])


def emit(g):
    """Called by the core (Core.transform: one hook line)."""
    global TF_TICKS
    utils(g)
    switch(g)
    TF_TICKS = transform(g)
    debuff(g)
    cure(g)
