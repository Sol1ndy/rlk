# 잔향 한 칸 꺼냄 (@s = 플레이어): 2 → 1, 3 → 2
scoreboard players operation @s rnE1 = @s rnE2
scoreboard players operation @s rnE2 = @s rnE3
scoreboard players set @s rnE3 0
