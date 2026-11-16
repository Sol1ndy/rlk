# disc_cast: 40 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 41.. run return run scoreboard players set @s rdRigT 41
execute if score @s rdRigT matches ..10 run return run function rlk:boss/raiden/rig/c/disc_cast/b/0_10
execute if score @s rdRigT matches ..26 run return run function rlk:boss/raiden/rig/c/disc_cast/b/12_26
execute if score @s rdRigT matches ..39 run return run function rlk:boss/raiden/rig/c/disc_cast/b/30_39
