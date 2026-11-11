# @s = 플레이어 (player/dash_move_tick). 이번 틱의 닷지 이동 속도 #dgSp tmp(칸 × 1000 / 틱), 남은 이동 틱 dashMoveT 로(round W; 원작
# dodge.mp4 에서 잰 것은 tools/dev/plan/combat/wp_progress.md):
#   1 제자리 비틀기(방향키 없음)   3틱 = 0.2 + 0.12 + 0.08 = 0.4칸(원작: 0.3 몸 높이 미만, 12프레임)
#   3 내딛는 걸음(방향키)          5틱 = 0.5 + 0.4 + 0.35 + 0.2 + 0.15 = 1.6칸(원작: 낮은 한 걸음 1.4 몸 높이, 20~25프레임)
#   4 백스텝(공격을 피함)          4틱 = 0.9 + 0.8 + 0.6 + 0.4 = 2.7칸(원작: 적에게서 똑바로 1.9~2.2 몸 높이, 5~12프레임)
#   2 옆돌기(더블 닷지)            6틱 = 0.3 + 0.45 + 0.45 + 0.45 + 0.35 + 0.2 = 2.2칸(원작: 1.3 몸 높이 더, 20프레임)
# 예전 대쉬는 3틱 내내 1칸(3칸)이었다
execute if score #dgMv cb matches 2 run return run function rlk:player/dodge/speed2
execute if score #dgMv cb matches 3 run return run function rlk:player/dodge/speed3
execute if score #dgMv cb matches 4 run return run function rlk:player/dodge/speed4
scoreboard players set #dgSp tmp 80
execute if score @s dashMoveT matches 3 run scoreboard players set #dgSp tmp 200
execute if score @s dashMoveT matches 2 run scoreboard players set #dgSp tmp 120
