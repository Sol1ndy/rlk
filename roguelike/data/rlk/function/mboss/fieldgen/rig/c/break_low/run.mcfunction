# break_low: 40 t, then groggy. @s = rig anchor.
execute if score @s fgRigT matches 40.. run return run function rlk:mboss/fieldgen/rig/start/groggy
execute if score @s fgRigT matches ..20 run return run function rlk:mboss/fieldgen/rig/c/break_low/b/0_20
function rlk:mboss/fieldgen/rig/c/break_low/b/21_40
