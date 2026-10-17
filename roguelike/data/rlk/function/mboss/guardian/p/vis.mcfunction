# GENERATED: hz_vis events of hazards with #hzVis = pattern id x 10 + k (k 1-9), @s = hazard marker.
scoreboard players operation #gdV mb = @s mbHzV
scoreboard players operation #gdV mb /= #c10 mb
execute if score #gdV mb matches 3 run return run function rlk:mboss/guardian/p/slam/vis
execute if score #gdV mb matches 4 run return run function rlk:mboss/guardian/p/pull/vis
