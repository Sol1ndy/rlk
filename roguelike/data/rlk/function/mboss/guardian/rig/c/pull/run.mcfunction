# pull: 32 t, then idle. @s = rig anchor.
execute if score @s gdRigT matches 32.. run return run function rlk:mboss/guardian/rig/start/idle
execute if score @s gdRigT matches ..16 run return run function rlk:mboss/guardian/rig/c/pull/b/0_16
function rlk:mboss/guardian/rig/c/pull/b/17_32
