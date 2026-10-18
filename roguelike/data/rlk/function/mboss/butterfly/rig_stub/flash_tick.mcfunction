scoreboard players remove @s bfStubY 1
execute if score @s bfStubY matches ..0 as @e[type=minecraft:item_display,tag=rlk_mb_bfs] run data merge entity @s {Glowing:0b}
