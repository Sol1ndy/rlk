# 날아가기 시작 (@s = 새 풀 원핵/기만의 핵, 시작 = 지금 자리, 도착 = rlk_cpos)
execute store result score @s cX0 run data get entity @s Pos[0] 1000
execute store result score @s cY0 run data get entity @s Pos[1] 1000
execute store result score @s cZ0 run data get entity @s Pos[2] 1000
execute store result score @s cX1 run data get entity @e[tag=rlk_cpos,limit=1] Pos[0] 1000
execute store result score @s cY1 run data get entity @e[tag=rlk_cpos,limit=1] Pos[1] 1000
execute store result score @s cZ1 run data get entity @e[tag=rlk_cpos,limit=1] Pos[2] 1000
scoreboard players set @s cF 1
data merge entity @s {teleport_duration:1}
