# 사라져 있는 중 (@s = 플레이어, at 몸)
scoreboard players remove @s arSk 1
particle minecraft:smoke ~ ~1 ~ 0.25 0.5 0.25 0.01 3
execute if score @s arSk matches ..0 run function rlk:char/arlecchino/skill_go
