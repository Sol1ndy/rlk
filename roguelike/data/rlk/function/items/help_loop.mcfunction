# items/help: rlk:help q 의 아이템마다, 등급이 바뀌면 등급 줄을 먼저
execute unless data storage rlk:help q[0] run return 0
data modify storage rlk:help r.id set from storage rlk:help q[0]
function rlk:items/help_rar with storage rlk:help r
function rlk:help/row with storage rlk:help r
data remove storage rlk:help q[0]
function rlk:items/help_loop
