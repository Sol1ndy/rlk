scoreboard players remove @s life 1
execute if score @s life matches ..0 run return run kill @s
scoreboard players operation #t1 itv = @s life
scoreboard players operation #t1 itv %= #st8 tmp
execute if score #t1 itv matches 0 run particle minecraft:wax_on ~ ~0.2 ~ 0.3 0.3 0.3 0 1
