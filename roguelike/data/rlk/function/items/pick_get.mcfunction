# cand[idx] → cid (macro: idx)
data remove storage rlk:pick cid
$data modify storage rlk:pick cid set from storage rlk:pick cand[$(idx)]
