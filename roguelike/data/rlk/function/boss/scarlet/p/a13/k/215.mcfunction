# A13 pattern tick 215.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c206_209]
function rlk:boss/scarlet/rig/play/g_vert
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c220] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c220,limit=1] ^-0.667 ^2.196 ^1.554
