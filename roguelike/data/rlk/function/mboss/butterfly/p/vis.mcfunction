# GENERATED: hz_vis events of hazards with #hzVis = pattern id x 10 + k (k 1-9), @s = hazard marker.
scoreboard players operation #bfV mb = @s mbHzV
scoreboard players operation #bfV mb /= #c10 mb
execute if score #bfV mb matches 13 run return run function rlk:mboss/butterfly/p/sweep/vis
