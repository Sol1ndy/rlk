# walk: 24 t, loops 0-24. @s = rig anchor.
execute if score @s hrRigT matches 24.. run scoreboard players set @s hrRigT 0
execute if score @s hrRigT matches ..9 run return run function rlk:boss/scarlet/rig/c/walk/b/0_9
execute if score @s hrRigT matches ..17 run return run function rlk:boss/scarlet/rig/c/walk/b/10_17
execute if score @s hrRigT matches ..23 run return run function rlk:boss/scarlet/rig/c/walk/b/18_23
