# 이번 틱의 #btHold · #btInv 를 적용한다(beat/p/clock · beat/d/clock): 멈춘 틱 수, 전투 시계 보정, 바닐라 AI 몹의 정지 / 풀기
execute if score #btHold cb matches 1 run scoreboard players add #btLag cb 1
scoreboard players operation #btAdj cb = #btLag cb
scoreboard players operation #btAdj cb -= #btHold cb
execute if score #btHold cb matches 1 unless score #btHeld cb matches 1 run function rlk:player/def/beat/hold_on
execute if score #btHold cb matches 0 if score #btHeld cb matches 1 run function rlk:player/def/beat/hold_off
