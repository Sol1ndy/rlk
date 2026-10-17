# fail clip tick 35
execute if score #gdFailN mb matches 1.. run execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t0,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t0,limit=1] run playsound minecraft:block.beacon.ambient hostile @a[tag=player] ~ ~ ~ 0.7 0.5 0.23
