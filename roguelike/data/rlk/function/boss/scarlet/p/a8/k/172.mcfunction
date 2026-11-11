# A8 pattern tick 172.
function rlk:boss/scarlet/g/cut/aim {s:181}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_164]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_166] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_168] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
