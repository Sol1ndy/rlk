# exhausted: 60 t, loop. @s = rig anchor.
execute if score @s rdRigT matches 60.. run scoreboard players set @s rdRigT 0
execute if score @s rdRigT matches 0 run return run function rlk:boss/raiden/rig/c/exhausted/k/0
execute if score @s rdRigT matches 15 run return run function rlk:boss/raiden/rig/c/exhausted/k/15
execute if score @s rdRigT matches 30 run return run function rlk:boss/raiden/rig/c/exhausted/k/30
execute if score @s rdRigT matches 45 run return run function rlk:boss/raiden/rig/c/exhausted/k/45
