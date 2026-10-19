# surface_p3: 40 t, then stand_p3. @s = rig anchor.
execute if score @s apRigT matches 40.. run return run function rlk:mboss/apep/rig/start/stand_p3
execute if score @s apRigT matches 0 run return run function rlk:mboss/apep/rig/c/surface_p3/k/0
execute if score @s apRigT matches 10 run return run function rlk:mboss/apep/rig/c/surface_p3/k/10
