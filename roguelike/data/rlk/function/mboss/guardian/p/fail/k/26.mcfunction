# fail clip tick 26
execute if score #gdFailN mb matches 1.. run execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t0,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t0,limit=1] run function rlk:mboss/guardian/p/fail/streakf
execute if score #gdFailN mb matches 1.. run kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p13c0]
