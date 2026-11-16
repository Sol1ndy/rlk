# HCUT pattern tick 28
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2429f,0.7713f,0.2669f],left_rotation:[-0.6375f,0.5993f,0.3059f,-0.3753f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_24] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_26] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_27,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0485f,0.7012f,0.4083f],left_rotation:[0.6617f,0.0402f,-0.7479f,0.0356f],scale:[0.8382f,0.3f,1.8199f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_27,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0238f,0.7638f,0.4006f],left_rotation:[0.8129f,0.0312f,-0.5799f,0.0438f],scale:[0.8223f,0.3f,1.7841f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutr0r24] remove rlk_hr_trg
kill @e[type=minecraft:marker,tag=rlk_hr_trt]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutw0w] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_rib_1"
