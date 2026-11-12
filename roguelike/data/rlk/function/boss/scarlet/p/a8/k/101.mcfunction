# A8 pattern tick 101.
function rlk:boss/scarlet/g/cut/lock {s:108}
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] positioned ^0.073 ^3.127 ^-0.021 run function rlk:boss/scarlet/fx/p/glint {c:2}
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @s ~ ~ ~ ~ 0
