# fail clip tick 75
execute if score #gdFailN mb matches 2.. run execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run function rlk:mboss/guardian/p/fail/streakf
execute if score #gdFailN mb matches 2.. run execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run playsound minecraft:item.trident.riptide_3 hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.3
