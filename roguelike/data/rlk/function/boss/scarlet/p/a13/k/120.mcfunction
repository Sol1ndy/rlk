# A13 pattern tick 120.
function rlk:boss/scarlet/g/cut/aim {s:128}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b101] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4727f,1.6063f,0.0163f],left_rotation:[-0.8881f,-0.3679f,0.1055f,0.2547f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_112]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_114] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_116] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
