# A13 pattern tick 104.
function rlk:boss/scarlet/g/cut/aim {s:112}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b100] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.1384f,0.6229f,0.2905f],left_rotation:[-0.6865f,-0.6215f,0.2292f,0.2998f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_100] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_102] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_103,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.139f,0.6209f,0.2768f],left_rotation:[-0.7265f,-0.5523f,0.3551f,0.2028f],scale:[0.745f,0.22f,1.5419f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^-0.252 ^0.644 ^0.173 run function rlk:boss/scarlet/core/sw/rib
