scoreboard players operation #pose tmp = @s cmAF
scoreboard players operation #pose tmp /= #c2c12 tmp
execute unless entity @s[tag=rlk_cmhold] unless entity @e[tag=rlk_body,distance=..2.3] run function rlk:cm/c2/walk8
execute if score @s cmAR matches 9.. run scoreboard players set #pose tmp 25
execute if score @s cmAR matches 5..8 run scoreboard players set #pose tmp 30
execute if score @s cmAR matches 1..4 run scoreboard players set #pose tmp 31
execute if score @s cmS matches 1 if score @s cmT matches 15.. run scoreboard players set #pose tmp 20
execute if score @s cmS matches 1 if score @s cmT matches ..14 run scoreboard players set #pose tmp 21
execute if score @s cmS matches 2 if score @s cmT matches 4.. run scoreboard players set #pose tmp 24
execute if score @s cmS matches 2 if score @s cmT matches ..3 run scoreboard players set #pose tmp 25
execute if score @s cmAH matches 4.. run scoreboard players set #pose tmp 40
execute if score @s cmAH matches 1..3 run scoreboard players set #pose tmp 41
