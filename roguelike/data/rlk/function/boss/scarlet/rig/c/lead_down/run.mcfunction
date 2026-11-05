# lead_down: 82 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 83.. run return run scoreboard players set @s hrRigT 83
execute if score @s hrRigT matches 0 run return run function rlk:boss/scarlet/rig/c/lead_down/k/0
