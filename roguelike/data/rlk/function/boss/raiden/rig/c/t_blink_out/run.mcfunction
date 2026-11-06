# t_blink_out: 6 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 7.. run return run scoreboard players set @s rdRigT 7
execute if score @s rdRigT matches 0 run return run function rlk:boss/raiden/rig/c/t_blink_out/k/0
execute if score @s rdRigT matches 3 run return run function rlk:boss/raiden/rig/c/t_blink_out/k/3
