execute unless data storage rlk:room wq[0] run return 0
data modify storage rlk:room a.e set from storage rlk:room wq[0]
function rlk:root/split_one with storage rlk:room a
data remove storage rlk:room wq[0]
function rlk:root/split_loop
