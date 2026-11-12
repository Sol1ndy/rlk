# ULT pattern tick 26
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/ult_web {t:22}
function rlk:boss/scarlet/fx/hud/ovl {g:"web",in:2,hold:16,out:2}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.7105f,1.143f,-0.0993f],left_rotation:[-0.5337f,-0.63f,-0.4639f,-0.321f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_22] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_24] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_25,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0152f,0.9824f,0.1436f],left_rotation:[-0.0048f,0.6755f,0.1184f,0.7278f],scale:[0.7018f,0.3f,2.2267f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_25,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1448f,1.0022f,0.1305f],left_rotation:[-0.0028f,0.7803f,0.1382f,0.6099f],scale:[0.6765f,0.3f,2.1459f],right_rotation:[0f,0f,0f,1f]}}
