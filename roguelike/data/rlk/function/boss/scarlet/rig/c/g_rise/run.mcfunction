# g_rise: 14 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 15.. run return run scoreboard players set @s hrRigT 15
execute if score @s hrRigT matches ..7 run return run function rlk:boss/scarlet/rig/c/g_rise/b/0_7
execute if score @s hrRigT matches ..13 run return run function rlk:boss/scarlet/rig/c/g_rise/b/8_13
