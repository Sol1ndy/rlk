# GENERATED: hz_vis events of hazards with #hzVis = pattern id x 10 + k (k 1-9), @s = hazard marker.
scoreboard players operation #fgV mb = @s mbHzV
scoreboard players operation #fgV mb /= #c10 mb
execute if score #fgV mb matches 1 run return run function rlk:mboss/fieldgen/p/bomb/vis
execute if score #fgV mb matches 2 run return run function rlk:mboss/fieldgen/p/slam/vis
execute if score #fgV mb matches 3 run return run function rlk:mboss/fieldgen/p/laser/vis
execute if score #fgV mb matches 4 run return run function rlk:mboss/fieldgen/p/missile/vis
execute if score #fgV mb matches 5 run return run function rlk:mboss/fieldgen/p/burst/vis
execute if score #fgV mb matches 6 run return run function rlk:mboss/fieldgen/p/rock/vis
execute if score #fgV mb matches 11 run return run function rlk:mboss/fieldgen/p/fzone/vis
execute if score #fgV mb matches 12 run return run function rlk:mboss/fieldgen/p/frock/vis
