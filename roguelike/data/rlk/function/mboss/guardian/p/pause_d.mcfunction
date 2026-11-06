# GENERATED dispatcher: the running pattern's optional pause (the fight just froze: player dead or
# reviving), by #gdPat. Not for a pattern picked this tick (its start has not run yet).
execute unless score #gdPat mb matches 1.. run return 0
execute if score #gdPNew mb matches 1 run return 0
execute if score #gdPat mb matches 4 run return run function rlk:mboss/guardian/p/pull/pause
