execute unless data storage rlk:tune iq[0] run return 0
data modify storage rlk:tune cur set value {}
data modify storage rlk:tune cur.id set from storage rlk:tune iq[0]
function rlk:items/tune/capture with storage rlk:tune cur
function rlk:items/tune/apply with storage rlk:tune cur
data remove storage rlk:tune iq[0]
function rlk:items/tune/init_loop
