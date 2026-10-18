# #g mb = a volley group that just landed a hit: its hazards and props stop testing for hits (the strike
# visuals and the flights go on).
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzG = #g mb run scoreboard players set @s mbHzHit 1
execute as @e[tag=rlk_mb_pj] if score @s mbPjG = #g mb run scoreboard players set @s mbPjHit 1
