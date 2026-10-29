# Hook tick (@s = body, at it, fight state #mbSt 1): the phase machine, then the rig tick (the shown clip tick ==
# the pattern clock #pt).
execute if score #ph tk matches 0 run function rlk:boss/tachy/core/intro/done
execute if score #ph tk matches 1..7 run function rlk:boss/tachy/core/fight
function rlk:boss/tachy/rig_stub/tick
