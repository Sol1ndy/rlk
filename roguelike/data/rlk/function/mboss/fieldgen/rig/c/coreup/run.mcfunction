# coreup: 130 t, then idle_cruise. @s = rig anchor.
execute if score @s fgRigT matches 130.. run return run function rlk:mboss/fieldgen/rig/start/idle_cruise
execute if score @s fgRigT matches ..64 run return run function rlk:mboss/fieldgen/rig/c/coreup/b/0_64
function rlk:mboss/fieldgen/rig/c/coreup/b/65_129
