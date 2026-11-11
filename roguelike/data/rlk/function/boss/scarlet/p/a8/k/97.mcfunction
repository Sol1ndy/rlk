# A8 pattern tick 97.
function rlk:boss/scarlet/g/cut/aim {s:109}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b79] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4709f,1.6141f,0.0096f],left_rotation:[-0.8881f,-0.3679f,0.1055f,0.2547f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_89]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_91] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_93] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
