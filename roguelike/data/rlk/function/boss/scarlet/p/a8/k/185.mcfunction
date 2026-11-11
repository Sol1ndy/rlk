# A8 pattern tick 185.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c180_179]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c180_181] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c180_183] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/g/cut/aim {s:196}
