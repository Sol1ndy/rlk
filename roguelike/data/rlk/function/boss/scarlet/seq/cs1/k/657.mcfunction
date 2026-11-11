# cs1: the timeline at #sq 657 (@s = the body).
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 positioned ^0.48 ^0.766 ^1.217 facing entity @e[type=minecraft:armor_stand,tag=rlk_mb_cam1,limit=1] feet run tp @s ~ ~ ~ ~ ~
execute positioned ~ ~6 ~ rotated as @s rotated ~ 0 run function rlk:boss/scarlet/fx/p/leaves_dark {n:-20}
