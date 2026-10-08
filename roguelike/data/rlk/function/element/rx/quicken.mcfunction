# 활성 (번개+풀): 두 원소를 같은 양만큼 소모하고 활성 상태로. 활성 중 번개 = 촉진, 풀 = 발산. macro: e(붙어 있던 원소)
$scoreboard players operation #m tmp = @s a$(e)
execute if score #elU tmp < #m tmp run scoreboard players operation #m tmp = #elU tmp
$scoreboard players operation @s a$(e) -= #m tmp
# 지속시간(틱) = 5초 × 소모량(U) + 6초
scoreboard players operation #qt tmp = #m tmp
scoreboard players operation #qt tmp /= #st10 tmp
scoreboard players add #qt tmp 120
execute unless score @s quickT >= #qt tmp run scoreboard players operation @s quickT = #qt tmp
scoreboard players set #rx tmp 14
