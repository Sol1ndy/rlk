# A10 pattern tick 23
function rlk:boss/scarlet/core/cam_clear
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a10b2]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_19] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_21] remove rlk_hr_trr
execute at @s rotated as @s rotated ~ 0 positioned ^ ^1.1 ^0.25 run function rlk:boss/scarlet/core/sw/rib
