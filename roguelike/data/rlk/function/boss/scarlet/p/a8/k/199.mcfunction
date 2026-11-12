# A8 pattern tick 199.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_193] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_195] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_197] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_198,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.4501f,1.4549f,0.6352f],left_rotation:[-0.277f,0.1699f,0.5502f,0.7692f],scale:[0.7981f,0.22f,1.7721f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_198,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.4072f,1.4354f,0.605f],left_rotation:[-0.3478f,0.3838f,0.6233f,0.5859f],scale:[0.8129f,0.22f,1.8104f],right_rotation:[0f,0f,0f,1f]}}
