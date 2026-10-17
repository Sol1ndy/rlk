execute unless data storage rlk:mboss cand[0] run return 0
execute store result score #v mb run data get storage rlk:mboss cand[0].w
execute if score #r mb < #v mb run return run data modify storage rlk:mboss cur set from storage rlk:mboss cand[0]
scoreboard players operation #r mb -= #v mb
data remove storage rlk:mboss cand[0]
function rlk:mboss/roll_pick_loop
