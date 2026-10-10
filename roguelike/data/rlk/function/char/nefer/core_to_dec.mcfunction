# 풀 씨앗 → 기만의 핵 (@s = 풀 씨앗)
scoreboard players set #cpHere tmp 1
execute positioned ~ ~-0.5 ~ run function rlk:char/nefer/dec_spawn
scoreboard players set #cpHere tmp 0
kill @s
