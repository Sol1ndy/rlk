# intro_end: 150 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 151.. run return run scoreboard players set @s hrRigT 151
execute if score @s hrRigT matches ..47 run return run function rlk:boss/scarlet/rig/c/intro_end/b/0_47
execute if score @s hrRigT matches ..60 run return run function rlk:boss/scarlet/rig/c/intro_end/b/48_60
execute if score @s hrRigT matches ..130 run return run function rlk:boss/scarlet/rig/c/intro_end/b/64_130
