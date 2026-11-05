# intro_end: 86 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 87.. run return run scoreboard players set @s hrRigT 87
execute if score @s hrRigT matches 0 run return run function rlk:boss/scarlet/rig/c/intro_end/k/0
