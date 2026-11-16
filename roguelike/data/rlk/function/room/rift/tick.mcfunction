# From room/tick while #riftOn room is 1 (the run is active): every rift of the map, and the queued shows.
scoreboard players set #riftOn room 0
execute as @e[type=minecraft:marker,tag=rlk_rift] at @s run function rlk:room/rift/t/one
execute as @e[type=minecraft:marker,tag=rlk_riftq] at @s run function rlk:room/rift/show_now
