# A13 pattern tick 45.
function rlk:boss/scarlet/g/cut/aim {s:58}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b16] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5758f,1.7493f,-0.3005f],left_rotation:[-0.3036f,-0.733f,-0.5624f,-0.233f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_39] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_41] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_43] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_44,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2681f,1.4385f,-0.1833f],left_rotation:[-0.2939f,0.7093f,0.2451f,0.5919f],scale:[0.202f,0.18f,2.055f],right_rotation:[0f,0f,0f,1f]}}
