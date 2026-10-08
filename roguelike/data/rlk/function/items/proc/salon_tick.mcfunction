# @s = 플레이어, 위치 = 몸 (#salonT > 0 인 동안 매 틱). 1.5초마다 가장 가까운 적(12칸)에게 최대 체력의 5퍼센트 물 원소 피해
particle minecraft:bubble_pop ~ ~2.4 ~ 0.5 0.15 0.5 0.01 1
scoreboard players operation #t1 itv = #salonT itv
scoreboard players operation #t1 itv %= #st30 tmp
execute if score #t1 itv matches 1 if entity @e[tag=rlk_mob,distance=..12,limit=1] run function rlk:items/proc/salon_hit
