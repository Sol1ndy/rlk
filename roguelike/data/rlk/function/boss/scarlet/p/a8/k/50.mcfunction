# A8 pattern tick 50.
function rlk:boss/scarlet/g/cut/aim {s:64}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_44] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_46] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_48] remove rlk_hr_trr
