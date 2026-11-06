# t_reform: 20 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 21.. run return run scoreboard players set @s rdRigT 21
execute if score @s rdRigT matches 0 run return run function rlk:boss/raiden/rig/c/t_reform/k/0
execute if score @s rdRigT matches 3 run return run function rlk:boss/raiden/rig/c/t_reform/k/3
execute if score @s rdRigT matches 6 run return run function rlk:boss/raiden/rig/c/t_reform/k/6
