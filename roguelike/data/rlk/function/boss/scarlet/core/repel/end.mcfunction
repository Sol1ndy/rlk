# The counter cinematic ended (@s = body): cine off; CS2 -> the down window; CS3 -> the lethal true hit if its kick did
# not land (it normally kills at 102: death_start took over before this).
function rlk:mboss/cine/end
execute if score #ph hr matches 10 run return run function rlk:boss/scarlet/core/kill
function rlk:boss/scarlet/core/down/start
