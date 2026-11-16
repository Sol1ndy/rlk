# dbg_loop: 2 t, loop. @s = rig anchor.
execute if score @s azRigT matches 2.. run scoreboard players set @s azRigT 0
execute if score @s azRigT matches 0 run return run function rlk:boss/azhdaha/rig/c/dbg_loop/k/0
