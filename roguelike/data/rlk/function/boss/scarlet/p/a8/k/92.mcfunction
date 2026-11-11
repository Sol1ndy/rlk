# A8 pattern tick 92.
function rlk:boss/scarlet/g/cut/aim {s:108}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b76] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4675f,1.6295f,-0.004f],left_rotation:[-0.8881f,-0.3679f,0.1055f,0.2547f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_86] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_88] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_90] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_91,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.6032f,1.4328f,0.4835f],left_rotation:[-0.6703f,0.6576f,0.3309f,0.0942f],scale:[0.8153f,0.22f,2.0717f],right_rotation:[0f,0f,0f,1f]}}
