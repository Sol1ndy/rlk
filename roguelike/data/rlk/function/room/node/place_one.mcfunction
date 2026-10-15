# macro: r = mids 의 순번
$data modify storage rlk:room a.si set from storage rlk:room mids[$(r)]
data modify storage rlk:room a.sk set from storage rlk:room pq[0]
function rlk:room/gen_special2 with storage rlk:room a
$data remove storage rlk:room mids[$(r)]
