# @s = 플레이어, 위치 = 몸 (#gringT > 0 인 동안 매 틱). 1.5초마다 반경 3.5칸에 공격력의 25퍼센트 번개 원소 피해 + 회복
scoreboard players operation #t1 itv = #gringT itv
scoreboard players operation #t1 itv %= #st4 tmp
execute if score #t1 itv matches 0 run function rlk:items/proc/gring_fx
scoreboard players operation #t1 itv = #gringT itv
scoreboard players operation #t1 itv %= #st30 tmp
execute if score #t1 itv matches 1 run function rlk:items/proc/gring_pulse
