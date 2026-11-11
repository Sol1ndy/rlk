# A13 pattern tick 49.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c41_43]
function rlk:boss/scarlet/g/cut/aim {s:58}
function rlk:boss/scarlet/rig/play/g_leap
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_swr] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c58,limit=1] ^1.466 ^2.597 ^-0.67
