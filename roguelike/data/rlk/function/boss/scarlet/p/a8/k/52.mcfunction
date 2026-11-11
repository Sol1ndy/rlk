# A8 pattern tick 52.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c48]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c48_48] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c48_50] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/g/cut/aim {s:64}
