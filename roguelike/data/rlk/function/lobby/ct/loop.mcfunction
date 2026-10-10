execute unless data storage rlk:lobby ct.q[0] run return 0
data modify storage rlk:lobby ct.list append value {text:"\n"}
data modify storage rlk:lobby ct.list append from storage rlk:lobby ct.q[0]
data remove storage rlk:lobby ct.q[0]
function rlk:lobby/ct/loop
