"""Chapter-2 elites (part B): 카이라기·뇌전 (kr), 그림자 닌자 (nj), 우인단 번개 시킨 술사 (cc) + 번개 시킨 (ci).

build(w): w(path, text) writes data/rlk/function/<path>.mcfunction. Writes ONLY cm/{kr,nj,cc,ci}/** and
cm/spawn/{kr,nj,cc,ci}. The shared framework lines these mobs need are elite_lib.HOOKS (install_hooks()).

Framework reuse (README 5-1): transparent husk brain (rlk_cmb, cmId) + display rig + the shared lure; damage only via
cm/hit_me / cm/hit_pl (player/take_damage: dodge i-frames, level scaling); cmS is the attack state, so the shared
freeze / player-down cancel (cm/cancel sets cmS 0) is noticed here (rlk_c2_busy) and cleaned up. rlk_cmch (stun
immunity, cm/ch_begin) only while an attack must not be interrupted; every punish window is stunnable.
No element immunity, no resistances: every element damages these mobs normally.

Tuning: the numbers live in CFG below (raw damage before the level rule, ticks at 20/s).
"""
try:
    from . import elite_lib as L
except ImportError:  # run as a plain module by the temporary runner
    import elite_lib as L

ps = L.ps
CFG = {
    'kr': dict(hp=70, xp=12, speed=0.30, scale=1.08, dash_dmg=14, dash_tell=7, dash_follow=2, dashes=3, rest=24,
               spin_dmg=18, spin_tell=16, spin_r=3.0, spin_rest=12, cd_a=64, cd_b=100, range_a=7.5, range_b=3.2),
    'nj': dict(hp=45, xp=9, speed=0.38, scale=0.96, slash_dmg=16, vanish=8, glint=12, slash_r=2.3, ambushes=2, tired=30,
               gap=14, cd_after_tired=40, shu_dmg=8, shu_tell=10, shu_life=20, shu_cd=60, far=10),
    'cc': dict(hp=50, xp=10, speed=0.24, cast=20, resummon=80, ram_gap=30, blink_r=3, blink_cd=100, dazed=20, keep=7),
    'ci': dict(hp=2, ram_dmg=8, tell=10, fly=12, orbit_r=4, orbit_deg=6, solo_cd=50),
}


def build(w):
    for m, hp in (('kr', 70), ('nj', 45), ('cc', 50), ('ci', 2)):
        L.lib(w, m, hp=CFG[m]['hp'])
    kr(w)
    nj(w)
    cc(w)
    ci(w)


def fnw(w, m):
    return lambda rel, *lines: w(f'cm/{m}/{rel}', '\n'.join(lines))


def husk_spawn(w, m, title, *, scale, speed, xp, extra_tags='', nbt='', zmob=True):
    tags = ('"rlk_room","rlk_zmob",' if zmob else '"rlk_room",') + f'"rlk_newmob","rlk_cmb","rlk_cm_{m}","rlk_m_cm{m}","rlk_cmnew","rlk_c2e"{extra_tags}'
    w(f'cm/spawn/{m}', '\n'.join([
        f'# {title}: transparent husk brain (pathing, health bar, hits) + display rig linked by cmId; at the caller\'s position',
        f'function rlk:cm/{m}/lib/obj',
        f'summon minecraft:husk ~ ~ ~ {{Tags:[{tags}],PersistenceRequired:1b,DeathLootTable:"minecraft:empty",Silent:1b,IsBaby:0b,'
        f'CanPickUpLoot:0b{nbt},active_effects:[{{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b,ambient:1b}}],'
        f'attributes:[{{id:"minecraft:scale",base:{scale}d}},{{id:"minecraft:movement_speed",base:{speed}d}}]}}',
        'scoreboard players add #cmIdC tmp 1',
        'scoreboard players operation @e[tag=rlk_cmnew] cmId = #cmIdC tmp',
        f'scoreboard players set @e[tag=rlk_cmnew] xpDrop {xp}',
        f'execute as @e[tag=rlk_cmnew] at @s run function rlk:cm/{m}/init']))


def common(f, m, reset_extra=()):
    f('init', '# new brain (@s, at @s): the shared cm init, then this mob\'s rig',
      'function rlk:cm/init', 'scoreboard players set @s cmN 0', 'scoreboard players set @s c2eF 0',
      'scoreboard players set @s cmD 0', f'function rlk:cm/{m}/rig/create')
    f('idle', 'scoreboard players set @s cmS 0', 'tag @s remove rlk_c2_busy', 'tag @s remove rlk_c2_fix', 'tag @s remove rlk_cmch')
    f('reset', '# the attack was cleared from outside (freeze / player down -> cm/cancel set cmS 0): drop what it left behind',
      'tag @s remove rlk_c2_busy', 'tag @s remove rlk_c2_fix', 'tag @s remove rlk_cmch', *reset_extra,
      'execute if score @s cmCd matches ..19 run scoreboard players set @s cmCd 20')


def frames(f, m):
    """idle/walk frame counter -> #c2p (0..3 breath, 10..17 walk, 50/51 hurt); attack states go to rig/choose_s."""
    f('rig/walkf', 'scoreboard players operation #c2p tmp = @s cmAF', 'scoreboard players operation #c2p tmp /= #3 tmp',
      'scoreboard players add #c2p tmp 10')
    return ['scoreboard players add @s cmAF 1', 'execute if score @s cmAF matches 24.. run scoreboard players set @s cmAF 0',
            f'execute if score @s cmS matches 1.. run return run function rlk:cm/{m}/rig/choose_s',
            'scoreboard players operation #c2p tmp = @s cmAF', 'scoreboard players operation #c2p tmp /= #st6 tmp',
            f'execute unless entity @s[tag=rlk_cmhold] unless score @s stunT matches 1.. unless entity @e[tag=rlk_body,distance=..2.2] run function rlk:cm/{m}/rig/walkf',
            'execute if score @s cmAH matches 4.. run scoreboard players set #c2p tmp 50',
            'execute if score @s cmAH matches 1..3 run scoreboard players set #c2p tmp 51']


def face_body(f, m, fixed=True):
    lines = []
    if fixed:
        lines += ['execute if entity @s[tag=rlk_c2_fix] store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw',
                  f'execute if entity @s[tag=rlk_c2_fix] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 as @e[tag=rlk_{m}_this] run tp @s ~ ~ ~ ~ 0',
                  f'execute unless entity @s[tag=rlk_c2_fix] facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_{m}_this] run tp @s ~ ~ ~ ~ 0']
    else:
        lines += [f'execute facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_{m}_this] run tp @s ~ ~ ~ ~ 0']
    f('rig/face', '# displays to the brain; yaw toward the body (or the locked attack yaw cmYaw while rlk_c2_fix)', *lines)


# ============================================================================================== 카이라기·뇌전
def kr(w):
    c, f = CFG['kr'], fnw(w, 'kr')
    husk_spawn(w, 'kr', '카이라기·뇌전', scale=c['scale'], speed=c['speed'], xp=c['xp'])
    common(f, 'kr', reset_extra=['execute as @e[tag=rlk_kr_dst] if score @s cmId = #cid tmp run kill @s'])
    f('tick', '# 카이라기·뇌전 (@s = brain, at @s; cm/tick hook). A: 3 zig-zag dash slashes -> 1.2 s spent (punish).',
      '# B: electro spin slash after a 0.8 s blade glow. Not staggerable from the first tell to the last dash / the spin.',
      'function rlk:cm/kr/lib/pre',
      'execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/kr/reset',
      'execute if score @s cmS matches 1 run return run function rlk:cm/kr/a_tell',
      'execute if score @s cmS matches 2 run return run function rlk:cm/kr/a_after',
      'execute if score @s cmS matches 3 run return run function rlk:cm/kr/a_rest',
      'execute if score @s cmS matches 4 run return run function rlk:cm/kr/b_tell',
      'execute if score @s cmS matches 5 run return run function rlk:cm/kr/b_rest',
      'execute if score #free tmp matches 0 run return 0',
      f'execute if score @s cmCd2 matches ..0 if entity @e[tag=rlk_body,distance=..{c["range_b"]}] run return run function rlk:cm/kr/b_start',
      f'execute if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..{c["range_a"]}] run function rlk:cm/kr/a_start')
    # ---- A: dash combo
    f('a_start', 'scoreboard players set @s cmS 1', 'scoreboard players set @s cmN 0', 'tag @s add rlk_c2_busy',
      'function rlk:cm/ch_begin', 'function rlk:cm/kr/a_aim')
    f('a_aim', f'# one dash tell ({c["dash_tell"]} t): lock the yaw (zig-zag +12 / -12 / +12 deg off the body), walk the landing now',
      f'scoreboard players set @s cmT {c["dash_tell"]}',
      'execute if score @s cmN matches 1 facing entity @e[tag=rlk_body,limit=1] feet rotated ~-12 0 run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0',
      'execute unless score @s cmN matches 1 facing entity @e[tag=rlk_body,limit=1] feet rotated ~12 0 run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0',
      'execute store result score @s cmYaw run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100',
      'tag @s add rlk_c2_fix',
      '# length: about 1.5 b past the body, 3..6 b (0.5 b steps)',
      'scoreboard players set #wN tmp 12',
      'execute if entity @e[tag=rlk_body,distance=..3.5] run scoreboard players set #wN tmp 10',
      'execute if entity @e[tag=rlk_body,distance=..2.5] run scoreboard players set #wN tmp 8',
      'execute if entity @e[tag=rlk_body,distance=..1.5] run scoreboard players set #wN tmp 6',
      'execute as @e[tag=rlk_kr_dst] if score @s cmId = #cid tmp run kill @s',
      'summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_kr_dst","rlk_c2cur","rlk_cmlink","rlk_cmsync"]}',
      'scoreboard players operation @e[tag=rlk_c2cur] cmId = #cid tmp',
      'execute rotated as @e[tag=rlk_cmrot,limit=1] as @e[tag=rlk_c2cur,limit=1] run tp @s ~ ~ ~ ~ 0',
      'execute as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/kr/lib/walk',
      'scoreboard players operation @s cmD = #wK tmp',
      'tag @e[tag=rlk_c2cur] remove rlk_c2cur',
      '# tell: the blade flares purple + a bright ring',
      'particle minecraft:electric_spark ^-0.45 ^1.3 ^0.5 0.12 0.35 0.12 0.05 12',
      'particle minecraft:end_rod ^-0.45 ^1.7 ^0.5 0 0 0 0 1',
      ps('item.trident.return', 1, 1.7))
    f('a_tell', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute as @e[tag=rlk_kr_dst] if score @s cmId = #cid tmp run tag @s add rlk_cmsync',
      'particle minecraft:electric_spark ^-0.45 ^1.3 ^0.6 0.1 0.25 0.1 0.02 2',
      'execute if score @s cmT matches ..0 run function rlk:cm/kr/a_dash')
    f('a_dash', '# sweep start -> landing (one hit per dash), then move there; the rig slides over 2 ticks',
      'execute as @e[tag=rlk_kr_dst] if score @s cmId = #cid tmp run tag @s add rlk_kr_dsel',
      'scoreboard players operation #wN tmp = @s cmD',
      'scoreboard players set #c2h tmp 0',
      'execute unless entity @e[tag=rlk_kr_dsel,limit=1] run scoreboard players set #wN tmp 0',
      'execute unless entity @e[tag=rlk_kr_dsel,limit=1] run function rlk:cm/kr/a_ray',
      'execute if entity @e[tag=rlk_kr_dsel,limit=1] facing entity @e[tag=rlk_kr_dsel,limit=1] feet run function rlk:cm/kr/a_ray',
      'execute if score #c2h tmp matches 1 run function rlk:cm/kr/a_hit',
      'execute if entity @e[tag=rlk_kr_dsel,limit=1] run tp @s @e[tag=rlk_kr_dsel,limit=1]',
      'kill @e[tag=rlk_kr_dsel]',
      'scoreboard players add @s cmN 1',
      'scoreboard players set @s cmS 2',
      f'scoreboard players set @s cmT {c["dash_follow"]}',
      ps('item.trident.riptide_1', 0.9, 1.5))
    f('a_ray', 'particle minecraft:electric_spark ~ ~0.9 ~ 0.1 0.3 0.1 0.03 2',
      'particle minecraft:dust{color:[0.72,0.45,1.0],scale:1.3} ~ ~1 ~ 0.05 0.25 0.05 0 2',
      'execute if score #c2h tmp matches 0 if entity @e[tag=rlk_body,distance=..1.3] run scoreboard players set #c2h tmp 1',
      'scoreboard players remove #wN tmp 1',
      'execute if score #wN tmp matches 0.. positioned ^ ^ ^0.5 run function rlk:cm/kr/a_ray')
    f('a_hit', f'scoreboard players set #cmDmg tmp {c["dash_dmg"]}', 'function rlk:cm/hit_me',
      'execute at @e[tag=rlk_body,limit=1] run particle minecraft:sweep_attack ~ ~1 ~ 0 0 0 0 1',
      ps('entity.player.attack.sweep', 1, 1.2))
    f('a_after', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches 1.. run return 0',
      f'execute if score @s cmN matches ..{c["dashes"] - 1} run return run function rlk:cm/kr/a_next',
      'function rlk:cm/kr/a_rest_start')
    f('a_next', 'scoreboard players set @s cmS 1', 'function rlk:cm/kr/a_aim')
    f('a_rest_start', f'# spent after the third dash: {c["rest"]} t standing still, staggerable (the punish window)',
      'scoreboard players set @s cmS 3', f'scoreboard players set @s cmT {c["rest"]}',
      'tag @s remove rlk_cmch', 'tag @s remove rlk_c2_fix',
      f'scoreboard players set @s cmCd {c["cd_a"]}',
      'execute if score @s cmCd2 matches ..19 run scoreboard players set @s cmCd2 20',
      'particle minecraft:large_smoke ~ ~1.6 ~ 0.2 0.1 0.2 0.01 4',
      ps('block.fire.extinguish', 0.6, 1.5))
    f('a_rest', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches 12 run particle minecraft:large_smoke ~ ~1.7 ~ 0.15 0.05 0.15 0.01 3',
      'execute if score @s cmT matches ..0 run function rlk:cm/kr/idle')
    # ---- B: spin
    f('b_start', 'scoreboard players set @s cmS 4', f'scoreboard players set @s cmT {c["spin_tell"]}', 'tag @s add rlk_c2_busy',
      'function rlk:cm/ch_begin', 'particle minecraft:electric_spark ^-0.5 ^1.6 ^0.2 0.2 0.5 0.2 0.06 16',
      ps('block.respawn_anchor.charge', 1, 1.4))
    f('b_tell', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'particle minecraft:electric_spark ^-0.5 ^1.6 ^0.2 0.2 0.5 0.2 0.04 3',
      'execute if score @s cmT matches 7 run ' + ps('block.beacon.power_select', 0.6, 1.8),
      'execute if score @s cmT matches ..0 run function rlk:cm/kr/b_hit')
    ring = [f'execute rotated {a} 0 positioned ^ ^0.9 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1' for a in range(0, 360, 45)]
    f('b_hit', f'execute if entity @e[tag=rlk_body,distance=..{c["spin_r"]}] run function rlk:cm/kr/b_dmg', *ring,
      'particle minecraft:electric_spark ~ ~1 ~ 1.4 0.3 1.4 0.1 40',
      ps('entity.player.attack.sweep', 1, 0.8), ps('entity.lightning_bolt.impact', 0.6, 1.6),
      'scoreboard players set @s cmS 5', f'scoreboard players set @s cmT {c["spin_rest"]}',
      f'scoreboard players set @s cmCd2 {c["cd_b"]}',
      'execute if score @s cmCd matches ..15 run scoreboard players set @s cmCd 16', 'tag @s remove rlk_cmch')
    f('b_dmg', f'scoreboard players set #cmDmg tmp {c["spin_dmg"]}', 'scoreboard players set #cmEl tmp 3',
      'scoreboard players operation #cmLv tmp = @s mlv', 'function rlk:cm/hit_pl')
    f('b_rest', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches ..0 run function rlk:cm/kr/idle')
    # ---- rig
    L.rig(w, 'kr', tp_dur=2, glow=('aura',), death=[(0, 60), (4, 61), (9, 62), (13, 63), (18, None)],
          die_fx='particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.15 30\n' + ps('entity.wither_skeleton.death', 0.7, 0.9),
          death_fx='execute if score @s cmAD matches 13 run particle minecraft:large_smoke ~ ~0.4 ~ 0.6 0.1 0.3 0.02 16')
    face_body(f, 'kr')
    f('rig/choose', *frames(f, 'kr'))
    f('rig/choose_s', 'execute if score @s cmS matches 1 run scoreboard players set #c2p tmp 20',
      'execute if score @s cmS matches 2 run scoreboard players set #c2p tmp 21',
      'execute if score @s cmS matches 2 if score @s cmT matches ..1 run scoreboard players set #c2p tmp 22',
      'execute if score @s cmS matches 3 run scoreboard players set #c2p tmp 30',
      'execute if score @s cmS matches 3 if score @s cmT matches ..14 run scoreboard players set #c2p tmp 31',
      'execute if score @s cmS matches 4 run scoreboard players set #c2p tmp 40',
      'execute if score @s cmS matches 5 run scoreboard players set #c2p tmp 44',
      'execute if score @s cmS matches 5 if score @s cmT matches 11.. run scoreboard players set #c2p tmp 41',
      'execute if score @s cmS matches 5 if score @s cmT matches 9..10 run scoreboard players set #c2p tmp 42',
      'execute if score @s cmS matches 5 if score @s cmT matches 7..8 run scoreboard players set #c2p tmp 43')


# ============================================================================================== 그림자 닌자
def nj(w):
    c, f = CFG['nj'], fnw(w, 'nj')
    husk_spawn(w, 'nj', '그림자 닌자', scale=c['scale'], speed=c['speed'], xp=c['xp'])
    common(f, 'nj')
    f('tick', '# 그림자 닌자 (@s = brain, at @s). Vanish in smoke -> reappear behind the body on safe ground -> 0.6 s glint',
      '# -> slash. After two ambushes: 1.5 s exhausted (punish). Far away: a three-shuriken fan after a 0.5 s tell.',
      'function rlk:cm/nj/lib/pre',
      'execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/nj/reset',
      'execute if entity @e[tag=rlk_nj_shu,limit=1] run function rlk:cm/nj/shu_all',
      'execute if score @s cmS matches 1 run return run function rlk:cm/nj/v_out',
      'execute if score @s cmS matches 2 run return run function rlk:cm/nj/v_tell',
      'execute if score @s cmS matches 3 run return run function rlk:cm/nj/v_after',
      'execute if score @s cmS matches 4 run return run function rlk:cm/nj/tired',
      'execute if score @s cmS matches 5 run return run function rlk:cm/nj/s_tell',
      'execute if score @s cmS matches 6 run return run function rlk:cm/nj/s_after',
      'execute if score #free tmp matches 0 run return 0',
      f'execute if score @s cmCd2 matches ..0 unless entity @e[tag=rlk_body,distance=..{c["far"]}] if entity @e[tag=rlk_body,distance=..24] run return run function rlk:cm/nj/s_start',
      f'execute if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..{c["far"]}] run function rlk:cm/nj/v_start')
    # ---- ambush
    smoke = ['particle minecraft:large_smoke ~ ~1 ~ 0.35 0.6 0.35 0.02 24', 'particle minecraft:poof ~ ~1 ~ 0.4 0.6 0.4 0.03 16']
    f('v_start', 'scoreboard players set @s cmS 1', f'scoreboard players set @s cmT {c["vanish"]}', 'tag @s add rlk_c2_busy',
      'function rlk:cm/ch_begin', *smoke, ps('entity.illusioner.mirror_move', 1, 1.3))
    f('v_out', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches ..0 run function rlk:cm/nj/v_appear')
    tries = [180, 140, -140, 100, -100]
    f('v_appear', '# 3 b behind the body (then the back diagonals, then the sides) on walked-to safe ground; else in place',
      'scoreboard players set #c2ok tmp 0', 'summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2cur"]}',
      f'function rlk:cm/nj/v_try {{a:{tries[0]}}}',
      *[f'execute if score #c2ok tmp matches 0 run function rlk:cm/nj/v_try {{a:{a}}}' for a in tries[1:]],
      'execute if score #c2ok tmp matches 1 run tp @s @e[tag=rlk_c2cur,limit=1]',
      'kill @e[tag=rlk_c2cur]',
      'scoreboard players set @s cmS 2', f'scoreboard players set @s cmT {c["glint"]}',
      '# the rig stays hidden for this tick while it moves; it appears next tick, crouched, blade glinting',
      'scoreboard players set @s cmAR 1', 'tag @s remove rlk_cmch',
      *['execute at @s run ' + s for s in smoke],
      'execute at @s run particle minecraft:end_rod ~ ~1.6 ~ 0.1 0.1 0.1 0.02 3',
      'execute at @s run ' + ps('entity.phantom.flap', 1, 1.4),
      'execute at @s run ' + ps('block.note_block.bell', 0.9, 2))
    f('v_try', '$execute as @e[tag=rlk_c2cur,limit=1] at @e[tag=rlk_body,limit=1] rotated ~$(a) 0 run tp @s ~ ~ ~ ~ 0',
      'execute as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/nj/lib/drop',
      'scoreboard players set #wN tmp 6',
      'execute as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/nj/lib/walk',
      'execute if score #wK tmp matches 4.. run scoreboard players set #c2ok tmp 1')
    f('v_tell', 'scoreboard players set #hold tmp 1',
      '# a hit that staggers it during the glint cancels the slash (still counts as an ambush)',
      'execute if score #free tmp matches 0 run return run function rlk:cm/nj/v_cancel',
      'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches 5 run particle minecraft:end_rod ^-0.3 ^1.7 ^0.3 0 0 0 0 1',
      'execute if score @s cmT matches ..0 run function rlk:cm/nj/v_slash')
    f('v_cancel', 'scoreboard players add @s cmN 1', 'scoreboard players set @s cmS 3', 'scoreboard players set @s cmT 4',
      'particle minecraft:crit ~ ~1.4 ~ 0.3 0.3 0.3 0.1 8')
    f('v_slash', '# a short lunge (up to 1.5 b of walked safe ground toward the body), then the cut',
      'summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2cur"]}',
      'execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 as @e[tag=rlk_c2cur,limit=1] run tp @s ~ ~ ~ ~ 0',
      'scoreboard players set #wN tmp 3', 'execute as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/nj/lib/walk',
      'execute if score #wK tmp matches 1.. run tp @s @e[tag=rlk_c2cur,limit=1]', 'kill @e[tag=rlk_c2cur]',
      f'execute at @s if entity @e[tag=rlk_body,distance=..{c["slash_r"]}] run function rlk:cm/nj/v_dmg',
      'execute at @s facing entity @e[tag=rlk_body,limit=1] feet positioned ^ ^1.1 ^1.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1',
      'execute at @s run ' + ps('entity.player.attack.sweep', 1, 1.4),
      'scoreboard players add @s cmN 1', 'scoreboard players set @s cmS 3', 'scoreboard players set @s cmT 5')
    f('v_dmg', f'scoreboard players set #cmDmg tmp {c["slash_dmg"]}', 'function rlk:cm/hit_me')
    f('v_after', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches 1.. run return 0',
      f'execute if score @s cmN matches {c["ambushes"]}.. run return run function rlk:cm/nj/tired_start',
      'function rlk:cm/nj/idle', f'scoreboard players set @s cmCd {c["gap"]}')
    f('tired_start', f'# exhausted: {c["tired"]} t standing, staggerable (the punish window)',
      'scoreboard players set @s cmS 4', f'scoreboard players set @s cmT {c["tired"]}', 'scoreboard players set @s cmN 0',
      'tag @s remove rlk_cmch', 'particle minecraft:cloud ^ ^1.4 ^0.4 0.05 0.05 0.05 0.01 3', ps('entity.player.breath', 1, 0.9))
    f('tired', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches 20 run particle minecraft:cloud ^ ^1.4 ^0.4 0.05 0.05 0.05 0.01 2',
      'execute if score @s cmT matches 10 run particle minecraft:cloud ^ ^1.4 ^0.4 0.05 0.05 0.05 0.01 2',
      'execute if score @s cmT matches ..0 run function rlk:cm/nj/tired_end')
    f('tired_end', 'function rlk:cm/nj/idle', f'scoreboard players set @s cmCd {c["cd_after_tired"]}')
    # ---- shuriken fan
    f('s_start', 'scoreboard players set @s cmS 5', f'scoreboard players set @s cmT {c["shu_tell"]}', 'tag @s add rlk_c2_busy',
      'particle minecraft:end_rod ^0.4 ^1.9 ^0.2 0 0 0 0 1', ps('item.crossbow.loading_middle', 1, 1.5))
    f('s_tell', 'scoreboard players set #hold tmp 1',
      'execute if score #free tmp matches 0 run return run function rlk:cm/nj/s_cancel',
      'scoreboard players operation @s cmT -= #eStep tmp',
      'particle minecraft:electric_spark ^0.4 ^1.9 ^0.2 0.05 0.05 0.05 0 1',
      'execute if score @s cmT matches ..0 run function rlk:cm/nj/s_throw')
    f('s_cancel', 'function rlk:cm/nj/idle', 'scoreboard players set @s cmCd2 30')
    aim = 'execute positioned ~ ~1.3 ~ facing entity @e[tag=rlk_cmaim,limit=1] feet positioned ^ ^ ^0.6'
    f('s_throw', '# three shuriken, -15 / 0 / +15 deg around the line to the chest',
      f'{aim} rotated ~-15 ~ run function rlk:cm/nj/shu_new', f'{aim} run function rlk:cm/nj/shu_new',
      f'{aim} rotated ~15 ~ run function rlk:cm/nj/shu_new', ps('item.trident.throw', 1, 1.6),
      'scoreboard players set @s cmS 6', 'scoreboard players set @s cmT 6', f'scoreboard players set @s cmCd2 {c["shu_cd"]}')
    f('s_after', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches ..0 run function rlk:cm/nj/idle')
    f('shu_new', '# @s = ninja brain; position/rotation = launch point and flight direction',
      'summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_nj_shu","rlk_cmlink","rlk_cmsync","rlk_c2new"],billboard:"fixed",'
      'item_display:"none",teleport_duration:1,interpolation_duration:1,view_range:1f,shadow_radius:0f,brightness:{sky:15,block:13},'
      'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f],right_rotation:[0f,0f,0f,1f]},'
      'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/nj/shuriken"}}}',
      'execute as @e[tag=rlk_c2new] run tp @s ~ ~ ~ ~ ~',
      'scoreboard players operation @e[tag=rlk_c2new] cmId = #cid tmp',
      'scoreboard players operation @e[tag=rlk_c2new] cmLv = @s mlv',
      f'scoreboard players set @e[tag=rlk_c2new] cmT {c["shu_life"]}',
      'scoreboard players set @e[tag=rlk_c2new] cmAF 0',
      'tag @e[tag=rlk_c2new] remove rlk_c2new')
    f('shu_all', 'execute as @e[tag=rlk_nj_shu] if score @s cmId = #cid tmp at @s run function rlk:cm/nj/shu_step')
    f('shu_step', '# @s = shuriken: 0.9 b/tick in three checked 0.3 b steps; spins in its own plane',
      'tag @s add rlk_cmsync', 'scoreboard players remove @s cmT 1', 'scoreboard players add @s cmAF 1',
      'execute if score @s cmAF matches 3.. run scoreboard players set @s cmAF 0',
      'execute if score @s cmAF matches 0 run data merge entity @s {start_interpolation:0,transformation:{left_rotation:[0f,0f,0f,1f]}}',
      'execute if score @s cmAF matches 1 run data merge entity @s {start_interpolation:0,transformation:{left_rotation:[0f,0.86603f,0f,0.5f]}}',
      'execute if score @s cmAF matches 2 run data merge entity @s {start_interpolation:0,transformation:{left_rotation:[0f,0.86603f,0f,-0.5f]}}',
      'scoreboard players set #c2s tmp 3', 'function rlk:cm/nj/shu_move',
      'execute if score @s cmT matches ..0 run kill @s')
    f('shu_move', 'execute at @s positioned ^ ^ ^0.3 unless block ~ ~ ~ #rlk:dash_pass run return run function rlk:cm/nj/shu_wall',
      'execute at @s run tp @s ^ ^ ^0.3',
      'execute at @s if entity @e[tag=rlk_cmaim,distance=..0.75] run return run function rlk:cm/nj/shu_hit',
      'scoreboard players remove #c2s tmp 1', 'execute if score #c2s tmp matches 1.. run function rlk:cm/nj/shu_move')
    f('shu_wall', 'particle minecraft:crit ~ ~ ~ 0.1 0.1 0.1 0.1 6', ps('item.trident.hit', 0.5, 1.8), 'kill @s')
    f('shu_hit', f'scoreboard players set #cmDmg tmp {c["shu_dmg"]}', 'scoreboard players set #cmEl tmp 0',
      'scoreboard players operation #cmLv tmp = @s cmLv', 'function rlk:cm/hit_pl', 'kill @s')
    # ---- rig
    L.rig(w, 'nj', tp_dur=1, glow=('glint',), death=[(0, 60), (5, 61), (11, None)],
          frozen_extra=['# frozen while vanished: show it (crouched) so a frozen ninja is never invisible',
                        'execute if score @s cmAP matches 20 run scoreboard players set #c2p tmp 21',
                        'execute if score @s cmAP matches 20 run function rlk:cm/nj/rig/apply',
                        'execute if score @s cmAP matches 20 run scoreboard players set @s cmAP 21'],
          die_fx=ps('entity.illusioner.mirror_move', 0.8, 0.8),
          death_fx='execute if score @s cmAD matches 5 run particle minecraft:large_smoke ~ ~0.8 ~ 0.35 0.5 0.35 0.02 30\n'
                   'execute if score @s cmAD matches 5 run particle minecraft:poof ~ ~0.8 ~ 0.35 0.5 0.35 0.02 12')
    face_body(f, 'nj', fixed=False)
    f('rig/choose', *frames(f, 'nj'))
    f('rig/choose_s', 'execute if score @s cmS matches 1 run scoreboard players set #c2p tmp 20',
      'execute if score @s cmS matches 2 run scoreboard players set #c2p tmp 22',
      'execute if score @s cmS matches 2 if score @s cmT matches 9.. run scoreboard players set #c2p tmp 21',
      'execute if score @s cmS matches 2 if score @s cmAR matches 1.. run scoreboard players set #c2p tmp 20',
      'execute if score @s cmAR matches 1.. run scoreboard players remove @s cmAR 1',
      'execute if score @s cmS matches 3 run scoreboard players set #c2p tmp 24',
      'execute if score @s cmS matches 3 if score @s cmT matches 3.. run scoreboard players set #c2p tmp 23',
      'execute if score @s cmS matches 4 run function rlk:cm/nj/rig/tiredf',
      'execute if score @s cmS matches 5 run scoreboard players set #c2p tmp 40',
      'execute if score @s cmS matches 6 run scoreboard players set #c2p tmp 41')
    f('rig/tiredf', 'scoreboard players operation #c2p tmp = @s cmT', 'scoreboard players operation #c2p tmp /= #st6 tmp',
      'scoreboard players operation #c2p tmp %= #2 tmp', 'scoreboard players add #c2p tmp 30')


# ============================================================================================== 시킨 술사
def cc(w):
    c, f = CFG['cc'], fnw(w, 'cc')
    husk_spawn(w, 'cc', '우인단 번개 시킨 술사', scale=1.0, speed=c['speed'], xp=c['xp'])
    common(f, 'cc')
    f('tick', '# 우인단 번개 시킨 술사 (@s = brain, at @s). Summons 4 cicins (cap 4, a new flock only when all are dead and',
      '# the cooldown is over), sends one at a time; blinks 6 b away from a close body (5 s), then is dazed (punish).',
      'function rlk:cm/cc/lib/pre',
      'execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/cc/reset',
      'function rlk:cm/cc/flock',
      'execute if score @s cmS matches 1 run return run function rlk:cm/cc/c_tell',
      'execute if score @s cmS matches 2 run return run function rlk:cm/cc/c_after',
      'execute if score @s cmS matches 3 run return run function rlk:cm/cc/b_shim',
      'execute if score @s cmS matches 4 run return run function rlk:cm/cc/dazed',
      f'execute if entity @e[tag=rlk_body,distance=..{c["keep"]}] run scoreboard players set #hold tmp 1',
      'execute if score #free tmp matches 0 run return 0',
      f'execute if score @s cmCd2 matches ..0 if entity @e[tag=rlk_body,distance=..{c["blink_r"]}] run return run function rlk:cm/cc/b_start',
      'execute if score #ccN tmp matches 0 if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..22] run function rlk:cm/cc/c_start')
    f('flock', '# own cicins (not brains of their own: no rlk_cmb, linked by rlk_cmlink, so they die with the caster):',
      '# tick each one, count (#ccN), any ram in progress (#ccR), idle ones tagged for the next ram, pass the haste on',
      'scoreboard players set #ccN tmp 0', 'scoreboard players set #ccR tmp 0',
      'scoreboard players operation #c2es tmp = #eStep tmp',
      'scoreboard players set #c2hs tmp 0', 'execute if entity @s[tag=rlk_cm_haste] run scoreboard players set #c2hs tmp 1',
      'execute as @e[tag=rlk_cm_ci] if score @s c2eOw = #cid tmp at @s run function rlk:cm/cc/flock_one',
      'scoreboard players operation #eStep tmp = #c2es tmp',
      'execute if score #ccN tmp matches 0 if score @s c2eF matches 1 run function rlk:cm/cc/flock_gone',
      'execute if score @s cmD matches 1.. run scoreboard players operation @s cmD -= #eStep tmp',
      'execute if score #ccR tmp matches 0 if score @s cmD matches ..0 if entity @e[tag=rlk_ci_idle,limit=1] run function rlk:cm/cc/flock_ram',
      'tag @e[tag=rlk_ci_idle] remove rlk_ci_idle')
    f('flock_one', 'scoreboard players add #ccN tmp 1',
      'execute if score #c2hs tmp matches 1 run tag @s add rlk_cm_haste', 'execute if score #c2hs tmp matches 0 run tag @s remove rlk_cm_haste',
      'function rlk:cm/ci/own_tick',
      'execute if score @s cmS matches 1.. run scoreboard players set #ccR tmp 1',
      'execute if score @s cmS matches 0 unless score @s frzT matches 1.. run tag @s add rlk_ci_idle')
    f('flock_gone', f'# the whole flock is dead: a new one only after {c["resummon"]} t', 'scoreboard players set @s c2eF 0',
      f'execute if score @s cmCd matches ..{c["resummon"] - 1} run scoreboard players set @s cmCd {c["resummon"]}')
    f('flock_ram', 'execute as @e[tag=rlk_ci_idle,sort=random,limit=1] at @s run function rlk:cm/ci/r_start',
      f'scoreboard players set @s cmD {c["ram_gap"]}')
    f('c_start', 'scoreboard players set @s cmS 1', f'scoreboard players set @s cmT {c["cast"]}', 'tag @s add rlk_c2_busy',
      'particle minecraft:witch ^-0.4 ^2.4 ^0.3 0.2 0.3 0.2 0 8', ps('entity.evoker.prepare_summon', 1, 1.3))
    f('c_tell', 'scoreboard players set #hold tmp 1',
      'execute if score #free tmp matches 0 run return run function rlk:cm/cc/c_cancel',
      'scoreboard players operation @s cmT -= #eStep tmp',
      'particle minecraft:witch ^-0.4 ^2.4 ^0.3 0.2 0.2 0.2 0 2',
      'particle minecraft:electric_spark ^-0.4 ^2.4 ^0.3 0.15 0.15 0.15 0.05 2',
      'execute if score @s cmT matches ..0 run function rlk:cm/cc/c_summon')
    f('c_cancel', 'function rlk:cm/cc/idle', 'scoreboard players set @s cmCd 30', 'particle minecraft:smoke ^-0.4 ^2.4 ^0.3 0.1 0.1 0.1 0.02 6')
    f('c_summon', '# up to the cap of 4, from just above its head (a cell the brain itself stands in).',
      '# cm/init (run by each new cicin) overwrites #cid: keep the caster id in #c2cc and restore #cid after',
      'scoreboard players operation #c2lv tmp = @s mlv', 'scoreboard players operation #c2cc tmp = @s cmId', 'scoreboard players set #c2k tmp 4',
      'scoreboard players operation #c2k tmp -= #ccN tmp',
      *[f'execute if score #c2k tmp matches {i + 1}.. positioned ~ ~1.5 ~ run function rlk:cm/cc/summon_one {{a:{i * 90}}}' for i in range(4)],
      'scoreboard players operation #cid tmp = @s cmId',
      'scoreboard players set @s c2eF 1', f'scoreboard players set @s cmD {c["ram_gap"]}',
      'scoreboard players set @s cmS 2', 'scoreboard players set @s cmT 8',
      'particle minecraft:electric_spark ~ ~2 ~ 0.5 0.4 0.5 0.1 20', ps('entity.evoker.cast_spell', 1, 1.4))
    f('summon_one', 'function rlk:cm/spawn/ci',
      '$execute as @e[tag=rlk_cm_ci] if score @s cmId = #cmIdC tmp run function rlk:cm/cc/ci_own {a:$(a)}')
    f('ci_own', '# @s = the cicin just made: owned, the caster\'s level, a quarter of the ring each',
      'tag @s remove rlk_newmob', 'tag @s remove rlk_cmb', 'tag @s add rlk_cmlink', 'tag @s add rlk_cmsync',
      'scoreboard players operation @s c2eOw = #c2cc tmp', '$scoreboard players set @s c2eA $(a)',
      'scoreboard players operation @s mlv = #c2lv tmp', f'scoreboard players set @s mhp0 {CFG["ci"]["hp"]}',
      'function rlk:mob/level_apply', 'attribute @s minecraft:attack_damage base set 0', 'scoreboard players set @s c2eQ 1')
    f('c_after', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches ..0 run function rlk:cm/cc/idle')
    f('b_start', 'scoreboard players set @s cmS 3', 'scoreboard players set @s cmT 4', 'tag @s add rlk_c2_busy',
      'function rlk:cm/ch_begin', 'particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.05 20', ps('block.amethyst_block.resonate', 1, 1.6))
    f('b_shim', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches ..0 run function rlk:cm/cc/b_go')
    tries = [180, 135, -135, 90, -90]
    f('b_go', '# 6 b straight away from the body (then the back diagonals, the sides) on walked safe ground; at least 4 b',
      'scoreboard players set #c2ok tmp 0', 'summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2cur"]}',
      f'function rlk:cm/cc/b_try {{a:{tries[0]}}}',
      *[f'execute if score #c2ok tmp matches 0 run function rlk:cm/cc/b_try {{a:{a}}}' for a in tries[1:]],
      'execute if score #c2ok tmp matches 1 run function rlk:cm/cc/b_land',
      'kill @e[tag=rlk_c2cur]',
      'execute if score #c2ok tmp matches 0 run function rlk:cm/cc/b_fail')
    f('b_try', '$execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~$(a) 0 as @e[tag=rlk_c2cur,limit=1] run tp @s ~ ~ ~ ~ 0',
      'scoreboard players set #wN tmp 12',
      'execute as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/cc/lib/walk',
      'execute if score #wK tmp matches 8.. run scoreboard players set #c2ok tmp 1')
    f('b_land', 'particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.7 0.3 0.1 30', 'particle minecraft:witch ~ ~1 ~ 0.3 0.6 0.3 0 10',
      'tp @s @e[tag=rlk_c2cur,limit=1]',
      'execute at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.7 0.3 0.1 30',
      'execute at @s run ' + ps('entity.enderman.teleport', 1, 1.3),
      f'# dazed after the blink: {c["dazed"]} t, no cast, staggerable (the punish window)',
      'scoreboard players set @s cmS 4', f'scoreboard players set @s cmT {c["dazed"]}',
      f'scoreboard players set @s cmCd2 {c["blink_cd"]}', 'tag @s remove rlk_cmch')
    f('b_fail', 'function rlk:cm/cc/idle', 'scoreboard players set @s cmCd2 20')
    f('dazed', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches 12 run particle minecraft:electric_spark ~ ~2.2 ~ 0.25 0.05 0.25 0 3',
      'execute if score @s cmT matches ..0 run function rlk:cm/cc/idle')
    L.rig(w, 'cc', tp_dur=1, glow=('flare',), death=[(0, 60), (4, 61), (9, 62), (13, 63), (18, None)],
          die_fx='particle minecraft:witch ~ ~1.2 ~ 0.4 0.6 0.4 0 20\n' + ps('entity.evoker.death', 0.8, 1.2))
    face_body(f, 'cc', fixed=False)
    f('rig/choose', *frames(f, 'cc'))
    f('rig/choose_s', 'execute if score @s cmS matches 1 run scoreboard players set #c2p tmp 21',
      'execute if score @s cmS matches 1 if score @s cmT matches 15.. run scoreboard players set #c2p tmp 20',
      'execute if score @s cmS matches 2 run scoreboard players set #c2p tmp 22',
      'execute if score @s cmS matches 3 run scoreboard players set #c2p tmp 30',
      'execute if score @s cmS matches 4 run function rlk:cm/cc/rig/dazedf')
    f('rig/dazedf', 'scoreboard players operation #c2p tmp = @s cmT', 'scoreboard players operation #c2p tmp /= #st6 tmp',
      'scoreboard players operation #c2p tmp %= #2 tmp', 'scoreboard players add #c2p tmp 31')


# ============================================================================================== 번개 시킨
def ci(w):
    c, f = CFG['ci'], fnw(w, 'ci')
    husk_spawn(w, 'ci', '번개 시킨 (술사가 부름; 단독 소환은 시험용)', scale=0.5, speed=0.0, xp=0,
               extra_tags=',"rlk_lobby"', nbt=',NoAI:1b,NoGravity:1b', zmob=False)
    # rlk_lobby: no gold / xp / heal orb for summons (the three reward functions skip that tag); no rlk_zmob, so
    # cicins never hold a room fight open.
    f('init', '# new cicin (@s, at @s)', 'function rlk:cm/init', 'scoreboard players set @s c2eOw 0',
      'execute store result score @s c2eA run random value 0..359', 'scoreboard players set @s c2eF 0',
      f'scoreboard players set @s cmCd {c["solo_cd"]}', 'function rlk:cm/ci/rig/create')
    f('idle', 'scoreboard players set @s cmS 0', 'tag @s remove rlk_c2_busy', 'tag @s remove rlk_cmch')
    f('reset', 'function rlk:cm/ci/idle')
    f('tick', '# 번개 시킨 (@s = small NoAI brain, at @s). Orbits the body at ~4 b; when its caster picks it: 0.5 s glow',
      '# + vex cue, then a straight ram at the chest (8, electro). Owned ones are linked to the caster (cm/clean removes',
      '# them with it); a test-spawned one (/function rlk:cm/test {t:"ci"}) is its own brain and rams on its own timer.',
      'function rlk:cm/ci/lib/pre',
      'execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/ci/reset',
      'execute if score @s frzT matches 1.. if score @s cmS matches 1.. run function rlk:cm/ci/idle',
      'execute if score @s frzT matches 1.. run return 0',
      'execute if score @s cmS matches 1 run return run function rlk:cm/ci/r_tell',
      'execute if score @s cmS matches 2 run return run function rlk:cm/ci/r_fly',
      'execute if score @s cmS matches 3 run function rlk:cm/ci/r_back',
      'function rlk:cm/ci/orbit',
      'execute if score @s c2eOw matches 0 if score @s cmS matches 0 if score @s cmCd matches ..0 if score #free tmp matches 1 run function rlk:cm/ci/r_start')
    f('own_tick', '# an owned cicin, ticked by its caster (cc/flock_one); it keeps its own rig synced',
      'tag @s add rlk_cmsync', 'function rlk:cm/ci/tick', 'function rlk:cm/ci/rig/tick')
    f('orbit', f'# toward the ring point (r {c["orbit_r"]}, 1.2 b up; r 2.5 when that is inside a block) at 0.4 b/tick, never into a block',
      f'scoreboard players add @s c2eA {c["orbit_deg"]}',
      f'execute if score #eStep tmp matches 2 run scoreboard players add @s c2eA {c["orbit_deg"]}',
      'execute if score @s c2eA matches 360.. run scoreboard players remove @s c2eA 360',
      'execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 1 run scoreboard players get @s c2eA',
      f'execute positioned as @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^1.2 ^{c["orbit_r"]} run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~',
      'execute at @e[tag=rlk_cmrot,limit=1] unless block ~ ~ ~ #rlk:dash_pass run return run function rlk:cm/ci/orbit_near',
      'execute at @e[tag=rlk_cmrot,limit=1] unless block ~ ~0.5 ~ #rlk:dash_pass run return run function rlk:cm/ci/orbit_near',
      'function rlk:cm/ci/orbit_go')
    f('orbit_near', 'execute positioned as @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^1.2 ^2.5 run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~',
      'execute at @e[tag=rlk_cmrot,limit=1] unless block ~ ~ ~ #rlk:dash_pass run return 0',
      'execute at @e[tag=rlk_cmrot,limit=1] unless block ~ ~0.5 ~ #rlk:dash_pass run return 0',
      'function rlk:cm/ci/orbit_go')
    f('orbit_go', 'execute if entity @e[tag=rlk_cmrot,distance=..0.45] run return run tp @s @e[tag=rlk_cmrot,limit=1]',
      'execute facing entity @e[tag=rlk_cmrot,limit=1] feet positioned ^ ^ ^0.4 if block ~ ~0.05 ~ #rlk:dash_pass if block ~ ~0.5 ~ #rlk:dash_pass run tp @s ~ ~ ~')
    f('r_start', '# picked by its caster (or its own timer when summoned alone for a test)',
      'scoreboard players set @s cmS 1', f'scoreboard players set @s cmT {c["tell"]}', 'tag @s add rlk_c2_busy',
      f'scoreboard players set @s cmCd {c["solo_cd"]}',
      'particle minecraft:electric_spark ~ ~0.5 ~ 0.2 0.2 0.2 0.05 8', ps('entity.vex.charge', 0.9, 1.4))
    f('r_tell', 'scoreboard players operation @s cmT -= #eStep tmp', 'particle minecraft:electric_spark ~ ~0.5 ~ 0.15 0.15 0.15 0.02 2',
      'execute if score @s cmT matches ..0 run function rlk:cm/ci/r_go')
    f('r_go', '# lock the ram line now: from its centre to the chest',
      'execute positioned ~ ~0.45 ~ facing entity @e[tag=rlk_cmaim,limit=1] feet positioned ~ ~-0.45 ~ run tp @s ~ ~ ~ ~ ~',
      'scoreboard players set @s cmS 2', f'scoreboard players set @s cmT {c["fly"]}', ps('entity.breeze.shoot', 0.8, 1.6))
    f('r_fly', 'scoreboard players operation @s cmT -= #eStep tmp', 'scoreboard players set #c2s tmp 2',
      'function rlk:cm/ci/r_step', 'execute at @s run particle minecraft:electric_spark ~ ~0.45 ~ 0.05 0.05 0.05 0 2',
      'execute if score @s cmS matches 2 if score @s cmT matches ..0 run function rlk:cm/ci/r_end')
    f('r_step', 'execute at @s positioned ^ ^ ^0.4 unless block ~ ~0.45 ~ #rlk:dash_pass run return run function rlk:cm/ci/r_end',
      'execute at @s positioned ^ ^ ^0.4 unless block ~ ~0.05 ~ #rlk:dash_pass run return run function rlk:cm/ci/r_end',
      'execute at @s run tp @s ^ ^ ^0.4',
      'execute at @s positioned ~ ~0.45 ~ if entity @e[tag=rlk_cmaim,distance=..0.9] run return run function rlk:cm/ci/r_hit',
      'scoreboard players remove #c2s tmp 1', 'execute if score #c2s tmp matches 1.. run function rlk:cm/ci/r_step')
    f('r_hit', f'scoreboard players set #cmDmg tmp {c["ram_dmg"]}', 'scoreboard players set #cmEl tmp 3',
      'scoreboard players operation #cmLv tmp = @s mlv', 'function rlk:cm/hit_pl',
      'execute at @s run particle minecraft:electric_spark ~ ~0.45 ~ 0.3 0.3 0.3 0.1 12', 'function rlk:cm/ci/r_end')
    f('r_end', 'scoreboard players set @s cmS 3', 'scoreboard players set @s cmT 12')
    f('r_back', 'scoreboard players operation @s cmT -= #eStep tmp', 'execute if score @s cmT matches ..0 run function rlk:cm/ci/idle')
    L.rig(w, 'ci', tp_dur=1, bright_all=True, death=[(0, 60), (4, None)],
          die_fx='particle minecraft:electric_spark ~ ~0.5 ~ 0.25 0.25 0.25 0.12 14\n' + ps('entity.vex.death', 0.6, 1.6))
    f('rig/face', '# yaw toward the body; while ramming, along the locked ram line',
      'execute if score @s cmS matches 2 rotated as @s rotated ~ 0 as @e[tag=rlk_ci_this] run tp @s ~ ~ ~ ~ 0',
      'execute unless score @s cmS matches 2 facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_ci_this] run tp @s ~ ~ ~ ~ 0')
    f('rig/choose', 'scoreboard players add @s cmAF 1', 'execute if score @s cmAF matches 6.. run scoreboard players set @s cmAF 0',
      'scoreboard players operation #c2p tmp = @s cmAF', 'scoreboard players operation #c2p tmp /= #3 tmp',
      'execute if score @s cmS matches 1 run scoreboard players set #c2p tmp 2',
      'execute if score @s cmS matches 2 run scoreboard players set #c2p tmp 3')
