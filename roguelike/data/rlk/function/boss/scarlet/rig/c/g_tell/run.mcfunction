# g_tell: 12 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 13.. run return run scoreboard players set @s hrRigT 13
execute if score @s hrRigT matches 0 run return run function rlk:boss/scarlet/rig/c/g_tell/k/0
execute if score @s hrRigT matches 3 run return run function rlk:boss/scarlet/rig/c/g_tell/k/3
execute if score @s hrRigT matches 4 run return run function rlk:boss/scarlet/rig/c/g_tell/k/4
execute if score @s hrRigT matches 5 run return run function rlk:boss/scarlet/rig/c/g_tell/k/5
