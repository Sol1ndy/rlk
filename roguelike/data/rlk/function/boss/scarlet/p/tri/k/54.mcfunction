# TRI pattern tick 54
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2261f,1.5378f,0.5968f],left_rotation:[-0.7784f,-0.3796f,0.2192f,0.4494f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_46]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_48] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_50] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_52] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_53,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0856f,1.8188f,0.3752f],left_rotation:[-0.7456f,0.0735f,0.6038f,0.2722f],scale:[0.2987f,0.22f,1.1121f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_53,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.1226f,1.8202f,0.3604f],left_rotation:[-0.8191f,0.1099f,0.4998f,0.2593f],scale:[0.2942f,0.22f,1.095f],right_rotation:[0f,0f,0f,1f]}}
