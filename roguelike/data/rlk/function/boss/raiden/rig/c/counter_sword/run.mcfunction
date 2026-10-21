# counter_sword: 46 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 47.. run return run scoreboard players set @s rdRigT 47
execute if score @s rdRigT matches ..10 run return run function rlk:boss/raiden/rig/c/counter_sword/b/0_10
execute if score @s rdRigT matches ..20 run return run function rlk:boss/raiden/rig/c/counter_sword/b/11_20
execute if score @s rdRigT matches ..37 run return run function rlk:boss/raiden/rig/c/counter_sword/b/22_37
execute if score @s rdRigT matches ..45 run return run function rlk:boss/raiden/rig/c/counter_sword/b/38_45
