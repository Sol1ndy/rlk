# A8 pattern tick 100.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c91_94]
function rlk:boss/scarlet/g/cut/aim {s:109}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c109] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c109,limit=1] ^-0.467 ^2.579 ^-0.469
