# g_drop: 14 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 15.. run return run scoreboard players set @s hrRigT 15
execute if score @s hrRigT matches ..9 run return run function rlk:boss/scarlet/rig/c/g_drop/b/0_9
execute if score @s hrRigT matches ..13 run return run function rlk:boss/scarlet/rig/c/g_drop/b/10_13
