# recover: 28 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 29.. run return run scoreboard players set @s rdRigT 29
execute if score @s rdRigT matches 0 run return run function rlk:boss/raiden/rig/c/recover/k/0
execute if score @s rdRigT matches 8 run return run function rlk:boss/raiden/rig/c/recover/k/8
execute if score @s rdRigT matches 16 run return run function rlk:boss/raiden/rig/c/recover/k/16
