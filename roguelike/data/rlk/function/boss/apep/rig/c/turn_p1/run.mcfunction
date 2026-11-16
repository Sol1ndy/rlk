# turn_p1: 20 t, loop. @s = rig anchor.
execute if score @s apRigT matches 20.. run scoreboard players set @s apRigT 0
execute if score @s apRigT matches ..9 run return run function rlk:boss/apep/rig/c/turn_p1/b/0_9
function rlk:boss/apep/rig/c/turn_p1/b/10_19
