# A8 pattern tick 55.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c48_49]
execute as @e[type=minecraft:item_display,tag=rlk_hr_sw_c48_51] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_2"
function rlk:boss/scarlet/g/cut/aim {s:64}
function rlk:boss/scarlet/rig/play/g_leap
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c64] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c64,limit=1] ^1.466 ^2.597 ^-0.67
