# A8 pattern tick 191.
function rlk:boss/scarlet/rig/play/g_vert
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b154] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.1146f,1.3862f,0.3838f],left_rotation:[-0.5792f,-0.0616f,0.4056f,0.7044f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_183]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_185] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
