# 노드 맵 제목 rlk:room nt = {name:"A · B", color: 첫 노드 색}
data modify storage rlk:room nt set value {name:"",color:"white"}
execute unless data storage rlk:room next[0] run return 0
execute store result storage rlk:room a.k int 1 run data get storage rlk:room next[0]
function rlk:room/node/load1 with storage rlk:room a
data modify storage rlk:room nt.name set from storage rlk:room n1.name
data modify storage rlk:room nt.color set from storage rlk:room n1.color
execute unless data storage rlk:room next[1] run return 0
execute store result storage rlk:room a.k int 1 run data get storage rlk:room next[1]
function rlk:room/node/load2 with storage rlk:room a
data modify storage rlk:room a.na set from storage rlk:room n1.name
data modify storage rlk:room a.nb set from storage rlk:room n2.name
function rlk:room/node/title2 with storage rlk:room a
