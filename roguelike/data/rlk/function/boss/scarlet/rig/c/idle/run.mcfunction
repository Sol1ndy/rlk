# idle: 40 t, loops 0-40. @s = rig anchor.
execute if score @s hrRigT matches 40.. run scoreboard players set @s hrRigT 0
execute if score @s hrRigT matches ..14 run return run function rlk:boss/scarlet/rig/c/idle/b/0_14
execute if score @s hrRigT matches ..27 run return run function rlk:boss/scarlet/rig/c/idle/b/15_27
execute if score @s hrRigT matches ..37 run return run function rlk:boss/scarlet/rig/c/idle/b/29_37
