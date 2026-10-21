# t_blink_in: 10 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 11.. run return run scoreboard players set @s rdRigT 11
execute if score @s rdRigT matches 0 run return run function rlk:boss/raiden/rig/c/t_blink_in/k/0
execute if score @s rdRigT matches 3 run return run function rlk:boss/raiden/rig/c/t_blink_in/k/3
