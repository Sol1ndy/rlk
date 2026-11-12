# crawl_stop_p1: 32 t, then idle_p1. @s = rig anchor.
execute if score @s apRigT matches 32.. run return run function rlk:boss/apep/rig/start/idle_p1
execute if score @s apRigT matches ..16 run return run function rlk:boss/apep/rig/c/crawl_stop_p1/b/0_16
function rlk:boss/apep/rig/c/crawl_stop_p1/b/17_31
