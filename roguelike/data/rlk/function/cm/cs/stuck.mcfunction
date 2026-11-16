scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
execute if score @s cmT matches 12 run particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.3 ~ 0.6 0.1 0.6 0 10
execute if score @s cmT matches ..0 run function rlk:cm/cs/idle
