# g_dive: 10 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 11.. run return run scoreboard players set @s hrRigT 11
execute if score @s hrRigT matches ..4 run return run function rlk:boss/scarlet/rig/c/g_dive/b/0_4
execute if score @s hrRigT matches ..9 run return run function rlk:boss/scarlet/rig/c/g_dive/b/5_9
