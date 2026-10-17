# pose_ref: 20 t, loop. @s = rig anchor.
execute if score @s gdRigT matches 20.. run scoreboard players set @s gdRigT 0
execute if score @s gdRigT matches ..10 run return run function rlk:mboss/guardian/rig/c/pose_ref/b/0_10
function rlk:mboss/guardian/rig/c/pose_ref/b/11_17
