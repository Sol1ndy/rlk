# intro: the timeline at #sq 176 (@s = the body).
function rlk:boss/scarlet/rig/anchor/hand_r
kill @e[type=minecraft:item_display,tag=rlk_hr_sqp_1]
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s rotated ~ 0 positioned ^0 ^0.8 ^0 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_sqp","rlk_hr_sqp_1"],teleport_duration:1,view_range:2f}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_1,limit=1] run function rlk:boss/scarlet/fx/prop/petal_big {look:"whole"}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_1,limit=1] run data merge entity @s {billboard:"center"}
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_1,limit=1] run data merge entity @s {transformation:{scale:[0.42f,0.42f,0.42f]}}
