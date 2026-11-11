# A13 pattern tick 95.
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c91]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c91_89]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c91_91] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c91_93] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
