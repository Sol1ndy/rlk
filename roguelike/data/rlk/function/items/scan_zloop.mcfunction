execute unless data storage rlk:scan ids[0] run return 0
data modify storage rlk:scan cur set from storage rlk:scan ids[0]
function rlk:items/scan_zero with storage rlk:scan
data remove storage rlk:scan ids[0]
function rlk:items/scan_zloop
