# A4 pattern tick 21
function rlk:boss/scarlet/core/cam_clear
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3689f,0.8214f,0.6757f],left_rotation:[-0.2098f,-0.0001f,-0.0004f,-0.9777f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_13]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_15] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_17] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_19] remove rlk_hr_trr
execute at @s rotated as @s rotated ~ 0 positioned ^0.369 ^0.754 ^0.826 run function rlk:boss/scarlet/core/sw/rib
