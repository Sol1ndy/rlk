# ending: 1042 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 1043.. run return run scoreboard players set @s hrRigT 1043
execute if score @s hrRigT matches 0 run return run function rlk:boss/scarlet/rig/c/ending/k/0
