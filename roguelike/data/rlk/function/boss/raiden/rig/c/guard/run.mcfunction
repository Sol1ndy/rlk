# guard: 20 t, loop. @s = rig anchor.
execute if score @s rdRigT matches 20.. run scoreboard players set @s rdRigT 0
execute if score @s rdRigT matches 0 run return run function rlk:boss/raiden/rig/c/guard/k/0
execute if score @s rdRigT matches 5 run return run function rlk:boss/raiden/rig/c/guard/k/5
execute if score @s rdRigT matches 10 run return run function rlk:boss/raiden/rig/c/guard/k/10
execute if score @s rdRigT matches 15 run return run function rlk:boss/raiden/rig/c/guard/k/15
