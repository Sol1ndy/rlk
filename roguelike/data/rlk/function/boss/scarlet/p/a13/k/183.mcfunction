# A13 pattern tick 183.
function rlk:boss/scarlet/g/cut/lock {s:190}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] positioned ^-0.639 ^2.068 ^0.619 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @s ~ ~ ~ ~ 0
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run function rlk:mboss/mv/glide {t:3}
