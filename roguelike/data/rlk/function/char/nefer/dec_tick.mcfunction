# 기만의 핵 (@s, at @s)
scoreboard players remove @s life 1
particle minecraft:dust{color:[0.75,0.95,0.6],scale:0.6} ~ ~0.25 ~ 0.15 0.15 0.15 0 1
execute if score @s life matches ..0 run kill @s
