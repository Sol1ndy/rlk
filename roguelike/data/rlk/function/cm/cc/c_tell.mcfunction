scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/cc/c_cancel
scoreboard players operation @s cmT -= #eStep tmp
particle minecraft:witch ^-0.4 ^2.4 ^0.3 0.2 0.2 0.2 0 2
particle minecraft:electric_spark ^-0.4 ^2.4 ^0.3 0.15 0.15 0.15 0.05 2
execute if score @s cmT matches ..0 run function rlk:cm/cc/c_summon
