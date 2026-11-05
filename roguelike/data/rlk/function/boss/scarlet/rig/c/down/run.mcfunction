# down: 40 t, loops 0-40. @s = rig anchor.
execute if score @s hrRigT matches 40.. run scoreboard players set @s hrRigT 0
execute if score @s hrRigT matches 0 run return run function rlk:boss/scarlet/rig/c/down/k/0
execute if score @s hrRigT matches 24 run return run function rlk:boss/scarlet/rig/c/down/k/24
execute if score @s hrRigT matches 27 run return run function rlk:boss/scarlet/rig/c/down/k/27
execute if score @s hrRigT matches 35 run return run function rlk:boss/scarlet/rig/c/down/k/35
execute if score @s hrRigT matches 36 run return run function rlk:boss/scarlet/rig/c/down/k/36
