# sq 의 노드를 이번 챕터 기록(rlk:room seen)에 추가
execute unless data storage rlk:room sq[0] run return 0
data modify storage rlk:room seen append from storage rlk:room sq[0]
data remove storage rlk:room sq[0]
function rlk:room/node/seen_loop
