# @s = body. One AI state per tick (the pattern slot runs after it, see p/run).
execute if score #fgSt mb matches 0 run return run function rlk:mboss/fieldgen/ai/idle
execute if score #fgSt mb matches 3 run return run function rlk:mboss/fieldgen/groggy/tick
execute if score #fgSt mb matches 4 run return run function rlk:mboss/fieldgen/recover/tick
execute if score #fgSt mb matches 6 run return run function rlk:mboss/fieldgen/brk/tick
