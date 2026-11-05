# The rig looks the module owns (form, phase, blade, state) for the current phase (@s = body; reload, tests).
function rlk:boss/scarlet/rig/look/form/normal
execute if score #ph hr matches ..1 run function rlk:boss/scarlet/rig/look/phase/p1
execute if score #ph hr matches 2.. run function rlk:boss/scarlet/rig/look/phase/p2
function rlk:boss/scarlet/rig/look/blade/off
function rlk:boss/scarlet/rig/state/normal
