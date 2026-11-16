scoreboard players operation #pose tmp = @s cmAF
scoreboard players operation #pose tmp /= #c2c12 tmp
scoreboard players operation #pose tmp %= #c2c2 tmp
execute if score @s c2T2 matches 7.. run scoreboard players set #pose tmp 7
execute if score @s c2T2 matches 3..6 run scoreboard players set #pose tmp 6
execute if score @s c2T2 matches 1..2 run scoreboard players set #pose tmp 7
execute if score @s cmAR matches 1.. run scoreboard players set #pose tmp 7
execute if score @s cmS matches 1 run scoreboard players set #pose tmp 5
execute if score @s cmS matches 2 run scoreboard players set #pose tmp 6
execute if score @s cmAH matches 3.. run scoreboard players set #pose tmp 40
execute if score @s c2T2 matches 1.. run scoreboard players remove @s c2T2 1
