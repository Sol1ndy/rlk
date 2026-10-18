# hold_laser: 72 t, loop. @s = rig anchor.
execute if score @s fgRigT matches 72.. run scoreboard players set @s fgRigT 0
execute if score @s fgRigT matches ..36 run return run function rlk:mboss/fieldgen/rig/c/hold_laser/b/0_36
function rlk:mboss/fieldgen/rig/c/hold_laser/b/38_71
