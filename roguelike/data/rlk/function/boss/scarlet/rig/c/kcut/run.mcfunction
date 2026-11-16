# kcut: 50 t, holds the last pose. @s = rig anchor.
execute if score @s hrRigT matches 51.. run return run scoreboard players set @s hrRigT 51
execute if score @s hrRigT matches ..10 run return run function rlk:boss/scarlet/rig/c/kcut/b/0_10
execute if score @s hrRigT matches ..19 run return run function rlk:boss/scarlet/rig/c/kcut/b/12_19
execute if score @s hrRigT matches ..27 run return run function rlk:boss/scarlet/rig/c/kcut/b/20_27
execute if score @s hrRigT matches ..35 run return run function rlk:boss/scarlet/rig/c/kcut/b/28_35
execute if score @s hrRigT matches ..43 run return run function rlk:boss/scarlet/rig/c/kcut/b/36_43
execute if score @s hrRigT matches ..49 run return run function rlk:boss/scarlet/rig/c/kcut/b/44_49
