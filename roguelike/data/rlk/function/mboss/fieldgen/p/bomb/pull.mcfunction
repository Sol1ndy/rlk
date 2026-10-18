# @s = the route end (facing back to the start): 0.5 b steps back until inside the body disc r 16.5.
execute positioned ~ 201 ~ if entity @e[tag=rlk_mb_arena,distance=..16.5,limit=1] run return 0
scoreboard players add #fq1N mb 1
execute if score #fq1N mb matches 50.. run return 0
execute at @s rotated as @s run tp @s ^ ^ ^0.5
execute at @s run function rlk:mboss/fieldgen/p/bomb/pull
