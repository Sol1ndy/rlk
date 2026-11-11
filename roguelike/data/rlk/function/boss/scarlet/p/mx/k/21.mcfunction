# MX pattern tick 21
function rlk:boss/scarlet/fx/follow_on
execute at @s rotated as @s rotated ~ 0 positioned ^-0.6 ^2.052 ^0.714 run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mxb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.0939f,1.3899f,0.4282f],left_rotation:[-0.5792f,-0.0862f,0.4056f,0.7018f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_13]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_15] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_17] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_19] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_20,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1474f,1.1519f,0.3354f],left_rotation:[-0.1962f,-0.2466f,0.6588f,0.6831f],scale:[0.7407f,0.18f,1.814f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_20,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1305f,1.1478f,0.2967f],left_rotation:[-0.358f,-0.0736f,0.705f,0.6078f],scale:[0.7493f,0.18f,1.8391f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_20,tag=rlk_hr_tr_i2] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0745f,1.1944f,0.3513f],left_rotation:[-0.497f,0.104f,0.7061f,0.4936f],scale:[0.7316f,0.18f,1.796f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mxr0r14] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_rib_2"
