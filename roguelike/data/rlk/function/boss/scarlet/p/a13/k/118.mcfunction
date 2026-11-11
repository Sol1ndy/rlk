# A13 pattern tick 118.
kill @e[type=minecraft:marker,tag=rlk_hr_gst]
function rlk:boss/scarlet/g/spot/side
execute as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
tag @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] add rlk_hr_gst
tag @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] remove rlk_hr_gsp
function rlk:boss/scarlet/g/cut/aim {s:128}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b101] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4692f,1.6218f,0.0028f],left_rotation:[-0.8881f,-0.3679f,0.1055f,0.2547f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_110]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_112] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_114] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_116] remove rlk_hr_trr
