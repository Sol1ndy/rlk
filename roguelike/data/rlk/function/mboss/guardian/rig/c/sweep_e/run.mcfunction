# sweep_e: 45 t, then idle. @s = rig anchor.
execute if score @s gdRigT matches 45.. run return run function rlk:mboss/guardian/rig/start/idle
execute if score @s gdRigT matches ..23 run return run function rlk:mboss/guardian/rig/c/sweep_e/b/0_23
function rlk:mboss/guardian/rig/c/sweep_e/b/24_45
