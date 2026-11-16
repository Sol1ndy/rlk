# idle_dormant: 40 t, loop. @s = rig anchor.
execute if score @s fgRigT matches 40.. run scoreboard players set @s fgRigT 0
execute if score @s fgRigT matches 0 run return run function rlk:mboss/fieldgen/rig/c/idle_dormant/k/0
