# 시전 중 (@s = 플레이어, at 몸): 힘이 모이는 효과 → 끝나면 발동
execute if score @s dead matches 1 run return run function rlk:char/burst_wind_end
scoreboard players remove @s buT 1
particle minecraft:enchant ~ ~1.6 ~ 0.9 0.9 0.9 0.6 10
particle minecraft:end_rod ~ ~0.2 ~ 0.6 0.05 0.6 0.01 2
execute if score @s buT matches 1.. run return 0
function rlk:char/burst_wind_end
function rlk:char/burst_go
