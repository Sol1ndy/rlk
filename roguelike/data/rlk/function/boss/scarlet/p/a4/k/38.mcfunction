# A4 pattern tick 38
function rlk:boss/scarlet/ai/tail
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_30]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_32] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
