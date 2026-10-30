# t_waves: 70 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 71.. run return run scoreboard players set @s rdRigT 71
execute if score @s rdRigT matches ..8 run return run function rlk:boss/raiden/rig/c/t_waves/b/0_8
execute if score @s rdRigT matches ..24 run return run function rlk:boss/raiden/rig/c/t_waves/b/18_24
execute if score @s rdRigT matches ..40 run return run function rlk:boss/raiden/rig/c/t_waves/b/25_40
execute if score @s rdRigT matches ..62 run return run function rlk:boss/raiden/rig/c/t_waves/b/48_62
