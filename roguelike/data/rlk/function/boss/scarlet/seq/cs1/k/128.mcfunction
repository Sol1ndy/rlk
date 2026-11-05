# cs1 at #sq 128 (@s = the body).
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_1,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0.725 ^1.85 ^0.9 facing entity @e[tag=rlk_body,limit=1] eyes run tp @s ~ ~ ~ ~ ~
kill @e[type=minecraft:item_display,tag=rlk_hr_sqp_2]
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0.9 ^ ^1.6 positioned ~ 202.62 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqp","rlk_hr_sqp_2"],teleport_duration:1,view_range:2f}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_2,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] eyes run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_2,limit=1] run function rlk:boss/scarlet/fx/prop/petal_big {look:"whole"}
