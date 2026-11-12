# 상점 노드 진열대의 표시 기록(rlk:shop records.k<gid>) 지우기 (room/clear 에서). 운영자가 놓은 상점의 기록은 그대로
execute unless data storage rlk:shop nodekeys[0] run return 0
data modify storage rlk:shop fk.k set from storage rlk:shop nodekeys[0]
function rlk:shop/node/forget1 with storage rlk:shop fk
data remove storage rlk:shop nodekeys[0]
function rlk:shop/node/forget
