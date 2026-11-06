# Tests: make the fight state ready for a forced step (@s = body): the intro ends, whatever runs stops (pattern,
# gauntlet, sequence, replay), cine off. Returns 1.
execute if score #mbSt mb matches 0 run function rlk:boss/scarlet/core/intro/done
function rlk:boss/scarlet/core/stop_all
function rlk:mboss/cine/end
function rlk:boss/scarlet/core/stop_move
function rlk:boss/scarlet/core/ground
scoreboard players set #lock hr 0
return 1
