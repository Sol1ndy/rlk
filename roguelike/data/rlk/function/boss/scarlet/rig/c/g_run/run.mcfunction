# g_run: 14 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 15.. run return run scoreboard players set @s hrRigT 15
execute if score @s hrRigT matches ..6 run return run function rlk:boss/scarlet/rig/c/g_run/b/0_6
execute if score @s hrRigT matches ..12 run return run function rlk:boss/scarlet/rig/c/g_run/b/7_12
