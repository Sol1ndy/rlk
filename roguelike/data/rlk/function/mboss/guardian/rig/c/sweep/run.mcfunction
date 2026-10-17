# sweep: 44 t, then idle. @s = rig anchor.
execute if score @s gdRigT matches 44.. run return run function rlk:mboss/guardian/rig/start/idle
execute if score @s gdRigT matches ..22 run return run function rlk:mboss/guardian/rig/c/sweep/b/0_22
function rlk:mboss/guardian/rig/c/sweep/b/23_43
