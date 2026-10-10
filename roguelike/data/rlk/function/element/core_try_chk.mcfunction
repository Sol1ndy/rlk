# 후보 자리 (위치 = 후보, 높이 = 몹 발)
execute unless block ~ ~0.2 ~ #rlk:dash_pass run return 0
execute unless block ~ ~0.8 ~ #rlk:dash_pass run return 0
execute if entity @e[tag=rlk_mob,distance=..1.1] run return 0
tp @e[tag=rlk_cpos] ~ ~ ~
scoreboard players set #cpOk tmp 1
