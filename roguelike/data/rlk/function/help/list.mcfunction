# rlk:help q 의 id 마다 help/row 한 줄 (rlk:help r = row 의 나머지 인자 {pre, post, st, np, ns}). q 는 비워진다
execute unless data storage rlk:help q[0] run return 0
data modify storage rlk:help r.id set from storage rlk:help q[0]
function rlk:help/row with storage rlk:help r
data remove storage rlk:help q[0]
function rlk:help/list
