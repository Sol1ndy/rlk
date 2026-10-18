"""Cruise-form patterns C1-C6 of the field generator (stage-1 STUBS by the core author: the timelines, hit areas,
coefficients, volley groups and telegraphs of plan.md "Rotation" are final; the visuals are plain vanilla particles
for the pattern author to replace with the fx kit, see scratchpad mb3/fg_contract.md §12).

    1 bomb     C1 중력 시스템·일점 상쇄 (폭격)   mid / far x2
    2 slam     C2 내려찍기                      melee x2 / mid
    3 laser    C3 중력 시스템·코어 (레이저 빔)    melee x2 / mid x2
    4 missile  C4 중력 시스템·바위 폭탄 (미사일)  far x3 only
    5 burst    C5 중력 시스템·지면 충격 (중력 폭발) melee x2 / mid
    6 rock     C6 중력 시스템·파쇄 (바위 날리기)   mid x2 / far

Every damaging hit is a framework hz/* (or a blade pj for the slabs) with >= 10 t of telegraph; the framework draws
the outlines while no kit decal exists (#hzQuiet 0). Pattern scores #fq<id>*, tags rlk_mb_fg_p<id>* + rlk_mb_fg_pat.
"""
from .api import Pattern, TL, ev_or, clip_len, DMG, KB, CY, NS, L, rocks, rocks_cancel, GOLD, GOLD_DEEP, WHITE_GOLD, AMBER

BODY = '@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]'
PLAYER = '@e[tag=rlk_body,limit=1]'

# C1: turn 10 + ports 2, then 20 bombs over 45 t along the locked flight line (glide <= 0.55 b/t), the slam finisher
C1_RUN = ev_or('bomb_run', 'run', 12)
C1_GLIDE = 45
C1_BOMBS = [C1_RUN + (9 * k) // 4 for k in range(20)]          # drop ticks, 2.25 t apart
C1_FALL = 6                                                    # a bomb falls 6 t onto its decal
C1_LEAD = 4                                                    # decal made 4 t before the drop: 10 t of warning
C1_SIDE = (-1.2, 0.0, 1.2)
C1_SLAM = clip_len('bomb_run')                                 # 58: the finisher's clip
C1_SLAM_HIT = C1_SLAM + ev_or('slam', 'impact', 17)            # 75
# C2: the column tell 13 t, plunge 4 t, slam at 17
C2_HIT = ev_or('slam', 'impact', 17)
# C3: pods drop 4 + charge 18 + aim 2: fire at 24 for 133 t, two counter-rotating beams 5 deg/t
C3_FIRE = ev_or('laser', 'fire', 24)
C3_ACT = 133
C3_R0, C3_LEN = 2.8, 3.0                                       # beam band from r 2.8 to r 5.8 (floor spots on r ~5)
# C4: flares 8 + vent 13, 10 missiles over 14 t, late lock at +7 (decal tell 13), impact at +20
C4_LAUNCH = ev_or('missiles', 'launch', 21)
C4_T = [C4_LAUNCH + (3 * i) // 2 for i in range(10)]
C4_LOCK, C4_HIT = 7, 20
# C5: rim decal + hazard at 3 (tell 45), blast at 48
C5_RIM = ev_or('coreup', 'rim', 3)
C5_BLAST = ev_or('coreup', 'blast', 48)
# C6: dip 12, vent 8, tower 18, flame band 17, then 8 bursts 6 t apart, 5 slab throws 8 t apart
C6_BURST = ev_or('tower_throw', 'burst', 55)
C6_THROW = ev_or('tower_throw', 'throw', 95)

PATTERNS = [
    Pattern(1, 'bomb', '중력 시스템·일점 상쇄', 'c', 'bomb_run', bands=('mid', 'far'), weight={'far': 2},
            max_len=110, length=C1_SLAM_HIT + 25),
    Pattern(2, 'slam', '내려찍기', 'c', 'slam', bands=('melee', 'mid'), weight={'melee': 2},
            max_len=clip_len('slam') + 7, length=clip_len('slam')),
    Pattern(3, 'laser', '중력 시스템·코어', 'c', 'laser', bands=('melee', 'mid'), weight={'melee': 2, 'mid': 2},
            max_len=clip_len('laser') + 6, length=clip_len('laser')),
    Pattern(4, 'missile', '중력 시스템·바위 폭탄', 'c', 'missiles', bands=('far',), weight={'far': 3},
            max_len=clip_len('missiles') + 8, length=clip_len('missiles')),
    Pattern(5, 'burst', '중력 시스템·지면 충격', 'c', 'coreup', bands=('melee', 'mid'), weight={'melee': 2},
            max_len=clip_len('coreup') + 8, length=clip_len('coreup')),
    Pattern(6, 'rock', '중력 시스템·파쇄', 'c', 'tower_throw', bands=('mid', 'far'), weight={'mid': 2},
            max_len=clip_len('tower_throw') + 8, length=clip_len('tower_throw')),
]


def face(g):
    return f'execute at @s facing entity {PLAYER} feet run tp @s ~ ~ ~ ~ 0'


def column(g, sel, top=4.2):
    """Gold column particles from `top` b down to the floor at the entity sel (a telegraph look)."""
    return [f'execute at {sel} run ' + g.dust(GOLD, 1.6, f'~ ~{L.num(top * f, 2)} ~', (0.12, 0.05, 0.12), 2)
            for f in (1.0, 0.75, 0.5, 0.25, 0.05)]


def emit(g):
    bomb(g)
    slam(g)
    laser(g)
    missile(g)
    burst(g)
    rock(g)


# ---------------------------------------------------------------------------------------------
def bomb(g):
    """C1 일점 상쇄: the route is locked at 0 (toward the player, 24.75 b = 45 t x 0.55 b/t, its end pulled back along
    the line into r 16.5); a predictor marker glides the same route 4 t ahead of the body, so every bomb's decal
    (hz/disc r 1.3, tell 10) is made at the predictor 4 t before the drop and the bomb lands on it 6 t after the
    drop. Bombs every 2.25 t from three ports (-1.2 / 0 / +1.2 b across the line), volley groups of 4 (all four
    decals of a group exist before its first strike). Then the slam: column 13 t, plunge, disc r 5 at 75."""
    key, tl = 'bomb', TL(g, 'bomb')
    P, E, B = 'rlk_mb_fg_p1p', 'rlk_mb_fg_p1e', 'rlk_mb_fg_p1b'
    pred, end = f'@e[type=minecraft:marker,tag={P},limit=1]', f'@e[type=minecraft:marker,tag={E},limit=1]'
    tags = '"rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p1"'
    g.pw(key, 'route', [
        '# @s = body, at it, facing the player: the end of the flight line (pulled back along it into r 16.5) and the',
        '# predictor at the body with the locked yaw.',
        f'kill @e[type=minecraft:marker,tag={P}]', f'kill @e[type=minecraft:marker,tag={E}]',
        f'summon minecraft:marker ~ ~ ~ {{Tags:[{tags},"{P}"]}}',
        f'execute rotated as @s run tp {pred} ~ ~ ~ ~ 0',
        f'execute rotated as @s positioned ^ ^ ^{L.num(0.55 * C1_GLIDE)} run summon minecraft:marker ~ ~ ~ {{Tags:[{tags},"{E}"]}}',
        f'execute as {end} at @s rotated as {BODY} run tp @s ~ ~ ~ ~180 0',
        'scoreboard players set #fq1N mb 0',
        f'execute as {end} at @s run function {NS}p/{key}/pull'])
    g.pw(key, 'pull', [
        '# @s = the route end (facing back to the start): 0.5 b steps back until inside the body disc r 16.5.',
        f'execute positioned ~ {CY} ~ if entity @e[tag=rlk_mb_arena,distance=..16.5,limit=1] run return 0',
        'scoreboard players add #fq1N mb 1',
        'execute if score #fq1N mb matches 50.. run return 0',
        'execute at @s rotated as @s run tp @s ^ ^ ^0.5',
        f'execute at @s run function {NS}p/{key}/pull'])
    g.pw(key, 'drop', [
        '# @s = body (on the route), rotated as the predictor: one bomb display at the port, falling next tick.',
        f'summon minecraft:item_display ^ ^4.2 ^ {{Tags:[{tags},"{B}","rlk_mb_fg_pnew"],teleport_duration:{C1_FALL - 1},'
        'billboard:"center",brightness:{block:15,sky:15},item:{id:"minecraft:fire_charge",count:1},'
        'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}',
        'scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbT 0',
        'tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew',
        g.particle('flame', '~ ~4 ~', (0.15, 0.1, 0.15), 0.01, 2)])
    g.pw(key, 'bomb', [
        '# @s = a falling bomb, at it: down to the floor in 5 t (client-interpolated), burst on its decal.',
        'scoreboard players add @s mbT 1',
        'execute if score @s mbT matches 1 run tp @s ~ ~-4.2 ~',
        f'execute if score @s mbT matches {C1_FALL}.. run ' + g.particle('explosion', '~ ~0.2 ~', (0.2, 0.05, 0.2), 0, 1),
        f'execute if score @s mbT matches {C1_FALL}.. run ' + g.dust(GOLD_DEEP, 1.4, '~ ~0.2 ~', (0.5, 0.1, 0.5), 6),
        f'execute if score @s mbT matches {C1_FALL}.. run ' + g.sound('entity.generic.explode', 0.45, 1.6),
        f'execute if score @s mbT matches {C1_FALL}.. run kill @s'])
    tl.at(0, face(g), f'execute rotated as @s rotated ~ 0 run function {NS}p/{key}/route',
          g.sound('block.piston.extend', 0.8, 0.6), g.sound('block.chain.place', 0.8, 0.8))
    tl.at(10, g.sound('block.beacon.power_select', 0.6, 1.6),
          f'execute at @s rotated as @s run ' + g.dust(GOLD, 1.2, '^ ^3.8 ^', (1.0, 0.1, 1.0), 10))
    tl.at(C1_RUN - C1_LEAD, f'execute as {pred} positioned as {end} run function rlk:mboss/mv/glide {{t:{C1_GLIDE}}}')
    tl.at(C1_RUN, f'execute positioned as {end} run function rlk:mboss/mv/glide {{t:{C1_GLIDE}}}',
          g.sound('entity.breeze.charge', 0.8, 0.6))
    for k, tk in enumerate(C1_BOMBS):
        off = C1_SIDE[k % 3]
        lines = []
        if k % 4 == 0:
            lines.append(g.GRP_NEW)
        lines += g.hz_opts(kb=KB['light'], grp=True)
        lines.append(f'execute at {pred} rotated as {pred} positioned ^{L.num(off)} ^ ^ positioned ~ {CY} ~ run '
                     + g.hz_disc(1.3, C1_LEAD + C1_FALL, DMG['c1']))
        tl.at(tk - C1_LEAD, *lines)
        tl.at(tk, f'execute rotated as {pred} positioned ^{L.num(off)} ^ ^ run function {NS}p/{key}/drop',
              g.sound('block.dispenser.launch', 0.5, 1.4))
    tl.at(C1_SLAM, g.play('slam'), *g.hz_opts(kb=KB['heavy'], y1=2.0, vis=12), g.hz_disc(5.0, C1_SLAM_HIT - C1_SLAM, DMG['c1s']),
          g.sound('block.respawn_anchor.charge', 0.9, 0.7), g.sound('block.beacon.activate', 0.6, 1.5))
    for t in range(C1_SLAM, C1_SLAM + 13, 2):
        tl.at(t, *column(g, '@s'))
    tl.at(C1_SLAM + 13, g.sound('block.piston.contract', 1.0, 0.5))
    tl.at(C1_SLAM_HIT + 25, f'kill @e[type=minecraft:marker,tag={P}]', f'kill @e[type=minecraft:marker,tag={E}]', g.end())
    tl.write([f'# C1 일점 상쇄 (clip bomb_run, then slam at {C1_SLAM}; @s = body, at it): route locked at 0, bombs '
              f'{C1_BOMBS[0]}..{C1_BOMBS[-1]} (hits +{C1_FALL}), slam r 5 at {C1_SLAM_HIT}.'],
             ['# bomb tick.'],
             extra_tick=[f'execute as @e[type=minecraft:item_display,tag={B}] at @s run function {NS}p/{key}/bomb'])
    g.pw(key, 'vis', [
        '# @s = the slam hazard (#hzEv 1 = the impact).',
        'execute unless score #hzEv mb matches 1 run return 0',
        g.particle('explosion', '~ ~0.3 ~', (1.5, 0.1, 1.5), 0, 6),
        *g.ring_dust(GOLD_DEEP, 5.0, 24, 0.2, 1.6),
        g.sound('block.anvil.land', 1.0, 0.5), g.sound('entity.generic.explode', 0.9, 0.7)])
    g.pw(key, 'cancel', ['# Everything of C1 (the route markers, falling bombs).', 'kill @e[tag=rlk_mb_fg_p1]'])


# ---------------------------------------------------------------------------------------------
def slam(g):
    """C2 내려찍기: the player's spot is locked at 0 (inside r 16.5), the device glides over it in 10 t while the gold
    column falls (13 t), plunge, disc r 5 (height 0-2) at 17. Coefficient 1.4."""
    key, tl = 'slam', TL(g, 'slam')
    A2 = 'rlk_mb_fg_p2a'
    sel = f'@e[type=minecraft:marker,tag={A2},limit=1]'
    tl.at(0, g.lockb(), g.keep(A2), f'tag {sel} add rlk_mb_fg_pat',
          f'execute positioned as {sel} run function rlk:mboss/mv/glide {{t:10}}',
          *g.hz_opts(kb=KB['heavy'], y1=2.0, vis=21), f'execute at {sel} run ' + g.hz_disc(5.0, C2_HIT, DMG['c2']),
          g.sound('block.respawn_anchor.charge', 0.9, 0.7), g.sound('block.piston.extend', 0.8, 0.6))
    for t in range(0, 13, 2):
        tl.at(t, *column(g, sel))
    tl.at(13, g.sound('block.piston.contract', 1.0, 0.5))
    tl.at(clip_len('slam'), f'kill {sel}', g.end())
    tl.write([f'# C2 내려찍기 (clip slam; @s = body): lock + glide 10 t, slam r 5 at {C2_HIT}.'], ['# slam tick.'])
    g.pw(key, 'vis', [
        '# @s = the slam hazard (#hzEv 1 = the impact).',
        'execute unless score #hzEv mb matches 1 run return 0',
        g.particle('explosion', '~ ~0.3 ~', (1.5, 0.1, 1.5), 0, 6),
        *g.ring_dust(GOLD_DEEP, 5.0, 24, 0.2, 1.6),
        g.sound('block.anvil.land', 1.0, 0.5), g.sound('entity.generic.explode', 0.9, 0.7)])
    g.pw(key, 'cancel', ['# The locked point.', 'kill @e[tag=rlk_mb_fg_p2a]'])


# ---------------------------------------------------------------------------------------------
def laser(g):
    """C3 코어: two line hazards from r 2.8 to r 5.8 along yaw and yaw + 180 (made at 0, tell 24 = the pods' drop and
    the spark charge), active 133 t, one volley group re-armed every 10 t (at most one hit per 10 t from both beams),
    height band -0.5..2 b (the beam slopes to the floor there); every tick from 25 the module re-aims them (hz/aim):
    beam A +5 deg/t, beam B -5 deg/t (counter-rotating, the spots meet every 36 t front and back); width 0.5 -> 1.0
    (bloom at 27) -> 0.5 (at 150). Coefficient 0.5 per touch."""
    key, tl = 'laser', TL(g, 'laser')
    A3, B3 = 'rlk_mb_fg_p3a', 'rlk_mb_fg_p3b'
    sa, sb = f'@e[type=minecraft:marker,tag={A3},limit=1]', f'@e[type=minecraft:marker,tag={B3},limit=1]'
    opts = lambda: g.hz_opts(act=C3_ACT, y0=-0.5, y1=2.0, kb=KB['light'], grp=True, rearm=10, sfx=0)
    tl.at(0, g.GRP_NEW, f'kill @e[type=minecraft:marker,tag={A3}]', f'kill @e[type=minecraft:marker,tag={B3}]',
          *opts(), f'execute rotated as @s rotated ~ 0 positioned ^ ^ ^{L.num(C3_R0)} run ' + g.hz_line(C3_LEN, 0.5, C3_FIRE, DMG['c3']),
          g.tag_last_hz(A3),
          *opts(), f'execute rotated as @s rotated ~180 0 positioned ^ ^ ^{L.num(C3_R0)} run ' + g.hz_line(C3_LEN, 0.5, C3_FIRE, DMG['c3']),
          g.tag_last_hz(B3),
          g.sound('block.piston.extend', 0.8, 0.8), g.sound('block.chain.place', 0.8, 1.0))
    for t in range(4, C3_FIRE - 1, 2):
        tl.at(t, f'execute at @s rotated as @s run ' + g.particle('electric_spark', '^2.8 ^2.2 ^', (0.2, 0.2, 0.2), 0.05, 3),
              f'execute at @s rotated as @s run ' + g.particle('electric_spark', '^-2.8 ^2.2 ^', (0.2, 0.2, 0.2), 0.05, 3))
    tl.at(4, g.sound('block.beacon.power_select', 0.7, 1.8))
    tl.at(C3_FIRE - 2, g.sound('block.respawn_anchor.charge', 0.7, 1.6))
    tl.at(C3_FIRE, g.sound('block.beacon.activate', 1.0, 1.8), g.sound('block.respawn_anchor.set_spawn', 0.6, 1.4))
    tl.at(C3_FIRE + 3, f'execute as {sa} run ' + g.hz_resize(C3_LEN, 0, 1.0), f'execute as {sb} run ' + g.hz_resize(C3_LEN, 0, 1.0))
    tl.at(C3_FIRE + C3_ACT - 7, f'execute as {sa} run ' + g.hz_resize(C3_LEN, 0, 0.5), f'execute as {sb} run ' + g.hz_resize(C3_LEN, 0, 0.5))
    for t in range(C3_FIRE, C3_FIRE + C3_ACT, 10):
        tl.at(t, g.sound('block.beacon.ambient', 1.0, 1.8))
    tl.at(C3_FIRE + C3_ACT, g.sound('block.beacon.deactivate', 0.8, 1.6))
    tl.at(clip_len('laser'), f'kill @e[type=minecraft:marker,tag={A3}]', f'kill @e[type=minecraft:marker,tag={B3}]', g.end())
    g.pw(key, 'aim', [
        f'# Clock {C3_FIRE + 1}..{C3_FIRE + C3_ACT - 1} (@s = body): beam A turns +5, beam B -5 degrees; the beam particles every 2 t.',
        f'execute as {sa} at {BODY} rotated as @s rotated ~5 0 positioned ^ ^ ^{L.num(C3_R0)} run function rlk:mboss/hz/aim',
        f'execute as {sb} at {BODY} rotated as @s rotated ~-5 0 positioned ^ ^ ^{L.num(C3_R0)} run function rlk:mboss/hz/aim',
        'scoreboard players operation #fgM mb = #fgPT mb', 'scoreboard players operation #fgM mb %= #fgK2 mb',
        f'execute if score #fgM mb matches 0 as {sa} at @s rotated as @s run function {NS}p/{key}/beam',
        f'execute if score #fgM mb matches 0 as {sb} at @s rotated as @s run function {NS}p/{key}/beam'])
    g.pw(key, 'beam', ['# @s = a beam hazard at r 2.8, rotated along it: the gold beam from the emitter (2.2 b up) to the floor spot.']
         + [g.dust(GOLD, 1.3, f'^ ^{L.num(2.2 * (1 - f), 2)} ^{L.num(3.0 * f, 2)}', (0.05, 0.05, 0.05), 1) for f in (0.0, 0.25, 0.5, 0.75, 1.0)]
         + [g.particle('electric_spark', '^ ^0.1 ^3', (0.3, 0.05, 0.3), 0.02, 2)])
    tl.write([f'# C3 코어 (clip laser; @s = body): two beams made at 0 (tell {C3_FIRE}), active {C3_ACT} t, counter-rotating 5 deg/t.'],
             ['# laser tick.'],
             extra_tick=[f'execute if score #fgPT mb matches {C3_FIRE + 1}..{C3_FIRE + C3_ACT - 1} run function {NS}p/{key}/aim'])
    g.pw(key, 'cancel', ['# Both beams.', f'kill @e[type=minecraft:marker,tag={A3}]', f'kill @e[type=minecraft:marker,tag={B3}]'])


# ---------------------------------------------------------------------------------------------
def missile(g):
    """C4 바위 폭탄 (far band only): tip flares 8 t + vent shaft 13 t, 10 drill missiles launched over 14 t; each rises
    out of view (apex 15 b, 7 t), locks the player's feet at its turnover (inside the walk disc: the decal hz/disc r 1.5,
    tell 13) and dives onto it with one interpolated teleport (12 t): the impacts lag a running player and land on a
    standing one (the plan's weak homing). Two volley groups (missiles 1-5, 6-10): at most 2 hits. Coefficient 0.9."""
    key, tl = 'missile', TL(g, 'missile')
    M = 'rlk_mb_fg_p4m'
    tags = '"rlk_room","rlk_mb_aux","rlk_mb_fg_pat","rlk_mb_fg_p4"'
    for i, t in enumerate(C4_T):
        side = 1.2 if i % 2 else -1.2
        lines = [g.GRP_NEW] if i in (0, 5) else []
        lines += [f'execute at @s rotated as @s positioned ^{L.num(side)} ^4.6 ^ run summon minecraft:item_display ~ ~ ~ '
                  f'{{Tags:[{tags},"{M}","rlk_mb_fg_pnew"],Rotation:[{36 * i}.0f,0.0f],teleport_duration:7,billboard:"fixed",'
                  'brightness:{block:15,sky:15},item:{id:"minecraft:pointed_dripstone",count:1},'
                  'transformation:{translation:[0f,0f,0f],left_rotation:[1f,0f,0f,0f],right_rotation:[0f,0f,0f,1f],scale:[1.2f,1.6f,1.2f]}}',
                  'scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbT 0',
                  'scoreboard players operation @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] mbS = #mbGrp mb',
                  'tag @e[type=minecraft:item_display,tag=rlk_mb_fg_pnew] remove rlk_mb_fg_pnew',
                  g.sound('entity.breeze.shoot', 0.7, 1.2)]
        tl.at(t, *lines)
    g.pw(key, 'age', [
        '# @s = a missile, at it: rise (1), turnover lock + decal + dive (7), impact (20).',
        'scoreboard players add @s mbT 1',
        'execute if score @s mbT matches 1 rotated as @s run tp @s ^ ^11 ^3',
        f'execute if score @s mbT matches {C4_LOCK} run function {NS}p/{key}/lock',
        f'execute if score @s mbT matches {C4_HIT}.. run function {NS}p/{key}/impact'])
    g.pw(key, 'lock', [
        '# @s = a missile at its apex: the late lock under the player (walk disc), its decal (tell 13), the dive.',
        g.lockp(),
        'scoreboard players operation #hzGrp mb = @s mbS',
        *g.hz_opts(kb=KB['default'], vis=41),
        'execute at @e[type=minecraft:marker,tag=rlk_mb_fg_lock,limit=1] run ' + g.hz_disc(1.5, C4_HIT - C4_LOCK, DMG['c4']),
        f'data merge entity @s {{teleport_duration:{C4_HIT - C4_LOCK - 1}}}',
        'execute at @e[type=minecraft:marker,tag=rlk_mb_fg_lock,limit=1] run tp @s ~ ~0.6 ~',
        'kill @e[type=minecraft:marker,tag=rlk_mb_fg_lock]',
        g.sound('entity.breeze.wind_burst', 0.4, 1.6)])
    g.pw(key, 'impact', [g.particle('explosion', '~ ~ ~', (0.2, 0.1, 0.2), 0, 1),
                         g.dust(GOLD_DEEP, 1.3, '~ ~0.2 ~', (0.6, 0.1, 0.6), 6),
                         g.sound('entity.generic.explode', 0.5, 1.3), 'kill @s'])
    tl.at(0, face(g), g.sound('block.beacon.power_select', 0.8, 1.4))
    for t in range(0, ev_or('missiles', 'vent', 8), 2):
        tl.at(t, f'execute at @s rotated as @s run ' + g.particle('end_rod', '^3.6 ^4.6 ^', (0.1, 0.1, 0.1), 0.02, 2),
              f'execute at @s rotated as @s run ' + g.particle('end_rod', '^-3.6 ^4.6 ^', (0.1, 0.1, 0.1), 0.02, 2))
    for t in range(ev_or('missiles', 'vent', 8), C4_LAUNCH, 2):
        tl.at(t, 'execute at @s run ' + g.dust(GOLD, 1.5, '~ ~6 ~', (0.3, 1.5, 0.3), 6))
    tl.at(ev_or('missiles', 'vent', 8), g.sound('block.respawn_anchor.charge', 0.8, 1.2), g.sound('block.vault.activate', 0.7, 1.0))
    tl.at(clip_len('missiles'), g.end())
    tl.write([f'# C4 바위 폭탄 (clip missiles; @s = body): launches {C4_T}, lock +{C4_LOCK}, impact +{C4_HIT}.'], ['# missile tick.'],
             extra_tick=[f'execute as @e[type=minecraft:item_display,tag={M}] at @s run function {NS}p/{key}/age'])
    g.pw(key, 'vis', ['# @s = a missile decal (#hzEv 1 = its impact).', 'execute unless score #hzEv mb matches 1 run return 0',
                      g.particle('block{block_state:"minecraft:gold_block"}', '~ ~0.2 ~', (0.5, 0.1, 0.5), 0, 8)])
    g.pw(key, 'cancel', ['# Every missile.', 'kill @e[tag=rlk_mb_fg_p4]'])


# ---------------------------------------------------------------------------------------------
def burst(g):
    """C5 지면 충격: the core flips up (spark 0, flash + lift 5), the rim decal at R 12 from 3 (hz/disc r 12, tell 45:
    the framework draws the rim and the growing fill), the up-beam 29-40, the column down 41-44, ONE full-area blast
    at 48 with a low hit band (#hzY1 0.5: a jump clears it; dash i-frames work: the default). Leave the disc, jump or
    dash. Coefficient 2.2, heavy knockback."""
    key, tl = 'burst', TL(g, 'burst')
    tl.at(0, g.sound('block.respawn_anchor.charge', 0.8, 1.4), 'execute at @s run ' + g.particle('electric_spark', '~ ~4.6 ~', (0.3, 0.2, 0.3), 0.1, 8))
    tl.at(C5_RIM, *g.hz_opts(kb=KB['heavy'], y1=0.5, vis=51), g.hz_disc(12.0, C5_BLAST - C5_RIM, DMG['c5']),
          g.sound('block.beacon.power_select', 0.9, 0.8))
    tl.at(5, 'execute at @s run ' + g.particle('flash{color:[0.98,0.87,0.66,1.0]}', '~ ~6 ~', (0, 0, 0), 0, 1), g.sound('block.amethyst_block.resonate', 1.0, 1.2))
    for t in range(29, 41, 2):
        tl.at(t, 'execute at @s run ' + g.dust(GOLD, 1.6, '~ ~9 ~', (0.15, 2.0, 0.15), 6))
    tl.at(29, g.sound('block.beacon.activate', 0.9, 1.2))
    for t in range(41, C5_BLAST, 1):
        tl.at(t, *column(g, '@s', 7.0))
    tl.at(41, g.sound('block.respawn_anchor.deplete', 0.9, 0.8))
    tl.at(clip_len('coreup'), g.end())
    tl.write([f'# C5 지면 충격 (clip coreup; @s = body): disc r 12 made at {C5_RIM}, blast at {C5_BLAST}.'], ['# burst tick.'])
    g.pw(key, 'vis', ['# @s = the blast hazard (#hzEv 1 = the blast).', 'execute unless score #hzEv mb matches 1 run return 0',
                      g.particle('explosion_emitter', '~ ~0.5 ~', (0, 0, 0), 0, 1),
                      *g.ring_dust(GOLD_DEEP, 12.0, 40, 0.3, 2.0), *g.ring_dust(WHITE_GOLD, 6.0, 20, 0.3, 1.6),
                      g.sound('entity.generic.explode', 1.2, 0.6), g.sound('block.anvil.land', 0.8, 0.5)])
    g.pw(key, 'cancel', ['# Nothing of its own lingers.'])


# ---------------------------------------------------------------------------------------------
def rock(g):
    """C6 파쇄: dip and roll toward the player 12 t, vent flare + medallions flung up 8 t, tower 18 t, flame-band
    charge 17 t (the long tell), then api.rocks(): 8 floor bursts 6 t apart walking onto the player (r 1.8, tell 10,
    jumpable, coefficient 1.3, heavy knockback), the lifted slabs, 5 throws 8 t apart (blade pj 1.5 b/t, 1.1),
    revert 15 t."""
    key, tl = 'rock', TL(g, 'rock')
    tl.at(0, face(g), g.sound('block.piston.extend', 0.8, 0.5))
    tl.at(12, g.sound('block.respawn_anchor.charge', 0.8, 0.9), 'execute at @s run ' + g.particle('flame', '~ ~5 ~', (0.6, 0.3, 0.6), 0.02, 10))
    tl.at(20, g.sound('block.chain.place', 1.0, 0.6), g.sound('block.piston.contract', 0.9, 0.6))
    for t in range(38, C6_BURST, 2):
        tl.at(t, *['execute at @s run ' + x for x in g.ring_dust(AMBER, 3.0, 12, 1.0, 1.3)])
    tl.at(38, g.sound('block.fire.ambient', 1.0, 0.7), g.sound('block.blastfurnace.fire_crackle', 1.0, 0.8))
    done = rocks(g, tl, key, 6, C6_BURST, throw0=C6_THROW, dmg=DMG['c6'], dmg_s=DMG['c6s'])
    assert done <= clip_len('tower_throw'), done
    tl.at(clip_len('tower_throw'), *rocks_cancel(6), g.end())
    tl.write([f'# C6 파쇄 (clip tower_throw; @s = body): bursts from {C6_BURST}, throws from {C6_THROW}.'], ['# rock tick.'],
             extra_tick=[f'function {NS}p/{key}/slabs'])
    g.pw(key, 'vis', ['# @s = a floor burst (#hzEv 1 = it strikes).', 'execute unless score #hzEv mb matches 1 run return 0',
                      g.particle('block{block_state:"minecraft:tuff"}', '~ ~0.3 ~', (0.8, 0.3, 0.8), 0, 14),
                      g.particle('flame', '~ ~0.4 ~', (0.6, 0.2, 0.6), 0.03, 6),
                      g.sound('block.tuff.break', 1.2, 0.5), g.sound('entity.generic.explode', 0.6, 1.1)])
    g.pw(key, 'cancel', ['# Walker, slabs, locks.'] + rocks_cancel(6) + ['kill @e[type=minecraft:marker,tag=rlk_mb_fg_kept]'])
