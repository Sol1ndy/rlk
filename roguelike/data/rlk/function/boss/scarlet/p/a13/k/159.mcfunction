# A13 pattern tick 159.
function rlk:boss/scarlet/g/cut/aim {s:170}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b139] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.0785f,1.3961f,0.4339f],left_rotation:[-0.5792f,-0.0616f,0.4056f,0.7044f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_151]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_153] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_155] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
