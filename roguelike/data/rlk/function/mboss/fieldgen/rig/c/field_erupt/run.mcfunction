# field_erupt: 40 t, then field_idle. @s = rig anchor.
execute if score @s fgRigT matches 40.. run return run function rlk:mboss/fieldgen/rig/start/field_idle
execute if score @s fgRigT matches ..21 run return run function rlk:mboss/fieldgen/rig/c/field_erupt/b/0_21
function rlk:mboss/fieldgen/rig/c/field_erupt/b/22_40
