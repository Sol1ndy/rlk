# guard_entry: 50 t, then guard. @s = rig anchor.
execute if score @s gdRigT matches 50.. run return run function rlk:mboss/guardian/rig/start/guard
execute if score @s gdRigT matches ..25 run return run function rlk:mboss/guardian/rig/c/guard_entry/b/0_25
function rlk:mboss/guardian/rig/c/guard_entry/b/26_49
