# DPS 판 다시 쓰기
scoreboard players set #dpsR lob 0
execute store result storage rlk:lobby d.sum int 1 run scoreboard players get #dpsSum lob
scoreboard players operation #t lob = #dpsT lob
scoreboard players operation #t lob /= #c20 lob
execute store result storage rlk:lobby d.s int 1 run scoreboard players get #t lob
scoreboard players operation #t lob = #dpsT lob
scoreboard players operation #t lob %= #c20 lob
scoreboard players operation #t lob /= #c2 lob
execute store result storage rlk:lobby d.d int 1 run scoreboard players get #t lob
# DPS = 누적 × 20 / 틱 (넘침 방지: 1억이 넘으면 먼저 나눔)
scoreboard players set #t2 lob 0
execute if score #dpsT lob matches 1.. if score #dpsSum lob matches ..99999999 run scoreboard players operation #t2 lob = #dpsSum lob
execute if score #dpsT lob matches 1.. if score #dpsSum lob matches ..99999999 run scoreboard players operation #t2 lob *= #c20 lob
execute if score #dpsT lob matches 1.. if score #dpsSum lob matches ..99999999 run scoreboard players operation #t2 lob /= #dpsT lob
execute if score #dpsT lob matches 1.. if score #dpsSum lob matches 100000000.. run scoreboard players operation #t2 lob = #dpsSum lob
execute if score #dpsT lob matches 1.. if score #dpsSum lob matches 100000000.. run scoreboard players operation #t2 lob /= #dpsT lob
execute if score #dpsT lob matches 1.. if score #dpsSum lob matches 100000000.. run scoreboard players operation #t2 lob *= #c20 lob
execute store result storage rlk:lobby d.dps int 1 run scoreboard players get #t2 lob
data modify storage rlk:lobby d.st set value "더미를 때리면 측정을 시작합니다"
execute if score #dpsOn lob matches 1 if score #dpsIdle lob matches ..60 run data modify storage rlk:lobby d.st set value "측정 중 · 3초 동안 안 때리면 멈춤"
execute if score #dpsOn lob matches 1 if score #dpsIdle lob matches 61.. run data modify storage rlk:lobby d.st set value "측정 끝 · 다시 때리면 새로 잽니다"
function rlk:lobby/try/board_m with storage rlk:lobby d
