# @s = 인형, at @s. 3초마다 가장 가까운 적(10칸)에게 방어력의 70퍼센트 바위 원소 피해
scoreboard players remove @s life 1
execute if score @s life matches ..0 run particle minecraft:poof ~ ~0.6 ~ 0.2 0.3 0.2 0.02 10
execute if score @s life matches ..0 run return run kill @s
scoreboard players operation #t1 itv = @s life
scoreboard players operation #t1 itv %= #dollGap tmp
execute if score #t1 itv matches 0 if entity @e[tag=rlk_mob,distance=..10,limit=1] run function rlk:items/proc/doll_hit
