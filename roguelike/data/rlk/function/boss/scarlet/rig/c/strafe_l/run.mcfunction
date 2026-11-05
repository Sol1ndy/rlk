# strafe_l: 20 t, loops 0-20. @s = rig anchor.
execute if score @s hrRigT matches 20.. run scoreboard players set @s hrRigT 0
execute if score @s hrRigT matches ..10 run return run function rlk:boss/scarlet/rig/c/strafe_l/b/0_10
execute if score @s hrRigT matches ..18 run return run function rlk:boss/scarlet/rig/c/strafe_l/b/11_18
