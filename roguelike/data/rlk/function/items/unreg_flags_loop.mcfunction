execute unless data storage rlk:items fscan[0] run return 0
data modify storage rlk:items fcur set from storage rlk:items fscan[0]
function rlk:items/unreg_flag with storage rlk:items
data remove storage rlk:items fscan[0]
function rlk:items/unreg_flags_loop
