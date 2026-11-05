# intro: 554 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 555.. run return run scoreboard players set @s hrRigT 555
execute if score @s hrRigT matches 0 run return run function rlk:boss/scarlet/rig/c/intro/k/0
