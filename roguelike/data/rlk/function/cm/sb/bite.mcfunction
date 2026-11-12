# 물기: 반경 1.9 안의 몸에 8. 전갈 새끼 전체로 한 틱 한 번. 경직 · 빙결이면 못 묾
scoreboard players set @s c2T2 -1
execute unless score #free tmp matches 1 run return 0
scoreboard players set @s cmAR 6
execute unless score #c3sbbite snd matches 1 run function rlk:cm/c3/snd/sbbite
execute if score #c3SbHit tmp matches 0 if entity @e[tag=rlk_body,distance=..1.9] run function rlk:cm/sb/hit
