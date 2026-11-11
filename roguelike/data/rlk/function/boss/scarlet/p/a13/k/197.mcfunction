# A13 pattern tick 197.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c190_191]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c190_193] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
function rlk:boss/scarlet/g/cut/aim {s:206}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_swr] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c206,limit=1] ^-1.473 ^1.595 ^0.947
