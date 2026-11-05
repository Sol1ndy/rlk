# cs1 at #sq 171 (@s = the body).
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_2,limit=1] at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^ ^1.6 positioned ~ 202.567 ~ facing entity @e[tag=rlk_body,limit=1] eyes run tp @s ~ ~ ~ ~ ~
execute positioned ~ ~6 ~ rotated as @s rotated ~ 0 run function rlk:boss/scarlet/fx/p/leaves_dark {n:40}
