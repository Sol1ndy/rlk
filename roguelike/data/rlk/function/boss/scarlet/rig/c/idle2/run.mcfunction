# idle2: 40 t, loops 0-40. @s = rig anchor.
execute if score @s hrRigT matches 40.. run scoreboard players set @s hrRigT 0
execute if score @s hrRigT matches ..18 run return run function rlk:boss/scarlet/rig/c/idle2/b/0_18
execute if score @s hrRigT matches ..29 run return run function rlk:boss/scarlet/rig/c/idle2/b/21_29
execute if score @s hrRigT matches ..39 run return run function rlk:boss/scarlet/rig/c/idle2/b/32_39
