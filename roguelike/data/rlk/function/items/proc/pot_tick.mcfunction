# @s = 솥, at @s (자기 방향 = 놓을 때 바라본 쪽). 0.5초 뒤부터 1.25초마다 불을 뿜는다(남은 횟수 pcVal)
scoreboard players add @s life 1
particle minecraft:smoke ~ ~0.6 ~ 0.1 0.1 0.1 0.01 1
scoreboard players operation #t1 itv = @s life
scoreboard players operation #t1 itv %= #potGap tmp
execute if score #t1 itv matches 10 run function rlk:items/proc/pot_fire
execute if score @s pcVal matches ..0 run kill @s
