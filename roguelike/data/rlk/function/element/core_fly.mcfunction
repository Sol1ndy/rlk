# 날아가는 중 (@s = 풀 원핵/기만의 핵, cF = 지난 틱 1~#cN): 위치 = 시작 + (도착 - 시작) × t/N, 높이 + #cArc × t × (N - t)
scoreboard players operation #fx tmp = @s cX1
scoreboard players operation #fx tmp -= @s cX0
scoreboard players operation #fx tmp *= @s cF
scoreboard players operation #fx tmp /= #cN tmp
scoreboard players operation #fx tmp += @s cX0
scoreboard players operation #fy tmp = @s cY1
scoreboard players operation #fy tmp -= @s cY0
scoreboard players operation #fy tmp *= @s cF
scoreboard players operation #fy tmp /= #cN tmp
scoreboard players operation #fy tmp += @s cY0
scoreboard players operation #fz tmp = @s cZ1
scoreboard players operation #fz tmp -= @s cZ0
scoreboard players operation #fz tmp *= @s cF
scoreboard players operation #fz tmp /= #cN tmp
scoreboard players operation #fz tmp += @s cZ0
scoreboard players operation #fa tmp = #cN tmp
scoreboard players operation #fa tmp -= @s cF
scoreboard players operation #fa tmp *= @s cF
scoreboard players operation #fa tmp *= #cArc tmp
scoreboard players operation #fy tmp += #fa tmp
execute store result storage rlk:cf p.x double 0.001 run scoreboard players get #fx tmp
execute store result storage rlk:cf p.y double 0.001 run scoreboard players get #fy tmp
execute store result storage rlk:cf p.z double 0.001 run scoreboard players get #fz tmp
function rlk:element/core_fly_tp with storage rlk:cf p
execute at @s run particle minecraft:dust{color:[0.6,0.95,0.35],scale:0.8} ~ ~0.3 ~ 0.05 0.05 0.05 0 2
execute if score @s cF >= #cN tmp run return run function rlk:element/core_land
scoreboard players add @s cF 1
