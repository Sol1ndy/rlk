# 일반 공격 춤추는 뱀 4타: 61% / 60% / 40% ×2 / 98% (@s = 플레이어, comboStep 0~3). 발차기는 가볍고 빠르다
scoreboard players set #naSteps tmp 4
scoreboard players set #coef tmp 61
execute if score @s comboStep matches 1 run scoreboard players set #coef tmp 60
execute if score @s comboStep matches 2 run scoreboard players set #coef tmp 40
execute if score @s comboStep matches 2 run scoreboard players set #naX2 tmp 1
execute if score @s comboStep matches 3.. run scoreboard players set #coef tmp 98
scoreboard players set #naD tmp 90
