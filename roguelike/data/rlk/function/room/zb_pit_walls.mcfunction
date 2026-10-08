# 낙사 구간 1단계: 구덩이 둘레(바닥판 아래 y 186~199)를 벽 블록으로 채운다
execute unless data storage rlk:room q[0] run return 0
data modify storage rlk:room it set from storage rlk:room q[0]
data modify storage rlk:room it merge from storage rlk:room th
function rlk:room/zb_pit_wall with storage rlk:room it
data remove storage rlk:room q[0]
function rlk:room/zb_pit_walls
