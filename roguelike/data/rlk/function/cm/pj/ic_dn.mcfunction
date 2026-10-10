# 떨어질 자리(바닥)에 폭발 범위 표시
scoreboard players add #rl tmp 1
execute if score #rl tmp matches 24.. run return 0
execute unless block ~ ~-0.5 ~ #rlk:cm_pass run return run function rlk:cm/pj/ic_ring
execute positioned ~ ~-0.5 ~ run function rlk:cm/pj/ic_dn
