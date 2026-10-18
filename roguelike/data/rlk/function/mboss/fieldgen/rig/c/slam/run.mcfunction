# slam: 45 t, then idle_cruise. @s = rig anchor.
execute if score @s fgRigT matches 45.. run return run function rlk:mboss/fieldgen/rig/start/idle_cruise
execute if score @s fgRigT matches ..25 run return run function rlk:mboss/fieldgen/rig/c/slam/b/0_25
function rlk:mboss/fieldgen/rig/c/slam/b/26_44
