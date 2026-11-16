scoreboard players operation #c2p tmp = @s cmT
scoreboard players operation #c2p tmp /= #st6 tmp
scoreboard players operation #c2p tmp %= #2 tmp
scoreboard players add #c2p tmp 27
execute if score @s cmT matches 17..20 run scoreboard players set #c2p tmp 26
execute if score @s cmT matches 21.. run scoreboard players set #c2p tmp 25
