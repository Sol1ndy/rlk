# crawl_stop_p1: 32 t, then idle_p1. @s = rig anchor.
execute if score @s apRigT matches 32.. run return run function rlk:mboss/apep/rig/start/idle_p1
execute if score @s apRigT matches ..15 run return run function rlk:mboss/apep/rig/c/crawl_stop_p1/b/0_15
function rlk:mboss/apep/rig/c/crawl_stop_p1/b/16_31
