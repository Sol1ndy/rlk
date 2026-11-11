# A8 pattern tick 222.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_216] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_218] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_220] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_221,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1538f,1.3795f,0.2929f],left_rotation:[0.4246f,0.1555f,0.0741f,0.8888f],scale:[0.4177f,0.26f,1.5863f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8r5r217] remove rlk_hr_trg
kill @e[type=minecraft:marker,tag=rlk_hr_trt]
