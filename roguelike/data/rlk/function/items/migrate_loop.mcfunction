execute unless data storage rlk:mig q[0] run return 0
data modify storage rlk:mig cmp set value "favonius_bow"
execute store success score #migD tmp run data modify storage rlk:mig cmp set from storage rlk:mig q[0]
execute if score #migD tmp matches 1 run data modify storage rlk:mig out append from storage rlk:mig q[0]
data remove storage rlk:mig q[0]
function rlk:items/migrate_loop
