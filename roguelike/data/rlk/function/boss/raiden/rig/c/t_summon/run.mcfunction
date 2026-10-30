# t_summon: 24 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 25.. run return run scoreboard players set @s rdRigT 25
execute if score @s rdRigT matches 0 run return run function rlk:boss/raiden/rig/c/t_summon/k/0
execute if score @s rdRigT matches 4 run return run function rlk:boss/raiden/rig/c/t_summon/k/4
execute if score @s rdRigT matches 12 run return run function rlk:boss/raiden/rig/c/t_summon/k/12
execute if score @s rdRigT matches 14 run return run function rlk:boss/raiden/rig/c/t_summon/k/14
