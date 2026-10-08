execute unless data storage rlk:rb xq[0] run return 0
data modify storage rlk:rb x.cur set from storage rlk:rb xq[0]
function rlk:codex/lists_one with storage rlk:rb x
data remove storage rlk:rb xq[0]
function rlk:codex/lists_loop
