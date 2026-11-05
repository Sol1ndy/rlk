# g_wrap: 12 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 13.. run return run scoreboard players set @s hrRigT 13
execute if score @s hrRigT matches ..4 run return run function rlk:boss/scarlet/rig/c/g_wrap/b/0_4
execute if score @s hrRigT matches ..8 run return run function rlk:boss/scarlet/rig/c/g_wrap/b/5_8
