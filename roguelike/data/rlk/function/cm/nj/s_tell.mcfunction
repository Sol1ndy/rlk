scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/nj/s_cancel
scoreboard players operation @s cmT -= #eStep tmp
particle minecraft:electric_spark ^0.4 ^1.9 ^0.2 0.05 0.05 0.05 0 1
execute if score @s cmT matches ..0 run function rlk:cm/nj/s_throw
