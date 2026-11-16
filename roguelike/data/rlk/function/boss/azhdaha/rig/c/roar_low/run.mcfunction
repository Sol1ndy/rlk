# roar_low: 40 t, then idle. @s = rig anchor.
execute if score @s azRigT matches 40.. run return run function rlk:boss/azhdaha/rig/start/idle
execute if score @s azRigT matches ..20 run return run function rlk:boss/azhdaha/rig/c/roar_low/b/0_20
function rlk:boss/azhdaha/rig/c/roar_low/b/21_39
