# A13 pattern tick 198.
function rlk:boss/scarlet/g/cut/aim {s:206}
execute at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~-130 0 positioned ^ ^ ^5.2 positioned ~ 201 ~ run function rlk:boss/scarlet/g/bolt
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b140] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.1091f,1.3933f,0.3868f],left_rotation:[-0.5792f,-0.0616f,0.4056f,0.7044f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_190]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_192] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_194] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
