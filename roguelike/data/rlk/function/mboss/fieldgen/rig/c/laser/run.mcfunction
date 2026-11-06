# laser: 165 t, then idle_cruise. @s = rig anchor.
execute if score @s fgRigT matches 165.. run return run function rlk:mboss/fieldgen/rig/start/idle_cruise
execute if score @s fgRigT matches ..84 run return run function rlk:mboss/fieldgen/rig/c/laser/b/0_84
function rlk:mboss/fieldgen/rig/c/laser/b/85_164
