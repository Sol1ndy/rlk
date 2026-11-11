# A13 pattern tick 67.
function rlk:boss/scarlet/rig/state/hidden
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_59]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_61] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_63] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
