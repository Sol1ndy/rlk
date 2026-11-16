execute unless data storage rlk:help q[0] run return 0
data modify storage rlk:help it set from storage rlk:help q[0]
function rlk:char/select_help_one with storage rlk:help
data remove storage rlk:help q[0]
function rlk:char/select_help_loop
