# A13 pattern tick 195.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c190_189]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c190_191] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c190_193] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/g/cut/aim {s:206}
