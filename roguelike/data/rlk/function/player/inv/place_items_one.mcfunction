data modify storage rlk:pf id set from storage rlk:pinv q[0]
execute store result storage rlk:pf sl int 1 run scoreboard players get #si tmp
data remove storage rlk:pf base
data modify storage rlk:pf ver set from storage rlk:items ver
function rlk:player/inv/place_fetch with storage rlk:pf
scoreboard players add #si tmp 1
data remove storage rlk:pinv q[0]
function rlk:player/inv/place_items_loop
