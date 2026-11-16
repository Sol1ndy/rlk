scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
execute if score @s cmT matches 20 run particle minecraft:crit ~ ~1 ~ 0.3 0.1 0.3 0 5
execute if score @s cmT matches 10 run particle minecraft:crit ~ ~1 ~ 0.3 0.1 0.3 0 5
execute if score @s cmT matches ..0 run function rlk:cm/rv/to_start
