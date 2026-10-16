# 일반 공격 4타: 256% / 239% / 94% ×3 / 366% (@s = 플레이어, comboStep 0~3). 양손검이라 다음 타까지가 길다(#naD)
# 모션이 원신과 같은 박자(재생 100%, 연타 한 바퀴 75틱)로 느려진 만큼 계수를 올려 초당 피해를 예전(150/140/55×3/215%, 44틱)과 같게 맞춘다(×75/44)
scoreboard players set #naSteps tmp 4
scoreboard players set #coef tmp 256
execute if score @s comboStep matches 1 run scoreboard players set #coef tmp 239
execute if score @s comboStep matches 2 run scoreboard players set #coef tmp 94
execute if score @s comboStep matches 2 run scoreboard players set #naX2 tmp 2
execute if score @s comboStep matches 3.. run scoreboard players set #coef tmp 366
scoreboard players set #naD tmp 155
execute if score @s comboStep matches 2 run scoreboard players set #naD tmp 190
