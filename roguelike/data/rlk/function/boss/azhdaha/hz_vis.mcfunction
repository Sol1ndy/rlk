# Hook hz_vis (@s = hazard marker, #hzEv 0 create / 1 strike / 2 end): routed by mbHzV / 10 = the pattern id.
scoreboard players operation #azV mb = @s mbHzV
scoreboard players operation #azV mb /= #c10 mb
execute if score #azV mb matches 41 run return run function rlk:boss/azhdaha/p/frost/vis
execute if score #azV mb matches 42 run return run function rlk:boss/azhdaha/p/bolt/vis
execute if score #azV mb matches 43 run return run function rlk:boss/azhdaha/p/icicle/vis
execute if score #azV mb matches 44 run return run function rlk:boss/azhdaha/p/shell/vis
execute if score #azV mb matches 45 run return run function rlk:boss/azhdaha/p/icespike/vis
execute if score #azV mb matches 46 run return run function rlk:boss/azhdaha/p/elspike/vis
