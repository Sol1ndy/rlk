# A8 pattern tick 61.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b20] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4089f,1.5234f,-0.3753f],left_rotation:[-0.8625f,0.3573f,-0.1371f,0.3311f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_55] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_57] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_60,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.4676f,1.5061f,-0.5281f],left_rotation:[-0.7444f,-0.5759f,-0.3352f,0.0428f],scale:[0.1837f,0.22f,1.435f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8r1r58] remove rlk_hr_trg
execute at @s rotated as @s rotated ~ 0 positioned ^0.487 ^1.601 ^-0.498 run function rlk:boss/scarlet/core/sw/rib
