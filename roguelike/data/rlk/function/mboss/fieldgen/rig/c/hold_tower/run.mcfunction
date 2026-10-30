# hold_tower: 80 t, loop. @s = rig anchor.
execute if score @s fgRigT matches 80.. run scoreboard players set @s fgRigT 0
execute if score @s fgRigT matches ..45 run return run function rlk:mboss/fieldgen/rig/c/hold_tower/b/0_45
function rlk:mboss/fieldgen/rig/c/hold_tower/b/48_79
