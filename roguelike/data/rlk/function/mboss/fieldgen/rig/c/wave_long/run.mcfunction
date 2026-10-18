# wave_long: 56 t, then field_idle. @s = rig anchor.
execute if score @s fgRigT matches 56.. run return run function rlk:mboss/fieldgen/rig/start/field_idle
execute if score @s fgRigT matches ..24 run return run function rlk:mboss/fieldgen/rig/c/wave_long/b/0_24
function rlk:mboss/fieldgen/rig/c/wave_long/b/27_54
