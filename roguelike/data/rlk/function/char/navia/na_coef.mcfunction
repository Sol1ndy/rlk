# 일반 공격 4타: 150% / 140% / 55% ×3 / 215% (@s = 플레이어, comboStep 0~3). 양손검이라 다음 타까지가 길다(#naD)
scoreboard players set #naSteps tmp 4
scoreboard players set #coef tmp 150
execute if score @s comboStep matches 1 run scoreboard players set #coef tmp 140
execute if score @s comboStep matches 2 run scoreboard players set #coef tmp 55
execute if score @s comboStep matches 2 run scoreboard players set #naX2 tmp 2
execute if score @s comboStep matches 3.. run scoreboard players set #coef tmp 215
scoreboard players set #naD tmp 155
execute if score @s comboStep matches 2 run scoreboard players set #naD tmp 190
