# strafe_r: 20 t, loops 0-20. @s = rig anchor.
execute if score @s hrRigT matches 20.. run scoreboard players set @s hrRigT 0
execute if score @s hrRigT matches ..7 run return run function rlk:boss/scarlet/rig/c/strafe_r/b/0_7
execute if score @s hrRigT matches ..14 run return run function rlk:boss/scarlet/rig/c/strafe_r/b/8_14
execute if score @s hrRigT matches ..19 run return run function rlk:boss/scarlet/rig/c/strafe_r/b/15_19
