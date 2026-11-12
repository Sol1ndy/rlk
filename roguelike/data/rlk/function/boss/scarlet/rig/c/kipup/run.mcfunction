# kipup: 20 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 21.. run return run scoreboard players set @s hrRigT 21
execute if score @s hrRigT matches ..8 run return run function rlk:boss/scarlet/rig/c/kipup/b/0_8
execute if score @s hrRigT matches ..15 run return run function rlk:boss/scarlet/rig/c/kipup/b/9_15
execute if score @s hrRigT matches ..20 run return run function rlk:boss/scarlet/rig/c/kipup/b/16_20
