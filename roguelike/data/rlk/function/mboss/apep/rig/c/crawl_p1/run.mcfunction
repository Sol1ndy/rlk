# crawl_p1: 16 t, loop. @s = rig anchor.
execute if score @s apRigT matches 16.. run scoreboard players set @s apRigT 0
execute if score @s apRigT matches 0 run return run function rlk:mboss/apep/rig/c/crawl_p1/k/0
execute if score @s apRigT matches 3 run return run function rlk:mboss/apep/rig/c/crawl_p1/k/3
execute if score @s apRigT matches 7 run return run function rlk:mboss/apep/rig/c/crawl_p1/k/7
execute if score @s apRigT matches 8 run return run function rlk:mboss/apep/rig/c/crawl_p1/k/8
execute if score @s apRigT matches 10 run return run function rlk:mboss/apep/rig/c/crawl_p1/k/10
