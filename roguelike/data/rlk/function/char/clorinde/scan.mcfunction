# 총알의 줄을 0.5칸씩 따라간다 (@s = 표식, 위치·방향 = 지금 지점, 남은 횟수 #cs). 관통이 아니면 첫 적에서 멈춘다
execute if score #cStop tmp matches 1 run return 0
execute if score #cs tmp matches ..0 run return 0
scoreboard players remove #cs tmp 1
execute unless block ~ ~ ~ #rlk:dash_pass run return run particle minecraft:electric_spark ~ ~ ~ 0.1 0.1 0.1 0.2 6
particle minecraft:dust{color:[0.77f,0.55f,1.0f],scale:0.7f} ~ ~ ~ 0 0 0 0 1
execute if score #clPierce tmp matches 1 positioned ~-0.75 ~-0.75 ~-0.75 run tag @e[tag=rlk_mob,dx=0.5,dy=0.5,dz=0.5] add rlk_hit
execute if score #clPierce tmp matches 0 positioned ~-0.75 ~-0.75 ~-0.75 if entity @e[tag=rlk_mob,dx=0.5,dy=0.5,dz=0.5] run function rlk:char/clorinde/scan_hit
execute positioned ^ ^ ^0.5 run function rlk:char/clorinde/scan
