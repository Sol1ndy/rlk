scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
execute if score @s cmT matches 12 run particle minecraft:large_smoke ~ ~1.7 ~ 0.15 0.05 0.15 0.01 3
execute if score @s cmT matches ..0 run function rlk:cm/kr/idle
