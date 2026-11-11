# A8 pattern tick 146.
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_138]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_140] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_142] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_144] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_145,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1257f,0.8643f,-0.2697f],left_rotation:[0.4577f,-0.1175f,0.8792f,0.0612f],scale:[0.612f,0.18f,1.797f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_145,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2696f,0.837f,-0.1256f],left_rotation:[0.298f,-0.1264f,0.9453f,0.0398f],scale:[0.5768f,0.18f,1.6929f],right_rotation:[0f,0f,0f,1f]}}
