# A13 pattern tick 120.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c113_114]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c113_116] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
function rlk:boss/scarlet/g/cut/aim {s:128}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c128] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c128,limit=1] ^-0.517 ^2.704 ^-0.039
