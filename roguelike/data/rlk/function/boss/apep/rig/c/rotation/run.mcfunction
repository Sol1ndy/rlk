# rotation: 130 t, then idle_p1. @s = rig anchor.
execute if score @s apRigT matches 130.. run return run function rlk:boss/apep/rig/start/idle_p1
execute if score @s apRigT matches ..64 run return run function rlk:boss/apep/rig/c/rotation/b/0_64
function rlk:boss/apep/rig/c/rotation/b/65_129
