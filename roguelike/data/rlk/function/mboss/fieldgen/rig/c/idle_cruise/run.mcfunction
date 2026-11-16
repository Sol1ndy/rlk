# idle_cruise: 240 t, loop. @s = rig anchor.
execute if score @s fgRigT matches 240.. run scoreboard players set @s fgRigT 0
execute if score @s fgRigT matches ..128 run return run function rlk:mboss/fieldgen/rig/c/idle_cruise/b/0_128
function rlk:mboss/fieldgen/rig/c/idle_cruise/b/130_239
