# entrance: 130 t, then idle_cruise. @s = rig anchor.
execute if score @s fgRigT matches 130.. run return run function rlk:mboss/fieldgen/rig/start/idle_cruise
execute if score @s fgRigT matches ..65 run return run function rlk:mboss/fieldgen/rig/c/entrance/b/0_65
function rlk:mboss/fieldgen/rig/c/entrance/b/67_124
