# KCUT pattern tick 23
kill @e[type=minecraft:marker,tag=rlk_hr_a9s]
function rlk:boss/scarlet/core/cam_clear
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.3411f,1.2888f,0.5067f],left_rotation:[-0.8446f,0.3074f,0.4119f,0.1499f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_17] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_19] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_21] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_22,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0723f,0.7751f,0.4925f],left_rotation:[-0.6096f,-0.1772f,0.7199f,0.2808f],scale:[0.722f,0.26f,1.7942f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_22,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.1745f,0.9001f,0.5701f],left_rotation:[-0.741f,-0.1083f,0.5924f,0.2969f],scale:[0.6957f,0.26f,1.7254f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_22,tag=rlk_hr_tr_i2] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.3034f,1.0742f,0.5914f],left_rotation:[-0.8438f,-0.0354f,0.4422f,0.3018f],scale:[0.6599f,0.26f,1.6329f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^-0.441 ^1.372 ^0.405 run function rlk:boss/scarlet/core/sw/rib
