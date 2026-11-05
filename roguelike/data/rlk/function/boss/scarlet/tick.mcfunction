# Hook tick (@s = body, at it, fight state #mbSt 1): the phase machine, then the rig tick (the shown clip tick ==
# the pattern / sequence clock).
execute if score #ph hr matches 0 run function rlk:boss/scarlet/core/intro/done
function rlk:boss/scarlet/core/fight
function rlk:boss/scarlet/rig_stub/tick
