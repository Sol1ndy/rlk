# A8 pattern tick 39.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c30_33]
function rlk:boss/scarlet/g/cut/aim {s:48}
function rlk:boss/scarlet/rig/play/g_rise
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c48] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c48,limit=1] ^-0.78 ^0.192 ^-0.626
