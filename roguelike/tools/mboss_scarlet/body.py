"""Round X (lane XB; tools/dev/plan/combat/x_brief.md rulings 1-2): the body rule of 홍련's fight, her side.

Her body and the player's avatar (@e[tag=rlk_body]: the mannequin of the F5 / shoulder view, the player in first person) are
never closer than api.BODY['rule'] b centre to centre on the floor plane while she is fought. The investigation (x_brief causes
1-2): her stop points were chosen from where the player WAS (the lock 7 t before the hit, the stations 10-14 t before the cut)
and nothing looked at the live body; core/cam_ok measured from the camera rider's eyes 2.36 b over the avatar's feet; nothing
separated the bodies (the avatar is a vehicle: vanilla push never moves it; her husk is NoAI, every move of hers a scripted tp).

Written by the S3 Writer (core/**), run at the end of every fight tick (core/fight -> core/body while #ph is P1 / P2 / G1 / G2):
- core/guard (one shared helper for every arrival: dash-throughs, dives, MX's streak, Q's and TRI's lunges, the gauntlet glides
  and stations, the G1 / G2 dives, `land`, cam_clear's step, the recovery): while she glides (mboss/mv/glide: rlk_mb_mv), the
  step mv/tick will take next tick is tested against the avatar where it is now; when that step would bring her nearer than
  api.BODY['stop'] b she stops on her path at the last point that keeps it (0.2-b probe steps) and spends the glide's ticks left
  going there and to its end height (a dive still lands; the hazard keeps the locked spot: reach and timing do not change). A
  leap (mv/leap, an arc) keeps its arc: only its end is pulled out of the avatar's 'stop' circle. The choice of a stop point
  (dash stop, near(), the spots / stations, MX's streak, cam_clear) is checked when the move starts by core/cam_ok's body clause
  (p1.sw_runtime).
- core/sep (the soft separation, chosen over the framework's #mbPushOn capsule: that one is a set of anchor-frame boxes whose
  exits are its sides and ends, 0.6 b a tick, refused while the player dodges, and does not touch the walk; the rule here is a
  circle, radial, 0.25 b a tick, and the avatar's walk must stop at it): the avatar within api.BODY['rule'] b of her is moved
  straight away from her (never through her) by what is missing, at most api.BODY['push'] b this tick, in 0.05-b steps each
  checked like a knockback step (player/knockback/check: no block in a 0.6 x 1.8 body) and inside the arena (mboss/mv/ok); and
  within api.BODY['near'] b the avatar's Motion (the walk view/move set this tick, applied after the functions) loses the part
  that would carry it inside the rule. Not while the player is dead, reviving, in the map or held by a camera; mboss/main does
  not run on a beat's held tick (the player's own side: view/body_rule keeps the walk out there too).
"""
from . import api
from .s3lib import sset, fn, num

OBJ, CY = api.OBJ, api.CY
RULE, STOP, PUSH, NEAR = (api.BODY[k] for k in ('rule', 'stop', 'push', 'near'))
AVATAR = '@e[tag=rlk_body,limit=1]'
AV = '@e[tag=rlk_av,limit=1]'
GN, GP = 'rlk_hr_bxn', 'rlk_hr_bxp'          # the guard's next-step and probe markers (made and killed in one function)
GN_M, GP_M = f'@e[type=minecraft:marker,tag={GN},limit=1]', f'@e[type=minecraft:marker,tag={GP},limit=1]'
STO = f'{api.STORAGE} bx'
FP = ('#bx_px', '#bx_pz', '#bx_t', '#bx_nx', '#bx_nz', '#bx_dx', '#bx_dz', '#bx_qx', '#bx_qz', '#bx_a', '#bx_b', '#bx_u',
      '#bx_h', '#bx_k', '#bx_n', '#bx_d', '#bx_r', '#bx_ux', '#bx_uz', '#bx_p', '#bx_mx', '#bx_mz', '#bx_in', '#bx_al')
REACH = 11      # b: no glide step of hers is longer than 8.7 b (hcut: 16 b + the spot's 1.5 b in 2 t), + 'stop'
MARGIN = 10     # mb: core/sep's push and Motion clamp aim this far past the rule (whole-milliblock reads)


def sop(a, op, b):
    return f'scoreboard players operation {a} {OBJ} {op} {b} {OBJ}'


def mb(a, op, b):
    """a hr <op> b (an objective of the framework: @s mbMv*, #mbPX mb)."""
    return f'scoreboard players operation {a} {OBJ} {op} {b}'


def isqrt(W):
    """core/isqrt: #bx_r = sqrt(#bx_n) within 1 for 121 <= #bx_n <= 2e7 (Newton from 2000, 8 steps: the squared distances in
    milliblocks of core/sep, < 2.2 b; below 400 core/sep takes the distance as 0)."""
    lines = ['# #bx_r hr = isqrt(#bx_n hr) within 1, 121 <= #bx_n <= 2e7 (Newton from 2000, 8 steps; round X core/sep).', sset('#bx_r', 2000)]
    for _ in range(8):
        lines += [sop('#bx_k', '=', '#bx_n'), sop('#bx_k', '/=', '#bx_r'), sop('#bx_r', '+=', '#bx_k'), sop('#bx_r', '/=', '#c2'),
                  f'execute if score #bx_r {OBJ} matches ..0 run {sset("#bx_r", 1)}']
    W.w('core/isqrt', lines)


def runtime(W):
    """Every core/body* / guard* / sep* file (core.helper_files)."""
    w = W.w
    isqrt(W)
    stop_cb = int(round(STOP * 100))
    w('core/body', [
        f'# Round X (x_brief rulings 1-2; tools/mboss_scarlet/body.py): the body rule at the end of a fight tick (@s = the body, at it;',
        f'# P1 / P2 / G1 / G2): her glide checked against the live avatar (core/guard), the avatar kept {num(RULE)} b off her (core/sep).',
        f'execute unless entity {AVATAR} run return 0',
        f'execute if entity @s[tag=rlk_mb_mv] run {fn("core/guard")}',
        f'execute at @s positioned ~ {CY} ~ if entity @e[tag=rlk_body,distance=..{num(NEAR + 0.45, 2)}] run {fn("core/sep")}'])
    # ---------------------------------------------------------------------------------------------------------------- the guard
    w('core/guard', [
        f'# @s = the body gliding (rlk_mb_mv): the step mboss/mv/tick takes next tick (its own arithmetic at mbMvT + 1) against the',
        f'# avatar now. A step that would come nearer than {num(STOP)} b to it: core/guard_stop (she stops on her path). A leap (mbMvH):',
        '# its end only (core/guard_arc). Centi-blocks relative to her: every product stays inside int32.',
        f'execute at @s positioned ~ {CY} ~ unless entity @e[tag=rlk_body,distance=..{REACH}] run return 0',
        f'execute if score @s mbMvH matches 1.. run return run {fn("core/guard_arc")}',
        'scoreboard players set #mbPlG mb -1',
        'execute unless function rlk:mboss/mv/plpos run return 0',
        f'execute store result score #bx_px {OBJ} run data get entity @s Pos[0] 1000',
        f'execute store result score #bx_pz {OBJ} run data get entity @s Pos[2] 1000',
        mb('#bx_t', '=', '@s mbMvT'), f'scoreboard players add #bx_t {OBJ} 1',
        mb('#bx_nx', '=', '@s mbMvX1'), mb('#bx_nx', '-=', '@s mbMvX0'), sop('#bx_nx', '*=', '#bx_t'), mb('#bx_nx', '/=', '@s mbMvN'),
        mb('#bx_nx', '+=', '@s mbMvX0'),
        mb('#bx_nz', '=', '@s mbMvZ1'), mb('#bx_nz', '-=', '@s mbMvZ0'), sop('#bx_nz', '*=', '#bx_t'), mb('#bx_nz', '/=', '@s mbMvN'),
        mb('#bx_nz', '+=', '@s mbMvZ0'),
        sop('#bx_dx', '=', '#bx_nx'), sop('#bx_dx', '-=', '#bx_px'), sop('#bx_dx', '/=', '#c10'),
        sop('#bx_dz', '=', '#bx_nz'), sop('#bx_dz', '-=', '#bx_pz'), sop('#bx_dz', '/=', '#c10'),
        mb('#bx_qx', '=', '#mbPX mb'), sop('#bx_qx', '-=', '#bx_px'), sop('#bx_qx', '/=', '#c10'),
        mb('#bx_qz', '=', '#mbPZ mb'), sop('#bx_qz', '-=', '#bx_pz'), sop('#bx_qz', '/=', '#c10'),
        # a = |D|^2, b = Q . D: a step with no floor travel, or one that does not go toward the avatar, is free
        sop('#bx_a', '=', '#bx_dx'), sop('#bx_a', '*=', '#bx_dx'), sop('#bx_k', '=', '#bx_dz'), sop('#bx_k', '*=', '#bx_dz'),
        sop('#bx_a', '+=', '#bx_k'),
        f'execute if score #bx_a {OBJ} matches ..0 run return 0',
        sop('#bx_b', '=', '#bx_qx'), sop('#bx_b', '*=', '#bx_dx'), sop('#bx_k', '=', '#bx_qz'), sop('#bx_k', '*=', '#bx_dz'),
        sop('#bx_b', '+=', '#bx_k'),
        f'execute if score #bx_b {OBJ} matches ..0 run return 0',
        # u = the step's nearest point to the avatar (per mille of the step), h = its squared distance (cb^2)
        sop('#bx_u', '=', '#bx_b'), sop('#bx_u', '*=', '#c1000'), sop('#bx_u', '/=', '#bx_a'),
        f'execute if score #bx_u {OBJ} matches 1001.. run {sset("#bx_u", 1000)}',
        sop('#bx_k', '=', '#bx_dx'), sop('#bx_k', '*=', '#bx_u'), sop('#bx_k', '/=', '#c1000'), sop('#bx_qx', '-=', '#bx_k'),
        sop('#bx_k', '=', '#bx_dz'), sop('#bx_k', '*=', '#bx_u'), sop('#bx_k', '/=', '#c1000'), sop('#bx_qz', '-=', '#bx_k'),
        sop('#bx_h', '=', '#bx_qx'), sop('#bx_h', '*=', '#bx_qx'), sop('#bx_k', '=', '#bx_qz'), sop('#bx_k', '*=', '#bx_qz'),
        sop('#bx_h', '+=', '#bx_k'),
        f'execute if score #bx_h {OBJ} matches {stop_cb * stop_cb}.. run return 0',
        fn('core/guard_stop')])
    w('core/guard_stop', [
        f'# @s = the body: her next glide step would come nearer than {num(STOP)} b to the avatar. A probe walks from her toward that',
        f'# step\'s end (#bx_nx / #bx_nz, at her height) in 0.2-b steps while the next point keeps {num(STOP)} b from the avatar (on',
        '# the floor plane); she glides there instead, and to the glide\'s end height, in the ticks the glide had left.',
        f'kill @e[type=minecraft:marker,tag={GN}]', f'kill @e[type=minecraft:marker,tag={GP}]',
        f'summon minecraft:marker ~ ~ ~ {{Tags:["{GN}","rlk_room","rlk_mb_aux"]}}',
        f'summon minecraft:marker ~ ~ ~ {{Tags:["{GP}","rlk_room","rlk_mb_aux"]}}',
        f'execute store result entity {GN_M} Pos[0] double 0.001 run scoreboard players get #bx_nx {OBJ}',
        f'execute store result entity {GN_M} Pos[2] double 0.001 run scoreboard players get #bx_nz {OBJ}',
        f'execute as {GP_M} at @s facing entity {GN_M} feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0',
        sset('#bx_k', 0),
        f'execute as {GP_M} at @s run {fn("core/guard_step")}',
        f'execute store result entity {GP_M} Pos[1] double 0.001 run scoreboard players get @s mbMvY1',
        mb('#bx_k', '=', '@s mbMvN'), mb('#bx_k', '-=', '@s mbMvT'),
        f'execute if score #bx_k {OBJ} matches ..0 run {sset("#bx_k", 1)}',
        f'execute store result storage {STO}.t int 1 run scoreboard players get #bx_k {OBJ}',
        f'execute positioned as {GP_M} run function rlk:mboss/mv/glide with storage {STO}',
        f'kill @e[type=minecraft:marker,tag={GN}]', f'kill @e[type=minecraft:marker,tag={GP}]'])
    w('core/guard_step', [
        f'# @s = the guard\'s probe (at / rotated as it): 0.2 b on toward the step\'s end while the point keeps {num(STOP)} b from the',
        '# avatar on the floor plane (at most 44 steps: 8.8 b).',
        f'execute if score #bx_k {OBJ} matches 44.. run return 0',
        f'execute if entity @e[type=minecraft:marker,tag={GN},distance=..0.2] run return 0',
        f'execute positioned ^ ^ ^0.2 positioned ~ {CY} ~ if entity @e[tag=rlk_body,distance=..{num(STOP)}] run return 0',
        'tp @s ^ ^ ^0.2', f'scoreboard players add #bx_k {OBJ} 1', f'execute at @s run {fn("core/guard_step")}'])
    w('core/guard_arc', [
        f'# @s = the body in a leap (mboss/mv/leap: the arc of mbMvH): the arc is kept; its end (mbMvX1 / Z1) inside {num(STOP)} b of the',
        f'# avatar on the floor plane moves straight away from the avatar to {num(STOP + 0.1)} b (when mv/ok passes there).',
        f'kill @e[type=minecraft:marker,tag={GN}]',
        f'execute positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:["{GN}","rlk_room","rlk_mb_aux"]}}',
        f'execute store result entity {GN_M} Pos[0] double 0.001 run scoreboard players get @s mbMvX1',
        f'execute store result entity {GN_M} Pos[2] double 0.001 run scoreboard players get @s mbMvZ1',
        f'execute at {GN_M} unless entity @e[tag=rlk_body,distance=..{num(STOP)}] run return run kill {GN_M}',
        f'execute at {AVATAR} positioned ~ {CY} ~ facing entity {GN_M} feet rotated ~ 0 positioned ^ ^ ^{num(STOP + 0.1)} '
        f'if function rlk:mboss/mv/ok run tp {GN_M} ~ ~ ~',
        f'execute at {GN_M} if entity @e[tag=rlk_body,distance=..{num(STOP)}] run return run kill {GN_M}',
        f'execute store result score @s mbMvX1 run data get entity {GN_M} Pos[0] 1000',
        f'execute store result score @s mbMvZ1 run data get entity {GN_M} Pos[2] 1000',
        f'kill {GN_M}'])
    # ---------------------------------------------------------------------------------------------------------------- the separation
    # the push and the Motion clamp aim MARGIN mb past the rule (the positions are read in whole milliblocks: aiming at the rule
    # itself leaves 1.3996 b)
    rule_mm, near_mm, push_mm = int(round(RULE * 1000)) + MARGIN, int(round(NEAR * 1000)), int(round(PUSH * 1000))
    w('core/sep', [
        f'# @s = the body; the avatar near her floor point. Round X\'s soft separation (body.py): inside {num(RULE)} b (floor plane) the',
        f'# avatar goes straight away from her by what is missing, at most {num(PUSH)} b this tick (core/sep_push); within {num(NEAR)} b its',
        f'# Motion keeps no more pull toward her than leaves it {num(RULE)} b off after this tick\'s physics (core/sep_motion). Not while',
        '# the player is dead, reviving, choosing, in the map or held by a camera.',
        'execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0',
        'execute if entity @a[tag=player,scores={rnDie=1..}] run return 0',
        'execute if entity @a[tag=player,scores={pkMode=1..}] run return 0',
        'execute if entity @a[tag=player,scores={vMap=1}] run return 0',
        'execute if entity @a[tag=rlk_mb_camh] run return 0',
        'scoreboard players set #mbPlG mb -1',
        'execute unless function rlk:mboss/mv/plpos run return 0',
        f'execute store result score #bx_px {OBJ} run data get entity @s Pos[0] 1000',
        f'execute store result score #bx_pz {OBJ} run data get entity @s Pos[2] 1000',
        mb('#bx_qx', '=', '#mbPX mb'), sop('#bx_qx', '-=', '#bx_px'), mb('#bx_qz', '=', '#mbPZ mb'), sop('#bx_qz', '-=', '#bx_pz'),
        f'execute unless score #bx_qx {OBJ} matches -2500..2500 run return 0',
        f'execute unless score #bx_qz {OBJ} matches -2500..2500 run return 0',
        sop('#bx_n', '=', '#bx_qx'), sop('#bx_n', '*=', '#bx_qx'), sop('#bx_k', '=', '#bx_qz'), sop('#bx_k', '*=', '#bx_qz'),
        sop('#bx_n', '+=', '#bx_k'),
        f'execute if score #bx_n {OBJ} matches {near_mm * near_mm}.. run return 0',
        sset('#bx_d', 0),
        f'execute if score #bx_n {OBJ} matches 400.. run {fn("core/isqrt")}',
        f'execute if score #bx_n {OBJ} matches 400.. run {sop("#bx_d", "=", "#bx_r")}',
        # the unit her -> the avatar (per mille); on top of her: her facing
        f'execute if score #bx_d {OBJ} matches ..9 run return run {fn("core/sep_face")}',
        sop('#bx_ux', '=', '#bx_qx'), sop('#bx_ux', '*=', '#c1000'), sop('#bx_ux', '/=', '#bx_d'),
        sop('#bx_uz', '=', '#bx_qz'), sop('#bx_uz', '*=', '#c1000'), sop('#bx_uz', '/=', '#bx_d'),
        fn('core/sep_go')])
    w('core/sep_face', [
        '# @s = the body, the avatar (almost) on her centre: the way out is her facing.',
        f'kill @e[type=minecraft:marker,tag={GN}]',
        f'execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {{Tags:["{GN}","rlk_room","rlk_mb_aux"]}}',
        f'execute store result score #bx_ux {OBJ} run data get entity {GN_M} Pos[0] 1000',
        f'execute store result score #bx_uz {OBJ} run data get entity {GN_M} Pos[2] 1000',
        f'kill {GN_M}',
        sop('#bx_ux', '-=', '#bx_px'), sop('#bx_uz', '-=', '#bx_pz'),
        fn('core/sep_go')])
    w('core/sep_go', [
        f'# @s = the body; #bx_d = the avatar\'s distance (mb), #bx_ux / #bx_uz the unit her -> the avatar (per mille).',
        sop('#bx_p', '=', '#bx_d'), f'scoreboard players set #bx_k {OBJ} {rule_mm}', sop('#bx_k', '-=', '#bx_p'), sop('#bx_p', '=', '#bx_k'),
        f'execute if score #bx_p {OBJ} matches {push_mm + 1}.. run {sset("#bx_p", push_mm)}',
        # one 0.05-b step's offset (b x 1000 -> storage doubles)
        sop('#bx_k', '=', '#bx_ux'), sop('#bx_k', '*=', '#c5'), sop('#bx_k', '/=', '#c100'),
        f'execute store result storage {STO}.x double 0.001 run scoreboard players get #bx_k {OBJ}',
        sop('#bx_k', '=', '#bx_uz'), sop('#bx_k', '*=', '#c5'), sop('#bx_k', '/=', '#c100'),
        f'execute store result storage {STO}.z double 0.001 run scoreboard players get #bx_k {OBJ}',
        f'execute if score #bx_p {OBJ} matches 1.. run function {api.NS}core/sep_step with storage {STO}',
        f'execute if entity {AV} run {fn("core/sep_motion")}',
        'scoreboard players set #mbPlG mb -1'])
    w('core/sep_step', [
        '# {x,z} one 0.05-b step of the avatar straight away from her (#bx_p mb left; each step checked like a knockback step: no block',
        '# in the body, inside the arena - else the push ends here).',
        'scoreboard players set #pkbBlocked tmp 0',
        '$execute at @e[tag=rlk_body,limit=1] positioned ~$(x) ~ ~$(z) run function rlk:player/knockback/check',
        'execute if score #pkbBlocked tmp matches 1 run return 0',
        '$execute at @e[tag=rlk_body,limit=1] positioned ~$(x) ~ ~$(z) positioned ~ ' + str(CY) + ' ~ unless function rlk:mboss/mv/ok run return 0',
        '$execute at @e[tag=rlk_body,limit=1] run tp @e[tag=rlk_body,limit=1] ~$(x) ~ ~$(z)',
        f'scoreboard players add #bx_d {OBJ} 50', f'scoreboard players remove #bx_p {OBJ} 50',
        f'$execute if score #bx_p {OBJ} matches 1.. run function {api.NS}core/sep_step {{x:$(x),z:$(z)}}'])
    w('core/sep_motion', [
        f'# @s = the body; the avatar entity (rlk_av) #bx_d mb from her: its Motion (b/t x 10000) loses the pull toward her beyond what',
        f'# leaves it {num(RULE)} b off after this tick\'s physics (the walk view/move set; vanilla moves it by Motion after the functions).',
        f'execute store result score #bx_mx {OBJ} run data get entity {AV} Motion[0] 10000',
        f'execute store result score #bx_mz {OBJ} run data get entity {AV} Motion[2] 10000',
        sop('#bx_in', '=', '#bx_mx'), sop('#bx_in', '*=', '#bx_ux'), sop('#bx_k', '=', '#bx_mz'), sop('#bx_k', '*=', '#bx_uz'),
        sop('#bx_in', '+=', '#bx_k'), sop('#bx_in', '/=', '#cn1000'),
        sop('#bx_al', '=', '#bx_d'), f'scoreboard players remove #bx_al {OBJ} {rule_mm}', sop('#bx_al', '*=', '#c10'),
        f'execute if score #bx_al {OBJ} matches ..-1 run {sset("#bx_al", 0)}',
        f'execute if score #bx_in {OBJ} <= #bx_al {OBJ} run return 0',
        sop('#bx_in', '-=', '#bx_al'),
        sop('#bx_k', '=', '#bx_ux'), sop('#bx_k', '*=', '#bx_in'), sop('#bx_k', '/=', '#c1000'), sop('#bx_mx', '+=', '#bx_k'),
        sop('#bx_k', '=', '#bx_uz'), sop('#bx_k', '*=', '#bx_in'), sop('#bx_k', '/=', '#c1000'), sop('#bx_mz', '+=', '#bx_k'),
        f'execute store result entity {AV} Motion[0] double 0.0001 run scoreboard players get #bx_mx {OBJ}',
        f'execute store result entity {AV} Motion[2] double 0.0001 run scoreboard players get #bx_mz {OBJ}'])
