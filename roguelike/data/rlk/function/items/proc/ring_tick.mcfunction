# @s = 플레이어, 위치 = 몸 (#ringT > 0 인 동안 매 틱). 2초마다 반경 3.5칸에 공격력의 35퍼센트 불 원소 피해
scoreboard players operation #t1 itv = #ringT itv
scoreboard players operation #t1 itv %= #st4 tmp
execute if score #t1 itv matches 0 run function rlk:items/proc/ring_fx
scoreboard players operation #t1 itv = #ringT itv
scoreboard players operation #t1 itv %= #st40 tmp
execute if score #t1 itv matches 1 if entity @e[tag=rlk_mob,distance=..3.5,limit=1] run function rlk:items/proc/ring_hit
