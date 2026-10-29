# 부풀기(예고 0.5초, 갓이 커지고 반점이 빛남): 경직 · 빙결이면 취소
scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/cancel
scoreboard players remove @s cmT 1
execute if score @s cmT matches 1.. run particle minecraft:spore_blossom_air ~ ~1.3 ~ 0.35 0.2 0.35 0 2 normal
execute if score @s cmT matches ..0 run function rlk:cm/fu/go
