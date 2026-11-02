# Hook tick (@s = body, at it, fight state #mbSt 1): the phase machine, then the rig tick (the shown clip tick ==
# the pattern clock #pt).
execute if score #ph kn matches 0 run function rlk:boss/arlecchino/core/intro/done
execute if score #ph kn matches 1..5 run function rlk:boss/arlecchino/core/fight
function rlk:boss/arlecchino/rig_stub/tick
