# 기본 공격 5타: 60% ×2 / 105% / 135% / 83% ×2 / 195% (#step = 0~4)
scoreboard players set #bSteps tmp 5
execute if score #step tmp matches 0 run scoreboard players set #bCoef tmp 60
execute if score #step tmp matches 0 run scoreboard players set #bN tmp 2
execute if score #step tmp matches 1 run scoreboard players set #bCoef tmp 105
execute if score #step tmp matches 2 run scoreboard players set #bCoef tmp 135
execute if score #step tmp matches 3 run scoreboard players set #bCoef tmp 83
execute if score #step tmp matches 3 run scoreboard players set #bN tmp 2
execute if score #step tmp matches 4.. run scoreboard players set #bCoef tmp 195
