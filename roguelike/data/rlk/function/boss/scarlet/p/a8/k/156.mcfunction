# A8 pattern tick 156.
function rlk:boss/scarlet/g/cut/lock {s:163}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] positioned ^0.16 ^2.98 ^0.272 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c163] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c163,limit=1] ^2.035 ^1.737 ^1.045
