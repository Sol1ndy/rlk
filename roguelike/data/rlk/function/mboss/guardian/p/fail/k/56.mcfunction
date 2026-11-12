# fail clip tick 56
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q13r0_1]
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q13r0_8]
execute if score #gdFailN mb matches 2.. run execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p13t1,limit=1] run playsound minecraft:item.trident.riptide_3 hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
