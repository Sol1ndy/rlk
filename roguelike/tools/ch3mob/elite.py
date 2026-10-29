"""Chapter-3 elites (part B): 성수 전갈 (cs), 성수 붉은 독수리 (rv), 원시 정령 기계·재구성자 (pc).

build(w): w(path, text) writes data/rlk/function/<path>.mcfunction. Writes ONLY cm/{cs,rv,pc}/** and cm/spawn/{cs,rv,pc}.
The shared framework lines these mobs need are elite_lib.HOOKS (install_hooks()).

Framework reuse (README 5-1 / 5-2): transparent husk brain (rlk_cmb, cmId) + display rig + the shared lure; damage only via
cm/hit_me / cm/hit_pl (player/take_damage: dodge i-frames, level scaling); cmS is the attack state, so the shared freeze /
player-down cancel (cm/cancel sets cmS 0) is noticed here (rlk_c2_busy) and cleaned up. rlk_cmch (stun immunity) only from
a tell to its hit; every punish window is stunnable. No element immunity, no resistances, no element-gated shield.

* cs  burrows (untargetable: no rlk_mob / rlk_pet / Invulnerable while under, so player attacks, AoE and auto-aim skip it),
      travels on walked safe ground leaving a sand trail, surfaces on a timer under the body's last spot.
* rv  NoAI / NoGravity brain flown by checked 0.32 b steps inside the room box (zone cells + wall top) under a ceiling;
      dives only along a path checked clear onto safe ground.
* pc  scatters and reforms beside the body on a spot walked from the body (safe-ground walker), then slams or spins;
      after two reforms it overheats: tag rlk_c3_core (combat/apply hook: x1.5 damage taken), stunnable.

Tuning: the numbers live in CFG below (raw damage before the level rule, ticks at 20/s).
"""
try:
    from . import elite_lib as L
except ImportError:  # run as a plain module by the temporary runner
    from ch3mob import elite_lib as L

ps = L.ps
CFG = {
    'cs': dict(hp=80, xp=14, speed=0.27, scale=1.1, pinch_tell=10, pinch_gap=6, pinch1=10, pinch2=12, pinch_rec=10, pinch_r=2.7,
               tail_tell=16, tail_lock=6, tail_dmg=20, tail_steps=7, tail_rec=12, tail_range=4.6, cd_a=46,
               dig=10, travel=50, mound=12, erupt_dmg=18, erupt_r=1.8, stuck=24, cd_burrow=150, burrow_min=5.5, stall=6, keep=2.3),
    'rv': dict(hp=55, xp=12, scale=0.9, alt=300, orbit_r=5.5, orbit_deg=3, rise=10, aim=14, lock=6, dive_dmg=18, dive_steps=3,
               grounded=30, takeoff=12, fan_tell=12, fan_dmg=7, fan_rec=8, fe_life=26, cd_dive=140, cd_fan=70, dive_min=3.5,
               dive_max=13, fan_min=5, fan_max=14, box=14, ceil=7),
    'pc': dict(hp=75, xp=14, speed=0.22, scale=1.15, scatter=8, reform=10, slam_tell=14, slam_r=2.5, slam_dmg=18, spin_tell=16,
               spin_r=3.0, spin_dmg=14, rec=8, overheat=30, reforms=2, cd_between=16, cd_after=50, range=14, keep=2.0),
}


def build(w):
    for m in ('cs', 'rv', 'pc'):
        L.lib(w, m, hp=CFG[m]['hp'])
    cs(w)
    rv(w)
    pc(w)


def fnw(w, m):
    return lambda rel, *lines: w(f'cm/{m}/{rel}', '\n'.join(lines))


def husk_spawn(w, m, title, *, scale, speed, xp, nbt=''):
    tags = f'"rlk_room","rlk_zmob","rlk_newmob","rlk_cmb","rlk_cm_{m}","rlk_m_cm{m}","rlk_cmnew","rlk_c3e"'
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


def common(f, m, reset_extra=(), init_extra=(), reset_first=()):
    f('init', '# new brain (@s, at @s): the shared cm init, then this mob\'s rig',
      'function rlk:cm/init', 'scoreboard players set @s cmN 0', 'scoreboard players set @s c2eF 0',
      'scoreboard players set @s cmD 0', *init_extra, f'function rlk:cm/{m}/rig/create')
    f('idle', 'scoreboard players set @s cmS 0', 'tag @s remove rlk_c2_busy', 'tag @s remove rlk_c2_fix', 'tag @s remove rlk_cmch')
    f('reset', '# the attack was cleared from outside (freeze / player down -> cm/cancel set cmS 0): drop what it left behind',
      *reset_first, 'tag @s remove rlk_c2_busy', 'tag @s remove rlk_c2_fix', 'tag @s remove rlk_cmch', *reset_extra,
      'execute if score @s cmCd matches ..19 run scoreboard players set @s cmCd 20')


def hurt_frames(lines_extra=()):
    return ['execute if score @s cmAH matches 4.. run scoreboard players set #c2p tmp 50',
            'execute if score @s cmAH matches 1..3 run scoreboard players set #c2p tmp 51', *lines_extra]


def lock_yaw(target='feet'):
    return ['execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0',
            'execute store result score @s cmYaw run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100',
            'tag @s add rlk_c2_fix']


ROT = 'execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw'
AT_YAW = 'execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0'


def face(f, m):
    f('rig/face', '# displays to the brain; yaw toward the body, or the locked attack yaw cmYaw while rlk_c2_fix',
      'execute if entity @s[tag=rlk_c2_fix] store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw',
      f'execute if entity @s[tag=rlk_c2_fix] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 as @e[tag=rlk_{m}_this] run tp @s ~ ~ ~ ~ 0',
      f'execute unless entity @s[tag=rlk_c2_fix] facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_{m}_this] run tp @s ~ ~ ~ ~ 0')


def ring(r, part, n=12, y=0.1):
    return [f'execute rotated {a * 360 // n} 0 positioned ^ ^{y} ^{r} run particle {part} ~ ~ ~ 0.02 0 0.02 0 1' for a in range(n)]


SAND = 'minecraft:block{block_state:"minecraft:sand"}'
RSAND = 'minecraft:falling_dust{block_state:"minecraft:red_sand"}'


# ============================================================================================== 성수 전갈
def cs(w):
    c, f = CFG['cs'], fnw(w, 'cs')
    husk_spawn(w, 'cs', '성수 전갈', scale=c['scale'], speed=c['speed'], xp=c['xp'])
    common(f, 'cs', reset_extra=['execute if entity @s[tag=rlk_c3_under] run function rlk:cm/cs/surface'])
    f('tick', '# 성수 전갈 (@s = brain, at @s; cm/tick hook). Burrow: dig 0.5 s -> sand trail toward the body (untargetable) ->',
      '# trail stops, mound shakes 0.6 s -> erupts there (uppercut 18) -> stuck 1.2 s (punish). Close: pincer 0.5 s -> 10 + 12.',
      '# Mid range: tail charge 0.8 s (aim locks for the last 0.3 s) -> electro stab 20 along a short line.',
      'function rlk:cm/cs/lib/pre',
      'execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/cs/reset',
      'execute if score @s cmS matches 1 run return run function rlk:cm/cs/dig',
      'execute if score @s cmS matches 2 run return run function rlk:cm/cs/under',
      'execute if score @s cmS matches 3 run return run function rlk:cm/cs/mound',
      'execute if score @s cmS matches 4 run return run function rlk:cm/cs/stuck',
      'execute if score @s cmS matches 5 run return run function rlk:cm/cs/p_tell',
      'execute if score @s cmS matches 6 run return run function rlk:cm/cs/p_mid',
      'execute if score @s cmS matches 7 run return run function rlk:cm/cs/p_rec',
      'execute if score @s cmS matches 8 run return run function rlk:cm/cs/t_tell',
      'execute if score @s cmS matches 9 run return run function rlk:cm/cs/t_rec',
      f'execute if entity @e[tag=rlk_body,distance=..{c["keep"]}] run scoreboard players set #hold tmp 1',
      'execute if score #free tmp matches 0 run return 0',
      f'execute if score @s cmCd2 matches ..0 unless entity @e[tag=rlk_body,distance=..{c["burrow_min"]}] if entity @e[tag=rlk_body,distance=..28] run return run function rlk:cm/cs/b_start',
      f'execute if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..{c["pinch_r"]}] run return run function rlk:cm/cs/p_start',
      f'execute if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..{c["tail_range"]}] run function rlk:cm/cs/t_start')
    # ---- burrow
    f('b_start', 'scoreboard players set @s cmS 1', f'scoreboard players set @s cmT {c["dig"]}', 'tag @s add rlk_c2_busy',
      'function rlk:cm/ch_begin', f'particle {SAND} ~ ~0.2 ~ 0.7 0.15 0.7 0 30', ps('entity.warden.dig', 0.9, 1.5))
    f('dig', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      f'particle {SAND} ~ ~0.15 ~ 0.6 0.1 0.6 0 6',
      'execute if score @s cmT matches ..0 run function rlk:cm/cs/go_under')
    f('go_under', '# under the sand: no rlk_mob (player attacks / AoE / auto-aim skip it, no health bar), rlk_pet (mob/setup leaves',
      '# it alone), Invulnerable (a stray vanilla hit does nothing). Still rlk_zmob: the room waits for it, it surfaces on a timer.',
      'tag @s add rlk_c3_under', 'tag @s add rlk_pet', 'tag @s remove rlk_mob', 'data merge entity @s {Invulnerable:1b}',
      'tag @s remove rlk_cmch', 'scoreboard players set @s cmS 2', f'scoreboard players set @s cmT {c["travel"]}',
      'scoreboard players set @s cmN 0', ps('block.sand.break', 1, 0.6))
    f('surface', '# targetable again (mob/setup re-adds rlk_mob and the health bar next tick)',
      'tag @s remove rlk_c3_under', 'tag @s remove rlk_pet', 'data merge entity @s {Invulnerable:0b}')
    f('under', '# the trail: one walked 0.5 b step per tick toward the body\'s feet (two with haste); a blocked step tries +-45 deg',
      'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if entity @e[tag=rlk_body,distance=..0.9] run return run function rlk:cm/cs/m_start',
      'summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2cur"]}',
      'scoreboard players set #wK tmp 0',
      'execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 as @e[tag=rlk_c2cur,limit=1] run tp @s ~ ~ ~ ~ 0',
      'scoreboard players operation #wN tmp = #eStep tmp',
      'execute as @e[tag=rlk_c2cur,limit=1] at @s run function rlk:cm/cs/lib/walk_step',
      'execute if score #wK tmp matches 0 facing entity @e[tag=rlk_body,limit=1] feet rotated ~45 0 as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/cs/u_try',
      'execute if score #wK tmp matches 0 facing entity @e[tag=rlk_body,limit=1] feet rotated ~-45 0 as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/cs/u_try',
      'execute if score #wK tmp matches 1.. run tp @s @e[tag=rlk_c2cur,limit=1]',
      'execute if score #wK tmp matches 0 run scoreboard players add @s cmN 1',
      'kill @e[tag=rlk_c2cur]',
      f'execute at @s run particle {SAND} ~ ~0.15 ~ 0.3 0.08 0.3 0 7',
      f'execute at @s run particle {RSAND} ~ ~0.35 ~ 0.25 0.1 0.25 0 2',
      'execute store result score #c2t tmp run scoreboard players get @s cmT', 'scoreboard players operation #c2t tmp %= #3 tmp',
      'execute if score #c2t tmp matches 0 at @s run ' + ps('block.sand.hit', 0.8, 0.7),
      f'execute if score @s cmN matches {c["stall"]}.. run return run function rlk:cm/cs/m_start',
      'execute if score @s cmT matches ..0 run function rlk:cm/cs/m_start')
    f('u_try', 'tp @s ~ ~ ~ ~ 0', 'scoreboard players operation #wN tmp = #eStep tmp', 'execute at @s run function rlk:cm/cs/lib/walk_step')
    f('m_start', f'# the trail stops: a shaking sand mound for {c["mound"]} t marks the eruption spot (still underground)',
      'scoreboard players set @s cmS 3', f'scoreboard players set @s cmT {c["mound"]}', ps('entity.warden.dig', 1, 0.8))
    f('mound', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      f'particle {SAND} ~ ~0.25 ~ 0.6 0.15 0.6 0 8',
      'execute store result score #c2t tmp run scoreboard players get @s cmT', 'scoreboard players operation #c2t tmp %= #2 tmp',
      *['execute if score #c2t tmp matches 0 run ' + x for x in ring(c['erupt_r'], SAND, 10)],
      'execute if score @s cmT matches 4 run ' + ps('block.sand.break', 1, 0.5),
      'execute if score @s cmT matches ..0 run function rlk:cm/cs/erupt')
    f('erupt', '# surfaces right here (a walked safe column) with an uppercut; then stuck in the sand: the punish window',
      'function rlk:cm/cs/surface',
      f'execute if entity @e[tag=rlk_body,distance=..{c["erupt_r"]}] run function rlk:cm/cs/e_dmg',
      f'particle {SAND} ~ ~0.6 ~ 0.9 0.6 0.9 0.15 70', 'particle minecraft:poof ~ ~0.5 ~ 0.7 0.3 0.7 0.05 16',
      'particle minecraft:electric_spark ~ ~1.2 ~ 0.4 0.6 0.4 0.1 12',
      ps('entity.warden.emerge', 0.8, 1.6), ps('entity.player.attack.knockback', 1, 0.6),
      'scoreboard players set @s cmS 4', f'scoreboard players set @s cmT {c["stuck"]}',
      f'scoreboard players set @s cmCd2 {c["cd_burrow"]}', 'execute if score @s cmCd matches ..29 run scoreboard players set @s cmCd 30')
    f('e_dmg', f'scoreboard players set #cmDmg tmp {c["erupt_dmg"]}', 'function rlk:cm/hit_me')
    f('stuck', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      f'execute if score @s cmT matches 12 run particle {SAND} ~ ~0.3 ~ 0.6 0.1 0.6 0 10',
      'execute if score @s cmT matches ..0 run function rlk:cm/cs/idle')
    # ---- pincer combo (front, 2 hits)
    f('p_start', 'scoreboard players set @s cmS 5', f'scoreboard players set @s cmT {c["pinch_tell"]}', 'tag @s add rlk_c2_busy',
      'function rlk:cm/ch_begin', *lock_yaw(), ps('item.crossbow.loading_start', 1, 0.6), ps('entity.spider.ambient', 0.8, 0.7))
    f('p_tell', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      ROT, f'{AT_YAW} run particle minecraft:crit ^-0.9 ^1 ^1.2 0.1 0.1 0.1 0 1',
      f'{AT_YAW} run particle minecraft:crit ^0.9 ^1 ^1.2 0.1 0.1 0.1 0 1',
      'execute if score @s cmT matches 5 run ' + ps('item.crossbow.loading_middle', 1, 0.6),
      'execute if score @s cmT matches ..0 run function rlk:cm/cs/p_hit1')
    pinch_area = f'{AT_YAW} positioned ^ ^ ^1.3 if entity @e[tag=rlk_body,distance=..1.6]'
    f('p_hit1', ROT, f'{pinch_area} run function rlk:cm/cs/p_dmg1', f'{AT_YAW} positioned ^0.5 ^1 ^1.6 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1',
      ps('entity.player.attack.sweep', 0.8, 0.7), 'scoreboard players set @s cmS 6', f'scoreboard players set @s cmT {c["pinch_gap"]}')
    f('p_dmg1', f'scoreboard players set #cmDmg tmp {c["pinch1"]}', 'function rlk:cm/hit_me')
    f('p_mid', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches ..0 run function rlk:cm/cs/p_hit2')
    f('p_hit2', ROT, f'{pinch_area} run function rlk:cm/cs/p_dmg2', f'{AT_YAW} positioned ^-0.5 ^1 ^1.6 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1',
      ps('entity.player.attack.strong', 0.8, 0.7), 'scoreboard players set @s cmS 7', f'scoreboard players set @s cmT {c["pinch_rec"]}',
      'tag @s remove rlk_cmch', f'scoreboard players set @s cmCd {c["cd_a"]}')
    f('p_dmg2', f'scoreboard players set #cmDmg tmp {c["pinch2"]}', 'function rlk:cm/hit_me')
    f('p_rec', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches ..0 run function rlk:cm/cs/idle')
    # ---- tail stab (electro, a short line ahead)
    f('t_start', 'scoreboard players set @s cmS 8', f'scoreboard players set @s cmT {c["tail_tell"]}', 'tag @s add rlk_c2_busy',
      'function rlk:cm/ch_begin', ps('block.respawn_anchor.charge', 0.9, 1.5), ps('entity.spider.ambient', 0.6, 0.5))
    f('t_tell', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'particle minecraft:electric_spark ~ ~2.3 ~ 0.25 0.25 0.25 0.05 3',
      f'execute if score @s cmT matches ..{c["tail_lock"]} unless entity @s[tag=rlk_c2_fix] run function rlk:cm/cs/t_lock',
      'execute if entity @s[tag=rlk_c2_fix] run function rlk:cm/cs/t_line',
      'execute if score @s cmT matches ..0 run function rlk:cm/cs/t_hit')
    f('t_lock', f'# the last {c["tail_lock"]} t: the stab line is fixed and drawn on the ground',
      *lock_yaw(), ps('block.note_block.bit', 0.8, 1.8))
    f('t_line', ROT, 'scoreboard players set #n tmp {}'.format(c['tail_steps']),
      f'{AT_YAW} positioned ^ ^0.1 ^0.6 run function rlk:cm/cs/t_lstep')
    f('t_lstep', 'execute unless block ~ ~0.8 ~ #rlk:dash_pass run return 0',
      'particle minecraft:dust{color:[0.78,0.55,1.0],scale:1.1} ~ ~ ~ 0.05 0 0.05 0 1',
      'scoreboard players remove #n tmp 1', 'execute if score #n tmp matches 1.. positioned ^ ^ ^0.5 run function rlk:cm/cs/t_lstep')
    f('t_hit', ROT, 'scoreboard players set #c2h tmp 0', 'scoreboard players set #n tmp {}'.format(c['tail_steps']),
      f'{AT_YAW} positioned ^ ^0.9 ^0.6 run function rlk:cm/cs/t_ray',
      'execute if score #c2h tmp matches 1 run function rlk:cm/cs/t_dmg',
      ps('item.trident.hit', 1, 0.7), ps('entity.lightning_bolt.impact', 0.4, 1.8),
      'scoreboard players set @s cmS 9', f'scoreboard players set @s cmT {c["tail_rec"]}', 'tag @s remove rlk_cmch',
      f'scoreboard players set @s cmCd {c["cd_a"]}')
    f('t_ray', 'execute unless block ~ ~ ~ #rlk:dash_pass run return 0',
      'particle minecraft:electric_spark ~ ~ ~ 0.08 0.08 0.08 0.02 2',
      'execute if score #c2h tmp matches 0 positioned ~ ~-0.9 ~ if entity @e[tag=rlk_body,distance=..0.95] run scoreboard players set #c2h tmp 1',
      'scoreboard players remove #n tmp 1', 'execute if score #n tmp matches 1.. positioned ^ ^ ^0.5 run function rlk:cm/cs/t_ray')
    f('t_dmg', f'scoreboard players set #cmDmg tmp {c["tail_dmg"]}', 'scoreboard players set #cmEl tmp 3',
      'scoreboard players operation #cmLv tmp = @s mlv', 'function rlk:cm/hit_pl')
    f('t_rec', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches ..0 run function rlk:cm/cs/idle')
    # ---- rig
    L.rig(w, 'cs', tp_dur=2, glow=('sglow',), cull=4.0, death=[(0, 60), (5, 61), (10, 62), (18, 63), (24, None)],
          die_fx='particle minecraft:electric_spark ~ ~0.8 ~ 0.6 0.4 0.6 0.1 24\n' + ps('entity.spider.death', 0.9, 0.6),
          death_fx=f'execute if score @s cmAD matches 18 run particle {SAND} ~ ~0.4 ~ 0.8 0.3 0.8 0 30')
    face(f, 'cs')
    f('rig/walkf', 'scoreboard players operation #c2p tmp = @s cmAF', 'scoreboard players operation #c2p tmp /= #3 tmp',
      'scoreboard players add #c2p tmp 10')
    f('rig/choose', 'scoreboard players add @s cmAF 1', 'execute if score @s cmAF matches 24.. run scoreboard players set @s cmAF 0',
      'execute if score @s cmS matches 1.. run return run function rlk:cm/cs/rig/choose_s',
      'scoreboard players operation #c2p tmp = @s cmAF', 'scoreboard players operation #c2p tmp /= #st6 tmp',
      'execute unless entity @s[tag=rlk_cmhold] unless score @s stunT matches 1.. unless entity @e[tag=rlk_body,distance=..2.4] run function rlk:cm/cs/rig/walkf',
      *hurt_frames())
    f('rig/choose_s', 'execute if score @s cmS matches 1 run scoreboard players set #c2p tmp 21',
      'execute if score @s cmS matches 1 if score @s cmT matches 6.. run scoreboard players set #c2p tmp 20',
      'execute if score @s cmS matches 2 run scoreboard players set #c2p tmp 22',
      'execute if score @s cmS matches 3 run function rlk:cm/cs/rig/moundf',
      'execute if score @s cmS matches 4 run function rlk:cm/cs/rig/stuckf',
      'execute if score @s cmS matches 5 run scoreboard players set #c2p tmp 30',
      'execute if score @s cmS matches 6 run scoreboard players set #c2p tmp 31',
      'execute if score @s cmS matches 7 run scoreboard players set #c2p tmp 33',
      f'execute if score @s cmS matches 7 if score @s cmT matches {c["pinch_rec"] - 3}.. run scoreboard players set #c2p tmp 32',
      'execute if score @s cmS matches 8 run scoreboard players set #c2p tmp 40',
      'execute if score @s cmS matches 9 run scoreboard players set #c2p tmp 42',
      f'execute if score @s cmS matches 9 if score @s cmT matches {c["tail_rec"] - 3}.. run scoreboard players set #c2p tmp 41',
      '# a hit shows the recoil only in the punish window (never over a tell pose)',
      'execute if score @s cmS matches 4 if score @s cmT matches ..16 if score @s cmAH matches 4.. run scoreboard players set #c2p tmp 50')
    f('rig/moundf', 'scoreboard players operation #c2p tmp = @s cmT', 'scoreboard players operation #c2p tmp /= #2 tmp',
      'scoreboard players operation #c2p tmp %= #2 tmp', 'scoreboard players add #c2p tmp 23')
    f('rig/stuckf', 'scoreboard players operation #c2p tmp = @s cmT', 'scoreboard players operation #c2p tmp /= #st6 tmp',
      'scoreboard players operation #c2p tmp %= #2 tmp', 'scoreboard players add #c2p tmp 27',
      f'execute if score @s cmT matches {c["stuck"] - 7}..{c["stuck"] - 4} run scoreboard players set #c2p tmp 26',
      f'execute if score @s cmT matches {c["stuck"] - 3}.. run scoreboard players set #c2p tmp 25')


# ============================================================================================== 성수 붉은 독수리
def rv(w):
    c, f = CFG['rv'], fnw(w, 'rv')
    husk_spawn(w, 'rv', '성수 붉은 독수리', scale=c['scale'], speed=0.0, xp=c['xp'], nbt=',NoAI:1b,NoGravity:1b')
    common(f, 'rv', init_extra=['execute store result score @s c2eA run random value 0..359', 'function rlk:cm/rv/box'],
           reset_extra=['function rlk:cm/rv/tgt_kill', 'tag @s remove rlk_rv_lk'])
    f('tick', '# 성수 붉은 독수리 (@s = NoAI flying brain, at @s). Circles the body ~3 b up inside the room box. Dive: rise + shriek',
      '# 0.5 s -> aim 0.7 s (shadow line on the ground, locked for the last 0.3 s, path checked clear) -> straight dive 18 pyro',
      '# -> crashed 1.5 s (punish) -> takes off. Fan: wings spread 0.6 s -> 5 burning feathers +-30 deg (7 pyro each).',
      'function rlk:cm/rv/lib/pre',
      'execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/rv/reset',
      'execute as @e[tag=rlk_rv_tgt] if score @s cmId = #cid tmp run tag @s add rlk_cmsync',
      'execute if entity @e[tag=rlk_rv_fe,limit=1] run function rlk:cm/rv/fe_all',
      'execute if score @s cmS matches 1 run return run function rlk:cm/rv/d_rise',
      'execute if score @s cmS matches 2 run return run function rlk:cm/rv/d_aim',
      'execute if score @s cmS matches 3 run return run function rlk:cm/rv/dive',
      'execute if score @s cmS matches 4 run return run function rlk:cm/rv/grounded',
      'execute if score @s cmS matches 5 run return run function rlk:cm/rv/takeoff',
      'execute if score @s cmS matches 6 run return run function rlk:cm/rv/f_tell',
      'execute if score @s cmS matches 7 run return run function rlk:cm/rv/f_rec',
      'function rlk:cm/rv/fly',
      'execute if score #free tmp matches 0 run return 0',
      f'execute if score @s cmCd2 matches ..0 if entity @e[tag=rlk_body,distance={c["dive_min"]}..{c["dive_max"]}] if function rlk:cm/rv/d_try run return 0',
      f'execute if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance={c["fan_min"]}..{c["fan_max"]}] run function rlk:cm/rv/f_start')
    # ---- room box: x/z = the fight zone's cells (inside the walls, 0.6 b margin), ceiling = wall top - 3 or spawn + 7
    f('box', '# @s = new brain at its spawn spot. Fallback (no fight zone around it, e.g. a test spawn): +-14 b, spawn + 7 b',
      'execute store result score #px tmp run data get entity @s Pos[0] 100',
      'execute store result score #py tmp run data get entity @s Pos[1] 100',
      'execute store result score #pz tmp run data get entity @s Pos[2] 100',
      'scoreboard players operation @s cmAX = #px tmp', f'scoreboard players remove @s cmAX {c["box"] * 100}',
      'scoreboard players operation @s cmVx = #px tmp', f'scoreboard players add @s cmVx {c["box"] * 100}',
      'scoreboard players operation @s cmAZ = #pz tmp', f'scoreboard players remove @s cmAZ {c["box"] * 100}',
      'scoreboard players operation @s cmVz = #pz tmp', f'scoreboard players add @s cmVz {c["box"] * 100}',
      'scoreboard players operation @s cmVy = #py tmp', f'scoreboard players add @s cmVy {c["ceil"] * 100}',
      'scoreboard players set #bOk tmp 0',
      'execute if score #active room matches 1 as @e[tag=rlk_zone] if score @s zid = #combat room run function rlk:cm/rv/box_zone',
      'execute if score #bOk tmp matches 1 run function rlk:cm/rv/box_set')
    f('box_zone', '# @s = the fight zone marker: bounding box of its cells\' interiors (block coords) and its wall top',
      'data modify storage rlk:c2e bc set from entity @s data.cells',
      'execute store result score #bTop tmp run data get entity @s data.by',
      'scoreboard players set #bx0 tmp 2147483647', 'scoreboard players set #bz0 tmp 2147483647',
      'scoreboard players set #bx1 tmp -2147483648', 'scoreboard players set #bz1 tmp -2147483648',
      'function rlk:cm/rv/box_cell',
      '# usable only when the spawn spot lies inside that box',
      'scoreboard players set #t1 tmp 100', 'scoreboard players operation #bx0 tmp *= #t1 tmp', 'scoreboard players operation #bz0 tmp *= #t1 tmp',
      'scoreboard players operation #bx1 tmp *= #t1 tmp', 'scoreboard players operation #bz1 tmp *= #t1 tmp',
      'scoreboard players add #bx1 tmp 100', 'scoreboard players add #bz1 tmp 100',
      'execute if score #px tmp >= #bx0 tmp if score #px tmp < #bx1 tmp if score #pz tmp >= #bz0 tmp if score #pz tmp < #bz1 tmp run scoreboard players set #bOk tmp 1')
    f('box_cell', 'execute unless data storage rlk:c2e bc[0] run return 0',
      'execute store result score #t1 tmp run data get storage rlk:c2e bc[0].ix0', 'scoreboard players operation #bx0 tmp < #t1 tmp',
      'execute store result score #t1 tmp run data get storage rlk:c2e bc[0].ix1', 'scoreboard players operation #bx1 tmp > #t1 tmp',
      'execute store result score #t1 tmp run data get storage rlk:c2e bc[0].iz0', 'scoreboard players operation #bz0 tmp < #t1 tmp',
      'execute store result score #t1 tmp run data get storage rlk:c2e bc[0].iz1', 'scoreboard players operation #bz1 tmp > #t1 tmp',
      'data remove storage rlk:c2e bc[0]', 'function rlk:cm/rv/box_cell')
    f('box_set', '# walls stand y 201..210 + zone height: the brain\'s feet stay at or below wall top - 3 (its top 1.6 b higher)',
      'scoreboard players operation @s cmAX = #bx0 tmp', 'scoreboard players add @s cmAX 60',
      'scoreboard players operation @s cmVx = #bx1 tmp', 'scoreboard players remove @s cmVx 60',
      'scoreboard players operation @s cmAZ = #bz0 tmp', 'scoreboard players add @s cmAZ 60',
      'scoreboard players operation @s cmVz = #bz1 tmp', 'scoreboard players remove @s cmVz 60',
      'scoreboard players set #t1 tmp 100', 'scoreboard players operation #bTop tmp *= #t1 tmp', 'scoreboard players add #bTop tmp 20700',
      'scoreboard players operation @s cmVy < #bTop tmp')
    # ---- flight
    f('fly', f'# orbit point: {c["orbit_r"]} b from the body at {c["alt"] / 100:g} b over its feet, clamped into the box and under the ceiling',
      'execute if score @s frzT matches 1.. run return 0',
      'execute if score @s stunT matches 1.. run return 0',
      f'scoreboard players add @s c2eA {c["orbit_deg"]}',
      f'execute if score #eStep tmp matches 2 run scoreboard players add @s c2eA {c["orbit_deg"]}',
      'execute if score @s c2eA matches 360.. run scoreboard players remove @s c2eA 360',
      'execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 1 run scoreboard players get @s c2eA',
      f'execute positioned as @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^ ^{c["orbit_r"]} run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~',
      f'scoreboard players set #oUp tmp {c["alt"]}',
      'function rlk:cm/rv/clamp',
      'function rlk:cm/rv/step',
      'execute if score #eStep tmp matches 2 at @s run function rlk:cm/rv/step')
    f('clamp', '# rlk_cmrot += #oUp (x100) in y, then clamped into this bird\'s box (x/z) and under its ceiling (y)',
      'execute store result score #ox tmp run data get entity @e[tag=rlk_cmrot,limit=1] Pos[0] 100',
      'execute store result score #oy tmp run data get entity @e[tag=rlk_cmrot,limit=1] Pos[1] 100',
      'execute store result score #oz tmp run data get entity @e[tag=rlk_cmrot,limit=1] Pos[2] 100',
      'scoreboard players operation #oy tmp += #oUp tmp',
      'scoreboard players operation #ox tmp > @s cmAX', 'scoreboard players operation #ox tmp < @s cmVx',
      'scoreboard players operation #oz tmp > @s cmAZ', 'scoreboard players operation #oz tmp < @s cmVz',
      'scoreboard players operation #oy tmp < @s cmVy',
      'execute store result entity @e[tag=rlk_cmrot,limit=1] Pos[0] double 0.01 run scoreboard players get #ox tmp',
      'execute store result entity @e[tag=rlk_cmrot,limit=1] Pos[1] double 0.01 run scoreboard players get #oy tmp',
      'execute store result entity @e[tag=rlk_cmrot,limit=1] Pos[2] double 0.01 run scoreboard players get #oz tmp')
    f('step', '# one 0.32 b move toward rlk_cmrot; blocked -> slide level, then up (under the ceiling) or down (>= 1.2 b over ground)',
      'execute if entity @e[tag=rlk_cmrot,distance=..0.35] run return 0',
      'execute facing entity @e[tag=rlk_cmrot,limit=1] feet positioned ^ ^ ^0.32 if function rlk:cm/rv/free run return run tp @s ~ ~ ~',
      'execute facing entity @e[tag=rlk_cmrot,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.3 if function rlk:cm/rv/free run return run tp @s ~ ~ ~',
      'execute if function rlk:cm/rv/below_cap positioned ~ ~0.3 ~ if function rlk:cm/rv/free run return run tp @s ~ ~ ~',
      'execute positioned ~ ~-0.3 ~ if block ~ ~-1.2 ~ #rlk:cm_pass if function rlk:cm/rv/free run tp @s ~ ~ ~')
    f('free', '# the bird\'s box at the execution position: feet / body / top and the wing roots (+-0.6 b) are open air',
      'execute unless block ~ ~0.1 ~ #rlk:dash_pass run return 0', 'execute unless block ~ ~0.9 ~ #rlk:dash_pass run return 0',
      'execute unless block ~ ~1.7 ~ #rlk:dash_pass run return 0', 'execute unless block ~0.6 ~1 ~ #rlk:dash_pass run return 0',
      'execute unless block ~-0.6 ~1 ~ #rlk:dash_pass run return 0', 'execute unless block ~ ~1 ~0.6 #rlk:dash_pass run return 0',
      'execute unless block ~ ~1 ~-0.6 #rlk:dash_pass run return 0', 'return 1')
    f('below_cap', 'execute store result score #y tmp run data get entity @s Pos[1] 100', 'scoreboard players add #y tmp 30',
      'execute if score #y tmp > @s cmVy run return 0', 'return 1')
    f('rise', '# straight up by #oUp/100 b if open and under the ceiling',
      'execute unless function rlk:cm/rv/below_cap run return 0',
      'execute positioned ~ ~0.3 ~ if function rlk:cm/rv/free run tp @s ~ ~ ~')
    # ---- dive
    f('d_try', '# only start the dive when a straight dive onto the body\'s spot is open right now (else the fan may go; retry in 0.6 s)',
      'execute unless function rlk:cm/rv/d_pre run scoreboard players set @s cmCd2 12',
      'execute if score @s cmCd2 matches 1.. run return fail', 'function rlk:cm/rv/d_start', 'return 1')
    f('d_pre', 'execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_rv_tsel","rlk_rv_pre"]}',
      'execute as @e[tag=rlk_rv_pre] run function rlk:cm/rv/lib/drop',
      'execute store result score #ok2 tmp run function rlk:cm/rv/d_check',
      'kill @e[tag=rlk_rv_pre]', 'return run scoreboard players get #ok2 tmp')
    f('d_start', 'scoreboard players set @s cmS 1', f'scoreboard players set @s cmT {c["rise"]}', 'tag @s add rlk_c2_busy',
      'function rlk:cm/ch_begin', ps('entity.phantom.ambient', 1, 0.6), ps('entity.ravager.roar', 0.5, 1.8),
      'particle minecraft:flame ~ ~1 ~ 0.6 0.3 0.6 0.02 10')
    f('d_rise', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute store result score #c2t tmp run scoreboard players get @s cmT', 'scoreboard players operation #c2t tmp %= #2 tmp',
      'execute if score #c2t tmp matches 0 run function rlk:cm/rv/rise',
      'execute if score @s cmT matches ..0 run function rlk:cm/rv/d_aim_start')
    f('d_aim_start', 'scoreboard players set @s cmS 2', f'scoreboard players set @s cmT {c["aim"]}',
      'function rlk:cm/rv/tgt_kill',
      'summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_rv_tgt","rlk_cmlink","rlk_cmsync","rlk_c3new"]}',
      'scoreboard players operation @e[tag=rlk_c3new] cmId = #cid tmp', 'tag @e[tag=rlk_c3new] remove rlk_c3new',
      ps('entity.phantom.swoop', 0.7, 1.4))
    f('tgt_kill', 'execute as @e[tag=rlk_rv_tgt] if score @s cmId = #cid tmp run kill @s')
    TS = '@e[tag=rlk_rv_tsel,limit=1]'
    f('d_aim', f'# {c["aim"]} t: the landing point follows the body\'s feet (dropped onto the ground), then locks for the last {c["lock"]} t',
      'scoreboard players operation @s cmT -= #eStep tmp',
      'execute as @e[tag=rlk_rv_tgt] if score @s cmId = #cid tmp run tag @s add rlk_rv_tsel',
      f'execute unless entity {TS} run return run function rlk:cm/rv/d_abort',
      f'execute unless entity @s[tag=rlk_rv_lk] as {TS} at @e[tag=rlk_body,limit=1] run function rlk:cm/rv/d_track',
      f'execute if score @s cmT matches ..{c["lock"]} unless entity @s[tag=rlk_rv_lk] unless function rlk:cm/rv/d_lock run return run function rlk:cm/rv/d_abort',
      'scoreboard players set #lk tmp 0', 'execute if entity @s[tag=rlk_rv_lk] run scoreboard players set #lk tmp 1',
      'scoreboard players set #n tmp 32',
      f'execute at {TS} facing entity @s feet rotated ~ 0 run function rlk:cm/rv/line',
      f'execute if entity @s[tag=rlk_rv_lk] at {TS} run particle minecraft:flame ~ ~0.1 ~ 0.25 0 0.25 0.01 2',
      'execute if score @s cmT matches ..0 run function rlk:cm/rv/d_go',
      'tag @e[tag=rlk_rv_tsel] remove rlk_rv_tsel')
    f('d_track', 'tp @s ~ ~ ~', 'function rlk:cm/rv/lib/drop')
    f('line', '# the dive shadow on the ground: from the landing point back to under the bird (dark; red once locked)',
      'execute positioned ~-0.5 ~ ~-0.5 if entity @s[dx=0,dy=24,dz=0] run return 0',
      'execute if score #lk tmp matches 0 run particle minecraft:dust{color:[0.13,0.05,0.03],scale:1.7} ~ ~0.08 ~ 0.05 0 0.05 0 1',
      'execute if score #lk tmp matches 1 run particle minecraft:dust{color:[0.85,0.16,0.05],scale:1.7} ~ ~0.08 ~ 0.05 0 0.05 0 1',
      'scoreboard players remove #n tmp 1', 'execute if score #n tmp matches 1.. positioned ^ ^ ^0.5 run function rlk:cm/rv/line')
    f('d_lock', 'execute unless function rlk:cm/rv/d_check run return 0', 'tag @s add rlk_rv_lk', ps('block.note_block.bit', 0.8, 0.8), 'return 1')
    f('d_check', '# the landing must be safe ground inside the box and the straight path from the bird to it open (feet + 0.25 / 0.95 / 1.7)',
      f'execute at {TS} unless block ~ ~0.1 ~ #rlk:dash_pass run return 0',
      f'execute at {TS} unless block ~ ~1.1 ~ #rlk:dash_pass run return 0',
      f'execute at {TS} unless block ~ ~1.75 ~ #rlk:dash_pass run return 0',
      f'execute at {TS} if block ~ ~-0.3 ~ #rlk:cm_pass run return 0',
      f'execute store result score #ox tmp run data get entity {TS} Pos[0] 100',
      f'execute store result score #oz tmp run data get entity {TS} Pos[2] 100',
      'execute if score #ox tmp < @s cmAX run return 0', 'execute if score #ox tmp > @s cmVx run return 0',
      'execute if score #oz tmp < @s cmAZ run return 0', 'execute if score #oz tmp > @s cmVz run return 0',
      'scoreboard players set #n tmp 96', 'scoreboard players set #ok tmp 0',
      f'execute facing entity {TS} feet run function rlk:cm/rv/ray',
      'execute if score #ok tmp matches 0 run return 0', 'return 1')
    f('ray', '# 0.2 b steps along the feet path; the brain\'s box (feet + 0.25 / 0.95 / 1.7) must stay in open air',
      f'execute if entity @e[tag=rlk_rv_tsel,distance=..0.25] run return run scoreboard players set #ok tmp 1',
      'execute unless block ~ ~0.25 ~ #rlk:dash_pass run return 0', 'execute unless block ~ ~0.95 ~ #rlk:dash_pass run return 0',
      'execute unless block ~ ~1.7 ~ #rlk:dash_pass run return 0',
      'scoreboard players remove #n tmp 1', 'execute if score #n tmp matches 1.. positioned ^ ^ ^0.2 run function rlk:cm/rv/ray')
    f('d_go', 'scoreboard players set @s cmS 3', 'scoreboard players set @s cmT 40', 'scoreboard players set @s c2eF 0',
      f'execute facing entity {TS} feet rotated ~ 0 run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0',
      'execute store result score @s cmYaw run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100',
      'tag @s add rlk_c2_fix', ps('entity.phantom.swoop', 1, 0.8), ps('entity.blaze.shoot', 0.7, 0.7))
    f('d_abort', '# no clear path / no safe landing (or the mark vanished): no dive this time',
      'function rlk:cm/rv/tgt_kill', 'tag @s remove rlk_rv_lk', 'function rlk:cm/rv/idle',
      'scoreboard players set @s cmCd2 40', 'execute if score @s cmCd matches ..9 run scoreboard players set @s cmCd 10')
    f('dive', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute as @e[tag=rlk_rv_tgt] if score @s cmId = #cid tmp run tag @s add rlk_rv_tsel',
      f'execute unless entity {TS} run return run function rlk:cm/rv/d_abort',
      f'scoreboard players set #c2s tmp {c["dive_steps"]}', f'execute if score #eStep tmp matches 2 run scoreboard players add #c2s tmp 1',
      'function rlk:cm/rv/dv_step',
      'execute at @s run particle minecraft:flame ~ ~0.7 ~ 0.25 0.25 0.25 0.02 4',
      'execute at @s run particle minecraft:large_smoke ~ ~0.7 ~ 0.15 0.15 0.15 0.01 1',
      'execute if score @s cmS matches 3 if score @s cmT matches ..0 run function rlk:cm/rv/d_abort',
      'tag @e[tag=rlk_rv_tsel] remove rlk_rv_tsel')
    f('dv_step', f'execute at @s if entity {TS.replace(",limit=1", ",distance=..0.35")} run return run function rlk:cm/rv/d_land',
      f'execute at @s facing entity {TS} feet positioned ^ ^ ^0.15 unless function rlk:cm/rv/dfree run return run function rlk:cm/rv/d_abort',
      f'execute at @s facing entity {TS} feet positioned ^ ^ ^0.3 unless function rlk:cm/rv/dfree run return run function rlk:cm/rv/d_abort',
      f'execute at @s facing entity {TS} feet run tp @s ^ ^ ^0.3',
      'execute if score @s c2eF matches 0 at @s positioned ~ ~0.6 ~ if entity @e[tag=rlk_cmaim,distance=..1.3] run function rlk:cm/rv/d_hit',
      'scoreboard players remove #c2s tmp 1', 'execute if score #c2s tmp matches 1.. run function rlk:cm/rv/dv_step')
    f('dfree', 'execute unless block ~ ~0.25 ~ #rlk:dash_pass run return 0', 'execute unless block ~ ~0.95 ~ #rlk:dash_pass run return 0',
      'execute unless block ~ ~1.7 ~ #rlk:dash_pass run return 0', 'return 1')
    f('d_hit', f'scoreboard players set #cmDmg tmp {c["dive_dmg"]}', 'scoreboard players set #cmEl tmp 1',
      'scoreboard players operation #cmLv tmp = @s mlv', 'function rlk:cm/hit_pl', 'scoreboard players set @s c2eF 1',
      'execute at @s run particle minecraft:flame ~ ~0.8 ~ 0.4 0.4 0.4 0.08 16', 'execute at @s run ' + ps('entity.blaze.hurt', 0.8, 0.8))
    f('d_land', f'tp @s {TS}', 'function rlk:cm/rv/tgt_kill', 'tag @s remove rlk_rv_lk',
      f'# crashed: {c["grounded"]} t on the ground, stunnable (the punish window)',
      'scoreboard players set @s cmS 4', f'scoreboard players set @s cmT {c["grounded"]}', 'tag @s remove rlk_cmch', 'tag @s remove rlk_c2_fix',
      f'execute at @s run particle {SAND} ~ ~0.2 ~ 0.8 0.15 0.8 0.1 40', 'execute at @s run particle minecraft:flame ~ ~0.3 ~ 0.7 0.1 0.7 0.04 14',
      'execute at @s run particle minecraft:large_smoke ~ ~0.4 ~ 0.6 0.2 0.6 0.02 8',
      'execute at @s run ' + ps('entity.generic.big_fall', 1, 0.7), 'execute at @s run ' + ps('block.fire.extinguish', 0.7, 0.9))
    f('grounded', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches 20 run particle minecraft:crit ~ ~1 ~ 0.3 0.1 0.3 0 5',
      'execute if score @s cmT matches 10 run particle minecraft:crit ~ ~1 ~ 0.3 0.1 0.3 0 5',
      'execute if score @s cmT matches ..0 run function rlk:cm/rv/to_start')
    f('to_start', 'scoreboard players set @s cmS 5', f'scoreboard players set @s cmT {c["takeoff"]}', ps('entity.phantom.flap', 1, 0.7))
    f('takeoff', 'scoreboard players operation @s cmT -= #eStep tmp', 'function rlk:cm/rv/rise',
      'execute if score @s cmT matches ..0 run function rlk:cm/rv/to_end')
    f('to_end', 'function rlk:cm/rv/idle', f'scoreboard players set @s cmCd2 {c["cd_dive"]}',
      'execute if score @s cmCd matches ..29 run scoreboard players set @s cmCd 30')
    # ---- fire-feather fan
    f('f_start', 'scoreboard players set @s cmS 6', f'scoreboard players set @s cmT {c["fan_tell"]}', 'tag @s add rlk_c2_busy',
      'function rlk:cm/ch_begin', ps('entity.phantom.flap', 1, 1.2), ps('item.firecharge.use', 0.8, 1.3))
    f('f_tell', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 run particle minecraft:flame ^1.6 ^1.1 ^0.4 0.1 0.1 0.1 0.01 2',
      'execute facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 run particle minecraft:flame ^-1.6 ^1.1 ^0.4 0.1 0.1 0.1 0.01 2',
      'execute if score @s cmT matches ..0 run function rlk:cm/rv/f_throw')
    aim = 'execute positioned ~ ~0.9 ~ facing entity @e[tag=rlk_cmaim,limit=1] feet positioned ^ ^ ^0.8'
    f('f_throw', '# five burning feathers: -30 / -15 / 0 / +15 / +30 deg around the line to the chest',
      *[f'{aim} rotated ~{a} ~ run function rlk:cm/rv/fe_new' for a in (-30, -15, 0, 15, 30)],
      ps('entity.blaze.shoot', 1, 1.1), ps('entity.phantom.flap', 1, 1.5),
      'scoreboard players set @s cmS 7', f'scoreboard players set @s cmT {c["fan_rec"]}', 'tag @s remove rlk_cmch',
      f'scoreboard players set @s cmCd {c["cd_fan"]}')
    f('f_rec', 'scoreboard players operation @s cmT -= #eStep tmp', 'function rlk:cm/rv/fly',
      'execute if score @s cmT matches ..0 run function rlk:cm/rv/idle')
    f('fe_new', '# @s = bird brain; position / rotation = launch point and flight direction',
      'summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_rv_fe","rlk_cmlink","rlk_cmsync","rlk_c3new"],billboard:"fixed",'
      'item_display:"none",teleport_duration:1,interpolation_duration:1,view_range:1f,shadow_radius:0f,brightness:{sky:15,block:15},'
      'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.1f,1.1f,1.1f],right_rotation:[0f,0f,0f,1f]},'
      'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/rv/feather"}}}',
      'execute as @e[tag=rlk_c3new] run tp @s ~ ~ ~ ~ ~',
      'scoreboard players operation @e[tag=rlk_c3new] cmId = #cid tmp',
      'scoreboard players operation @e[tag=rlk_c3new] cmLv = @s mlv',
      f'scoreboard players set @e[tag=rlk_c3new] cmT {c["fe_life"]}',
      'tag @e[tag=rlk_c3new] remove rlk_c3new')
    f('fe_all', 'execute as @e[tag=rlk_rv_fe] if score @s cmId = #cid tmp at @s run function rlk:cm/rv/fe_step')
    f('fe_step', '# @s = feather: 0.7 b/tick in two checked 0.35 b steps', 'tag @s add rlk_cmsync', 'scoreboard players remove @s cmT 1',
      'scoreboard players set #c2s tmp 2', 'function rlk:cm/rv/fe_move',
      'execute at @s run particle minecraft:small_flame ~ ~ ~ 0.03 0.03 0.03 0 1',
      'execute if score @s cmT matches ..0 run kill @s')
    f('fe_move', 'execute at @s positioned ^ ^ ^0.35 unless block ~ ~ ~ #rlk:dash_pass run return run function rlk:cm/rv/fe_wall',
      'execute at @s run tp @s ^ ^ ^0.35',
      'execute at @s if entity @e[tag=rlk_cmaim,distance=..0.8] run return run function rlk:cm/rv/fe_hit',
      'scoreboard players remove #c2s tmp 1', 'execute if score #c2s tmp matches 1.. run function rlk:cm/rv/fe_move')
    f('fe_wall', 'particle minecraft:flame ~ ~ ~ 0.1 0.1 0.1 0.02 5', ps('block.fire.extinguish', 0.4, 1.6), 'kill @s')
    f('fe_hit', f'scoreboard players set #cmDmg tmp {c["fan_dmg"]}', 'scoreboard players set #cmEl tmp 1',
      'scoreboard players operation #cmLv tmp = @s cmLv', 'function rlk:cm/hit_pl', 'particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.04 8', 'kill @s')
    # ---- rig
    L.rig(w, 'rv', tp_dur=1, glow=('fll', 'flr'), cull=5.0, fall=True, death=[(0, 60), (12, 61), (22, 62), (28, None)],
          die_fx='particle minecraft:flame ~ ~1 ~ 0.5 0.4 0.5 0.05 20\n' + ps('entity.phantom.death', 0.9, 0.7),
          death_fx='execute if score @s cmAD matches 22 run particle minecraft:large_smoke ~ ~0.4 ~ 0.6 0.2 0.6 0.02 16')
    f('rig/face', '# yaw toward the body; while diving, along the locked dive line',
      'execute if entity @s[tag=rlk_c2_fix] store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw',
      'execute if entity @s[tag=rlk_c2_fix] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 as @e[tag=rlk_rv_this] run tp @s ~ ~ ~ ~ 0',
      'execute unless entity @s[tag=rlk_c2_fix] facing entity @e[tag=rlk_cmaim,limit=1] feet rotated ~ 0 as @e[tag=rlk_rv_this] run tp @s ~ ~ ~ ~ 0')
    f('rig/choose', 'scoreboard players add @s cmAF 1', 'execute if score @s cmAF matches 12.. run scoreboard players set @s cmAF 0',
      'scoreboard players operation #c2p tmp = @s cmAF', 'scoreboard players operation #c2p tmp /= #3 tmp',
      'execute if score @s cmS matches 1 run scoreboard players set #c2p tmp 10',
      'execute if score @s cmS matches 2 run scoreboard players set #c2p tmp 11',
      'execute if score @s cmS matches 3 run scoreboard players set #c2p tmp 12',
      'execute if score @s cmS matches 4 run function rlk:cm/rv/rig/crashf',
      'execute if score @s cmS matches 5 run scoreboard players set #c2p tmp 22',
      'execute if score @s cmS matches 6 run scoreboard players set #c2p tmp 30',
      f'execute if score @s cmS matches 7 if score @s cmT matches {c["fan_rec"] - 3}.. run scoreboard players set #c2p tmp 31',
      '# hit recoil only while just flying or crashed (never over a tell pose)',
      'execute if score @s cmS matches 0 if score @s cmAH matches 4.. run scoreboard players set #c2p tmp 50',
      'execute if score @s cmS matches 0 if score @s cmAH matches 1..3 run scoreboard players set #c2p tmp 51',
      'execute if score @s cmS matches 4 if score @s cmAH matches 3.. run scoreboard players set #c2p tmp 52')
    f('rig/crashf', 'scoreboard players operation #c2p tmp = @s cmT', 'scoreboard players operation #c2p tmp /= #st6 tmp',
      'scoreboard players operation #c2p tmp %= #2 tmp', 'scoreboard players add #c2p tmp 20')


# ============================================================================================== 원시 정령 기계·재구성자
def pc(w):
    c, f = CFG['pc'], fnw(w, 'pc')
    husk_spawn(w, 'pc', '원시 정령 기계·재구성자', scale=c['scale'], speed=c['speed'], xp=c['xp'])
    common(f, 'pc', reset_first=['# frozen while overheated: the core stays exposed (and the window keeps running) until its timer ends',
                                 'execute if entity @s[tag=rlk_c3_core] run return run scoreboard players set @s cmS 7'])
    f('tick', '# 원시 정령 기계·재구성자 (@s = brain, at @s). Scatter into cubes 0.4 s -> reform beside the body (0.5 s cube glow at',
      '# the spot, walked from the body) -> hammer slam r 2.5 (0.7 s raised arm + ring, 18) or cube spin r 3 (0.8 s, 14).',
      '# After two reforms: overheated 1.5 s, core exposed (rlk_c3_core: x1.5 damage taken), stunnable.',
      'function rlk:cm/pc/lib/pre',
      'execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/pc/reset',
      'execute if score @s cmS matches 1 run return run function rlk:cm/pc/scatter',
      'execute if score @s cmS matches 2 run return run function rlk:cm/pc/reform',
      'execute if score @s cmS matches 3 run return run function rlk:cm/pc/sl_tell',
      'execute if score @s cmS matches 4 run return run function rlk:cm/pc/after',
      'execute if score @s cmS matches 5 run return run function rlk:cm/pc/sp_tell',
      'execute if score @s cmS matches 6 run return run function rlk:cm/pc/after',
      'execute if score @s cmS matches 7 run return run function rlk:cm/pc/overheat',
      f'execute if entity @e[tag=rlk_body,distance=..{c["keep"]}] run scoreboard players set #hold tmp 1',
      'execute if score #free tmp matches 0 run return 0',
      f'execute if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..{c["range"]}] run function rlk:cm/pc/s_start')
    f('s_start', 'scoreboard players set @s cmS 1', f'scoreboard players set @s cmT {c["scatter"]}', 'tag @s add rlk_c2_busy',
      'function rlk:cm/ch_begin', 'particle minecraft:end_rod ~ ~1.4 ~ 0.6 0.6 0.6 0.08 16',
      'particle minecraft:block{block_state:"minecraft:smooth_quartz"} ~ ~1.4 ~ 0.6 0.6 0.6 0 16',
      ps('block.beacon.deactivate', 0.8, 1.6), ps('block.stone.break', 1, 0.8))
    f('scatter', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches ..0 run function rlk:cm/pc/r_find')
    tries = [90, -90, 135, -135, 45, -45, 180]
    f('r_find', '# beside the body: walk 2 b out from the body\'s feet (sides, back diagonals, front diagonals, behind it), at least',
      '# 1.5 b of walked safe ground; none -> reform where it scattered. The walk starts at the body, so never behind a wall.',
      'scoreboard players set #c2ok tmp 0', 'summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2cur"]}',
      f'function rlk:cm/pc/r_try {{a:{tries[0]}}}',
      *[f'execute if score #c2ok tmp matches 0 run function rlk:cm/pc/r_try {{a:{a}}}' for a in tries[1:]],
      'execute if score #c2ok tmp matches 1 run tp @s @e[tag=rlk_c2cur,limit=1]',
      'kill @e[tag=rlk_c2cur]',
      'scoreboard players set @s cmS 2', f'scoreboard players set @s cmT {c["reform"]}',
      'execute at @s run ' + ps('block.amethyst_block.resonate', 1, 1.3), 'execute at @s run ' + ps('block.beacon.activate', 0.6, 1.8))
    f('r_try', '$execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~$(a) 0 as @e[tag=rlk_c2cur,limit=1] run tp @s ~ ~ ~ ~ 0',
      'execute as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/pc/lib/drop',
      'scoreboard players set #wN tmp 4',
      'execute as @e[tag=rlk_c2cur,limit=1] run function rlk:cm/pc/lib/walk',
      'execute if score #wK tmp matches 3.. run scoreboard players set #c2ok tmp 1')
    f('reform', f'# {c["reform"]} t: the cubes stream in and glow at the spot; then the attack tell',
      'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'particle minecraft:dust{color:[1.0,0.86,0.45],scale:1.3} ~ ~1.2 ~ 0.45 0.7 0.45 0 5',
      'particle minecraft:end_rod ~ ~0.15 ~ 0.6 0.02 0.6 0.01 2',
      *['execute if score @s cmT matches 8 run ' + x for x in ring(1.2, 'minecraft:end_rod', 10)],
      *['execute if score @s cmT matches 4 run ' + x for x in ring(1.2, 'minecraft:end_rod', 10)],
      'execute if score @s cmT matches ..0 run function rlk:cm/pc/pick')
    f('pick', 'execute store result score #c2t tmp run random value 0..1',
      'execute if score #c2t tmp matches 0 run return run function rlk:cm/pc/sl_start', 'function rlk:cm/pc/sp_start')
    f('sl_start', 'scoreboard players set @s cmS 3', f'scoreboard players set @s cmT {c["slam_tell"]}', *lock_yaw(),
      ps('block.beacon.power_select', 0.9, 0.7), ps('entity.iron_golem.repair', 0.8, 0.6))
    ring_slam = ring(c['slam_r'], 'minecraft:dust{color:[1.0,0.84,0.38],scale:1.3}', 16)
    f('sl_tell', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute store result score #c2t tmp run scoreboard players get @s cmT', 'scoreboard players operation #c2t tmp %= #2 tmp',
      ROT, f'execute if score #c2t tmp matches 0 {AT_YAW[len("execute "):]} positioned ^ ^ ^1 run function rlk:cm/pc/sl_ring',
      'execute if score @s cmT matches ..0 run function rlk:cm/pc/sl_hit')
    f('sl_ring', *ring_slam, 'particle minecraft:end_rod ~ ~0.1 ~ 0.3 0 0.3 0 1')
    f('sl_hit', ROT, f'{AT_YAW} positioned ^ ^ ^1 if entity @e[tag=rlk_body,distance=..{c["slam_r"]}] run function rlk:cm/pc/sl_dmg',
      f'{AT_YAW} positioned ^ ^0.2 ^1 run particle minecraft:explosion ~ ~ ~ 0 0 0 0 1',
      f'{AT_YAW} positioned ^ ^0.2 ^1 run particle minecraft:block{{block_state:"minecraft:smooth_quartz"}} ~ ~ ~ 1.2 0.1 1.2 0 40',
      ps('entity.iron_golem.attack', 1, 0.6), ps('entity.generic.explode', 0.4, 1.3),
      'scoreboard players set @s cmS 4', f'scoreboard players set @s cmT {c["rec"]}', 'tag @s remove rlk_cmch')
    f('sl_dmg', f'scoreboard players set #cmDmg tmp {c["slam_dmg"]}', 'function rlk:cm/hit_me')
    f('sp_start', 'scoreboard players set @s cmS 5', f'scoreboard players set @s cmT {c["spin_tell"]}',
      ps('entity.breeze.charge', 1, 0.8), ps('block.beacon.ambient', 1, 1.6))
    f('sp_tell', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute store result score #c2t tmp run scoreboard players get @s cmT', 'scoreboard players operation #c2t tmp %= #2 tmp',
      *['execute if score #c2t tmp matches 0 run ' + x for x in ring(c['spin_r'], 'minecraft:dust{color:[0.55,0.95,0.9],scale:1.3}', 16)],
      'execute if score @s cmT matches ..0 run function rlk:cm/pc/sp_hit')
    f('sp_hit', f'execute if entity @e[tag=rlk_body,distance=..{c["spin_r"]}] run function rlk:cm/pc/sp_dmg',
      *[f'execute rotated {a} 0 positioned ^ ^1 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 0 0 0 0 1' for a in range(0, 360, 45)],
      ps('entity.breeze.shoot', 1, 0.7), ps('entity.player.attack.sweep', 1, 0.6),
      'scoreboard players set @s cmS 6', f'scoreboard players set @s cmT {c["rec"]}', 'tag @s remove rlk_cmch')
    f('sp_dmg', f'scoreboard players set #cmDmg tmp {c["spin_dmg"]}', 'function rlk:cm/hit_me')
    f('after', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute if score @s cmT matches ..0 run function rlk:cm/pc/after_end')
    f('after_end', 'scoreboard players add @s cmN 1',
      f'execute if score @s cmN matches {c["reforms"]}.. run return run function rlk:cm/pc/oh_start',
      'function rlk:cm/pc/idle', f'scoreboard players set @s cmCd {c["cd_between"]}')
    f('oh_start', f'# overheated: {c["overheat"]} t in place, core exposed (rlk_c3_core: every hit x1.5), stunnable (the punish window)',
      'scoreboard players set @s cmS 7', f'scoreboard players set @s cmT {c["overheat"]}', 'scoreboard players set @s cmN 0',
      'tag @s add rlk_c3_core', 'tag @s remove rlk_cmch', 'tag @s remove rlk_c2_fix',
      'particle minecraft:cloud ~ ~1.6 ~ 0.4 0.4 0.4 0.05 12', 'particle minecraft:lava ~ ~1.5 ~ 0.3 0.3 0.3 0 4',
      ps('block.fire.extinguish', 1, 0.6), ps('block.beacon.deactivate', 0.9, 0.7))
    f('overheat', 'scoreboard players set #hold tmp 1', 'scoreboard players operation @s cmT -= #eStep tmp',
      'execute store result score #c2t tmp run scoreboard players get @s cmT', 'scoreboard players operation #c2t tmp %= #3 tmp',
      'execute if score #c2t tmp matches 0 run particle minecraft:cloud ~ ~2 ~ 0.25 0.2 0.25 0.03 2',
      'execute if score #c2t tmp matches 0 run particle minecraft:flame ~ ~1.45 ~ 0.25 0.25 0.25 0.01 2',
      'execute if score @s cmT matches 15 run ' + ps('block.lava.extinguish', 0.6, 1.2),
      'execute if score @s cmT matches ..0 run function rlk:cm/pc/oh_end')
    f('oh_end', 'tag @s remove rlk_c3_core', 'function rlk:cm/pc/idle', f'scoreboard players set @s cmCd {c["cd_after"]}',
      ps('block.beacon.activate', 0.7, 1.5))
    f('core_hit', '# combat/apply hook (@s = this brain, while rlk_c3_core): the exposed core takes x1.5 from every hit',
      'scoreboard players operation #dmg tmp *= #3 tmp', 'scoreboard players operation #dmg tmp /= #2 tmp',
      'particle minecraft:crit ~ ~1.5 ~ 0.25 0.25 0.25 0.3 8', ps('block.amethyst_block.hit', 0.6, 0.7))
    # ---- rig
    L.rig(w, 'pc', tp_dur=1, glow=('core',), cull=4.0, death=[(0, 60), (14, 61), (22, None)],
          die_fx='particle minecraft:end_rod ~ ~1.4 ~ 0.6 0.6 0.6 0.06 20\n' + ps('block.beacon.deactivate', 1, 0.6) + '\n' + ps('block.stone.break', 1, 0.6),
          death_fx='execute if score @s cmAD matches 14 run particle minecraft:block{block_state:"minecraft:smooth_quartz"} ~ ~0.4 ~ 0.8 0.2 0.8 0 30')
    face(f, 'pc')
    f('rig/choose', 'scoreboard players add @s cmAF 1', 'execute if score @s cmAF matches 32.. run scoreboard players set @s cmAF 0',
      'execute if score @s cmS matches 1.. run return run function rlk:cm/pc/rig/choose_s',
      'scoreboard players operation #c2p tmp = @s cmAF', 'scoreboard players operation #c2p tmp /= #4 tmp',
      'execute unless entity @s[tag=rlk_cmhold] unless score @s stunT matches 1.. unless entity @e[tag=rlk_body,distance=..2.6] run scoreboard players add #c2p tmp 10',
      'execute if score @s cmAH matches 4.. run scoreboard players set #c2p tmp 55',
      'execute if score @s cmAH matches 1..3 run scoreboard players set #c2p tmp 56')
    f('rig/choose_s', 'execute if score @s cmS matches 1 run scoreboard players set #c2p tmp 20',
      'execute if score @s cmS matches 2 run scoreboard players set #c2p tmp 22',
      f'execute if score @s cmS matches 2 if score @s cmT matches {c["reform"] - 1}.. run scoreboard players set #c2p tmp 21',
      'execute if score @s cmS matches 3 run scoreboard players set #c2p tmp 30',
      'execute if score @s cmS matches 4 run scoreboard players set #c2p tmp 32',
      f'execute if score @s cmS matches 4 if score @s cmT matches {c["rec"] - 2}.. run scoreboard players set #c2p tmp 31',
      'execute if score @s cmS matches 5 run scoreboard players set #c2p tmp 40',
      'execute if score @s cmS matches 6 run scoreboard players set #c2p tmp 44',
      f'execute if score @s cmS matches 6 if score @s cmT matches {c["rec"] - 1}.. run scoreboard players set #c2p tmp 41',
      f'execute if score @s cmS matches 6 if score @s cmT matches {c["rec"] - 3}..{c["rec"] - 2} run scoreboard players set #c2p tmp 42',
      f'execute if score @s cmS matches 6 if score @s cmT matches {c["rec"] - 5}..{c["rec"] - 4} run scoreboard players set #c2p tmp 43',
      'execute if score @s cmS matches 7 run function rlk:cm/pc/rig/heatf')
    f('rig/heatf', 'scoreboard players operation #c2p tmp = @s cmT', 'scoreboard players operation #c2p tmp /= #st6 tmp',
      'scoreboard players operation #c2p tmp %= #2 tmp', 'scoreboard players add #c2p tmp 50')
