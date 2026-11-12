# MX pattern tick 9
function rlk:boss/scarlet/p/mx/lockp
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mxb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.561f,0.8816f,-0.4229f],left_rotation:[0.3586f,-0.8628f,0.3282f,-0.1389f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_1]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_3] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
