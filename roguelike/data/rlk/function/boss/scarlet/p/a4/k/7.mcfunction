# A4 pattern tick 7
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4103f,1.7275f,-0.0558f],left_rotation:[-0.9336f,0f,0f,0.3584f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_3] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_5] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_6,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3989f,1.558f,0.1124f],left_rotation:[-0.6498f,0.6277f,0.2999f,0.3065f],scale:[0.5659f,0.22f,1.8299f],right_rotation:[0f,0f,0f,1f]}}
