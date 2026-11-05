# cs1: 213 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 214.. run return run scoreboard players set @s hrRigT 214
execute if score @s hrRigT matches 0 run return run function rlk:boss/scarlet/rig/c/cs1/k/0
