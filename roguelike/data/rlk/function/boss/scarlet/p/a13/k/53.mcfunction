# A13 pattern tick 53.
function rlk:boss/scarlet/g/cut/aim {s:66}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_45]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_47] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_49] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
