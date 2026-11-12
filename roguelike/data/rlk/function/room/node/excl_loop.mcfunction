execute unless data storage rlk:room xq[0] run return 0
execute store result score #xk tmp run data get storage rlk:room xq[0]
execute if score #xk tmp = #ck tmp run return run scoreboard players set #cok tmp 0
data remove storage rlk:room xq[0]
function rlk:room/node/excl_loop
