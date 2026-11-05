# g_dash: 12 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 13.. run return run scoreboard players set @s hrRigT 13
execute if score @s hrRigT matches ..7 run return run function rlk:boss/scarlet/rig/c/g_dash/b/0_7
execute if score @s hrRigT matches ..11 run return run function rlk:boss/scarlet/rig/c/g_dash/b/8_11
