# idle: 40 t, loops 0-40. @s = rig anchor.
execute if score @s hrRigT matches 40.. run scoreboard players set @s hrRigT 0
execute if score @s hrRigT matches ..13 run return run function rlk:boss/scarlet/rig/c/idle/b/0_13
execute if score @s hrRigT matches ..25 run return run function rlk:boss/scarlet/rig/c/idle/b/15_25
execute if score @s hrRigT matches ..39 run return run function rlk:boss/scarlet/rig/c/idle/b/26_39
