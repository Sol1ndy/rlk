# g_vert: 20 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 21.. run return run scoreboard players set @s hrRigT 21
execute if score @s hrRigT matches ..7 run return run function rlk:boss/scarlet/rig/c/g_vert/b/0_7
execute if score @s hrRigT matches ..14 run return run function rlk:boss/scarlet/rig/c/g_vert/b/8_14
execute if score @s hrRigT matches ..19 run return run function rlk:boss/scarlet/rig/c/g_vert/b/15_19
