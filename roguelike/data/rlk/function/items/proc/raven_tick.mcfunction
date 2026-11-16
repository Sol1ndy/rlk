# @s = 플레이어, 위치 = 몸 (#ravenT > 0 인 동안 매 틱). 까마귀가 머리 위를 맴돌고 1초마다 가까운 적(12칸)에게 번개
execute as @e[tag=rlk_raven,limit=1] rotated as @s run tp @s ^ ^2.4 ^0.8 ~9 ~
particle minecraft:dust{color:[0.77f,0.55f,1.0f],scale:0.6f} ~ ~2.5 ~ 0.3 0.1 0.3 0 1
scoreboard players operation #t1 itv = #ravenT itv
scoreboard players operation #t1 itv %= #ravenItv tmp
execute if score #t1 itv matches 0 if entity @e[tag=rlk_mob,distance=..12,limit=1] run function rlk:items/proc/raven_hit
execute if score #ravenT itv matches ..1 run kill @e[tag=rlk_raven]
