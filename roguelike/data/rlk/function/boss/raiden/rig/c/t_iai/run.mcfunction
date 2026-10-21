# t_iai: 40 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 41.. run return run scoreboard players set @s rdRigT 41
execute if score @s rdRigT matches ..24 run return run function rlk:boss/raiden/rig/c/t_iai/b/0_24
execute if score @s rdRigT matches ..39 run return run function rlk:boss/raiden/rig/c/t_iai/b/25_39
