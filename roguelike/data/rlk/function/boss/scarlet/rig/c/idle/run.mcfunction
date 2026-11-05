# idle: 40 t, loops 0-40. @s = rig anchor.
execute if score @s hrRigT matches 40.. run scoreboard players set @s hrRigT 0
execute if score @s hrRigT matches ..12 run return run function rlk:boss/scarlet/rig/c/idle/b/0_12
execute if score @s hrRigT matches ..25 run return run function rlk:boss/scarlet/rig/c/idle/b/14_25
execute if score @s hrRigT matches ..37 run return run function rlk:boss/scarlet/rig/c/idle/b/26_37
