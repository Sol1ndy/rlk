# lead_re: 60 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 61.. run return run scoreboard players set @s hrRigT 61
execute if score @s hrRigT matches 0 run return run function rlk:boss/scarlet/rig/c/lead_re/k/0
execute if score @s hrRigT matches 3 run return run function rlk:boss/scarlet/rig/c/lead_re/k/3
execute if score @s hrRigT matches 10 run return run function rlk:boss/scarlet/rig/c/lead_re/k/10
execute if score @s hrRigT matches 44 run return run function rlk:boss/scarlet/rig/c/lead_re/k/44
