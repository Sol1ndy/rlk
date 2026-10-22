execute if score #puDone mb matches 1 run return 0
execute unless data storage rlk:mboss pq[0] run return 0
function rlk:mboss/push/cap_one
data remove storage rlk:mboss pq[0]
function rlk:mboss/push/cap_loop
