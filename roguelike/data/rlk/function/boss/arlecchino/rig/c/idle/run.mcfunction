# idle: 40 t, loops 0-40. @s = rig anchor.
execute if score @s knRigT matches 40.. run scoreboard players set @s knRigT 0
execute if score @s knRigT matches ..26 run return run function rlk:boss/arlecchino/rig/c/idle/b/0_26
execute if score @s knRigT matches ..38 run return run function rlk:boss/arlecchino/rig/c/idle/b/31_38
