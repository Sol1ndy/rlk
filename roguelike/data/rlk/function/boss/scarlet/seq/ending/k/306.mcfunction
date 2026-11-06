# ending at #sq 306 (@s = the body).
kill @e[type=minecraft:item_display,tag=rlk_hr_sqp_3]
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^1 ^ ^1.4 positioned ~ 202.5 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqp","rlk_hr_sqp_3"],teleport_duration:1,view_range:2f}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] eyes run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3,limit=1] run function rlk:boss/scarlet/fx/prop/petal_big {look:"whole"}
