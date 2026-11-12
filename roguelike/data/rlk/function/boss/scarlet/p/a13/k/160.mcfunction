# A13 pattern tick 160.
kill @e[type=minecraft:marker,tag=rlk_hr_gst]
function rlk:boss/scarlet/g/spot/side
execute as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
tag @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] add rlk_hr_gst
tag @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] remove rlk_hr_gsp
function rlk:boss/scarlet/g/cut/aim {s:170}
execute at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~75 0 positioned ^ ^ ^4.4 positioned ~ 201 ~ run function rlk:boss/scarlet/g/bolt
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_152]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_154] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_156] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
