# A4 pattern tick 20
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ 201.1 ~ run function rlk:boss/scarlet/fx/p/dive_impact {r:26}
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run function rlk:boss/scarlet/fx/snd/a4_impact
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3096f,0.7877f,0.6531f],left_rotation:[0.2009f,0.0001f,0.0003f,0.9796f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_12]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_14] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_16] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_18] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_19,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3343f,1.0953f,-0.1493f],left_rotation:[-0.1307f,-0.1308f,-0.6949f,0.6949f],scale:[0.7271f,0.26f,2.3762f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_19,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3007f,1.0781f,-0.2259f],left_rotation:[-0.0243f,-0.0242f,-0.7066f,0.7068f],scale:[0.739f,0.26f,2.415f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_19,tag=rlk_hr_tr_i2] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2671f,1.0719f,-0.1507f],left_rotation:[0.0828f,0.0829f,-0.7021f,0.7024f],scale:[0.7276f,0.26f,2.3777f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.31 ^0.723 ^0.805 run function rlk:boss/scarlet/core/sw/rib
