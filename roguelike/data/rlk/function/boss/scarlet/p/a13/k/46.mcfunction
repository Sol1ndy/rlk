# A13 pattern tick 46.
function rlk:boss/scarlet/g/cut/aim {s:58}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_40] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_42] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_44] remove rlk_hr_trr
