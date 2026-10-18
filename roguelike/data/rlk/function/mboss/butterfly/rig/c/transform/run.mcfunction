# transform: 30 t, then idle_b. @s = rig anchor.
execute if score @s bfRigT matches 30.. run return run function rlk:mboss/butterfly/rig/start/idle_b
execute if score @s bfRigT matches ..15 run return run function rlk:mboss/butterfly/rig/c/transform/b/0_15
function rlk:mboss/butterfly/rig/c/transform/b/16_29
