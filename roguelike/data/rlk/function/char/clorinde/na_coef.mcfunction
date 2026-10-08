# 일반 공격 5타: 105% / 100% / 65% ×2 / 130% / 175% (@s = 플레이어, comboStep 0~4)
scoreboard players set #naSteps tmp 5
scoreboard players set #coef tmp 105
execute if score @s comboStep matches 1 run scoreboard players set #coef tmp 100
execute if score @s comboStep matches 2 run scoreboard players set #coef tmp 65
execute if score @s comboStep matches 2 run scoreboard players set #naX2 tmp 1
execute if score @s comboStep matches 3 run scoreboard players set #coef tmp 130
execute if score @s comboStep matches 4.. run scoreboard players set #coef tmp 175
# 박자(다음 타까지 간격 %): 찌르고 바로 베기 → 연속 찌르기는 길게
execute if score @s comboStep matches 0 run scoreboard players set #naD tmp 70
execute if score @s comboStep matches 1 run scoreboard players set #naD tmp 100
execute if score @s comboStep matches 2 run scoreboard players set #naD tmp 130
execute if score @s comboStep matches 3 run scoreboard players set #naD tmp 100
