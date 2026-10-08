# 보는 방향(수평)으로 살짝 전진 (@s = 플레이어). 입력: #nSpd tmp(틱당 0.1칸 × 값) · #nT tmp(틱). 대쉬 중에는 하지 않는다. 벽은 대쉬와 같은 방식으로 막힌다
execute if score @s dashMoveT matches 1.. run return 0
execute store result score #cx tmp run data get entity @e[tag=rlk_body,limit=1] Pos[0] 100
execute store result score #cz tmp run data get entity @e[tag=rlk_body,limit=1] Pos[2] 100
function rlk:player/dash_lookvec
function rlk:player/dash_norm
scoreboard players operation @s dashDX = #ux tmp
scoreboard players operation @s dashDX *= #nSpd tmp
scoreboard players operation @s dashDZ = #uz tmp
scoreboard players operation @s dashDZ *= #nSpd tmp
scoreboard players operation @s dashUX = #ux tmp
scoreboard players operation @s dashUZ = #uz tmp
scoreboard players operation @s stepT = #nT tmp
