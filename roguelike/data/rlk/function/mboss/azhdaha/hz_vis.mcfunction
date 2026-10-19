# Hook hz_vis (@s = hazard marker, #hzEv 0 create / 1 strike / 2 end): routed by mbHzV / 10 = the pattern id.
scoreboard players operation #azV mb = @s mbHzV
scoreboard players operation #azV mb /= #c10 mb
