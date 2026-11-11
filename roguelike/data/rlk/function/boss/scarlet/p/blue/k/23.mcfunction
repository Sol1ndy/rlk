# BLUE pattern tick 23
kill @e[type=minecraft:marker,tag=rlk_hr_a9s]
function rlk:boss/scarlet/core/cam_clear
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_blueb1]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_blue_19] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_quad_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_blue_21] remove rlk_hr_trr
execute at @s rotated as @s rotated ~ 0 positioned ^ ^1.1 ^0.25 run function rlk:boss/scarlet/core/sw/rib
