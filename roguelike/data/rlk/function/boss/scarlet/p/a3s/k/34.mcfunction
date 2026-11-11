# A3S pattern tick 34
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a330]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_a330_30] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
function rlk:boss/scarlet/ai/tail
