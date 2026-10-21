# combo_end: 20 t, then idle_p1. @s = rig anchor.
execute if score @s apRigT matches 20.. run return run function rlk:mboss/apep/rig/start/idle_p1
execute if score @s apRigT matches 0 run return run function rlk:mboss/apep/rig/c/combo_end/k/0
execute if score @s apRigT matches 10 run return run function rlk:mboss/apep/rig/c/combo_end/k/10
execute if score @s apRigT matches 11 run return run function rlk:mboss/apep/rig/c/combo_end/k/11
