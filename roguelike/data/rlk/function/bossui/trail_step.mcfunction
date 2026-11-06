# Drain a fifth of the gap (at least 1/150 of max HP) per call.
scoreboard players operation #step bu = @s buTrail
scoreboard players operation #step bu -= #buHp bu
scoreboard players set #c5 bu 5
scoreboard players operation #step bu /= #c5 bu
scoreboard players operation #min bu = #buMax bu
scoreboard players set #c150 bu 150
scoreboard players operation #min bu /= #c150 bu
execute if score #min bu matches ..0 run scoreboard players set #min bu 1
execute if score #step bu < #min bu run scoreboard players operation #step bu = #min bu
scoreboard players operation @s buTrail -= #step bu
execute if score @s buTrail < #buHp bu run scoreboard players operation @s buTrail = #buHp bu
