# g_deflect: 12 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 13.. run return run scoreboard players set @s hrRigT 13
execute if score @s hrRigT matches ..5 run return run function rlk:boss/scarlet/rig/c/g_deflect/b/0_5
execute if score @s hrRigT matches ..11 run return run function rlk:boss/scarlet/rig/c/g_deflect/b/6_11
