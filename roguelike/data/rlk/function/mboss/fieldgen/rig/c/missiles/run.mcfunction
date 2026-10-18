# missiles: 60 t, then idle_cruise. @s = rig anchor.
execute if score @s fgRigT matches 60.. run return run function rlk:mboss/fieldgen/rig/start/idle_cruise
execute if score @s fgRigT matches ..32 run return run function rlk:mboss/fieldgen/rig/c/missiles/b/0_32
function rlk:mboss/fieldgen/rig/c/missiles/b/33_59
