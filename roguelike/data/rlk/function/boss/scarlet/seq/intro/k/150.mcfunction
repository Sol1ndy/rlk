# intro: the timeline at #sq 150 (@s = the body).
kill @e[type=minecraft:item_display,tag=rlk_hr_sqp_1]
execute at @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] positioned ^0.4 ^0.9 ^1.5 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqp","rlk_hr_sqp_1"],teleport_duration:1,view_range:2f}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_1,limit=1] at @s facing entity @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] feet run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_1,limit=1] run function rlk:boss/scarlet/fx/prop/petal_big {look:"whole"}
function rlk:boss/scarlet/fx/snd/cs0_petals
