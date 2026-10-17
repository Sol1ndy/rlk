# fail clip tick 33
execute if score #gdFailN mb matches 1.. run execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t0,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t0,limit=1] run playsound minecraft:item.trident.riptide_3 hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
