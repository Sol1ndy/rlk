# cs1: the timeline at #sq 656 (@s = the body).
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3_a,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^1.45 ^0.569 ^0.88 run tp @s ~ ~ ~
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3_b,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0.802 ^0.218 ^1.258 run tp @s ~ ~ ~
execute positioned ~ ~6 ~ rotated as @s rotated ~ 0 run function rlk:boss/scarlet/fx/p/leaves_dark {n:20}
