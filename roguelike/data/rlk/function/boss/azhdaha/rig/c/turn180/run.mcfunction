# turn180: 60 t, then idle. @s = rig anchor.
execute if score @s azRigT matches 60.. run return run function rlk:boss/azhdaha/rig/start/idle
execute if score @s azRigT matches ..30 run return run function rlk:boss/azhdaha/rig/c/turn180/b/0_30
function rlk:boss/azhdaha/rig/c/turn180/b/31_59
