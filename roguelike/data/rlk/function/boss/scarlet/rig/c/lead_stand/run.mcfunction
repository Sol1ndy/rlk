# lead_stand: 70 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 71.. run return run scoreboard players set @s hrRigT 71
execute if score @s hrRigT matches 0 run return run function rlk:boss/scarlet/rig/c/lead_stand/k/0
