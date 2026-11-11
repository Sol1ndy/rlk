# A8 pattern tick 187.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c180_181]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c180_183] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
function rlk:boss/scarlet/g/cut/aim {s:196}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c196] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c196,limit=1] ^-1.161 ^2.675 ^0.316
