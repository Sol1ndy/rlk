"""P5 하늘을 심판하는 자 (fly-slam), P6 guard sweeps (gold / enchanted) and the chaos fail spears.

The sweeps (ids 11, 12) and the fail spears (13) are service patterns: the core starts them from
guard mode (timeout / record) and from the chaos fail; they never come out of the shuffle bag.

Inputs the core sets before starting them (see gd_contract.md):
  11 sweep_g   nothing (gold Geo sweep)
  12 sweep_e   #gdSwEl mb = recorded element 1-4; the core already turned the spear (rig spear/<el>)
               and restores it when the pattern ends or is cancelled
  13 fail      #gdFailN mb = surviving stars (1-2), #gdFailK1 / #gdFailK2 mb = their kinds
               (1-4 element, 5 inert gold, 6 inert blue); pattern clock 0 = the timer ran out (T0).
               The core plays chaos_fail / chaos_land / chaos_raise on the body and runs the ambience.

STUB QUALITY: right clips and hit ticks, planned arcs/radii/coefficients, element and colour per
hit. Still to author (patterns.md §7, §8.5-8.8, §9.4; plan.md K12, K26):
  P5  black-brown cubes climbing the shaft (0-12), gold spiral ribbons (12-16), the take-off beam
      with crescent arcs (16-19), the dark-cube trail, falling gold sparkles over the ring (26-40),
      the descent pillar, the gold/orange crystal spike ring (47-71).
  P6  gold sweep: the crescent and the row of vertical crystal spikes along the arc edge; enchanted
      sweep: the element line through her (4-6), the coloured crescent, per-element strike fx
      (electro forked bolts, pyro flames, hydro splash, cryo shards) and the lingering arcs.
  fail the gold cube column, the red giant spear growing out of it and turning to the star colour
      (37-40 + 31k), the concave 4-point star decal (side arms opening to >= 9 b), the X of light
      beams, the dome, the spike field / ice splash, the cracks, the dissolve after 30 t.
Owner of this file: the P5/P6/fail pattern author. Write only through gen.pw(key, ...).
"""
from .api import (Pattern, ev, clip_len, DMG, KB, CY, GOLD, GOLD_PALE, EL_RGB, EL_KEY, STAR_RGB, STAR_HZCOL)

FAIL_DECAL, FAIL_GAP, FAIL_TELL = 25, 31, 24      # decal at T0+25+31k, impact 24 t later (K12: >= 20 t)

PATTERNS = [
    Pattern(5, 'flyslam', '하늘을 심판하는 자', bands=('far',), recover=22, max_len=clip_len('flyslam') + 4),
    Pattern(11, 'sweep_g', '파수 모드 – 휘두르기', kind='service', recover=20, max_len=clip_len('sweep') + 4),
    Pattern(12, 'sweep_e', '파수 모드 – 원소 휘두르기', kind='service', recover=20, max_len=clip_len('sweep_e') + 4),
    Pattern(13, 'fail', '파괴 실패 – 거대한 창', kind='service', recover=20,
            max_len=FAIL_DECAL + FAIL_GAP + FAIL_TELL + 40),
]

SPEAR_MODEL = {1: 'pyro', 2: 'hydro', 3: 'electro', 4: 'cryo', 5: 'gold', 6: 'hydro'}


def emit(g):
    flyslam(g)
    sweep_g(g)
    sweep_e(g)
    fail(g)


def flyslam(g):
    k = 'flyslam'
    ring, imp = ev(k, 'ring'), ev(k, 'impact')
    g.pw(k, 'start', [
        '# P5 start (@s = body, player far): flyslam clip (101 t: glint 6, beam 16, takeoff 19, ring 21, gone 23,',
        '# dive 39, impact 41, spikes 47, pull 71, twirl 79). The rig rises 8 b; the body (hitbox) glides under the',
        '# locked ring during 23-39 and is untargetable while she is up (21-41).',
        g.rig('face/player'),
        g.play(k)])
    g.pw(k, 'tick', [
        '# P5 tick (@s = body, #gdPT = clip tick). Ring locked at take-off + 2 (K26), 20 t to the impact, r 4.5.',
        g.at((0, 12), 'execute rotated as @s rotated ~ 0 run ' + g.dust((0.25, 0.16, 0.1), 1.2, '^-0.4 ^2.6 ^0.4', (0.1, 0.6, 0.1), 2)),
        g.at(ev(k, 'glint'), 'execute rotated as @s rotated ~ 0 run ' + g.card('star', '^-0.4 ^4.6 ^0.3', bb='center', spin=60, s0=0.1, s1=1.0, life=6, fade=3)),
        g.at(ev(k, 'beam'), g.dust(GOLD_PALE, 1.6, '~ ~3 ~', (0.15, 3.0, 0.15), 30)),
        g.at(ev(k, 'beam'), g.sound('block.beacon.activate', 0.6, 1.6)),
        g.at(ev(k, 'takeoff'), g.voice_attack()),
        g.at(ev(k, 'takeoff'), 'scoreboard players set #mbNoLeash mb 1'),
        g.at(ev(k, 'takeoff'), g.sound('entity.ender_dragon.flap', 0.8, 1.3)),
        g.at(ev(k, 'takeoff'), g.sound('item.trident.riptide_3', 0.7, 1.0)),
        g.at(ring, f'execute at @e[tag=rlk_body,limit=1] positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p5"]}}'),
        g.at(ring, 'scoreboard players set #hzSfx mb 1'),
        g.at(ring, f'execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p5,limit=1] run {g.hz_disc(4.5, imp - ring, DMG["p5"])}'),
        g.at(ring, 'tag @s add rlk_mb_inv'),
        g.at(ev(k, 'gone'), f'execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p5,limit=1] run function rlk:mboss/mv/glide {{t:{ev(k, "dive") - ev(k, "gone")}}}'),
        g.at((ev(k, 'gone') + 3, ev(k, 'dive')), 'execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p5,limit=1] run ' + g.particle('end_rod', '~ ~6 ~', (0.6, 2.0, 0.6), 0, 1)),
        g.at(ev(k, 'dive') - 2, g.sound('block.beacon.deactivate', 0.7, 1.8)),
        g.at(imp, 'tag @s remove rlk_mb_inv'),
        g.at(imp, 'scoreboard players set #mbNoLeash mb 0'),
        g.at(imp, g.card('burst', '~ ~1.2 ~', bb='center', spin=20, s0=0.8, s1=3.6, life=6, fade=3)),
        g.at(imp, g.card('ring', '~ ~0.1 ~', rot='~ 90', s0=1.0, s1=9.0, life=8, fade=3)),
        g.at(imp, g.particle('block{block_state:"minecraft:gold_block"}', '~ ~0.3 ~', (2.2, 0.2, 2.2), 0, 34)),
        g.at(imp, g.sound('entity.generic.explode', 0.9, 0.9)),
        g.at(imp, g.sound('entity.zombie.attack_iron_door', 0.6, 0.6)),
        g.at(imp, 'kill @e[type=minecraft:marker,tag=rlk_mb_gd_p5]'),
        g.at(ev(k, 'spikes'), g.sound('block.pointed_dripstone.land', 0.8, 1.0)),
        g.at(ev(k, 'spikes'), g.sound('block.amethyst_cluster.place', 0.8, 1.0)),
        g.at(ev(k, 'pull'), g.sound('block.chain.break', 0.8, 0.6)),
        g.at(ev(k, 'twirl'), g.sound('item.trident.riptide_1', 0.5, 1.4)),
        g.at(clip_len(k), g.end())])
    g.pw(k, 'cancel', ['# P5 cancel: the ring marker (rlk_mb_inv and the leash are reset by the core).',
                       'kill @e[type=minecraft:marker,tag=rlk_mb_gd_p5]'])


def sweep_g(g):
    k = 'sweep_g'
    act = ev('sweep', 'active')
    g.pw(k, 'start', [
        '# Gold sweep (guard timeout; @s = body): sweep clip (44 t, active 19-24): 200 degree front arc, r 5 (K6).',
        g.rig('face/player'),
        g.play('sweep'),
        g.sound('item.trident.riptide_2', 0.7, 0.7),
        'scoreboard players set #hzSfx mb 2',
        f'scoreboard players set #hzKB mb {KB["default"]}',
        f'scoreboard players set #hzAct mb {ev("sweep", "active_end") - act}',
        f'execute at @s rotated as @s rotated ~ 0 positioned ~ {CY} ~ run {g.hz_sector(5.0, 100, act, DMG["gold"])}'])
    g.pw(k, 'tick', [
        '# Gold sweep tick (@s = body, #gdPT = clip tick).',
        g.at(act, 'execute rotated as @s rotated ~ 0 run ' + g.card('crescent', '^ ^1.0 ^', spin=-150, s0=8.0, s1=9.6, life=6, fade=2)),
        g.at(act, g.sound('entity.player.attack.sweep', 1.0, 0.6)),
        g.at(act, g.sound('block.pointed_dripstone.land', 0.8, 0.9)),
        g.at(act, g.sound('entity.generic.explode', 0.3, 1.3)),
        g.at((act, act + 3), 'execute rotated as @s rotated ~ 0 run ' + g.dust(GOLD, 1.3, '^ ^0.6 ^3.2', (2.6, 0.3, 1.4), 12)),
        g.at(clip_len('sweep'), g.end())])
    g.pw(k, 'cancel', ['# Gold sweep cancel: nothing of its own.'])


def sweep_e(g):
    k = 'sweep_e'
    act, act_end = ev('sweep_e', 'active'), ev('sweep_e', 'active_end')
    strike = ['# Element-coloured strike fx over the arc (#gdSwEl), every tick of the active window.']
    pts = {1: ('flame', 0.03), 2: ('splash', 0.2), 3: ('electric_spark', 0.2), 4: ('snowflake', 0.05)}
    for e, (pt, sp) in pts.items():
        strike.append(f'execute if score #gdSwEl mb matches {e} rotated as @s rotated ~ 0 run '
                      + g.dust(EL_RGB[e], 1.5, '^ ^0.8 ^3.0', (2.6, 0.4, 1.6), 10))
        strike.append(f'execute if score #gdSwEl mb matches {e} rotated as @s rotated ~ 0 run '
                      + g.particle(pt, '^ ^0.8 ^3.0', (2.4, 0.4, 1.4), sp, 8))
    g.pw(k, 'strike', strike)
    g.pw(k, 'start', [
        '# Enchanted sweep (record complete; @s = body, spear already in the element): sweep_e clip (50 t: enchant 0,',
        '# windup 7, active 19-27): 200 degree front arc r 5, x2.5 with the recorded element, strong knockback (K16).',
        g.rig('face/player'),
        g.play('sweep_e'),
        'scoreboard players set #hzSfx mb 2',
        f'scoreboard players set #hzKB mb {KB["ench"]}',
        f'scoreboard players set #hzAct mb {act_end - act}',
        'scoreboard players operation #hzEl mb = #gdSwEl mb',
        'scoreboard players operation #hzCol mb = #gdSwEl mb',
        f'execute at @s rotated as @s rotated ~ 0 positioned ~ {CY} ~ run {g.hz_sector(5.0, 100, act, DMG["ench"])}'])
    tick = ['# Enchanted sweep tick (@s = body, #gdPT = clip tick).']
    for e in EL_KEY:
        tick.append(g.at((4, 6), f'execute if score #gdSwEl mb matches {e} rotated as @s rotated ~ 0 run '
                         + g.dust(EL_RGB[e], 1.2, '^ ^1.7 ^0.3', (1.6, 0.04, 0.04), 8)))
        tick.append(g.at((7, act - 1), f'execute if score #gdSwEl mb matches {e} rotated as @s rotated ~ 0 run '
                         + g.dust(EL_RGB[e], 1.0, '^0.8 ^3.2 ^0.2', (0.3, 0.6, 0.3), 2)))
    tick += [g.at(4, g.sound('block.beacon.activate', 0.6, 1.2)),
             g.at(5, g.sound('entity.warden.sonic_charge', 0.25, 1.6)),
             g.at((act, act_end), g.fn('p/sweep_e/strike')),
             g.at(act, 'execute rotated as @s rotated ~ 0 run ' + g.card('crescent', '^ ^1.1 ^', spin=-150, s0=8.0, s1=9.8, life=7, fade=2)),
             g.at(act, g.sound('entity.player.attack.sweep', 1.0, 0.6)),
             g.at(act, 'execute if score #gdSwEl mb matches 3 run ' + g.sound('entity.lightning_bolt.impact', 0.5, 1.8)),
             g.at(act, 'execute if score #gdSwEl mb matches 1 run ' + g.sound('item.firecharge.use', 0.8, 0.8)),
             g.at(act, 'execute if score #gdSwEl mb matches 2 run ' + g.sound('entity.player.splash.high_speed', 0.8, 1.0)),
             g.at(act, 'execute if score #gdSwEl mb matches 4 run ' + g.sound('block.glass.break', 0.8, 1.3)),
             g.at(clip_len('sweep_e'), g.end())]
    g.pw(k, 'tick', tick)
    g.pw(k, 'cancel', ['# Enchanted sweep cancel: nothing of its own (the core restores the spear look).'])


def fail(g):
    k = 'fail'
    lines = ['# Fail spears tick (@s = body, #gdPT = ticks since T0). Spear j (0, 1) for every surviving star:',
             f'# decal + locked target at {FAIL_DECAL} + {FAIL_GAP}j, impact {FAIL_TELL} t later, cylinder r 2.8 (K12).']
    for j in (0, 1):
        dec = FAIL_DECAL + FAIL_GAP * j
        hit = dec + FAIL_TELL
        need = f'if score #gdFailN mb matches {j + 1}..'
        kk = f'#gdFailK{j + 1}'
        lines += [
            f'execute if score #gdPT mb matches {dec} {need} run {g.fn(f"p/fail/lock{j}")}',
            f'execute if score #gdPT mb matches {dec + 1}..{hit - 1} {need} at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t{j},limit=1] run '
            + g.dust((0.75, 0.10, 0.18), 1.4, '~ ~0.15 ~', (1.8, 0.02, 1.8), 4),
            f'execute if score #gdPT mb matches {dec + 13} {need} run {g.fn(f"p/fail/tint{j}")}',
            f'execute if score #gdPT mb matches {hit - 4} {need} run ' + g.sound('item.trident.riptide_3', 0.5, 1.4),
            f'execute if score #gdPT mb matches {hit} {need} run {g.fn(f"p/fail/drop{j}")}',
            f'execute if score #gdPT mb matches {hit + 30} {need} run {g.fn(f"p/fail/fade{j}")}']
    lines += [f'execute if score #gdFailN mb matches 1 if score #gdPT mb matches {FAIL_DECAL + FAIL_TELL + 31} run {g.end()}',
              f'execute if score #gdFailN mb matches 2.. if score #gdPT mb matches {FAIL_DECAL + FAIL_GAP + FAIL_TELL + 31} run {g.end()}',
              f'execute unless score #gdFailN mb matches 1.. run {g.end()}']
    g.pw(k, 'tick', lines)
    g.pw(k, 'start', ['# Fail spears start (@s = body, T0): nothing yet; the first decal comes at +25.',
                      g.sound('block.respawn_anchor.charge', 0.5, 0.8)])
    for j in (0, 1):
        kk = f'#gdFailK{j + 1}'
        lock = [f'# Spear {j + 1}: lock the player\'s position, the hazard (element/colour by the star kind) and the giant',
                '# red spear hanging point-down, its tip 3.8 b above the target (prop scale 5.5: tip 8.1 b below the grip).',
                f'execute at @e[tag=rlk_body,limit=1] positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ '
                f'{{Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p13","rlk_mb_gd_p13t{j}"]}}',
                'scoreboard players set #hzSfx mb 4',
                f'scoreboard players set #hzKB mb {KB["default"]}']
        for kind in range(1, 7):
            if kind <= 4:
                lock.append(f'execute if score {kk} mb matches {kind} run scoreboard players set #hzEl mb {kind}')
            lock.append(f'execute if score {kk} mb matches {kind} run scoreboard players set #hzCol mb {STAR_HZCOL[kind]}')
        lock += [f'execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t{j},limit=1] run {g.hz_disc(2.8, FAIL_TELL, DMG["fail"])}',
                 f'execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t{j},limit=1] positioned ~ ~11.9 ~ rotated 0 0 run ' + g.rig('prop/spear'),
                 'data merge entity @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] {transformation:{left_rotation:[1f,0f,0f,0f],scale:[5.5f,5.5f,5.5f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/guardian/prop_spear_red"}}}',
                 f'tag @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] add rlk_mb_gd_p13s{j}',
                 'tag @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] add rlk_mb_gd_p13',
                 f'execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t{j},limit=1] run ' + g.particle('block{block_state:"minecraft:gold_block"}', '~ ~11 ~', (0.3, 1.2, 0.3), 0, 20),
                 g.sound('block.respawn_anchor.charge', 0.8, 0.8), g.sound('block.beacon.power_select', 0.6, 0.6),
                 g.sound('block.amethyst_block.resonate', 0.8, 0.8)]
        if j == 0:
            lock.append(g.voice_attack())
        g.pw(k, f'lock{j}', lock)
        tint = [f'# Spear {j + 1} turns from red to the star colour.', g.sound('block.amethyst_block.chime', 0.8, 1.5)]
        for kind, m in SPEAR_MODEL.items():
            tint.append(f'execute if score {kk} mb matches {kind} run data modify entity @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s{j},limit=1] '
                        f'item.components."minecraft:item_model" set value "rlk:mboss/guardian/prop_spear_{m}"')
        g.pw(k, f'tint{j}', tint)
        drop = [f'# Spear {j + 1} drops in 1 t and strikes (the hazard resolves this tick).',
                f'execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s{j},limit=1] at @s run tp @s ~ ~-3.8 ~',
                f'execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t{j},limit=1] run ' + g.card('burst', '~ ~1.4 ~', bb='center', spin=20, s0=0.8, s1=3.4, life=6, fade=3),
                f'execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t{j},limit=1] run ' + g.dust(GOLD_PALE, 1.8, '~ ~4 ~', (0.2, 4.0, 0.2), 30)]
        for kind in range(1, 7):
            drop.append(f'execute if score {kk} mb matches {kind} at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t{j},limit=1] run '
                        + g.dust(STAR_RGB[kind], 1.6, '~ ~0.6 ~', (1.8, 0.4, 1.8), 30))
        drop += [g.sound('item.trident.hit_ground', 1.0, 0.5), g.sound('entity.lightning_bolt.impact', 0.6, 0.8),
                 g.sound('entity.generic.explode', 0.8, 0.7), g.sound('block.amethyst_cluster.break', 1.0, 0.8)]
        g.pw(k, f'drop{j}', drop)
        g.pw(k, f'fade{j}', [f'# Spear {j + 1} dissolves upward into cubes.',
                             f'execute at @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s{j},limit=1] run '
                             + g.particle('block{block_state:"minecraft:red_concrete"}', '~ ~-4 ~', (0.4, 3.0, 0.4), 0, 24),
                             f'kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s{j}]',
                             f'kill @e[type=minecraft:marker,tag=rlk_mb_gd_p13t{j}]'])
    g.pw(k, 'cancel', ['# Fail spears cancel: spears and target markers.', 'kill @e[tag=rlk_mb_gd_p13]'])
