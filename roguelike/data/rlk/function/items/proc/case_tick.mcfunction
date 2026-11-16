# @s = 향수함, at @s. 2초마다 가장 가까운 적(10칸)에게 풀 원소 피해. 불 원소가 붙은 적이면 80퍼센트, 아니면 40퍼센트
scoreboard players remove @s life 1
execute if score @s life matches ..0 run return run kill @s
scoreboard players operation #t1 itv = @s life
scoreboard players operation #t1 itv %= #caseGap tmp
execute unless score #t1 itv matches 0 run return 0
particle minecraft:spore_blossom_air ~ ~0.6 ~ 0.4 0.3 0.4 0 6
execute unless entity @e[tag=rlk_mob,distance=..10,limit=1] run return 0
scoreboard players set #t2 itv 0
execute as @e[tag=rlk_mob,distance=..10,sort=nearest,limit=1] if score @s aFire matches 1.. run scoreboard players set #t2 itv 1
execute if score #t2 itv matches 0 run function rlk:items/proc/case_hit1
execute if score #t2 itv matches 1 run function rlk:items/proc/case_hit2
