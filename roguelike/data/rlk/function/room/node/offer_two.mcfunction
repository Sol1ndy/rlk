data modify storage rlk:room excl set value []
data modify storage rlk:room excl append from storage rlk:room cur_nodes[0]
function rlk:room/node/draw
execute if score #nk tmp matches ..0 run return 0
data modify storage rlk:room cur_nodes append value 0
execute store result storage rlk:room cur_nodes[-1] int 1 run scoreboard players get #nk tmp
