# 일반 공격 6타: 90% / 95% / 120% / 65% ×2 / 130% / 160% (@s = 플레이어, comboStep 0~5)
scoreboard players set #naSteps tmp 6
scoreboard players set #arUsed tmp 0
scoreboard players set #coef tmp 90
execute if score @s comboStep matches 1 run scoreboard players set #coef tmp 95
execute if score @s comboStep matches 2 run scoreboard players set #coef tmp 120
execute if score @s comboStep matches 3 run scoreboard players set #coef tmp 65
execute if score @s comboStep matches 3 run scoreboard players set #naX2 tmp 1
execute if score @s comboStep matches 4 run scoreboard players set #coef tmp 130
execute if score @s comboStep matches 5.. run scoreboard players set #coef tmp 160
# 박자(다음 타까지 간격 %): 휩쓸기 → 빠르게 찌르기 → 한 바퀴 돌기(두 번)는 길게
execute if score @s comboStep matches 0 run scoreboard players set #naD tmp 100
execute if score @s comboStep matches 1 run scoreboard players set #naD tmp 85
execute if score @s comboStep matches 2 run scoreboard players set #naD tmp 85
execute if score @s comboStep matches 3 run scoreboard players set #naD tmp 140
execute if score @s comboStep matches 4 run scoreboard players set #naD tmp 90
