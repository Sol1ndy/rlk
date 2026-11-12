# g_x: 16 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 17.. run return run scoreboard players set @s hrRigT 17
execute if score @s hrRigT matches ..6 run return run function rlk:boss/scarlet/rig/c/g_x/b/0_6
execute if score @s hrRigT matches ..15 run return run function rlk:boss/scarlet/rig/c/g_x/b/7_15
