# repel: 104 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 105.. run return run scoreboard players set @s hrRigT 105
execute if score @s hrRigT matches 0 run return run function rlk:boss/scarlet/rig/c/repel/k/0
