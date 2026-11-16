# BLUE pattern tick 15
function rlk:boss/scarlet/p/blue/lockp
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1,distance=..7] rotated as @s rotated ~ 0 positioned ^ ^ ^7 run tp @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_blueb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.44f,1.2839f,0.0989f],left_rotation:[-0.2067f,0.0862f,-0.6762f,0.7018f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_blue_9] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_blue_11] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
