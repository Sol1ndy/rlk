execute unless data storage rlk:lvpick xq[0] run return 0
data modify storage rlk:lvpick a.e set from storage rlk:lvpick xq[0]
function rlk:lvup/eng/item_add with storage rlk:lvpick a
data remove storage rlk:lvpick xq[0]
function rlk:lvup/eng/item_loop
