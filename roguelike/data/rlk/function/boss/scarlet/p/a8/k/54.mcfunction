# A8 pattern tick 54.
kill @e[type=minecraft:marker,tag=rlk_hr_gst]
function rlk:boss/scarlet/g/spot/over
execute as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] at @s positioned ~ ~2.5 ~ facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
tag @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] add rlk_hr_gst
tag @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] remove rlk_hr_gsp
function rlk:boss/scarlet/g/cut/aim {s:64}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_46]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_48] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
