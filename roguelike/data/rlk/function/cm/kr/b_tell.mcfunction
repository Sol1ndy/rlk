scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
particle minecraft:electric_spark ^-0.5 ^1.6 ^0.2 0.2 0.5 0.2 0.04 3
execute if score @s cmT matches 7 run playsound minecraft:block.beacon.power_select master @a ~ ~ ~ 0.6 1.8
execute if score @s cmT matches ..0 run function rlk:cm/kr/b_hit
