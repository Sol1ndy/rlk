# fail clip tick 53
execute if score #gdFailN mb matches 2.. run execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run function rlk:mboss/guardian/p/fail/streakf
execute if score #gdFailN mb matches 2.. run execute if score #gp13K1 mb matches 6 as @e[type=minecraft:item_display,tag=rlk_mb_gd_p13s1,limit=1] run function rlk:mboss/guardian/p/fail/tint2_6
execute if score #gdFailN mb matches 2.. run execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run particle minecraft:dust{color:[0.92f,0.94f,1f],scale:1} ~ ~7 ~ 0.25 2.5 0.25 0 8 force @a[tag=player]
