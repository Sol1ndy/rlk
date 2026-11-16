# @s 의 속도 = 실행 방향 x #c2Fw/1000 칸/틱, 위로 #c2Up/1000 (#c2Up < 0 이면 세로 속도는 그대로). 블록 충돌은 바닐라 물리가 맡음
function rlk:cm/c2/vec
scoreboard players operation #c2vx tmp *= #c2Fw tmp
scoreboard players operation #c2vx tmp /= #c2c1000 tmp
scoreboard players operation #c2vz tmp *= #c2Fw tmp
scoreboard players operation #c2vz tmp /= #c2c1000 tmp
execute store result entity @s Motion[0] double 0.001 run scoreboard players get #c2vx tmp
execute store result entity @s Motion[2] double 0.001 run scoreboard players get #c2vz tmp
execute if score #c2Up tmp matches 0.. store result entity @s Motion[1] double 0.001 run scoreboard players get #c2Up tmp
