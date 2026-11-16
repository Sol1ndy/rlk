# Clock 23..154 (@s = body): the eye beam turns 5, the gear beam -5
# degrees (the rig orbit); hz/aim from the body at r 3.0 along the new yaw; spots every 3 t.
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~5 0 positioned ^ ^ ^3 run function rlk:mboss/hz/aim
execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~-5 0 positioned ^ ^ ^3 run function rlk:mboss/hz/aim
scoreboard players operation #fgM mb = #fgPT mb
scoreboard players operation #fgM mb %= #fgK3 mb
execute if score #fgM mb matches 1 run execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3e,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^0.05 ^5.58 run function rlk:mboss/fieldgen/fx/p/laser_spot
execute if score #fgM mb matches 1 run execute as @e[type=minecraft:marker,tag=rlk_mb_fg_p3g,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @s rotated ~ 0 positioned ^ ^0.05 ^5.58 run function rlk:mboss/fieldgen/fx/p/laser_spot
