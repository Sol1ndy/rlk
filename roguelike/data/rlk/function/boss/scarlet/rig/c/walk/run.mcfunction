# walk: 24 t, loops 0-24. @s = rig anchor.
execute if score @s hrRigT matches 24.. run scoreboard players set @s hrRigT 0
execute if score @s hrRigT matches ..8 run return run function rlk:boss/scarlet/rig/c/walk/b/0_8
execute if score @s hrRigT matches ..16 run return run function rlk:boss/scarlet/rig/c/walk/b/9_16
execute if score @s hrRigT matches ..23 run return run function rlk:boss/scarlet/rig/c/walk/b/17_23
