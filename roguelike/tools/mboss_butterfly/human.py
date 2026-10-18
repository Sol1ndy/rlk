"""Human-form patterns of the butterfly: H1 달빛 발차기, H2 달빛 점프, H3 달빛 돌진, H4 광폭한 진공.

STUBS (stage 1, the core author): the plan.md timelines, the hit areas with their telegraphs (>= 10 t), the damage
coefficients, the elements and the body travel, so the fight is playable end to end. The real fx (crescent
cards, trails, kick waves), the telegraph decals and the composed vanilla sounds belong to the human-pattern
author (stage 2; see the scratchpad file mb2/bf_contract.md): replace the bodies below, keep the ids, keys, clips
and hit ticks (or update the timing test with them).

Clock: #bfPT = the clip tick (the core plays the clip at clock 0); a pattern with lead L starts at -L.
"""
from . import api as A
from .api import Pattern, TL, ev_or, clip_len, DMG, KB, CY

TELL = 10                                     # telegraph floor (plan.md: every damaging hit >= 10 t)
K_KICK, K_JUMP, K_DASH, K_VAC = 'kick', 'jump', 'dash', 'vacuum'
L_KICK, L_JUMP, L_DASH, L_VAC = (clip_len(c) for c in ('kick_combo', 'kick_jump', 'dash_kick', 'vacuum'))
H1_HIT1, H1_HIT2 = ev_or('kick_combo', 'hit1', 8), ev_or('kick_combo', 'hit2', 40)
H2_SWEEP, H2_SWEEP_END = ev_or('kick_jump', 'sweep', 13), ev_or('kick_jump', 'sweep_end', 19)
H2_JUMP, H2_DISC = ev_or('kick_jump', 'jump', 33), ev_or('kick_jump', 'disc', 40)
H2_IMPACT, H2_LAND = ev_or('kick_jump', 'impact', H2_DISC + 10), ev_or('kick_jump', 'land', 55)
H3_DASH, H3_DASH_END, H3_KICK = ev_or('dash_kick', 'dash', 10), ev_or('dash_kick', 'dash_end', 12), ev_or('dash_kick', 'kick', 15)
H4_BLADE = ev_or('vacuum', 'blade', 17)
H4_LAND = ev_or('vacuum', 'land', 38)
H1_LEAD = max(0, TELL - H1_HIT1)              # hit 1 lands 8 t into the clip: its telegraph starts 2 t before the clip

PATTERNS = [
    Pattern(1, K_KICK, '달빛 발차기', 'h', 'kick_combo', bands=('melee', 'mid'), weight={'melee': 2}, lead=H1_LEAD,
            recover=16, max_len=L_KICK + 5, length=L_KICK),
    Pattern(2, K_JUMP, '달빛 점프', 'h', 'kick_jump', bands=('melee', 'mid'), close=3.0, recover=16,
            max_len=L_JUMP + 5, length=L_JUMP),
    Pattern(3, K_DASH, '달빛 돌진', 'h', 'dash_kick', bands=('mid', 'far'), weight={'far': 2}, recover=16,
            max_len=L_DASH + 5, length=L_DASH),
    Pattern(4, K_VAC, '광폭한 진공', 'h', 'vacuum', bands=('far', 'mid'), weight={'far': 2}, recover=18,
            max_len=L_VAC + 5, length=L_VAC),
]


def on_floor(sel, face='facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0'):
    """execute prefix: at a marker, aimed at the player, on the floor."""
    return f'execute at {sel} {face} positioned ~ {CY} ~ run '


def emit(g):
    R = g.rig
    lime = A.LIME

    # ---- H1 달빛 발차기: burst-run ~4 b in 5 t, rising flip-kick crescent (front arc r 4) at 8, backflip, sideways-hop
    # wind-up, flying leap, axe-kick crescent (r 5) + ground wave line 6 x 2 at 40 (one hit for both: a volley group).
    k = K_KICK
    a, b = 'rlk_mb_bf_p1a', 'rlk_mb_bf_p1b'
    A_ = f'@e[type=minecraft:marker,tag={a},limit=1]'
    B_ = f'@e[type=minecraft:marker,tag={b},limit=1]'
    tl = TL(g, k)
    t0 = H1_HIT1 - TELL
    tl.at(t0, R('face/player'), g.dest(4.0, 1.5), g.keep(a),
          g.hz_opts(sfx=2, kb=KB['default']), on_floor(A_) + g.hz_sector(4.0, 75, TELL, DMG['h1a']))
    tl.at(0, f'execute positioned as {A_} run function rlk:mboss/mv/glide {{t:5}}',
          g.sound('entity.breeze.jump', 0.6, 1.3))
    tl.at(H1_HIT1, g.sound('entity.breeze.wind_burst', 0.6, 1.4), g.sound('block.azalea_leaves.break', 0.7, 1.0),
          g.dust(lime, 1.2, '^ ^2 ^1.5', (0.6, 1.0, 0.3), 12))
    tl.span(H1_HIT1 + 2, H1_HIT1 + 9, 'function rlk:mboss/mv/away {d:0.25}')
    t1 = H1_HIT2 - TELL
    tl.at(t1, R('face/player'), g.dest(3.0, 1.0), g.keep(b), g.GRP_NEW,
          g.hz_opts(sfx=2, kb=KB['default'], grp=True), on_floor(B_) + g.hz_sector(5.0, 90, TELL, DMG['h1b']),
          g.hz_opts(sfx=0, kb=KB['default'], grp=True), on_floor(B_) + g.hz_line(6.0, 2.0, TELL, DMG['h1b']))
    tl.at(H1_HIT2 - 6, f'execute positioned as {B_} run function rlk:mboss/mv/glide {{t:5}}')
    tl.at(H1_HIT2, g.sound('entity.player.attack.sweep', 0.8, 0.8), g.sound('entity.breeze.wind_burst', 0.7, 1.0),
          g.dust(lime, 1.4, '^ ^0.3 ^3', (0.8, 0.2, 2.5), 18))
    tl.at(L_KICK, g.end())
    tl.write([f'# H1 달빛 발차기 (STUB; lead {H1_LEAD}: start at clock {t0}, clip kick_combo at 0, hits {H1_HIT1} / {H1_HIT2}).'],
             ['# H1 tick.'], t0=t0)
    g.pw(k, 'cancel', [f'kill @e[type=minecraft:marker,tag={a}]', f'kill @e[type=minecraft:marker,tag={b}]'])

    # ---- H2 달빛 점프: arm-shard glow tell (13 t), 360 low sweep r 3 at 13-19, spiral jump toward the player at 33,
    # Dendro disc kicked onto the player position locked at 40, impact 50, r 2.5.
    k = K_JUMP
    a, b = 'rlk_mb_bf_p2a', 'rlk_mb_bf_p2b'
    A_ = f'@e[type=minecraft:marker,tag={a},limit=1]'
    B_ = f'@e[type=minecraft:marker,tag={b},limit=1]'
    tl = TL(g, k)
    tl.at(0, R('face/player'), g.sound('block.amethyst_block.chime', 0.7, 1.6), g.sound('block.beacon.ambient', 0.4, 1.8))
    tl.at(H2_SWEEP - TELL, g.hz_opts(act=H2_SWEEP_END - H2_SWEEP, sfx=2, kb=KB['default']),
          f'execute positioned ~ {CY} ~ run ' + g.hz_disc(3.0, TELL, DMG['h2a']))
    tl.at(H2_SWEEP, g.sound('entity.player.attack.sweep', 0.7, 1.1), g.sound('entity.breeze.whirl', 0.5, 1.4))
    tl.at(H2_JUMP, R('face/player'), g.dest(3.5, 0.8), g.keep(a),
          f'execute positioned as {A_} run function rlk:mboss/mv/glide {{t:{H2_LAND - H2_JUMP}}}',
          g.sound('entity.breeze.charge', 0.6, 1.1))
    tl.at(H2_DISC, g.lockp(), g.keep(b, 'rlk_mb_bf_lock'), g.hz_opts(sfx=1, kb=KB['heavy']),
          f'execute at {B_} run ' + g.hz_disc(2.5, H2_IMPACT - H2_DISC, DMG['h2b']),
          g.sound('block.conduit.activate', 0.4, 1.8))
    tl.at(H2_IMPACT, g.sound('entity.generic.explode', 0.4, 1.4), g.sound('block.azalea_leaves.break', 0.8, 1.0))
    tl.at(L_JUMP, g.end())
    tl.write([f'# H2 달빛 점프 (STUB; clip kick_jump: sweep {H2_SWEEP}-{H2_SWEEP_END}, jump {H2_JUMP}, disc lock {H2_DISC}, impact {H2_IMPACT}).'],
             ['# H2 tick.'])
    g.pw(k, 'cancel', [f'kill @e[type=minecraft:marker,tag={a}]', f'kill @e[type=minecraft:marker,tag={b}]'])

    # ---- H3 달빛 돌진: mote charge 10 t, dash 5-6 b in 2 t (10-12), kick + Dendro ring r 3.5 at 15.
    k = K_DASH
    a = 'rlk_mb_bf_p3a'
    A_ = f'@e[type=minecraft:marker,tag={a},limit=1]'
    tl = TL(g, k)
    tl.at(0, R('face/player'), g.sound('entity.breeze.charge', 0.6, 1.4))
    tl.span(1, H3_DASH - 1, g.dust(lime, 0.8, '~ ~1.2 ~', (0.6, 0.6, 0.6), 2))
    tl.at(H3_KICK - TELL, R('face/player'), g.dest(6.0, 1.0), g.keep(a), g.hz_opts(sfx=1, kb=KB['default']),
          f'execute at {A_} run ' + g.hz_disc(3.5, TELL, DMG['h3']))
    tl.at(H3_DASH, f'execute positioned as {A_} run function rlk:mboss/mv/glide {{t:{H3_DASH_END - H3_DASH}}}',
          g.sound('entity.breeze.jump', 0.7, 1.3))
    tl.at(H3_KICK, g.sound('entity.breeze.wind_burst', 0.8, 1.0), g.sound('block.cherry_leaves.break', 0.8, 1.0))
    tl.at(L_DASH, g.end())
    tl.write([f'# H3 달빛 돌진 (STUB; clip dash_kick: dash {H3_DASH}-{H3_DASH_END}, kick {H3_KICK}).'], ['# H3 tick.'])
    g.pw(k, 'cancel', [f'kill @e[type=minecraft:marker,tag={a}]'])

    # ---- H4 광폭한 진공: crouch, spike + glint tell, a vertical crescent blade (3 wide x 4 tall) launched at 17 along the
    # line locked at 7 (telegraph-only ground line), 0.7 b/t to the arena edge, no homing; backflip, airborne 21 t.
    k = K_VAC
    blade = 'rlk_mb_bf_p4b'
    tl = TL(g, k)
    tl.at(0, R('face/player'))
    lock = H4_BLADE - TELL
    tl.at(lock, R('face/player'),
          f'execute rotated as @s rotated ~ 0 positioned ^ ^0.9 ^1.0 run summon minecraft:item_display ~ ~ ~ '
          f'{{Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_p4","{blade}"],teleport_duration:1,brightness:{{block:15,sky:15}},'
          'item:{id:"minecraft:lime_stained_glass_pane",count:1},transformation:{translation:[0f,1.1f,0f],'
          'left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[3f,4f,0.3f]}}',
          f'execute rotated as @s rotated ~ 0 positioned ^ ^0.9 ^1.0 run tp @e[type=minecraft:item_display,tag={blade},limit=1] ~ ~ ~ ~ 0',
          f'scoreboard players set @e[type=minecraft:item_display,tag={blade}] mbId 4',
          g.hz_opts(sfx=0, col=7), f'execute rotated as @s rotated ~ 0 positioned ~ {CY} ~ run ' + g.tell_line(30.0, 3.0, TELL),
          g.sound('block.amethyst_cluster.hit', 0.7, 1.8))
    tl.at(H4_BLADE, *g.pj_opts(shape=1, kb=KB['default']),
          f'execute as @e[type=minecraft:item_display,tag={blade},limit=1] at @s run ' + g.pj_launch(0.7, 60, DMG['h4'], 1.5),
          g.sound('entity.breeze.wind_burst', 0.8, 1.0), g.sound('item.trident.riptide_2', 0.6, 1.2))
    tl.span(H4_BLADE + 1, H4_LAND, 'function rlk:mboss/mv/away {d:0.12}')
    tl.at(H4_LAND, g.sound('entity.breeze.land', 0.6, 0.9))
    tl.at(L_VAC, g.end())
    tl.write([f'# H4 광폭한 진공 (STUB; clip vacuum: line lock {lock}, blade {H4_BLADE} = a pj blade prop 0.7 b/t, backflip to {H4_LAND}).'],
             ['# H4 tick.'])
    g.pw(k, 'cancel', ['kill @e[type=minecraft:item_display,tag=rlk_mb_bf_p4]'])
