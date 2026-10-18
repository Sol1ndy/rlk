# missiles: 64 t, then idle_cruise. @s = rig anchor.
execute if score @s fgRigT matches 64.. run return run function rlk:mboss/fieldgen/rig/start/idle_cruise
execute if score @s fgRigT matches ..36 run return run function rlk:mboss/fieldgen/rig/c/missiles/b/0_36
function rlk:mboss/fieldgen/rig/c/missiles/b/37_63
