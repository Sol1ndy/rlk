# A8 pattern tick 35.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c30_29]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c30_31] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c30_33] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/g/cut/aim {s:48}
