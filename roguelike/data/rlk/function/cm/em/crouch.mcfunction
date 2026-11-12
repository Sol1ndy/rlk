# 웅크림(예고 0.6초, 두 단검이 빛남): 경직 · 빙결이면 그 용병만 취소. 시작한 틱에는 줄지 않음(둘이 같은 틱에 돌진)
scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/cancel
execute if entity @s[tag=rlk_c3fresh] run return 0
scoreboard players remove @s cmT 1
execute if score @s cmT matches 3..7 run particle minecraft:end_rod ~ ~0.9 ~ 0.3 0.1 0.3 0.01 1 normal
execute if score @s cmT matches ..0 run function rlk:cm/em/go
