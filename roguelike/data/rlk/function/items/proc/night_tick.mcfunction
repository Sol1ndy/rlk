# @s = 플레이어, 위치 = 몸 (#nightT > 0 인 동안 매 틱). 보호막이 있을 때 #nightGap 틱(1.5초)마다 별 +1, 4개면 가장 가까운 적(12칸)에게 발사 (4개는 고정)
execute unless score @s shieldHP matches 1.. run return 0
scoreboard players operation #t1 itv = #nightT itv
scoreboard players operation #t1 itv %= #nightGap tmp
execute if score #t1 itv matches 1 if score #stars itv matches ..3 run scoreboard players add #stars itv 1
execute if score #t1 itv matches 1 run particle minecraft:end_rod ~ ~2.4 ~ 0.3 0.1 0.3 0.01 3
execute if score #stars itv matches 4.. if entity @e[tag=rlk_mob,distance=..12,limit=1] run function rlk:items/proc/night_fire
