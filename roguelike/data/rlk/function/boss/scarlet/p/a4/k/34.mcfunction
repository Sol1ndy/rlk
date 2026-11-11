# A4 pattern tick 34
execute at @s positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:4}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3195f,1.4191f,0.3472f],left_rotation:[-0.5161f,-0.4834f,0.4834f,0.5161f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_26]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_28] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_30] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_32] remove rlk_hr_trr
