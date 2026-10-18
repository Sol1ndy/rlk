# wave_drop: 84 t, then field_idle. @s = rig anchor.
execute if score @s fgRigT matches 84.. run return run function rlk:mboss/fieldgen/rig/start/field_idle
execute if score @s fgRigT matches ..42 run return run function rlk:mboss/fieldgen/rig/c/wave_drop/b/0_42
function rlk:mboss/fieldgen/rig/c/wave_drop/b/43_81
