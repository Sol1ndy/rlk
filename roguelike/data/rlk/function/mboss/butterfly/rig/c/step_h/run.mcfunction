# step_h: 16 t, loop. @s = rig anchor.
execute if score @s bfRigT matches 16.. run scoreboard players set @s bfRigT 0
execute if score @s bfRigT matches ..8 run return run function rlk:mboss/butterfly/rig/c/step_h/b/0_8
function rlk:mboss/butterfly/rig/c/step_h/b/9_15
