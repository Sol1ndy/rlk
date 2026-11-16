# Internal: the anchor string of clip $(c) tick $(t) (the held last pose past the end).
$data modify storage rlk:hr rig.q.p set from storage rlk:hr rig.an[$(c)].$(a)[$(t)]
execute unless data storage rlk:hr rig.q.p run data modify storage rlk:hr rig.q.p set value "^ ^1.8 ^"
function rlk:boss/scarlet/rig/anchor/r/go with storage rlk:hr rig.q
data remove storage rlk:hr rig.q.p
