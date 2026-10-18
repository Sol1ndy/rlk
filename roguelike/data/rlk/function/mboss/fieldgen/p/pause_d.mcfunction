# GENERATED dispatcher: the running pattern's optional pause (the fight just froze), by #fgPat.
execute unless score #fgPat mb matches 1.. run return 0
execute if score #fgPNew mb matches 1 run return 0
execute if score #fgPat mb matches 1 run return run function rlk:mboss/fieldgen/p/bomb/pause
execute if score #fgPat mb matches 2 run return run function rlk:mboss/fieldgen/p/slam/pause
execute if score #fgPat mb matches 3 run return run function rlk:mboss/fieldgen/p/laser/pause
execute if score #fgPat mb matches 4 run return run function rlk:mboss/fieldgen/p/missile/pause
execute if score #fgPat mb matches 5 run return run function rlk:mboss/fieldgen/p/burst/pause
execute if score #fgPat mb matches 6 run return run function rlk:mboss/fieldgen/p/rock/pause
