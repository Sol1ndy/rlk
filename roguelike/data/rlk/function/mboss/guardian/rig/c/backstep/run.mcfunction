# backstep: 12 t, then idle. @s = rig anchor.
execute if score @s gdRigT matches 12.. run return run function rlk:mboss/guardian/rig/start/idle
execute if score @s gdRigT matches ..5 run return run function rlk:mboss/guardian/rig/c/backstep/b/0_5
function rlk:mboss/guardian/rig/c/backstep/b/6_10
