execute unless data storage rlk:lvpick dropq[0] run return 0
data modify storage rlk:gv id set from storage rlk:lvpick dropq[0]
function rlk:items/drop with storage rlk:gv
data remove storage rlk:lvpick dropq[0]
execute positioned ~0.9 ~ ~ run function rlk:lvup/drop_loop
