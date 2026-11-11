# A13 pattern tick 109.
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_101]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_103] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute at @s rotated as @s rotated ~ 0 positioned ^-0.251 ^0.644 ^0.171 run function rlk:boss/scarlet/core/sw/rib
