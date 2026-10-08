# 스택당 공속 +1.5(스택 × 3 / 2, 소수점 버림), 이속 +1
scoreboard players operation #pd tmp = @s pdStack
scoreboard players operation #pd tmp *= #c3 tmp
scoreboard players operation #pd tmp /= #st2 tmp
scoreboard players operation @s atkSpeed += #pd tmp
scoreboard players operation @s moveSpeed += @s pdStack
