# S3 break 5: the bubble bursts (crack 4 is the core's): the flash and the glass shards at the core, the gold
# spark ring at the floor, the cracked-bubble pop and a gold flat on the title line.
execute unless score #fgBrkLo mb matches 1 positioned ~ ~4.1 ~ run function rlk:mboss/fieldgen/fx/p/break_burst
execute if score #fgBrkLo mb matches 1 positioned ~ ~1.3 ~ run function rlk:mboss/fieldgen/fx/p/break_burst
execute positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/break_ring
function rlk:mboss/fieldgen/fx/hud/pop_break
function rlk:mboss/fieldgen/fx/hud/flash_gold
function rlk:mboss/fieldgen/fx/snd/break_burst
