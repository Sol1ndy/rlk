"""Raiden blinks (footage A-19, plan rd/plan.md A.2: she never walks; she closes distance only by a 16 t blink).

A blink plays the rig clip blink_out (t_blink_out in the Tenma form: gone at its tick 4) with the kit cue
fx/blink_out where she stands, relocates her while she is invisible, then plays blink_in (t_blink_in: visible from its
tick 3, settled at 8) with fx/blink_in at the destination. combat/apply keeps her immune while rdBlink is 1.. .

    movement/blink_start   @s = boss: blink to the rlk_rd_blink_dest marker if one exists, else in front of the player
                           (core blink_relocate). A blink already running is not restarted.
    movement/blink_to      @s = boss, the execution position is the destination (pulled in to radius 20).
    movement/blink_tick    core tick while rdBlink 1..: rdBlink 2..9 is the blink (relocation at 6), 20..29 a plain
                           immune hold that patterns set themselves (e.g. 몽상의 일심 sets 24 for her first 6 t).
    movement/depart|arrive the cue helpers alone (fx/blink_out | fx/blink_in at @s); never move her.
    movement/cleanup       pause / exhausted / death: no destination marker, no blink.

The release's walking helpers and its 12 silhouette-fragment models (fx_movement/*) are gone (S2-SHOGUN); the
--resourcepack argument is still accepted so build_raiden_all.py keeps working, and nothing is written to the pack.
"""
from pathlib import Path
import argparse


def build(datapack):
    out = Path(datapack) / 'data/rlk/function/boss/raiden/movement'

    def fn(name, lines):
        p = out / (name + '.mcfunction')
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    fn('init', [f'scoreboard objectives add {name} dummy' for name in ('rdBlink', 'rdWalk', 'rdWalkDir')])
    fn('cleanup', ['kill @e[tag=rlk_rd_blink_dest]',
                   'scoreboard players set @e[tag=rlk_raiden] rdBlink 0',
                   'scoreboard players set @e[tag=rlk_raiden] rdWalk 0'])
    fn('blink_start', [
        '# @s boss where it stands. Immune while rdBlink 1.. (combat/apply); relocates at rdBlink 6 (4 t later).',
        'execute if score @s rdBlink matches 1.. run return 0',
        'scoreboard players set @s rdWalk 0',
        'scoreboard players set @s rdBlink 1',
        'execute if score @s rdPhase matches 2 run function rlk:boss/raiden/rig/play/t_blink_out',
        'execute unless score @s rdPhase matches 2 run function rlk:boss/raiden/rig/play/blink_out',
        'execute at @s run function rlk:boss/raiden/fx/blink_out',
    ])
    fn('blink_to', [
        '# @s boss; the execution position is the destination, pulled in to radius 20 about the arena centre.',
        'kill @e[tag=rlk_rd_blink_dest]',
        'summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_blink_dest"]}',
        'execute as @e[tag=rlk_rd_blink_dest] at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..20] '
        'facing entity @s feet rotated ~ 0 positioned ^ ^ ^20 run tp @s ~ ~ ~',
        '# A blink that has not relocated yet simply takes the new destination.',
        'execute if score @s rdBlink matches 1..5 run return 0',
        'scoreboard players set @s rdBlink 0',
        'execute at @s run function rlk:boss/raiden/movement/blink_start',
    ])
    fn('blink_tick', [
        '# Core tick, as the boss, while rdBlink 1.. .',
        'execute unless score @s rdBlink matches 1.. run return 0',
        'scoreboard players add @s rdBlink 1',
        'execute if score @s rdBlink matches 6 run function rlk:boss/raiden/movement/blink_land',
        'execute if score @s rdBlink matches 10..19 run scoreboard players set @s rdBlink 0',
        'execute if score @s rdBlink matches 30.. run scoreboard players set @s rdBlink 0',
    ])
    fn('blink_land', [
        '# Invisible (blink_out gone at 4): relocate (core blink_relocate), then reappear there.',
        'function rlk:boss/raiden/blink_relocate',
        'execute if score @s rdPhase matches 2 run function rlk:boss/raiden/rig/play/t_blink_in',
        'execute unless score @s rdPhase matches 2 run function rlk:boss/raiden/rig/play/blink_in',
        'execute at @s run function rlk:boss/raiden/fx/blink_in',
    ])
    for kind, cue in (('depart', 'blink_out'), ('arrive', 'blink_in')):
        fn(kind, ['# Pure cue helper: call as boss at @s; never moves the boss or changes rdBlink.',
                  f'function rlk:boss/raiden/fx/{cue}'])
    print('Built the blink helpers (no walking, no pack content).')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--datapack', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--resourcepack', type=Path, help='accepted for build_raiden_all.py; unused')
    args = parser.parse_args()
    build(args.datapack)
