execute unless data storage rlk:sort rarities[0] run return 0
data modify storage rlk:sort rar set from storage rlk:sort rarities[0]
data modify storage rlk:sort work set from storage rlk:sort src
function rlk:items/sort_rar_one
data remove storage rlk:sort rarities[0]
function rlk:items/sort_rar_loop
