# A8 pattern tick 59.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b19] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3839f,1.3566f,-0.4162f],left_rotation:[-0.8735f,0.3618f,-0.1246f,0.3008f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_51]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_55] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_57] remove rlk_hr_trr
execute at @s rotated as @s rotated ~ 0 positioned ^0.456 ^1.428 ^-0.546 run function rlk:boss/scarlet/core/sw/rib
