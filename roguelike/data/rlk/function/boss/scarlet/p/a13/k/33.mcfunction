# A13 pattern tick 33.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c27_27]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c27_29] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
function rlk:boss/scarlet/g/cut/aim {s:41}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c41] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c41,limit=1] ^-0.957 ^0.115 ^-0.183
