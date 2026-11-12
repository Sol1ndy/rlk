$data modify storage rlk:room cur_nodes set from storage rlk:room offers[$(i)].nodes
execute unless data storage rlk:room cur_nodes[0] run return 0
execute store result storage rlk:room a.k int 1 run data get storage rlk:room cur_nodes[0]
function rlk:room/node/load1 with storage rlk:room a
scoreboard players set #oact tmp 9
scoreboard players operation #oarg tmp = #slot tmp
execute unless data storage rlk:room cur_nodes[1] run return run function rlk:room/obj/make_node with storage rlk:room n1
execute store result storage rlk:room a.k int 1 run data get storage rlk:room cur_nodes[1]
function rlk:room/node/load2 with storage rlk:room a
data modify storage rlk:room n12 set value {}
data modify storage rlk:room n12.item set from storage rlk:room n1.item
data modify storage rlk:room n12.model set from storage rlk:room n1.model
data modify storage rlk:room n12.name set from storage rlk:room n1.name
data modify storage rlk:room n12.desc set from storage rlk:room n1.desc
data modify storage rlk:room n12.color set from storage rlk:room n1.color
data modify storage rlk:room n12.model2 set from storage rlk:room n2.model
data modify storage rlk:room n12.item2 set from storage rlk:room n2.item
data modify storage rlk:room n12.name2 set from storage rlk:room n2.name
data modify storage rlk:room n12.desc2 set from storage rlk:room n2.desc
data modify storage rlk:room n12.color2 set from storage rlk:room n2.color
function rlk:room/obj/make_node2 with storage rlk:room n12
