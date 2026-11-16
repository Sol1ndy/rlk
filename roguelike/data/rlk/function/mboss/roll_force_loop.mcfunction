execute unless data storage rlk:mboss wq[0] run return 0
execute store result score #v mb run data get storage rlk:mboss wq[0].n
execute if score #v mb = #mbForce mb run return run data modify storage rlk:mboss cur set from storage rlk:mboss wq[0]
data remove storage rlk:mboss wq[0]
function rlk:mboss/roll_force_loop
