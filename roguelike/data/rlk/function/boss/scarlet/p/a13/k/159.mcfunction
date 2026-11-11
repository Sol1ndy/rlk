# A13 pattern tick 159.
kill @e[type=minecraft:marker,tag=rlk_hr_gst]
function rlk:boss/scarlet/g/spot/side
execute as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
tag @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] add rlk_hr_gst
tag @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] remove rlk_hr_gsp
function rlk:boss/scarlet/g/cut/aim {s:169}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b140] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.0728f,1.397f,0.4154f],left_rotation:[-0.5792f,-0.0616f,0.4056f,0.7044f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_151]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_153] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_155] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_157] remove rlk_hr_trr
