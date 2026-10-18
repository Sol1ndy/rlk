# field_end: 102 t, then idle_cruise. @s = rig anchor.
execute if score @s fgRigT matches 102.. run return run function rlk:mboss/fieldgen/rig/start/idle_cruise
execute if score @s fgRigT matches ..51 run return run function rlk:mboss/fieldgen/rig/c/field_end/b/0_51
function rlk:mboss/fieldgen/rig/c/field_end/b/52_99
