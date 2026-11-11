# A13 pattern tick 47.
function rlk:boss/scarlet/g/cut/aim {s:58}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_39]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_41] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_43] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
