scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
execute if score @s cmT matches 20 run particle minecraft:cloud ^ ^1.4 ^0.4 0.05 0.05 0.05 0.01 2
execute if score @s cmT matches 10 run particle minecraft:cloud ^ ^1.4 ^0.4 0.05 0.05 0.05 0.01 2
execute if score @s cmT matches ..0 run function rlk:cm/nj/tired_end
