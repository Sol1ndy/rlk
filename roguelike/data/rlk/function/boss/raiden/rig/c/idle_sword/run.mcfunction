# idle_sword: 40 t, loop. @s = rig anchor.
execute if score @s rdRigT matches 40.. run scoreboard players set @s rdRigT 0
execute if score @s rdRigT matches 0 run return run function rlk:boss/raiden/rig/c/idle_sword/k/0
execute if score @s rdRigT matches 10 run return run function rlk:boss/raiden/rig/c/idle_sword/k/10
execute if score @s rdRigT matches 20 run return run function rlk:boss/raiden/rig/c/idle_sword/k/20
execute if score @s rdRigT matches 30 run return run function rlk:boss/raiden/rig/c/idle_sword/k/30
