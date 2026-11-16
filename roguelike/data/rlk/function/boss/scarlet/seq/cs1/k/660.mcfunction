# cs1: the timeline at #sq 660 (@s = the body).
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3_a,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^1.65 ^0.257 ^0.76 run tp @s ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3_b,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0.714 ^0.06 ^1.306 run tp @s ~ ~ ~
scoreboard players set #hrLook hr 2
function rlk:boss/scarlet/rig/look/phase/p2
