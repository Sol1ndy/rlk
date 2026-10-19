# turn_p1: 20 t, loop. @s = rig anchor.
execute if score @s apRigT matches 20.. run scoreboard players set @s apRigT 0
execute if score @s apRigT matches 0 run return run function rlk:mboss/apep/rig/c/turn_p1/k/0
