# t_vanish: 14 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 15.. run return run scoreboard players set @s rdRigT 15
execute if score @s rdRigT matches 0 run return run function rlk:boss/raiden/rig/c/t_vanish/k/0
execute if score @s rdRigT matches 8 run return run function rlk:boss/raiden/rig/c/t_vanish/k/8
execute if score @s rdRigT matches 11 run return run function rlk:boss/raiden/rig/c/t_vanish/k/11
