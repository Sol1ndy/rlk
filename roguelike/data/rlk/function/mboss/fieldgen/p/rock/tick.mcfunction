# rock tick.
execute if score #fgPT mb matches 1..11 run execute at @s unless entity @e[tag=rlk_body,distance=..5] run function rlk:mboss/fieldgen/u/toward {d:0.2}
execute if score #fgPT mb matches 1..140 run function rlk:mboss/fieldgen/rig/face/track
execute as @e[type=minecraft:item_display,tag=rlk_mb_fg_p6s] at @s run function rlk:mboss/fieldgen/p/rock/rk_slab
scoreboard players operation #fgM mb = #fgPT mb
scoreboard players operation #fgM mb %= #fgK2 mb
execute if score #fgM mb matches 0 as @e[type=minecraft:item_display,tag=rlk_mb_fg_p6f] at @s rotated as @s run function rlk:mboss/fieldgen/fx/p/slab_trail
execute if score #fgPT mb matches 12..75 run return run function rlk:mboss/fieldgen/p/rock/d/12_75
execute if score #fgPT mb matches 81..158 run return run function rlk:mboss/fieldgen/p/rock/d/81_158
