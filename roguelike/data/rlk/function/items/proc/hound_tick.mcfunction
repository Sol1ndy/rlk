# @s = 사냥개, at @s. 1초마다 몸에서 12칸 안의 가장 가까운 적에게 달려들어 공격력의 35퍼센트 번개 원소 피해 + 회복. 적이 없으면 몸 옆으로
scoreboard players remove @s life 1
execute if score @s life matches ..0 run particle minecraft:poof ~ ~0.4 ~ 0.3 0.3 0.3 0.02 12
execute if score @s life matches ..0 run return run kill @s
scoreboard players operation #t1 itv = @s life
scoreboard players operation #t1 itv %= #houndGap tmp
execute unless score #t1 itv matches 0 run return 0
execute at @e[tag=rlk_body,limit=1] unless entity @e[tag=rlk_mob,distance=..12,limit=1] run return run tp @s ~1 ~ ~
execute at @e[tag=rlk_body,limit=1] as @e[tag=rlk_mob,distance=..12,sort=nearest,limit=1] run tag @s add rlk_ht
execute at @e[tag=rlk_ht,limit=1] run tp @s ~0.7 ~ ~ facing entity @e[tag=rlk_ht,limit=1]
execute at @e[tag=rlk_ht,limit=1] run function rlk:items/proc/hound_bite
tag @e[tag=rlk_ht] remove rlk_ht
