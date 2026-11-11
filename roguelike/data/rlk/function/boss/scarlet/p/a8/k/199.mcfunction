# A8 pattern tick 199.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_195] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_197] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_198,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.4346f,1.3961f,0.4015f],left_rotation:[0.0962f,0.004f,0.7647f,0.6371f],scale:[0.8065f,0.26f,1.8669f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_198,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.4706f,1.4246f,0.6175f],left_rotation:[-0.0657f,0.1187f,0.8702f,0.4736f],scale:[0.7581f,0.26f,1.7533f],right_rotation:[0f,0f,0f,1f]}}
