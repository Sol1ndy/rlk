# GENERATED dispatcher: the running pattern's optional pause (the fight just froze), by #fgPat.
execute unless score #fgPat mb matches 1.. run return 0
execute if score #fgPNew mb matches 1 run return 0
execute if score #fgPat mb matches 11 run return run function rlk:mboss/fieldgen/p/fzone/pause
execute if score #fgPat mb matches 12 run return run function rlk:mboss/fieldgen/p/frock/pause
execute if score #fgPat mb matches 21 run return run function rlk:mboss/fieldgen/p/waves/pause
