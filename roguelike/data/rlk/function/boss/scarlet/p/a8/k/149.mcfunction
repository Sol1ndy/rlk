# A8 pattern tick 149.
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.1 ~ run function rlk:boss/scarlet/fx/p/ghost_burst
function rlk:boss/scarlet/g/cut/aim {s:163}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_141]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_143] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_145] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
