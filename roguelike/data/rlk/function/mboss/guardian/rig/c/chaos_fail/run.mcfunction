# chaos_fail: 30 t, holds the last pose. @s = rig anchor.
execute if score @s gdRigT matches 31.. run return run scoreboard players set @s gdRigT 31
execute if score @s gdRigT matches ..14 run return run function rlk:mboss/guardian/rig/c/chaos_fail/b/0_14
function rlk:mboss/guardian/rig/c/chaos_fail/b/15_30
