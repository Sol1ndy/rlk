# counter_sword: 46 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 47.. run return run scoreboard players set @s rdRigT 47
execute if score @s rdRigT matches ..11 run return run function rlk:boss/raiden/rig/c/counter_sword/b/0_11
execute if score @s rdRigT matches ..25 run return run function rlk:boss/raiden/rig/c/counter_sword/b/12_25
execute if score @s rdRigT matches ..45 run return run function rlk:boss/raiden/rig/c/counter_sword/b/26_45
