# cast: 20 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 21.. run return run scoreboard players set @s rdRigT 21
execute if score @s rdRigT matches 0 run return run function rlk:boss/raiden/rig/c/cast/k/0
execute if score @s rdRigT matches 4 run return run function rlk:boss/raiden/rig/c/cast/k/4
execute if score @s rdRigT matches 8 run return run function rlk:boss/raiden/rig/c/cast/k/8
execute if score @s rdRigT matches 14 run return run function rlk:boss/raiden/rig/c/cast/k/14
execute if score @s rdRigT matches 17 run return run function rlk:boss/raiden/rig/c/cast/k/17
