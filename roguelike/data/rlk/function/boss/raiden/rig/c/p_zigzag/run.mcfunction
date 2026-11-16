# p_zigzag: 64 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 65.. run return run scoreboard players set @s rdRigT 65
execute if score @s rdRigT matches ..31 run return run function rlk:boss/raiden/rig/c/p_zigzag/b/0_31
execute if score @s rdRigT matches ..41 run return run function rlk:boss/raiden/rig/c/p_zigzag/b/32_41
execute if score @s rdRigT matches ..63 run return run function rlk:boss/raiden/rig/c/p_zigzag/b/47_63
