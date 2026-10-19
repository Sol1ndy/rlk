# crawl_stop_p1: 32 t, then idle_p1. @s = rig anchor.
execute if score @s apRigT matches 32.. run return run function rlk:mboss/apep/rig/start/idle_p1
execute if score @s apRigT matches 0 run return run function rlk:mboss/apep/rig/c/crawl_stop_p1/k/0
execute if score @s apRigT matches 7 run return run function rlk:mboss/apep/rig/c/crawl_stop_p1/k/7
execute if score @s apRigT matches 8 run return run function rlk:mboss/apep/rig/c/crawl_stop_p1/k/8
execute if score @s apRigT matches 10 run return run function rlk:mboss/apep/rig/c/crawl_stop_p1/k/10
