# sweep_e: 50 t, then idle. @s = rig anchor.
execute if score @s gdRigT matches 50.. run return run function rlk:mboss/guardian/rig/start/idle
execute if score @s gdRigT matches ..25 run return run function rlk:mboss/guardian/rig/c/sweep_e/b/0_25
function rlk:mboss/guardian/rig/c/sweep_e/b/26_50
