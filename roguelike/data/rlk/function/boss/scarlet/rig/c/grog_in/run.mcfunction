# grog_in: 12 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 13.. run return run scoreboard players set @s hrRigT 13
execute if score @s hrRigT matches 0 run return run function rlk:boss/scarlet/rig/c/grog_in/k/0
execute if score @s hrRigT matches 3 run return run function rlk:boss/scarlet/rig/c/grog_in/k/3
execute if score @s hrRigT matches 6 run return run function rlk:boss/scarlet/rig/c/grog_in/k/6
execute if score @s hrRigT matches 10 run return run function rlk:boss/scarlet/rig/c/grog_in/k/10
