"""Field-form patterns of the field generator (stage-1 STUBS by the core author: timelines, hit areas, coefficients,
volley groups and telegraphs of plan.md "Field" are final; the visuals are plain vanilla particles for the pattern
author to replace with the fx kit, see scratchpad mb3/fg_contract.md §12).

    11 fzone  F1 중력 시스템·감소 영역   9 eruption events, 1-4 dark discs each
    12 frock  F2 중력 시스템·파쇄        bursts walking onto the player + slab throws (C6 without the tower)
    21 waves  「인력 충격파」 x3          service: the core runs it at the field's start (#fgWvK 1) and end (2)

The device sits at the arena centre for the whole field (the core put it there); low gravity is on and the meter
is open while these run. Pattern scores #fq<id>*, tags rlk_mb_fg_p<id>* + rlk_mb_fg_pat.
"""
from .api import Pattern, TL, ev_or, clip_len, DMG, KB, CY, NS, L, rocks, rocks_cancel, GOLD, GOLD_DEEP, WHITE_GOLD, VIOLET, ROCK

# F1: activation 22 t, then 9 eruption events at 11-50 t intervals; each 1-4 discs r 2.8, 15 t decal, gold eruption
F1_ACT = ev_or('field_erupt', 'erupt', 22)
F1_EVENTS = [F1_ACT + d for d in (0, 18, 30, 56, 78, 94, 124, 148, 168)]       # gaps 18 12 26 22 16 30 24 20
F1_TELL = 15
F1_END = F1_EVENTS[-1] + F1_TELL + 11
# F2: a 20 t activation, then the rocks: bursts from 20, throws from 62
F2_BURST, F2_THROW = 20, 62
# waves: impacts 24 / 92 / 175 (gaps 68, 83), charges 24 / 24 / 40; below 50 % HP the 3rd fires 3 fronts 9 t apart
W_IMPACT = (24, 92, 175)
W_CHARGE = (24, 24, 40)
W_TRI_GAP = 9
W_SPEED = 0.55          # front speed, b/t (r = 2.5 + 0.55 k after the impact)
W_BAND = 2.5            # hit band [r - 2.5, r]
W_ACT = 36              # r 2.5 -> 22.3: past the wall
W_LEN = W_IMPACT[2] + 2 * W_TRI_GAP + W_ACT + 3
assert all(W_IMPACT[i] - W_CHARGE[i] >= 0 for i in range(3)) and W_IMPACT[1] - W_IMPACT[0] == 68 and W_IMPACT[2] - W_IMPACT[1] == 83

PATTERNS = [
    Pattern(11, 'fzone', '중력 시스템·감소 영역', 'f', 'field_erupt', bands=('melee', 'mid', 'far'), recover=14,
            max_len=F1_END + 8, length=F1_END),
    Pattern(12, 'frock', '중력 시스템·파쇄', 'f', 'field_erupt', bands=('melee', 'mid', 'far'), recover=14,
            max_len=128, length=120),
    Pattern(21, 'waves', '「인력 충격파」', 'f', 'wave', kind='service', recover=0, max_len=W_LEN + 8, length=W_LEN),
]


def emit(g):
    fzone(g)
    frock(g)
    waves(g)


# ---------------------------------------------------------------------------------------------
def fzone(g):
    """F1 감소 영역: the gyroscope locks and the medallions slide out on link beams (activation 22 t), then 9
    eruption events at 11-30 t intervals: 1-4 dark discs (hz/disc r 2.8, tell 15, not jumpable) 2-8 b from the
    player, the first 2-3 b off (never on the player, but a standing player is inside it), one volley group per event
    (all its discs made in the same tick), inside the walk disc; gold eruptions + rock debris at the strike."""
    key, tl = 'fzone', TL(g, 'fzone')
    D = 'rlk_mb_fg_p11d'
    tags = '"rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p11"'
    g.pw(key, 'event', [
        '# One eruption event (@s = body): 1-4 discs, the first 2-3 b off the player, the others 2-8 b; one volley group.',
        g.GRP_NEW,
        'execute store result score #fq11N mb run random value 1..4',
        'execute store result storage rlk:mboss fg.fz.d double 0.1 run random value 20..30',
        f'function {NS}p/{key}/disc',
        f'function {NS}p/{key}/more',
        g.sound('block.respawn_anchor.charge', 0.6, 1.5)])
    g.pw(key, 'more', [
        'scoreboard players remove #fq11N mb 1',
        'execute if score #fq11N mb matches ..0 run return 0',
        'execute store result storage rlk:mboss fg.fz.d double 0.1 run random value 20..80',
        f'function {NS}p/{key}/disc',
        f'function {NS}p/{key}/more'])
    g.pw(key, 'disc', [
        '# A random yaw and the distance fg.fz.d from the player: a marker, pulled into the walk disc, the disc there.',
        'execute store result storage rlk:mboss fg.fz.a double 1 run random value 0..359',
        f'function {NS}p/{key}/place with storage rlk:mboss fg.fz',
        f'execute as @e[type=minecraft:marker,tag={D}] run {g.clamp_walk()}',
        *g.hz_opts(kb=KB['default'], grp=True, vis=111),
        f'execute at @e[type=minecraft:marker,tag={D},limit=1] run ' + g.hz_disc(2.8, F1_TELL, DMG['f1']),
        f'execute at @e[type=minecraft:marker,tag={D},limit=1] run ' + g.dust((0.18, 0.12, 0.22), 1.6, '~ ~0.1 ~', (1.2, 0.02, 1.2), 10),
        f'kill @e[type=minecraft:marker,tag={D}]'])
    g.pw(key, 'place', [f'$execute at @e[tag=rlk_body,limit=1] rotated $(a) 0 positioned ^ ^ ^$(d) run summon minecraft:marker ~ {CY} ~ '
                        f'{{Tags:[{tags},"{D}"]}}'])
    tl.at(0, g.sound('block.beacon.power_select', 0.8, 1.0), g.sound('block.chain.place', 0.8, 1.2))
    for t in range(0, F1_ACT, 3):
        tl.at(t, 'execute at @s rotated as @s run ' + g.dust(GOLD, 1.0, '^3.85 ^3.8 ^', (0.1, 0.1, 0.1), 2),
              'execute at @s rotated as @s run ' + g.dust(GOLD, 1.0, '^-3.85 ^3.8 ^', (0.1, 0.1, 0.1), 2))
    for t in F1_EVENTS:
        tl.at(t, f'function {NS}p/{key}/event')
    tl.at(F1_END, g.end())
    tl.write([f'# F1 감소 영역 (clip field_erupt; @s = body at the centre): events {F1_EVENTS} (strike +{F1_TELL}).'], ['# fzone tick.'])
    g.pw(key, 'vis', ['# @s = an eruption disc (#hzEv 1 = it erupts): gold eruption 3.5 b tall, rock chunks.',
                      'execute unless score #hzEv mb matches 1 run return 0',
                      g.dust(GOLD_DEEP, 1.8, '~ ~1.5 ~', (1.0, 1.4, 1.0), 14), g.dust(WHITE_GOLD, 1.2, '~ ~0.5 ~', (1.4, 0.3, 1.4), 8),
                      g.particle('block{block_state:"minecraft:tuff"}', '~ ~0.5 ~', (1.0, 0.5, 1.0), 0, 16),
                      g.sound('entity.generic.explode', 0.7, 1.0), g.sound('block.basalt.break', 1.0, 0.6)])
    g.pw(key, 'cancel', ['# The placement marker (the discs are framework hazards).', 'kill @e[tag=rlk_mb_fg_p11]'])


# ---------------------------------------------------------------------------------------------
def frock(g):
    """F2 파쇄 in the field form: no tower build-up (a 20 t activation with the flame band), then api.rocks(): 8 floor
    bursts walking onto the player from 20 (r 1.8, tell 10, jumpable, 1.3, heavy KB), the lifted slabs, 5 throws from
    62 8 t apart (blade pj 1.5 b/t, 1.1)."""
    key, tl = 'frock', TL(g, 'frock')
    tl.at(0, g.sound('block.respawn_anchor.charge', 0.8, 0.9), g.sound('block.chain.place', 0.8, 0.8))
    for t in range(0, F2_BURST, 2):
        tl.at(t, *['execute at @s run ' + x for x in g.ring_dust(VIOLET, 3.0, 12, 1.0, 1.3)])
    done = rocks(g, tl, key, 12, F2_BURST, throw0=F2_THROW, dmg=DMG['f2'], dmg_s=DMG['f2s'])
    assert done <= 120, done
    tl.at(120, *rocks_cancel(12), g.end())
    tl.write([f'# F2 파쇄 (clip field_erupt; @s = body at the centre): bursts from {F2_BURST}, throws from {F2_THROW}.'],
             ['# frock tick.'], extra_tick=[f'function {NS}p/{key}/slabs'])
    g.pw(key, 'vis', ['# @s = a floor burst (#hzEv 1 = it strikes).', 'execute unless score #hzEv mb matches 1 run return 0',
                      g.particle('block{block_state:"minecraft:tuff"}', '~ ~0.3 ~', (0.8, 0.3, 0.8), 0, 14),
                      g.dust(GOLD_DEEP, 1.4, '~ ~0.4 ~', (0.6, 0.2, 0.6), 6),
                      g.sound('block.tuff.break', 1.2, 0.5), g.sound('entity.generic.explode', 0.6, 1.1)])
    g.pw(key, 'cancel', ['# Walker, slabs, locks.'] + rocks_cancel(12))


# ---------------------------------------------------------------------------------------------
def waves(g):
    """「인력 충격파」 x3 (service 21; the core starts it at the field's start, #fgWvK 1, and end, #fgWvK 2): per wave a
    charge sphere at the core (24 / 24 / 40 t), a 1-tick beam, a flare dome, then an arena-wide ring front expanding at
    0.55 b/t from r 2.5: framework hz/ring made at the charge start (its outline is the telegraph), hit band
    [r - 2.5, r], height 0..0.7 b (a jump clears it), #hzNoDodge 1 (dash i-frames do NOT help), the radius grown every
    tick with hz/resize_s; below 50 % HP (or test 42) the 3rd wave fires 3 fronts 9 t apart. Coefficient 1.2 each."""
    key, tl = 'waves', TL(g, 'waves')
    F = 'rlk_mb_fg_p21f'
    starts = [W_IMPACT[i] - W_CHARGE[i] for i in range(3)]

    def front(tell):
        return [*g.hz_opts(act=W_ACT, y1=0.7, kb=KB['default'], nododge=1, sfx=0, vis=211),
                g.hz_ring(0.0, W_BAND, tell, DMG['wave']), g.tag_last_hz(F)]

    g.pw(key, 'grow', [
        '# @s = a live front (from tick, before hz/all): radius 2.5 + 0.55 k b at its k-th active tick (this tick\'s hit',
        '# test), inner radius r - 2.5 (tenths: r = 25 + 11 k / 2).',
        'scoreboard players operation #hzSzR mb = @s mbHzT',
        'scoreboard players operation #hzSzR mb -= @s mbHzW',
        'scoreboard players add #hzSzR mb 1',
        'execute if score #hzSzR mb matches ..0 run return 0',
        f'execute if score #hzSzR mb matches {W_ACT + 1}.. run return 0',
        'scoreboard players operation #hzSzR mb *= #fgK11 mb',
        'scoreboard players operation #hzSzR mb /= #c2 mb',
        f'scoreboard players add #hzSzR mb {int(W_BAND * 10)}',
        'scoreboard players operation #hzSzR0 mb = #hzSzR mb',
        f'scoreboard players remove #hzSzR0 mb {int(W_BAND * 10)}',
        'scoreboard players set #hzSzW mb 0',
        'function rlk:mboss/hz/resize_s',
        'scoreboard players operation #fgM mb = @s mbHzT',
        'scoreboard players operation #fgM mb %= #fgK2 mb',
        f'execute if score #fgM mb matches 0 at @s run function {NS}p/{key}/draw'])
    g.pw(key, 'draw', [
        '# @s = a live front, at it: its current rim as dust points (the framework circle primitive of radius k / 2).',
        'scoreboard players operation #fq21K mb = @s mbHzR',
        'scoreboard players add #fq21K mb 250',
        'scoreboard players operation #fq21K mb /= #c500 mb',
        'execute if score #fq21K mb matches ..0 run scoreboard players set #fq21K mb 1',
        'execute if score #fq21K mb matches 61.. run scoreboard players set #fq21K mb 60',
        'execute store result storage rlk:mboss fg.wv.k int 1 run scoreboard players get #fq21K mb',
        'scoreboard players set #hzAng mb 180',
        f'function {NS}p/{key}/draw_m with storage rlk:mboss fg.wv'])
    g.pw(key, 'draw_m', ['$function rlk:mboss/hz/p/c/$(k) with storage rlk:mboss fg.wv'])
    g.pw(key, 'charge', ['# @s = body: the charge sphere at the hanging core (about 3.8 b up), pulsing.',
                         'execute at @s run ' + g.dust(WHITE_GOLD, 1.4, '~ ~3.8 ~', (0.45, 0.45, 0.45), 6),
                         'execute at @s run ' + g.particle('end_rod', '~ ~3.8 ~', (0.3, 0.3, 0.3), 0.02, 1)])
    g.pw(key, 'impact', ['# @s = body: the 1-tick beam, the flare dome and the burning disc under the core.',
                         *[f'execute at @s run ' + g.dust(WHITE_GOLD, 1.6, f'~ ~{L.num(y, 1)} ~', (0.08, 0.1, 0.08), 2) for y in (3.4, 2.6, 1.8, 1.0, 0.2)],
                         'execute at @s run ' + g.particle('flash{color:[0.99,0.95,0.70,1.0]}', '~ ~0.6 ~', (0, 0, 0), 0, 1),
                         'execute at @s run ' + g.dust(GOLD_DEEP, 2.0, '~ ~0.3 ~', (1.2, 0.1, 1.2), 16),
                         g.sound('entity.generic.explode', 1.0, 0.8), g.sound('block.respawn_anchor.deplete', 0.9, 0.9),
                         g.sound('entity.breeze.wind_burst', 1.0, 0.6)])
    g.pw(key, 'tri', [
        '# Clock {0}: the 3rd wave fires 3 fronts below 50 % HP (or with test 42, #fgTri 1).'.format(starts[2]),
        'scoreboard players set #fq21T mb 0',
        'scoreboard players operation #fgX mb = @s mhpC',
        'scoreboard players operation #fgX mb *= #c2 mb',
        'execute if score #fgX mb < @s mhpM run scoreboard players set #fq21T mb 1',
        'execute if score #fgTri mb matches 1 run scoreboard players set #fq21T mb 1'])
    g.pw(key, 'tri_go', ['# The two extra fronts of the 3rd wave (9 and 18 t after its first).',
                         *front(W_CHARGE[2] + W_TRI_GAP), *front(W_CHARGE[2] + 2 * W_TRI_GAP)])
    tl.at(0, 'data modify storage rlk:mboss fg.wv set value {k:5,col:"[0.98f,0.66f,0.28f]",sc:"1.8"}',
          f'kill @e[type=minecraft:marker,tag={F}]')
    for i in range(3):
        s0, imp = starts[i], W_IMPACT[i]
        lines = list(front(W_CHARGE[i]))
        if i == 2:
            lines = [f'function {NS}p/{key}/tri'] + lines + [f'execute if score #fq21T mb matches 1 run function {NS}p/{key}/tri_go']
        clip_at = imp - ev_or('wave', 'impact', 24)
        if clip_at > 0:
            tl.at(clip_at, g.play('wave'))
        tl.at(s0, *lines, g.sound('block.beacon.power_select', 0.9, 0.7), g.sound('entity.breeze.charge', 0.8, 0.5))
        for t in range(s0, imp, 2):
            tl.at(t, f'function {NS}p/{key}/charge')
        for t in range(s0, imp, 8):
            tl.at(t, g.sound('block.respawn_anchor.ambient', 0.9, 1.4))
        tl.at(imp, f'function {NS}p/{key}/impact')
        if i == 2:
            for k in (1, 2):
                tl.at(imp + k * W_TRI_GAP, f'execute if score #fq21T mb matches 1 run function {NS}p/{key}/impact')
    tl.at(W_LEN, f'kill @e[type=minecraft:marker,tag={F}]', g.end())
    tl.write([f'# 「인력 충격파」 x3 (service 21, clip wave; @s = body at the centre): impacts {W_IMPACT} (charges {W_CHARGE}),',
              f'# the 3rd wave x3 below 50 % HP; end {W_LEN}.'], ['# waves tick.'],
             extra_tick=[f'execute as @e[type=minecraft:marker,tag={F}] run function {NS}p/{key}/grow'])
    g.pw(key, 'vis', ['# @s = a front (#hzEv 1 = the impact under the core).', 'execute unless score #hzEv mb matches 1 run return 0',
                      g.particle('block{block_state:"minecraft:tuff"}', '~ ~0.3 ~', (1.0, 0.2, 1.0), 0, 12)])
    g.pw(key, 'cancel', ['# The fronts (framework hazards; lib_clear usually got them first).', f'kill @e[type=minecraft:marker,tag={F}]'])
