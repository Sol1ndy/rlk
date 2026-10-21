# turn_p1_step: 10 t, then idle_p1. @s = rig anchor.
execute if score @s apRigT matches 10.. run return run function rlk:mboss/apep/rig/start/idle_p1
execute if score @s apRigT matches ..4 run return run function rlk:mboss/apep/rig/c/turn_p1_step/b/0_4
function rlk:mboss/apep/rig/c/turn_p1_step/b/5_9
