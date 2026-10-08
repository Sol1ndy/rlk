# @s = 해파리, at @s. 2초마다 반경 4칸: 물 원소 피해(최대 체력의 4%) + 몸이 근처면 회복
scoreboard players remove @s life 1
execute if score @s life matches ..0 run return run kill @s
particle minecraft:dripping_water ~ ~-0.2 ~ 0.25 0.1 0.25 0 1
scoreboard players operation #t1 itv = @s life
scoreboard players operation #t1 itv %= #st40 tmp
execute if score #t1 itv matches 0 positioned ~ ~-1.6 ~ run function rlk:items/proc/jelly_pulse
