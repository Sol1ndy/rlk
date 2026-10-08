execute unless data storage rlk:sort work[0] run return 0
data modify storage rlk:sort cur set from storage rlk:sort work[0]
function rlk:items/sort_rar_check with storage rlk:sort
data remove storage rlk:sort work[0]
function rlk:items/sort_rar_one
