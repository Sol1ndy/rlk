execute unless data storage rlk:eng gid[0] run return 0
data modify storage rlk:eng sq append value {}
data modify storage rlk:eng sq[-1].id set from storage rlk:eng gid[0]
data modify storage rlk:eng sq[-1].n set from storage rlk:eng gq[0].n
data remove storage rlk:eng gid[0]
function rlk:engravings/info_rest_sq2
