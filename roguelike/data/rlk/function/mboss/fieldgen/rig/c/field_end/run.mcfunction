# field_end: 70 t, then idle_cruise. @s = rig anchor.
execute if score @s fgRigT matches 70.. run return run function rlk:mboss/fieldgen/rig/start/idle_cruise
execute if score @s fgRigT matches ..38 run return run function rlk:mboss/fieldgen/rig/c/field_end/b/0_38
function rlk:mboss/fieldgen/rig/c/field_end/b/39_70
