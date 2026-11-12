scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.15 ~ 0.6 0.1 0.6 0 6
execute if score @s cmT matches ..0 run function rlk:cm/cs/go_under
