# 실행 위치 = 카메라 조준선의 검사점. 투사체와 같은 통과 블록을 사용하여 벽 뒤 적을 고르지 않는다.
execute unless block ~ ~ ~ #rlk:dash_pass run return run tp @e[tag=rlk_rn_aim,limit=1] ~ ~ ~
execute positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[tag=rlk_mob,dx=0,dy=0,dz=0,limit=1] run return run function rlk:char/ronova/na_aim_hit
execute if score #rnAimStep tmp matches 144.. run return run tp @e[tag=rlk_rn_aim,limit=1] ~ ~ ~
scoreboard players add #rnAimStep tmp 1
execute positioned ^ ^ ^0.25 run function rlk:char/ronova/na_aim_step
