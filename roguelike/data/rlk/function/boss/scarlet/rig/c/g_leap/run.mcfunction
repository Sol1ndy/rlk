# g_leap: 18 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 19.. run return run scoreboard players set @s hrRigT 19
execute if score @s hrRigT matches ..9 run return run function rlk:boss/scarlet/rig/c/g_leap/b/0_9
execute if score @s hrRigT matches ..17 run return run function rlk:boss/scarlet/rig/c/g_leap/b/10_17
