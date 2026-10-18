# warp_in_field: 24 t, then field_idle. @s = rig anchor.
execute if score @s fgRigT matches 24.. run return run function rlk:mboss/fieldgen/rig/start/field_idle
execute if score @s fgRigT matches ..14 run return run function rlk:mboss/fieldgen/rig/c/warp_in_field/b/0_14
function rlk:mboss/fieldgen/rig/c/warp_in_field/b/15_23
