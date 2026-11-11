# A8 pattern tick 187.
function rlk:boss/scarlet/g/cut/aim {s:195}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b154] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.0983f,1.3974f,0.3895f],left_rotation:[-0.5792f,-0.0616f,0.4056f,0.7044f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_179]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_181] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_183] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_185] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_186,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.065f,1.1827f,0.3056f],left_rotation:[-0.5503f,-0.1876f,0.2887f,0.7607f],scale:[0.2231f,0.22f,1.8663f],right_rotation:[0f,0f,0f,1f]}}
