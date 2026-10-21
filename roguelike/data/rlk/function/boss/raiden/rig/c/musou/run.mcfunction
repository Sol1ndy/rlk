# musou: 166 t, holds the last pose. @s = rig anchor.
execute if score @s rdRigT matches 167.. run return run scoreboard players set @s rdRigT 167
execute if score @s rdRigT matches ..10 run return run function rlk:boss/raiden/rig/c/musou/b/0_10
execute if score @s rdRigT matches ..126 run return run function rlk:boss/raiden/rig/c/musou/b/20_126
execute if score @s rdRigT matches ..165 run return run function rlk:boss/raiden/rig/c/musou/b/129_165
