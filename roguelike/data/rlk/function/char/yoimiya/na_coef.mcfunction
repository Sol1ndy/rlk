# 기본 공격 5타: 40% ×2 / 70% / 90% / 55% ×2 / 130% (#step = 0~4)
scoreboard players set #bSteps tmp 5
execute if score #step tmp matches 0 run scoreboard players set #bCoef tmp 40
execute if score #step tmp matches 0 run scoreboard players set #bN tmp 2
execute if score #step tmp matches 1 run scoreboard players set #bCoef tmp 70
execute if score #step tmp matches 2 run scoreboard players set #bCoef tmp 90
execute if score #step tmp matches 3 run scoreboard players set #bCoef tmp 55
execute if score #step tmp matches 3 run scoreboard players set #bN tmp 2
execute if score #step tmp matches 4.. run scoreboard players set #bCoef tmp 130
