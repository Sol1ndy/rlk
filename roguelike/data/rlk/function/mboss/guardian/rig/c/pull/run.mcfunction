# pull: 40 t, then idle. @s = rig anchor.
execute if score @s gdRigT matches 40.. run return run function rlk:mboss/guardian/rig/start/idle
execute if score @s gdRigT matches ..20 run return run function rlk:mboss/guardian/rig/c/pull/b/0_20
function rlk:mboss/guardian/rig/c/pull/b/21_40
