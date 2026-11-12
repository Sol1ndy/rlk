# idle2: 40 t, loops 0-40. @s = rig anchor.
execute if score @s hrRigT matches 40.. run scoreboard players set @s hrRigT 0
execute if score @s hrRigT matches ..17 run return run function rlk:boss/scarlet/rig/c/idle2/b/0_17
execute if score @s hrRigT matches ..27 run return run function rlk:boss/scarlet/rig/c/idle2/b/21_27
execute if score @s hrRigT matches ..36 run return run function rlk:boss/scarlet/rig/c/idle2/b/29_36
