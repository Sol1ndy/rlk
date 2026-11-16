# wave: 40 t, then field_idle. @s = rig anchor.
execute if score @s fgRigT matches 40.. run return run function rlk:mboss/fieldgen/rig/start/field_idle
execute if score @s fgRigT matches ..15 run return run function rlk:mboss/fieldgen/rig/c/wave/b/0_15
function rlk:mboss/fieldgen/rig/c/wave/b/16_39
