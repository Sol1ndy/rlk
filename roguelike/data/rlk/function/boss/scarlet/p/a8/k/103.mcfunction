# A8 pattern tick 103.
function rlk:boss/scarlet/rig/play/g_x
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run function rlk:mboss/mv/glide {t:2}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c109] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c109,limit=1] ^-0.459 ^2.771 ^0.848
