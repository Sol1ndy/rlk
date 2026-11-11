# A8 pattern tick 188.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c180_182]
function rlk:boss/scarlet/g/cut/aim {s:196}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c196] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c196,limit=1] ^-1.078 ^2.596 ^0.657
