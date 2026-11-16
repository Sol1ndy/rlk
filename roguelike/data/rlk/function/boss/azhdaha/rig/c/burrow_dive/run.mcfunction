# burrow_dive: 40 t, then burrow_travel. @s = rig anchor.
execute if score @s azRigT matches 40.. run return run function rlk:boss/azhdaha/rig/start/burrow_travel
execute if score @s azRigT matches ..20 run return run function rlk:boss/azhdaha/rig/c/burrow_dive/b/0_20
function rlk:boss/azhdaha/rig/c/burrow_dive/b/21_39
