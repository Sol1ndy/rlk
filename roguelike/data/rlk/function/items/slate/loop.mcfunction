execute unless data storage rlk:scan sq[0] run return 0
data modify storage rlk:scan scur set from storage rlk:scan sq[0]
data modify storage rlk:scan nxt set value ""
execute if data storage rlk:scan sq[1] run data modify storage rlk:scan nxt set from storage rlk:scan sq[1]
execute if data storage rlk:scan {scur:"old_slate"} run function rlk:items/slate/hit
data modify storage rlk:scan prev set from storage rlk:scan scur
data remove storage rlk:scan sq[0]
function rlk:items/slate/loop
