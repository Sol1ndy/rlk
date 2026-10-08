# 장식 목록(rlk:room q)을 차례로 놓는다
execute unless data storage rlk:room q[0] run return 0
data modify storage rlk:room it set from storage rlk:room q[0]
function rlk:room/deco/op with storage rlk:room it
data remove storage rlk:room q[0]
function rlk:room/deco_loop
