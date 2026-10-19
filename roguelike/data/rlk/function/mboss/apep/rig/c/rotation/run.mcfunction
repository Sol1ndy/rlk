# rotation: 130 t, then idle_p1. @s = rig anchor.
execute if score @s apRigT matches 130.. run return run function rlk:mboss/apep/rig/start/idle_p1
execute if score @s apRigT matches 0 run return run function rlk:mboss/apep/rig/c/rotation/k/0
