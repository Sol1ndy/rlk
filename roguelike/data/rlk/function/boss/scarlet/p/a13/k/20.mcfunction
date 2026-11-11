# A13 pattern tick 20.
function rlk:boss/scarlet/g/cut/lock {s:27}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] positioned ^0.679 ^1.776 ^-1.127 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c27] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c27,limit=1] ^2.23 ^0.891 ^-0.111
