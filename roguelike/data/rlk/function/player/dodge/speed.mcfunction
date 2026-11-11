# @s = 플레이어 (player/dash_move_tick). 이번 틱의 닷지 이동 속도 #dgSp tmp(칸 × 1000 / 틱), 남은 이동 틱 dashMoveT 로:
#   일반 닷지(#dgMv cb 1)  3틱 = 0.5 + 0.3 + 0.2 = 1.0칸(빠르게 나가 멈춤; 원작: 몸 높이의 절반쯤 = 0.9칸, 12~15프레임)
#   더블 닷지의 두 번째 동작(#dgMv cb 2)  6틱 = 0.25 + 0.4 + 0.4 + 0.35 + 0.25 + 0.15 = 1.8칸(도약 · 공중 · 착지)
# 예전 대쉬는 3틱 내내 1칸(3칸)이었다
scoreboard players set #dgSp tmp 200
execute if score #dgMv cb matches 2 run return run function rlk:player/dodge/speed2
execute if score @s dashMoveT matches 3 run scoreboard players set #dgSp tmp 500
execute if score @s dashMoveT matches 2 run scoreboard players set #dgSp tmp 300
