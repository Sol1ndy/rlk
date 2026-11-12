# HCUT pattern tick 8
function rlk:boss/scarlet/rig/anchor/blade_tip
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:5}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3919f,0.5507f,0.0093f],left_rotation:[-0.5572f,0.646f,-0.4353f,0.2876f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_2] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_4] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
