# charge_stop: 21 t, then idle. @s = rig anchor.
execute if score @s azRigT matches 21.. run return run function rlk:mboss/azhdaha/rig/start/idle
execute if score @s azRigT matches ..10 run return run function rlk:mboss/azhdaha/rig/c/charge_stop/b/0_10
function rlk:mboss/azhdaha/rig/c/charge_stop/b/11_20
