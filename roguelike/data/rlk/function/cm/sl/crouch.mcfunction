# 웅크림(예고): 경직 · 빙결이면 취소
scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/cancel
scoreboard players remove @s cmT 1
execute if score #c2X tmp matches 1 run scoreboard players remove @s cmT 1
execute if score @s cmT matches 1.. run particle minecraft:electric_spark ~ ~0.4 ~ 0.45 0.1 0.45 0.05 2 normal
execute if score @s cmT matches ..0 run function rlk:cm/sl/leap
