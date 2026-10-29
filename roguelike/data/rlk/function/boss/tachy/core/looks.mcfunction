# The rig looks of the current state (reload, phase steps, tests; @s = body).
execute if score #ph tk matches 0..2 run function rlk:boss/tachy/rig_stub/look/form/cape
execute if score #ph tk matches 3..5 run function rlk:boss/tachy/rig_stub/look/form/winged
execute if score #ph tk matches 6..8 run function rlk:boss/tachy/rig_stub/look/form/abyss
function rlk:boss/tachy/el/visor
function rlk:boss/tachy/el/edge
function rlk:boss/tachy/rig_stub/look/chest/off
function rlk:boss/tachy/rig_stub/look/hands/grip
function rlk:boss/tachy/rig_stub/state/normal
