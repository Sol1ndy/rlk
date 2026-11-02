# The rig looks of the current phase (reload, phase steps, tests; @s = body).
execute if score #ph kn matches ..4 run function rlk:boss/arlecchino/rig_stub/look/form/p1
execute if score #ph kn matches 5.. run function rlk:boss/arlecchino/rig_stub/look/form/p2
function rlk:boss/arlecchino/rig_stub/look/props/none
function rlk:boss/arlecchino/rig_stub/state/normal
function rlk:boss/arlecchino/core/looks_rest
