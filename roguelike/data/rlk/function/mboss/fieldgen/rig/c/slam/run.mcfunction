# slam: 37 t, then idle_cruise. @s = rig anchor.
execute if score @s fgRigT matches 37.. run return run function rlk:mboss/fieldgen/rig/start/idle_cruise
execute if score @s fgRigT matches ..18 run return run function rlk:mboss/fieldgen/rig/c/slam/b/0_18
function rlk:mboss/fieldgen/rig/c/slam/b/19_36
