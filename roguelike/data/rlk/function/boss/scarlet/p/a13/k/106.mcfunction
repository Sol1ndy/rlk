# A13 pattern tick 106.
function rlk:boss/scarlet/g/cut/lock {s:113}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] positioned ^-0.223 ^2.891 ^0.366 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @e[type=minecraft:item_display,tag=rlk_hr_sw_c113] ~ ~ ~ ~ 0
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] rotated ~ 0 run tp @e[type=minecraft:item_display,tag=rlk_hr_swh,tag=rlk_hr_sw_c113,limit=1] ^-1.673 ^0.169 ^0.477
