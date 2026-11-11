# A13 pattern tick 121.
kill @e[type=minecraft:item_display,tag=rlk_hr_sw_c113_115]
function rlk:boss/scarlet/g/cut/lock {s:128}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] positioned ^0.073 ^3.127 ^-0.021 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @s ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c128] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c128,limit=1] ^-0.505 ^2.757 ^0.402
