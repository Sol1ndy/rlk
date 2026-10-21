# p_rear: 36 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 37.. run return run scoreboard players set @s rdRigT 37
execute if score @s rdRigT matches ..16 run return run function rlk:boss/raiden/rig/c/p_rear/b/0_16
execute if score @s rdRigT matches ..35 run return run function rlk:boss/raiden/rig/c/p_rear/b/18_35
