# A8 pattern tick 83.
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b76] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.1379f,0.6232f,0.2893f],left_rotation:[-0.6864f,-0.6213f,0.23f,0.2998f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_77] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_79] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
execute at @s rotated as @s rotated ~ 0 positioned ^-0.251 ^0.644 ^0.171 run function rlk:boss/scarlet/core/sw/rib
