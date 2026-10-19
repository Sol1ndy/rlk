# tail_p1x2: 127 t, then idle_p1. @s = rig anchor.
execute if score @s apRigT matches 127.. run return run function rlk:mboss/apep/rig/start/idle_p1
execute if score @s apRigT matches 0 run return run function rlk:mboss/apep/rig/c/tail_p1x2/k/0
