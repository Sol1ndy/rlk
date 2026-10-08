# 일반 공격 5타: 110% / 100% / 65% ×2 / 120% / 160% (@s = 플레이어, comboStep 0~4)
scoreboard players operation #skStep tmp = @s comboStep
scoreboard players set #skDepUsed tmp 0
scoreboard players set #coef tmp 110
execute if score #skStep tmp matches 1 run scoreboard players set #coef tmp 100
execute if score #skStep tmp matches 2 run scoreboard players set #coef tmp 65
execute if score #skStep tmp matches 3 run scoreboard players set #coef tmp 120
execute if score #skStep tmp matches 4.. run scoreboard players set #coef tmp 160
# 박자(다음 타까지 간격 %): 빠르게 두 번 → X자(두 번 베기)는 길게 → 올려베기
execute if score #skStep tmp matches 0 run scoreboard players set #naD tmp 85
execute if score #skStep tmp matches 1 run scoreboard players set #naD tmp 85
execute if score #skStep tmp matches 2 run scoreboard players set #naD tmp 130
execute if score #skStep tmp matches 3 run scoreboard players set #naD tmp 100
