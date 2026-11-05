# a2: 30 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 31.. run return run scoreboard players set @s hrRigT 31
execute if score @s hrRigT matches ..7 run return run function rlk:boss/scarlet/rig/c/a2/b/0_7
execute if score @s hrRigT matches ..15 run return run function rlk:boss/scarlet/rig/c/a2/b/8_15
execute if score @s hrRigT matches ..23 run return run function rlk:boss/scarlet/rig/c/a2/b/16_23
execute if score @s hrRigT matches ..29 run return run function rlk:boss/scarlet/rig/c/a2/b/24_29
