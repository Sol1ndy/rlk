# Break one living star (as if its pool ran out).
execute as @e[type=minecraft:husk,tag=rlk_mb_gd_star,tag=!rlk_mb_broken,limit=1] run scoreboard players set @s mhpC 0
execute as @e[type=minecraft:husk,tag=rlk_mb_gd_star,tag=!rlk_mb_broken,limit=1] run tag @s add rlk_mb_broken
