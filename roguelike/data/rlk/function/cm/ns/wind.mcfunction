# 칼을 든 채 선딜: 경직 · 빙결이면 취소. 시작한 틱에는 줄지 않음(무리 전체가 같은 틱에 벰). 가속 중이면 한 틱 더
scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/cancel
execute if entity @s[tag=rlk_c2fresh] run return 0
scoreboard players remove @s cmT 1
execute if score #c2X tmp matches 1 run scoreboard players remove @s cmT 1
execute if score @s cmT matches 4..8 run particle minecraft:end_rod ~ ~2.15 ~ 0.12 0.12 0.12 0.01 1 normal
execute if score @s cmT matches ..0 run function rlk:cm/ns/strike
