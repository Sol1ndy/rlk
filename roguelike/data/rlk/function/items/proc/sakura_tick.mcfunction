# @s = 살생앵, at @s. 3초마다 가장 가까운 적(10칸)에게 번개 원소 피해. 그루 수에 따라 25 / 35 / 45퍼센트
scoreboard players remove @s life 1
execute if score @s life matches ..0 run particle minecraft:cherry_leaves ~ ~0.5 ~ 0.3 0.4 0.3 0 12
execute if score @s life matches ..0 run return run kill @s
scoreboard players operation #t1 itv = @s life
scoreboard players operation #t1 itv %= #st60 tmp
execute unless score #t1 itv matches 0 run return 0
particle minecraft:cherry_leaves ~ ~0.6 ~ 0.3 0.3 0.3 0 2
execute unless entity @e[tag=rlk_mob,distance=..10,limit=1] run return 0
execute store result score #sakN itv if entity @e[tag=rlk_sakura]
execute if score #sakN itv matches ..1 run function rlk:items/proc/sakura_hit1
execute if score #sakN itv matches 2 run function rlk:items/proc/sakura_hit2
execute if score #sakN itv matches 3.. run function rlk:items/proc/sakura_hit3
