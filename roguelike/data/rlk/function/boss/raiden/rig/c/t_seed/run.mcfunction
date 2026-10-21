# t_seed: 20 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 21.. run return run scoreboard players set @s rdRigT 21
execute if score @s rdRigT matches 0 run return run function rlk:boss/raiden/rig/c/t_seed/k/0
execute if score @s rdRigT matches 5 run return run function rlk:boss/raiden/rig/c/t_seed/k/5
execute if score @s rdRigT matches 7 run return run function rlk:boss/raiden/rig/c/t_seed/k/7
