scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
execute if score @s cmT matches 12 run particle minecraft:electric_spark ~ ~2.2 ~ 0.25 0.05 0.25 0 3
execute if score @s cmT matches ..0 run function rlk:cm/cc/idle
