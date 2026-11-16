# warp_in_field: 40 t, then field_idle. @s = rig anchor.
execute if score @s fgRigT matches 40.. run return run function rlk:mboss/fieldgen/rig/start/field_idle
execute if score @s fgRigT matches ..13 run return run function rlk:mboss/fieldgen/rig/c/warp_in_field/b/0_13
function rlk:mboss/fieldgen/rig/c/warp_in_field/b/14_39
