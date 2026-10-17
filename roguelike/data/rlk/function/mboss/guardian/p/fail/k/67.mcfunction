# fail clip tick 67
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q13r0_2]
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q13r0_6]
execute if score #gdFailN mb matches 2.. run execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run function rlk:mboss/guardian/p/fail/streakf
