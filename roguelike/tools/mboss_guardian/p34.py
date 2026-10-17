"""P3 공간을 집행하는 시련 (melee spear slam) and P4 어둠 속에서 퍼지는 공간 (pull + two 360 swings).

STUB QUALITY: right clips, hits on the clip ticks, planned radii and coefficients, the undodgeable
pull after a 32 t tell. Still to author (patterns.md §5, §6; plan.md K14, K15, K21, K25):
  P3  the gold ellipse ring decal with an amber fill (9-26), the lens glint (12), the vertical gold
      pillar + white-gold flash + radial crystal blades (26-32), sparkles at the planted tip (32-48).
  P4  the red haze and energy arcs behind her (1-14), the black-cube cage stacking up the player
      (11-27, block displays), the screen vignette / white flash / red diamond (26-32: title font glyph
      or darkness), a line-of-sight test before the relocation, the gold crescents of both swings and
      the dark cubes in their trail.
Owner of this file: the P3/P4 pattern author. Write only through gen.pw(key, ...).
"""
from .api import Pattern, ev, clip_len, DMG, KB, CY, GOLD, GOLD_PALE, CRIMSON

SWING_GAP = 12        # relocation -> swing clip start (K15: 10-14 t)
PULL_LEN = clip_len('pull')
SWING_AT = ev('pull', 'relocate') + SWING_GAP

PATTERNS = [
    Pattern(3, 'slam', '공간을 집행하는 시련', bands=('melee',), close=3.0, recover=20, max_len=clip_len('slam') + 4),
    Pattern(4, 'pull', '어둠 속에서 퍼지는 공간', bands=('far',), recover=22, max_len=SWING_AT + clip_len('swing') + 4),
]


def emit(g):
    slam(g)
    pull(g)


def slam(g):
    k = 'slam'
    ring, imp = ev(k, 'ring'), ev(k, 'impact')
    g.pw(k, 'start', [
        '# P3 start (@s = body, already within 3 b after the core\'s close-in): slam clip (70 t: raise 0, ring 9,',
        '# glint 12, down 22, impact 26, pull 48, twirl 54; the spear stays planted 26-48, so the body stays still).',
        g.rig('face/player'),
        g.play(k),
        g.sound('entity.player.attack.sweep', 0.5, 0.6)])
    g.pw(k, 'tick', [
        '# P3 tick (@s = body, #gdPT = clip tick): disc r 5 centred 3.5 b in front (K25), ring lead 17 t.',
        g.at(ring, 'scoreboard players set #hzSfx mb 4'),
        g.at(ring, f'scoreboard players set #hzKB mb {KB["default"]}'),
        g.at(ring, f'execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 positioned ~ {CY} ~ run {g.hz_disc(5.0, imp - ring, DMG["p3"])}'),
        g.at(ev(k, 'glint'), 'execute rotated as @s rotated ~ 0 run ' + g.card('star', '^-0.3 ^4.6 ^0.2', bb='center', spin=60, s0=0.1, s1=1.1, life=8, fade=3)),
        g.at(ev(k, 'glint'), g.sound('block.respawn_anchor.charge', 0.6, 1.5)),
        g.at(imp, 'execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 run ' + g.card('burst', f'~ {CY + 1.2} ~', bb='center', spin=20, s0=0.8, s1=3.4, life=6, fade=3)),
        g.at(imp, 'execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 run ' + g.dust(GOLD_PALE, 1.6, f'~ {CY + 1.5} ~', (0.15, 2.0, 0.15), 24)),
        g.at(imp, 'execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^3.5 run ' + g.particle('block{block_state:"minecraft:gold_block"}', f'~ {CY + 0.3} ~', (2.0, 0.2, 2.0), 0, 30)),
        g.at(imp, g.sound('entity.generic.explode', 0.8, 0.9)),
        g.at(imp, g.sound('block.amethyst_cluster.break', 1.0, 0.9)),
        g.at(imp, g.sound('item.trident.thunder', 0.3, 1.2)),
        g.at(ev(k, 'pull'), g.sound('block.chain.break', 0.8, 0.6)),
        g.at(ev(k, 'pull'), g.sound('block.stone.break', 0.8, 0.8)),
        g.at(ev(k, 'twirl'), g.sound('item.trident.riptide_1', 0.5, 1.4)),
        g.at(clip_len(k), g.end())])
    g.pw(k, 'cancel', ['# P3 cancel: no entities of its own.'])


def pull(g):
    k = 'pull'
    reloc = ev('pull', 'relocate')
    s1 = SWING_AT + ev('swing', 'swing1')
    s2 = SWING_AT + ev('swing', 'swing2')
    tell = 20
    g.pw(k, 'start', [
        '# P4 start (@s = body, player far): pull clip (40 t: aura 0, cage 11, relocate 32), then the swing clip',
        f'# {SWING_GAP} t after the relocation (51 t: swing1 20-24, swing2 33-39). Pull: undodgeable after the 32 t tell (K14).',
        g.rig('face/player'),
        g.play(k),
        g.voice_attack(),
        g.sound('block.respawn_anchor.charge', 0.7, 0.9),
        g.sound('entity.warden.sonic_charge', 0.3, 1.4)])
    g.pw(k, 'tick', [
        '# P4 tick (@s = body, #gdPT = 0..: pull clip ticks, then swing clip ticks + ' + str(SWING_AT) + ').',
        g.at((1, reloc - 1), g.fn('rig/face/track')),
        g.at((1, reloc - 1), 'execute rotated as @s rotated ~ 0 run ' + g.dust(CRIMSON, 1.8, '^ ^1.8 ^-0.6', (0.6, 0.8, 0.3), 2)),
        g.at((ev('pull', 'cage'), reloc - 1), 'execute at @e[tag=rlk_body,limit=1] run ' + g.dust((0.72, 0.18, 0.23), 1.4, '~ ~1 ~', (0.35, 0.9, 0.35), 6)),
        g.at((ev('pull', 'cage'), reloc - 1), 'execute at @e[tag=rlk_body,limit=1] run ' + g.dust((0.06, 0.0, 0.0), 1.2, '~ ~0.6 ~', (0.3, 0.6, 0.3), 3)),
        g.at(reloc - 4, 'effect give @a[tag=player] minecraft:darkness 1 0 true'),
        g.at(reloc, 'execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^1.3 positioned ~ ' + str(CY) + ' ~ run function rlk:mboss/pull/start {t:0}'),
        g.at(reloc, g.sound('entity.enderman.teleport', 0.9, 0.6)),
        g.at(reloc, g.sound('block.respawn_anchor.deplete', 0.8, 1.0)),
        g.at(reloc, g.sound('entity.illusioner.mirror_move', 0.8, 1.0)),
        g.at(SWING_AT, g.play('swing')),
        g.at(SWING_AT, 'scoreboard players set #hzSfx mb 2'),
        g.at(SWING_AT, f'execute at @s positioned ~ {CY} ~ run {g.hz_sector(5.5, 180, tell, DMG["p4"])}'),
        g.at(s2 - tell, 'scoreboard players set #hzSfx mb 2'),
        g.at(s2 - tell, f'execute at @s positioned ~ {CY} ~ run {g.hz_sector(5.5, 180, tell, DMG["p4"])}'),
        g.at(s1, g.particle('sweep_attack', '~ ~1.1 ~', (2.6, 0.1, 2.6), 0, 10)),
        g.at(s1, g.dust(GOLD, 1.2, '~ ~1.1 ~', (2.8, 0.05, 2.8), 30)),
        g.at(s1, g.sound('item.trident.riptide_1', 0.5, 1.4)),
        g.at(s2, g.particle('sweep_attack', '~ ~1.4 ~', (2.6, 0.3, 2.6), 0, 10)),
        g.at(s2, g.dust(GOLD, 1.3, '~ ~1.4 ~', (2.8, 0.3, 2.8), 30)),
        g.at(s2, g.sound('item.trident.riptide_1', 0.5, 1.3)),
        g.at(SWING_AT + clip_len('swing'), g.end())])
    g.pw(k, 'cancel', ['# P4 cancel: the pull point goes with lib_clear; no other entities.'])
