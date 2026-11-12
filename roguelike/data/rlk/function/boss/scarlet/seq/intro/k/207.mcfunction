# intro: the timeline at #sq 207 (@s = the body).
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_1,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:10,transformation:{scale:[0f,0f,0f]}}
function rlk:boss/scarlet/rig/anchor/hand_r
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_1,limit=1] at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s rotated ~ 0 positioned ^0.045 ^0.061 ^-0.014 run tp @s ~ ~ ~
