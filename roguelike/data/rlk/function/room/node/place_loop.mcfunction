execute unless data storage rlk:room pq[0] run return 0
execute unless data storage rlk:room mids[0] run return 0
execute store result score #mc tmp run data get storage rlk:room mids
execute store result score #r tmp run random value 0..999
scoreboard players operation #r tmp %= #mc tmp
execute store result storage rlk:room a.r int 1 run scoreboard players get #r tmp
function rlk:room/node/place_one with storage rlk:room a
data remove storage rlk:room pq[0]
function rlk:room/node/place_loop
