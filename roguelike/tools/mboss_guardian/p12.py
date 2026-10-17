"""P1 공간 찌르기 (two thrusts) and P2 공간 투창 – 심판하는 파수꾼 (javelin).

STUB QUALITY: both patterns already play the right rig clips, deal their damage on the clip's hit
ticks through framework hazards with >= 12 t telegraphs (K4), move the body where the clip expects
it and use the planned coefficients. Still to author (patterns.md §3, §4; plan.md K4, K16, K23):
  P1  the gold charge streak along the shaft (4-16), the glint flare (19), the hit-1 burst sphere and
      shock-ring arc, the hit-2 streak along the dash, dark cubes and rock debris; a line decal that
      reads better than the framework particles; the exact fly-back path (4-6 b, 2-3 b up).
  P2  the rotating 4-point glyph (11-27) compressing into a ring, the vertical beam (28), the release
      explosion and launch disc (35-37), the trail (39-43), tumbling cubes; the prop timing so the spear
      returns along the line by clip tick 58-63.
Owner of this file: the P1/P2 pattern author. Write only through gen.pw(key, ...).
"""
from .api import Pattern, ev, clip_len, DMG, KB, CY, GOLD, GOLD_PALE

PATTERNS = [
    Pattern(1, 'thrust', '공간 찌르기', bands=('melee', 'mid'), recover=18, max_len=clip_len('thrust') + 4),
    Pattern(2, 'javelin', '공간 투창', bands=('mid', 'far'), recover=20, max_len=clip_len('javelin') + 4),
]

AIM = 'at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0'


def emit(g):
    thrust(g)
    javelin(g)


def thrust(g):
    k = 'thrust'
    h1, h2 = ev(k, 'hit1'), ev(k, 'hit2')
    t1, t2 = h1 - 12, ev(k, 'rise') + 4             # line decals: 12 t before hit 1, 16 t before hit 2
    g.pw(k, 'start', [
        '# P1 start (@s = body, #gdPT 0): face the player, thrust clip (91 t: glow 4, glint 19, hit1 28, rise 38,',
        '# dive 54, hit2 58, land 65, flourish 72).',
        g.rig('face/player'),
        g.play(k),
        g.sound('block.beacon.power_select', 0.35, 1.8)])
    g.pw(k, 'tick', [
        '# P1 tick (@s = body, #gdPT = clip tick).',
        g.at((4, 16), 'execute rotated as @s rotated ~ 0 run ' + g.dust(GOLD, 0.9, '^-0.5 ^2.0 ^1.2', (0.3, 0.1, 0.3), 2)),
        g.at(7, g.sound('block.amethyst_block.chime', 0.6, 1.9)),
        # thrust 1: aim locked t1, 12 t line decal, lunge 2.7 b at 26-28
        g.at(t1, f'execute {AIM} run tp @s ~ ~ ~ ~ 0'),
        g.at(t1, 'scoreboard players set #hzSfx mb 3'),
        g.at(t1, f'execute {AIM} positioned ~ {CY} ~ run {g.hz_line(5.5, 2.2, h1 - t1, DMG["p1a"])}'),
        g.at(ev(k, 'glint'), 'execute rotated as @s rotated ~ 0 run ' + g.card('star', '^-0.4 ^1.9 ^2.6', bb='center', spin=45, s0=0.1, s1=0.9, life=6, fade=3)),
        g.at((h1 - 2, h1), 'function rlk:mboss/mv/step {d:0.9}'),
        g.at(h1, 'execute rotated as @s rotated ~ 0 run ' + g.card('burst', '^ ^1.2 ^1.6', bb='center', spin=20, s0=0.6, s1=2.6, life=5, fade=2)),
        g.at(h1, g.sound('item.trident.hit', 1.0, 0.8)),
        g.at(h1, g.sound('block.amethyst_cluster.break', 0.9, 1.0)),
        g.at(h1, g.sound('entity.generic.explode', 0.4, 1.6)),
        # fly back 4 b, then thrust 2 from the new spot: 16 t line decal, dash 5.6 b at 57-58
        g.at((ev(k, 'rise'), ev(k, 'dive')), 'function rlk:mboss/mv/away {d:0.25}'),
        g.at(t2, f'execute {AIM} run tp @s ~ ~ ~ ~ 0'),
        g.at(t2, 'scoreboard players set #hzSfx mb 3'),
        g.at(t2, f'scoreboard players set #hzKB mb {KB["p1b"]}'),
        g.at(t2, f'execute {AIM} positioned ~ {CY} ~ run {g.hz_line(7.0, 2.0, h2 - t2, DMG["p1b"])}'),
        g.at(ev(k, 'dive'), g.sound('entity.player.attack.sweep', 0.8, 0.7)),
        g.at((h2 - 1, h2), 'function rlk:mboss/mv/step {d:2.8}'),
        g.at(h2, 'execute rotated as @s rotated ~ 0 run ' + g.card('burst', '^ ^1.0 ^1.2', bb='center', spin=20, s0=0.6, s1=2.8, life=5, fade=2)),
        g.at(h2, g.sound('item.trident.hit', 1.0, 0.75)),
        g.at(h2, g.sound('entity.generic.explode', 0.45, 1.5)),
        g.at(ev(k, 'flourish'), g.sound('item.trident.riptide_1', 0.5, 1.4)),
        g.at(clip_len(k), g.end())])
    g.pw(k, 'cancel', ['# P1 cancel: it owns no entities (hazards go with lib_clear).'])


def javelin(g):
    k = 'javelin'
    rel, launch = ev(k, 'release'), ev(k, 'launch')
    lock = launch - 12                               # K23 + K4: aim locked, 12 t line decal, hit at the launch
    g.pw(k, 'start', [
        '# P2 start (@s = body): face the player, javelin clip (76 t: spin 0, vanish 10, glyph 11, beam 28,',
        '# rematerialise 31, release 35, launch 36, return 58, catch 63; the rig spear is hidden 10-31 and 36-63).',
        g.rig('face/player'),
        g.play(k),
        g.sound('entity.player.attack.sweep', 0.7, 0.7),
        g.sound('item.trident.riptide_1', 0.4, 1.4)])
    g.pw(k, 'tick', [
        '# P2 tick (@s = body, #gdPT = clip tick). Damage comes from the line; the flying spear is visual only.',
        g.at(ev(k, 'vanish'), g.sound('entity.player.attack.sweep', 0.7, 0.8)),
        g.at(ev(k, 'glyph'), g.sound('block.amethyst_block.resonate', 0.8, 1.3)),
        g.at((ev(k, 'glyph'), ev(k, 'beam')), 'execute rotated as @s rotated ~ 0 run ' + g.dust(GOLD, 1.0, '^-1.5 ^1.5 ^0.3', (0.25, 0.25, 0.05), 2)),
        g.at(lock, f'execute {AIM} run tp @s ~ ~ ~ ~ 0'),
        g.at(lock, 'scoreboard players set #hzSfx mb 3'),
        g.at(lock, 'scoreboard players set #hzAct mb 2'),
        g.at(lock, f'scoreboard players set #hzKB mb {KB["light"]}'),
        g.at(lock, f'execute {AIM} positioned ~ {CY} ~ run {g.hz_line(40.0, 1.0, launch - lock, DMG["p2"])}'),
        g.at(ev(k, 'beam'), 'execute rotated as @s rotated ~ 0 run ' + g.dust(GOLD_PALE, 1.6, '^-1.5 ^1.5 ^0.3', (0.05, 1.2, 0.05), 20)),
        g.at(ev(k, 'beam'), g.sound('block.beacon.activate', 0.6, 1.8)),
        g.at(rel, g.voice_attack()),
        g.at(rel, g.sound('item.trident.throw', 1.0, 0.7)),
        g.at(rel, g.sound('entity.firework_rocket.blast', 0.8, 1.2)),
        g.at(launch, g.fn('p/javelin/throw')),
        g.at(ev(k, 'catch'), g.sound('item.trident.return', 0.8, 0.8)),
        g.at(clip_len(k), g.end())])
    g.pw(k, 'throw', [
        '# @s = body: the visual spear (rig prop, tip turned forward) flies 3 b/t for 9 t and returns (pj, harmless).',
        'execute at @s rotated as @s rotated ~ 0 positioned ^-0.5 ^1.6 ^0.8 run ' + g.rig('prop/spear'),
        'data merge entity @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] {transformation:{left_rotation:[0.7071f,0f,0f,0.7071f]}}',
        'tag @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] add rlk_mb_gd_p2',
        'scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] mbId 2',
        'scoreboard players set #pjRet mb 1',
        'execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] at @s run function rlk:mboss/pj/launch {spd:30,life:9,dmg:0,hr:6}',
        g.sound('item.trident.riptide_2', 0.6, 1.0)])
    g.pw(k, 'cancel', ['# P2 cancel: the flying spear (lib_clear removes it while it is a projectile; this catches the rest).',
                       'kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p2]'])
