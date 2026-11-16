# hold_deployed: 80 t, loop. @s = rig anchor.
execute if score @s fgRigT matches 80.. run scoreboard players set @s fgRigT 0
execute if score @s fgRigT matches ..40 run return run function rlk:mboss/fieldgen/rig/c/hold_deployed/b/0_40
function rlk:mboss/fieldgen/rig/c/hold_deployed/b/48_79
