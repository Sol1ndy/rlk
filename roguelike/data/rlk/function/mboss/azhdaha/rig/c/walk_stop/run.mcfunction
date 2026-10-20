# walk_stop: 16 t, then idle. @s = rig anchor.
execute if score @s azRigT matches 16.. run return run function rlk:mboss/azhdaha/rig/start/idle
execute if score @s azRigT matches ..8 run return run function rlk:mboss/azhdaha/rig/c/walk_stop/b/0_8
function rlk:mboss/azhdaha/rig/c/walk_stop/b/9_15
