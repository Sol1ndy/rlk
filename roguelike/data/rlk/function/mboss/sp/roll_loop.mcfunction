execute unless data storage rlk:mboss wq[0] run return 0
scoreboard players set #ok mb 1
execute store result score #v mb run data get storage rlk:mboss wq[0].w
execute if score #v mb matches ..0 run scoreboard players set #ok mb 0
execute store result score #v mb run data get storage rlk:mboss wq[0].minCh
execute if score #mbUseCh mb matches 1 if score #chapter room < #v mb run scoreboard players set #ok mb 0
execute store result score #v mb run data get storage rlk:mboss wq[0].maxCh
execute if score #mbUseCh mb matches 1 if score #chapter room > #v mb run scoreboard players set #ok mb 0
execute if score #ok mb matches 1 if score #mbUseMet mb matches 1 run function rlk:mboss/sp/roll_met with storage rlk:mboss wq[0]
execute if score #ok mb matches 1 run data modify storage rlk:mboss cand append from storage rlk:mboss wq[0]
execute if score #ok mb matches 1 store result score #v mb run data get storage rlk:mboss wq[0].w
execute if score #ok mb matches 1 run scoreboard players operation #wsum mb += #v mb
data remove storage rlk:mboss wq[0]
function rlk:mboss/sp/roll_loop
