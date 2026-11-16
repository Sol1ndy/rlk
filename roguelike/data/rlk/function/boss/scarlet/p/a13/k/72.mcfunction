# A13 pattern tick 72.
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_64]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_66] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_68] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_70] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_71,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3438f,1.8525f,-0.1622f],left_rotation:[-0.4545f,-0.4545f,-0.5417f,0.5417f],scale:[0.6859f,0.22f,1.9449f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_71,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3438f,1.9135f,-0.1401f],left_rotation:[-0.3536f,-0.3536f,-0.6124f,0.6124f],scale:[0.6746f,0.22f,1.913f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_71,tag=rlk_hr_tr_i2] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3438f,2.0264f,-0.0453f],left_rotation:[-0.2418f,-0.2418f,-0.6645f,0.6645f],scale:[0.649f,0.22f,1.8404f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13r1r64]
