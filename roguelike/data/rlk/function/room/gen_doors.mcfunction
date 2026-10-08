execute unless data storage rlk:room q[0] run return 0
data modify storage rlk:room it set from storage rlk:room q[0]
function rlk:room/gen_door with storage rlk:room it
data remove storage rlk:room q[0]
function rlk:room/gen_doors
