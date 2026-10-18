# field_idle: 240 t, loop. @s = rig anchor.
execute if score @s fgRigT matches 240.. run scoreboard players set @s fgRigT 0
execute if score @s fgRigT matches ..120 run return run function rlk:mboss/fieldgen/rig/c/field_idle/b/0_120
function rlk:mboss/fieldgen/rig/c/field_idle/b/122_239
