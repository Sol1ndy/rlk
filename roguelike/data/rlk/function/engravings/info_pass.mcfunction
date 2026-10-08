execute unless data storage rlk:eng q[0] run return 0
data modify storage rlk:eng e set from storage rlk:eng q[0]
function rlk:engravings/info_pass_one with storage rlk:eng
data remove storage rlk:eng q[0]
function rlk:engravings/info_pass
