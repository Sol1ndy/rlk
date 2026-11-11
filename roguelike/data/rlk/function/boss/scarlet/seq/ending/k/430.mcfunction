# ending: the timeline at #sq 430 (@s = the body).
kill @e[type=minecraft:item_display,tag=rlk_hr_sqp_4]
execute at @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] positioned ^1 ^0.35 ^1.2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqp","rlk_hr_sqp_4"],teleport_duration:1,view_range:2f}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_4,limit=1] at @s facing entity @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] feet run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_4,limit=1] run function rlk:boss/scarlet/fx/prop/petal_big {look:"whole"}
