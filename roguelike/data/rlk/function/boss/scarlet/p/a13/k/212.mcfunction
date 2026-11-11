# A13 pattern tick 212.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c206_206]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c206_208] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
function rlk:boss/scarlet/g/cut/aim {s:220}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c220] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c220,limit=1] ^-1.078 ^2.596 ^0.657
