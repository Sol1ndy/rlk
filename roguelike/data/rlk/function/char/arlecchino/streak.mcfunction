# 플레이어 → 대상으로 0.5칸씩 이어지는 핏빛 줄기 (대상 = rlk_arS)
particle minecraft:dust{color:[0.88,0.12,0.20],scale:0.9} ~ ~ ~ 0 0 0 0 1
scoreboard players add #sn tmp 1
execute positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[tag=rlk_arS,dx=0,dy=0,dz=0] run return 0
execute if score #sn tmp matches ..40 positioned ^ ^ ^0.5 run function rlk:char/arlecchino/streak
