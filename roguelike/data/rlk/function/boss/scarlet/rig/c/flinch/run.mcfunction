# flinch: 6 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 7.. run return run scoreboard players set @s hrRigT 7
execute if score @s hrRigT matches 0 run return run function rlk:boss/scarlet/rig/c/flinch/k/0
execute if score @s hrRigT matches 3 run return run function rlk:boss/scarlet/rig/c/flinch/k/3
execute if score @s hrRigT matches 4 run return run function rlk:boss/scarlet/rig/c/flinch/k/4
execute if score @s hrRigT matches 5 run return run function rlk:boss/scarlet/rig/c/flinch/k/5
