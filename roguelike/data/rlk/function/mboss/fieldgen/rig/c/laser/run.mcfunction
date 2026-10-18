# laser: 175 t, then idle_cruise. @s = rig anchor.
execute if score @s fgRigT matches 175.. run return run function rlk:mboss/fieldgen/rig/start/idle_cruise
execute if score @s fgRigT matches ..93 run return run function rlk:mboss/fieldgen/rig/c/laser/b/0_93
function rlk:mboss/fieldgen/rig/c/laser/b/95_174
