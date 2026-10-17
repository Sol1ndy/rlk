# javelin clip tick 40
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q2h]
scoreboard players set #gp2S mb 0
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] run function rlk:mboss/guardian/p/javelin/trail
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p2s,limit=1] at @s run particle minecraft:end_rod ~ ~ ~ 0.2 0.2 0.2 0.01 2 force @a[tag=player]
