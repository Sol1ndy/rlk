# A13 pattern tick 117.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c113]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c113_111]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c113_113] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c113_115] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/g/cut/aim {s:128}
