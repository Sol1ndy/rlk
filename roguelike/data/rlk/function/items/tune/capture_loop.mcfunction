execute unless data storage rlk:tune q[0] run return 0
function rlk:items/tune/capture_one with storage rlk:tune q[0]
data modify storage rlk:tune qo append from storage rlk:tune q[0]
data remove storage rlk:tune q[0]
function rlk:items/tune/capture_loop
