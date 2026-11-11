# A13 pattern tick 178.
function rlk:boss/scarlet/g/cut/aim {s:190}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_170]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_172] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_174] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
