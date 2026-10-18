# hold_deployed: 80 t, loop. @s = rig anchor.
execute if score @s fgRigT matches 80.. run scoreboard players set @s fgRigT 0
execute if score @s fgRigT matches ..41 run return run function rlk:mboss/fieldgen/rig/c/hold_deployed/b/0_41
function rlk:mboss/fieldgen/rig/c/hold_deployed/b/42_79
