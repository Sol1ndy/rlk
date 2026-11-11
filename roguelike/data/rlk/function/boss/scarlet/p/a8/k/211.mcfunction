# A8 pattern tick 211.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b203] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0685f,2.1949f,0.3852f],left_rotation:[-0.8333f,0.0039f,-0.0076f,0.5527f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_203]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_205] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_207] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_209] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_210,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0701f,2.2078f,0.3806f],left_rotation:[-0.553f,0.6103f,0.4115f,0.3903f],scale:[0.1591f,0.18f,1.5965f],right_rotation:[0f,0f,0f,1f]}}
