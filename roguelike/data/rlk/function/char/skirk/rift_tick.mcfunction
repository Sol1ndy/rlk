# @s = 허계 균열, at @s
scoreboard players remove @s life 1
particle minecraft:reverse_portal ~ ~ ~ 0.15 0.15 0.15 0.01 1
execute if score @s life matches ..0 run particle minecraft:smoke ~ ~ ~ 0.1 0.1 0.1 0.02 8
execute if score @s life matches ..0 run kill @s
