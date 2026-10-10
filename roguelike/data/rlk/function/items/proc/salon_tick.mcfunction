# @s = 플레이어, 위치 = 몸 (#salonT > 0 인 동안 매 틱). 멤버 셋이 몸 주위를 돌고, 1.5초마다 차례로 한 멤버가 가장 가까운 적(12칸)에게 물 원소 피해
execute unless entity @e[tag=rlk_salon,limit=1] run function rlk:items/proc/salon_spawn
execute as @e[tag=rlk_salonPv] at @s run tp @s ~ ~ ~ ~4 0
execute store result score #t2 itv run time query gametime
scoreboard players operation #t2 itv %= #c40 tmp
scoreboard players remove #t2 itv 20
execute if score #t2 itv matches ..-1 run scoreboard players operation #t2 itv *= #neg1 tmp
execute store result storage rlk:sal dy double 0.006 run scoreboard players get #t2 itv
function rlk:items/proc/salon_pos with storage rlk:sal
execute at @e[tag=rlk_salon] run particle minecraft:bubble_pop ~ ~ ~ 0.15 0.15 0.15 0.005 1
scoreboard players operation #t1 itv = #salonT itv
scoreboard players operation #t1 itv %= #st30 tmp
execute if score #t1 itv matches 1 if entity @e[tag=rlk_mob,distance=..12,limit=1] run function rlk:items/proc/salon_hit
