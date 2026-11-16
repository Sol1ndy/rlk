# sweep: 39 t, then idle. @s = rig anchor.
execute if score @s gdRigT matches 39.. run return run function rlk:mboss/guardian/rig/start/idle
execute if score @s gdRigT matches ..19 run return run function rlk:mboss/guardian/rig/c/sweep/b/0_19
function rlk:mboss/guardian/rig/c/sweep/b/20_38
