# @s = body: one pre-turn step (#aq8D centi-degrees)
execute store result score #t mb run data get entity @s Rotation[0] 100
scoreboard players operation #t mb += #aq8D mb
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #t mb
