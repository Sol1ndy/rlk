scoreboard players operation #pose tmp = @s cmAF
scoreboard players operation #pose tmp /= #c3c3 tmp
scoreboard players operation #pose tmp %= #c3c4 tmp
execute if score @s c2T matches 37.. run scoreboard players set #pose tmp 82
execute if score @s cmAR matches 4.. run scoreboard players set #pose tmp 24
execute if score @s cmAR matches 1..3 run scoreboard players set #pose tmp 30
execute if score @s cmAH matches 3.. run scoreboard players set #pose tmp 40
