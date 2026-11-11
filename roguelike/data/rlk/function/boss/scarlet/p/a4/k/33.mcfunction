# A4 pattern tick 33
scoreboard players set #hzEl mb 3
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoParry mb 0
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:30,tell:1,dmg:31}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/scarlet/core/hz_tag/a4
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3471f,1.4025f,0.2918f],left_rotation:[-0.5174f,-0.4997f,0.4826f,0.4997f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_25]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_27] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_29] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_31] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_32,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.3179f,1.4316f,0.2113f],left_rotation:[-0.0062f,-0.938f,-0.0168f,0.3461f],scale:[0.6247f,0.26f,1.4098f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_32,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0138f,1.4233f,0.4404f],left_rotation:[-0.0097f,-0.8409f,-0.015f,0.5409f],scale:[0.7071f,0.26f,1.5958f],right_rotation:[0f,0f,0f,1f]}}
