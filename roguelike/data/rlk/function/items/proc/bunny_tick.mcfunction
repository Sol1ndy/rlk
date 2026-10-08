# @s = 인형의 표식, at @s. 인형을 따라가며 수명을 센다. 인형이 죽었거나 수명이 다하면 폭발
scoreboard players remove @s life 1
execute unless entity @e[tag=rlk_decoy,distance=..8,limit=1] run return run function rlk:items/proc/bunny_boom
execute if score @s life matches ..0 run return run function rlk:items/proc/bunny_boom
tp @s @e[tag=rlk_decoy,limit=1,sort=nearest]
scoreboard players operation #t1 itv = @s life
scoreboard players operation #t1 itv %= #st20 tmp
execute if score #t1 itv matches 0 as @e[tag=rlk_decoy,limit=1] at @s run function rlk:items/proc/bunny_taunt
particle minecraft:flame ~ ~1.1 ~ 0.1 0.1 0.1 0.01 1
