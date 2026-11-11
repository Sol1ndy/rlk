# A13 pattern tick 221.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_217] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_219] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_220,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2752f,1.516f,-0.0317f],left_rotation:[0.4851f,-0.1425f,0.7883f,0.3506f],scale:[0.6419f,0.3f,2.194f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_220,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2863f,1.4964f,-0.0117f],left_rotation:[0.3447f,-0.1519f,0.8882f,0.2631f],scale:[0.6382f,0.3f,2.1835f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_220,tag=rlk_hr_tr_i2] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3749f,1.4614f,0.1321f],left_rotation:[0.1914f,-0.1557f,0.9548f,0.1659f],scale:[0.6116f,0.3f,2.084f],right_rotation:[0f,0f,0f,1f]}}
