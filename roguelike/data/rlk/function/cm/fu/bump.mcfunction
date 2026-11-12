# 박치기 중: 반경 1.5 안의 몸에 10, 버섯 한 마리당 한 번 · 버섯 전체로 한 틱 한 번
scoreboard players set #hold tmp 1
execute if score @s c2T2 matches 0 if score #c3FuHit tmp matches 0 if entity @e[tag=rlk_body,distance=..1.5] run function rlk:cm/fu/hit
scoreboard players remove @s cmT 1
execute if score @s cmT matches ..0 run function rlk:cm/fu/end
