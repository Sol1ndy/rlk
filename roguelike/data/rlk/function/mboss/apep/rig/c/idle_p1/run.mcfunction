# idle_p1: 60 t, loop. @s = rig anchor.
execute if score @s apRigT matches 60.. run scoreboard players set @s apRigT 0
execute if score @s apRigT matches 0 run return run function rlk:mboss/apep/rig/c/idle_p1/k/0
