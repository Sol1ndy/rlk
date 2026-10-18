# recover: 15 t, then idle_cruise. @s = rig anchor.
execute if score @s fgRigT matches 15.. run return run function rlk:mboss/fieldgen/rig/start/idle_cruise
execute if score @s fgRigT matches ..7 run return run function rlk:mboss/fieldgen/rig/c/recover/b/0_7
function rlk:mboss/fieldgen/rig/c/recover/b/9_14
