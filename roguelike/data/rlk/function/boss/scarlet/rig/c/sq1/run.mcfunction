# sq1: 60 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 61.. run return run scoreboard players set @s hrRigT 61
execute if score @s hrRigT matches 0 run return run function rlk:boss/scarlet/rig/c/sq1/k/0
