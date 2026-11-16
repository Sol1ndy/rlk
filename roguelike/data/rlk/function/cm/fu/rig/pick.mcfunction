scoreboard players operation #pose tmp = @s cmAF
scoreboard players operation #pose tmp /= #c2c12 tmp
execute if score @s cmAR matches 5.. run scoreboard players set #pose tmp 30
execute if score @s cmAR matches 1..4 run scoreboard players set #pose tmp 31
execute if score @s cmS matches 1 if score @s cmT matches 6.. run scoreboard players set #pose tmp 20
execute if score @s cmS matches 1 if score @s cmT matches ..5 run scoreboard players set #pose tmp 21
execute if score @s cmS matches 2 run scoreboard players set #pose tmp 24
execute if score @s cmAH matches 3.. run scoreboard players set #pose tmp 40
