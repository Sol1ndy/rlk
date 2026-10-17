# fail clip tick 47
execute if score #gdFailN mb matches 2.. run execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run function rlk:mboss/guardian/p/fail/streak24
execute if score #gdFailN mb matches 1 run function rlk:mboss/guardian/p/release
