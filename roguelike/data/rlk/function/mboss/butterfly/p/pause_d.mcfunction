# GENERATED dispatcher: the running pattern's optional pause (the fight just froze), by #bfPat.
execute unless score #bfPat mb matches 1.. run return 0
execute if score #bfPNew mb matches 1 run return 0
execute if score #bfPat mb matches 13 run return run function rlk:mboss/butterfly/p/sweep/pause
