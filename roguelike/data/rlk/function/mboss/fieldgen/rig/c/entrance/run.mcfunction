# entrance: 110 t, then idle_cruise. @s = rig anchor.
execute if score @s fgRigT matches 110.. run return run function rlk:mboss/fieldgen/rig/start/idle_cruise
execute if score @s fgRigT matches ..52 run return run function rlk:mboss/fieldgen/rig/c/entrance/b/0_52
function rlk:mboss/fieldgen/rig/c/entrance/b/53_109
