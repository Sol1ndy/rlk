# stagger: 60 t, loops 20-60. @s = rig anchor.
execute if score @s rdRigT matches 60.. run scoreboard players set @s rdRigT 20
execute if score @s rdRigT matches 0 run return run function rlk:boss/raiden/rig/c/stagger/k/0
execute if score @s rdRigT matches 4 run return run function rlk:boss/raiden/rig/c/stagger/k/4
execute if score @s rdRigT matches 6 run return run function rlk:boss/raiden/rig/c/stagger/k/6
execute if score @s rdRigT matches 8 run return run function rlk:boss/raiden/rig/c/stagger/k/8
execute if score @s rdRigT matches 9 run return run function rlk:boss/raiden/rig/c/stagger/k/9
execute if score @s rdRigT matches 12 run return run function rlk:boss/raiden/rig/c/stagger/k/12
execute if score @s rdRigT matches 20 run return run function rlk:boss/raiden/rig/c/stagger/k/20
execute if score @s rdRigT matches 40 run return run function rlk:boss/raiden/rig/c/stagger/k/40
