# 낙사 구간 2단계: 구덩이를 파고 바닥을 깐다(몹 길찾기가 피하는 블록 두 겹)
execute unless data storage rlk:room q[0] run return 0
data modify storage rlk:room it set from storage rlk:room q[0]
data modify storage rlk:room it merge from storage rlk:room th
function rlk:room/zb_pit_hole with storage rlk:room it
data remove storage rlk:room q[0]
function rlk:room/zb_pit_holes
