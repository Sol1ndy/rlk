"""Butterfly-form patterns: B1 우아한 날개, B2 화염 날개의 습격, B3 날개 휩쓸개, B4 달빛 축복, and the finale B5 달빛 해제
(service pattern 15: the core starts it and owns its mechanics: the caption at clock 0, the flat look, the revert to
human form, the heal orbs vanishing, the groggy after it).

STUBS (stage 1, the core author): the plan.md timelines, the hit areas with their telegraphs (>= 10 t), the damage
coefficients and elements (the core switches the wing look to Pattern.el before the start), the body travel, the
volley groups (one hit per B2 swing, per B4 orb, max 2 flame-trail touches) and the B4 homing orbs (pj/steer), so the
fight is playable end to end. The real fx (wing crescents, fire crescents, flame fan, orb sphere with gyroscope rings,
radial blades, the release's star flare / X glint / ring cage / pod / dome), the decals and the sounds belong to the
wing-pattern author (stage 2; see the scratchpad file mb2/bf_contract.md).

Clock: #bfPT = the clip tick (the core plays the clip at clock 0).
"""
from . import api as A
from .api import Pattern, TL, ev_or, clip_len, DMG, KB, CY, EL_PYRO, EL_DENDRO

TELL = 10
K_STRIKE, K_BARRAGE, K_SWEEP, K_COCO, K_RELEASE = 'strike', 'barrage', 'sweep', 'coco', 'release'
L_STRIKE, L_BARRAGE, L_SWEEP, L_COCO, L_RELEASE = (clip_len(c) for c in ('wing_strike', 'wing_barrage', 'flap_dive', 'coco', 'release'))
B1_DIVE, B1_HIT = ev_or('wing_strike', 'dive', 12), ev_or('wing_strike', 'hit', 15)
B2_SWINGS = [ev_or('wing_barrage', f'swing{i}', d) for i, d in enumerate((0, 26, 64, 89), 1)]
B2_DIVE = (14, 15, 16, 17, 18)                # the five crescents of a swing land 14-18 t after it
B3_DIVE, B3_SLAM, B3_GLIDE = ev_or('flap_dive', 'dive', 22), ev_or('flap_dive', 'slam', 26), ev_or('flap_dive', 'glide', 34)
B3_FAN = (B3_SLAM + 2, 5)                     # flame fan active 28-32
B3_TRAIL = [B3_GLIDE + 3 * i for i in range(5)]
B4_ORBS = (ev_or('coco', 'orb1', 19), ev_or('coco', 'orb2', 46))
B4_STEER, B4_LIFE = 40, 50                    # homing for 40 t, burst (radial blades) at 50
B4_END = max(L_COCO, B4_ORBS[-1] + B4_LIFE + 2)
B5_DET = ev_or('release', 'detonation', 53)
B5_TELL = 15                                  # the ring cage at E-15 starts the dome's telegraph

PATTERNS = [
    Pattern(11, K_STRIKE, '우아한 날개', 'b', 'wing_strike', bands=('melee', 'mid', 'far'), el=EL_DENDRO, recover=18,
            max_len=L_STRIKE + 5, length=L_STRIKE),
    Pattern(12, K_BARRAGE, '화염 날개의 습격', 'b', 'wing_barrage', bands=('mid', 'far'), weight={'far': 2}, el=EL_PYRO,
            recover=20, max_len=L_BARRAGE + 5, length=L_BARRAGE),
    Pattern(13, K_SWEEP, '날개 휩쓸개', 'b', 'flap_dive', bands=('melee', 'mid', 'far'), weight={'mid': 2}, el=EL_PYRO,
            recover=18, max_len=L_SWEEP + 5, length=L_SWEEP),
    Pattern(14, K_COCO, '달빛 축복', 'b', 'coco', bands=('mid', 'far'), el=EL_DENDRO, recover=20,
            max_len=B4_END + 4, length=B4_END),
    Pattern(15, K_RELEASE, '달빛 해제', 'b', 'release', kind='service', el=EL_DENDRO, recover=0,
            max_len=L_RELEASE + 4, length=L_RELEASE),
]


def on_floor(sel, face='facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0'):
    return f'execute at {sel} {face} positioned ~ {CY} ~ run '


def emit(g):
    R = g.rig

    # ---- B1 우아한 날개 / 날개 치기 (Dendro): bank 8 t, dive 3 t, wing-arc hit at 15 (front arc r 4) + a ground slash
    # band (one hit for both), climb / flutter recovery.
    k = K_STRIKE
    a = 'rlk_mb_bf_p11a'
    A_ = f'@e[type=minecraft:marker,tag={a},limit=1]'
    tl = TL(g, k)
    tl.at(0, R('face/player'), g.sound('entity.ender_dragon.flap', 0.5, 1.8))
    tl.at(B1_HIT - TELL, R('face/player'), g.dest(6.0, 1.5), g.keep(a), g.GRP_NEW,
          g.hz_opts(sfx=2, kb=KB['default'], grp=True), on_floor(A_) + g.hz_sector(4.0, 80, TELL, DMG['b1']),
          g.hz_opts(sfx=0, kb=KB['default'], back=2.0, grp=True), on_floor(A_) + g.hz_line(4.0, 2.0, TELL, DMG['b1']))
    tl.at(B1_DIVE - 3, f'execute positioned as {A_} run function rlk:mboss/mv/glide {{t:{B1_HIT - B1_DIVE + 3}}}',
          g.sound('entity.phantom.swoop', 0.6, 1.3))
    tl.at(B1_HIT, g.sound('entity.player.attack.sweep', 0.8, 0.8), g.sound('block.cherry_leaves.break', 0.7, 1.0),
          g.dust(A.LIME, 1.3, '^ ^1.5 ^1.5', (1.5, 0.6, 0.6), 16))
    tl.span(B1_HIT + 5, B1_HIT + 20, 'function rlk:mboss/mv/away {d:0.15}')
    tl.at(L_STRIKE, g.end())
    tl.write([f'# B1 우아한 날개 (STUB; clip wing_strike: dive {B1_DIVE}, hit {B1_HIT}).'], ['# B1 tick.'])
    g.pw(k, 'cancel', [f'kill @e[type=minecraft:marker,tag={a}]'])

    # ---- B2 화염 날개의 습격 / 날개탄 (Pyro): 4 spinning wing swings; each throws 5 fire crescents that fan out and dive onto
    # the player position 14-18 t later (1 b splash each, a ground marker); one hit per swing at most (volley group).
    k = K_BARRAGE
    lk = 'rlk_mb_bf_p12l'
    L_ = f'@e[type=minecraft:marker,tag={lk},limit=1]'
    tl = TL(g, k)
    for s in B2_SWINGS:
        lines = [R('face/player'), g.lockp(), f'kill @e[type=minecraft:marker,tag={lk}]', g.keep(lk, 'rlk_mb_bf_lock'), g.GRP_NEW,
                 g.particle('flame', '^ ^3.0 ^', (1.8, 0.8, 0.5), 0.04, 14), g.sound('entity.ender_dragon.flap', 0.6, 1.6),
                 g.sound('item.firecharge.use', 0.6, 1.2)]
        for i, d in enumerate(B2_DIVE):
            off = (i - 2) * 1.1
            lines += g.hz_opts(el=EL_PYRO, kb=KB['light'], sfx=0, grp=True)
            lines.append(f'execute at {L_} facing entity @s feet rotated ~ 0 positioned ^{A.L.num(off)} ^ ^ positioned ~ {CY} ~ run '
                         + g.hz_disc(1.0, d, DMG['b2']))
        tl.at(s, *lines)
        tl.at(s + B2_DIVE[0], g.sound('entity.blaze.shoot', 0.5, 1.2))
    tl.at(L_BARRAGE, g.end())
    tl.write([f'# B2 화염 날개의 습격 (STUB; clip wing_barrage: swings {B2_SWINGS}, 5 crescents each landing +{B2_DIVE[0]}..+{B2_DIVE[-1]}).'],
             ['# B2 tick.'])
    g.pw(k, 'cancel', [f'kill @e[type=minecraft:marker,tag={lk}]'])

    # ---- B3 날개 휩쓸개 / 날갯짓 (Pyro): 2 flaps and a rise (20 t), head-first dive (4 t), wing slam at 26, 180 degree front
    # flame fan (r 4.5, 2.5 tall) active 28-32, then a low glide leaving a flame trail (0.3 per touch, max 2).
    k = K_SWEEP
    a = 'rlk_mb_bf_p13a'
    A_ = f'@e[type=minecraft:marker,tag={a},limit=1]'
    tl = TL(g, k)
    tl.at(0, R('face/player'), g.sound('entity.ender_dragon.flap', 0.7, 1.4))
    tl.at(10, g.sound('entity.ender_dragon.flap', 0.7, 1.3))
    fan0, fan_act = B3_FAN
    tl.at(fan0 - 12, R('face/player'), g.dest(5.0, 2.0), g.keep(a),
          g.hz_opts(el=EL_PYRO, act=fan_act, y1=2.5, sfx=4, kb=KB['default']), on_floor(A_) + g.hz_sector(4.5, 90, 12, DMG['b3']))
    tl.at(B3_DIVE, f'execute positioned as {A_} run function rlk:mboss/mv/glide {{t:{B3_SLAM - B3_DIVE}}}',
          g.sound('entity.phantom.swoop', 0.7, 1.2))
    tl.at(B3_SLAM, g.sound('entity.blaze.shoot', 0.8, 0.8), g.sound('item.firecharge.use', 0.8, 0.9))
    tl.span(B3_GLIDE, B3_TRAIL[-1], 'function rlk:mboss/mv/step {d:0.3}')
    for i, t in enumerate(B3_TRAIL):
        lines = []
        if i in (0, 3):
            lines.append(g.GRP_NEW)        # two groups: at most 2 touches of the trail
        lines += g.hz_opts(el=EL_PYRO, kb=KB['none'], sfx=0, grp=True)
        lines.append(f'execute positioned ~ {CY} ~ run ' + g.hz_disc(1.0, TELL, DMG['b3t']))
        lines.append(g.particle('flame', '~ ~0.3 ~', (0.4, 0.1, 0.4), 0.01, 6))
        tl.at(t, *lines)
    tl.at(L_SWEEP, g.end())
    tl.write([f'# B3 날개 휩쓸개 (STUB; clip flap_dive: dive {B3_DIVE}, slam {B3_SLAM}, fan {fan0}-{fan0 + fan_act - 1}, trail {B3_TRAIL}).'],
             ['# B3 tick.'])
    g.pw(k, 'cancel', [f'kill @e[type=minecraft:marker,tag={a}]'])

    # ---- B4 달빛 축복 / 2단 코코볼 (Dendro): two slow, strongly homing orbs (19 and 46): they steer toward the player for 40 t,
    # then burst with radial ground blades r 2.8 (telegraphed 10 t); a dash dodges them; one hit per orb (contact or burst).
    k = K_COCO
    orb = 'rlk_mb_bf_p14o'
    new = 'rlk_mb_bf_p14n'
    tl = TL(g, k)
    tl.at(0, R('face/player'), g.sound('block.amethyst_block.resonate', 0.6, 1.2))
    for t in B4_ORBS:
        tl.at(t, R('face/player'), g.fn(f'p/{k}/orb_new'))
    tl.at(B4_END, g.end())
    tl.write([f'# B4 달빛 축복 (STUB; clip coco: orbs at {B4_ORBS}, homing {B4_STEER} t, burst at +{B4_LIFE}; end {B4_END}).'],
             ['# B4 tick: the orbs steer (they are pj props; the module tick runs before pj/all).',
              f'execute if entity @e[type=minecraft:item_display,tag={orb},limit=1] as @e[type=minecraft:item_display,tag={orb}] at @s run {g.fn(f"p/{k}/orb")}'])
    g.pw(k, 'orb_new', [
        '# @s = body: a lime orb (1.7 b) at her chest, aimed at the player, launched slow (0.35 b/t) as a pj prop in its own group.',
        f'execute rotated as @s rotated ~ 0 positioned ^ ^2.2 ^1.2 run summon minecraft:item_display ~ ~ ~ '
        f'{{Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p14","{orb}","{new}"],teleport_duration:1,billboard:"center",Glowing:1b,'
        f'glow_color_override:{int(A.LIME_HEX[1:], 16)},brightness:{{block:15,sky:15}},item:{{id:"minecraft:slime_ball",count:1}},'
        'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.7f,1.7f,1.7f]}}',
        f'execute as @e[type=minecraft:item_display,tag={new},limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ ~',
        f'scoreboard players set @e[type=minecraft:item_display,tag={new}] mbId 14',
        f'scoreboard players set @e[type=minecraft:item_display,tag={new}] mbT 0',
        g.GRP_NEW,
        *g.pj_opts(el=EL_DENDRO, kb=KB['light'], grp=True),
        f'execute as @e[type=minecraft:item_display,tag={new},limit=1] at @s run ' + g.pj_launch(0.35, B4_LIFE, DMG['b4'], 0.8),
        f'tag @e[type=minecraft:item_display,tag={new}] remove {new}',
        g.sound('block.conduit.activate', 0.5, 1.6), g.sound('entity.breeze.shoot', 0.5, 1.2)])
    g.pw(k, 'orb', [
        f'# @s = an orb, at it: homing for {B4_STEER} t (9 deg/t), then it slows over the burst decal locked under it.',
        'scoreboard players add @s mbT 1',
        f'execute if score @s mbT matches 1..{B4_STEER} run ' + g.pj_steer(9),
        f'execute if score @s mbT matches {B4_STEER} run {g.fn(f"p/{k}/burst_tell")}',
        'scoreboard players operation #bfM mb = @s mbT', 'scoreboard players operation #bfM mb %= #bfK3 mb',
        'execute if score #bfM mb matches 0 run ' + g.dust(A.LIME_PALE, 1.0, '~ ~ ~', (0.4, 0.4, 0.4), 3)])
    g.pw(k, 'burst_tell', [
        '# @s = orb at the end of its homing: radial blades r 2.8 under it in 10 t, same group as the orb (one hit).',
        'scoreboard players set @s mbPjV 1',
        *g.hz_opts(el=EL_DENDRO, kb=KB['default'], sfx=1),
        'scoreboard players operation #hzGrp mb = @s mbPjG',
        f'execute positioned ~ {CY} ~ run ' + g.hz_disc(2.8, B4_LIFE - B4_STEER, DMG['b4'])])
    g.pw(k, 'pj_end', [
        '# An orb event (@s = orb): a hit pops it at once; its life end (or a wall) bursts it.',
        'execute if score #pjEv mb matches 4 run scoreboard players set #pjKeep mb 0',
        g.dust(A.LIME, 1.6, '~ ~ ~', (0.8, 0.8, 0.8), 18), g.particle('end_rod', '~ ~ ~', (0.3, 0.3, 0.3), 0.1, 8),
        g.sound('block.amethyst_cluster.break', 0.6, 1.4)])
    g.pw(k, 'cancel', ['kill @e[type=minecraft:item_display,tag=rlk_mb_bf_p14]'])

    # ---- B5 달빛 해제 / 강화 해제 (Dendro, service 15): wings fold, a swoop past the player, climb, whirl with a lime star
    # flare, wings cup forward, ground flash, cyan X glint, ring cage (E-15..-10: the dome's telegraph), the pod, the
    # detonation E: a white flash and a lime dome r 10 (dodge: farther than 10 b, or a dash at E). The core: caption at
    # 0, wings flat lime at its flat event, human form at its revert event, then the groggy.
    k = K_RELEASE
    a, b = 'rlk_mb_bf_p15a', 'rlk_mb_bf_p15b'
    A_ = f'@e[type=minecraft:marker,tag={a},limit=1]'
    B_ = f'@e[type=minecraft:marker,tag={b},limit=1]'
    tl = TL(g, k)
    tl.at(0, R('face/player'), g.lockp(), g.keep(a, 'rlk_mb_bf_lock'),
          f'execute at {A_} facing entity @s feet rotated ~180 0 positioned ^ ^ ^3 run summon minecraft:marker ~ ~ ~ '
          f'{{Tags:["rlk_room","rlk_mb_aux","{b}"]}}',
          f'execute as {B_} run function rlk:mboss/mv/clamp',
          f'execute positioned as {B_} run function rlk:mboss/mv/glide {{t:14}}',
          g.sound('entity.phantom.swoop', 0.6, 1.3))
    tl.at(28, g.sound('entity.breeze.whirl', 0.6, 1.3))
    tl.at(B5_DET - B5_TELL, g.hz_opts(sfx=4, kb=KB['heavy']), f'execute positioned ~ {CY} ~ run ' + g.hz_disc(10.0, B5_TELL, DMG['b5']),
          g.sound('block.beacon.power_select', 0.8, 1.4))
    tl.at(B5_DET - 9, g.sound('block.respawn_anchor.charge', 0.7, 1.2))
    tl.at(B5_DET - 4, g.sound('entity.warden.sonic_charge', 0.5, 1.6))
    tl.at(B5_DET, g.sound('entity.generic.explode', 1.0, 0.8), g.sound('entity.warden.sonic_boom', 0.6, 1.4),
          g.dust(A.LIME, 2.0, '~ ~2 ~', (3.0, 1.5, 3.0), 40))
    tl.at(L_RELEASE, g.end())
    tl.write([f'# B5 달빛 해제 (STUB; clip release: dome telegraph {B5_DET - B5_TELL}, detonation {B5_DET}).'], ['# B5 tick.'])
    g.pw(k, 'cancel', [f'kill @e[type=minecraft:marker,tag={a}]', f'kill @e[type=minecraft:marker,tag={b}]'])
