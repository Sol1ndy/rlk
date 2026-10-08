scoreboard players remove #spawnT room 1
execute if score #spawnT room matches 1.. run return 0
execute as @e[tag=rlk_zone] if score @s zid = #combat room at @s run function rlk:room/mob_wave
