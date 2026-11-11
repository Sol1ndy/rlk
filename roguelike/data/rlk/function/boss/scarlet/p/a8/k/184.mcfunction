# A8 pattern tick 184.
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c180]
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c180_178]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c180_180] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c180_182] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
function rlk:boss/scarlet/g/cut/aim {s:196}
