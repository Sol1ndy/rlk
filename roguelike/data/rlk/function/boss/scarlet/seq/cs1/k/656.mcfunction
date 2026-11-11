# cs1: the timeline at #sq 656 (@s = the body).
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3,limit=1] at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^-0.72 ^1.26 ^3.18 facing entity @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] feet run tp @s ~ ~ ~ ~ ~
execute positioned ~ ~6 ~ rotated as @s rotated ~ 0 run function rlk:boss/scarlet/fx/p/leaves_dark {n:20}
