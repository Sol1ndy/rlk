# idle: 40 t, loop. @s = rig anchor.
execute if score @s gdRigT matches 40.. run scoreboard players set @s gdRigT 0
execute if score @s gdRigT matches ..20 run return run function rlk:mboss/guardian/rig/c/idle/b/0_20
function rlk:mboss/guardian/rig/c/idle/b/21_39
