# tail_p1x2: 127 t, then idle_p1. @s = rig anchor.
execute if score @s apRigT matches 127.. run return run function rlk:mboss/apep/rig/start/idle_p1
execute if score @s apRigT matches ..59 run return run function rlk:mboss/apep/rig/c/tail_p1x2/b/0_59
function rlk:mboss/apep/rig/c/tail_p1x2/b/60_126
